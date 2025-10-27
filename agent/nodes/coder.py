"""Coder Agent - Executes code tasks with self-debugging retry logic"""
from langchain.chat_models import init_chat_model
from langchain_experimental.tools import PythonREPLTool
from langchain_core.messages import HumanMessage
import logging
from agent.states import AgentState
from agent.config import settings


logger = logging.getLogger(__name__)


coder_llm = init_chat_model(
    settings.coder_model,
    model_provider="ollama",
    base_url=settings.ollama_base_url,
    temperature=settings.coder_temperature,
)
python_tool = PythonREPLTool()


def coder_node(state: AgentState) -> AgentState:
    """
    Coder executes a single specific task from the analyst:
    - Writes Python code based on the task
    - Executes the code
    - Has retry logic for self-debugging if errors occur
    - Returns execution result back to analyst
    """
    dataset_info = state.dataset_info
    code_task = state.code_task
    retry_count = state.retry_count
    execution_error = state.execution_error
    previous_code = state.code_written
    
    # Build context for retry attempts
    retry_context = ""
    if retry_count > 0 and execution_error:
        retry_context = f"""
PREVIOUS ATTEMPT FAILED (Attempt {retry_count + 1}/{settings.max_code_retries + 1}):

Previous code:
```python
{previous_code}
```

Error encountered:
{execution_error}

DEBUGGING INSTRUCTIONS:
- Fix the technical error in the code
- Common issues: missing imports, syntax errors, undefined variables
- Available libraries: pandas, numpy, matplotlib, seaborn, scipy
- Cannot install new packages - use only available libraries
- Handle missing/null data appropriately
- Verify column names match the dataset
"""
    
    prompt = f"""You are an expert Python data scientist. 

DATASET INFO:
{dataset_info}

TASK FROM ANALYST:
{code_task}

{retry_context}

Write clean, executable Python code to complete this specific task.

Requirements:
- Load data from 'data/titanic.csv' using pandas
- Focus on the specific task given by the analyst
- Print results clearly with descriptive labels
- PRIORITIZE NUMERICAL OUTPUT: statistics, percentages, counts, correlations, summary tables
- AVOID creating visualizations/charts unless explicitly requested by the analyst
- Use print statements extensively to show all key results and statistics
- If you must create a plot, also print the underlying data/statistics

{"IMPORTANT: This is a retry. Fix the error from the previous attempt!" if retry_count > 0 else ""}

Respond with ONLY the Python code to execute, nothing else.
"""
    
    response = coder_llm.invoke([HumanMessage(content=prompt)])
    code_to_run = response.content.strip()
    
    # Clean up code formatting
    if code_to_run.startswith("```python"):
        code_to_run = code_to_run.split("```python")[1].split("```")[0].strip()
    elif code_to_run.startswith("```"):
        code_to_run = code_to_run.split("```")[1].split("```")[0].strip()
    
    state.code_written = code_to_run
    
    attempt_label = f"(Attempt {retry_count + 1})" if retry_count > 0 else ""
    logger.info(f"Executing code {attempt_label}:\n{code_to_run[:500]}...")
    
    # Execute the code
    try:
        output = python_tool.run(code_to_run)
        state.code_output = output
        state.execution_error = ""  # Clear any previous errors
        logger.info(f"Code executed successfully. Output:\n{output[:300]}...")
    except Exception as e:
        error_msg = str(e)
        state.code_output = f"EXECUTION ERROR: {error_msg}"
        state.execution_error = error_msg
        logger.error(f"Code execution failed: {error_msg}")
    
    return state
