# Outcome Analysis of 1,000 Rows: Associations of feat_a, feat_b and feat_c with a Binary Outcome

## Summary

- **feat_b is the only feature with a clear linear association with outcome.** Its outcome=1 rate rises across quintiles from 26% to 50%. It stays significant after Holm correction (Holm-adjusted p = 2.3e-08), with an odds ratio of 1.47 per SD (95% CI 1.29 to 1.69).
- **feat_a has a U-shaped association that a linear test misses.** The outcome=1 rate is 60% in the lowest quintile, falls to 16% in Q3, and rises to 61% in the highest quintile. A linear test gives p = 0.844, but adding a quadratic term gives LR chi2 = 246.6 (1 df, p about 1e-55), and a spline gives a similar shape.
- **feat_c shows no detectable association**, either as a flat binned rate or in any model reported here.
- **No feature interactions were detected.** All three pairwise interaction terms are non-significant, but their confidence intervals are wide enough to allow moderate effects.
- **Predictive lift over the majority-class baseline is weak.** The gradient-boosted model reaches test accuracy 0.645 against a 0.62 baseline and test ROC AUC 0.664 (bootstrap 95% interval 0.58 to 0.74) on 200 test rows. It overfits strongly. Logistic regression's log-loss gain over baseline (0.015) is not statistically established.

## Data

- **Size:** 1,000 rows and 4 columns.
- **Target:** `outcome`, binary. Class 0 is 62.0% (620 rows) and class 1 is 38.0% (380 rows).
- **Features:** three numeric features (feat_a, feat_b, feat_c). There are no categorical, date/time, identifier or free-text columns.
- **Missing values:** none.

## Findings

### Outcome distribution and binned rates

The outcome is not balanced: 38% of rows are class 1. The outcome=1 rate was computed within quintile bins of each feature (about 200 rows per bin).

**feat_a (U-shaped):**

| Quintile | Count | Rate of outcome=1 |
|---|---|---|
| Q1 (lowest) | 200 | 60% |
| Q2 | 200 | 27.5% |
| Q3 | 200 | 16% |
| Q4 | 201 | 25.9% |
| Q5 (highest) | 199 | 60.8% |

**feat_b (monotone increasing):**

| Quintile | Count | Rate of outcome=1 |
|---|---|---|
| Q1 (lowest) | 200 | 26% |
| Q2 | 200 | 36% |
| Q3 | 200 | 36.5% |
| Q4 | 200 | 41.5% |
| Q5 (highest) | 200 | 50% |

**feat_c (flat):**

| Quintile | Count | Rate of outcome=1 |
|---|---|---|
| Q1 (lowest) | 200 | 37.5% |
| Q2 | 200 | 36.5% |
| Q3 | 200 | 39.5% |
| Q4 | 200 | 38.5% |
| Q5 (highest) | 200 | 38% |

The rates for feat_c stay between 36.5% and 39.5%, with no clear trend.

All three features have mean near 0, standard deviation between 0.97 and 1.02, and skew between -0.10 and -0.03, so none is strongly skewed.

![Rate of outcome=1 per quintile bin of feat_a, feat_b and feat_c](tasks/eda_1/charts/rate_by_bin.png)

### Feature associations and effect sizes

- **feat_b is significant.** Mean feat_b is -0.115 for outcome=0 and 0.248 for outcome=1. Welch t = 5.84, p = 7.8e-09, Holm-adjusted p = 2.3e-08 across the three features. Cohen's d = 0.38 (95% CI 0.25 to 0.51). Logistic OR per SD = 1.47 (95% CI 1.29 to 1.69).
- **feat_a is not significant on a linear basis.** Mean feat_a is -0.004 for outcome=0 and -0.019 for outcome=1. Welch p = 0.844 (Holm-adjusted p = 1.0). Cohen's d = -0.015 (95% CI -0.14 to 0.11). Logistic OR per SD = 0.99 (95% CI 0.87 to 1.12). The team notes that a linear test does not capture the U-shape.
- **feat_c is not significant.** Mean feat_c is -0.017 for outcome=0 and 0.015 for outcome=1. Welch p = 0.620 (Holm-adjusted p = 1.0). Cohen's d = 0.032 (95% CI -0.10 to 0.16). Logistic OR per SD = 1.03 (95% CI 0.91 to 1.17).
- After Holm correction across the three features, only feat_b remains significant at alpha 0.05.

