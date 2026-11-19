# Daily Sales Analysis: Promo and Temperature Effects on Sales (daily_sales, 730 rows)

## Summary

- **Promo days sell more.** Promo days average 298.39 units against 266.27 on non-promo days, a difference of 32.12 (95% Welch CI 23.97 to 40.27, a 12.06% lift). Both the Welch t-test (p = 1.3e-12) and the Mann-Whitney test (p = 4.5e-12) reject equal sales, and Cohen's d is 0.81.
- **Temperature shows no meaningful association with sales.** Pearson r is 0.016 (p = 0.67), and the promo×temperature interaction is not significant (p = 0.41). Mean sales are nearly flat across temperature quartile bands.
- **Date features predict sales far better than temperature and promo.** A linear model on month, weekday and trend reaches test RMSE 19.30 (R² 0.743), against 38.78 for the mean baseline. Adding temperature and promo gives the best result, RMSE 16.71 (R² 0.807). The temperature+promo models alone barely beat the baseline (RMSE 36.72 for linear regression).
- **Sales rise over 2023–2024.** Quarterly means climb from 223.16 (2023Q1) to 321.05 (2024Q4). The seasonal-looking pattern by calendar quarter is confounded with this trend and is not established as seasonality.

## Data

- 730 rows and 4 columns. Target: `sales` (regression).
- Numeric features used: `temperature` and `promo`. There are no categorical features.
- The `date` column is not used as a feature as it stands. It is used only to derive month, weekday and trend features in the date-based models.
- Missing values: none across all four columns. There are no fully duplicated rows and no repeated dates. Consecutive dates run without gaps from 2023-01-01 to 2024-12-30.

## Findings

### Sales distribution and temperature bands

Overall sales are roughly symmetric: mean 270.84, median 270.25, standard deviation 41.13, skew 0.10.

Mean sales by temperature quartile band are nearly flat:

| Band | Temperature range | Mean sales | Promo rate |
|---|---|---|---|
| Q1 (coldest) | -4.0 to 6.4 | 269.61 | 0.15 |
| Q2 | 6.5 to 12.4 | 273.74 | 0.17 |
| Q3 | 12.5 to 18.1 | 266.61 | 0.10 |
| Q4 (warmest) | 18.2 to 28.1 | 273.38 | 0.14 |

The promo rate does not vary enough across bands to explain this flat pattern. Whether the flatness holds within years is addressed under the 2023–2024 findings below.

![Left: histogram of daily sales (counts of days). Right: mean daily sales per temperature quartile band.](tasks/eda_1/charts/sales_distribution_and_temp_bands.png)

### Promo effect

- Promo=1 days (n=104) have mean sales 298.39 (SD 38.79). Promo=0 days (n=626) have mean sales 266.27 (SD 39.72). Medians are 295.4 and 266.4.
- The difference in means is 32.12 units (95% Welch CI 23.97 to 40.27), a percent lift of 12.06% over the promo=0 mean.
- Welch t = 7.79 (df 141.3), p = 1.3e-12. Mann-Whitney p = 4.5e-12.
- Cohen's d = 0.81 using the pooled SD.

![Boxplot of daily sales for promo=0 and promo=1 days](tasks/stat_1/charts/promo_sales_boxplot.png)

### Temperature association and promo×temperature interaction

- Temperature and sales: Pearson r = 0.016 (95% CI -0.057 to 0.088, p = 0.67). Spearman rho = 0.010 (p = 0.78), with an approximate 95% CI of -0.067 to 0.087.
- In an OLS model of sales on temperature, promo and their interaction, the interaction coefficient is 0.49 sales per degree (95% CI -0.68 to 1.67, p = 0.41). The data do not show that the promo effect changes significantly with temperature.
- Promo lift by temperature tercile:
  - Low (-4.0 to 8.2): 26.7 units
  - Middle (8.3 to 16.4): 35.8 units
  - High (16.5 to 28.1): 34.4 units

  The lift is positive in every tercile, and the differences between terciles are not significant (interaction p = 0.41). These tercile estimates are not tested individually with confidence intervals.

### Prediction on the shared test split

The data are split 80/20 with random_state 42, giving 584 training rows and 146 test rows. The mean baseline (predicting the training mean of 272.3) has test RMSE 38.78 and MAE 31.68.

| Model | Features | Test RMSE | Test MAE | Test R² | Train R² |
|---|---|---|---|---|---|
| Mean baseline | none | 38.78 | 31.68 | — | — |
| Linear regression | temperature, promo | 36.72 | 29.60 | 0.069 | 0.069 |
| Gradient boosting | temperature, promo | 37.75 | 31.03 | 0.016 | 0.291 |
| Linear regression | month, weekday, trend | 19.30 | 15.17 | 0.743 | 0.734 |
| Gradient boosting | month, weekday, trend | 20.06 | 15.68 | 0.722 | 0.876 |
| Linear regression | temperature, promo, month, weekday, trend | 16.71 | 12.87 | 0.807 | 0.804 |
| Gradient boosting | temperature, promo, month, weekday, trend | 16.92 | 13.64 | 0.802 | 0.924 |

