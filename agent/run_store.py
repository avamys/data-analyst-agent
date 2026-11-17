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
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

import httpx
from langchain_core.callbacks import BaseCallbackHandler
from pydantic_core import to_jsonable_python

logger = logging.getLogger(__name__)

# Stop reasons of a reply that hit the output cap: Ollama and OpenAI-style
# providers say "length" (num_predict / max_tokens), Anthropic "max_tokens"
CUT_OFF = {"length", "max_tokens"}

# Ollama's timings (nanoseconds) -> the seconds recorded per call
OLLAMA_SECONDS = {
    "load_duration": "load_seconds",
    "prompt_eval_duration": "prompt_seconds",
    "eval_duration": "generation_seconds",
}


def call_health(message) -> dict:
    """Why a call stopped and, on Ollama, where its time went; a field is
    absent when the provider doesn't return it"""
    meta = message.response_metadata or {}
    health = {}
    stop = (
        meta.get("done_reason") or meta.get("stop_reason") or meta.get("finish_reason")
    )
    if stop:
        health["stop_reason"] = stop
    for key, name in OLLAMA_SECONDS.items():
        if meta.get(key) is not None:
            health[name] = round(meta[key] / 1e9, 2)
    for tokens, seconds, name in (
        ("prompt_eval_count", "prompt_seconds", "prompt_tok_s"),
        ("eval_count", "generation_seconds", "generation_tok_s"),
    ):
        if meta.get(tokens) and health.get(seconds):
            health[name] = round(meta[tokens] / health[seconds], 1)
    return health


def ollama_snapshot(base_url: str) -> list[dict] | None:
    """The models Ollama has loaded and how much of each sits in VRAM; None
    when Ollama can't be reached"""
    try:
        models = httpx.get(f"{base_url}/api/ps", timeout=5).json()["models"]
    except (httpx.HTTPError, ValueError, KeyError) as e:
        logger.debug(f"Could not read {base_url}/api/ps: {e}")
        return None
    return [
        {
            "model": m["name"],
            "size_gb": round(m["size"] / 1e9, 2),
            "vram_gb": round(m.get("size_vram", 0) / 1e9, 2),
            "on_gpu": round(m.get("size_vram", 0) / m["size"], 2) if m["size"] else 0,
            "context_length": m.get("context_length"),
        }
        for m in models
    ]


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
        self.cut_off = 0  # Replies that hit the output cap
        self.empty = 0  # Replies with neither text nor a tool call
        # Ollama only: seconds per phase, and tokens generated
        self.ollama: dict[str, float] = {}
        self._pending: dict[UUID, dict] = {}
        self._lock = threading.Lock()  # Tasks run in parallel threads

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
        health = call_health(message)
        empty = not message.tool_calls and not message.text().strip()
        with self._lock:
            self.input_tokens += usage.get("input_tokens", 0)
            self.max_input_tokens = max(
                self.max_input_tokens, usage.get("input_tokens", 0)
            )
            self.output_tokens += usage.get("output_tokens", 0)
            self.cut_off += health.get("stop_reason") in CUT_OFF
            self.empty += empty
            if "generation_seconds" in health:
                for name in OLLAMA_SECONDS.values():
                    total = self.ollama.get(name, 0) + health.get(name, 0)
                    self.ollama[name] = round(total, 2)
                self.ollama["generation_tokens"] = self.ollama.get(
                    "generation_tokens", 0
                ) + usage.get("output_tokens", 0)
        self._write(
            run_id,
            # Structured calls over function calling (OpenRouter) arrive as tool calls
            response=message.content or message.tool_calls,
            input_tokens=usage.get("input_tokens"),
            output_tokens=usage.get("output_tokens"),
            # Part of output_tokens; billed as output by hosted providers
            reasoning_tokens=(usage.get("output_token_details") or {}).get("reasoning"),
            **health,
            **({"empty": True} if empty else {}),
        )

    def on_llm_error(self, error, *, run_id, **kwargs):
        self._write(run_id, error=repr(error))

    def _write(self, run_id: UUID, **fields):
        call = self._pending.pop(run_id, {})
        started = call.pop("started", time.time())
        record = {
            "time": datetime.now().isoformat(timespec="seconds"),
            **call,
            "seconds": round(time.time() - started, 2),
            **fields,
        }
        with self._lock, self.path.open("a") as f:
            self.calls += 1
            f.write(json.dumps(record, default=str) + "\n")
