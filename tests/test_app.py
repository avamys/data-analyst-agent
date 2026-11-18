import json
import os

import pytest

from agent.config import settings
from app.runs import list_runs, read_events, task_rows


def _brief(task_id):
    return {"id": task_id, "specialist": "eda", "question": f"q {task_id}"}


def test_read_events_skips_a_line_still_being_written(tmp_path):
    (tmp_path / "progress.jsonl").write_text('{"event": "plan", "tasks": []}\n{"ev')
    assert read_events(tmp_path) == [{"event": "plan", "tasks": []}]
    assert read_events(tmp_path / "missing") == []


def test_task_rows_follow_each_task_through_review():
    events = [
        {"event": "plan", "tasks": [_brief("eda_1"), _brief("eda_2")]},
        {"event": "task_started", "task": "eda_1", "revision": 0},
        {"event": "step", "task": "eda_1", "error": "KeyError: 'x'"},
        {"event": "step", "task": "eda_1", "error": None},
        {"event": "task_finished", "task": "eda_1", "findings": 2},
        {"event": "reviewed", "task": "eda_1", "outcome": "revise", "follow_ups": []},
        {"event": "task_started", "task": "eda_1", "revision": 1},
        {"event": "task_finished", "task": "eda_1", "findings": 3},
        {
            "event": "reviewed",
            "task": "eda_1",
            "outcome": "completed",
            "follow_ups": [_brief("eda_3")],
        },
    ]
    rows = {r["task"]: r for r in task_rows(events)}
    assert list(rows) == ["eda_1", "eda_2", "eda_3"]
    first = rows["eda_1"]
    assert (first["state"], first["cells"], first["errors"]) == ("accepted", 2, 1)
    assert (first["findings"], first["revisions"]) == (3, 1)
    assert task_rows(events[:6])[0]["state"] == "sent back"
    assert rows["eda_2"]["state"] == "waiting"
    assert rows["eda_3"]["follow-up"] is True


def _run(root, name, started, **meta):
    run = root / name
    run.mkdir(parents=True)
    meta = {"status": "ok", "started": started, "seconds": 120, **meta}
    (run / "run_meta.json").write_text(json.dumps(meta))
    return run


def test_list_runs_finds_runs_at_any_depth_newest_first(tmp_path):
    _run(tmp_path, "a", "2026-11-17T10:00:00")
    newer = _run(tmp_path, "suite/case/r1/b", "2026-11-18T10:00:00")
    os.symlink(newer, tmp_path / "suite/case/r1/latest")
    runs = list_runs(tmp_path)
    assert [r["name"] for r in runs] == ["b", "a"]
    assert (runs[0]["minutes"], runs[0]["report"]) == (2.0, False)


def test_the_app_opens_a_past_run(monkeypatch, tmp_path):
    run = _run(tmp_path, "20261118-120000_small_m", "2026-11-18T12:00:00")
    (run / "report.md").write_text("# The report\n\nSurvival was 38%.")
    monkeypatch.setattr(settings, "runs_directory", str(tmp_path))
    testing = pytest.importorskip("streamlit.testing.v1")  # the ui group
    app = testing.AppTest.from_file("../app/streamlit_app.py", default_timeout=30)
    app.run()
    assert not app.exception
    assert app.title[0].value == "Analyse a CSV"
    app.sidebar.radio[0].set_value("Past runs").run()
    assert not app.exception
    assert app.selectbox[0].value == run
