# P1.2 reference run: claim-by-claim check

Report: [report.md](report.md) · run `20261101-112045_titanic_qwen3.5-9b` · commit `833df9c` · model `qwen3.5:9b`, 6 tasks, 45 min, 29 LLM calls, 6 charts.
Same method as the [baseline annotations](../../baseline/annotations.md): true values computed directly from `data/titanic.csv`.

**Legend:** ✅ correct · ❌ wrong · ⚠️ unsupported (not computed in this run) · ➖ misleading or incomplete

## Summary

| | Baseline | P1.2 |
|---|---|---|
| ✅ Correct | 15 | 14 |
| ❌ Wrong | 7 | 4 |
| ⚠️ Unsupported | 6 | 7 |
| ➖ Misleading | 6 | 2 |
| Baseline "computed but missing" findings still absent | 7 | 6 |
| Charts | 0 | 6 |

- **Computed results now reach the report.** Every metric for both models (accuracy, precision, recall, F1, AUC), the full t-test (t, p, Cohen's d, 95% CI) and both χ² tests are reported as recorded. The baseline lost these to truncation.
- **The remaining wrong numbers were computed wrong, not lost.** Cramér's V for Pclass used the wrong formula, and a finding mixed up the missing-Age counts. Nobody checks the specialists' work yet; that's the lead's review (P1.4).
- **The gap moved from "lost" to "never computed".** Survival by sex and by class, fare by outcome and feature importances weren't asked for by the plan. Specialists suggested related follow-ups, but nothing acts on them yet (P1.4).
- **A methodological problem went unnoticed.** `ml_1` prepared a clean 7-column feature set but didn't publish it. `ml_2` rebuilt its own and one-hot encoded `Name` and `Ticket`, giving 1,294 columns. The report then credits ml_1's cleaning for the models' performance.

## Claims

| Line | Claim | Verdict | Truth / evidence |
|---|---|---|---|
| 4 | Sex vs Survived: χ² 260.72, p < 0.001, Cramér's V 0.54, large effect | ✅ | Yates-corrected χ² (scipy default); V = 0.541 |
| 5 | Pclass: χ² 102.89, p < 0.001, an advantage for first class over third | ⚠️ | Test correct; survival by class was never computed in this run (true: 63.0% vs 24.2%) |
| 6 | Random Forest accuracy 83.80%, F1 77.17%; survival rate 38.38% | ✅ | `ml_2.rf_metrics`, `eda_1.survived_proportions` |
| 7 | Dropping Cabin and stratified Age imputation "resulted in a clean feature set that maximized model performance" | ❌ | The models (`ml_2`) were trained on a different, rebuilt feature set with one-hot `Name` and `Ticket` (1,294 columns); no comparison was made |
| 13 | Cabin 687 and Age 177 missing | ✅ | |
| 30 | "Total Execution Time: 81.7 seconds" | ➖ | Code time only; the run took 45 minutes |
| 35 | 38.38% survived (342 of 891), 61.62% did not (549) | ✅ | |
| 35 | "Inherently imbalanced" | ➖ | 1.6 : 1 |
| 37 | Cabin 687 missing (~77%), values fragmented with no dominant category | ✅ | Top value occurs 4 times |
| 38 | Missing Age "heavily concentrated in Third Class males (136 out of 157 missing ages)" | ❌ | 136 is all of 3rd class, out of 177 missing; 3rd-class males account for 94 |
| 38 | Age records "less meticulously kept for lower socioeconomic groups" | ⚠️ | Speculation |
| 39 | Median age 28.0, mean 29.7 | ✅ | |
| 48–49 | Pclass χ² 102.89, p 4.55 × 10⁻²³ | ✅ | |
| 50 | Pclass Cramér's V 0.24, "moderate" | ❌ | True V = 0.340. The code divided by 2 instead of min(rows, cols) − 1 = 1. Earlier attempts also left wrong values in the fact table (`sex_cramers_v = 0`, `pclass_cramers_v = 7.17`). |
| 53 | Mean age 28.34 (survived) vs 30.63 (died) | ✅ | |
| 54–56 | t = −2.07, p = 0.039, Cohen's d = −0.16 | ✅ | Student's t; Welch's test gives p = 0.041 |
| 57 | 95% CI of the difference [−4.25, −0.31] | ✅ | |
| 62–66 | RF accuracy 83.80%, precision 84.48%, recall 71.01%, F1 77.17%, AUC 0.847 | ✅ | `ml_2.rf_metrics` |
| 68–72 | LR accuracy 82.68%, precision 82.76%, recall 69.57%, F1 75.59%, AUC 0.855 | ✅ | `ml_2.log_reg_metrics` |
| 73 | Feature importance: Sex > Pclass > Age > Fare / Embarked | ⚠️ | No importances were computed |
| 73 | RF captures interactions "e.g. young females in first class" | ⚠️ | Not analyzed |
| 76 | "Women and children first" is statistically validated | ⚠️ | Children were not analyzed |
| 79 | Class "acted as a proxy for access to lifeboats" | ⚠️ | Historical narrative, not from the data |
| 79 | The imputation "recovered predictive signal without biasing the model" | ⚠️ | Never tested |
| 85 | Embarked was not tested | ✅ | Honest limitation |
| 97 | Optimize thresholds to "maximize lives saved" | ❌ | Meaningless for a historical dataset |

## Baseline findings that are still absent

| Finding | This run |
|---|---|
| Survival by sex (74.2% vs 18.9%) | Not computed; only shown as counts in a chart |
| Survival by class (63 / 47 / 24%) | Not computed; counts in a chart |
| Fare by outcome | Not computed (Fare was dropped from the t-test task) |
| Survival with / without a cabin record | Not computed |
| Survival with missing Age | Not computed |
| RF feature importances | Not computed |
| Precision / recall / F1 | ✅ Present |

## Observations for the next steps

| Observation | Step |
|---|---|
| `NameError: plt` / `pd` cost steps in 2 tasks (the setup cell only imports the helpers) | P1.3 |
| Charts are usable but sloppy: "Survival Rate" titles on count plots, wrong n labels, overlapping labels | P1.3 |
| `ml_1` didn't publish its feature set despite the rule; `ml_2` tried `load("ml_1/train_test")`, failed, and rebuilt it differently | P1.4 (briefs name the expected outputs) |
| No check of the specialists' work: wrong Cramér's V, one-hot `Name`/`Ticket`, superseded wrong facts left in the table | P1.4 (review + sanity checks), P1.5 (number check) |
| Coverage: the plan never asks for group survival rates or importances; specialists' follow-ups (Embarked, interactions) go nowhere | P1.4 (planning + follow-ups) |
