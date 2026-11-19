# Outcome Analysis of an 800-Row Dataset: Binary Target `outcome`

## Summary

- **No group or numeric-feature association with outcome survives testing.** The outcome rate falls from 46.2% in g1 to 36.8% in g4, but the chi-square test gives p = 0.289 (Cramér's V = 0.068). For each numeric feature, Holm-adjusted Mann-Whitney p-values are 1.0 across six tests. The largest effects (feat_3 rank-biserial -0.056, feat_5 0.052) have confidence intervals that include 0.
- **No feature-by-group interaction survives correction.** The smallest raw overall p-value is feat_3 (p = 0.029), which has a Holm-adjusted p of 0.147. The single nominal term, feat_3 for g2 versus g1 (raw p = 0.049), has a Holm-adjusted p of 0.741 across 15 terms.
- **Predictive models do not beat the majority-class baseline.** On one 80/20 split, logistic regression reached 55.0% test accuracy against 58.75% for the baseline, with test AUC 0.392. Gradient boosting reached 53.1%. Over 25 repeated stratified CV folds, logistic regression averaged 57.2% accuracy (baseline 58.9%) and AUC 0.505. Gradient boosting averaged 52.7% accuracy and AUC 0.465.
- **The below-0.5 AUC from the single split did not persist.** Across CV folds, logistic AUC averaged 0.505 (SD 0.039), with 44% of folds below 0.5. Neither model beat a constant class-prior predictor on log loss (0.677 for the prior, 0.684 for logistic, 0.754 for gradient boosting).

## Data

- **Size:** 800 rows, 7 columns.
- **Target:** `outcome`, binary. 471 rows are class 0 (58.9%) and 329 are class 1 (41.1%).
- **Features:** five numeric features (feat_1 to feat_5) and one categorical feature, `group`. The results report four levels (g1: 182 rows, g2: 206, g3: 200, g4: 212). The analysis brief described three levels (g1, g2, g3). The results use four, so this report does too.
- **Missing values:** none in any of the 7 columns.
- **Date, id, or free-text columns:** none.

## Findings

### Outcome rate and group

- The overall outcome rate is 41.1%.
- Outcome rate by group: g1 46.2% (84 of 182), g2 42.2% (87 of 206), g3 40.0% (80 of 200), g4 36.8% (78 of 212).
- The chi-square test of outcome by group gives χ² = 3.75, df = 3, p = 0.289. Cramér's V is 0.068, a negligible association. After Holm adjustment across the six tests in stat_1, p = 1.0. The rate differences are consistent with chance at n = 800.

![Outcome rate by group, with the overall rate as a dashed line](tasks/eda_1/charts/outcome_rate_by_group.png)

- Feature means differ by group in the descriptive table:
  - feat_4 is highest in g3 (0.204) and lowest in g1 (-0.059).
  - feat_1 is highest in g4 (0.121) and lowest in g3 (-0.070).
  - feat_3 is highest in g4 (0.123).
  - feat_5 is highest in g3 (0.125).
- Kruskal-Wallis tests across groups, with Holm correction over five features, find no significant difference for any feature:

| Feature | H (df = 3) | Raw p | Holm p | ε² (95% bootstrap CI) |
|---|---|---|---|---|
| feat_1 | 3.97 | 0.265 | 1.0 | 0.001 (-0.003 to 0.019) |
| feat_2 | 0.31 | 0.957 | 1.0 | -0.003 (-0.003 to 0.009) |
| feat_3 | 2.35 | 0.503 | 1.0 | -0.001 (-0.003 to 0.015) |
| feat_4 | 5.88 | 0.118 | 0.588 | 0.004 (-0.002 to 0.025) |
| feat_5 | 3.05 | 0.383 | 1.0 | 0.000 (-0.003 to 0.016) |

- Group explains almost none of the rank variation in any feature. Per-group effect sizes and pairwise comparisons were not computed.

![Epsilon-squared effect of group on each numeric feature, with bootstrap 95% CI. Values near 0 mean group explains almost none of the rank variation.](tasks/stat_3/charts/stat3_eps2_by_feature.png)

### Outcome rate across quartiles of each numeric feature

Quartiles contain about 200 rows each (feat_4: 201, 199, 200, 200). Outcome rate by quartile, Q1 to Q4:

| Feature | Q1 | Q2 | Q3 | Q4 | Spread (max − min) |
|---|---|---|---|---|---|
| feat_1 | 44.0% | 39.5% | 38.5% | 42.5% | 0.055 (U-shape) |
| feat_2 | 39.5% | 43.5% | 41.5% | 40.0% | 0.040 (no clear pattern) |
| feat_3 | 42.5% | 43.5% | 44.0% | 34.5% | 0.095 (peaks in Q3, drops in Q4) |
| feat_4 | 39.8% | 42.2% | 44.0% | 38.5% | 0.055 (inverted-U) |
| feat_5 | 38.5% | 40.0% | 43.5% | 42.5% | 0.050 (closest to monotone, slight dip in Q4) |

- Ranked by spread: feat_3 (0.095), feat_1 (0.055), feat_4 (0.055), feat_5 (0.050), feat_2 (0.040).
- No feature has a strictly monotone pattern. The standard error of a quartile rate is roughly 0.035, so these spreads are not shown to exceed chance. No trend test was run in this task.

![Outcome rate by quartile of feat_1 to feat_5, dashed line = overall outcome rate](tasks/eda_2/charts/quartile_outcome_rate.png)

### Feature associations with outcome

- Mann-Whitney U tests compare each feature between outcome 1 and outcome 0. No feature is significant after correction. Holm-adjusted p is 1.0 across the six tests in stat_1.

| Feature | Raw p | Rank-biserial | 95% CI (approx.) |
|---|---|---|---|
| feat_1 | 0.740 | -0.014 | -0.095 to 0.067 |
| feat_2 | 0.978 | 0.001 | -0.080 to 0.083 |
| feat_3 | 0.179 | -0.056 | -0.137 to 0.025 |
| feat_4 | 0.864 | 0.007 | -0.074 to 0.088 |
| feat_5 | 0.210 | 0.052 | -0.029 to 0.133 |

- The largest effects are small. The feat_3 and feat_5 intervals include 0. The other features have |rank-biserial| of 0.014 or less. The intervals are approximate (Hanley-McNeil based).
- Holm correction over five features only (the family used in stat_3) gives adjusted p-values of 0.897 for feat_3 and feat_5 and 1.0 for the other three. The two correction families therefore give different adjusted values, but no feature is significant under either.
- Adjusting for group (logistic regression, stat_3) leaves every association non-significant:

| Feature | Unadjusted coefficient (p) | Group-adjusted coefficient (p) |
|---|---|---|
| feat_1 | -0.0131 (0.853) | -0.0069 (0.922) |
| feat_2 | 0.0168 (0.814) | 0.0159 (0.824) |
| feat_3 | -0.0833 (0.250) | -0.0793 (0.275) |
| feat_4 | -0.0050 (0.945) | +0.0015 (0.984) |
| feat_5 | 0.0896 (0.209) | 0.0961 (0.180) |

- Group adjustment changes the feat_4 coefficient from negative to positive, at a magnitude near zero in both models. The feat_4 sign is therefore unstable across the two models. The direction of the other four features agrees with stat_1.

### Feature-by-group interaction

- Likelihood-ratio tests for feature-by-group interaction (3 df each):

| Feature | LR | Raw p | Holm p (5 features) |
|---|---|---|---|
| feat_1 | 0.95 | 0.813 | 1.0 |
| feat_2 | 6.29 | 0.098 | 0.394 |
| feat_3 | 8.99 | 0.029 | 0.147 |
| feat_4 | 1.30 | 0.729 | 1.0 |
| feat_5 | 3.48 | 0.323 | 0.968 |

- feat_3 is the strongest candidate for a group-dependent effect, but it does not survive correction across five features.
- feat_3 interaction terms against g1 (log-odds per unit of feat_3):
  - g2: coefficient -0.418 (95% CI -0.835 to -0.001), raw p = 0.049, Holm p = 0.741 across 15 terms.
  - g3: coefficient -0.127 (95% CI -0.539 to 0.285), raw p = 0.546.
  - g4: coefficient 0.178 (95% CI -0.240 to 0.596), raw p = 0.403.
- Per-group odds ratios for feat_3, each fitted within its group: g1 1.02 (95% CI 0.75 to 1.38, p = 0.896); g2 0.67 (0.50 to 0.90, p = 0.007); g3 0.90 (0.68 to 1.19, p = 0.456); g4 1.22 (0.91 to 1.63, p = 0.178). The g2 interval excludes 1, but the intervals overlap and the interaction is not significant after correction. The analysis treats this difference as exploratory.
- No term among the 15 feature-by-group interaction terms is significant after Holm correction.

### Predictive models on a single 80/20 split

- The split is stratified, with 640 training and 160 test rows, seed 42. The majority-class baseline (class 0) reaches 58.75% test accuracy.
- Logistic regression (standardized, feat_1 to feat_5 plus group dummies): test accuracy 55.0%, precision 0.31, recall 0.08, ROC AUC 0.392, log loss 0.709. Training accuracy was 58.6%.
- Gradient boosting: test accuracy 53.1%, precision 0.40, recall 0.27, ROC AUC 0.467, log loss 0.754. Training accuracy was 83.6%, a gap of 0.30 from test.
- Permutation importance (logistic, drop in test ROC AUC over 30 repeats):
  - feat_3: +0.023 (SD 0.008), the largest drop.
  - feat_2: +0.005 (SD 0.009).
  - feat_4: -0.009 (SD 0.009). feat_1: -0.017 (SD 0.012). feat_5: -0.037 (SD 0.030).
  - Group dummies shuffled jointly: -0.076 (SD 0.030).
  - Negative values mean AUC rose when the feature was shuffled. The ranking is therefore unreliable.
- Permutation importance (gradient boosting) gives small values relative to their SDs: feat_3 0.016 (SD 0.034), feat_4 0.011 (SD 0.019), feat_2 0.007 (SD 0.020). feat_1 (-0.008) and feat_5 (-0.009) are negative. Group values are near zero. No feature shows a reliable effect.

![Permutation importance of each feature for the logistic regression model: drop in test ROC AUC when the feature is shuffled, mean and SD over 30 repeats](tasks/ml_1/charts/ml_1_permutation_importance.png)

### Predictive models under repeated stratified cross-validation

Repeated stratified 5×5 CV (25 folds):

| Model | Accuracy (mean ± SD) | Accuracy vs baseline | Folds beating baseline | ROC AUC (mean ± SD) | Log loss (mean ± SD) |
|---|---|---|---|---|---|
| Majority baseline | 58.9% ± 0.3 pts | — | — | 0.500 ± 0.000 | 14.82 ± 0.09 (artifact of hard 0/1 probabilities) |
| Logistic regression | 57.2% ± 1.9 pts | 1.7 pts below on average | 3 of 25 | 0.505 ± 0.039 | 0.684 ± 0.008 |
| Gradient boosting | 52.7% ± 2.8 pts | 6.2 pts below on average | 0 of 25 | 0.465 ± 0.041 | 0.754 ± 0.021 |
| Constant class-prior predictor | — | — | — | — | 0.677 ± 0.001 |

- Logistic AUC is below 0.5 in 44% of folds (11 of 25). The task reports that the single-split logistic AUC of 0.392 was split-specific variation around chance. The CV results do not show a stable AUC below 0.5.
- Neither model improves on the constant class-prior predictor in log loss.

![Per-fold test accuracy of the majority baseline, logistic regression and gradient boosting over 25 CV folds](tasks/ml_2/charts/ml_2_cv_accuracy.png)

## Limitations

- **Sample size and power.** With 800 rows, the tests can detect only fairly large effects. The minimum detectable effect size was not computed. Three-degree-of-freedom interaction tests have low power. The analysis did not establish whether feat_3 or feat_5 needs a larger sample.
- **Approximate intervals.** The Mann-Whitney confidence intervals are approximate (Hanley-McNeil based) and should be read with caution.
- **Quartile spreads.** Quartile outcome rates have a standard error of roughly 0.035. The spreads, including feat_3's 0.095, are not shown to exceed chance. No trend test was run.
- **Model evaluation.** The single 160-row test split is very noisy. Its permutation importance rankings are unreliable, as the findings state. The CV results are more stable but still show wide SDs.
- **No significant findings.** No association, group difference, or interaction is significant after correction. All model results are below the majority-class baseline or indistinguishable from it.
- **Group levels.** The analysis brief described three group levels (g1, g2, g3). The results include four (g1 to g4). This report follows the results.
- **Discrepancy in the EDA text.** The eda_1 finding says feat_3 is lowest in g2 (-0.009). Its own means table gives g3 as lowest (-0.051). This report uses the table values.
- **Correction families differ.** stat_1 applies Holm across six tests, including the chi-square test. stat_3 applies Holm across five features. The adjusted values for feat_3 and feat_5 are therefore 1.0 in stat_1 and 0.897 in stat_3. Both are reported above.
- **Unresolved review issue (stat_3, direction of agreement).** The stat_3 finding's statement that "direction agrees with stat_1 for every feature" is inaccurate. The unadjusted logistic coefficient for feat_4 is negative (-0.0050), while the stat_1 rank-biserial for feat_4 is positive (+0.007). Direction agrees for feat_1, feat_2, feat_3 and feat_5 only. The group-adjusted feat_4 coefficient is positive (+0.0015). The feat_4 sign is therefore unstable across the two models, and it is near zero in both. This objection affects the feat_4 direction statement in the adjusted-association findings above.
- **Failed tasks.** None. All tasks completed.

## Open questions

- Is the quartile trend in outcome rate significant for each feature, for example under a chi-square test for trend or a logistic regression on the continuous feature?
- Do the features stay associated with outcome after controlling for group and for each other, in a multivariable logistic regression?
- Is feat_3's Q4 drop (34.5%) a real effect or noise, and does it hold in a held-out split?
- Does feat_3's effect differ for g2 in a larger sample, or is the nominal interaction (raw p = 0.029 overall, 0.049 for the g2 term) a chance result from testing five features?
- Is the feat_2 interaction (raw p = 0.098) worth a larger-sample check?
- Does feat_4 differ between specific group pairs (for example g3 against the others), and does that survive correction across the pairwise comparisons?
- What is the minimum effect size these tests can detect at n = 800, and do feat_3 and feat_5 warrant a larger sample?
- Do repeated CV or a larger sample give a more reliable estimate of predictive skill than the single 160-row test split?
- Does logistic regression on group alone match the prior baseline in repeated CV?
- Do a regularized or shallower gradient boosting model reduce its below-chance AUC and accuracy gap?
- Does any feature subset give CV AUC reliably above 0.5?