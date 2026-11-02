# First eval suite, judged by hand (P2.3)

The first two suite runs: all 7 cases, 1 repeat, Claude Haiku 5.5, baseline (`v0.1.1-baseline-hosted`) and current (`9d1f7ec`, `local` preset). The `must_find` items were judged by hand against the reports, before the graders and the LLM judge exist. These labels are a first set for calibrating the judge (P2.6).

Results: [baseline](../../evals/results/20261102-203054_baseline_claude-haiku-5-5.jsonl), [current](../../evals/results/20261102-203054_current_claude-haiku-5-5.jsonl). The run directories are under `evals/runs/` (not committed).

**Legend:** ✓ found · ½ half: the effect is named but without its direction or size · ✗ missing

## Summary

| | Baseline | Current |
|---|---|---|
| Runs finished with a report | 7 / 7 | 7 / 7 |
| `must_find` items | **16 / 30 (53%)** | **30 / 30** |
| `must_not_claim` items violated | ½ (`leakage`: refund as a valid predictor) | 0 |
| Other false claims found | 1 (`titanic`: adjusted OR for female 3.91; true 12–14) | 0 in the spot checks |
| Expected facts stated (deterministic) | 9 / 21 | 21 / 21 |
| Required caveats (keywords) | 4 / 4 | 4 / 4 |
| Time per case | 2.8–5.1 min | 7.6–10.8 min |
| Cost, all 7 cases | $0.16 | $0.50 |

- **The baseline loses findings to truncated output, and mostly says so.** Its reports state that results "were not returned", the direction is "unconfirmed", or the effect is "not quantified". The specialists never saw their own output.
- **Both versions pass `pure_noise`.** The baseline also passes it on a clean run. In the first, discarded run it invented a data-integrity problem from a truncated table.
- **Only the current version passes `leakage`.** It shows churn is 95.9% with a refund and 1.6% without, and that models lose to the baseline once the column is removed. The baseline calls `refund_issued` "the strongest reported predictor" and only suspects leakage.
- **`datetime_trend` is not the gap expected.** Both versions derive weekday, month and trend from `date`, even though the profile classifies it as an id column.

## Item by item

| Case | Item | Baseline | Current |
|---|---|---|---|
| titanic | Women survived far more than men | ✓ | ✓ |
| | Survival falls with class | ✓ | ✓ |
| | Survivors paid higher fares | ✗ not reported | ✓ |
| | No cabin record: lower survival | ✗ Cabin dropped | ✓ |
| | Missing Age: lower survival | ✗ | ✓ |
| | Model beats the majority-class baseline | ✓ | ✓ |
| | Precision, recall or F1 reported | ✗ "not reported" | ✓ |
| planted_effects | feat_a strongest | ✓ | ✓ |
| | feat_b weaker | ✓ | ✓ |
| | feat_d associated | ✗ only its missingness discussed | ✓ |
| | feat_c no association | ✓ | ✓ |
| | ~15% of feat_d missing | ✓ | ✓ |
| pure_noise | No feature associated | ✓ | ✓ |
| | Models don't beat the baseline | ✓ | ✓ |
| leakage | refund_issued leaks the target | ½ "may be inflated by leakage" | ✓ |
| | Without it, models predict only moderately | ✗ | ✓ |
| | Lower usage, more churn | ✓ | ✓ |
| | Shorter tenure, more churn | ✗ "not returned" | ✓ |
| | Basic plan churns more | ✗ "not reported" | ✓ |
| regression_outliers | Right-skewed price with outliers | ✓ | ✓ |
| | size_sqm strong positive | ½ no direction | ✓ |
| | age_years negative | ✗ | ✓ |
| | rating no association | ✗ | ✓ |
| string_target | Monthly contracts churn more | ½ "direction unconfirmed" | ✓ |
| | Higher fee, more churn | ✗ | ✓ |
| | More support calls, more churn | ✗ | ✓ |
| | region no association | ✓ | ✓ |
| datetime_trend | Upward trend | ✓ | ✓ |
| | Weekends higher | ½ "day of week" without direction | ✓ |
| | Promotion days higher | ✓ | ✓ |

## Problems this suite exposed

| Problem | Done |
|---|---|
| The dataset file names gave the answer away: a baseline report on `pure_noise.csv` called its result "consistent with the file name" | Neutral file names (`0992eb3`); the first suite was discarded and re-run |
| Specialists put computed numbers in fact descriptions ("…; sd 0.0349"), which the number check ignores, so the report lists them as untraced (`planted_effects`: 8, `datetime_trend`: 3) | Open: ask specialists to record every number they cite as a value |

## Caveats

One repeat and one judge (me), on Haiku: a first look, not the before/after result. P2.8 runs 3 repeats with the calibrated judge.
