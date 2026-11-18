"""Command line: `analyst run <csv>` runs one analysis into its own run directory"""

import argparse
import logging
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv

from agent import context
from agent.config import PRESETS, settings
from agent.core.llm_manager import LLMManager
from agent.costs import fetch_prices
from agent.data_loader import generate_dataset_info, load_dataset
from agent.execution.runner import network_blocked
from agent.graph import build_hierarchical_graph
from agent.logging_config import setup_logging
from agent.progress import Progress
from agent.run_grades import run_grades
from agent.run_store import LLMCallRecorder, RunStore, ollama_snapshot
from agent.tracing import eval_metadata, trace_url, tracing_enabled

logger = logging.getLogger(__name__)


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout.strip()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="analyst", description="Data Analysis Agent")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run", help="Analyse a CSV and write a report")
    run.add_argument("csv_path", type=Path, help="Path to the CSV dataset")
    run.add_argument("--target", help="Target column (detected when omitted)")
    run.add_argument("--max-tasks", type=int, help="Upper bound on planned tasks")
    run.add_argument(
        "--provider",
        choices=["ollama", "openrouter", "anthropic"],
        help="Overrides MODEL_PROVIDER",
    )
    run.add_argument(
        "--preset", choices=list(PRESETS), help="Named settings (overrides PRESET)"
    )
    run.add_argument("--model", help="Model for all agents (overrides settings)")
    run.add_argument(
        "--out", type=Path, help="Directory for run directories (default: runs)"
    )
    run.add_argument(
        "--verbose", action="store_true", help="Show the full log, not just progress"
    )
    return parser


def apply_flags(args: argparse.Namespace) -> None:
    """Command-line flags override the settings"""
    # The preset first, so explicit flags below override it
    if args.preset:
        settings.use_preset(args.preset)
    if args.max_tasks is not None:
        settings.max_tasks = args.max_tasks
    if args.provider:
        settings.model_provider = args.provider
    if args.model:
        settings.analyst_model = settings.coder_model = settings.reporter_model = (
            args.model
        )
    if args.out:
        settings.runs_directory = str(args.out)


