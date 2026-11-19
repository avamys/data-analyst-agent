# Outcome Analysis of a 1,000-Row Binary Dataset: Predicting `outcome` from feat_a, feat_b and feat_c

## Summary

- **feat_a has a U-shaped relation with outcome.** The outcome=1 rate is 60.0% in the lowest quintile, falls to 16.0% in the third, and rises to 60.8% in the highest. A squared term improves the logit fit strongly (LR = 226.1, p = 4.3e-51), and the effect survives adjustment for feat_b. The linear feat_a test alone is null (p = 0.844).
- **feat_b has a monotone, significant association with outcome.** Its outcome=1 rate rises from 26.0% in the lowest quintile to 50.0% in the highest. It is the only feature that survives Holm correction (Holm-adjusted p < 0.001), and it keeps an independent effect after adjusting for feat_a (LR = 54.1, p = 2.0e-13).
- **feat_c shows no detectable association.** Its bin rates range from 36.5% to 39.5%, and no test is significant (Welch p = 0.620; Holm-adjusted p = 1.0).
- **Prediction is weak to moderate.** Only gradient boosting beats the 62% majority-class baseline on accuracy (test accuracy 0.695, test ROC AUC 0.690), and it overfits. Tuned gradient boosting has test ROC AUC 0.681 and test accuracy 0.690. Logistic regression is near chance on ranking (test ROC AUC 0.588) and no better than the baseline on accuracy. Almost all of the model's signal comes from feat_a.

## Data

- 1,000 rows and 4 columns: the binary target `outcome` and three numeric features (feat_a, feat_b, feat_c). There are no categorical, date/time, identifier or free-text columns.
- Target classes: outcome=0 is 62.0% and outcome=1 is 38.0%.
- Missing values: none in any column.
- For modelling, a stratified 80/20 split (seed 42) gave 800 training rows and 200 test rows, both with a 38% positive rate.

## Findings

### Outcome rate across the range of each feature

The outcome=1 rate is 38.0% overall, with no missing values (eda_1).

**feat_a (U-shaped).** Quintile outcome=1 rates are 60.0% (Q1, n=200), 27.5% (Q2, n=200), 16.0% (Q3, n=200), 25.9% (Q4, n=201) and 60.8% (Q5, n=199). The feat_a mean is -0.004 for outcome=0 and -0.019 for outcome=1.

![Share of outcome=1 per quintile bin of feat_a](tasks/eda_1/charts/rate_by_feat_a.png)

**feat_b (monotone increasing).** Quintile outcome=1 rates are 26.0% (Q1), 36.0% (Q2), 36.5% (Q3), 41.5% (Q4) and 50.0% (Q5), each with n=200. Q2 and Q3 are nearly equal. The feat_b mean is -0.115 for outcome=0 and 0.248 for outcome=1.

![Share of outcome=1 per quintile bin of feat_b](tasks/eda_1/charts/rate_by_feat_b.png)

**feat_c (flat in bins).** Quintile outcome=1 rates are 37.5% (Q1), 36.5% (Q2), 39.5% (Q3), 38.5% (Q4) and 38.0% (Q5), each with n=200. The feat_c mean is -0.017 for outcome=0 and 0.015 for outcome=1. Formal testing is in the section below.

![Share of outcome=1 per quintile bin of feat_c](tasks/eda_1/charts/rate_by_feat_c.png)

### Differences between outcome classes

**feat_b differs significantly.** Welch t = 5.84 (p = 7.8e-9; Holm-adjusted p = 2.3e-8, reported as < 0.001). Mann-Whitney p = 1.6e-7. The mean difference (outcome=1 minus outcome=0) is 0.363 (95% CI 0.241 to 0.485). Cohen's d is 0.38 (95% CI 0.25 to 0.51). The point-biserial r is 0.18. The univariate logit coefficient is 0.401 (95% CI 0.262 to 0.539). These are univariate results.

