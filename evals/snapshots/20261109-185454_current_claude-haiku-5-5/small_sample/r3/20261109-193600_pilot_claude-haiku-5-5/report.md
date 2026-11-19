# Score Prediction from Six Numeric Features (n = 60): Final Report

## Summary

- **feat_1 is the only feature with a robust association with score.** Pearson r = 0.41 (95% CI 0.18 to 0.60, Holm p = 0.007). Users in the upper median half of feat_1 have a mean score of 54.2, against 43.7 in the lower half (Cohen's d = 1.04). The association holds after adjusting for feat_2 to feat_6 (coefficient 4.86 points per unit, p = 0.001).
- **No other feature survives multiplicity correction.** feat_3 and feat_6 are weakly negative (raw p = 0.063 and 0.21). feat_2, feat_4 and feat_5 show essentially no association. In the full multiple regression, feat_3 is nominally significant (p = 0.039), but this does not survive correction and is exploratory.
- **No model beats a mean-predicting baseline.** On the 12-row test split, the baseline RMSE is 9.71, linear regression 9.75 and random forest 10.87. Five-fold cross-validation on the 48 training rows gives similar results (11.52, 11.53 and 11.39). Both fitted models overfit.
- **Interactions are not statistically supported.** The three pairwise interactions among feat_1, feat_3 and feat_6 all have Holm-adjusted p values above 0.24. Their sign patterns are descriptive only.

## Data

- **Size:** 60 rows × 7 columns.
- **Target:** score (numeric regression target). Mean 48.95, median 48.75, SD 11.22, range 25.3 to 75.6, skew −0.15.
- **Features:** six numeric features (feat_1 to feat_6). There are no categorical, date/time, identifier or free-text columns.
- **Missing values:** none in any column.

## Findings

### Score distribution and univariate relationships

Score is roughly symmetric and centred near 49 (mean 48.95, median 48.75, SD 11.22, skew −0.15). No column has any row with an absolute z-score above 3.

![Histogram of score: count of rows per bin](tasks/eda_1/charts/score_hist.png)

Pearson and Spearman correlations of each feature with score, from the 60 rows:

| Feature | Pearson r | Spearman rho | Pearson p |
|---|---|---|---|
| feat_1 | 0.41 | 0.47 | 0.001 |
| feat_2 | 0.02 | 0.06 | 0.88 |
| feat_3 | −0.24 | −0.21 | 0.063 |
| feat_4 | −0.09 | −0.08 | 0.51 |
| feat_5 | 0.08 | 0.07 | 0.56 |
| feat_6 | −0.16 | −0.20 | 0.21 |

Only feat_1 has a clear linear and rank relationship with score. feat_3 and feat_6 are weakly negative but not significant at the 0.05 level. feat_2, feat_4 and feat_5 are all |r| ≤ 0.09 with p > 0.5.

![Scatter of each feature against score, one point per row](tasks/eda_1/charts/feature_scatter.png)

### Statistical significance and effect sizes

**feat_1 (significant after correction).** Across six tests, the Pearson r is 0.41 (95% CI 0.18 to 0.60; raw p = 0.001; Holm p = 0.007; n = 60).

In a median split on feat_1 (30 rows per half), the upper half has mean score 54.2 and the lower half 43.7, a difference of 10.4 points. Welch p = 0.0002 (Holm p = 0.001), and Cohen's d = 1.04 (approximate 95% CI 0.50 to 1.58), a large effect.

**feat_3 and feat_6 (not significant after correction).**
- feat_3: r = −0.24 (95% CI −0.47 to 0.01; raw p = 0.063; Holm p = 0.31). Median-split d = −0.29 (CI −0.80 to 0.22; Welch p = 0.26).
- feat_6: r = −0.16 (95% CI −0.40 to 0.09; raw p = 0.21; Holm p = 0.83). Median-split d = −0.07 (CI −0.58 to 0.44; Welch p = 0.79).

**feat_2, feat_4 and feat_5 (no association).**
- feat_2: r = 0.02 (95% CI −0.23 to 0.27; p = 0.88). Median-split d = −0.20 (CI −0.70 to 0.31).
- feat_4: r = −0.09 (95% CI −0.33 to 0.17; p = 0.51). Median-split d = −0.10 (CI −0.60 to 0.41).
- feat_5: r = 0.08 (95% CI −0.18 to 0.32; p = 0.56). Median-split d = 0.20 (CI −0.31 to 0.70).

All of these CIs include zero, and their Holm-adjusted p values are 1.0.

### Adjusted (multiple regression) association

In the full multiple regression of score on all six features (R² = 0.27, adjusted R² = 0.19):

| Feature | Coefficient (points per unit) | SE | p |
|---|---|---|---|
| feat_1 | 4.86 | 1.39 | 0.001 |
| feat_2 | 0.77 | 1.39 | 0.58 |
| feat_3 | −2.81 | 1.33 | 0.039 |
| feat_4 | −0.72 | 1.34 | 0.59 |
| feat_5 | 3.33 | 2.06 | 0.11 |
| feat_6 | −1.08 | 1.24 | 0.39 |

- The feat_1 slope is essentially unchanged by adjustment: 4.74 points per unit in the simple regression (SE 1.38, p = 0.001) against 4.86 in the full model.
- The feat_3 coefficient (p = 0.039) would not survive Bonferroni correction for six tests (adjusted p about 0.23). It should be treated as exploratory.
- **Curvature:** the squared term for centred feat_1 has coefficient 0.63 (SE 0.87, p = 0.48). The ANOVA comparing models with and without it gives F = 0.52, p = 0.475. Curvature was not detected, but this does not establish linearity.
- **Residuals:** no obvious pattern against fitted values. Shapiro-Wilk W = 0.987, p = 0.79, so normality of residuals is not rejected.

![Residuals of the full multiple regression against fitted score, one point per row](tasks/stat_2/charts/resid_vs_fitted.png)

### Interactions

**Descriptive cell means (median splits).** Each pair was split at the median, giving four cells of 13 to 17 rows.

- **feat_1 × feat_3:** within the feat_1 upper half, the feat_3 effect is −6.7 points (57.8 for feat_3 low, 51.0 for feat_3 high). Within the lower half it is −1.2 points (44.3 vs 43.1). The sign is the same in both halves; the size differs.
- **feat_1 × feat_6:** the feat_6 effect is −1.3 points in the feat_1 lower half (44.5 vs 43.2) and +2.5 points in the upper half (53.1 vs 55.6). The sign reverses.
- **feat_3 × feat_6:** the feat_6 effect is +1.3 points in the feat_3 lower half (49.9 vs 51.2) and −3.4 points in the upper half (48.9 vs 45.5). The sign reverses.

![Mean score in each median-split cell for the top three features by correlation with score (feat_1, feat_3, feat_6), one panel per pair; y-axis is mean score](tasks/eda_2/charts/interaction_plots.png)

These cells are small, and the reversals are described as tentative.

**Formal interaction tests.** Neither the median-split nor the continuous interaction term is distinguishable from zero after Holm correction across the three pairs.

| Pair | Median-split coefficient (95% CI; Holm p) | Continuous coefficient (95% CI; Holm p) |
|---|---|---|
| feat_1 × feat_3 | −5.50 (−15.72 to 4.72; 0.86) | −2.49 (−5.31 to 0.32; 0.24) |
| feat_1 × feat_6 | +3.77 (−6.80 to 14.33; 0.86) | +0.15 (−2.41 to 2.71; 0.90) |
| feat_3 × feat_6 | −4.71 (−16.44 to 7.02; 0.86) | −1.72 (−4.27 to 0.83; 0.36) |

The median-split CIs are about 20 to 23 points wide, so they cannot exclude interactions of practical size. The signs of the formal tests match the descriptive patterns in direction. The reported magnitudes are not statistically supported.

### Predictive models against a mean baseline

Models were fitted on an 80/20 split (seed 42: 48 training rows, 12 test rows).

| Model | Test RMSE | Test R² | 5-fold CV RMSE (mean, SD) on training rows | Train R² |
|---|---|---|---|---|
| Mean baseline | 9.71 | 0.00 | 11.52 (2.50) | — |
| Linear regression | 9.75 | −0.01 | 11.53 (1.92) | 0.30 |
| Random forest | 10.87 | −0.25 | 11.39 (2.77) | 0.78 |

- No model beats the mean baseline meaningfully on either test RMSE or CV RMSE. The CV differences are far smaller than one SD.
- Both fitted models overfit. The train-to-test R² gap is 0.31 for linear regression and 1.04 for random forest.

![Test RMSE and 5-fold CV RMSE of each model against the mean baseline](tasks/ml_1/charts/ml1_model_rmse.png)

**Feature importance.**
- Linear regression: the largest absolute coefficients are feat_1 (5.14), feat_3 (3.40), feat_5 (1.94), feat_2 (1.55), feat_6 (1.04) and feat_4 (0.29).
- Random forest: the largest importances are feat_1 (0.42), feat_6 (0.14), feat_3 (0.12), feat_5 (0.12), feat_2 (0.11) and feat_4 (0.09).
- Permutation importance on the test set is positive for feat_1 in both models (increase in RMSE of 0.52 for linear regression and 0.54 for random forest). This is the most consistent signal, but it rests on 12 test rows and has large SDs (0.49 and 1.17).
- For the other features, signs and sizes differ between the two models. With 12 test rows, the ranking beyond feat_1 should not be used to choose features.

**Influence check.** Dropping the five largest in-sample residual rows (indices 38, 17, 34, 44, 19) and refitting the linear regression reduces test RMSE from 9.75 to 8.98. This is below the 9.71 baseline, but it rests on a single refit and 12 test rows, and it should not be read as the model beating the baseline. After dropping these rows, feat_2's coefficient moves from 1.57 to 0.47 and feat_4's changes sign, from 0.31 to −0.24. Other coefficient shifts are smaller: feat_3 moves from −3.32 to −1.95 and feat_6 from −0.92 to −0.48. feat_1 moves from 4.88 to 5.76.

**Missingness.** No missing values occur in any column across all 60 rows, so no missingness pattern exists.

## Limitations

- **Sample size.** With 60 rows, the study has limited power. Non-significant results for feat_2 to feat_6 do not establish absence of association. The median-split cells hold 13 to 17 rows each.
- **Test set.** Every model comparison on the 80/20 split uses 12 test rows. Test RMSE and permutation importances are therefore unstable. The CV results use the same 48 training rows.
- **Permutation importance for the best model is uninformative.** The best model by test RMSE is the mean baseline, and its permutation importances are all zero. The feature importances reported above therefore come from linear regression and random forest, not from the model that performed best.
- **Mislabelled coefficient units in the stat_3 interaction results.** The continuous interaction coefficients were recorded with a "standardized-term" description, which is incorrect. The values are raw-unit coefficients (score points per unit of the feature product). The mislabel should be disregarded, and the values read as raw units.
- **Influence refit is post hoc.** The five rows were selected by in-sample residual size and dropped after the fact. The resulting test RMSE change (−0.77) and coefficient shifts are not established as stable.
- **Multiplicity.** The feat_3 adjusted coefficient (p = 0.039) and all interaction p values are unadjusted for the full set of tests run across the analysis. Only the eda_1 correlations were corrected for multiplicity.
- **Linearity.** Curvature was tested only as a squared term for feat_1. The absence of a detected quadratic effect does not establish linearity.
- **Failed or inconclusive steps.** The permutation-importance step for the best model returned all zeros and gave no information. The planned permutation tests on the interaction terms were not run, and no tertile-based interaction analysis was done.
- **Unresolved review issues.** None were recorded beyond the caveats above.

## Open questions

- Does the feat_1 association hold, and is it linear, in a larger sample or under bootstrap or spline fits? The tasks did not test this beyond the quadratic check.
- Does feat_3's negative adjusted coefficient persist in a larger sample, given its borderline p value and sensitivity to multiplicity?
- Are the feat_1 × feat_3 and feat_1 × feat_6 interactions real? The tasks did not run a permutation test on the interaction terms or a tertile-based repeat of the analysis.
- Do feat_2, feat_4 and feat_5 contribute through interactions or nonlinear effects that pairwise correlation and median splits do not capture?
- Would repeated k-fold cross-validation or a larger sample show whether any model beats the mean baseline? The current evidence is limited to a 12-row test set and a single CV run.
- Are the feat_2 and feat_4 coefficient changes after dropping influential rows stable under different training subsets?