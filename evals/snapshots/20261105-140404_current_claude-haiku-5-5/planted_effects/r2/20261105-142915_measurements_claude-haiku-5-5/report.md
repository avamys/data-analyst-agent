# Outcome Analysis of a 1,000-Row Binary Dataset (Target: `outcome`)

## Summary

- **Outcome is moderately imbalanced.** 397 of 1,000 rows (39.7%) have outcome=1 and 603 (60.3%) have outcome=0. feat_a and feat_d have the strongest univariate associations with outcome, and both stay significant after Holm correction. feat_c shows no association.
- **Interactions are not supported.** None of the six pairwise product terms is significant (smallest p = 0.21, on 850 complete rows). The data do not show that any feature changes the effect of another.
- **Missingness in feat_d is not related to the other features or the outcome in these tests.** 150 rows (15.0%) are missing. Outcome rates are 41.3% when missing and 39.4% when present (chi-square p = 0.657). The tests have limited power, and MAR cannot be confirmed from the data.
- **Both models beat the majority-class baseline.** On a single 250-row test split, logistic regression reaches accuracy 0.772 and ROC AUC 0.839, and gradient boosting reaches accuracy 0.756 and ROC AUC 0.803. The baseline accuracy is 0.604. Under repeated stratified 5×5 CV, logistic regression keeps the higher ROC AUC (0.813 vs 0.776) and lower log-loss (0.514 vs 0.568) in all 25 folds.
- **feat_a dominates prediction, and feat_d is second.** Shuffling feat_a lowers test ROC AUC by 0.215 to 0.250 across models and resampling schemes. Shuffling feat_d lowers it by 0.054 to 0.075. feat_b and feat_c contribute little.

## Data

- **Size:** 1,000 rows × 5 columns.
- **Target:** `outcome`, binary. Class 0: 603 rows (60.3%). Class 1: 397 rows (39.7%).
- **Features:** four numeric features (feat_a, feat_b, feat_c, feat_d). There are no categorical, date/time, identifier or free-text columns.
- **Missing values:** feat_d only, 150 rows (15.0%). All other columns are complete.

## Findings

### Distributions, range and outliers (eda_1)

- Summary statistics use observed values. feat_a, feat_b and feat_c have n = 1,000. feat_d has n = 850.

| Feature | Mean | SD | Median | Min | Max | Skew |
|---|---|---|---|---|---|---|
| feat_a | -0.013 | 0.990 | 0.056 | -3.331 | 3.134 | -0.095 |
| feat_b | 0.062 | 1.016 | 0.051 | -3.066 | 3.669 | -0.003 |
| feat_c | -0.006 | 1.013 | -0.054 | -3.370 | 3.297 | 0.080 |
| feat_d | 0.047 | 1.000 | 0.052 | -3.047 | 3.276 | 0.023 |

- All four features are close to symmetric.
- IQR-rule outliers are few: 5 of 1,000 feat_a values, 6 of 1,000 feat_b, 5 of 1,000 feat_c, and 9 of 850 feat_d. These are 0.5% to 1.1% of observed values. Whether they are data errors was not checked.

![Histograms of the four numeric features (counts of rows; feat_d excludes missing values)](tasks/eda_1/charts/eda1_histograms.png)

### Missingness in feat_d (eda_2)

- **Relation to other features:** Mann-Whitney tests found no detectable difference in feature means between rows with feat_d missing and present.
  - feat_a: mean -0.073 (missing, n=150) vs -0.002 (present, n=850), p = 0.284.
  - feat_b: mean 0.128 vs 0.050, p = 0.353.
  - feat_c: mean 0.009 vs -0.009, p = 0.984.
- **Relation to outcome:** The outcome rate is 41.3% when feat_d is missing (62 of 150) and 39.4% when present (n = 850). The chi-square p-value is 0.657.
- Across feat_a, feat_b, feat_c and the outcome, none of the four tests shows a relationship with feat_d missingness (all p > 0.28). The data are consistent with feat_d being missing at random with respect to the observed variables. The tests only check dependence on the variables measured here. With 150 missing rows, small associations cannot be ruled out.

![Outcome rate for rows with feat_d missing vs present (rates of outcome=1)](tasks/eda_2/charts/d_missing_outcome_rate.png)

### Association of each feature with outcome (stat_1)

Logistic slopes are per SD, using non-missing rows. Holm correction covers the four slope tests. Quartile cut points come from each feature's own non-missing distribution.

