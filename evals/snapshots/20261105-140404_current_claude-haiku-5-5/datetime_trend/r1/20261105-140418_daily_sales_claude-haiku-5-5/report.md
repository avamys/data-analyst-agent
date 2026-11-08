# Daily Sales Analysis: Promo and Temperature as Predictors of Daily Sales (730 Days)

## Summary

- **Promo days sell more.** Promo days average 298.4 sales versus 266.3 on non-promo days, a difference of 32.1 (95% CI [24.0, 40.3], Welch p = 1.3e-12; Cohen's d = 0.81). The Mann-Whitney test agrees (p = 4.5e-12). After adjusting for the upward time trend, the promo effect is +29.6 (95% CI [20.3, 38.9], p < 0.001).
- **Temperature has no detectable relationship with sales.** Pearson r = 0.016 (95% CI [-0.057, 0.088], p = 0.67) across all 730 days, and it explains well under 1% of sales variance.
- **The temperature × promo interaction is inconclusive.** The interaction coefficient is 0.495 sales per degree (95% CI [-0.682, 1.672], p = 0.41) unadjusted, and 0.197 (95% CI [-0.484, 0.878], p = 0.57) after adjusting for time. The intervals include meaningful effects in either direction, so this does not show that temperature modifies the promo effect, nor that it does not.
- **Predictive power is small.** On 146 held-out days, linear regression on temperature and promo reaches test R² of 0.069, against -0.038 for the mean baseline. Gradient boosting overfits (training R² 0.29, test R² 0.016). Promo is the feature that matters in the linear model.

## Data

- 730 daily rows with 4 columns: date, temperature, promo and sales.
- Target: sales, a continuous value.
- Features used: temperature (numeric) and promo (binary, about 14% of days are promo days, n = 104).
- Date is not used as a model feature. Time effects were checked through trend analysis in EDA and as a time index in the adjusted model.
- Missing values: none. Each column (date, temperature, promo, sales) has zero missing values.

## Findings

### Sales distribution

Overall daily sales (n = 730) have a mean of 270.8, a median of 270.3, an SD of 41.1 and a skewness of 0.10, so the distribution is close to symmetric.

![Distribution of daily sales across all 730 days](tasks/eda_1/charts/sales_histogram.png)

### Promo effect

- Promo=1 days (n = 104) have a mean of 298.4 and a median of 295.4. Promo=0 days (n = 626) have a mean of 266.3 and a median of 266.4.
- Mean difference (promo=1 minus promo=0): 32.1, 95% CI [24.0, 40.3], Welch t = 7.79, df = 141.3, p = 1.3e-12.
- Mann-Whitney U = 46333, p = 4.5e-12, so the rank-based test agrees with the parametric test.
- Cohen's d = 0.81 (pooled SD), a large effect by the usual benchmarks.

![Distribution of daily sales for promo=0 and promo=1 days](tasks/stat_1/charts/sales_by_promo.png)

### Promo effect within years and months

- 2023: promo=1 days (n = 51) average 272.1 versus 238.5 for promo=0 (n = 314), a gap of 33.6. Promo share is 14.0%.
- 2024: promo=1 days (n = 53) average 323.7 versus 294.2 for promo=0 (n = 312), a gap of 29.5. Promo share is 14.5%.
- Both gaps are unadjusted for the time trend.
- Monthly promo share ranges from 3.2% (2023-03) to 35.5% (2024-01). Promo days are a minority in every month, and every one of the 24 months has at least one promo day.
- Monthly promo share does not trend: its correlation with the month index is -0.013 (p = 0.95), and its correlation with monthly mean sales is 0.061 (p = 0.78).

![Share of days with promo=1 per month, 2023-2024](tasks/eda_2/charts/promo_share_monthly.png)

![Share of days with promo in each calendar month](tasks/stat_3/charts/stat3_promo_share_by_month.png)

### Promo effect adjusted for the time trend

In an OLS model of sales on promo, a time index in days, temperature and temperature × promo (n = 730, R² = 0.69), the promo coefficient is +29.6 (95% CI [20.3, 38.9], p = 6.7e-10). This is similar in size to the unadjusted quartile differences, and the adjustment changes the estimate only modestly. The time trend is +0.153 sales per day (p < 0.001).

### Promo effect by temperature quartile

The promo mean difference is positive in every temperature quartile:

| Quartile | Temperature range | Promo=1 days | Difference | 95% CI | p |
|---|---|---|---|---|---|
| Q1 | -4.0 to 6.4 | 28 | +21.9 | [6.1, 37.8] | 0.008 |
| Q2 | 6.5 to 12.4 | 31 | +40.6 | [25.0, 56.2] | < 0.001 |
| Q3 | 12.5 to 18.1 | 19 | +29.4 | [11.1, 47.8] | 0.003 |
| Q4 | 18.2 to 28.1 | 26 | +34.0 | [16.6, 51.4] | < 0.001 |

Q1 has the smallest difference, but its interval overlaps the others and the quartile sizes are small (19 to 31 promo days). The variation does not show a monotone pattern and is compatible with noise.

### Temperature and sales

- Across all 730 days: Pearson r = 0.016 (95% CI [-0.057, 0.088], p = 0.67); Spearman rho = 0.010 (p = 0.78, approximate 95% CI [-0.062, 0.083]).
- Quartile sales means range from 266.6 to 273.7, with medians from 265.3 to 276.3.

![Scatter of daily sales against temperature](tasks/eda_1/charts/sales_vs_temperature.png)

Within promo groups:

- **Promo=0 (n = 626):** Pearson r = 0.013 (95% CI [-0.066, 0.091], p = 0.75); Spearman rho = 0.008 (p = 0.85).
- **Promo=1 (n = 104):** Pearson r = 0.103 (95% CI [-0.091, 0.290], p = 0.30); Spearman rho = 0.139 (p = 0.16, approximate 95% CI [-0.055, 0.323]). The interval is wide because the group is small. A weak positive relationship cannot be ruled out, but there is no evidence for one.

Temperature slopes from OLS:

- Promo=0: 0.073 sales per degree (95% CI [-0.377, 0.523], p = 0.75).
- Promo=1: 0.568 sales per degree (95% CI [-0.508, 1.644], p = 0.30).

### Temperature × promo interaction

- **Unadjusted:** coefficient 0.495 sales per degree (95% CI [-0.682, 1.672], p = 0.41).
- **Adjusted for time:** coefficient 0.197 sales per degree (95% CI [-0.484, 0.878], p = 0.57).

Both results are inconclusive. The promo effect is positive across all temperature quartiles, but the data cannot settle whether it varies with temperature.

### Time trend

Monthly mean sales rise from 219.7 in January 2023 to 324.4 in December 2024. The linear trend is about +4.7 per month across 24 months.

![Monthly mean of daily sales over time](tasks/eda_1/charts/sales_monthly_mean.png)

### Predictive models

The mean baseline, linear regression and gradient boosting were all evaluated on the same held-out split (random_state 42): 584 training days and 146 test days.

| Model | Test R² | Test RMSE | Test MAE |
|---|---|---|---|
| Mean baseline | -0.038 | 38.78 | 31.68 |
| Linear regression | 0.069 | 36.72 | 29.60 |
| Gradient boosting | 0.016 | 37.75 | 31.03 |

- Linear regression lowers the typical error by about 2 sales units per day (RMSE down about 5%, MAE down about 7% against the baseline). These test-set differences rest on only 146 days, so they are indicative rather than precise.
- Five-fold cross-validated R² for linear regression on the training set ranges from -0.021 to 0.083, with mean 0.042 and SD 0.035. Some folds show no gain.
- Gradient boosting has training R² of 0.29 but test R² of 0.016, so it generalizes worse than the linear model.

Feature importance:

- **Linear model:** the standardized coefficient is 10.995 for promo and 0.56 for temperature. The linear coefficient for promo is 30.3 sales per unit. Permutation importance (drop in test R²) is 0.137 for promo and 0.002 for temperature.
- **Gradient boosting:** impurity-based importance gives temperature 0.76 and promo 0.24. Permutation importance gives promo 0.131 and temperature 0.099. These two rankings disagree. The impurity ranking should not be trusted given the model's overfitting, and the permutation result is weak evidence for temperature.

![Test-set RMSE and MAE of the mean baseline, linear regression and gradient boosting on 146 held-out days](tasks/ml_1/charts/ml_1_model_comparison.png)

## Limitations

- **Association, not causation.** All promo and temperature estimates are associations. The data do not establish why promo days sell more.
- **Time trend in unadjusted results.** The promo estimates in the EDA, the unadjusted quartile analysis, the interaction test before adjustment and the linear regression coefficient (30.3) do not adjust for the time trend. The time-adjusted model (stat_3) gives +29.6 for promo. Its interaction result is also inconclusive.
- **Limited promo sample.** There are 104 promo days in total, and 19 to 31 per temperature quartile. Intervals for promo-specific temperature effects are wide.
- **Small predictive gain.** The models explain only a few percent of out-of-sample variance. The test set has 146 days, and the single split is one estimate. Model comparisons are indicative.
- **Limited time modeling.** Seasonality was not modeled beyond the linear time index. The adjusted model's R² of 0.69 includes the time index, but the models in ml_1 do not include it.
- **Monthly promo shares.** Monthly shares are based on 1 to 11 promo days per month and are noisy.
- **Unresolved issues.** No unresolved review issues or failed tasks were recorded.

## Open questions

- Is the promo effect still present after controlling for seasonality (month or season), not only the linear time trend?
- Does the promo effect differ by month, season or temperature range? A larger sample of promo days, especially in low-share months, would be needed to narrow the interaction interval.
- Is the promo=1 temperature relationship (slope 0.568 per degree, not significant) meaningfully positive?
- What drives the upward sales trend over 2023–2024: seasonality, growth, or a change in promo frequency? Promo share shows no trend, but the cause of the rise is not identified.
- What explains the remaining variation in daily sales that temperature and promo do not capture?
- Would adding calendar features (month, weekday) or a time trend improve out-of-sample R² materially?