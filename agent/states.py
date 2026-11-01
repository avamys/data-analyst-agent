"""State definitions for hierarchical multi-agent analysis workflow"""

from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, Field


class AnalysisStrategy(StrEnum):
    """Types of analysis strategies"""

    EXPLORATORY = "exploratory"
    STATISTICAL = "statistical"
    PREDICTIVE = "predictive"


TargetType = Literal["binary", "multiclass", "regression", "none"]


class DatasetProfile(BaseModel):
    """Automated dataset profiling"""

    n_rows: int
    n_cols: int
    target_column: str | None = None
    target_type: TargetType = "none"
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


class Finding(BaseModel):
    """One conclusion from a task, backed by recorded facts"""

    statement: str = Field(description="One conclusion, stated with its numbers")
    facts: list[str] = Field(
        default_factory=list,
        description="Names of the recorded facts that support the statement",
    )


class TaskReport(BaseModel):
    """What a specialist hands back when it finishes a task"""

    status: Literal["answered", "partial", "failed"] = Field(
        description="answered: the task is done; partial: only part of it; failed: no usable result"
    )
    findings: list[Finding] = Field(default_factory=list)
    follow_ups: list[str] = Field(
        default_factory=list,
        description="Questions worth a separate task, raised by the results",
    )


class SpecialistStep(BaseModel):
    """One step of a specialist: run a new cell, or finish with a report"""

    reasoning: str = Field(
        description="Briefly: what the latest result shows and what to do next"
    )
    action: Literal["run", "finish"]
    code: str = Field(default="", description="Python code for one new cell (run)")
    report: TaskReport | None = Field(default=None, description="The report (finish)")


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
    report: TaskReport | None = None
    facts: dict[str, Any] = Field(default_factory=dict)  # facts.json of the task
    charts: dict[str, Any] = Field(default_factory=dict)  # charts.json of the task
    artifacts: list[str] = Field(default_factory=list)  # File paths
    # Every run of a new cell: attempt (step), code, output, error, seconds
    attempts: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class HierarchicalState(BaseModel):
    """State for hierarchical multi-agent analysis workflow"""

    # Input
    dataset_info: str
    dataset_path: str
    target_column: str | None = None  # Detected from column names when None
    run_dir: str  # Task scripts and their outputs live under <run_dir>/tasks/

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
    completed_tasks: list[TaskResult] = Field(default_factory=list)
    failed_tasks: list[TaskResult] = Field(default_factory=list)

    # Synthesis layer
    synthesis: str = ""

    # Output
    report: str = ""
