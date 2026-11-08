# Outcome Analysis of an 800-Row Survey (Binary Outcome, 41.1% Positive)

## Summary

- **No group or numeric-feature association survives correction.** The group chi-square is not significant (p = 0.289; BH-adjusted p = 0.637). No numeric feature shows a significant association with outcome after Benjamini-Hochberg (BH) adjustment. Within the stat_1 family, the smallest adjusted p-value is 0.637.
- **The feat_3 low-outcome pattern in its top quintile is not established.** Q5 has an outcome rate of 33.1%, against 42.5%, 42.2%, 45.3% and 42.5% in Q1 to Q4. The quintile chi-square is not significant (p = 0.223), and the linear trend is not significant (p = 0.133). The Q5 contrast is significant unadjusted (p = 0.022) but was chosen after viewing the data, and it does not survive adjustment. Its result also depends on the cut point used.
- **Predictive performance is at chance.** Neither logistic regression nor gradient boosting beats the majority-class baseline on the test split (55.0% and 53.1% against 58.75%). Cross-validated ROC AUC is 0.533 for logistic regression and 0.457 for gradient boosting, where 0.5 is chance.
- **Group does not change the feat_5 slope and does not explain outcome after adjustment.** The group × feat_5 interaction is not significant (p = 0.323), and the group effect after adjusting for feat_1 to feat_5 is not significant (p = 0.280). The model explains almost none of the outcome variation (McFadden R² = 0.0065).
- **The multiple-testing picture is not final.** The BH family could not be rerun on the full set of tests. The adjusted values in this report come from partial or provisional families, and they disagree across tasks. The conclusion that no feat_3 result is significant after adjustment holds under every version reported.

## Data

- 800 rows and 7 columns: one binary target (`outcome`), five numeric features (`feat_1` to `feat_5`) and one categorical column (`group`).
- Target classes: 0 at 58.9% and 1 at 41.1%.
- No missing values. No date/time features, identifiers or free text.
- The `group` column has **four** levels, g1 (n = 182), g2 (n = 206), g3 (n = 200) and g4 (n = 212). The task brief named three.

## Findings

### Outcome by group and by quintile of the numeric features

Outcome rates by group were g1 46.2%, g2 42.2%, g3 40.0% and g4 36.8% (eda_1). The Wilson 95% intervals overlap (g1 39.1% to 53.4%; g4 30.6% to 43.5%).

For each numeric feature, the outcome rate was computed by quintile (Q1 lowest). The quintile spread (maximum minus minimum) was largest for feat_3 at 0.122, followed by feat_1 (0.085), feat_4 (0.075), feat_5 (0.069) and feat_2 (0.063). The feat_3 quintile rates were 42.5%, 42.2%, 45.3%, 42.5% and 33.1%.

Mean differences between outcome groups were small. feat_5 is higher for outcome 1 (mean 0.092 against 0.001 for outcome 0). feat_3 is lower for outcome 1 (mean -0.027 against 0.055 for outcome 0). feat_1, feat_2 and feat_4 differ little.

![Outcome rate by group and by quintile of the strongest feature](tasks/eda_1/charts/eda1_outcome_rate_group_quintile.png)

*Note: eda_1 names feat_3 as the strongest feature by quintile spread. stat_2 names feat_5 as the strongest by absolute correlation with outcome (|r| = 0.044 by point-biserial). These are different criteria, and both are reported here.*

### Significance and effect sizes

- **Group:** chi-square = 3.754 (3 df), p = 0.289, Cramér's V = 0.068 (negligible). BH-adjusted p = 0.637 over the 11 stat_1 tests.

![Outcome rate by group with 95% Wilson intervals](tasks/stat_1/charts/stat1_outcome_rate_by_group.png)

- **feat_5:** mean difference (outcome 1 minus outcome 0) +0.091, 95% CI -0.050 to 0.233. Mann-Whitney p = 0.210. Rank-biserial 0.052. Point-biserial r = 0.044. BH p = 0.637.
- **feat_3:** mean difference -0.082, 95% CI -0.221 to 0.057. Mann-Whitney p = 0.179. Rank-biserial -0.056. Point-biserial r = -0.041. BH p = 0.637.
- **feat_1, feat_2, feat_4:** no association. Rank-biserial magnitudes are below 0.02 (feat_1 -0.014, feat_2 0.001, feat_4 0.007). Mean-difference intervals span zero. BH p = 0.978 for each.

Taken together, the stat_1 BH values are 0.637 for the group test and the feat_3 and feat_5 tests, and 0.978 for feat_1, feat_2 and feat_4 (as stated in stat_1). Note the conflict with the 17-test values in the Limitations.

### feat_3 Q5 pattern: trend, cut-point and spline tests

