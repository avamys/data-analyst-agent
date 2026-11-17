# Final Report: Predictors of score_gain in a 1,000-Student Dataset

## Summary

- **Target distribution:** score_gain is centred near zero and nearly symmetric (median -0.30, mean -0.00, SD 11.48, range -33.8 to 40.9). Outliers are rare: 0.6% of points fall outside the 1.5×IQR fences.
- **pre_score is the strongest numeric relation:** Pearson r = -0.46 (95% CI -0.51 to -0.41), with an OLS slope of -0.40 points per pre_score point and R² = 0.21. attendance_pct has a modest positive relation (r = 0.29, 95% CI 0.23 to 0.35; R² = 0.085).
- **The extra_sessions gap is large but confounded:** students with extra_sessions=1 score 9.76 points higher on average (95% CI 8.17 to 11.34), but their mean pre_score is 43.3 against 65.8 for extra_sessions=0. No adjusted estimate of the extra_sessions effect is reported in the findings.
- **A linear model beats the mean baseline on a 200-student hold-out:** test RMSE 9.65 versus 11.61, test R² 0.31 versus -0.00. Age and class_size add no out-of-sample predictive value.

## Data

- Size: 1,000 rows × 6 columns.
- Target: score_gain (continuous regression target).
- Features: five numeric features (pre_score, extra_sessions, attendance_pct, age, class_size). There are no categorical, date/time, identifier or free-text features.
- Missing values: none. The dataset has no empty cells, so missingness was not investigated.

## Findings

### Distribution of score_gain

score_gain is centred near zero and nearly symmetric: mean -0.00 (SD 11.48), median -0.30, quartiles -7.53 and 7.83, skew 0.11, range -33.8 to 40.9 (n = 1,000). Only 6 of 1,000 points (0.6%) fall outside the 1.5×IQR fences of -30.55 and 30.85, so the tails are not heavy.

![Histogram of score_gain across all 1,000 students](tasks/eda_1/charts/score_gain_hist.png)

### Relations with pre_score and attendance_pct

- **pre_score:** Pearson r = -0.46 (95% CI -0.51 to -0.41, p = 5e-54); Spearman rho = -0.45 (approximate 95% CI -0.50 to -0.40, p = 2e-50); n = 1,000. Each one-point increase in pre_score is associated with a score_gain change of -0.40 points (OLS 95% CI -0.45 to -0.35). pre_score explains about 21% of score_gain variance (R² = 0.213).
- **attendance_pct:** Pearson r = 0.29 (95% CI 0.23 to 0.35, p = 6e-21); Spearman rho = 0.28 (approximate 95% CI 0.22 to 0.34, p = 3e-19); n = 1,000. Each one-percentage-point increase is associated with a score_gain change of +0.23 points (OLS 95% CI 0.18 to 0.28). attendance_pct explains about 8% of score_gain variance (R² = 0.085).

![Scatter of score_gain against pre_score and attendance_pct with fitted OLS line](tasks/stat_1/charts/score_gain_vs_predictors.png)

### Differences by extra_sessions, age and class_size

**extra_sessions.** Students with extra_sessions=1 (n = 250) have higher score_gain than those with extra_sessions=0 (n = 750). Means are 7.32 (median 8.05) versus -2.44 (median -2.80). The Welch t-test gives p = 5.7e-29, the mean difference is 9.76 points (95% CI 8.17 to 11.34), and Cohen's d = 0.91. extra_sessions explains about 13.6% of score_gain variance (eta-squared 0.136). This is the largest group difference in the dataset. The section "Balance of pre_score and attendance_pct across extra_sessions groups" below shows that these groups differ strongly on pre_score.

**age.** No detectable difference. One-way ANOVA F = 0.22, p = 0.88; Kruskal-Wallis p = 0.70; eta-squared 0.0007. Group means are -0.42 (age 15, n = 263), -0.08 (16, n = 222), 0.36 (17, n = 270) and 0.11 (18, n = 245). Medians are -1.10, -1.05, 1.15 and -0.50, with no monotone trend.

