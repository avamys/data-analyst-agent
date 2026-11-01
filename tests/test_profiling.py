import numpy as np
import pandas as pd
import pytest

from agent.profiling import auto_profile_dataset, detect_target


def test_string_target_is_binary():
    # B6: non-numeric targets used to get type "none"
    df = pd.DataFrame({"x": range(6), "churned_flag": ["yes", "no"] * 3})
    assert detect_target(df, "churned_flag") == ("churned_flag", "binary")


def test_override_wins_over_name_heuristic():
    df = pd.DataFrame({"target": [0, 1, 0, 1], "Survived": [1, 0, 1, 1]})
    assert detect_target(df, "Survived") == ("Survived", "binary")


def test_unknown_override_raises():
    with pytest.raises(ValueError, match="not a column"):
        detect_target(pd.DataFrame({"x": [1]}), "nope")


def test_no_target_detected():
    # B6: "survived" was hard-coded, so this used to be detected on Titanic only
    df = pd.DataFrame({"Survived": [0, 1], "x": [1, 2]})
    assert detect_target(df) == (None, "none")


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([0, 1, 2, 0, 1, 2], "multiclass"),
        ([float(i) for i in range(30)], "regression"),
        (["a", "b", "c"] * 2, "multiclass"),
    ],
)
def test_target_types(values, expected):
    df = pd.DataFrame({"label": values})
    assert detect_target(df) == ("label", expected)


def test_profile_uses_requested_target(small_df):
    profile = auto_profile_dataset(small_df, "x.csv", target="sex")
    assert (profile.target_column, profile.target_type) == ("sex", "binary")


def test_ids_and_free_text_are_flagged_and_not_features():
    n = 50
    df = pd.DataFrame(
        {
            "row_id": range(n),
            "full_name": [
                f"Person number {i}, called something long" for i in range(n)
            ],
            "code": [f"A{i % 40}" for i in range(n)],  # mostly unique, short
            "group": ["a", "b"] * (n // 2),
            "value": [float(i % 7) for i in range(n)],
            "label": [0, 1] * (n // 2),
        }
    )
    profile = auto_profile_dataset(df, "x.csv", target="label")
    assert profile.feature_types == {
        "row_id": "id",
        "full_name": "text",
        "code": "id",
        "group": "categorical",
        "value": "numeric",
        "label": "target",
    }
    assert profile.numeric_features == ["value"]
    assert profile.categorical_features == ["group"]
    assert profile.id_columns == ["row_id", "code"]
    assert profile.text_columns == ["full_name"]


def test_columns_that_copy_the_target_are_leakage_suspects(small_df):
    df = small_df.assign(leak=small_df["target"].map({0: "no", 1: "yes"}))
    profile = auto_profile_dataset(df, "x.csv")
    assert profile.leakage_suspects == {"leak": 1.0}
    assert set(profile.class_shares) == {"0", "1"}


def test_near_copies_of_a_numeric_target_are_leakage_suspects():
    rng = np.random.default_rng(0)
    y = rng.normal(size=200)
    df = pd.DataFrame(
        {
            "y": y,
            "copy": y * 2 + rng.normal(0, 0.01, 200),
            "noise": rng.normal(size=200),
        }
    )
    profile = auto_profile_dataset(df, "x.csv")
    assert profile.target_type == "regression"
    assert list(profile.leakage_suspects) == ["copy"]
