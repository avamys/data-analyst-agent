"""Planner Agent - Decomposes strategies into actionable tasks"""

import logging

from agent.config import settings
from agent.core.base_agent import BaseAgent
from agent.core.template_manager import prompt_templates
from agent.states import AnalysisPlan, AnalysisStrategy, HierarchicalState

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

        # Get structured plan from LLM
        analysis_plan = self.invoke(prompt)

        # The model may ignore the requested count; dependencies on dropped
        # tasks are skipped by _compute_execution_order
        if len(analysis_plan.tasks) > settings.max_tasks:
            self.logger.warning(
                f"Plan has {len(analysis_plan.tasks)} tasks, keeping first {settings.max_tasks}"
            )
            analysis_plan.tasks = analysis_plan.tasks[: settings.max_tasks]

        # Build execution order respecting dependencies
        execution_order = _compute_execution_order(analysis_plan.tasks)
        analysis_plan.execution_order = execution_order

        # Build parallel groups (tasks with no dependencies can run together)
        parallel_groups = _compute_parallel_groups(analysis_plan.tasks, execution_order)
        analysis_plan.parallel_groups = parallel_groups

        # Log the plan
        self._log_analysis_plan(analysis_plan)

        # Update state
        state.analysis_plan = analysis_plan
        state.pending_tasks = execution_order.copy()
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
        self.logger.info(
            f"Parallel Groups: {len(analysis_plan.parallel_groups)} groups"
        )
        self.logger.info("=" * 60)


def planner_node(state: HierarchicalState) -> HierarchicalState:
    """
    Planner node for graph integration

    Creates and executes planner agent.
    """
    agent = PlannerAgent()
    return agent.execute(state)


def _compute_execution_order(tasks: list) -> list:
    """
    Compute execution order using topological sort
    """
    task_dict = {t.id: t for t in tasks}
    visited = set()
    order = []

    def visit(task_id):
        if task_id in visited:
            return
        visited.add(task_id)

        task = task_dict.get(task_id)
        if task:
            # Visit dependencies first
            for dep in task.dependencies:
                if dep in task_dict:
                    visit(dep)
            order.append(task_id)

    # Visit all tasks
    for task in tasks:
        visit(task.id)

    return order


def _compute_parallel_groups(tasks: list, execution_order: list) -> list:
    """
    Group tasks that can run in parallel (no dependencies between them)
    """
    task_dict = {t.id: t for t in tasks}
    groups = []
    remaining = set(execution_order)
    completed = set()

    while remaining:
        # Find tasks whose dependencies are all completed
        ready = []
        for task_id in remaining:
            task = task_dict[task_id]
            if all(dep in completed for dep in task.dependencies):
                ready.append(task_id)

        if ready:
            groups.append(ready)
            for task_id in ready:
                remaining.remove(task_id)
                completed.add(task_id)
        else:
            # Shouldn't happen with valid dependencies
            logger.warning(
                f"Circular dependency detected in remaining tasks: {remaining}"
            )
            groups.append(list(remaining))
            break

    return groups
