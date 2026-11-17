"""Token usage and cost of runs, from their llm_calls.jsonl.

Shows tokens and seconds per node (on Ollama split into model loading, prompt
processing and generation) and calls cut off at the output cap, that filled the
context window, or empty. Prices
each run at OpenRouter list prices: at the model it ran with, and at any models
given with --price-as. Projecting a run onto
another model is an estimate: tokenizers differ (often by 10-20%), and reasoning
models add output tokens. A real run on the model gives the firm number.

Usage:
  uv run python scripts/run_cost.py [RUN_DIR ...] [--price-as MODEL ...]
  uv run python scripts/run_cost.py runs/latest --price-as anthropic/claude-sonnet-5.5
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

import httpx

from agent.run_store import CUT_OFF

MODELS_URL = "https://openrouter.ai/api/v1/models"
FIELDS = ("calls", "input", "output", "reasoning", "seconds")
# Ollama only: where a call's seconds went
PHASES = ("load_seconds", "prompt_seconds", "generation_seconds")
HEALTH = ("cut_off", "window_full", "empty")


def summarize_calls(path: Path) -> dict[str, dict[str, float]]:
    """Totals per node (in call order), plus a "total" row"""
    nodes: dict[str, dict[str, float]] = {}
    for line in path.open():
        call = json.loads(line)
        row = nodes.setdefault(
            call.get("node") or "?", dict.fromkeys(FIELDS + PHASES + HEALTH, 0)
        )
        row["calls"] += 1
        row["input"] += call.get("input_tokens") or 0
        row["output"] += call.get("output_tokens") or 0
        row["reasoning"] += call.get("reasoning_tokens") or 0
        row["seconds"] += call.get("seconds") or 0
        for phase in PHASES:
            row[phase] += call.get(phase) or 0
        row["window_full"] += bool(call.get("window_full"))
        row["cut_off"] += call.get("stop_reason") in CUT_OFF and not call.get(
            "window_full"
        )
        row["empty"] += bool(call.get("empty"))
    nodes["total"] = {
        f: sum(row[f] for row in nodes.values()) for f in FIELDS + PHASES + HEALTH
    }
    return nodes


def run_model(path: Path) -> str | None:
    """The model most calls of a run went to"""
    models = Counter(json.loads(line).get("model") for line in path.open())
    return models.most_common(1)[0][0] if models else None


def openrouter_id(model: str) -> str:
    """Anthropic API ids (claude-haiku-5-5) as OpenRouter names them"""
    if model.startswith("claude-"):
        return "anthropic/" + re.sub(r"-(\d+)-(\d+)$", r"-\1.\2", model)
    return model


def estimate_cost(total: dict[str, float], price: dict[str, str]) -> float:
    """USD for the run's tokens at a model's per-token prices"""
    return total["input"] * float(price["prompt"]) + total["output"] * float(
        price["completion"]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("runs", nargs="*", type=Path, default=[Path("runs/latest")])
    parser.add_argument(
        "--price-as", nargs="+", default=[], metavar="MODEL", help="OpenRouter ids"
    )
    args = parser.parse_args()

    prices = {m["id"]: m["pricing"] for m in httpx.get(MODELS_URL).json()["data"]}
    for model in args.price_as:
        if openrouter_id(model) not in prices:
            print(f"Unknown OpenRouter model: {model}")
            return 1

    for run in args.runs:
        log = run / "llm_calls.jsonl"
        if not log.exists():
            print(f"No llm_calls.jsonl in {run}")
            return 1
        nodes = summarize_calls(log)
        model = run_model(log)
        local = nodes["total"]["generation_seconds"] > 0
        print(f"\n## {run.resolve().name} ({model})\n")
        header = "| node | calls | input | output | of which reasoning | seconds |"
        if local:
            header += " load s | prompt s | generation s |"
        print(header)
        print("|---|" + "---:|" * (header.count("|") - 2))
        for node, row in nodes.items():
            line = (
                f"| {node} | {row['calls']} | {row['input']:,} | {row['output']:,} "
                f"| {row['reasoning']:,} | {row['seconds']:,.0f} |"
            )
            if local:
                line += "".join(f" {row[p]:,.0f} |" for p in PHASES)
            print(line)
        total = nodes["total"]
        if total["cut_off"] or total["window_full"] or total["empty"]:
            print(
                f"\n**{total['cut_off']} calls cut off at the output cap, "
                f"{total['window_full']} filled the context window, "
                f"{total['empty']} empty.**"
            )

        print("\n| priced as | $/M input | $/M output | cost (USD) |")
        print("|---|---:|---:|---:|")
        for name in [model, *args.price_as]:
            price = prices.get(openrouter_id(name))
            if price is None:
                print(f"| {name} | | | not on OpenRouter (local) |")
                continue
            print(
                f"| {name} | {float(price['prompt']) * 1e6:.2f} "
                f"| {float(price['completion']) * 1e6:.2f} "
                f"| {estimate_cost(nodes['total'], price):.4f} |"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
