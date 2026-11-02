"""Deterministic graders: read a finished run directory, no LLM

Shared by both versions: run success, tasks, LLM calls, tokens, cost, the case's
expected facts in the report text, required caveats. Phase 1 agent only (None
for the baseline, which has no reviews or number check): numbers the check left
unverified, revisions, objections left unresolved, follow-up tasks.
"""

import json
from pathlib import Path

import httpx

from agent.number_check import numbers_in
from evals.cases import Case, Fact
from scripts.run_cost import estimate_cost, openrouter_id, summarize_calls

PRICES_URL = "https://openrouter.ai/api/v1/models"


def fetch_prices() -> dict | None:
    """OpenRouter list prices per model; None offline (costs are left empty)"""
    try:
        models = httpx.get(PRICES_URL, timeout=20).json()["data"]
    except (httpx.HTTPError, KeyError, ValueError):
        return None
    return {m["id"]: m["pricing"] for m in models}


def grade(case: Case, run_dir: Path, prices: dict | None = None) -> dict:
    """Every deterministic grade of one run; prices: OpenRouter's, for the cost"""
    meta = _json(run_dir / "run_meta.json") or {}
    report_file = run_dir / "report.md"
    report = report_file.read_text() if report_file.exists() else ""
    facts = [f.name for f in case.facts if fact_stated(report, f)]
    caveats = [
        name
        for name, keywords in case.caveats.items()
        if any(k.lower() in report.lower() for k in keywords)
    ]
    return {
        "run_ok": meta.get("status") == "ok" and bool(report),
        "tasks_completed": meta.get("tasks_completed"),
        "tasks_failed": meta.get("tasks_failed"),
        "llm_calls": meta.get("llm_calls"),
        "input_tokens": meta.get("input_tokens"),
        "output_tokens": meta.get("output_tokens"),
        "cost_usd": _cost(run_dir, prices),
        "facts_stated": facts,
        "fact_recall": len(facts) / len(case.facts) if case.facts else None,
        "caveats_stated": caveats,
        **_review_grades(run_dir, meta),
    }


def fact_stated(report: str, fact: Fact) -> bool:
    """The value appears, rounded as written, on a line with one of the keywords"""
    keywords = [k.lower() for k in fact.near]
    target = abs(fact.value)
    for _, number, tol, line in numbers_in(report):
        if not any(k in line.lower() for k in keywords):
            continue
        slack = tol + 1e-9 * number
        if abs(target - number) <= slack or abs(target * 100 - number) <= slack:
            return True
    return False


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
