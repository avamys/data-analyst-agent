# Sales Drivers and Predictive Performance: Daily Sales (Target) with Promo and Temperature

## Summary

- **Promo days sell more than non-promo days, and the gap holds after adjustment.** Promo=1 days average 298.4 units (n=104) versus 266.3 for promo=0 (n=626). The Welch t-test gives p = 1.3e-12, and the mean difference is 32.1 units (95% CI 24.0 to 40.3). After adjusting for temperature and month, the promo coefficient is 32.9 (95% CI 25.3 to 40.6).
- **Temperature shows no detectable association with sales.** Pearson r is 0.016 (p = 0.67) and Spearman rho is 0.010 (p = 0.78). Quartile means vary by only about 7 units against an overall standard deviation of 41.1. The promo effect does not significantly change with temperature (interaction p = 0.41).
- **Linear regression is the preferred predictor on the random 80/20 split, but only modestly.** On the random split (random_state=42), linear regression reaches test RMSE 30.61 and R² 0.354, against 33.16 and 0.241 for gradient boosting and 38.78 and -0.038 for the mean baseline. A second random split (random_state=0) ranks gradient boosting first, so the ranking depends on the split.
- **Under a time-ordered split, no model explains later-period sales.** The test set (latest 20% of dates) has a mean of 316.78 versus a training mean of 259.36. The mean baseline has RMSE 63.17 and R² -4.75. Linear regression lowers RMSE to 55.19 but still has R² -3.39, and gradient boosting has R² -3.70.
- **The later period's higher level appears to be a 2023-to-2024 shift, not a promo or seasonal effect, but this is not formally settled.** Promo share is 14.2% earlier and 14.4% later. A linear time trend and a 2024 indicator fit almost equally well, and two years of data cannot separate them.

## Data

- 730 rows and 4 columns.
- Target: `sales` (regression).
- Numeric features: `temperature`, `promo` (binary 0/1).
- No categorical features. The `date` column is an identifier-like text field and was not used directly. Month and day-of-week were derived from it for the models.
- Missing values: none in any column, so no imputation was needed. The missingness check is a confirmation only.

## Findings

### Sales distribution

Daily sales are centred near 271 units (mean 270.8, median 270.25, standard deviation 41.1). The middle half of days falls between 239.4 and 300.5, and the full range is 178.3 to 391.8.

![Histogram of daily sales, count of days per bin](tasks/eda_1/charts/sales_histogram.png)

### Sales by promo and temperature (descriptive)

- **Promo:** promo=1 has mean 298.4 and median 295.4 (n=104). promo=0 has mean 266.3 and median 266.4 (n=626). The mean gap is about 32 units and the median gap about 29 units.
- **Temperature quartiles:** mean sales are 269.6 (coldest quartile, n=184), 273.7 (Q2, n=183), 266.6 (Q3, n=181) and 273.4 (warmest, n=182). The spread between bin means is about 7 units.

![Scatter of temperature against sales, one point per day](tasks/eda_1/charts/temp_vs_sales_scatter.png)

### Promo effect: significance and size

- Welch t-test: t = 7.79, df = 141.3, p = 1.3e-12.
- Mean difference (promo=1 minus promo=0): 32.1 units, 95% CI 24.0 to 40.3.
- Cohen's d: 0.81 (approximate 95% CI 0.60 to 1.02).

![Boxplot of daily sales in units for promo=0 days and promo=1 days](tasks/stat_1/charts/sales_by_promo_box.png)

### Temperature association

- Pearson r = 0.016 (95% CI -0.057 to 0.088, p = 0.67).
- Spearman rho = 0.010 (p = 0.78).
- Neither test detects a linear or monotonic association.

### Promo by temperature interaction

- The temperature × promo interaction is not significant: coefficient 0.49 units per degree (SE 0.60, 95% CI -0.68 to 1.67, p = 0.41).
- The full OLS model (sales ~ temperature × promo, n = 730) has R² = 0.076.
- The estimated promo effect rises with temperature but the intervals overlap almost entirely:
  - 27.8 units at the 10th-percentile temperature (2.7 degrees; 95% CI 14.3 to 41.2).
  - 32.6 units at the median temperature (12.4 degrees; 95% CI 24.3 to 40.8).
  - 36.9 units at the 90th-percentile temperature (21.1 degrees; 95% CI 23.1 to 50.6).
- The analysis does not report this interaction as a finding. The data cannot distinguish a constant promo effect from a temperature-dependent one.

### Promo effect adjusted for temperature and month