- **Quintiles (stat_4):** chi-square = 5.70 (4 df), p = 0.223. The linear trend across quintile scores gives OR = 0.926 per step (95% CI 0.838 to 1.024), p = 0.133. The continuous logistic term gives OR = 0.920 per unit of raw feat_3 (95% CI 0.798 to 1.060), p = 0.250. Q5 against Q1 to Q4 gives OR = 0.653 (95% CI 0.454 to 0.941), p = 0.022 unadjusted. The quintile rates are non-monotone, with Q3 the highest.
- **Tertiles (stat_5):** rates 40.4%, 46.2% and 36.7% (n = 267, 266, 267). Chi-square = 5.08 (2 df), p = 0.079. Trend OR = 0.926 per step (95% CI 0.779 to 1.100), p = 0.379. Top tertile against the rest OR = 0.758 (95% CI 0.560 to 1.026), p = 0.072.
- **Deciles (stat_5):** rates range from 32.5% to 46.9%, with no monotone pattern. Chi-square = 8.54 (9 df), p = 0.480. Trend OR = 0.966 per decile (95% CI 0.920 to 1.015), p = 0.169. Top decile against the rest OR = 0.663 (95% CI 0.406 to 1.082), p = 0.100.

![Outcome rate by feat_3 decile, 800 rows](tasks/stat_5/charts/stat5_decile_rates.png)

- **Spline (stat_5):** the omnibus likelihood-ratio test of a truncated cubic spline against linear is 9.70 (5 df), p = 0.084. Predicted rates are 44.5% at p10, 46.1% at p50 and 32.9% at p90. The post hoc p90 against p10 contrast gives OR = 0.611 (95% CI 0.390 to 0.958), p = 0.032, and a rate difference of -11.6 percentage points (95% CI -22.1 to -1.1), p = 0.030. This contrast was chosen after viewing the data and is not corrected for the omnibus test.
- **Continuous, adjusted (stat_3):** feat_3 OR = 0.918 per unit (95% CI 0.796 to 1.060), p = 0.244, after adjusting for feat_1 to feat_5.

**Conclusion:** the feat_3 low rate in the top quintile is a descriptive pattern. It is not significant under the quintile chi-square, the trend tests, the tertile or decile tests, or the spline omnibus. The only result under 0.05 is the post hoc spline contrast (p = 0.032 unadjusted), and it does not survive the provisional adjustment (see Limitations).

### Group effect after adjustment for the numeric features

Logistic regression of outcome on group and feat_1 to feat_5 (stat_3):

- Group likelihood-ratio test: chi-square = 3.832 (3 df), p = 0.280.
- g4 against g1 (reference): OR = 0.678 (95% CI 0.452 to 1.018), p = 0.061. This is the closest group contrast and is not significant at 0.05.
- g2 against g1: OR = 0.849 (95% CI 0.567 to 1.270), p = 0.425.
- g3 against g1: OR = 0.760 (95% CI 0.505 to 1.145), p = 0.189.
- Numeric features (ORs per unit): feat_1 0.998 (p = 0.978), feat_2 1.017 (p = 0.817), feat_4 1.003 (p = 0.965), feat_5 1.107 (95% CI 0.961 to 1.274, p = 0.158).
- Model fit: McFadden R² = 0.0065, LLR p = 0.537, against a baseline outcome rate of 41.1%.

### Group × feat_5 interaction

stat_2 standardized feat_5 and fitted outcome ~ x × group (g1 as reference):

- Interaction terms: g2 coefficient 0.024 (95% CI -0.377 to 0.424), p = 0.907; g3 0.231 (95% CI -0.176 to 0.639), p = 0.266; g4 0.325 (95% CI -0.094 to 0.744), p = 0.128.
- Joint likelihood-ratio test: chi-square = 3.485 (3 df), p = 0.323.

Split at the feat_5 median (0.0515), outcome rates were:

| Group | High half (n) | Low half (n) |
|---|---|---|
| g1 | 46.5% (86) | 45.8% (96) |
| g2 | 41.6% (101) | 42.9% (105) |
| g3 | 43.8% (105) | 35.8% (95) |
| g4 | 40.7% (108) | 32.7% (104) |

The low-half gap is descriptive. It is not supported by the interaction test.

![Outcome rate by group within low and high halves of feat_5 (split at median)](tasks/stat_2/charts/stat2_rate_by_group_half.png)

### Predictive models

Setup: features feat_1 to feat_5 plus one-hot group, stratified 80/20 split (160 test rows), seed 42.

- **Logistic regression:** test accuracy 55.0%, precision 0.313, recall 0.076, F1 0.122, ROC AUC 0.392. Training accuracy 58.6%.
- **Gradient boosting:** test accuracy 53.1%, precision 0.400, recall 0.273, F1 0.324, ROC AUC 0.467. Training accuracy 83.6%, which indicates overfitting.
- **Baseline:** majority-class accuracy is 58.75% on the test split and 58.9% on all 800 rows.
- **Five-fold stratified CV on all 800 rows:** ROC AUC 0.533 ± 0.040 for logistic regression and 0.457 ± 0.028 for gradient boosting. CV accuracy is 58.6% and 52.1%.

