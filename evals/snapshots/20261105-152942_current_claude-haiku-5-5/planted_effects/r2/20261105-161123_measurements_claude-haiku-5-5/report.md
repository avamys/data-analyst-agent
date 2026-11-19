# Outcome Prediction and Feature Association Analysis: 1,000 Rows, Binary Target `outcome`

## Summary

- **feat_a is the strongest predictor of outcome.** Its outcome rate rises from 11.6% in the lowest quartile to 70.8% in the highest. Per SD, its odds ratio is 3.30 (95% CI 2.76 to 3.95). It stays strong in a joint model adjusted for feat_b and feat_d (OR 3.54 per SD).
- **feat_d and feat_b also predict outcome, feat_c does not.** feat_d gives OR 1.81 per SD in unadjusted analysis and 2.07 adjusted (complete cases). feat_b gives OR 1.35 unadjusted and 1.41 adjusted. feat_c gives OR 1.00 (95% CI 0.88 to 1.14).
- **Both models beat the majority-class baseline.** On a 200-row test split, logistic regression reaches 0.750 accuracy and gradient boosting 0.755, against 0.605 for always predicting 0. Under 5-fold CV on all rows, logistic regression has the best log loss (0.513) and ROC AUC (0.812) of the three fitted models.
- **No detectable feat_a × feat_b interaction.** The interaction term has OR 1.07 (95% CI 0.89 to 1.28, p = 0.48). The feat_a gradient is similar across feat_b tertiles.
- **feat_d missingness shows no detectable link to the other columns or to outcome.** The conditional test, adjusting for feat_a, feat_b and feat_d, gives OR 1.09 per SD (95% CI 0.94 to 1.26, p = 0.28). Whether the missingness is random with respect to feat_d's own values cannot be tested with these data.

## Data

- **Size:** 1,000 rows and 5 columns: four numeric features (feat_a, feat_b, feat_c, feat_d) and the binary target `outcome`. There are no categorical, date/time, identifier or free-text columns.
- **Target:** 603 rows with outcome 0 (60.3%) and 397 rows with outcome 1 (39.7%). This is moderate imbalance, so the majority-class baseline is about 60%.
- **Missing values:** feat_d is missing in 150 of 1,000 rows (15.0%). feat_a, feat_b and feat_c have no missing values. Feature summaries and feat_d quartiles use the 850 non-missing rows.

## Findings

### Feature distributions and outcome rate across quartiles

The features are roughly centred, with standard deviations near 1 (feat_a mean -0.013, SD 0.99; feat_b mean 0.062, SD 1.02; feat_c mean -0.006, SD 1.01; feat_d mean 0.047, SD 1.00 on non-missing rows). Histograms by outcome class are below.

![Histograms (row counts) of feat_a to feat_d, split by outcome class; feat_d excludes missing rows](tasks/eda_1/charts/feature_distributions_by_outcome.png)

Outcome rate by quartile of each feature:

- **feat_a:** rises steeply: 11.6% (Q1, n = 251), 32.5% (Q2, n = 249), 44.0% (Q3, n = 250), 70.8% (Q4, n = 250).
- **feat_d** (non-missing rows): rises monotonically: 24.9% (Q1, n = 213), 35.4% (Q2, n = 212), 39.2% (Q3, n = 212), 58.2% (Q4, n = 213).
- **feat_b:** weaker and non-monotone: 26.8%, 44.4%, 37.6%, 50.0% (n = 250 per quartile). Whether this pattern is real or noise was not settled (see Limitations and Open questions).
- **feat_c:** little association: quartile rates range only from 35.6% to 42.8%.

### Feature-by-outcome association tests

Tests compare outcome = 1 with outcome = 0. feat_d uses the 850 non-missing rows. Odds ratios (OR) are per SD of each feature, from a univariate logistic model.

![Mean difference in each feature between outcome=1 and outcome=0 rows, with 95% Welch CI; feat_d uses non-missing rows only](tasks/stat_1/charts/stat_mean_diff_forest.png)

