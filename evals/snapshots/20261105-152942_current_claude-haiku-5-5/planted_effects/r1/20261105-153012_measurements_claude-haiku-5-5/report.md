# Outcome Analysis of a 1,000-Row Dataset: Four Numeric Features and a Binary Outcome

## Summary

- **feat_a is the strongest predictor of outcome.** Its outcome rate rises across quartiles from 11.6% (Q1) to 70.8% (Q4). In a multivariable logistic model on 850 complete rows, its adjusted OR is 3.61 per raw unit (95% CI 2.92 to 4.45).
- **feat_d is also associated with outcome,** rising from 24.9% in Q1 to 58.2% in Q4 (850 non-missing rows). Its adjusted OR is 2.07 per raw unit (1.73 to 2.47). feat_b is associated with outcome, with adjusted OR 1.40 (1.19 to 1.66). feat_c shows no association (adjusted OR 0.99, 0.84 to 1.16, p=0.87).
- **Logistic regression beats the majority-class baseline on a held-out split.** Test accuracy is 75.5% against a 60.5% baseline, with ROC AUC 0.821. Gradient boosting overfits and does not beat it.
- **feat_b's non-monotone pattern is not established.** Its quartile rates are not monotone, but the specific Q2-peak/Q3-dip reading rests on one nominal, post-hoc contrast that does not survive multiplicity correction. No feature–feature interaction was significant.
- **feat_d missingness is not detectably related to the observed columns or to outcome.** This is a limited test. Missingness is not established as random, and the 150 missing rows give wide confidence intervals.

## Data

- **Size:** 1,000 rows × 5 columns.
- **Target:** `outcome`, binary. Class 0 is 60.3% and class 1 is 39.7%.
- **Features:** four numeric features (feat_a, feat_b, feat_c, feat_d). There are no categorical, date/time, identifier or free-text features.
- **Missing values:** only feat_d, with 150 of 1,000 rows (15.0%) missing. feat_a, feat_b, feat_c and outcome have no missing values.

## Findings

### Outcome rates across quartiles of each feature

Quartile bins were computed for each feature. feat_d was binned on its 850 non-missing rows. Rates below are outcome rates within each bin.

| Feature | Q1 | Q2 | Q3 | Q4 | Pattern |
|---|---|---|---|---|---|
| feat_a | 11.6% (n=251) | 32.5% (n=249) | 44.0% (n=250) | 70.8% (n=250) | Rises at every step |
| feat_b | 26.8% (n=250) | 44.4% (n=250) | 37.6% (n=250) | 50.0% (n=250) | Non-monotone; Q4 highest, Q3 dip |
| feat_c | 38.8% (n=250) | 42.8% (n=250) | 35.6% (n=250) | 41.6% (n=250) | No clear trend; 7-point spread |
| feat_d | 24.9% (n=213) | 35.4% (n=212) | 39.2% (n=212) | 58.2% (n=213) | Rises; Q4 clearly highest |

- The overall outcome rate is 39.7% across all 1,000 rows.
- For feat_a, the Q4 minus Q1 difference is 59.2 points (95% CI 52.4 to 66.1), and the odds ratio is 18.6 (11.6 to 29.8).
- For feat_b, the range runs from Q1 26.8% to Q4 50.0%, about 23 points. Q4 minus Q1 is 23.2 points (95% CI 14.9 to 31.5), with odds ratio 2.73.
- For feat_c, the full spread runs from 35.6% (Q3) to 42.8% (Q2). No significance test was run in the descriptive step. The later test is reported below.
- For feat_d, Q4 minus Q1 is 33.3 points (95% CI 24.5 to 42.1), with odds ratio 4.21.

![Distribution of feat_a split by outcome (counts)](tasks/eda_1/charts/dist_feat_a.png)

![Distribution of feat_b split by outcome (counts)](tasks/eda_1/charts/dist_feat_b.png)

![Distribution of feat_c split by outcome (counts)](tasks/eda_1/charts/dist_feat_c.png)

![Distribution of feat_d split by outcome (counts)](tasks/eda_1/charts/dist_feat_d.png)

### Significance and effect sizes (univariate)

Chi-square tests on the quartile tables were Bonferroni-corrected across the four features (×4). Mann-Whitney and point-biserial tests are uncorrected.

| Feature | Chi-square p | Bonferroni p (×4) | Mann-Whitney p | Point-biserial r |
|---|---|---|---|---|
| feat_a | 3.1e-41 | 1.2e-40 | 8.1e-48 | 0.456 |
| feat_b | 7.6e-7 | 3.0e-6 | 5.0e-6 | 0.144 |
| feat_c | 0.36 | 1.0 (capped) | 0.90 | 0.002 |
| feat_d | 3.3e-11 | 1.3e-10 | 1.8e-14 | 0.269 |

- feat_a, feat_b and feat_d remain significant at 0.05 after correction. feat_c does not, under either test.
- The feat_c Q4 minus Q1 difference is 2.8 points (95% CI -5.8 to 11.4), odds ratio 1.12 (0.79 to 1.61).

