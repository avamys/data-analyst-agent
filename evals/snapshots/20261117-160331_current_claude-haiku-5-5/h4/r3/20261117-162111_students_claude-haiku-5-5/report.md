# Predicting Student Score Gain: Analysis of 1,000 Students (Target: score_gain)

## Summary

- **Three features show significant associations with score_gain in marginal tests:** pre_score (Pearson r = -0.462, r² = 21.3%), attendance_pct (r = 0.291, r² = 8.5%) and extra_sessions (mean gap 9.76 points, Cohen's d = 0.91). All three survive Holm correction. Age and class_size do not (ANOVA p = 0.88 and p = 0.41).
- **extra_sessions and the lowest pre_score quartile are the same 250 students,** so their marginal effects cannot be separated. In the multiple regression, pre_score (coefficient -0.346 per point) and attendance_pct (0.213 per percentage point) remain significant. The extra_sessions coefficient falls to 1.758, with a 95% CI of -0.296 to 3.812 (p = 0.093).
- **Neither interaction is significant.** The extra_sessions interactions with pre_score (p = 0.792) and attendance_pct (p = 0.699) give no evidence that the slopes differ between groups.
- **Linear regression beats a mean baseline on one 200-row test split,** with test RMSE 9.58 against 10.62 and test R² 0.184 against -0.004. It overfits somewhat (train R² 0.308). The random forest does worse on test (R² 0.042). The advantage has no uncertainty estimate.

## Data

- The dataset has 1,000 rows and 6 columns.
- The target is score_gain, a continuous variable. Its mean is -0.003, its median is -0.3, its SD is 11.48, and its range is -33.8 to 40.9.
- There are five numeric features: pre_score, extra_sessions, attendance_pct, age and class_size. There are no categorical, date/time, id or free-text features.
- There are no empty cells. The clean_students table has 0 missing values in total.
- extra_sessions takes the values 0 and 1 (750 and 250 students). age takes the values 15 to 18. class_size takes 15 levels from 18 to 32.

## Findings

### Distribution of score_gain

score_gain is centred near zero and close to symmetric: skew is 0.106, and 68.5% of students lie within one SD of the mean. The quartiles are -7.53 and 7.83.

![Histogram of score_gain across all 1000 students (counts per bin)](tasks/eda_1/charts/score_gain_histogram.png)

### extra_sessions

- Students with one extra session gain more than students with none. The mean is 7.32 (n = 250) against -2.44 (n = 750), and the median is 8.05 against -2.80.
- Welch t = 12.10, p = 5.7e-29. The Mann-Whitney p-value is 1.6e-30. The 95% CI for the mean difference is 8.17 to 11.34 points, and Cohen's d is 0.91.
- The association survives Holm correction (adjusted p = 2.3e-28).
- This is a marginal association. The extra_sessions=1 group is identical to the pre_score Q1 group (250 of 250 students overlap), so the gap cannot be attributed to extra_sessions separately from pre_score in the marginal analysis. The adjusted estimate is in the multiple regression below.

![Mean score_gain for students with 0 vs 1 extra sessions; whiskers show 95% confidence intervals of the mean](tasks/stat_1/charts/stat1_extra_sessions_means.png)

### pre_score

- The relation is negative and moderate. Pearson r = -0.462 (95% CI -0.509 to -0.412, p = 5.2e-54) and Spearman rho = -0.448 (p = 1.9e-50). r² is 0.213. Students with higher pre_score gain less.
- The relation is close to linear. Linear R² is 0.2134 and quadratic R² is 0.2143.
- Quartile means fall steeply: Q1 (20.8 to 52.1) 7.32; Q2 (52.2 to 60.2) 0.57; Q3 (60.3 to 68.9) -1.38; Q4 (69.0 to 102.9) -6.51.
- Like extra_sessions, this association is marginal and confounded in this sample.

### attendance_pct

- The relation is positive and weak to modest. Pearson r = 0.291 (95% CI 0.233 to 0.347, p = 5.9e-21), Spearman rho = 0.278 (p = 3.4e-19), and r² = 0.085. The association survives Holm correction. It is not yet adjusted for pre_score or extra_sessions.
- Quartile means rise steadily: Q1 (50.0 to 62.8) -4.39; Q2 (62.9 to 75.6) -1.16; Q3 (75.7 to 87.9) 1.17; Q4 (88.1 to 100.0) 4.42.
- The relation is near linear. Linear and quadratic R² are both 0.0846.

![Scatter of score_gain against pre_score and attendance_pct, with decile means of score_gain in blue](tasks/eda_2/charts/eda_2_scatter_binned.png)

### age and class_size

- **Age:** There is no significant association. One-way ANOVA gives F = 0.22 and p = 0.88. Kruskal-Wallis gives p = 0.70, and eta² is 0.0007. Group means range from -0.42 (age 15) to 0.36 (age 17), a range of 0.79 points.
- **Class_size:** There is no significant association. One-way ANOVA gives F = 1.04 and p = 0.41. Kruskal-Wallis gives p = 0.49, and eta² is 0.015 (1.5% of variance). Group means run from -2.80 (size 22) to 3.49 (size 24). The 24-student group drives the high end. The ANOVA and Kruskal-Wallis results indicate these differences are consistent with chance.

### Multiple regression (adjusted effects)

In one OLS model of score_gain on pre_score, attendance_pct and extra_sessions (n = 1,000):

| Predictor | Coefficient | 95% CI | p |
|---|---|---|---|
| pre_score | -0.346 | -0.414 to -0.279 | 5.8e-23 |
| attendance_pct | 0.213 | 0.171 to 0.255 | 1.0e-22 |
| extra_sessions | 1.758 | -0.296 to 3.812 | 0.093 |

- R² is 0.2875 and adjusted R² is 0.2854.
- Each point of pre_score is associated with about 0.35 lower gain. Each percentage point of attendance is associated with about 0.21 higher gain.
- The extra_sessions effect is positive but not significant at the 5% level, and its CI includes zero. The marginal result (p = 5.7e-29) and the adjusted result (p = 0.093) disagree on significance. The marginal result is confounded with pre_score, so the adjusted result is the one that separates them, with wide uncertainty.
- Collinearity is modest. VIF is 2.18 for pre_score, 2.18 for extra_sessions and 1.00 for attendance_pct. The correlation between pre_score and extra_sessions is -0.736.
- The 250 students in pre_score Q1 are exactly the 250 students with extra_sessions=1. The model can fit both terms because pre_score varies within each extra_sessions group, but the extra_sessions coefficient depends on comparing students across the pre_score range under a linearity assumption.

### Interactions

In score_gain ~ extra_sessions*pre_score + extra_sessions*attendance_pct (R² = 0.288):

- The extra_sessions:pre_score coefficient is -0.025 (SE 0.096, p = 0.792, 95% CI -0.214 to 0.163).
- The extra_sessions:attendance_pct coefficient is -0.019 (SE 0.049, p = 0.699, 95% CI -0.116 to 0.078).
- Neither interaction is significant.
- Group slopes on pre_score are -0.343 per point (95% CI -0.416 to -0.270) for extra_sessions=0 and -0.368 (95% CI -0.542 to -0.194) for extra_sessions=1.
- Group slopes on attendance_pct are 0.218 per percent (95% CI 0.170 to 0.265) for extra_sessions=0 and 0.198 (95% CI 0.114 to 0.283) for extra_sessions=1.
- The extra_sessions=1 slope CIs are wide, so modest slope differences cannot be ruled out.
- The extra_sessions coefficient in this model is conditional on pre_score = 0 and attendance_pct = 0. It is not an adjusted main effect.

### Effect sizes and multiple-comparison control

Five primary tests were corrected with Holm's step-down method. Adjusted p-values are: extra_sessions 2.3e-28; pre_score 2.6e-53; attendance_pct 1.8e-20; age 0.88; class_size 0.82. The three significant results remain significant after correction.

Effect sizes are on a common variance-explained scale. The ranking is indicative only, because the measures differ in type:

- pre_score: 21.3% (r² = 0.213)
- extra_sessions: 13.5% (point-biserial r = 0.368, converted from Cohen's d = 0.91)
- attendance_pct: 8.5% (r² = 0.085)
- class_size: 1.5% (eta² = 0.015)
- age: 0.07% (eta² = 0.0007)

extra_sessions and pre_score are confounded in this sample, so the marginal measures do not identify their separate contributions. The adjusted coefficients in the multiple regression are the only attempt to separate them, and they carry wide intervals.

### Predictive models

Models were fit on 800 training rows and tested on a 200-row split (seed 42).

| Model | Train R² | Test R² | Test RMSE | Test MAE |
|---|---|---|---|---|
| Mean baseline | 0.000 | -0.004 | 10.62 | 8.84 |
| Linear regression | 0.308 | 0.184 | 9.58 | 7.75 |
| Random forest (300 trees) | 0.892 | 0.042 | 10.38 | 8.38 |

- Linear regression has the lowest test RMSE. Its train-test R² gap is 0.12.
- The random forest overfits more (train R² 0.892) and performs worse on test.
- The linear advantage is a point estimate from one split, with no uncertainty estimate.

![Test RMSE of score_gain for the mean baseline, linear regression and random forest on the same 200-row test set; lower is better](tasks/ml_1/charts/ml1_model_rmse.png)

Permutation importance (increase in test RMSE when shuffled, 20 repeats):

- **Linear regression:** pre_score 1.38 (SD 0.32); attendance_pct 0.89 (SD 0.27); age 0.03 (SD 0.02); class_size 0.0001 (SD 0.0001); extra_sessions -0.02 (SD 0.10). Age and class_size are negligible. The extra_sessions result does not show that it is irrelevant, because its effect is confounded with pre_score.
- **Random forest:** pre_score 1.61 (SD 0.33); attendance_pct 0.63 (mean only); extra_sessions -0.025 (SD 0.008). This agrees with the linear model on the top two features. The forest's test performance is poor, so its importance values are less reliable.
- The linear coefficients are not a measure of importance. The features are unscaled, and extra_sessions is a 0/1 indicator.

## Limitations

- **Confounding:** The extra_sessions=1 group is identical to the pre_score Q1 group (250 of 250 students). The marginal effects of these two features cannot be separated. The adjusted extra_sessions coefficient has a CI from -0.296 to 3.812 and is not significant at 5%.
- **Marginal results:** The pre_score and attendance_pct results are marginal and were not adjusted for each other in the bivariate tests. The multiple regression adjusts for both, but it assumes linearity. The quadratic terms added little fit.
- **Model evaluation:** Predictive performance rests on one 200-row test split with no uncertainty estimate. The linear advantage over the baseline and the overfitting gap are point estimates. The random forest's importance values are less reliable because its test R² is 0.042.
- **Interaction precision:** The extra_sessions=1 slope CIs are wide, so modest slope differences between groups cannot be ruled out.
- **Review objection (stat_1), still standing:** The lead's objection asked that the effect-size ranking use only the common-metric values and state that it is indicative, and that the class_size "consistent with chance" conclusion be attributed to the ANOVA and Kruskal-Wallis results. The ranking above uses those values and is marked indicative. The class_size conclusion rests on the ANOVA (p = 0.41) and Kruskal-Wallis (p = 0.49) results. The objection affects the effect-size ranking and the class_size finding.
- **Review objection (ml_1), still standing:** The lead's objection asked that the random forest attendance_pct SD and the "not recorded separately" wording be removed, and that the linear model's age and class_size importance values be checked against the full record. The forest attendance_pct value is reported as a mean only (0.63). The linear age (0.03, SD 0.02) and class_size (0.0001, SD 0.0001) values match the full record. The objection affects the permutation-importance findings.
- **eda_1 class_size comparison:** The comparison of class_size with extra_sessions is supported for age but only weakly for class_size. The class_size differences are judged by the ANOVA and Kruskal-Wallis tests, not by the descriptive range.
- **Failed tasks:** None. All six tasks (eda_1, eda_2, stat_1, stat_2, stat_3, ml_1) are complete.

## Open questions

- Does the extra_sessions effect hold after adjusting for pre_score, attendance_pct, age and class_size together? The multiple regression covers only the first three.
- Do age and class_size change the pre_score, attendance_pct or extra_sessions coefficients when added to the model?
- Does the pre_score relation hold after controlling for extra_sessions and attendance_pct, with a non-linear pre_score term or an interaction?
- Does the attendance_pct effect persist after adjusting for pre_score and extra_sessions, with uncertainty on the adjusted estimate?
- Would a sample in which extra_sessions and the pre_score bottom quartile differ allow the two effects to be separated?
- Would repeated cross-validation put uncertainty on the linear advantage over the baseline and on the overfitting gap?
- Does a regularised or gradient-boosted model improve on linear regression without the random forest's overfitting?