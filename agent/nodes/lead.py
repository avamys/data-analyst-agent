"""Lead analyst: plans a backlog of briefs, hands each to a specialist, reviews it

Nodes return partial state updates; `next_step` routes the loop:
plan → run_task → review → run_task (sent back, or next brief) … → synthesizer
"""

import logging

import pandas as pd

from agent.checks import missing_outputs, sanity_checks
from agent.config import settings
from agent.core.base_agent import BaseAgent
from agent.core.specialists import format_task_report, get_specialist
from agent.core.template_manager import prompt_templates
from agent.profiling import auto_profile_dataset, profile_summary
from agent.states import Brief, HierarchicalState, LeadPlan, Review

logger = logging.getLogger(__name__)

# The lead sees at most this much of a task's script when reviewing it
MAX_SCRIPT_CHARS = 8000

ID_PREFIX = {"eda": "eda", "statistical": "stat", "ml": "ml"}


def profile_node(state: HierarchicalState) -> dict:
    """Deterministic profile of the dataset; no LLM"""
    df = pd.read_csv(state.dataset_path)
    profile = auto_profile_dataset(df, state.dataset_path, state.target_column)
    return {"dataset_profile": profile}


def plan_node(state: HierarchicalState) -> dict:
    """The lead plans the backlog of briefs"""
    prompt = prompt_templates.render(
        "lead/plan.jinja2",
        profile=profile_summary(state.dataset_profile),
        dataset_info=state.dataset_info[:1000],
        has_target=state.dataset_profile.target_column is not None,
        max_tasks=settings.max_tasks,
    )
    lead = BaseAgent("lead", use_structured_output=True, output_schema=LeadPlan)
    plan: LeadPlan = lead.invoke(prompt)
    backlog = validate_plan(plan, settings.max_tasks)
    logger.info(f"Plan: {plan.reasoning}")
    for brief in backlog:
        deps = f" [after {', '.join(brief.depends_on)}]" if brief.depends_on else ""
        outputs = ", ".join(o.name for o in brief.outputs)
        logger.info(
            f"  {brief.id} ({brief.specialist}): {brief.question}{deps}"
            + (f" → publishes {outputs}" if outputs else "")
        )
    return {"plan": plan, "backlog": backlog}


def run_task_node(state: HierarchicalState) -> dict:
    """Run the task sent back by the last review, else the next brief"""
    previous = state.under_review
    if previous is not None:
        brief, backlog = previous.brief, state.backlog
        logger.info(f"Revising {brief.id} (revision {previous.revisions})")
    else:
        brief, backlog = state.backlog[0], state.backlog[1:]
        logger.info(f"Running {brief.id} ({brief.specialist}): {brief.question}")
    result = get_specialist(brief.specialist).execute(brief, state, previous)
    return {"under_review": result, "backlog": backlog}


def review_node(state: HierarchicalState) -> dict:
    """The lead accepts the task or sends it back, and may add follow-up briefs"""
    result = state.under_review
    brief = result.brief
    checks = sanity_checks(brief, result, state.dataset_profile)
    can_revise = result.revisions < settings.max_revisions
    follow_ups_left = settings.max_follow_ups - state.follow_ups_added
    script = result.code
    if len(script) > MAX_SCRIPT_CHARS:
        script = "# … (earlier cells cut)\n" + script[-MAX_SCRIPT_CHARS:]
    prompt = prompt_templates.render(
        "lead/review.jinja2",
        profile=profile_summary(state.dataset_profile),
        brief=brief,
        report=format_task_report(result),
        script=script,
        checks=checks,
        accepted=_accepted_findings(state),
        backlog="\n".join(
            f"- {b.id} ({b.specialist}): {b.question}" for b in state.backlog
        ),
        can_revise=can_revise,
        follow_ups_left=follow_ups_left,
    )
    lead = BaseAgent("lead", use_structured_output=True, output_schema=Review)
    review: Review = lead.invoke(prompt)

    missing = missing_outputs(brief, result.published)
    if missing and review.verdict == "accept":
        # Later tasks depend on these, so this is not the lead's call
        review.verdict = "revise"
        review.feedback = f"Publish the outputs later tasks need: {missing}. {review.feedback}".strip()
    logger.info(f"Review of {brief.id}: {review.verdict}: {review.reasoning}")
    if review.feedback:
        logger.info(f"  Feedback: {review.feedback}")

    result = result.model_copy(update={"reviews": [*result.reviews, review]})
    follow_ups = admit_follow_ups(review.follow_ups, state, follow_ups_left)
    update = {
        "backlog": [*state.backlog, *follow_ups],
        "follow_ups_added": state.follow_ups_added + len(follow_ups),
    }
    if review.verdict == "revise" and can_revise:
        result.revisions += 1
        return {**update, "under_review": result}

    key = "completed_tasks" if result.success else "failed_tasks"
    logger.info(f"{brief.id} done: {key.split('_')[0]}")
    return {**update, "under_review": None, key: [*getattr(state, key), result]}


