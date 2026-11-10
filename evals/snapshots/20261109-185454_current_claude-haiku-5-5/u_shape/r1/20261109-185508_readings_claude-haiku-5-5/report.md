# Outcome Analysis of a 1,000-Row Dataset with a Binary Target (outcome)

## Summary

- **The outcome is 38% positive and the majority-class baseline is 62% accuracy.** Gradient boosting reached 0.708 test accuracy and 0.699 test ROC AUC on a 250-row split. Its 5-fold cross-validated ROC AUC was 0.738, against 0.586 for a linear logistic regression.
- **feat_a has a U-shaped association with the outcome that linear tests miss.** Adding feat_a squared to the logit gave LR chi2 = 226.1 on 1 df (p ≈ 4e-51). Implied outcome rates were 52.6% at the 10th percentile, 19.8% at the median and 55.9% at the 90th percentile. feat_a is the most important feature in gradient boosting.
- **feat_b has a monotonic positive association with the outcome.** The rate rises from 26.0% in its lowest quintile to 50.0% in its highest. It is the only feature significant in the linear logistic model (OR 1.50 per raw unit, 95% CI 1.31 to 1.73).
- **feat_b's effect depends on feat_a.** No linear feat_a × feat_b interaction was found, but once feat_a squared is modelled, the feat_a² × feat_b term gives LR chi2 = 5.62 (p = 0.018).
- **feat_c shows no detectable signal.** Its quintile rates are flat (36.5% to 39.5%), it is not significant in any model, and its permutation importance is close to zero.

## Data

- Size: 1,000 rows × 4 columns.
- Target: `outcome`, binary. Class 0 is 62.0% (620 rows) and class 1 is 38.0% (380 rows).
- Features: three numeric features (feat_a, feat_b, feat_c). There are no categorical, date/time, identifier or free-text features.
- Missing values: none in any column.
- All three features are centred near zero with standard deviation near 1 and are close to symmetric (skewness −0.101 for feat_a, −0.025 for feat_b, −0.041 for feat_c).

## Findings

### 1. Feature distributions and outcome rates by quintile

Each feature was binned into quintiles (200 rows each, except feat_a Q4 with 201 and Q5 with 199).

![Histogram of feat_a, feat_b and feat_c (count of rows per value bin)](tasks/eda_1/charts/feature_histograms.png)

- **feat_a is U-shaped:** 60.0%, 27.5%, 16.0%, 25.9% and 60.8% across Q1 to Q5. Both extremes have the highest outcome rates.
- **feat_b rises steadily:** 26.0%, 36.0%, 36.5%, 41.5% and 50.0% across Q1 to Q5.
- **feat_c is flat:** between 36.5% and 39.5% in every quintile.

![Outcome rate by quintile for feat_a, feat_b and feat_c](tasks/eda_1/charts/outcome_rate_by_quintile.png)

These are descriptive rates only; they are not adjusted for the other features.

### 2. Group differences and linear logistic model

![Mean difference of each feature between outcome=1 and outcome=0 in raw feature units, with 95% Welch confidence interval](tasks/stat_1/charts/group_mean_differences.png)

- **feat_b differs significantly between outcome groups.** Mean is 0.248 for outcome=1 and −0.115 for outcome=0, a difference of 0.363 (95% Welch CI 0.241 to 0.485) in raw units. Welch p < 0.001, Holm-adjusted p < 0.001, Cohen's d = 0.38.
- **feat_a shows no difference under the linear comparison.** The difference is −0.015 (95% CI −0.163 to 0.134), Welch p = 0.84, Cohen's d = −0.015. This null result applies only to the linear specification. The mean comparison cannot detect the U-shape reported in Finding 1, and the quadratic test is in Finding 3.
- **feat_c shows no significant difference.** The difference is 0.032 (95% CI −0.096 to 0.160), Welch p = 0.62, Cohen's d = 0.032.
- **Linear logistic regression on all three features** (odds ratios per raw unit, which is approximately per standard deviation):
  - feat_a: OR 0.98 (95% CI 0.86 to 1.11), p = 0.75.
  - feat_b: OR 1.50 (95% CI 1.31 to 1.73), p < 0.001.
  - feat_c: OR 1.06 (95% CI 0.93 to 1.21), p = 0.35.