- **feat_a:** mean 0.54 when outcome = 1 vs -0.38 when outcome = 0; difference 0.92 (95% CI 0.81 to 1.03). OR per SD 3.30 (95% CI 2.76 to 3.95). p < 0.001, still below 0.001 after Holm correction.
- **feat_d** (n = 850): mean 0.38 vs -0.17; difference 0.55 (95% CI 0.42 to 0.69). OR per SD 1.81 (95% CI 1.55 to 2.12). p < 0.001, still below 0.001 after Holm correction.
- **feat_b:** mean 0.24 vs -0.06; difference 0.30 (95% CI 0.17 to 0.42). OR per SD 1.35 (95% CI 1.18 to 1.54). p < 0.001, still below 0.001 after Holm correction.
- **feat_c:** mean difference 0.004 (95% CI -0.12 to 0.13). OR per SD 1.00 (95% CI 0.88 to 1.14). Mann-Whitney p = 0.90 and logit p = 0.95; not significant after Holm correction.

Ranking by OR per SD: feat_a (3.30) > feat_d (1.81) > feat_b (1.35) > feat_c (1.00). feat_a, feat_d and feat_b are significant after Holm correction across the four features; feat_c is not.

### Joint adjustment for the other features

In one logistic model on the 850 complete rows, with standardized features, each of the three features still predicts outcome after adjusting for the other two (Holm adjustment across the three terms):

- feat_a: OR 3.54 per SD (95% CI 2.88 to 4.36), Holm p = 2.4e-32.
- feat_d: OR 2.07 per SD (95% CI 1.73 to 2.47), Holm p = 3.5e-15.
- feat_b: OR 1.41 per SD (95% CI 1.19 to 1.67), Holm p = 7.0e-05.

The pseudo R² of this model is 0.248. Unadjusted ORs on the same 850 rows were 3.23 (feat_a), 1.34 (feat_b) and 1.81 (feat_d). Each estimate rises slightly after adjustment. The features are nearly uncorrelated (feat_a–feat_b r = 0.053, feat_a–feat_d r = 0.028, feat_b–feat_d r = 0.009), so adjustment changes the estimates little.

### feat_a × feat_b interaction

On standardized features, the interaction term has coefficient 0.066 (OR 1.07, 95% CI 0.89 to 1.28; log-odds CI -0.118 to 0.250), p = 0.48. The additive model gives feat_a OR 3.31 (coefficient 1.197, p = 7e-38) and feat_b OR 1.35 (coefficient 0.303, p = 5.7e-05). Both effects hold without the interaction term.

Outcome rates by feat_a tertile, within each feat_b tertile (cells hold 98 to 124 rows):

| feat_b tertile | Low feat_a | Mid feat_a | High feat_a |
|---|---|---|---|
| Low | 0.12 | 0.28 | 0.55 |
| Mid | 0.16 | 0.41 | 0.68 |
| High | 0.15 | 0.47 | 0.74 |

The low-to-high feat_a rise is 0.43, 0.52 and 0.59 across the low, mid and high feat_b tertiles. Individual steps range from 0.15 to 0.32. The chart below shows the pattern.

![Share of outcome=1 by feat_a tertile, one line per feat_b tertile](tasks/stat_2/charts/interaction_tertile_rates.png)

The interaction is not statistically supported. The test could detect only fairly large interactions, so small ones are not excluded.

### Non-linearity of feat_b

- A quadratic feat_b term does not significantly improve the joint model: LR statistic 1.79, p = 0.18 (n = 850). The quadratic coefficient is -0.082 (p = 0.18).
- A natural spline for feat_b (df = 4) does not improve fit over the linear model: LR statistic 1.94 on 3 df, p = 0.58.
- The feat_b OR per SD is 1.41 (95% CI 1.19 to 1.67) in the linear model and 1.42 (95% CI 1.20 to 1.69) for the linear term in the quadratic model. The quadratic-model value is the slope at the mean of feat_b, not an average effect.

Taken together, these tests give no evidence against a linear feat_b effect on the logit scale. They do not show whether the non-monotone quartile pattern in the univariate outcome rates is real.

