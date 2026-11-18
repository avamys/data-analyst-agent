"""Questions about a finished run: the lead answers from the recorded facts, or
first has up to settings.max_question_tasks new tasks compute what is missing

ask → answer, or ask → run_task ⇄ review … → answer. The tasks run and are
reviewed as in the analysis (lead.py), without follow-ups. The answer's numbers
are checked against recorded values like the report's (report.py).
"""

import json
import logging
from pathlib import Path

from agent.config import settings
from agent.core.base_agent import BaseAgent
from agent.core.template_manager import prompt_templates
from agent.nodes.lead import ID_PREFIX, _refs, _resolve
from agent.nodes.report import (
    drop_missing_images,
    format_for_writer,
    recorded_numbers,
    reply_text,
    write_checked,
)
from agent.number_check import recorded_values
from agent.profiling import profile_summary
from agent.states import Brief, HierarchicalState, QuestionPlan

logger = logging.getLogger(__name__)


def ask_node(state: HierarchicalState) -> dict:
    """The lead picks the facts that answer the last question, or plans tasks"""
    question = state.questions[-1]
    prompt = prompt_templates.render(
        "lead/ask.jinja2",
        profile=profile_summary(state.dataset_profile),
        results="\n\n".join(_with_outputs(r) for r in state.completed_tasks),
        failed=_failed(state.failed_tasks),
        earlier="\n\n".join(
            f"Q{q.number}: {q.text}\nA{q.number}: {q.answer}"
            for q in state.questions[:-1]
        ),
        question=question.text,
        max_tasks=settings.max_question_tasks,
    )
    lead = BaseAgent("lead", use_structured_output=True, output_schema=QuestionPlan)
    plan: QuestionPlan = lead.invoke(prompt)
    briefs = [] if plan.answer_now else question_briefs(plan.briefs, state)
    logger.info(f"Q{question.number}: {plan.reasoning}")
    for brief in briefs:
        logger.info(f"  {brief.id} ({brief.specialist}): {brief.question}")
    question = question.model_copy(
        update={
            "reasoning": plan.reasoning,
            "facts": known_facts(plan.facts, state),
            "tasks": [b.id for b in briefs],
        }
    )
    return {"backlog": briefs, "questions": [*state.questions[:-1], question]}


def question_briefs(briefs: list[Brief], state: HierarchicalState) -> list[Brief]:
    """
    Up to settings.max_question_tasks briefs, with ids q<N>_<specialist>_<k>.
    They may depend on tasks already run or on an earlier brief of the list.
    """
    number = state.questions[-1].number
    done = [r.brief for r in state.completed_tasks + state.failed_tasks if r.brief]
    refs = _refs(done)
    kept = [b.model_copy(deep=True) for b in briefs[: settings.max_question_tasks]]
    if len(briefs) > len(kept):
        logger.warning(f"Question capped at {len(kept)} tasks")
    new_refs: dict[str, str] = {}
    for k, brief in enumerate(kept, 1):
        new_id = f"q{number}_{ID_PREFIX[brief.specialist]}_{k}"
        # Dependencies on a brief later in the list are dropped
        brief.depends_on = _resolve(brief.depends_on, {**refs, **new_refs})
        for ref in [brief.id, *(o.name for o in brief.outputs)]:
            if ref and ref not in refs:
                new_refs.setdefault(ref, new_id)
        brief.id = new_id
    needed = {d for b in kept for d in b.depends_on}
    for brief in kept:
        if brief.id not in needed:
            brief.outputs = []  # nothing would load them, as in validate_plan
    return kept


def known_facts(refs: list[str], state: HierarchicalState) -> list[str]:
    """The task_id.fact_name references that name a recorded fact"""
    facts = {f"{r.task_id}.{name}" for r in state.completed_tasks for name in r.facts}
    unknown = [ref for ref in refs if ref not in facts]
    if unknown:
        logger.warning(f"Facts that don't exist, dropped: {unknown}")
    return list(dict.fromkeys(ref for ref in refs if ref in facts))


def answer_node(state: HierarchicalState) -> dict:
    """The lead answers from the facts it picked and the new tasks' results"""
    question = state.questions[-1]
    new = [r for r in state.completed_tasks if r.task_id in question.tasks]
    failed = [r for r in state.failed_tasks if r.task_id in question.tasks]
    picked = _picked(question.facts, state)

    def prompt(**draft) -> str:
        return prompt_templates.render(
            "lead/answer.jinja2",
            profile=profile_summary(state.dataset_profile),
            question=question.text,
            reasoning=question.reasoning,
            facts="\n".join(
                f"{ref} = {json.dumps(f['value'])}  # {f['desc']}"
                for ref, f in picked.items()
            ),
            results="\n\n".join(format_for_writer(r) for r in new),
            failed=_failed(failed),
            **draft,
        )

    writer = BaseAgent(agent_type="reporter")
    values = recorded_numbers(state)
    values += recorded_values([[ref, f["value"]] for ref, f in picked.items()])
    answer, unmatched = write_checked(
        lambda **draft: reply_text(writer.invoke(prompt(**draft)), "answer"), values
    )
    if unmatched:
        logger.warning(f"Numbers still matching no fact: {unmatched}")
        answer += "\n\n**Numbers not traced to a recorded fact:** " + ", ".join(
            n for n, _ in unmatched
        )
    answer = drop_missing_images(answer, Path(state.run_dir))
    question = question.model_copy(
        update={"answer": answer, "unverified_numbers": [n for n, _ in unmatched]}
    )
    return {"questions": [*state.questions[:-1], question]}


def _with_outputs(result) -> str:
    """A task's findings for the lead, and the objects later tasks can load"""
    text = format_for_writer(result)
    if result.published:
        text += "\nPublished objects (load): " + ", ".join(result.published)
    return text


def _failed(results) -> str:
    return "\n".join(
        f"- [{r.task_id}] {r.description}: {r.error or 'no usable result'}"
        for r in results
    )


def _picked(refs: list[str], state: HierarchicalState) -> dict:
    """task_id.fact_name -> the recorded fact"""
    results = {r.task_id: r for r in state.completed_tasks}
    picked = {}
    for ref in refs:
        task_id, name = ref.split(".", 1)
        picked[ref] = results[task_id].facts[name]
    return picked
