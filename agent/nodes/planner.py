"""Planner Agent - Decomposes strategies into actionable tasks"""

import logging

from agent.config import settings
from agent.core.base_agent import BaseAgent
from agent.core.template_manager import prompt_templates
from agent.states import AnalysisPlan, AnalysisStrategy, HierarchicalState, SubTask

logger = logging.getLogger(__name__)


class PlannerAgent(BaseAgent):
    """
    Planner decomposes strategic plan into detailed sub-tasks

    Responsibilities:
    - Break down each strategy into specific, actionable tasks
    - Assign tasks to appropriate specialist agents
    - Define dependencies between tasks
    - Create execution order with parallel groups
    """

    def __init__(self, **kwargs):
        super().__init__(
            agent_type="planner",
            use_structured_output=True,
            output_schema=AnalysisPlan,
            **kwargs,
        )

    def execute(self, state: HierarchicalState) -> HierarchicalState:
        """Execute planner logic"""
        strategic_plan = state.strategic_plan
        dataset_profile = state.dataset_profile

        # Build context for planning
        strategies_text = "\n".join(
            [f"- {s.value.upper()}" for s in strategic_plan.strategies]
        )
        priority_order = " → ".join([s.value for s in strategic_plan.priority_order])

        # Get prompt from template
        prompt = prompt_templates.render(
            "planner/task_decomposition.jinja2",
            strategies_text=strategies_text,
            priority_order=priority_order,
            reasoning=strategic_plan.reasoning,
            n_rows=dataset_profile.n_rows,
            n_cols=dataset_profile.n_cols,
            target_column=dataset_profile.target_column,
            target_type=dataset_profile.target_type,
            n_numeric=len(dataset_profile.numeric_features),
            n_categorical=len(dataset_profile.categorical_features),
            has_missing=dataset_profile.has_missing,
            has_imbalance=dataset_profile.has_imbalance,
            estimated_tasks=min(strategic_plan.estimated_tasks, settings.max_tasks),
        )

        # Get structured plan from LLM, then check and repair it
        analysis_plan = validate_plan(self.invoke(prompt), settings.max_tasks)

        # Log the plan
        self._log_analysis_plan(analysis_plan)

        # Update state
        state.analysis_plan = analysis_plan
        state.current_phase = "execution"

        return state

    def _log_analysis_plan(self, analysis_plan: AnalysisPlan):
        """Log the analysis plan"""
        self.logger.info("=" * 60)
        self.logger.info("ANALYSIS PLAN")
        self.logger.info("=" * 60)
        self.logger.info(f"Total Tasks: {len(analysis_plan.tasks)}")

        for strategy in [
            AnalysisStrategy.EXPLORATORY,
            AnalysisStrategy.STATISTICAL,
            AnalysisStrategy.PREDICTIVE,
        ]:
            strategy_tasks = [t for t in analysis_plan.tasks if t.strategy == strategy]
            if strategy_tasks:
                self.logger.info(
                    f"\n{strategy.value.upper()} Tasks ({len(strategy_tasks)}):"
                )
                for task in strategy_tasks:
                    deps = (
                        f" [depends on: {', '.join(task.dependencies)}]"
                        if task.dependencies
                        else ""
                    )
                    self.logger.info(f"  • {task.id}: {task.description}{deps}")

        self.logger.info(
            f"\nExecution Order: {' → '.join(analysis_plan.execution_order)}"
        )
        self.logger.info("=" * 60)


def planner_node(state: HierarchicalState) -> HierarchicalState:
    """
    Planner node for graph integration

    Creates and executes planner agent.
    """
    agent = PlannerAgent()
    return agent.execute(state)


class PlanValidationError(ValueError):
    """The planner produced a plan that can't be executed"""


def validate_plan(plan: AnalysisPlan, max_tasks: int) -> AnalysisPlan:
    """
    Check and repair an LLM-produced plan, then compute its execution order

    - Duplicate task IDs and dependency cycles raise PlanValidationError
    - Only the max_tasks highest-priority tasks are kept (ties keep plan order)
    - Unknown, self, and dropped-task dependencies are removed
    """
    plan = plan.model_copy(deep=True)

    ids = [t.id for t in plan.tasks]
    duplicates = sorted({i for i in ids if ids.count(i) > 1})
    if duplicates:
        raise PlanValidationError(f"Duplicate task IDs: {duplicates}")

    kept = {t.id for t in sorted(plan.tasks, key=lambda t: t.priority)[:max_tasks]}
    if len(kept) < len(plan.tasks):
        dropped = [t.id for t in plan.tasks if t.id not in kept]
        logger.warning(f"Plan capped at {max_tasks} tasks, dropped: {dropped}")
    plan.tasks = [t for t in plan.tasks if t.id in kept]

    for task in plan.tasks:
        valid = [d for d in task.dependencies if d in kept and d != task.id]
        if len(valid) < len(task.dependencies):
            removed = sorted(set(task.dependencies) - set(valid))
            logger.warning(f"Task {task.id}: removed invalid dependencies {removed}")
        task.dependencies = valid

    plan.execution_order = _topological_order(plan.tasks)
    return plan


def _topological_order(tasks: list[SubTask]) -> list[str]:
    """Dependencies first, otherwise plan order; raises on cycles"""
    by_id = {t.id: t for t in tasks}
    order: list[str] = []
    visiting: set[str] = set()
    done: set[str] = set()

    def visit(task_id: str, path: list[str]):
        if task_id in done:
            return
        if task_id in visiting:
            cycle = " -> ".join([*path[path.index(task_id) :], task_id])
            raise PlanValidationError(f"Dependency cycle: {cycle}")
        visiting.add(task_id)
        for dep in by_id[task_id].dependencies:
            visit(dep, [*path, task_id])
        visiting.remove(task_id)
        done.add(task_id)
        order.append(task_id)

    for task in tasks:
        visit(task.id, [])
    return order