### Predictive models and test-split baseline

A stratified 80/20 split with seed 42 gives 800 training rows and 200 test rows. feat_d was median-imputed (0.043) using training data only, with a missing-indicator column. The test set has 39.5% outcome-1 rows, so the majority-class baseline accuracy is 0.605.

Test-set results (200 rows):

| Model | Accuracy | Precision | Recall | F1 | ROC AUC | Log loss | Train accuracy |
|---|---|---|---|---|---|---|---|
| Logistic regression | 0.750 | 0.710 | 0.620 | 0.662 | 0.817 | 0.504 | 0.741 |
| Gradient boosting (default) | 0.755 | 0.688 | 0.696 | 0.692 | 0.807 | 0.528 | 0.869 |

For reference, a constant predictor at the training class-1 rate has log loss 0.671.

![Test accuracy of the majority-class baseline, logistic regression and gradient boosting on the 200-row test set](tasks/ml_2/charts/ml2_accuracy_comparison.png)

Gradient boosting overfits this split: the train-test accuracy gap is 0.114, against -0.009 for logistic regression. Its test figures are therefore optimistic relative to logistic regression. On log loss, logistic regression is better. On ROC AUC the two models are close.

Standardized logistic coefficients and gradient boosting impurity importances:

- **feat_a:** 1.25 (logistic) and 0.513 (boosting).
- **feat_d:** 0.610 and 0.212.
- **feat_b:** 0.375 and 0.181.
- **feat_c:** -0.025 and 0.093.

The two models disagree on feat_c. Impurity importances favour continuous features and are not directly comparable with standardized logistic coefficients, so each ranking should be read within its own model.

### Cross-validation on all 1,000 rows

Under 5-fold stratified CV on all rows (ddof = 1 for SDs):

| Model | Log loss (mean, SD) | ROC AUC (mean, SD) | Accuracy (mean, SD) |
|---|---|---|---|
| Majority baseline | 0.672 (0.001) | 0.500 | 0.603 (0.003) |
| Logistic regression | 0.513 (0.036) | 0.812 (0.033) | 0.746 (0.035) |
| Gradient boosting, default (depth 3, 100 trees) | 0.565 (0.025) | 0.780 (0.017) | 0.730 (0.012) |
| Gradient boosting, regularised (depth 2, 100 trees, lr 0.05, subsample 0.8) | 0.527 (0.024) | 0.802 (0.024) | 0.738 (0.036) |

Paired fold comparisons (logistic minus boosting):

- **Against default boosting:** logistic has lower log loss in all 5 folds (mean difference -0.052) and higher ROC AUC in all 5 folds (mean +0.032).
- **Against regularised boosting:** logistic has lower log loss in all 5 folds (mean -0.015). Its AUC is higher in 4 of 5 folds (mean +0.010). Accuracy is nearly tied (0.746 vs 0.738).

The train-test accuracy gap in CV is about 0.000 for logistic regression, 0.134 (SD 0.019) for default boosting and 0.042 (SD 0.037) for regularised boosting. Regularisation removes most of the overfitting, but a small residual gap remains.

![5-fold stratified CV mean test log loss with fold sd for the majority baseline, logistic regression, default gradient boosting and regularised gradient boosting](tasks/ml_3/charts/ml3_cv_log_loss.png)

### feat_d missingness

- **Marginal association with outcome:** the outcome rate is 41.3% when feat_d is missing (n = 150) and 39.4% when observed. Two tests disagree on the p-value: the eda_2 chi-square gives p = 0.72, and the recomputed chi-square on all 1,000 rows in stat_4 gives p = 0.66 (chi-square 0.197). The reason for the difference has not been identified.
- **Relation to other features (eda_2):** rows with feat_d missing do not differ from observed rows on feat_a (standardized difference -0.07, Welch p = 0.42), feat_b (0.08, p = 0.40) or feat_c (0.02, p = 0.83). All standardized differences are under 0.1. The test cannot rule out small effects.

