import json
import os

import pytest

from agent.config import settings
from app.runs import list_runs, plan_chat, read_events, stage, task_rows, waiting_plan


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


def test_stage_names_the_steps_without_a_task():
    assert stage([]).startswith("Profiling")
    plan = {"event": "plan", "tasks": [_brief("eda_1")]}
    assert stage([plan]) is None
    done = {"event": "reviewed", "task": "eda_1", "outcome": "completed"}
    assert "writing the report" in stage([plan, done])


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


def test_hosted_runs_get_the_hosted_preset(monkeypatch, tmp_path):
    pytest.importorskip("streamlit")
    import subprocess

    from app import streamlit_app

    commands = []
    monkeypatch.setattr(
        subprocess, "Popen", lambda command, **_: commands.append(command)
    )
    for provider in ("anthropic", "ollama"):
        streamlit_app.launch(tmp_path / "a.csv", None, provider, "m", tmp_path)
    assert commands[0][-2:] == ["--preset", "hosted"]
    assert "--preset" not in commands[1]


def test_a_questions_tasks_and_stages():
    asked = {"event": "asked", "number": 1, "facts": [], "tasks": [_brief("q1_eda_1")]}
    question = {"event": "question", "number": 1, "question": "q"}
    assert "reading the question" in stage([question])
    done = {"event": "reviewed", "task": "q1_eda_1", "outcome": "completed"}
    assert [r["task"] for r in task_rows([question, asked])] == ["q1_eda_1"]
    assert "writing the answer" in stage([question, asked, done])
    from_facts = {**asked, "facts": ["eda_1.n"], "tasks": []}
    assert "recorded facts answer it" in stage([question, from_facts])


def test_the_app_shows_answers_and_asks_a_question(monkeypatch, tmp_path):
    run = _run(tmp_path, "20261118-120000_small_m", "2026-11-18T12:00:00")
    (run / "report.md").write_text("# The report\n\nSurvival was 38%.")
    (run / "questions.md").write_text(
        "## Questions after the report\n\n### Q1. Why?\n\nBecause.\n"
    )
    monkeypatch.setattr(settings, "runs_directory", str(tmp_path))
    testing = pytest.importorskip("streamlit.testing.v1")
    import subprocess

    commands = []

    class Running:
        def poll(self):
            return None

    def popen(command, **_):
        commands.append(command)
        return Running()

    monkeypatch.setattr(subprocess, "Popen", popen)
    app = testing.AppTest.from_file("../app/streamlit_app.py", default_timeout=30)
    app.run()
    app.sidebar.radio[0].set_value("Past runs").run()
    app.text_area[0].input("Does it hold for women?")
    app.button[0].click().run()  # the form's Ask button
    assert not app.exception
    assert commands[0][-3:] == ["ask", str(run.resolve()), "Does it hold for women?"]
    assert app.info[0].value == "Loading the run…"


# Plan review


def _waiting(tasks, reply=None):
    full = [{**t, "depends_on": []} for t in tasks]
    return {"event": "plan_waiting", "tasks": full, "reply": reply}


def test_the_plan_waits_and_a_revision_replaces_the_task_list():
    plan = {"event": "plan", "tasks": [_brief("eda_1"), _brief("eda_2")]}
    message = {"event": "plan_message", "text": "drop eda_2, add fare"}
    revised = {
        "event": "plan_revised",
        "tasks": [_brief("eda_1"), _brief("eda_3")],
        "reply": "Dropped eda_2, added eda_3",
    }
    events = [plan, _waiting(plan["tasks"]), message]
    assert waiting_plan(events, answered=1) is None  # answered, not shown again
    assert "reading your message" in stage(events)
    events += [revised, _waiting(revised["tasks"], revised["reply"])]
    assert waiting_plan(events, answered=1)["reply"] == "Dropped eda_2, added eda_3"
    assert [r["task"] for r in task_rows(events)] == ["eda_1", "eda_3"]
    assert plan_chat(events) == [
        ("human", "drop eda_2, add fare"),
        ("lead", "Dropped eda_2, added eda_3"),
    ]
    assert waiting_plan([plan]) is None


def test_the_app_shows_the_waiting_plan_and_sends_the_approval(monkeypatch, tmp_path):
    testing = pytest.importorskip("streamlit.testing.v1")
    import io

    run = tmp_path / "20261120-120000_small_m"
    run.mkdir()
    tasks = [_brief("eda_1")]
    events = [{"event": "plan", "tasks": tasks}, _waiting(tasks)]
    (run / "progress.jsonl").write_text("".join(json.dumps(e) + "\n" for e in events))
    log = tmp_path / "console.log"
    log.write_text(f"Run directory: {run} (anthropic, m)\n")

    class Waiting:
        stdin = io.StringIO()

        def poll(self):
            return None

    process = Waiting()
    monkeypatch.setattr(settings, "runs_directory", str(tmp_path))
    app = testing.AppTest.from_file("../app/streamlit_app.py", default_timeout=30)
    app.session_state["launched"] = {"process": process, "log": log, "started": 0}
    app.run()
    assert not app.exception
    assert app.subheader[0].value == "The plan, waiting for your approval"
    assert list(app.dataframe[0].value["task"]) == ["eda_1"]
    app.button[0].click().run()  # Approve and run
    assert not app.exception
    assert process.stdin.getvalue() == "approve\n"
    assert app.session_state["launched"]["answered"] == 1


def test_plan_review_reaches_the_command_and_keeps_stdin(monkeypatch, tmp_path):
    pytest.importorskip("streamlit")
    import subprocess

    from app import streamlit_app

    calls = []
    monkeypatch.setattr(
        subprocess, "Popen", lambda command, **kw: calls.append((command, kw))
    )
    streamlit_app.launch(tmp_path / "a.csv", None, "anthropic", "m", tmp_path, True)
    streamlit_app.launch(tmp_path / "a.csv", None, "anthropic", "m", tmp_path)
    (on, on_kw), (off, off_kw) = calls
    assert "--approve-plan" in on and on_kw["stdin"] is subprocess.PIPE
    assert "--approve-plan" not in off and off_kw["stdin"] is None
