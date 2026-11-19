# Before/after: the baseline and the Phase 1 agent (P2.8)

All 7 eval cases, 3 repeats each, on Claude Haiku 5.5. Three suites: the baseline (`v0.1.1-baseline-hosted`), the Phase 1 agent with its default budgets, and the Phase 1 agent with the `hosted` preset (`max_follow_ups` 2 → 5, `max_revisions` 1 → 2). Findings, false claims and caveats are scored by the LLM judge (Claude Sonnet 5.5, rubric `983aca5d02a5`, [calibrated](calibration/README.md)); facts, unverified numbers, cost and time by the deterministic graders.

Results: [baseline](../../evals/results/20261105-134725_baseline_claude-haiku-5-5.jsonl), [current](../../evals/results/20261105-140404_current_claude-haiku-5-5.jsonl), [current, `hosted`](../../evals/results/20261105-152942_current_claude-haiku-5-5.jsonl). Snapshots in `evals/snapshots/`, regraded in CI. Each cell is the mean over repeats, with min–max where they differ.

## Summary

| Metric | Baseline | Current | Current, `hosted` |
|---|---|---|---|
| Runs ok | 100% | 100% | 100% |
| **Findings** | **53% (47–58%)** | **98% (95–100%)** | 96% (95–99%) |
| False claims a run | 0.1 | 0.0 | 0.0 |
| Facts | 57% (44–79%) | 90% | 94% (90–100%) |
| Caveats | 100% | 100% | 100% |
| Unverified numbers a run | not checked | 0.1 | 0.2 |
| Unresolved review objections a run | no review | 1.2 | 0.7 |
| Cost a run | $0.024 | $0.076 | $0.138 |
| Minutes a run | 4.1 | 14.3 | 23.7 |
| Cost, 21 runs | $0.50 | $1.59 | $2.90 |

- **The Phase 1 agent finds 98% of the planted findings, against 53% for the baseline, with no false claims.** `evals compare` finds no case where it does worse than the baseline on any quality metric. It costs 3× as much and takes 3.5× as long.
- **The baseline makes the claims the traps are built for.** Once each on `leakage` and `pure_noise`, both hedged (½). The Phase 1 agent makes none in 42 runs.
- **The `hosted` preset buys review closure, not findings.** Twice the revisions and follow-ups leave fewer objections unresolved (15 of 21 runs → 11), but findings don't rise (−2 points, within the judge's noise) and it costs 1.8× as much. The cases can't show more than that: the default agent is already at 98%.
- **The weakest finding is the weekend effect in `datetime_trend`.** The current agent misses it in 1 of 3 repeats, the `hosted` preset in 2. Two of those reports never test the weekly pattern (one lists it as an open question); the third uses day of week only as a model feature.

## Before the runs

- **Specialists record every number they cite as a fact value.** In the first suite they put some in fact descriptions ("…; sd 0.0346", "at mid temperature 12.40"), which the number check doesn't read: 8 untraced numbers in `planted_effects`, 3 in `datetime_trend`. One prompt line ([step.jinja2](../../agent/templates/specialists/step.jinja2)); a two-case check run gave 0 and 0. The current suites ran with it before it was committed, hence `code 9066886-dirty` in their results: the difference is that line.

## After the runs

- **`target` added to the keywords of the outcome-rate facts** in `planted_effects` and `pure_noise`, after the results. Two current reports and one baseline report give the rate on a "Target" line, without the word "outcome" outside a code span (the number check drops code spans). All three matches checked by hand; the first suite's grades don't change.
- **The judge checked on 3 fresh reports, labelled by the owner**: 15 of 20 items exact, 20 of 20 within ½; on the 14 items labelled before seeing the verdicts, 9 exact and 14 within ½. All 5 disagreements are in the baseline report, and in each the judge gives the report more credit than the owner. Details in the [calibration README](calibration/README.md).

## Caveats

- **Times are inflated by load.** Up to 8 runs shared the machine (the baseline ran alongside the current suite, as in the first suite). The current agent took 8.9 min a run in the first suite and 14.3 here. Compare times between these suites, not with other runs.
- **The judge may flatter the baseline.** On the fresh baseline report it gives hedged statements ("Supported, but unverified", "Probably not supported") `partly`, where the owner labels them `no`: 70% findings by the judge, 40% by the owner. If anything, the gap is larger than 53% → 98%.
- **The cases are near the ceiling for the current agent.** A change that helps it (Phase 3) can show up only on `datetime_trend`, as fewer unresolved objections, or as lower cost and time. Harder cases are needed to measure more.
- **One model, 3 repeats.** Not re-run on qwen3.5.
- **Not a held-out measurement.** Phase 1 was developed on titanic, one of the 7 cases; the other 6 were written after it, by people who knew the design. The one agent change made after seeing these cases is the step.jinja2 line above. No prompt names a case or its traps (checked 2026-11-09). Phase 3 adds held-out cases, written by the owner, that nothing is tuned on, and runs the baseline on them too.

## Per suite

### baseline · claude-haiku-5-5 · code v0.1.1-baseline-hosted

`20261105-134725_baseline_claude-haiku-5-5`: 7 cases × 3 repeats

