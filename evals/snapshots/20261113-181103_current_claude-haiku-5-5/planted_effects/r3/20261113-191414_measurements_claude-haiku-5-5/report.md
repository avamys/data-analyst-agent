# Outcome Analysis of a 1,000-Row Dataset: Predictors of a Binary Outcome (39.7% Positive)

## Summary

- **feat_a is the strongest associated feature.** Its outcome rate rises from 11.6% in its lowest quartile to 70.8% in its highest. It stays the largest effect after adjusting for feat_b, feat_c and feat_d (adjusted OR 3.61 per SD).
- **feat_d and feat_b are weaker but significant, and feat_c shows no association.** feat_d reaches 58.2% in its top quartile against 24.9% in its bottom quartile (850 non-missing rows). feat_c's quartile rates stay between 35.6% and 42.8%.
- **Logistic regression and gradient boosting both beat the majority-class baseline** (accuracy 0.605 on a 200-row test set). Logistic regression reached 75.0% accuracy and ROC AUC 0.817. Gradient boosting reached 75.5% accuracy and ROC AUC 0.807. The two models are not clearly different.
- **feat_d missingness (15.0%) shows no detectable relationship with the other features or the outcome.** Univariate and joint tests both find nothing, but these tests cannot establish that the missingness is random. The missingness indicator does not contribute to prediction in either model.
- **No interaction was statistically significant.** Cell-level outcome rates suggest that the effects may combine, but the interaction tests were low-powered and these patterns are hypothesis-generating only.

## Data

- **Size:** 1,000 rows and 5 columns: the binary target `outcome`, plus four numeric features (feat_a, feat_b, feat_c, feat_d). There are no categorical, date/time, identifier or free-text columns.
- **Target:** `outcome` has 397 rows with value 1 (39.7%) and 603 rows with value 0 (60.3%).
- **Missing values:** feat_d is missing in 150 rows (15.0%). No other column has missing values. Adjusted and univariate feat_d analyses use the 850 non-missing rows.
- **Feature distributions:** All four features are close to standardized. Their means range from -0.013 to 0.062, their standard deviations from 0.99 to 1.02, and their skew from -0.10 to 0.08, so they look roughly symmetric and normal-like.

![Histograms of the four numeric features and counts of the outcome classes](tasks/eda_1/charts/eda1_histograms.png)

## Findings

### Outcome rates across quartiles

- **feat_a:** The outcome rate rises steadily: 11.6% in Q1 (n = 251), 32.5% in Q2, 44.0% in Q3 and 70.8% in Q4 (n = 250).
- **feat_d (non-missing rows):** The rate rises from 24.9% in Q1 to 58.2% in Q4, with Q2 at 35.4% and Q3 at 39.2%. This is the second-strongest gradient after feat_a.
- **feat_b:** The rates are 26.8%, 44.4%, 37.6% and 50.0% across Q1 to Q4. The pattern trends upward overall but is not monotonic.
- **feat_c:** The rates are 38.8%, 42.8%, 35.6% and 41.6%. There is no clear relationship, and all four are within about 7 points of each other.

![Share of rows with outcome=1 within each quartile of each feature (feat_d uses non-missing rows)](tasks/eda_1/charts/eda1_quartile_rates.png)

### Significance and effect sizes

Univariate tests of each feature against the outcome. The rank-biserial CIs use an approximate Fisher-z method, not an exact one.

| Feature | n | Mann-Whitney p | Rank-biserial (95% CI) | Univariate OR per SD (95% CI) |
|---|---|---|---|---|
| feat_a | 1,000 | 8.1e-48 | 0.542 (0.497 to 0.585) | 3.34 (2.79 to 4.01) |
| feat_d | 850 | 1.8e-14 | 0.311 (0.249 to 0.370) | 1.81 (1.55 to 2.12) |
| feat_b | 1,000 | 5.0e-6 | 0.170 (0.110 to 0.230) | 1.34 (1.18 to 1.53) |
| feat_c | 1,000 | 0.90 | -0.005 (-0.067 to 0.057) | 1.00 (0.886 to 1.138), p = 0.95 |

feat_a is the strongest feature. feat_d is significant on the 850 non-missing rows. feat_b is significant but small. feat_c shows no association with the outcome.

