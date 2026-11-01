"""Specialist agents: work a task as a loop of cells, then report findings"""

import json
import logging
import traceback
from importlib.metadata import version
from pathlib import Path

from agent.checks import missing_outputs
from agent.config import settings
from agent.core.base_agent import BaseAgent
from agent.core.template_manager import prompt_templates
from agent.execution.cells import join_cells, split_cells
from agent.execution.runner import SCRIPT, ScriptResult, prepare_task_dir, run_script
from agent.states import (
    Brief,
    HierarchicalState,
    SpecialistStep,
    TaskReport,
    TaskResult,
)

logger = logging.getLogger(__name__)

# First cell of every task script
SETUP_CELL = """import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from agent.execution.runtime import (
    df,
    load,
    publish,
    record_fact,
    record_model,
    save_chart,
)"""

# Analysis libraries task scripts may use (besides the standard library)
ANALYSIS_LIBRARIES = [
    "pandas",
    "numpy",
    "scipy",
    "statsmodels",
    "scikit-learn",
    "matplotlib",
    "seaborn",
]

ROLES = {
    "eda": "exploratory data analysis specialist",
    "statistical": "statistician (hypothesis tests, effect sizes, confidence intervals)",
    "ml": "machine learning specialist (scikit-learn)",
}


def clean_code(code: str) -> str:
    """Remove markdown code fences from generated code"""
    if code.startswith("```python"):
        code = code.split("```python")[1].split("```")[0].strip()
    elif code.startswith("```"):
        code = code.split("```")[1].split("```")[0].strip()
    return code


def format_facts(facts: dict, task_id: str | None = None) -> str:
    """One line per fact: name = value  # description (values capped at 200 chars)"""
    prefix = f"{task_id}." if task_id else ""
    lines = []
    for name, fact in facts.items():
        value = json.dumps(fact["value"])
        value = value if len(value) <= 200 else value[:200] + "…"
        lines.append(f"- {prefix}{name} = {value}  # {fact['desc']}")
    return "\n".join(lines) or "(none)"


def format_task_report(result: TaskResult) -> str:
    """A task's report with its full fact table, for the lead, synthesizer and reporter"""
    report = result.report or TaskReport(status="failed")
    lines = [f"[{result.task_id}] {result.description} (status: {report.status})"]
    lines.append("Findings:")
    lines += [f"- {f.statement} [facts: {', '.join(f.facts)}]" for f in report.findings]
    lines.append("Facts:")
    lines.append(format_facts(result.facts, result.task_id))
    if result.charts:
        lines.append("Charts:")
        lines += [f"- {name}: {c['caption']}" for name, c in result.charts.items()]
    if result.published:
        lines.append("Published outputs:")
        lines += [f'- load("{ref}")' for ref in result.published]
    if report.follow_ups:
        lines.append("Suggested follow-ups:")
        lines += [f"- {q}" for q in report.follow_ups]
    if result.reviews and result.reviews[-1].verdict == "revise":
        # Sent back once too often: the lead's last objection still stands
        lines.append(f"Unresolved review issue: {result.reviews[-1].feedback}")
    return "\n".join(lines)


