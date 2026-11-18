import json
from pathlib import Path

from conftest import ScriptedLLM
from test_lead import _brief, _plan, accept
from test_specialist import finish

from agent.cli import apply_flags, build_parser, run_analysis
from agent.config import settings
from agent.core.llm_manager import LLMManager

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
    meta = json.loads((run_dir / "run_meta.json").read_text())
    assert (meta["status"], meta["tasks_completed"]) == ("ok", 1)
