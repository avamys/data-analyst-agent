# Score Prediction From Six Numeric Features: Analysis of 60 Rows

## Summary

- **One feature has a clear linear association with score.** feat_1 has Pearson r = 0.41 (95% CI 0.18 to 0.60, p = 0.001) and survives Holm correction across the six simple tests (Holm p = 0.007). With its 3 IQR outliers removed (n = 57), r = 0.35 (p = 0.008).
- **No pairwise interaction was detected.** The joint F-test of the 15 product terms gives F = 1.20 on 15 df, p = 0.31. No individual interaction survives multiple-comparison correction.
- **No model beat the mean-prediction baseline in cross-validation.** On 5-fold CV of the 42-row training split, the baseline has MAE 9.58 and R² -0.34. The random forest is nominally better (MAE 9.24, R² -0.27), but its differences are smaller than the fold-to-fold spread, and its R² is still negative.
- **feat_1 ranks first on average in permutation importance under both models, but the ranking is unstable.** Across six seeded 70/30 splits, its mean rank is 1.667 (linear) and 1.500 (random forest). Its importance sd across splits is 0.85 and 0.81. On the single seed-42 split, the random forest ranked it fourth.
- **The other features show no reliable association with score.** feat_3 (r = -0.24, p = 0.063) and feat_6 (r = -0.16, p = 0.21) are weak and negative, and feat_2, feat_4 and feat_5 have |r| ≤ 0.09.

## Data

- 60 rows and 7 columns: the target `score` and six numeric features (feat_1 to feat_6).
- No categorical, date/time, identifier or free-text columns.
- No missing values and no duplicate rows.

## Findings

### Target distribution

- score: mean 48.95, median 48.75, sd 11.22, range 25.3 to 75.6, skewness -0.14.
- No score values are outliers under the IQR rule, so the distribution is close to symmetric.

![Histogram and box plot of score across the 60 rows](tasks/eda_1/charts/score_hist_box.png)

### Feature distributions and intercorrelations

- Each feature is centred near zero, with sd between 0.66 (feat_5) and 1.10 (feat_6). The absolute skewness of every feature is at most 0.29.
- IQR-rule outlier counts: feat_1 3, feat_2 1, feat_5 2, and feat_3, feat_4 and feat_6 none.
- The largest absolute Pearson correlation between any two features is 0.185 (feat_2 with feat_5). Two other pairs are close: feat_1 with feat_5 (r = -0.184) and feat_4 with feat_6 (r = 0.178). No pair meets the collinearity flag.

### Simple associations with score

Pearson r, Fisher 95% CI, p-value, Holm-adjusted p (across the six simple tests), and OLS slope (score points per unit) with 95% CI:

| Feature | Pearson r (95% CI) | p | Holm p | Spearman rho | Slope (95% CI) |
|---|---|---|---|---|---|
| feat_1 | 0.41 (0.18 to 0.60) | 0.001 | 0.007 | 0.47 (p = 0.0001) | 4.74 (1.97 to 7.50) |
| feat_3 | -0.24 (-0.47 to 0.01) | 0.063 | 0.31 | -0.21 | -2.71 (-5.57 to 0.15) |
| feat_6 | -0.16 (-0.40 to 0.09) | 0.21 | 0.83 | -0.20 | -1.69 (-4.34 to 0.97) |
| feat_5 | 0.08 (-0.18 to 0.32) | 0.56 | 1.0 | 0.07 | 1.30 (-3.12 to 5.72) |
| feat_2 | 0.02 (-0.23 to 0.27) | 0.88 | 1.0 | 0.06 | 0.23 (-2.78 to 3.25) |
| feat_4 | -0.09 (-0.33 to 0.17) | 0.51 | 1.0 | -0.08 | -0.98 (-3.92 to 1.95) |

- feat_1 is the only feature that survives Holm correction.
- feat_3 and feat_6 have weak negative associations that are not significant at 0.05.
- feat_2, feat_4 and feat_5 have no detectable linear association with score; none of their raw p-values is below 0.5.

![Scatter plots of score against feat_1 and feat_3, the features with the strongest correlations to score](tasks/eda_1/charts/score_scatter_top_features.png)

### Multiple regression on all six features

