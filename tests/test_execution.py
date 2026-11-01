from agent.nodes.reporter import build_execution_summary
from agent.states import TaskResult


def _result(task_id: str, success: bool, specialist: str = "eda") -> TaskResult:
    return TaskResult(
        task_id=task_id,
        specialist=specialist,
        description="d",
        success=success,
        execution_time=1.0,
    )


def test_execution_summary_counts_each_task_once():
    # B2: failed tasks used to be counted as completed too
    completed = [_result(f"ok_{i}", True) for i in range(4)]
    failed = [_result("bad", False, specialist="ml")]
    summary = build_execution_summary(completed, failed)
    assert "Total Tasks: 5" in summary
    assert "Completed: 4" in summary
    assert "Failed: 1" in summary
    assert "Success Rate: 80.0%" in summary
    assert "Total Execution Time: 5.0 seconds" in summary


def test_execution_summary_without_tasks():
    assert "Total Tasks: 0" in build_execution_summary([], [])