![Standardized mean differences of feat_a to feat_c between rows with feat_d missing and rows with feat_d observed](tasks/eda_2/charts/feat_d_missing_std_diff.png)

- **Conditional association with outcome (stat_4):** in a logistic model on all 1,000 rows, with feat_a, feat_b and median-imputed feat_d, the missing indicator has adjusted OR 1.09 per SD (95% CI 0.94 to 1.26, p = 0.28). Adjustment moves the OR from 1.03 (unadjusted) to 1.09.
- **Missing-indicator coefficient in the ML model (ml_2):** the standardized logistic coefficient for the indicator is 0.131, and its gradient boosting importance is 0.002. This coefficient comes from the training model on 800 rows, adjusted for feat_d. No interval or p-value is reported for it. It is not directly comparable with the stat_4 result, which uses a different sample and specification.

## Limitations

- **feat_d missingness mechanism is untested.** The tests compare missing and observed rows on the other columns and on outcome. They cannot assess whether missingness depends on feat_d's own unobserved values (MNAR).
- **Unreconciled marginal p-values for feat_d missingness.** eda_2 reports p = 0.72 for the marginal outcome test. stat_4 recomputes p = 0.66 on all 1,000 rows. The two tests may differ in method or sample. This discrepancy has not been resolved, so the eda_2 figure should be checked before it is quoted.
- **feat_d missing-indicator coefficient not tested in the ML model.** The 0.131 coefficient in ml_2 has no interval or p-value. stat_4 provides an interval for the indicator in a different model, which is not directly comparable.
- **feat_b quartile pattern unresolved.** The non-monotone quartile rates (26.8%, 44.4%, 37.6%, 50.0%) are based on about 250 rows per quartile. The non-linearity tests found no evidence against a linear feat_b effect, but they do not explain the quartile pattern. Confounding by feat_a or feat_d was not checked with a binned model.
- **Interaction test has limited power.** Cells hold 98 to 124 rows, so only fairly large interactions could have been detected. The interaction is not statistically supported, but small interactions are not excluded.
- **Associations are not causal.** All effects are observational associations from the models reported.
- **Small test split.** The 200-row test split gives wide uncertainty on accuracy and AUC. The CV results are more stable but still show fold-level SDs of 0.03 to 0.04 on accuracy and log loss.
- **Gradient boosting overfits on the single split and in CV (default).** Regularised boosting narrows the gap but still shows a small residual difference.
- **Feature importance measures are not comparable across models.** Standardized logistic coefficients and impurity importances measure different things. feat_c's contribution in boosting (importance 0.093) may partly reflect the impurity measure's preference for continuous features. Its logistic coefficient is -0.025. Permutation importance has not been run.
- **Missing feat_d handling.** Models using feat_d either drop the 150 missing rows (complete-case analyses such as stat_3) or impute with the training median plus an indicator (ml_1, ml_2, stat_4). Results from the two approaches are not directly interchangeable.
- **No tasks failed.** All tasks were accepted as complete.

## Open questions

- Is feat_d missingness related to its own unobserved values (MNAR)? The data cannot answer this, and the missing-indicator column captures only whether a value is missing, not why.
- Why do the eda_2 (p = 0.72) and stat_4 (p = 0.66) marginal tests of feat_d missingness and outcome differ? Which sample and test did eda_2 use?
- Is the non-monotone feat_b quartile pattern real or noise? Does it reflect confounding by feat_a or feat_d? A binned-effect model adjusted for the other features has not been run.
- Does feat_c's contribution in gradient boosting (importance 0.093) reflect a real non-linear or interaction effect, or the impurity-based measure? Permutation importance under CV has not been run.
- Is the feat_d missing-indicator effect (coefficient 0.131 in the ML model) distinguishable from zero under CV or with a confidence interval?
- Does the logistic regression vs gradient boosting gap in log loss and AUC persist on a larger sample or with more tuning of boosting (fewer estimators, lower learning rate, larger minimum leaf size)?
- Does the feat_a association hold after a sensitivity analysis comparing complete-case and median-imputed-with-indicator feat_d models?