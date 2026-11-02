"""Deterministic sanity checks on a task result, shown to the lead during review"""

from agent.config import settings
from agent.states import Brief, DatasetProfile, TaskResult


def missing_outputs(brief: Brief, published: list[str]) -> list[str]:
    """Names the brief asks the task to publish that aren't among its load() refs"""
    names = {ref.split("/", 1)[1] for ref in published}
    return [o.name for o in brief.outputs if o.name not in names]


def sanity_checks(
    brief: Brief, result: TaskResult, profile: DatasetProfile
) -> list[str]:
    """Problems found in the result, one sentence each; empty when none"""
    problems = []
    missing = missing_outputs(brief, result.published)
    if missing:
        problems.append(
            f"Outputs later tasks need were not published: {missing}. "
            "The task must be sent back to publish them."
        )

    for name, fact in result.facts.items():
        if fact.get("kind") != "model":
            continue
        scores = fact["value"]
        metric = "accuracy" if scores["kind"] == "classifier" else "r2"
        train, test = scores[f"train_{metric}"], scores[f"test_{metric}"]
        if train - test > settings.overfit_gap:
            problems.append(
                f"Model {name}: train {metric} {train} vs test {test}, a gap of "
                f"{train - test:.2f}: overfitting. The report must say so."
            )
        if test >= settings.near_perfect_score:
            problems.append(
                f"Model {name}: test {metric} {test} is near-perfect, which usually "
                "means a feature leaks the target. It must be investigated, not praised."
            )
        if scores["kind"] == "classifier":
            baseline = scores["baseline_accuracy"]
            if test - baseline < settings.baseline_margin:
                problems.append(
                    f"Model {name}: test accuracy {test} is no better than always "
                    f"predicting the most frequent class ({baseline})."
                )

    if brief.specialist == "ml":
        if profile.leakage_suspects:
            problems.append(
                "The profile found columns that alone predict the target almost "
                f"perfectly: {profile.leakage_suspects}. Using them as features "
                "would leak the target."
            )
        if profile.has_imbalance:
            problems.append(
                f"The target classes are imbalanced ({profile.class_shares}): "
                "accuracy alone is misleading; judge models by recall, F1 or AUC "
                "against the baseline."
            )
    return problems