**feat_a shows no significant linear difference.** Welch p = 0.844 (Holm-adjusted p = 1.0), Mann-Whitney p = 0.949. The mean difference is -0.015 (95% CI -0.163 to 0.134), Cohen's d is -0.015, and the logit coefficient is -0.014 (95% CI -0.140 to 0.111). This linear test misses the U-shape reported in eda_1, so the null applies only to a monotone or linear effect.

**feat_c shows no significant difference.** Welch p = 0.620 (Holm-adjusted p = 1.0), Mann-Whitney p = 0.661. The mean difference is 0.032 (95% CI -0.096 to 0.160), and the logit coefficient is 0.033 (95% CI -0.096 to 0.161).

Only feat_b's effect survives Holm correction across the three Welch tests.

![Boxplots of feat_a, feat_b and feat_c for outcome=0 versus outcome=1 (1000 rows)](tasks/stat_1/charts/feat_by_outcome_boxplots.png)

### Nonlinearity of feat_a and its adjustment for feat_b

**The U-shape is real nonlinearity.** Adding a squared feat_a term to the logit improves fit with LR = 226.1 on 1 df (p = 4.3e-51). The squared-term coefficient is 0.937 (95% CI 0.778 to 1.096). The linear feat_a coefficient alone is -0.014 (95% CI -0.140 to 0.111), so the relation is almost purely quadratic.

**The U-shape survives adjustment for feat_b.** With feat_a, squared feat_a and feat_b in the model, the squared term gives LR = 246.4 (p = 1.6e-55) and coefficient 1.031 (95% CI 0.861 to 1.201). The unadjusted coefficient was 0.937 (95% CI 0.778 to 1.096). The two intervals overlap.

**feat_b keeps an independent effect.** Its adjusted logit coefficient is 0.589 (95% CI 0.424 to 0.753). The LR test of feat_b given feat_a and squared feat_a gives LR = 54.1 (p = 2.0e-13).

**The turning point is near zero.** In the adjusted quadratic, the vertex of feat_a is -0.001 (delta-method SE 0.040; 95% CI -0.080 to 0.078). The interval includes zero, so the minimum of the U lies close to zero.

![Predicted share of outcome=1 by feat_a from the adjusted quadratic logit, feat_b held at its mean](tasks/stat_3/charts/quad_pred_feat_a.png)

### Interactions

**feat_a with feat_b (linear product term).** The interaction coefficient is 0.050 (OR 1.051, 95% CI 0.918 to 1.203), p = 0.470.

**feat_a with feat_c (linear product term).** The interaction coefficient is -0.009 (OR 0.991, 95% CI 0.870 to 1.130), p = 0.898. Jointly, both linear interactions give LR = 0.558 on 2 df (p = 0.757).

**Median-split 2x2 for feat_a and feat_b.** Outcome rates by cell (hi = above median; medians: feat_a -0.0225, feat_b 0.011):

| feat_a | feat_b | Outcome rate | n |
|---|---|---|---|
| low | low | 31.6% | 256 |
| low | high | 45.1% | 244 |
| high | low | 32.8% | 244 |
| high | high | 42.6% | 256 |

The feat_b-high rate is 45.1% when feat_a is low and 42.6% when feat_a is high. The feat_b-high versus feat_b-low comparison, for each feat_a stratum, is consistent with no linear interaction. The median split pools both tails of the U-shaped feat_a, so these cells cannot detect a U-shaped interaction and offer no evidence against one. The linear null does not establish that feat_a leaves the effect of feat_b unchanged; a nonlinear feat_a-dependent effect remains untested.

**Median-split 2x2 for feat_a and feat_c** (medians: feat_a -0.0225, feat_c 0.014):

| feat_a | feat_c | Outcome rate | n |
|---|---|---|---|
| low | low | 37.4% | 243 |
| low | high | 38.9% | 257 |
| high | low | 36.0% | 258 |
| high | high | 39.7% | 242 |