![Outcome rate (%) in each within-feature quartile of feat_a, feat_b, feat_c and feat_d; feat_d uses the 850 non-missing rows](tasks/stat_1/charts/stat1_rates_by_quartile.png)

### Adjusted association (multivariable logistic regression, 850 complete rows)

In one logistic model with all four features, on the 850 rows with feat_d observed:

| Feature | Adjusted OR per raw unit (95% CI) | p |
|---|---|---|
| feat_a | 3.61 (2.92 to 4.45) | 8.4e-33 |
| feat_b | 1.40 (1.19 to 1.66) | 7.1e-5 |
| feat_c | 0.99 (0.84 to 1.16) | 0.87 |
| feat_d | 2.07 (1.73 to 2.47) | 1.7e-15 |

- Per one SD (standardized refit): feat_a 3.54 (2.88 to 4.36), feat_b 1.41 (1.19 to 1.67), feat_d 2.07 (1.73 to 2.47), feat_c 0.99 (0.84 to 1.16).
- Crude ORs per raw unit were feat_a 3.28, feat_b 1.33 and feat_d 1.81. Adjustment increased these estimates on the same rows. feat_c stayed null.

### feat_b shape: non-linearity versus a specific dip

- The feat_b quartile categories depart from a monotone linear trend (LR = 14.89, df = 2, p = 0.0006), adjusted for feat_a, feat_c and feat_d. This establishes non-linearity only.
- Adjusted ORs versus Q1 are: Q2 2.69 (1.65 to 4.38), Q3 1.56 (0.96 to 2.54) and Q4 3.51 (2.16 to 5.70). Q4 has the highest OR.
- **Q3 vs Q2 (nominal, post hoc):** adjusted OR 0.58 (95% CI 0.36 to 0.92), p = 0.022. The contrast was chosen after viewing the pattern and is not multiplicity-corrected in the stated test.
- **Q3 vs Q1:** not significant, adjusted OR 1.56 (0.96 to 2.54), p = 0.074.

Corrected pairwise contrasts (six contrasts, same adjusted model, 850 rows):

| Contrast | Adjusted OR (95% CI) | Raw p | Holm p | Bonferroni p |
|---|---|---|---|---|
| Q2 vs Q1 | 2.69 (1.65 to 4.38) | 0.00007 | 0.00034 | 0.00041 |
| Q3 vs Q1 | 1.56 (0.96 to 2.54) | 0.074 | 0.148 | 0.444 |
| Q4 vs Q1 | 3.51 (2.16 to 5.70) | <0.0001 | <0.0001 | <0.0001 |
| Q3 vs Q2 | 0.58 (0.36 to 0.92) | 0.022 | 0.067 | 0.133 |
| Q4 vs Q2 | 1.30 (0.83 to 2.06) | 0.255 | 0.255 | 1.00 |
| Q4 vs Q3 | 2.25 (1.41 to 3.59) | 0.0007 | 0.0026 | 0.0040 |

- Under Holm and Bonferroni correction, Q2 vs Q1, Q4 vs Q1 and Q4 vs Q3 remain significant at 0.05.
- Q3 vs Q2 does not survive correction (Holm p 0.067, Bonferroni p 0.133).

![Adjusted odds ratio with 95% CI for each pairwise feat_b quartile contrast, adjusted for feat_a, feat_c and feat_d; 850 complete rows](tasks/stat_6/charts/stat_6_forest.png)

The Q2-peak/Q3-dip pattern is therefore not established as distinguishable from noise. The reliable feat_b effects are the upper quartiles relative to Q1, and Q4 relative to Q3.

### Missingness of feat_d

- **Only feat_d has missing values:** 150 of 1,000 rows (15.0%).
- **Versus outcome:** the outcome rate is 41.3% among missing rows (62 of 150) and 39.4% among observed rows (335 of 850). The odds ratio is 1.08. The uncorrected chi-square is 0.197 (p = 0.66). The continuity-corrected value is 0.125 (p = 0.72). The corrected value was reported in eda_2 and stat_1, and stat_4 identifies it as the Yates-corrected value of the same table. Both show no association.
- **Versus other features (marginal Mann-Whitney tests):** feat_a p = 0.28, feat_b p = 0.35 and feat_c p = 0.98. Missing and observed rows do not differ detectably on these features.
- **Jointly (logit of missingness on feat_a, feat_b, feat_c and outcome, n = 1,000):** the likelihood-ratio test gives p = 0.70, pseudo R² = 0.0026. No coefficient is significant:
  - feat_a OR 0.89 (0.73 to 1.09), p = 0.25
  - feat_b OR 1.08 (0.90 to 1.28), p = 0.41
  - feat_c OR 1.02 (0.86 to 1.21), p = 0.83
  - outcome OR 1.18 (0.79 to 1.76), p = 0.42

The results are compatible with missingness being unrelated to the observed columns and outcome. They do not establish that it is. Power is limited, and moderate associations cannot be excluded.

### Interactions

Pairwise interaction terms were tested in logistic models on the 850 complete rows.

