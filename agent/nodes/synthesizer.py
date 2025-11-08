"""Synthesizer - Combines findings from all specialist agents"""
import logging
from agent.core.base_agent import BaseAgent
from agent.core.template_manager import prompt_templates
from agent.states import HierarchicalState, AnalysisStrategy

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
    
    # Collect all insights
    all_insights = []
    for result in completed_tasks:
        all_insights.extend(result.insights)
    
    # Build prompt
    insights_text = '\n'.join([f'• {insight}' for insight in all_insights[:20]])
    prompt = prompt_templates.render(
        "synthesizer/synthesis.jinja2",
        n_eda=len(eda_results),
        n_stat=len(stat_results),
        n_ml=len(ml_results),
        n_failed=len(failed_tasks),
        eda_summary=eda_summary,
        stat_summary=stat_summary,
        ml_summary=ml_summary,
        all_insights=insights_text,
    )
    
    # Use BaseAgent directly - no need for subclass
    agent = BaseAgent(agent_type="synthesizer")
    response = agent.invoke(prompt)
    synthesis = response.content.strip() if hasattr(response, 'content') else str(response)
    
    # Extract cross-cutting insights
    cross_insights = _extract_cross_insights(completed_tasks)
    
    logger.info("Synthesis complete")
    logger.info(f"Cross-insights identified: {len(cross_insights)}")
    
    # Update state
    state.synthesis = synthesis
    state.cross_insights = cross_insights
    state.current_phase = "reporting"
    
    return state


def _summarize_results(results: list, category: str) -> str:
    """Summarize results from a category of tasks"""
    if not results:
        return f"\n{category.upper()}: No tasks completed\n"
    
    summary = f"\n{category.upper()} ({len(results)} tasks):\n"
    
    for result in results:
        summary += f"\n[{result.task_id}] {result.description}\n"
        if result.success:
            # Include output snippet
            output_lines = result.output.split('\n')
            key_lines = [line for line in output_lines if line.strip() and not line.startswith('#')][:10]
            summary += '\n'.join(key_lines[:5]) + '\n'
            
            # Include insights
            if result.insights:
                summary += f"Key insights: {'; '.join(result.insights[:2])}\n"
        else:
            summary += f"ERROR: {result.error}\n"
    
    return summary


def _extract_cross_insights(results: list) -> list:
    """Extract insights that appear across multiple analyses"""
    # Simple heuristic: insights mentioned by multiple specialists
    insight_counts = {}
    
    for result in results:
        for insight in result.insights:
            # Normalize insight (lowercase, remove punctuation)
            normalized = insight.lower().strip('.,!?')
            insight_counts[normalized] = insight_counts.get(normalized, 0) + 1
    
    # Insights mentioned more than once
    cross_insights = [
        insight for insight, count in insight_counts.items() 
        if count > 1
    ]
    
    return cross_insights[:10]  # Top 10
