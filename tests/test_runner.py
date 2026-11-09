import errno
import json
import pickle

import pytest

from agent.execution import runner
from agent.execution.cells import join_cells, split_cells
from agent.execution.runner import prepare_task_dir, run_script


@pytest.fixture
def task_dir(tmp_path, small_csv):
    run_dir = tmp_path / "run"
    return prepare_task_dir(run_dir / "tasks" / "t1", small_csv, run_dir, "t1")


def _run(task_dir, *cells, timeout=60):
    (task_dir / "analysis.py").write_text(join_cells(list(cells)))
    return run_script(task_dir, timeout=timeout)


def test_cells_round_trip():
    cells = ["import pandas as pd", "x = 1\nprint(x)"]
    text = join_cells(cells)
    assert text == "# %%\nimport pandas as pd\n\n# %%\nx = 1\nprint(x)\n"
    assert split_cells(text) == cells


def test_split_keeps_code_before_first_marker():
    assert split_cells("a = 1\n# %%\nb = 2\n") == ["a = 1", "b = 2"]


def test_output_is_captured_per_cell_and_state_carries_over(task_dir):
    result = _run(task_dir, "x = 40\nprint('first')", "print(x + 2)")
    assert result.ok
    assert [c.output for c in result.cells] == ["first\n", "42\n"]


def test_failing_cell_is_reported_with_traceback(task_dir):
    result = _run(task_dir, "print('ok')", "{}['missing']", "print('never')")
    assert not result.ok
    assert result.failed_cell == 1
    assert len(result.cells) == 2
    assert "KeyError: 'missing'" in result.cells[1].error
    assert "{}['missing']" in result.cells[1].error  # traceback shows the source line


def test_output_mentioning_errors_is_not_a_failure(task_dir):
    result = _run(
        task_dir, "print('Mean Squared Error: 0.1')\nprint('ModelError: none')"
    )
    assert result.ok


def test_timeout_marks_the_running_cell(task_dir):
    result = _run(task_dir, "print('fast')", "import time\ntime.sleep(30)", timeout=3)
    assert not result.ok
    assert result.failed_cell == 1
    assert "timed out" in result.cells[1].error


def test_runtime_helpers_write_to_disk(task_dir):
    result = _run(
        task_dir,
        "from agent.execution.runtime import df, load, publish, record_fact, save_chart",
        "record_fact('n_rows', len(df), 'Number of rows')\n"
        "record_fact('rate', df['target'].mean(), 'Share of target = 1')",
        "import matplotlib.pyplot as plt\n"
        "fig, ax = plt.subplots()\nax.plot([1, 2])\n"
        "save_chart(fig, 'line', 'A line')",
        "publish('numbers', [1, 2, 3])\nprint(load('t1/numbers'))",
    )
    assert result.ok, result.cells[-1].error

    facts = json.loads((task_dir / "facts.json").read_text())
    assert facts["n_rows"] == {"value": 40, "desc": "Number of rows", "cell": 1}
    assert isinstance(facts["rate"]["value"], float)

    charts = json.loads((task_dir / "charts.json").read_text())
    assert charts["line"]["caption"] == "A line"
    assert (task_dir / charts["line"]["file"]).exists()

    published = task_dir.parent.parent / "workspace" / "t1" / "numbers.pkl"
    assert pickle.loads(published.read_bytes()) == [1, 2, 3]
    assert result.cells[3].output == "[1, 2, 3]\n"


def test_facts_are_rebuilt_on_every_run(task_dir):
    _run(
        task_dir,
        "from agent.execution.runtime import record_fact\nrecord_fact('old', 1, 'd')",
    )
    _run(
        task_dir,
        "from agent.execution.runtime import record_fact\nrecord_fact('new', 2, 'd')",
    )
    assert list(json.loads((task_dir / "facts.json").read_text())) == ["new"]


def test_load_of_unknown_output_names_what_is_available(task_dir):
    result = _run(
        task_dir, "from agent.execution.runtime import load\nload('t9/nothing')"
    )
    assert "No published output 't9/nothing'" in result.cells[0].error


