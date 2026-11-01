"""Main entry point for the data analysis agent system"""

import argparse
import logging
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv

# Load before anything reads LangSmith env vars
load_dotenv(".env")

from agent.config import settings  # noqa: E402
from agent.data_loader import generate_dataset_info, load_dataset  # noqa: E402
from agent.graph import build_hierarchical_graph  # noqa: E402
from agent.logging_config import setup_logging  # noqa: E402
from agent.run_store import LLMCallRecorder, RunStore  # noqa: E402
from agent.tracing import trace_url, tracing_enabled  # noqa: E402

logger = logging.getLogger(__name__)


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout.strip()


def main():
    """Run the data analysis workflow"""
    parser = argparse.ArgumentParser(description="Data Analysis Agent")
    parser.add_argument("csv_path", type=Path, help="Path to the CSV dataset")
    parser.add_argument("--target", help="Target column (detected when omitted)")
    parser.add_argument("--max-tasks", type=int, help="Upper bound on planned tasks")
    parser.add_argument("--model", help="Model for all agents (overrides settings)")
    args = parser.parse_args()

    if not args.csv_path.exists():
        parser.error(f"Dataset not found: {args.csv_path}")
    if args.max_tasks is not None:
        settings.max_tasks = args.max_tasks
    if args.model:
        settings.analyst_model = settings.coder_model = settings.reporter_model = (
            args.model
        )

    dataset = args.csv_path.stem
    store = RunStore(settings.runs_directory, dataset, settings.analyst_model)
    setup_logging(settings.log_level, log_file=store.path / "run.log")
    logger.info(f"Run directory: {store.path}")

    df = load_dataset(str(args.csv_path))
    dataset_info = generate_dataset_info(df, str(args.csv_path))
    workflow = build_hierarchical_graph()
    initial_state = {
        "dataset_info": dataset_info,
        # Absolute, because task scripts run inside their task directories
        "dataset_path": str(args.csv_path.resolve()),
        "target_column": args.target,
        "run_dir": str(store.path.resolve()),
    }

    commit = _git("rev-parse", "--short", "HEAD")
    recorder = LLMCallRecorder(store.path / "llm_calls.jsonl")
    run_id = uuid4()
    config = {
        "run_id": run_id,
        "run_name": f"analysis:{dataset}",
        "tags": [dataset, settings.analyst_model],
        "metadata": {"commit": commit, "run_dir": store.path.name},
        "callbacks": [recorder],
    }
    meta = {
        "status": "running",
        "started": datetime.now().isoformat(timespec="seconds"),
        "command": sys.argv,
        "commit": commit,
        "dirty": bool(_git("status", "--porcelain", "--untracked-files=no")),
        "settings": settings.model_dump(exclude={"openai_api_key"}),
        "nodes": [],
    }
    store.write_json("run_meta.json", meta)

    logger.info(
        f"Running analysis flow (LangSmith tracing {'on' if tracing_enabled() else 'off'})..."
    )
    result = {}
    start = node_start = time.time()
    try:
        # "updates" gives each node's output, "values" the full state after it.
        # subgraphs=True also streams the tasks inside the execution step, so
        # each task is saved as soon as it finishes.
        for namespace, mode, chunk in workflow.stream(
            initial_state,
            config=config,
            stream_mode=["updates", "values"],
            subgraphs=True,
        ):
            if mode == "values":
                if not namespace:
                    result = chunk
                continue
            for node, update in chunk.items():
                if namespace:
                    results = update.get("completed_tasks", []) + update.get(
                        "failed_tasks", []
                    )
                    store.write_tasks([r for r in results if r.task_id == node])
                    continue
                step = len(meta["nodes"]) + 1
                meta["nodes"].append(
                    {"node": node, "seconds": round(time.time() - node_start, 1)}
                )
                store.write_json(f"state/{step:02d}_{node}.json", update)
                store.write_json("run_meta.json", meta)
                node_start = time.time()
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
            tasks_completed=len(result.get("completed_tasks", [])),
            tasks_failed=len(result.get("failed_tasks", [])),
            trace_url=trace_url(run_id),
        )
        store.write_json("run_meta.json", meta)
        if meta["trace_url"]:
            logger.info(f"LangSmith trace: {meta['trace_url']}")
        logger.info(f"Run {meta['status']} in {meta['seconds']}s: {store.path}")

    if result.get("report"):
        store.write_text("report.md", result["report"])
        logger.info(f"Report saved to: {store.path / 'report.md'}")


if __name__ == "__main__":
    main()