The feat_c-high rate is 38.9% when feat_a is low and 39.7% when feat_a is high. The linear feat_a × feat_c interaction is not significant (p = 0.898), and the 2x2 cells do not test a U-shaped interaction. No significance test on the feat_c gap within each feat_a stratum is recorded.

### Predictive models

**Majority-class baseline.** Test accuracy is 0.62 by construction. Its balanced accuracy and ROC AUC are both 0.50, so it carries no information about outcome. Its log loss of 13.70 comes from hard 0/1 probabilities and is not a meaningful reference. A constant predictor at the training rate of 0.38 gives test log loss 0.664.

**Untuned logistic regression** (standardised feat_a, feat_b, feat_c). Test accuracy is 0.625, balanced accuracy 0.527, ROC AUC 0.588 and log loss 0.649. Test precision is 0.529 and recall 0.118. Standardised coefficients are feat_b 0.397, feat_c 0.043 and feat_a 0.035. The linear model cannot represent the feat_a U-shape.

Logistic regression test accuracy of 0.625 is no better than the 0.62 majority-class baseline. Only gradient boosting, with test accuracy 0.695, exceeds the baseline on accuracy.

**Untuned gradient boosting** (default settings, random_state 42). Train accuracy is 0.864 and test accuracy is 0.695, a gap of about 0.17, so the model overfits. Test ROC AUC is 0.690, balanced accuracy 0.637, log loss 0.631, precision 0.667 and recall 0.395. Its selection as the best model used the test set, so these scores are optimistic. Feature importances are feat_a 0.632, feat_b 0.238 and feat_c 0.130.

![Test-set ROC AUC of the majority-class baseline, logistic regression and gradient boosting](tasks/ml_1/charts/test_roc_auc_by_model.png)

**Feature contribution in the untuned gradient boosting model.** Permutation importance, measured as the mean drop in test ROC AUC over 30 repeats, is 0.149 (sd 0.038) for feat_a, 0.033 (sd 0.017) for feat_b and 0.007 (sd 0.010) for feat_c. Removing feat_a drops test ROC AUC from 0.690 to 0.540. Removing feat_b gives 0.686 and removing feat_c gives 0.686. feat_b's importance is about twice its sd, so its contribution is modest and uncertain. feat_c is within noise. These figures come from an overfit model scored on the test set and are indicative only.

**Tuned models (5-fold CV on the 800 training rows, then test).**
- Tuned gradient boosting has CV ROC AUC 0.777 (sd 0.029) and CV log loss 0.549 (sd 0.017). Test ROC AUC is 0.681, test accuracy 0.690, balanced accuracy not recorded, test precision 0.706 and recall 0.316. Train accuracy is 0.758, so the train-test gap narrows to about 0.068. Its importances are feat_a 0.801, feat_b 0.188 and feat_c 0.011.
- Its selected hyperparameters are learning_rate 0.03, max_depth 3, min_samples_leaf 20 and n_estimators 50.
- Tuned logistic regression (C = 0.01) has CV ROC AUC 0.597 (sd 0.023) and CV log loss 0.651 (sd 0.003). Test ROC AUC is 0.589, test accuracy 0.645 and test recall 0.066. Its coefficients are feat_b 0.253, feat_c 0.023 and feat_a 0.021.
- The CV estimate for gradient boosting is optimistic because its hyperparameters were chosen on the same folds. The drop from CV (0.777) to test (0.681) shows this.
- The gradient boosting advantage over logistic regression holds in both CV and test ROC AUC.
- The tuned gradient boosting test accuracy of 0.690 is above the 0.62 baseline. The tuned logistic regression test accuracy of 0.645 exceeds the baseline by a small margin. The untuned and tuned gradient boosting models differ little on test metrics: test ROC AUC is 0.690 untuned and 0.681 tuned, and test accuracy is 0.695 untuned and 0.690 tuned. On 200 test rows these differences are within noise, so the untuned model is not shown to be better.

