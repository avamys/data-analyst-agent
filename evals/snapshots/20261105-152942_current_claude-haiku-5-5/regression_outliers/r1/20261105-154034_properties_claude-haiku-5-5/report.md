# Price Determinants in a 600-Listing Dataset: Distribution, Associations, Interactions and Predictive Models (Target: price)

## Summary

- **Size is the dominant driver of price.** Size_sqm has a strong monotone association with price (Spearman 0.89, 95% CI 0.87 to 0.90). Each additional square metre is associated with a 1.24% higher price (95% CI 1.18% to 1.30%). Size alone explains R² 0.71 of log price.
- **Age has a small, significant negative association that survives adjustment.** After adjusting for size and rating, each year is associated with a 0.64% lower price (95% CI −0.82% to −0.46%, p = 1e-11). Rating shows no detectable association with price (adjusted +0.81% per level, 95% CI −1.31% to 2.97%, p = 0.46).
- **Predictive gains over a mean baseline are modest.** On a single 120-row test split, the best model by MAE is linear regression on log price (MAE 91,530 versus 173,453 for the mean baseline). Under repeated 5-fold cross-validation, linear regression on log price has the lowest mean MAE (82,881) and beats the log-target random forest in all 25 folds.
- **Size-by-age interaction is not supported; size-by-rating is undetected but not ruled out.** The size-by-age interaction is null for linear (p = 0.59), log (p = 0.70) and spline (p = 0.88) size terms. The size-by-rating interaction is null (p = 0.28 linear, 0.64 log, 0.78 spline), but its confidence intervals are wide enough to include moderate effects.

## Data

- 600 rows × 4 columns.
- Target: price (regression).
- Numeric features: size_sqm, age_years, rating. Rating takes five integer values.
- Categorical features, date/time features, and id or free-text columns: none.
- Missing values: none. A missingness analysis was therefore not part of the work.

## Findings

### Price distribution and bin-level patterns

Price is strongly right-skewed. The mean is 289,164 and the median is 217,450. Skewness is 6.44 on the linear scale and 0.35 on the log scale, so a log scale is appropriate for modelling and display. Price quartiles are 119,225 (Q1), 217,450 (median) and 371,400 (Q3), with SD 322,321 and range 44,100 to 4,130,400.

![Distribution of price: linear and log10 scale histograms](tasks/eda_1/charts/price_histogram.png)

**By size_sqm.** Size shows the clearest bin-level gradient. Mean price rises from 106,167 in the smallest size quartile (30.1 to 72.8 sqm) to 202,297 (Q2), 315,489 (Q3) and 532,703 in the largest quartile (163.1 to 199.7 sqm). Median price rises from 94,650 to 160,200, 265,000 and 452,900.

**By age_years.** There is no clear monotone pattern. Median price is 237,600 in the youngest quartile (0.1 to 16.8 years), 263,650 in Q2, then 187,800 in Q3 and 205,000 in the oldest quartile (44.0 to 59.8 years). Means follow a similar weak pattern.

**By rating.** Mean and median price do not rise steadily with rating. Rating 5 has the highest mean (355,663, n = 134) but a median (227,200) only slightly above rating 4 (217,200). Rating 2 has the lowest median (184,150, n = 112). Group sizes range from 109 to 134.

![Scatter of price against size_sqm, points coloured by rating level](tasks/eda_1/charts/price_vs_size_by_rating.png)

**Correlations with price.**

| Feature | Pearson | Spearman |
|---|---|---|
| size_sqm | 0.50 | 0.89 |
| age_years | −0.08 | −0.16 |
| rating | 0.07 | 0.03 |

The size relationship is strongly monotone but nonlinear, so the linear measure understates it.

### Significance and effect sizes

**Size_sqm.** Spearman rho is 0.887 (95% CI 0.869 to 0.903, p ≈ 6e-203, n = 600). The OLS slope on log price is 0.0123 per sqm, which corresponds to 1.24% per sqm (95% CI 1.18% to 1.30%, p ≈ 5e-164). R² is 0.71.

**Age_years.** Spearman rho is −0.157 (95% CI −0.234 to −0.078, p = 0.00011). Univariately, each year is associated with −0.65% in price (95% CI −0.99% to −0.30%, p = 0.0003, R² 0.02). After adjusting for size and rating, the effect is −0.64% per year (95% CI −0.82% to −0.46%, p = 1e-11). The age association is therefore not explained by size.

**Rating.** No detectable association. Spearman rho is 0.034 (95% CI −0.046 to 0.114, p = 0.40). Kruskal-Wallis across the five levels gives H = 3.28 (df 4, p = 0.51), with epsilon-squared effectively zero. The univariate OLS slope is +2.23% per level (95% CI −1.88% to 6.52%, p = 0.29). Adjusted for size and age, it is +0.81% per level (95% CI −1.31% to 2.97%, p = 0.46).

