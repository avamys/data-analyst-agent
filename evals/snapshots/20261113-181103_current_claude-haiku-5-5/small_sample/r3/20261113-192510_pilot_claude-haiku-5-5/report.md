# Analysis of Score in a 60-Row Dataset with Six Numeric Features

## Summary

- **feat_1 is the only feature with a clear linear association with score.** Its OLS slope is 4.74 score points per unit (95% CI 1.97 to 7.50, p = 0.0011), and its Pearson r is 0.41 (95% CI 0.18 to 0.60). It stays significant after Holm correction across six tests (adjusted p = 0.0067). The other five features are not significant after correction.
- **No feature significantly modifies the effect of another.** The smallest Holm-adjusted p across 15 pairwise interactions is 0.476. The interaction model does not improve fit over main effects (nested F-test p = 0.31).
- **Six-feature models do not beat a mean-only baseline out of sample.** Baseline 5-fold CV R² is -0.105; linear regression is -0.126 and random forest is -0.267.
- **A one-feature model on feat_1 does beat the baseline out of sample, but the gain is modest and likely overstated.** On one 5-fold split, mean CV R² is 0.098 versus -0.105. Across 10 repeated 5-fold seeds, mean R² is 0.010 versus -0.107 (feat_1 wins in 9 of 10 repeats). feat_1 was selected using the full dataset, so these CV results are not a clean held-out test.

## Data

- 60 rows and 7 columns: the target `score` and six numeric features (`feat_1` to `feat_6`).
- No categorical, date/time, identifier or free-text columns.
- No missing values in any column (0 missing cells), so no rows were dropped.
- The team also published a clean table with 60 rows and 13 columns: the 7 raw columns plus six z-score columns.

## Findings

### Score distribution and feature distributions (eda_1)

- Score has mean 48.95, median 48.75, sd 11.22, minimum 25.3 and maximum 75.6. Skewness is -0.15, so the distribution is roughly symmetric with no strong tail.
- Feature skewness is small for all six features, between about -0.30 and 0.29.
- Among the six features, the largest absolute correlation between any two is 0.19, so multicollinearity is not a concern.

![Histograms of score and the six features: count of rows per value bin](tasks/eda_1/charts/feature_histograms.png)

![Scatter of score (y axis) against each feature (x axis), one point per row](tasks/eda_1/charts/score_vs_features_scatter.png)

### Association of each feature with score (stat_1, eda_1)

| Feature | OLS slope (95% CI) | slope p | Pearson r (95% CI) | Holm-adjusted p |
|---|---|---|---|---|
| feat_1 | 4.74 (1.97 to 7.50) | 0.0011 | 0.41 (0.18 to 0.60) | 0.0067 (significant) |
| feat_2 | 0.23 (-2.78 to 3.25) | 0.878 | 0.02 (-0.23 to 0.27) | 1.000 |
| feat_3 | -2.71 (-5.57 to 0.15) | 0.063 | -0.24 (-0.47 to 0.01) | 0.313 |
| feat_4 | -0.98 (-3.92 to 1.95) | 0.505 | -0.09 (-0.33 to 0.17) | 1.000 |
| feat_5 | 1.30 (-3.12 to 5.72) | 0.559 | 0.08 (-0.18 to 0.32) | 1.000 |
| feat_6 | -1.69 (-4.34 to 0.97) | 0.209 | -0.16 (-0.40 to 0.09) | 0.835 |

- Slopes are in score points per unit of the feature. Holm adjustment was applied to the six slope p-values.
- For feat_1, the Spearman rank correlation is 0.47 (p = 0.0001), compared with the Pearson r of 0.41. The two measures differ somewhat, and the team did not resolve whether the relationship is nonlinear.
- For feat_3, the association is negative but not significant (raw p = 0.063).
- **Median split, feat_1:** mean score is 43.73 in the low half and 54.17 in the high half, Welch p = 0.00016, Cohen's d = 1.04 (n = 30 per half).
- **Median split, feat_2 to feat_6:** Welch p-values range from 0.26 to 0.79 and |Cohen's d| is at most 0.29 (feat_3). The team reports that this agrees with the Holm-adjusted regression results.

![Mean score for feat_1 below versus above its median (n=30 per half)](tasks/stat_1/charts/feat1_median_split.png)

### Interactions (stat_2)

- None of the 15 pairwise interaction terms is significant after Holm correction. The smallest adjusted p is 0.476 (feat_2 × feat_4, raw p = 0.032, coefficient -4.47, 95% CI -8.52 to -0.41).
- Adding the 15 interaction terms raises R² from 0.273 to 0.507. The nested F-test gives F = 1.20 on 15 numerator degrees of freedom, p = 0.31. Adjusted R² rises from 0.191 to 0.234.
- Because no interaction was significant, the median-split breakdown was not run.
- The intervals are wide, so the team states that interactions of moderate size remain compatible with the data. The null result does not show the absence of moderation.

### Predictive performance of the six features against the baseline (ml_1)

- Model comparison uses 5-fold CV on the six z-scored features:

