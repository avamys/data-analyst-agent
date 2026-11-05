"""Eval runner: run.py once per case × repeat, in parallel; one JSONL line per run

Versions: "current" runs the working tree, "baseline" the tagged baseline from a
git worktree. Each run gets its own runs directory under evals/runs/ (gitignored);
results go to evals/results/<suite id>.jsonl (committed). A run that fails, times
out or crashes is a result, not an error of the suite. A snapshot keeps what the
graders read of a suite's runs, in evals/snapshots/ (committed), so CI can grade it.
"""

import json
import os
import signal
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from dotenv import dotenv_values

from evals.cases import Case, dataset, load_case
from evals.graders import fetch_prices, grade

ROOT = Path(__file__).resolve().parent.parent
RUNS_DIR = ROOT / "evals" / "runs"
RESULTS_DIR = ROOT / "evals" / "results"
WORKTREES_DIR = ROOT / "evals" / "worktrees"
SNAPSHOTS_DIR = ROOT / "evals" / "snapshots"
BASELINE_TAG = "v0.1.1-baseline-hosted"


@dataclass
class Config:
    version: str  # "current" or "baseline"
    provider: str
    model: str
    preset: str | None = None  # current version only
    repeats: int = 1
    jobs: int = 4
    timeout_s: int = 3600


def _git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=True
    ).stdout.strip()


def checkout(version: str) -> Path:
    """Directory to run a version from; the baseline gets a synced worktree"""
    if version == "current":
        return ROOT
    path = WORKTREES_DIR / BASELINE_TAG
    if not path.exists():
        _git("worktree", "add", "--detach", str(path), BASELINE_TAG)
        # Once, before parallel runs would all try to create its environment
        subprocess.run(["uv", "sync", "--quiet"], cwd=path, env=_env({}), check=True)
    return path


def version_id(version: str) -> str:
    """The code a version runs: commit (+ "-dirty"), or the baseline tag"""
    if version == "baseline":
        return BASELINE_TAG
    dirty = _git("status", "--porcelain", "--untracked-files=no")
    return _git("rev-parse", "--short", "HEAD") + ("-dirty" if dirty else "")


def command(config: Config, case: Case, csv: Path) -> list[str]:
    cmd = ["uv", "run", "python", "run.py", str(csv), "--target", case.target]
    cmd += ["--model", config.model]
    if config.version == "current":  # the baseline reads MODEL_PROVIDER only
        cmd += ["--provider", config.provider]
        if config.preset:
            cmd += ["--preset", config.preset]
    return cmd


def _env(extra: dict[str, str]) -> dict[str, str]:
    """The environment of a run: .env (for API keys), then the real environment"""
    env = {k: v for k, v in dotenv_values(ROOT / ".env").items() if v is not None}
    env.update(os.environ)
    env.pop("VIRTUAL_ENV", None)  # each checkout uses its own .venv
    env.update(extra)
    return env


def _execute(
    cmd: list[str], cwd: Path, env: dict, log: Path, timeout_s: int
) -> int | None:
    """Run cmd, output to log; the exit code, or None when it timed out"""
    with log.open("w") as out:
        proc = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=env,
            stdout=out,
            stderr=subprocess.STDOUT,
            start_new_session=True,  # so a timeout kills uv and the run under it
        )
        try:
            return proc.wait(timeout=timeout_s)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
            return None


