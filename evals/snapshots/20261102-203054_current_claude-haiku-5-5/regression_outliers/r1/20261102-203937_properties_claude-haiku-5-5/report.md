# Price of 600 Listings: Associations with Size, Age and Rating, and Prediction Performance

## Summary

- **Size is the only feature with a strong association with price.** Across size quartiles, median price rises by 358,250 from Q1 to Q4 (bootstrap 95% CI [338,700, 386,507]), Kruskal-Wallis epsilon-squared is 0.741 (large), and Spearman rho is 0.887.
- **Age has a small, statistically significant negative association.** Spearman rho is -0.157 (95% CI [-0.234, -0.078]), and the Kruskal-Wallis epsilon-squared is 0.027 (small). **Rating shows no significant association** with price (Kruskal-Wallis p = 0.51).
- **Price is strongly right-skewed (skewness 6.44), and log10 price is roughly symmetric (skewness 0.35).** On the log10 scale, the size association is stronger (Pearson r 0.844 across all rows, 0.914 with 19 high-side outliers removed).
- **No size × age interaction was detected at the 5% level** (p = 0.586), and no quadratic effect of size on log price was detected (p = 0.607). Both tests have wide confidence intervals, so they do not establish that the effects are constant or linear.
- **Prediction is weak.** The best-performing linear model reaches test R² 0.189 (RMSE 273,535 against 303,756 for the mean baseline). Gradient boosting overfits with default settings, and the models disagree on which metric ranks them best.

## Data

- 600 rows and 4 columns.
- Target: `price` (continuous regression).
- Features: `size_sqm`, `age_years`, `rating`. All three are numeric. There are no categorical, date/time, identifier or free-text features.
- Missing values: none in `size_sqm`, `age_years`, `rating` or `price`.

## Findings

### Price distribution and outliers

- Price has a mean of 289,164 and a median of 217,450. The standard deviation is 322,321, the minimum is 44,100, the maximum is 4,130,400, and the quartiles are 119,225 (Q1) and 371,400 (Q3).
- Price is strongly right-skewed (skewness 6.44). Taking log10 reduces the skewness to 0.35.
- Six listings (1.0%) are above the 99th percentile of 1,591,094.
- Nineteen listings (3.2%) are above the upper 1.5 IQR fence of 749,663. None are below the lower fence (-259,038), so all outliers are on the high side.

![Price distribution: linear-scale histogram (left) and log10-scale histogram (right) of price for 600 listings](tasks/eda_1/charts/price_histograms.png)

### Price by size, age and rating (binned averages and tests)

**Size (`size_sqm`, quartiles of 150 rows each)**

- Mean price rises from 106,167 (Q1) to 532,703 (Q4). Median price rises from 94,650 to 452,900.
- Kruskal-Wallis H = 444.69, p = 4.6e-96, epsilon-squared = 0.741 (large).
- The Q4 minus Q1 median difference is 358,250 (bootstrap 95% CI [338,700, 386,507]).
- Spearman rho between size and price is 0.887 (95% CI [0.869, 0.903], p = 5.8e-203). Pearson r on the raw price scale is 0.498. The team describes the relation as strongly monotonic but curved on the raw scale, with the largest gap in Q4.

![Price distribution per size_sqm quartile](tasks/stat_1/charts/price_by_size_bin_box.png)

**Age (`age_years`, quartiles)**

- Mean price by age quartile is 317,557 (Q1), 309,303 (Q2), 251,963 (Q3) and 277,834 (Q4). There is no steady trend in means. Medians fall from 237,600 (Q1) to 205,000 (Q4).
- Kruskal-Wallis H = 18.83, p = 0.0003, epsilon-squared = 0.027 (small).
- Spearman rho is -0.157 (95% CI [-0.234, -0.078], p = 0.00011). Pearson r is -0.077.
- The Q1 minus Q3 median difference is 49,800 (bootstrap 95% CI [800, 118,754]), which only just excludes zero. This contrast was chosen after looking at the data and should be treated as exploratory.

