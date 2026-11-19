"""Check the configured LLM setup before a long run.

Verifies the provider is reachable (Ollama: models pulled; OpenRouter: key valid,
free requests left today) and one structured-output call parses. Reports speed,
GPU offload and the LangSmith trace URL when tracing is enabled.

Usage: uv run python scripts/llm_smoke.py
"""

import sys
import time
from uuid import uuid4

import httpx
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv(".env")

from agent.config import settings  # noqa: E402
from agent.core.llm_manager import LLMManager  # noqa: E402
from agent.tracing import trace_url, tracing_enabled  # noqa: E402


class Answer(BaseModel):
    test_name: str
    used_for: str
    code: str = Field(description="Python code, several lines, running it with scipy")


def main() -> int:
    models = sorted(
        {LLMManager.resolve_config(t)[0] for t in ("lead", "ml", "reporter")}
    )
    print(f"Provider: {settings.model_provider} | models: {models}")
    if settings.model_provider == "openrouter":
        print(
            f"reasoning={settings.openrouter_reasoning} "
            f"max_tokens={settings.llm_max_tokens} timeout={settings.llm_timeout_s}s"
        )
    elif settings.model_provider == "ollama":
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

    if settings.model_provider == "openrouter":
        if settings.openrouter_api_key is None:
            print("FAIL: OPENROUTER_API_KEY is not set")
            return 1
        key = settings.openrouter_api_key.get_secret_value()
        resp = httpx.get(
            f"{settings.openrouter_base_url}/key",
            headers={"Authorization": f"Bearer {key}"},
            timeout=10,
        )
        if resp.status_code != 200:
            print(f"FAIL: OpenRouter key check: HTTP {resp.status_code} {resp.text}")
            return 1
        # A reference run makes ~60 calls; free models are capped per UTC day
        free = resp.json()["data"].get("free_model_daily_requests")
        print(f"OK: OpenRouter key valid | free-model requests today: {free}")

    llm = LLMManager.with_structured_output(
        LLMManager.get_llm("lead"), Answer, include_raw=True
    )
    run_id = uuid4()
    start = time.time()
    out = llm.invoke(
        "Name one statistical test for two categorical variables, what it is used "
        "for, and the code to run it.",
        config={"run_name": "llm-smoke", "run_id": run_id, "tags": ["smoke"]},
    )
    secs = time.time() - start
    if out["parsing_error"] or out["parsed"] is None:
        print(f"FAIL: structured output did not parse: {out['parsing_error']}")
        return 1
    # Specialists send code in structured output; some models flatten it to one
    # line, which turns a cell that starts with a comment into a no-op
    if "\n" not in out["parsed"].code:
        print(f"FAIL: code came back without line breaks: {out['parsed'].code!r}")
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
