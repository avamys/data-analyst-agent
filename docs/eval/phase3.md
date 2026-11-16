# Phase 3: dev and held-out (P3.5)

The Phase 3 agent (`v0.3.0-phase3`, `b5cd09c`) and the baseline (`v0.1.1-baseline-hosted`) on Claude Haiku 5.5, judged by Claude Sonnet 5.5 (rubric `983aca5d02a5`, [calibrated](calibration/README.md)). **Dev** is the 12 cases fixes were developed on: the 7 original ones and the 5 from P3.2. **Held-out** is 4 synthetic cases the owner wrote before any P3.4 change ([brief](heldout-brief.md)). Nobody saw them run before this, and their hash (`84373d41…`) matched before the run. Each cell is the mean over repeats, with min–max where they differ.

Results: dev [Phase 3](../../evals/results/20261113-181103_current_claude-haiku-5-5.jsonl), [Phase 3 at `low` effort](../../evals/results/20261113-194554_current_claude-haiku-5-5.jsonl); held-out [Phase 3](../../evals/results/20261116-140723_current_claude-haiku-5-5.jsonl), [baseline](../../evals/results/20261116-143625_baseline_claude-haiku-5-5.jsonl); dev baseline from [P2.8](before-after.md). Snapshots in `evals/snapshots/`, regraded in CI.

## Summary

| Metric | Phase 3, dev (12 × 3) | Phase 3, held-out (4 × 3) | Baseline, dev (7 × 3, P2.8) | Baseline, held-out (4 × 3) |
|---|---|---|---|---|
| Runs ok | 100% | 100% | 100% | 100% |
| **Findings** | **96% (94–97%)** | **78% (68–84%)** | 53% (47–58%) | 19% (16–21%) |
| False claims a run | 0.01 | **0.2 (0.1–0.2)** | 0.1 | 0.0 (0.0–0.1) |
| Facts | 92% | 67% (50–75%) | 57% | 0% |
| Caveats | 100% | 58% | 100% | 52% |
| Unverified numbers a run | 0.3 | 0.2 | not checked | not checked |
| Cost a run | $0.087 | $0.080 | $0.024 | $0.021 |
| Minutes a run | 9.5 | 8.4 | 4.1 | 3.9 |

- **The gap to the baseline holds on unseen data, and widens.** 78% against 19% held-out (+59 points), against 96% vs 53% on dev. Both agents score lower held-out, which suggests the cases are harder, not only new.
- **The Phase 3 agent makes false claims held-out, all in one case.** h3 hides missing weights as zeros. 150 of 1,000 parcels have weight 0.0, and those parcels take ~30 h longer, so the pooled weight effect turns negative. The agent reports "heavier parcels are delivered faster" in 2 of 3 runs (half a claim in the third). It never counts the zeros as missing and never finds the positive slope among recorded weights. Findings 42%.
- **The dev twin of h3 scored 100%, which suggests memory.** `diabetes` (Pima) has the same trap, and the agent treated its zeros as missing in every run. Pima's zeros are well known; h3's dataset can't be. P3.2 named this risk; this is the first measure of it.
- **The dev/held-out gap is mostly h3.** The plan reads a gap as tuning. Phase 3 changed no prompts aimed at the dev cases, though, and without h3 the held-out score is 90% (h1 83%, h2 100%, h4 87%).

## By case, held-out

| Case | Tests | Phase 3 findings | False claims a run | Baseline findings |
|---|---|---|---|---|
| h1 | Confounding by a tier mix that shifts over time (pooled rate rises, every tier falls) | 83% (75–100%) | 0 | 12% |
| h2 | Effect directions that run against intuition, in features that top any importance ranking | 100% | 0 | 17% |
| h3 | Missing values coded as 0, reversing an effect | 42% (25–62%) | 0.8 | 12% |
| h4 | Regression to the mean: extra sessions given to the lowest scorers | 87% (70–100%) | 0 | 33% |

## The known weaknesses

Both were found on dev in P3.2 and left unfixed in P3.4. The held-out cases were written to measure them.

| Weakness | Dev | Held-out |
|---|---|---|
| Effect direction given only as an importance rank | 2 findings in 36 runs (bike_sharing temperature, penguins flipper length) | 0 in 3 runs: all three state h2's reversed directions |
| Confounding not followed through | penguins, 2 of 3 runs | h1: no run claims improvement; the within-tier fall is stated in all 3 (with figures in 1), the mix as its cause in 2 of 3 (partly in the third) |

Neither shows up held-out at the dev rate. The weakness that does show up is a third one: a trap the agent passes on a famous dataset and fails on an unknown one.

## Effort

Specialists at `low` effort on dev, × 1: findings 95% against 96%, false claims 0.04 against 0.01 a run, −15% cost, −12% time. One repeat shows large differences only, and there are none. Evals stay at the default (`medium`); `SPECIALIST_EFFORT=low` stays a setting for quick runs.

## After the run

`evals/heldout/` was committed byte-for-byte (the hash still matches) and excluded from ruff, which would reformat two files.

**One change, made after seeing h3** (`8a83b62`). It isn't part of the numbers above, and h3 is no longer unseen evidence for it. The cause of h3's failure was in our own dataset profile: it told every agent "Missing values: none", because it counts empty cells only, and r2's report repeated that. The profile now says "Empty cells". It also gives every numeric column its min, 1st percentile, median, max and, when it covers at least 1% of rows, its most common value. These are facts with no judgement: h3's weight reads "min 0, 1st pct 0, median 3.735, max 35.12; most common 0 (150 of 1,000)". The same lines show the zeros in Pima's columns, Titanic's zero fares and one bike-sharing day at 0% humidity. Standardized columns show nothing unusual.

h3 × 3 with the change ([results](../../evals/results/20261116-154250_current_claude-haiku-5-5.jsonl), $0.31, outside the $10 budget):

| h3 | Before | After |
|---|---|---|
| Findings | 42% | 75% (62–88%) |
| False claims a run | 0.8 | 0 |
| Facts | 0% | 100% |
| Weight effect among recorded weights found | 0 of 3 (1 partly) | 2 of 3 (1 partly) |
| Zero-weight parcels ~30 h slower | 0 of 3 (1 partly) | 3 of 3 |

All three lead plans now mention the 150 zeros from the profile; none did before. The reports still hedge on calling the zeros missing (`partly` in all 3). Not checked: the other cases. The change alters what the agent sees on titanic, diabetes and bike_sharing, and those weren't re-run.

## Caveats

- **Held-out is 4 cases × 3.** One case moves the overall score by about 12 points, and h3's 0.8 false claims a run is 2.5 claims in 3 runs.
- **Caveats are scored on case-specific terms.** The held-out cases ask for domain caveats the dev cases don't, such as an engagement proxy (h2) and regression to the mean (h4). 58% partly reflects that.
- **Times are at 4 runs at a time**, as for the dev suites. The two held-out suites ran one after the other, not side by side.
- **Cost:** dev × 3 $3.87, `low` × 1 $1.13, held-out $1.71 (Phase 3 $1.22, baseline $0.49), all including the judge. That makes $6.71 of the $10 budget.
