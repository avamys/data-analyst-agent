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
    
    Evaluate if the output adequately answers ALL analysis questions.
    
    Respond in this format:
    VERDICT: [APPROVED/NEEDS_REVISION]
    FEEDBACK: [Specific feedback about what's missing or wrong]
    """
    
    response = analyst_llm.invoke([HumanMessage(content=prompt)])
    feedback = response.content.strip()
    
    state.critic_feedback = feedback
    logger.info(f"Critic feedback (revision {revision_count}):\n{feedback}")
    
    return state