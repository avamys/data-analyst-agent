# Score Regression on the 60-Row Pilot Dataset (pilot.csv): Target `score`

## Summary

- **feat_1 is the only feature with a significant linear association with score.** Pearson r = 0.41 (95% CI 0.18 to 0.60, Holm p = 0.0067). Under the outlier exclusions tested, r stays between 0.40 and 0.50. feat_3 (r = -0.24) and feat_6 (r = -0.16) are weaker and do not survive multiple-comparison correction.
- **feat_3's association does not hold after adjusting for feat_1.** Its coefficient is -2.53 (95% CI -5.16 to 0.10, p = 0.059). Its nominal significance in the six-feature model (p = 0.039) is borderline and sensitive to the model choice.
- **No model beats a mean-only baseline reliably.** Linear regression has the best single-split test scores (test R² 0.144 vs -0.106 for the baseline). Its mean 5-fold CV R² is -0.68, and no model has a positive mean CV R².
- **feat_1 is the most important feature in both models, but the importance estimates are noisy.** feat_1, feat_3 and feat_6 are the top three in the single split and in repeated CV, as a set. Their permutation-importance SDs are large relative to their means.

## Data

- **Size:** 60 rows, 7 columns.
- **Target:** `score`, numeric (regression).
- **Features:** six numeric features (feat_1 to feat_6). There are no categorical, date/time, identifier or free-text columns.
- **Missing values:** none in any column.

## Findings

### Distribution and outliers

`score` is roughly symmetric: mean 48.95, median 48.75, SD 11.22, range 25.3 to 75.6, skew -0.15, with no IQR outliers.

![Distribution of score across the 60 rows](tasks/eda_1/charts/score_histogram.png)

Feature summaries:

| Feature | Mean | Median | SD | Range | Skew | IQR outliers |
|---|---|---|---|---|---|---|
| feat_1 | -0.04 | -0.12 | 0.97 | -2.93 to 2.55 | -0.30 | 3 |
| feat_2 | -0.16 | -0.23 | 0.98 | -2.19 to 2.50 | 0.29 | 1 |
| feat_3 | -0.32 | -0.30 | 1.00 | -2.88 to 1.73 | -0.09 | 0 |
| feat_4 | -0.08 | -0.06 | 1.00 | -2.19 to 2.07 | 0.12 | 0 |
| feat_5 | -0.22 | -0.17 | 0.66 | -2.13 to 1.65 | -0.16 | 2 |
| feat_6 | -0.10 | -0.20 | 1.10 | -2.54 to 2.53 | 0.03 | 0 |

### Univariate associations with score

Linear association with score, measured by Pearson r, is strongest for feat_1 (r = 0.41) and feat_3 (r = -0.24), with feat_6 (r = -0.16) weaker. feat_2 (r = 0.02), feat_4 (r = -0.09) and feat_5 (r = 0.08) are near zero.

![Scatter plots of score against feat_1 to feat_6, one point per row](tasks/eda_1/charts/score_vs_features_scatter.png)

Test results for each feature, with six tests and Holm correction:

- **feat_1:** Pearson r = 0.41 (95% CI 0.18 to 0.60, p = 0.0011, Holm p = 0.0067). Spearman rho = 0.47 (bootstrap 95% CI 0.22 to 0.69, Holm p = 0.0008). OLS slope 4.74 per unit (95% CI 1.97 to 7.50), R² = 0.169. This is the only feature significant after correction.
- **feat_3:** Pearson r = -0.24 (95% CI -0.47 to 0.01, p = 0.063, Holm p = 0.31). Spearman rho = -0.21 (Holm p = 0.58). OLS slope -2.71 (95% CI -5.57 to 0.15), R² = 0.059. Not significant after correction.
- **feat_6:** Pearson r = -0.16 (95% CI -0.40 to 0.09, p = 0.209, Holm p = 0.83). Spearman rho = -0.20 (Holm p = 0.58). OLS slope -1.69 (95% CI -4.34 to 0.97), R² = 0.027. Not significant.
- **feat_2:** Pearson r = 0.02 (95% CI -0.23 to 0.27, p = 0.878). Spearman rho = 0.06 (p = 0.640). OLS slope 0.23 (95% CI -2.78 to 3.25), R² = 0.0004. No association.
- **feat_4:** Pearson r = -0.09 (95% CI -0.33 to 0.17, p = 0.505). Spearman rho = -0.08 (p = 0.567). OLS slope -0.98 (95% CI -3.92 to 1.95), R² = 0.008. No association.
- **feat_5:** Pearson r = 0.08 (95% CI -0.18 to 0.32, p = 0.559). Spearman rho = 0.07 (p = 0.599). OLS slope 1.30 (95% CI -3.12 to 5.72), R² = 0.006. No association.

