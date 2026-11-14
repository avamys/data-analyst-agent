# Bike Rental Demand (cnt): Distribution, Group Differences and Predictive Models

## Summary

- **Year is the largest and most robust effect.** Mean daily rentals for yr=1 exceed yr=0 by 2194 (95% CI 1962 to 2426, Cohen's d = 1.37). Adjusting for season and month leaves the estimate essentially unchanged at 2199.
- **Season and weathersit differ significantly, while holiday and workingday do not.** Season has eta-squared 0.347 (a large effect, about 35% of variance). Weathersit has eta-squared 0.099 (a medium effect). Holiday (p = 0.103) and workingday (p = 0.110) are not significant under the reported tests.
- **Gradient boosting predicts best among the non-leaky models.** On the 147-row test split, it reaches RMSE 662.3 and R² 0.891. Linear regression reaches RMSE 831.3 and R² 0.828. The mean baseline reaches RMSE 2022.2 and R² -0.020.
- **Weather and temperature features rank above calendar features under permutation, but this depends on grouping.** Under joint shuffling on the full test split, the weather group raises test RMSE by 1131.0 versus 920.9 for the calendar group. The ordering holds only when season is excluded from both groups. Counting season as calendar reverses it.
- **Interactions are weak.** The weathersit × season interaction is statistically significant (p = 0.016) but adds little to adjusted R² (from 0.7387 to 0.7422). The workingday × yr interaction is not significant (p = 0.123).

## Data

- **Size:** 731 daily rows and 16 columns.
- **Target:** cnt, the daily count of bike rentals (regression).
- **Features used:** season, yr, mnth, holiday, weekday, workingday, weathersit, temp, atemp, hum, windspeed (11 features). All are numeric; there are no categorical or date/time features.
- **Excluded:** casual and registered, because they sum exactly to cnt and are leakage. instant and dteday, an identifier and a date, are not used as features.
- **Missing values:** none in cnt or in the listed categorical columns, as confirmed by the EDA.
- **Leakage warning:** registered alone predicts the target almost perfectly (0.946 per the dataset profile).

## Findings

### Distribution of cnt and group means

cnt is roughly symmetric, with mean 4504.3, median 4548, standard deviation 1937.2, minimum 22, maximum 8714, and skew -0.047.

![Histogram of daily total rentals (cnt) across 731 days](tasks/eda_1/charts/cnt_histogram.png)

- **Season** (mean / median cnt): winter (1) 2604 / 2209 (181 rows); spring (2) 4992 / 4941.5 (184); summer (3) 5644 / 5353.5 (188); fall (4) 4728 / 4634.5 (178).
- **Year** (mean / median): yr=0, 3406 / 3740 (365 rows); yr=1, 5600 / 5927 (366 rows).
- **Month:** mean cnt rises from 2176 in January (median 1939) to a peak of 5772 in June (median 5308.5). September (5767) is the second-highest monthly mean. Mean cnt falls to 3404 in December (median 3444).
- **Weekday** (codes 0 to 6): mean cnt ranges from 4229 (code 0) to 4690 (code 5). The EDA describes these differences as modest. No weekday significance test was reported.
- **Holiday:** 710 non-holiday days, mean 4527 / median 4558; 21 holidays, mean 3735 / median 3351.
- **Workingday:** 231 non-working days, mean 4330 / median 4459; 500 working days, mean 4585 / median 4582.
- **Weathersit:** level 1 has 463 rows, mean 4877 / median 4844; level 2 has 247 rows, mean 4036 / median 4040; level 3 has 21 rows, mean 1803 / median 1817. The level-3 estimate is less stable because of its small count.

### Significance tests and effect sizes

Tests were run for yr, holiday, workingday, season and weathersit. Holm correction was applied across the five features.

![Mean daily rentals (cnt) by level of yr, holiday, workingday, season and weathersit, with 95% confidence intervals for each mean](tasks/stat_1/charts/stat1_mean_cnt_by_feature.png)

- **yr:** Welch t = 18.58, p = 1.05e-62 (Holm across five: 4.19e-62). Mann-Whitney p = 7.06e-54. The yr=1 minus yr=0 difference is 2194 (95% CI 1962 to 2426), with Cohen's d = 1.37, a very large effect.
- **season:** one-way ANOVA F = 128.77, p = 6.72e-67 (Holm across five: 3.36e-66). Kruskal-Wallis p = 4.11e-54. Eta-squared = 0.347, a large effect. Pairwise Welch contrasts, Holm-adjusted within season:
  - spring vs winter: +2388 (CI 2068 to 2708)
  - summer vs winter: +3040 (CI 2747 to 3333)
  - fall vs winter: +2124 (CI 1800 to 2448)
  - summer vs spring: +652 (CI 329 to 975), Holm p = 1.7e-4
  - fall vs spring: -264 (CI -615 to 87), Holm p = 0.14, not significant
  - fall vs summer: -916 (CI -1243 to -590), Holm p = 2.0e-7
- **weathersit:** one-way ANOVA F = 40.07, p = 3.11e-17 (Holm across five: 9.32e-17). Kruskal-Wallis p = 2.59e-15. Eta-squared = 0.099, a medium effect. Pairwise Welch contrasts, Holm-adjusted within feature:
  - level 2 vs 1: -841 (CI -1125 to -557), Holm p = 2.1e-8
  - level 3 vs 1: -3074 (CI -3660 to -2487), Holm p = 2.6e-10
  - level 3 vs 2: -2233 (CI -2835 to -1630), Holm p = 3.0e-8
  - The level-3 contrasts rest on 21 rows, so their estimates are imprecise.
- **holiday:** Welch t = -1.70, p = 0.103 (Holm across five: 0.206). Mann-Whitney p = 0.083. Holiday days average 792 fewer rentals (CI -1758 to 174). Cohen's d = -0.41, a small-to-medium effect that is not significant. Only 21 days are holidays, so the estimate is imprecise.
- **workingday:** Welch t = 1.60, p = 0.110 (Holm across five: 0.206). Mann-Whitney p = 0.119. Working days average 255 more rentals (CI -58 to 567). Cohen's d = 0.13, negligible; not significant.

### Interactions

Both interaction tests are nested F-tests added to an additive OLS model of cnt on weathersit, season, workingday and yr. This breakdown is exploratory.

- **weathersit × season:** F = 2.64 on 6 df, p = 0.016. Adjusted R² rises from 0.7387 to 0.7422, a very small gain. The weathersit 3 cells contain only 3 to 10 rows each.
- **Joint test (both interactions added):** F = 2.68 on 7 df, p = 0.0097.
- **Cell means, weathersit × season** (row counts in brackets):
  - Weathersit 1: winter 2811.1 (111), spring 5548.5 (113), summer 5878.3 (136), fall 5043.6 (103).
  - Weathersit 2: winter 2357.2 (66), spring 4236.7 (68), summer 5222.5 (48), fall 4654.0 (65).
  - Weathersit 3: winter 934.8 (4), spring 1169.0 (3), summer 2751.8 (4), fall 1961.6 (10).
- **Seasonal swing:** weathersit 2 is not clearly smaller than weathersit 1, so the claim of a smaller seasonal swing is weak for level 2. The weathersit 3 pattern is smaller, but it rests on 3 to 10 rows per season cell.
- For weathersit 1 and 2, mean cnt peaks in spring and summer rather than in summer and fall. Winter is lowest in both. Fall falls below summer in every weathersit.

![Mean daily rentals (cnt) for each interaction cell: weathersit by season (left) and workingday by yr (right)](tasks/stat_2/charts/interaction_means.png)

- **workingday × yr:** F = 2.38 on 1 df, p = 0.123. Adjusted R² moves from 0.7387 to 0.7392. Cell means: for yr=0, non-working days 3363.8 (n=115) and working days 3425.1 (n=250); for yr=1, non-working days 5288.2 (n=116) and working days 5744.6 (n=250). The pattern is suggestive but not established, so it does not warrant a further breakdown by yr.

### Year effect after adjustment for season and month

- Unadjusted OLS coefficient for yr: 2194 (CI 1962 to 2426, p = 2.5e-63).
- Adjusted for season and mnth as categorical controls: 2199 (CI 2054 to 2345, p = 9.2e-127). Adjustment changes the coefficient by only about 5 rentals.
- Partial eta-squared for yr, given season and mnth, is 0.552. The adjusted coefficient is 2.20 residual standard deviations (residual SD about 1002). The adjusted model has R² = 0.738.
- Season and month absorb none of the yr=0 to yr=1 gap, so the effect is not mainly explained by seasonal or monthly differences. The analysis cannot tell a step change between years from a continuous trend, because the model uses only a yr indicator. The p-values assume independent days, which likely overstates precision for daily data.

### Predictive models

Models were trained on 80% of the rows and tested on 147 rows (80/20 split, seed 42), using the 11 non-leaky features.

| Model | Test RMSE | Test MAE | Test R² |
|---|---|---|---|
| Mean baseline | 2022.2 | 1712.0 | -0.020 |
| Linear regression | 831.3 | 617.4 | 0.828 |
| Gradient boosting | 662.3 | 462.8 | 0.891 |

- Gradient boosting has the lowest test RMSE of the three, about 67% below the mean baseline. Linear regression is clearly better than the mean baseline.
- Linear regression's largest coefficients by absolute value are atemp (3488), temp (2097), windspeed (2081) and yr (2024). Its train R² is 0.791.
- Gradient boosting's train R² is 0.954. Its impurity-based feature importances are led by temp (0.386) and yr (0.304), followed by season (0.096) and atemp (0.073).

![Test RMSE by model on 11 non-leaky features; lower is better](tasks/ml_1/charts/ml1_model_rmse.png)

- **Leakage check (not used):** gradient boosting including registered reaches R² 0.980 (RMSE 282.0). This is leakage, since registered is a component of cnt, so it is excluded from all models.

### Feature importance (permutation, test split)

Permutation importance was computed for the best model (gradient boosting) on the 147-row test split, with 30 repeats and seed 42. Each value is the RMSE increase when that feature is shuffled.

- yr: 889.3 (sd 53.6)
- temp: 656.5 (sd 55.8)
- hum: 224.5 (sd 25.2)
- season: 222.7 (sd 31.0)
- weathersit: 110.3 (sd 16.8)
- windspeed: 88.7 (sd 24.0)
- atemp: 65.4 (sd 22.0)
- mnth: 39.1 (sd 11.7)
- weekday: 26.0 (sd 13.6)
- holiday: 12.1 (sd 14.0)
- workingday: 1.7 (sd 9.2)

The impurity-based and permutation rankings disagree: impurity importance puts temp first, while permutation importance puts yr first. The two measures are not reconciled here.

- **Group comparison, season excluded from both groups:** weather and temperature features (temp, atemp, hum, windspeed, weathersit) sum to 1145.3. Calendar features (yr, mnth, weekday, holiday, workingday) sum to 968.1. Weather exceeds calendar.
- **Group comparison, season counted as calendar:** calendar sums to 1190.7 and weather to 1145.3. The ordering reverses.

### Stability of the weather-versus-calendar comparison

Temp and atemp are almost perfectly correlated (r = 0.992). Correlations of hum with temp (r = 0.127) and with atemp (r = 0.140) are weak. Because of the temp–atemp correlation, individual permutation credits for these features are split and unreliable.

- **Joint shuffling of temp, atemp and hum:** RMSE increase 1005.7 (sd 69.0). This is larger than the sum of their three individual increases in the earlier permutation run.
- **Joint weather group** (temp, atemp, hum, windspeed, weathersit): 1131.0 on the full test split. A separate run recorded 1109.1 (sd 64.6) for the same group. Both runs used seed 42 but different random draws, and the difference between them is attributed to repeat-to-repeat noise.
- **Joint calendar group** (yr, mnth, weekday, holiday, workingday): 920.9 (sd 69.0) on the full test split.
- **Five random 50% test subsets** (10 repeats each): the weather group ranges from 1027.9 to 1236.1, and the calendar group ranges from 752.1 to 1013.6. The lowest weather value exceeds the highest calendar value, so weather exceeds calendar on every subset. The size of the gap varies across subsets; the direction does not.
- The ordering depends on season being excluded from both groups, as in the earlier group comparison.

## Limitations

- **Unresolved review issue (month peak).** The EDA's month sentence named September as the peak. The group means show June has the highest monthly mean (5772), with September (5767) second. This report uses June. The review objection to the EDA's month sentence stands, and it affects only the monthly description under Distribution of cnt.
- **Trend versus step change.** The yr effect is not explained by season or month. The analysis does not test whether the gap is a continuous trend or a step change, because yr is a two-level indicator.
- **Independence of days.** The p-values and confidence intervals assume independent days. Daily data are likely autocorrelated, so they probably overstate precision. Autocorrelation was not checked.
- **Small groups.** Weathersit level 3 has 21 rows (3 to 10 per season cell). Holiday has 21 rows. Their estimates are imprecise.
- **Interaction results.** The weathersit × season interaction is significant but adds little to adjusted R². The cell-level breakdown is exploratory. The workingday × yr pattern is not established.
- **Model evaluation.** Model scores come from one 147-row test split with one seed. Gradient boosting's train R² (0.954) is well above its test R² (0.891), and this gap was not examined further.
- **Permutation importance.** Correlated features (temp, atemp, hum) share credit, so their individual rankings are indicative only. The weather-versus-calendar ordering depends on whether season is counted in a group. Its magnitude varies across splits, and the two runs of the joint weather value (1131.0 and 1109.1) differ by an amount attributed to noise.
- **Leakage.** registered and casual were excluded. The registered leakage check is reported only to show the effect of including it.
- **Failed tasks.** None. All tasks completed.

## Open questions

- Does a continuous time trend (for example, days since the start of the series) or a within-year trend explain the yr=0 to yr=1 gap better than a yr indicator?
- Are the residuals from the season and month model autocorrelated, and do HAC or block-bootstrap intervals for the yr effect remain as narrow as the reported ones?
- How much of the yr effect is explained by weather (temp, hum, windspeed, weathersit) once these are added to the model?
- Does the yr effect remain after controlling for season and month, or is it a trend over time? Only the season-and-month adjustment has been answered.
- Does the weathersit 3 effect (21 rows) justify separate modelling, or does it need pooling with weathersit 2?
- How much of the season and month effect is explained by temp and atemp?
- Does the weathersit × season interaction hold after pooling weathersit 2 and 3, and is it driven by weathersit 1 alone?
- Does the workingday × yr gap survive controlling for temp and month?
- How much of the gain from gradient boosting over linear regression comes from non-linear temperature effects?
- Are the permutation importances stable under other test splits or cross-validation folds, and what confidence interval does the weather-versus-calendar gap have across many more splits?