def next_step(state: HierarchicalState) -> str:
    """After planning or a review: a task sent back, the next brief, or writing"""
    if state.under_review is not None or state.backlog:
        return "run_task"
    return "synthesizer"


def admit_follow_ups(
    follow_ups: list[Brief], state: HierarchicalState, limit: int
) -> list[Brief]:
    """Up to `limit` follow-ups, with new ids and dependencies on known tasks"""
    results = state.completed_tasks + state.failed_tasks
    if state.under_review is not None:
        results.append(state.under_review)
    existing = [r.brief for r in results if r.brief] + state.backlog
    known = {b.id for b in existing}
    refs = _refs(existing)
    if len(follow_ups) > max(limit, 0):
        dropped = [b.question for b in follow_ups[max(limit, 0) :]]
        logger.warning(f"Follow-up budget spent, dropped: {dropped}")
    admitted = []
    for brief in follow_ups[: max(limit, 0)]:
        brief = brief.model_copy(deep=True)
        brief.id = _new_id(brief.specialist, known)
        brief.depends_on = _resolve(brief.depends_on, refs)
        known.add(brief.id)
        admitted.append(brief)
        logger.info(f"Follow-up {brief.id} ({brief.specialist}): {brief.question}")
    return admitted


def _new_id(specialist: str, taken: set[str]) -> str:
    n = 1
    while f"{ID_PREFIX[specialist]}_{n}" in taken:
        n += 1
    return f"{ID_PREFIX[specialist]}_{n}"


def _refs(briefs: list[Brief]) -> dict[str, str]:
    """What a model may write in depends_on (an id or an output name) -> task id"""
    refs = {}
    for brief in briefs:
        for ref in [brief.id, *(o.name for o in brief.outputs)]:
            refs.setdefault(ref, brief.id)
    return refs


def _resolve(depends_on: list[str], refs: dict[str, str]) -> list[str]:
    """Task ids the references point to, in order, without unknowns or repeats"""
    return list(dict.fromkeys(refs[d] for d in depends_on if d in refs))


def _accepted_findings(state: HierarchicalState) -> str:
    """One line per accepted finding, and one per failed task"""
    lines = [
        f"- [{r.task_id}] {f.statement}"
        for r in state.completed_tasks
        for f in r.report.findings
    ]
    lines += [f"- [{r.task_id}] failed: {r.description}" for r in state.failed_tasks]
    return "\n".join(lines)


class PlanValidationError(ValueError):
    """The lead produced a plan that can't be executed"""


def validate_plan(plan: LeadPlan, max_tasks: int) -> list[Brief]:
    """
    Check and repair an LLM-produced plan; return the briefs in execution order

    - Only the first max_tasks briefs are kept (the lead lists them by priority)
    - Ids are assigned here (eda_1, stat_1, ml_1, ...): qwen3.5 left them all
      empty. Dependencies may name the model's id or an earlier brief's output.
    - Unknown, self, and dropped-task dependencies are removed; cycles raise
      PlanValidationError
    - Outputs of tasks no other task depends on are removed: the specialist
      must publish every output, and nothing would load these
    """
    briefs = [b.model_copy(deep=True) for b in plan.briefs]
    if len(briefs) > max_tasks:
        dropped = [b.question for b in briefs[max_tasks:]]
        logger.warning(f"Plan capped at {max_tasks} tasks, dropped: {dropped}")
        briefs = briefs[:max_tasks]

    refs: dict[str, str] = {}
    for brief in briefs:
        new_id = _new_id(brief.specialist, set(refs.values()))
        for ref in [brief.id, *(o.name for o in brief.outputs)]:
            if ref:
                refs.setdefault(ref, new_id)
        refs.setdefault(new_id, new_id)
        brief.id = new_id

    for brief in briefs:
        valid = [d for d in _resolve(brief.depends_on, refs) if d != brief.id]
        unknown = [d for d in brief.depends_on if d not in refs]
        if unknown:
            logger.warning(f"Task {brief.id}: removed unknown dependencies {unknown}")
        brief.depends_on = valid

    needed = {d for b in briefs for d in b.depends_on}
    for brief in briefs:
        if brief.outputs and brief.id not in needed:
            logger.info(f"Task {brief.id}: no task depends on it, outputs dropped")
            brief.outputs = []

    by_id = {b.id: b for b in briefs}
    return [by_id[i] for i in _topological_order(briefs)]


def _topological_order(briefs: list[Brief]) -> list[str]:
    """Dependencies first, otherwise plan order; raises on cycles"""
    by_id = {b.id: b for b in briefs}
    order: list[str] = []
    visiting: set[str] = set()
    done: set[str] = set()

    def visit(task_id: str, path: list[str]):
        if task_id in done:
            return
        if task_id in visiting:
            cycle = " -> ".join([*path[path.index(task_id) :], task_id])
            raise PlanValidationError(f"Dependency cycle: {cycle}")
        visiting.add(task_id)
        for dep in by_id[task_id].depends_on:
            visit(dep, [*path, task_id])
        visiting.remove(task_id)
        done.add(task_id)
        order.append(task_id)

    for brief in briefs:
        visit(brief.id, [])
    return order
