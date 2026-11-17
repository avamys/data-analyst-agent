"""Results tables: one suite per results file, and the comparison of two suites

Per case: the mean over repeats, with min–max when they differ. The
overall row is the mean over cases within each repeat, then the mean and
min–max of those over repeats. A run without a report found nothing: its
findings and caveats count as 0, and its false claims aren't counted.

A local run whose generation speed is below half the suite's median (host asleep,
hot, GPU shared) is flagged and left out of the Minutes column, so it doesn't
skew it. Runs with calls cut off at the output cap or empty are flagged too.
"""

import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, median

from evals.cases import load_case
from evals.judge import PROMPT_VERSION

# name: (column header, formatter, higher is better); quality metrics first
METRICS = {
    "run_ok": ("Runs ok", lambda v: f"{v:.0%}", True),
    "finding_recall": ("Findings", lambda v: f"{v:.0%}", True),
    "false_claims": ("False claims", lambda v: f"{v:.1f}", False),
    "fact_recall": ("Facts", lambda v: f"{v:.0%}", True),
    "caveat_coverage": ("Caveats", lambda v: f"{v:.0%}", True),
    "unverified_numbers": ("Unverified numbers", lambda v: f"{v:.1f}", False),
    "cost_usd": ("Cost", lambda v: f"${v:.3f}", False),
    "minutes": ("Minutes", lambda v: f"{v:.1f}", False),
}
QUALITY = [m for m in METRICS if m not in ("cost_usd", "minutes")]
SLOW = 0.5  # Of the suite's median generation speed


def generation_speed(line: dict) -> float | None:
    """Tokens a second generated over the run (Ollama runs only)"""
    ollama = line.get("ollama") or {}
    if not ollama.get("generation_seconds"):
        return None
    return ollama["generation_tokens"] / ollama["generation_seconds"]


def load(path: Path) -> list[dict]:
    """The result lines, each marked "slow" when its generation speed is below
    SLOW × the suite's median"""
    lines = [json.loads(line) for line in path.read_text().splitlines()]
    speeds = [s for line in lines if (s := generation_speed(line)) is not None]
    for line in lines:
        speed = generation_speed(line)
        line["slow"] = speed is not None and speed < SLOW * median(speeds)
    return lines


def values(line: dict) -> dict[str, float | None]:
    """The metrics of one run; None where they don't apply or weren't judged"""
    grades = line.get("grades") or {}
    scores = (line.get("judge") or {}).get("scores")
    if scores is None and not line.get("has_report"):
        caveats = 0.0 if load_case(line["case"]).caveats else None
        scores = {"finding_recall": 0.0, "caveat_coverage": caveats}
    scores = scores or {}
    return {
        "run_ok": float(bool(grades.get("run_ok"))),
        "finding_recall": scores.get("finding_recall"),
        "false_claims": scores.get("false_claims"),
        "fact_recall": grades.get("fact_recall"),
        "caveat_coverage": scores.get("caveat_coverage"),
        "unverified_numbers": grades.get("unverified_numbers"),
        "cost_usd": grades.get("cost_usd"),
        "minutes": (
            line["seconds"] / 60
            if line.get("seconds") is not None and not line.get("slow")
            else None
        ),
    }


def _mean(xs: list) -> float | None:
    xs = [x for x in xs if x is not None]
    return mean(xs) if xs else None


def per_case(lines: list[dict]) -> dict[str, dict[str, list]]:
    """case -> metric -> the value of each repeat"""
    cases: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    for line in sorted(lines, key=lambda line: line["repeat"]):
        for metric, value in values(line).items():
            cases[line["case"]][metric].append(value)
    return cases


def overall(lines: list[dict]) -> dict[str, list]:
    """metric -> the mean over cases of each repeat"""
    repeats = defaultdict(list)
    for line in lines:
        repeats[line["repeat"]].append(values(line))
    return {
        metric: [
            _mean([v[metric] for v in runs]) for _, runs in sorted(repeats.items())
        ]
        for metric in METRICS
    }


def _cell(metric: str, xs: list) -> str:
    xs = [x for x in xs if x is not None]
    if not xs:
        return "—"
    fmt = METRICS[metric][1]
    if min(xs) == max(xs):
        return fmt(xs[0])
    return f"{fmt(mean(xs))} ({fmt(min(xs))}–{fmt(max(xs))})"


def _signed(metric: str, delta: float) -> str:
    """A difference in the metric's own format: +46%, −$0.012"""
    return ("+" if delta >= 0 else "−") + METRICS[metric][1](abs(delta))


def _traces(lines: list[dict]) -> str:
    links = [
        f"[r{line['repeat']}]({line['trace_url']})"
        for line in sorted(lines, key=lambda line: line["repeat"])
        if line.get("trace_url")
    ]
    return " ".join(links) or "—"


