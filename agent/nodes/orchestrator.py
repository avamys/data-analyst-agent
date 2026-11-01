"""Orchestrator Agent - Strategic decision maker for analysis approach"""

import logging

import pandas as pd

from agent.core.base_agent import BaseAgent
from agent.core.template_manager import prompt_templates
from agent.states import DatasetProfile, HierarchicalState, StrategicPlan, TargetType

logger = logging.getLogger(__name__)


# Column names treated as the target when none is given explicitly
TARGET_NAMES = ["target", "label", "class", "outcome", "y"]


def detect_target(
    df: pd.DataFrame, target: str | None = None
) -> tuple[str | None, TargetType]:
    """
    Pick the target column (explicit name, else a conventional name) and its type

    The type comes from the number of distinct values, not the dtype, so string
    labels such as "yes"/"no" are classification targets too.
    """
    if target is not None:
        if target not in df.columns:
            raise ValueError(f"Target {target!r} is not a column of the dataset")
    else:
        by_lower = {c.lower(): c for c in df.columns}
        target = next((by_lower[n] for n in TARGET_NAMES if n in by_lower), None)
        if target is None:
            return None, "none"

    n_unique = df[target].nunique()
    if n_unique == 2:
        return target, "binary"
    if not pd.api.types.is_numeric_dtype(df[target]) or n_unique <= 10:
        return target, "multiclass"
    return target, "regression"


def _column_kind(series: pd.Series) -> str:
    """
    numeric, categorical, datetime, or one of the kinds that aren't features as is:
    id (mostly unique values, e.g. row numbers or ticket codes) or text (long
    mostly unique strings, e.g. names). One-hot encoding those creates a column
    per row.
    """
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    values = series.dropna()
    n_unique = values.nunique()
    mostly_unique = n_unique > 20 and n_unique > 0.5 * len(values)
    if pd.api.types.is_numeric_dtype(series):
        # Integers unique on every row are identifiers; measurements are numeric
        if (
            pd.api.types.is_integer_dtype(series)
            and mostly_unique
            and n_unique == len(series)
        ):
            return "id"
        return "numeric"
    if mostly_unique:
        return "text" if values.astype(str).str.len().mean() > 20 else "id"
    return "categorical"


def auto_profile_dataset(
    df: pd.DataFrame, dataset_path: str, target: str | None = None
) -> DatasetProfile:
    """
    Automatically profile a dataset to understand its characteristics

    Args:
        target: Target column; detected from conventional names when omitted
    """
    n_rows, n_cols = df.shape
    target_column, target_type = detect_target(df, target)

    # Every column gets a kind; only numeric/categorical/datetime are features
    feature_types = {
        col: "target" if col == target_column else _column_kind(df[col])
        for col in df.columns
    }

    def of_kind(kind: str) -> list[str]:
        return [col for col, k in feature_types.items() if k == kind]

    numeric_features = of_kind("numeric")
    categorical_features = of_kind("categorical")
    datetime_features = of_kind("datetime")

    # Check for missing values
    has_missing = df.isnull().any().any()
    missing_percentages = {}
    if has_missing:
        missing_percentages = (df.isnull().sum() / len(df) * 100).to_dict()
        missing_percentages = {k: v for k, v in missing_percentages.items() if v > 0}

    # Check for class imbalance (if target exists)
    has_imbalance = False
    if target_column and target_type in ["binary", "multiclass"]:
        class_counts = df[target_column].value_counts()
        ratio = class_counts.max() / class_counts.min() if len(class_counts) > 1 else 1
        has_imbalance = ratio > 2.0

    # Has temporal data
    has_temporal = len(datetime_features) > 0

    profile = DatasetProfile(
        n_rows=n_rows,
        n_cols=n_cols,
        target_column=target_column,
        target_type=target_type,
        feature_types=feature_types,
        numeric_features=numeric_features,
        categorical_features=categorical_features,
        datetime_features=datetime_features,
        id_columns=of_kind("id"),
        text_columns=of_kind("text"),
        has_missing=has_missing,
        missing_percentages=missing_percentages,
        has_imbalance=has_imbalance,
        has_temporal=has_temporal,
    )

    logger.info(f"Dataset Profile: {n_rows} rows, {n_cols} cols")
    logger.info(f"Target: {target_column} ({target_type})")
    logger.info(
        f"Features: {len(numeric_features)} numeric, {len(categorical_features)} categorical"
    )

    return profile


