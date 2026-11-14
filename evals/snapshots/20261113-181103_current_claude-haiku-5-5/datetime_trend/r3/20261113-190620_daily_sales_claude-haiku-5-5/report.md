# Sales Analysis Report: Drivers of Daily Sales (Target: sales, 730 rows)

## Summary

- **Sales distribution:** Sales are roughly symmetric, with a mean of 270.8, a median of 270.25, a standard deviation of 41.1, and a range of 178.3 to 391.8.
- **Promo:** Promo=1 rows have higher mean sales (298.4) than promo=0 rows (266.3). The difference is statistically significant (Welch t-test, stat_1.promo_welch_ttest) but is not adjusted for temperature and is associational, not a tested causal effect. In the model with month and temperature, the promo coefficient is 32.9 units (95% CI 25.3 to 40.6, p<0.001).
- **Temperature:** Temperature shows no detectable linear relation with sales overall (Pearson r=0.016, stat_1.temp_sales_pearson). Its sign is not consistent across the analyses, and no temperature coefficient is significant.
- **Calendar month and year:** Month remains significant after adjusting for promo and temperature (F(11, 716)=14.31, p=3.7e-25). Mean sales in 2024 are higher than in 2023 in every calendar month, which suggests a level shift between years that the analysis has not separated from a trend.
- **Prediction:** Linear regression on temperature and promo beats a mean baseline only slightly (test RMSE 39.03 vs 40.24, test R² 0.056). Gradient boosting does worse than the baseline on the test set.

## Data

- **Size:** 730 rows, 4 columns (date, temperature, promo, sales).
- **Target:** sales (regression).
- **Features:** temperature and promo are the numeric features. There are no categorical features. The date column is not used as a raw feature; it was parsed only to examine sales by calendar month and by year.
- **Missing values:** None. Date, temperature, promo and sales each have 0 missing values (eda_1.missing_values).

## Findings

### Sales distribution

Sales are roughly symmetric: mean 270.8, median 270.25, std 41.1, skew 0.10, range 178.3 to 391.8 (eda_1.sales_summary). The 10-bin histogram has counts of 28, 59, 112, 125, 121, 140, 82, 38, 21 and 4, peaking in the 285.05 to 306.4 bin (eda_1.sales_histogram).

### Promo

- **Descriptive:** Promo=1 rows (n=104) have mean sales of 298.4 and median 295.4. Promo=0 rows (n=626) have mean 266.3 and median 266.4 (eda_1.sales_by_promo). The boxplot five-number summaries are in eda_1.sales_boxplot_by_promo.

  ![Boxplot of sales for promo=0 versus promo=1](tasks/eda_1/charts/sales_boxplot_by_promo.png)