![Mean of feat_a, feat_b and feat_c for outcome=0 and outcome=1, with 95% CI error bars](tasks/stat_1/charts/stat1_mean_by_outcome.png)

### Interactions

Logistic regression on standardized features with all pairwise interactions found no significant interaction:

- feat_a × feat_b: OR 1.05 (95% CI 0.92 to 1.20), p = 0.44
- feat_a × feat_c: OR 0.99 (95% CI 0.87 to 1.13), p = 0.88
- feat_b × feat_c: OR 1.07 (95% CI 0.93 to 1.23), p = 0.32

The team notes that these intervals are compatible with interactions of modest size in either direction, so the result does not rule out a moderate moderating effect. In the same model, the feat_b main effect remains significant (OR 1.48, 95% CI 1.29 to 1.70), while the feat_a and feat_c main effects do not (OR 0.98 and 1.06). The pseudo R² is 0.027 (n = 1,000), so the model fits weakly overall. Because no interaction term was significant, the median-split analysis was not run.

### Nonlinear effect of feat_a

Two findings test the U-shape in logistic models adjusted for feat_b and feat_c.

**Quadratic term:**
- The adjusted quadratic coefficient is 1.029 (SE 0.086, p about 1e-32). The likelihood-ratio test against the linear-only adjusted model gives chi2 = 246.6 (1 df, p about 1e-55).
- The unadjusted quadratic coefficient is 0.937 (SE 0.081, LR chi2 = 226.1), so the U-shape survives adjustment.
- The adjusted linear feat_a coefficient is 0.003 (SE 0.083, p = 0.97). The fitted curve is therefore nearly symmetric about feat_a = 0, with its minimum at feat_a ≈ -0.002.
- At feat_b = feat_c = 0, the fitted rate is 0.179 at feat_a = 0 and 0.9996 at feat_a = ±3. At feat_a = ±1 it is 0.377 and 0.379.

**Spline term:**
- A spline for feat_a improves on the linear-only adjusted model (LR chi2 = 248.3, 4 df, p = 1.5e-52).
- At feat_b = feat_c = 0, the spline gives 0.159 at feat_a = 0 and 0.996 at feat_a = ±3.
- Adding the spline to the adjusted quadratic model gives LR chi2 = 1.09 (4 df, p = 0.90), so the team detects no nonlinearity beyond the quadratic.
- AIC: linear 1301.5, quadratic 1056.8, spline 1059.1. The quadratic is marginally preferred.
- Spline and quadratic fitted rates differ by at most about 0.03 across the grid from -3 to 3. The largest gap is 0.026 at feat_a = -1.

![Fitted rate of outcome=1 across feat_a from the adjusted quadratic logistic model](tasks/stat_3/charts/stat3_feat_a_fitted_curve.png)

![Fitted outcome=1 rate across feat_a from spline and quadratic logits, with observed binned rates](tasks/stat_4/charts/stat4_spline_vs_quad.png)

**Tail calibration:**
- Lower 5% of feat_a (n = 50): observed rate 0.90, spline-fitted 0.898, quadratic-fitted 0.917.
- Upper 5% of feat_a (n = 50): observed rate 0.86, spline-fitted 0.883, quadratic-fitted 0.901.
- The team describes tail calibration as acceptable for both models, while noting that the tail samples are small.

### feat_b and feat_c in the adjusted model

In the adjusted quadratic logit, feat_b has a positive effect (coefficient 0.597, SE 0.084, p = 1.5e-12). feat_c has no detectable effect (coefficient 0.080, SE 0.077, p = 0.30). So the feat_b effect holds after adjusting for feat_a's nonlinear term and feat_c.

### Predictive models

The test set has 200 rows, with a stratified 80/20 split and seed 42 (800 training rows).

| Model | Test accuracy | Baseline accuracy | Test ROC AUC | Test log-loss |
|---|---|---|---|---|
| Majority-class baseline | 0.62 | 0.62 | 0.5 | 0.664 |
| Logistic regression | 0.625 | 0.62 | 0.588 | 0.649 |
| Gradient boosting (HistGradientBoosting) | 0.645 | 0.62 | 0.664 | 0.854 |