**Joint model.** The multiple OLS of log price on size, age and rating has R² 0.73.

### Price per square metre and extreme listings

**Extreme listings.** The six listings at or above the 99th percentile (threshold 1,591,094) average 154 sqm, are 33.8 years old on average, and have mean rating 4.0. Their mean price per sqm is 18,086 (median 17,696), against an all-listing median price per sqm of 1,999. Excluding them raises the size-price Pearson correlation from 0.50 to 0.75 (n = 594). This is still below the Spearman of 0.89, so the extreme listings explain part of the Pearson–Spearman gap, not all of it.

**Top 5% listings.** The 30 listings in the top 5% of price average 160 sqm and 25.7 years old, against 117 sqm and 30.4 years for all listings. Their mean price per sqm is 8,375 (median 4,535), against 2,017 (median 1,956) for the rest. The extremes are therefore concentrated in price per sqm as well as in price.

![Scatter of log10 price against size_sqm; top 1% price listings in red](tasks/eda_2/charts/log_price_vs_size.png)

**Price per sqm by age quartile.** Median price per sqm is 2,300 (youngest quartile), 2,203, 1,748 and 1,809 (oldest quartile). Means are 2,617, 2,473, 2,091 and 2,160. The decline is modest and not strictly monotone. This is unadjusted for size.

**Price per sqm by rating.** Medians are 2,002 (rating 1), 2,028, 2,015, 1,902 and 2,042 (rating 5), with no clear pattern. The rating 5 mean (2,654) is well above its median.

**Rating 5 check.** On all listings, the rating 5 mean-minus-median gap is 612. After excluding the top 5% of price listings, the rating 5 mean is 2,039 and the median is 1,971, a gap of 67 (n = 122). The gap stays positive, but after exclusion the mean-minus-median gaps across ratings range from 19 to 79, so rating 5 is not distinctive. Medians after exclusion range from 1,872 (rating 4, n = 123) to 2,017 (rating 2, n = 110). Means range from 1,951 to 2,040. No formal test of rating differences in price per sqm was run, so this pattern is described, not shown to be absent.

![Mean and median price per sqm by rating level, on all listings and after excluding the top 5% of price listings](tasks/eda_3/charts/ppsqm_rating_mean_median.png)

### Interactions

**Linear size-by-age and size-by-rating.** The size × age coefficient on log price is 1.0e-5 (95% CI −2.7e-5 to 4.7e-5, p = 0.59). The size × rating coefficient is 2.4e-4 (95% CI −1.9e-4 to 6.8e-4, p = 0.28). The rating interaction is not detected, but it is not confirmed as null. The upper bound corresponds to a slope increase of about 0.07% per rating point, against a size slope near 0.012.

**Within-group size slopes (linear model).**

- By age (split at median 30.1 years, 300 listings each): low age 0.01187 per sqm (95% CI 0.01105 to 0.01269), about 12.6% per 10 sqm; high age 0.01267 (95% CI 0.01176 to 0.01357), about 13.5% per 10 sqm. The CIs overlap.
- By rating: slopes are 0.01279 (rating 1, n = 109), 0.01154 (rating 2, n = 112), 0.01162 (rating 3, n = 118), 0.01226 (rating 4, n = 127) and 0.01330 (rating 5, n = 134), about 12.2% to 14.2% per 10 sqm. All CIs overlap, and the upward trend is not statistically supported.

**Spline and log size terms.** The results below are from models that replace the linear size term.

- Spline (natural cubic, centred basis) nested F-tests: size-by-age block F = 0.22 (df 3, p = 0.88); size-by-rating block F = 0.36 (df 3, p = 0.78). The centred spline design has rank 12 with 15 columns, so the individual spline interaction terms are not identified and are not reported (see Limitations).
- Log size model: log-size × age coefficient 0.00075 (95% CI −0.0031 to 0.0046, p = 0.70); log-size × rating coefficient 0.0110 (95% CI −0.035 to 0.057, p = 0.64). The rating CI is wide enough to include moderate effects.
- Spline within-group effect of +10 sqm (averaged over group rows): age low 12.8% (11.2% to 14.4%), age high 13.7% (12.1% to 15.2%). By rating: 12.6% (rating 1), 13.0% (2), 13.2% (3), 13.5% (4), 13.7% (5). The CIs overlap, and the rise across ratings is not statistically supported.
- Log-model within-group effect of +10 sqm, evaluated at group mean size: age low 9.7% (9.0% to 10.5%), age high 10.6% (9.8% to 11.5%); rating 1 11.1% (9.7% to 12.5%), rating 2 9.7% (8.6% to 10.8%), rating 3 9.7% (8.5% to 11.1%), rating 4 10.0% (8.9% to 11.0%), rating 5 10.7% (9.2% to 12.2%).

