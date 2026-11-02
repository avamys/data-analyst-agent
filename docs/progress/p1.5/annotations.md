# P1.5 reference run: claim-by-claim check

Report: [report.md](report.md) · run `20261102-181146_titanic_claude-haiku-5-5` on **Claude Haiku 5.5** · commit `4352465` + the P1.5 changes (committed right after) · 7 tasks (5 planned + 2 follow-ups), 9.3 min, 47 LLM calls, 375k input / 89k output tokens, **$0.08**.
Method as in the [baseline annotations](../../baseline/annotations.md). Every number was recomputed from the raw CSV. The model is Haiku, not qwen3.5: see the [Haiku check of the P1.4 code](../models/haiku-5.5/annotations.md) for the model's effect on its own.

**Legend:** ✅ correct · ❌ wrong · ⚠️ unsupported (not computed in this run) · ➖ misleading or incomplete

## Summary

| | Baseline (qwen) | P1.4 (qwen) | P1.4 (Haiku) | P1.5 (Haiku) |
|---|---|---|---|---|
| ✅ Correct | 15 | 14 | 26 | 24 |
| ❌ Wrong | 7 | 5 | 0 | **0** |
| ⚠️ Unsupported | 6 | 6 | 3 | **0** |
| ➖ Misleading | 6 | 2 | 4 | 1 |
| Baseline findings still absent | 7 | 2 | 0 | **0** |
| Charts in the report | 0 | 0 (12 saved) | 1 (broken link) | **5** |
| Time / cost | 25 min | 120 min | 12.5 min / $0.12 | 9.3 min / $0.08 |

- **The writer stays within the findings.** Each interpretive sentence traced back to an accepted finding, for example "the simpler logistic regression is as good a choice" (`ml_1`). Where findings disagree (Welch against Mann-Whitney on Age; logistic coefficients against permutation importance), the report gives both and says that it doesn't resolve the disagreement. The unresolved review issue (`ml_1`, collinearity) is stated under Limitations, along with the findings it affects.
- **The number check works on real reports.** Calibrated on the earlier Haiku report, it flagged exactly the 7 numbers no fact backs (survivor counts and gaps the writer had worked out, an execution time) out of hundreds. In the first P1.5 run it sent back a count the writer had computed (110), which the rewrite removed.
- **Two false positives, fixed after the runs.** Numbers recorded inside strings (`"(7.91, 14.454]"`) and in fact names (`survival_rate_Fare_bin_(-0.001, 7.91]`) didn't count as recorded. This run's report lists `7.91` and `31.0` as untraced. Both are recorded, and the fixed check finds nothing in this report.
- **Charts:** 5 saved and 5 embedded, one per finding group, all rendering.
- **The one ➖ is an analysis choice, not the writer:** `stat_3` entered Pclass as a single linear number without saying so. The conclusion holds with Pclass as a category, but the numbers differ. `stat_3` did the same in the first P1.5 run.

## Claims

