from agent.config import settings
from agent.core.specialists import CodeExecutor, get_specialist
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


class TestErrorDetection:
    # B5: normal output mentioning "Error:" used to be flagged as a failure
    executor = CodeExecutor.__new__(CodeExecutor)

    def test_metric_names_are_not_errors(self):
        assert not self.executor._has_execution_error(
            "Mean Squared Error: 0.12\nRMSE: 0.35"
        )
        assert not self.executor._has_execution_error("ModelError: none, all fine")

    def test_repl_exception_repr_is_error(self):
        # PythonREPLTool returns repr(exception) when the code raises
        assert self.executor._has_execution_error("ValueError('cannot convert')")
        assert self.executor._has_execution_error("KeyError('Age')\n")

    def test_traceback_is_error(self):
        assert self.executor._has_execution_error(
            'Traceback (most recent call last):\n  File "x.py", line 1\nNameError: x'
        )

    def test_real_execution(self):
        executor = CodeExecutor()
        ok, _, _, _ = executor.execute("print('Mean Squared Error: 0.1')", "t1")
        assert ok
        ok, _, error, _ = executor.execute(
            "import pandas as pd\npd.Series([1])['x']", "t2"
        )
        assert not ok
        assert "KeyError" in error
