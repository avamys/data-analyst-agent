"""Shared test fixtures. Tests never depend on data/ (gitignored) or a running LLM."""

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def small_df() -> pd.DataFrame:
    """Small mixed-type dataset with a binary target and missing values"""
    rng = np.random.default_rng(0)
    n = 40
    df = pd.DataFrame(
        {
            "age": rng.integers(18, 80, n).astype(float),
            "fare": rng.normal(30, 10, n).round(2),
            "sex": rng.choice(["male", "female"], n),
            "port": rng.choice(["S", "C", "Q"], n),
            "target": rng.integers(0, 2, n),
        }
    )
    df.loc[:4, "age"] = np.nan
    return df


@pytest.fixture
def small_csv(tmp_path, small_df) -> str:
    path = tmp_path / "small.csv"
    small_df.to_csv(path, index=False)
    return str(path)
