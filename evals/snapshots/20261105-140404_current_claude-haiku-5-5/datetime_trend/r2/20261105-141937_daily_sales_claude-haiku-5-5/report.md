# Daily Sales Dataset (730 Rows): Target `sales`, Predictors Promo and Temperature

## Summary

- **Promo days sell more.** Mean sales were 298.39 on promo days (n=104) and 266.27 on non-promo days (n=626), a difference of 32.12 units (95% Welch CI 23.97 to 40.27, p=1.28e-12, Cohen's d=0.81). The Mann-Whitney test agrees (p=4.5e-12).
- **Temperature shows no detectable association with sales.** Pearson r was 0.016 (p=0.67) and Spearman rho was 0.010 (p=0.78). The promo × temperature interaction was not significant (p=0.41).
- **Sales rose over the 730 dates.** Mean sales were 243.20 in 2023 and 298.48 in 2024, and the OLS slope on day index was 55.94 units per year. No breakpoint test was run. Promo share and mean temperature were nearly the same in both years, and the rise appears within both promo groups in descriptive comparisons.
- **Linear regression is the best of the models tested, and it beats the mean baseline.** On the 146-row test split, it reached RMSE 30.61 and R² 0.354, against a baseline RMSE of 38.78 and R² of -0.038. Random forest reached RMSE 35.38 and R² 0.136 and overfit (train R² 0.877).
- **Calendar features carry more predictive weight than temperature.** Weekend and month effects were large in the descriptive and model results, while temperature's permutation importance was near zero in the linear model.

## Data

- **Size:** 730 rows × 4 columns.
- **Target:** `sales` (regression).
- **Features:** `temperature` and `promo` (numeric). `date` is not used as a feature as-is; month and weekday were derived from it for modelling. There are no categorical features.
- **Missing values:** none. The total count of missing cells across all four columns is zero, confirmed in eda_1.

## Findings

### Sales distribution

- Daily sales are roughly symmetric around the centre: mean 270.84, median 270.25, standard deviation 41.13, range 178.3 to 391.8.
- The 10-bin histogram has counts [28, 59, 112, 125, 121, 140, 82, 38, 21, 4]. The largest bin is 140 days (bin 6, 285.05 to 306.40), followed by 121 days (bin 5, 263.70 to 285.05). The distribution has a short right tail.

![Histogram of daily sales, counts of days per bin](tasks/eda_1/charts/sales_histogram.png)

### Promo and sales

- Mean sales were 298.39 (median 295.4, n=104) on promo 1 days and 266.27 (median 266.4, n=626) on promo 0 days.
- Welch t-test: mean difference 32.12, 95% CI 23.97 to 40.27, t=7.79, df=141.3, p=1.28e-12.
- Mann-Whitney U=46333, p=4.5e-12, so the result does not depend on the normality assumption.
- Cohen's d=0.81. This is at or above the conventional 0.8 benchmark for a large effect.

![Mean daily sales for promo 0 and promo 1 days with 95% confidence intervals of the mean](tasks/stat_1/charts/promo_mean_sales_ci.png)

### Temperature and sales

- Mean sales by temperature quartile were 269.61 (Q1, −4.0 to 6.4 degrees, n=184), 273.74 (Q2, 6.5 to 12.4, n=183), 266.61 (Q3, 12.5 to 18.1, n=181) and 273.38 (Q4, 18.2 to 28.1, n=182). The eda_1 summary describes this as a spread of about 7 units with no monotonic trend.
- Pearson r=0.016, 95% Fisher-z CI −0.057 to 0.088, p=0.67 (n=730).
- Spearman rho=0.010, approximate 95% CI −0.062 to 0.083, p=0.78 (n=730).
- The temperature effect is described as negligible, with both correlation CIs including zero.

![Scatter of daily sales against temperature, one point per day](tasks/eda_1/charts/sales_vs_temperature.png)

![Mean daily sales by temperature quartile band](tasks/eda_1/charts/sales_by_temp_band.png)

### Promo × temperature interaction

- OLS of sales on temperature, promo and their product (n=730):
  - Interaction: coefficient 0.495, SE 0.599, p=0.41, 95% CI −0.682 to 1.672.
  - Temperature main effect: 0.073, SE 0.228, p=0.75, 95% CI −0.375 to 0.521.
  - Promo main effect: 26.42, SE 8.18, p=0.0013, 95% CI 10.35 to 42.48.
- Temperature slope within promo 0 days: 0.073 per degree (SE 0.229, p=0.75, n=626). Within promo 1 days: 0.568 (SE 0.543, p=0.30, n=104). Neither slope is significant, and the interaction is not significant.
- The promo main effect of 26.42 is the difference at temperature 0, not the average promo uplift. The average uplift from the t-test is 32.12. The two figures are different quantities and are not reconciled further.

### Time trend and seasonality

- Mean sales were 243.20 in 2023 and 298.48 in 2024. The OLS slope on day index was 55.94 units per year (0.153 per day). This describes a steady upward drift; no breakpoint test was run, so no level change is claimed.
- Monthly means in 2023 ranged from 219.66 (January) to 268.66 (November). In 2024 they ranged from 274.60 (February) to 324.43 (December). The lowest 2024 month is above the highest 2023 month, and monthly means rise in most consecutive months.

| Month | Mean sales | n |
|---|---|---|
| 2023-01 | 219.66 | 31 |
| 2023-02 | 228.72 | 28 |
| 2023-03 | 221.65 | 31 |
| 2023-04 | 228.46 | 30 |
| 2023-05 | 231.72 | 31 |
| 2023-06 | 241.43 | 30 |
| 2023-07 | 248.11 | 31 |
| 2023-08 | 244.16 | 31 |
| 2023-09 | 255.30 | 30 |
| 2023-10 | 267.17 | 31 |
| 2023-11 | 268.66 | 30 |
| 2023-12 | 262.69 | 31 |
| 2024-01 | 275.71 | 31 |
| 2024-02 | 274.60 | 29 |
| 2024-03 | 281.35 | 31 |
| 2024-04 | 284.32 | 30 |
| 2024-05 | 287.70 | 31 |
| 2024-06 | 294.10 | 30 |
| 2024-07 | 302.11 | 31 |
| 2024-08 | 305.41 | 31 |
| 2024-09 | 313.09 | 30 |
| 2024-10 | 319.41 | 31 |
| 2024-11 | 319.36 | 30 |
| 2024-12 | 324.43 | 30 |

![Daily sales against date with 30-day centred rolling mean](tasks/eda_2/charts/sales_time_series.png)

### Day-of-week and weekend effects

Mean sales by day of week, pooled over both years:

| Day | Mean sales | n |
|---|---|---|
| Monday | 260.91 | 105 |
| Tuesday | 257.30 | 104 |
| Wednesday | 258.72 | 104 |
| Thursday | 259.47 | 104 |
| Friday | 261.91 | 104 |
| Saturday | 297.25 | 104 |
| Sunday | 300.15 | 105 |

- Monday to Friday means lie between 257.30 and 261.91. The day-of-week pattern is driven by the weekend.
- The weekend minus weekday gap is 42.08 units in 2023 (weekend 273.18, n=105; weekday 231.10, n=260) and 36.35 units in 2024 (weekend 324.47, n=104; weekday 288.12, n=261). These gaps are descriptive.
- The eda_2 summary describes the change between years as about 5.7 units. This is a descriptive difference only. No test of the change was run, so it is not established whether it differs from noise.

### Year-level confounding check

- Promo share was 13.97% in 2023 (51 of 365 days) and 14.52% in 2024 (53 of 365 days).
- Mean temperature was 12.282 in 2023 and 12.065 in 2024.
- Within promo groups, mean sales rose from 238.52 (n=314) to 294.19 (n=312) for promo 0, and from 272.07 (n=51) to 323.72 (n=53) for promo 1.
- On these descriptive summaries, the small changes in promo share and mean temperature do not account for the rise. This is not an adjusted estimate. Temperature balance was checked by mean only, not within groups.

![Mean daily sales by calendar year for promo 0 days and promo 1 days](tasks/eda_3/charts/eda3_promo_year_sales.png)

### Predictive models

Setup: 80/20 split with seed 42, giving 584 training rows and 146 test rows. Features were temperature, promo, and month and weekday derived from date.

| Model | Test RMSE | Test MAE | Test R² | Train R² |
|---|---|---|---|---|
| Mean baseline (train mean 272.32) | 38.78 | 31.68 | -0.038 | — |
| Linear regression | 30.61 | 26.67 | 0.354 | 0.346 |
| Random forest | 35.38 | 30.25 | 0.136 | 0.877 |

- Both models beat the mean baseline on the test split. Linear regression has the lowest test RMSE, MAE and highest test R², so it is the preferred model here.
- The random forest fits the training data well but generalises worse, which indicates overfitting.

![Test RMSE of the mean baseline, linear regression and random forest on the 146-row test split](tasks/ml_2/charts/ml2_model_test_rmse.png)

Feature importance. The two importance measures in the results disagree in part, and both are reported:

- **Linear regression, absolute coefficient:** promo 30.26, weekday 6.98, month 4.90, temperature 0.19.
- **Linear regression, permutation importance (drop in test R²):** month 0.386, weekday 0.246, promo 0.126, temperature −0.002.
- **Random forest, impurity importance:** temperature 0.389, weekday 0.301, month 0.240, promo 0.070.
- **Random forest, permutation importance (drop in test R²):** weekday 0.402, month 0.347, promo 0.202, temperature 0.060.

Points of agreement and disagreement:
- Promo is the largest of the two named features in the linear model's coefficient ranking and in both models' permutation results relative to temperature. The random forest's impurity ranking places temperature first.
- Month and weekday are the largest features under permutation importance in both models. The ml_2 summary describes month as the largest feature in both models, but in the random forest permutation results weekday (0.402) is above month (0.347). This is reported as given, not resolved.
- Temperature's permutation importance is near zero in the linear model (−0.002) and 0.060 in the random forest.

## Limitations

- **Association, not causation.** All results are associations in this dataset. None of the findings establishes a cause for the promo difference, the upward trend, or the weekend effect.
- **Promo uplift not adjusted in the t-test.** The 32.12 difference from the Welch test is unadjusted. Whether it holds after controlling for temperature and calendar effects was raised but not tested in the accepted results. The interaction model gives a different promo figure (26.42 at temperature 0), which is a different quantity and is not reconciled with 32.12.
- **Trend not established as a step change.** The upward drift is described by a linear slope. No breakpoint test was run. The eda_3 summary uses the term "level shift" for the 2023 to 2024 difference, while eda_2 claims no level change. These descriptions differ and are reported as they are.
- **Trend and weekend effects not adjusted.** The year, weekend and trend comparisons are descriptive. The 2023 to 2024 rise was not tested against promo and temperature in one model.
- **Weekend gap change not tested.** The change from 42.08 to 36.35 units (about 5.7 units) is descriptive only. It is not established whether it reflects a real change or noise.
- **Temperature balance.** The year comparison of temperature used means only. No within-group temperature check was run.
- **Non-linearity not tested.** Only linear temperature terms were examined in the regressions and correlations. A threshold or quadratic temperature effect was raised but not tested.
- **Model evaluation.** Models were evaluated on a single 146-row test split with one seed. The random forest was not tuned.
- **Feature importance disagreement.** Importance measures disagree on ranking, particularly for the random forest, as shown above.
- **Histogram ordering.** The eda_1 finding describes the peak bins in an order that does not match the stored counts. The report uses the stored counts: bin 6 has 140 days and bin 5 has 121.
- **Unresolved review issues (eda_2).** The lead's objections to eda_2 still stand:
  1. The full day-of-week table is required by the brief. It is included above from the eda2 and eda3 results, but the eda_2 task itself remains unresolved on this point. The affected finding is the day-of-week and weekend section.
  2. The weekend-gap statement must report 42.08 and 36.35 and the change of about 5.7 units as descriptive only. The report follows this wording, but the eda_2 task itself remains unresolved on this point. The affected findings are the weekend-gap statements in the day-of-week section and the year-level comparison.
- **Failed tasks.** None. All seven accepted tasks (eda_1, stat_1, stat_2, ml_1, ml_2, eda_2, eda_3) are marked complete. ml_1 provides the split and baseline, which are used in ml_2.

## Open questions

- Does the promo uplift of about 32 units hold after controlling for temperature and calendar effects such as day of week, month or season?
- Does the temperature effect hold within promo and non-promo days when adjusted for other factors? The interaction term was not significant, but nonlinear effects were not tested.
- Is there a time trend or seasonality beyond the weekend effect once the trend is removed?
- Does the 2023 to 2024 upward shift persist, or is it a step change at a specific date? A breakpoint test or a model with a year indicator was proposed but not run.
- Does the weekend gap narrowing from 42.08 to 36.35 units reflect a real change or noise?
- Is the strong month effect real seasonality, and would a model with explicit seasonal terms improve on the linear model?
- Why does the random forest overfit (train R² 0.88 vs test 0.14), and would tuning its depth or leaf size help?
- Is temperature balanced within promo groups and weekend status across the two years?