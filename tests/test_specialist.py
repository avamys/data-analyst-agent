"""The specialist loop, driven by a scripted model (no LLM needed)"""

import pytest
from conftest import ScriptedLLM

from agent.config import settings
from agent.core.llm_manager import LLMManager
from agent.core.specialists import SpecialistAgent, format_task_report
from agent.profiling import auto_profile_dataset
from agent.states import (
    Brief,
    Finding,
    HierarchicalState,
    Output,
    Review,
    SpecialistStep,
    TaskReport,
)


@pytest.fixture
def run(monkeypatch, tmp_path, small_df, small_csv):
    """Run the specialist on one brief with scripted responses"""

    def _run(*responses, brief=None, previous=None):
        llm = ScriptedLLM(responses)
        monkeypatch.setattr(LLMManager, "get_llm", lambda **_: llm)
        state = HierarchicalState(
            dataset_info="",
            dataset_path=small_csv,
            run_dir=str(tmp_path),
            dataset_profile=auto_profile_dataset(small_df, small_csv),
        )
        brief = brief or Brief(
            id="eda_1", specialist="eda", question="q", complete_when="c"
        )
        return SpecialistAgent("eda").execute(brief, state, previous), llm

    return _run


def run_cell(code: str) -> SpecialistStep:
    return SpecialistStep(reasoning="r", action="run", code=code)


def finish(*facts: str, status="complete", cite=True) -> SpecialistStep:
    """A finish step; its one finding cites `facts` (no finding without facts)"""
    findings = [Finding(statement="s", facts=list(facts))] if facts or not cite else []
    return SpecialistStep(
        reasoning="r",
        action="finish",
        report=TaskReport(status=status, findings=findings),
    )


def test_failed_cell_is_replaced_and_its_error_shown(run, tmp_path):
    result, llm = run(
        run_cell("df['missing']"),
        run_cell("record_fact('rate', df['target'].mean(), 'Share of target = 1')"),
        finish("rate"),
    )
    assert "KeyError: 'missing'" in llm.prompts[1]  # the model sees the traceback
    assert result.success
    assert result.report.findings[0].facts == ["rate"]
    assert "rate" in result.facts
    assert len(result.attempts) == 2
    script = (tmp_path / "tasks" / "eda_1" / "analysis.py").read_text()
    assert "missing" not in script  # the failed cell was replaced


def test_output_of_the_latest_cell_is_shown(run):
    _, llm = run(run_cell("print('hello from the cell')"), finish())
    assert "Cell 1 output:\nhello from the cell" in llm.prompts[1]


def test_citing_an_unrecorded_fact_gets_feedback(run):
    result, llm = run(
        finish("made_up"),
        run_cell("record_fact('n', len(df), 'Rows')"),
        finish("n"),
    )
    assert "never recorded: ['made_up']" in llm.prompts[1]
    assert result.report.findings[0].facts == ["n"]


def test_spent_budget_forces_a_partial_report(run, monkeypatch):
    monkeypatch.setattr(settings, "max_specialist_steps", 2)
    final = TaskReport(
        status="complete", findings=[Finding(statement="s", facts=["n"])]
    )
    result, llm = run(
        run_cell("record_fact('n', len(df), 'Rows')"),
        run_cell("print(1)"),
        final,  # asked for by the finisher after the budget is spent
    )
    assert "step budget is spent" in llm.prompts[-1]
    assert result.report.status == "partial"
    assert result.success


def test_published_outputs_are_listed_for_later_tasks(run):
    result, _ = run(run_cell("publish('clean', df.dropna())"), finish())
    assert result.published == ["eda_1/clean"]
    assert 'load("eda_1/clean")' in format_task_report(result)


def test_syntax_errors_are_caught_before_running(run):
    result, llm = run(run_cell("print('unclosed'"), run_cell("print('ok')"), finish())
    assert "SyntaxError" in llm.prompts[1]
    assert "not run" in llm.prompts[1]
    assert [a["error"] is not None for a in result.attempts] == [True, False]
    assert result.code.count("print(") == 1  # the broken cell never joined the script


def test_cells_can_use_the_standard_imports(run):
    result, _ = run(run_cell("print(pd.__name__, np.__name__, plt.__name__)"), finish())
    assert result.attempts[0]["output"] == "pandas numpy matplotlib.pyplot\n"


def test_findings_must_cite_a_recorded_fact(run):
    # P1.3: findings that cited nothing passed, with wrong unrecorded numbers
    result, llm = run(
        finish(cite=False),  # a finding that cites nothing
        run_cell("record_fact('n', len(df), 'Rows')"),
        finish("n"),
    )
    assert "cite no recorded fact" in llm.prompts[1]
    assert result.report.findings[0].facts == ["n"]


def test_failed_cell_feedback_asks_for_a_complete_replacement(run):
    _, llm = run(run_cell("import math\nmath.nope()"), run_cell("print(1)"), finish())
    assert "replaces the failed cell completely" in llm.prompts[1]


def test_outputs_the_brief_names_must_be_published_before_finishing(run):
    # P1.2, P1.3: ml_1 never published its split and ml_2 couldn't load it
    brief = Brief(
        id="eda_1",
        specialist="eda",
        question="q",
        complete_when="c",
        outputs=[Output(name="clean", contents="df without missing rows")],
    )
    result, llm = run(
        finish(), run_cell("publish('clean', df.dropna())"), finish(), brief=brief
    )
    assert "- clean: df without missing rows" in llm.prompts[0]
    assert "not published: ['clean']" in llm.prompts[1]
    assert result.published == ["eda_1/clean"]


def test_a_revision_continues_the_script_with_the_leads_feedback(run, tmp_path):
    first, _ = run(run_cell("record_fact('n', len(df), 'Rows')"), finish("n"))
    first.reviews.append(Review(reasoning="r", verdict="revise", feedback="Add m."))
    first.revisions = 1
    result, llm = run(
        run_cell("record_fact('m', 2, 'Two')"), finish("n", "m"), previous=first
    )
    assert "SENT YOUR REPORT BACK" in llm.prompts[0]
    assert "Add m." in llm.prompts[0]
    assert "record_fact('n'" in llm.prompts[0]  # its own script so far
    assert set(result.facts) == {"n", "m"}
    assert [(a["attempt"], a["revision"]) for a in result.attempts] == [(1, 0), (2, 1)]
    assert result.revisions == 1 and len(result.reviews) == 1
    script = (tmp_path / "tasks" / "eda_1" / "analysis.py").read_text()
    assert script.count("record_fact(") == 2