def run_one(
    config: Config,
    case: Case,
    repeat: int,
    suite_dir: Path,
    cwd: Path,
    prices: dict | None = None,
) -> dict:
    """Run one case once; the result line (run_meta.json figures included)"""
    runs_dir = suite_dir / case.name / f"r{repeat}"
    runs_dir.mkdir(parents=True, exist_ok=True)
    env = _env(
        {
            "MODEL_PROVIDER": config.provider,
            "RUNS_DIRECTORY": str(runs_dir),
            # One LangSmith project per suite: traces grouped by version and suite
            "LANGSMITH_PROJECT": f"evals-{suite_dir.name}",
            "LANGCHAIN_PROJECT": f"evals-{suite_dir.name}",
            # Trace metadata (agent/tracing.py); the tagged baseline ignores them
            "EVAL_CASE": case.name,
            "EVAL_REPEAT": str(repeat),
            "EVAL_VERSION": config.version,
        }
    )
    start = time.time()
    exit_code = _execute(
        command(config, case, dataset(case)),
        cwd,
        env,
        runs_dir / "output.log",
        config.timeout_s,
    )
    run_dir = next(
        (p for p in runs_dir.iterdir() if p.is_dir() and not p.is_symlink()), None
    )
    meta_file = run_dir / "run_meta.json" if run_dir else None
    meta = json.loads(meta_file.read_text()) if meta_file and meta_file.exists() else {}
    if exit_code is None:
        status = "timeout"
    else:
        status = meta.get("status", "crashed")  # no run_meta: died before starting
    return {
        "case": case.name,
        "repeat": repeat,
        "version": config.version,
        "code": version_id(config.version),
        "provider": config.provider,
        "model": config.model,
        "preset": config.preset if config.version == "current" else None,
        "status": status,
        "exit_code": exit_code,
        "seconds": round(time.time() - start, 1),
        "run_dir": str(run_dir.relative_to(ROOT)) if run_dir else None,
        "has_report": bool(run_dir and (run_dir / "report.md").exists()),
        **{
            key: meta.get(key)
            for key in (
                "llm_calls",
                "input_tokens",
                "output_tokens",
                "tasks_completed",
                "tasks_failed",
                "unverified_numbers",
                "run_id",
                "trace_url",
            )
        },
        "grades": grade(case, run_dir, prices) if run_dir else None,
    }


def regrade(results: Path) -> None:
    """Recompute the grades of every line of a results file, in place"""
    prices = fetch_prices()
    lines = [json.loads(line) for line in results.read_text().splitlines()]
    for line in lines:
        run_dir = ROOT / line["run_dir"] if line["run_dir"] else None
        case = load_case(line["case"])
        line["grades"] = grade(case, run_dir, prices) if run_dir else None
    results.write_text("".join(json.dumps(line) + "\n" for line in lines))


def snapshot_path(run_dir: str) -> Path:
    """Where the snapshot of a run directory (as a result line names it) lives"""
    return SNAPSHOTS_DIR / Path(run_dir).relative_to("evals/runs")


def snapshot(results: Path) -> None:
    """Copy what the graders read from each run of a suite (evals/graders.py):
    run_meta.json, report.md, and of the task results and plan only the review
    verdicts and task ids. Not the LLM calls, so CI can't check the cost"""
    for line in (json.loads(x) for x in results.read_text().splitlines()):
        if not line["run_dir"]:
            continue
        src, dst = ROOT / line["run_dir"], snapshot_path(line["run_dir"])
        dst.mkdir(parents=True, exist_ok=True)
        for name in ("run_meta.json", "report.md"):
            if (src / name).exists():
                (dst / name).write_bytes((src / name).read_bytes())
        for result in src.glob("tasks/*/result.json"):
            task = json.loads(result.read_text())
            kept = {"task_id": task["task_id"]}
            if "reviews" in task:  # the baseline has none
                kept["revisions"] = task["revisions"]
                kept["reviews"] = [{"verdict": r["verdict"]} for r in task["reviews"]]
            out = dst / result.relative_to(src)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(kept, indent=1) + "\n")
        for plan in src.glob("state/*_plan.json"):
            ids = [{"id": b["id"]} for b in json.loads(plan.read_text())["backlog"]]
            out = dst / plan.relative_to(src)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps({"backlog": ids}, indent=1) + "\n")


def run_suite(config: Config, cases: list[Case]) -> Path:
    """Every case × repeat, `jobs` at a time; returns the results file"""
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    suite_id = f"{stamp}_{config.version}_{config.model.replace('/', '-')}"
    suite_dir = RUNS_DIR / suite_id
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    results = RESULTS_DIR / f"{suite_id}.jsonl"
    cwd = checkout(config.version)
    prices = fetch_prices()
    for case in cases:
        dataset(case)  # generate or download each dataset once, up front
    jobs = [(case, r) for r in range(1, config.repeats + 1) for case in cases]
    lock = threading.Lock()
    print(f"Suite {suite_id}: {len(jobs)} runs, {config.jobs} at a time")
    with ThreadPoolExecutor(max_workers=config.jobs) as pool:
        futures = [
            pool.submit(run_one, config, c, r, suite_dir, cwd, prices) for c, r in jobs
        ]
        for done, future in enumerate(as_completed(futures), 1):
            line = future.result()
            with lock, results.open("a") as f:
                f.write(json.dumps(line) + "\n")
            print(
                f"[{done}/{len(jobs)}] {line['case']} r{line['repeat']}: "
                f"{line['status']} in {line['seconds']:.0f}s"
            )
    return results
