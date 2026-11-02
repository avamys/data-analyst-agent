"""The lead writes the final report from the accepted results; code checks it

The writer sees each accepted finding with the facts it cites (not the whole
fact table, which holds stale values from failed attempts), the charts, open
review issues and failed tasks. Every number in the draft must match a recorded
value: mismatches go back to the writer once, and any left are listed under
Limitations. Images whose file doesn't exist are removed.
"""

import json
import logging
import re
from pathlib import Path

from agent.core.base_agent import BaseAgent
from agent.core.template_manager import prompt_templates
from agent.number_check import code_literals, recorded_values, unmatched_numbers
from agent.profiling import profile_summary
from agent.states import HierarchicalState, TaskReport, TaskResult

logger = logging.getLogger(__name__)

IMAGE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)\n?")


def write_report_node(state: HierarchicalState) -> dict:
    """The lead writes the report; numbers are checked, then images"""
    values = recorded_values(state.dataset_profile.model_dump())
    for result in state.completed_tasks:
        # Names too: grouped facts are often named after their group, e.g.
        # rate_(7.91, 14.454]. Not descriptions: those are free text.
        facts = cited_facts(result)
        values += recorded_values([[name, f["value"]] for name, f in facts.items()])
        values += code_literals(result.code)

    def prompt(**draft) -> str:
        return prompt_templates.render(
            "lead/report.jinja2",
            profile=profile_summary(state.dataset_profile),
            reasoning=state.plan.reasoning,
            results="\n\n".join(format_for_writer(r) for r in state.completed_tasks),
            failed="\n".join(
                f"- [{r.task_id}] {r.description}: {r.error or 'no usable result'}"
                for r in state.failed_tasks
            ),
            **draft,
        )

    writer = BaseAgent(agent_type="reporter")
    # text(): with thinking on (Claude), content is a list of blocks
    report = writer.invoke(prompt()).text().strip()
    unmatched = unmatched_numbers(report, values)
    if unmatched:
        logger.warning(f"Numbers matching no fact, sent back: {unmatched}")
        listed = "\n".join(f'- {n} in: "{line}"' for n, line in unmatched)
        report = writer.invoke(prompt(draft=report, unmatched=listed)).text().strip()
        unmatched = unmatched_numbers(report, values)
    if unmatched:
        logger.warning(f"Numbers still matching no fact: {unmatched}")
        report = add_to_limitations(report, unmatched)
    report = drop_missing_images(report, Path(state.run_dir))
    logger.info(f"Report written: {len(report)} characters")
    return {"report": report, "unverified_numbers": [n for n, _ in unmatched]}


def cited_facts(result: TaskResult) -> dict:
    """The facts a task's findings cite, by name"""
    report = result.report or TaskReport(status="failed")
    names = [name for finding in report.findings for name in finding.facts]
    return {name: result.facts[name] for name in names if name in result.facts}


def format_for_writer(result: TaskResult) -> str:
    """A task's findings, each with its cited facts, plus charts and open issues"""
    report = result.report or TaskReport(status="failed")
    lines = [f"[{result.task_id}] {result.description} (status: {report.status})"]
    lines.append("Findings:")
    for finding in report.findings:
        lines.append(f"- {finding.statement}")
        for name in finding.facts:
            if name in result.facts:
                fact = result.facts[name]
                value = json.dumps(fact["value"])
                lines.append(f"    {result.task_id}.{name} = {value}  # {fact['desc']}")
    if result.charts:
        # report.md is in the run directory, charts in tasks/<id>/charts/
        lines.append("Charts:")
        lines += [
            f"- ![{c['caption']}](tasks/{result.task_id}/{c['file']})"
            for c in result.charts.values()
        ]
    if result.reviews and result.reviews[-1].verdict == "revise":
        lines.append(f"Unresolved review issue: {result.reviews[-1].feedback}")
    if report.follow_ups:
        lines.append("Questions it raised:")
        lines += [f"- {q}" for q in report.follow_ups]
    return "\n".join(lines)


def add_to_limitations(report: str, unmatched: list[tuple[str, str]]) -> str:
    """List the numbers no fact backs at the end of the Limitations section"""
    note = (
        "\n\n**Numbers not traced to a recorded fact.** The automatic check found "
        "no recorded value for these numbers:\n"
        + "\n".join(f'- {n} in: "{line}"' for n, line in unmatched)
    )
    section = re.search(r"^## Limitations.*?(?=^## |\Z)", report, re.S | re.M)
    if section is None:
        return f"{report}\n\n## Limitations{note}"
    end = section.start() + len(section[0].rstrip())
    return report[:end] + note + report[end:]


def drop_missing_images(report: str, run_dir: Path) -> str:
    """Remove images whose file doesn't exist in the run directory"""

    def keep_if_exists(m: re.Match) -> str:
        if (run_dir / m[1]).is_file():
            return m[0]
        logger.warning(f"Report image not found, removed: {m[1]}")
        return ""

    return IMAGE.sub(keep_if_exists, report)
