# Daily Bike Rental Count (cnt): Associations with Season, Year, Month, Weather, Holiday and Working Day

## Summary

- **Season, year and weather are significantly associated with cnt; holiday and working day are not significant on their own.** Season (ANOVA p = 6.7e-67, η² = 0.347) and weathersit (ANOVA p = 3.1e-17, η² = 0.099) are significant. Year is significant (Welch p = 1.0e-62, mean difference 2194.2). Holiday (Welch p = 0.103) and working day (Welch p = 0.110) are not significant unadjusted.
- **Adjusting for temperature and other covariates changes the picture for holiday and working day.** In the six-variable OLS, holiday is significant (coefficient -629.9, p = 0.0013). In the ten-variable OLS it remains significant (-538.6, p = 0.0041). Working day stays borderline (p = 0.055 in the six-variable model, p = 0.086 in the ten-variable model).
- **Year and temperature carry most of the predictive signal.** A random forest on 11 legitimate features reaches test R² 0.887 and test RMSE 674.7, against 2022.2 for a training-mean baseline. Permutation importance ranks yr first and temp second.
- **Leakage was excluded.** Adding the leaky columns casual and registered inflates test R² to 0.998, so that score is not a real predictive result.
- **The working-day effect does not significantly differ by season or weathersit** (interaction p = 0.213 and p = 0.598).

## Data

- 731 daily rows, 16 columns. Target: cnt (daily total rentals), a regression target.
- Features used (11, all numeric-coded; no categorical or date/time features): season, yr, mnth, holiday, weekday, workingday, weathersit, temp, atemp, hum, windspeed.
- Excluded: casual and registered (leakage, since cnt is their sum), and instant and dteday (identifier and date fields).
- Missing values: none. The EDA confirmed 0 missing values across all 16 columns.
- cnt summary: mean 4504.35, median 4548, standard deviation 1937.21, range 22 to 8714.

## Findings

### Distribution and group differences

cnt is fairly symmetric across the 731 days (mean 4504.35, median 4548.0; quartiles 3152 and 5956).

![Histogram of daily total rentals (cnt) across 731 days](tasks/eda_1/charts/cnt_histogram.png)

Gap between the highest and lowest group mean, by feature: month 3596.1, weathersit 3073.5, season 3040.2, year 2194.1, holiday 792.1, weekday 461.5, working day 254.6. The month, weathersit and season gaps are the largest.

- **Month:** January has the lowest mean (2176.3, median 1939.0). Month 6 has a mean of 5772.4, and month 9 has 5766.5. Month 12 has 3403.8.
- **Season:** Season 1 averages 2604.1 (median 2209.0). Season 3 averages 5644.3 (median 5353.5). Season 2 averages 4992.3 and season 4 averages 4728.2.
- **Weathersit:** Weathersit 1 (463 days) averages 4876.8. Weathersit 2 (247 days) averages 4035.9. Weathersit 3 (21 days) averages 1803.3.
- **Year:** Year 1 averages 5599.9 against 3405.8 for year 0. This is a descriptive difference in one split. It does not separate a trend from seasonal or month effects, since both years cover the same months.
- **Holiday:** Holidays (21 days) average 3735.0 against 4527.1 on other days.
- **Working day:** Working days average 4584.8 against 4330.2 on non-working days.
- **Weekday:** Means range from 4228.8 (weekday 0) to 4690.3 (weekday 5).

![Mean daily rentals (cnt) by each categorical feature group](tasks/eda_1/charts/cnt_group_means.png)

### Significance tests and effect sizes

| Feature | Test results | Mean difference (95% CI) |
|---|---|---|
| Season | ANOVA F = 128.77, p = 6.7e-67; Kruskal-Wallis H = 250.93, p = 4.1e-54; η² = 0.347 (large) | Season 3 minus season 1: 3040.2 (2747.4 to 3332.9) |
| Weathersit | ANOVA F = 40.07, p = 3.1e-17; Kruskal-Wallis H = 67.18, p = 2.6e-15; η² = 0.099 (small to medium) | Weathersit 1 minus 2: 840.9 (557.0 to 1124.8) |
| Year | Welch t = 18.58, p = 1.0e-62; Mann-Whitney p = 7.1e-54; rank-biserial +0.66 for yr 1 vs yr 0 (large) | Year 1 minus 0: 2194.2 (1962.3 to 2426.1) |
| Holiday | Welch p = 0.103; Mann-Whitney p = 0.083; rank-biserial -0.22 for holiday 1 vs 0 (small) | -792.1 (-1758.4 to 174.2) |
| Working day | Welch p = 0.110; Mann-Whitney p = 0.119; rank-biserial +0.07 for working day 1 vs 0 (negligible) | 254.7 (-57.9 to 567.2) |