![Mean price by size_sqm quartile, age_years quartile and rating level (600 listings)](tasks/eda_2/charts/mean_price_by_bins.png)

![Price distribution per age_years quartile and per rating level](tasks/stat_1/charts/price_by_age_rating_box.png)

**Rating (`rating`, levels)**

- Mean price by level ranges from 250,008 (rating 2) to 355,663 (rating 5). The median is 184,150 for rating 2 and 227,200 for rating 5.
- Rating 5 has the highest mean, but its median (227,200, n = 134) is close to the others, so the mean is pulled up by high-price listings.
- Kruskal-Wallis H = 3.28, p = 0.51, epsilon-squared is about 0 (-0.001).
- All 10 pairwise Mann-Whitney tests with Holm correction have p = 1.0.
- Spearman rho is 0.034 (95% CI [-0.046, 0.114], p = 0.40). Pearson r is 0.066.
- The rating 5 minus rating 1 median difference is -9,900 (bootstrap 95% CI [-57,159, 57,209]).

### Log-scale size effect and the outliers

- On the log10 scale, mean price rises from 4.980 (size Q1) to 5.674 (Q4), and median price from 4.976 to 5.656. The steps between quartiles are roughly 0.2 to 0.25 log10 units and close to linear.
- Across all 600 rows, Pearson r between size and log10 price is 0.844 and Spearman rho is 0.887. The team notes that the curvature seen in raw price is largely a scale effect.
- With the 19 high-side outliers removed (n = 581), Pearson r rises to 0.914 and Spearman rho to 0.917. The size association on the log10 scale does not depend on these outliers.

![Mean and median log10 price by size_sqm quartile, all 600 listings](tasks/eda_3/charts/log_price_by_size_quartile.png)

### Size × age interaction

- In the log-price OLS with HC3 errors, the size_sqm × age_years interaction coefficient is 9.99e-06 per sqm per year, p = 0.586, 95% CI [-2.59e-05, 4.59e-05] (R² = 0.734).
- **No interaction was detected at the 5% level.** The confidence interval is wide enough to include effects that would matter against the size slope of 0.0120, so the data cannot establish that the size and age effects are constant.
- Main effects, each evaluated at zero for the other variable:
  - Size: 0.0120 log-price per sqm (about 1.2% per sqm), HC3 p = 7.65e-89.
  - Age: -0.0076 per year (about -0.8% per year), HC3 p = 0.0009. This is evaluated at size 0, which lies outside the data, so it is an extrapolated quantity.
- Within age terciles, the slope of log price on size is similar:
  - Young (age 0.1 to 21.3, n = 202): 0.01192 (CI 0.01093 to 0.01292).
  - Middle (age 21.4 to 38.2, n = 198): 0.01270 (CI 0.01177 to 0.01364).
  - Old (age 38.6 to 59.8, n = 200): 0.01239 (CI 0.01130 to 0.01349).
  - The intervals overlap. This is supporting but not conclusive evidence.

### Non-linearity of size on log price

- Adding a quadratic term in size to the log-price model does not improve fit. The squared-size coefficient is -3.61e-06 (HC3 SE 7.02e-06), p = 0.607, 95% CI [-1.74e-05, 1.02e-05]. The Wald test gives the same p-value.
- The linear size model has a slope of 0.01232 per sqm, with p below machine precision (recorded as 0.0). Its R² is 0.71253, against 0.71265 for the quadratic model. AIC is 571.8 for the linear model and 573.6 for the quadratic, so the linear model is preferred on fit.
- The data show no clear non-linear effect. The confidence interval includes zero and is consistent with curvature of either sign, so non-linearity is not excluded.

### Predicting price

All models use `size_sqm`, `age_years` and `rating`. Test results are on a fixed 80/20 split (480 training rows, 120 test rows, random_state = 42).

