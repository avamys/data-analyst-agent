"""Runs a task's cell script (`analysis.py`) in a fresh subprocess"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

from pydantic import BaseModel

from agent.execution.cells import split_cells

SCRIPT = "analysis.py"
RESULTS = ".results.jsonl"


class CellResult(BaseModel):
    output: str = ""
    error: str | None = None  # Traceback when the cell raised


class ScriptResult(BaseModel):
    """Results of the cells that ran; execution stops at the first failing cell"""

    cells: list[CellResult]
    seconds: float

    @property
    def failed_cell(self) -> int | None:
        return next((i for i, c in enumerate(self.cells) if c.error), None)

    @property
    def ok(self) -> bool:
        return self.failed_cell is None


def prepare_task_dir(
    task_dir: str | Path, data_path: str | Path, run_dir: str | Path, task_id: str
) -> Path:
    """Create the task directory and the context the runtime helpers read"""
    task_dir = Path(task_dir)
    task_dir.mkdir(parents=True, exist_ok=True)
    context = {
        "data_path": str(Path(data_path).resolve()),
        "run_dir": str(Path(run_dir).resolve()),
        "task_id": task_id,
    }
    (task_dir / ".analyst.json").write_text(json.dumps(context, indent=2))
    return task_dir


def run_script(task_dir: str | Path, timeout: float) -> ScriptResult:
    task_dir = Path(task_dir)
    n_cells = len(split_cells((task_dir / SCRIPT).read_text()))
    results = task_dir / RESULTS
    results.unlink(missing_ok=True)

    start = time.time()
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "agent.execution.driver", SCRIPT, RESULTS],
            cwd=task_dir,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ, "MPLBACKEND": "Agg"},
        )
        problem = (
            None
            if proc.returncode == 0
            else f"Process exited with code {proc.returncode}:\n{proc.stderr[-2000:]}"
        )
    except subprocess.TimeoutExpired:
        problem = f"TimeoutError: the script timed out after {timeout}s"

    cells = (
        [CellResult(**json.loads(line)) for line in results.read_text().splitlines()]
        if results.exists()
        else []
    )
    # A timeout or crash interrupts the next cell before it reports
    if problem and len(cells) < n_cells and not any(c.error for c in cells):
        cells.append(CellResult(error=problem))
    return ScriptResult(cells=cells, seconds=round(time.time() - start, 2))
