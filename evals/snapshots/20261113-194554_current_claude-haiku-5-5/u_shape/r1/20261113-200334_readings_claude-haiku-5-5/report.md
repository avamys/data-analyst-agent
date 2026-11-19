# Outcome Analysis of 1,000 Rows with Three Numeric Features (feat_a, feat_b, feat_c) and a Binary Outcome

## Summary

- **feat_b has a monotone rising association with the outcome.** The outcome rate rises from 29.2% in the lowest feat_b quartile to 49.6% in the highest. The Welch test of the mean difference between outcome groups is significant (p about 8e-9, Bonferroni-adjusted p about 2.3e-8), with a difference of 0.363 (95% CI 0.241 to 0.485).
- **feat_a has a U-shaped association with the outcome, which a mean-difference test misses.** Outcome rates are 53.6% and 54.8% in the lowest and highest feat_a quartiles, against 20.8% and 22.8% in the middle two. In a logistic model, the quadratic feat_a term is strongly significant (p = 6.9e-31), while the linear term is not (p = 0.90).
- **feat_c shows no detectable association with the outcome.** Its quartile rates lie between 36% and 40%, its mean-difference test gives p = 0.620, and its logistic coefficient, controlling for all three features, gives p = 0.354.
- **No pairwise interaction was detected among the linear terms.** The likelihood-ratio test of three pairwise product terms gives p = 0.67. This test would not detect modification of feat_a's non-linear effect.
- **Prediction gains are modest.** Gradient boosting reaches test accuracy 0.695 and test ROC AUC 0.691, against a majority-class baseline of 0.62 accuracy and 0.5 AUC. Logistic regression reaches test accuracy 0.625 and ROC AUC 0.588. The gradient boosting model overfits (train accuracy 0.864), and its permutation importance is largest for feat_a (mean drop in test ROC AUC 0.148).

## Data

- **Size:** 1,000 rows and 4 columns.
- **Target:** `outcome`, binary. Class 0 is 62.0% of rows and class 1 is 38.0%.
- **Features:** three numeric features, feat_a, feat_b and feat_c. There are no categorical, date/time, identifier or free-text columns.
- **Missing values:** none in any column (0 missing cells).
- **Feature distributions:** all three are roughly centred and unskewed. Means are -0.01, 0.02 and -0.00, standard deviations are 1.02, 0.97 and 0.99, and skew values are -0.10, -0.03 and -0.04 for feat_a, feat_b and feat_c respectively.

## Findings

### Outcome distribution and quantile bins

The overall outcome rate is 38% (0.38). Outcome rates were computed within quartile bins of each feature, with 250 rows per bin for feat_a and feat_b and 249 to 251 for feat_c.

**feat_a (U-shaped):**

| Quartile | Count | Mean feat_a | Outcome rate |
|---|---|---|---|
| Q1 | 250 | -1.31 | 53.6% |
| Q2 | 250 | -0.33 | 22.8% |
| Q3 | 250 | 0.31 | 20.8% |
| Q4 | 250 | 1.28 | 54.8% |

![Outcome rate by feat_a quartile bin](tasks/eda_1/charts/feat_a_outcome_rate_by_quartile.png)

**feat_b (monotone rising):**

| Quartile | Count | Mean feat_b | Outcome rate |
|---|---|---|---|
| Q1 | 250 | -1.20 | 29.2% |
| Q2 | 250 | -0.30 | 35.2% |
| Q3 | 250 | 0.34 | 38.0% |
| Q4 | 250 | 1.26 | 49.6% |

![Outcome rate by feat_b quartile bin](tasks/eda_1/charts/feat_b_outcome_rate_by_quartile.png)

**feat_c (flat):**

| Quartile | Count | Mean feat_c | Outcome rate |
|---|---|---|---|
| Q1 | 250 | -1.26 | 37.2% |
| Q2 | 251 | -0.34 | 36.3% |
| Q3 | 249 | 0.33 | 40.2% |
| Q4 | 250 | 1.25 | 38.4% |

