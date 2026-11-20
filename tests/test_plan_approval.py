"""Plan approval: the run waits after the plan; the human's messages make the
lead answer or revise it, and the approved plan runs (scripted model)"""

import pytest
from conftest import ScriptedLLM
from langgraph.types import Command
from test_lead import _brief, _plan, accept
from test_specialist import finish

from agent.config import settings
from agent.core.llm_manager import LLMManager
from agent.graph import build_hierarchical_graph
from agent.nodes.lead import validate_plan
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
