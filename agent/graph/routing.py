"""Routing logic for the iterative analyst-coder workflow"""
import logging
from agent.states import AgentState
from agent.config import settings

logger = logging.getLogger(__name__)


def route_analyst_decision(state: AgentState) -> str:
    """
    Route based on analyst's decision:
    - ASK_CODER: Send task to coder
    - FINISH: Move to reporter for final report
    """
    decision = state.current_decision
    
    if not decision:
        logger.error("No decision from analyst!")
        return "reporter"
    
    if decision.decision == "ASK_CODER":
        logger.info(f"Analyst requests code task: {decision.code_task}")
        return "coder"
    elif decision.decision == "FINISH":
        logger.info("Analyst decided to finish. Moving to reporter.")
        return "reporter"
    else:
        logger.warning(f"Unknown decision: {decision.decision}. Defaulting to reporter.")
        return "reporter"


def route_coder_result(state: AgentState) -> str:
    """
    Check coder's execution result:
    - If error and retries available: retry
    - If error and max retries reached: back to analyst (analyst will see error)
    - If success: back to analyst for interpretation
    """
    execution_error = state.execution_error
    retry_count = state.retry_count
    iteration_count = state.iteration_count
    
    # Check if we've hit max iterations (safety limit)
    if iteration_count >= settings.max_iterations:
        logger.warning(f"Max iterations ({settings.max_iterations}) reached.")
        # Analyst will need to see max iterations and decide to finish
        # Just send back to analyst regardless of error state
        state.retry_count = 0
        return "analyst"
    
    # Check for execution errors
    if execution_error and retry_count < settings.max_code_retries:
        logger.warning(f"Code error detected. Retry {retry_count + 1}/{settings.max_code_retries}")
        return "retry"
    elif execution_error and retry_count >= settings.max_code_retries:
        logger.error(f"Max retries reached. Sending error result back to analyst.")
        # Reset retry count for next task
        state.retry_count = 0
        return "analyst"
    else:
        # Success - reset retry count and return to analyst
        logger.info("Code executed successfully. Returning to analyst for interpretation.")
        state.retry_count = 0
        return "analyst"


def retry_node(state: AgentState) -> AgentState:
    """Update state for code retry"""
    state.retry_count += 1
    logger.info(f"Preparing retry attempt {state.retry_count}")
    return state