| Line | Claim | Verdict | Truth / evidence |
|---|---|---|---|
| 5, 33 | Female 74.2% vs male 18.9%; χ² 263.05, V 0.543; OR male vs female 0.081 (0.058–0.112) | ✅ | Recomputed |
| 6, 44 | Sex × Pclass LR χ² 28.79, p 5.6e-7; female/male OR 51.9 / 62.5 / 6.38 by class | ✅ | Recomputed |
| 6, 45 | Adjusted for Age, Fare, Embarked on 712 rows: χ² 33.70, p 4.8e-8; same 712 rows unadjusted: 29.93 | ✅ | Recomputed; comparing on the same rows is right |
| 7, 53–56 | Fare adds nothing once Pclass and Sex are in: LR 0.715, p 0.40; OR 1.10 per log unit, 1.015 per 10 units; coefficient 0.642 → 0.099, "about 85%" | ➖ | Reproduces exactly with **Pclass as one linear term**, which the report doesn't say. With Pclass as a category: LR 0.97, p 0.33, 82%. The conclusion holds. |
| 7, 26 | Fare quartiles 19.7 / 30.4 / 45.5 / 58.1%, edges 7.91 / 14.45 / 31.0, n 223 / 224 / 222 / 222 | ✅ | |
| 8, 72–75 | Baseline 61.4%; LR 78.5% (AUC 0.840), RF 78.9% (AUC 0.836); training 81.0% / 92.1%; 668 / 223 rows | ✅ | `ml_1` facts; 25% stratified split |
| 12–16 | 891 × 12; 38.4% survived (342); feature types; missing Age 177 (19.9%), Cabin 687 (77.1%), Embarked 2 | ✅ | |
| 22–24 | Survival by sex, class and port, with n; both missing-port passengers survived | ✅ | |
| 25 | Age quartiles 45.8 / 36.1 / 43.4 / 37.3%; missing Age 29.4% | ✅ | Bins 0.42–20.1 / –28 / –38 / –80 |
| 27 | Means: Fare 48.4 / 22.1, Age 28.3 / 30.6, SibSp 0.47 / 0.55, Parch 0.47 / 0.33 | ✅ | Survivors' Parch is 0.4649: the fact was recorded rounded (0.465) and rounded again |
| 34 | Pclass χ² 102.89, V 0.340; OR against the other classes 3.87 / 1.59 / 0.254 | ✅ | Recomputed |
| 35 | Embarked on 889 rows: χ² 26.49, V 0.173; minimum expected count 29.4 | ✅ | Excluding the 2 missing is justified correctly |
| 36 | Fare: Mann-Whitney p 4.6e-22, Welch p 2.7e-11, difference 26.28 (18.73–33.83), medians 26.0 / 10.5 | ✅ | |
| 37, 90 | Age: Mann-Whitney p 0.16 against Welch p 0.041; −2.28 years (−4.47 to −0.09); disagreement left open | ✅ | |
| 43 | The six Sex × Pclass cells; "gap widest in classes 1 and 2" | ✅ | Gaps 59.9 / 76.4 / 36.5 points |
| 46 | Sex × Age: χ² 9.55, p 0.002; per-year OR 1.020 (women), 0.979 (men); interaction 0.960 | ✅ | Recomputed |
| 47, 91 | With Pclass: χ² 11.90, p 0.00056; not adjusted for Fare or Embarked | ✅ | |
| 55 | Fare–Pclass r −0.55; log(Fare+1) −0.66 | ✅ | |
| 60–64 | Missingness: survival 29.4 / 40.6% (Age), 30.0 / 66.7% (Cabin); class shares; p-values; Age vs Sex p 0.119 | ✅ | |
| 65 | Missing port: median Fare 80.0 against 14.45; both first-class women who survived | ✅ | |
| 71, 87 | Age median and Embarked mode computed on the full data before the split, so test scores are slightly optimistic | ✅ | `ml_1/analysis.py` lines 20–21 |
| 76 | The models perform almost identically; RF overfits more | ✅ | From `ml_1`'s finding |
| 77–80 | Feature importances (standardized coefficients, impurity, permutation); the measures disagree, left open | ✅ | `ml_1` facts |
| 86 | Unresolved review issue: collinearity of SibSp / Age_missing / Embarked coefficients | ✅ | The lead's last objection on `ml_1` |
| 89 | Class 1 and 2 male cells have 45 and 17 survivors; wide CIs | ✅ | |

## Baseline findings that are still absent

| Finding | This run |
|---|---|
| Survival by sex | ✅ Present |
| Survival by class | ✅ Present |
| Fare by outcome | ✅ Present |
| Survival with / without a cabin record | ✅ Present (30.0% vs 66.7%) |
| Survival with missing Age | ✅ Present (29.4% vs 40.6%) |
| Feature importances | ✅ Present (three measures, disagreement stated) |
| Precision / recall / F1 | ✅ Present |

## Phase 1 exit criteria

| Criterion | Status |
|---|---|
| Specialists see their output and iterate; each task's code is a runnable cell script | ✅ (P1.1–P1.2) |
| The lead reviews every task (accept / revise / follow-up) within budgets | ✅ 7 of 7 reviewed, 2 follow-ups |
| The report is written from accepted findings, facts and charts; every number matches a recorded fact (automatic check) | ✅ |
| Reference run: 0 wrong, ≤ 2 unsupported, every baseline finding present, ≥ 2 charts | ✅ 0 / 0 / 7 of 7 / 5, **on Haiku 5.5**. Not yet run on qwen3.5. |
| No dataset-specific text and no example pipelines in prompts | ✅ (test) |

## Observations for the next steps

| Observation | Step |
|---|---|
| Statistical tasks put ordinal columns in models as one linear term without saying so (`stat_3`, two runs in a row) | Prompt: state how each predictor is coded; or a sanity check on `smf.logit` formulas with a numeric ordinal column |
| Specialists round values before `record_fact` (0.4649 → 0.465 → "0.47") | Prompt: record values unrounded; rounding is for display |
| Numbers matched by coincidence: with hundreds of recorded values, a wrong number can round to some other fact's value | Phase 3 plan: the writer cites `{{fact:…}}` references if drift shows up in the eval |
| The check covers digits only: "about double", "most" are not checked | The eval's LLM judge (Phase 2) |
