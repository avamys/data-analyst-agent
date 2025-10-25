from pydantic import BaseModel
from typing import List, Optional


class Insight(BaseModel):
    task: str
    goal: str


class InsightsList(BaseModel):
    insights: List[Insight]


class AgentState(BaseModel):
    dataset_info: str
    analysis_plan: Optional[InsightsList] = None
    code_output: str = ""
    code_written: str = ""
    error_message: str = ""
    retry_count: int = 0
    critic_feedback: str = ""
    revision_count: int = 0
    report: str = ""