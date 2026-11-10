# Predicting a Binary Outcome from Three Numeric Features (1,000 Rows)

## Summary

- **feat_b is the only feature with a clear, significant link to the outcome.** Its mean is higher for outcome=1 (0.248) than for outcome=0 (-0.115). The difference is significant after Holm correction (Welch p = 2.3e-8 adjusted), with Cohen's d of 0.381. In the joint logistic model, its odds ratio is 1.50 (95% CI 1.31 to 1.73). The model's McFadden pseudo R² is only 0.026.
- **feat_a has no mean difference by outcome but a non-linear pattern.** Its means are nearly equal and its linear logit term is not significant (OR 0.98, p = 0.753). The outcome=1 rate across feat_a quartiles is U-shaped (0.536, 0.228, 0.208, 0.548). Adding a squared feat_a term raises pseudo R² from 0.027 to 0.212 (LR test on two squared terms: p = 3.4e-54). The feat_b squared term is not significant.
- **No pairwise interaction between the features is significant** (all Holm-adjusted p-values above 0.05; smallest unadjusted p = 0.323).
- **Predictive gain over the majority baseline depends on the model.** Logistic regression barely matches the baseline on test accuracy (0.628 vs 0.62; test AUC 0.587). Gradient boosting reaches test accuracy 0.708 and AUC 0.698. In 5×5 repeated stratified CV on the training part, gradient boosting beat the baseline on accuracy and log loss in all 25 folds.
- **In gradient boosting, feat_a is the most important feature in every CV fold.** This conflicts with the linear analyses, which show no feat_a effect. The two results are reported side by side below and were not reconciled.

## Data

- **Size:** 1,000 rows × 4 columns.
- **Features:** three numeric features (feat_a, feat_b, feat_c). There are no categorical, date/time, ID, or free-text columns.
- **Target:** `outcome`, binary. Class 0 is 62.0% and class 1 is 38.0%.
- **Missing values:** none in any column.

## Findings

### Distributions by outcome class (EDA)

- **feat_b** differs by location. For outcome=0, the mean is -0.115 and the median is -0.089 (SD 0.950, n = 620). For outcome=1, the mean is 0.248 and the median is 0.209 (SD 0.958, n = 380). The outcome=1 rate rises across feat_b quartiles: 29.2%, 35.2%, 38.0%, 49.6%.
- **feat_a** differs in spread, not location. Means are -0.004 (outcome=0) and -0.019 (outcome=1), and medians are -0.022 and -0.044. SDs are 0.731 for outcome=0 and 1.359 for outcome=1. The outcome=1 rate across feat_a quartiles is U-shaped: 53.6%, 22.8%, 20.8%, 54.8%.
- **feat_c** shows little difference. Means are -0.017 and 0.015, medians -0.012 and 0.034, and SDs 0.986 and 1.007. The outcome=1 rate stays between 36.2% and 40.2% across quartiles, with no clear trend.

![Box plots of feat_a, feat_b and feat_c for outcome=0 and outcome=1](tasks/eda_1/charts/eda1_boxplots_by_outcome.png)

### Univariate tests and effect sizes (stat_1)

- **feat_b:** significant. Welch p = 7.8e-9 (Holm-adjusted 2.3e-8). Mann-Whitney p = 1.6e-7 (Holm-adjusted 4.7e-7). Mean difference is 0.363 (95% CI 0.241 to 0.485), and Cohen's d is 0.381.
- **feat_a:** not significant. Welch p = 0.844 and Mann-Whitney p = 0.949, both Holm-adjusted to 1.0. Mean difference is -0.015 (95% CI -0.163 to 0.134), and Cohen's d is -0.015. The spread difference seen in EDA does not appear as a location difference.
- **feat_c:** not significant. Welch p = 0.620 and Mann-Whitney p = 0.661, both Holm-adjusted to 1.0. Mean difference is 0.032 (95% CI -0.096 to 0.160), and Cohen's d is 0.032.

![Mean difference between outcome=1 and outcome=0 with 95% Welch CI for feat_a, feat_b and feat_c](tasks/stat_1/charts/stat1_mean_diff_ci.png)

