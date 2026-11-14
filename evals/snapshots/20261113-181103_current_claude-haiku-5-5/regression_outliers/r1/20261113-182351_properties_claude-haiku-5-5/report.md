# Property Price Analysis: Drivers and Predictability of Price (600 Properties)

## Summary

- **Price is strongly right-skewed and has a high-price tail.** The mean is 289,164 against a median of 217,450 (skewness 6.44). Nineteen properties lie above the IQR high fence of 749,662.5. Without them, the mean is 248,826 and the skewness is 0.83.
- **Size is the dominant association with price.** The Spearman correlation of size_sqm with price is 0.887 (bootstrap 95% CI 0.857 to 0.911). Age has a weak negative association (rho −0.157). Rating shows no detectable association (rho 0.034, p = 0.40).
- **The size effect does not depend on age or rating.** The joint interaction F-test gives p = 0.326 on price and p = 0.588 on log price. No age band or rating level has a size slope that clearly differs from the others.
- **A linear model beats the mean baseline but explains little variance.** On the 120-property test set, test MAE falls from 165,645 to 102,395, but test R² is 0.189. Gradient boosting does not beat the linear model (test MAE 104,343, R² 0.079) and overfits heavily (train R² 0.915).
- **The 19 high-price outliers differ from the rest mainly in size.** Their median size is 169.3 sqm against 120.4 sqm (Holm-adjusted p = 0.0195, rank-biserial r = 0.37). Age and rating show no significant difference, but with 19 outliers the tests have low power.

## Data

- **Size:** 600 rows and 4 columns.
- **Target:** `price`, a continuous variable, so the task is regression. The currency is not stated in the profile.
- **Features:** three numeric features, `size_sqm`, `age_years` and `rating`. There are no categorical, date/time, identifier or free-text features.
- **Missing values:** none in any column.

## Findings

### 1. Price distribution and group differences (eda_1)

Price is strongly right-skewed. Summary statistics:

| Statistic | Value |
|---|---|
| Mean | 289,164 |
| Median | 217,450 |
| Std | 322,321 |
| Q1 / Q3 | 119,225 / 371,400 |
| Min / Max | 44,100 / 4,130,400 |
| Skewness | 6.44 |

By the 1.5 × IQR rule, the fences are −259,037.5 (low) and 749,662.5 (high). There are 19 outliers, all above the high fence and none below the low fence.

![Histogram of price, 50 bins, counts of properties](tasks/eda_1/charts/price_histogram.png)

**By rating (1 to 5).** The mean exceeds the median at every rating level.

| Rating | Median | Mean | n |
|---|---|---|---|
| 1 | 237,100 | 286,769 | 109 |
| 2 | 184,150 | 250,008 | 112 |
| 3 | 204,600 | 291,622 | 118 |
| 4 | 217,200 | 253,302 | 127 |
| 5 | 227,200 | 355,663 | 134 |

**By size_sqm quartile band.** Median and mean both rise with each band.

| Band | Median | Mean | n |
|---|---|---|---|
| Q1 (lowest) | 94,650 | 106,167 | 150 |
| Q2 | 160,200 | 202,297 | 150 |
| Q3 | 265,000 | 315,489 | 150 |
| Q4 (highest) | 452,900 | 532,703 | 150 |

**By age_years quartile band.** The pattern is non-monotone. Medians rise from Q1 to Q2, fall to Q3, then edge up in Q4. Price does not simply fall with age.

| Band | Median | Mean | n |
|---|---|---|---|
| Q1 (lowest) | 237,600 | 317,557 | 150 |
| Q2 | 263,650 | 309,303 | 150 |
| Q3 | 187,800 | 251,963 | 150 |
| Q4 (highest) | 205,000 | 277,834 | 150 |

### 2. Feature associations and effect sizes (stat_1, partial)

**Spearman correlations with price** (bootstrap 95% CIs, n = 600):

- `size_sqm`: rho = 0.887 [0.857, 0.911], p = 5.8e-203. Strong positive association.
- `age_years`: rho = −0.157 [−0.233, −0.083], p = 0.00011. Weak but significant negative association.
- `rating`: rho = 0.034 [−0.047, 0.115], p = 0.40. No significant association.

