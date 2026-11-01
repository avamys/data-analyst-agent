"""Synthesizer - Combines findings from all specialist agents"""

import logging

from agent.core.base_agent import BaseAgent
from agent.core.specialists import format_task_report
from agent.core.template_manager import prompt_templates
from agent.states import HierarchicalState

logger = logging.getLogger(__name__)


def synthesizer_node(state: HierarchicalState) -> HierarchicalState:
    """
    Synthesizes findings from all specialist agents

    No need for subclass - simple enough to use BaseAgent directly

    Responsibilities:
    - Aggregate results from EDA, Statistical, and ML specialists
    - Identify cross-cutting insights
    - Validate hypotheses with statistical evidence
    - Identify contradictions or gaps
    - Prioritize findings by importance
    """
    completed_tasks = state.completed_tasks
    failed_tasks = state.failed_tasks

    if not completed_tasks:
        logger.warning("No completed tasks to synthesize!")
        state.synthesis = "No analysis results to synthesize."
        state.current_phase = "reporting"
        return state

    logger.info("=" * 60)
    logger.info("SYNTHESIS PHASE")
    logger.info("=" * 60)

    # Group results by specialist
    eda_results = [r for r in completed_tasks if r.specialist == "eda"]
    stat_results = [r for r in completed_tasks if r.specialist == "statistical"]
    ml_results = [r for r in completed_tasks if r.specialist == "ml"]

    # Build detailed summaries
    eda_summary = _summarize_results(eda_results, "Exploratory Data Analysis")
    stat_summary = _summarize_results(stat_results, "Statistical Testing")
    ml_summary = _summarize_results(ml_results, "Machine Learning")

    findings_text = "\n".join(
        f"• [{r.task_id}] {f.statement}"
        for r in completed_tasks
        for f in r.report.findings
    )
    prompt = prompt_templates.render(
        "synthesizer/synthesis.jinja2",
        n_eda=len(eda_results),
        n_stat=len(stat_results),
        n_ml=len(ml_results),
        n_failed=len(failed_tasks),
        eda_summary=eda_summary,
        stat_summary=stat_summary,
        ml_summary=ml_summary,
        all_findings=findings_text,
    )

    # Use BaseAgent directly - no need for subclass
    agent = BaseAgent(agent_type="synthesizer")
    response = agent.invoke(prompt)
    synthesis = (
        response.content.strip() if hasattr(response, "content") else str(response)
    )

    logger.info("Synthesis complete")

    # Update state
    state.synthesis = synthesis
    state.current_phase = "reporting"

    return state


def _summarize_results(results: list, category: str) -> str:
    """Task reports (findings and full fact tables) of one category of tasks"""
    if not results:
        return f"\n{category.upper()}: No tasks completed\n"
    reports = "\n\n".join(format_task_report(r) for r in results)
    return f"\n{category.upper()} ({len(results)} tasks):\n\n{reports}\n"
