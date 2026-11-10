# Score Prediction from Six Numeric Features: 60-Row Regression Analysis

## Summary

- **Feature 1 is the only reliable association with score.** Its Pearson r is 0.411 (95% CI 0.175 to 0.602), and it stays significant after Holm correction (adjusted p = 0.0067). Its OLS slope is 4.74 score points per unit, and it explains R² = 0.169 of the variance.
- **No feature interacts with another beyond its main effect.** No pairwise interaction is significant after Holm correction, and the joint F-test of all 15 product terms gives F(15,38) = 1.20, p = 0.31.
- **The models disagree on whether they beat the mean baseline.** On a single 75/25 split (15 test rows), no model beats the mean baseline. Under repeated 5-fold CV over all 60 rows (10 repeats), both linear models beat it (ridge RMSE 10.905 vs. 11.245 for the baseline). The two evaluations disagree, and the report does not resolve this.
- **Random forest is the weakest model under repeated CV, and it overfits.** It has a train R² of 0.796 against a test R² of −0.426 on the single split, and a repeated-CV RMSE of 11.399, worse than the baseline's 11.245.
- **The flagged outliers do not drive the feature 1 result.** Removing the six rows with 1.5 IQR-flagged values raises the feature 1–score correlation from 0.411 to 0.465 (n = 54), with widely overlapping intervals.

## Data

- **Size:** 60 rows × 7 columns.
- **Target:** `score`, a regression target. Mean 48.95, median 48.75, sd 11.22, range 25.3 to 75.6, skew −0.14.
- **Features:** six numeric features, `feat_1` to `feat_6`. There are no categorical, date/time, identifier, or free-text features.
- **Missing values:** none in any of the seven columns, so no rows were dropped or imputed.

## Findings

### Distributions and pairwise correlations

Score is roughly symmetric, with a mean of 48.95, a median of 48.75, and a skew of −0.14.

![Distribution of score across 60 rows](tasks/eda_1/charts/score_histogram.png)

Per-feature means lie between about −0.32 and 0, and standard deviations are between 0.66 and 1.10. The features are close to standardised in form.

Pearson and Spearman correlations of each feature with score:

| Feature | Pearson r (p) | Spearman ρ (p) |
|---|---|---|
| feat_1 | 0.411 (0.001) | 0.474 (<0.001) |
| feat_2 | 0.020 (0.878) | 0.062 (0.640) |
| feat_3 | −0.242 (0.063) | −0.205 (0.116) |
| feat_4 | −0.088 (0.505) | −0.075 (0.567) |
| feat_5 | 0.077 (0.559) | 0.069 (0.599) |
| feat_6 | −0.165 (0.209) | −0.203 (0.119) |

The feature 1 Spearman correlation is stronger than its Pearson correlation, which suggests a monotone but not perfectly linear relationship.

![Scatter plots of each feature against score (60 rows)](tasks/eda_1/charts/feature_vs_score_scatter.png)

The six features are essentially uncorrelated with each other. The largest absolute pairwise Pearson r is −0.184 (feat_1 with feat_5), and no pair reaches |r| = 0.3.

### Significance and effect sizes

Six tests were run, with Holm correction applied.

- **feat_1:** r = 0.411 (95% CI 0.175 to 0.602), raw p = 0.0011, Holm p = 0.0067. OLS slope 4.74 (95% CI 1.97 to 7.50), R² = 0.169. This is the only feature significant after correction.
- **feat_3:** r = −0.242 (95% CI −0.467 to 0.013), raw p = 0.063, Holm p = 0.31. Slope −2.71 (95% CI −5.57 to 0.15), R² = 0.059. The negative association does not survive correction, and its CI includes zero.
- **feat_6:** r = −0.165 (95% CI −0.402 to 0.093), raw p = 0.209, Holm p = 0.83. Slope −1.69 (95% CI −4.34 to 0.97), R² = 0.027. Not significant.
- **feat_4:** r = −0.088 (95% CI −0.334 to 0.170), raw p = 0.51, Holm p = 1.0. R² = 0.008.
- **feat_5:** r = 0.077 (95% CI −0.181 to 0.325), raw p = 0.56, Holm p = 1.0. R² = 0.006.
- **feat_2:** r = 0.020 (95% CI −0.235 to 0.273), raw p = 0.88, Holm p = 1.0. R² = 0.0004.