![Outcome rate by feat_c quartile bin](tasks/eda_1/charts/feat_c_outcome_rate_by_quartile.png)

### Feature differences between outcome groups

Welch t-tests compare each feature's mean between outcome=1 and outcome=0. The three tests were corrected for multiplicity with Bonferroni and Holm.

- **feat_b:** mean 0.248 for outcome=1 against -0.115 for outcome=0. The difference is 0.363 (95% CI 0.241 to 0.485), p about 8e-9, Cohen's d 0.381. The result survives Bonferroni (p about 2.3e-8) and Holm correction across the three tests.
- **feat_a:** mean -0.019 for outcome=1 against -0.004 for outcome=0. The difference is -0.015 (95% CI -0.163 to 0.134), p = 0.844, Cohen's d -0.015. It does not survive correction. The mean-difference test does not capture the U-shape reported in the EDA.
- **feat_c:** mean 0.015 for outcome=1 against -0.017 for outcome=0. The difference is 0.032 (95% CI -0.096 to 0.160), p = 0.620, Cohen's d 0.032. It does not survive correction.

In a logistic regression with all three features, the coefficients are:

- feat_b: 0.406 per unit (95% CI 0.267 to 0.545, p about 1e-8). Feature standard deviations are about 1, so this is approximately per standard deviation.
- feat_a: -0.021 per unit (95% CI -0.149 to 0.108, p = 0.75).
- feat_c: 0.062 per unit (95% CI -0.069 to 0.193, p = 0.354).

![Cohen d (outcome 1 vs 0) per feature](tasks/stat_1/charts/cohen_d_by_feature.png)

### Shape of the feat_a relation

The U-shape appears when feat_a is split into deciles. Outcome rates by decile, from lowest to highest feat_a, are:

| Decile | n | Mean feat_a | Outcome rate |
|---|---|---|---|
| 1 | 100 | -1.82 | 77% |
| 2 | 100 | -1.05 | 43% |
| 3 | 100 | -0.70 | 28% |
| 4 | 100 | -0.38 | 27% |
| 5 | 100 | -0.13 | 16% |
| 6 | 100 | 0.10 | 16% |
| 7 | 100 | 0.37 | 24% |
| 8 | 101 | 0.70 | 28% |
| 9 | 100 | 1.06 | 44% |
| 10 | 99 | 1.75 | 78% |

Both tails are high: decile 1 is at 77% and decile 10 at 78%, so the U comes from both tails. The lowest rates are in deciles 5 and 6, at 16% each.

A logistic model with linear and quadratic feat_a terms gives a quadratic coefficient of 0.937 (95% CI 0.778 to 1.096, p = 6.9e-31). The linear coefficient is 0.010 (p = 0.90), which confirms significant curvature. The fitted quadratic's vertex, where the fitted logit-scale outcome is at its minimum, is at -0.005, close to the feat_a mean of -0.01. The fitted logit quadratic is symmetric about that vertex. The observed bottom and top decile rates (77% and 78%) are only approximately equal.

![Outcome rate by feat_a decile](tasks/stat_3/charts/feat_a_outcome_rate_by_decile.png)

### Pairwise interactions

A likelihood-ratio test of adding three pairwise product terms (feat_a×feat_b, feat_a×feat_c, feat_b×feat_c) to the logistic model gives LR = 1.54 on 3 degrees of freedom, p = 0.67. The individual terms are:

- feat_a×feat_b: coefficient 0.053 (95% CI -0.082 to 0.189, p = 0.44)
- feat_a×feat_c: coefficient -0.010 (95% CI -0.140 to 0.121, p = 0.88)
- feat_b×feat_c: coefficient 0.073 (95% CI -0.071 to 0.216, p = 0.32)

All intervals include zero. This is evidence against linear pairwise modification of the feat_b and feat_c slopes by feat_a. It is not proof that feat_a never modifies them. Because no interaction was significant, two-by-two median-split outcome rates were not computed.

### Predictive models

The data were split into 800 training and 200 test rows, stratified on the outcome, with seed 42. The majority-class baseline has test accuracy 0.62 and ROC AUC 0.5.

