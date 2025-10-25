from langchain.chat_models import init_chat_model
from langchain_experimental.tools import PythonREPLTool
from langchain_core.messages import AnyMessage, SystemMessage, ToolMessage, HumanMessage
import logging
from agent.states import AgentState, InsightsList


logger = logging.getLogger(__name__)


coder_llm = init_chat_model(
    "llama3.1:8b",
    model_provider="ollama",
    base_url="http://host.docker.internal:11434",
    temperature=0.2,
)
python_tool = PythonREPLTool()


def coder_node(state: AgentState):
    """Coder writes AND executes Python code"""
    dataset_info = state.dataset_info
    analysis_plan = state.analysis_plan
    retry_count = state.retry_count
    error_message = state.error_message

    insights_text = "\n".join([
        f"{i+1}. Task: {insight.task}\n   Goal: {insight.goal}"
        for i, insight in enumerate(analysis_plan.insights)
    ])

    error_context = ""
    if error_message:
        error_context = f"""
        PREVIOUS ATTEMPT FAILED with error:
        {error_message}
        
        Please fix the error and try again. Make sure to:
        - Check syntax carefully
        - Handle missing data appropriately
        - Use correct variable names
        """

    prompt = f"""
    You are a Python data scientist. Write Python code to analyze the data.

    Dataset info:
    {dataset_info}

    Analysis plan:
    {insights_text}

    {error_context}

    Write clean, executable Python code using pandas. 
    The code should:
    - Load data from 'data/titanic.csv'
    - Perform the analysis from the plan
    - Print results clearly
    
    Only respond with the Python code to execute, nothing else.
    """

    response = coder_llm.invoke([HumanMessage(content=prompt)])
    code_to_run = response.content.strip()

    if code_to_run.startswith("```python"):
        code_to_run = code_to_run.split("```python")[1].split("```")[0].strip()
    elif code_to_run.startswith("```"):
        code_to_run = code_to_run.split("```")[1].split("```")[0].strip()
    
    logger.info(f"Executing code (attempt {retry_count + 1}):\n{code_to_run}")
    
    try:
        output = python_tool.run(code_to_run)
        state.code_output = output
        logger.info(f"Code output:\n{output}")
    except Exception as e:
        error_output = f"Execution Error: {str(e)}"
        state.code_output = error_output
        logger.error(f"Code execution error:\n{error_output}")

    return state