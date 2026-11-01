from agent.config import settings
from agent.core.specialists import CodeExecutor, get_specialist
from agent.execution.runner import prepare_task_dir
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


def test_retries_default_to_setting():
    # B4: retries were hard-coded to 2
    assert get_specialist("eda").max_retries == settings.max_code_retries


def test_code_executor_runs_code_in_the_task_dir(tmp_path, small_csv):
    # B5: output mentioning "Error:" is not a failure; failures carry the traceback
    task_dir = prepare_task_dir(tmp_path / "tasks" / "t1", small_csv, tmp_path, "t1")
    executor = CodeExecutor(task_dir)

    ok, output, _, _ = executor.execute(
        "```python\nprint('Mean Squared Error: 0.1')\n```", "t1"
    )
    assert ok
    assert output == "Mean Squared Error: 0.1\n"
    assert "print('Mean Squared Error: 0.1')" in (task_dir / "analysis.py").read_text()

    ok, _, error, _ = executor.execute("print(len(df))\ndf['missing']", "t1")
    assert not ok
    assert "KeyError: 'missing'" in error
