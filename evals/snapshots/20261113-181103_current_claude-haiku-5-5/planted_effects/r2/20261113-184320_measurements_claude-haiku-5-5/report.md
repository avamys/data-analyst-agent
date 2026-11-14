# Outcome Analysis of a 1,000-Row Dataset with a Binary Target (outcome)

## Summary

- **Strongest signal: feat_a.** Outcome-1 rates rise across its quintiles from 9.0% (Q1) to 76.0% (Q5). Its class difference is large (mean 0.544 for outcome 1 vs -0.379 for outcome 0; Cohen's d 1.046), and logistic regression ranks it first by permutation importance (test ROC AUC drops 0.226 when shuffled).
- **feat_d is a medium-sized, weaker-supported signal.** Its class difference is significant (Cohen's d 0.571, Holm p = 1.8e-14). Whether its association is curved is unresolved: one single-df test is nominally significant (p = 0.037), while the joint, spline and trimmed-sample tests are not.
- **feat_b is significant but small; feat_c shows no association.** feat_b's class difference is significant after correction (Cohen's d 0.296), but its outcome rates are non-monotone. feat_c's class difference is 0.004 (95% CI -0.124 to 0.132).
- **No interactions were detected.** The smallest raw interaction p-value across six pairs is 0.150, and the feat_a × feat_d and feat_c × feat_d estimates have confidence intervals that include zero.
- **Model performance:** logistic regression reaches test ROC AUC 0.817 and accuracy 0.750, against 0.500 and 0.605 for the majority-class baseline. Gradient boosting overfits and scores lower (test ROC AUC 0.763). These are single-split results on 200 test rows. The feat_b coefficient-versus-importance conflict is unresolved (see Limitations).

## Data

- **Size:** 1,000 rows, 5 columns: four numeric features (feat_a, feat_b, feat_c, feat_d) and a binary target, outcome. There are no categorical, date/time, identifier or free-text columns.
- **Target:** outcome = 0 for 60.3% of rows and outcome = 1 for 39.7%.
- **Missing values:** feat_d is missing in 150 of 1,000 rows (15.0%). No other column has missing values.

## Findings

### Distributions of the target and numeric features

All four numeric features are close to standard normal, with means near zero, standard deviations between 0.99 and 1.02, and skew between -0.10 and 0.08.

Summary statistics (mean / median / sd / min / max / skew):
- feat_a: -0.013 / 0.056 / 0.990 / -3.331 / 3.134 / -0.095
- feat_b: 0.062 / 0.051 / 1.016 / -3.066 / 3.669 / -0.003
- feat_c: -0.006 / -0.054 / 1.013 / -3.370 / 3.297 / 0.080
- feat_d (non-missing): 0.047 / 0.052 / 1.000 / -3.047 / 3.276 / 0.023

Histograms of each feature split by outcome:

![Histograms of feat_a to feat_d (row counts) split by outcome 0 and 1; feat_d excludes missing rows](tasks/eda_1/charts/hist_by_outcome.png)

### feat_d missingness

- Missingness is not clearly related to the outcome or to the other numeric features. The outcome-1 rate is 41.3% when feat_d is missing (n = 150) and 39.4% when present (n = 850), a difference of +1.9 points. The chi-square p-value is 0.72 with Yates correction (the value reported by the eda_1 task). The uncorrected chi-square (stat_1) gives chi2 = 0.197, p = 0.657. Both tests give the same conclusion. The odds ratio for missing vs present is 1.08 (95% CI 0.76 to 1.54).
- Mean feature values, missing vs present, with Welch p-values:
  - feat_a: -0.073 vs -0.002 (difference -0.071, p = 0.42)
  - feat_b: 0.128 vs 0.050 (difference +0.078, p = 0.40)
  - feat_c: 0.009 vs -0.009 (difference +0.018, p = 0.83)
- No difference is significant at the 0.05 level.

### Outcome rate across each feature's range

Outcome-1 rate by quintile (Q1 lowest, Q5 highest), each bin n = 200 unless noted:

| Feature | Q1 | Q2 | Q3 | Q4 | Q5 |
|---|---|---|---|---|---|
| feat_a | 9.0% | 25.0% | 39.5% | 49.0% | 76.0% |
| feat_b | 25.9% (n=201) | 39.5% | 43.7% (n=199) | 39.5% | 50.0% |
| feat_c | 40.0% | 41.6% (n=202) | 39.9% (n=198) | 35.5% | 41.5% |
| feat_d | 24.7% (n=170) | 30.0% (n=170) | 34.7% (n=170) | 44.1% (n=170) | 63.5% (n=170) |

- feat_a rises at every step.
- feat_b is not monotone. Its rates go 25.9%, 39.5%, 43.7%, 39.5%, 50.0%.
- feat_c shows no meaningful relation to the outcome, with bin rates between 35.5% and 41.6%.
- feat_d rises across its quintiles. Its missing-value rows have a 41.3% outcome-1 rate, which lies within the range of the present-value bins. The table excludes feat_d-missing rows.

![Outcome-1 rate (share of rows) by quantile bin of each numeric feature; feat_d missing rows excluded from the lines](tasks/eda_2/charts/outcome_rate_by_bin.png)

### Differences between outcome classes

| Feature | Mean (outcome 0) | Mean (outcome 1) | Difference (95% CI) | Cohen's d | Welch p (Holm p) | Mann-Whitney p (Holm p) |
|---|---|---|---|---|---|---|
| feat_a | -0.379 | 0.544 | 0.922 (0.812 to 1.032) | 1.046 | 2.3e-53 (9.3e-53) | 8.1e-48 (3.2e-47) |
| feat_b | -0.057 | 0.241 | 0.298 (0.171 to 0.425) | 0.296 | 4.5e-06 (9.0e-06) | 5.0e-06 (1.0e-05) |
| feat_c | -0.008 | -0.004 | 0.004 (-0.124 to 0.132) | 0.004 | 0.951 (0.951) | 0.899 (0.899) |
| feat_d (n=850) | -0.170 | 0.381 | 0.551 (0.415 to 0.686) | 0.571 | 6.0e-15 (1.8e-14) | 1.8e-14 (5.3e-14) |

- feat_a and feat_d show a large and medium difference, respectively, and both remain significant after Holm correction across the four features.
- feat_b is significant but small (Cohen's d 0.296).
- feat_c is not significant. Its confidence interval rules out differences larger than about 0.13 standard deviations.

![Mean of each feature for outcome 0 vs outcome 1; feat_d excludes missing rows](tasks/stat_1/charts/class_means.png)

### Interactions

- No pairwise interaction term is significant (complete cases, n = 850; six pairs; Holm-adjusted p-values 0.899 to 1.0).
- Largest estimate: feat_c × feat_d, coefficient 0.122 (95% CI -0.044 to 0.288), raw p = 0.150.
- Second: feat_a × feat_d, coefficient -0.119 (95% CI -0.333 to 0.094), raw p = 0.273.
- Median-split 2×2 table of outcome-1 rates (feat_a × feat_d):
  - feat_a low, feat_d low: 13.1%
  - feat_a low, feat_d high: 30.8%
  - feat_a high, feat_d low: 47.4%
  - feat_a high, feat_d high: 66.4%
- Within each half of feat_d, the outcome rate rises with feat_a, and the feat_a slopes are reported as similar across the two halves. The confidence intervals for these slopes are wide. The result is consistent with no modification but does not rule out moderate interaction.

### Predictive performance

Method: one stratified split (800 training rows, 200 test rows; random_state 42). feat_d was median-imputed with a missing-indicator added. Logistic regression used scaled features. All models were trained on the training split only.

| Model | Test accuracy | Test ROC AUC | Test log loss | Precision | Recall | F1 |
|---|---|---|---|---|---|---|
| Majority-class baseline | 0.605 | 0.500 | not meaningful | 0.0 | 0.0 | 0.0 |
| Logistic regression | 0.750 | 0.817 | 0.505 | 0.710 | 0.620 | 0.662 |
| Gradient boosting | 0.730 | 0.763 | 0.684 | 0.651 | 0.684 | 0.667 |

- Logistic regression outperforms the baseline and gradient boosting on the test set.
- Gradient boosting overfits: training accuracy is 0.999.
- The baseline's log loss (14.24) reflects constant extreme predictions, so it should not be compared with the fitted models.

![Test-set ROC AUC of the majority baseline, logistic regression and gradient boosting classifier](tasks/ml_1/charts/ml1_model_auc.png)

Permutation importance in the logistic regression (drop in test ROC AUC when shuffled, 30 repeats):
- feat_a: 0.226 (sd 0.035)
- feat_d: 0.085 (sd 0.018)
- feat_b: 0.002 (sd 0.009)
- feat_c: 0.001 (sd 0.001)
- feat_d_missing: -0.003 (sd 0.004)

Standardised logistic coefficients (absolute): feat_a 1.251, feat_d 0.610, feat_b 0.375, feat_d_missing 0.137, feat_c 0.025. The feat_b coefficient conflicts with its permutation importance; see Limitations.

### Linearity on the logit scale (feat_a and feat_d)

- **Joint quadratic test (both variables, 2 df):** LR = 4.35, p = 0.113. AIC is 867.3 for the quadratic model vs 867.7 for linear.
- **Cubic regression spline (4 df each vs linear):** LR = 4.37 on 4 df, p = 0.36. AIC is 871.3 for the spline vs 867.7 for linear, so the linear model is preferred.
- **Trimmed sample (1st to 99th percentile, n = 814):** quadratic LR = 3.17 on 2 df, p = 0.205. AIC is 837.5 for linear vs 838.4 for quadratic.
- **Linear odds ratios per unit:** feat_a 3.61 (full) and 3.73 (trimmed); feat_d 2.07 (full) and 2.08 (trimmed).

Odds ratio by value of feat_a (quadratic logit, full sample): 3.71 at the 10th percentile, 3.48 at the 90th. The confidence interval widens at the tails (1.84 to 6.56 at the 90th percentile).

Odds ratio by value of feat_d (quadratic logit, full sample, without feat_b and feat_c): 1.66 (95% CI 1.28 to 2.16) at the 10th percentile and 3.28 (95% CI 2.02 to 5.32) at the 90th percentile.

![Odds ratio per +1 unit of feat_a and feat_d across their values: quadratic logit (solid) vs linear logit (dashed), non-missing rows](tasks/stat_3/charts/stat3_or_curves.png)

### Curvature: separate tests and verdict

- **feat_a quadratic term:** not supported (LR = 0.019, p = 0.891; adjusted for feat_b, feat_c, feat_d and feat_d squared; n = 850).
- **feat_d quadratic term:** nominally significant in one separate single-df test (LR = 4.35 on 1 df, p = 0.037; adjusted for feat_a, feat_b, feat_c and feat_a squared; n = 850).
- **These results disagree.** The single-df feat_d test (p = 0.037) conflicts with the joint test (p = 0.113), the spline test (p = 0.36) and the trimmed-sample test (p = 0.205), which do not reject linearity.
- **feat_d odds ratio change (adjusted model, n = 850):** the odds ratio per unit goes from 1.45 at the 10th percentile to 2.87 at the 90th. The change in log odds ratio is 0.682 (percentile bootstrap 95% CI -0.005 to 1.294; 1,000 resamples, no failures). 97.4% of bootstrap draws are above zero.
- **Verdict (stated by the analysis):** the feat_d gradient is not robustly supported. The evidence is suggestive, not conclusive, at n = 850. The odds ratios here are not directly comparable with the 1.66 to 3.28 values above, because the two models differ in covariates and sample.

## Limitations

- **Missingness power:** only 150 feat_d rows are missing, so the missingness tests have limited power to detect a weak dependence.
- **Interactions:** the interaction tests use complete cases (n = 850). Confidence intervals for the largest estimates include zero, so moderate interactions are not ruled out. Interaction models were not fitted with splines or thresholds.
- **Curvature:** the feat_d curvature result is not robust across specifications. Its odds ratio estimates depend on whether feat_b and feat_c are included (1.66 to 3.28 without them; 1.45 to 2.87 with them, on a different sample). The tail confidence intervals are wide.
- **feat_b, unresolved review issue:** the logistic coefficient for feat_b (0.375) is the third largest, yet its permutation importance is 0.002 (sd 0.009). The reviewer's objection stands. The analysis has not reconciled these, and this report does not explain the discrepancy. The permutation result supports only that shuffling feat_b changed test ROC AUC by 0.002. It does not support calling feat_b unrelated to the outcome, since stat_1 found a significant, small marginal association (Cohen's d 0.296, Holm p = 9.0e-06).
- **Model validation:** all model scores come from one 200-row test split. Gradient boosting was not tuned. Results may vary with another split.
- **Causality:** the analysis reports associations only.
- **Failed tasks:** none. All seven tasks (eda_1, eda_2, stat_1, stat_2, stat_3, stat_4, ml_1) completed.

## Open questions

- Does feat_a have a nonlinear effect that gradient boosting could capture with stronger regularisation or early stopping?
- Would tuning gradient boosting reduce its overfitting enough to beat the logistic model on the test set?
- Are feat_b and feat_c redundant once feat_a and feat_d are in the model?
- Does feat_b's non-monotone pattern reflect a threshold effect worth modelling separately?
- Do feat_a and feat_d interact in their effect on the outcome, with the association modelled non-linearly?
- Does the feat_c × feat_d interaction (the largest estimate, confidence interval -0.044 to 0.288) become significant with a larger sample or a more targeted model?
- Does the feat_d curvature hold on a larger sample, or in a model with a feat_a × feat_d interaction? Is it driven by a few extreme values, given the trimmed-sample test is not significant?
- Does feat_d missingness depend on combinations of features rather than on any single feature? Would a logistic model of the missingness indicator on all columns detect a weak dependence?
- Would imputing feat_d change model performance, and is the imputation choice sensitive to the small mean shift in feat_a?