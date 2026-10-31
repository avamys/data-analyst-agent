"""State definitions for hierarchical multi-agent analysis workflow"""

from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, Field


class AnalysisStrategy(StrEnum):
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
    target_column: str | None = None
    target_type: Literal["binary", "multiclass", "regression", "none"] = "none"
    feature_types: dict[str, str] = Field(
        default_factory=dict
    )  # {col: "numeric"/"categorical"/"datetime"}
    numeric_features: list[str] = Field(default_factory=list)
    categorical_features: list[str] = Field(default_factory=list)
    datetime_features: list[str] = Field(default_factory=list)
    has_missing: bool = False
    missing_percentages: dict[str, float] = Field(default_factory=dict)
    has_imbalance: bool = False
    has_temporal: bool = False


class StrategicPlan(BaseModel):
    """High-level analysis strategy from orchestrator"""

    strategies: list[AnalysisStrategy]
    priority_order: list[AnalysisStrategy]
    reasoning: str
    estimated_tasks: int


class SubTask(BaseModel):
    """Individual analysis sub-task"""

    id: str
    strategy: AnalysisStrategy
    specialist: Literal["eda", "statistical", "ml"]
    description: str
    dependencies: list[str] = Field(
        default_factory=list
    )  # Task IDs that must complete first
    priority: int = 1
    estimated_complexity: int = 1  # 1-5 scale


class AnalysisPlan(BaseModel):
    """Detailed execution plan with tasks"""

    tasks: list[SubTask]
    execution_order: list[str]  # Task IDs in order
    parallel_groups: list[list[str]] = Field(
        default_factory=list
    )  # Tasks that can run in parallel


class TaskResult(BaseModel):
    """Result from executing a single task"""

    task_id: str
    specialist: str
    description: str
    code: str = ""
    output: str = ""
    execution_time: float = 0.0
    success: bool = True
    error: str | None = None
    insights: list[str] = Field(default_factory=list)
    artifacts: list[str] = Field(default_factory=list)  # File paths
    metadata: dict[str, Any] = Field(default_factory=dict)


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
    current_phase: Literal[
        "orchestration", "planning", "execution", "synthesis", "reporting"
    ] = "orchestration"

    # Orchestration layer
    dataset_profile: DatasetProfile | None = None
    strategic_plan: StrategicPlan | None = None

    # Planning layer
    analysis_plan: AnalysisPlan | None = None

    # Execution layer
    pending_tasks: list[str] = Field(default_factory=list)
    completed_tasks: list[TaskResult] = Field(default_factory=list)
    failed_tasks: list[TaskResult] = Field(default_factory=list)
    current_task_index: int = 0

    # Synthesis layer
    synthesis: str = ""
    cross_insights: list[str] = Field(default_factory=list)

    # Visualization
    viz_opportunities: list[VizOpportunity] = Field(default_factory=list)
    viz_artifacts: list[str] = Field(default_factory=list)

    # Output
    report: str = ""
    artifacts_dir: str = "output"
