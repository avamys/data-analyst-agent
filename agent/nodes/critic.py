"""Critic agent implementation"""
from langchain_core.messages import HumanMessage
import logging
from agent.states import AgentState
from agent.nodes.analyst import analyst_llm

logger = logging.getLogger(__name__)

def critic_node(state: AgentState) -> AgentState:
    """Critic evaluates if the code output answers the analysis questions"""
    analysis_plan = state.analysis_plan
    code_output = state.code_output
    revision_count = state.revision_count
    
    insights_text = "\n".join([
        f"{i+1}. {insight.task} (Goal: {insight.goal})"
        for i, insight in enumerate(analysis_plan.insights)
    ])
    
    prompt = f"""
    You are a critical data science reviewer.
    
    ANALYSIS QUESTIONS TO ANSWER:
    {insights_text}
    
    CODE OUTPUT RECEIVED:
    {code_output}
    
    Evaluate the output carefully:
    1. Does it address ALL {len(analysis_plan.insights)} analysis tasks?
    2. Are the results clearly presented and interpretable?
    3. Are the insights accurate and meaningful?
    4. Is anything missing or incorrect?
    
    Respond in this EXACT format:
    VERDICT: [APPROVED or NEEDS_REVISION]
    FEEDBACK: [If APPROVED: Summarize what was done well. If NEEDS_REVISION: Specific list of what's missing or wrong]
    
    Be specific about which tasks (by number) are incomplete or incorrect.
    """
    
    response = analyst_llm.invoke([HumanMessage(content=prompt)])
    feedback = response.content.strip()
    
    state.critic_feedback = feedback
    logger.info(f"Critic feedback (revision {revision_count}):\n{feedback}")
    
    return state