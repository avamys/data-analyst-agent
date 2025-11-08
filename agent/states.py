"""State definitions for hierarchical multi-agent analysis workflow"""
from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any
from enum import Enum


class AnalysisStrategy(str, Enum):
    """Types of analysis strategies"""
    EXPLORATORY = "exploratory"
    STATISTICAL = "statistical"
    PREDICTIVE = "predictive"
    TIME_SERIES = "time_series"
    CLUSTERING = "clustering"


class DatasetProfile(BaseModel):
    """Automated dataset profiling"""
    n_rows: int
    n_cols: int
    target_column: Optional[str] = None
    target_type: Literal["binary", "multiclass", "regression", "none"] = "none"
    feature_types: Dict[str, str] = Field(default_factory=dict)  # {col: "numeric"/"categorical"/"datetime"}
    numeric_features: List[str] = Field(default_factory=list)
    categorical_features: List[str] = Field(default_factory=list)
    datetime_features: List[str] = Field(default_factory=list)
    has_missing: bool = False
    missing_percentages: Dict[str, float] = Field(default_factory=dict)
    has_imbalance: bool = False
    has_temporal: bool = False
    

class StrategicPlan(BaseModel):
    """High-level analysis strategy from orchestrator"""
    strategies: List[AnalysisStrategy]
    priority_order: List[AnalysisStrategy]
    reasoning: str
    estimated_tasks: int


class SubTask(BaseModel):
    """Individual analysis sub-task"""
    id: str
    strategy: AnalysisStrategy
    specialist: Literal["eda", "statistical", "ml"]
    description: str
    dependencies: List[str] = Field(default_factory=list)  # Task IDs that must complete first
    priority: int = 1
    estimated_complexity: int = 1  # 1-5 scale


class AnalysisPlan(BaseModel):
    """Detailed execution plan with tasks"""
    tasks: List[SubTask]
    execution_order: List[str]  # Task IDs in order
    parallel_groups: List[List[str]] = Field(default_factory=list)  # Tasks that can run in parallel


class TaskResult(BaseModel):
    """Result from executing a single task"""
    task_id: str
    specialist: str
    description: str
    code: str = ""
    output: str = ""
    execution_time: float = 0.0
    success: bool = True
    error: Optional[str] = None
    insights: List[str] = Field(default_factory=list)
    artifacts: List[str] = Field(default_factory=list)  # File paths
    metadata: Dict[str, Any] = Field(default_factory=dict)


class VizOpportunity(BaseModel):
    """Visualization opportunity identified during analysis"""
    task_id: str
    description: str
    plot_type: str  # bar, scatter, box, histogram, heatmap
    data_summary: str
    priority: int = 1


class HierarchicalState(BaseModel):
    """State for hierarchical multi-agent analysis workflow"""
    
    # Input
    dataset_info: str
    dataset_path: str
    
    # Phase tracking
    current_phase: Literal["orchestration", "planning", "execution", "synthesis", "reporting"] = "orchestration"
    
    # Orchestration layer
    dataset_profile: Optional[DatasetProfile] = None
    strategic_plan: Optional[StrategicPlan] = None
    
    # Planning layer
    analysis_plan: Optional[AnalysisPlan] = None
    
    # Execution layer
    pending_tasks: List[str] = Field(default_factory=list)
    completed_tasks: List[TaskResult] = Field(default_factory=list)
    failed_tasks: List[TaskResult] = Field(default_factory=list)
    current_task_index: int = 0
    
    # Synthesis layer
    synthesis: str = ""
    cross_insights: List[str] = Field(default_factory=list)
    
    # Visualization
    viz_opportunities: List[VizOpportunity] = Field(default_factory=list)
    viz_artifacts: List[str] = Field(default_factory=list)
    
    # Output
    report: str = ""
    artifacts_dir: str = "output"
