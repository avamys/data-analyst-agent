# Outcome Analysis of a 1,000-Row Dataset with a Binary Target (outcome)

## Summary

- **Outcome is 39.7% positive** (397 of 1,000 rows). Its rate rises steeply across quartiles of feat_a (11.6% in Q1 to 70.8% in Q4) and of feat_d (24.9% to 58.2%).
- **Three of four features differ significantly by outcome class after Holm correction.** feat_a has the largest effect (Cohen's d 1.046), then feat_d (d 0.571, n = 850) and feat_b (d 0.296, small). feat_c shows no difference (Holm-adjusted p = 0.95).
- **A logistic regression predicts outcome better than the majority-class baseline on a 200-row test set.** Accuracy is 0.750 against 0.605, and ROC AUC is 0.817 against 0.500. Gradient boosting overfits and scores lower on test (AUC 0.760).
- **No pairwise interaction between features is significant** (smallest Holm-adjusted p = 0.898), though the tests cannot exclude small interactions.
- **feat_d missingness (15.0%) shows no detectable association** with feat_a, feat_b, feat_c or outcome, either marginally or jointly (LR p = 0.696). Dependence on feat_d's own value cannot be tested with these data.

## Data

- **Size:** 1,000 rows and 5 columns.
- **Target:** `outcome`, binary. Class 0 is 60.3% and class 1 is 39.7%.
- **Features:** four numeric features (feat_a, feat_b, feat_c, feat_d). There are no categorical, date/time, id or free-text features.
- **Missing values:** feat_d, 15.0% (150 rows). feat_a, feat_b and feat_c have none.

## Findings

### Outcome rates across feature quartiles

Quartile bins are roughly 250 rows each (feat_d bins have 212–213 rows, excluding its 150 missing rows).

- **feat_a:** The outcome rate rises from 11.6% (Q1) to 32.5% (Q2), 44.0% (Q3) and 70.8% (Q4).
- **feat_b:** The rates are 26.8%, 44.4%, 37.6% and 50.0% across Q1 to Q4. This is an observed pattern with a dip in Q3. Its significance was not tested at the quartile level.
- **feat_c:** The rates are 38.8%, 42.8%, 35.6% and 41.6% against an overall rate of 39.7%. There is no clear monotone trend. Significance was not tested at the quartile level.
- **feat_d:** The rates are 24.9%, 35.4%, 39.2% and 58.2%.

All four features have means near 0 and standard deviations between 0.990 and 1.016, so they appear standardized.

![Box plots of feat_a to feat_d split by outcome value; feat_d excludes missing values](tasks/eda_1/charts/boxplots_by_outcome.png)

### Differences between outcome classes

Tests are Welch t-tests with Mann-Whitney checks, Holm-corrected across the four features.

- **feat_a:** Mean 0.544 for outcome = 1 and -0.379 for outcome = 0. The difference is 0.922 (95% CI 0.812 to 1.032), p < 0.001 (Holm-adjusted p < 0.001), Cohen's d 1.046. Mann-Whitney p < 0.001, rank-biserial 0.542.
- **feat_b:** Mean 0.241 vs -0.057. The difference is 0.298 (95% CI 0.171 to 0.425), p = 4.5e-06 (Holm-adjusted p < 0.001). Cohen's d 0.296, a small effect. Mann-Whitney p < 0.001, rank-biserial 0.170.
- **feat_c:** Mean -0.004 vs -0.008. The difference is 0.004 (95% CI -0.124 to 0.132), p = 0.95 (Holm-adjusted p = 0.95), Cohen's d 0.004. Mann-Whitney p = 0.90.
- **feat_d** (850 non-missing rows): Mean 0.381 vs -0.170. The difference is 0.551 (95% CI 0.416 to 0.686), p < 0.001 (Holm-adjusted p < 0.001), Cohen's d 0.571. Mann-Whitney p < 0.001, rank-biserial 0.311.

![Box plots of feat_a to feat_d split by outcome class (0 or 1); feat_d excludes 150 missing rows](tasks/stat_1/charts/boxplots_by_outcome_stat.png)

### Missingness in feat_d

**Marginal tests (eda_2).** Four tests were run without multiplicity correction.

- feat_a: mean -0.073 for missing rows (n = 150) vs -0.002 for observed rows (n = 850), Welch p = 0.424.
- feat_b: mean 0.128 vs 0.050, Welch p = 0.400.
- feat_c: mean 0.009 vs -0.009, Welch p = 0.835.
- Outcome: 41.3% (62 of 150) for missing rows vs 39.4% (335 of 850) for observed rows, chi-square p = 0.724.

None is significant, but the tests do not rule out a small association.

**Joint test (stat_3).** A logistic model of the missing indicator on feat_a, feat_b, feat_c and outcome has LR chi² = 2.218 on 4 df, p = 0.696, pseudo R² = 0.003. No individual predictor is significant after adjustment:

- feat_a: OR 0.891, p = 0.252
- feat_b: OR 1.075, p = 0.412
- feat_c: OR 1.019, p = 0.826
- outcome: OR 1.180, p = 0.419

This test does not rule out small effects. It also does not test dependence on feat_d's own value, which cannot be assessed from the data.

![Proportion of outcome = 1 for rows where feat_d is observed vs missing](tasks/eda_2/charts/outcome_rate_by_feat_d_missing.png)

### Feature interactions

Six pairwise interaction terms were tested by likelihood ratio on the 850 non-missing feat_d rows.

- LR p-values range from 0.150 (feat_c × feat_d) to 0.789 (feat_a × feat_c). Holm-adjusted p is 0.898 for feat_c × feat_d and 1.000 for the other five.
- The feat_c × feat_d coefficient is 0.109 (95% CI -0.061 to 0.278). The feat_a × feat_d coefficient is -0.109 (95% CI -0.325 to 0.108), with LR p = 0.274.
- Every interaction CI includes zero. The CIs are about ±0.2 on the log-odds scale, so interactions of around 0.1 to 0.2 cannot be excluded.

In the full model with all six interactions, the main effects are feat_a 1.307 (95% CI 1.088 to 1.525), feat_d 0.753 (0.567 to 0.939), feat_b 0.321 (0.145 to 0.498) and feat_c -0.016 (-0.192 to 0.160).

### Predictive performance

**Setup.** A stratified 80/20 split (seed 42) gives 800 training rows and 200 test rows, with a test outcome rate of 39.5%. feat_d was imputed with the training median (0.043), and a feat_d_missing indicator was added.

**Scores on the 200-row test set.**

| Model | Accuracy | ROC AUC | Log loss | Precision | Recall | F1 |
|---|---|---|---|---|---|---|
| Majority-class baseline | 0.605 | 0.500 | 14.237* | 0.0 | 0.0 | 0.0 |
| Logistic regression | 0.750 | 0.817 | 0.505 | 0.710 | 0.620 | 0.662 |
| Gradient boosting | 0.730 | 0.760 | 0.681 | 0.654 | 0.671 | 0.663 |

*The baseline's log loss reflects constant hard probabilities and should not be compared with the model log losses. The AUC comparison (0.817 against 0.500) is the relevant one.

Gradient boosting reaches 0.999 training accuracy against 0.730 on test, which indicates overfitting. Its test scores are below those of logistic regression.

**Feature importance (logistic regression).** Standardised coefficients are feat_a 1.251, feat_d 0.610, feat_b 0.375, feat_d_missing 0.137 and feat_c 0.025. Permutation importance (drop in test ROC AUC, 30 repeats) is:

- feat_a: 0.226 (sd 0.035)
- feat_d: 0.085 (sd 0.018)
- feat_b: 0.002 (sd 0.009)
- feat_c: 0.001 (sd 0.0008)
- feat_d_missing: -0.003 (sd 0.004)

The feat_c and feat_d_missing values match the full permutation-importance record.

The permutation result for feat_d_missing shows only that permuting the indicator does not reduce test AUC. It does not show that the model ignores missingness. The indicator is coupled with the median-imputed feat_d, so the two effects cannot be separated here. Whether missingness carries outcome information is untested in this task and is left to stat_3, which tested dependence on the observed features and outcome (see above).

![Drop in test ROC AUC when each feature is permuted, logistic regression (higher = more important)](tasks/ml_1/charts/ml1_permutation_importance.png)

### feat_b association after adjustment

In a logit of outcome on feat_a, feat_b and feat_d (complete cases, n = 850), the feat_b coefficient is 0.339 (OR 1.40, 95% CI 1.19 to 1.66), p = 7.0e-05.

- Unadjusted on the same 850 rows: coefficient 0.288 (OR 1.33, 95% CI 1.16 to 1.53), p = 5.8e-05.
- Unadjusted on all 1,000 non-missing feat_b rows: coefficient 0.295 (OR 1.34, 95% CI 1.18 to 1.53), p = 7.0e-06.

Adjustment did not reduce the feat_b coefficient. It is 17.8% larger than the unadjusted complete-case coefficient. The feat_b association persists after adjusting for feat_a and feat_d. This adjusted model does not include feat_c, and the quartile pattern was not modelled.

## Limitations

- **feat_d missingness.** feat_d is missing in 15.0% of rows. The eda_2 marginal tests were not corrected for multiplicity. The joint test (stat_3) covers only feat_a, feat_b, feat_c and outcome. Dependence on feat_d's own value (MNAR) cannot be assessed.
- **Unresolved review issue on ml_1 (feat_d_missing).** The permutation result (-0.003) and the standardised coefficient (0.137) show only that permuting the indicator does not reduce test AUC. They do not show whether missingness carries outcome information, and the indicator is coupled with the median-imputed feat_d. This affects the feature-importance finding for feat_d_missing. Whether missingness carries outcome information remains untested and is left to stat_3.
- **Quartile patterns.** The feat_b rise and Q3 dip, and the feat_c pattern, were not tested at the quartile level. The class-level tests in stat_1 cover only the two outcome classes.
- **Sample sizes.** feat_d tests use 850 complete rows. Interaction CIs are about ±0.2 on the log-odds scale, so small interactions cannot be excluded.
- **Predictive evaluation.** Results come from a single 80/20 split with a 200-row test set.
- **Imputation.** feat_d was imputed with the training median. The stability of results under other imputation schemes was not tested.
- **Failed tasks.** None. All tasks (eda_1, eda_2, stat_1 to stat_4 and ml_1) completed.

## Open questions

- Is the feat_b rise and its Q3 dip (26.8%, 44.4%, 37.6%, 50.0%) real at the quartile level?
- Is the feat_c quartile pattern (38.8% to 42.8%, then 35.6% and 41.6%) distinguishable from no association when tested by quartile?
- Is the feat_a effect non-linear, and does a multivariable logistic model with feat_a, feat_b and feat_d explain most of the outcome variation?
- Do feat_a and feat_d interact, and does the feat_d effect, or the feat_b effect, differ for the 150 missing rows?
- Is feat_b correlated with feat_a or feat_d, and does collinearity account for the coefficient change after adjustment?
- Does feat_d missingness depend on interactions or non-linear combinations of features, or on feat_d's own value? What sensitivity analysis (for example, pattern-mixture or selection models) could bound such dependence?
- Is the feat_d missingness pattern stable across outcome classes when imputation is applied before modelling?
- Is the modest feat_d importance stable under other imputation schemes, such as group-wise or outcome-stratified medians?
- Does gradient boosting's test performance improve with stronger regularisation or cross-validated tuning?