The log-model estimates are lower than the spline estimates. The two are different estimands: the log estimate is evaluated at group mean size, and the spline estimate averages over group rows. The gap is not yet explained and should not be read as a model disagreement until both are put on a common estimand.

**Common-estimand comparison on the same rows (bootstrap 95% CIs, per +10 sqm).**

- High-age listings (n = 284): spline 35,332 (25,247 to 50,325) versus log 25,440 (22,632 to 28,618). The gap is 9,892 (CI 379 to 23,624), which excludes zero.
- Low-age listings (n = 281): spline 31,372 (23,460 to 40,120) versus log 29,486 (26,481 to 32,328). The gap is 1,885 (CI −6,138 to 10,360), which includes zero.
- By rating within high-age listings, the spline-minus-log gaps are 7,826 (rating 1), 8,864 (2), 10,289 (3), 12,420 (4) and 10,048 (5). Only the rating 3 and rating 4 gap CIs exclude zero. Within low-age listings, all rating-level gap CIs include zero.
- The log model's implied size elasticity is 1.14 for low-age and 1.22 for high-age listings. Its derivative-based average price change per 10 sqm over each group's size range is 29,445 (low age) and 25,366 (high age). These are not identical to the finite +10 sqm differences above.

The size-dependent slope in the log model does not account for the high-age gap. The log model already includes that slope and still gives a smaller high-age effect than the spline. The cause is not established. The spline is fit on the price scale and is sensitive to the extreme high-price listings, and the log model's back-transformed effects depend on the Duan smearing factor of 1.12.

![Mean price change for +10 sqm by age group (low/high) and rating level, both models on the same listings; bars are 95% bootstrap CIs](tasks/stat_4/charts/size_effects_by_group.png)

### Predictive models

**Protocol.** All models were evaluated on one fixed-seed (42) 80/20 split: 480 training rows and 120 test rows, stratified by rating, with features size_sqm, age_years and rating and target price.

**Single split (test set).**

| Model | MAE | RMSE | R² |
|---|---|---|---|
| Mean baseline | 173,453 | 323,395 | −0.01 |
| Linear regression, price | 111,189 | 282,184 | 0.23 |
| Linear regression, log price (back-transformed) | 91,530 | 284,744 | 0.22 |
| Random forest, price | 112,002 | 301,250 | 0.13 |
| Random forest, log price | 97,512 | 293,265 | 0.17 |

Every model beats the mean baseline on MAE and RMSE, but gains are modest. Linear regression on log price has the lowest test MAE, though its RMSE and R² are slightly worse than raw-price linear regression. Among raw-price models, linear regression and the random forest are essentially tied on MAE (111,189 versus 112,002).

![Test-set MAE of each model on the shared 120-row split; lower is better](tasks/ml_2/charts/ml2_model_mae.png)

The random forest (300 trees, min_samples_leaf = 3) overfits: train R² is 0.53 and test R² is 0.13. Log-target training improves all three test metrics for the forest but raises RMSE slightly for linear regression.

**Feature importance on the single split.** These measures are not all on the same model.

- Raw-price linear regression, permutation importance on test MAE: size_sqm about 113,752 (sd 9,422), age_years about 2,231 (sd 1,579), rating −173 (sd 914, indistinguishable from zero).
- Standardised linear coefficients (change in price per SD): size_sqm +162,648, age_years −19,706, rating +13,124. The rating coefficient is not reliably distinguishable from zero on this test set. The raw rating coefficient (9,269 per unit) is unit-dependent and is not comparable with the others.
- Random forest, permutation importance on test MAE: size_sqm about 113,655 (sd 8,777), age_years about 1,772 (sd 2,945), rating about −2,083 (sd 2,645). The forest's age signal is near zero, which conflicts with the linear model's age effect. Overfitting or nonlinearity of the forest may explain this, but that is untested.

**Repeated 5-fold cross-validation (5 repeats, 25 folds on all 600 rows).**

| Model | Mean MAE | SD of MAE across folds | Mean RMSE | Mean R² |
|---|---|---|---|---|
| Mean baseline | 173,561 | 21,527 | 303,370 | −0.03 |
| Linear regression, raw | 103,667 | 21,295 | 253,623 | 0.33 |
| Linear regression, log | 82,881 | 25,105 | 248,844 | 0.37 |
| Random forest, raw | 107,670 | 21,697 | 270,980 | 0.20 |
| Random forest, log | 89,360 | 24,573 | 254,552 | 0.33 |

