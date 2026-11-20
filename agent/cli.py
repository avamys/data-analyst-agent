"""Command line: `analyst run <csv>` runs one analysis into its own run directory;
`analyst ask <run dir> "<question>"` answers a question about it, in that run"""

import argparse
import json
import logging
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from langgraph.types import Command

from agent import context
from agent.config import PRESETS, settings
from agent.core.llm_manager import LLMManager
from agent.costs import fetch_prices
from agent.data_loader import generate_dataset_info, load_dataset
from agent.execution.runner import network_blocked
from agent.graph import build_hierarchical_graph, build_question_graph
from agent.html_report import write_html
from agent.logging_config import setup_logging
from agent.progress import Progress
from agent.run_grades import question_grades, run_grades
from agent.run_store import (
    LLMCallRecorder,
    RunNotLoadable,
    RunStore,
    load_run,
    ollama_snapshot,
    state_files,
)
from agent.states import Question
from agent.tracing import eval_metadata, trace_url, tracing_enabled

logger = logging.getLogger(__name__)

# What a question takes from its run unless flags say otherwise: the same models
# and limits answer it
RUN_SETTINGS = (
    "model_provider",
    "ollama_model",
    "openrouter_model",
    "anthropic_model",
    "analyst_model",
    "coder_model",
    "reporter_model",
    "preset",
    "max_revisions",
    "lead_effort",
    "specialist_effort",
    "llm_num_ctx",
)


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
        "--approve-plan",
        action="store_true",
        help="Show the plan and wait: approve it, or tell the lead what to change",
    )
    run.add_argument(
        "--out", type=Path, help="Directory for run directories (default: runs)"
    )
    ask = commands.add_parser(
        "ask", help="Answer a question about a finished run, recorded in that run"
    )
    ask.add_argument("run_dir", type=Path, help="A run directory under runs/")
    ask.add_argument("question", help="The question, in quotes")
    for command in (run, ask):
        command.add_argument(
            "--provider",
            choices=["ollama", "openrouter", "anthropic"],
            help="Overrides MODEL_PROVIDER"
            + (" and the run's" if command is ask else ""),
        )
        command.add_argument(
            "--preset", choices=list(PRESETS), help="Named settings (overrides PRESET)"
        )
        command.add_argument(
            "--model", help="Model for all agents (overrides settings)"
        )
        command.add_argument(
            "--verbose",
            action="store_true",
            help="Show the full log, not just progress",
        )
    report = commands.add_parser(
        "report", help="Write report.html for an existing run directory"
    )
    report.add_argument("run_dir", type=Path, help="A run directory under runs/")
    return parser