**Joint logistic regression on all three features (stat_1):** only feat_b is significant after Holm correction. Its odds ratio is 1.50 (95% CI 1.31 to 1.73), p = 1.1e-8. feat_a has OR 0.98 (95% CI 0.86 to 1.11), p = 0.753. feat_c has OR 1.06 (95% CI 0.93 to 1.21), p = 0.354. McFadden pseudo R² is 0.026.

### Interactions (stat_2)

- feat_a × feat_b: OR 1.054 (95% CI 0.922 to 1.204), p = 0.440.
- feat_a × feat_c: OR 0.990 (95% CI 0.868 to 1.130), p = 0.885.
- feat_b × feat_c: OR 1.072 (95% CI 0.934 to 1.231), p = 0.323.
- None of the three is significant after Holm correction. Because of this, the 2×2 median-split check was not run.
- In the interaction model (standardized features), feat_b remains the only significant main effect: OR 1.481 per SD (95% CI 1.293 to 1.695), p = 1.3e-8. feat_a has OR 0.976 (p = 0.716) and feat_c has OR 1.055 (p = 0.422).
- Pseudo R² is 0.027 with interactions, against 0.026 for the main-effects model. Adding interactions barely changes fit.

### Non-linear effects (stat_3)

- **Squared feat_a term:** significant. Coefficient 1.0615, OR 2.89 per SD² (95% CI 2.43 to 3.44), p = 1.6e-32.
- **Squared feat_b term:** not significant. Coefficient -0.0140, OR 0.986 (95% CI 0.877 to 1.109), p = 0.815. The feat_b linear coefficient in this extended model is 0.581.
- **Model fit:** McFadden pseudo R² rises from 0.027 (linear logit with interactions) to 0.212 in the extended model, a change of 0.185.
- **Joint test:** the likelihood-ratio test of the two squared terms gives LR = 246.25 on 2 df, p = 3.4e-54. Because the feat_b squared term is not significant, this result rests on the feat_a squared term. No separate LR test of the feat_a squared term alone was run. Its contribution is inferred from its Wald p-value.
- **Fit to the quartile pattern:** the observed feat_a quartile rates are consistent with the significant squared term and the near-zero linear coefficient (-0.014). The fitted curve was not checked against the quartile rates, so this report makes no claim that the model reproduces them.

![Predicted share with outcome=1 by standardized feat_a: linear logit vs extended logit, with observed quartile rates](tasks/stat_3/charts/feat_a_linear_vs_extended.png)

### Train/test split (ml_1)

- A stratified 75/25 split with random_state=42 gives 750 training rows and 250 test rows. Outcome=1 is 38% in both (285 of 750 in training, 95 of 250 in test).
- Leakage check: the outcome column is excluded from the features, and no feature is derived from outcome. On the test set, this check reduces to the feature-list check. The largest absolute feature–outcome correlation on the training part is 0.18. It is reported as descriptive only.
- The majority-class baseline (always predict 0) reaches 0.62 accuracy on the test set.

### Predictive models on the test split (ml_2)

- **Logistic regression:** test accuracy 0.628 vs baseline 0.62. Precision 0.542, recall 0.137, F1 0.219, ROC AUC 0.587. Its only gain over the baseline is a small log-loss improvement (0.6491 vs 0.6641). The AUC is close to chance.
- **Gradient boosting:** test accuracy 0.708 vs baseline 0.62. Precision 0.704, recall 0.400, F1 0.510, ROC AUC 0.698. Test log loss is 0.6256 vs 0.6641 for the baseline. Training accuracy is 0.865, which is well above test accuracy.
- The gradient boosting gain rests on one 250-row test split and has not been checked for stability in this step. The report treats it as modest rather than established beyond that split.

**Permutation importance on test ROC AUC (ml_2, 30 repeats):**

| Model | feat_a | feat_b | feat_c |
|---|---|---|---|
| Logistic regression | -0.005 (sd 0.006) | 0.092 (sd 0.037) | 0.003 (sd 0.006) |
| Gradient boosting | 0.158 (sd 0.039) | 0.038 (sd 0.019) | 0.010 (sd 0.007) |

- feat_b is the only feature with a clear effect in logistic regression. In gradient boosting its effect is smaller.
- feat_a has a large effect in gradient boosting and none in logistic regression. The stated explanation for this is a non-linear or threshold effect that the linear model misses. This is a hypothesis, and it was not established by this step. The train–test gap may also inflate the gradient boosting feat_a value.