### feat_3 after adjusting for feat_1

- In a model with feat_1 and feat_3, the feat_3 coefficient is -2.53 (95% CI -5.16 to 0.10, p = 0.059). It is not distinguishable from zero at 5%. It moved about 7% from its simple slope of -2.71. The adjusted R² is 0.192 for this model and 0.042 for feat_3 alone.
- The feat_1 coefficient in this model is 4.63 (95% CI 1.93 to 7.34, p = 0.001).
- feat_1 and feat_3 are weakly correlated (Pearson r = -0.04, 95% CI -0.29 to 0.22, p = 0.76). The interval includes moderate correlations, so a meaningful correlation cannot be excluded with 60 rows.
- In the model with all six features, the feat_3 coefficient is -2.81 (95% CI -5.47 to -0.15, p = 0.039). The adjusted R² is 0.191, no better than the two-feature model. The result is nominally significant but borderline and not robust to the modelling choice.
- The analysis does not establish whether confounding by feat_1 explains the feat_3 association. It states that confounding is unlikely to be large given the weak feat_1–feat_3 correlation, but cannot be ruled out.

### Feature correlations and interactions

- **Feature–feature correlations:** no pair of features has |r| above 0.5, and no pair is flagged. The accepted finding names feat_1 with feat_5 (r = -0.184) as the largest magnitude. The correlation matrix itself gives feat_2 with feat_5 at -0.185, which is marginally larger. Both pairs are about 0.18 in magnitude.
- **Pairwise interactions** among feat_1, feat_3 and feat_6, with Holm correction across three tests:
  - feat_1 × feat_3: coefficient -2.49 (95% CI -5.31 to 0.32), p = 0.081, Holm p = 0.24.
  - feat_1 × feat_6: coefficient 0.15 (95% CI -2.41 to 2.71), p = 0.904, Holm p = 0.90.
  - feat_3 × feat_6: coefficient -1.72 (95% CI -4.27 to 0.83), p = 0.182, Holm p = 0.36.
- No interaction is significant after correction. No slope-at-levels analysis was reported. With n = 60, the study has limited power to detect interactions, so these results do not rule out small interactions.

### Predictive performance against a mean baseline

The fixed stratified 75/25 split gives 45 training rows and 15 test rows. Each model is compared with a mean-of-training baseline.

![Test-set RMSE of score for the mean baseline, linear regression and random forest on the fixed split](tasks/ml_1/charts/ml_1_test_rmse.png)

| Model | Test RMSE | Test MAE | Test R² | Train R² | Mean 5-fold CV R² (SD) |
|---|---|---|---|---|---|
| Mean baseline | 12.75 | 9.85 | -0.106 | 0.0 | -0.12 (0.11) |
| Linear regression | 11.21 | 8.98 | 0.144 | 0.245 | -0.68 (1.06) |
| Random forest | 13.32 | 9.55 | -0.207 | 0.866 | -0.35 (0.40) |

- **Baseline:** its train R² is 0.0 by definition. Its negative test R² (-0.106) reflects the test-set mean differing from the training mean, not overfitting.
- **Linear regression** beats the baseline on test RMSE, MAE and R². Its train R² (0.245) exceeds its test R² (0.144) by a gap of 0.10, which the finding describes as modest overfitting. Its mean CV R² on the training part is negative, so the test-set advantage is not reliable on 15 rows. Its largest absolute coefficients are feat_3 (3.91) and feat_1 (3.74).
- **Random forest** is worse than the baseline on test RMSE and R², and slightly better on test MAE (9.55 vs 9.85). It fits the training data well (train R² 0.866) and overfits badly, with test R² -0.207.
- **Disagreement between sources on the random forest:** the ml_2 record gives test R² -0.170, test RMSE 13.11 and train R² 0.863. The ml_1 record gives test R² -0.207, test RMSE 13.32 and train R² 0.866. Both are reported here. The source of the difference is not established.
- Overall, no model has a positive mean CV R², so generalisation is poor and the test-set verdicts are unstable.