**Rating (Kruskal-Wallis across levels 1 to 5).** H = 3.28, p = 0.51, epsilon² = −0.001. A negative epsilon² is reported as zero. This indicates no detectable effect; it does not establish a zero effect.

**Rating, pairwise Mann-Whitney with Holm correction.** All 10 pairs have p_holm = 1.0, so no pair differs. The stat_1 report printed only three of these values. The full table below uses the raw and Holm p-values recorded in the stat_2 task.

| Pair | Median diff | Raw p | Holm p |
|---|---|---|---|
| 1 vs 2 | 52,950 | 0.456 | 1.0 |
| 1 vs 3 | 32,500 | 0.882 | 1.0 |
| 1 vs 4 | 19,900 | 0.479 | 1.0 |
| 1 vs 5 | 9,900 | 0.474 | 1.0 |
| 2 vs 3 | −20,450 | 0.516 | 1.0 |
| 2 vs 4 | −33,050 | 0.963 | 1.0 |
| 2 vs 5 | −43,050 | 0.103 | 1.0 |
| 3 vs 4 | −12,600 | 0.624 | 1.0 |
| 3 vs 5 | −22,600 | 0.332 | 1.0 |
| 4 vs 5 | −10,000 | 0.150 | 1.0 |

**Age band (Kruskal-Wallis across quartile bands).** H = 18.83, k = 4, p = 0.0003, epsilon² = 0.027. This is a small effect.

**Age band, pairwise Mann-Whitney with Holm correction.** All six pairs are shown below, with raw and Holm p-values from the stat_2 task's recorded facts. The Q2 vs Q3 contrast is significant after Holm correction.

| Pair | Median diff | Raw p | Holm p |
|---|---|---|---|
| Q1 vs Q2 | −26,050 | 0.669 | 0.669 |
| Q1 vs Q3 | 49,800 | 0.00055 | 0.0033 |
| Q1 vs Q4 | 32,600 | 0.0081 | 0.0325 |
| Q2 vs Q3 | 75,850 | 0.00088 | 0.0044 |
| Q2 vs Q4 | 58,650 | 0.0113 | 0.0340 |
| Q3 vs Q4 | −17,200 | 0.306 | 0.612 |

The largest contrast, Q2 minus Q3, has a median difference of 75,850 with a bootstrap 95% CI of 27,786 to 117,552 (n = 150 per band). It is significant after Holm correction (p_holm = 0.0044). Q1 vs Q2 and Q3 vs Q4 are not significant.

![Boxplot of price per age_years quartile band (n=150 each; whiskers exclude outlier points)](tasks/stat_1/charts/price_by_age_band_boxplot.png)

### 3. Does age or rating change the size effect? (stat_2)

**Interaction tests.** Neither age nor rating detectably changes the size slope.

- Joint F-test of the three pairwise interactions on price: F = 1.15, df = 3, p = 0.326.
- Same test on log price: F = 0.64, p = 0.588.

**Full OLS model of price** (size, age, rating and pairwise interactions):

- `size_sqm` main slope: 2,581 per sqm (95% CI 1,198 to 3,963, p = 0.0003).
- Size × age interaction: −6.1 (CI −33.8 to 21.6, p = 0.666).
- Size × rating interaction: 264 (CI −59 to 588, p = 0.109).

Neither interaction is significant.

**Size slope within age bands** (OLS, price per sqm):

- Q1: 3,446 (CI 2,766 to 4,125, n = 150)
- Q2: 3,048 (CI 2,178 to 3,917, n = 150)
- Q3: 3,075 (CI 2,259 to 3,892, n = 150)
- Q4: 3,344 (CI 2,126 to 4,562, n = 150)

All slopes are positive and their intervals overlap. No band shows a distinct size effect.

**Size slope within rating levels** (OLS, price per sqm):

- Rating 1: 3,222 (CI 2,395 to 4,049, n = 109)
- Rating 2: 2,642 (CI 2,254 to 3,030, n = 112)
- Rating 3: 3,088 (CI 1,983 to 4,193, n = 118)
- Rating 4: 2,633 (CI 2,201 to 3,064, n = 127)
- Rating 5: 4,343 (CI 2,761 to 5,925, n = 134)

