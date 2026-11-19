"""CI grades the committed eval suites: their snapshots (evals/snapshots/) must
grade exactly as their results files record, with no LLM calls and no API keys"""

import json

import pytest

from evals.cases import load_case
from evals.graders import grade
from evals.judge import scores
from evals.report import suite_table
from evals.runner import RESULTS_DIR, snapshot_path

SUITES = [
    results
    for results in sorted(RESULTS_DIR.glob("*.jsonl"))
    if snapshot_path(
        json.loads(results.read_text().splitlines()[0])["run_dir"]
    ).parent.exists()
]


def without_cost(grades: dict) -> dict:
    return {k: v for k, v in grades.items() if k != "cost_usd"}  # needs the calls


def test_there_is_a_committed_suite_to_grade():
    assert SUITES


@pytest.mark.parametrize("results", SUITES, ids=lambda p: p.stem)
def test_a_committed_suite_grades_as_recorded(results):
    lines = [json.loads(x) for x in results.read_text().splitlines()]
    for line in lines:
        graded = grade(load_case(line["case"]), snapshot_path(line["run_dir"]))
        assert without_cost(graded) == without_cost(line["grades"]), line["case"]
        if (judge := line.get("judge")) and not judge.get("error"):
            assert scores(judge) == judge["scores"], line["case"]
    assert "| **Overall** |" in suite_table(lines, results.stem)
