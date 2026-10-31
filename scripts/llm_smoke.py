"""Check the configured LLM setup before a long run.

Verifies Ollama is reachable, the configured models are pulled, and one
structured-output call parses. Reports speed, GPU offload and the LangSmith
trace URL when tracing is enabled.

Usage: uv run python scripts/llm_smoke.py
"""

import sys
import time
from uuid import uuid4

import httpx
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv(".env")

from agent.config import settings  # noqa: E402
from agent.core.llm_manager import LLMManager  # noqa: E402
from agent.tracing import trace_url, tracing_enabled  # noqa: E402


class Answer(BaseModel):
    test_name: str
    used_for: str


def main() -> int:
    models = sorted(
        {settings.analyst_model, settings.coder_model, settings.reporter_model}
    )
    print(f"Provider: {settings.model_provider} | models: {models}")
    print(
        f"reasoning={settings.llm_reasoning} num_ctx={settings.llm_num_ctx} "
        f"max_tokens={settings.llm_max_tokens} timeout={settings.llm_timeout_s}s "
        f"num_gpu={settings.llm_num_gpu or 'auto'}"
    )
    print(f"LangSmith tracing: {'on' if tracing_enabled() else 'off'}")

    if settings.model_provider == "ollama":
        try:
            tags = httpx.get(f"{settings.ollama_base_url}/api/tags", timeout=5).json()
        except httpx.HTTPError as e:
            print(f"FAIL: Ollama not reachable at {settings.ollama_base_url}: {e}")
            return 1
        pulled = {m["name"] for m in tags["models"]}
        missing = [m for m in models if m not in pulled]
        if missing:
            print(f"FAIL: models not pulled: {missing} (available: {sorted(pulled)})")
            return 1
        print("OK: Ollama reachable, models pulled")

    llm = LLMManager.get_llm("orchestrator").with_structured_output(
        Answer, include_raw=True
    )
    run_id = uuid4()
    start = time.time()
    out = llm.invoke(
        "Name one statistical test for two categorical variables and what it is used for.",
        config={"run_name": "llm-smoke", "run_id": run_id, "tags": ["smoke"]},
    )
    secs = time.time() - start
    if out["parsing_error"] or out["parsed"] is None:
        print(f"FAIL: structured output did not parse: {out['parsing_error']}")
        return 1
    usage = out["raw"].usage_metadata or {}
    meta = out["raw"].response_metadata
    print(f"OK: structured output parsed in {secs:.0f}s -> {out['parsed']}")
    print(f"Tokens in/out: {usage.get('input_tokens')}/{usage.get('output_tokens')}")
    if meta.get("eval_duration"):  # Ollama timings, in nanoseconds
        print(
            f"Generation: {meta['eval_count'] / (meta['eval_duration'] / 1e9):.1f} tok/s "
            f"| model load: {meta.get('load_duration', 0) / 1e9:.0f}s"
        )

    if settings.model_provider == "ollama":
        for m in httpx.get(f"{settings.ollama_base_url}/api/ps", timeout=5).json()[
            "models"
        ]:
            share = m.get("size_vram", 0) / m["size"] if m.get("size") else 0
            print(
                f"Loaded: {m['name']} | ctx {m.get('context_length')} | "
                f"{share:.0%} on GPU ({m.get('size_vram', 0) / 1e9:.1f}/{m['size'] / 1e9:.1f} GB)"
            )

    if url := trace_url(run_id):
        print(f"Trace: {url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