class OrchestratorAgent(BaseAgent):
    """
    Orchestrator analyzes dataset and decides analysis strategy

    Responsibilities:
    - Profile the dataset automatically
    - Decide which analysis strategies to apply (EDA, Statistical, ML, etc.)
    - Determine priority order
    - Estimate complexity
    """

    def __init__(self, **kwargs):
        super().__init__(
            agent_type="orchestrator",
            use_structured_output=True,
            output_schema=StrategicPlan,
            **kwargs,
        )

    def execute(self, state: HierarchicalState) -> HierarchicalState:
        """Execute orchestrator logic"""
        dataset_info = state.dataset_info
        dataset_path = state.dataset_path

        # Load and profile dataset
        df = pd.read_csv(dataset_path)
        profile = auto_profile_dataset(df, dataset_path, state.target_column)

        # Build profile summary
        profile_summary = self._build_profile_summary(profile)

        # Get prompt from template
        prompt = prompt_templates.render(
            "orchestrator/strategy_selection.jinja2",
            profile_summary=profile_summary,
            dataset_info=dataset_info[:1000],
        )

        # Invoke LLM (already configured with structured output)
        strategic_plan = self.invoke(prompt)

        # Log the strategic plan
        self._log_strategic_plan(strategic_plan)

        # Update state
        state.dataset_profile = profile
        state.strategic_plan = strategic_plan
        state.current_phase = "planning"

        return state

    def _build_profile_summary(self, profile: DatasetProfile) -> str:
        """Build formatted profile summary"""
        summary = f"""
DATASET PROFILE:
- Size: {profile.n_rows:,} rows × {profile.n_cols} columns
- Target Variable: {profile.target_column or "None detected"} ({profile.target_type})
- Features:
  • Numeric: {len(profile.numeric_features)} ({", ".join(profile.numeric_features[:5])}{", ..." if len(profile.numeric_features) > 5 else ""})
  • Categorical: {len(profile.categorical_features)} ({", ".join(profile.categorical_features[:5])}{", ..." if len(profile.categorical_features) > 5 else ""})
  • Temporal: {len(profile.datetime_features)}
- Not features as they are (ids, free text): {", ".join(profile.id_columns + profile.text_columns) or "none"}
- Data Quality:
  • Missing values: {"Yes" if profile.has_missing else "No"}"""

        if profile.has_missing:
            missing_info = ", ".join(
                [
                    f"{k} ({v:.1f}%)"
                    for k, v in list(profile.missing_percentages.items())[:3]
                ]
            )
            summary += f"\n  • Missing in: {missing_info}"

        summary += f"""
  • Class imbalance: {"Yes" if profile.has_imbalance else "No"}
"""
        return summary

    def _log_strategic_plan(self, strategic_plan: StrategicPlan):
        """Log the strategic plan"""
        self.logger.info("=" * 60)
        self.logger.info("STRATEGIC PLAN")
        self.logger.info("=" * 60)
        self.logger.info(f"Strategies: {[s.value for s in strategic_plan.strategies]}")
        self.logger.info(
            f"Priority Order: {[s.value for s in strategic_plan.priority_order]}"
        )
        self.logger.info(f"Reasoning: {strategic_plan.reasoning}")
        self.logger.info(f"Estimated Tasks: {strategic_plan.estimated_tasks}")
        self.logger.info("=" * 60)


def orchestrator_node(state: HierarchicalState) -> HierarchicalState:
    """
    Orchestrator node for graph integration

    Creates and executes orchestrator agent.
    """
    agent = OrchestratorAgent()
    return agent.execute(state)