All slopes are positive and overlap. Rating 5 has the largest point estimate and the widest interval, so no rating level is shown to differ.

![OLS slope of price on size_sqm with 95% CI, by age_years quartile band (left) and by rating level (right)](tasks/stat_2/charts/size_slope_by_group.png)

The age-band price differences in section 2 concern price levels, not the size slope. The slope check shows that the Q2 vs Q3 contrast does not indicate that age changes the size effect.

### 4. Predictive models on a fixed split (ml_1, ml_2)

The test set has 120 properties and the training set has 480.

**Mean baseline and linear regression (ml_1):**

| Model | Test MAE | Test RMSE | Test R² |
|---|---|---|---|
| Mean baseline | 165,645 | 303,756 | — |
| Linear regression | 102,395 | 273,535 | 0.189 |

The linear model's test MAE is lower than the baseline's. It explains little of the test variance: train R² is 0.270 and test R² is 0.189.

5-fold cross-validated R² on the training set averages 0.346 (SD 0.180), ranging from 0.129 to 0.600. The fit is unstable across folds. The CV average (0.346) is well above the test R² (0.189); the findings do not explain this gap.

![Test-set mean absolute error of the mean-prediction baseline and the linear regression on the 120 test properties](tasks/ml_1/charts/ml1_mae_comparison.png)

**Feature importance in the linear model.** Ranked by standardized coefficient (raw coefficient × training SD):

1. `size_sqm`: about 165,940 per SD
2. `age_years`: about −20,533 per SD (negative)
3. `rating`: about 18,640 per SD

The earlier raw-coefficient ranking, which put rating first, was an artefact of scale and is withdrawn. The stored `feature_ranking` field still reads "abs_coefficient", which conflicts with this withdrawn ranking. The rating coefficient is conditional on size and age; rating has no marginal association with price (section 2), so the coefficient is not evidence of a strong rating effect.

**Gradient boosting versus linear regression (ml_2).** On the same 120-property test split:

| Model | Test MAE | Test RMSE | Test R² |
|---|---|---|---|
| Mean baseline | 165,645 | 303,756 | 0.0 |
| Linear regression | 102,395 | 273,535 | 0.189 |
| Gradient boosting | 104,343 | 291,489 | 0.079 |

Gradient boosting does not beat the linear model on this split. Both models beat the mean baseline on MAE and RMSE. Gradient boosting overfits: train R² is 0.915 against test R² of 0.079.

![Test-set mean absolute error of the mean baseline, linear regression and gradient boosting on the 120 test properties](tasks/ml_2/charts/ml2_mae_comparison.png)

**Permutation importance (test set, 30 repeats, mean drop in R²):**

- `size_sqm`: 0.403 (SD 0.101)
- `age_years`: −0.020 (SD 0.042), no positive effect when shuffled
- `rating`: −0.035 (SD 0.011), no positive effect when shuffled

Size is the only feature with a positive out-of-sample contribution under this model. The linear model's standardized coefficients also rank size first.

### 5. The 19 high-price outliers (eda_2 and stat_3)

**Descriptive profile** (outliers above 749,662.5, n = 19, vs the other 581 properties):

- **Size:** median 169.3 sqm vs 120.4 sqm. 52.6% of outliers exceed the rest's 75th percentile of size (161.4 sqm), against 25.0% of the rest.
- **Age:** median 27.9 years vs 30.3 years. 52.6% of outliers have age inside the rest's IQR (16.9 to 44.0 years).
- **Rating:** median 3.0 in both groups. Outliers have a larger share at rating 3 (26.3% vs 19.4%) and rating 5 (31.6% vs 22.0%), and a smaller share at rating 4 (15.8% vs 21.3%). These shares are descriptive and are not tested for significance. They should not be read as a skew toward higher ratings, given the null rating result in section 2.

![Boxplot of size_sqm for the 19 price outliers (above 749662.5) and the other 581 properties](tasks/eda_2/charts/eda2_outlier_size_sqm.png)

**Effect on price summary** (eda_2): with all 600 properties the mean is 289,164 and the median is 217,450. Without the 19 outliers (n = 581), the mean is 248,826 and the median is 210,500. Skewness falls from 6.44 to 0.83.