def run_analysis(
    csv_path: Path, target: str | None = None, verbose: bool = False
) -> Path:
    """Run the analysis workflow; returns the run directory. The console shows
    progress and warnings, or with `verbose` the full log; run.log has it all."""
    dataset = csv_path.stem
    model = LLMManager.resolve_config("lead")[0]
    store = RunStore(settings.runs_directory, dataset, model)
    setup_logging(
        settings.log_level if verbose else "WARNING", log_file=store.path / "run.log"
    )
    progress = Progress(store.path / "progress.jsonl", echo=not verbose)
    logger.info(f"Run directory: {store.path}")
    if not verbose:
        print(f"Run directory: {store.path} ({settings.model_provider}, {model})")

    df = load_dataset(str(csv_path))
    dataset_info = generate_dataset_info(df, str(csv_path))
    workflow = build_hierarchical_graph()
    initial_state = {
        "dataset_info": dataset_info,
        # Absolute, because task scripts run inside their task directories
        "dataset_path": str(csv_path.resolve()),
        "target_column": target,
        "run_dir": str(store.path.resolve()),
    }

    commit = _git("rev-parse", "--short", "HEAD")
    recorder = LLMCallRecorder(
        store.path / "llm_calls.jsonl",
        num_ctx=settings.llm_num_ctx if settings.model_provider == "ollama" else None,
    )
    run_id = uuid4()
    config = {
        "run_id": run_id,
        "run_name": f"analysis:{dataset}",
        "tags": [dataset, settings.model_provider, model, settings.preset],
        "metadata": {"commit": commit, "run_dir": store.path.name, **eval_metadata()},
        "callbacks": [recorder],
        # Each task is a run_task + review step, once more per revision
        "recursion_limit": 10
        + 2
        * (settings.max_tasks + settings.max_follow_ups)
        * (1 + settings.max_revisions),
    }
    meta = {
        "status": "running",
        "run_id": str(run_id),
        "started": datetime.now().isoformat(timespec="seconds"),
        "command": sys.argv,
        "commit": commit,
        "dirty": bool(_git("status", "--porcelain", "--untracked-files=no")),
        "network_blocked": network_blocked(),
        "parallel_tasks": settings.parallel_tasks,
        "settings": settings.model_dump(
            exclude={"openrouter_api_key", "anthropic_api_key"}
        ),
        "nodes": [],
    }
    store.write_json("run_meta.json", meta)

    logger.info(
        f"Running analysis flow (LangSmith tracing {'on' if tracing_enabled() else 'off'})..."
    )
    result = {}
    start = node_start = time.time()
    try:
        # "updates" gives each node's output, "values" the full state after it,
        # "custom" the progress events sent from inside nodes (agent/progress.py)
        for mode, chunk in workflow.stream(
            initial_state, config=config, stream_mode=["updates", "values", "custom"]
        ):
            if mode == "values":
                result = chunk
                continue
            if mode == "custom":
                progress.event(chunk)
                continue
            for node, update in chunk.items():
                # Save each task as soon as it has run or been reviewed
                if isinstance(update, dict):
                    tasks = [update.get("under_review")]
                    tasks += update.get("completed_tasks", [])[-1:]
                    tasks += update.get("failed_tasks", [])[-1:]
                    store.write_tasks([t for t in tasks if t is not None])
                step = len(meta["nodes"]) + 1
                meta["nodes"].append(
                    {"node": node, "seconds": round(time.time() - node_start, 1)}
                )
                store.write_json(f"state/{step:02d}_{node}.json", update)
                store.write_json("run_meta.json", meta)
                progress.update(node, update)
                node_start = time.time()
        if result.get("report"):
            store.write_text("report.md", result["report"])
            logger.info(f"Report saved to: {store.path / 'report.md'}")
        meta["status"] = "ok"
    except KeyboardInterrupt:
        meta["status"] = "interrupted"
        raise
    except Exception as e:
        meta["status"] = "failed"
        meta["error"] = repr(e)
        raise
    finally:
        # Written even when the run fails, so it can be inspected
        store.write_tasks(
            result.get("completed_tasks", []) + result.get("failed_tasks", [])
        )
        meta.update(
            finished=datetime.now().isoformat(timespec="seconds"),
            seconds=round(time.time() - start, 1),
            llm_calls=recorder.calls,
            input_tokens=recorder.input_tokens,
            output_tokens=recorder.output_tokens,
            # Replies that hit the output cap or (Ollama) filled the context
            # window, and replies with nothing in them
            calls_cut_off=recorder.cut_off,
            calls_window_full=recorder.window_full,
            calls_empty=recorder.empty,
            tasks_completed=len(result.get("completed_tasks", [])),
            tasks_failed=len(result.get("failed_tasks", [])),
            unverified_numbers=result.get("unverified_numbers"),
            # What the agents didn't see: prompt caps that cut, prompts near
            # the context window (see agent/context.py)
            context={
                "largest_prompt_tokens": recorder.max_input_tokens,
                "window_warnings": context.warnings,
                "prompt_cuts": dict(context.cuts),
            },
            trace_url=trace_url(run_id),
        )
        if recorder.ollama:
            # Where local time went, and how the model sat in VRAM at the end
            meta["ollama"] = {
                **recorder.ollama,
                "loaded": ollama_snapshot(settings.ollama_base_url),
            }
        store.write_json("run_meta.json", meta)
        # Graded from the files just written; no prices for local models
        prices = fetch_prices() if settings.model_provider != "ollama" else None
        meta["grades"] = run_grades(store.path, prices)
        store.write_json("run_meta.json", meta)
        if meta["trace_url"]:
            logger.info(f"LangSmith trace: {meta['trace_url']}")
        logger.info(f"Run {meta['status']} in {meta['seconds']}s: {store.path}")
        report = store.path / "report.md"
        progress.event(
            {
                "event": "run_done",
                "status": meta["status"],
                "seconds": meta["seconds"],
                "error": meta.get("error"),
                "report": str(report) if report.exists() else None,
                "grades": meta["grades"],
            }
        )
    return store.path


def main(argv: list[str] | None = None) -> int:
    # Into the environment for LangSmith (Settings reads .env itself)
    load_dotenv(".env")
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.csv_path.exists():
        parser.error(f"Dataset not found: {args.csv_path}")
    apply_flags(args)
    run_analysis(args.csv_path, args.target, verbose=args.verbose)
    return 0


if __name__ == "__main__":
    sys.exit(main())