### Feature importance

Permutation importance on the 15-row test set (mean drop in R², 20 repeats):

| Feature | Linear regression: mean (SD) | Random forest: mean (SD) |
|---|---|---|
| feat_1 | 0.405 (0.153) | 0.167 (0.187) |
| feat_3 | 0.062 (0.173) | 0.041 (0.134) |
| feat_6 | 0.053 (0.039) | 0.025 (0.033) |
| feat_5 | 0.046 (0.036) | 0.005 (0.023) |
| feat_4 | 0.011 (0.042) | -0.036 (0.019) |
| feat_2 | 0.005 (0.011) | 0.006 (0.035) |

- feat_1 is the most important feature for both models. Its lead is clearly larger than its uncertainty only in the linear model.
- The top three features (feat_1, feat_3, feat_6) are in the same order in both models. The full rankings differ only in the bottom three. Linear regression: feat_1, feat_3, feat_6, feat_5, feat_4, feat_2. Random forest: feat_1, feat_3, feat_6, feat_2, feat_5, feat_4.
- feat_3's SD exceeds its mean drop in both models, so its separation from the rest is weak.
- Because the random forest overfits strongly, its importances describe a model that does not generalise.

### Robustness of the feat_1 association

![Scatter of score against feat_1 with OLS fitted line and LOWESS curve](tasks/eda_2/charts/eda2_scatter.png)

- Excluding the top and bottom 5% of feat_1 (n = 54) gives Pearson r = 0.40 (p = 0.003), close to the full-sample r = 0.41 (n = 60, p = 0.001).
- Excluding the 5% of rows with the largest absolute OLS residuals (n = 57) gives r = 0.50 (p < 0.001). These rows weaken the association rather than create it.
- Excluding both the extreme 5% of feat_1 and the largest residuals gives r = 0.44 (n = 53, p = 0.0011) (eda_2 sensitivity record, trim5_and_resid5).
- Across these exclusions, the correlation stays in the range 0.40 to 0.50. The association is therefore positive and of similar size under these exclusions. The analysis does not show that it is unaffected by the few influential rows.
- The LOWESS curve gives score values of 44.0 at the 10th percentile of feat_1 (-1.182), 49.8 at the median (-0.115) and 59.2 at the 90th percentile (1.204). Linearity was not tested.

### Repeated 5-fold cross-validation on all 60 rows

Permutation importance (drop in R²) across 25 folds, mean (SD):

| Feature | Linear regression | Random forest |
|---|---|---|
| feat_1 | 0.287 (0.298) | 0.185 (0.335) |
| feat_2 | -0.012 (0.037) | -0.033 (0.069) |
| feat_3 | 0.116 (0.142) | -0.018 (0.117) |
| feat_4 | -0.034 (0.082) | -0.046 (0.057) |
| feat_5 | -0.002 (0.149) | -0.048 (0.083) |
| feat_6 | 0.022 (0.043) | -0.001 (0.058) |

- **Linear regression:** the CV ranking is feat_1, feat_3, feat_6, feat_5, feat_2, feat_4. The top three match the single-split ranking in identical order.
- **Random forest:** the CV ranking is feat_1, feat_6, feat_3, feat_2, feat_4, feat_5. The top three form the same set as the single-split top three, but feat_6 and feat_3 are swapped. feat_1 is top for both models, but its SD is large relative to its mean.
- **Disagreement on the random-forest single-split ranking:** the ml_3 record gives the single-split random-forest ranking as feat_1, feat_3, feat_6, feat_5, feat_2, feat_4. The ml_2 accepted ranking is feat_1, feat_3, feat_6, feat_2, feat_5, feat_4. They differ in the bottom three. Both are reported. The source of the difference is not established.
- **Overfitting across folds:**
  - Linear regression: mean train-minus-test R² is 0.356 (SD 0.343). This is moderate on average but varies widely across folds. It is much larger than the single-split gap of 0.10.
  - Random forest: mean train-minus-test R² is 1.020 (SD 0.428), confirming strong overfitting.
