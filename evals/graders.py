"""Deterministic graders: read a finished run directory, no LLM

Shared by both versions: the run-level grades (agent/run_grades.py: run
success, tasks, LLM calls, tokens, cost; for the Phase 1 agent also numbers the
check left unverified, revisions, objections left unresolved, follow-up tasks),
plus the case's expected facts in the report text and required caveats.
"""

from pathlib import Path

from agent.number_check import numbers_in
from agent.run_grades import run_grades
from evals.cases import Case, Fact


def grade(case: Case, run_dir: Path, prices: dict | None = None) -> dict:
    """Every deterministic grade of one run; prices: OpenRouter's, for the cost"""
    report_file = run_dir / "report.md"
    report = report_file.read_text() if report_file.exists() else ""
    facts = [f.name for f in case.facts if fact_stated(report, f)]
    caveats = [
        name
        for name, keywords in case.caveats.items()
        if any(k.lower() in report.lower() for k in keywords)
    ]
    return {
        **run_grades(run_dir, prices),
        "facts_stated": facts,
        "fact_recall": len(facts) / len(case.facts) if case.facts else None,
        "caveats_stated": caveats,
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
