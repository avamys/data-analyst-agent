"""Deterministic dataset profile: target, column kinds, data quality, leakage"""

import logging

import pandas as pd

from agent.config import settings
from agent.states import DatasetProfile, TargetType

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
        has_imbalance = ratio > settings.imbalance_ratio

    # Has temporal data
    has_temporal = len(datetime_features) > 0

    class_shares = {}
    leakage_suspects = {}
    if target_column:
        if target_type != "regression":
            shares = df[target_column].value_counts(normalize=True)
            class_shares = {str(k): round(float(v), 4) for k, v in shares.items()}
        leakage_suspects = _leakage_suspects(
            df, target_column, target_type, feature_types
        )

    # A code standing in for "unknown" (0, -1, 999) fills the cell, so it
    # isn't counted as missing; it shows as a repeated value or a gap
    numeric_columns = numeric_features + (
        [target_column] if target_type == "regression" else []
    )
    distributions = {
        col: _distribution(df[col]) for col in numeric_columns if df[col].notna().any()
    }

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
        class_shares=class_shares,
        leakage_suspects=leakage_suspects,
        distributions=distributions,
    )

    logger.info(f"Dataset Profile: {n_rows} rows, {n_cols} cols")
    logger.info(f"Target: {target_column} ({target_type})")
    logger.info(
        f"Features: {len(numeric_features)} numeric, {len(categorical_features)} categorical"
    )

    if leakage_suspects:
        logger.warning(f"Leakage suspects: {leakage_suspects}")

    return profile


def _leakage_suspects(
    df: pd.DataFrame, target: str, target_type: str, feature_types: dict[str, str]
) -> dict[str, float]:
    """
    Feature columns that alone predict the target almost perfectly, which usually
    means they were derived from it

    Classification: accuracy of predicting the most frequent class within each of
    the column's values (numeric columns in deciles). Regression: |correlation|.
    """
    y = df[target]
    baseline = y.value_counts(normalize=True).iloc[0]
    suspects = {}
    for col, kind in feature_types.items():
        if kind not in ("numeric", "categorical"):
            continue
        x = df[col]
        if target_type == "regression":
            if kind != "numeric":
                continue
            score = abs(x.corr(y))
            suspect = score >= settings.leakage_score
        else:
            if kind == "numeric" and x.nunique() > 10:
                x = pd.qcut(x, 10, duplicates="drop")
            groups = x.astype(str)
            hits = y.groupby(groups).agg(lambda s: s.value_counts().max()).sum()
            score = hits / y.notna().sum()
            suspect = (
                baseline < 1
                and (score - baseline) / (1 - baseline) >= settings.leakage_score
            )
        if suspect:
            suspects[col] = round(float(score), 3)
    return suspects


def _distribution(series: pd.Series) -> dict[str, float]:
    """Where a numeric column's values lie, and its most common value"""
    values = series.dropna()
    counts = values.value_counts()
    return {
        "min": float(values.min()),
        "p1": float(values.quantile(0.01)),
        "median": float(values.median()),
        "max": float(values.max()),
        "mode": float(counts.index[0]),
        "mode_count": int(counts.iloc[0]),
    }


def profile_summary(profile: DatasetProfile) -> str:
    """The profile as text for the lead's prompts"""

    def names(cols: list[str]) -> str:
        return ", ".join(cols) or "none"

    lines = [
        f"- Size: {profile.n_rows:,} rows × {profile.n_cols} columns",
        f"- Target: {profile.target_column or 'none detected'} ({profile.target_type})",
        f"- Numeric features: {names(profile.numeric_features)}",
        f"- Categorical features: {names(profile.categorical_features)}",
        f"- Date/time features: {names(profile.datetime_features)}",
        f"- Not features as they are (ids, free text): "
        f"{names(profile.id_columns + profile.text_columns)}",
    ]
    if profile.class_shares:
        shares = ", ".join(f"{k}: {v:.1%}" for k, v in profile.class_shares.items())
        lines.append(
            f"- Target classes: {shares}"
            + (" (imbalanced)" if profile.has_imbalance else "")
        )
    missing = ", ".join(
        f"{col} ({pct:.1f}%)" for col, pct in profile.missing_percentages.items()
    )
    lines.append(f"- Empty cells: {missing or 'none'}")
    if profile.distributions:
        lines.append("- Numeric columns:")
    for col, d in profile.distributions.items():
        line = (
            f"  - {col}: min {d['min']:.4g}, 1st pct {d['p1']:.4g}, "
            f"median {d['median']:.4g}, max {d['max']:.4g}"
        )
        # A few repeats in a continuous column are rounding, not a spike
        if d["mode_count"] > 1 and d["mode_count"] >= 0.01 * profile.n_rows:
            line += (
                f"; most common {d['mode']:.4g} "
                f"({int(d['mode_count']):,} of {profile.n_rows:,})"
            )
        lines.append(line)
    if profile.leakage_suspects:
        suspects = ", ".join(
            f"{col} ({score})" for col, score in profile.leakage_suspects.items()
        )
        lines.append(
            "- WARNING, possible target leakage: these columns alone predict the "
            f"target almost perfectly: {suspects}"
        )
    return "\n".join(lines)
