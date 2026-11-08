# Outcome Analysis of 800 Survey Rows: Binary Target `outcome`

## Summary

- **No feature or group shows a statistically significant association with outcome.** Group is not associated with outcome (chi-square = 3.75, df = 3, p = 0.289, Cramér's V = 0.068). None of feat_1 to feat_5 differs significantly between outcome classes, and every Holm-adjusted p-value across the 11 primary tests is 1.0.
- **One nominal result, a lower outcome rate in the feat_3 top quartile (34.5% vs 43.3%), does not survive correction.** It has Fisher p = 0.031 unadjusted and Holm-adjusted p = 0.371. After adjustment for group and feat_1 to feat_5 it is nominal (OR 0.60, 95% CI 0.37 to 0.98, p = 0.040), but it is not significant once a non-linear feat_3 term is added (p = 0.177). The cut was chosen after looking at the data, so the result is exploratory.
- **Predictive models show no out-of-sample signal.** On the 160-row test set, logistic regression reached accuracy 0.550 and gradient boosting 0.531, both below the majority-class accuracy of 0.588. Test ROC AUC was 0.391 and 0.467. Repeated stratified 5-fold CV on all 800 rows gave a mean AUC of 0.509 for a strongly regularized logistic regression and 0.479 for a depth-2 gradient boosting model.
- **Interaction evidence is weak and conflicting.** The feat_3 by group interaction has a likelihood-ratio p of 0.026 in one model (Holm p = 0.132) and a group by top-quartile interaction p of 0.130 in another. Neither survives correction, and the two tests are not reconciled.

## Data

- 800 rows and 7 columns: five numeric features (feat_1 to feat_5), one categorical group column (levels g1 to g4), and a binary target `outcome`.
- Outcome classes: 0 at 58.9% and 1 at 41.1% (overall outcome-1 rate 41.1%).
- Missing values: none in any column, so no rows were dropped.
- No date or time features, and no identifier or free-text columns.

## Findings

### Outcome and feature distributions by group and quantile

The overall outcome-1 rate is 41.1% across all 800 rows. Outcome rates by group level were:

| Group | Outcome-1 rate | n |
|---|---|---|
| g1 | 46.2% | 182 |
| g2 | 42.2% | 206 |
| g3 | 40.0% | 200 |
| g4 | 36.8% | 212 |

![Outcome rate (share of outcome=1) by group level (left) and by feat_1 quartile (right)](tasks/eda_1/charts/outcome_rate_by_group_and_feat1_quartile.png)

Quartile outcome rates varied as follows:
- **feat_3:** Q1 42.5%, Q2 43.5%, Q3 44.0%, Q4 34.5%. The top quartile is the lowest.
- **feat_4:** Q1 39.8%, Q2 42.2%, Q3 44.0%, Q4 38.5%.
- **feat_1:** Q1 44.0%, Q2 39.5%, Q3 38.5%, Q4 42.5%.
- **feat_2:** Q1 39.5%, Q2 43.5%, Q3 41.5%, Q4 40.0%.
- **feat_5:** Q1 38.5%, Q2 40.0%, Q3 43.5%, Q4 42.5%.

Mean feature values by outcome class were as follows.
- feat_5: 0.001 for outcome 0 and 0.092 for outcome 1.
- feat_3: 0.055 and -0.027.
- feat_2: -0.006 and 0.011.
- feat_1: 0.011 and -0.002.
- feat_4: 0.062 and 0.057.

The feat_5 difference is the largest of the five, and feat_4 is the smallest.

### Group association with outcome

Group is not significantly associated with outcome: chi-square = 3.75, df = 3, p = 0.289, Cramér's V = 0.068, which is negligible. The 95% Wilson intervals overlap heavily:
- g1: 46.2% (39.1% to 53.4%)
- g2: 42.2% (35.7% to 49.1%)
- g3: 40.0% (33.5% to 46.9%)
- g4: 36.8% (30.6% to 43.5%)

![Outcome rate (share of outcome=1) by group level with 95% Wilson confidence intervals; chi-square p = 0.289](tasks/stat_1/charts/group_outcome_rate_ci.png)

### Numeric features by outcome class

None of feat_1 to feat_5 differs significantly between outcome classes. Welch p-values run from 0.207 (feat_5) to 0.944 (feat_4), and Mann-Whitney p-values from 0.18 to 0.98. Effect sizes are negligible (|Cohen's d| about 0.1 or less).

| Feature | Mean difference (outcome 1 minus 0) | 95% CI | Welch p | Cohen's d |
|---|---|---|---|---|
| feat_5 | 0.091 | -0.051 to 0.233 | 0.207 | 0.09 |
| feat_3 | -0.082 | -0.222 to 0.057 | 0.246 | -0.08 |
| feat_1 | -0.014 | -0.160 to 0.132 | 0.855 | -0.01 |
| feat_2 | 0.017 | -0.124 to 0.158 | 0.813 | 0.02 |
| feat_4 | -0.005 | -0.143 to 0.133 | 0.944 | -0.00 |

### feat_3 top quartile

- Top quartile: 34.5% outcome-1 (95% CI 28.3% to 41.3%, n = 200). Rest of sample: 43.3% (95% CI 39.4% to 47.3%, n = 600).
- Difference: -0.088 (95% CI -0.165 to -0.011). Fisher exact p = 0.031, odds ratio 0.69, chi-square p = 0.028, phi = 0.078 (small).
- Holm-adjusted across the 12 tests in the analysis, p = 0.371. It does not survive correction.
- This was a post-hoc quartile split, not a pre-specified test.

**Adjusted for group and feat_1 to feat_5 (logistic regression):**
- Top quartile vs Q1 to Q3: OR 0.60 (95% CI 0.37 to 0.98, p = 0.040).
- Linear feat_3 term: OR 0.92 per SD (95% CI 0.80 to 1.06, p = 0.244). No significant monotone linear trend.
- Adding quadratic and cubic feat_3 terms does not significantly improve the model (LR chi-square = 3.91, df = 2, p = 0.142).
- With those non-linear terms included, the top-quartile OR is 0.66 (95% CI 0.37 to 1.20, p = 0.177). The LR test for the top-quartile indicator gives p = 0.176.

The feat_3 pattern is therefore not clearly monotone or clearly non-linear. The adjusted top-quartile result is nominal in the simplest model and is not robust to a flexible specification of feat_3.

### Feature by group interaction

- Likelihood-ratio tests for feature-by-group interaction (logit, Holm-adjusted across five features):

| Feature | LR | df | p | Holm p |
|---|---|---|---|---|
| feat_1 | 1.12 | 3 | 0.772 | 1.0 |
| feat_2 | 6.71 | 3 | 0.082 | 0.327 |
| feat_3 | 9.22 | 3 | 0.026 | 0.132 |
| feat_4 | 1.42 | 3 | 0.701 | 1.0 |
| feat_5 | 3.43 | 3 | 0.330 | 0.991 |

- No interaction is significant after correction. feat_3 is the only nominal case.
- In a logit model with a feat_3 by group interaction and the other features, per-group feat_3 log-odds slopes were: g1 0.01 (95% CI -0.29 to 0.32), g2 -0.40 (95% CI -0.69 to -0.12), g3 -0.12 (95% CI -0.40 to 0.16), and g4 0.20 (95% CI -0.09 to 0.49). The slopes appear to diverge, but the interaction is not significant after correction. These slopes are exploratory.

![Per-group logit slope of feat_3 on outcome with 95% CI, from a logistic model with feat_3 x group interaction](tasks/stat_2/charts/feat3_group_slopes.png)

**Conflicting result on the same question.** The adjusted model in the stat_3 analysis tested a group by feat_3 top-quartile interaction and found LR chi-square = 5.64, df = 3, p = 0.130. This is a different specification from the stat_2 feat_3 by group test (p = 0.026). The two results disagree in strength, and this report does not resolve the difference. The group variation claim rests only on the top-quartile interaction test (p = 0.130), which is not significant.

### Predictive models

**Hold-out test (80/20 stratified split, seed 42; 640 train, 160 test):**

| Model | Test accuracy | Test ROC AUC | Test log loss |
|---|---|---|---|
| Logistic regression | 0.550 | 0.391 | 0.708 |
| Gradient boosting | 0.531 | 0.467 | 0.754 |
| Majority-class baseline | 0.588 | — | — |
| Constant prior-rate baseline | — | 0.5 | 0.678 |

- Neither model beats the majority-class accuracy.
- Gradient boosting's test log loss of 0.754 is 0.076 worse than the constant prior-rate baseline (0.678). Logistic regression's is 0.708.
- Gradient boosting overfits: train accuracy 0.836, train AUC 0.949, and 5-fold CV AUC 0.472. Logistic regression's train AUC was 0.586 and its CV AUC 0.546 (SD 0.050).

![Test accuracy of logistic regression and gradient boosting against the always-majority baseline](tasks/ml_1/charts/ml_1_accuracy.png)

**Feature importance on the hold-out test.** The two methods disagree, so no feature ranking is reliable.
- Logistic regression permutation importance (drop in test AUC): feat_3 +0.023, feat_2 +0.004, feat_4 -0.010, feat_1 -0.018, feat_5 -0.038, group -0.067. Only feat_3 and feat_2 show a positive drop.
- Logistic regression coefficient magnitude: group g4 0.356, group g1 0.203, feat_5 0.139, group g2 0.134, feat_1 0.064, feat_4 0.055, feat_3 0.048, feat_2 0.034, group g3 0.024.
- Gradient boosting impurity importance: feat_3 0.249, feat_4 0.196, feat_1 0.181, feat_2 0.170, feat_5 0.147, with group summing to 0.056 across its columns. This ranking reflects overfitting.

**Repeated stratified 5x5 CV on all 800 rows:**

| Model | Mean ROC AUC (SD) | Log loss vs prior baseline (0.677) | Mean accuracy |
|---|---|---|---|
| Logistic regression, strong L2 (C = 0.1) | 0.509 (0.039) | 0.683 (worse by 0.005) | 0.575 |
| Gradient boosting, depth 2, 100 trees | 0.479 (0.048) | 0.703 (worse by 0.026) | 0.558 |

- The majority-class accuracy on all 800 rows is 0.589 (471 of 800 rows are outcome 0).
- The regularized logistic regression's mean AUC is not meaningfully above 0.5 given its SD. The depth-2 gradient boosting model is at or slightly below chance.
- The analysis concludes that the outcome is essentially unpredictable from feat_1 to feat_5 and group. The CV folds are not independent, so the SDs understate the uncertainty in the means.

## Limitations

- **Statistical power:** None of the feature or group tests is significant, and the confidence intervals are wide. Absence of significance is not evidence of no effect.
- **Multiple comparisons:** Holm correction across the 11 primary tests left all p-values at 1.0. Across 12 tests, including the feat_3 top-quartile test, its adjusted p is 0.371.
- **Post-hoc feat_3 cut:** The top-quartile split was chosen after examining the data. Its adjusted OR (0.60, p = 0.040) is nominal, is not significant under a non-linear feat_3 specification (p = 0.177), and is not significant after Holm correction. Treat it as a hypothesis for confirmation, not an established effect.
- **Conflicting interaction results:** The feat_3 by group interaction is p = 0.026 in the stat_2 model (Holm p = 0.132) and p = 0.130 in the stat_3 group by top-quartile test. The two tests use different specifications. They have not been reconciled.
- **Small hold-out set:** The 160-row test set makes the hold-out accuracy and AUC estimates imprecise. Model results rely on the 5x5 repeated CV, whose folds are not independent.
- **Unresolved review issue (eda_1):** The feat_1 class-mean gap should be reported as 0.014, not 0.013. The feat_1 means are 0.0114 for outcome 0 and -0.0022 for outcome 1, a gap of 0.0136, which rounds to 0.014. The stat_1 mean difference (outcome 1 minus outcome 0) is -0.014. The rest of the eda_1 results stand.
- **Unresolved review issue (stat_3):** The within-group top-quartile rates for g1 to g4 have no recorded basis, so they are omitted from this report. The group-variation claim rests only on the recorded interaction test (LR chi-square = 5.64, df = 3, p = 0.130). Any explanation for the difference from stat_2 is unverified and is not offered here.
- **Failed tasks:** None. All tasks (eda_1, stat_1, stat_2, stat_3, ml_1, ml_2) completed.

## Open questions

- Does the feat_3 top-quartile drop hold on a pre-specified cut, such as a clinically motivated threshold, or with a spline on feat_3 in an independent sample?
- Does the feat_3 top-quartile effect change across cut points? A scan with correction for multiple looks has not been done.
- Which of the two conflicting feat_3 by group interaction results (stat_2 p = 0.026; stat_3 p = 0.130) reflects the true pattern? Do group-specific feat_3 effects exist?
- Is the stat_2 group-specific feat_3 slope pattern (for example, the group 2 slope) driven by the top-quartile drop?
- Does a bootstrap of the feat_3 by group interaction LR statistic, or a larger sample, support the nominal interaction?
- Does feat_5 (mean difference 0.091, not significant) carry any predictive signal once a model is fitted? The models so far show none.
- Do any subgroups show signal that the pooled model misses?