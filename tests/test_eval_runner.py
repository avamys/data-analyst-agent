import json

import pytest

from evals import runner
from evals.cases import load_case
from evals.runner import Config, command, run_one, run_suite

CASE = load_case("pure_noise")


def fake_run(meta: dict | None, exit_code: int | None = 0, report=True):
    """Stands in for _execute: writes a run directory the way run.py does"""

    def _execute(cmd, cwd, env, log, timeout_s):
        log.write_text("output")
        if meta is not None:
            run_dir = log.parent / "20261102-120000_pure_noise_m"
            run_dir.mkdir()
            (run_dir / "run_meta.json").write_text(json.dumps(meta))
            if report:
                (run_dir / "report.md").write_text("# Report")
        return exit_code

    return _execute


@pytest.fixture
def dirs(monkeypatch, tmp_path):
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    monkeypatch.setattr(runner, "RUNS_DIR", tmp_path / "runs")
    monkeypatch.setattr(runner, "RESULTS_DIR", tmp_path / "results")
    monkeypatch.setattr(runner, "version_id", lambda version: "abc123")
    monkeypatch.setattr(runner, "dataset", lambda case: tmp_path / "data.csv")
    return tmp_path


def test_commands_per_version(tmp_path):
    def args(config):
        cmd = command(config, CASE, tmp_path / "d.csv")
        return cmd[cmd.index("--target") :]

    current = Config("current", "anthropic", "m", preset="hosted")
    assert args(current) == [
        "--target", "outcome", "--model", "m",
        "--provider", "anthropic", "--preset", "hosted",
    ]  # fmt: skip
    # The baseline has no --provider or --preset; it reads MODEL_PROVIDER
    baseline = Config("baseline", "anthropic", "m", preset="hosted")
    assert args(baseline) == ["--target", "outcome", "--model", "m"]


def test_a_finished_run_is_read_from_its_run_meta(monkeypatch, dirs):
    meta = {"status": "ok", "llm_calls": 47, "tasks_completed": 7, "tasks_failed": 0}
    monkeypatch.setattr(runner, "_execute", fake_run(meta))
    line = run_one(Config("current", "anthropic", "m"), CASE, 1, dirs / "s", dirs)
    assert line["status"] == "ok" and line["has_report"]
    assert (line["llm_calls"], line["tasks_completed"]) == (47, 7)
    assert line["run_dir"] == "s/pure_noise/r1/20261102-120000_pure_noise_m"


@pytest.mark.parametrize(
    ("meta", "exit_code", "status"),
    [
        ({"status": "running"}, None, "timeout"),
        (None, 1, "crashed"),  # died before run.py wrote run_meta.json
        ({"status": "failed"}, 1, "failed"),
    ],
)
def test_failures_are_results(monkeypatch, dirs, meta, exit_code, status):
    monkeypatch.setattr(runner, "_execute", fake_run(meta, exit_code, report=False))
    line = run_one(Config("current", "anthropic", "m"), CASE, 1, dirs / "s", dirs)
    assert line["status"] == status and not line["has_report"]


def test_a_suite_writes_one_line_per_case_and_repeat(monkeypatch, dirs):
    monkeypatch.setattr(runner, "_execute", fake_run({"status": "ok"}))
    monkeypatch.setattr(runner, "checkout", lambda version: dirs)
    cases = [CASE, load_case("leakage")]
    results = run_suite(Config("current", "anthropic", "m", repeats=2, jobs=2), cases)
    lines = [json.loads(line) for line in results.read_text().splitlines()]
    assert sorted((x["case"], x["repeat"]) for x in lines) == [
        ("leakage", 1),
        ("leakage", 2),
        ("pure_noise", 1),
        ("pure_noise", 2),
    ]
