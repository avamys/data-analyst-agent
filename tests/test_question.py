import json
from pathlib import Path

import pytest
from conftest import ScriptedLLM
from test_lead import _brief, _plan, accept, revise
from test_specialist import finish, run_cell

from agent.cli import (
    RUN_SETTINGS,
    apply_flags,
    build_parser,
    main,
    run_analysis,
    use_run_settings,
)
from agent.config import settings
from agent.core.llm_manager import LLMManager
from agent.graph import build_question_graph
from agent.nodes.question import question_briefs
from agent.run_grades import run_grades
from agent.run_store import load_run
from agent.states import Brief, HierarchicalState, Question, QuestionPlan


@pytest.fixture
def finished(monkeypatch, tmp_path, small_csv) -> HierarchicalState:
    """A finished run: eda_1 recorded the row count (40) and published a frame"""
    monkeypatch.setattr(settings, "runs_directory", str(tmp_path / "runs"))
    monkeypatch.setattr(settings, "max_parallel_tasks", 1)
    cell = "record_fact('n', len(df), 'Rows')\npublish('frame', df.head())"
    llm = ScriptedLLM(
        [_plan(_brief("eda_1")), run_cell(cell), finish("n"), accept(), "report"]
    )
    monkeypatch.setattr(LLMManager, "get_llm", lambda **_: llm)
    return load_run(run_analysis(Path(small_csv)))


def ask(monkeypatch, state: HierarchicalState, text: str, *responses):
    """Ask the question with scripted replies; the new state and the prompts"""
    llm = ScriptedLLM(responses)
    monkeypatch.setattr(LLMManager, "get_llm", lambda **_: llm)
    number = len(state.questions) + 1
    state = state.model_copy(
        update={"questions": [*state.questions, Question(number=number, text=text)]}
    )
    return HierarchicalState(**build_question_graph().invoke(state)), llm.prompts


def answer_now(*facts: str) -> QuestionPlan:
    return QuestionPlan(reasoning="r", answer_now=True, facts=list(facts))


def new_tasks(*briefs: Brief, facts=()) -> QuestionPlan:
    return QuestionPlan(
        reasoning="r", answer_now=False, briefs=list(briefs), facts=list(facts)
    )


def test_an_answer_from_recorded_facts_runs_no_task(monkeypatch, finished):
    state, prompts = ask(
        monkeypatch,
        finished,
        "How many rows?",
        answer_now("eda_1.n", "eda_1.made_up"),
        "There are 40 rows.",
    )
    (question,) = state.questions
    assert (question.facts, question.tasks) == (["eda_1.n"], [])
    assert (question.answer, question.unverified_numbers) == ("There are 40 rows.", [])
    assert "Published objects (load): eda_1/frame" in prompts[0]
    assert "eda_1.n = 40  # Rows" in prompts[1]
    assert [r.task_id for r in state.completed_tasks] == ["eda_1"]


def test_new_tasks_run_through_review_and_later_questions_see_them(
    monkeypatch, finished
):
    count = "record_fact('m', len(load('eda_1/frame')), 'Rows in the head')"
    follow_up = _brief("x", question="Another question")
    state, prompts = ask(
        monkeypatch,
        finished,
        "How many rows does the head have?",
        new_tasks(_brief("head", deps=["eda_1"])),
        run_cell(count),
        finish("m"),
        revise("Say it is the head."),
        finish("m"),
        accept(follow_up),  # no follow-ups while answering a question
        "The head has 5 rows.",
    )
    (question,) = state.questions
    assert question.tasks == ["q1_eda_1"]
    task = state.completed_tasks[-1]
    assert (task.task_id, task.revisions, task.facts["m"]["value"]) == (
        "q1_eda_1",
        1,
        5,
    )
    assert task.brief.depends_on == ["eda_1"]
    assert state.backlog == [] and state.follow_ups_added == finished.follow_ups_added
    assert "leave follow_ups empty" in prompts[-2]  # the review offered none
    assert question.answer == "The head has 5 rows."

    state, prompts = ask(
        monkeypatch, state, "And the rows?", answer_now("eda_1.n"), "40 rows."
    )
    assert (
        "Q1: How many rows does the head have?\nA1: The head has 5 rows." in prompts[0]
    )
    assert "[q1_eda_1]" in prompts[0]
    assert [q.number for q in state.questions] == [1, 2]


def test_a_failed_task_reaches_the_answer(monkeypatch, finished):
    state, prompts = ask(
        monkeypatch,
        finished,
        "Can it be done?",
        new_tasks(_brief("a")),
        finish(status="failed"),
        accept(),
        "It could not be computed.",
    )
    assert [r.task_id for r in state.failed_tasks] == ["q1_eda_1"]
    assert "TASKS RUN FOR THIS QUESTION THAT FAILED:\n- [q1_eda_1]" in prompts[-1]


def test_numbers_matching_no_fact_go_back_once_then_are_flagged(monkeypatch, finished):
    state, prompts = ask(
        monkeypatch,
        finished,
        "How many rows?",
        answer_now("eda_1.n"),
        "There are 12345 rows.",
        "There are 12345 rows.",
    )
    (question,) = state.questions
    assert "12345" in prompts[-1] and "YOUR DRAFT" in prompts[-1]
    assert question.unverified_numbers == ["12345"]
    assert question.answer.endswith("**Numbers not traced to a recorded fact:** 12345")


