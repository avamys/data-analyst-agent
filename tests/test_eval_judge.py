from pathlib import Path
from types import SimpleNamespace

import pytest

from evals import judge as judge_module
from evals.cases import load_case
from evals.judge import (
    PROMPT_VERSION,
    JudgeError,
    Verdict,
    Verdicts,
    judge,
    judge_results,
)

CASE = load_case("leakage")  # 5 findings, 2 forbidden claims, 1 caveat
REPORT = "# Report\n\n**refund_issued** almost perfectly separates churn: a leak.\n"


def verdicts(
    find=("yes",) * 5,
    claims=("no", "no"),
    caveats=("yes",),
    quote="refund_issued almost perfectly separates churn",
):
    def v(x):
        return Verdict(quote=quote if x != "no" else "", reason="r", verdict=x)

    return Verdicts(
        must_find=[v(x) for x in find],
        must_not_claim=[v(x) for x in claims],
        caveats=[v(x) for x in caveats],
    )


class FakeClient:
    """Stands in for anthropic.Anthropic: returns the given verdicts"""

    def __init__(self, parsed, stop_reason="end_turn"):
        self.prompts = []
        self.beta = SimpleNamespace(messages=SimpleNamespace(create=self._create))
        self.parsed, self.stop_reason = parsed, stop_reason

    def _create(self, **kwargs):
        self.prompts.append(kwargs["messages"][0]["content"])
        thinking = SimpleNamespace(type="thinking", thinking="")
        text = SimpleNamespace(type="text", text=self.parsed.model_dump_json())
        return SimpleNamespace(
            content=[thinking, text],
            stop_reason=self.stop_reason,
            stop_details=None,
            model=kwargs["model"],
            usage=SimpleNamespace(input_tokens=100, output_tokens=50),
        )


def test_the_prompt_numbers_the_items_and_holds_the_report():
    client = FakeClient(verdicts())
    judge(CASE, REPORT, client)
    [prompt] = client.prompts
    assert REPORT in prompt
    assert (
        f"1. {CASE.must_find[0]}" in prompt and f"2. {CASE.must_not_claim[1]}" in prompt
    )
    assert "1. leakage (e.g. mentioning: leak)" in prompt


def test_scores_count_partly_as_half():
    find = ("yes", "partly", "no", "yes", "yes")
    result = judge(CASE, REPORT, FakeClient(verdicts(find, claims=("partly", "no"))))
    assert result["scores"]["finding_recall"] == pytest.approx(3.5 / 5)
    assert result["scores"]["false_claims"] == 0.5
    assert result["scores"]["caveat_coverage"] == 1.0
    assert result["prompt"] == PROMPT_VERSION


def test_quotes_are_checked_against_the_report():
    # Markdown emphasis and spacing don't count; made-up quotes do
    ok = judge(CASE, REPORT, FakeClient(verdicts()))
    assert all(v["quote_found"] for v in ok["must_find"])
    elided = "refund_issued almost ... separates churn"
    assert judge(CASE, REPORT, FakeClient(verdicts(quote=elided)))["must_find"][0][
        "quote_found"
    ]
    made_up = judge(CASE, REPORT, FakeClient(verdicts(quote="refunds cause churn")))
    assert made_up["scores"]["quotes_not_found"] == 6  # every yes or partly


def test_refusals_and_misaligned_verdicts_are_errors():
    with pytest.raises(JudgeError, match="declined"):
        judge(CASE, REPORT, FakeClient(verdicts(), stop_reason="refusal"))
    with pytest.raises(JudgeError, match="4 verdicts for 5 items"):
        judge(CASE, REPORT, FakeClient(verdicts(find=("yes",) * 4)))


def test_only_lines_not_judged_with_this_prompt_are_judged(monkeypatch, tmp_path):
    (tmp_path / "run").mkdir()
    (tmp_path / "run" / "report.md").write_text(REPORT)
    calls = []
    monkeypatch.setattr(
        judge_module,
        "judge",
        lambda case, report: calls.append(case.name) or {"prompt": PROMPT_VERSION},
    )
    line = {"case": "leakage", "run_dir": "run", "has_report": True}
    lines = [
        dict(line),
        {**line, "judge": {"prompt": PROMPT_VERSION}},  # already judged
        {**line, "judge": {"prompt": "older"}},  # an older rubric
        {**line, "has_report": False},  # nothing to judge
    ]
    assert judge_results(lines, Path(tmp_path), jobs=2) == 2
    assert judge_results(lines, Path(tmp_path), jobs=2, force=True) == 3
