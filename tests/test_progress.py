import json
import threading
from pathlib import Path

from conftest import ScriptedLLM
from test_lead import _brief, _plan, _RoutedLLM, accept, revise
from test_specialist import finish, run_cell

from agent.cli import run_analysis
from agent.config import settings
from agent.core.llm_manager import LLMManager


def _run(monkeypatch, tmp_path, small_csv, llm) -> tuple[Path, list[dict]]:
    monkeypatch.setattr(settings, "runs_directory", str(tmp_path / "runs"))
    monkeypatch.setattr(LLMManager, "get_llm", lambda **_: llm)
    run_dir = run_analysis(Path(small_csv))
    lines = (run_dir / "progress.jsonl").read_text().splitlines()
    return run_dir, [json.loads(line) for line in lines]


def test_a_run_writes_its_progress_in_order(monkeypatch, tmp_path, small_csv, capsys):
    monkeypatch.setattr(settings, "max_parallel_tasks", 1)
    llm = ScriptedLLM(
        [
            _plan(_brief("eda_1")),
            run_cell("record_fact('n', len(df), 'Rows')"),
            finish("n"),
            revise("Also record m."),
            run_cell("df['missing']"),
            run_cell("record_fact('m', 2, 'Two')"),
            finish("n", "m"),
            accept(),
            "the report",
        ]
    )
    run_dir, events = _run(monkeypatch, tmp_path, small_csv, llm)
    assert [e["event"] for e in events] == [
        "plan",
        "task_started",
        "step",
        "task_finished",
        "reviewed",
        "task_started",
        "step",
        "step",
        "task_finished",
        "reviewed",
        "report",
        "run_done",
    ]
    assert events[0]["tasks"][0]["id"] == "eda_1"
    assert (events[4]["outcome"], events[4]["feedback"]) == ("revise", "Also record m.")
    assert events[5]["revision"] == 1
    assert events[6]["error"] == "KeyError: 'missing'"
    assert (events[8]["status"], events[8]["findings"]) == ("complete", 1)
    assert events[9]["outcome"] == "completed"
    assert events[-1]["report"] == str(run_dir / "report.html")

    printed = capsys.readouterr().out
    assert "↺ eda_1 sent back: Also record m." in printed
    assert "eda_1 step 1: cell error: KeyError: 'missing'" in printed
    assert "✓ eda_1 accepted" in printed
    assert "Done in 0m" in printed


def test_tasks_run_in_parallel_threads_report_their_progress(
    monkeypatch, tmp_path, small_csv
):
    monkeypatch.setattr(settings, "max_parallel_tasks", 2)
    second_started = threading.Event()

    def work(task_id):
        if task_id == "eda_2":
            second_started.set()
        if task_id == "eda_1":
            assert second_started.wait(timeout=10)  # eda_2 runs alongside
        return finish()

    llm = _RoutedLLM(_plan(_brief("eda_1"), _brief("eda_2")), work)
    _, events = _run(monkeypatch, tmp_path, small_csv, llm)
    started = {e["task"] for e in events if e["event"] == "task_started"}
    finished = [e["task"] for e in events if e["event"] == "task_finished"]
    assert started == {"eda_1", "eda_2"}
    assert finished == ["eda_1", "eda_2"]
