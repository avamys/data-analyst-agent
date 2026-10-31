import pandas as pd
import pytest

from agent.nodes.orchestrator import auto_profile_dataset, detect_target


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
