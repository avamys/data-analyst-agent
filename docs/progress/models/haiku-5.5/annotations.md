# Claude Haiku 5.5 reference run: claim-by-claim check

Report: [report.md](report.md) · run `20261102-170201_titanic_claude-haiku-5-5` · commit `2b189ff` + the provider changes (uncommitted at run time, committed right after) · 7 tasks (5 planned + 2 follow-ups), 12.5 min, 58 LLM calls, 607k input / 118k output tokens, **$0.12**.
Same code and prompts as the [P1.4 run](../../p1.4/annotations.md); only the model differs. Method as in the [baseline annotations](../../../baseline/annotations.md). Every number below was recomputed from the raw CSV, not taken from the run's facts.

**Legend:** ✅ correct · ❌ wrong · ⚠️ unsupported (not computed in this run) · ➖ misleading or incomplete

## Summary

| | Baseline (qwen) | P1.4 (qwen) | Haiku 5.5 |
|---|---|---|---|
| ✅ Correct | 15 | 14 | 26 |
| ❌ Wrong | 7 | 5 | **0** |
| ⚠️ Unsupported | 6 | 6 | 3 |
| ➖ Misleading | 6 | 2 | 4 |
| Baseline findings still absent | 7 | 2 | **0** |
| Charts | 0 | 12 | 1 (its link in the report has no path) |
| Time | 25 min | 120 min | 12.5 min |

- **Both P1.4 method errors are gone.** Age is tested on recorded ages (Welch p = 0.041, Holm 0.082: "borderline, not significant after correction"). Feature importance is permutation importance on the test set, and the report says the logistic coefficients are unscaled and can't be ranked.
- **The statistics reproduce exactly**, including the less routine ones: Sex × Pclass LR χ² 28.79 (AIC 834.9 → 810.1) and, adjusted for Age and Fare on 714 rows, 33.81 (659.2 → 629.4); Sex × Age 9.55; adjusted Embarked ORs 1.81 / 1.57.
- **It states the right caveats:** the two interaction tests use different samples (on the same 714 rows the unadjusted χ² is 30.16, so the rise to 33.81 is not an adjustment effect); median imputation before the split leaks a little test data; the random forest overfits (train–test gap 0.20).
- **What's left is the writer going beyond the findings:** 3 unsupported and 4 misleading statements, all in summary or synthesis prose, none in a computed number. That is P1.5's job.
- **More tokens:** 2.7× the input of the qwen run. Haiku records far more facts (75 in `eda_1`), and the fact lists go into later prompts.
- **Charts regressed:** 1 chart in the whole run, against 12 for qwen.

## Claims

