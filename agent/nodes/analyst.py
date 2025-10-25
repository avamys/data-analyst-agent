from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
import logging
from agent.states import AgentState, InsightsList


logger = logging.getLogger(__name__)


analyst_llm = init_chat_model(
    "llama3.1:8b",
    model_provider="ollama",
    base_url="http://host.docker.internal:11434",
    temperature=0.4,
)
analyst_structured = analyst_llm.with_structured_output(InsightsList)


def analyst_node(state: AgentState) -> AgentState:
    """Analyst defines analysis plan"""
    dataset_info = state.dataset_info
    
    prompt = f"""
    You are a data analyst. Based on this dataset info:
    {dataset_info}

    Define 3–5 data insights to investigate.
    Each insight should be a structured task with clear goal and approach.
    """
    
    analysis_plan = analyst_structured.invoke([HumanMessage(content=prompt)])
    logger.info(f"Analysis plan defined:\n{analysis_plan}")
    
    state.analysis_plan = analysis_plan
    return state