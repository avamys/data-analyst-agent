# P1.4 reference run: claim-by-claim check

Report: [report.md](report.md) · run `20261101-192628_titanic_qwen3.5-9b` · commit `3040863` · 6 tasks, 120 min, 58 LLM calls, 12 charts saved (none in the report yet: P1.5).
Method as in the [baseline annotations](../../baseline/annotations.md).

**Legend:** ✅ correct · ❌ wrong · ⚠️ unsupported (not computed in this run) · ➖ misleading or incomplete

## Summary

| | Baseline | P1.2 | P1.3 | P1.4 |
|---|---|---|---|---|
| ✅ Correct | 15 | 14 | 14 | 14 |
| ❌ Wrong | 7 | 4 | 3 | 5 |
| ⚠️ Unsupported | 6 | 7 | 7 | 6 |
| ➖ Misleading | 6 | 2 | 3 | 2 |
| Baseline findings still absent | 7 | 6 | 5 | 2 |
| Charts | 0 | 6 | 9 | 12 |

- **Better:**
  - **Coverage:** 5 of the 7 baseline findings are back. They include survival by sex, a trained model with precision, recall, F1 and AUC against the majority baseline, and a feature ranking.
  - **Reviews caught real calculation errors.** Two were caught and fixed:
    - `stat_1` used the wrong Cramér's V formula (V = 16.1). After revision all three V values are right (0.541, 0.340, 0.173).
    - `ml_1` kept `Pclass` next to its own dummies.
  - **No wrong statistic comes from a lost or truncated number.** All 5 wrong claims are method errors or interpretations.
- **Worse:**
  - **More wrong claims (3 → 5).** This report makes more claims, because a model was trained this time. The two biggest errors are method errors that the review missed:
    - **Age "not significant", p = 0.058:** the t-test ran after missing ages were filled with the median, which shrinks the difference. On the recorded ages the result is p = 0.039 (Student's t) or p = 0.041 (Welch's). The report builds an "Age paradox" on it, in 4 places.
    - **"Fare is surprisingly weak … multicollinearity":** the ranking compares raw coefficients on unscaled features. Fare's coefficient is per pound (0–512) and Age's per year, so the ranking compares units, not importance.
  - **Time: 120 min**, against 54 for P1.3. Specialists took 76 min, reviews 28 min, and 4 of the 6 tasks were revised.
- **The hand-off wasn't tested.** The plan gave every task `depends_on: [""]`, so no task depended on another and no outputs were required. `ml_2` rebuilt its own features, with `Pclass` as a number, instead of loading ml_1's one-hot table.
- **No follow-ups were added** (0 of the 2 allowed). The Sex × Pclass interaction, the biggest open question, appears only in the report's "Future analysis".

## Claims

| Line | Claim | Verdict | Truth / evidence |
|---|---|---|---|
| 5 | Female 74.2% vs male 18.9%, Cramér's V = 0.541 | ✅ | `eda_1.survival_sex_*`, `stat_1.final_sex_effect_size` |
| 6 | Mean fare $48.40 (survived) vs $22.12 (died); first class correlates with survival | ✅ | `eda_2.fare_mean_*`, `eda_1.survival_pclass_*` |
| 6 | "The model identifies socioeconomic status as the primary proxy" | ❌ | The model's top feature is `Sex_male` (2.59, against 0.94 for `Pclass`) |
| 6, 98 | Wealth was the "primary proxy for access to lifeboats" | ⚠️ | Speculation |
| 7 | Cherbourg 55.36% vs Southampton 33.70% | ✅ | `eda_1.survival_embarked_*` |
| 7 | "Suggesting demographic differences in boarding groups" | ⚠️ | Not computed |
| 8, 83 | 81.0% test accuracy vs a 58.7% majority-class baseline | ✅ | `ml_2.logistic_regression_corrected` |
| 9, 72, 106, 126 | Age "not statistically significant" (p = 0.058) | ❌ | The test ran on median-imputed ages. On recorded ages: p = 0.039 (Student) / 0.041 (Welch). Limitations (126) blames sample "power". |
| 9 | Class and gender "outweighed individual age" | ⚠️ | No model or test compares them |
| 19–20 | Numeric features include Embarked; categorical are Sex and Pclass | ❌ | Swapped: the profile has Pclass as numeric and Embarked as categorical |
| 36–37 | 6 tasks, 6 completed | ✅ | |
| 50–52 | Missing Age 19.87% (177), Cabin 77.10% (687), Embarked 0.22% (2) | ✅ | |
| 51 | Cabin missing 97.56% in 3rd class vs 18.52% in 1st | ✅ | `eda_3.cabin_missing_rate_by_pclass` |
| 55 | Survival 38.38% (342 of 891) | ✅ | |
| 56–58 | Survival by sex, class and port | ✅ | |
| 62 | Mean age 28.34 (survived) vs 30.63 (died) | ✅ | `eda_2.age_mean_*`, recorded ages |
| 68–71 | p-values and effect sizes for Sex, Pclass, Fare, Embarked | ✅ | χ² p = 1.20 × 10⁻⁵⁸ / 4.55 × 10⁻²³ / 1.77 × 10⁻⁶; Welch p = 2.70 × 10⁻¹¹; d = 0.505 (average-variance form; pooled d = 0.547) |
| 69, 71 | Pclass V = 0.34 a "large" effect, Embarked V = 0.17 "medium" | ❌ | With 2 degrees of freedom, Cohen's thresholds are 0.07 / 0.21 / 0.35: medium and small |
| 76 | "Logistic Regression with One-Hot Encoding" | ➖ | `Pclass` entered as the number 1–3; ml_1's encoded table wasn't used |
| 78–82 | Accuracy 81.0%, precision 78.6%, recall 74.3%, F1 76.4%, AUC 0.882 | ✅ | `ml_2.logistic_regression_corrected` |
| 85–91 | Ranking by absolute coefficient: Sex_male, Pclass, Embarked_S, SibSp, … | ✅ | As computed, but see the next row |
| 92, 107, 116, 127 | Fare "surprisingly weak … likely due to multicollinearity" | ❌ | The features were not scaled. Fare's coefficient is per pound, so its rank reflects units. Multicollinearity was never checked. |
| 101 | "Women and Children First" is "statistically robust" | ⚠️ | Children were never analysed |
| 103 | Missing Cabin marks lower class | ✅ | `eda_3.cabin_missing_rate_by_pclass` |
| 106 | "Children survived at high rates" | ⚠️ | Not computed (true: 59% under 16) |
| 113, 119 | "Not a matter of chance"; the model is "validating the historical understanding" | ➖ | Overclaims from one model at 81% accuracy |
| 135 | Fare "adds little incremental value if Pclass is already included" | ⚠️ | Never tested |