| Model | Train accuracy | Test accuracy | Test ROC AUC | Test log loss |
|---|---|---|---|---|
| Majority-class baseline | n/a | 0.62 | 0.5 | n/a |
| Logistic regression | 0.63 | 0.625 | 0.588 | 0.649 |
| Gradient boosting | 0.864 | 0.695 | 0.691 | 0.631 |

- **Logistic regression** has test precision 0.529, recall 0.118 and F1 0.194. Its test accuracy of 0.625 is no meaningful gain over the 0.62 baseline. Its largest absolute coefficient is feat_b (0.397), followed by feat_c (0.043) and feat_a (0.035). These coefficients come from the model fitted on the 800 training rows.
- **Gradient boosting** has test precision 0.667, recall 0.395 and F1 0.496. It is the better of the two models on every test metric. Its train accuracy is 0.864 against a test accuracy of 0.695, which indicates overfitting. The finding states that the test figure is likely optimistic for new data.

Permutation importance for gradient boosting, measured as the drop in test ROC AUC over 30 repeats, is:

- feat_a: mean drop 0.148 (sd 0.038)
- feat_b: mean drop 0.031 (sd 0.017)
- feat_c: mean drop 0.006 (sd 0.010), which the finding describes as not clearly above zero

The finding notes that feat_a's near-zero logistic coefficient is consistent with its U-shaped relation to the outcome, which a linear model cannot represent.

![Permutation feature importance of the gradient boosting model on the held-out test set](tasks/ml_1/charts/gbm_perm_importance.png)

![Test-set ROC AUC of the majority baseline, logistic regression and gradient boosting](tasks/ml_1/charts/model_comparison_auc.png)

## Limitations

- **Unresolved review issues in the decile analysis (stat_3).** The lead's objections to that task still stand. They affect the feat_a shape finding and its quadratic-vertex statement:
  1. The claim that the top-end rise alone produces the U has been removed. Both tails are high (decile 1 at 77%, decile 10 at 78%), so the U comes from both tails.
  2. The outcome rates for all ten deciles, including deciles 4 and 7, are reported in the table above.
  3. The vertex statement is worded as a symmetry of the fitted logit quadratic about its vertex at about -0.005. The observed bottom and top decile rates (77% and 78%) are only approximately equal.
- **Linear-only interaction test (stat_2).** The interaction test uses linear product terms only. Because feat_a's effect is non-linear, a modification of that effect by feat_b or feat_c would not be detected by these terms.
- **Overfitting and small test set (ml_1).** Gradient boosting overfits, so its test scores are likely optimistic. The 200-row test set adds further uncertainty, and no repeated cross-validation was run. The feat_c permutation importance (mean 0.006, sd 0.010) is not clearly above zero.
- **Different fits for different coefficients.** The logistic coefficients in the statistics tasks come from a model fitted on all 1,000 rows. The feature ranking in the ML task comes from a model fitted on the 800 training rows. The two are not the same fit. Both put feat_b first and feat_a and feat_c small.
- **Failed tasks.** None. All tasks (eda_1, stat_1, stat_2, ml_1, stat_3) completed.

## Open questions

- Is the U-shaped effect of feat_a better captured by a squared term, a spline or another non-linear model fitted jointly with feat_b and feat_c? The findings do not establish how the quadratic term behaves alongside the other two features.
- Does feat_a's U-shaped effect interact with feat_b or feat_c once non-linear terms are included? The linear interaction test cannot answer this.
- Is the weak feat_c signal real, or noise? Its logistic coefficient controlling for feat_a and feat_b is not significant (p = 0.354), but repeated cross-validation has not confirmed that it adds nothing to prediction.
- Does a tuned, regularised non-linear model reduce the gradient boosting train-test gap and improve the test ROC AUC of 0.691?
- Is the upper-tail rise in feat_a (deciles 9 and 10) driven by a subgroup or a different mechanism? The analysis did not examine this.
- Do feat_b and feat_c interact beyond the linear pairwise terms tested, or through higher-order terms?