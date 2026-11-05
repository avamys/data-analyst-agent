"""Judge calibration: does the LLM judge agree with hand labels?

Each labelled report is a directory docs/eval/calibration/<name>/ with
    report.md     the report, copied so the set reproduces from git
    labels.yaml   its case, where the report came from, and a hand label for
                  every item of the case (yes / partly / no, as the judge)
    judge.json    the judge's verdict, stored; judged again when the rubric changes
"""

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, field_validator

from evals.cases import Case, load_case
from evals.judge import PROMPT_VERSION, SCORE, judge

CALIBRATION_DIR = Path(__file__).parent.parent / "docs" / "eval" / "calibration"
KINDS = ("must_find", "must_not_claim", "caveats")


class Label(BaseModel):
    item: str  # The case's item (a caveat by its name), to catch edited cases
    label: Literal["yes", "partly", "no"]
    note: str = ""

    @field_validator("label", mode="before")
    @classmethod
    def _yaml_booleans(cls, value):
        # YAML reads unquoted yes / no as booleans
        return {True: "yes", False: "no"}.get(value, value)


class Labels(BaseModel):
    case: str
    source: str
    must_find: list[Label]
    must_not_claim: list[Label] = []
    caveats: list[Label] = []


def load(path: Path) -> tuple[Labels, Case]:
    """The labels of a calibration directory, checked against its case's items"""
    labels = Labels(**yaml.safe_load((path / "labels.yaml").read_text()))
    case = load_case(labels.case)
    expected = {
        "must_find": case.must_find,
        "must_not_claim": case.must_not_claim,
        "caveats": list(case.caveats),
    }
    for kind in KINDS:
        given = [label.item for label in getattr(labels, kind)]
        if given != expected[kind]:
            raise ValueError(f"{path.name}: {kind} labels don't match the case's items")
    return labels, case


def verdict(path: Path, case: Case, force: bool = False) -> dict:
    """The stored judge verdict, or a new one if the rubric changed"""
    stored = path / "judge.json"
    if not force and stored.exists():
        result = json.loads(stored.read_text())
        if result.get("prompt") == PROMPT_VERSION:
            return result
    result = judge(
        case,
        (path / "report.md").read_text(),
        project="evals-calibration",
        metadata={"calibration": path.name},
    )
    stored.write_text(json.dumps(result, indent=2) + "\n")
    return result


def compare(labels: Labels, result: dict) -> list[dict]:
    """One row per item: the hand label, the judge's verdict and its grounds"""
    return [
        {
            "kind": kind,
            "item": label.item,
            "label": label.label,
            "note": label.note,
            **{k: v[k] for k in ("verdict", "quote", "reason")},
            "exact": label.label == v["verdict"],
            "within_half": abs(SCORE[label.label] - SCORE[v["verdict"]]) <= 0.5,
        }
        for kind in KINDS
        for label, v in zip(getattr(labels, kind), result[kind], strict=True)
    ]


def agreement(rows: list[dict]) -> dict[str, dict]:
    """Exact and within-½ agreement per kind of item, and over all items"""
    groups = {kind: [r for r in rows if r["kind"] == kind] for kind in KINDS}
    groups["all"] = rows
    return {
        kind: {
            "items": len(group),
            "exact": sum(r["exact"] for r in group) / len(group),
            "within_half": sum(r["within_half"] for r in group) / len(group),
        }
        for kind, group in groups.items()
        if group
    }


def calibrate(
    root: Path = CALIBRATION_DIR, jobs: int = 4, force: bool = False
) -> list[dict]:
    """Rows for every labelled report under root, judged where needed"""
    paths = sorted(p for p in root.iterdir() if (p / "labels.yaml").exists())
    loaded = [load(p) for p in paths]  # All labels are valid before any judge call

    def one(args):
        path, (labels, case) = args
        rows = compare(labels, verdict(path, case, force))
        return [{"report": path.name, **row} for row in rows]

    with ThreadPoolExecutor(max_workers=jobs) as pool:
        return [
            row
            for rows in pool.map(one, zip(paths, loaded, strict=True))
            for row in rows
        ]