class SpecialistAgent(BaseAgent):
    """
    Works one task as a loop: write a cell, run the whole script, read the result

    Each step the model either runs one new cell (replacing the last cell if it
    failed) or finishes with a report whose findings cite recorded facts. When
    the step budget runs out it must finish with what it has. A task the lead
    sent back continues its own script, with the lead's feedback.
    """

    def __init__(self, specialist_type: str, **kwargs):
        super().__init__(
            agent_type=specialist_type,
            use_structured_output=True,
            output_schema=SpecialistStep,
            **kwargs,
        )
        self.specialist_type = specialist_type
        self.finisher = BaseAgent(
            agent_type=specialist_type,
            use_structured_output=True,
            output_schema=TaskReport,
        )

    def execute(
        self,
        task: Brief,
        state: HierarchicalState,
        previous: TaskResult | None = None,
    ) -> TaskResult:
        """Work a brief; with `previous`, revise it after the lead's last review"""
        task_dir = prepare_task_dir(
            Path(state.run_dir) / "tasks" / task.id,
            state.dataset_path,
            state.run_dir,
            task.id,
        )
        cells = [SETUP_CELL]
        last: ScriptResult | None = None
        observation = "Nothing has run yet."
        attempts = []
        revision = None
        if previous is not None:
            attempts = list(previous.attempts)
            revision = {
                "feedback": previous.reviews[-1].feedback,
                "report": format_task_report(
                    previous.model_copy(update={"reviews": []})
                ),
            }
            script = task_dir / SCRIPT
            if script.exists():
                # Re-run, so the next cell builds on the current state
                cells = split_cells(script.read_text())
                last = run_script(task_dir, timeout=settings.code_timeout_s)
                observation = self._observe(last, len(cells) - 1)
        max_steps = settings.max_specialist_steps

        for step in range(1, max_steps + 1):
            prompt = self._prompt(
                task, state, cells, observation, task_dir, step, revision=revision
            )
            decision: SpecialistStep = self.invoke(prompt)
            self.logger.info(
                f"{task.id} step {step}: {decision.action}: {decision.reasoning}"
            )

            if decision.action == "finish":
                if decision.report is None:
                    observation = (
                        "You chose finish but gave no report. Include the report."
                    )
                    continue
                problem = self._report_problem(task, decision.report, task_dir)
                if problem and step < max_steps:
                    observation = problem
                    continue
                return self._result(
                    task, decision.report, cells, last, attempts, task_dir, previous
                )

            code = clean_code(decision.code.strip())
            if not code:
                observation = "You chose run but gave no code. Write one cell."
                continue
            try:
                compile(code, "<new cell>", "exec")
            except SyntaxError as e:
                error = "".join(traceback.format_exception_only(e))
                attempts.append(
                    {
                        "attempt": len(attempts) + 1,
                        "revision": previous.revisions if previous else 0,
                        "step": step,
                        "code": code,
                        "output": "",
                        "error": error,
                        "seconds": 0.0,
                    }
                )
                observation = f"Your cell has a syntax error and was not run:\n{error}"
                continue
            if last is not None and not last.ok:
                cells[-1] = code  # Replace the cell that failed
            else:
                cells.append(code)

            (task_dir / SCRIPT).write_text(join_cells(cells))
            last = run_script(task_dir, timeout=settings.code_timeout_s)
            cell = last.cells[-1]
            attempts.append(
                {
                    "attempt": len(attempts) + 1,
                    "revision": previous.revisions if previous else 0,
                    "step": step,
                    "code": code,
                    "output": cell.output,
                    "error": cell.error,
                    "seconds": last.seconds,
                }
            )
            self.logger.debug(
                f"{task.id} cell {len(cells) - 1}:\n{code}\nOutput:\n{cell.output}"
                + (f"\nError:\n{cell.error}" if cell.error else "")
            )
            observation = self._observe(last, len(cells) - 1)

        # Budget spent without finishing: report what was found
        self.logger.warning(f"{task.id}: step budget spent, asking for a final report")
        prompt = self._prompt(
            task,
            state,
            cells,
            observation,
            task_dir,
            max_steps,
            revision=revision,
            must_finish=True,
        )
        report: TaskReport = self.finisher.invoke(prompt)
        if report.status == "complete":
            report.status = "partial"
        return self._result(task, report, cells, last, attempts, task_dir, previous)

    def _prompt(
        self,
        task,
        state,
        cells,
        observation,
        task_dir,
        step,
        revision=None,
        must_finish=False,
    ):
        profile = state.dataset_profile
        return prompt_templates.render(
            "specialists/step.jinja2",
            role=ROLES[self.specialist_type],
            task_id=task.id,
            question=task.question,
            complete_when=task.complete_when,
            outputs=task.outputs,
            n_rows=profile.n_rows,
            n_cols=profile.n_cols,
            columns=", ".join(
                f"{col} ({kind})" for col, kind in profile.feature_types.items()
            ),
            libraries=", ".join(f"{lib} {version(lib)}" for lib in ANALYSIS_LIBRARIES),
            target_column=profile.target_column,
            target_type=profile.target_type,
            previous_findings=self._previous_findings(task, state),
            script=join_cells(cells),
            observation=observation,
            facts=format_facts(_read_json(task_dir / "facts.json")),
            charts="\n".join(
                f"- {name}: {c['caption']}"
                for name, c in _read_json(task_dir / "charts.json").items()
            )
            or "(none)",
            revision=revision,
            step=step,
            max_steps=settings.max_specialist_steps,
            must_finish=must_finish,
        )

    @staticmethod
    def _observe(result: ScriptResult, index: int) -> str:
        limit = settings.max_cell_output_chars
        cell = result.cells[-1]
        if cell.error:
            return (
                f"Cell {index} failed. Your next cell replaces the failed cell completely,"
                " so repeat everything it needed (imports, variables), not just the fix:\n"
                f"{cell.error[-limit:]}"
            )
        output = cell.output or "(no output)"
        if len(output) > limit:
            output = output[:limit] + f"\n… ({len(output) - limit} more characters cut)"
        return f"Cell {index} output:\n{output}"

    @staticmethod
    def _previous_findings(task: Brief, state: HierarchicalState) -> str:
        results = {r.task_id: r for r in state.completed_tasks}
        return "\n\n".join(
            format_task_report(results[dep])
            for dep in task.depends_on
            if dep in results
        )

    @staticmethod
    def _report_problem(task: Brief, report: TaskReport, task_dir: Path) -> str | None:
        """
        Feedback when findings cite unrecorded facts or none at all, or when
        outputs the brief asks for are not published
        """
        recorded = _read_json(task_dir / "facts.json")
        cited = {name for finding in report.findings for name in finding.facts}
        unknown = sorted(cited - set(recorded))
        uncited = [f.statement for f in report.findings if not f.facts]
        problems = []
        if unknown:
            problems.append(
                f"Your report cites facts that were never recorded: {unknown}."
            )
        if uncited:
            problems.append(f"These findings cite no recorded fact: {uncited}.")
        if problems:
            problems.append(
                "Every finding must cite the recorded facts behind it: record missing"
                " ones with record_fact in a new cell, then finish again."
            )
        missing = missing_outputs(task, _published(task_dir, task.id))
        if missing:
            problems.append(
                f"Later tasks need outputs you have not published: {missing}."
                " Publish each with publish(name, obj) in a new cell, then finish again."
            )
        return " ".join(problems) or None

    def _result(
        self, task, report, cells, last, attempts, task_dir, previous
    ) -> TaskResult:
        facts = _read_json(task_dir / "facts.json")
        # Citations that still don't resolve (last step) are dropped
        for finding in report.findings:
            finding.facts = [name for name in finding.facts if name in facts]
        self.logger.info(
            f"{task.id} finished ({report.status}): {len(report.findings)} findings, "
            f"{len(facts)} facts, {len(attempts)} cells run"
        )
        return TaskResult(
            task_id=task.id,
            specialist=self.specialist_type,
            description=task.question,
            code=join_cells(cells),
            output="".join(c.output for c in last.cells) if last else "",
            execution_time=sum(a["seconds"] for a in attempts),
            success=report.status != "failed",
            error=None if report.status != "failed" else "Specialist reported failure",
            report=report,
            facts=facts,
            charts=_read_json(task_dir / "charts.json"),
            published=_published(task_dir, task.id),
            attempts=attempts,
            metadata={"steps": len(attempts)},
            brief=task,
            revisions=previous.revisions if previous else 0,
            reviews=previous.reviews if previous else [],
        )


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() else {}


def _published(task_dir: Path, task_id: str) -> list[str]:
    """load() refs of what a task published, e.g. ["ml_1/train_test"]"""
    workspace = task_dir.parent.parent / "workspace" / task_id
    return sorted(f"{task_id}/{p.stem}" for p in workspace.glob("*.pkl"))


def get_specialist(specialist_type: str) -> SpecialistAgent:
    """Get a specialist by type: one of "eda", "statistical", "ml" """
    if specialist_type not in ROLES:
        raise ValueError(
            f"Unknown specialist type: {specialist_type}. Must be one of: {', '.join(ROLES)}"
        )
    return SpecialistAgent(specialist_type=specialist_type)