- The full model explains R² = 0.273 (adjusted R² = 0.191), with overall F-test p = 0.0075.
- Standardized coefficients: feat_1 0.42, feat_3 -0.25, feat_5 0.20, feat_6 -0.11, feat_2 0.07, feat_4 -0.06.
- Raw coefficient p-values: feat_1 0.00098, feat_3 0.039, feat_5 0.11, feat_6 0.39, feat_2 0.58, feat_4 0.59.
- After Holm correction across the six coefficients, only feat_1 survives (Holm p = 0.0059). feat_3 does not (Holm p = 0.196). The feat_3 negative association is significant only unadjusted, in the full model.

### Robustness of the feat_1 association

- With all 60 rows: Pearson r = 0.41 (p = 0.001) and Spearman rho = 0.47 (p = 0.0001).
- After excluding the 3 feat_1 IQR outliers (fences -1.71 and 1.81; n = 57): Pearson r = 0.35 (p = 0.008) and Spearman rho = 0.43 (p = 0.001).
- The findings state that excluding the outliers lowers Pearson r by 0.06 and Spearman rho by 0.05. Both remain significant at 0.05, and the findings conclude that the association is not materially changed and does not depend on the outliers.

### Interactions

- The joint F-test of the 15 pairwise product terms against the main-effects model gives F = 1.20 on 15 df, p = 0.31. This is the test that addresses whether any pair interacts, and it does not show an interaction.
- R² rises from 0.273 to 0.507 when the terms are added. The findings state that this increase is expected from fitting 15 extra terms to 60 rows and is not evidence of interaction on its own.
- No individual interaction survives correction. The two smallest raw p-values are feat_2 × feat_4 (coefficient -4.54 on standardized features, 95% CI -8.67 to -0.42, p = 0.032, Holm 0.48) and feat_3 × feat_4 (coefficient 3.07, 95% CI -0.03 to 6.17, p = 0.052, Holm 0.73). The remaining terms all have raw p above 0.2.
- Because no interaction survives correction, no conditional slopes were estimated.

### Predictive performance against the mean baseline

Five-fold cross-validation on the 42-row training split (same folds for all models; 18-row test split, seed 42):

| Model | CV MAE (fold sd) | CV RMSE (fold sd) | CV R² (fold sd) |
|---|---|---|---|
| Mean-prediction baseline | 9.58 (1.51) | 12.16 (1.98) | -0.34 (0.30) |
| Linear regression | 10.51 (2.51) | 12.38 (2.90) | -0.38 (0.43) |
| Ridge | 10.33 (2.49) | 12.20 (2.92) | -0.34 (0.42) |
| Random forest | 9.24 (2.20) | 11.85 (3.19) | -0.27 (0.47) |

- Linear regression and ridge are worse than the baseline on all three metrics.
- The random forest is nominally better than the baseline on all three metrics, but the findings describe its differences (about 0.3) as far smaller than the fold sd (2.2 to 3.2 for the models). Its R² is still negative. The findings conclude that the result does not show any model beating the mean, and that the random forest's advantage is not reliable.
- An overfitting explanation for the random forest's out-of-fold performance (possibly linked to the 2-row minimum leaf setting) is recorded as plausible but was not tested by tuning or nested CV.

![Cross-validated MAE of the mean-prediction baseline and three models on identical 5-fold splits of the 42-row training set; bars show mean across folds with fold sd](tasks/ml_1/charts/ml1_cv_mae_comparison.png)

### Feature importance: single split

Random forest permutation importance on the 18-row test split (seed 42), ranked by mean increase in MAE when the feature is shuffled (30 repeats):

- feat_6 0.244 (sd 0.246)
- feat_5 0.223 (sd 0.226)
- feat_4 -0.065 (sd 0.249)
- feat_1 -0.138 (sd 0.836), fourth of six
- feat_3 -0.266 (sd 0.242)
- feat_2 -0.294 (sd 0.416)

- For feat_4, feat_1, feat_3 and feat_2, the mean importance is at or below zero. The findings state that shuffling them did not raise test error, which is consistent with no contribution but does not prove it.
- The findings describe this ranking as unstable, because the sd values are as large as the means, and as disagreeing with the EDA: feat_1 has the strongest correlation with score, yet ranks fourth here.

### Feature importance: repeated splits

Six seeded 70/30 splits, 30 permutation repeats each. Rank 1 is most important.

