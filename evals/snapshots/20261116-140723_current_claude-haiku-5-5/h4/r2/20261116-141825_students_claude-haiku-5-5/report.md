# Predicting Score Gain: Analysis of 1,000 Students (Target: score_gain)

## Summary

- **extra_sessions has the largest raw association with score_gain, but it does not hold after adjustment.** Students with 1 extra session averaged 7.32 versus -2.44 for those with 0, a difference of 9.76 (95% CI 8.17 to 11.34, p = 5.7e-29). In a multiple regression that also includes pre_score and attendance_pct, the extra_sessions coefficient falls to 1.76 (95% CI -0.30 to 3.81, p = 0.093).
- **pre_score is the strongest correlate and the main predictor.** Its correlation with score_gain is r = -0.46 (95% CI -0.51 to -0.41). In the adjusted regression its coefficient is -0.346. Without pre_score, the linear model's test R² falls from 0.18 to 0.07.
- **attendance_pct has a small-to-medium positive association.** Its correlation with score_gain is r = 0.29, and it remains significant in the adjusted regression (coefficient 0.213). It ranks second in permutation importance.
- **No interaction was detected.** The extra_sessions × attendance_pct (p = 0.70) and extra_sessions × pre_score (p = 0.79) terms are non-significant.
- **Predictive power is modest.** On a single 200-row test set, linear regression reduces RMSE from 10.62 (mean baseline) to 9.58 (test R² 0.18). Gradient boosting performs worse than linear regression (RMSE 10.03, test R² 0.10).

## Data

- **Size:** 1,000 rows and 6 columns (one target, five numeric features).
- **Target:** score_gain, a numeric regression target.
- **Features:** pre_score, extra_sessions, attendance_pct, age and class_size, all numeric. There are no categorical, date/time, id or free-text columns.
- **Missing values:** none in any of the six columns.

## Findings

### 1. Distribution of score_gain

score_gain is roughly centred and symmetric. The mean is -0.003, the median is -0.3 and the standard deviation is 11.48. The minimum is -33.8, the maximum is 40.9 and the skew is 0.11. The 30-bin histogram is unimodal. The most populated bin spans 1.06 to 3.55 and contains 89 students, and counts fall off on both sides.

![Histogram of score_gain across 1000 students](tasks/eda_1/charts/score_gain_hist.png)

### 2. Associations with score_gain and between features (eda_1)

Pearson correlations with score_gain:

| Feature | r |
|---|---|
| pre_score | -0.46 |
| extra_sessions | 0.37 |
| attendance_pct | 0.29 |
| age | 0.02 |
| class_size | -0.02 |

Average score_gain is -2.44 for students with extra_sessions = 0 and 7.32 for students with extra_sessions = 1.

Among the five features, only pre_score and extra_sessions are strongly correlated (r = -0.736). All other pairs are weak. The largest of these is age with class_size (r = -0.052), which is the only other pair with |r| above 0.05.

### 3. Significance and effect sizes (stat_1)

- **extra_sessions (group comparison, Welch t-test):** 1 extra session (n = 250) versus 0 (n = 750) gives a difference of 9.76 (95% CI 8.17 to 11.34), t = 12.10, p = 5.7e-29, Cohen's d = 0.91. The result survives Holm correction (adjusted p = 2.3e-28 across the family that includes the correlations).
- **pre_score:** r = -0.46 (95% CI -0.51 to -0.41), p = 5.2e-54, Holm-adjusted p = 2.6e-53. This is a medium-to-large effect that survives correction.
- **extra_sessions (correlation):** r = 0.37 (95% CI 0.31 to 0.42), p = 1.8e-33, Holm-adjusted p = 7.2e-33. This is consistent with the group comparison.
- **attendance_pct:** r = 0.29 (95% CI 0.23 to 0.35), p = 5.9e-21, Holm-adjusted p = 1.8e-20. This survives correction.
- **age:** r = 0.02 (95% CI -0.04 to 0.08), p = 0.51, Holm-adjusted p = 1.0. Not significant.
- **class_size:** r = -0.02 (95% CI -0.08 to 0.05), p = 0.62, Holm-adjusted p = 1.0. Not significant.

