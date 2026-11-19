# Baseline report: claim-by-claim check

Report: [run/report.md](run/report.md) · run `20261031-204254_titanic_qwen3.5-9b` · commit `03d2f98` (tag `v0.1.0-baseline`) · model `qwen3.5:9b`, 6 tasks.
True values computed directly from `data/titanic.csv` with pandas/scipy.

**Legend:** ✅ correct · ❌ wrong · ⚠️ unsupported (not computed in this run) · ➖ misleading or incomplete

## Summary

| Verdict | Count |
|---|---|
| ✅ Correct | 15 |
| ❌ Wrong | 7 |
| ⚠️ Unsupported | 6 |
| ➖ Misleading / incomplete | 6 |

- **Every specific number in the report matches the data.** Unlike the [legacy report](legacy_report_titanic.md) ("61.62% survived"), no number was invented.
- **The errors are interpretation errors.** The report calls overfitting healthy, ranks feature importance from guesses, and makes up a mechanism for the port effect.
- **Others come from context loss.** Results that were computed never reached the writer, so it guessed or wrote "N/A".
- **Several headline findings computed in the run are missing entirely** (see the end of this file).

## Claims

| Line | Claim | Verdict | Truth / evidence |
|---|---|---|---|
| 4 | Sex vs Survived χ² = 263.05, p < 0.0001 | ✅ | Uncorrected χ². Scipy's default for 2×2 tables (Yates-corrected) gives 260.72; the report doesn't say which. |
| 4 | Pclass and Embarked are "critical determinants" | ✅ | Both significant, but Embarked is weak (Cramér's V = 0.17). "Critical" overstates it. |
| 5 | ~81–82% test accuracy | ✅ | Three separate RF fits: 81.01%, 82.68%, 82.12% |
| 5 | "Strong generalization" | ❌ | Train 98% vs test 82%: a textbook overfitting gap (unlimited-depth RF) |
| 6 | Cabin 77.10% missing | ✅ | 687 / 891 |
| 7 | RF ~82%, LR ~80.5% | ✅ | LR test 80.45% |
| 7 | Relationships are "largely linear or monotonic" | ⚠️ | Speculation from a 2-point accuracy difference |
| 7 | Trees capture the "Child + Female" interaction | ⚠️ | No interaction was analyzed |
| 13 | "7 numeric (Age, Fare, …) and 5 categorical (Sex, Pclass, Embarked, Cabin, Ticket)" | ❌ | Categorical are Name, Sex, Ticket, Cabin, Embarked; Pclass was profiled as numeric. The 7 "numeric features" include `PassengerId` and the target itself. |
| 14 | Survival rate 38.38% (342 of 891) | ✅ | |
| 20 | "Visualized distributions" | ❌ | No plots were made; the EDA prompt forbids them |
| 21 | Chi-square tests for Sex, Pclass, Embarked | ✅ | |
| 31 | "Total Execution Time: 9.0 seconds" | ➖ | Sum of code execution only; the run took 25 minutes |
| 36 | 61.62% died (549) vs 38.38% survived (342) | ✅ | |
| 36 | "The dataset is imbalanced" | ➖ | 1.6 : 1. The profiler's own rule (> 2 : 1) says not imbalanced. |
| 38 | Age: 177 missing (19.87%), mean 29.70, median 28.00 | ✅ | |
| 39 | Cabin: 687 missing, 147 unique values | ✅ | |
| 39 | Lower-class passengers likely lacked cabins | ⚠️ | Not computed. True: Cabin missing for 97.6% of 3rd class vs 18.5% of 1st. |
| 47 | Sex: χ² 263.05, V 0.543 | ✅ | |
| 48 | Pclass: χ² 102.89, V 0.340 | ✅ | |
| 49 | Embarked: χ² "N/A", V "N/A" | ➖ | Computed in `stat_1` (χ² 26.49, V 0.173) but cut off before reaching the writer |
| 55 | RF train accuracy ~98% | ✅ | 98.17% / 97.89% |
| 56 | RF test accuracy "81.0–82.1%" | ➖ | Range leaves out the 82.68% fit; the three fits used different preprocessing and splits |
| 59–60 | LR train 80.2%, test 80.45% | ✅ | |
| 63–67 | Feature importance: Sex > Pclass > Embarked > Age ("inferred") | ❌ | Computed RF importances: Fare 0.27–0.28, Sex 0.26–0.27, Age 0.25, Pclass 0.09, Embarked 0.03 (lowest). Fare is missing entirely. The real values were computed three times but never reached the writer. |
| 71 | Female + 1st class has the highest survival | ⚠️ | Not computed. True: 96.8% |
| 72 | Cherbourg and Southampton had distinct survival rates | ⚠️ | Computed in `eda_1` (55.4% vs 33.7%) but not shown to the writer; right by luck |
| 72 | Due to "proximity to the sinking location relative to embarkation points" | ❌ | Nonsense: everyone was on the same ship when it sank |
| 73 | The 98% → 82% gap "is healthy … learning genuine patterns rather than memorizing" | ❌ | The opposite: this is memorization |
| 78 | Class matters "independent of gender to some extent" | ⚠️ | No stratified analysis. True in the data: 1st vs 3rd class survival is 96.8% vs 50.0% (women), 36.9% vs 13.5% (men). |
| 84 | "The large gap … warrants caution" | ➖ | Contradicts line 73 |
| 85 | Precision/recall "were truncated in the initial synthesis" | ✅ | Accurate: classification reports were computed in `ml_1`–`ml_3` and cut off. The report noticed its own context loss. |
| 92 | Median imputation "to minimize skew from outliers, as the distribution is relatively symmetric" | ➖ | The reasoning contradicts itself |
| 97 | Optimize the threshold for the "saving lives" objective | ❌ | Meaningless for a historical dataset |

## Computed in the run but missing from the report

These are the strongest findings of the analysis. The code computed all of them correctly, and none reached the report:

| Finding | Value | Computed in |
|---|---|---|
| Survival by sex | female 74.2%, male 18.9% | `eda_1` |
| Survival by class | 1st 63.0%, 2nd 47.3%, 3rd 24.2% | `eda_1` |
| Fare by outcome | mean 48.40 (survived) vs 22.12 (died) | `eda_1` |
| Survival with / without a cabin record | 66.7% vs 30.0% | `eda_2` |
| Survival with missing Age | 29.4% (52 of 177) vs 40.6% | `eda_2` (as counts) |
| RF feature importances | Fare, Sex, Age ≫ Pclass > SibSp > Parch > Embarked | `ml_1`, `ml_2`, `ml_3` |
| Precision / recall / F1 | e.g. RF survived-class recall 0.71–0.74 | `ml_1`, `ml_2`, `ml_3` |
