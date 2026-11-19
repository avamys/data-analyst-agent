"""Eval harness CLI

uv run python -m evals run --version current --provider anthropic --repeats 3
uv run python -m evals run --version baseline --provider anthropic --cases titanic
uv run python -m evals grade evals/results/<suite id>.jsonl
uv run python -m evals judge evals/results/<suite id>.jsonl
uv run python -m evals report evals/results/<suite id>.jsonl [...]
uv run python -m evals compare evals/results/<A>.jsonl evals/results/<B>.jsonl
uv run python -m evals snapshot evals/results/<suite id>.jsonl
uv run python -m evals agree
"""

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(".env")

from agent.config import PRESETS, settings  # noqa: E402
from evals.calibration import agreement, calibrate  # noqa: E402
from evals.cases import SUITES, all_cases, load_case  # noqa: E402
from evals.judge import PROMPT_VERSION, judge_results  # noqa: E402
from evals.report import compare, report  # noqa: E402
from evals.runner import ROOT, Config, regrade, run_suite, snapshot  # noqa: E402


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
    run.add_argument(
        "--suite",
        choices=SUITES,
        default="dev",
        help="Which cases 'all' means (held-out: evals/heldout/, evals/heldout2/)",
    )
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
    table = commands.add_parser("report", help="Markdown table per results file")
    table.add_argument("results", nargs="+", type=Path)
    diff = commands.add_parser("compare", help="Deltas from suite A to suite B")
    diff.add_argument("a", type=Path)
    diff.add_argument("b", type=Path)
    snap = commands.add_parser(
        "snapshot", help="Keep what the graders read of a suite's runs, for CI"
    )
    snap.add_argument("results", nargs="+", type=Path)
    agree = commands.add_parser(
        "agree", help="Judge agreement with the hand labels (docs/eval/calibration)"
    )
    agree.add_argument("--jobs", type=int, default=4)
    agree.add_argument("--force", action="store_true", help="Re-judge every report")
    args = parser.parse_args()

    if args.command == "report":
        print(report(args.results))
        return 0

    if args.command == "compare":
        print(compare(args.a, args.b))
        return 0

    if args.command == "snapshot":
        for results in args.results:
            snapshot(results)
            print(f"Snapshot of {results} in evals/snapshots/")
        return 0

    if args.command == "agree":
        return _agree(calibrate(jobs=args.jobs, force=args.force))

    if args.command == "grade":
        for results in args.results:
            regrade(results)
            print(f"Graded: {results}")
        return 0

    if args.command == "judge":
        for results in args.results:
            lines = [json.loads(line) for line in results.read_text().splitlines()]
            # Traced to the suite's project, next to the runs it judges
            n = judge_results(
                lines,
                ROOT,
                jobs=args.jobs,
                force=args.force,
                project=f"evals-{results.stem}",
            )
            results.write_text("".join(json.dumps(line) + "\n" for line in lines))
            errors = sum(1 for line in lines if (line.get("judge") or {}).get("error"))
            print(f"Judged {n} reports in {results} ({errors} errors)")
        return 0

    settings.model_provider = args.provider
    cases = (
        [load_case(n) for n in args.cases.split(",")]
        if args.cases
        else all_cases(args.suite)
    )
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


def _agree(rows: list[dict]) -> int:
    print("| Items | n | Exact | Within ½ |\n|---|---|---|---|")
    for kind, a in agreement(rows).items():
        print(f"| {kind} | {a['items']} | {a['exact']:.0%} | {a['within_half']:.0%} |")
    print(f"\nRubric {PROMPT_VERSION}, {len({r['report'] for r in rows})} reports")
    for r in rows:
        if not r["exact"]:
            print(f"\n{r['report']} · {r['kind']}: {r['item']}")
            note = f" ({r['note']})" if r["note"] else ""
            print(f"  label {r['label']}{note}")
            print(f"  judge {r['verdict']}: {r['reason']}")
            if r["quote"]:
                print(f"  quote: {r['quote']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
