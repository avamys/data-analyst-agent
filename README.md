# Data Analyst Agent

A local-first, multi-agent data analyst: point it at a CSV and it plans an analysis, runs Python on the data, and writes a report. It runs on a local model through [Ollama](https://ollama.com), with optional tracing in LangSmith.

> **Status: under active rebuild.** The current version is a baseline (tag [`v0.1.0-baseline`](https://github.com/avamys/data-analyst-agent/tree/v0.1.0-baseline)). Its [review](docs/baseline/review.md) found that the agents never see their own results and nobody reviews anybody's work. The redesign, with a lead analyst, specialists that iterate on their output, and reports built from recorded facts, is tracked in [PLAN.md](PLAN.md).

## Quickstart

Requires [uv](https://docs.astral.sh/uv/) and either a running Ollama with the model pulled (`ollama pull qwen3.5:9b`) or an [OpenRouter](https://openrouter.ai) or [Anthropic](https://platform.claude.com) API key (`MODEL_PROVIDER=openrouter|anthropic` in `.env`, or `--provider`).

```bash
uv sync
cp .env.example .env              # pick the provider and model; LangSmith tracing; GPU layers
uv run python scripts/llm_smoke.py   # checks the model setup (about a minute)
uv run python run.py data/titanic.csv --target Survived
```

Each run writes a directory under `runs/` with the full log, every LLM call, the state after each step, every code attempt, and `report.md`. See [docs/baseline/run/](docs/baseline/run/) for an example.

To see a run's token usage per step and its cost at OpenRouter prices, also projected onto other models: `uv run python scripts/run_cost.py runs/latest --price-as anthropic/claude-haiku-5.5`.

## Development

```bash
uv sync --group dev
uv run ruff check && uv run ruff format --check
uv run pytest
```
