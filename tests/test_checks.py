"""Deterministic sanity checks the lead sees when reviewing a task"""

from agent.checks import sanity_checks
from agent.profiling import auto_profile_dataset
from agent.states import Brief, Output, TaskResult


def _brief(specialist="ml", outputs=()) -> Brief:
    return Brief(
        id="ml_1",
        specialist=specialist,
        question="q",
        complete_when="c",
        outputs=[Output(name=o, contents="x") for o in outputs],
    )


def _model(**scores) -> TaskResult:
    value = {
        "kind": "classifier",
        "train_accuracy": 0.8,
        "test_accuracy": 0.8,
        "baseline_accuracy": 0.6,
    } | scores
    facts = {"m": {"value": value, "desc": "d", "kind": "model"}}
    return TaskResult(task_id="ml_1", specialist="ml", description="d", facts=facts)


def test_a_sound_model_passes(small_df):
    profile = auto_profile_dataset(small_df, "x.csv")
    assert sanity_checks(_brief(), _model(), profile) == []


def test_overfitting_near_perfect_and_baseline_level_models_are_flagged(small_df):
    profile = auto_profile_dataset(small_df, "x.csv")
    (overfit,) = sanity_checks(_brief(), _model(train_accuracy=1.0), profile)
    assert "overfitting" in overfit
    (perfect,) = sanity_checks(
        _brief(), _model(train_accuracy=1.0, test_accuracy=0.995), profile
    )
    assert "near-perfect" in perfect
    (useless,) = sanity_checks(
        _brief(), _model(train_accuracy=0.62, test_accuracy=0.61), profile
    )
    assert "no better than always predicting" in useless


def test_regressors_are_checked_on_r2(small_df):
    profile = auto_profile_dataset(small_df, "x.csv")
    result = _model(kind="regressor", train_r2=0.9, test_r2=0.5)
    (problem,) = sanity_checks(_brief(), result, profile)
    assert "train r2 0.9 vs test 0.5" in problem


def test_missing_outputs_are_flagged(small_df):
    profile = auto_profile_dataset(small_df, "x.csv")
    (problem,) = sanity_checks(_brief(outputs=["split"]), _model(), profile)
    assert "not published: ['split']" in problem


def test_ml_tasks_are_warned_about_leakage_suspects(small_df):
    df = small_df.assign(leak=small_df["target"].map({0: "no", 1: "yes"}))
    profile = auto_profile_dataset(df, "x.csv")
    (warning,) = sanity_checks(_brief(), _model(), profile)
    assert "'leak'" in warning
    assert sanity_checks(_brief(specialist="eda"), _model(), profile) == []
