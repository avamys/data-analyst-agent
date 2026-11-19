# Price Drivers in a 600-Listing Dataset: Distribution, Ratings, Size, Age and Prediction

## Summary

- **Size is the clearest driver of price.** Price rises with size_sqm (Spearman rho = 0.887, 95% CI 0.869 to 0.903, n = 600). In the three-feature OLS, each additional sqm is associated with about 3,219 more in price (95% CI 2,768 to 3,669). The three features together explain about 26% of price variance in-sample (R² = 0.256).
- **Age has a small but significant negative association with price.** The unadjusted Spearman rho is -0.157 (p = 0.00011). It stays significant after controlling for size and rating, and in log-price and robust models. In the log-price OLS, price falls about 0.64% per year of age (95% CI -0.83% to -0.46%).
- **Rating shows no detectable association with price.** The Kruskal-Wallis test gives p = 0.51, and no pairwise comparison is significant after Holm correction. The size slope also does not vary detectably with rating or with age.
- **Prediction gains over a mean baseline are modest.** On a single 120-row test split, linear regression cuts test RMSE by about 10% and MAE by about 38% relative to the mean baseline, with test R² of 0.189. Gradient boosting overfits and does worse than the baseline on RMSE.
- **Price is heavily right-skewed, and nine extreme listings above 1,000,000 cannot be classed as genuine or erroneous from this data.** Their prices sit far above the size-price pattern of the other listings. Several results (OLS coefficients, R², mean-median gaps) are sensitive to them.

## Data

- **Size:** 600 rows × 4 columns.
- **Target:** price (regression).
- **Numeric features:** size_sqm, age_years, rating. Rating is integer-valued with few levels, so it is treated both as a numeric feature and as a grouping variable.
- **Categorical, date/time, and identifier or free-text features:** none.
- **Missing values:** none.

## Findings

### Price distribution

Price is strongly right-skewed. The mean is 289,164, the median is 217,450, the standard deviation is 322,321 and the skewness is 6.44. stat_1 reports a skewness of 6.42.

The top of the distribution is a long tail. The five highest listings are 4,130,400; 3,485,400; 2,628,000; 2,451,700 and 2,228,000. Nine listings (1.5%) exceed 1,000,000.

![Histogram of price, count of listings per bin](tasks/eda_1/charts/price_histogram.png)

### Price by rating

Mean and median price do not move together across rating levels, and there is no clear monotone pattern:

| Rating | Count | Mean | Median |
|---|---|---|---|
| 1 | 109 | 286,769 | 237,100 |
| 2 | 112 | 250,008 | 184,150 |
| 3 | 118 | 291,622 | 204,600 |
| 4 | 127 | 253,302 | 217,200 |
| 5 | 134 | 355,663 | 227,200 |

Rating 5 has the highest mean but not the highest median.

The rating tests (stat_1) found:
- Spearman correlation of price with rating is 0.034 (95% CI -0.046 to 0.114, p = 0.40).
- Kruskal-Wallis across rating levels gives H = 3.28, df = 4, p = 0.51, with epsilon-squared = 0.005 (negligible).
- None of the ten pairwise Mann-Whitney comparisons is significant after Holm correction; all Holm-adjusted p-values equal 1.0.
- The largest absolute rank-biserial effect is 0.121 (rating 2 vs 5, raw p = 0.103). For the first pair, 1 vs 2, the rank-biserial is -0.058 (raw p = 0.456).
- stat_3 recomputed the same ten tests with the opposite ordering convention, so it reports 1 vs 2 as +0.058 and 2 vs 5 as -0.121. The magnitudes agree; the signs are reversed by convention.

![Boxplot of price for each rating level; whiskers and outlier points show the spread and extreme listings](tasks/stat_1/charts/price_by_rating_box.png)

### Price by size and age

**Size.** Price rises steeply with size_sqm (Pearson 0.498). Median and mean price by size quintile:

| Size quintile | Median | Mean |
|---|---|---|
| Q1 | 90,850 | 102,376 |
| Q2 | 137,950 | 154,502 |
| Q3 | 215,900 | 249,432 |
| Q4 | 327,150 | 391,283 |
| Q5 | 474,000 | 548,226 |

Each quintile has 120 listings. The step between adjacent quintiles grows across the range, for both medians and means, so the relationship appears to accelerate rather than flatten. This is read from the quintile summaries; the scatter itself was not measured.

**Age.** The linear correlation with price is -0.077, close to zero. Mean price by age quintile is 329,558, 292,717, 305,690, 264,858 and 253,106. Medians are 240,150, 263,400, 195,200, 200,550 and 202,000. The mean-median gap is large in most quintiles, ranging from 51,106 to 110,490. It is largest in age Q1 (89,408) and Q3 (110,490) and smallest in Q2 (29,317). Outliers are a likely cause of the gap but this is not confirmed.

![Scatter of price against size_sqm (left) and against age_years (right)](tasks/eda_1/charts/price_scatter.png)

### Size and age associations, and the regression model

