import pytest

from agent.nodes.planner import PlanValidationError, validate_plan
from agent.states import AnalysisPlan, SubTask


def _task(task_id: str, deps=(), priority: int = 1) -> SubTask:
    return SubTask(
        id=task_id,
        strategy="exploratory",
        specialist="eda",
        description=task_id,
        dependencies=list(deps),
        priority=priority,
    )


def _plan(*tasks: SubTask) -> AnalysisPlan:
    return AnalysisPlan(tasks=list(tasks), execution_order=[])


def test_order_respects_dependencies():
    plan = validate_plan(_plan(_task("c", ["b"]), _task("a"), _task("b", ["a"])), 10)
    order = plan.execution_order
    assert order.index("a") < order.index("b") < order.index("c")


def test_cycle_raises():
    # B3: cycles used to be silently ordered
    with pytest.raises(PlanValidationError, match="cycle"):
        validate_plan(_plan(_task("a", ["b"]), _task("b", ["a"])), 10)


def test_duplicate_ids_raise():
    with pytest.raises(PlanValidationError, match="Duplicate"):
        validate_plan(_plan(_task("a"), _task("a")), 10)


def test_unknown_and_self_dependencies_are_dropped():
    plan = validate_plan(_plan(_task("a", ["missing", "a"])), 10)
    assert plan.tasks[0].dependencies == []


def test_cap_keeps_highest_priority_and_drops_dangling_deps():
    plan = validate_plan(
        _plan(
            _task("low", priority=3),
            _task("high", priority=1),
            _task("mid", ["low"], priority=2),
        ),
        max_tasks=2,
    )
    assert {t.id for t in plan.tasks} == {"high", "mid"}
    assert next(t for t in plan.tasks if t.id == "mid").dependencies == []
    assert plan.execution_order == ["high", "mid"]