| Line | Claim | Verdict | Truth / evidence |
|---|---|---|---|
| 5, 94 | Female 74.2% (233/314) vs male 18.9% (109/577); V = 0.543, χ² = 263.05 | ✅ | χ² without continuity correction (260.72 / V = 0.541 with it) |
| 6, 71–74, 110–111 | Sex × class rates and gaps; interaction LR χ² = 28.79, df 2, p = 5.6e-7; AIC 834.9 → 810.1; sex gaps 60 / 76 / 36 points | ✅ | Recomputed |
| 6, 115 | Adjusted for Age and Fare on 714 rows: χ² = 33.81, p = 4.6e-8, AIC 659.2 → 629.4 | ✅ | Recomputed |
| 117, 224 | The 891- and 714-row tests aren't comparable | ✅ | On the same 714 rows the unadjusted χ² is 30.16 |
| 7, 145–149, 153–154 | LR test accuracy 77.6%, AUC 0.841, precision/recall/F1; RF 0.780; baseline 61.4%; gaps 0.03 / 0.20; ±5 points at n = 223 | ✅ | `ml_1.ml_1_logreg`, `ml_1_rf`; baseline 137/223 |
| 8, 100, 107 | Age: Welch p = 0.041, Holm 0.082, Mann-Whitney p = 0.160, rank-biserial −0.062 | ✅ | Recorded ages only |
| 9, 21–25, 217 | Missing Cabin 77.1%, Age 19.9%, Embarked 0.2%; Age median (28.0) imputed before the split | ✅ | `ml_1/analysis.py` lines 20–26 |
| 13 | 549 (61.6%) died, 342 (38.4%) survived | ✅ | |
| 15–16 | Numeric: Age, Fare, SibSp, Parch, Pclass; categorical: Sex, Embarked | ✅ | (P1.4 swapped these) |
| 58–67, 76, 79–80 | Survival by sex, class, port, SibSp, Parch, with n | ✅ | |
| 83–84 | Age mean 28.3 / 30.6, median 28 / 28, IQR 19–36 / 21–39; Fare mean 48.40 / 22.12, median 26.0 / 10.5 | ✅ | |
| 94–100 | χ² and Welch p-values, mean differences, Holm values for 7 tests | ✅ | Recomputed |
| 95 | Pclass V = 0.340 "medium to large" | ✅ | df 2: thresholds 0.07 / 0.21 / 0.35, so 0.340 is just below "large" |
| 96 | Embarked V = 0.173 "small" | ✅ | |
| 98–99, 187 | Any parent/child +16.8 points (p = 1.1e-5); any sibling/spouse +12.1 (p = 5.4e-4) | ✅ | χ² without correction |
| 113 | Sex × Age, 714 rows: χ² = 9.55, p = 0.002 | ✅ | Model without Pclass |
| 118 | Fare–Pclass r = −0.554 | ✅ | On the 714 complete cases (−0.549 on all rows) |
| 124, 127 | Adjusted Embarked: LR χ² = 7.96, p = 0.019; OR C 1.81 (1.16–2.83), Q 1.57 | ✅ | Recomputed |
| 124–125 | "Holm-adjusted p (approx.)" 0.056 / 0.037 | ➖ | An adjusted test slotted into the primary 7-test family: improvised. Flagged as approximate. |
| 130–131 | Missingness: survival 30.0 vs 66.7% (Cabin), 29.4 vs 40.6% (Age); p-values; rates by class; fare medians; Age vs sex p = 0.12 | ✅ | Recomputed |
| 132, 219 | Both missing-Embarked passengers survived, both first class; filled with S in the model | ✅ | |
| 136 | Stratified 75/25, seed 42, 668 / 223 rows | ✅ | |
| 156–168 | Permutation importances; Sex about 4× the next | ✅ | `ml_1` facts; 0.209 / 0.054 |
| 172 | "Logistic regression coefficients (Sex 2.54, Pclass 1.10, Fare 0.003)" | ➖ | Absolute values: the Pclass coefficient is −1.10. The point made (unscaled, not comparable) is right. |
| 175 | "Knowing sex alone captures most of the predictable signal" | ⚠️ | No sex-only model was fitted |
| 176 | Good at identifying non-survivors | ✅ | Not recorded, but follows from the metrics: specificity 0.83 |
| 183, 198 | Sex is the strongest factor in tests, model and EDA | ✅ | |
| 184 | The interaction is significant "in the model, where class and sex are both important" | ➖ | The model has no interaction term; it shows two main effects |
| 185 | Fare "carries only a limited independent signal once class is controlled" | ⚠️ | Never tested. The next sentence says it isn't settled; RF permutation gives Fare 0.040. |
| 192 | Age matters conditionally on sex: "a hypothesis, not a tested result" | ✅ | Correctly labelled |
| 201 | "Sex and passenger class are the two features that consistently carry predictive value" | ➖ | Age (0.051) ties with Pclass (0.054); Fare 0.040 |
| 205 | Cherbourg OR about 1.8–1.9 after adjustment, provisional | ✅ | |
| 225 | "The coefficient (−0.041) was not recorded … and is excluded from this report" | ⚠️ | States a number it says it excludes; no fact backs it (the lead had asked stat_2 to remove it) |

## Baseline findings that are still absent

| Finding | This run |
|---|---|
| Survival by sex | ✅ Present |
| Survival by class | ✅ Present |
| Fare by outcome | ✅ Present |
| Survival with / without a cabin record | ✅ Present (30.0% vs 66.7%) |
| Survival with missing Age | ✅ Present (29.4% vs 40.6%) |
| Feature importances | ✅ Present (permutation, valid as a ranking) |
| Precision / recall / F1 | ✅ Present |

## The lead's reviews

All 7 tasks were sent back once. 4 were accepted after the revision. 3 were still at "revise" when the budget (1 revision) ran out: `ml_1`, `stat_2`, `stat_4`. Two follow-ups were added: the Embarked effect adjusted for class and sex (`stat_3`), and the Sex × Pclass interaction adjusted for Age and Fare (`stat_4`). Both made it into the report.

Every send-back named a real problem: an uncorrected p-value, a number in the report that no fact backed, a claim about an interaction term the model didn't have. No review introduced an error.

## Fixes this run needed

| Run | Failure | Fix |
|---|---|---|
| `20261102-145428` | Review of `stat_1`, after 4 min: Haiku left out the required `verdict` field twice. The forced tool call doesn't enforce the schema. | Structured output on Anthropic uses JSON outputs (`output_config.format`), which do. The failing prompt then parsed 3 of 3 times. |
| `20261102-150716` | After all 8 tasks: with thinking on, a text reply is a list of blocks, and the synthesizer's `.content.strip()` crashed | `message.text()` in the synthesizer and the reporter |

## Observations for the next steps

| Observation | Step |
|---|---|
| The remaining errors are all writer prose beyond the findings | P1.5: the lead writes from accepted findings only, plus the number check |
| 1 chart in the whole run; the report's image link has no path | P1.5: charts embedded in `report.md`. The prompts may need to ask Haiku for charts more firmly. |
| 3 of 7 tasks ended unresolved at the revision budget | Raise `max_revisions` to 2 for hosted runs: cheap at $0.12 a run |
| 607k input tokens, 2.7× qwen, from long fact lists in prompts | Cap or summarise facts in prompts; it matters on Sonnet (about $2.40 a run at these tokens) |