### 4. Interactions (stat_2)

Using an OLS model on all 1,000 rows with attendance_pct and pre_score centred:

- **extra_sessions × attendance_pct:** coefficient -0.019 (SE 0.049, 95% CI -0.116 to 0.078), p = 0.70. No evidence that extra_sessions changes the attendance slope.
- **extra_sessions × pre_score:** coefficient -0.025 (SE 0.096, 95% CI -0.214 to 0.163), p = 0.79. No evidence that extra_sessions changes the pre_score slope.
- **Main effects in this model:** attendance_pct 0.218 (SE 0.024, p < 0.001); pre_score -0.343 (SE 0.037, p < 0.001); extra_sessions 1.42 (SE 1.67, 95% CI -1.85 to 4.69), p = 0.39.
- **Within-group attendance slopes:** 0.225 for extra_sessions = 0 (SE 0.025, 95% CI 0.176 to 0.274, n = 750) and 0.213 for extra_sessions = 1 (SE 0.048, 95% CI 0.119 to 0.307, n = 250). Both are positive and similar. The interaction test is non-significant, but this does not prove the slopes are identical.

### 5. Adjusted multiple regression (stat_3)

The model regresses score_gain on extra_sessions, pre_score and attendance_pct (n = 1,000; R² = 0.287; adjusted R² = 0.285).

| Term | Coefficient | 95% CI | p | Holm-adjusted p |
|---|---|---|---|---|
| extra_sessions | 1.76 | -0.30 to 3.81 | 0.093 | 0.093 |
| pre_score | -0.346 | -0.414 to -0.279 | < 0.001 | < 0.001 |
| attendance_pct | 0.213 | 0.171 to 0.255 | < 0.001 | < 0.001 |

The extra_sessions association does not remain significant after adjustment, down from the unadjusted difference of 9.76. pre_score and attendance_pct remain significant.

Variance inflation factors are 2.18 for extra_sessions, 2.18 for pre_score and 1.00 for attendance_pct. The stat_3 finding describes collinearity as moderate and acceptable, well below common thresholds of 5 or 10. It states that collinearity widens the extra_sessions confidence interval but does not bias the point estimate.

### 6. Predictive performance (ml_1)

Models were evaluated on a single 200-row test set (800 training rows, random_state 42).

| Model | Test RMSE | Test MAE | Test R² | Train R² |
|---|---|---|---|---|
| Mean baseline | 10.62 | 8.84 | -0.004 | n/a |
| Linear regression | 9.58 | 7.75 | 0.18 | 0.31 |
| Gradient boosting | 10.03 | 8.03 | 0.10 | 0.56 |

Linear regression beats the mean baseline and gradient boosting on test RMSE, MAE and R². Its train-test R² gap is 0.12 on 800 training rows. Gradient boosting overfits more strongly, with train R² 0.56 against test R² 0.10.

![Test RMSE of the mean baseline, linear regression and gradient boosting on the 200-student test set](tasks/ml_1/charts/ml1_model_test_rmse.png)

### 7. Feature importance and agreement with the statistics (ml_2, ml_3)

**With all five features (linear regression, permutation importance on the test set, increase in RMSE when shuffled, mean (SD) over 30 repeats):**

| Rank | Feature | Importance |
|---|---|---|
| 1 | pre_score | 1.360 (0.320) |
| 2 | attendance_pct | 0.882 (0.234) |
| 3 | age | 0.029 (0.021) |
| 4 | class_size | 0.0001 (0.0001) |
| 5 | extra_sessions | -0.038 (0.102) |

pre_score and attendance_pct rank first and second, and both have significant correlations with score_gain (r = -0.46 and 0.29). extra_sessions ranks last with a slightly negative value, so shuffling it does not increase test RMSE. This does not match its statistical association: it has the largest group difference (9.76) and a significant correlation (r = 0.37). Age ranks third (0.029) despite a non-significant correlation, and class_size ranks fourth (0.0001), though both values are near zero. The linear model's largest unscaled absolute coefficient is extra_sessions (2.90), but these coefficients come from unscaled features and are not comparable across features.