- **Size:** Spearman rho = 0.887 (95% CI 0.869 to 0.903, p < 0.001, n = 600). This is the strongest rank correlation of the three features.
- **Age:** Spearman rho = -0.157 (95% CI -0.234 to -0.078, p = 0.00011, n = 600). The squared rho, about 2.5% of rank variance, indicates a small effect.
- **Three-feature OLS of price on size_sqm, age_years and rating** (R² = 0.256, adjusted R² = 0.252):

| Term | Coefficient | 95% CI | p |
|---|---|---|---|
| size_sqm (per sqm) | 3,219 | 2,768 to 3,669 | < 0.001 |
| age_years (per year) | -1,470 | -2,825 to -115 | 0.034 |
| rating (per level) | 11,476 | -4,310 to 27,262 | 0.154 |
| Intercept | -79,317 | -164,870 to 6,236 | 0.069 |

The age and size coefficients are the only ones significant at 0.05. These estimates are sensitive to the skew and the extreme listings and are not robust estimates.

### Interactions: does size's effect depend on rating or age?

Neither interaction is statistically significant:
- **Size × rating:** F = 2.49, p = 0.115. The interaction coefficient is 260 per rating level (95% CI -64 to 583).
- **Size × age:** F = 0.13, p = 0.715. The interaction coefficient is -5.1 per year (95% CI -32.7 to 22.5).

The full interaction model has R² = 0.259 (adjusted 0.253). Its main effects match the three-feature model: size 3,220 per sqm (CI 2,770 to 3,671); rating 10,935 per level (CI -4,861 to 26,731, p = 0.174); age -1,482 per year (CI -2,836 to -128, p = 0.032).

Size slopes within each rating level:

| Rating | Slope per sqm | 95% CI |
|---|---|---|
| 1 | 3,222 | 2,395 to 4,049 |
| 2 | 2,642 | 2,254 to 3,030 |
| 3 | 3,088 | 1,983 to 4,193 |
| 4 | 2,633 | 2,201 to 3,064 |
| 5 | 4,343 | 2,761 to 5,925 |

Size slopes within age terciles: T1 (age 0.1 to 21.3) 3,158 (CI 2,631 to 3,685); T2 (age 21.4 to 38.2) 3,395 (CI 2,518 to 4,272); T3 (age 38.6 to 59.8) 3,143 (CI 2,231 to 4,055).

The confidence intervals overlap across all levels, so the variation is consistent with noise. The analysis does not split the effect by subgroup and summarises size as one common slope of about 3,220 per sqm. This conclusion assumes a linear size effect, which eda_1 suggested is not the case. Neither the stratified nor the pooled slopes were tested under a nonlinear specification in this task.

![OLS slope of price on size_sqm within each rating level and within each age tercile, with 95% CI](tasks/stat_2/charts/stat2_size_slopes.png)

### Age after controlling for size: log, robust and nonlinear models

Age stays significant in every specification tested. Each model includes centred size, size squared, age and rating.

- **Log-price OLS:** age coefficient -0.00646 per year (95% CI -0.00829 to -0.00464, p = 8.8e-12). This is about -0.64% per year (95% CI -0.83% to -0.46%).
- **Log-price Huber robust regression:** age coefficient -0.00653 per year (95% CI -0.00781 to -0.00526, p = 7.8e-24). This is about -0.65% per year, close to the log-OLS estimate.
- **Raw-price OLS:** age coefficient -1,387 per year (95% CI -2,733 to -42, p = 0.043). The interval is wide and the p-value is near 0.05.
- **Raw-price Huber robust regression:** age coefficient -1,478 per year (95% CI -1,775 to -1,182, p = 1.3e-22).

On the squared size term the models disagree. In the log-price OLS it is not significant (p = 0.45) and in the log-price robust model it is not significant either (p = 0.51). In the raw-price OLS it is significant (p = 0.0016), and in the raw-price robust model it is significant (p = 1.6e-33). The nonlinear size term therefore depends on the price scale. The analysis does not resolve this.

### Predictive accuracy

Evaluation uses a fixed 80/20 split (480 training rows, 120 test rows, seed 42).

| Model | Test RMSE | Test MAE | Test R² |
|---|---|---|---|
| Mean baseline | 303,756 | 165,645 | about 0 |
| Linear regression | 273,535 | 102,395 | 0.189 |
| Gradient boosting | 342,792 | 122,790 | -0.27 |

- Linear regression lowers RMSE by about 10% and MAE by about 38% relative to the baseline.
- Gradient boosting has training R² of 0.92 against test R² of -0.27, so it overfits. Its test RMSE is worse than the mean baseline's.
- Linear regression explains about 19% of test variance. Most price variation therefore comes from factors not in the three numeric features.

Permutation importance for linear regression (increase in test MAE when a feature is shuffled):
- size_sqm: 111,845 (sd 9,066)
- age_years: 8,133 (sd 1,567)
- rating: 1,305 (sd 1,502), within about one sd of zero

The coefficient-magnitude ranking for linear regression puts rating first (13,363), then size (3,315), then age (1,230). This ranking compares raw coefficients on features with different scales and disagrees with the permutation ranking. Gradient boosting importances are size 0.578, age 0.380 and rating 0.042.