Holiday and working day are not significant at the 0.05 level in these unadjusted tests. The rank-biserial signs above are for group 1 vs group 0, as corrected from the originally recorded values.

Weathersit 3 against weathersit 1 (unadjusted): difference -3073.5 (95% CI -3660.0 to -2487.0, p = 8.8e-11, n = 21).

Correlations with cnt:
- temp: Spearman ρ = 0.622 (p = 1.7e-79); Pearson r = 0.627 (p = 2.8e-81).
- atemp: Spearman ρ = 0.623 (p = 9.6e-80); Pearson r = 0.631 (p = 1.9e-82).
- hum: Spearman ρ = -0.098 (p = 0.008); Pearson r = -0.101 (p = 0.006). This is a weak negative correlation.
- windspeed: Spearman ρ = -0.217 (p = 3.0e-9); Pearson r = -0.235 (p = 1.4e-10). This is a weak negative correlation.

![Mean daily rentals with 95% confidence intervals by season, yr and weathersit](tasks/stat_1/charts/cnt_mean_ci_season_yr_weathersit.png)

### Working day by season and weathersit

- **Season:** The working-day × season interaction is not significant (F = 1.50 on 3 df, p = 0.213). Mean cnt for non-working vs working days is 2257 vs 2781 in season 1, 5142 vs 4927 in season 2, 5475 vs 5718 in season 3, and 4606 vs 4786 in season 4.
- **Weathersit:** The working-day × weathersit interaction is not significant (F = 0.52 on 2 df, p = 0.598). Mean cnt for non-working vs working days is 4587 vs 5024 at weathersit 1, and 3937 vs 4075 at weathersit 2. Weathersit 3 has only 5 non-working and 16 working days (means 1815 and 1800), too few to estimate the interaction reliably.
- The three-way working day × season × weathersit term adds no significant explanatory power (F = 1.47, p = 0.117). This test compares the full three-way model against a model containing the working-day × season interaction plus weathersit main effects only. It does not compare against all two-way terms.

The source finding describes the pattern as consistent with sampling noise, so the interaction is not reported as a finding in its own right.

![Mean cnt by workingday across season (left) and weathersit (right)](tasks/stat_2/charts/wd_interaction_plot.png)

### Joint adjusted models

**Six-variable OLS** (yr, holiday, workingday, temp, season dummies, weathersit dummies; R² 0.810, adjusted R² 0.808). Coefficients are in rentals with 95% CIs:

- yr: 2049.8 (1925.8 to 2173.9), p < 0.0001. This is smaller than the unadjusted difference of 2194.2 and remains highly significant.
- holiday: -629.9 (-1011.9 to -247.8), p = 0.0013. The unadjusted difference is -792.1 (p = 0.103).
- workingday: 134.5 (-3.1 to 272.1), p = 0.055. The unadjusted difference is 254.6 (p = 0.110).
- temp: 4937.9 per unit (4329.6 to 5546.3), p < 0.0001.
- season (reference 1): season 2 1149.7, season 3 942.2, season 4 1590.0, all p < 0.0001. The season 3 vs 1 difference is 942.2 (95% CI 639.4 to 1244.9) adjusted, against 3040.2 unadjusted. Season 3 remains significant.
- weathersit (reference 1): weathersit 2 -628.4 (p < 0.0001), against an unadjusted weathersit 1 minus 2 difference of 840.9. Weathersit 3 -2447.7 (p < 0.0001), against an unadjusted value of -3073.5.
- Constant: 321.7 (75.4 to 568.0), p = 0.011.

Variance inflation factors are all below 5 (largest: season 3 at 4.61). The season code and temp correlate at r = 0.334.

**Ten-variable OLS** (adds mnth, weekday, hum, windspeed; R² 0.827, adjusted R² 0.824). Compared with the six-variable model:

- yr: 2018.4 (1898.6 to 2138.1), p < 0.0001. Change of -1.5%.
- holiday: -538.6 (-905.9 to -171.2), p = 0.0041. About 14.5% smaller in magnitude, still significant at 0.05.
- workingday: 115.4 (-16.3 to 247.1), p = 0.086. Shrinks about 14% and becomes non-significant at 0.05.
- weathersit 2: -454.9 (p < 0.0001), about 28% smaller in magnitude. Weathersit 3: -1965.4 (p < 0.0001), about 20% smaller.
- temp: 5094.6 (4499.3 to 5689.9), p < 0.0001. About 3% larger.
- season 2 1161.3, season 3 910.3, season 4 1657.2, all p < 0.0001.
- New terms: weekday 66.8 (p < 0.001); hum -1183.1 (p = 0.0001); windspeed -2774.0 (p < 0.0001). mnth is not significant (-15.4, p = 0.34) once season is in the model.