| Pair | Coefficient | Wald p | LR p |
|---|---|---|---|
| feat_a × feat_c | -0.028 | 0.79 | 0.79 |
| feat_b × feat_c | -0.079 | 0.35 | 0.35 |
| feat_a × feat_d | -0.119 | 0.27 | 0.27 |
| feat_b × feat_d | 0.037 | 0.68 | 0.68 |

- Jointly, the four interactions do not improve the main-effects model: LR chi-square 2.23 on 4 df, p = 0.69.
- No pair was significant, so no stratified 2×2 tables were produced. With 850 rows, the test has limited power to detect small interactions, so these results do not rule them out.

### Predictive performance

Protocol: stratified split on outcome (random_state 42), giving 800 training and 200 test rows. feat_d was median-imputed using the training split only.

| Model | Test accuracy | Test ROC AUC | Test log loss | Other |
|---|---|---|---|---|
| Logistic regression | 75.5% | 0.821 | 0.4995 | Precision 0.714, recall 0.633, F1 0.671; train accuracy 0.741 |
| Gradient boosting | 73.0% | 0.754 | 0.6961 | Train accuracy 1.0; precision 0.651, recall 0.684, F1 0.667 |
| Majority-class baseline | 60.5% | — | 0.6709 (constant train-rate predictor) | — |

- Logistic regression exceeds the 60.5% baseline by about 15 points of accuracy on the test split.
- Gradient boosting overfits (train accuracy 1.0). Its test log loss is worse than the constant baseline.

Permutation importance for logistic regression (drop in test ROC AUC, 30 repeats):

| Feature | Mean drop | SD |
|---|---|---|
| feat_a | 0.222 | 0.035 |
| feat_d | 0.083 | 0.019 |
| feat_b | 0.0004 | 0.0084 |
| feat_c | 0.0002 | 0.0011 |

- Standardized coefficient magnitudes were feat_a 1.246, feat_d 0.605, feat_b 0.378 and feat_c 0.025. feat_b has a non-zero coefficient but near-zero permutation importance on the test split.

![Drop in test ROC AUC when each feature is shuffled, logistic regression, 30 repeats](tasks/ml_1/charts/ml1_perm_importance.png)

## Limitations

- **Complete-case analysis.** The multivariable model, interaction tests and the feat_b quartile contrasts used 850 rows. The 150 rows missing feat_d were dropped. These estimates are unbiased only if feat_d missingness is unrelated to outcome given the other features, which is not established. The predictive models used median imputation for feat_d instead.
- **Missingness mechanism not established.** Tests are compatible with missing-at-random given the observed columns and outcome. MNAR cannot be ruled out. The tests have wide confidence intervals and limited power.
- **Unresolved review issue on the eda_1 feat_b finding.** The eda_1 finding stated that feat_b peaks in Q2. That is incorrect. The correct pattern is non-monotone: Q4 (50.0%) is highest, Q2 (44.4%) second, and Q3 (37.6%) is the dip. The range runs from Q1 26.8% to Q4 50.0%, about 23 points. The corrected values are confirmed in eda_2 and stat_1, and this report uses those values. The eda_1 record still contains the incorrect statement, and the review objection is recorded against it. The Q3 and Q4 rates for feat_a and feat_d, and the Q4 rates for feat_b and feat_c, were also confirmed against the quartile facts (eda_2 and stat_1).
- **feat_b Q3 vs Q2 is nominal and post hoc.** It was chosen after viewing the pattern and does not survive correction across six contrasts. The Q2-peak/Q3-dip reading is not established.
- **Quartile chi-square tests on about 250-row bins.** Sampling noise cannot be excluded for the fine-grained bin differences.
- **Interaction tests have limited power** on 850 rows, so the absence of significant interactions does not rule out small effects.
- **Multiple comparisons.** Bonferroni correction was applied only to the quartile chi-square p-values. Mann-Whitney and point-biserial p-values are uncorrected.
- **Model overfitting.** Gradient boosting overfits (train accuracy 1.0) and performs worse than logistic regression and the constant baseline on log loss.
- **Test-set size.** The predictive evaluation uses 200 test rows. Scores are estimates with that uncertainty.
- **No task failed.** All six analysis tasks (eda_1, eda_2, stat_1 to stat_6, ml_1) are recorded as complete.

## Open questions

- Is the feat_b non-linearity, and especially the Q3 dip relative to Q2, real or sampling noise? The planned checks are a bootstrap or permutation test of all feat_b quartile contrasts with multiplicity correction, and a spline model of feat_b.
- Does feat_b add predictive value beyond feat_a and feat_d? A nested model comparison or likelihood-ratio test was suggested. Permutation importance on the test split is near zero.
- Is the feat_a effect nonlinear, given its strong quartile gradient (11.6% to 70.8%)?
- Do the feat_d estimates hold under a sensitivity analysis for the 150 missing rows, such as multiple imputation? Current feat_d estimates use complete cases (regression) or median imputation (ML).
- Would a regularised or shallower gradient boosting model, or one with an explicit feat_d missingness indicator, improve on logistic regression?
- What size of association between feat_d missingness and the observed columns or outcome could the 150 missing rows detect? A power or sensitivity analysis would bound it.