| Case | Runs ok | Findings | False claims | Facts | Caveats | Unverified numbers | Cost | Minutes |
|---|---|---|---|---|---|---|---|---|
| datetime_trend | 100% | 44% (33%–50%) | 0.0 | 22% (0%–33%) | — | — | $0.024 ($0.023–$0.025) | 4.1 (3.8–4.3) |
| leakage | 100% | 53% (50%–60%) | 0.3 (0.0–0.5) | 56% (33%–67%) | 100% | — | $0.019 ($0.018–$0.020) | 3.4 (3.2–3.5) |
| planted_effects | 100% | 57% (40%–70%) | 0.0 | 83% (50%–100%) | 100% | — | $0.021 ($0.018–$0.023) | 4.0 (3.5–4.3) |
| pure_noise | 100% | 67% (50%–100%) | 0.2 (0.0–0.5) | 67% (0%–100%) | — | — | $0.024 ($0.020–$0.031) | 4.2 (3.3–5.5) |
| regression_outliers | 100% | 33% (12%–50%) | 0.0 | 33% (0%–100%) | 100% | — | $0.021 ($0.019–$0.024) | 3.7 (3.0–4.9) |
| string_target | 100% | 67% (62%–75%) | 0.0 | 56% (33%–100%) | — | — | $0.034 ($0.031–$0.037) | 5.3 (4.6–6.3) |
| titanic | 100% | 50% (43%–57%) | 0.0 | 81% (57%–100%) | 100% | — | $0.025 ($0.022–$0.029) | 4.3 (3.6–5.0) |
| **Overall** | **100%** | **53% (47%–58%)** | **0.1** | **57% (44%–79%)** | **100%** | **—** | **$0.024 ($0.023–$0.025)** | **4.1 (3.8–4.5)** |

Total cost $0.50. Judge: claude-sonnet-5-5 (rubric `983aca5d02a5`)

### current · claude-haiku-5-5 · code 9066886-dirty

`20261105-140404_current_claude-haiku-5-5`: 7 cases × 3 repeats

| Case | Runs ok | Findings | False claims | Facts | Caveats | Unverified numbers | Cost | Minutes |
|---|---|---|---|---|---|---|---|---|
| datetime_trend | 100% | 89% (67%–100%) | 0.0 | 44% (33%–67%) | — | 0.0 | $0.060 ($0.054–$0.066) | 10.5 (9.5–12.1) |
| leakage | 100% | 100% | 0.0 | 89% (67%–100%) | 100% | 0.0 | $0.078 ($0.064–$0.088) | 15.2 (14.5–15.7) |
| planted_effects | 100% | 100% | 0.0 | 100% | 100% | 0.0 | $0.069 ($0.055–$0.082) | 13.7 (8.7–17.6) |
| pure_noise | 100% | 100% | 0.0 | 100% | — | 0.3 (0.0–1.0) | $0.084 ($0.078–$0.090) | 16.0 (14.6–18.4) |
| regression_outliers | 100% | 100% | 0.0 | 100% | 100% | 0.7 (0.0–2.0) | $0.074 ($0.069–$0.083) | 14.5 (13.2–16.1) |
| string_target | 100% | 100% | 0.0 | 100% | — | 0.0 | $0.061 ($0.048–$0.080) | 12.3 (9.9–14.7) |
| titanic | 100% | 100% | 0.0 | 100% | 100% | 0.0 | $0.103 ($0.070–$0.134) | 18.1 (13.9–22.2) |
| **Overall** | **100%** | **98% (95%–100%)** | **0.0** | **90%** | **100%** | **0.1 (0.0–0.4)** | **$0.076 ($0.068–$0.082)** | **14.3 (12.9–16.0)** |

Total cost $1.59. Judge: claude-sonnet-5-5 (rubric `983aca5d02a5`)

### current · claude-haiku-5-5 · preset hosted · code 9066886-dirty

`20261105-152942_current_claude-haiku-5-5`: 7 cases × 3 repeats

| Case | Runs ok | Findings | False claims | Facts | Caveats | Unverified numbers | Cost | Minutes |
|---|---|---|---|---|---|---|---|---|
| datetime_trend | 100% | 78% (67%–100%) | 0.0 | 56% (33%–100%) | — | 0.0 | $0.081 ($0.064–$0.101) | 14.6 (10.4–19.4) |
| leakage | 100% | 97% (90%–100%) | 0.0 | 100% | 100% | 0.0 | $0.126 ($0.122–$0.133) | 21.0 (20.6–21.4) |
| planted_effects | 100% | 100% | 0.0 | 100% | 100% | 0.0 | $0.132 ($0.111–$0.153) | 24.9 (20.2–31.3) |
| pure_noise | 100% | 100% | 0.0 | 100% | — | 0.7 (0.0–2.0) | $0.145 ($0.125–$0.159) | 26.5 (24.4–30.3) |
| regression_outliers | 100% | 100% | 0.0 | 100% | 100% | 0.7 (0.0–2.0) | $0.176 ($0.159–$0.195) | 29.2 (22.8–34.0) |
| string_target | 100% | 100% | 0.0 | 100% | — | 0.0 | $0.124 ($0.071–$0.176) | 23.8 (9.1–41.4) |
| titanic | 100% | 100% | 0.0 | 100% | 100% | 0.0 | $0.183 ($0.179–$0.187) | 25.8 (20.9–28.5) |
| **Overall** | **100%** | **96% (95%–99%)** | **0.0** | **94% (90%–100%)** | **100%** | **0.2 (0.0–0.6)** | **$0.138 ($0.134–$0.143)** | **23.7 (21.3–25.3)** |

Total cost $2.90. Judge: claude-sonnet-5-5 (rubric `983aca5d02a5`)
