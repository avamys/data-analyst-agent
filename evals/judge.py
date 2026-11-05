"""LLM judge: does a report make the case's findings and avoid its false claims?

One call per report to the judge model (settings.judge_model, Claude Sonnet 5.5),
through the Anthropic SDK: independent of the provider of the agent under test.
Each item gets yes / partly / no with the quote it rests on; quotes are checked
against the report. Verdicts are stored with the results, tagged with a hash of
the prompt and schema, so a changed rubric is re-judged and an unchanged one
is not. With LangSmith tracing on, each call is traced with its case and rubric.
"""

import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from typing import Literal

import anthropic
from anthropic import transform_schema
from langsmith import tracing_context
from langsmith.wrappers import wrap_anthropic
from pydantic import BaseModel, Field

from agent.config import settings
from evals.cases import Case

PROMPT = """You are grading a data analysis report against known answers: the true findings in its dataset, and claims that would be false.

THE REPORT:
<report>
{report}
</report>

Grade each item by what the report says, nothing else. Wording may differ from the item; what matters is whether the report states the same thing about the same variables.

FINDINGS THE REPORT SHOULD MAKE:
{must_find}
- yes: the report states it, with its direction (which group is higher, positive or negative) where the item has one, and with numbers close to the item's where the item gives them
- partly: the report relates the item's variables to each other but leaves out the direction, size or comparison (for example "significant, but the direction was not reported"), states only part of the item, or gives a number clearly different from the item's
- no: the report doesn't state it, states the opposite, or says it could not determine whether the effect exists at all. The report must make the statement itself: giving numbers from which a reader could work it out, or discussing the variable only in another connection, is no

CLAIMS THE REPORT MUST NOT MAKE:
{must_not_claim}
- yes: the report makes the claim as a conclusion
- partly: the report makes it hedged, or in passing, without its caveat
- no: the report doesn't make it, or mentions it only to reject it

CAVEATS THE REPORT SHOULD STATE:
{caveats}
- yes: the report warns about it, even if it could not measure it
- partly: it is mentioned without being treated as a limitation
- no: not mentioned

For every item give the quote first: the exact words from the report your verdict rests on, copied character for character (one or two sentences; leave it empty if the report says nothing about the item). Then one sentence of reason, then the verdict. Give the verdicts in the order of the items."""


class Verdict(BaseModel):
    quote: str = Field(description="Exact words from the report; empty if none")
    reason: str = Field(description="One sentence")
    verdict: Literal["yes", "partly", "no"]


class Verdicts(BaseModel):
    must_find: list[Verdict]
    must_not_claim: list[Verdict]
    caveats: list[Verdict]


PROMPT_VERSION = hashlib.sha256(
    (PROMPT + json.dumps(Verdicts.model_json_schema(), sort_keys=True)).encode()
).hexdigest()[:12]

SCORE = {"yes": 1.0, "partly": 0.5, "no": 0.0}
KINDS = ("must_find", "must_not_claim", "caveats")


class JudgeError(RuntimeError):
    """The judge refused, or its verdicts don't match the items"""


def _items(case: Case) -> dict[str, list[str]]:
    return {
        "must_find": case.must_find,
        "must_not_claim": case.must_not_claim,
        "caveats": [
            f"{name.replace('_', ' ')} (e.g. mentioning: {', '.join(keywords)})"
            for name, keywords in case.caveats.items()
        ],
    }


def _numbered(items: list[str]) -> str:
    return "\n".join(f"{i}. {item}" for i, item in enumerate(items, 1)) or "(none)"


def _normalized(text: str) -> str:
    """For finding quotes: markdown emphasis and spacing don't count"""
    return re.sub(r"\s+", " ", re.sub(r"[*_`>#|]", "", text)).strip().lower()


def _quoted(quote: str, report: str) -> bool:
    """Every part of the quote is in the (normalized) report; parts may be
    joined by an ellipsis where the judge left something out"""
    parts = [_normalized(p) for p in re.split(r"\.\.\.|…", quote)]
    return all(part in report for part in parts if part)


def scores(graded: dict) -> dict:
    """The scores of a report from its verdicts (also from stored ones)"""

    def mean(kind):
        values = [SCORE[v["verdict"]] for v in graded[kind]]
        return sum(values) / len(values) if values else None

    return {
        "finding_recall": mean("must_find"),
        "false_claims": sum(SCORE[v["verdict"]] for v in graded["must_not_claim"]),
        "caveat_coverage": mean("caveats"),
        "quotes_not_found": sum(
            not v["quote_found"] for kind in KINDS for v in graded[kind]
        ),
    }


def judge(
    case: Case,
    report: str,
    client: anthropic.Anthropic | None = None,
    project: str | None = None,
    metadata: dict | None = None,
) -> dict:
    """The judge's verdict on every item of the case, with scores. The trace goes
    to the given LangSmith project, with the case, rubric and metadata"""
    items = _items(case)
    prompt = PROMPT.format(report=report, **{k: _numbered(v) for k, v in items.items()})
    client = client or wrap_anthropic(
        anthropic.Anthropic(api_key=settings.anthropic_api_key.get_secret_value())
    )
    with tracing_context(
        project_name=project,
        tags=["judge", case.name],
        metadata={"case": case.name, "rubric": PROMPT_VERSION, **(metadata or {})},
    ):
        response = client.beta.messages.create(
            model=settings.judge_model,
            max_tokens=16000,  # thinking counts against it
            messages=[{"role": "user", "content": prompt}],
            output_config={
                "format": {"type": "json_schema", "schema": transform_schema(Verdicts)}
            },
            # Recommended for Sonnet 5.5: a declined request is retried on another
            # model. Which model served is recorded, so a fallback shows.
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        )
    if response.stop_reason == "refusal":
        raise JudgeError(f"The judge declined: {response.stop_details}")
    # The schema guarantees the text block is valid JSON; thinking blocks come first
    text = next(block.text for block in response.content if block.type == "text")
    verdicts = Verdicts.model_validate_json(text)
    found = _normalized(report)
    graded = {}
    for kind, texts in items.items():
        given = getattr(verdicts, kind)
        if len(given) != len(texts):
            raise JudgeError(f"{kind}: {len(given)} verdicts for {len(texts)} items")
        graded[kind] = [
            {
                "item": text,
                **v.model_dump(),
                "quote_found": _quoted(v.quote, found),
            }
            for text, v in zip(texts, given, strict=True)
        ]

    return {
        "model": settings.judge_model,
        "served_by": response.model,
        "prompt": PROMPT_VERSION,
        **graded,
        "scores": scores(graded),
        "usage": {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        },
    }


def judge_results(
    lines: list[dict],
    root,
    jobs: int = 4,
    force: bool = False,
    project: str | None = None,
) -> int:
    """Judge result lines in place (those not judged with this prompt yet)"""
    from evals.cases import load_case

    todo = [
        line
        for line in lines
        if line.get("has_report")
        and (force or (line.get("judge") or {}).get("prompt") != PROMPT_VERSION)
    ]

    def one(line):
        report = (root / line["run_dir"] / "report.md").read_text()
        try:
            line["judge"] = judge(
                load_case(line["case"]),
                report,
                project=project,
                metadata={k: line[k] for k in ("repeat", "version", "run_dir")},
            )
        except (JudgeError, anthropic.APIError) as e:
            line["judge"] = {"prompt": None, "error": repr(e)}

    with ThreadPoolExecutor(max_workers=jobs) as pool:
        list(pool.map(one, todo))
    return len(todo)
