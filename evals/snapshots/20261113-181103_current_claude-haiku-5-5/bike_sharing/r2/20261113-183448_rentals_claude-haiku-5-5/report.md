# Bike-Rental Demand: Daily Count (cnt) Analysis of 731 Days

## Summary

- **Year and season show the strongest differences in daily rentals.** Mean cnt is 2194 higher in yr 1 than yr 0 (bootstrap 95% CI 1951.9 to 2414.1; Mann-Whitney p = 7.06e-54, Holm p = 4.94e-53). Season is also significant (Kruskal-Wallis, epsilon-squared 0.344, a large effect).
- **Gradient boosting predicts cnt best without leakage.** On the 147-day test set it reached RMSE 662, MAE 463 and R² 0.891, against RMSE 2022 for the training-mean baseline. Dropping atemp improved it to RMSE 640 and R² 0.898.
- **Temperature is the most important feature once atemp is removed.** Shuffling temp raises test RMSE by 972.9, and shuffling yr raises it by 900.8. Temp and atemp correlate at 0.990, so their individual importances are unstable.
- **Holiday and workingday effects are weak or uncertain.** The unadjusted holiday gap is -792 rentals per day, and its interval includes zero. After adjusting for season and yr, the gap is -578 (CI -1082 to -45), but this rests on a 2-test correction and is tentative. Workingday is not significant after correction, and weekday shows no significant difference.
- **Weathersit 3 has low demand, but only 21 days support it.** Its mean is 1803, against 4877 for weathersit 1 and 4036 for weathersit 2.

## Data

- **Size:** 731 rows and 16 columns.
- **Target:** cnt, the daily rental count (regression). It has mean 4504.3, median 4548, SD 1937.2, minimum 22 and maximum 8714.
- **Missing values:** none in any column.
- **Excluded columns:** casual and registered, because cnt equals casual plus registered on all 731 rows. registered alone correlates 0.946 with cnt (linear R² 0.894), so it would leak the target. instant and dteday are identifiers and were not used as features.
- **Features used:** season, yr, mnth, holiday, weekday, workingday, weathersit, temp, atemp, hum and windspeed. There are no categorical or date/time features beyond these numeric codes.

## Findings

### Distribution and group differences

The distribution of cnt is mildly left-skewed, since the median (4548) sits slightly above the mean (4504.3).

![Distribution of daily cnt across 731 days](tasks/eda_1/charts/cnt_histogram.png)

- **Season:** Mean cnt rises from 2604 in season 1 to 5644 in season 3, with season 2 at 4992 and season 4 at 4728. Season 3 has the highest median (5353.5). Season 1 has n = 181.
- **Year:** Mean cnt is 3406 in yr 0 (median 3740) and 5600 in yr 1 (median 5927).
- **Month:** Mean cnt is lowest in January (2176) and peaks in mid-year, from May to September (5350 to 5772).
- **Holiday:** Holiday days average 3735 (n = 21) against 4527 for non-holidays (n = 710).
- **Workingday:** Working days average 4585 (n = 500) against 4330 for non-working days (n = 231).
- **Weekday:** The mean ranges only from 4229 (weekday 0) to 4690 (weekday 5).
- **Weathersit:** Means are 4877 for level 1 (n = 463), 4036 for level 2 (n = 247) and 1803 for level 3 (n = 21).
- **Temperature quartiles:** Mean cnt rises from 2615 in the coldest quartile to 5631 in the warmest.
- **Humidity quartiles:** The mean is 4378 in Q1 and 3879 in Q4, the lowest. The pattern is not monotone.
- **Windspeed quartiles:** The mean is 4923 in Q1 and 3978 in Q4, the lowest.

![Mean daily cnt by season and by weathersit](tasks/eda_1/charts/mean_cnt_by_season_weathersit.png)

### Significance tests

Ten tests were run, with Holm correction across all ten.

| Feature | Test | Raw p | Holm p | Effect | Survives at 0.05 |
|---|---|---|---|---|---|
| yr | Mann-Whitney U | 7.06e-54 | 4.94e-53 | rank-biserial 0.660 | Yes |
| season | Kruskal-Wallis | 4.11e-54 | 3.29e-53 | epsilon² 0.344 (large) | Yes |
| weathersit | Kruskal-Wallis | 2.59e-15 | 1.55e-14 | epsilon² 0.092 (medium) | Yes |
| temp | Spearman | 1.67e-79 | 1.51e-78 | rho 0.622 | Yes |
| atemp | Spearman | 9.62e-80 | 9.62e-79 | rho 0.623 | Yes |
| windspeed | Spearman | 2.97e-09 | 1.48e-08 | rho -0.217 | Yes |
| hum | Spearman | 0.0079 | 0.032 | rho -0.098 (very small) | Yes |
| holiday | Mann-Whitney U | 0.083 | 0.25 | rank-biserial -0.222 | No |
| workingday | Mann-Whitney U | 0.119 | 0.25 | rank-biserial 0.072 | No |
| weekday | Kruskal-Wallis | 0.631 | 0.631 | epsilon² 0.006 (negligible) | No |

- **Year:** The mean difference is 2194 rentals per day (yr 1 minus yr 0), with bootstrap 95% CI 1951.9 to 2414.1.
- **Holiday:** The unadjusted mean difference is -792 rentals per day, with bootstrap 95% CI -1672 to 101. It is not significant after the 10-test correction.
- **Workingday:** The mean difference is 255 rentals per day, with bootstrap 95% CI -52 to 561.

![Boxplots of daily cnt (rentals per day) by season and by weathersit level](tasks/stat_1/charts/cnt_by_season_weathersit.png)