All ten-variable VIFs are below 6 (largest: season 3 at 5.74).

![Coefficients of the six-variable and ten-variable OLS models of daily rentals cnt; bars show estimated change in cnt per unit of each predictor](tasks/stat_4/charts/stat4_coef_comparison.png)

### Predictive models

Predictions are for cnt on a 147-row test set, with 584 training rows. The leaky columns are excluded.

| Model | Test R² | Test RMSE | Test MAE | Reduction in RMSE vs baseline |
|---|---|---|---|---|
| Training-mean baseline | -0.020 | 2022.2 | — | — |
| Linear regression (11 features) | 0.828 | 831.3 | 617.4 | 58.9% |
| Random forest (11 features, ml_2 refit) | 0.8865 | 674.7 | 430.9 | — |

- The random forest reaches 0.8865 test R² and 674.7 RMSE in the reportable refit. Training R² is 0.983, so it overfits somewhat. Linear regression has training R² 0.791 against test R² 0.828.
- Random forest permutation importance (drop in test R²), ranked: yr 0.516, temp 0.306, hum 0.079, atemp 0.069, season 0.057, mnth 0.038, windspeed 0.021, weathersit 0.019, weekday 0.006, workingday 0.002, holiday 0.0001.
- Linear regression coefficients are from unscaled features, and atemp and temp are collinear. Their magnitudes should not be ranked as separate effects.

![Test-set RMSE of predicting daily cnt for the training-mean baseline, linear regression and random forest (lower is better)](tasks/ml_1/charts/ml1_model_rmse.png)

### Leakage check

- With casual and registered added, the random forest reaches test R² 0.9977 and RMSE 97.0. Registered alone has importance 0.895 and casual 0.100; all other features are below 0.001.
- The profile reports that registered alone predicts cnt with R² 0.946. The leaked score is not a real predictive result, and these columns are excluded from every reported result.

## Limitations

- **Leakage:** casual and registered sum to cnt and were excluded. Their inclusion gives a misleading test R² of 0.998.
- **Unresolved discrepancy in the random forest results:** the ml_1 random forest (RMSE 674.2, MAE 426.2, R² 0.8867) and the ml_2 refit with identical settings (RMSE 674.7, MAE 430.9, R² 0.8865) differ. The cause was not verified. This report uses the ml_2 values. The ml_1 figures should not be treated as an exact replication.
- **Year is descriptive in the unadjusted case:** it does not separate a trend from seasonal or month effects, because both years cover the same months. The adjusted models keep the year effect, but none models a time index.
- **Small weathersit 3 group:** 21 days (5 non-working, 16 working). Interaction estimates for this group are unreliable.
- **Working day is borderline and sensitive to covariates:** p = 0.110 unadjusted, 0.055 in the six-variable model, 0.086 in the ten-variable model.
- **Holiday has a small sample:** 21 holiday days.
- **Collinearity:** season and temp are moderately correlated (r = 0.334), and season coefficients shrink after temp is added. Individual coefficients for atemp and temp should not be read separately.
- **Three-way interaction test:** the F-test compares only against a model with the working-day × season interaction and weathersit main effects, not against all two-way terms.
- **Rank-biserial signs:** the originally recorded signs for year, holiday and working day were reversed. This report uses the corrected group 1 vs group 0 values.
- **Model scope:** regression coefficients and predictions describe associations in this dataset. They do not establish causal effects.
- No tasks failed.

## Open questions

- Is the year effect a trend across time (for example, months or days since the start of the series) rather than a step between years? The adjusted models keep the year term but do not test this.
- Does the holiday association hold within season and weathersit strata? Its adjusted p-value (0.0013 in the six-variable model, 0.0041 in the ten-variable model) is much smaller than the unadjusted p-value (0.103).
- Does temperature interact with season, so that season gaps differ between warm and cold days?
- Does the large negative humidity coefficient (-1183.1 per unit in the ten-variable model) reflect a nonlinear weather effect that a weathersit-by-humidity interaction would clarify?
- Would a model with interaction terms or gradient boosting close the gap between linear regression and the random forest on temperature effects?
- How do prediction errors vary by season, working day and weathersit? Are the largest errors concentrated on extreme-weather days?
- Does yr partly reflect a split at a single year boundary?
- Why does the random forest refit differ slightly from the earlier run with identical settings?