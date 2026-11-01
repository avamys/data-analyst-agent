"""Helpers for analysis code: the dataset, facts, charts, and hand-offs between tasks.

Imported by the first cell of every task script. Reads `.analyst.json` from the
working directory (the task directory), so `python analysis.py` also works there.
"""

import json
import math
import os
import pickle
import re
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

_context = json.loads(Path(".analyst.json").read_text())
_task_dir = Path.cwd()
_workspace = Path(_context["run_dir"]) / "workspace"

df = pd.read_csv(_context["data_path"])


def record_fact(name: str, value: Any, desc: str) -> None:
    """Record a result the report may cite, e.g. record_fact("survival_rate", 0.38, "...")"""
    _update_json("facts.json", name, {"value": _plain(value), "desc": desc})


def record_model(name: str, model, X_train, y_train, X_test, y_test, desc: str) -> dict:
    """
    Record a fitted model's scores as fact `name` and return them: train and test
    scores, the score of a trivial baseline, and the top features when the model
    exposes importances or coefficients
    """
    from sklearn import metrics
    from sklearn.base import is_classifier

    if is_classifier(model):
        y_train, y_test = np.asarray(y_train), np.asarray(y_test)
        majority = pd.Series(y_train).mode()[0]
        pred = model.predict(X_test)
        scores = {
            "kind": "classifier",
            "train_accuracy": metrics.accuracy_score(y_train, model.predict(X_train)),
            "test_accuracy": metrics.accuracy_score(y_test, pred),
            # Always predicting the most frequent training class
            "baseline_accuracy": float(np.mean(y_test == majority)),
        }
        if len(model.classes_) == 2:
            positive = model.classes_[1]
            truth, hits = y_test == positive, pred == positive
            scores |= {
                "positive_class": positive,
                "test_precision": metrics.precision_score(truth, hits, zero_division=0),
                "test_recall": metrics.recall_score(truth, hits),
                "test_f1": metrics.f1_score(truth, hits),
            }
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(X_test)[:, 1]
                scores["test_roc_auc"] = metrics.roc_auc_score(truth, proba)
        else:
            scores["test_macro_f1"] = metrics.f1_score(y_test, pred, average="macro")
    else:
        pred = model.predict(X_test)
        scores = {
            "kind": "regressor",
            "train_r2": metrics.r2_score(y_train, model.predict(X_train)),
            "test_r2": metrics.r2_score(y_test, pred),
            "test_rmse": metrics.root_mean_squared_error(y_test, pred),
            "test_mae": metrics.mean_absolute_error(y_test, pred),
            # Always predicting the training mean
            "baseline_rmse": metrics.root_mean_squared_error(
                y_test, np.full(len(y_test), np.mean(y_train))
            ),
        }
    scores = {k: round(v, 4) if isinstance(v, float) else v for k, v in scores.items()}
    scores |= _top_features(model, X_train)
    scores["n_train"], scores["n_test"] = len(y_train), len(y_test)
    _update_json(
        "facts.json", name, {"value": _plain(scores), "desc": desc, "kind": "model"}
    )
    return scores


def _top_features(model, X_train, n: int = 10) -> dict:
    """The n largest importances (or |coefficients|) by feature name, if available"""
    estimator = model.steps[-1][1] if hasattr(model, "steps") else model
    names = list(getattr(X_train, "columns", []))
    if hasattr(model, "steps"):
        try:
            names = list(model[:-1].get_feature_names_out())
        except Exception:
            pass
    if hasattr(estimator, "feature_importances_"):
        method, weights = "importance", np.asarray(estimator.feature_importances_)
    elif hasattr(estimator, "coef_"):
        coef = np.atleast_2d(estimator.coef_)
        method, weights = "abs_coefficient", np.abs(coef).mean(axis=0)
    else:
        return {}
    if len(names) != len(weights):
        return {}
    top = sorted(zip(names, weights, strict=True), key=lambda p: -p[1])[:n]
    return {
        "feature_ranking": method,
        "top_features": {k: round(float(w), 4) for k, w in top},
    }


def save_chart(fig, name: str, caption: str) -> None:
    """Save a matplotlib figure for the report and close it"""
    name = re.sub(r"[^\w-]+", "_", name)  # used as a file name
    path = Path("charts") / f"{name}.png"
    path.parent.mkdir(exist_ok=True)
    fig.savefig(path, dpi=100, bbox_inches="tight")
    import matplotlib.pyplot as plt

    plt.close(fig)
    _update_json("charts.json", name, {"file": str(path), "caption": caption})


def publish(name: str, obj: Any) -> None:
    """Make an object available to later tasks as load("<this task>/<name>")"""
    path = _workspace / _context["task_id"] / f"{name}.pkl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(pickle.dumps(obj))


def load(ref: str) -> Any:
    """Load an object published by an earlier task, e.g. load("ml_1/train_test")"""
    path = _workspace / f"{ref}.pkl"
    if not path.exists():
        available = sorted(
            str(p.relative_to(_workspace).with_suffix(""))
            for p in _workspace.glob("*/*.pkl")
        )
        raise FileNotFoundError(f"No published output {ref!r}. Available: {available}")
    return pickle.loads(path.read_bytes())


def _update_json(filename: str, key: str, entry: dict) -> None:
    path = _task_dir / filename
    data = json.loads(path.read_text()) if path.exists() else {}
    data[key] = {**entry, "cell": int(os.environ.get("ANALYST_CELL", -1))}
    path.write_text(json.dumps(data, indent=2))


def _plain(value: Any) -> Any:
    """Convert pandas/numpy values to JSON-friendly Python values"""
    if isinstance(value, pd.Series | pd.DataFrame):
        value = value.to_dict()
    if isinstance(value, np.ndarray):
        value = value.tolist()
    if isinstance(value, dict):
        return {str(k): _plain(v) for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [_plain(v) for v in value]
    if isinstance(value, np.generic):
        value = value.item()
    if isinstance(value, float) and math.isnan(value):
        return None
    return value
