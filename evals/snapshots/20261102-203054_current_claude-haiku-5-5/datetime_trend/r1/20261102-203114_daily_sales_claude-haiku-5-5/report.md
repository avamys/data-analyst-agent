# Sales Drivers and Predictability: Promo, Temperature and Calendar Effects on Daily Sales

## Summary

- **Promo is the clearest driver of sales.** Promo=1 rows average 298.4 against 266.3 for promo=0 (Welch p = 1.3e-12, Cohen's d = 0.81). The gap of 32.1 units holds at 30.3 after adjusting for month, weekday and time trend. The two groups overlap substantially, so promo shifts sales but does not separate them.
- **Temperature shows no significant linear relation to sales.** Pearson r = 0.016 (p = 0.67) on all 730 rows. The promo effect does not show a statistically detectable change with temperature (interaction p = 0.41), but the interval is too wide to rule out a substantial change.
- **A linear model on promo and temperature beats a mean baseline only modestly.** On the 146-row test split, test R² is 0.069 against -0.038 for the baseline, with MAE 29.60 against 31.68. Most of the variation in sales is not explained by these two features.
- **Gradient boosting does not improve on linear regression.** It overfits (train R² 0.29, test R² 0.016) and scores worse than linear regression on every test metric. The two importance methods disagree on whether promo or temperature matters more.
- **Sales rise steadily over the two years.** Monthly mean sales climb from 219.7 to 324.4 (Spearman rho = 0.992 with the month index). The data cover only 24 months, so this cannot be separated into trend and seasonality.

## Data

- 730 rows and 4 columns (date, temperature, promo, sales).
- Target: sales, a continuous variable with mean 270.8, median 270.25 and standard deviation 41.1.
- Features used: temperature (continuous, about -4 to 25) and promo (binary, 14.2% of rows promoted). The date column is an id-like text field and was excluded as a feature. It was used only to derive month, weekday and time index in the calendar analysis.
- Missing values: none in any of the four columns.

## Findings

### Sales distribution

Sales are centred near 271, with quartiles of 239.4 and 300.5. The middle half is roughly symmetric around the median.

![Distribution of sales across all rows, counts per bin](tasks/eda_1/charts/sales_histogram.png)

### Promo and sales

- Promo=1 sales are shifted upward. Median is 295.4 against 266.4 for promo=0, and mean is 298.4 against 266.3.
- The distributions overlap substantially. The promo=0 75th percentile is 294.95, and the promo=1 25th percentile is 272.2.
- Spread is similar in both groups (standard deviation 38.8 for promo=1, 39.7 for promo=0). Promo mainly changes the level of sales rather than its spread.
- Welch t-test: t = 7.79, p = 1.3e-12. Mean difference 32.1 units (95% CI 24.0 to 40.3). Cohen's d = 0.81, which the analysis classes as a large effect.

![Box plot of sales (units) for each promo group, promo=0 vs promo=1](tasks/stat_1/charts/sales_by_promo_boxplot.png)

### Temperature and sales

- Across temperature quartiles, mean sales stay between 266.6 and 273.7 with no clear trend. The promo rate is lowest in the third quartile (10.5%) and between 14% and 17% in the other quartiles.
- Pearson r between temperature and sales is 0.016 (95% CI -0.057 to 0.088, p = 0.67). Spearman rho is 0.010 (p = 0.78). The Spearman interval uses a Fisher z approximation, the same as the Pearson interval, so it is approximate and not rank-based.
- Within promo=1 rows, the Pearson correlation is 0.10. Within promo=0 rows it is 0.013. The promo=1 subgroup is small (14.2% of rows), and the analysis did not test the within-group correlations for significance.

![Sales against temperature, one point per row, colored by promo flag](tasks/eda_1/charts/sales_vs_temperature.png)

### Promo by temperature interaction

- In the OLS model sales ~ temperature × promo, the interaction coefficient is 0.49 (95% CI -0.68 to 1.67, p = 0.41). The data show no statistically detectable variation in the promo effect across temperature. The interval is wide enough that a substantial change cannot be ruled out, so the promo effect should not be described as constant.
- The main temperature slope is 0.07 (p = 0.75).
- The promo effect is significant within each temperature band:
  - At 2.70 (10th percentile): 27.8 units (95% CI 14.3 to 41.2).
  - At 12.40 (median): 32.6 (95% CI 24.3 to 40.8).
  - At 21.11 (90th percentile): 36.9 (95% CI 23.1 to 50.6).
  - The wide intervals at the extremes reflect limited precision of the interaction-based estimates.

### Promo effect after adjusting for calendar and trend

- Adjusted for month, weekday and time trend, the promo coefficient is 30.3 (95% CI 27.1 to 33.5, p = 1.1e-63). Unadjusted it is 32.1 (p = 5.8e-14), a change of about 6%, which the analysis judges not material.

### Predictive performance on the shared test split

Split: 80/20, random_state = 42, 584 training rows and 146 test rows.

| Model | Test MAE | Test RMSE | Test R² | Train R² |
|---|---|---|---|---|
| Mean baseline | 31.68 | 38.78 | -0.038 | 0.0 |
| Linear regression (temperature, promo) | 29.60 | 36.72 | 0.069 | 0.069 |
| Gradient boosting (temperature, promo) | 31.03 | 37.75 | 0.016 | 0.29 |

- Linear regression beats the mean baseline on all three metrics. Train and test R² are almost identical (0.069), so the model is not overfitting, but it has little predictive power.
- Fitted coefficients: promo adds about 30.3 units, temperature adds about 0.081 units per degree, and the intercept is 266.6.
- Gradient boosting overfits (train R² 0.29, test R² 0.016). It beats the mean baseline only marginally and does not beat linear regression on any test metric.

![Test MAE and RMSE in sales units for the mean baseline and the linear regression, 146 test rows](tasks/ml_1/charts/ml1_test_error.png)

![Test MAE and RMSE in sales units for the mean baseline, linear regression and gradient boosting, 146 test rows](tasks/ml_2/charts/ml2_model_comparison.png)

### Feature importance: the two methods disagree

- Built-in impurity importance from gradient boosting ranks temperature first (0.757) and promo second (0.243).
- Test-set permutation importance (increase in MAE) ranks promo first (1.97, std 0.81) and temperature second (1.09, std 1.08).
- The two results disagree. Temperature's permutation importance is about one standard deviation above zero, which the analysis does not consider clearly distinguishable from noise. The linear and correlation evidence (r = 0.016, p = 0.67) shows no significant linear relation between temperature and sales.

### Monthly promo rate and sales level

- The monthly promo rate ranges from 3.2% (1 promo day, in 2023-03, 2023-12, 2024-04 and 2024-09) to 35.5% (11 days, in 2024-01). Fourteen of 24 months have fewer than 5 promo days.
- Chi-square test of promo by month: p = 0.013. However, 50% of expected cell counts are below 5, so the approximation is unreliable. A permutation test (5,000 shuffles) gives p = 0.010, which the analysis describes as agreeing only marginally.
- Monthly mean sales rise from 219.7 (2023-01) to 324.4 (2024-12). The Spearman correlation between month index and monthly mean sales is 0.992 (p about 2e-21). This is a monotone rise over two years, not an established seasonal pattern.

![Share of days with promo=1 in each month](tasks/eda_2/charts/promo_rate_by_month.png)

![Mean sales per month split by promo flag (units)](tasks/eda_2/charts/sales_by_month_promo.png)

### Promo gap within months

- The promo=1 minus promo=0 sales gap is positive in all 24 months. Monthly gaps range from 12.8 to 76.5, with a median of 32.9.
- The extreme gaps come from months with one promo day, so month-level gaps are imprecise.
- The average gap is 33.6 in 2023 and 29.5 in 2024.

### Weekend premium

- Unadjusted, weekend rows have higher mean sales (298.7 against 259.7 on weekdays) and a higher promo rate (15.8% against 13.6%).
- Among promo=0 rows, the weekend coefficient adjusted for month and time is 39.1 (95% CI 36.5 to 41.8, p = 9.9e-118). The unadjusted promo=0 difference is 39.8 (p = 1.3e-32).
- Full sample: the weekend coefficient is 39.0 unadjusted, 38.9 adjusted for month and time, and 38.2 adjusted for month, time and promo (95% CI 35.8 to 40.6). Adding promo does not materially change the weekend premium.

![OLS coefficients with 95% CI: promo=1 effect (adjusted for month, weekday, time) and weekend premium among promo=0 rows (adjusted for month, time)](tasks/stat_2/charts/stat2_effects_ci.png)

## Limitations

- **Short time span.** The data cover 24 months. Trend and seasonality cannot be separated, and month-level estimates rest on 1 to 11 promo days.
- **Unreliable chi-square test.** The promo-by-month chi-square test has 50% of expected cell counts below 5. The permutation p-value (0.010) agrees only marginally.
- **Small promo=1 subgroup for temperature.** The within-promo=1 temperature correlation (r = 0.10) rests on the promo=1 subgroup (14.2% of rows) and was not tested for significance.
- **Imprecise interaction estimates.** The promo-by-temperature interaction is not significant, but its interval is wide, and the stratified promo effects at the temperature extremes have wide intervals. A substantial change in the promo effect across temperature cannot be ruled out.
- **Approximate Spearman interval.** The Spearman confidence interval uses the Pearson Fisher z method and is not rank-based.
- **Limited predictive power.** The best model explains about 7% of test variance (R² 0.069), and test RMSE is about 36.7. Most sales variation is not captured by promo or temperature.
- **Small test set.** Model scores rest on 146 test rows, and the permutation importance for temperature (1.09, std 1.08) is not clearly distinguishable from noise.
- **Conflicting importance results.** Impurity and permutation importance rank the two features in opposite order. The analysis reports both and does not resolve the disagreement.
- **Unadjusted gap in several findings.** The promo-group, weekend and monthly gap results are descriptive or adjusted only for month, weekday and time. The analysis did not test for other confounders.
- **No failed tasks or unresolved review issues** were recorded for this analysis.

**Numbers not traced to a recorded fact.** The automatic check found no recorded value for these numbers:
- 2.70 in: "- At 2.70 (10th percentile): 27.8 units (95% CI 14.3 to 41.2)."
- 12.40 in: "- At 12.40 (median): 32.6 (95% CI 24.3 to 40.8)."
- 21.11 in: "- At 21.11 (90th percentile): 36.9 (95% CI 23.1 to 50.6)."

## Open questions

- Is the weak positive temperature-sales relation within promo=1 rows real, or noise from the small promo=1 subgroup? The analysis did not test this.
- Would a larger sample or a bootstrap analysis narrow the promo-by-temperature interval enough to decide whether the promo effect changes with temperature?
- Is the monthly sales rise a long-run trend or a seasonal cycle? Separating these requires more than the two years available.
- Are the monthly promo-rate spikes, such as 35.5% in 2024-01, real calendar effects or noise from small promo-day counts?
- Is the weekend premium stable across months and years, or driven by particular periods?
- Does the promo effect differ by weekday or by season (interaction of promo with month)?
- Would a nonlinear model with calendar features reduce the large unexplained residual spread (test RMSE about 36.7)? Gradient boosting on temperature and promo alone did not.
- Does temperature explain part of the sales variation, or any part of the promo or weekend effects, once calendar terms are included?