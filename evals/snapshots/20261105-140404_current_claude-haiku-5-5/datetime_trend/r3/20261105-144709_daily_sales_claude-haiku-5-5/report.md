# Daily Sales Analysis: Promo, Temperature and Time Effects on Sales (730 Days)

## Summary

- **Promo days sell more.** Promo-day sales average 298.39 against 266.27 on non-promo days, a Welch difference of 32.12 units (95% CI 23.97 to 40.27, p = 1.28e-12). Cohen's d is 0.81. The effect holds at the mean temperature (32.44 units) and after adjusting for a day-index trend (promo coefficient 31.99).
- **Temperature has almost no linear relation to sales.** Pearson r is 0.016 (p = 0.67), and temperature explains about 0.02% of sales variance. The interaction between temperature and promo is not significant (p = 0.41).
- **Time and weekday explain far more than temperature or promo.** Sales correlate with day index at r = 0.785. Adding weekday dummies raises R² from 0.691 to 0.868 in the promo-plus-trend model. Weekend days average about 37 units above weekdays.
- **Predictive models barely beat the mean baseline.** Using only temperature and promo, linear regression reaches test R² 0.069 and gradient boosting 0.016, against -0.038 for the mean baseline. Linear regression is preferred, with promo as the dominant feature.

## Data

- 730 rows and 4 columns. Target: `sales` (regression).
- Numeric features: `temperature`, `promo`. No categorical or date/time features are used as model inputs.
- `date` is excluded as a raw feature. It was used only to derive a day index, month and weekday for the time analysis.
- Missing values: none in any column (date, temperature, promo, sales all have 0).

## Findings

### Sales distribution

Daily sales are roughly symmetric and unimodal: mean 270.84, median 270.25, standard deviation 41.13, skew 0.10, excess kurtosis -0.49, range 178.3 to 391.8. The 10-bin histogram peaks in the 221.0 to 306.4 range, with counts 112, 125, 121 and 140 in the four central bins.

![Histogram of daily sales](tasks/eda_1/charts/sales_histogram.png)

### Promo effect

Promo days have higher sales (eda_1, stat_1):

| Group | Mean | SD | n |
|---|---|---|---|
| promo = 0 | 266.27 | 39.72 | 626 |
| promo = 1 | 298.39 | 38.79 | 104 |

- Welch difference: 32.12 units, 95% CI 23.97 to 40.27, t = 7.79, df ≈ 141, p = 1.28e-12.
- Cohen's d = 0.81 (approximate 95% CI 0.60 to 1.02, pooled SD 39.6). The analysis describes this as a large effect. The CI is approximate.

![Mean daily sales with 95% CI for promo=0 and promo=1 days](tasks/stat_1/charts/stat1_promo_mean_sales.png)

### Temperature

- Mean sales by temperature quartile are 269.61 (Q1, coldest, n = 184), 273.74 (Q2, n = 183), 266.61 (Q3, n = 181) and 273.38 (Q4, warmest, n = 182). Standard deviations range from 37.7 to 45.2.
- Pearson r between temperature and sales is 0.016 (95% CI -0.057 to 0.088, p = 0.67, n = 730). R² is 0.0002.
- Spearman rho is 0.010 (p = 0.78), which the analysis describes as negligible. Two Spearman confidence intervals were reported (see Limitations).
- Within promo groups, r is 0.013 for promo = 0 (n = 626) and 0.103 for promo = 1 (n = 104). The analysis describes the promo effect as dominating the temperature effect.

![Scatter of daily sales against temperature, colored by promo flag](tasks/eda_1/charts/sales_vs_temp_by_promo.png)

### Temperature × promo interaction

- In OLS of sales on temperature, promo and their product (n = 730), the interaction coefficient is 0.49 sales units per degree (95% CI -0.68 to 1.67, p = 0.41). This is not significant.
- Promo differences within temperature quintiles (stat_2) range from 25.75 to 39.57 units. Each band has 18 to 24 promo days, and the CIs overlap widely:

| Quintile | Promo n / non-promo n | Difference | p | 95% CI |
|---|---|---|---|---|
| Q1 (≤5.0) | 24 / 123 | 25.75 | 0.006 | 8.52 to 42.99 |
| Q2 (5.0–9.96) | 24 / 121 | 32.83 | 0.0003 | 16.59 to 49.06 |
| Q3 (9.96–14.9) | 19 / 128 | 39.57 | 0.001 | 18.46 to 60.67 |
| Q4 (14.9–19.0) | 18 / 130 | 29.26 | 0.004 | 11.34 to 47.18 |
| Q5 (>19.0) | 19 / 124 | 35.34 | 0.002 | 15.55 to 55.13 |

- With temperature centred at its mean (12.17), the promo effect in the interaction model is 32.44 units (95% CI 24.18 to 40.70, p = 4e-14). This matches the Welch estimate. The uncentred promo coefficient of 26.4 is the effect at temperature 0 and is not an average effect.
- The model R² is 0.076.

