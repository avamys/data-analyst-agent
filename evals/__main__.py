"""Eval harness CLI

uv run python -m evals run --version current --provider anthropic --repeats 3
uv run python -m evals run --version baseline --provider anthropic --cases titanic
uv run python -m evals grade evals/results/<suite id>.jsonl
uv run python -m evals judge evals/results/<suite id>.jsonl
"""

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(".env")

from agent.config import PRESETS, settings  # noqa: E402
from evals.cases import all_cases, load_case  # noqa: E402
from evals.judge import judge_results  # noqa: E402
from evals.runner import ROOT, Config, regrade, run_suite  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="evals",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run", help="Run cases and write a results file")
    run.add_argument("--version", choices=["current", "baseline"], default="current")
    run.add_argument("--cases", help="Comma-separated case names (default: all)")
    run.add_argument("--provider", default=settings.model_provider)
    run.add_argument("--model", help="Default: the provider's model in the settings")
    run.add_argument("--preset", choices=list(PRESETS), help="Current version only")
    run.add_argument("--repeats", type=int, default=1)
    run.add_argument("--jobs", type=int, default=4)
    run.add_argument("--timeout-min", type=int, default=60, help="Per run")
    grade = commands.add_parser("grade", help="Recompute the grades of results files")
    grade.add_argument("results", nargs="+", type=Path)
    judge = commands.add_parser("judge", help="Judge reports with the LLM judge")
    judge.add_argument("results", nargs="+", type=Path)
    judge.add_argument("--jobs", type=int, default=4)
    judge.add_argument("--force", action="store_true", help="Re-judge judged lines")
    args = parser.parse_args()

    if args.command == "grade":
        for results in args.results:
            regrade(results)
            print(f"Graded: {results}")
        return 0

    if args.command == "judge":
        for results in args.results:
            lines = [json.loads(line) for line in results.read_text().splitlines()]
            n = judge_results(lines, ROOT, jobs=args.jobs, force=args.force)
            results.write_text("".join(json.dumps(line) + "\n" for line in lines))
            errors = sum(1 for line in lines if (line.get("judge") or {}).get("error"))
            print(f"Judged {n} reports in {results} ({errors} errors)")
        return 0

    settings.model_provider = args.provider
    cases = [load_case(n) for n in args.cases.split(",")] if args.cases else all_cases()
    config = Config(
        version=args.version,
        provider=args.provider,
        model=args.model or settings.model,
        preset=args.preset,
        repeats=args.repeats,
        jobs=args.jobs,
        timeout_s=args.timeout_min * 60,
    )
    print(f"Results: {run_suite(config, cases)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