- **Gradient boosting** has a lift of +0.025 in accuracy over the baseline. Its test precision is 0.5397, recall 0.4474, and F1 0.4892. Its bootstrap 95% interval for test ROC AUC is 0.58 to 0.74. The team did not formally test its significance.
- **Overfitting:** training accuracy is 0.9925 against test accuracy 0.645. The team names this overfitting as the likely cause of the boosted model's test log-loss of 0.854, which is worse than the baseline's 0.664.
- **Logistic regression:** test accuracy 0.625, a lift of only +0.005 over the baseline. This is no better than always predicting class 0. Its test ROC AUC is 0.588. Its test log-loss is 0.649, a gain of 0.015 over the baseline. The bootstrap 95% interval for this gain is -0.011 to +0.040, which includes zero, so the gain is not established. Calibration was not measured separately.
- **Cross-validation:** the 5-fold CV ROC AUC on the training set is 0.727 (SD 0.028) for gradient boosting and 0.596 (SD 0.023) for logistic regression. The ranking matches the test split (0.664 and 0.588). Only the size of the gap differs.
- **Overall:** the team describes the features as giving weak predictive lift over the majority-class baseline.

### Feature importance

The two importance measures disagree on which feature matters most. The team reports both as given.

- **Gradient boosting (permutation importance, drop in test ROC AUC, 30 repeats):** feat_a 0.142 (SD 0.032), feat_b 0.025 (SD 0.022), feat_c 0.003 (SD 0.017), which is near zero.
- **Logistic regression (absolute standardized coefficient):** feat_b 0.397, feat_c 0.043, feat_a 0.035.

The team's interpretation is that the boosted trees can capture the non-monotone feat_a effect, which would explain why feat_a dominates the boosted model's importance. feat_b has the largest linear coefficient, a linear effect the boosted model uses less. This is the team's interpretation and was not separately tested.

![Permutation importance of feat_a, feat_b, feat_c for the gradient-boosted model, test set](tasks/ml_1/charts/hgb_permutation_importance.png)

## Limitations

- **Small test set.** The model results rest on 200 test rows. The bootstrap intervals are wide: the gradient-boosting test ROC AUC interval is 0.58 to 0.74, and the logistic regression log-loss gain interval includes zero. The team notes that a larger test set or repeated cross-validation on all 1,000 rows would narrow these intervals. That analysis was not run.
- **Overfitting of the boosted model.** Training accuracy of 0.9925 against test accuracy of 0.645 means its test log-loss (0.854) is worse than baseline. The team did not tune or regularize the model.
- **Weak model fit and predictive lift.** The interaction model has a pseudo R² of 0.027. Predictive lift over baseline is small (+0.025 accuracy at best).
- **Interactions not ruled out.** The interaction confidence intervals are compatible with moderate effects, as the team notes.
- **Non-significant linear results do not show absence.** feat_a's linear test is not significant, but its nonlinear effect is strongly supported. The non-significant feat_c results should be read as no detectable effect at this sample size.
- **Spline coefficients not identified.** The spline basis coefficients are collinear with the intercept, so the team reports only fitted curves, not coefficients.
- **Tail calibration on small samples.** The tail checks use n = 50 per tail, and the team describes them as small.
- **Calibration of the logistic model not measured separately.**
- **Review issues and failed tasks.** The record contains no unresolved review issues and no failed tasks.

**Numbers not traced to a recorded fact.** The automatic check found no recorded value for these numbers:
- 0.027 in: "The team notes that these intervals are compatible with interactions of modest size in either direction, so the result does not rule out a moderate moderating e"
- 0.026 in: "- Spline and quadratic fitted rates differ by at most about 0.03 across the grid from -3 to 3. The largest gap is 0.026 at feat_a = -1."
- 0.027 in: "- **Weak model fit and predictive lift.** The interaction model has a pseudo R² of 0.027. Predictive lift over baseline is small (+0.025 accuracy at best)."

## Open questions

- Is the U-shape of feat_a real, or does it reflect noise? The quadratic and spline tests support its existence, but the team did not assess this beyond these tests.
- Does an interaction between feat_a and feat_b exist? The interaction test was non-significant but imprecise, and the feat_a pattern across feat_b levels was not examined in a stratified analysis.
- Would regularizing or tuning the gradient-boosted model (depth, learning rate, early stopping) remove its overfitting and improve its test log-loss?
- Would a larger test set or repeated cross-validation on all 1,000 rows narrow the wide uncertainty on test AUC and log-loss gain?
- Is the 0.86 to 0.90 observed tail rate consistent with the near-1 fitted rates at the extremes of feat_a? A larger sample or a bootstrap of tail calibration would test this.
- Does the feat_a nonlinearity explain why feat_a dominates the boosted model's importance while feat_b dominates the logistic model's coefficients? The team offers this as an interpretation only.