![Mean sales difference (promo=1 minus promo=0) with approximate 95% CI within each temperature quintile band](tasks/stat_2/charts/stat2_promo_effect_by_band.png)

### Time trend and calendar pattern

- Sales rise over the two years. Correlation with day index (days since 2023-01-01) is r = 0.785 overall, 0.813 within promo = 0 and 0.835 within promo = 1. After subtracting promo-group means, r is 0.816.
- Mean sales by month rise from 247.7 in January to 293–294 in October through December. Each month has 57 to 62 days. Adding month dummies to a promo-plus-day-index model changes R² only from 0.6907 to 0.6931. Most of the monthly pattern is therefore the linear trend.

![Mean daily sales by calendar month, derived from the date column](tasks/eda_2/charts/eda2_month_means.png)

- Weekends are higher. Saturday and Sunday average about 297 and 300, against 257 to 262 on Monday to Friday, about 37 units higher. After subtracting promo-group means, weekend residuals are +27.0 and +27.8, and weekday residuals are -8.7 to -13.3.
- Adding weekday dummies raises R² from 0.6907 to 0.8683 in the promo-plus-day-index model. Adding both weekday and month dummies gives 0.8706.
- In this model the promo coefficient is 31.99 and the per-day time coefficient is 0.153.

### Predictive models

Features were temperature and promo only, with a seed-42 80/20 split (584 training rows, 146 test rows). The mean baseline predicts 272.32.

| Model | Train R² | Test R² | Test MAE | Test RMSE |
|---|---|---|---|---|
| Mean baseline | — | -0.038 | 31.68 | 38.78 |
| Linear regression | 0.069 | 0.069 | 29.60 | 36.72 |
| Gradient boosting | 0.291 | 0.016 | 31.03 | 37.75 |

- Both models beat the baseline only marginally on the test set.
- Gradient boosting shows a large gap between train and test R², which the analysis reads as overfitting. Linear regression shows no such gap.
- Linear coefficients: promo 30.31 sales units; temperature 0.081 sales units per degree, described as small.
- Permutation importance (test-set increase in MAE, 30 repeats):
  - Linear: promo 2.25 (SD 0.75); temperature 0.046 (SD 0.043).
  - Gradient boosting: promo 1.97 (SD 0.82); temperature 1.09 (SD 1.08).
- Promo is the dominant feature in both models. The temperature result differs by model. The analysis reports gradient boosting's impurity ranking (temperature 0.76, promo 0.24) as inflated by overfitting, and states that the test-set permutation result does not support temperature as a strong driver.
- The analysis recommends linear regression: best test R², MAE and RMSE of the three, consistent train and test R², and interpretable with two features.

![Test-set R² of mean baseline, linear regression and gradient boosting predicting sales](tasks/ml_2/charts/ml2_model_r2.png)

## Limitations

- **Promo estimates differ by model specification.** The promo effect is 32.12 in the Welch test and 32.44 at mean temperature in the interaction model. Both exclude date. The date-adjusted model gives 31.99. The predictive linear model gives 30.31. These are different models and the figures are not identical.
- **Two Spearman confidence intervals disagree.** One is -0.067 to 0.087 (Fisher approximation). The other is -0.062 to 0.083 (Fisher z with a Bonett-Wright standard error, which the analysis describes as approximate). Both give rho = 0.010 and are reported here without choosing between them.
- **Approximate intervals.** The Cohen's d interval is approximate. The Bonett-Wright interval is approximate.
- **Small promo subgroups.** There are 104 promo days in total, and 18 to 24 per temperature quintile. Quintile-level estimates are imprecise.
- **Temperature bands differ between tasks.** The EDA uses temperature quartiles and the interaction analysis uses quintiles. Their results are not directly comparable.
- **Predictive models omit the main drivers.** The models use only temperature and promo and exclude date. Their test R² of 0.069 and 0.016 therefore reflects that restriction. The time and weekday analysis shows that adding these features raises R² substantially in a regression, though no model with them was evaluated on held-out data.
- **Promo effect not adjusted for weekday in the main tests.** The 32-unit promo effect in the Welch and interaction tests does not control for weekday or trend. The date-adjusted check uses trend only, not weekday.
- **Review issues.** No unresolved review issues were recorded.
- **Failed tasks.** None. All five analysis tasks (eda_1, stat_1, stat_2, ml_1, ml_2) and eda_2 completed.

## Open questions

- Does the promo effect of about 32 units hold after controlling for weekday as well as the time trend? The analysis gives only the trend-adjusted estimate (31.99), with weekday dummies not included in the promo coefficient.
- Is the weak positive temperature slope among promo days (r = 0.103, n = 104) statistically significant, or is it noise? No test of this slope was reported.
- Is the weekend uplift the same size on promo and non-promo days? This interaction was suggested but not tested.
- Does the time trend hold when the two years are compared directly, given that month and trend are confounded in a 730-day series?
- What variation remains after promo, day index and weekday (residual SD about 41 before adjustment), and is any of it explained by temperature or other factors? No residual analysis was reported.
- Would a model including day index and weekday, evaluated on held-out data, outperform the temperature-and-promo models reported here?