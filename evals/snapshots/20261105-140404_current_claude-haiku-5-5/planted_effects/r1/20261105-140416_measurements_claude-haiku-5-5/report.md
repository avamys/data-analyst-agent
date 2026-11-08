# Outcome Analysis of a 1,000-Row Dataset: Predictors of a Binary Outcome

## Summary

- **feat_a is the dominant predictor.** Its outcome rate rises from 11.6% in the lowest quartile to 70.8% in the highest. It has the largest group difference (Cohen's d 1.05) and the largest logistic odds ratio (3.54 per SD).
- **feat_d is a medium, independent predictor.** On the 850 rows where it is observed, its outcome rate rises from 24.9% to 58.2% across quartiles, and it keeps a significant odds ratio (2.07 per SD) alongside feat_a and feat_b. feat_b is a small but significant predictor (odds ratio 1.41 per SD). feat_c shows no relation to outcome.
- **A logistic regression on the four features beats the majority-class baseline.** On the 200-row test set it reaches 75.5% accuracy and ROC AUC 0.821, against 60.5% accuracy and AUC 0.5 for the baseline. Gradient boosting matches its accuracy but has lower AUC (0.801) and overfits the training data.
- **feat_d missingness shows no detectable relation to the outcome or to the other measured columns.** The tests have limited power with 150 missing rows, and the missingness mechanism cannot be checked against unobserved variables.

## Data

- **Size:** 1,000 rows, 5 columns: four numeric features (feat_a, feat_b, feat_c, feat_d) and a binary target, `outcome`. There are no categorical, date/time, identifier or free-text columns.
- **Target:** outcome is 60.3% class 0 and 39.7% class 1.
- **Missing values:** feat_d is missing for 15.0% of rows (150 rows). No other column has missing values.

## Findings

### Distributions and outcome rates by quartile

All four features are centred near zero, with standard deviations near 1 and ranges of about 6.3 to 6.7, so their distributions look alike. The differences lie in how strongly each relates to outcome.

- **feat_a** has the strongest relation. The outcome rate rises steadily across quartiles: 11.6% (Q1, n=251), 32.5% (Q2, n=249), 44.0% (Q3, n=250), 70.8% (Q4, n=250). Summary: mean -0.013, median 0.056, sd 0.990.
- **feat_b** has a moderate, non-monotone relation: 26.8% (Q1), 44.4% (Q2), 37.6% (Q3), 50.0% (Q4), 250 rows per bin. The dip at Q3 has not been tested against sampling noise.
- **feat_c** shows essentially no gradient: 38.8%, 42.8%, 35.6%, 41.6% across Q1 to Q4 (250 rows per bin).
- **feat_d** has a clear upward gradient on the 850 non-missing rows: 24.9% (Q1, n=213), 35.4% (Q2, n=212), 39.2% (Q3, n=212), 58.2% (Q4, n=213).

![Outcome rate by quartile bin of each feature; feat_d uses non-missing rows](tasks/eda_1/charts/eda1_outcome_rate_by_quartile.png)

### Group differences and effect sizes

Each feature was compared between outcome=1 and outcome=0 with Welch and Mann-Whitney tests, using Holm correction across the four features.

| Feature | Mean (outcome=1) | Mean (outcome=0) | Cohen's d (95% CI) | Welch p | Holm-adjusted p | Result |
|---|---|---|---|---|---|---|
| feat_a | 0.544 | -0.379 | 1.05 (0.91 to 1.18) | 2.3e-53 | 9.3e-53 | Significant |
| feat_d (n=850) | 0.381 | -0.170 | 0.57 (0.43 to 0.71) | 6.0e-15 | 1.8e-14 | Significant |
| feat_b | 0.241 | -0.057 | 0.30 (0.17 to 0.42) | 4.5e-06 | 9.0e-06 | Significant |
| feat_c | -0.004 | -0.008 | 0.004 (-0.12 to 0.13) | 0.95 | 0.95 | Not significant |

Mann-Whitney p-values agree with the Welch results: feat_a 8.1e-48, feat_d 1.8e-14, feat_b 5.0e-06, feat_c 0.90. The feat_d comparison uses the 850 complete rows only, so it may not generalise to the rows where feat_d is missing.

![Cohen d of each feature between outcome=1 and outcome=0, with 95% CI](tasks/stat_1/charts/stat1_cohens_d.png)

### Multivariable logistic regression

On standardized features (850 complete rows):

| Feature | Odds ratio per SD (95% CI) | Holm-adjusted p |
|---|---|---|
| feat_a | 3.54 (2.88 to 4.36) | 3.4e-32 |
| feat_d | 2.07 (1.73 to 2.47) | 5.2e-15 |
| feat_b | 1.41 (1.19 to 1.67) | 0.00014 |
| feat_c | 0.99 (0.84 to 1.16) | 0.87 |

feat_a, feat_b and feat_d each carry signal independently of the others. feat_c does not.

### Interactions

Six pairwise interaction terms were added to the main-effects logistic model (standardized features, n=850, log-odds scale). None is significant:

- feat_a × feat_b: coefficient 0.055 (95% CI -0.149 to 0.260), LR p = 0.59
- feat_a × feat_c: -0.028 (-0.236 to 0.179), LR p = 0.79
- feat_a × feat_d: -0.118 (-0.329 to 0.093), LR p = 0.27
- feat_b × feat_c: -0.082 (-0.254 to 0.090), LR p = 0.35
- feat_b × feat_d: 0.038 (-0.139 to 0.215), LR p = 0.68
- feat_c × feat_d: 0.124 (-0.045 to 0.294), LR p = 0.15

The feat_a × feat_d interval excludes large interactions but not modest ones, so the sample cannot rule out a small effect.

### feat_d missingness

- **Outcome:** the 150 rows with feat_d missing have an outcome rate of 41.3%, against 39.4% for the 850 rows where it is present. Chi-square p = 0.724; Fisher exact p = 0.652.
- **Other features:** standardized differences (missing minus present) are -0.072 for feat_a (Welch p = 0.42), 0.076 for feat_b (p = 0.40) and 0.018 for feat_c (p = 0.83). All fall below the usual 0.1 threshold for meaningful imbalance.
- **Joint model:** a logistic regression of missingness on feat_a, feat_b and feat_c gives LR p = 0.667 and pseudo R² = 0.002. No single coefficient is significant (p = 0.38, 0.35, 0.82).

These tests show no detectable relation. With 150 missing rows they can detect only fairly large differences, so modest relations may remain. The analysis treats missingness as missing completely at random as a working assumption, not a finding.

![Outcome rate for rows with feat_d missing vs present](tasks/eda_2/charts/eda2_outcome_by_feat_d_missing.png)

### Predictive models

Models were trained on 800 rows and scored on a 200-row test set. feat_d was median-imputed.

| Model | Test accuracy | Precision | Recall | F1 | ROC AUC | Log loss | Train accuracy |
|---|---|---|---|---|---|---|---|
| Majority-class baseline | 60.5% | 0.0 | 0.0 | 0.0 | 0.5 | not meaningful | 60.3% |
| Logistic regression | 75.5% | 71.4% | 63.3% | 0.671 | 0.821 | 0.4995 | 74.1% |
| Gradient boosting | 75.5% | 68.8% | 69.6% | 0.692 | 0.801 | 0.533 | 85.9% |

The baseline log loss of 14.24 is an artifact of the dummy classifier outputting hard 0/1 probabilities. It should not be compared with the model log losses, and the constant-prior reference was not computed.

Logistic regression is the preferred model: it has higher test ROC AUC and lower log loss. Gradient boosting's training accuracy (85.9%) is about 10 points above its test accuracy, and it gains no test accuracy over logistic regression.

**Permutation importance** (logistic regression, drop in test ROC AUC, 30 repeats):
- feat_a: 0.222 (sd 0.035)
- feat_d: 0.083 (sd 0.019)
- feat_b: 0.0004 (sd 0.008)
- feat_c: 0.0002 (sd 0.001)

feat_b's permutation importance is near zero, yet its logistic coefficient is the third largest (0.378). On the training set, unstandardized, with feat_d median-imputed, its odds ratio is 1.45 (coefficient 0.369, Wald p = 1.5e-05). The task reports this as modest independent signal, but permutation importance on the test set does not show it. The two measures are reported side by side and are not reconciled. feat_c contributes essentially nothing on either measure.

![Permutation importance of each feature for the logistic regression on the test set (drop in ROC AUC, 30 repeats)](tasks/ml_1/charts/ml1_perm_importance.png)

### Sensitivity of the feat_d effect to imputation

- **feat_d coefficient:** 0.656 with median imputation, 0.662 with median plus missingness indicator, 0.663 when fitted on the 682 complete training rows. The ml_1 logistic model reports an absolute feat_d coefficient of 0.605 under the same median-imputation setup. This differs from the 0.656 in the sensitivity run, and the two were not reconciled.
- **Test metrics on all 200 rows:** median imputation gives accuracy 0.755, ROC AUC 0.821, log loss 0.4995. Median plus indicator gives accuracy 0.750, ROC AUC 0.817, log loss 0.504. The indicator's coefficient is 0.37 and does not improve prediction.
- **On the 168 test rows with feat_d observed:** complete-case gives accuracy 0.744, ROC AUC 0.827, log loss 0.501. Median imputation gives accuracy 0.750, ROC AUC 0.827, log loss 0.501.
- **feat_d permutation importance:** 0.080 (median), 0.082 (median plus indicator), 0.090 (complete-case, observed subset). Standard deviations are about 0.02, so the differences are within noise.

![Sensitivity of the logistic model to feat_d imputation: test ROC AUC (left) and feat_d permutation importance (right) for median imputation, median plus missingness indicator, and complete-case fit. Complete-case is scored on the 168 test rows with feat_d observed; the other two use all 200 test rows.](tasks/ml_2/charts/ml2_imputation_sensitivity.png)

## Limitations

- **Missing feat_d:** 150 of 1,000 rows (15.0%) lack feat_d. The feat_d group comparisons and odds ratio use only the 850 complete rows. The missingness tests have limited power, and dependence on unobserved variables cannot be tested with the available columns.
- **Missingness assumption:** treating feat_d missingness as missing completely at random is a working assumption, not a finding.
- **Small test set:** all model scores come from a 200-row test set. The complete-case comparison uses only 168 rows.
- **Interaction power:** the feat_a × feat_d interval (-0.33 to 0.09) cannot rule out a modest interaction.
- **Conflicting feat_b measures:** the logistic coefficient points to modest independent signal, while test permutation importance is near zero. Both are reported as stated.
- **feat_d coefficient:** 0.605 (ml_1) and 0.656 (ml_2) for the same median-imputed logistic setup were not reconciled.
- **Baseline log loss:** the baseline log loss is an artifact and is not comparable with the model values. The constant-prior reference was not computed.
- **Gradient boosting:** it was run without tuning. Its train-test gap may narrow with tuning, which was not tested.
- **Failed or unresolved tasks:** none. All tasks are marked complete and accepted.

## Open questions

- Is feat_a's relation to outcome non-linear, or only a monotone trend? This was raised but not tested.
- Is the Q3 dip in feat_b's outcome rate real or sampling noise? It was raised but not tested.
- Does the feat_a × feat_d interaction exist at a size a larger sample would detect, or does it hold once non-linear feat_a terms are modelled?
- Could feat_d missingness depend on variables outside this dataset? This cannot be tested with the available columns.
- Would model-based multiple imputation change the feat_d coefficient or its permutation importance? Median imputation was the only method used beyond the indicator and complete-case variants.
- Does gradient boosting improve with tuning (depth, learning rate, regularization), narrowing its train-test gap?