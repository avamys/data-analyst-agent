# Outcome Prediction from Three Numeric Features: Final Report

## Summary

- **feat_b is the only feature with a significant marginal association with outcome.** Its mean differs between outcome groups by 0.363 (95% CI 0.241 to 0.485; Cohen's d = 0.381), and it stays significant after Bonferroni correction across three features. The outcome rate rises across feat_b quartiles from 0.292 to 0.496. In the joint logistic model its odds ratio is 1.50 per unit (95% CI 1.31 to 1.73).
- **feat_a has no linear association with outcome but a U-shaped one.** The outcome rate across feat_a quartiles is 0.536, 0.228, 0.208, 0.548. A quadratic logistic term is strongly supported (LR 246.6, 1 df, p ≈ 1.4e-55), but its extreme-tail predictions are not credible.
- **feat_c shows no meaningful association** (Cohen's d = 0.032, p = 0.62), and no pairwise linear interaction among the three features is significant (smallest p = 0.32).
- **Gradient boosting beats the majority-class baseline and logistic regression on the 200-row test split.** Accuracy is 0.695 against a baseline of 0.62, and ROC AUC is 0.690 against 0.588 for logistic regression. The advantage also holds in all five cross-validation folds on the training portion. Its size is imprecise, and the model fits are weak (McFadden pseudo R² = 0.027 for the interaction logit).
- **Feature importance depends on the model.** In logistic regression feat_b carries nearly all the signal. In gradient boosting feat_a is the most important feature. ml_2 reads this as a possible nonlinear effect of feat_a, a reading that stat_3 tested only at quartile level.

## Data

- 1,000 rows, 4 columns: three numeric features (feat_a, feat_b, feat_c) and one binary target, `outcome`.
- No categorical, date/time, identifier or free-text columns.
- Target split: outcome = 0 at 62%, outcome = 1 at 38%.
- Missing values: none in any column.

## Findings

### Feature distributions and outcome rates by quartile (eda_1)

The three features are approximately standardised and close to symmetric:

- feat_a: mean -0.010, SD 1.016, min -3.267, max 2.804, skew -0.101.
- feat_b: mean 0.023, SD 0.969, min -4.057, max 3.335, skew -0.025.
- feat_c: mean -0.005, SD 0.994, min -3.555, max 3.273, skew -0.041.

Each quartile holds about 250 rows. The outcome=1 rate by quartile (Q1 to Q4) is:

- **feat_a:** 0.536, 0.228, 0.208, 0.548. This is U-shaped.
- **feat_b:** 0.292, 0.352, 0.380, 0.496. This rises steadily.
- **feat_c:** 0.372, 0.363, 0.402, 0.384. This varies little, so its marginal quartile signal is weak.

![Histograms of feat_a, feat_b, feat_c: row counts per value bin](tasks/eda_1/charts/eda_histograms.png)

![Outcome=1 rate per quartile bin of feat_a, feat_b, feat_c (dashed line: overall rate)](tasks/eda_1/charts/quartile_outcome_rates.png)

### Significant associations and effect sizes (stat_1)

- **feat_b:** The mean is -0.115 for outcome=0 and 0.248 for outcome=1, a difference of 0.363 (95% CI 0.241 to 0.485). Welch t = 5.84, p = 7.8e-09, Bonferroni-adjusted p = 2.3e-08. Point-biserial r = 0.182 (95% CI 0.121 to 0.241). Cohen's d = 0.381. This is the only feature significant after correction.
- **feat_a:** The mean difference is -0.015 (95% CI -0.163 to 0.134). Welch t = -0.197, p = 0.844, Bonferroni-adjusted p = 1.0. Point-biserial r = -0.007. Cohen's d = -0.015. A linear test does not capture the U-shape.
- **feat_c:** The mean difference is 0.032 (95% CI -0.096 to 0.160). Welch t = 0.495, p = 0.620, Bonferroni-adjusted p = 1.0. Point-biserial r = 0.016. Cohen's d = 0.032. The effect is negligible.

![Mean of feat_a, feat_b and feat_c for outcome=0 and outcome=1 (bars), 1000 rows](tasks/stat_1/charts/stat1_group_means.png)

### Interactions and joint linear model (stat_2)

- No pairwise linear-by-linear interaction is significant. feat_b × feat_c has OR 1.08 (95% CI 0.93 to 1.24, p = 0.32). feat_a × feat_b has OR 1.05 (95% CI 0.92 to 1.21, p = 0.44). feat_a × feat_c has OR 0.99 (95% CI 0.87 to 1.13, p = 0.88).
- These tests cover only linear product terms. They do not rule out nonlinear or U-shaped dependence.
- Because no interaction was significant, the median split on a moderating feature was not run.
- In the joint model without interactions, feat_b is significant: OR 1.50 per unit (95% CI 1.31 to 1.73, p = 1.2e-08). feat_a (OR 0.98, p = 0.70) and feat_c (OR 1.05, p = 0.44) show no linear main effect.
- The full interaction model has McFadden pseudo R² = 0.027 (log-likelihood -645.96, n = 1,000).

### Nonlinear effect of feat_a (stat_3)

- Adding a squared feat_a term to the logistic model improves fit: LR statistic 246.6 on 1 df, p ≈ 1.4e-55; AIC falls from 1301.5 (linear) to 1056.8 (quadratic). The LR test controls for feat_b and feat_c.
- Quadratic model coefficients (feat_b and feat_c held in the model):
  - feat_a (linear term): 0.0032, p = 0.97.
  - feat_a squared: 1.0292, p reported as 0.0.
  - feat_b: 0.5965, p reported as 0.0.
  - feat_c: 0.0804, p = 0.295.
- The linear model's feat_a coefficient is not available in the accepted results, so it is not reported.
- Predicted outcome=1 probability by feat_a quartile from the quadratic model is 0.536, 0.220, 0.227, 0.537. Observed rates are 0.536, 0.228, 0.208, 0.548. Each bin is within about 0.02 of observed.
- The fitted curve has its vertex at feat_a ≈ -0.002, with a predicted minimum of 0.18. The observed Q2 and Q3 rates are 0.228 and 0.208. The predicted minimum is therefore lower than both observed rates, and the fit reproduces the pattern but does not match those two bins exactly.
- At the observed feat_a extremes, with feat_b and feat_c at their means, the quadratic predicts 0.9999 at the minimum (-3.267) and 0.9986 at the maximum (2.804). No observed quartile rate is near 1, so these values are not credible.

![Predicted outcome=1 probability across feat_a for linear and quadratic logistic models, feat_b and feat_c held at their means](tasks/stat_3/charts/stat3_feat_a_fit.png)

### Predictive performance against the baseline (ml_1, ml_2)

- The stratified 80/20 split (seed 42) gives 800 training and 200 test rows. The outcome=1 rate is 0.38 in both (304 of 800; 76 of 200).
- The majority-class baseline on the test set has accuracy 0.62 and positive-class F1 0.0.
- Test-set results (n = 200, 76 positive):

| Model | Accuracy | ROC AUC | Log loss | Positive-class F1 |
|---|---|---|---|---|
| Majority-class baseline | 0.62 | – | – | 0.0 |
| Logistic regression | 0.625 | 0.588 | 0.649 | 0.194 |
| Gradient boosting | 0.695 | 0.690 | 0.631 | 0.496 |

- Logistic regression's accuracy (0.625) is essentially tied with the baseline (0.62). Its gains are in ROC AUC and positive-class F1.
- Gradient boosting scores higher on all four metrics. ml_2 states that this rests on a single 200-row split with no uncertainty estimate, so the size of the advantage is not established as statistically significant.

![Test-set accuracy, ROC AUC and F1 for the positive class: logistic regression vs gradient boosting (n=200 test rows)](tasks/ml_2/charts/ml2_model_comparison.png)

### Feature importance (ml_2)

These two results disagree about which feature matters most, and the report keeps both:

- **Logistic regression (standardised):** feat_b dominates, with coefficient 0.397 and a permutation drop in test ROC AUC of 0.091 (SD 0.037). feat_c (coefficient 0.043; ROC AUC change 0.003) and feat_a (coefficient -0.035; change -0.002) contribute almost nothing.
- **Gradient boosting:** feat_a has the largest permutation drop in test ROC AUC, 0.149 (SD 0.038). feat_b follows at 0.033 (SD 0.017), then feat_c at 0.007 (SD 0.010). ml_2 states that logistic regression misses feat_a's signal.

### Reliability of the gradient boosting advantage (ml_3)

- **Test split, ROC AUC:** The advantage is 0.110 with a paired bootstrap 95% CI of 0.026 to 0.197. 99.4% of the 2,000 resamples favour gradient boosting. The interval excludes zero.
- **Test split, accuracy:** The advantage is 0.100 with a paired bootstrap 95% CI of 0.035 to 0.170. 99.8% of resamples favour gradient boosting. The interval excludes zero.
- **Five-fold stratified CV on the training portion:** Gradient boosting has higher ROC AUC in all five folds (mean difference 0.150, SD 0.029) and higher accuracy in all five folds (mean difference 0.093, SD 0.026).
- The advantage holds on both metrics on the test split and across CV folds. Its size is less certain. The bootstrap resamples only the 200 test rows (76 positives), so the true gap may be much smaller than the point estimates.

## Limitations

- **Small sample for prediction.** The test set has 200 rows and 76 positives. The model comparison in ml_2 has no uncertainty estimate, and the bootstrap in ml_3 resamples only those rows.
- **Weak models.** The interaction logit has McFadden pseudo R² = 0.027. The best model's test ROC AUC is 0.690, a modest value, so these three features explain little of the outcome variation.
- **Interaction tests are limited.** Only linear-by-linear pairwise products were tested. Nonlinear or U-shaped dependence between features is not covered.
- **The feat_a U-shape is verified only at quartile level.** Its tail behaviour is not verified. The quadratic's predictions at the observed feat_a extremes (0.9999 and 0.9986) are implausible, and no observed quartile rate is near 1. Observed outcome rates in the far tails of feat_a (below the Q1 cut and above the Q4 cut) have not been checked.
- **Unresolved review issues (stat_3).** The lead's review raised three issues, which stand:
  1. The brief requires the coefficients and their significance. The quadratic model's coefficients are reported above. The linear model's feat_a coefficient is not available in the accepted results, so it is not reported.
  2. The quadratic's predicted minimum of 0.18 is lower than the observed Q2 and Q3 rates (0.228 and 0.208). The fit reproduces the pattern but does not match those bins exactly, and the earlier wording "within bin-level error" is withdrawn.
  3. The U-shape beyond the quartile range, including the predictions near 1 in the tails, is not verified.
- **Affected findings.** The U-shape, the quadratic fit and the feat_a importance ranking in gradient boosting all depend on the unverified nonlinear form.
- **Conflicting statements on significance.** ml_2 describes the gradient boosting advantage as not established as statistically significant. ml_3 reports bootstrap intervals for the same differences that exclude zero. Both are reported here; the difference is not resolved.
- **Failed tasks.** None.

## Open questions

- Is the U-shape in feat_a better captured by a nonlinear term or an interaction than by a linear effect? The quadratic has been tested, but a natural spline and interaction terms have not.
- Do the observed outcome rates in the far tails of feat_a support or contradict the near-1 predictions from the quadratic?
- Does a natural spline for feat_a, with more knots, fit the quartile pattern and tails better than the single quadratic term?
- Does an interaction between feat_a and feat_b or feat_c change the U-shape?
- Does feat_b's monotone rise in outcome rate hold after controlling for feat_a and feat_c? The joint logit gives OR 1.50 per unit, but the joint model did not include the quadratic term.
- Is feat_c's weak marginal association hiding an interaction with feat_a or feat_b?
- Does adding spline or squared terms for feat_a to logistic regression close the ROC AUC gap with gradient boosting?
- Why does the bootstrap point estimate of the ROC AUC advantage (0.110) differ from the gap implied by the reported test ROC AUCs (0.690 and 0.588)? Do both use the same split and model settings? This was raised in ml_3 and is not answered by the accepted results.
- Would repeated or nested cross-validation on the full dataset tighten the estimate of the advantage?
- Which unmeasured factors explain most of the outcome variation, given the low pseudo R²?