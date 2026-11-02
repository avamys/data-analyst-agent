"""Eval harness CLI

uv run python -m evals run --version current --provider anthropic --repeats 3
uv run python -m evals run --version baseline --provider anthropic --cases titanic
"""

import argparse
import sys

from dotenv import load_dotenv

load_dotenv(".env")

from agent.config import PRESETS, settings  # noqa: E402
from evals.cases import all_cases, load_case  # noqa: E402
from evals.runner import Config, run_suite  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(prog="evals", description=__doc__)
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
    args = parser.parse_args()

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
