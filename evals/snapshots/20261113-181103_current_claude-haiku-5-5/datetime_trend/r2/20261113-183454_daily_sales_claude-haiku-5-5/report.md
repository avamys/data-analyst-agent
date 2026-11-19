# Sales Analysis: Promo, Temperature and Day-of-Week Effects on Daily Sales (730 Days)

## Summary

- **Promo days sell more.** Promo days average 298.4 units against 266.3 on non-promo days, a raw gap of 32.1 (95% CI 23.97 to 40.27, Welch p = 1.3e-12, Cohen's d = 0.81). Adjusting for month, day of week and trend gives 30.5 (95% CI 27.3 to 33.7).
- **Temperature has no detectable linear association with sales.** Pearson r is 0.016 (p = 0.67), and mean sales vary by only about 7 units across temperature quartile bands with no monotone trend. A test of whether promo changes the temperature effect was null (interaction p = 0.41), which is not proof of no interaction.
- **Predictive power over the mean baseline is small.** On 146 test rows, linear regression on temperature and promo gives MAE 29.60 and R² 0.069, against MAE 31.68 and R² −0.038 for always predicting the training mean. Gradient boosting overfits (train R² 0.20, test R² 0.06).
- **Weekends sell more.** Adjusted for trend, month and promo, Saturday is 36.3 units above Monday (95% CI 32.3 to 40.4) and Sunday is 37.7 units above Monday (95% CI 33.6 to 41.7). Promo share does not differ significantly across days of week (chi-square p = 0.87).

## Data

- **Size:** 730 rows, 4 columns (date, temperature, promo, sales).
- **Target:** sales (regression), daily.
- **Features used for modelling:** temperature and promo, both numeric. There are no categorical, date or time features in the profile.
- **Excluded:** date was not used as a model feature. It was used in exploratory analysis to derive day of week, month and a linear trend.
- **Missing values:** none. The profile reports none, and the exploratory check confirmed 0 missing entries for date, temperature, promo and sales.

## Findings

### Sales distribution

Daily sales have a mean of 270.84, a median of 270.25, a standard deviation of 41.13 and a range of 178.3 to 391.8. The mean and median are close, so the distribution is roughly symmetric.

![Histogram of daily sales, counts of days per bin](tasks/eda_1/charts/sales_histogram.png)

### Promo effect

Promo 1 days (n = 104) have a mean of 298.39 and a median of 295.4. Promo 0 days (n = 626) have a mean of 266.27 and a median of 266.4.

- The mean difference is 32.12 units (95% CI 23.97 to 40.27).
- Welch t = 7.79, p = 1.3e-12, Cohen's d = 0.81 (a large effect).
- After adjustment for month, day of week and trend, the promo coefficient is 30.5 (SE 1.64, 95% CI 27.3 to 33.7, R² 0.873). Within the 24 months that contain both promo levels, the average gap is 34.2 units.
- In the full OLS model, the promo coefficient is 30.3 (95% CI 27.1 to 33.5, p < 1e-60).

The adjusted estimates (30.5 and 30.3) are close to the raw gap of 32.1. This is the check on whether time confounds the promo comparison, and adjustment changes the estimate only slightly.

![Mean daily sales for promo 0 and promo 1 days with 95% confidence intervals](tasks/stat_1/charts/promo_mean_sales.png)

### Temperature

- Mean sales by temperature quartile are 269.61 (Q1, coldest, n = 184), 273.74 (Q2, n = 183), 266.61 (Q3, n = 181) and 273.38 (Q4, warmest, n = 182). Medians are 267.9, 272.4, 265.3 and 276.25. Band edges are −4.0, 6.4, 12.4, 18.1 and 28.1 °C. The spread is about 7 units with no monotone trend.
- Pearson r = 0.016 (95% CI −0.057 to 0.088), p = 0.67.
- The simple OLS slope is 0.093 units per °C (95% CI −0.34 to 0.52).

![Scatter of temperature against sales for each promo group](tasks/eda_1/charts/temp_vs_sales_scatter.png)

### Promo–temperature interaction

In the OLS model sales ~ temperature × promo, the interaction coefficient is 0.49 (95% CI −0.68 to 1.67, p = 0.41). This is a null result and does not show that the temperature effect is unchanged by promo.

- Temperature slope is 0.07 per °C for promo 0 and 0.57 per °C for promo 1.
- The promo-1 slope has a 95% CI of −0.52 to 1.66, which includes zero. Both within-group estimates are imprecise.

### Day-of-week and time patterns

**Day of week (means and medians, unadjusted):**

| Day | Mean | Median | n |
|---|---|---|---|
| Monday | 260.9 | 260.7 | 105 |
| Tuesday | 257.3 | 252.4 | 104 |
| Wednesday | 258.7 | 258.9 | 104 |
| Thursday | 259.5 | 261.85 | 104 |
| Friday | 261.9 | 258.25 | 104 |
| Saturday | 297.2 | 300.45 | 104 |
| Sunday | 300.1 | 298.4 | 105 |

These are unadjusted size comparisons. The exploratory analysis did not test them for significance.

**Weekend effect, adjusted (OLS with trend, month and promo controls, relative to Monday):**

- Saturday: 36.3 (95% CI 32.3 to 40.4, p = 2.3e-57).
- Sunday: 37.7 (95% CI 33.6 to 41.7, p = 7.0e-61).

**Weekend effect without the promo control:** Saturday 36.3 (95% CI 31.3 to 41.2) and Sunday 39.5 (95% CI 34.5 to 44.4). The promo control changes the Sunday estimate from 39.5 to 37.7 and leaves Saturday unchanged.

**Promo share by day of week:** 13.3% (Monday), 13.5% (Tuesday), 13.5% (Wednesday), 14.4% (Thursday), 13.5% (Friday), 12.5% (Saturday) and 19.0% (Sunday). The chi-square test gives χ² = 2.47 on 6 degrees of freedom, p = 0.87, so promo share does not differ significantly across days of week. Sunday's share is the highest of the seven days.

**Trend:** Sales rise over the date range. The 2023 mean is 243.2 and the 2024 mean is 298.5. The linear slope is 0.153 units per day.

**Monthly means:** These rise through 2023, from 219.7 in January to 267.2 in October. With about two years of data, this cannot be separated from the upward trend, so it is not clear evidence of a seasonal cycle.

![Daily sales with 28-day rolling mean, and promo share per month](tasks/eda_2/charts/sales_time_series.png)

### Predictive models (test set, 146 rows)

A reproducible split (random_state = 42; 584 train rows, 146 test rows) on temperature and promo was used for all models. The training mean of sales is 272.32.

| Model | MAE | RMSE | R² |
|---|---|---|---|
| Mean baseline | 31.68 | 38.78 | −0.038 |
| Linear regression | 29.60 | 36.72 | 0.069 |
| Gradient boosting | 30.27 | 36.85 | 0.063 |

- Linear regression lowers test MAE from 31.68 to 29.60 relative to the baseline. The models explain under 7% of test variance, so they do not clearly beat the baseline.
- Gradient boosting has train R² 0.20 but test R² 0.06, so its extra flexibility does not generalize better than the linear model.

![Test-set MAE and RMSE in sales units for the mean baseline, linear regression and gradient boosting (146 test rows)](tasks/ml_2/charts/ml2_model_comparison.png)

**Feature importance (the findings disagree):**

- In the linear model, promo dominates: 10.99 sales per standard deviation, against 0.56 for temperature.
- In gradient boosting, built-in importance ranks temperature (0.65) above promo (0.35). Permutation importance gives promo 0.138 (SD 0.043) and temperature 0.097 (SD 0.045) in drop in R². The difference is about one SD, so the ranking is not clear.
- These sources disagree on which feature matters most. This report does not resolve the disagreement. Promo is the stronger feature in the linear model but is not clearly the most important overall.

## Limitations

- **Unresolved review issue: weekend effect and the exploratory day-of-week claim.** The lead's objection to the exploratory day-of-week finding still stands. That finding described the weekend gap as a real pattern, not noise, without a significance test or confidence interval, so this claim is not supported and is not relied on here. The weekend effect is tested only in the controlled analysis above (trend, month and promo controls, Monday baseline). The per-day means in the table are unadjusted size comparisons. The monthly promo–sales correlation is not used as evidence of confounding. The confounding check is the adjusted promo effect (30.5 against the raw 32.1), and promo-share balance by day of week is reported above.
- **Weekend effects are against Monday only.** The pooled Tuesday-to-Friday baseline and a joint test of the two weekend coefficients were not run.
- **Short time span.** The data cover about two years (2023 and 2024). Trend and seasonality cannot be cleanly separated, so the monthly pattern is not evidence of a seasonal cycle.
- **Model feature set.** All models use only temperature and promo. Models do not include the date-derived day-of-week, month or trend variables, which the exploratory analysis found associated with sales.
- **Null interaction.** The promo × temperature interaction is not significant, but the within-group temperature slopes are imprecise. The result does not show that promo has no effect on the temperature relationship.
- **Weak predictive performance.** Models explain under 7% of test variance and do not clearly beat the mean baseline on R².
- **Feature importance conflicts.** Linear coefficients, gradient-boosting built-in importance and permutation importance do not agree on the ranking of promo and temperature.
- **Overfitting.** Gradient boosting shows a large gap between train and test R².
- **Single split.** Model scores come from one split with a single random seed, so they may vary with other splits.
- **Failed tasks.** None reported.

## Open questions

- Is the weekend effect confounded with promo timing? Promo share does not differ significantly across days of week, but the effect was not estimated against a pooled Tuesday-to-Friday baseline, and a joint test of the weekend coefficients was not run.
- Does the promo uplift vary by day of week, particularly on Sundays, where promo share is highest?
- Is the weekend effect stable across 2023 and 2024, given the upward trend?
- Is the 2023-to-2024 level shift a step change or a continuing trend, and does it coincide with a change in promo frequency?
- Does the promo uplift vary by month (promo-by-period interaction)?
- Does a nonlinear temperature effect, such as a threshold or U-shape, exist that the linear analysis misses?
- Do holiday or weekly seasonal patterns remain once trend and weekday effects are removed?
- Which feature matters most for prediction? The linear and gradient-boosting analyses disagree.