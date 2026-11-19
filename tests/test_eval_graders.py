import json

import pytest

from evals.cases import Fact, load_case
from evals.graders import fact_stated, grade

TITANIC = load_case("titanic")
PRICES = {
    "anthropic/claude-haiku-5.5": {"prompt": "0.0000001", "completion": "0.0000005"}
}


@pytest.mark.parametrize(
    ("line", "value", "near", "stated"),
    [
        ("Survival was 38.4% overall.", 0.383838, ["surviv"], True),
        ("Survival was 0.38 overall.", 0.383838, ["surviv"], True),  # rounded
        ("Survival was 38.5% overall.", 0.383838, ["surviv"], False),  # wrong value
        ("38.4% of passengers.", 0.383838, ["surviv"], False),  # no keyword on the line
        ("Age is missing for 177 passengers.", 177, ["Age"], True),
        ("The median price is 217,450.", 217450, ["median"], True),
    ],
)
def test_a_fact_is_its_value_next_to_a_keyword(line, value, near, stated):
    report = f"# Report\n\nOther text with 12.5 in it.\n{line}\n"
    assert fact_stated(report, Fact(name="f", value=value, near=near)) is stated


def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(obj if isinstance(obj, str) else json.dumps(obj))


def result(task_id, *verdicts, revisions=0):
    reviews = [{"verdict": v} for v in verdicts]
    return {"task_id": task_id, "reviews": reviews, "revisions": revisions}


@pytest.fixture
def current_run(tmp_path):
    """A Phase 1 run: one planned task revised once, one follow-up left unresolved"""
    meta = {"status": "ok", "tasks_completed": 2, "tasks_failed": 0, "llm_calls": 9}
    write(tmp_path / "run_meta.json", {**meta, "unverified_numbers": ["41"]})
    write(tmp_path / "report.md", "Survival was 38.4%.\nCabin is mostly missing.\n")
    write(tmp_path / "state/02_plan.json", {"backlog": [{"id": "eda_1"}]})
    write(
        tmp_path / "tasks/eda_1/result.json",
        result("eda_1", "revise", "accept", revisions=1),
    )
    write(
        tmp_path / "tasks/eda_2/result.json",
        result("eda_2", "revise", "revise", revisions=1),
    )
    call = {"model": "claude-haiku-5-5", "input_tokens": 1_000_000, "output_tokens": 0}
    write(tmp_path / "llm_calls.jsonl", json.dumps(call) + "\n")
    return tmp_path


def test_grades_of_a_phase_1_run(current_run):
    g = grade(TITANIC, current_run, PRICES)
    assert g["run_ok"] and g["llm_calls"] == 9
    assert g["facts_stated"] == ["survival_rate"]
    assert g["fact_recall"] == pytest.approx(1 / len(TITANIC.facts))
    assert g["caveats_stated"] == ["missing_cabin"]
    assert g["cost_usd"] == pytest.approx(0.1)  # 1M input tokens at $0.10/M
    assert (g["revisions"], g["unresolved_objections"], g["follow_ups"]) == (2, 1, 1)
    assert g["unverified_numbers"] == 1


def test_without_prices_the_cost_is_left_empty(current_run):
    assert grade(TITANIC, current_run)["cost_usd"] is None


def test_the_baseline_has_no_review_grades(tmp_path):
    write(tmp_path / "run_meta.json", {"status": "ok"})
    write(tmp_path / "report.md", "# Report")
    write(tmp_path / "tasks/eda_1/result.json", {"task_id": "eda_1", "success": True})
    g = grade(TITANIC, tmp_path)
    assert g["run_ok"]
    assert g["revisions"] is None and g["unverified_numbers"] is None


def test_a_run_without_a_report_is_not_ok(tmp_path):
    write(tmp_path / "run_meta.json", {"status": "ok"})
    assert not grade(TITANIC, tmp_path)["run_ok"]