def test_chart_names_are_made_filename_safe(task_dir):
    result = _run(
        task_dir,
        "from agent.execution.runtime import save_chart\n"
        "import matplotlib.pyplot as plt\n"
        "save_chart(plt.figure(), 'ml_1/model comparison', 'c')",
    )
    assert result.ok, result.cells[-1].error
    charts = json.loads((task_dir / "charts.json").read_text())
    assert (task_dir / charts["ml_1_model_comparison"]["file"]).exists()


def test_record_model_records_train_test_and_baseline_scores(task_dir):
    result = _run(
        task_dir,
        "from agent.execution.runtime import df, record_model",
        "from sklearn.linear_model import LogisticRegression\n"
        "from sklearn.model_selection import train_test_split\n"
        "X = df[['fare']].fillna(0); y = df['target']\n"
        "Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=0)\n"
        "m = LogisticRegression().fit(Xtr, ytr)\n"
        "scores = record_model('logreg', m, Xtr, ytr, Xte, yte, 'Fare only')\n"
        "print(sorted(scores))",
    )
    assert result.ok, result.cells[-1].error
    fact = json.loads((task_dir / "facts.json").read_text())["logreg"]
    assert fact["kind"] == "model"
    scores = fact["value"]
    assert scores["kind"] == "classifier"
    assert {"train_accuracy", "test_accuracy", "baseline_accuracy"} <= set(scores)
    assert {"test_f1", "test_roc_auc", "test_recall"} <= set(scores)
    assert list(scores["top_features"]) == ["fare"]
    assert (scores["n_train"], scores["n_test"]) == (30, 10)


def test_record_model_handles_pipelines_and_regressors(task_dir):
    result = _run(
        task_dir,
        "from agent.execution.runtime import df, record_model",
        "from sklearn.ensemble import RandomForestRegressor\n"
        "from sklearn.pipeline import make_pipeline\n"
        "from sklearn.preprocessing import StandardScaler\n"
        "X = df[['fare', 'target']]; y = df['age'].fillna(40)\n"
        "m = make_pipeline(StandardScaler(), RandomForestRegressor(n_estimators=5,"
        " random_state=0)).fit(X[:30], y[:30])\n"
        "record_model('rf', m, X[:30], y[:30], X[30:], y[30:], 'Age')",
    )
    assert result.ok, result.cells[-1].error
    scores = json.loads((task_dir / "facts.json").read_text())["rf"]["value"]
    assert scores["kind"] == "regressor"
    assert {"train_r2", "test_r2", "test_rmse", "baseline_rmse"} <= set(scores)
    assert set(scores["top_features"]) == {"fare", "target"}


def test_scripts_dont_see_our_secrets(task_dir, monkeypatch):
    # LLM-written code must not reach API keys loaded from .env
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-secret")
    monkeypatch.setenv("LANGSMITH_API_KEY", "ls-secret")
    result = _run(
        task_dir,
        "from agent.execution.runtime import df\nimport os\nprint(sorted(os.environ))",
    )
    [cell] = result.cells
    assert cell.error is None
    assert "API_KEY" not in cell.output and "PATH" in cell.output


@pytest.fixture
def fresh_check():
    runner.network_blocked.cache_clear()
    yield
    runner.network_blocked.cache_clear()


@pytest.mark.skipif(not runner.network_blocked(), reason="unshare not available")
def test_scripts_have_no_network(task_dir):
    # Only loopback, so a connection fails at once, before any DNS or routing
    result = _run(
        task_dir,
        "import socket\nprint([name for _, name in socket.if_nameindex()])",
        "try:\n"
        "    socket.create_connection(('1.1.1.1', 80), timeout=5)\n"
        "except OSError as e:\n"
        "    print(e.errno)",
    )
    assert result.ok
    assert [c.output for c in result.cells] == ["['lo']\n", f"{errno.ENETUNREACH}\n"]


def test_scripts_run_where_the_network_cant_be_blocked(
    task_dir, monkeypatch, fresh_check, caplog
):
    monkeypatch.setattr(runner, "NO_NETWORK", ["no-such-unshare"])
    result = _run(task_dir, "print('ran')")
    assert result.ok and result.cells[0].output == "ran\n"
    assert not runner.network_blocked()
    assert "network access" in caplog.text