- Adjusted OLS (sales ~ promo + temperature + month dummies, January reference, n = 730): promo coefficient 32.9 units (95% CI 25.3 to 40.6, p < 0.001).
- The unadjusted difference is 32.1, so adjustment shifts the estimate by +0.8 units. Adding temperature alone gives 32.2.
- R² rises from 0.075 (promo only) to 0.242 (full model; adjusted R² 0.228).
  - Promo plus month alone gives R² 0.241.
  - Promo plus temperature alone gives R² 0.075.
  - Month accounts for most of the gain over promo alone. Temperature adds almost nothing beyond promo and month.
- Temperature coefficient in the adjusted model: -0.48 units per degree (p = 0.255), so no detectable temperature effect once promo and month are controlled.

### Predictive performance on a random 80/20 split (random_state=42)

Training uses 584 rows and testing uses 146 rows. Features are temperature, promo, month and day-of-week.

| Model | Test RMSE | Test MAE | Test R² |
|---|---|---|---|
| Mean baseline | 38.78 | 31.68 | -0.038 |
| Linear regression | 30.61 | 26.67 | 0.354 |
| Gradient boosting | 33.16 | 28.35 | 0.241 |

- Train R²: linear 0.346, gradient boosting 0.598. Gradient boosting shows a larger train-test gap.
- Permutation importance on the test set (mean drop in score when shuffled):
  - Linear: month 0.386, day-of-week 0.246, promo 0.126, temperature -0.002.
  - Gradient boosting: month 0.363, day-of-week 0.342, promo 0.144, temperature 0.069.
- The built-in importance rankings (absolute coefficient for linear, impurity for gradient boosting) differ from the permutation ranking. The permutation results are the ones to cite.
- Linear regression is preferred on this split.

![Test RMSE of the mean baseline, linear regression and gradient boosting (lower is better)](tasks/ml_2/charts/ml2_rmse_comparison.png)

### Predictive performance on a time-ordered split

The time-ordered split trains on the earliest 80% of dates (584 rows) and tests on the latest 20% (146 rows).

- The training mean is 259.36, against 272.32 under the random split.
- The test-period mean is 316.78 (sd 26.42), about 57.4 units above the training mean.
- The mean baseline on this test set scores RMSE 63.17 and R² -4.75. Under the random split it scored RMSE 38.78 and R² -0.04. The time-ordered RMSE is 1.63 times the random-split RMSE.

| Model (time-ordered test) | Test RMSE | Test MAE | Test R² |
|---|---|---|---|
| Mean baseline | 63.17 | 57.48 | -4.75 |
| Linear regression | 55.19 | 51.64 | -3.39 |
| Gradient boosting | 57.08 | 54.44 | -3.70 |

- Both feature-table models beat the baseline on RMSE and MAE. None has a positive R² on the time-ordered test set.
- Train R²: baseline 0.0, linear 0.284, gradient boosting 0.574. The larger train-test gaps for the models partly reflect the level shift, which the features do not capture.
- Linear regression has the lower time-split RMSE and MAE. Its top feature by absolute coefficient is promo (30.48), followed by day-of-week (7.08), month (1.43) and temperature (0.47). For gradient boosting, day-of-week has the highest importance (0.456), then temperature (0.279), promo (0.147) and month (0.118). The two models disagree on which feature matters most.

![Test RMSE of the mean-of-training-target baseline under a random 80/20 split versus a time-ordered split (train earlier, test later)](tasks/ml_3/charts/ml3_baseline_rmse_compare.png)

![Test RMSE of the mean baseline, linear regression and gradient boosting under a random 80/20 split versus a time-ordered split](tasks/ml_4/charts/ml4_model_rmse_compare.png)

### Random split comparison (random_state=0 on concatenated rows)

A second random split, used in the ml_4 task, gives different results from the ml_2 split:

| Model (random_state=0) | Test RMSE | Test MAE | Test R² |
|---|---|---|---|
| Baseline | 40.24 | 33.55 | -0.003 |
| Linear regression | 34.52 | 30.21 | 0.262 |
| Gradient boosting | 34.00 | 29.57 | 0.284 |

- On this split, gradient boosting ranks first on RMSE and R². On the random_state=42 split, linear regression ranks first.
- The two random-split results disagree on the preferred model. The time-ordered split favours linear regression, as does the random_state=42 split. Only the random_state=0 split favours gradient boosting.
- The random splits make the models look better on R² than they do on later dates.

### Level shift between early and late dates (eda_2, partial)

- Monthly sales means rise across 2023 and 2024, from 219.66 in January 2023 to 324.43 in December 2024.

![Monthly mean sales across the dataset dates](tasks/eda_2/charts/eda2_monthly_sales.png)