- **Temperature and promo models.** Linear regression is the better of the two, with RMSE about 5% below the baseline. Its R² of 0.069 means the model explains under 7% of test variance, so the improvement is small. Gradient boosting is about 2.7% below the baseline and overfits (train R² 0.291, test R² 0.016).
- **Permutation importance (linear model).** Shuffling promo raises test RMSE by 2.66 (SD 0.72). Shuffling temperature raises it by 0.036 (SD 0.046), which is effectively zero.
- **Date-based models.** Every date-based model cuts test RMSE by at least 45% against the baseline. The linear model on month, weekday and trend is about 50% below the baseline RMSE. Its top coefficients are weekday (7.18 per unit of the weekday index), trend (0.154) and month (0.117). Gradient boosting on the same features has trend as its main feature (importance 0.77).
- **All features.** Linear regression on all five features gives the lowest test error: RMSE 16.71 and MAE 12.87, against 38.78 and 31.68 for the baseline (R² 0.807). Its promo coefficient is 30.44, its weekday coefficient 6.92, and its temperature coefficient 0.045. Gradient boosting on all features is similar on test (RMSE 16.92) but overfits more (train R² 0.924).

![Test-set RMSE in sales units for the mean baseline, linear regression and gradient boosting](tasks/ml_2/charts/ml2_model_rmse.png)

### Trend and seasonality over 2023–2024

- The linear slope of sales on day index is 0.153 units per day (n=730).
- Quarterly mean sales (n per quarter in parentheses):
  - 2023Q1: 223.16 (90)
  - 2023Q2: 233.84 (91)
  - 2023Q3: 249.12 (92)
  - 2023Q4: 266.14 (92)
  - 2024Q1: 277.28 (91)
  - 2024Q2: 288.70 (91)
  - 2024Q3: 306.80 (92)
  - 2024Q4: 321.05 (91)

  By the quarterly means, the upward trend is the largest change across the period. No formal comparison of trend against seasonality or other components was made.
- Pooled by calendar quarter of year, mean sales rise from 250.37 (Q1, n=181) to 293.45 (Q4, n=183). This pattern is confounded with the upward trend across only two years, so no separate seasonality is established.
- The promo gap has the same sign in both years: 33.55 in 2023 (promo n=51, non-promo n=314) and 29.52 in 2024 (promo n=53, non-promo n=312). This is similar in direction and rough size. It was not tested per year.
- Temperature-band means differ by year:
  - 2023: 242.80, 243.33, 243.62, 243.00 (range 0.82).
  - 2024: 294.73, 303.18, 295.63, 300.00 (range 8.45), with no consistent ordering across bands.

  The 2024 band range of 8.45 is descriptive only. It has not been tested against noise or sampling variation.

![Mean daily sales per calendar quarter with row counts in the table](tasks/eda_2/charts/sales_by_quarter.png)

## Limitations

- **Two years of data.** The date range covers 2023–2024 only. Seasonality cannot be separated from trend with this span.
- **Random split, not out-of-time.** The model comparisons use a single random 80/20 split with one seed. No out-of-time validation was run, so the date-based scores may reflect the time structure of a random split.
- **Promo effect with date controls.** The promo coefficient of 30.44 (all-features linear model) and the raw difference of 32.12 come from different models. The promo model without date features was not refit for a direct comparison, so it is not shown whether trend or seasonality changes the promo effect. The 30.31 coefficient from the temperature+promo linear model is also a different model from the 32.12 raw difference.
- **Temperature-band findings disagree in scope.** Pooled across both years, the temperature-band means are flat (range from 266.61 to 273.74). Within years, the band pattern differs: the 2023 range is 0.82 and the 2024 range is 8.45. The within-year pattern is not tested, and the pooled and within-year results are reported as they stand.
- **Tercile lifts are not individually tested.** The per-tercile promo lifts have wide intervals and were not tested individually. Only the interaction test (p = 0.41) is reported.
- **Spearman interval is approximate.** The 95% CI for the Spearman correlation is an approximation.
- **Weekday as a numeric index.** Weekday enters the date models as a single numeric index, so its coefficient (7.18 per unit) assumes a linear effect across days. A one-hot encoding was not tested.
- **Gradient boosting not tuned.** Gradient boosting was run without tuning or regularisation. Its overfitting is recorded, but whether tuning would change the ranking is not tested.
- **Unresolved review issue (eda_2).** The lead's objection to two statements in the eda_2 findings still stands and has been reflected in the wording above. The first is that the 2024 band range of 8.45 is descriptive only and has not been tested against noise or sampling variation (affects the temperature-band finding for 2024). The second is that the upward trend is the largest change across the period by the quarterly means, with no formal comparison of trend against seasonality or other components (affects the trend and seasonality finding). No numbers were changed.
- **Failed tasks.** None. All eight tasks completed and were accepted.

## Open questions

- Does the promo effect of about 32 units hold after controlling for trend and seasonality? The date-controlled model gives a promo coefficient of 30.44, but no model without date features was refit for comparison.
- Does the upward trend persist after controlling for temperature and promo, or is it a level shift between 2023 and 2024?
- Is there true seasonality once the trend is removed, using more than two years of data?
- Is the flat pooled temperature-band pattern real, or hidden by within-band variation? What drives the 2024 band variation of 8.45 with no consistent ordering? A regression including year, temperature, promo and their interaction has been proposed but not run.
- Is the trend effect a true time trend or an artifact of how the series was generated? Does it hold on a later out-of-time split?
- Does weekday act as a weekly cycle that a one-hot encoding would model better than a numeric index?
- Does tuning or regularising gradient boosting let it beat linear regression on the full feature set?