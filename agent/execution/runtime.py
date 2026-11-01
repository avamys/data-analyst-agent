"""Helpers for analysis code: the dataset, facts, charts, and hand-offs between tasks.

Imported by the first cell of every task script. Reads `.analyst.json` from the
working directory (the task directory), so `python analysis.py` also works there.
"""

import json
import math
import os
import pickle
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


def save_chart(fig, name: str, caption: str) -> None:
    """Save a matplotlib figure for the report and close it"""
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