- After Holm correction across the three group comparisons, only feat_b is significant at α = 0.05.

### 3. Non-linearity of feat_a

![Predicted outcome rate across feat_a from the linear and quadratic logistic models](tasks/stat_3/charts/feat_a_model_curves.png)

- Adding feat_a squared improves fit: LR chi2 = 226.1 on 1 df, p ≈ 4e-51. AIC falls from 1332.1 (linear) to 1108.0 (quadratic).
- In the quadratic logit, the feat_a squared coefficient is 0.937 (SE 0.081, p < 0.001). The linear feat_a term is 0.010 (SE 0.080, p = 0.90).
- In the linear logit, feat_a has no association with the outcome (coefficient −0.014, SE 0.064, p = 0.82).
- Implied outcome rates from the quadratic model are 52.6% at the 10th percentile of feat_a (−1.27), 19.8% at the median (−0.02) and 55.9% at the 90th percentile (1.32). The linear model gives 38.4%, 38.0% and 37.6% at the same points.

### 4. Interactions

**Linear interactions (assume feat_a is linear on the log-odds):**
- feat_a × feat_b: OR 1.05 per raw unit (95% CI 0.92 to 1.20), Wald p = 0.47. LR chi2 = 0.54, p = 0.46.
- feat_a × feat_c: OR 0.99 (95% CI 0.87 to 1.13), Wald p = 0.90. LR chi2 = 0.03, p = 0.85.
- Jointly, LR chi2 = 0.56 on 2 df, p = 0.76.
- These tests cannot detect interactions with feat_a's U-shaped effect, so they do not settle whether feat_a modifies the feat_b or feat_c effects.

**Quadratic interactions (feat_a squared × feature), from the corrected results:**
- feat_a² × feat_b: LR chi2 = 5.62 on 1 df, p = 0.018. Coefficient 0.206, OR 1.23 per unit (95% CI 1.04 to 1.45), Wald p = 0.016.
- feat_a² × feat_c: LR chi2 = 1.07 on 1 df, p = 0.30. Coefficient −0.085, OR 0.92 (95% CI 0.78 to 1.08), Wald p = 0.31.
- Jointly, LR chi2 = 7.31 on 2 df, p = 0.026.
- In the full model with both quadratic interaction terms, feat_b has OR 1.54 (95% CI 1.25 to 1.90, p < 0.001) and feat_c has OR 1.17 (95% CI 0.95 to 1.43, p = 0.13).
- Interpretation of the feat_a² × feat_b result is conditional on the quadratic form. The finding that feat_b's effect varies with feat_a squared (so with distance of feat_a from zero) is the reported result; the linear interaction results above conflict with it only because they assume linearity in feat_a.

### 5. Predictive models

Train/test split: stratified 75/25, 750 training rows and 250 test rows. Baseline is the majority class (0), accuracy 0.620.

![Test ROC AUC of the majority-class dummy, logistic regression and gradient boosting models](tasks/ml_1/charts/model_test_roc_auc.png)

- **Gradient boosting** on the test split: accuracy 0.708, ROC AUC 0.699, precision 0.704, recall 0.400, log loss 0.625. Train accuracy is 0.865, so the model overfits.
- **Logistic regression** on the test split: accuracy 0.628, ROC AUC 0.587, log loss 0.649. Its accuracy is barely above the baseline. Its precision is 0.542 and recall 0.137.
- **Dummy (majority-class)** on the test split: accuracy 0.620, ROC AUC 0.500, log loss 13.70. Its log loss is degenerate because its probabilities are 0 or 1.
- **Disagreement between tasks on the same gradient boosting model:** ml_1 reports test accuracy 0.708, ROC AUC 0.699 and train accuracy 0.865. ml_2 refits the model and reports test accuracy 0.700, ROC AUC 0.697 and train accuracy 0.861. The two sets of figures differ slightly and are both reported here; the source of the difference is not established.
- **Permutation importance (gradient boosting, test split, drop in ROC AUC):** feat_a 0.159 (sd 0.039), feat_b 0.036 (sd 0.019), feat_c 0.009 (sd 0.007).

