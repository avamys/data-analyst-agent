# Predicting Student score_gain from Five Numeric Features: Distribution, Associations, and Model Comparison

## Summary

- **pre_score is the strongest associated feature.** Its correlation with score_gain is Pearson r = -0.462 (95% CI -0.509 to -0.412). It is the most important feature in both the linear and gradient boosting models, on the single split and under repeated CV. Higher pre_score goes with lower score_gain.
- **extra_sessions has the largest unadjusted difference, but it is fully confounded with pre_score.** Students with one extra session gained 9.76 points more than those with none (95% CI 8.17 to 11.34, Cohen's d = 0.91). All 250 students with extra_sessions = 1 are in the lowest pre_score quartile. In the adjusted model the extra_sessions effect is 1.42 points (p = 0.39). The two estimates disagree, and these data cannot separate the extra_sessions effect from pre_score.
- **attendance_pct has a moderate positive association** (Pearson r = 0.291, 95% CI 0.233 to 0.347). Its adjusted slope is 0.217 per centred point (p < 0.001). It is the second most important feature in the models evaluated.
- **The prediction gain over the mean baseline is real but modest.** Linear regression reduces test RMSE from 10.62 to 9.58 on a single 200-row split. Under repeated 5-fold CV, the baseline RMSE is 11.48 and linear regression's is 9.73, with CV R² of about 0.28. Gradient boosting has higher RMSE than linear regression in all 15 CV folds.
- **age and class_size show no association with score_gain** after Holm correction (adjusted p = 1.0 each), and their permutation importances are near zero.

## Data

- **Size:** 1,000 rows and 6 columns.
- **Target:** score_gain, a numeric regression target with mean -0.003, median -0.3, standard deviation 11.48, and range -33.8 to 40.9 points.
- **Features:** five numeric features (pre_score, extra_sessions, attendance_pct, age, class_size). There are no categorical, date/time, id or free-text features.
- **Missing values:** none in any of the six columns, so no rows were dropped. The cleaned table is published as clean_student_table.

## Findings

### Distribution of the target

score_gain is roughly symmetric and centred near zero. The mean is -0.003, the median is -0.3, the quartiles are -7.525 and 7.825, and the skew is 0.106.

![Histogram of score_gain: count of students per bin](tasks/eda_1/charts/score_gain_hist.png)

### Associations with each numeric feature

**pre_score (negative, strong, significant).** Pearson r = -0.462 (95% CI -0.509 to -0.412, p < 0.001). Spearman rho = -0.448 (bootstrap 95% CI -0.498 to -0.393). The Holm-adjusted p across the five tests is 2.6e-53. Mean score_gain by pre_score quartile, from lowest to highest, is 7.32, 0.57, -1.38 and -6.51 (250 students per bin).

**attendance_pct (positive, moderate, significant).** Pearson r = 0.291 (95% CI 0.233 to 0.347, p < 0.001). Spearman rho = 0.278 (bootstrap 95% CI 0.219 to 0.333). The Holm-adjusted p is 1.8e-20. Mean score_gain by attendance quartile, from lowest to highest, is -4.39, -1.16, 1.17 and 4.42.

**extra_sessions (binary, large unadjusted difference, significant).** The variable takes only the values 0 and 1. The 750 students with 0 have mean score_gain -2.44 (median -2.8). The 250 with 1 have mean 7.32 (median 8.05). The difference is 9.76 points (95% CI 8.17 to 11.34). Welch t = 12.10, p < 0.001. Mann-Whitney p < 0.001, Cohen's d = 0.91, and the Holm-adjusted p is 2.3e-28.

**age (no association).** Pearson r = 0.021 (95% CI -0.041 to 0.083, p = 0.51). Spearman rho = 0.027 (p = 0.39). Per-age means are -0.42 (15, n = 263), -0.08 (16, n = 222), 0.36 (17, n = 270) and 0.11 (18, n = 245). The pattern is not monotonic, and whether it is real or noise was not established. The Holm-adjusted p is 1.0.

**class_size (no association).** Pearson r = -0.016 (95% CI -0.077 to 0.047, p = 0.62). Spearman rho = -0.016 (p = 0.62). Quartile-bin means are 0.58, -0.31, -0.14 and -0.22, with medians between -1.6 and 0.7. The Holm-adjusted p is 1.0.

### Confounding between extra_sessions and the other features

- **pre_score:** The groups do not overlap. All 250 students with extra_sessions = 1 fall in the lowest pre_score quartile (Q1). All 750 with extra_sessions = 0 fall in Q2 to Q4 (250 each). Mean pre_score is 43.32 (median 44.60) for extra_sessions = 1 and 65.83 (median 64.35) for extra_sessions = 0.
- **attendance_pct:** The groups overlap almost completely. Mean attendance is 76.17 (median 75.8) for extra_sessions = 1 and 75.22 (median 75.6) for extra_sessions = 0. Both groups spread across all four attendance quartiles.
- No extra_sessions = 1 student has a pre_score above the Q1 cutoff, so the extra_sessions effect cannot be compared at similar pre_score values in these data.

![Distribution of pre_score and attendance_pct for extra_sessions 0 and 1](tasks/eda_3/charts/eda3_overlap.png)

### Adjusted model and interactions

In an OLS model with pre_score and attendance_pct centred at their sample means (R² = 0.288):
- The pre_score slope is -0.343 (p < 0.001).
- The attendance_pct slope is 0.217 (p < 0.001).
- The extra_sessions main effect is 1.42 (p = 0.39).

The unadjusted extra_sessions difference (9.76) and the adjusted estimate (1.42) disagree. The stat_2 findings attribute the gap to confounding or covariate overlap. eda_3 shows that extra_sessions and pre_score do not overlap at all, so this attribution was not tested and the data do not settle it.

**Interactions.** Neither interaction is statistically significant:
- extra_sessions × attendance_pct: coefficient -0.019 (95% CI -0.116 to 0.078, p = 0.70).
- extra_sessions × pre_score: coefficient -0.025 (95% CI -0.214 to 0.163, p = 0.79).

The pre_score interval is wide enough to include changes that are not negligible relative to the pre_score slope of -0.343. A non-significant result here is not evidence of no change.

**Tercile means.** Within each extra_sessions group, mean score_gain rises across attendance terciles. For extra_sessions = 0 the means are -6.17 (low, n = 262), -2.25 (mid, n = 236) and 1.25 (high, n = 252). For extra_sessions = 1 they are 3.64 (low, n = 73), 7.65 (mid, n = 95) and 10.20 (high, n = 82).

![Mean score_gain per attendance tercile, separately for extra_sessions 0 and 1](tasks/stat_2/charts/stat2_tercile_means.png)

### Predictive models on a single split

The split uses the five numeric features, with 800 training rows and 200 test rows (80/20, random_state 42). Features are standardised with a scaler fitted on the training rows only. The target mean is 0.132 on the training side and -0.544 on the test side.

| Model (200-row test split) | Test RMSE | Test MAE | Test R² |
|---|---|---|---|
| Mean baseline | 10.62 | 8.84 | -0.004 |
| Linear regression | 9.58 | 7.75 | 0.184 |
| Gradient boosting | 10.03 | 8.02 | 0.105 |

Linear regression beats the baseline on all three metrics. Its RMSE is 1.05 points lower, just over one point or about 9.8%. The model explains about 18% of test variance, which is a real but modest gain.

Gradient boosting overfits more than linear regression. Its train R² is 0.555 against a test R² of 0.105. Linear regression has train R² 0.308 against test R² 0.184. Gradient boosting does not beat linear regression on the test split.

![Test RMSE of score_gain for linear regression, gradient boosting and the mean baseline on the shared 200-row test split](tasks/ml_2/charts/ml2_model_test_rmse.png)

**Feature importance on the single split.**
- pre_score is the most important feature in both models. Its permutation drop in test R² is 0.249 (SD 0.061) for linear regression and 0.379 (SD 0.072) for gradient boosting. Its standardised linear coefficient is 4.478.
- attendance_pct is second. Its permutation drops are 0.158 (linear) and 0.134 (gradient boosting), and its linear coefficient is 3.155.
- extra_sessions has a permutation importance of -0.006 (linear) and -0.001 (gradient boosting). Its linear coefficient is 1.263, the third-largest in absolute size.
- class_size has a permutation importance of 0.000 in the linear model and -0.027 in gradient boosting. Its gradient boosting impurity importance is 0.0644, third after pre_score (0.571) and attendance_pct (0.338). Its linear coefficient is 0.002.
- age has a permutation importance of 0.005 in the linear model and -0.001 in gradient boosting. Its linear coefficient is 0.307 and its impurity importance is 0.026.

### Repeated cross-validation

Results come from 15 test folds (repeated 5-fold, 3 repeats) on all 1,000 rows.

| Model (15 CV folds) | RMSE mean (SD) | MAE mean (SD) | R² mean (SD) |
|---|---|---|---|
| Mean baseline | 11.48 (0.46) | 9.23 (0.33) | -0.005 (0.008) |
| Linear regression | 9.73 (0.46) | 7.77 (0.41) | 0.276 (0.050) |
| Gradient boosting | 10.26 (0.49) | 8.13 (0.41) | 0.196 (0.049) |

- Linear regression has lower RMSE than the baseline under CV (9.73 against 11.48). The single-split comparison (10.62 against 9.58) comes from a different test set. The two are reported side by side without one correcting the other.
- Gradient boosting has higher RMSE than linear regression in 15 of 15 folds. The paired per-fold difference (gradient boosting minus linear) is 0.52 points (SD 0.17), ranging from 0.24 to 0.91.

![Mean and SD of test RMSE of score_gain for linear regression, gradient boosting and the mean baseline across 15 repeated 5-fold CV test folds on 1000 rows](tasks/ml_3/charts/ml3_cv_rmse.png)

**Permutation importance under CV.**
- pre_score is the most important feature in both models. Its mean R² drop is 0.318 (SD 0.050) for linear regression and 0.407 (SD 0.060) for gradient boosting. It is positive in 15 of 15 folds for both.
- pre_score exceeds attendance_pct in 15 of 15 folds for both models. The per-fold differences are 0.085 to 0.274 (linear) and 0.171 to 0.400 (gradient boosting).
- attendance_pct is positive in all 15 folds, with a mean of 0.141 (SD 0.022) for linear regression and 0.128 (SD 0.027) for gradient boosting.
- extra_sessions has near-zero importance: 0.006 (SD 0.010) for linear regression, positive in 12 of 15 folds, and -0.0001 (SD 0.0009) for gradient boosting, positive in 5 of 15 folds.
- class_size is -0.001 (SD 0.002) for linear regression, positive in 5 of 15 folds, and -0.014 (SD 0.014) for gradient boosting, positive in 2 of 15 folds.
- age is 0.001 (SD 0.004) for linear regression, positive in 10 of 15 folds, and -0.005 (SD 0.007) for gradient boosting, positive in 3 of 15 folds.

## Limitations

- **Confounding of extra_sessions with pre_score.** All 250 students with extra_sessions = 1 are in the lowest pre_score quartile. The 9.76-point unadjusted difference and the 1.42-point adjusted estimate cannot be reconciled in these data. The adjusted estimate is not significant (p = 0.39). The findings do not establish whether extra_sessions has any effect separate from pre_score.
- **Interaction intervals are wide.** The pre_score interaction interval (-0.214 to 0.163) is wide, and a non-significant result does not show that the slopes are equal.
- **Modest predictive performance.** Linear regression explains about 18% of test variance on the single split and about 28% under CV. Gradient boosting overfits, with train R² 0.555 against test R² 0.105 on the single split. A more regularised gradient boosting model was not tested, so the comparison with linear regression covers only the model as fitted.
- **Single split and CV results differ.** On the 200-row split the RMSE values are 10.62 (baseline) and 9.58 (linear). Under CV they are 11.48 and 9.73. The findings report both without reconciling them.
- **Non-linearity not tested in the models.** The tercile means rise within both extra_sessions groups, but the linear model assumes a linear attendance_pct slope. No spline or quadratic model was fitted.
- **Age pattern.** The non-monotonic age means (-0.42, -0.08, 0.36, 0.11) were not tested for noise against the wide spread within each age group. The age association is null on both correlation measures.
- **Unresolved review issues (lead's objections still stand, with corrections applied in this report):**
  - *ml_2 RMSE wording:* The earlier claim that the linear RMSE gain was "under one point" is incorrect. The gain is 1.05 points (10.62 vs 9.58), just over one point. The "modest, not strong" interpretation is retained. This affects the ml_2 findings and the Summary.
  - *extra_sessions and the "carried by" claim:* The earlier statement that the extra_sessions association is "largely carried by pre_score and attendance_pct" is a hypothesis, not an established result. It has not been tested and appears here only as an open question. This affects the ml_2 and ml_3 findings.
  - *Permutation importance citations:* The class_size and age values for the single split come from the stored ml2_perm_importance facts: class_size 0.000 (linear) and -0.027 (gradient boosting); age 0.005 (linear) and -0.001 (gradient boosting). The ml_3 stored copies of these values were truncated in the brief. This affects the ml_2 and ml_3 findings.
- **No failed tasks.** All eight tasks (eda_1, eda_2, eda_3, stat_1, stat_2, ml_1, ml_2, ml_3) completed and were accepted.

## Open questions

- Does the extra_sessions association with score_gain disappear once pre_score and attendance_pct are both adjusted for? eda_3 shows no overlap on pre_score, so the adjusted estimate cannot yet be interpreted.
- Would a more regularised gradient boosting model (fewer trees, shallower depth, early stopping) close the train-test gap and beat linear regression under repeated CV?
- Does the attendance_pct effect on score_gain follow a non-linear shape? The tercile means suggest it might.
- Is the non-monotonic age pattern real or noise, given the wide spread within each age group?
- Do the pre_score and attendance_pct effects hold after adjusting for each other and for extra_sessions in a multivariable model with cross-validated estimates?