| Feature | n | OR per SD (95% CI) | Slope p | Holm-adjusted p | Quartile outcome rates (Q1 to Q4) | Quartile chi-square |
|---|---|---|---|---|---|---|
| feat_a | 1,000 | 3.30 (2.76 to 3.95) | 1.6e-38 | 6.6e-38 | 11.6%, 32.5%, 44.0%, 70.8% | 191.3 (p = 3.1e-41) |
| feat_d | 850 | 1.81 (1.55 to 2.12) | 4.0e-14 | 1.2e-13 | 24.9%, 35.4%, 39.2%, 58.2% | 51.8 (p = 3.3e-11) |
| feat_b | 1,000 | 1.35 (1.18 to 1.54) | 7.0e-6 | 1.4e-5 | 26.8%, 44.4%, 37.6%, 50.0% | 31.2 (p = 7.6e-7) |
| feat_c | 1,000 | 1.00 (0.88 to 1.14) | 0.95 | 0.95 | 38.8%, 42.8%, 35.6%, 41.6% | 3.2 (p = 0.36) |

- feat_a is strongly associated with outcome.
- feat_d is strongly associated with outcome, on 850 non-missing rows.
- feat_b shows a modest association. Its quartile pattern is not monotone, with a dip in Q3 (37.6%) after Q2 (44.4%). The findings do not establish whether this is noise or real nonlinearity.
- feat_c shows no association.
- The three significant features (feat_a, feat_d, feat_b) remain significant after Holm correction. feat_c does not. The quartile chi-square tests were not adjusted separately.

![Share of outcome=1 (%) by feature quartile; feat_d excludes missing rows](tasks/stat_1/charts/quartile_outcome_rates.png)

### Interactions (stat_2)

- No pairwise interaction between the four features is significant. The model contains all six product terms and is fitted on 850 complete rows.
- The smallest p-value is 0.21, for feat_c × feat_d (OR 1.12 per SD product, 95% CI 0.94 to 1.33). The next largest is feat_a × feat_d (OR 0.90, 95% CI 0.73 to 1.11, p = 0.33). Holm correction over six tests cannot make any of them significant.
- The wide confidence intervals rule out only large interactions. Small to moderate interactions remain possible.
- Because no interaction is significant, no split by pairs of features is reported.
- Main effects in this joint model, per SD, are feat_a OR 3.62 (95% CI 2.93 to 4.48), feat_d OR 2.13 (1.76 to 2.56), feat_b OR 1.39 (1.16 to 1.65) and feat_c OR 0.99 (0.83 to 1.18). The analysis describes these as consistent with stat_1. They are estimated jointly with the interaction terms, on the 850 complete rows.

### Predictive models on a single split (ml_1)

- Setup: stratified test split of 250 rows (seed 42), training on 750 rows, feat_d median-imputed on the training data.
- The constant-probability baseline predicts the training positive rate. It has accuracy 0.604 and log-loss 0.671.
- The earlier baseline log-loss of 14.27 used hard 0/1 probabilities and is superseded by 0.671.

| Model | Train accuracy | Test accuracy | Test precision | Test recall | Test F1 | Test ROC AUC | Test log-loss |
|---|---|---|---|---|---|---|---|
| Majority-class baseline | – | 0.604 | – | – | – | – | 0.671 |
| Logistic regression | 0.735 | 0.772 | 0.739 | 0.657 | 0.695 | 0.839 | 0.481 |
| Gradient boosting | 0.867 | 0.756 | 0.702 | 0.667 | 0.684 | 0.803 | 0.529 |

- On this split, logistic regression has the higher ROC AUC (0.839 vs 0.803) and lower log-loss (0.481 vs 0.529). The findings state this rests on one 250-row test split with no interval estimates, so the gap may not be stable.
- Gradient boosting overfits: train accuracy 0.867 against test accuracy 0.756.
- Permutation importance (drop in test ROC AUC when shuffled):
  - feat_a: 0.244 (SD 0.027) for gradient boosting and 0.250 (SD 0.030) for logistic regression.
  - feat_d: 0.066 (SD 0.014) and 0.075 (SD 0.014).
  - feat_b: 0.007 (SD 0.012) and 0.009 (SD 0.009).
  - feat_c: 0.008 (SD 0.005) and 0.0001 (SD 0.0008).
- feat_b and feat_c contribute little in either model. Their contributions are not distinguishable from zero on this split.

![Permutation importance on the test set for gradient boosting: mean drop in ROC AUC when each feature is shuffled (30 repeats, error bars = 1 SD)](tasks/ml_1/charts/ml1_perm_importance.png)

### Stability under repeated stratified CV (ml_2)

- Setup: 5×5 repeated stratified CV (25 folds), feat_d median-imputed within folds.

