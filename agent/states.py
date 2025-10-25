from pydantic import BaseModel, Field
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
    # error_message: str = ""
    
    execution_error: str = ""
    critic_feedback: str = ""
    debug_suggestions: str = ""

    retry_count: int = 0
    revision_count: int = 0
    report: str = ""

    addressed_insights: List[int] = Field(default_factory=list)