**class_size.** No detectable difference. One-way ANOVA F = 1.04, p = 0.41; Kruskal-Wallis p = 0.49; eta-squared 0.015. Group means range from -2.80 (size 22, n = 54) to 3.49 (size 24, n = 68), with no clear ordering by size. The groups contain 54 to 73 students each. The swings may reflect sampling noise; this was not tested with a regression or a formal trend test.

![Mean score_gain with 95% CI by extra_sessions, age and class_size level](tasks/stat_2/charts/score_gain_means_by_group.png)

### Balance of pre_score and attendance_pct across extra_sessions groups

- **pre_score differs strongly.** extra_sessions=1 (n = 250) has mean 43.3 (median 44.6); extra_sessions=0 (n = 750) has mean 65.8 (median 64.4).
- **attendance_pct is similar.** extra_sessions=1 has mean 76.2 (median 75.8); extra_sessions=0 has mean 75.2 (median 75.6).
- Because pre_score differs this much between groups, the raw extra_sessions gap of 9.76 points is confounded by pre_score and may be partly or largely driven by it. Attendance does not appear to confound the comparison.
- The training-set correlation of extra_sessions with pre_score is -0.75 (n = 800). The machine learning analysis describes the raw gap as plausibly confounded by pre_score, but states that this is untested.

![Distribution of pre_score and attendance_pct for students with extra_sessions=0 versus 1](tasks/eda_2/charts/balance_pre_attendance_by_extra_sessions.png)

### Interactions

Neither interaction is supported.
- pre_score × extra_sessions coefficient: -0.020 (95% CI -0.21 to 0.17, p = 0.84).
- pre_score × attendance_pct coefficient: -0.0005 per percentage point (95% CI -0.0037 to 0.0027, p = 0.77).
- These come from an OLS model with R² = 0.288 and n = 1,000.

The pre_score slope is similar across groups:
- extra_sessions=0: -0.35 (95% CI -0.43 to -0.28, n = 750).
- extra_sessions=1: -0.40 (95% CI -0.60 to -0.21, n = 250).
- Attendance tertiles (low, middle, high): -0.39, -0.38 and -0.40, with overlapping CIs.

### Nonlinearity and regression to the mean

- **Nonlinearity:** None detected. The pre_score quadratic term has coefficient 0.00032 (p = 0.81). The attendance_pct quadratic term has coefficient 0.00054 (p = 0.74). The joint F test of both gives F = 0.08, p = 0.92.
- **Quintile means:** score_gain falls steadily with pre_score across quintiles (7.91, 1.88, -0.01, -2.72, -7.23, lowest to highest). It rises steadily with attendance_pct (-4.97, -2.04, 0.34, 2.14, 4.56).

![score_gain against pre_score, coloured by extra_sessions group (0 or 1)](tasks/stat_4/charts/stat4_gain_vs_pre_by_extra.png)

- **Adjusted pre_score slope:** -0.35 (95% CI -0.41 to -0.28) after adjusting for attendance_pct and extra_sessions. This is close to the unadjusted -0.40, so the linear slope holds after adjustment.
- **Within-group slopes:** -0.354 (95% CI -0.428 to -0.279) for extra_sessions=0; -0.402 (CI lower bound -0.597) for extra_sessions=1. The negative slope is not an artifact of group composition.
- **Regression to the mean:** The implied post-on-pre slope is 1 + slope = 0.65. Reading this as pre_score reliability requires a pure measurement-error model, which cannot be checked because no test-retest data are available. Regression to the mean therefore cannot be confirmed, and a real pre-dependent gain cannot be ruled out.
- **Spearman intervals:** The stat_1 Spearman intervals are approximate. A percentile bootstrap (2,000 resamples) gives a pre_score Spearman interval of -0.50 to -0.39, close to the stat_1 interval.

### Predictive models

