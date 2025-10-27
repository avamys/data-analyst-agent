"""Reporter Agent - Generates final narrative report from all insights"""
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
import logging
from agent.states import AgentState
from agent.config import settings


logger = logging.getLogger(__name__)


reporter_llm = init_chat_model(
    settings.reporter_model,
    model_provider="ollama",
    base_url=settings.ollama_base_url,
    temperature=0.3,
)


def reporter_node(state: AgentState) -> AgentState:
    """
    Reporter creates a comprehensive final report:
    - Summarizes all findings from the investigation
    - Describes the analytical reasoning chain
    - Highlights key insights and patterns
    - Notes limitations and potential next steps
    """
    dataset_info = state.dataset_info
    conversation_history = state.conversation_history
    insights_collected = state.insights_collected
    
    # Build complete investigation narrative
    investigation_narrative = ""
    if conversation_history:
        investigation_narrative = "## Investigation Process\n\n"
        for turn in conversation_history:
            investigation_narrative += f"### Step {turn.iteration}: {turn.hypothesis}\n\n"
            investigation_narrative += f"**Approach:** {turn.code_task}\n\n"
            investigation_narrative += f"**Findings:**\n{turn.code_result}\n\n"
            investigation_narrative += f"**Interpretation:** {turn.interpretation}\n\n"
            investigation_narrative += "---\n\n"
    
    insights_summary = ""
    if insights_collected:
        insights_summary = "## Key Insights\n\n"
        for i, insight in enumerate(insights_collected, 1):
            insights_summary += f"{i}. {insight}\n"
        insights_summary += "\n"
    
    prompt = f"""You are a senior data scientist writing a final analysis report.

DATASET ANALYZED:
{dataset_info[:500]}...

{investigation_narrative}

{insights_summary}

Write a comprehensive final report in markdown format with these sections:

# Data Analysis Report

## Executive Summary
Provide a high-level overview of the key findings (2-3 sentences).

## Dataset Overview
Brief description of the data analyzed.

## Analysis Approach
Describe the analytical reasoning chain - what questions were asked and why.

## Key Findings
Detailed findings from each investigation step. Include:
- Patterns discovered
- Relationships identified
- Statistical insights
- Any surprising or noteworthy observations

## Conclusions
Synthesize the findings into actionable conclusions.

## Limitations & Next Steps
What are the limitations of this analysis?
What additional questions could be explored?

Make the report professional, insightful, and easy to understand.
"""
    
    response = reporter_llm.invoke([HumanMessage(content=prompt)])
    report = response.content.strip()
    
    state.report = report
    logger.info("Final report generated")
    logger.info(f"Report preview:\n{report[:500]}...")
    
    return state
