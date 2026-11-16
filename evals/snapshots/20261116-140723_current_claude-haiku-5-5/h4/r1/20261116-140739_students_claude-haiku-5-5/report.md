# Score Gain Analysis: Drivers and Predictability of score_gain in a 1,000-Student Dataset

## Summary

- **Distribution:** score_gain is centred near zero (mean -0.003, median -0.3, SD 11.48, range -33.8 to 40.9) and unimodal.
- **Strongest marginal association:** pre_score correlates negatively with score_gain (Pearson r = -0.462, slope -0.400 points per point, p = 5e-54). Extra_sessions (r = 0.368) and attendance_pct (r = 0.291) correlate positively. Age and class_size show no significant association.
- **Extra sessions are confounded with pre_score:** all 250 students with one extra session are in the lowest pre_score quartile, and no student outside that quartile has one. The unadjusted extra_sessions slope of 9.76 points is therefore not separable from pre_score in this sample. After adjusting for the other four numeric features, the extra_sessions coefficient is 1.77 (95% CI -0.29 to 3.82, p = 0.092), which is not significant at the 0.05 level and rests on the linear form assumed by the model.
- **Predictive power is modest:** a linear regression on the five numeric features reaches test R² 0.184 (RMSE 9.58) against 10.62 for a mean baseline (test R² -0.004). pre_score and attendance_pct carry the predictive contribution; extra_sessions adds none once the other features are included.
- **No detected interactions:** the extra_sessions interactions with pre_score and attendance_pct are not significant (joint Wald p = 0.90), though the data cannot rule out small differences in slope.

## Data

- 1,000 rows and 6 columns.
- Target: score_gain (continuous regression target).
- Features: five numeric features (pre_score, extra_sessions, attendance_pct, age, class_size). There are no categorical, date/time, or free-text features, and no identifier columns.
- Missing values: none. All six columns have zero missing values (0.0%).

## Findings

### Distribution of score_gain

score_gain has mean -0.003, median -0.3, SD 11.48, minimum -33.8 and maximum 40.9. Its 10-bin histogram is unimodal, peaking at 246 students in the fifth bin (edges -3.92 to 3.55).

![Histogram of score_gain, count of students per bin](tasks/eda_1/charts/score_gain_histogram.png)

### Marginal associations with score_gain (eda_1, stat_1)

Pearson correlations with score_gain: pre_score -0.46, extra_sessions 0.37, attendance_pct 0.29, age 0.02, class_size -0.02.

**pre_score:** The association is strong and negative. Pearson r = -0.462 (95% CI -0.509 to -0.412, p = 5e-54). Spearman rho = -0.448 (p = 2e-50). The linear slope is -0.400 points per pre_score point (95% CI -0.448 to -0.352). Holm-adjusted p is effectively 0. Mean and median score_gain fall across pre_score quartiles:

| pre_score quartile | n | Mean | Median |
|---|---|---|---|
| Q1 (20.8 to 52.2] | 250 | 7.32 | 8.05 |
| Q2 (52.2 to 60.25] | 250 | 0.57 | 0.60 |
| Q3 (60.25 to 68.9] | 250 | -1.38 | -1.15 |
| Q4 (68.9 to 102.9] | 250 | -6.51 | -6.25 |

![score_gain versus pre_score, one point per student](tasks/eda_1/charts/score_gain_vs_pre_score.png)