| Model | Mean CV R² (sd) | Mean CV RMSE (sd) |
|---|---|---|
| Mean-only baseline | -0.105 (0.078) | 11.25 (1.28) |
| Linear regression | -0.126 (0.378) | 11.16 (1.53) |
| Random forest | -0.267 (0.424) | 11.87 (1.96) |

- No model improves CV R² over the mean-only baseline. Linear regression's mean RMSE is only 0.09 below the baseline RMSE, which the team describes as well within one fold sd.
- Permutation importance for the linear regression (the best of the two fitted models by CV R²):
  - feat_1 ranks first, with a mean drop in CV R² of 0.416 (sd 0.239).
  - The other features rank 2 to 6: feat_3 (0.077, sd 0.172), feat_6 (0.040, sd 0.053), feat_2 (-0.009, sd 0.016), feat_5 (-0.026, sd 0.255), feat_4 (-0.086, sd 0.171).
  - The team reports that these ranks for feat_2 to feat_6 are unstable, because their sds are as large as their means.

![Cross-validated RMSE per model against the mean-only baseline](tasks/ml_1/charts/ml1_model_rmse.png)

### One-feature model on feat_1, single 5-fold split (ml_2)

- On KFold (shuffle, random_state = 0), the linear regression on z-scored feat_1 beats the mean-only baseline:
  - Mean CV R²: 0.098 (sd 0.113) versus -0.105 (sd 0.078). Gain 0.203 (sd 0.123).
  - Mean CV RMSE: 10.20 (sd 1.69) versus 11.25 (sd 1.28). Reduction 1.05 (sd 0.61).
- The feat_1 model has higher R² than the baseline in all 5 folds. Per-fold R² gains are +0.28, +0.31, +0.12, +0.03 and +0.28.
- No significance test of the gain was run.

![Out-of-sample R2 per fold for the mean-only baseline and the feat_1 linear regression, on the same 5 KFold splits (n=60)](tasks/ml_2/charts/ml2_fold_r2.png)

### Repeated 5-fold CV across 10 seeds (ml_3)

- Across 10 KFold (shuffle) seeds, mean CV R² is 0.010 (sd 0.148) for the feat_1 linear regression and -0.107 (sd 0.103) for the mean-only baseline. Mean gain is 0.117 (sd 0.082).
- The feat_1 model has a higher R² than the baseline in 9 of 10 repeats (90%). Per-seed gains range from -0.090 (seed 7) to +0.203 (seed 0).
- Mean CV RMSE is 10.39 (sd 0.30) for feat_1 versus 11.14 (sd 0.19) for the baseline. Mean reduction is 0.75 (sd 0.23).
- The single-split gain in ml_2 (0.203) is the upper end of these repeated results. The team says it overstates the typical gain.

## Limitations

- **Small sample.** With n = 60, confidence intervals are wide. The team did not run a power analysis, so it is unknown whether the weak associations of feat_2 to feat_6 with score are real but undetected or are noise.
- **Selection bias in the out-of-sample results (unresolved review issue, ml_2).** feat_1 was chosen as the strongest correlate of score using all 60 rows in the eda_1 and stat_1 findings (feat_1 has the largest correlation and the only significant association) and in the ml_1 permutation ranking. The ml_2 CV is therefore not a clean held-out test of that selection, and the gain is likely overstated. The ml_3 repeated CV reshuffles the same 60 rows and has the same limitation (not tested here).
- **Contrast between models (unresolved review issue, ml_2).** The one-feature feat_1 model beats the baseline (ml_2 mean R² 0.098 versus -0.105), while the six-feature linear regression does not (ml_1 mean R² -0.126 versus -0.105). This contrast is between two models as a whole, differing in number of features and evaluated in separate tasks. It should not be attributed to feat_1 alone. The team did not test whether adding features changes this result.
- **Single split and no formal test.** The ml_2 gain was not tested for significance and rests on one 5-fold split. The ml_3 results show it varies with the seed.
- **Linearity not tested.** The team did not test a quadratic or spline term. Pearson (0.41) and Spearman (0.47) values for feat_1 differ somewhat.
- **Feature importance instability.** Permutation importance ranks for feat_2 to feat_6 are unstable, and the team does not treat them as reliable.
- **Failed or skipped analyses.** No task failed. The median-split breakdown for interactions was not run because no interaction was significant.

## Open questions

- Does feat_1 remain the dominant predictor after controlling for the other features in a multivariate model with a formal coefficient test?
- Is the feat_1 relationship with score nonlinear? Would a quadratic or spline term improve the fit, both in-sample and out of sample?
- Does the feat_1 CV gain survive when feat_1 is selected inside each training fold (nested or permutation-based selection)?
- Does adding feat_3 or feat_6 to feat_1 improve CV performance beyond the one-feature model?
- Is the feat_2 × feat_4 interaction (raw p = 0.032) real? A pre-specified test or more data would be needed.
- What is the smallest effect a power analysis could detect for feat_2 to feat_6 at n = 60, and what size of interaction do the wide intervals rule out?
- Are the weak correlations of feat_2 to feat_6 with score real, as tested by repeated CV or bootstrapped feature importances?