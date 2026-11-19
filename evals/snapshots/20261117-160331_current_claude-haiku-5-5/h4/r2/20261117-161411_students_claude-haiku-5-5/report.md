# Score Gain Drivers in 1,000 Students: Analysis of the score_gain Target

## Summary

- **extra_sessions shows the largest unadjusted difference.** Students with extra_sessions=1 (n=250) had a mean score_gain of 7.32 versus -2.44 for extra_sessions=0 (n=750), a difference of 9.76 points (Cohen's d = 0.91). This survives Holm correction. After adjusting for pre_score, attendance_pct and class_size, the estimate falls to 1.76 points (p = 0.093), which is not significant.
- **pre_score and attendance_pct have significant, moderate correlations with score_gain.** pre_score: r = -0.46. attendance_pct: r = 0.29. Both remain significant after Holm correction. Higher starting scores go with smaller gains, and higher attendance with larger gains.
- **extra_sessions and pre_score are almost perfectly separated.** Students with extra_sessions=1 had a mean pre_score of 43.3 versus 65.8 for extra_sessions=0. No pre_score stratum contains both groups, so the adjusted extra_sessions estimate is weakly identified.
- **age and class_size show no detectable effect on score_gain.** Age: ANOVA p = 0.88, eta-squared 0.07%. Class size: ANOVA p = 0.41, eta-squared about 1.5%. Neither is significant after Holm correction.
- **Predictive power is low.** On a 200-row test set, linear regression reaches R² = 0.18 (RMSE 9.58) against 10.62 for a mean baseline. Gradient boosting overfits more and scores lower (test R² = 0.10). The permutation importance of extra_sessions conflicts with its coefficient, so feature importance is unresolved.

## Data

- **Size:** 1,000 rows × 6 columns.
- **Target:** score_gain (continuous regression target). Median -0.3, range -33.8 to 40.9.
- **Features:** five numeric features: pre_score, extra_sessions, attendance_pct, age, class_size. There are no categorical, date/time, id or free-text features.
- **Missing values:** none. Every column has zero missing cells, and the analysis used all 1,000 rows.
- **Value ranges:** extra_sessions takes values 0 and 1 (750 and 250 students). age runs from 15 to 18. class_size runs from 18 to 32. attendance_pct runs from 50 to 100.

## Findings

### Distribution of score_gain, and extra_sessions and age

score_gain is centred near zero and close to symmetric. Mean -0.003, median -0.3, standard deviation 11.48, quartiles -7.53 and 7.83, skew 0.11.

By extra_sessions, the mean and median differ substantially:

| extra_sessions | n | Mean score_gain | Median score_gain |
|---|---|---|---|
| 0 | 750 | -2.44 | -2.80 |
| 1 | 250 | 7.32 | 8.05 |

By age, means and medians vary only modestly:

| Age | n | Mean | Median |
|---|---|---|---|
| 15 | 263 | -0.42 | -1.10 |
| 16 | 222 | -0.08 | -1.05 |
| 17 | 270 | 0.36 | 1.15 |
| 18 | 245 | 0.11 | -0.50 |

The means rise slightly from 15 to 17, and the medians show no clear trend.

![Histogram of score_gain for students with extra_sessions 0 and 1, counts of students](tasks/eda_1/charts/score_gain_by_extra_sessions.png)

### pre_score, attendance_pct and class_size

- **pre_score:** Pearson r = -0.462, Spearman rho = -0.448. Mean score_gain by pre_score quartile (250 students each): Q1 7.32, Q2 0.57, Q3 -1.38, Q4 -6.51.
- **attendance_pct:** Pearson r = 0.291, Spearman rho = 0.278. Mean score_gain by attendance quartile: Q1 (n=252) -4.39, Q2 (n=249) -1.16, Q3 (n=249) 1.17, Q4 (n=250) 4.42.
- **class_size:** Pearson r = -0.016, Spearman rho = -0.016. There is no consistent trend. Mean score_gain by class size ranges from -2.8 (size 22, n=54) to 3.49 (size 24, n=68).

Full mean score_gain by class_size (count in brackets):

18: 0.55 (72); 19: 0.05 (72); 20: 0.21 (73); 21: 1.74 (57); 22: -2.80 (54); 23: -0.91 (71); 24: 3.49 (68); 25: -1.52 (68); 26: 0.58 (69); 27: 0.10 (68); 28: -1.37 (60); 29: -0.02 (73); 30: -0.78 (73); 31: -0.66 (59); 32: 0.85 (63).

The mode is not unique for class_size. Sizes 20, 29 and 30 are tied at 73 students each (mode output: [20, 29, 30]). The dataset profile states that 20 is the single most common class size (73 of 1,000). This is a discrepancy to be noted: the mode output shows three tied values, not one.

![Scatter of score_gain against pre_score (left) and attendance_pct (right), one point per student](tasks/eda_2/charts/score_gain_scatter_pre_and_attendance.png)

### Statistical significance and effect sizes

Seven primary tests were run and Holm-corrected together.

- **extra_sessions (Welch t-test):** The mean difference (1 minus 0) is 9.76 points, t = 12.10, df = 403.9, p = 5.7e-29. The 95% CI is 8.17 to 11.34. Cohen's d = 0.91 (large). Holm-adjusted p = 3.4e-28, so significant.
- **age (one-way ANOVA):** F = 0.22, p = 0.88. Kruskal-Wallis p = 0.70. Eta-squared 0.0007. Not significant after Holm correction (adjusted p = 1.0).
- **class_size (one-way ANOVA, 15 levels):** F = 1.04, p = 0.41. Kruskal-Wallis H = 13.44, p = 0.49. Eta-squared 0.015 (about 1.5% of variance). Not significant after Holm correction.
- **pre_score (Pearson):** r = -0.46, p = 5.2e-54, 95% CI -0.51 to -0.41. Significant after Holm correction.
- **attendance_pct (Pearson):** r = 0.29, p = 5.9e-21, 95% CI 0.23 to 0.35. Significant after Holm correction.

After Holm correction, only the extra_sessions difference, the pre_score correlation and the attendance_pct correlation remain significant.

![Mean score_gain with 95% CI by extra_sessions (left) and by age (right); the extra_sessions gap is about 10 points, the age means are flat](tasks/stat_1/charts/stat1_mean_gain_by_group.png)

### Whether extra_sessions moderates the effect of attendance_pct

- The attendance_pct × extra_sessions interaction is not significant: coefficient -0.019, 95% CI -0.116 to 0.078, p = 0.70. This model adjusts for pre_score, age and class_size (R² = 0.289).
- Within-group slopes of score_gain on attendance_pct: 0.217 points per percentage point for extra_sessions=0 (95% CI 0.169 to 0.265, p < 0.001) and 0.198 for extra_sessions=1 (95% CI 0.114 to 0.282, p = 4.2e-06). The two slopes are nearly equal and their CIs overlap.
- This model does not estimate an adjusted extra_sessions offset.

![Raw score_gain against attendance_pct, split by extra_sessions 0 and 1 (points only, no fitted lines)](tasks/stat_2/charts/stat2_attendance_by_extra_sessions.png)

![Points: raw score_gain. Lines: OLS fitted slope of score_gain on attendance_pct for extra_sessions 0 and 1, at mean pre_score, age and class_size](tasks/stat_2/charts/stat2_fitted_attendance_by_extra_sessions.png)

### The extra_sessions effect after adjustment

- **Unadjusted:** the difference is 9.76 points (95% CI 8.18 to 11.34, using the Welch standard error with a 1.96 normal approximation; p < 0.001).
- **Adjusted for pre_score, attendance_pct and class_size (OLS, n=1,000):** the extra_sessions coefficient is 1.76 points (SE 1.05, 95% CI -0.29 to 3.82, p = 0.093). This is not significant at 5%. The answer to whether the difference remains about 10 points is no.
- **Model fit:** R² = 0.288, adjusted R² = 0.285. Covariate coefficients: pre_score -0.35, attendance_pct 0.21, class_size -0.03 per unit.
- **Residual checks:** Breusch-Pagan p = 0.180 (no evidence of heteroskedasticity at 5%). Jarque-Bera p = 0.923, residual skew 0.03. Residual SD by fitted-value quartile: 9.82, 9.26, 9.27, 10.42. Residual means lie between -0.25 and 0.21. Spearman correlation of fitted values with absolute residuals is 0.007 (p = 0.83). The stat_3 finding describes the residuals-vs-fitted panel as a horizontal band around zero with no curve or funnel shape.
- Covariate balance between the extra_sessions groups was not tested.

![Left: unadjusted and adjusted difference in mean score_gain for extra_sessions 1 vs 0, with 95% CI. Right: residuals vs fitted values from the adjusted OLS model.](tasks/stat_3/charts/extra_sessions_effect_ci.png)

### extra_sessions and pre_score

- **Imbalance:** students with extra_sessions=1 had mean pre_score 43.3, and those with extra_sessions=0 had 65.8. The difference is -22.5 points (Welch 95% CI -23.6 to -21.4, t = -40.1, p = 1.5e-169).
- **Adjusting for pre_score alone:** the extra_sessions effect is 1.64 points (95% CI -0.52 to 3.79, p = 0.14), with a pre_score coefficient of -0.36. This differs from the 1.76 estimate in the previous section because that model also adjusts for attendance_pct and class_size. The two estimates differ by covariate set.
- **Interaction (extra_sessions × pre_score):** p = 0.63, coefficient -0.048. This test is uninformative, because the extra_sessions groups do not overlap on pre_score (see Limitations).
- **Strata:** pre_score quartile 1 (20.8 to 52.1) contains all 250 extra_sessions=1 students and no extra_sessions=0 students. Quartiles 2 to 4 (52.2 to 102.9) contain only extra_sessions=0 students. No within-stratum comparison is possible.

### Predictive models (test set, n=200; training n=800; five features; random_state 42)

| Model | Test RMSE | Test MAE | Test R² | Train R² |
|---|---|---|---|---|
| Mean baseline | 10.62 | 8.84 | -0.004 | n/a |
| Linear regression | 9.58 | 7.75 | 0.18 | 0.31 |
| Gradient boosting | 10.03 | 8.03 | 0.10 | 0.56 |

Both models beat the baseline on RMSE. Linear regression beats it by about 1.05 RMSE points. Linear regression overfits (train–test R² gap 0.12). Gradient boosting overfits more (gap 0.45).

![Test RMSE of the mean baseline, linear regression and gradient boosting on the 200-row test set](tasks/ml_1/charts/ml1_test_rmse.png)

**Feature importance (linear regression, absolute coefficient):** extra_sessions 2.90, pre_score 0.33, age 0.27, attendance_pct 0.22, class_size 0.0004.

**Permutation importance (linear regression, increase in test RMSE when shuffled):**
- pre_score: 1.36 (sd 0.32)
- attendance_pct: 0.88 (sd 0.23)
- age: 0.03 (sd 0.02)
- class_size: 0.0001 (sd 0.0001)
- extra_sessions: -0.04 (sd 0.10). This result is unresolved (see Limitations).

Gradient boosting's importances (pre_score 0.571, attendance_pct 0.338, class_size 0.064, age 0.026, extra_sessions 0.0005) are impurity-based values from a different model. They are not a permutation ranking and cannot be compared with the linear model's permutation results.

## Limitations

- **Unresolved: class_size mode.** The dataset profile says 20 is the single most common class size (73 of 1,000). The mode output shows sizes 20, 29 and 30 tied at 73 each. This discrepancy is stated, not resolved. The full class_size mean table is given in the eda_2 section so the counts and means can be checked.
- **Removed claim.** The scatter-plot pattern is not described as consistent with the quartile means, because no recorded fact supports that statement. The scatter chart is shown without that claim.
- **Unresolved: extra_sessions permutation importance.** The permutation importance for extra_sessions is -0.04 (sd 0.10). This conflicts with its linear coefficient of 2.90 and the 9.8-point unadjusted gap. The procedure and test-set alignment have not been confirmed as correct, and no error has been found. extra_sessions must not be ranked as unimportant. pre_score and attendance_pct are not the only drivers of predictive signal until this is resolved.
- **Unresolved: interaction under non-overlap (stat_4).** extra_sessions groups do not overlap on pre_score. The interaction test (p = 0.63, coefficient -0.048) is uninformative and cannot show whether the extra_sessions effect is constant across pre_score. The adjusted estimate of 1.64 (95% CI -0.52 to 3.79, p = 0.14) is weakly identified: it rests on linear extrapolation across non-overlapping pre_score ranges.
- **Adjusted estimates depend on the covariate set.** The 1.76 (stat_3) and 1.64 (stat_4) estimates use different covariate sets and are not tested against each other. Covariate balance between extra_sessions groups was not tested.
- **Confidence interval method.** The stat_1 Welch CI for extra_sessions is 8.17 to 11.34. The stat_3 CI is 8.18 to 11.34, computed with a 1.96 normal approximation. Both are reported as recorded.
- **Modelling constraints.** Linear regression and gradient boosting were run with default settings on one 80/20 split. Both models overfit to some degree, and their test scores come from 200 rows.
- **Task status.** stat_4 is partial. Its adjusted and interaction results are reported with the caveats above.
- **Scope.** The findings are associations. This report does not give causal interpretations.

## Open questions

- Does the extra_sessions effect hold where pre_score ranges overlap? The overlap restriction gave no usable result, so this needs a different design or a fix.
- Does a nonlinear pre_score adjustment (splines or a flexible model) change the adjusted extra_sessions estimate of 1.64 or 1.76?
- Why do extra_sessions and pre_score separate almost completely? Is this a data-generating or selection issue, and what does it mean for any causal reading?
- Are pre_score, attendance_pct and class_size balanced between extra_sessions groups?
- Does the extra_sessions effect differ by age (interaction test not yet run)?
- Is the pre_score relation non-linear, or partly a regression-to-the-mean effect?
- Does the pre_score relation persist after adjusting for attendance_pct, extra_sessions and class_size in a multiple regression?
- Why does the permutation importance of extra_sessions come out near zero or negative, given its coefficient of about 2.9? Are the permutation procedure and test-set alignment correct?
- Would a regularised or tuned model reduce the overfitting gap and improve on linear regression's test R² of 0.18?
- Does a heteroskedasticity-robust SE or a nonparametric check agree with the adjusted extra_sessions result?