![Mean 5-fold CV ROC AUC per model, dashed line = chance](tasks/ml_1/charts/ml1_cv_auc.png)

- **Log loss:** on the test split, logistic regression scores 0.709 and gradient boosting 0.754, against 0.678 for a constant training-prior predictor. The 5-fold CV log loss is 0.677 (logistic regression) and 0.753 (gradient boosting). Neither model beats the constant predictor. No calibration analysis was run.
- **Feature importance:** feat_3 has the largest permutation importance in both models on the test set (ROC AUC drop 0.023 for logistic regression and 0.016 for gradient boosting). The other features contribute little. feat_5 and group g4 have negative drops in logistic regression, and feat_5 is negative in gradient boosting. The ranking is unstable on 160 rows, and the feat_3 signal is not confirmed by the association tests.

## Limitations

- **Four group levels, not three.** The data contains g1 to g4. The findings use all four.
- **Multiple-testing family is incomplete (stat_6, stat_7 unresolved).**
  - stat_6 failed. None of the six missing stat_1 raw p-values could be recovered, because the stat_1 outputs were not published. The brief was not answered.
  - stat_7 gives a 17-test BH family. Six of its raw p-values are carried from earlier tasks (linear quintile trend 0.133, Q5 against Q1 to Q4 0.022, decile chi-square 0.480, decile trend 0.169, spline LR 0.084, spline p90 against p10 0.032). The family is therefore not fully recomputed.
  - stat_5 (partial) reports a provisional 17-test BH family. stat_4 reports BH over a 15-test family. stat_1 reports BH over an 11-test family. These families do not agree. The adjusted values are as follows.
    - Top-tertile contrast: adjusted p = 0.284 (stat_5 provisional), 0.289 (stat_7 17-test).
    - Q5 against Q1 to Q4: adjusted p = 0.331 (stat_4, 15-test), 0.269 (stat_5 provisional), 0.272 (stat_7 17-test).
    - Spline p90 against p10: adjusted p = 0.269 (stat_5 provisional), 0.272 (stat_7 17-test).
    - feat_3 point-biserial: adjusted p = 0.637 (stat_1, 11-test), 0.354 (stat_7 17-test), 0.392 (stat_7 11-test).
    - feat_1 and feat_2 point-biserial: adjusted p = 0.978 (stat_1), 0.906 (stat_7 17-test), 0.938 (stat_7 11-test).
    - The stat_1 BH value of 0.637 for point-biserial tests cannot be reproduced from the recomputed tests. Its value and the 17-test values cannot both stand. Only the 17-test output should be cited, and the 17-test values are not verified.
  - stat_7 also notes that the tertile chi-square, top-tertile and spline LR adjusted values (0.2890) do not match a BH step-up on the listed raw values. These values must be recomputed in code.
- **Conflicting raw p-values for the top tertile and top decile.** Accepted stat_5 values are 0.072 (top tertile) and 0.100 (top decile). Recomputed values in stat_7 are 0.085 and 0.125. Neither is significant after adjustment, under either value.
- **The spline p90 against p10 contrast is post hoc.** It is not corrected for the omnibus test and is not evidence of a cut-point-robust effect.
- **Power is limited.** stat_1 and stat_2 note limited power to detect effects of the size seen (|r| around 0.04 to 0.05, interactions of this size). The group effect in stat_3 (g4 OR about 0.68) was not significant.
- **The models have little predictive value.** The test split has 160 rows, the sub-0.5 test AUCs are treated as noise, and feature importance is unstable. Neither model beats the constant predictor on log loss. No calibration analysis was run.
- **Associations only.** The analysis is observational and reports associations. No causal claims are made.

## Open questions

- Recover the six missing stat_1 raw p-values from their source, then rerun BH over all stat_1, stat_4 and stat_5 tests with raw and adjusted values reported for each test.
- Reproduce the spline likelihood-ratio test (0.084) and the p90 against p10 contrast (0.032) from the data, and rerun BH on the 17-test family with no carried values.
- Settle whether the top-tertile and top-decile raw p-values are 0.072 and 0.100 (accepted) or 0.085 and 0.125 (recomputed), and state the test definition used.
- Does the feat_3 top-end effect hold at a pre-specified cut point, or with a penalized spline with a stated knot choice?
- Does the feat_3 Q5 drop hold under a quintile trend test or a logistic model with feat_3 as a continuous term, after adjustment for group and the other features?
- Does group interact with feat_3 on outcome, and does the group effect hold after adjusting for feat_3 and the other numeric features?
- What sample size is needed to detect a Q5 or top-decile effect (OR about 0.65) and a group effect (g4 OR about 0.68) with adequate power?
- Does a repeated cross-validation or bootstrap on all 800 rows give stable permutation importance?
- Would a calibration analysis (reliability curves or Brier score by model) be needed to make claims about calibration?