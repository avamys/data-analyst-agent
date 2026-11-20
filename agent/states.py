"""State definitions for hierarchical multi-agent analysis workflow"""

from typing import Any, Literal

from pydantic import BaseModel, Field

TargetType = Literal["binary", "multiclass", "regression", "none"]


class DatasetProfile(BaseModel):
    """Automated dataset profiling"""

    n_rows: int
    n_cols: int
    target_column: str | None = None
    target_type: TargetType = "none"
    # Every column: numeric / categorical / datetime / target / id / text
    feature_types: dict[str, str] = Field(default_factory=dict)
    numeric_features: list[str] = Field(default_factory=list)
    categorical_features: list[str] = Field(default_factory=list)
    datetime_features: list[str] = Field(default_factory=list)
    id_columns: list[str] = Field(default_factory=list)  # Not features as is
    text_columns: list[str] = Field(default_factory=list)  # Not features as is
    has_missing: bool = False
    missing_percentages: dict[str, float] = Field(default_factory=dict)
    has_imbalance: bool = False
    has_temporal: bool = False
    # Share of each target class (classification targets)
    class_shares: dict[str, float] = Field(default_factory=dict)
    # Columns that alone predict the target almost perfectly: column -> score
    # (accuracy of predicting by the column's groups, or |correlation|)
    leakage_suspects: dict[str, float] = Field(default_factory=dict)
    # Numeric columns and a numeric target: min, p1, median, max, mode, mode_count
    distributions: dict[str, dict[str, float]] = Field(default_factory=dict)


class Output(BaseModel):
    """An object a task publishes for later tasks"""

    name: str = Field(description="snake_case name to publish it under")
    contents: str = Field(description="What the object is and what it contains")


class Brief(BaseModel):
    """A task the lead hands to a specialist"""

    id: str = Field(description="Short unique id that other briefs use in depends_on")
    specialist: Literal["eda", "statistical", "ml"]
    question: str = Field(description="The one question this task answers")
    complete_when: str = Field(description="What a complete answer contains")
    depends_on: list[str] = Field(
        default_factory=list,
        description="Ids of earlier tasks whose results or outputs this task needs",
    )
    outputs: list[Output] = Field(
        default_factory=list,
        description="Objects this task must publish because later tasks need them",
    )


class LeadPlan(BaseModel):
    """The lead's backlog of briefs, in the order they run"""

    reasoning: str = Field(
        description="Briefly: what this analysis must find out about the dataset"
    )
    briefs: list[Brief]


class PlanMessage(BaseModel):
    """One message in the conversation about the plan before it runs"""

    role: Literal["human", "lead"]
    text: str


class PlanRevision(BaseModel):
    """The lead's answer to the human's message about the plan"""

    reply: str = Field(
        description="To the human, briefly: what you changed, or the answer to "
        "their question, and any problem with what they asked"
    )
    briefs: list[Brief] = Field(
        description="The whole plan after the change, in order. Unchanged for a "
        "question. Keep each kept task's id; leave new tasks' ids empty"
    )


class Review(BaseModel):
    """The lead's decision on a task report"""

    reasoning: str = Field(
        description="Briefly: is each finding supported, is the brief answered, "
        "and do the checks show a problem"
    )
    verdict: Literal["accept", "revise"]
    feedback: str = Field(
        default="", description="revise: exactly what the specialist must fix or add"
    )
    follow_ups: list[Brief] = Field(
        default_factory=list,
        description="New tasks the results call for and the backlog doesn't cover",
    )


class Finding(BaseModel):
    """One conclusion from a task, backed by recorded facts"""

    statement: str = Field(description="One conclusion, stated with its numbers")
    facts: list[str] = Field(
        default_factory=list,
        description="Names of the recorded facts that support the statement",
    )


class TaskReport(BaseModel):
    """What a specialist hands back when it finishes a task"""

    # Not "answered": under constrained JSON decoding qwen3.5 almost never emits it
    # (0 of 9 even for a finished task) but picks "complete" reliably
    status: Literal["complete", "partial", "failed"] = Field(
        description="complete: the task is done; partial: only part of it; failed: no usable result"
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
    published: list[str] = Field(default_factory=list)  # load() refs, e.g. "ml_1/split"
    artifacts: list[str] = Field(default_factory=list)  # File paths
    # Every new cell tried: attempt, revision, step, code, output, error, seconds
    attempts: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    brief: Brief | None = None
    revisions: int = 0  # Times the lead sent the report back
    reviews: list[Review] = Field(default_factory=list)


class QuestionPlan(BaseModel):
    """The lead's route to answering a question about a finished run"""

    reasoning: str = Field(
        description="Briefly: do the recorded facts answer the question, and if "
        "not, what must be computed"
    )
    answer_now: bool = Field(
        description="true: the facts above answer it, or the dataset can't answer it"
    )
    facts: list[str] = Field(
        default_factory=list,
        description="Facts above the answer needs, as task_id.fact_name",
    )
    briefs: list[Brief] = Field(
        default_factory=list,
        description="answer_now false: the tasks that compute what is missing",
    )


class Question(BaseModel):
    """A question asked about a finished run, and its answer"""

    number: int
    text: str
    reasoning: str = ""  # The lead's, when it chose how to answer
    facts: list[str] = Field(default_factory=list)  # task_id.fact_name it relies on
    tasks: list[str] = Field(default_factory=list)  # Ids of the tasks run for it
    answer: str = ""
    unverified_numbers: list[str] = Field(default_factory=list)  # Match no fact


class HierarchicalState(BaseModel):
    """State for hierarchical multi-agent analysis workflow"""

    # Input
    dataset_info: str
    dataset_path: str
    target_column: str | None = None  # Detected from column names when None
    run_dir: str  # Task scripts and their outputs live under <run_dir>/tasks/

    # Lead analyst
    dataset_profile: DatasetProfile | None = None
    plan: LeadPlan | None = None  # As planned, before follow-ups
    backlog: list[Brief] = Field(default_factory=list)  # Briefs not started yet
    # Plan approval (settings.plan_approval): the conversation, and its outcome
    plan_chat: list[PlanMessage] = Field(default_factory=list)
    plan_approved: bool = False
    under_review: TaskResult | None = None  # The task just run, until accepted
    follow_ups_added: int = 0

    # Accepted tasks: each result is in exactly one list
    completed_tasks: list[TaskResult] = Field(default_factory=list)
    failed_tasks: list[TaskResult] = Field(default_factory=list)

    # Output
    report: str = ""
    unverified_numbers: list[str] = Field(default_factory=list)  # Match no fact

    # Asked after the report, in order; the last one is being answered
    questions: list[Question] = Field(default_factory=list)
