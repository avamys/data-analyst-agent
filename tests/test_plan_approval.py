"""Plan approval: the run waits after the plan; the human's messages make the
lead answer or revise it, and the approved plan runs (scripted model)"""

import io
import json
import sys
from pathlib import Path

import pytest
from conftest import ScriptedLLM
from langgraph.types import Command
from test_lead import _brief, _plan, accept
from test_specialist import finish

from agent.cli import PlanNotApproved, run_analysis
from agent.config import settings
from agent.core.llm_manager import LLMManager
from agent.graph import build_hierarchical_graph
from agent.nodes.lead import validate_plan
from agent.run_store import load_run
from agent.states import PlanRevision

APPROVE = {"approve": True}


@pytest.fixture
def start(monkeypatch, tmp_path, small_csv):
    """Start a run with approval on; returns the graph, its config, the model
    and what the first stop shows"""

    def _start(*responses):
        monkeypatch.setattr(settings, "plan_approval", True)
        monkeypatch.setattr(settings, "max_parallel_tasks", 1)
        llm = ScriptedLLM(responses)
        monkeypatch.setattr(LLMManager, "get_llm", lambda **_: llm)
        graph = build_hierarchical_graph()
        config = {"configurable": {"thread_id": "t"}, "recursion_limit": 100}
        state = graph.invoke(
            {"dataset_info": "", "dataset_path": small_csv, "run_dir": str(tmp_path)},
            config=config,
        )
        return graph, config, llm, _shown(state)

    return _start


def _shown(state: dict) -> dict:
    """What the run shows the human while it waits"""
    (stop,) = state["__interrupt__"]
    return stop.value


def _ids(shown: dict) -> list[str]:
    return [t["id"] for t in shown["tasks"]]


def revision(*briefs, reply="done") -> PlanRevision:
    return PlanRevision(reply=reply, briefs=list(briefs))


def test_without_approval_the_plan_runs_at_once():
    assert "await_approval" not in build_hierarchical_graph().nodes


def test_the_run_waits_for_approval_then_runs_the_plan(start):
    graph, config, llm, shown = start(
        _plan(_brief("eda_1")), finish(), accept(), "the report"
    )
    assert _ids(shown) == ["eda_1"] and shown["reply"] is None
    assert len(llm.prompts) == 1  # only the plan, no task yet

    state = graph.invoke(Command(resume=APPROVE), config=config)
    assert state["plan_approved"] and state["report"] == "the report"
    assert [r.task_id for r in state["completed_tasks"]] == ["eda_1"]


def test_tasks_the_human_adds_raise_the_cap(start, monkeypatch):
    monkeypatch.setattr(settings, "max_tasks", 1)
    graph, config, llm, shown = start(
        _plan(_brief("eda_1"), _brief("eda_2")),  # the lead's own plan is capped
        revision(_brief("eda_1"), _brief("", question="fare by port"), reply="Added"),
        finish(),
        accept(),
        finish(),
        accept(),
        "the report",
    )
    assert _ids(shown) == ["eda_1"]

    state = graph.invoke(Command(resume={"message": "add fare by port"}), config)
    shown = _shown(state)
    assert _ids(shown) == ["eda_1", "eda_2"] and shown["reply"] == "Added"
    assert "add fare by port" in llm.prompts[-1]

    state = graph.invoke(Command(resume=APPROVE), config=config)
    assert [r.task_id for r in state["completed_tasks"]] == ["eda_1", "eda_2"]
    assert [(m.role, m.text) for m in state["plan_chat"]] == [
        ("human", "add fare by port"),
        ("lead", "Added"),
    ]


def test_a_removal_keeps_the_other_ids_and_later_messages_see_the_conversation(start):
    kept = (_brief("eda_1"), _brief("eda_3"))
    graph, config, llm, shown = start(
        _plan(_brief("a"), _brief("b"), _brief("c")),
        revision(*kept, reply="Removed eda_2"),
        revision(*kept, reply="Because the profile shows no missing values"),
    )
    assert _ids(shown) == ["eda_1", "eda_2", "eda_3"]

    state = graph.invoke(Command(resume={"message": "drop eda_2"}), config)
    assert _ids(_shown(state)) == ["eda_1", "eda_3"]  # not renumbered

    state = graph.invoke(
        Command(resume={"message": "why no missingness task?"}), config
    )
    assert _ids(_shown(state)) == ["eda_1", "eda_3"]  # a question changes nothing
    prompt = llm.prompts[-1]
    assert "drop eda_2" in prompt and "Removed eda_2" in prompt
    assert "why no missingness task?" in prompt


