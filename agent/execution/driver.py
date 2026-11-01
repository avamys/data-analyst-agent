"""Runs a cell script cell by cell in one namespace, one JSON line per finished cell.

Started by runner.run_script in a fresh process, with the task directory as the
working directory: python -m agent.execution.driver <script> <results.jsonl>
"""

import contextlib
import io
import json
import linecache
import os
import sys
import traceback
from pathlib import Path

from agent.execution.cells import split_cells


def main(script: str, results: str):
    cells = split_cells(Path(script).read_text())
    # Facts and charts describe this run only
    for stale in ("facts.json", "charts.json"):
        Path(stale).unlink(missing_ok=True)

    namespace = {"__name__": "__main__"}
    with open(results, "w") as out:
        for index, code in enumerate(cells):
            filename = f"<cell {index}>"
            # Lets tracebacks show the cell's source lines
            linecache.cache[filename] = (
                len(code),
                None,
                code.splitlines(True),
                filename,
            )
            os.environ["ANALYST_CELL"] = str(index)

            buffer = io.StringIO()
            error = None
            with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
                try:
                    exec(compile(code, filename, "exec"), namespace)
                except (Exception, SystemExit) as e:
                    # Skip this driver's own frame
                    tb = e.__traceback__.tb_next if e.__traceback__ else None
                    error = "".join(traceback.format_exception(type(e), e, tb))

            out.write(json.dumps({"output": buffer.getvalue(), "error": error}) + "\n")
            out.flush()
            if error:
                break


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