## Baseline findings that are still absent

| Finding | This run |
|---|---|
| Survival by sex (74.2% vs 18.9%) | ✅ Present |
| Survival by class (63 / 47 / 24%) | ✅ Present |
| Fare by outcome | ✅ Present |
| Survival with / without a cabin record | Not in the report. `eda_3` computed the reverse: 87.6% of those who died had no cabin record, against 60.2% of survivors. |
| Survival with missing Age | Not computed |
| Feature importances | ✅ Present (logistic coefficients; invalid as a ranking, see above) |
| Precision / recall / F1 | ✅ Present |

## The lead's reviews

| Task | Verdicts | What the review did |
|---|---|---|
| eda_1 | accept | |
| eda_2 | accept | |
| stat_1 | revise → accept | ✅ Caught the wrong Cramér's V formula. ❌ Missed the Age t-test on imputed data. The wrong first-attempt facts (`cramers_v_sex = 16.1`) stay in the fact table. |
| ml_1 | revise → accept | ✅ Caught `Pclass` kept next to its dummies (perfect multicollinearity) |
| ml_2 | revise → accept | ✅ Caught that the code didn't match ml_1's accepted one-hot description. ❌ Missed the unscaled coefficient ranking. |
| eda_3 | revise → revise (unresolved) | ✅ Caught a fare group lost by `.dropna()`. The "quartiles" are equal-width bins (`pd.cut`), which nobody noticed; they aren't in the report. |

- **The fixes from the second run held.** No review introduced an error: no made-up numbers, and the baseline was read correctly. Every send-back named a real problem.
- **The reviews check whether code and report agree, not whether the method is right.** Both misses look correct on the surface: a t-test on a column with no missing values, and coefficients ranked by size.

## Two runs that failed first

| Run | Failure | Fix (commit) |
|---|---|---|
| `20261101-171551` | Planning, after 2 min: qwen3.5 left every brief id empty and named outputs in `depends_on` | Ids assigned in code; dependencies resolve by id or output name (`537b9bb`) |
| `20261101-172109` | During task 6 of 8, after 119 min: "No data received from Ollama stream" was not retried | Retried (`3040863`). That run also showed reviews introducing errors:<ul><li>made-up per-class rates</li><li>the plan's "mean survival rate" taken as the baseline accuracy</li></ul>Other problems, also fixed in `3040863`:<ul><li>the lead re-read its own earlier objection</li><li>the fact cap cut off model scores</li><li>both follow-ups copied planned tasks</li></ul> |

## Observations for the next steps

| Observation | Step |
|---|---|
| A t-test on imputed values, and coefficients of unscaled features ranked as importances | Sanity checks, like the train/test gap: imputation before a test, `abs_coefficient` ranking without scaling. Or have `record_model` rank by permutation importance. |
| Stale facts from failed first attempts (`cramers_v_sex = 16.1`, `*_corrected` duplicates) stay in the fact table that the writer reads | P1.5: the writer works from the cited facts only |
| The writer interprets beyond the findings (lifeboats, children, multicollinearity) | P1.5: the lead writes from accepted findings, plus the number check |
| `depends_on: [""]`: no hand-off, so ml_2 rebuilt the features | Make the dependency of ML tasks on the feature-preparation task explicit in code, or merge preparation into the modelling brief |
| 120 min per run, 4 of 6 tasks revised | Watch it. If it stays this long, cap revision steps below the first attempt's budget. |