def test_a_kept_id_follows_its_specialist():
    stat = _brief("eda_2").model_copy(update={"specialist": "statistical"})
    briefs = validate_plan(
        _plan(_brief("eda_1"), stat, _brief("")), None, keep_ids={"eda_1", "eda_2"}
    )
    assert [b.id for b in briefs] == ["eda_1", "stat_1", "eda_2"]


# The CLI: replies come from stdin


def _cli_run(monkeypatch, tmp_path, small_csv, stdin: str, *responses) -> Path:
    runs = tmp_path / "runs"
    monkeypatch.setattr(settings, "runs_directory", str(runs))
    monkeypatch.setattr(settings, "plan_approval", True)
    monkeypatch.setattr(settings, "max_parallel_tasks", 1)
    monkeypatch.setattr(sys, "stdin", io.StringIO(stdin))
    llm = ScriptedLLM(responses)
    monkeypatch.setattr(LLMManager, "get_llm", lambda **_: llm)
    try:
        run_analysis(Path(small_csv), target="target")
    finally:
        (run_dir,) = [p for p in runs.iterdir() if not p.is_symlink()]
    return run_dir


def _events(run_dir: Path) -> list[dict]:
    lines = (run_dir / "progress.jsonl").read_text().splitlines()
    return [json.loads(line) for line in lines]


def test_the_cli_takes_messages_until_approve_and_records_them(
    monkeypatch, tmp_path, small_csv, capsys
):
    run_dir = _cli_run(
        monkeypatch,
        tmp_path,
        small_csv,
        "\nadd fare by port\napprove\n",  # an empty line asks again
        _plan(_brief("eda_1")),
        revision(_brief("eda_1"), _brief("", question="fare by port"), reply="Added"),
        *(finish(), accept()) * 2,
        "the report",
    )
    kinds = [e["event"] for e in _events(run_dir)]
    assert kinds[:6] == [
        "plan",
        "plan_waiting",
        "plan_message",
        "plan_revised",
        "plan_waiting",
        "plan_approved",
    ]
    assert kinds[-1] == "run_done"
    started = [e["task"] for e in _events(run_dir) if e["event"] == "task_started"]
    assert started == ["eda_1", "eda_2"]
    out = capsys.readouterr().out
    assert "Lead: Added" in out and "eda_2 (eda): fare by port" in out

    meta = json.loads((run_dir / "run_meta.json").read_text())
    assert meta["status"] == "ok" and meta["plan_approved"]
    assert [m["role"] for m in meta["plan_chat"]] == ["human", "lead"]
    assert meta["tasks_completed"] == 2
    # Numbered in order across the stops, one file per node
    names = sorted(p.name for p in (run_dir / "state").iterdir())
    assert names[:5] == [
        "01_profile.json",
        "02_plan.json",
        "03_await_approval.json",
        "04_revise_plan.json",
        "05_await_approval.json",
    ]
    assert len(names) == len(meta["nodes"])
    page = (run_dir / "report.html").read_text()
    assert "Plan review" in page and "add fare by port" in page
    # Questions after the report rebuild the state from these files
    state = load_run(run_dir)
    assert state.plan_approved and len(state.plan_chat) == 2


def test_input_closed_before_approval_ends_the_run(monkeypatch, tmp_path, small_csv):
    with pytest.raises(PlanNotApproved):
        run_dir = _cli_run(monkeypatch, tmp_path, small_csv, "", _plan(_brief("eda_1")))
    (run_dir,) = [p for p in (tmp_path / "runs").iterdir() if not p.is_symlink()]
    meta = json.loads((run_dir / "run_meta.json").read_text())
    assert meta["status"] == "failed" and meta["plan_approved"] is False
    assert "never approved" in (run_dir / "report.html").read_text()


def test_a_plan_the_human_grew_runs_past_the_default_step_limit(
    monkeypatch, tmp_path, small_csv
):
    # The default limit for 1 task allows 12 steps; 6 tasks need 15
    for name, value in (("max_tasks", 1), ("max_follow_ups", 0), ("max_revisions", 0)):
        monkeypatch.setattr(settings, name, value)
    briefs = [_brief("eda_1"), *(_brief("", question=f"q{i}") for i in range(5))]
    run_dir = _cli_run(
        monkeypatch,
        tmp_path,
        small_csv,
        "add five tasks\napprove\n",
        _plan(_brief("eda_1")),
        revision(*briefs),
        *(finish(), accept()) * 6,
        "the report",
    )
    meta = json.loads((run_dir / "run_meta.json").read_text())
    assert (meta["status"], meta["tasks_completed"]) == ("ok", 6)
