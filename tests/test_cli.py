import json
from pathlib import Path

import pytest
from conftest import ScriptedLLM
from test_lead import _brief, _plan, accept
from test_specialist import finish

from agent.cli import apply_flags, build_parser, run_analysis
from agent.config import settings
from agent.core.llm_manager import LLMManager
from agent.core.specialists import SpecialistAgent

CHANGED = (
    "preset",
    "max_follow_ups",
    "max_revisions",
    "max_tasks",
    "model_provider",
    "analyst_model",
    "coder_model",
    "reporter_model",
    "runs_directory",
)


def test_flags_override_the_preset_and_settings(monkeypatch, tmp_path):
    for name in CHANGED:  # restored after the test
        monkeypatch.setattr(settings, name, getattr(settings, name))
    args = build_parser().parse_args(
        ["run", "data.csv", "--preset", "hosted", "--provider", "ollama"]
        + ["--model", "m", "--max-tasks", "3", "--out", str(tmp_path)]
    )
    apply_flags(args)
    assert (settings.preset, settings.max_revisions) == ("hosted", 2)
    assert (settings.model_provider, settings.max_tasks) == ("ollama", 3)
    assert settings.analyst_model == settings.coder_model == "m"
    assert settings.reporter_model == "m"
    assert settings.runs_directory == str(tmp_path)


def test_a_run_returns_its_directory_with_the_report(monkeypatch, tmp_path, small_csv):
    monkeypatch.setattr(settings, "runs_directory", str(tmp_path / "runs"))
    llm = ScriptedLLM([_plan(_brief("eda_1")), finish(), accept(), "the report"])
    monkeypatch.setattr(LLMManager, "get_llm", lambda **_: llm)
    run_dir = run_analysis(Path(small_csv), target="target")
    assert run_dir.parent == tmp_path / "runs"
    assert (run_dir / "report.md").read_text() == "the report"
    assert "<p>the report</p>" in (run_dir / "report.html").read_text()
    meta = json.loads((run_dir / "run_meta.json").read_text())
    assert (meta["status"], meta["tasks_completed"]) == ("ok", 1)
    grades = meta["grades"]
    assert grades["run_ok"] and grades["tasks_completed"] == 1
    assert grades["cost_usd"] is None  # a local model: not priced
    assert (grades["revisions"], grades["unresolved_objections"]) == (0, 0)


def test_a_failed_run_is_graded_and_its_end_recorded(monkeypatch, tmp_path, small_csv):
    runs = tmp_path / "runs"
    monkeypatch.setattr(settings, "runs_directory", str(runs))
    llm = ScriptedLLM([_plan(_brief("eda_1"))])
    monkeypatch.setattr(LLMManager, "get_llm", lambda **_: llm)

    def crash(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(SpecialistAgent, "execute", crash)
    with pytest.raises(RuntimeError, match="boom"):
        run_analysis(Path(small_csv))
    (run_dir,) = [p for p in runs.iterdir() if not p.is_symlink()]
    meta = json.loads((run_dir / "run_meta.json").read_text())
    assert meta["status"] == "failed" and meta["grades"]["run_ok"] is False
    last = json.loads((run_dir / "progress.jsonl").read_text().splitlines()[-1])
    assert (last["event"], last["status"]) == ("run_done", "failed")