**extra_sessions:** The association is moderate and positive. Pearson r = 0.368 (95% CI 0.313 to 0.421, p = 2e-33). Spearman rho = 0.363. The slope is 9.76 points per extra session (95% CI 8.23 to 11.29). Students with at least one extra session gain 9.76 more points than those with none (Welch t = 12.10, df = 403.9, p = 6e-29; 95% CI 8.17 to 11.34; Cohen's d = 0.91). These figures are unadjusted and describe an association, not a causal effect. The group means are 7.32 (n = 250, one session) and -2.44 (n = 750, none).

**attendance_pct:** The association is weak to moderate and positive. Pearson r = 0.291 (95% CI 0.233 to 0.347, p = 6e-21). Spearman rho = 0.278. The slope is 0.23 points per percentage point (95% CI 0.18 to 0.28). Mean score_gain rises across attendance quartiles: Q1 (50 to 62.8] mean -4.39, Q2 (62.8 to 75.6] mean -1.16, Q3 (75.6 to 87.95] mean 1.17, Q4 (87.95 to 100] mean 4.42.

**age:** No significant association. Pearson r = 0.021 (p = 0.51), Spearman rho = 0.027 (p = 0.39), slope 0.21 per year (95% CI -0.42 to 0.84). Holm-adjusted p = 1.0. Mean score_gain by age (15 to 18) ranges only from -0.42 to 0.36.

**class_size:** No significant association. Pearson r = -0.016 (p = 0.62), slope -0.04 per student (95% CI -0.21 to 0.12). Holm-adjusted p = 1.0. Quartile means lie between -0.31 and 0.58.

### Joint distribution of extra_sessions and pre_score (eda_3)

Every extra_sessions=1 student falls in the lowest pre_score quartile. Q1 has 250 students with extra_sessions=1 and 0 with extra_sessions=0 (share 100%). Q2, Q3 and Q4 each have 250 students with extra_sessions=0 and none with extra_sessions=1 (share 0%). The lowest pre_score quartile and the extra_sessions=1 group are identical sets of students. The extra_sessions correlation with pre_score is -0.736 (stat_3).

This check resolves the confounding concern raised in eda_1: the two groups coincide, so the eda_1 extra_sessions difference (7.32 vs -2.44) cannot be separated from pre_score within this sample, because the groups have no pre_score overlap.

![Students per pre_score quartile, stacked by extra_sessions: the extra_sessions=1 group is exactly Q1.](tasks/eda_3/charts/eda3_crosstab.png)

### Adjusted association of extra_sessions (stat_3)

In an OLS model of score_gain on all five numeric features (n = 1,000; R² = 0.289, adjusted R² = 0.285), the extra_sessions coefficient falls from 9.76 (unadjusted) to 1.77 points per session (95% CI -0.29 to 3.82, p = 0.092), a change of -7.99. It is not significant at the 0.05 level.

Other coefficients from the same model:

| Feature | Coefficient | 95% CI | p |
|---|---|---|---|
| pre_score | -0.347 | -0.414 to -0.280 | < 0.001 |
| attendance_pct | 0.213 | 0.171 to 0.254 | < 0.001 |
| age | 0.351 | -0.186 to 0.887 | 0.20 |
| class_size | -0.023 | -0.162 to 0.116 | 0.75 |

Only pre_score and attendance_pct are significant after adjustment. Because no extra_sessions=0 student shares a pre_score value range with the extra_sessions=1 group, the adjusted 1.77 depends entirely on the assumed linear functional form and cannot be checked against comparable students. It should be treated as fragile.

### Interactions (stat_2)

No significant interaction was found.
- pre_score × extra_sessions: coefficient -0.025 (95% CI -0.214 to 0.163, p = 0.79).
- attendance_pct × extra_sessions: coefficient -0.019 (95% CI -0.116 to 0.078, p = 0.70).
- Joint Wald test of both: F = 0.103, p = 0.90 (model R² = 0.288, n = 1,000).

Within-group slopes are similar across extra_sessions groups. For pre_score: -0.343 (95% CI -0.414 to -0.272) when extra_sessions = 0 (n = 750) and -0.368 (95% CI -0.557 to -0.179) when extra_sessions ≥ 1 (n = 250). For attendance_pct: 0.217 (95% CI 0.171 to 0.264) and 0.198 (95% CI 0.107 to 0.290).

The confidence intervals exclude only large slope changes (roughly more than 0.16 points per pre_score point, or more than 0.08 points per attendance percentage point). This does not prove the absence of effect modification; it means the data do not show one at this sample size. Because the extra_sessions=1 group lies entirely within the lowest pre_score quartile, the interaction is weakly identified.

### Predictive performance (ml_1)

All models used the five numeric features, an 80/20 split (800 training, 200 test rows), and random_state = 42.

| Model | Train R² | Test R² | Test RMSE | Test MAE |
|---|---|---|---|---|
| Mean baseline | n/a | -0.004 | 10.62 | 8.84 |
| Linear regression | 0.308 | 0.184 | 9.58 | 7.75 |
| Gradient boosting | 0.555 | 0.104 | 10.03 | 8.03 |

Linear regression beats the baseline on the test set. Gradient boosting does worse than linear regression on test data and overfits more (train-test gap of 0.45 versus 0.12). The linear model's overfit gap is modest.

Permutation importance on the test set for the linear model (drop in R² when shuffled, 30 repeats):
- pre_score: 0.249 (SD 0.061)
- attendance_pct: 0.158 (SD 0.044)
- age: 0.005 (SD 0.004)
- class_size: 0.000 (SD 0.000025)
- extra_sessions: -0.006 (SD 0.017), so it adds no unique predictive contribution once the other features are included.

The linear model's absolute-coefficient ranking (extra_sessions 2.90 first) depends on scale, since extra_sessions is 0/1, and is not a measure of importance.

![Permutation feature importance on the 200-student test set for the linear regression predicting score_gain; bars show mean drop in R² with SD over 30 shuffles.](tasks/ml_1/charts/ml_1_permutation_importance.png)

### Missing values (eda_2)

No column has missing values: 0 of 1,000 rows (0.0%) for each of the six columns, and 0 missing cells in total. Because nothing is missing, no comparison of missing and present rows was run.

## Limitations

- **Observational data.** All associations are observational. None of the findings supports a causal reading of extra_sessions or any other feature.
- **Extra sessions and pre_score are not separable.** The eda_1 concern that extra sessions were assigned by pre_score is confirmed by eda_3: the two groups coincide exactly. The unadjusted extra_sessions effect (9.76) and the adjusted one (1.77) therefore cannot be cleanly attributed to extra sessions versus pre_score. The adjusted estimate depends on the linear form and is not significant at 0.05 (p = 0.092).
- **Interaction tests are weakly identified.** The interaction null result (p = 0.90) is not evidence of no effect modification, and the interaction terms cannot be estimated over the pre_score range where extra_sessions=1 students lie.
- **Linearity not tested.** The pre_score and attendance_pct relationships are summarised with linear slopes and quartile means. Whether the pre_score relationship is linear or partly reflects regression to the mean was not tested.
- **Model evaluation is limited.** The ML results rest on a single 80/20 split with a 200-row test set. Test-set differences between models (for example 9.58 versus 10.03 RMSE) are based on that single split. Regularised models and cross-validation were not run, so the train/test gap is not addressed.
- **Unadjusted results.** The marginal correlations and group comparisons (eda_1, stat_1) are not adjusted for other features and should not be read as independent effects.
- **Failed tasks.** None. All four analysis tasks (eda_1, stat_1, stat_2, ml_1) and the three supporting checks (eda_2, eda_3, stat_3) are complete and accepted.

## Open questions

- What process assigned extra_sessions, and was it based on pre_score? The data show the assignment but do not explain it, and this is required before any causal reading of the extra_sessions coefficient.
- Does the extra_sessions effect differ by pre_score level? This cannot be estimated from this data because there is no pre_score overlap between the groups; a design-based check is needed.
- Is the negative pre_score relationship linear, or does it partly reflect regression to the mean? A nonlinear term or spline would test whether the adjusted extra_sessions estimate depends on functional form.
- Does attendance_pct explain any of the score_gain difference between the extra_sessions groups? This was raised but not tested.
- Would regularised models or cross-validation narrow the train/test gap in both models?
- With a larger sample, would the interaction confidence intervals narrow enough to rule out small but meaningful differences in slope?