"""Token totals and cost of a run, from its llm_calls.jsonl, at OpenRouter's list
prices. Used by the run grades (agent/run_grades.py), scripts/run_cost.py and the
eval graders."""

import json
import re
from collections import Counter
from pathlib import Path

import httpx

from agent.run_store import CUT_OFF

MODELS_URL = "https://openrouter.ai/api/v1/models"
FIELDS = ("calls", "input", "output", "reasoning", "seconds")
# Ollama only: where a call's seconds went
PHASES = ("load_seconds", "prompt_seconds", "generation_seconds")
HEALTH = ("cut_off", "window_full", "empty")


def summarize_calls(path: Path) -> dict[str, dict[str, float]]:
    """Totals per node (in call order), plus a "total" row"""
    nodes: dict[str, dict[str, float]] = {}
    for line in path.open():
        call = json.loads(line)
        row = nodes.setdefault(
            call.get("node") or "?", dict.fromkeys(FIELDS + PHASES + HEALTH, 0)
        )
        row["calls"] += 1
        row["input"] += call.get("input_tokens") or 0
        row["output"] += call.get("output_tokens") or 0
        row["reasoning"] += call.get("reasoning_tokens") or 0
        row["seconds"] += call.get("seconds") or 0
        for phase in PHASES:
            row[phase] += call.get(phase) or 0
        row["window_full"] += bool(call.get("window_full"))
        row["cut_off"] += call.get("stop_reason") in CUT_OFF and not call.get(
            "window_full"
        )
        row["empty"] += bool(call.get("empty"))
    nodes["total"] = {
        f: sum(row[f] for row in nodes.values()) for f in FIELDS + PHASES + HEALTH
    }
    return nodes


def run_model(path: Path) -> str | None:
    """The model most calls of a run went to"""
    models = Counter(json.loads(line).get("model") for line in path.open())
    return models.most_common(1)[0][0] if models else None


def openrouter_id(model: str) -> str:
    """Anthropic API ids (claude-haiku-5-5) as OpenRouter names them"""
    if model.startswith("claude-"):
        return "anthropic/" + re.sub(r"-(\d+)-(\d+)$", r"-\1.\2", model)
    return model


def estimate_cost(total: dict[str, float], price: dict[str, str]) -> float:
    """USD for the run's tokens at a model's per-token prices"""
    return total["input"] * float(price["prompt"]) + total["output"] * float(
        price["completion"]
    )


def fetch_prices() -> dict | None:
    """OpenRouter list prices per model; None offline (costs are left empty)"""
    try:
        models = httpx.get(MODELS_URL, timeout=20).json()["data"]
    except (httpx.HTTPError, KeyError, ValueError):
        return None
    return {m["id"]: m["pricing"] for m in models}