![Permutation importance by feature for logistic regression and gradient boosting, test set](tasks/ml_2/charts/ml2_permutation_importance.png)

### Repeated cross-validation on the training part (ml_3, 5×5 stratified CV, 25 folds)

**Gradient boosting:**
- Beats the majority baseline on accuracy in 25 of 25 folds and on log loss in 25 of 25 folds.
- Mean accuracy 0.711 (sd 0.024), ROC AUC 0.723 (sd 0.030), log loss 0.591 (sd 0.037). The baseline values are accuracy 0.620, AUC 0.5, log loss 0.664. The 0.708 test accuracy from ml_2 falls within the fold spread.

**Logistic regression:**
- Log loss beats the baseline in 22 of 25 folds (mean 0.651, sd 0.011). Accuracy beats the baseline in 20 of 25 folds (mean 0.634, sd 0.018).
- Mean ROC AUC 0.592 (sd 0.029). Per-fold AUC was not compared with 0.5 in a count.
- The logistic regression edge is therefore not present in every fold.

![Held-out fold accuracy, ROC AUC and log loss by model over 25 folds of 5x5 repeated stratified CV on the training part](tasks/ml_3/charts/ml3_cv_metrics.png)

**Gradient boosting permutation importance per fold (ROC AUC drop):**
- feat_a is the largest importance in 25 of 25 folds, mean 0.193 (sd 0.031).
- feat_b is positive in 25 of 25 folds, mean 0.035 (sd 0.014). It is never the largest.
- feat_c is positive in 14 of 25 folds and negative in 11, mean 0.004 (sd 0.014). Its sign is not stable.

## Limitations

- **Conflicting feat_a results.** The linear analyses (stat_1, stat_2) find no feat_a effect. The squared-term model (stat_3) and gradient boosting (ml_2, ml_3) find a strong feat_a effect. These findings disagree and were not reconciled. The squared-term model's pseudo R² (0.212) was not compared with gradient boosting's performance.
- **Non-linear term inference.** The feat_a squared-term LR test is joint with the non-significant feat_b squared term. The feat_a contribution rests on its Wald p-value, and the fitted curve was not checked against the observed quartile rates.
- **Small effects and low explanatory power.** Pseudo R² is 0.026 for the main-effects model and 0.027 with interactions. Logistic regression's test AUC is 0.587 and its CV AUC is 0.592.
- **Test-set limitations.** The gradient boosting test gain comes from one 250-row split (95 positive cases). Its train accuracy (0.865) is well above test accuracy (0.708), so the test estimate may be optimistic or noisy. The fold results come from the training part only. The 250-row test split was not included in CV.
- **Leakage check scope.** On the test set, the check consists of the feature-list check only. No separate test-set computation was run.
- **Baseline definition.** The log-loss baseline is the training positive rate.
- **Unverified permutation importance.** The gradient boosting feat_a permutation value may be inflated by the train–test gap (ml_2). The per-fold values in ml_3 are computed on held-out folds but within the training part only.
- **Interaction tests.** The median-split check was not run, since no interaction was significant.
- **EDA quartile rates** are descriptive and based on the full dataset, not on a held-out split.
- **Failed tasks and unresolved review issues:** none recorded.

## Open questions

- Is the feat_a U-shape explained by a non-linear or threshold effect, a variance (mixture) difference between outcome groups, or both? The variance question was raised by EDA and stat_3, and the stat_3 model did not test it directly.
- Do a spline or GAM for feat_a, or |feat_a| and squared-feat_a terms in the logistic model, fit better than a single quadratic term, and do their predicted rates match the observed quartile rates?
- Do feat_a and feat_b interact on the squared scale (feat_a² × feat_b, feat_a × feat_b²), and does that change the feat_b conclusion?
- Does feat_c have a conditional or non-linear effect once feat_a and feat_b are controlled for?
- Does feat_b have a threshold effect? Only its squared term was tested.
- Is logistic regression's feat_b effect stable within CV folds, and does its ROC AUC exceed 0.5 in every fold?
- Does the gradient boosting gain over the baseline hold when the 250-row test split is pooled with the training data for repeated CV?