| Feature | Linear: mean rank | Linear: mean MAE increase (sd) | Random forest: mean rank | Random forest: mean MAE increase (sd) |
|---|---|---|---|---|
| feat_1 | 1.667 | 1.086 (0.852) | 1.500 | 1.173 (0.811) |
| feat_6 | 2.500 | 0.107 (0.222) | 2.833 | 0.066 (0.181) |
| feat_5 | 3.333 | 0.098 (0.407) | 3.667 | -0.058 (0.153) |
| feat_2 | 4.333 | -0.183 (0.301) | 4.000 | -0.117 (0.166) |
| feat_4 | 4.333 | -0.290 (0.276) | 4.333 | -0.173 (0.220) |
| feat_3 | 4.833 | -0.368 (0.236) | 4.667 | -0.296 (0.405) |

- feat_1 is in the top two in 5 of 6 seeds under both models.
- For the random forest, feat_1's mean increase has a range of -0.1375 to 2.1011 across seeds, and is positive in 5 of 6 seeds.
- The findings describe feat_6 and feat_5 as weak and unstable, with large sd values relative to their means.

![Permutation importance per feature for the linear and random forest models, mean MAE increase over 6 seeded 70/30 splits with sd across splits as error bars](tasks/ml_2/charts/ml2_repeated_importance.png)

## Limitations

- **Small sample.** There are 60 rows. Confidence intervals are wide: the feat_1 Pearson CI runs from 0.18 to 0.60. Results are stated cautiously in the findings and should be read that way.
- **Narrow model evaluation.** Model comparisons use one 5-fold CV on a 42-row training split and one 18-row test split. Predictive results are not repeated across folds or splits, and no hyperparameters were tuned. The random forest's advantage over the baseline is within fold-to-fold noise.
- **Permutation importance rests on 18 rows for the single-split result.** Importance values on the seed-42 split are unstable (sd up to 0.84), and the repeated-split analysis covers only six seeds.
- **Unverified fact source for the seed-42 importance ranking.** The ml1_perm_importance values were written from hard-coded literals in the code and were not recomputed. They rest on the ml_1 report alone.
- **Unresolved review issue: fourth place of feat_1 in ml_1.** The ml_2 finding makes two claims that disagree. One says the low rank "reflects the split on which it was measured" and that the seed-42 value (-0.138) matches the seed minimum (-0.1375). The other says the data "do not cleanly separate split effects from random forest effects," so the low rank is not attributed to the split rather than the model. The seed-42 match is inferred from the summary minimum, since per-seed values are not reported. The lead's objection stands: the evidence does not establish whether the fourth-place rank is due to the split or the model. The ranking of feat_1 across six seeds is top under both models, but with six seeds only.
- **Interaction results are unadjusted for the 15-term CIs** and have low power: with 60 rows, only interactions of substantial size would be reliably detected. The coefficients are on standardized features.
- **feat_3 negative association** is significant only unadjusted, in the full model. It does not survive Holm correction in either the simple or the full-model tests.
- **Outliers.** feat_1 has 3 IQR outliers and feat_5 has 2. The influence of the feat_5 pair on any relation was not checked.
- All six tasks (eda_1, stat_1, stat_2, ml_1, stat_3, ml_2) are recorded as complete. No task failed.

## Open questions

- Does a multivariable model using feat_1 with feat_3 and feat_6 improve on feat_1 alone, or do the negative associations of feat_3 and feat_6 disappear once feat_1 is controlled for? This has not been tested.
- Does feat_1 alone beat the mean in cross-validation, including after its 3 outliers are removed?
- Does the random forest's instability for feat_1 reflect overfitting? Nested CV over min_samples_leaf and max_depth has not been run.
- Does the top rank of feat_1 under both models hold across 20 or more seeds, or under repeated 5-fold CV, given sd values of 0.81 to 0.85?
- Is feat_1's importance driven by a few influential rows or by its 3 IQR outliers? Importance has not been re-run with those rows removed.
- Is the feat_2 × feat_4 interaction (raw p = 0.032, Holm 0.48) real? A targeted test and an influence check have not been done.
- How large an interaction could 60 rows detect reliably? A power analysis has not been done.
- Does the feat_1 main effect hold in a model refit with fewer interaction terms?
- Is the feat_5 outlier pair influential on the feat_5 and feat_1 coefficients? Is feat_5's narrow spread (sd 0.66) a sign of restricted range?