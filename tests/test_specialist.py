"""The specialist loop, driven by a scripted model (no LLM needed)"""

import pytest
from langchain_core.runnables import RunnableLambda

from agent.config import settings
from agent.core.llm_manager import LLMManager
from agent.core.specialists import SpecialistAgent
from agent.nodes.orchestrator import auto_profile_dataset
from agent.states import (
    Finding,
    HierarchicalState,
    SpecialistStep,
    SubTask,
    TaskReport,
)


class ScriptedLLM:
    """Returns the given responses in order and keeps the prompts it was sent"""

    def __init__(self, responses):
        self.responses = iter(responses)
        self.prompts = []

    def with_structured_output(self, schema):
        def respond(messages):
            self.prompts.append(messages[0].content)
            return next(self.responses)

        return RunnableLambda(respond)


@pytest.fixture
def run(monkeypatch, tmp_path, small_df, small_csv):
    """Run the specialist on one task with scripted responses"""

    def _run(*responses):
        llm = ScriptedLLM(responses)
        monkeypatch.setattr(LLMManager, "get_llm", lambda **_: llm)
        state = HierarchicalState(
            dataset_info="",
            dataset_path=small_csv,
            run_dir=str(tmp_path),
            dataset_profile=auto_profile_dataset(small_df, small_csv),
        )
        task = SubTask(
            id="eda_1", strategy="exploratory", specialist="eda", description="d"
        )
        return SpecialistAgent("eda").execute(task, state), llm

    return _run


def run_cell(code: str) -> SpecialistStep:
    return SpecialistStep(reasoning="r", action="run", code=code)


def finish(*facts: str, status="answered") -> SpecialistStep:
    finding = Finding(statement="s", facts=list(facts))
    return SpecialistStep(
        reasoning="r",
        action="finish",
        report=TaskReport(status=status, findings=[finding]),
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
        status="answered", findings=[Finding(statement="s", facts=["n"])]
    )
    result, llm = run(
        run_cell("record_fact('n', len(df), 'Rows')"),
        run_cell("print(1)"),
        final,  # asked for by the finisher after the budget is spent
    )
    assert "step budget is spent" in llm.prompts[-1]
    assert result.report.status == "partial"
    assert result.success