**Formal tests** (Mann-Whitney, two-sided, Holm across the three features):

- **Size:** U = 7,543, raw p = 0.0065, Holm p = 0.0195, significant at 0.05. Rank-biserial r = 0.37 and P(outlier > rest) = 0.68, a medium-sized effect per the finding.
- **Age:** U = 5,060.5, raw p = 0.537, Holm p = 0.822. Rank-biserial r = −0.08, P = 0.46. Not significant.
- **Rating:** U = 6,118.5, raw p = 0.411, Holm p = 0.822. Rank-biserial r = 0.11, P = 0.55. Not significant. Medians coincide because rating has few discrete values with heavy ties. Among outliers, 6 of 19 (31.6%) are at rating 5, with a Wilson 95% CI of 15.4% to 54.0%.

![Boxplots of size_sqm, age_years and rating for the 19 high-price outliers vs the other 581 properties](tasks/stat_3/charts/stat3_mwu_boxplots.png)

## Limitations

- **Association, not causation.** All results are associations in one cross-sectional sample of 600 properties. The outlier comparison describes a segment selected by price above the IQR fence. No causal link between size and price is established.
- **Feature set.** Only three numeric features are available. Unmeasured factors may drive price, which limits the predictive results.
- **Model performance is modest and unstable.** Linear test R² is 0.189 on 120 properties. Cross-validated R² on the training set averages 0.346 with a fold range of 0.129 to 0.600. Gradient boosting overfits. Rating is treated as numeric in the linear model, which has not been checked against a categorical encoding.
- **Skewed target.** Price is strongly right-skewed. Group comparisons and correlations were run on raw price; a log-transformed analysis was run only for the interaction test (section 3), and the other results were not checked on the log scale.
- **Outlier analysis is small and descriptive.** With n = 19, the age and rating tests have low power. Non-significance does not show absence of a difference. No confidence intervals were computed for the rank-biserial effects or P(outlier > rest). The shares in section 5 are descriptive.
- **Unresolved review issue (stat_1, status partial).** The stat_1 report did not print full Holm p-values for several pairs. The lead's review asked for them. The values in section 2 are taken from recorded facts in the stat_2 task: all seven rating pairs not printed by stat_1 (1 vs 5, 2 vs 3, 2 vs 4, 2 vs 5, 3 vs 4, 3 vs 5, 4 vs 5) have p_holm = 1.0, and the age pairs Q2 vs Q3 (p_holm 0.0044), Q1 vs Q4 (0.0325), Q2 vs Q4 (0.0340) and Q3 vs Q4 (0.612) are reported above. The stat_1 finding remains partial, and this review issue is addressed only through those recorded facts. The Q2 vs Q3 contrast is significant after Holm correction; its bootstrap CI (27,786 to 117,552) is wide.
- **Other task-level notes.**
  - The stat_2 slopes for rating 5 (CI 2,761 to 5,925, n = 134) are imprecise and may be driven by a few large-price homes. This was raised but not tested.
  - The linear model's `feature_ranking` field still reads "abs_coefficient" despite the withdrawn raw-coefficient ranking.

## Open questions

- Does the size_sqm effect on price hold after controlling for age_years and rating in a formal model? (Partly addressed by the interaction model, but no adjusted slope was tested on log price or with a rank-based method.)
- Is the non-monotone age pattern (Q2 peak, Q3 drop) driven by size or rating mix across age bands?
- Would a log transform of price, or a rank-based model, change the age-band and rating comparisons?
- Would a size_sqm-only model match the three-feature linear model on test R² and MAE?
- Would a regularised model or a larger sample reduce the gradient boosting overfit and allow a non-linear model to beat the linear baseline?
- Is the price–size relationship non-linear (for example, log price or a spline in size_sqm)?
- Why does the cross-validated R² (0.346) differ so much from the test R² (0.189), and what drives the wide fold-to-fold spread?
- Are the 19 high-price properties a distinct segment worth separate analysis? Are the size and rating results robust to a different high-price threshold, such as a percentile of price rather than the IQR fence?
- Do the outlier size differences persist after controlling for age and rating, and what are bootstrap CIs for the outlier effect sizes?
- Is rating truly numeric or ordinal, and does a categorical encoding change the results?