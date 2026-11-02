"""Local record of a run: logs, every LLM call, state per node, code attempts.

Layout of runs/<YYYYmmdd-HHMMSS>_<dataset>_<model>/:
    run.log               full log (DEBUG for agent modules)
    run_meta.json         commit, command, settings, timings, tokens, status
    llm_calls.jsonl       one line per LLM call
    state/NN_<node>.json  graph state after each top-level node
    tasks/<task_id>/      attempt_N.py, attempt_N_output.txt, result.json
    report.md             final report
"""

import json
import logging
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler
from pydantic_core import to_jsonable_python

logger = logging.getLogger(__name__)


class RunStore:
    def __init__(self, root: str | Path, dataset: str, model: str):
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_model = re.sub(r"[^\w.-]", "-", model)
        self.root = Path(root)
        self.path = self.root / f"{stamp}_{dataset}_{safe_model}"
        self.path.mkdir(parents=True)
        self._point_latest()

    def _point_latest(self):
        latest = self.root / "latest"
        try:
            latest.unlink(missing_ok=True)
            latest.symlink_to(self.path.name, target_is_directory=True)
        except OSError as e:  # e.g. filesystems without symlink support
            logger.debug(f"Could not update {latest}: {e}")

    def write_json(self, relpath: str, obj: Any):
        path = self.path / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(to_jsonable_python(obj, fallback=str), indent=2))

    def write_text(self, relpath: str, text: str):
        path = self.path / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def write_tasks(self, results: list) -> None:
        """Write every execution attempt of each task result"""
        for result in results:
            task_dir = f"tasks/{result.task_id}"
            for a in result.attempts:
                self.write_text(f"{task_dir}/attempt_{a['attempt']}.py", a["code"])
                self.write_text(
                    f"{task_dir}/attempt_{a['attempt']}_output.txt", a["output"] or ""
                )
            self.write_json(f"{task_dir}/result.json", result)


class LLMCallRecorder(BaseCallbackHandler):
    """Appends one JSON line per LLM call (prompt, response, tokens, timing)"""

    def __init__(self, path: Path):
        self.path = path
        self.calls = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.max_input_tokens = 0  # The largest prompt of the run
        self._pending: dict[UUID, dict] = {}

    def on_chat_model_start(self, serialized, messages, *, run_id, **kwargs):
        metadata = kwargs.get("metadata") or {}
        self._pending[run_id] = {
            "node": metadata.get("langgraph_node"),
            "model": metadata.get("ls_model_name"),
            "started": time.time(),
            "prompt": [{"role": m.type, "content": m.content} for m in messages[0]],
        }

    def on_llm_end(self, response, *, run_id, **kwargs):
        message = response.generations[0][0].message
        usage = message.usage_metadata or {}
        self.input_tokens += usage.get("input_tokens", 0)
        self.max_input_tokens = max(self.max_input_tokens, usage.get("input_tokens", 0))
        self.output_tokens += usage.get("output_tokens", 0)
        self._write(
            run_id,
            # Structured calls over function calling (OpenRouter) arrive as tool calls
            response=message.content or message.tool_calls,
            input_tokens=usage.get("input_tokens"),
            output_tokens=usage.get("output_tokens"),
            # Part of output_tokens; billed as output by hosted providers
            reasoning_tokens=(usage.get("output_token_details") or {}).get("reasoning"),
        )

    def on_llm_error(self, error, *, run_id, **kwargs):
        self._write(run_id, error=repr(error))

    def _write(self, run_id: UUID, **fields):
        self.calls += 1
        call = self._pending.pop(run_id, {})
        started = call.pop("started", time.time())
        record = {
            "time": datetime.now().isoformat(timespec="seconds"),
            **call,
            "seconds": round(time.time() - started, 2),
            **fields,
        }
        with self.path.open("a") as f:
            f.write(json.dumps(record, default=str) + "\n")