![Test-set RMSE of the mean baseline, linear regression and gradient boosting on the fixed 80/20 split](tasks/ml_1/charts/ml1_test_rmse_by_model.png)

### The nine listings above 1,000,000

- **Size, age and rating versus the other 591 listings:** the nine have a higher mean size (147.64 vs 116.8), but the difference is not significant (Mann-Whitney p = 0.069). Age (29.82 vs 30.36, p = 0.93) and rating (3.56 vs 3.1, p = 0.31) show no difference.
- **Price per sqm:** the median is 15,994 for the nine and 1,984 for the other 591. The minimum for the nine is 8,023, and the maximum among the other 591 is 15,587. Only 4 of the other 591 (0.68%) exceed 8,000 per sqm. This comparison selects on price above 1,000,000, so the gap is partly built into the grouping.
- **Log-price residuals:** log price was fitted on size_sqm using the 591 other listings (residual SD 0.31). The nine have a mean residual of +1.92, a minimum of +1.06 and a maximum of +2.40. They lie consistently above the line. Including them lowers the log-price and size correlation from 0.887 to 0.844 and barely changes the slope (0.01232 with all 600 vs 0.01199 with the 591).

The data cannot establish whether the nine are data errors or a genuine premium segment. Their consistent upward offset is equally consistent with a unit, currency or listing-type error. They should be checked against source records before being kept or dropped.

![Price against size_sqm on a log price scale, with the nine listings above 1,000,000 in red (left) and without them (right)](tasks/eda_2/charts/eda2_price_vs_size_log.png)

## Limitations

- **Skew and outliers.** Price is heavily right-skewed, and nine listings above 1,000,000 are strongly above the size-price pattern. The raw-scale OLS coefficients, R² values and mean-median gaps are sensitive to these listings. Robustness was tested only for the age effect (in the log and Huber models above); the raw-scale size and rating coefficients were not re-estimated without the nine.
- **Mean-median gaps.** Outliers are a likely but unconfirmed cause of the large mean-median gaps in the age quintiles.
- **Linearity.** The size-price relationship appears to accelerate, and the squared size term is significant on the raw scale but not on the log scale. The linear slopes in the interaction analysis may therefore be misspecified.
- **Power.** Rating groups have 109 to 134 listings. The size × rating interaction (p = 0.115) is not significant, and the study does not show whether it is absent or undetected.
- **Predictive results.** These come from a single 120-row test split. Gradient boosting was not tuned, and cross-validation was not run. The three-feature models explain a limited share of price variance.
- **Feature-importance ranking.** The coefficient ranking and the permutation ranking disagree on rating. Neither was adjusted for feature scale.
- **Skewness value.** eda_1 reports 6.44 and stat_1 reports 6.42. Both are cited as reported.
- **Pairwise rating sign convention.** stat_1 and stat_3 report the same rank-biserial magnitudes with opposite signs, reflecting the ordering convention.
- **Unresolved review issue, stat_1 (corrected in this report).** The original final finding called size_sqm "the only feature" with a significant association. The reviewer required this to be corrected: age_years is significant (Spearman rho -0.157, p = 0.00011; OLS p = 0.034). Size has the largest and clearest association, and age a small but significant negative one. The pairwise rank-biserial range has been restated to cite only the supported maximum of 0.121 (2 vs 5) and the first pair's -0.058.
- **Unresolved review issue, eda_2 (partial status; not resolved).** Two objections stand:
  1. The brief required each of the nine listings to be reported with size_sqm, age_years and rating. This report does not list the nine individually, because the per-listing values could not be cited from the accepted facts. Age and rating per listing were not verified. The per-listing values are in the eda2_hi_tuples record and should be read from there.
  2. The first finding about the nine listings' price and size pairs was uncited. It has therefore been removed from this report.
  The remaining eda_2 findings (group comparisons, price per sqm, log residuals) are supported by the facts they name.
- **Failed tasks.** None.

## Open questions

- Are the nine listings above 1,000,000 data errors (currency, unit or listing type) or a genuine premium segment? What distinguishes them in age and rating, once those values are checked per listing?
- Does a log transform of price make the size relationship close to linear and reduce the influence of the extreme listings?
- Do the nine listings drive the raw-price age coefficient and the mean-median gaps? Does the age-quintile mean-median gap shrink when they are removed?
- Is the nonlinear size term needed, and how much does it change the age estimate? Does a Box-Cox or quantile regression of price reproduce the log-scale age effect?
- Do the size interaction tests hold under a spline or squared size term, a log-price model, or an outlier-robust regression?
- Is the size × rating interaction (p = 0.115) detectable with more data, or is it absent?
- Is the price-by-rating pattern significant once the group sizes are considered? The current tests find no difference, but the analysis did not ask whether the study had enough power to detect one.
- Would tuning gradient boosting (depth, learning rate, minimum leaf size) or using cross-validation produce a model that beats linear regression?
- Which omitted factors (location or other columns) would add the most predictive power beyond the three numeric features?