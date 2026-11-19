# Daily Sales Analysis: Promo Status and Temperature as Predictors of Daily Sales (730 Days, 2023–2024)

## Summary

- **Promo days sell more.** Mean sales were 298.39 on promo days versus 266.27 on non-promo days, a difference of 32.12 units (Welch 95% CI 23.97 to 40.27, p < 0.001, Cohen's d = 0.81). The Mann-Whitney test also finds the distributions differ (p < 0.001). Adjusting for day of week and month leaves the promo coefficient at 31.33 units (95% CI 24.57 to 38.09, p < 0.001).
- **Temperature has no detectable linear relationship with sales.** Pearson r = 0.016 (95% CI -0.057 to 0.088, p = 0.67), and Spearman rho = 0.010 (p = 0.78). Mean sales barely change across temperature quartiles, from 266.61 to 273.74.
- **The promo effect does not show a significant dependence on temperature.** The promo × temperature interaction is 0.495 units per °C (95% CI -0.68 to 1.67, p = 0.41). The estimated promo effect runs from 27.8 to 36.9 units across the 10th to 90th percentile temperatures, but the intervals are wide.
- **Models barely beat the mean baseline.** The linear regression on temperature and promo has a test RMSE of 36.72 versus 38.78 for predicting the training mean (test R² 0.069). The random forest is worse than the baseline on test data (RMSE 40.34). Promo timing is uneven across months (chi-square p = 0.0025) but not across weekdays (p = 0.87).

## Data

- 730 daily rows across 4 columns, covering 2023-01-01 to 2024-12-30. The series is a complete daily sequence with no gaps and no duplicate dates.
- Target: `sales`, a continuous daily value.
- Features used: `temperature` (numeric, range -4.0 to 28.1 °C) and `promo` (binary, 0 or 1; 104 days with promo = 1). There are no categorical or other date/time features.
- `date` is an identifier-like text field and was not used as a feature directly. Day of week and month were derived from it only for the calendar controls.
- Missing values: none.

## Findings

### Sales distribution

Daily sales are roughly symmetric and centred near 271 units: mean 270.84, median 270.25, standard deviation 41.13, range 178.3 to 391.8, skew 0.10 (730 days).

![Histogram of daily sales, 730 days](tasks/eda_1/charts/sales_hist.png)

### Promo status

- Promo days (n = 104) have mean sales 298.39 (SD 38.79). Non-promo days (n = 626) have mean 266.27 (SD 39.72). The gap is 32.12 units, with similar spread in both groups.
- Welch t-test: t = 7.79, df = 141.3, p < 0.001. The 95% CI for the difference is 23.97 to 40.27. Cohen's d = 0.81, a large effect.
- Mann-Whitney test: U = 46333, p < 0.001. The rank-based test agrees that the distributions differ, so the difference is not only in the means.
- Adjusted for day of week and month (OLS with calendar controls, n = 730), the promo coefficient is 31.33 units (95% CI 24.57 to 38.09, SE 3.44, p = 9.1e-19). The unadjusted OLS coefficient is 32.12 (95% CI 23.89 to 40.35). The analysis reports calendar confounding as negligible for the promo effect; the adjusted confidence interval is narrower than the unadjusted one.

![Mean daily sales on promo vs non-promo days, bars show the mean and whiskers the 95% CI](tasks/stat_1/charts/sales_by_promo_mean_ci.png)

### Temperature

- Mean sales by temperature quartile: Q1 (coldest, -4.0 to 6.4 °C, n = 184) 269.61; Q2 (6.4 to 12.4 °C, n = 183) 273.74; Q3 (12.4 to 18.1 °C, n = 181) 266.61; Q4 (warmest, 18.1 to 28.1 °C, n = 182) 273.38.
- Standard deviations by quartile range from 37.7 to 45.2. Q2 is the widest band.
- Pearson r = 0.016 (95% CI -0.057 to 0.088, p = 0.67). Spearman rho = 0.010 (bootstrap 95% CI -0.068 to 0.081, p = 0.78). Both effects are negligible and not significant at alpha 0.05.

![Scatter of daily sales against temperature](tasks/eda_1/charts/sales_vs_temp_scatter.png)

![Mean daily sales by temperature quartile](tasks/eda_1/charts/sales_by_temp_band.png)

### Promo × temperature interaction

- In the OLS model sales ~ temperature + promo + temperature:promo (n = 730, R² = 0.076), the interaction coefficient is 0.495 units per °C (95% CI -0.68 to 1.67, p = 0.41).
- Temperature is not centred in this model. The intercept (265.37) is the expected non-promo sales at 0 °C, and the promo coefficient (26.42, 95% CI 10.35 to 42.48) is the promo effect at 0 °C, which is outside the typical observed range.
- Promo effect by temperature: 27.8 units at the 10th percentile (2.7 °C, 95% CI 14.3 to 41.2), 32.6 at the median (12.4 °C, 95% CI 24.3 to 40.8), and 36.9 at the 90th percentile (21.1 °C, 95% CI 23.1 to 50.6).
- The promo effect is positive across the observed temperature range. The change across temperature is small relative to the uncertainty. A non-significant interaction does not show that the effect is constant; the data are compatible with a modest slope change in either direction.

### Predictive models against the mean baseline

Evaluation uses one 80/20 split (random_state 42): 584 training rows and 146 test rows.

| Model | Test RMSE | Test MAE | Test R² |
|---|---|---|---|
| Mean baseline (training mean 272.32) | 38.78 | 31.68 | -0.038 |
| Linear regression | 36.72 | 29.60 | 0.069 |
| Random forest (300 trees) | 40.34 | 32.37 | -0.123 |

- The linear regression beats the baseline on test RMSE (36.72 vs 38.78) and test MAE (29.60 vs 31.68). This is a modest improvement and should not be overstated. Its training R² is 0.069, close to its test R².
- The random forest is worse than the baseline on test data. Its training R² is 0.39 against a negative test R², which indicates overfitting.

![Test RMSE of the mean baseline, linear regression and random forest on the 146-row test set](tasks/ml_2/charts/ml2_test_rmse.png)

### Feature importance

- Linear regression coefficients: promo 30.31 sales per unit; temperature 0.081 per °C.
- Permutation importance on the random forest (test set, 30 repeats): shuffling promo gives a mean drop in test R² of 0.151 (SD 0.051); shuffling temperature gives 0.065 (SD 0.085).
- The random forest's impurity importance ranks temperature first (0.867 vs 0.133 for promo). This disagrees with the permutation result and the linear coefficients. The analysis treated impurity importance as unreliable for an overfitted forest and based its conclusion on the permutation and linear results. Both results are reported here, and the disagreement is not resolved beyond that.
- Overall, promo is the dominant feature, and the effect of temperature is small and uncertain.

### Promo timing and calendar structure

- **Month:** Promo share varies from 6.5% in March to 29.0% in January (chi-square p = 0.0025). Promo days are concentrated in January (18 of 62 days), October (15 of 62) and July (14 of 62). March to June stay between 6.5% and 10.0%. Mean sales rise across the year, from 247.69 in January to 294.01 in November.
- **Day of week:** Promo share ranges from 12.5% (Saturday, 13 of 104) to 19.0% (Sunday, 20 of 105). The chi-square test finds no clustering (p = 0.87).
- **Weekend premium:** Weekday mean sales range from 257.30 to 261.91, with a weekday average of 259.66. Saturday (297.25) and Sunday (300.15) are 37.59 and 40.49 units above that average.

![Share of days with promo=1 by calendar month and by day of week (2023-2024)](tasks/eda_2/charts/promo_share_by_month_dow.png)

## Limitations

- **Promo timing is uneven across months.** Promo days cluster in January, July and October (chi-square p = 0.0025). The calendar-adjusted model (day of week and month) gives a promo coefficient of 31.33 against 32.12 unadjusted, but the adjustment is linear in the stated controls. Promo-by-month and promo-by-day-of-week interactions were not tested.
- **Interaction result is inconclusive.** The non-significant promo × temperature interaction does not establish that the promo effect is constant across temperature. The promo effect by temperature has wide intervals (for example, 23.1 to 50.6 at the 90th percentile).
- **Temperature is not centred.** The promo coefficient in the interaction model (26.42) refers to 0 °C, outside the observed range, and should not be read as an average effect.
- **Predictive gains are small.** The linear model improves on the baseline only modestly on a 146-row test set (test RMSE 36.72 vs 38.78), and its test R² is 0.069. The random forest overfits and does worse than the baseline.
- **Feature importance results conflict.** Impurity importance ranks temperature first; permutation importance and linear coefficients rank promo first. Both are reported above.
- **Temperature and promo do not explain most variation.** Models using only temperature and promo leave most of the daily variation in sales unexplained.
- **Linearity.** The temperature analysis checks only linear and rank-based association. A non-linear temperature effect was not tested.
- No review issues remain unresolved, and no tasks failed.

## Open questions

- Does the promo effect hold after controlling for the full seasonal structure (a month-of-year term, or a within-year trend), beyond the day-of-week and month controls used in the adjusted model?
- Is there a promo-by-month or promo-by-day-of-week interaction that changes the size of the promo effect?
- Is there a non-linear temperature effect, or a temperature effect within specific seasons, that the linear and rank-based tests miss?
- Does promo timing confound the promo effect beyond the linear calendar controls used here, given that promo days cluster in January, July and October?
- Is there a weekly or annual seasonal pattern in baseline sales that the temperature and promo variables do not capture?