### Interactions

- **Workingday × weathersit:** Not significant (OLS F = 0.515, p = 0.598; rank-based F = 0.850, p = 0.428). The change in the workingday effect (working minus non-working mean) is +437 at weathersit 1, +138 at weathersit 2 and -16 at weathersit 3. The weathersit 3 cells contain only 5 and 16 days, so that last value is unstable.
- **Year × season:** The two tests disagree. The OLS interaction is borderline (F = 2.43, p = 0.064), while the rank-based test is significant (F = 5.79, p = 0.00065). The yr 1 minus yr 0 change is +1865 in season 1, +2434 in season 2, +2360 in season 3 and +2127 in season 4. This interaction should be treated as tentative.

### Holiday effect, adjusted for season and year

This analysis used a separate 2-test Holm family. Its results are tentative and conditional on the season and yr controls.

- **Adjusted OLS:** The holiday coefficient is -578 rentals per day, with bootstrap 95% CI -1082 to -45 (2000 resamples). Raw p = 0.019, Holm p = 0.039.
- **Stratified permutation check:** The estimate is -570 (raw p = 0.020, Holm p = 0.039). All 8 season × yr strata contributed, and all 21 holiday days were used.
- **Effect of adjustment:** Adjustment shrinks the unadjusted gap of -792 to about -570 to -578. The adjusted CI excludes zero, while the unadjusted CI from the 10-test analysis includes zero.

![Holiday minus non-holiday difference in daily rentals: adjusted OLS with 95% bootstrap CI, stratified estimate, and unadjusted difference](tasks/stat_3/charts/holiday_adjusted_effect.png)

### Predictive models

Casual and registered were excluded as leakage. All models used the same split: 584 training rows and 147 test rows.

| Model | Test RMSE | Test MAE | Test R² | Train R² |
|---|---|---|---|---|
| Mean baseline (training mean 4561) | 2022 | 1712 | n/a | n/a |
| Linear regression | 831 | 617 | 0.828 | 0.791 |
| Random forest | 674 | 426 | 0.887 | 0.982 |
| Gradient boosting, with atemp | 662 | 463 | 0.891 | 0.954 |
| Gradient boosting, without atemp | 640 | 445 | 0.898 | 0.951 |

- Gradient boosting with atemp had the best test RMSE of the first three models. The random forest had a lower test MAE (426) but a larger train-test gap.
- **Permutation importance for gradient boosting with atemp (test RMSE increase):** yr 889, temp 656, hum 224, season 223, weathersit 110, windspeed 89, atemp 65, mnth 39, weekday 26, holiday 12, workingday 1.7.
- **Permutation importance without atemp (test RMSE increase):** temp 973, yr 901, hum 226, season 206, weathersit 119, windspeed 100, mnth 51, weekday 19, holiday 18, workingday 4.2. Across repeats, the no-atemp model has a standard deviation of 69.0 for temp and 51.8 for yr. The temp increase rose from 656 to 973 when atemp was removed, so the temp importance is not the same across the two models.
- **Collinearity:** Temp and atemp correlate at 0.990 on the training rows. Their individual importances are unstable, and unscaled linear coefficients (atemp 3488, temp 2097) are not comparable importances.
- **Linear model:** It ranks yr fourth by unscaled coefficient size (2024), behind atemp, temp and windspeed. The permutation results do not match this ranking, and the report does not treat the unscaled ranking as reliable.

![Permutation importance of each feature for the gradient boosting model, measured on the 147-day test set](tasks/ml_1/charts/ml_1_perm_importance.png)

## Limitations

- **Leakage excluded by design:** casual and registered were removed. registered alone gives a linear R² of 0.894 with cnt.
- **Year-by-season disagreement:** The OLS and rank-based tests disagree on the yr × season interaction (p = 0.064 against p = 0.00065). The analysis did not resolve this, and the interaction is reported only as tentative.
- **Holiday result depends on the correction family:** The unadjusted holiday effect is not significant across all 10 tests (Holm p = 0.25). The adjusted effect is significant only within the 2-test family used in the holiday analysis (Holm p = 0.039). Only 21 holiday days exist, so intervals are wide.
- **Workingday:** Not significant after correction (Holm p = 0.25). The interaction with weathersit is not significant.
- **Weathersit 3:** Based on 21 days. Its workingday interaction cells contain only 5 and 16 days, so those values are unstable.
- **Collinearity:** Temp and atemp correlate at 0.990. Permutation and linear importances for these two features are not reliable individually.
- **Superseded output:** One earlier permutation-importance output for gradient boosting without atemp had the wrong sign. It has been superseded by the corrected version with positive RMSE increases, which this report uses.
- **Small effect sizes:** Humidity (rho -0.098) and workingday have very small effects, even where they are significant or retained.
- **Modelling scope:** The models were evaluated on a single 147-day test split. No failed tasks or unresolved review objections were recorded.

## Open questions

- Does the yr effect reflect real growth in demand over time or a one-off shift between the two years? The analysis did not model a time trend.
- Does temp still explain cnt after controlling for season and month in a linear model? The analysis reported this only through the gradient boosting model.
- Is the yr × season interaction real? The OLS and rank-based tests disagree, and the analysis did not test it after controlling for temp.
- Is the holiday effect robust to dropping individual holiday days, or driven by one or two low-demand days? Is it unchanged once temp, weathersit and workingday are also controlled for?
- Is the low demand on weathersit 3 days robust, given that only 21 days exist?
- Do hum and season keep their importance after controlling for temp and yr, and does humidity act through weather conditions?
- Are test errors larger on high-demand days or on weathersit 3 days? The analysis did not examine residuals by group.