| Model | Test RMSE | Test MAE | Test R² |
|---|---|---|---|
| Mean-price baseline | 303,756 | 165,645 | -0.0002 |
| Linear regression (price) | 273,535 | 102,395 | 0.189 |
| Gradient boosting, default | 342,792 | 122,790 | -0.274 |
| Gradient boosting, shallow (depth 2, 150 trees, lr 0.05, subsample 0.8) | 281,805 | 95,561 | 0.139 |
| Linear regression on log price (back-transformed) | 274,205 | 80,231 | 0.185 |
| Gradient boosting on log price (back-transformed) | 279,228 | 88,506 | 0.155 |

- Linear regression reduces RMSE against the mean baseline by about 10% and MAE by about 38%, as stated by the team.
- Default gradient boosting overfits: train R² is 0.92 and test R² is -0.27. It is worse than the mean baseline on RMSE and R².
- The shallow gradient boosting model has a lower test MAE than linear regression (95,561 against 102,395), but a higher RMSE (281,805 against 273,535) and lower R² (0.139 against 0.189). **These results disagree on which model is best, depending on the metric.** The report does not resolve this.
- Modelling log price lowers typical absolute error (linear MAE 80,231 against 102,395) but does not lower RMSE (274,205 against 273,535). The R² on the log scale is 0.627 for the log-price linear model. Back-transformation uses exp without bias correction, so price-scale figures may understate the mean.

![Test-set RMSE of price by model; the mean baseline is 303,756 and the linear model is lowest](tasks/ml_1/charts/ml1_rmse_by_model.png)

### Feature importance

- **Permutation importance (linear model, test RMSE increase):** size_sqm 70,636; age_years 2,866; rating 484. Size dominates. With size in the model, permuting age or rating changes little.
- **Linear absolute coefficients (unscaled features):** rating 13,363; size_sqm 3,315; age_years 1,230. This ranking places rating first and conflicts with the permutation result. The team advises against presenting it as feature importance.
- **Default gradient boosting importances (overfit model):** size_sqm 0.578; age_years 0.380; rating 0.042. This agrees with the permutation result on size being first.

## Limitations

- **Unresolved review issue on the interaction finding.** The lead's objection stands. The wording "negligible" and "neither variable's effect depends on the other in this sample" overstates the result. The correct statement is that no interaction was detected at the 5% level. The 95% CI [-2.59e-05, 4.59e-05] is wide enough to include effects that would matter against the size slope of 0.0120, so the data cannot establish that the effects are constant. The tercile overlap is supporting but not conclusive. This affects the size × age interaction finding and its conclusion that the size effect is about 1.2% per sqm at every age.
- **Age association is weak and partly exploratory.** The Q1 vs Q3 contrast was chosen after looking at the data, and its confidence interval only just excludes zero. The age coefficient of the interaction model is evaluated at size 0, outside the data.
- **Non-linearity test has limited power.** The quadratic confidence interval does not exclude curvature that would matter.
- **Rating 5 mean is affected by high-price listings.** Its median is close to other levels.
- **Outliers are not removed from the main results.** Six listings are above the 99th percentile and 19 are above the IQR fence. The log10 correlations with outliers removed are reported, but model results with capped or removed outliers were not computed.
- **Prediction results are from one fixed split with 120 test rows.** Scores are low (best test R² 0.189), and rankings differ between RMSE and MAE.
- **Back-transformed predictions** use exp without bias correction, so price-scale results from log-price models may understate the mean.
- **Confounding is not examined.** Whether the age effect is confounded with size was not tested.
- **No task failed.** All analysis tasks are reported as complete.

## Open questions

- Is the size effect driven mainly by the highest-price listings? The outlier-removed correlations are higher, but a robust regression with slope estimates was not run.
- Do the high-price listings concentrate in rating 5 and the largest size quartile, which would explain the rating 5 mean?
- Is the weak negative age effect confounded with size, since older listings may be smaller?
- Does a natural spline or binned-size model show local non-linearity that the single quadratic term misses?
- Does a bias-corrected back-transform of log-price predictions change the price-scale RMSE comparison?
- Would capping or removing the 6 prices above the 99th percentile change the model results enough to matter?
- Why does gradient boosting overfit so strongly with 480 training rows, and do tuning or more data change the model ranking?
- Which high-price listings share a size, age or rating profile, and are they a separate market segment?