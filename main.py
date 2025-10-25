import pandas as pd
from langgraph.graph import StateGraph, END, START
from langchain.chat_models import init_chat_model
from langchain_experimental.tools import PythonREPLTool
from langchain_core.messages import AnyMessage, SystemMessage, ToolMessage, HumanMessage
import logging
from pydantic import BaseModel
from typing import List


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")

class Insight(BaseModel):
    task: str
    goal: str

class InsightsList(BaseModel):
    insights: List[Insight]


class AgentState(BaseModel):
    dataset_info: str
    analysis_plan: InsightsList = None
    code_output: str = ""
    error_message: str = ""
    retry_count: int = 0
    report: str = ""


analyst_llm = init_chat_model(
    "llama3.1:8b",
    model_provider="ollama",
    base_url="http://host.docker.internal:11434",
    temperature=0.4,
)
analyst_structured = analyst_llm.with_structured_output(InsightsList)


coder_llm = init_chat_model(
    "llama3.1:8b",
    model_provider="ollama",
    base_url="http://host.docker.internal:11434",
    temperature=0.2,
)
python_tool = PythonREPLTool()


def analyst_node(state: AgentState):
    """Analyst defines analysis plan"""
    dataset_info = state.dataset_info
    prompt = f"""
    You are a data analyst. Based on this dataset info:
    {dataset_info}

    Define 3–5 data insights to investigate.
    Each insight should be a structured task with clear goal and approach.
    """
    analysis_plan = analyst_structured.invoke([HumanMessage(content=prompt)])
    logging.info(f"Analysis plan defined:\n{analysis_plan}")
    state.analysis_plan = analysis_plan
    return state


def coder_node(state: AgentState):
    """Coder writes AND executes Python code"""
    dataset_info = state.dataset_info
    analysis_plan = state.analysis_plan
    retry_count = state.retry_count
    error_message = state.error_message

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
    {analysis_plan}

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
    
    logging.info(f"Executing code (attempt {retry_count + 1}):\n{code_to_run}")
    
    try:
        output = python_tool.run(code_to_run)
        state.code_output = output
        logging.info(f"Code output:\n{output}")
    except Exception as e:
        error_output = f"Execution Error: {str(e)}"
        state.code_output = error_output
        logging.error(f"Code execution error:\n{error_output}")

    return state


def check_code_success(state: AgentState) -> str:
    """Check if code execution was successful or had errors"""
    code_output = state.code_output
    retry_count = state.retry_count

    error_indicators = ["Error", "Exception", "Traceback", "SyntaxError", "NameError", "TypeError"]
    has_error = any(indicator in code_output for indicator in error_indicators)
    
    if has_error and retry_count < 3:
        logging.warning(f"Code execution failed (attempt {retry_count + 1}). Retrying...")
        return "retry"
    elif has_error:
        logging.error(f"Code execution failed after {retry_count + 1} attempts")
        return "finish"
    else:
        logging.info("Code execution successful")
        return "finish"


def retry_node(state: AgentState):
    """Update state for retry"""
    retry_count = state.retry_count
    state.error_message = state.code_output
    state.retry_count = retry_count + 1
    return state


def finish_node(state: AgentState):
    """Final report assembly"""
    return {
        "report": f"""
        === ANALYSIS PLAN ===
        {state.analysis_plan}

        === RESULTS ===
        {state.code_output}
        """
    }


graph = StateGraph(AgentState)
graph.add_node("analyst", analyst_node)
graph.add_node("coder", coder_node)
graph.add_node("retry", retry_node)
graph.add_node("finish", finish_node)

graph.add_edge(START, "analyst")
graph.add_edge("analyst", "coder")
graph.add_conditional_edges(
    "coder",
    check_code_success,
    {
        "retry": "retry",
        "finish": "finish"
    }
)
graph.add_edge("analyst", "coder")
graph.add_edge("retry", "coder")
graph.add_edge("finish", END)


data_analysis_flow = graph.compile()


def main():
    logging.info("Starting data analysis workflow")
    datafile = "data/titanic.csv"
    df = pd.read_csv(datafile)

    logging.info(
        f"Loaded dataset from {datafile} with {len(df)} rows and columns: {', '.join(df.columns)}"
    )
    logging.info("Running analysis flow...")

    result = data_analysis_flow.invoke(
        {
            "dataset_info": f"""
            file: {datafile}
            Columns: {", ".join([col for col in df.columns])}
            {len(df)} rows. {" | ".join([f"{col}: {df[col].dtype}" for col in df.columns])}
            Sample data:
            {df.head().to_markdown()}
            Column types:
            {" | ".join([f"{col}: {df[col].dtype}" for col in df.columns])}
            Statistical summary:
            {df.describe().to_markdown()}
            Categorical summary:
            {df.describe(include="object").to_markdown()}
            """
        }
    )
    logging.info("Analysis flow completed")

    logging.info(result)


if __name__ == "__main__":
    main()