- **Promo frequency does not explain the higher later level.** Promo share is 14.2% in the earliest 80% of dates and 14.4% in the latest 20%. The chi-square test on promo rate gives p = 1.0.
- **Calendar-month mix differs between periods, but this reflects the cutoff.** The latest 20% covers only August to December 2024 (25, 30, 31, 30 and 30 rows by month). The month-mix chi-square test gives p ≈ 9e-49, which the finding attributes to the August cutoff.
- **Same calendar months across years.** For August to December, mean sales are 259.56 in 2023 and 316.29 in 2024. Promo share is 14.4% in 2023 and 13.8% in 2024. The period comparison and the same-month comparison are the same 2024-versus-2023 contrast, not independent evidence.
- The eda_2 finding concludes that a seasonal month pattern does not explain the gap and that the most consistent explanation is a trend or year-level shift. This was not formally tested.

### Trend versus step change (stat_4)

- Full model (time index + month dummies + promo): time-index coefficient 0.151 units per day (OLS 95% CI 0.142 to 0.160), about 55 units per year. The 2024 indicator coefficient in the alternative model is 55.22.
- Newey-West HAC (maxlags 14) time-index CI: 0.145 to 0.157. The HAC standard error is smaller than the implied OLS standard error, which the finding flags as unusual and needing a check.
- The time index and the 2024 indicator are highly correlated (0.866). The trend model (R² 0.693) and the 2024-indicator model (R² 0.692) fit almost equally well, against R² 0.075 for promo alone. The choice between trend and step rests on functional form, and the data cannot separate them.
- Promo coefficient with time index and month dummies: 31.95 (OLS 95% CI 27.07 to 36.82). The HAC 95% CI is 27.78 to 36.11. The promo-only coefficient is 32.12.

## Limitations

- **Autocorrelation and OLS inference (stat_4).** Daily sales with a strong trend are likely autocorrelated. The OLS p-values for the time index (5.2e-143) and the 2024 indicator (2.4e-142) are probably overstated and should not be treated as strong evidence on their own. The HAC check supports a positive, significant time-index coefficient, but the HAC standard error is smaller than the implied OLS standard error, which has not been checked. The Welch test for promo (stat_1) is not covered by this caveat. The OLS-based promo and interaction estimates in stat_2 and stat_3 carry the same independence assumption.
- **Trend versus step change is unresolved (stat_4, eda_2).** Two years of data cannot separate a linear trend from a 2024 step. The eda_2 task is marked partial, and its trend-based explanation was not formally tested.
- **Cause of the level shift is untested.** No task established why the later period sits about 57 units higher. The features do not explain it.
- **Time-ordered results.** No model has a positive R² on the time-ordered test set. The test period covers only August to December 2024 and is a single split.
- **Random split inconsistency.** The two random splits (random_state=42 and random_state=0) use different row orderings and give different model rankings. Neither has been established as the reference split. The ml_1 baseline (RMSE 38.78) and the ml_4 random baseline (RMSE 40.24) are not directly comparable for this reason.
- **Interaction estimates are imprecise.** The promo-by-temperature interaction is not significant. The temperature-specific promo effects have overlapping intervals and are not reported as findings.
- **Residual diagnostics not run.** The stat_3 task raised heteroskedasticity and autocorrelation checks on the adjusted model. These have not been done, so the adjusted promo CI has not been checked against robust or HAC standard errors.
- **Only two years.** The 2023 and 2024 comparison rests on a single two-year span, and the same-month comparison overlaps with the period comparison.
- **Unexplained variance.** Promo, month and temperature together explain about 24% of variance in the adjusted model. Most variation in sales is unexplained.
- **Model tuning.** Gradient boosting was run without tuning or regularisation, and linear regression was not compared with other regularised models. The conclusion that gradient boosting overfits applies to these configurations only.
- No task failed, but eda_2 remains partial.

## Open questions

- Does the promo uplift of about 32 units hold across months and temperatures once interactions are tested, given that the interaction tests were not significant but had limited power?
- Is the promo effect different between 2023 and 2024? This was raised by eda_2 and not tested.
- Would a linear time trend, a 2024 step, or a longer history of data better explain the level shift? More history would be needed to separate them.
- What causes the 57-unit gap between the earlier and later periods: a trend, a seasonal effect, or a change in promo frequency? Promo frequency was ruled out as the cause of the gap, but a trend and a seasonal effect were not separately tested.
- Would adding a lagged or trend feature based on date order reduce time-split error enough to give a positive R²?
- Are the residuals well behaved (heteroskedasticity and autocorrelation), and do robust or HAC standard errors change the promo confidence interval?
- Why is the HAC standard error for the time index smaller than the OLS standard error, and does a different maxlags choice change this?
- Which random split (random_state=42 or random_state=0) should be the reference for model comparison?
- Would more data or stronger regularisation let gradient boosting beat linear regression on test error?