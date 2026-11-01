"""Deterministic sanity checks on a task result, shown to the lead during review"""

from agent.states import Brief, DatasetProfile, TaskResult

# Train score above test score by more than this suggests overfitting
OVERFIT_GAP = 0.1
# A test score at or above this is suspicious: leakage more often than skill
NEAR_PERFECT = 0.99
# Test accuracy within this of the majority-class baseline adds nothing
BASELINE_MARGIN = 0.02


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
        if train - test > OVERFIT_GAP:
            problems.append(
                f"Model {name}: train {metric} {train} vs test {test}, a gap of "
                f"{train - test:.2f}: overfitting. The report must say so."
            )
        if test >= NEAR_PERFECT:
            problems.append(
                f"Model {name}: test {metric} {test} is near-perfect, which usually "
                "means a feature leaks the target. It must be investigated, not praised."
            )
        if scores["kind"] == "classifier":
            baseline = scores["baseline_accuracy"]
            if test - baseline < BASELINE_MARGIN:
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