![ROC AUC of the majority-class baseline, tuned logistic regression and tuned gradient boosting: mean 5-fold CV on the training set (800 rows) and the single test set (200 rows). The majority-class CV bar is omitted because it is not cross-validated.](tasks/ml_3/charts/ml3_roc_auc_cv_vs_test.png)

## Limitations

- **Small sample.** The data have 1,000 rows, and the test set has 200. Test-set metrics, feature rankings and the untuned/tuned comparison are therefore noisy.
- **Test-set selection and overfitting.** The untuned gradient boosting model was chosen by test ROC AUC, so its test scores are optimistic. It overfits (train accuracy 0.864 against test 0.695). Its permutation importances are indicative only.
- **Tuning estimates.** The 0.777 CV ROC AUC is optimistic because hyperparameters were selected on the same folds. No nested cross-validation has been run, so no unbiased estimate exists for tuned gradient boosting. No separate validation estimate exists for the untuned model either.
- **Incomplete logistic regression parameters.** Only C = 0.01 is recorded for the tuned logistic regression. Its other parameters are not in the accepted results.
- **Linear-only tests in parts of the analysis.** The feat_a interaction test with feat_b uses a linear product term. The U-shape was not tested in interaction. feat_b's linearity in logit terms was not tested. The 2x2 median splits pool both tails of feat_a and cannot detect U-shaped interactions.
- **Unresolved review issue on the feat_a × feat_c 2x2 (stat_2).** The lead's objection stands. This report gives the rates and cell sizes. It does not state a significance test on the feat_c gap within each feat_a stratum, which the brief required. The only significance result recorded is the linear interaction (p = 0.898).
- **Unresolved review issue on the feat_a-high feat_b gap (stat_2).** The gap is defined by its source values: the feat_a-high, feat_b-high rate of 42.6% (n=256) and the feat_a-high, feat_b-low rate of 32.8% (n=244).
- **Unresolved review issue on the logistic regression baseline (ml_1).** The objection is addressed above: the 0.625 test accuracy is no better than the 0.62 baseline, and only gradient boosting exceeds it on accuracy. The ROC AUC, log loss and overfitting statements are unchanged.
- **Unresolved review issue on tuning reporting (ml_3).** The gradient boosting hyperparameters are reported above. The full logistic regression parameter set is not recorded. The untuned-versus-tuned differences are reported as values and described as within noise on 200 test rows.
- **Unresolved review issue on the baseline (ml_3).** The 0.62 majority-class accuracy is a trivial reference, since its ROC AUC is 0.50 and its balanced accuracy is 0.50. Accuracy comparisons against it are therefore weak evidence.
- **Univariate results.** The feat_b statistics in stat_1 are univariate. The adjusted effect is reported separately in stat_3.
- **Partial task.** stat_2 is marked partial, and its review issues are open.

## Open questions

- Does a spline of feat_a, rather than a quadratic, confirm the shape, and does the U-shape change at the tails?
- Does feat_a interact with feat_b in a nonlinear, U-shaped way? The linear product term was null, but the interaction was not tested with a squared or spline term.
- Is feat_b's trend linear in logit terms, or does it need a squared or spline term?
- Is feat_c irrelevant conditional on feat_a and feat_b? Its conditional effect within strata was not tested. Does feat_c contribute at all to the model (tuned importance 0.011)?
- Does the feat_c gap differ between feat_a-low and feat_a-high strata, and is that significant? The 2x2 rates exist, but no test was run on this gap.
- What is the unbiased predictive performance of tuned gradient boosting? Nested cross-validation with outer folds separate from the hyperparameter search has not been run.
- Does the feat_a nonlinearity explain the gradient boosting advantage over logistic regression? The question was raised but not tested with a squared or spline term in logistic regression.
- What do the results look like on a validation estimate separate from the test set, for both the untuned and tuned models?