**Adjusted model.** A logistic regression on feat_a, feat_b, feat_c and feat_d together, fitted to the 850 complete cases, gives these odds ratios per SD:

- feat_a: 3.61 (95% CI 2.92 to 4.45, p = 8.4e-33)
- feat_b: 1.40 (95% CI 1.19 to 1.66, p = 7.1e-5)
- feat_c: 0.99 (95% CI 0.84 to 1.16, p = 0.87)
- feat_d: 2.07 (95% CI 1.73 to 2.47, p = 1.7e-15)

feat_a, feat_b and feat_d keep their effects after mutual adjustment. feat_c adds nothing.

### Interactions

No significant interaction was found. The interaction tests are low-powered: the interaction CIs run from about 0.72 to 1.28, which includes effects well away from 1, so a real interaction cannot be excluded.

- feat_a × feat_b: OR 1.07 per SD² (95% CI 0.89 to 1.28, p = 0.48)
- feat_a × feat_c: OR 0.92 (95% CI 0.77 to 1.10, p = 0.38)
- feat_a × feat_d: OR 0.89 (95% CI 0.72 to 1.10, p = 0.28, n = 850)

The median-split cell rates below are descriptive. They come from median-split cells and are hypothesis-generating only, because the interaction terms are not significant.

- **feat_a × feat_d:** The outcome rate is 13.1% when both features are below median (n = 214), 30.8% when feat_a is low and feat_d high (n = 211), 47.4% when feat_a is high and feat_d low (n = 211), and 66.4% when both are high (n = 214).
- **feat_a × feat_b:** Within feat_a-high rows, the outcome rate is 51.1% when feat_b is low and 63.1% when feat_b is high. Within feat_a-low rows, it is 21.7% when feat_b is low and 22.4% when feat_b is high. The feat_b gap is therefore visible within feat_a-high rows and absent within feat_a-low rows.
- **feat_a × feat_c:** The outcome rate is 23.5% when both are below median (n = 264), 20.3% when feat_a is low and feat_c high (n = 236), 60.2% when feat_a is high and feat_c low (n = 236), and 54.9% when both are high (n = 264).

### feat_d missingness

- Missingness is 150 of 1,000 rows (15.0%).
- **Univariate tests (eda_2):** No significant difference was found between rows with and without feat_d for feat_a (mean -0.073 when missing vs -0.002 when present, Welch p = 0.424), feat_b (0.128 vs 0.050, p = 0.400), feat_c (0.009 vs -0.009, p = 0.835) or the outcome (rate 41.3% vs 39.4%, chi-square p = 0.724). These univariate tests do not establish independence.
- **Joint test (stat_2):** A logistic regression of the missing flag on feat_a, feat_b, feat_c and the outcome shows no joint dependence. The likelihood-ratio statistic is 2.218 on 4 df (p = 0.696), and the pseudo R-squared is 0.0026. No single predictor is significant: feat_a p = 0.252, feat_b p = 0.412, feat_c p = 0.826, outcome p = 0.419.
- **Interpretation:** The results are consistent with missing completely at random at the level these tests can detect. They do not show that the pattern is random.

![Outcome rate for rows with feat_d present vs missing](tasks/eda_2/charts/outcome_rate_by_feat_d_missing.png)

### Predictive models

The models were evaluated on a 200-row test set, trained on 800 rows. Missing feat_d values were imputed with the training median (0.052), and a feat_d missing indicator was included.

| Model | Accuracy | Precision | Recall | F1 | ROC AUC | Log loss | Train accuracy |
|---|---|---|---|---|---|---|---|
| Majority-class baseline | 0.605 | — | — | — | 0.5 | 0.671 | — |
| Logistic regression | 0.750 | 0.710 | 0.620 | 0.662 | 0.817 | 0.504 | 0.741 |
| Gradient boosting | 0.755 | 0.688 | 0.696 | 0.692 | 0.807 | 0.528 | 0.869 |

