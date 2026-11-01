# Data Analyst Agent

A local-first, multi-agent data analyst: point it at a CSV and it plans an analysis, runs Python on the data, and writes a report. It runs on a local model through [Ollama](https://ollama.com), with optional tracing in LangSmith.

> **Status: under active rebuild.** The current version is a baseline (tag [`v0.1.0-baseline`](https://github.com/avamys/data-analyst-agent/tree/v0.1.0-baseline)). Its [review](docs/baseline/review.md) found that the agents never see their own results and nobody reviews anybody's work. The redesign, with a lead analyst, specialists that iterate on their output, and reports built from recorded facts, is tracked in [PLAN.md](PLAN.md).

## Quickstart

Requires [uv](https://docs.astral.sh/uv/) and a running Ollama with the model pulled (`ollama pull qwen3.5:9b`).

```bash
uv sync
cp .env.example .env              # adjust OLLAMA_BASE_URL, LangSmith tracing, GPU layers
uv run python scripts/llm_smoke.py   # checks the model setup (about a minute)
uv run python run.py data/titanic.csv --target Survived
```

Each run writes a directory under `runs/` with the full log, every LLM call, the state after each step, every code attempt, and `report.md`. See [docs/baseline/run/](docs/baseline/run/) for an example.

## Development

```bash
uv sync --group dev
uv run ruff check && uv run ruff format --check
uv run pytest
```