By effect size, feat_1 is clearly largest. Only feat_1 is a reliable effect. The others are too small or too uncertain to separate from zero with 60 rows.

### Group averages across tertiles

Each feature was split into low, middle, and high tertiles of 20 rows each. No significance test was run on these group means. With n = 20 per tertile and score sd about 11, each group mean has a standard error of roughly 2.5 points.

| Feature | Low | Middle | High | Pattern |
|---|---|---|---|---|
| feat_1 | 41.7 | 51.7 | 53.4 | Rises; most of the rise is low to middle |
| feat_3 | 51.5 | 49.5 | 45.9 | Falls monotonically |
| feat_6 | 51.0 | 48.0 | 47.9 | Non-increasing; the drop is low to middle |
| feat_5 | 47.1 | 50.7 | 49.0 | Inverted U |
| feat_2 | 49.0 | 47.8 | 50.0 | Shallow U; spread about 2.3 points |
| feat_4 | 49.0 | 47.9 | 50.0 | Shallow U; spread about 2.0 points |

The feature 1 gap is the clearest pattern. The feature 3 and feature 6 gaps are borderline. The feature 2, feature 4 and feature 5 differences are within noise, according to the analysis.

![Mean score per feature tertile (low, middle, high), 60 rows](tasks/eda_2/charts/tertile_mean_score.png)

### Feature interactions

Fifteen pairwise product terms were tested over a main-effects model. No pair is significant after Holm correction. The three smallest raw p values are:

- feat_2 × feat_4: coefficient −3.70 (95% CI −7.19 to −0.21), raw p = 0.038, Holm p = 0.573, ΔR² = 0.058.
- feat_5 × feat_6: coefficient 3.32, raw p = 0.070, Holm p = 0.980, ΔR² = 0.045.
- feat_1 × feat_3: coefficient −2.70, raw p = 0.071, Holm p = 0.980, ΔR² = 0.045.

The main-effects model has R² = 0.273 (adjusted R² = 0.191). Adding all 15 product terms raises R² to 0.507, but the joint F-test gives F(15,38) = 1.20, p = 0.31. The analysis judges this no stronger than chance for 15 added terms on 60 rows.

### Predictive models

**Single 75/25 split** (45 training rows, 15 test rows, seed 42):

| Model | Test RMSE | Test MAE | Test R² | Train R² |
|---|---|---|---|---|
| Mean baseline | 9.88 | 8.19 | −0.001 | 0.0 |
| Linear regression | 10.35 | 8.92 | −0.097 | 0.319 |
| Random forest | 11.80 | 9.81 | −0.426 | 0.796 |

No model beats the mean baseline on test data. Both fitted models overfit. The linear regression train-test R² gap is 0.415, and the random forest gap is 1.222.

Five-fold CV on the training set ranked the random forest first (CV RMSE 10.85, against 11.43 for the baseline and 11.82 for linear regression). The fold SDs were 2.3 to 3.3, and the test set did not confirm this ranking.

Permutation importance for the random forest on test data (increase in test RMSE when shuffled) gives feat_1 0.422 and feat_6 0.174. The feat_3 value is −0.004. The feat_4, feat_5 and feat_2 values are negative (−0.270, −0.310, −0.659), so shuffling them did not hurt the test fit.

**Repeated 5-fold CV over all 60 rows** (10 repeats):

| Model | Mean CV RMSE | SD across repeats |
|---|---|---|
| Ridge | 10.905 | 0.259 |
| Linear regression | 10.945 | 0.269 |
| Mean baseline | 11.245 | 0.185 |
| Random forest | 11.399 | 0.293 |

Both linear models beat the mean baseline by about 0.3 RMSE. The analysis notes that this margin is modest relative to the fold-level SD of about 1.9. The across-repeat SD reflects only repeat-to-repeat variation of the same 60 rows, so it understates uncertainty. Random forest does not beat the baseline and has the widest fold-level SD (2.30).

![Repeated 5-fold x10 CV RMSE on all 60 rows for each model; lower is better](tasks/ml_2/charts/ml2_cv_rmse.png)