- **Significance:** The unadjusted promo difference in mean sales is statistically significant (Welch t-test, stat_1.promo_welch_ttest). The effect size is large (Cohen's d, stat_1.promo_welch_ttest). This difference is not adjusted for temperature.

  ![Boxplot of sales (units) for promo=0 (n=626) versus promo=1 (n=104)](tasks/stat_1/charts/sales_boxplot_promo_stat.png)

- **Adjusted, interaction model:** The OLS model sales ~ temperature + promo + temperature:promo gives a promo coefficient that the accepted findings describe as the promo gap at temperature 0. It is not a general temperature-adjusted effect. Its value is not reported here because it could not be matched to a recorded fact, and its upper 95% bound and p-value are also not in the accepted findings (stat_1.ols_main_effects).

- **Adjusted, month model:** In the model with month as a categorical term, promo carries a coefficient of 32.9 units (95% CI 25.3 to 40.6, p<0.001) (stat_2.promo_temp_coefs).

- **Linear model:** In the linear regression on temperature and promo, the promo coefficient is 33.6 units (ml_1.ml1_linear_regression).

### Temperature

- **Overall:** Temperature has no meaningful linear or rank relation with sales. Pearson r is 0.016 (stat_1.temp_sales_pearson, n=730), with no detectable linear relation. Spearman is 0.010 (eda_1.temp_sales_correlation).
- **By quartile:** Mean sales are flat across temperature quartiles: Q1 269.6 (n=184), Q2 273.7 (n=183), Q3 266.6 (n=181), Q4 273.4 (n=182) (eda_1.sales_by_temp_quartile).

  ![Scatter of sales against temperature, colored by promo group](tasks/eda_1/charts/sales_vs_temp_by_promo.png)

- **Within promo groups:** The temperature-sales correlation is r=0.013 for promo=0 (n=626) and r=0.103 for promo=1 (n=104). The promo=1 value was not tested for significance in the EDA (eda_1.sales_vs_temp_by_promo).
- **Temperature slope, promo=0:** The temperature main effect in the OLS model, which is the promo=0 slope, is positive but not significant. There is no detectable linear effect of temperature within promo=0 (stat_1.ols_main_effects).
- **Temperature slope, promo=1:** The promo=1 slope is 0.568 sales units per degree. Its 95% CI spans zero, so the slope is not significant at the 5% level (stat_1.temp_slope_by_promo.promo1). Its upper bound and p-value are not in the accepted findings, so they are not reported here.
- **Promo by temperature interaction:** The temperature:promo interaction is not significant. Promo does not significantly change the temperature slope (stat_1.interaction_term).
- **Model with month:** In the model with promo and month, temperature has a coefficient of -0.48 per degree (95% CI -1.31 to 0.35, p=0.26). This is not significant. Its sign is negative, while the promo=0 slope above is positive but not significant. The two analyses disagree in sign, and neither is significant (stat_2.promo_temp_coefs).

### Calendar month

- **Raw monthly means:** Mean sales are lowest in January (247.69) and February (252.06), and highest in November (294.01), October (293.29) and December (293.05). There is a small dip in March (251.5) below February. Promo rates vary by month, from 0.29 in January and 0.242 in October to 0.065 in March (eda_2.monthly_table).

  ![Line chart of mean sales per calendar month](tasks/eda_2/charts/monthly_mean_sales.png)

- **Temperature versus sales by month:** Mean temperature peaks in July (20.91) and is lowest in January (3.67). Sales do not follow the temperature pattern. The correlation between the 12 monthly mean sales and the 12 monthly mean temperatures is Pearson 0.093 and Spearman 0.168. With 12 points this is far from significant (eda_2.monthly_corr).
- **Adjusted month effect:** After adjusting for promo and temperature, the month term is strongly significant: F(11, 716)=14.31, p=3.7e-25. R² rises from 0.075 to 0.242 when month is added (stat_2.month_f_test).
- **Adjusted coefficients relative to January:** February +9.6 (p=0.149), March +13.7 (p=0.048), April +20.1 (p=0.010), May +25.1 (p=0.004), June +34.2 (p<0.001), July +37.8 (p<0.001), August +40.1, September +48.5, October +51.0, November +52.8 and December +51.7 (August to December all p<0.001) (stat_2.month_coefs_vs_jan).
- **Shape:** The early-year gap (January vs February) is small and not significant. The second-half-of-year gap is large. Promo adjustment does not remove the seasonal pattern (stat_2.month_coefs_vs_jan).

### Year and level shift

- **Monthly means by year:** Mean sales per calendar month in 2023 vs 2024 are: January 219.66 vs 275.71, February 228.72 vs 274.60, March 221.65 vs 281.35, April 228.46 vs 284.32, May 231.72 vs 287.70, June 241.43 vs 294.10, July 248.11 vs 302.11, August 244.16 vs 305.41, September 255.30 vs 313.09, October 267.17 vs 319.41, November 268.66 vs 319.36, December 262.69 vs 324.43. Overall means are 243.20 in 2023 and 298.48 in 2024 (eda_3.monthly_means_by_year, eda_3.year_overall_means).

  ![Mean sales per calendar month in 2023 and 2024 (28 to 31 rows per point)](tasks/eda_3/charts/eda3_monthly_sales_by_year.png)

- **Same ordering in both years:** The ranks of the 12 monthly means agree strongly across years (Spearman 0.923, Pearson 0.967). The order is not identical: January is lowest in 2023 but February is lowest in 2024, and November and December swap places (eda_3.month_order_corr).
- **Level shift:** The 2024 minus 2023 difference is positive in every calendar month, from +45.88 (February) to +61.74 (December) (eda_3.monthly_diff_2024_minus_2023). EDA 3 describes this pattern as looking mainly like a level shift between years rather than a change in within-year shape. This reading rests on year-month cells of 28 to 31 rows and has not been tested in a model.

### Predictive models

All three models use the same 80/20 split (random_state=0), with 584 training rows and 146 test rows.

| Model | Test RMSE | Test MAE | Test R² | Train R² |
|---|---|---|---|---|
| Mean-of-training baseline | 40.24 | 33.55 | -0.003 | 0.0 |
| Linear regression (temperature, promo) | 39.03 | 32.40 | 0.056 | 0.078 |
| Gradient boosting (temperature, promo) | 41.40 | 33.96 | -0.062 | 0.303 |

Sources: ml_1.ml1_baseline_mean, ml_1.ml1_linear_regression, ml_1.ml1_gradient_boosting.

- Linear regression has a lower test RMSE than the baseline (39.03 vs 40.24). This is a small gain on 146 test rows.
- Gradient boosting overfits: its training R² is 0.30, but it is worse than the baseline on the test set.

  ![Test RMSE of the mean baseline, linear regression and gradient boosting on the same split](tasks/ml_1/charts/ml1_model_test_rmse.png)

- **Feature importance:** In the linear model, promo has the largest coefficient in both raw and standardized form: 33.6 units raw, and 11.50 sales units per 1 SD (ml_1.ml1_lr_standardized_coef). Gradient boosting ranks temperature first (importance 0.72) and promo second (0.28) (ml_1.ml1_gradient_boosting). This ranking rests on one random split and has not been checked with other splits or cross-validation.
- **Temperature direction:** The raw linear coefficient for temperature is +0.0414 per degree, but the standardized coefficient is -0.28 per SD (ml_1.ml1_linear_regression, ml_1.ml1_lr_standardized_coef). Standardizing on the same training data cannot change the sign, so these two values are inconsistent. Temperature's direction cannot be relied on from these facts. The promo conclusion holds under both coefficients.

## Limitations

- **No causal estimates.** The promo differences are associational. The unadjusted difference is not adjusted for temperature, and promo rate varies by month (eda_2.monthly_table).
- **Promo gap at temperature 0.** The OLS interaction-model promo coefficient is the promo gap at temperature 0. It is not a general temperature-adjusted effect. Its value, upper 95% bound and p-value are not reported here.
- **Promo=1 temperature slope.** The slope of 0.568 per degree is not significant. Its upper 95% bound and p-value are not in the accepted findings. The promo=1 group has only 104 rows, so the slope is imprecise.
- **Temperature sign conflict.** Temperature's coefficient is positive but not significant within promo=0 (stat_1), -0.48 in the month model (stat_2), +0.0414 raw in the linear model, and -0.28 standardized (ml_1). The raw and standardized values from ml_1 have opposite signs, which cannot both be correct for the same training split. Review did not resolve this, so temperature's direction is unresolved.
- **Unresolved citation issue.** Several findings in the stat_1 and ml_1 reports do not cite the recorded fact names they rest on. The facts cited in this report are named where they were recorded. The stat_1 values that could not be matched to a recorded fact have been omitted.
- **Model evaluation.** Model scores come from one random 80/20 split of 146 test rows. The lower RMSE of linear regression relative to the baseline (39.03 vs 40.24) may not be reliable. Feature ranking has not been checked across other splits or with cross-validation.
- **Models omit date.** No model includes date-derived features such as month, year or trend. The month and year effects in stat_2 and eda_3 are therefore not reflected in the predictive models.
- **Year-month noise.** Each year-month cell has only 28 to 31 rows (eda_3.cell_counts). Monthly means and differences are noisy, and small differences in month ordering across years should not be over-interpreted.
- **Promo-by-month interaction untested.** The promo effect may differ by month, and this has not been tested.

**Numbers not traced to a recorded fact.** The automatic check found no recorded value for these numbers:
- 0.568 in: "- **Temperature slope, promo=1:** The promo=1 slope is 0.568 sales units per degree. Its 95% CI spans zero, so the slope is not significant at the 5% level (sta"
- 0.568 in: "- **Promo=1 temperature slope.** The slope of 0.568 per degree is not significant. Its upper 95% bound and p-value are not in the accepted findings. The promo=1"

## Open questions

- Does the promo effect persist after adjusting for date, weekday or trend, given that the promo group has a lower mean temperature (11.63 vs 12.26)? The month-adjusted model gives 32.9 units, but weekday and trend have not been tested.
- Is the 2024 level shift a trend across time or a single step at the year boundary? A regression with year and month terms, or a rolling trend, could separate these.
- Is the within-year rise from January to December still present after controlling for promo rate and temperature in a year-adjusted model?
- Is the promo=1 within-group temperature correlation (r=0.103) statistically significant? Its p-value was not tested in the EDA.
- Does promo remain the dominant feature across several random splits or under cross-validation?
- Does adding date-derived features (trend, seasonality) explain more variance in sales than temperature and promo do?
- Is the promo=1 temperature slope practically meaningful? More promo observations would be needed to tell.
- Would repeated cross-validation or a larger sample show whether the lower RMSE of linear regression over the mean baseline (39.03 vs 40.24) is reliable?
- Is the promo effect different by month (promo-by-month interaction)?