- The CV gaps come from 5-fold cross-validation on all 60 rows, whereas the single-split gap of 0.10 comes from the 45/15 split. The comparison is therefore indicative only.

![Mean and SD of permutation importance (drop in R²) across 25 CV folds, linear regression and random forest](tasks/ml_3/charts/ml3_cv_permutation_importance.png)

## Limitations

- **Sample size:** 60 rows, and a 15-row test set in the single split. Test-set R², RMSE and permutation importances are unstable. The findings say so, and the SDs are as large as the means for several features.
- **Model performance:** no model has a positive mean CV R². The linear model's test-set advantage over the baseline rests on 15 rows.
- **Interactions:** the study has limited power to detect interactions with n = 60, so non-significant interactions do not rule out small ones.
- **Confounding:** the feat_3 association cannot be separated from possible confounding by feat_1 with this sample.
- **Nonlinearity:** linearity of the feat_1 relationship was not tested. The LOWESS result is descriptive only.
- **Outliers:** feat_1 has 3 IQR outliers, feat_2 has 1 and feat_5 has 2. The robustness analysis of feat_1 excludes the extreme 5% and the largest residuals, but this does not establish that the association is unaffected by a few points.
- **Conflicting source values:** the random-forest test R² (-0.207 in ml_1, -0.170 in ml_2), train R² (0.866 in ml_1, 0.863 in ml_2) and single-split bottom-three ranking (ml_3 vs ml_2) differ between accepted records. Both values are reported; the disagreement is not resolved.
- **Fold sizes:** the fold sizes for the 5-fold CV are not recorded in the findings, so the CV gaps cannot be placed on the same footing as the 45/15 single split.
- **Unresolved review issues** (the lead's objections still stand):
  - *ml_1, baseline interpretation:* the statement that a mean-only predictor is overfit by construction and that its gap is an artifact has been withdrawn. The baseline's train R² is 0.0 by definition, and its negative test R² (-0.106) reflects the test-set mean differing from the training mean, not overfitting. This affects the baseline row of the model table above.
  - *eda_2, robustness wording:* the p-value for the case excluding the extreme 5% of feat_1 and the largest residuals (n = 53, r = 0.44) is p = 0.0011 (eda_2 sensitivity record, trim5_and_resid5). The robustness conclusion is limited to the r range of 0.40 to 0.50 that the exclusions produce. It is not a claim that the association is free of influence from a few points.
  - *ml_3, CV reporting:* per-feature means and SDs for both models are given in the CV table above. The CV gaps come from 5-fold cross-validation on all 60 rows, while the single-split gap comes from 45/15 data, so their comparison with 0.10 is indicative only. The linear gap is described as moderate, consistent with its SD of 0.343, and is not stated as small or large.
- **Failed tasks:** none. All tasks reported complete status.

## Open questions

- Is the feat_1 relationship linear, or does a nonlinear fit improve it? (raised by eda_1, stat_1, stat_2, eda_2)
- Does a multivariable model that includes feat_1 and feat_3 and controls for outliers change the feat_3 association? (raised by stat_1, stat_2, eda_2) Part of this was answered for feat_3 by stat_3, but robustness to the feat_1 outliers was not tested.
- Is the feat_3 association stable under robust regression or after removing the feat_1 IQR outliers? (raised by stat_3)
- Does the feat_3 effect differ by feat_1 level? (raised by stat_3; the interaction test in stat_2 is not significant but has low power)
- Does a larger sample, or repeated cross-validation, change which model beats the baseline? (raised by ml_1; partly addressed by ml_3, which found no model with positive mean CV R²)
- Does a regularised or nonlinear model change the feature ranking or improve generalisation? (raised by ml_1, ml_2)
- Does the high SD of feat_1 importance across folds reflect a few influential rows? (raised by ml_3)
- Why does the random forest overfit so strongly, and does stronger regularisation change its importance ranking? (raised by ml_3)
- Why is the linear CV overfitting gap much larger than the single-split gap (0.356 vs 0.10), and is it driven by a few folds? (raised by ml_3)