Gradient boosting's importances were pre_score 0.571, attendance_pct 0.338, class_size 0.064, age 0.026 and extra_sessions 0.0005.

![Permutation importance of each feature for the linear regression on the 200-row test set](tasks/ml_2/charts/ml2_permutation_importance.png)

![Corrected permutation importance (increase in test RMSE when shuffled) of each feature for the linear regression on the 200-row test set](tasks/ml_2/charts/ml2_permutation_importance_corrected.png)

**Without pre_score (ml_3):**

- The linear model's test R² falls to 0.07 (train R² 0.24), from 0.18 with pre_score included.
- extra_sessions' permutation importance rises from -0.038 to 0.859 (SD 0.312).
- The ranking without pre_score is attendance_pct 0.939 (SD 0.234), extra_sessions 0.859 (SD 0.312), age 0.013 (SD 0.024) and class_size 0.001 (SD 0.001).

The ml_3 finding states that the rise in extra_sessions' importance is consistent with pre_score masking its contribution, given r = -0.736. It also states that the VIF of about 2.2 indicates only moderate collinearity, so collinearity alone is an incomplete explanation for the mismatch.

Variance inflation factors on the 800-row training split are 2.23 for pre_score, 2.23 for extra_sessions, 1.01 for attendance_pct, 1.00 for age and 1.00 for class_size. The stat_3 values (2.18 for each collinear feature) come from the full 1,000-row data, and the difference is attributed to the different sample.

*Note: the uncorrected permutation importance values from ml_2 and ml_3 have flipped signs and are not used in this report. The "without pre_score" importances are reported only in their corrected form.*

## Limitations

- **Unresolved review issue on ml_2 (interaction part of the brief).** The review objection is that the ml_2 report did not answer the interaction part of the brief. The answer is in stat_2: the extra_sessions × attendance_pct (p = 0.70) and extra_sessions × pre_score (p = 0.79) interactions are non-significant. No interaction-based match or mismatch exists between extra_sessions and the top features. The ml_2 wording on the top features' agreement with the statistics was contradictory ("partly agree", then "both agree"). This report states only that pre_score and attendance_pct rank first and second, both with significant correlations.
- **Test-set instability.** All model scores and permutation importances come from one 200-row test split. The ml_1 and ml_3 open questions call for cross-validation or repeated splits, which were not run, so these estimates may be unstable.
- **Collinearity hypothesis only partly tested.** The extra_sessions mismatch is linked to pre_score collinearity. The ml_3 comparison supports this only partly, and no nested model comparison or formal test of independent signal was run.
- **Linearity not tested.** The linear models assume linear effects, and no finding tests whether the pre_score relationship needs a non-linear term. Gradient boosting is non-linear but was not used to test this.
- **Interaction slopes not proven equal.** The two attendance slopes (0.225 and 0.213) are similar, but a non-significant interaction test does not establish that they are identical.
- **Observational data.** The findings describe associations. They do not establish that extra_sessions causes score_gain, and no causal or confounding analysis was completed.
- **Gradient boosting overfits** (train R² 0.56 against test R² 0.10). Its results are reported but are weaker than linear regression's.
- **No failed tasks** are recorded.

## Open questions

- Does the extra_sessions effect hold after adjusting for pre_score in a causal sense (for example, by matching or propensity methods)? The regression gives 1.76 (p = 0.093), but no causal analysis was run.
- Does extra_sessions carry predictive signal independent of pre_score? A model without pre_score and a nested model comparison were suggested but not run.
- Is the pre_score relationship with score_gain linear, or does it need a non-linear term?
- Do the permutation importance rankings hold under cross-validation or repeated splits rather than a single 200-row test set?
- Is extra_sessions a true binary treatment indicator, and is the group difference confounded by attendance_pct or pre_score?