Fold-to-fold SDs (21,295 to 25,105 for MAE; 112,026 to 128,176 for RMSE) are large relative to the gaps between the learned models, except that the raw random forest is clearly weakest on RMSE and R².

Paired per-fold MAE differences:

- Linear regression on log price versus random forest on log price: mean difference −6,479 (sd 2,262). The log linear model has lower MAE in 25 of 25 folds. This is the most reliable model gap in the study.
- Linear regression on raw price versus random forest on raw price: mean difference −4,003 (sd 6,472). It is lower in 17 of 25 folds. The gap is modest and not decisive.
- Log target versus raw target: linear regression log is 20,786 lower than linear regression raw (sd 5,995; lower in 25 of 25 folds). Random forest log is 18,309 lower than random forest raw (sd 7,944; lower in 25 of 25 folds). The log-target MAE gain is consistent across both families.

The t statistics on these differences (for example, t ≈ −14.3 for the log linear model versus log forest) are optimistic because folds share training data.

![Fold-level test MAE of each model across 25 repeated K-fold splits on all 600 rows](tasks/ml_3/charts/ml3_cv_mae.png)

## Limitations

- **Unresolved review issue: spline interaction coefficients are not identified.** The centred spline model has rank 12 with 15 columns (full_rank 12, full_ncol 15), so the per-basis interaction terms (b0 to b3) are linearly dependent. Their individual coefficients, CIs and p-values are not reported here. The spline interaction conclusions rest on the nested F-tests only: age F = 0.22 (df 3, p = 0.88) and rating F = 0.36 (df 3, p = 0.78). The spline refit's joint age test (p ≈ 1.6e-9) is not reliable because that design is also rank-deficient, and it is disregarded. The within-group spline and log effects are reported as they stand, subject to the estimand caveat below.
- **Linearity caveat for within-group slopes.** The linear within-group percentages assume a linear effect of size on log price. The size association is monotone but nonlinear, so the per-10-sqm percentages are averages over the size range, not constant effects.
- **Estimand mismatch.** The spline and log within-group effects differ in estimand (group-row averages versus effects at group mean size). The gap between them is unexplained. The common-estimand comparison narrows but does not resolve it.
- **Extreme listings.** The six top-1% listings and the top 5% more generally are concentrated in price per sqm. Whether they are data errors or genuine luxury properties is not established, and their effect on the spline fit and on the high-age gap has not been removed.
- **Smearing factor.** The log model's back-transformed effects depend on the Duan smearing factor of 1.12.
- **Rating interaction not resolved.** The rating interaction is undetected but its CIs allow moderate differences. Per-rating group estimates have n between 47 and 134, which is small for these comparisons.
- **Small test set.** The single-split comparisons use 120 test rows. The MAE values of linear regression (111,189) and the random forest (112,002) are within split noise. The cross-validation results are more stable but use overlapping training folds.
- **Untuned forest.** The random forest used a fixed configuration (300 trees, min_samples_leaf = 3) and was not tuned under cross-validation.
- **Price per sqm analyses are unadjusted.** The age and rating patterns in price per sqm are not adjusted for size. No formal test of rating differences in price per sqm was run.
- **Rating coding.** Rating has only five integer levels and was treated as linear in the regressions. Its categorical treatment was not tested.
- **Failed tasks.** None. All tasks are recorded as complete.

## Open questions

- Does a spline or log-size term change the within-group slopes and the rating interaction estimate once both are placed on a common estimand? Does the spline refit on log price, or a log model with a spline in size, explain the high-age gap?
- Is the high-age gap between spline and log effects driven by spline misfit at large sizes, by the smearing back-transform, or by the extreme high-price listings? How much of it remains without those listings?
- Is the size-by-rating interaction null? A pre-specified single rating-slope contrast, a formal size-by-age-by-rating test, or more data is needed to rule out moderate interactions.
- Does price per square metre decline with age after controlling for size, using a regression on log price and log size?
- Is the rating-level spread in price per sqm statistically significant under a formal test such as Kruskal-Wallis?
- Are the six top-1% listings data errors or genuine luxury properties, and should they be capped before modelling?
- Does the log-target linear regression's MAE advantage hold after accounting for back-transformation bias in the mean of price, given that its RMSE does not improve as much?
- Does age_years have a nonlinear effect on price (log or spline term)? This could explain why the forest's age importance is near zero while the linear model's is not.
- Would tuning the random forest under cross-validation (leaf size, depth, max_features) change its ranking against linear regression?
- Should rating be treated as categorical, given its five discrete values and unreliable linear effect?