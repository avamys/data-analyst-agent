# Analysis of a Binary Outcome in 1,000 Rows: Drivers, Interactions and Predictive Performance

## Summary

- **feat_a is the dominant predictor.** Its outcome rate rises from 11.6% in the bottom quartile to 70.8% in the top quartile. It has the largest class separation (Cohen's d 1.05), and it is the top permutation-importance feature in both models tested.
- **Logistic regression beats the majority-class baseline and gradient-boosted trees.** On the 200-row test split it reached 75% accuracy against 60.5% for the baseline, with ROC AUC 0.817. Under repeated 5×5 cross-validation its ROC AUC was 0.812, against 0.742 for gradient-boosted trees, and it scored higher in all 25 folds.
- **feat_d and feat_b have smaller but significant associations, and feat_c has none.** feat_d shows a moderate separation (d 0.57) and feat_b a small one (d 0.30). feat_c's outcome groups do not differ (d 0.004).
- **No pairwise interaction is significant.** The largest raw p-value among the six tested interaction terms is 0.209 (feat_c:feat_d). A descriptive gap in feat_b's effect at high feat_a is hypothesis-generating only.
- **Missingness in feat_d shows no detectable relation to the other features or the outcome** (all p ≥ 0.40 for the feature tests, p = 0.724 for the outcome). The missing-indicator adds nothing measurable to the models.

## Data

- **Size:** 1,000 rows × 5 columns.
- **Target:** `outcome` (binary). Class 0: 60.3%; class 1: 39.7%.
- **Features:** four numeric features (feat_a, feat_b, feat_c, feat_d). There are no categorical, date/time, identifier or free-text features.
- **Missing values:** feat_d is missing for 150 rows (15.0%). The other three features are complete.

## Findings

### Feature distributions and outcome rates by quartile

The four features are close to standardized: sd about 1.00, means near zero, and |skew| below 0.1. Extremes stay within about ±3.7, so there is no sign of heavy skew or large outliers.

| Feature | Q1 | Q2 | Q3 | Q4 | Pattern |
|---|---|---|---|---|---|
| feat_a | 11.6% (n=251) | 32.5% (n=249) | 44.0% (n=250) | 70.8% (n=250) | Strong, monotone rise |
| feat_d | 24.9% (n=213) | 35.4% (n=212) | 39.2% (n=212) | 58.2% (n=213) | Rising (850 non-missing rows) |
| feat_b | 26.8% (n=250) | 44.4% (n=250) | 37.6% (n=250) | 50.0% (n=250) | Non-monotone (dip in Q3) |
| feat_c | 38.8% (n=250) | 42.8% (n=250) | 35.6% (n=250) | 41.6% (n=250) | No clear pattern |

The overall outcome rate is 39.7%.

![Share of outcome=1 within each quartile of each numeric feature (dashed line: overall rate 39.7%); feat_d excludes 150 missing rows](tasks/eda_1/charts/eda1_outcome_rate_by_quartile.png)

Summary statistics for the features are: feat_a mean −0.0125, sd 0.99, range −3.33 to 3.13; feat_b mean 0.062, sd 1.02, range −3.07 to 3.67; feat_c mean −0.006, sd 1.01, range −3.37 to 3.30; feat_d mean 0.047, sd 1.00, range −3.05 to 3.28 (850 non-missing rows).

### Trend tests across quartiles

- **feat_a:** a strong monotone trend. The logit odds ratio per quartile step is 2.45 (95% CI 2.14 to 2.81), trend p = 1.5e-37.
- **feat_d:** a significant trend on its 850 non-missing rows. The odds ratio per step is 1.57 (95% CI 1.38 to 1.79), trend p = 9.7e-12.
- **feat_b:** a significant overall upward trend. The odds ratio per step is 1.30 (95% CI 1.16 to 1.46), trend p = 6.5e-6.
- **feat_c:** no trend. The odds ratio per step is 1.01 (95% CI 0.90 to 1.13), trend p = 0.93.

**feat_b's Q3 dip.** The departure from linearity is significant (likelihood-ratio test of categorical vs linear quartile terms, p = 0.004). However, the Q3 vs Q2 difference is −6.8 percentage points (z = −1.55, p = 0.12), with overlapping Wilson intervals. The analysis concludes that the overall pattern is not a straight-line trend but that the dip cannot be singled out as real. A bootstrap interval for the second difference (Q3−Q2 minus Q2−Q1) is −0.39 to −0.10 as recorded; the trend analysis does not treat this as establishing the dip.

![Outcome rate within each quartile of each numeric feature with 95% Wilson intervals; dashed line is the overall rate; feat_d excludes 150 missing rows](tasks/stat_3/charts/stat3_quartile_rate_ci.png)

### Differences between outcome classes

Welch comparisons of each feature between outcome=1 and outcome=0, with Holm correction across four tests:

| Feature | Mean (outcome 1 vs 0) | Difference (95% CI) | Cohen's d | p (unadjusted / Holm) |
|---|---|---|---|---|
| feat_a | 0.544 vs −0.379 | 0.922 (0.812 to 1.032) | 1.05 | 2.3e-53 / 9.3e-53 |
| feat_d | 0.381 vs −0.170 | 0.551 (0.415 to 0.686) | 0.57 | 6.0e-15 / 1.8e-14 |
| feat_b | 0.241 vs −0.057 | 0.298 (0.171 to 0.425) | 0.30 | 4.5e-6 / 9.0e-6 |
| feat_c | −0.004 vs −0.008 | 0.004 (−0.124 to 0.132) | 0.004 | 0.95 / 0.95 |

Group sizes are 603 (outcome 0) and 397 (outcome 1) for feat_a, feat_b and feat_c. For feat_d they are 515 and 335, from 850 complete rows. Ranked by absolute Cohen's d, the order is feat_a, feat_d, feat_b, feat_c. Holm correction leaves the three non-zero effects significant and feat_c non-significant.

![Cohen d of outcome=1 vs outcome=0 for each feature; feat_d uses 850 non-missing rows](tasks/stat_1/charts/effect_sizes_by_feature.png)

### Missingness of feat_d

- feat_d is missing in 150 of 1,000 rows (15%).
- **feat_a:** mean −0.073 for missing rows vs −0.002 for present rows (diff −0.071), Welch p = 0.424.
- **feat_b:** mean 0.128 vs 0.050 (diff 0.078), Welch p = 0.400.
- **feat_c:** mean 0.009 vs −0.009 (diff 0.018), Welch p = 0.835.
- **Outcome:** 41.3% for missing rows vs 39.4% for present rows (diff 1.9 points), chi-square p = 0.724.

The analysis reads this as consistent with missingness completely at random. It also notes that with only 150 missing rows, small associations cannot be ruled out.

![Outcome rate for rows with feat_d present vs missing](tasks/eda_2/charts/outcome_rate_by_feat_d_missing.png)

### Interactions

In a logistic model with all six pairwise terms (n = 850 complete cases), no interaction is significant, and every Holm-adjusted p is 1.0.

| Term | Coefficient | 95% CI | Raw p |
|---|---|---|---|
| feat_a:feat_b | 0.056 | −0.153 to 0.265 | 0.60 |
| feat_a:feat_c | −0.011 | −0.222 to 0.201 | 0.92 |
| feat_a:feat_d | −0.109 | −0.325 to 0.108 | 0.33 |
| feat_b:feat_c | −0.063 | −0.233 to 0.106 | 0.47 |
| feat_b:feat_d | 0.033 | −0.147 to 0.212 | 0.72 |
| feat_c:feat_d | 0.109 | −0.061 to 0.278 | 0.21 |

Descriptively, in the median split of the full data, feat_b's outcome rates differ more at high feat_a than at low feat_a: 51.1% (feat_b low) vs 63.1% (feat_b high) when feat_a is high, against 21.7% vs 22.4% when feat_a is low. The analysis treats this only as a hypothesis, and says confirming it would need a larger sample or a targeted test of feat_b within feat_a strata.

![Share of outcome=1 in each 2x2 median split of feat_a and feat_b, full data](tasks/stat_2/charts/split_2x2_outcome_rates.png)

### Predictive modelling: single split

- **Setup:** stratified 80/20 split, 800 training rows and 200 test rows, with five columns (feat_a to feat_d and a feat_d missing indicator). feat_d was imputed with its training median (0.043). Outcome=1 is 39.75% of training and 39.5% of test rows.
- **Baseline:** predicting class 0 gives 60.5% test accuracy and log loss 0.671.
- **Logistic regression:** test accuracy 75%, ROC AUC 0.817, log loss 0.505, precision 71.0%, recall 62.0%, F1 0.662. Training accuracy is 74%.
- **Gradient-boosted trees:** test accuracy 74%, ROC AUC 0.790, log loss 0.557, precision 66.3%, recall 69.6%, F1 0.679. Training accuracy is 81.4%, which the analysis reads as some overfitting.
- **Permutation importance on test set (drop in ROC AUC, logistic regression, 30 repeats):** feat_a 0.226 (sd 0.035); feat_d 0.085 (sd 0.018); feat_b 0.002 (sd 0.009); feat_c 0.001 (sd 0.001); feat_d_missing −0.003 (sd 0.004).

The analysis describes the logistic regression result as meaningfully better than chance on a 200-row test set. The single-split estimates are noisier than the cross-validated ones in the next section.

![Test accuracy and ROC AUC of logistic regression, gradient-boosted trees, and the majority-class baseline (ROC AUC 0.5 by definition)](tasks/ml_2/charts/ml2_model_comparison.png)

### Predictive modelling: repeated cross-validation

Repeated stratified 5×5 CV on all 1,000 rows (25 folds, mean and sd):

| Model | ROC AUC | Log loss | Accuracy |
|---|---|---|---|
| Logistic regression | 0.812 (sd 0.031) | 0.514 (sd 0.032) | 74.1% (sd 2.6) |
| Gradient-boosted trees | 0.742 (sd 0.028) | 0.717 (sd 0.063) | 69.3% (sd 1.8) |
| Majority baseline | 0.500 | 0.672 | 60.3% |

- The paired fold-level AUC difference (logistic regression minus gradient-boosted trees) is 0.070 (fold-level sd 0.017). Logistic regression is higher in 25 of 25 folds. The descriptive interval of 0.063 to 0.077 treats overlapping folds as independent, so the analysis says it understates uncertainty.
- The ranking holds only for the fixed, untuned gradient-boosted settings used (max_iter 200, learning rate 0.05, default depth). It does not apply to tuned boosting models.
- **Disagreement between analyses:** the gradient-boosted ROC AUC is 0.790 in the single split and 0.742 in the 25-fold CV. The CV analysis attributes the gap to the noisier single split and treats the CV mean as more reliable. It did not re-verify the single-split figure.

![Test ROC AUC per fold for each model across 25 CV folds](tasks/ml_3/charts/ml3_auc_boxplot.png)

**Permutation importance in repeated CV (ROC AUC drop on test folds):**

- **Logistic regression:** feat_a 0.232 (sd 0.030, positive in 25 of 25 folds); feat_d 0.064 (sd 0.014, 25 of 25 folds); feat_d_missing 0.0005 (sd 0.003, p = 0.42, positive in 17 of 25 folds).
- **Gradient-boosted trees:** feat_a 0.188 (sd 0.027, 25 of 25 folds); feat_d 0.042 (sd 0.020, 25 of 25 folds); feat_d_missing −0.0004 (sd 0.003, p = 0.52, positive in 10 of 25 folds).

The analysis concludes that feat_d_missing is not distinguishable from zero for either model.

## Limitations

- **Missingness:** 150 feat_d values are missing. The missingness tests have limited power, so small associations cannot be ruled out. Interaction tests used only the 850 complete rows.
- **Single test split:** the logistic and gradient-boosted results from the single 200-row split are noisy. The gradient-boosted figure (0.790) disagrees with the 25-fold CV mean (0.742), and the single-split value was not re-verified.
- **Gradient-boosted settings:** the CV ranking applies only to the fixed, untuned settings. Tuned models were not tested.
- **Overlapping CV folds:** the interval for the AUC difference is approximate and likely too narrow.
- **feat_b dip:** the non-linearity is significant (p = 0.004), but the Q3 dip itself is not distinguishable from noise (p = 0.12). The source of the non-linearity was not established.
- **Interaction evidence:** the descriptive feat_b-by-feat_a gap is not a tested effect, and no interaction is significant.
- **Unresolved review issue (ml_3):** the reviewer's objection still stands. The ml_3 finding does not report permutation importance for feat_b and feat_c for either model, though the brief asks for every feature. Those values are therefore not reported here. The reviewer also states that the majority-baseline standard deviations for ROC AUC, log loss and accuracy are missing from the finding, so they are not reported here. The core ml_3 conclusions on logistic regression versus gradient-boosted trees and on feat_d_missing are supported and stand.
- **Failed tasks:** none. All seven tasks reported complete.

## Open questions

- Is feat_b's non-linearity robust, and does it come from Q1 or Q4 rather than the Q3 dip? A spline or categorical model with more data or a bootstrap was proposed but not run.
- Is the feat_b effect at high feat_a a real interaction? A targeted test of feat_b within feat_a strata was proposed but not run.
- Does the feat_d_missing indicator add predictive value beyond imputed feat_d? It shows no measurable permutation importance, but its incremental value was not tested directly.
- Is feat_d missingness related to the outcome or the features jointly, and does its rate vary across quantiles of feat_a, feat_b and feat_c? These were proposed but not run.
- Would a tuned gradient-boosted model close the 0.07 AUC gap to logistic regression, and does feat_a show non-linear dependence that would explain it?
- Would repeated cross-validation of the full model set confirm the single-split logistic regression result (0.817 test ROC AUC)?