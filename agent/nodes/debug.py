from langchain_core.messages import HumanMessage
import logging
from agent.state import AgentState
from agent.nodes.analyst import analyst_llm


logger = logging.getLogger(__name__)


def debugger_node(state: AgentState):
    """Specialized agent that analyzes errors and suggests fixes for coder"""
    execution_error = state.execution_error
    code_written = state.code_written
    dataset_info = state.dataset_info
    analysis_plan = state.analysis_plan
    retry_count = state.retry_count
    
    # Format the analysis plan for context
    insights_text = "\n".join([
        f"{i+1}. {insight.task} (Goal: {insight.goal})"
        for i, insight in enumerate(analysis_plan.insights)
    ])
    
    prompt = f"""
    You are a Python debugging expert specializing in fixing code that runs in isolated PythonREPL environment.
    
    EXECUTION ENVIRONMENT CONSTRAINTS:
    - Code runs in an isolated PythonREPL session
    - Only standard library and pre-installed packages are available (pandas, numpy, matplotlib, sklearn, scipy)
    - CANNOT install new packages (no pip, conda, or package managers)
    - CANNOT modify system files or environment
    - Code must be self-contained and executable in one run
    - File I/O is limited to the data directory
    
    ORIGINAL ANALYSIS GOAL:
    {insights_text}
    
    CODE THAT FAILED (Attempt #{retry_count + 1}):
    ```python
    {code_written}
    ```
    
    ERROR MESSAGE:
    {execution_error}
    
    DATASET INFORMATION:
    {dataset_info}
    
    Analyze the error and provide a fix that:
    1. DOES NOT require installing any packages
    2. Uses only available libraries (pandas, numpy, matplotlib, scipy)
    3. Is self-contained and executable in PythonREPL
    4. Handles the specific error properly
    
    Provide your response in this format:
    
    ROOT CAUSE:
    [Brief explanation of what caused the error]
    
    FIX STRATEGY:
    [Specific approach to fix the error within REPL constraints]
    
    CORRECTED CODE:
    ```python
    [Only the corrected Python code, ready to execute]
    ```
    
    Be precise and ensure the fix works in an isolated REPL environment.
    """
    
    response = analyst_llm.invoke([HumanMessage(content=prompt)])
    state.debug_suggestions = response.content

    logger.info(f"Debugging suggestions (attempt {retry_count + 1}):\n{state.debug_suggestions}")
    
    return state