Setup: five numeric features, 80/20 split (800 training, 200 hold-out), random_state 0. The mean baseline has test RMSE 11.61 and test R² -0.00.

| Model | Train R² | Test R² | Test RMSE | Test MAE |
|---|---|---|---|---|
| Mean baseline | 0.00 | -0.00 | 11.61 | 9.34 |
| Linear regression | 0.28 | 0.31 | 9.65 | 7.70 |
| Gradient boosting | 0.53 | 0.25 | 10.06 | 8.05 |

- Linear regression beats the baseline meaningfully. Gradient boosting also beats it but is weaker and overfits (train R² 0.53 against test R² 0.25).
- **Permutation importance (drop in test R²):** pre_score is the most important feature in both models (0.376 linear, sd 0.051; 0.384 gradient boosting, sd 0.052). attendance_pct is second (0.164 linear, sd 0.027; 0.156 gradient boosting, sd 0.040). extra_sessions scores 0.007 (linear, sd 0.004) and 0.0 (gradient boosting).
- **Age and class_size:** Permutation importances are zero or negative in both models. Age is -0.0015 (linear) and -0.0043 (gradient boosting). class_size is -0.0008 (linear) and -0.0148 (gradient boosting). Shuffling these features does not reduce test R².
- **Coefficients per 1 SD (training set):** pre_score -4.90, attendance_pct 2.80, age 0.54, extra_sessions 0.39, class_size 0.07.
- **Disagreement on ranking:** The raw linear coefficient ranking puts extra_sessions (0.89) and age (0.47) at the top. The permutation importances and per-SD coefficients put pre_score and attendance_pct first. The raw ranking reflects units and is not an importance ranking. The report does not resolve this further; the permutation results are the ones the analysis used to judge predictive importance.

![Test RMSE of score_gain for the mean baseline, linear regression and gradient boosting on the 200-student hold-out set](tasks/ml_1/charts/ml_1_model_rmse.png)

## Limitations

- **Confounding of extra_sessions:** The 9.76-point extra_sessions gap is confounded by pre_score (the group means are 43.3 and 65.8). No adjusted extra_sessions effect is reported in any finding, so the size of the effect after adjustment is unknown.
- **Causal direction of pre_score:** The negative pre_score relation may partly reflect regression to the mean. This cannot be confirmed without test-retest data for pre_score.
- **Small groups and class_size:** Class_size group means (54 to 73 students each) show swings that may be sampling noise. No formal trend test was run.
- **Approximate Spearman intervals:** The stat_1 Spearman intervals are approximate. The bootstrap check agrees closely for pre_score; the attendance_pct bootstrap was reported as a value, not as a separate check.
- **Single hold-out split:** Model scores come from one 80/20 split (random_state 0). Stability across splits was not checked, so the linear model's advantage over gradient boosting and the zero importance of age and class_size have not been confirmed across resamples.
- **Model scope:** The models use only the five numeric features. Results describe these features only, and the models explain roughly a quarter to a third of score_gain variance on the hold-out (test R² 0.25 to 0.31).
- **Unresolved review issues:** None were recorded as unresolved. All tasks are marked complete and accepted.
- **Failed tasks:** None.

## Open questions

- Does the extra_sessions gap of about 9.8 points persist after adjusting for pre_score and attendance_pct? The question was raised in several tasks, and no adjusted extra_sessions estimate was produced.
- Are extra_sessions students systematically different on pre_score, and does that difference account for the raw 9.76-point gap?
- Does class_size have a real effect on score_gain once adjusted for other variables, for example in a regression or a formal test across class sizes?
- Can pre_score reliability be estimated (for example from a retest), to quantify how much of the negative pre_score slope reflects regression to the mean?
- Does pre_score have a nonlinear relation with score_gain, such as a spline? The quadratic test found no curvature, but no spline was fitted.
- Are the linear model's advantage over gradient boosting and the zero importance of age and class_size stable under cross-validation across several random splits?