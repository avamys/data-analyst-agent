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
    execution_error = state.execution_error
    revision_count = state.revision_count
    critic_feedback = state.critic_feedback
    code_written = state.code_written

    insights_text = "\n".join([
        f"{i+1}. Task: {insight.task}\n   Goal: {insight.goal}"
        for i, insight in enumerate(analysis_plan.insights)
    ])

    code_written_context = ""
    if code_written:
        code_written_context = f"""
        PREVIOUS CODE WRITTEN:
        ```python
        {code_written}
        ```
        """

    execution_error_context = ""
    if execution_error:
        execution_error_context = f"""
        PREVIOUS CODE HAD EXECUTION ERROR:
        {execution_error}
        
        Fix the technical error:
        - Check syntax and indentation
        - Verify variable names and imports (Available libraries: pandas, numpy, matplotlib, scipy)
        - Handle missing/null data appropriately
        """

    critic_feedback_context = ""
    if critic_feedback and revision_count > 0:
        critic_feedback_context = f"""
        CRITIC'S FEEDBACK (Revision #{revision_count}):
        {critic_feedback}
        
        The previous analysis was incomplete or incorrect.
        Address the critic's concerns in your code:
        - Add missing analyses
        - Provide more detailed insights
        - Fix incorrect interpretations
        - Ensure all tasks are completed
        """

    debug_context = ""
    if state.debug_suggestions:
        debug_context = f"""
        DEBUGGING SUGGESTIONS:
        {state.debug_suggestions}
        """

    prompt = f"""
    You are a Python data scientist. Write Python code to analyze the data.

    Dataset info:
    {dataset_info}

    Analysis plan:
    {insights_text}

    {code_written_context}

    {execution_error_context}

    {critic_feedback_context}

    Write clean, executable Python code using pandas. 
    The code should:
    - Load data from 'data/titanic.csv'
    - Perform ALL analysis tasks listed above
    - Print results clearly with descriptive labels
    
    {"IMPORTANT: This is revision #" + str(revision_count) + ". Make sure to address the critic's feedback!" if revision_count > 0 else ""}

    {debug_context}

    Only respond with the Python code to execute, nothing else.
    """

    response = coder_llm.invoke([HumanMessage(content=prompt)])
    code_to_run = response.content.strip()

    if code_to_run.startswith("```python"):
        code_to_run = code_to_run.split("```python")[1].split("```")[0].strip()
    elif code_to_run.startswith("```"):
        code_to_run = code_to_run.split("```")[1].split("```")[0].strip()
    
    state.code_written = code_to_run
    attempt_label = f"attempt {retry_count + 1}" if retry_count > 0 else f"revision {revision_count}"
    logger.info(f"Executing code ({attempt_label}):\n{code_to_run}")

    output = python_tool.run(code_to_run)
    state.code_output = output
    logger.info(f"Code output:\n{output}")

    return state