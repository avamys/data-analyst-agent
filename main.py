import pandas as pd
from langgraph.graph import StateGraph, END
from langchain.chat_models import init_chat_model
from langchain_experimental.tools import PythonREPLTool
from langchain_core.messages import AnyMessage, SystemMessage, ToolMessage, HumanMessage
import logging
from pydantic import BaseModel
from typing import List


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")


class AgentState(dict):
    dataset_info: str
    analysis_plan: str
    code_output: str

class Insight(BaseModel):
    task: str
    goal: str

class InsightsList(BaseModel):
    insights: List[Insight]


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
coder_agent = coder_llm.bind_tools([python_tool])


def analyst_node(state: AgentState):
    """Analyst defines analysis plan"""
    dataset_info = state.get("dataset_info")
    prompt = f"""
    You are a data analyst. Based on this dataset info:
    {dataset_info}

    Define 3–5 data insights to investigate.
    Each insight should be a structured task with clear goal and approach.
    """
    analysis_plan = analyst_structured.invoke([HumanMessage(content=prompt)])
    logging.info(f"Analysis plan defined:\n{analysis_plan}")
    state["analysis_plan"] = analysis_plan
    return state


def coder_node(state: AgentState):
    """Coder writes AND executes Python code"""
    dataset_info = state["dataset_info"]
    analysis_plan = state["analysis_plan"]

    prompt = f"""
    You are a Python data scientist.

    Dataset info:
    {dataset_info}

    Analysis plan:
    {analysis_plan}

    Your task:
    - Implement Python code using pandas, numpy, matplotlib (if relevant)
    - Execute your code to produce insights or printed outputs.
    - Summarize results in plain text.
    """

    response = coder_agent.invoke([HumanMessage(content=prompt)])

    if response.tool_calls:
        tool_call = response.tool_calls[0]
        code_to_run = tool_call["args"]["query"]
        output = python_tool.run(code_to_run)
        state["code_output"] = output
    else:
        state["code_output"] = response.content

    return state


def finish_node(state: AgentState):
    """Final report assembly"""
    return {
        "report": f"""
        === ANALYSIS PLAN ===
        {state["analysis_plan"]}

        === RESULTS ===
        {state["code_output"]}
        """
    }


graph = StateGraph(AgentState)
graph.add_node("analyst", analyst_node)
graph.add_node("coder", coder_node)
graph.add_node("finish", finish_node)

graph.add_edge("analyst", "coder")
graph.add_edge("coder", "finish")
graph.set_entry_point("analyst")
graph.set_finish_point("finish")


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
