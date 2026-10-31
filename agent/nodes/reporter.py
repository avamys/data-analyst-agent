"""Hierarchical Reporter - Generates comprehensive final report"""

import logging

from agent.core.base_agent import BaseAgent
from agent.core.template_manager import prompt_templates
from agent.states import HierarchicalState

logger = logging.getLogger(__name__)


def hierarchical_reporter_node(state: HierarchicalState) -> HierarchicalState:
    """
    Generates comprehensive final report from hierarchical analysis

    Responsibilities:
    - Incorporate strategic approach and execution summary
    - Include synthesized insights
    - Present detailed findings organized by analysis type
    - Provide actionable recommendations
    """
    strategic_plan = state.strategic_plan
    dataset_profile = state.dataset_profile
    completed_tasks = state.completed_tasks
    failed_tasks = state.failed_tasks
    synthesis = state.synthesis

    logger.info("=" * 60)
    logger.info("REPORTING PHASE")
    logger.info("=" * 60)

    execution_summary = build_execution_summary(completed_tasks, failed_tasks)

    # Build detailed findings section
    detailed_findings = _format_detailed_findings(completed_tasks)

    # Build prompt using template
    strategies = ", ".join([s.value for s in strategic_plan.strategies])
    priority_order = " → ".join([s.value for s in strategic_plan.priority_order])

    prompt = prompt_templates.render(
        "reporter/final_report.jinja2",
        dataset_path=state.dataset_path,
        n_rows=dataset_profile.n_rows,
        n_cols=dataset_profile.n_cols,
        target_column=dataset_profile.target_column,
        target_type=dataset_profile.target_type,
        n_numeric=len(dataset_profile.numeric_features),
        n_categorical=len(dataset_profile.categorical_features),
        strategies=strategies,
        priority_order=priority_order,
        reasoning=strategic_plan.reasoning,
        execution_summary=execution_summary,
        synthesis=synthesis,
        detailed_findings=detailed_findings[:3000],
        n_ml=len([t for t in completed_tasks if t.specialist == "ml"]),
    )

    # Use BaseAgent directly - no need for subclass
    agent = BaseAgent(agent_type="reporter")
    response = agent.invoke(prompt)
    report = response.content.strip() if hasattr(response, "content") else str(response)

    logger.info("Final report generated")
    logger.info(f"Report length: {len(report)} characters")
    logger.info("=" * 60)

    # Update state
    state.report = report

    return state


def build_execution_summary(completed_tasks: list, failed_tasks: list) -> str:
    """Summarize task outcomes; each task is in exactly one of the two lists"""
    all_tasks = completed_tasks + failed_tasks
    total = len(all_tasks)
    success_rate = len(completed_tasks) / total * 100 if total else 0.0
    counts = {
        s: sum(t.specialist == s for t in completed_tasks)
        for s in ("eda", "statistical", "ml")
    }
    total_time = sum(t.execution_time for t in all_tasks)

    return f"""
Total Tasks: {total}
- Completed: {len(completed_tasks)}
- Failed: {len(failed_tasks)}
- Success Rate: {success_rate:.1f}%

Completed By Specialist:
- EDA: {counts["eda"]} tasks
- Statistical: {counts["statistical"]} tasks
- Machine Learning: {counts["ml"]} tasks

Total Execution Time: {total_time:.1f} seconds
"""


def _format_detailed_findings(completed_tasks: list) -> str:
    """Format detailed findings for inclusion in report"""
    findings = ""

    # Group by specialist
    for specialist in ["eda", "statistical", "ml"]:
        tasks = [t for t in completed_tasks if t.specialist == specialist]
        if not tasks:
            continue

        findings += f"\n### {specialist.upper()} Findings\n\n"

        for task in tasks:
            findings += f"**{task.description}**\n\n"

            # Include key output lines
            output_lines = task.output.split("\n")
            key_lines = [
                line
                for line in output_lines
                if line.strip() and not line.startswith("#")
            ]
            findings += "\n".join(key_lines[:15]) + "\n\n"

            # Include insights
            if task.insights:
                findings += "Key Insights:\n"
                for insight in task.insights:
                    findings += f"- {insight}\n"
                findings += "\n"

    return findings
