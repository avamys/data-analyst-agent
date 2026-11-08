# Judge calibration (P2.6)

Does the LLM judge (`evals/judge.py`, Claude Sonnet 5.5) agree with hand labels? Each directory here is one report: `report.md` (copied, so the set reproduces from git), `labels.yaml` (a hand label for every item of its case, with notes where the call isn't obvious), and `judge.json` (the judge's stored verdict). `uv run python -m evals agree` judges what the current rubric hasn't judged yet and prints the agreement and every disagreement.

## The set

15 reports, 130 items, labelled from the whole report before the judge saw it. Every label answers one question: does the report say this item? So for `must_not_claim`, `no` is the good outcome.

| Report | Source |
|---|---|
| `titanic-baseline-qwen`, `titanic-p1.2-qwen`, `titanic-p1.3-qwen`, `titanic-p1.4-qwen` | The claim-checked reference runs on qwen3.5 (`docs/baseline/run/`, `docs/progress/p1.x/`) |
| `titanic-p1.4-haiku`, `titanic-p1.5-haiku` | The same on Claude Haiku 5.5 |
| `leakage-baseline`, `regression_outliers-baseline`, `string_target-baseline`, `datetime_trend-baseline` | First eval suite, baseline (`20261102-203054`) |
| `leakage-current`, `pure_noise-current` | First eval suite, current version |
| `planted_effects-baseline-p2.8`, `datetime_trend-current-p2.8`, `regression_outliers-current-p2.8` | P2.8 suites (`20261105-*`), labelled by the owner |

Labels: `must_find` 42 yes / 13 partly / 22 no; `must_not_claim` 40 no / 2 partly; caveats 9 yes / 2 partly.

## Results

| Rubric | Run | must_find (65) | must_not_claim (36) | caveats (9) | All (110) | Within ½ |
|---|---|---|---|---|---|---|
| `effcd858a723` (P2.5) | 1 | 94% | 100% | 89% | 95% | 100% |
| `983aca5d02a5` | 1 | 88% | 100% | 100% | 93% | 100% |
| `983aca5d02a5` | 2 | 94% | 100% | 100% | 96% | 100% |
| `983aca5d02a5` | 2, + 3 fresh reports (77 / 42 / 11 / 130) | 91% | 98% | 91% | 93% | 100% |

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

## Fresh reports (P2.8)

The rubric was adjusted on the first 12 reports, so its test is reports it hasn't seen. The owner labelled three P2.8 reports without seeing the judge's verdicts; Claude picked them: the two lowest-scoring and one 100% current report, to check that the judge isn't too generous to the current agent.

| Report | Exact | Within ½ |
|---|---|---|
| `datetime_trend-current-p2.8` | 5 / 5 | 5 / 5 |
| `regression_outliers-current-p2.8` | 7 / 7 | 7 / 7 |
| `planted_effects-baseline-p2.8` | 3 / 8 | 8 / 8 |

**All 5 disagreements are in the baseline report, and in each the judge gives the report more credit than the owner.** Three are hedged findings: the report calls feat_b "Supported", feat_d "Supported, but unverified" and feat_c "Probably not supported", and the owner labels them `no` ("not demonstrated, left as a question"), the judge `partly`. The rubric says how to grade a hedged claim (`partly`) but not a hedged finding; the judge treats both alike. This is a difference between labellers, left as it is: it can only make the baseline look better, not the current agent. The other two: the missing-values caveat (`partly` by the owner, who noted that the mechanism stays unresolved; `yes` by the judge, as the report lists it among its limitations) and "feat_b is the strongest predictor" (`partly` by the owner, `no` by the judge: the report names feat_a).

**The label format was misread once.** In the first pass, the owner labelled 4 `must_not_claim` items `yes` in the sense "the report passes", against the reports' own text ("Temperature has no detectable relationship with sales"). Each contradicted the owner's own `must_find` label on the same report ("sales rise over time": `yes`, "sales decline over time": `yes`). They were corrected to `no` after the owner had seen the judge's verdicts, as were two more: the age association (`no` → `yes`; the report's summary states it) and the 15% missing item (left blank, then `yes`). So 6 of the 20 items are not blind; on the 14 that are, exact agreement is 9 of 14 and within ½ 14 of 14. The P2.6 labels, drafted by Claude, never tested the instructions; the sentence under "The set" now says what a label means.

## Caveats

- **The labels were drafted by Claude (Opus 5.5), and the judge is also Claude (Sonnet 5.5).** Labels from the same model family may agree with the judge more than an independent labeller's would. The owner spot-checked the 13 borderline calls (2026-11-05), including the disagreements above, and changed none.
- One label was changed after the first run: `leakage-baseline`, tenure, from `no` to `partly`. The judge had agreed with `no`; the change makes it consistent with the same call in `string_target-baseline` (fee, support calls), once the rule was written down.
- The rubric was adjusted on the first 12 reports; the three fresh ones are its test so far (above).
- `must_not_claim` is almost all `no` (35 of 36), so its 100% says little about how the judge handles a violated claim. The only such label (`leakage-baseline`, refund as a valid predictor, `partly`) agrees.