def test_question_briefs_get_ids_and_known_dependencies(finished):
    state = finished.model_copy(update={"questions": [Question(number=3, text="q")]})
    first = _brief("a", deps=["b", "eda_1", "unknown"], outputs=["split"])
    second = Brief(**{**_brief("b", deps=["split"]).model_dump(), "specialist": "ml"})
    briefs = question_briefs([first, second, _brief("c")], state)
    assert [b.id for b in briefs] == ["q3_eda_1", "q3_ml_2"]  # capped at 2
    assert briefs[0].depends_on == ["eda_1"]  # not a later brief, not unknowns
    assert briefs[1].depends_on == ["q3_eda_1"]  # by its output's name
    assert [o.name for o in briefs[0].outputs] == ["split"]


def _events(run_dir: Path) -> list[dict]:
    return [json.loads(line) for line in (run_dir / "progress.jsonl").open()]


def _cli_ask(monkeypatch, run_dir: Path, text: str, *responses) -> dict:
    llm = ScriptedLLM(responses)
    monkeypatch.setattr(LLMManager, "get_llm", lambda **_: llm)
    assert main(["ask", str(run_dir), text]) == 0
    return json.loads((run_dir / "run_meta.json").read_text())


def test_analyst_ask_records_the_question_in_its_run(monkeypatch, finished, capsys):
    run_dir = Path(finished.run_dir)
    grades_before = run_grades(run_dir)
    states_before = len(list((run_dir / "state").glob("*.json")))
    count = "record_fact('m', len(load('eda_1/frame')), 'Rows in the head')"
    meta = _cli_ask(
        monkeypatch,
        run_dir,
        "How many rows does the head have?",
        new_tasks(_brief("head", deps=["eda_1"])),
        run_cell(count),
        finish("m"),
        accept(),
        "The head has 5 rows.",
    )
    (entry,) = meta["questions"]
    assert (entry["number"], entry["status"], entry["tasks"]) == (1, "ok", ["q1_eda_1"])
    assert entry["grades"]["tasks_completed"] == 1  # (scripted calls go uncounted)
    assert (run_dir / "tasks/q1_eda_1/result.json").exists()
    assert run_grades(run_dir) == grades_before  # the run's own grades
    states = sorted(int(p.name.split("_")[0]) for p in (run_dir / "state").glob("*"))
    assert states == list(range(1, states_before + 5))  # ask, run_task, review, answer
    assert (run_dir / "questions.md").read_text() == (
        "## Questions after the report\n"
        "\n### Q1. How many rows does the head have?\n\nThe head has 5 rows.\n"
    )
    events = [e["event"] for e in _events(run_dir)]
    assert events[events.index("question") :] == [
        "question",
        "asked",
        "task_started",
        "step",
        "task_finished",
        "reviewed",
        "answered",
        "question_done",
    ]
    page = (run_dir / "report.html").read_text()
    assert "<h3>Q1. How many rows does the head have?</h3>" in page
    assert "<dt>Questions</dt><dd>1 answered</dd>" in page
    assert page.index("<b>eda_1</b>") < page.index("<b>q1_eda_1</b>")
    printed = capsys.readouterr().out
    assert "Q1: How many rows" in printed and printed.rstrip().endswith("5 rows.")

    meta = _cli_ask(
        monkeypatch, run_dir, "And in all?", answer_now("eda_1.n"), "40 rows."
    )
    assert [q["number"] for q in meta["questions"]] == [1, 2]
    assert "### Q2. And in all?\n\n40 rows.\n" in (run_dir / "questions.md").read_text()
    assert load_run(run_dir).questions[0].answer == "The head has 5 rows."


def test_a_failed_question_is_recorded_and_the_next_one_works(monkeypatch, finished):
    run_dir = Path(finished.run_dir)
    with pytest.raises(RuntimeError, match="StopIteration"):  # no more replies
        _cli_ask(monkeypatch, run_dir, "Broken?", new_tasks(_brief("a")), finish())
    (entry,) = json.loads((run_dir / "run_meta.json").read_text())["questions"]
    assert entry["status"] == "failed" and "StopIteration" in entry["error"]
    assert _events(run_dir)[-1]["event"] == "question_done"
    assert "Q1. Broken?: no answer" in (run_dir / "report.html").read_text()

    # Left half done (a task in review), it doesn't carry over to the next one
    meta = _cli_ask(monkeypatch, run_dir, "Rows?", answer_now("eda_1.n"), "40 rows.")
    assert [q["status"] for q in meta["questions"]] == ["failed", "ok"]
    assert "### Q2. Rows?" in (run_dir / "questions.md").read_text()


def test_a_run_that_cant_take_questions_says_why(monkeypatch, finished, capsys):
    run_dir = Path(finished.run_dir)
    (run_dir / "report.md").unlink()
    with pytest.raises(SystemExit):
        main(["ask", str(run_dir), "Rows?"])
    assert "has no finished report to ask about" in capsys.readouterr().err


def test_a_question_uses_its_runs_settings_unless_flags_say_otherwise(
    monkeypatch, finished
):
    for name in RUN_SETTINGS:  # restored after the test
        monkeypatch.setattr(settings, name, getattr(settings, name))
    run_dir = Path(finished.run_dir)
    meta = json.loads((run_dir / "run_meta.json").read_text())
    meta["settings"].update(model_provider="anthropic", max_revisions=2)
    (run_dir / "run_meta.json").write_text(json.dumps(meta))
    use_run_settings(run_dir)
    assert (settings.model_provider, settings.max_revisions) == ("anthropic", 2)
    apply_flags(
        build_parser().parse_args(["ask", str(run_dir), "q", "--provider", "ollama"])
    )
    assert (settings.model_provider, settings.max_revisions) == ("ollama", 2)
