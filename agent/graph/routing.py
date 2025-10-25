"""Routing logic for conditional edges"""
import logging
from agent.states import AgentState
from agent.config import settings

logger = logging.getLogger(__name__)

def check_code_success(state: AgentState) -> str:
    """Check if code execution was successful or had errors"""
    code_output = state.code_output
    retry_count = state.retry_count

    error_indicators = ["Error", "Exception", "Traceback", "SyntaxError", "NameError", "TypeError"]
    has_error = any(indicator in code_output for indicator in error_indicators)
    
    if has_error and retry_count < settings.max_code_retries:
        logger.warning(f"Code execution failed (attempt {retry_count + 1}). Retrying...")
        return "retry"
    elif has_error:
        logger.error(f"Code execution failed after {retry_count + 1} attempts")
        state.execution_error = code_output
        return "debug"
    else:
        logger.info("Code execution successful")
        return "critic"

def check_critic_verdict(state: AgentState) -> str:
    """Route based on critic's verdict"""
    feedback = state.critic_feedback
    revision_count = state.revision_count
    
    if "APPROVED" in feedback.upper():
        logger.info("Critic approved the analysis")
        return "finish"
    elif revision_count < settings.max_revisions:
        logger.warning(f"Critic requested revision ({revision_count + 1}/{settings.max_revisions})")
        return "revise"
    else:
        logger.error("Max revisions reached, finishing anyway")
        return "finish"

def retry_node(state: AgentState) -> AgentState:
    """Update state for retry"""
    state.retry_count += 1
    return state

def revise_node(state: AgentState) -> AgentState:
    """Prepare state for revision"""
    state.revision_count += 1
    state.retry_count = 0
    state.execution_error = ""
    return state

def debug_node(state: AgentState) -> AgentState:
    """Handle debugging after max retries"""
    state.retry_count = 0
    state.execution_error = ""
    return state

def finish_node(state: AgentState) -> dict:
    """Final report assembly"""
    return {
        "report": f"""
        === ANALYSIS PLAN ===
        {state.analysis_plan}

        === RESULTS ===
        {state.code_output}
        
        === CRITIC FEEDBACK ===
        {state.critic_feedback}
        """
    }