# Judge calibration (P2.6)

Does the LLM judge (`evals/judge.py`, Claude Sonnet 5.5) agree with hand labels? Each directory here is one report: `report.md` (copied, so the set reproduces from git), `labels.yaml` (a hand label for every item of its case, with notes where the call isn't obvious), and `judge.json` (the judge's stored verdict). `uv run python -m evals agree` judges what the current rubric hasn't judged yet and prints the agreement and every disagreement.

## The set

12 reports, 110 items, labelled from the whole report before the judge saw it.

| Report | Source |
|---|---|
| `titanic-baseline-qwen`, `titanic-p1.2-qwen`, `titanic-p1.3-qwen`, `titanic-p1.4-qwen` | The claim-checked reference runs on qwen3.5 (`docs/baseline/run/`, `docs/progress/p1.x/`) |
| `titanic-p1.4-haiku`, `titanic-p1.5-haiku` | The same on Claude Haiku 5.5 |
| `leakage-baseline`, `regression_outliers-baseline`, `string_target-baseline`, `datetime_trend-baseline` | First eval suite, baseline (`20261102-203054`) |
| `leakage-current`, `pure_noise-current` | First eval suite, current version |

Labels: `must_find` 34 yes / 13 partly / 18 no; `must_not_claim` 35 no / 1 partly; caveats 8 yes / 1 partly.

## Results

| Rubric | Run | must_find (65) | must_not_claim (36) | caveats (9) | All (110) | Within ½ |
|---|---|---|---|---|---|---|
| `effcd858a723` (P2.5) | 1 | 94% | 100% | 89% | 95% | 100% |
| `983aca5d02a5` | 1 | 88% | 100% | 100% | 93% | 100% |
| `983aca5d02a5` | 2 | 94% | 100% | 100% | 96% | 100% |

**The judge disagrees with itself on 5% of items.** Two runs of the same rubric on the same reports differ on 5 of 110 verdicts, all `must_find` items at the `partly` boundary. So an agreement figure moves by about ±3 points from noise alone, and the two rubrics can't be told apart on `must_find`. What holds in every run: **no verdict is more than ½ from the label**, and `must_not_claim` agrees 100%.

**The rubric change (`983aca5d02a5`)** wrote down the calls the first run disagreed on:
- An established association whose direction the report couldn't give is `partly`. "Could not determine it" (`no`) means it couldn't tell whether the effect exists. The first run had marked one such item `no` and an identical one in the same report `partly`.
- The report must make the statement itself: numbers from which a reader could work it out, or the variable discussed only in another connection, are `no`.
- A number clearly different from the item's is `partly`.
- A caveat counts when the report warns about it, even if it couldn't measure it. This fixed the one caveat disagreement in both runs.

**Two disagreements persist:** in both runs the judge doesn't follow two of these rules.
- `titanic-p1.2-qwen`, the baseline comparison: `partly` from the judge, though its own reason says the report "never compares accuracy with the 62% majority-class baseline".
- `titanic-p1.4-qwen`, a baseline given as 58.7% (true 61.6%): `yes` from the judge, despite the number rule.

Both are one item each. Pushing further on wording would fit the rubric to these 12 reports.

## Caveats

- **The labels were drafted by Claude (Opus 5.5), and the judge is also Claude (Sonnet 5.5).** Labels from the same model family may agree with the judge more than an independent labeller's would. The owner spot-checked the 13 borderline calls (2026-11-05), including the disagreements above, and changed none.
- One label was changed after the first run: `leakage-baseline`, tenure, from `no` to `partly`. The judge had agreed with `no`; the change makes it consistent with the same call in `string_target-baseline` (fee, support calls), once the rule was written down.
- The rubric was adjusted on these reports. Its real test is fresh reports: label a few P2.8 reports before looking at their verdicts.
- `must_not_claim` is almost all `no` (35 of 36), so its 100% says little about how the judge handles a violated claim. The only such label (`leakage-baseline`, refund as a valid predictor, `partly`) agrees.
