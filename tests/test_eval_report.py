import json

import pytest

from evals.judge import PROMPT_VERSION
from evals.report import compare, load, overall, per_case, suite_table, values


def line(case="leakage", repeat=1, findings=1.0, claims=0.0, facts=1.0, **extra):
    """A result line as the runner and judge write it"""
    return {
        "case": case,
        "repeat": repeat,
        "version": "current",
        "model": "m",
        "preset": None,
        "code": "abc123",
        "seconds": 600,
        "has_report": True,
        "trace_url": f"https://smith/{case}/{repeat}",
        "grades": {"run_ok": True, "fact_recall": facts, "cost_usd": 0.05},
        "judge": {
            "model": "j",
            "prompt": PROMPT_VERSION,
            "scores": {
                "finding_recall": findings,
                "false_claims": claims,
                "caveat_coverage": 1.0,
            },
        },
        **extra,
    }


def write(path, lines):
    path.write_text("".join(json.dumps(x) + "\n" for x in lines))
    return path


def test_a_run_without_a_report_found_nothing():
    failed = {**line(), "has_report": False, "judge": None}
    failed["grades"] = {"run_ok": False, "fact_recall": 0.0}
    v = values(failed)
    assert (v["run_ok"], v["finding_recall"], v["caveat_coverage"]) == (0, 0, 0)
    assert v["false_claims"] is None  # not counted: there is nothing to check
    # pure_noise has no caveats: none to miss
    assert values({**failed, "case": "pure_noise"})["caveat_coverage"] is None


def test_cases_get_every_repeat_and_overall_the_mean_per_repeat():
    lines = [
        line("leakage", 1, findings=1.0),
        line("leakage", 2, findings=0.6),
        line("titanic", 1, findings=0.5),
        line("titanic", 2, findings=0.7),
    ]
    assert per_case(lines)["leakage"]["finding_recall"] == [1.0, 0.6]
    assert overall(lines)["finding_recall"] == pytest.approx([0.75, 0.65])


def test_the_table_shows_min_max_traces_and_the_rubric():
    lines = [line(repeat=1, findings=1.0), line(repeat=2, findings=0.6)]
    table = suite_table(lines, "suite")
    assert "| leakage | 100% | 80% (60%–100%) |" in table
    assert "[r1](https://smith/leakage/1) [r2](https://smith/leakage/2)" in table
    assert "7 cases" not in table and "1 cases × 2 repeats" in table
    assert "re-judge" not in table
    stale = [line(judge={"model": "j", "prompt": "old", "scores": {}})]
    assert "re-judge to update" in suite_table(stale, "suite")


def test_compare_shows_deltas_and_the_cases_that_got_worse(tmp_path):
    a = write(tmp_path / "a.jsonl", [line("leakage"), line("titanic", findings=0.5)])
    b = write(
        tmp_path / "b.jsonl",
        [line("leakage", findings=0.8, claims=1.0), line("titanic", findings=1.0)],
    )
    text = compare(a, b)
    assert "| Findings | 75% | 90% | +15% |" in text
    assert "- leakage: Findings 100% → 80%" in text
    assert "- leakage: False claims 0.0 → 1.0" in text
    assert "titanic:" not in text  # better, not worse


def test_slow_local_runs_and_cut_off_calls_are_flagged(tmp_path):
    def local(repeat, tok_s, **extra):
        ollama = {"generation_tokens": tok_s * 100, "generation_seconds": 100}
        return line(repeat=repeat, ollama=ollama, **extra)

    path = write(
        tmp_path / "r.jsonl",
        [
            local(1, 10),
            local(2, 11),
            {**local(3, 3), "seconds": 6000},  # asleep: 3 tok/s < half of 10
            local(4, 10, calls_cut_off=2, calls_empty=1),
        ],
    )
    lines = load(path)
    assert [x["slow"] for x in lines] == [False, False, True, False]
    assert values(lines[2])["minutes"] is None  # left out, so it doesn't skew
    table = suite_table(lines, "suite")
    assert "| 10.0 |" in table  # the Minutes cell: 600 s for the three others
    assert "calls cut off at the output cap: leakage r4 (2)" in table
    assert "empty replies: leakage r4 (1)" in table
    assert "left out of Minutes: leakage r3 (3.0 tok/s)" in table


def test_hosted_runs_are_never_slow(tmp_path):
    [hosted] = load(write(tmp_path / "r.jsonl", [line()]))
    assert hosted["slow"] is False and "Generating below" not in suite_table(
        [hosted], "suite"
    )
