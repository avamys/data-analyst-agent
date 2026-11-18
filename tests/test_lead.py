"""The lead's plan validation and the plan → run → review loop, with a scripted model"""

import re
import threading

import pytest
from conftest import ScriptedLLM
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import AIMessage
from test_specialist import finish, run_cell

from agent.config import settings
from agent.context import ContextOverflowError
from agent.core.llm_manager import LLMManager
from agent.core.specialists import SpecialistAgent, format_task_report
from agent.graph import build_hierarchical_graph
from agent.nodes.lead import PlanValidationError, validate_plan
from agent.states import Brief, Finding, LeadPlan, Output, Review, TaskReport


def _brief(task_id: str, deps=(), outputs=(), question=None) -> Brief:
    return Brief(
        id=task_id,
        specialist="eda",
        question=question or f"question {task_id}",
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
    """Run the whole graph; the plan and the report's text are added around"""

    def _analyse(plan: LeadPlan, *responses):
        # Responses come in call order, so tasks run one at a time
        monkeypatch.setattr(settings, "max_parallel_tasks", 1)
        llm = ScriptedLLM([plan, *responses, "the report"])
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
    second_review = llm.prompts[-2]  # before the report's
    assert "can't be redone" in second_review
    # P1.4 run: shown its own earlier objection, the lead argued with it
    assert "Wrong formula" not in second_review
    assert "Unresolved review issue: Still the wrong formula." in format_task_report(
        result
    )


def test_follow_ups_are_added_within_budget_with_unique_ids(analyse, monkeypatch):
    monkeypatch.setattr(settings, "max_follow_ups", 1)
    state, llm = analyse(
        _plan(_brief("eda_1")),
        finish(),
        accept(
            _brief("eda_1", deps=["eda_1", "nope"], question="follow-up"),
            _brief("eda_9"),
        ),
        finish(),
        accept(),
    )
    assert [r.task_id for r in state["completed_tasks"]] == ["eda_1", "eda_2"]
    follow_up = state["completed_tasks"][1].brief
    assert follow_up.depends_on == ["eda_1"]
    assert state["follow_ups_added"] == 1
    assert "follow-up tasks is spent" in llm.prompts[-2]


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


def test_a_prompt_too_long_for_the_window_fails_the_task_not_the_run(
    analyse, monkeypatch
):
    # P4.2: on Ollama one oversized prompt stopped a 2-hour run
    def too_long(self, brief, state, previous=None):
        raise ContextOverflowError("eda prompt can't fit")

    monkeypatch.setattr(SpecialistAgent, "execute", too_long)
    state, llm = analyse(_plan(_brief("eda_1")))
    (failed,) = state["failed_tasks"]
    assert "can't fit" in failed.error
    assert not any("Review the report" in p for p in llm.prompts)  # nothing to review


def test_a_revision_too_long_for_the_window_keeps_the_last_report(analyse, monkeypatch):
    execute = SpecialistAgent.execute

    def too_long_on_revision(self, brief, state, previous=None):
        if previous is not None:
            raise ContextOverflowError("eda prompt can't fit")
        return execute(self, brief, state)

    monkeypatch.setattr(SpecialistAgent, "execute", too_long_on_revision)
    state, llm = analyse(
        _plan(_brief("eda_1")),
        run_cell("record_fact('n', len(df), 'Rows')"),
        finish("n"),
        revise("Also record m."),
    )
    # As when revisions run out: the report stands, the objection unresolved
    (result,) = state["completed_tasks"]
    assert set(result.facts) == {"n"}
    assert "Unresolved review issue: Also record m." in format_task_report(result)
    assert sum("Review the report" in p for p in llm.prompts) == 1


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


def test_uncited_findings_send_the_task_back_even_if_the_lead_accepts(
    analyse, monkeypatch
):
    # The specialist's own check can't send its last step back (titanic ml_1)
    monkeypatch.setattr(settings, "max_specialist_steps", 1)
    cited = TaskReport(
        status="complete", findings=[Finding(statement="s", facts=["n"])]
    )
    state, llm = analyse(
        _plan(_brief("eda_1")),
        finish(cite=False),  # last step: a finding that cites nothing
        accept(),
        run_cell("record_fact('n', len(df), 'Rows')"),
        cited,  # the finisher, budget spent
        accept(),
    )
    result = state["completed_tasks"][0]
    assert "cite no recorded fact: ['s']" in llm.prompts[2]  # shown to the lead
    assert result.reviews[0].verdict == "revise"
    assert "must cite the recorded facts" in result.reviews[0].feedback
    assert result.reviews[1].verdict == "accept"
    assert result.report.findings[0].facts == ["n"] and "n" in result.facts


def test_follow_ups_repeating_a_brief_are_dropped(analyse):
    # P1.4 run: both follow-ups were copies of briefs still in the backlog
    state, _ = analyse(
        _plan(_brief("eda_1"), _brief("eda_2")),
        finish(),
        accept(_brief("x"), _brief("y", question=" Question  EDA_2")),
        finish(),  # eda_2
        accept(),
        finish(),  # the follow-up
        accept(),
    )
    assert [r.brief.question for r in state["completed_tasks"]] == [
        "question eda_1",
        "question eda_2",
        "question x",
    ]
    assert state["follow_ups_added"] == 1


def test_writers_read_text_from_block_replies(monkeypatch, tmp_path, small_csv):
    # With thinking on (Claude), a plain reply is a list: thinking, then text
    def blocks(text):
        return AIMessage(
            content=[
                {"type": "thinking", "thinking": "", "signature": "s"},
                {"type": "text", "text": text},
            ]
        )

    llm = ScriptedLLM(
        [
            _plan(_brief("eda_1")),
            finish(),
            accept(),
            blocks("report"),
        ]
    )
    monkeypatch.setattr(LLMManager, "get_llm", lambda **_: llm)
    state = build_hierarchical_graph().invoke(
        {"dataset_info": "", "dataset_path": small_csv, "run_dir": str(tmp_path)},
        config={"recursion_limit": 100},
    )
    assert state["report"] == "report"


class _RoutedLLM(ScriptedLLM):
    """Answers each prompt by its kind and task, whatever the call order"""

    def __init__(self, plan: LeadPlan, work):
        super().__init__([])
        self.plan, self.work = plan, work
        self.events = []  # ("work" | "review", task id), in call order

    def _respond(self, messages):
        prompt = messages[0].content
        if "You plan the analysis" in prompt:
            return self.plan
        if "Review the report" in prompt:
            self.events.append(("review", re.search(r"THE BRIEF \((\w+),", prompt)[1]))
            return accept()
        if task := re.search(r"^TASK (\w+):", prompt, re.MULTILINE):
            self.events.append(("work", task[1]))
            return self.work(task[1])
        return AIMessage(content="the report")


class _Calls(BaseCallbackHandler):
    def __init__(self):
        self.inputs = []

    def on_chain_start(self, serialized, inputs, **kwargs):
        self.inputs.append(str(inputs))


def test_independent_tasks_run_at_once_and_reviews_keep_their_order(
    monkeypatch, tmp_path, small_csv
):
    monkeypatch.setattr(settings, "max_parallel_tasks", 3)
    second_started = threading.Event()

    def work(task_id):
        if task_id == "eda_2":
            second_started.set()
        if task_id == "eda_1":
            # Finishes only while eda_2 is being worked: never, in a serial run
            assert second_started.wait(timeout=10)
        return finish()

    llm = _RoutedLLM(
        _plan(_brief("eda_1"), _brief("eda_2"), _brief("eda_3", deps=["eda_1"])), work
    )
    monkeypatch.setattr(LLMManager, "get_llm", lambda **_: llm)
    calls = _Calls()
    state = build_hierarchical_graph().invoke(
        {"dataset_info": "", "dataset_path": small_csv, "run_dir": str(tmp_path)},
        config={"recursion_limit": 100, "callbacks": [calls]},
    )

    assert [r.task_id for r in state["completed_tasks"]] == ["eda_1", "eda_2", "eda_3"]
    reviews = [task for kind, task in llm.events if kind == "review"]
    assert reviews == ["eda_1", "eda_2", "eda_3"]
    # eda_3 needs eda_1's findings, so it starts only after eda_1 is accepted
    assert llm.events.index(("work", "eda_3")) > llm.events.index(("review", "eda_1"))
    # eda_2 ran in a task thread; its calls still reach the run's callbacks
    assert any("TASK eda_2:" in i for i in calls.inputs)