**Cross-validation (5-fold stratified, 750 training rows):**

![Validation ROC AUC per CV fold (5-fold stratified, 750 training rows), logistic regression vs gradient boosting](tasks/ml_2/charts/cv_roc_auc_per_fold.png)

- Gradient boosting: mean ROC AUC 0.738 (sd 0.058), per-fold range 0.656 to 0.811.
- Logistic regression: mean ROC AUC 0.586 (sd 0.049), per-fold range 0.519 to 0.643.
- Every gradient boosting fold scores above every logistic fold.
- On the 250-row test split, the gap is smaller (0.697 against 0.587). The test score for gradient boosting is below its CV mean, which the finding attributes to noise from the small test set. The CV comparison is described as the more reliable measure of the advantage.
- The logistic model's accuracy is no better than the baseline, so its CV ROC AUC is meaningful only as a ranking measure.

**Feature importance across CV folds (gradient boosting, permutation importance):**
- feat_a ranks first in all 5 folds. Mean importance 0.208 (sd 0.038).
- feat_b ranks second in folds 1 to 4 and third in fold 0, where its importance is negative (−0.032). Mean 0.027 (sd 0.033).
- feat_c ranks last in four folds and second in fold 0. Its importance is near zero in every fold (range −0.017 to 0.000), with mean −0.009.

## Limitations

- **Sample size:** 1,000 rows in total. The test split has 250 rows, so test-set scores are noisy. The findings state this and treat the CV comparison as the more reliable measure.
- **Overfitting:** gradient boosting has train accuracy about 0.86 to 0.87 against test accuracy about 0.70 to 0.71. The findings describe the advantage over the baseline as moderate.
- **No tuning or repeated CV:** the gradient boosting advantage was not checked under repeated CV or tuned depth and learning rate.
- **Linear-model assumptions:** the linear logistic model and the linear interaction tests cannot represent feat_a's U-shape. The ML comparison with logistic regression therefore reflects a linear model and does not show what a non-linear logistic model achieves.
- **Quadratic form:** the feat_a² × feat_b interaction is from a quadratic approximation. The findings note that a spline or dropping extreme feat_a values was not checked.
- **Small test-score discrepancy:** ml_1 and ml_2 report slightly different test figures for the same gradient boosting model (see Section 5).
- **Corrected data error (resolved):** an earlier stat_4 result listed the feat_a² × feat_b and feat_a² × feat_c LR statistics with swapped values. The corrected values (`quadratic_interaction_lr_tests_fixed`) are used in this report. The earlier object was overwritten with the corrected values.
- **Overall outcome-rate note:** the eda_1 quintile rates are unadjusted descriptive rates.
- **Failed tasks:** none. All tasks are marked complete.

## Open questions

- Does a spline or binned non-parametric fit confirm the feat_a U-shape and locate its minimum (the quadratic places it near feat_a = 0)?
- Does feat_b's effect hold after adjusting for feat_a in a non-linear model, and does its effect change sign across the range of feat_a? A plot of feat_b's log-odds effect across low, median and high feat_a has not been produced.
- Does the feat_a² × feat_b result hold with a spline in feat_a or after dropping extreme feat_a values?
- Can feat_c be dropped without loss of predictive performance? The comparison of gradient boosting with and without feat_c under the same 5 folds has not been run.
- Does a non-linear logistic model with the quadratic terms close the CV gap with gradient boosting (0.738 against 0.586)? This has not been tested.
- Does gradient boosting's advantage hold under repeated cross-validation or with tuned depth and learning rate?