| Model | Accuracy (mean, SD) | ROC AUC (mean, SD) | Log-loss (mean, SD) |
|---|---|---|---|
| Majority-class baseline | 0.603 (0.003) | 0.5 | 0.672 (0.001) |
| Logistic regression | 0.743 (0.026) | 0.813 (0.030) | 0.514 (0.034) |
| Gradient boosting | 0.718 (0.022) | 0.776 (0.026) | 0.568 (0.037) |

- The logistic regression advantage holds in every fold. Its ROC AUC is higher in 25 of 25 folds, with a mean per-fold difference of 0.037 (SD 0.019). Its log-loss is lower in 25 of 25 folds, with a mean per-fold difference of 0.055 (SD 0.021).
- Both models beat the baseline on accuracy.
- The findings state that the CV gaps are about the same size as the single-split gaps in ml_1 and point in the same direction. The CV ROC AUC gap is 0.037, and the ml_1 split gave 0.839 vs 0.803. The CV log-loss gap is 0.055, and the ml_1 split gave 0.481 vs 0.529. The per-fold SDs describe spread across folds. The 25 folds come from repeated 5-fold CV and are not independent, so they do not give confidence intervals for the gap.
- Permutation drop in ROC AUC across 25 folds:
  - feat_a: 0.234 (SD 0.030) for logistic regression and 0.215 (SD 0.032) for gradient boosting.
  - feat_d: 0.063 (SD 0.018) and 0.054 (SD 0.020).

![Test ROC AUC (left) and log-loss (right) per fold of 5x5 repeated stratified CV, logistic regression vs gradient boosting; boxes show the 25 fold values.](tasks/ml_2/charts/ml2_cv_scores.png)

### Sensitivity of quartile rates to IQR outliers (eda_3)

- Excluding IQR outliers (5 rows from feat_a, 9 from feat_d) leaves the quartile pattern almost unchanged.
  - feat_a: Q1 11.6% → 11.6%, Q2 32.5% → 32.4%, Q3 44.0% → 44.4%, Q4 70.8% → 70.6% (n=248 after exclusion).
  - feat_d: Q1 24.9% → 25.1%, Q2 35.4% → 35.7%, Q3 39.2% → 39.0%, Q4 58.2% → 57.6% (n=210 after exclusion).
- IQR fences are feat_a [-2.764, 2.729] and feat_d [-2.601, 2.679]. The findings conclude that the quartile gradient is not produced by these outliers.

![Outcome=1 rate by quartile of feat_a and feat_d, all rows vs IQR outliers excluded](tasks/eda_3/charts/eda3_iqr_quartile_rates.png)

## Limitations

- **Outlier validity is unchecked.** The flagged IQR outliers were not checked against valid ranges or for data errors. Their effect on the quartile rates was checked (eda_3), but their status as true values was not.
- **MAR is not confirmed.** The feat_d missingness tests cover only the observed variables. Missingness could depend on unobserved values. The 150 missing rows give limited power, so small associations cannot be ruled out.
- **Interactions are imprecise.** The confidence intervals are wide. Small to moderate interactions are not excluded.
- **Nonlinearity was not tested.** No nonlinear terms were fitted for feat_a or feat_d. The non-monotone pattern for feat_b (Q3 dip) is not explained.
- **The predictive comparison on the single split has no interval estimates.** The repeated-CV results in ml_2 use folds that are not independent, so they do not give confidence intervals for the model gap.
- **Imputation choice.** feat_d was median-imputed in all models. Missing-indicator and model-based imputation were not tested.
- **Multiple testing.** Holm correction covers the four slope tests and the six interaction tests. The quartile chi-square tests were not adjusted.
- **Superseded baseline value.** The baseline log-loss of 14.27 in ml_1 is superseded by 0.671.
- **Unresolved review issues:** none recorded. No tasks failed.

## Open questions

- Are the flagged IQR outliers in feat_a and feat_d true extreme values or data errors? Checking them against the valid ranges of each feature was raised but not done.
- Is the relationship of feat_a and feat_d with outcome linear, or does it need nonlinear terms?
- Does the non-monotone quartile pattern of feat_b (dip in Q3) reflect noise or a real nonlinearity?
- Does a missing-indicator for feat_d add signal to the outcome model, or does simple imputation suffice?
- Does feat_d missingness depend on combinations of features or on feat_d's own unobserved values, as tested with a logistic model of the missing indicator on all features?
- Are the 150 missing feat_d rows a single block (for example, by row index or collection batch)?
- Does the feat_d importance hold when feat_d is imputed by a model (for example, an iterative imputer) rather than the training median?
- Would tuning gradient boosting (depth, learning rate, regularisation) close the log-loss and ROC AUC gap with logistic regression?