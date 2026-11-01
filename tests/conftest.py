"""Shared test fixtures. Tests never depend on data/ (gitignored) or a running LLM."""

import numpy as np
import pandas as pd
import pytest
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda


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


class ScriptedLLM:
    """
    Stands in for every model: returns the given responses in call order and
    keeps the prompts. Structured calls get the objects as they are; plain-text
    calls get strings wrapped in an AIMessage.
    """

    def __init__(self, responses):
        self.responses = iter(responses)
        self.prompts = []

    def _respond(self, messages):
        self.prompts.append(messages[0].content)
        response = next(self.responses)
        return AIMessage(content=response) if isinstance(response, str) else response

    def with_structured_output(self, schema):
        return RunnableLambda(self._respond)

    def with_retry(self, **kwargs):
        return RunnableLambda(self._respond)