def apply_flags(args: argparse.Namespace) -> None:
    """Command-line flags override the settings"""
    # The preset first, so explicit flags below override it
    if args.preset:
        settings.use_preset(args.preset)
    if getattr(args, "max_tasks", None) is not None:
        settings.max_tasks = args.max_tasks
    if getattr(args, "approve_plan", False):
        settings.plan_approval = True
    if args.provider:
        settings.model_provider = args.provider
    if args.model:
        settings.analyst_model = settings.coder_model = settings.reporter_model = (
            args.model
        )
    if getattr(args, "out", None):
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
        # Flushed: the app finds the run by this line while the run goes on
        print(
            f"Run directory: {store.path} ({settings.model_provider}, {model})",
            flush=True,
        )

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
        "recursion_limit": _recursion_limit(settings.max_tasks),
    }
    if settings.plan_approval:
        # The checkpointer keeps the waiting run under this id
        config["configurable"] = {"thread_id": str(run_id)}
    meta = {
        "status": "running",
        "run_id": str(run_id),
        "dataset": dataset,
        "dataset_path": initial_state["dataset_path"],
        "target": target,
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
    start = time.time()
    waited = 0.0  # For the human's replies to the plan; not the run's time
    try:
        inputs = initial_state
        while shown := _stream(
            workflow, inputs, config, store, progress, meta, meta["nodes"], result
        ):
            meta["status"] = "awaiting_approval"
            store.write_json("run_meta.json", meta)
            progress.event({"event": "plan_waiting", **shown})
            asked = time.time()
            reply = read_reply()
            waited += time.time() - asked
            meta["status"] = "running"
            if reply.get("approve"):  # tasks the human added raise the limit
                config["recursion_limit"] = _recursion_limit(
                    max(settings.max_tasks, len(shown["tasks"]))
                )
            inputs = Command(resume=reply)
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
            seconds=round(time.time() - start - waited, 1),
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
        if settings.plan_approval:
            meta["plan_chat"] = result.get("plan_chat", [])
            meta["plan_approved"] = result.get("plan_approved", False)
            meta["seconds_waiting"] = round(waited, 1)
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
        try:
            write_html(store.path)
        except Exception as e:  # never hides the run's own error
            logger.warning(f"Could not write report.html: {e!r}")
        if meta["trace_url"]:
            logger.info(f"LangSmith trace: {meta['trace_url']}")
        logger.info(f"Run {meta['status']} in {meta['seconds']}s: {store.path}")
        report = store.path / "report.html"
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


def _recursion_limit(tasks: int) -> int:
    """Graph steps a run may take: each task is a run_task + review step, once
    more per revision"""
    return 10 + 2 * (tasks + settings.max_follow_ups) * (1 + settings.max_revisions)


class PlanNotApproved(RuntimeError):
    pass


def read_reply() -> dict:
    """The human's reply to the plan, from stdin: a terminal, or the app's pipe"""
    while True:
        print(
            "Type 'approve' to run the plan, or tell the lead what to change: ",
            end="",
            flush=True,
        )
        line = sys.stdin.readline()
        if not line:
            raise PlanNotApproved("Input closed before the plan was approved")
        if line.strip().lower() == "approve":
            return {"approve": True}
        if line.strip():
            return {"message": line.strip()}


def _stream(workflow, state, config, store, progress, meta, nodes, result):
    """Run a graph, or resume it (state is a Command). Each task is saved as
    soon as it has run or been reviewed, each node's update to
    state/NN_<node>.json (numbered after those there) and its time to `nodes`
    in meta; `result` holds the last full state. Returns what the graph shows
    the human when it stops to wait for them, else None."""
    first_step = len(state_files(store.path)) + 1
    known = len(nodes)  # From earlier calls, whose state files are counted
    waiting = None
    node_start = time.time()
    # "updates" gives each node's output, "values" the full state after it,
    # "custom" the progress events sent from inside nodes (agent/progress.py)
    for mode, chunk in workflow.stream(
        state, config=config, stream_mode=["updates", "values", "custom"]
    ):
        if mode == "values":
            result.update(chunk)
            continue
        if mode == "custom":
            progress.event(chunk)
            continue
        for node, update in chunk.items():
            if node == "__interrupt__":
                waiting = update[0].value
                continue
            if isinstance(update, dict):
                tasks = [update.get("under_review")]
                tasks += update.get("completed_tasks", [])[-1:]
                tasks += update.get("failed_tasks", [])[-1:]
                store.write_tasks([t for t in tasks if t is not None])
            step = first_step + len(nodes) - known
            nodes.append({"node": node, "seconds": round(time.time() - node_start, 1)})
            store.write_json(f"state/{step:02d}_{node}.json", update)
            store.write_json("run_meta.json", meta)
            progress.update(node, update)
            node_start = time.time()
    return waiting


def use_run_settings(run_dir: Path) -> None:
    """A question's settings default to its run's (RUN_SETTINGS)"""
    meta = json.loads((run_dir / "run_meta.json").read_text())
    for name, value in (meta.get("settings") or {}).items():
        if name in RUN_SETTINGS:
            setattr(settings, name, value)


def ask_question(run_dir: Path, text: str, verbose: bool = False) -> dict:
    """Answer a question about a finished run; returns its entry in run_meta.json.
    The answer is appended to questions.md, its tasks go to tasks/q<N>_*, its
    LLM calls to questions/q<N>_llm_calls.jsonl, its progress to progress.jsonl."""
    run_dir = run_dir.resolve()
    state = load_run(run_dir)  # RunNotLoadable: it can't take questions
    store = RunStore.open(run_dir)
    meta = json.loads((run_dir / "run_meta.json").read_text())
    questions = meta.setdefault("questions", [])
    number = len(questions) + 1  # failed questions keep their number
    (run_dir / "questions").mkdir(exist_ok=True)
    setup_logging(
        settings.log_level if verbose else "WARNING",
        log_file=run_dir / "questions" / f"q{number}.log",
    )
    model = LLMManager.resolve_config("lead")[0]
    if not verbose:
        print(
            f"Question {number} on {run_dir} ({settings.model_provider}, {model})",
            flush=True,
        )
    progress = Progress(run_dir / "progress.jsonl", echo=not verbose)
    progress.known |= {r.task_id for r in state.completed_tasks + state.failed_tasks}

    # A question that failed may have left work half done; its accepted tasks stay
    state = state.model_copy(
        update={
            "backlog": [],
            "under_review": None,
            "questions": [*state.questions, Question(number=number, text=text)],
        }
    )
    recorder = LLMCallRecorder(
        run_dir / "questions" / f"q{number}_llm_calls.jsonl",
        num_ctx=settings.llm_num_ctx if settings.model_provider == "ollama" else None,
    )
    run_id = uuid4()
    commit = _git("rev-parse", "--short", "HEAD")
    dataset = meta.get("dataset") or run_dir.name
    config = {
        "run_id": run_id,
        "run_name": f"question:{dataset}",
        "tags": [dataset, settings.model_provider, model, "question"],
        "metadata": {"commit": commit, "run_dir": run_dir.name, "question": number},
        "callbacks": [recorder],
        "recursion_limit": 10
        + 2 * settings.max_question_tasks * (1 + settings.max_revisions),
    }
    entry = {
        "number": number,
        "question": text,
        "status": "running",
        "run_id": str(run_id),
        "started": datetime.now().isoformat(timespec="seconds"),
        "commit": commit,
        "provider": settings.model_provider,
        "model": model,
        "nodes": [],
    }
    questions.append(entry)
    store.write_json("run_meta.json", meta)
    progress.event({"event": "question", "number": number, "question": text})

    result = {}
    start = time.time()
    try:
        workflow = build_question_graph()
        _stream(workflow, state, config, store, progress, meta, entry["nodes"], result)
        answered = result["questions"][-1]
        _append_answer(run_dir / "questions.md", answered)
        entry.update(
            status="ok",
            tasks=answered.tasks,
            facts=answered.facts,
            unverified_numbers=answered.unverified_numbers,
        )
    except KeyboardInterrupt:
        entry["status"] = "interrupted"
        raise
    except Exception as e:
        entry["status"] = "failed"
        entry["error"] = repr(e)
        raise
    finally:
        mine = f"q{number}_"
        store.write_tasks(
            [
                r
                for r in result.get("completed_tasks", [])
                + result.get("failed_tasks", [])
                if r.task_id.startswith(mine)
            ]
        )
        entry.update(
            finished=datetime.now().isoformat(timespec="seconds"),
            seconds=round(time.time() - start, 1),
            llm_calls=recorder.calls,
            input_tokens=recorder.input_tokens,
            output_tokens=recorder.output_tokens,
            calls_cut_off=recorder.cut_off,
            calls_window_full=recorder.window_full,
            calls_empty=recorder.empty,
            trace_url=trace_url(run_id),
        )
        prices = fetch_prices() if settings.model_provider != "ollama" else None
        entry["grades"] = question_grades(run_dir, number, prices)
        store.write_json("run_meta.json", meta)
        try:
            write_html(run_dir)
        except Exception as e:  # never hides the question's own error
            logger.warning(f"Could not write report.html: {e!r}")
        progress.event(
            {
                "event": "question_done",
                "number": number,
                "status": entry["status"],
                "seconds": entry["seconds"],
                "error": entry.get("error"),
                "grades": entry["grades"],
            }
        )
    if not verbose:
        print("\n" + result["questions"][-1].answer, flush=True)
    return entry


def _append_answer(path: Path, question: Question) -> None:
    """questions.md: each question and its answer, after a heading for them all.
    In the run directory, so chart paths are the same as in report.md."""
    text = "" if path.exists() else "## Questions after the report\n"
    text += f"\n### Q{question.number}. {question.text}\n\n{question.answer}\n"
    with path.open("a") as f:
        f.write(text)


def main(argv: list[str] | None = None) -> int:
    # Into the environment for LangSmith (Settings reads .env itself)
    load_dotenv(".env")
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "report":
        if not (args.run_dir / "run_meta.json").exists():
            parser.error(f"Not a run directory: {args.run_dir}")
        print(write_html(args.run_dir))
        return 0
    if args.command == "ask":
        if not (args.run_dir / "run_meta.json").exists():
            parser.error(f"Not a run directory: {args.run_dir}")
        use_run_settings(args.run_dir)
        apply_flags(args)
        try:
            ask_question(args.run_dir, args.question, verbose=args.verbose)
        except RunNotLoadable as e:  # say why the run can't take questions
            parser.error(str(e))
        return 0
    if not args.csv_path.exists():
        parser.error(f"Dataset not found: {args.csv_path}")
    apply_flags(args)
    run_analysis(args.csv_path, args.target, verbose=args.verbose)
    return 0


if __name__ == "__main__":
    sys.exit(main())