For ridge under repeated CV, permutation importance (RMSE increase when shuffled, across 50 folds) is led by feat_1 at 1.502 (SD 1.115), then feat_3 at 0.521 (SD 0.465). The feat_4, feat_2, feat_6 and feat_5 values are −0.156, −0.033, −0.033 and 0.037, so the analysis finds they add no predictive value.

**Disagreement between evaluations:** The single split ranks the models with random forest worst and no model beating the baseline. Repeated CV on all 60 rows ranks the linear models first and random forest last, and finds that the linear models beat the baseline. The analysis states that the single 15-row test set gave a misleading picture. Both results are reported here as they stand.

Across the EDA correlation, the linear coefficients (largest absolute coefficient 4.99 for feat_1), and the random forest permutation importance (0.422), feat_1 is the only feature that consistently stands out.

### Outliers and influence

By the 1.5 IQR rule, six feature values are flagged: three in feat_1, one in feat_2, and two in feat_5. No feat_3, feat_4 or feat_6 value is flagged, and no score value is flagged.

The six flagged values sit on six distinct rows (19, 25, 29, 30, 38, 49):

- feat_1: row 25 (−2.54, score 29.2), row 29 (−2.93, score 46.3), row 30 (2.55, score 63.4).
- feat_2: row 49 (2.5, score 49.7).
- feat_5: row 19 (1.65, score 29.1), row 38 (−2.13, score 25.3).

Removing these six rows changes the feature 1–score Pearson r from 0.411 (95% CI 0.175 to 0.602, n = 60) to 0.465 (95% CI 0.225 to 0.652, n = 54). The analysis concludes that the flagged rows do not drive the feature 1 relationship, since the intervals overlap widely. None of the flagged scores is outside the score fences of 22.14 to 77.44.

## Limitations

- **Small sample.** There are 60 rows. The single test split has only 15 rows, and the analysis states that this is too few to turn the feature 1 association into a predictive advantage over the mean. Most non-feature-1 effects cannot be separated from zero.
- **Tertile differences are untested.** The group means carry a standard error of roughly 2.5 points per tertile. No significance test was run on them, and the feature 3 and feature 6 gaps were described as borderline.
- **Interaction test power.** The interaction terms are underpowered for 60 rows. The feat_2 × feat_4 interaction (raw p = 0.038) does not survive correction (Holm p = 0.573).
- **Conflicting model rankings.** The single split and repeated CV disagree about whether any model beats the baseline (see Findings). The repeated-CV fold-level SDs (about 1.9) are wider than the margin by which the linear models beat the baseline.
- **Repeated-CV uncertainty.** The across-repeat SD reflects only repeat variation over the same 60 rows, so it understates uncertainty. The analysis states this directly.
- **Outlier handling.** The flagged values were kept in all analyses. The influence check (removing the six flagged rows) changed the feature 1 correlation from 0.411 to 0.465, with overlapping intervals.
- **No failed tasks or unresolved review objections** are recorded for this analysis.

## Open questions

- Does feat_1 have a monotone or threshold relationship with score that a non-linear model (isotonic or spline regression) could exploit better than the linear fit? The Spearman correlation (0.474) exceeds the Pearson correlation (0.411), and the middle-to-high tertile step for feat_1 is small.
- Are the negative trends of feat_3 and feat_6 real? The analysis says they need more rows or a multivariable model that adjusts for feat_1.
- Do the feat_2 × feat_4, feat_5 × feat_6, and feat_1 × feat_3 interactions hold with more data? If the feat_2 × feat_4 interaction is real, conditional slopes of score on feat_2 at low and high feat_4 would be needed.
- Do the tertile patterns for feat_5 (inverted U) and feat_1 and feat_3 hold beyond noise under a formal test such as Kruskal-Wallis or a permutation test?
- Does feat_1 keep its main effect after adjusting for the other five features?
- Would a paired comparison across the 50 CV folds show whether ridge's 0.34 RMSE gain over the baseline exceeds fold-to-fold noise?
- Would regularised or shallower models reduce the large train-test gaps seen for linear regression and random forest?
- Would a rank-based or robust regression give a similar feature 1–score relationship, given that the feature 1 outliers sit at both ends of its range?