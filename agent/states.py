from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class AnalystDecision(BaseModel):
    """Structured output from analyst"""
    decision: Literal["ASK_CODER", "FINISH"]
    reasoning: str
    hypothesis: Optional[str] = None
    code_task: Optional[str] = None


class ConversationTurn(BaseModel):
    """Record of one iteration in the analysis"""
    iteration: int
    hypothesis: str
    code_task: str
    code_result: str
    interpretation: str


class AgentState(BaseModel):
    """State for the iterative analysis workflow"""
    # Input data
    dataset_info: str
    
    # Analyst state
    current_decision: Optional[AnalystDecision] = None
    conversation_history: List[ConversationTurn] = Field(default_factory=list)
    insights_collected: List[str] = Field(default_factory=list)
    
    # Coder state
    code_task: str = ""
    code_written: str = ""
    code_output: str = ""
    execution_error: str = ""
    retry_count: int = 0
    
    # Control flow
    iteration_count: int = 0
    
    # Final output
    report: str = ""