def _title(lines: list[dict], name: str) -> str:
    first = lines[0]
    parts = [first["version"], first["model"]]
    if first.get("preset"):
        parts.append(f"preset {first['preset']}")
    parts.append(f"code {first['code']}")
    repeats = max(line["repeat"] for line in lines)
    cases = len({line["case"] for line in lines})
    plural = "s" if repeats > 1 else ""
    return (
        f"### {' · '.join(parts)}\n\n`{name}`: {cases} cases × {repeats} repeat{plural}"
    )


def _judged_with(lines: list[dict]) -> str:
    judges = {
        (j.get("model"), j.get("prompt"))
        for line in lines
        if (j := line.get("judge")) and not j.get("error")
    }
    errors = sum(1 for line in lines if (line.get("judge") or {}).get("error"))
    if not judges:
        return "Not judged: run `python -m evals judge` for findings and claims."
    text = "Judge: " + ", ".join(f"{m} (rubric `{p}`)" for m, p in sorted(judges))
    if any(p != PROMPT_VERSION for _, p in judges):
        text += f". The current rubric is `{PROMPT_VERSION}`: re-judge to update."
    if errors:
        text += f" {errors} runs failed to be judged."
    return text


def flagged(lines: list[dict]) -> str:
    """Runs whose calls hit the output cap or came back empty, and slow runs"""
    notes = []
    for key, text in (
        ("calls_cut_off", "calls cut off at the output cap"),
        ("calls_empty", "empty replies"),
    ):
        runs = [
            f"{line['case']} r{line['repeat']} ({line[key]})"
            for line in lines
            if line.get(key)
        ]
        if runs:
            notes.append(f"Runs with {text}: {', '.join(runs)}.")
    slow = [
        f"{line['case']} r{line['repeat']} ({generation_speed(line):.1f} tok/s)"
        for line in lines
        if line.get("slow")
    ]
    if slow:
        notes.append(
            f"Generating below {SLOW:.0%} of the suite's median speed, left out "
            f"of Minutes: {', '.join(slow)}."
        )
    return " ".join(notes)


def suite_table(lines: list[dict], name: str) -> str:
    """Markdown table of one suite: a row per case and an overall row"""
    header = ["Case", *[METRICS[m][0] for m in METRICS], "Traces"]
    rows = [
        "| " + " | ".join(header) + " |",
        "|" + "---|" * len(header),
    ]
    by_case = defaultdict(list)
    for line in lines:
        by_case[line["case"]].append(line)
    for case, metrics in sorted(per_case(lines).items()):
        cells = [_cell(m, metrics[m]) for m in METRICS]
        rows.append(
            f"| {case} | " + " | ".join(cells) + f" | {_traces(by_case[case])} |"
        )
    totals = overall(lines)
    cells = [f"**{_cell(m, totals[m])}**" for m in METRICS]
    rows.append("| **Overall** | " + " | ".join(cells) + " | |")
    cost = sum(v for line in lines if (v := values(line)["cost_usd"]) is not None)
    parts = [
        _title(lines, name),
        "\n".join(rows),
        f"Total cost ${cost:.2f}. {_judged_with(lines)}",
    ]
    if notes := flagged(lines):
        parts.append(notes)
    return "\n\n".join(parts)


def report(paths: list[Path]) -> str:
    return "\n\n".join(suite_table(load(p), p.stem) for p in paths)


def compare(a: Path, b: Path) -> str:
    """Overall deltas from suite A to suite B, and the cases B does worse on"""
    lines_a, lines_b = load(a), load(b)
    all_a, all_b = overall(lines_a), overall(lines_b)
    rows = ["| Metric | A | B | Δ (B − A) |", "|---|---|---|---|"]
    for metric, (header, _, _) in METRICS.items():
        ma, mb = _mean(all_a[metric]), _mean(all_b[metric])
        delta = _signed(metric, mb - ma) if None not in (ma, mb) else "—"
        rows.append(
            f"| {header} | {_cell(metric, all_a[metric])} "
            f"| {_cell(metric, all_b[metric])} | {delta} |"
        )
    cases_a, cases_b = per_case(lines_a), per_case(lines_b)
    worse = []
    for case in sorted(cases_a.keys() & cases_b.keys()):
        for metric in QUALITY:
            header, fmt, higher = METRICS[metric]
            ma, mb = _mean(cases_a[case][metric]), _mean(cases_b[case][metric])
            if ma is None or mb is None or ma == mb or (mb > ma) == higher:
                continue
            worse.append(f"- {case}: {header} {fmt(ma)} → {fmt(mb)}")
    only = sorted(cases_a.keys() ^ cases_b.keys())
    parts = [
        f"A: `{a.stem}`  \nB: `{b.stem}`",
        "\n".join(rows),
        "**Cases B does worse on**\n\n" + ("\n".join(worse) or "None."),
    ]
    if only:
        parts.append(f"In one suite only (not compared): {', '.join(only)}")
    return "\n\n".join(parts)
