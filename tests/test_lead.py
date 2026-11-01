"""The lead's plan validation and the plan → run → review loop, with a scripted model"""

import pytest
from conftest import ScriptedLLM
from test_specialist import finish, run_cell

from agent.config import settings
from agent.core.llm_manager import LLMManager
from agent.core.specialists import format_task_report
from agent.graph import build_hierarchical_graph
from agent.nodes.lead import PlanValidationError, validate_plan
from agent.states import Brief, LeadPlan, Output, Review, TaskReport


def _brief(task_id: str, deps=(), outputs=()) -> Brief:
    return Brief(
        id=task_id,
        specialist="eda",
        question=f"question {task_id}",
        complete_when="c",
        depends_on=list(deps),
        outputs=[Output(name=o, contents="x") for o in outputs],
    )


def _plan(*briefs: Brief) -> LeadPlan:
    return LeadPlan(reasoning="r", briefs=list(briefs))


def accept(*follow_ups: Brief) -> Review:
    return Review(reasoning="r", verdict="accept", follow_ups=list(follow_ups))


def revise(feedback: str) -> Review:
    return Review(reasoning="r", verdict="revise", feedback=feedback)


@pytest.fixture
def analyse(monkeypatch, tmp_path, small_csv):
    """Run the whole graph; the plan and the writers' texts are added around"""

    def _analyse(plan: LeadPlan, *responses):
        llm = ScriptedLLM([plan, *responses, "synthesis", "the report"])
        monkeypatch.setattr(LLMManager, "get_llm", lambda **_: llm)
        state = build_hierarchical_graph().invoke(
            {"dataset_info": "", "dataset_path": small_csv, "run_dir": str(tmp_path)},
            config={"recursion_limit": 100},
        )
        assert state["report"] == "the report"
        return state, llm

    return _analyse


# Plan validation


def _questions(briefs) -> list[str]:
    return [b.question for b in briefs]


def test_order_respects_dependencies():
    briefs = validate_plan(
        _plan(_brief("c", ["b"]), _brief("a"), _brief("b", ["a"])), 10
    )
    assert _questions(briefs) == ["question a", "question b", "question c"]


def test_ids_are_assigned_and_dependencies_resolve_by_id_or_output():
    # The P1.4 run: qwen3.5 left every id empty and named outputs in depends_on
    plan = _plan(
        _brief("", outputs=["summary"]),
        Brief(
            id="",
            specialist="statistical",
            question="q",
            complete_when="c",
            depends_on=["summary"],
        ),
        Brief(id="T3", specialist="ml", question="q", complete_when="c"),
        _brief("x", deps=["T3"]),
    )
    briefs = validate_plan(plan, 10)
    assert [b.id for b in briefs] == ["eda_1", "stat_1", "ml_1", "eda_2"]
    assert [b.depends_on for b in briefs] == [[], ["eda_1"], [], ["ml_1"]]


def test_duplicate_ids_get_distinct_ids():
    briefs = validate_plan(_plan(_brief("a"), _brief("a")), 10)
    assert [b.id for b in briefs] == ["eda_1", "eda_2"]


def test_cycle_raises():
    # B3: cycles used to be silently ordered
    with pytest.raises(PlanValidationError, match="cycle"):
        validate_plan(_plan(_brief("a", ["b"]), _brief("b", ["a"])), 10)


def test_unknown_and_self_dependencies_are_dropped():
    briefs = validate_plan(_plan(_brief("a", ["missing", "a"])), 10)
    assert briefs[0].depends_on == []


def test_outputs_nothing_depends_on_are_dropped():
    # qwen3.5 gave every brief outputs, needed or not; each costs a step
    plan = _plan(_brief("a", outputs=["x"]), _brief("b", ["a"], outputs=["y"]))
    a, b = validate_plan(plan, 10)
    assert [o.name for o in a.outputs] == ["x"]
    assert b.outputs == []


