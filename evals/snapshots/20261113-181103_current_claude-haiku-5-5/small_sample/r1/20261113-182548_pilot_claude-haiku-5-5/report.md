# Analysis Report: Predictors of `score` in a 60-Row Dataset with Six Numeric Features

## Summary

- **feat_1 is the only feature with a robust relation to score.** Pearson r = 0.41 (95% CI 0.18 to 0.60, p = 0.0011, BH-adjusted p = 0.0067). The high-minus-low tertile difference is 11.69 points (95% CI 4.72 to 18.67, Cohen's d = 1.07), and it survives correction.
- **No model beat the mean baseline on the single 15-row test split.** The mean-of-train baseline had test RMSE 9.88. Linear regression (10.35), random forest (11.73) and gradient boosting (11.44) were all worse.
- **A feat_1-only linear model did beat the baseline more often than not across repeated splits.** Its test RMSE was lower on 38 of 50 random 75/25 splits (76%), with mean RMSE 10.52 against 11.32. The margin is small relative to the split-to-split spread.
- **feat_3 and feat_6 are weak and not significant after correction.** feat_3 has r = -0.24 (p = 0.063). Controlling for feat_1 leaves its partial r at -0.25 (BH-adjusted p = 0.117). feat_6's partial r falls to -0.11 (p = 0.40). Neither is confounded with feat_1 or with each other.
- **No interaction was significant.** Of the five tested pairwise terms, the smallest BH-adjusted p is 0.4351. The other ten pairs were not tested.

## Data

- 60 rows and 7 columns: the target `score` and six numeric features, `feat_1` to `feat_6`.
- No categorical, date/time, identifier or free-text columns.
- No missing values in any column.

## Findings

### Score distribution and univariate relations

Score is roughly symmetric and unimodal. Mean is 48.95, median 48.75, sd 11.22, range 25.3 to 75.6, skew -0.15. The histogram peaks around 46 to 50.

![Histogram of score across the 60 rows](tasks/eda_1/charts/score_histogram.png)

- **feat_1:** Pearson r = 0.41 (p = 0.001); Spearman rho = 0.47 (p = 0.0001). Mean score by feat_1 tertile is 41.7 (low), 51.7 (middle) and 53.4 (high). The jump occurs from low to middle, and the middle-to-high step is small.
- **feat_3:** Pearson r = -0.24 (p = 0.063); Spearman rho = -0.21 (p = 0.12). Tertile means are 51.5 (low) and 45.9 (high). Not significant.
- **feat_6:** Pearson r = -0.16 (p = 0.21); Spearman rho = -0.20 (p = 0.12). Not significant.
- **feat_2, feat_4, feat_5:** all |Pearson r| ≤ 0.09 and |Spearman rho| ≤ 0.08, none significant (p ≥ 0.50). Tertile means stay within about 47 to 51.

### Statistical significance and effect sizes

Correlations are with 95% Fisher-z CIs; tertile comparisons are high versus low, with Welch CIs.

![Difference in mean score between the high and low tertile of each feature, with 95% Welch CI. Only feat_1 excludes zero, and it survives BH correction.](tasks/stat_1/charts/tertile_mean_differences.png)

- **feat_1:** r = 0.41 (95% CI 0.18 to 0.60, p = 0.0011, BH p = 0.0067). Tertile difference 11.69 (95% CI 4.72 to 18.67; t-test p = 0.0016, BH p = 0.0098; Mann-Whitney p = 0.0015; d = 1.07). This is the only result that survives Benjamini-Hochberg correction across the six features, on both tests.
- **feat_3:** r = -0.24 (95% CI -0.47 to 0.01, p = 0.063, BH p = 0.19). Tertile difference -5.57 (95% CI -12.53 to 1.38; t-test p = 0.11, BH p = 0.34; Mann-Whitney p = 0.27; d = -0.51). Neither test survives correction.
- **feat_6:** r = -0.16 (95% CI -0.40 to 0.09, p = 0.21, BH p = 0.42). Tertile difference -3.37 (95% CI -9.28 to 2.53; t-test p = 0.25; d = -0.37). Not significant.
- **feat_2, feat_4, feat_5:** |r| ≤ 0.09, BH-adjusted p ≥ 0.67, tertile CIs span zero, |d| ≤ 0.18.

### Confounding and partial correlations

- feat_3 and feat_6 are essentially uncorrelated with feat_1 and with each other: feat_1–feat_3 r = -0.04 (p = 0.76); feat_1–feat_6 r = -0.15 (p = 0.24); feat_3–feat_6 r = -0.05 (p = 0.71).
- **feat_3 controlling for feat_1:** partial r = -0.25 (95% CI -0.47 to 0.01, raw p = 0.059, BH p = 0.117 across the two partial tests). This is essentially unchanged from the raw r, but it does not survive correction at 0.05.
- **feat_6 controlling for feat_1:** partial r = -0.11 (95% CI -0.36 to 0.15, p = 0.40). It weakens from the raw r of -0.16 and is not significant.

### Interactions

Five pairwise interaction terms were tested: the top five by absolute correlation out of 15 possible pairs. OLS coefficients are on centred features.

| Term | Coefficient | 95% CI | Raw p | BH p | Bonferroni p |
|---|---|---|---|---|---|
| feat_2 × feat_5 | 4.15 | -0.63 to 8.93 | 0.087 | 0.4351 | 0.4351 |
| feat_1 × feat_5 | 2.39 | -2.20 to 6.99 | 0.3004 | 0.7511 | 1.0 |
| feat_4 × feat_6 | -0.17 | -3.25 to 2.90 | 0.9096 | 0.9096 | 1.0 |
| feat_1 × feat_6 | -0.33 | -3.01 to 2.36 | 0.8074 | 0.9096 | 1.0 |
| feat_2 × feat_6 | -0.67 | -3.30 to 1.97 | 0.6138 | 0.9096 | 1.0 |

None is significant. The largest estimate, feat_2 × feat_5, has a CI that includes zero, so the data are compatible with an interaction of that size and with none. The six-feature-plus-five-interaction OLS model has R² = 0.33 on the full 60 rows. This is in-sample and was not evaluated on held-out data.

### Predictive models

All held-out results come from a single shared 15-row test set (45 training rows) unless stated otherwise.

| Model | Test RMSE | Test R² | Train R² |
|---|---|---|---|
| Mean-of-train baseline | 9.88 | -0.001 | 0.00 |
| Linear regression (six standardized features) | 10.35 | -0.097 | 0.32 |
| Random forest | 11.73 | -0.410 | 0.78 |
| Gradient boosting | 11.44 | -0.340 | 0.95 |

- The linear model overfits the training rows. Its five-fold CV RMSE on training data was 11.82 (sd 3.69), with one fold at 18.32 against 9.35 to 11.20 for the others. The baseline's CV RMSE was 11.64 (sd 2.05).
- **Model choice: the criteria disagree.** Random forest had the lower five-fold CV RMSE on training data (10.85, sd 3.35) against gradient boosting (11.16, sd 3.35), so it was the preferred model. Gradient boosting had the lower test RMSE (11.44 against 11.73). The difference is small relative to fold spread. Neither model beat the baseline on the test set.
- **Feature importance is unstable.** Impurity importance ranks feat_1 first for both tree models (0.44 random forest; 0.38 gradient boosting). Permutation importance on the test set ranks feat_3 first for both (random forest RMSE increase 0.11, sd 0.19; gradient boosting 1.72, sd 0.77). feat_1 is second for both (sd 0.92 and 1.15). The sd values are of the same order as the means, so these rankings are not reliable. On the test set, the models do not clearly recover the feat_1 signal.
- **Linear coefficients (standardized):** feat_1 has the largest absolute coefficient (5.36), followed by feat_3 (2.82). With 45 training rows, these are unreliable.

![Test-set RMSE of random forest, gradient boosting, linear regression and mean baseline](tasks/ml_2/charts/ml2_test_rmse.png)

![Test-set RMSE of random forest, gradient boosting, linear regression and mean-of-train baseline on 15 test rows](tasks/ml_2/charts/ml2_test_rmse_v2.png)

### feat_1-only model across repeated splits

Across 50 random 75/25 splits, the feat_1-only linear model had lower mean test RMSE than the mean-of-train baseline: 10.52 (sd 1.90) against 11.32 (sd 1.80). Its RMSE was lower on 38 of 50 splits (76%). Mean test R² was 0.047 (sd 0.231) for the linear model and -0.092 (sd 0.133) for the baseline. The linear model's R² is negative on many splits.

![Test RMSE across 50 random 75/25 splits for the feat_1 linear model and the mean-of-train baseline](tasks/ml_3/charts/ml3_rmse_boxplot.png)

The single-split result in the six-feature model (worse than baseline) is not a test of feat_1 alone. It does show that single-split comparisons vary considerably.

## Limitations

- **Small sample.** With 60 rows, a 15-row test set gives unstable comparisons. Several conclusions depend on split choice (see the repeated-split result above). The interaction tests have low power.
- **No model beat the baseline on the shared test split.** Model rankings on that split are not reliable.
- **Overfitting.** Both tree models reach train R² of 0.78 and 0.95 but test R² of -0.41 and -0.34. The linear model's CV error varies widely by fold.
- **Unstable feature importance.** Impurity and permutation rankings disagree, and permutation standard deviations are of the same order as their means.
- **Model-selection disagreement.** Random forest was preferred on CV RMSE; gradient boosting had the lower test RMSE. Both are reported without resolution.
- **Multiple-testing corrections.** feat_3's effect does not survive BH correction. Its evidence is borderline and is reported as suggestive only.
- **Interaction scope.** Only five of 15 pairs were tested. The other ten, including feat_1 × feat_3, feat_1 × feat_2 and feat_1 × feat_4, are unknown.
- **Non-linearity not tested.** The feat_1 tertile pattern (a jump from low to middle, then flattening) was not tested against a linear fit.
- **Tertile means differ between tasks.** The low-tertile means for feat_4 (48.99 in the EDA task, 49.91 in the statistics task) and feat_6 (50.96 against 51.31) disagree. The statistics task uses 21 rows in these low groups, against 20 in the EDA task. This was not resolved.
- **Failed tasks:** none.

## Open questions

- Does feat_1 remain the strongest predictor in a multivariate model, and does feat_3 add predictive value beyond feat_1? The repeated-split comparison of feat_1 alone against feat_1 plus feat_3 has not been run.
- Is the feat_1 relation linear or threshold-like, as the tertile pattern suggests?
- Is the RMSE advantage of the feat_1 model statistically significant when tested on paired split differences? The 50 splits share training data, so they are not independent.
- Do repeated splits or nested CV show any model beating the mean baseline on held-out data?
- Would a heavily regularized model (a shallow forest or ridge regression) reduce the overfitting and stabilize the feature ranking?
- Would a larger sample, or a pre-specified test of feat_1 × feat_3, change the interaction conclusion?