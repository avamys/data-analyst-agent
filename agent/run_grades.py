"""Run-level grades from a run directory, no LLM: whether the run worked, its
tasks, tokens and cost, and what the checks left open (numbers no fact backs,
revisions, objections the lead still had, follow-up tasks). Every run records
them in run_meta.json; the eval graders (evals/graders.py) add the
case-specific ones. None where the baseline agent has no such record.
"""

import json
from pathlib import Path

from agent.costs import estimate_cost, openrouter_id, summarize_calls


def run_grades(run_dir: Path, prices: dict | None = None) -> dict:
    """prices: OpenRouter's (agent/costs.py), for the cost; None leaves it empty"""
    meta = _json(run_dir / "run_meta.json") or {}
    report = run_dir / "report.md"
    return {
        "run_ok": meta.get("status") == "ok"
        and report.exists()
        and bool(report.read_text()),
        "tasks_completed": meta.get("tasks_completed"),
        "tasks_failed": meta.get("tasks_failed"),
        "llm_calls": meta.get("llm_calls"),
        "input_tokens": meta.get("input_tokens"),
        "output_tokens": meta.get("output_tokens"),
        "cost_usd": _cost(run_dir, prices),
        **_review_grades(run_dir, meta),
    }


def _review_grades(run_dir: Path, meta: dict) -> dict:
    results = [_json(p) for p in sorted(run_dir.glob("tasks/*/result.json"))]
    if not results or "reviews" not in results[0]:  # the baseline has no reviews
        return dict.fromkeys(
            ("unverified_numbers", "revisions", "unresolved_objections", "follow_ups")
        )
    plan = next(iter(sorted(run_dir.glob("state/*_plan.json"))), None)
    planned = (
        {b["id"] for b in (_json(plan) or {}).get("backlog", [])} if plan else set()
    )
    return {
        "unverified_numbers": len(meta.get("unverified_numbers") or []),
        "revisions": sum(r["revisions"] for r in results),
        "unresolved_objections": sum(
            1
            for r in results
            if r["reviews"] and r["reviews"][-1]["verdict"] == "revise"
        ),
        "follow_ups": sum(1 for r in results if r["task_id"] not in planned),
    }


def _cost(run_dir: Path, prices: dict | None) -> float | None:
    calls = run_dir / "llm_calls.jsonl"
    if not prices or not calls.exists():
        return None
    model = next((json.loads(line).get("model") for line in calls.open()), None)
    price = prices.get(openrouter_id(model)) if model else None
    if price is None:
        return None
    return round(estimate_cost(summarize_calls(calls)["total"], price), 5)


def _json(path: Path) -> dict | None:
    return json.loads(path.read_text()) if path and path.exists() else None