def test_cap_keeps_the_first_briefs_and_drops_dangling_deps():
    briefs = validate_plan(_plan(_brief("a"), _brief("b"), _brief("c", ["b"])), 2)
    assert _questions(briefs) == ["question a", "question b"]
    capped = validate_plan(_plan(_brief("a"), _brief("c", ["z"])), 1)
    assert _questions(capped) == ["question a"]


# The loop


def test_a_task_sent_back_is_revised_then_the_next_runs(analyse):
    state, llm = analyse(
        _plan(_brief("eda_1"), _brief("eda_2")),
        run_cell("record_fact('n', len(df), 'Rows')"),
        finish("n"),
        revise("Also record m."),
        run_cell("record_fact('m', 2, 'Two')"),
        finish("n", "m"),
        accept(),
        finish(),
        accept(),
    )
    assert [r.task_id for r in state["completed_tasks"]] == ["eda_1", "eda_2"]
    first = state["completed_tasks"][0]
    assert first.revisions == 1
    assert [r.verdict for r in first.reviews] == ["revise", "accept"]
    assert set(first.facts) == {"n", "m"}
    review_prompt = next(p for p in llm.prompts if "Review the report" in p)
    assert "record_fact('n'" in review_prompt  # the lead sees the code
    assert "No problems found" in review_prompt


def test_revisions_are_capped_and_the_last_objection_is_kept(analyse, monkeypatch):
    monkeypatch.setattr(settings, "max_revisions", 1)
    state, llm = analyse(
        _plan(_brief("eda_1")),
        finish(),
        revise("Wrong formula."),
        finish(),
        revise("Still the wrong formula."),
    )
    (result,) = state["completed_tasks"]
    assert result.revisions == 1
    assert "can't be redone" in llm.prompts[-3]  # the second review
    assert "Unresolved review issue: Still the wrong formula." in format_task_report(
        result
    )


def test_follow_ups_are_added_within_budget_with_unique_ids(analyse, monkeypatch):
    monkeypatch.setattr(settings, "max_follow_ups", 1)
    state, llm = analyse(
        _plan(_brief("eda_1")),
        finish(),
        accept(_brief("eda_1", deps=["eda_1", "nope"]), _brief("eda_9")),
        finish(),
        accept(),
    )
    assert [r.task_id for r in state["completed_tasks"]] == ["eda_1", "eda_2"]
    follow_up = state["completed_tasks"][1].brief
    assert follow_up.depends_on == ["eda_1"]
    assert state["follow_ups_added"] == 1
    assert "follow-up tasks is spent" in llm.prompts[-3]


def test_a_failed_task_is_recorded_and_the_run_continues(analyse):
    state, _ = analyse(
        _plan(_brief("eda_1"), _brief("eda_2")),
        finish(status="failed"),
        accept(),
        finish(),
        accept(),
    )
    assert [r.task_id for r in state["failed_tasks"]] == ["eda_1"]
    assert [r.task_id for r in state["completed_tasks"]] == ["eda_2"]


def test_missing_outputs_send_the_task_back_even_if_the_lead_accepts(
    analyse, monkeypatch
):
    monkeypatch.setattr(settings, "max_specialist_steps", 1)
    state, llm = analyse(
        _plan(_brief("eda_1", outputs=["clean"]), _brief("eda_2", ["eda_1"])),
        finish(),  # last step: finishes without publishing
        accept(),
        run_cell("publish('clean', df.dropna())"),
        TaskReport(status="complete"),  # the finisher, budget spent
        accept(),
        finish(),  # eda_2
        accept(),
    )
    result = state["completed_tasks"][0]
    assert "not published: ['clean']" in llm.prompts[2]  # shown to the lead
    assert result.reviews[0].verdict == "revise"
    assert (
        "Publish the outputs later tasks need: ['clean']" in result.reviews[0].feedback
    )
    assert result.published == ["eda_1/clean"]