- Both models beat the majority-class baseline on accuracy, ROC AUC and log loss.
- Gradient boosting overfits: the gap between train accuracy (0.869) and test accuracy (0.755) is 0.11. Logistic regression shows no such gap. The gradient boosting test scores are therefore probably optimistic for an untuned model.
- Logistic regression and gradient boosting are not clearly different. ROC AUC is 0.817 for logistic regression against 0.807 for gradient boosting. Log loss is 0.504 against 0.528, and accuracy is 0.750 against 0.755. All of these differences are within noise on 200 rows. Logistic regression is at most the more stable choice.

**Feature importance for logistic regression.** Permutation importance is the mean drop in test ROC AUC over 30 repeats:

- feat_a: 0.225 (sd 0.035)
- feat_d: 0.085 (sd 0.018)
- feat_b: 0.001 (sd 0.008)
- feat_c: 0.000 (sd 0.001)
- feat_d missing indicator: -0.003 (sd 0.004)

For gradient boosting, the ranking by importance is feat_a (0.513), feat_d (0.212), feat_b (0.181) and feat_c (0.093), with the missing indicator at 0.002.

**The missing indicator.** The indicator does not contribute to prediction for either model:

- Logistic regression: ROC AUC is 0.821 without the indicator and 0.817 with it. Log loss is 0.500 without it and 0.504 with it.
- Gradient boosting: ROC AUC is 0.802 without it and 0.807 with it, a difference of 0.005.

The measures do not agree on the indicator. Its standardized coefficient in the logistic regression is 0.363, which is fourth in the coefficient ranking. Its permutation importance is -0.003, and the ablation shows no gain in performance from including it. The findings report both measures and do not resolve the difference.

![Permutation importance of each feature for logistic regression, measured as the drop in test ROC AUC](tasks/ml_1/charts/perm_importance_logreg.png)

## Limitations

- **feat_d missingness:** 15% of rows are missing feat_d. The adjusted and univariate feat_d results use complete cases (n = 850). The predictive models use median imputation. The effect of this choice on the odds ratios and on the models was not tested.
- **Missingness mechanism:** Only univariate tests and one joint logistic test were run. The results are consistent with missing completely at random at the level these tests can detect, but this is not established.
- **Interactions:** All three interaction tests are low-powered. The median-split cell rates are descriptive and hypothesis-generating only.
- **feat_b non-monotonicity:** The quartile rates for feat_b are not monotonic. Whether this reflects real structure or sampling noise was not tested.
- **Rank-biserial intervals:** These use an approximate Fisher-z method, not an exact one.
- **Model evaluation:** Model comparison rests on one 200-row test split. Cross-validation was not run. Gradient boosting was not tuned, and it overfits.
- **Conflicting importance measures:** The coefficient ranking places the feat_d missing indicator fourth (0.363), but permutation importance and the ablation show no contribution. The findings report both and do not resolve the difference.
- **Unresolved review issue (feat_a × feat_b):** The lead's objection still stands. The stat_1 wording that the rise with feat_a is "not driven by feat_a alone" and "concentrated in the feat_a-high group" is not supported by the cell rates, and it is not carried into this report. This report states only the feat_b gap within feat_a-high rows (51.1% vs 63.1%) and its absence within feat_a-low rows (21.7% vs 22.4%). It is a descriptive pattern from median-split cells, and the interaction term (OR 1.07, p = 0.48) is not significant and low-powered, so it is hypothesis-generating. The same hedge applies to the feat_a × feat_d and feat_a × feat_c cell patterns.
- **Failed tasks:** None. All four analysis tasks and both model tasks completed.

## Open questions

- Is the non-monotonic pattern in feat_b's quartile rates real or sampling noise? A spline fit or bootstrap interval was proposed but not run.
- Do the feat_a and feat_d effects hold with nonlinear terms? Is the feat_a effect non-linear?
- Does the 150-row feat_d missingness bias the adjusted odds ratios? Does multiple imputation change them, or does a model-based or group-wise imputation change the importance of feat_d?
- Would a larger sample, or a bootstrap of the feat_a × feat_d interaction, narrow its CI enough to rule out a real modifying effect?
- Do the logistic regression and gradient boosting differences, and the missing-indicator effect, hold beyond noise under cross-validation?
- Does tuning gradient boosting (depth, learning rate or early stopping) reduce the train-test gap of 0.11, and how does it then compare with logistic regression?
- Would imputing feat_d change model performance, given the 15% missing share?