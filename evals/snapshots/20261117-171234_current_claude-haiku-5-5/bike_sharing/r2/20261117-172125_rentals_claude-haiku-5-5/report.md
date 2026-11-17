# Daily Rental Counts (cnt): Analysis of 731 Days

## Summary

- **Year and season show the largest significant differences in daily rentals.** Rentals with yr=1 averaged 5599.9 against 3405.8 for yr=0, a gap of 2194.2 (Welch 95% CI 1962.3 to 2426.1, p=1.05e-62). Season is also significant (Kruskal-Wallis p=4.1e-54), with season 3 averaging 5644.3 and season 1 averaging 2604.1. Both effects persist, with smaller estimates, in a joint model.
- **Weather is a significant association with rentals.** Heavy weather (weathersit 3, 21 days) averages 1803.3 against 4876.8 for clear weather, and light precipitation (weathersit 2) averages 4035.9. Both differences hold in a joint model that also controls for season, workingday and holiday.
- **Working day and holiday effects are small or uncertain.** Working days average 254.7 more rentals than non-working days, not significant in the one-feature test (p=0.110), but significant in the joint model (+204.8, p=0.0119). Holiday days average 792.1 fewer, but rest on 21 days and are not significant in the one-feature test (p=0.103).
- **The random forest predicts cnt best on the shared split.** Test RMSE is 690.3 for the random forest and 831.3 for linear regression, against 2022.2 for the mean baseline. The random forest's most important features are temp, yr and atemp.
- **The weathersit x season interaction is fragile.** It is significant without covariates (p=0.025) but not after adjusting for temp, hum and month (p=0.192). The weathersit x workingday interaction is not significant (p=0.598).

## Data

- **Size:** 731 rows and 16 columns.
- **Target:** cnt, daily total rentals (range 22 to 8714, median 4548.0).
- **Features used:** 11 columns: season, yr, mnth, holiday, weekday, workingday, weathersit, temp, atemp, hum, windspeed. The columns instant and dteday were not used as features, and casual and registered were excluded because they leak the target. The registered column alone correlates with cnt at about r=0.946.
- **Missing values:** none. The total empty-cell count is 0 across all 16 columns.
- **Zero values:** most zeros are category codes (yr, holiday, weekday, workingday). hum has one exact zero, and windspeed has none. See Findings: Data quality.

## Findings

### Distribution of cnt

cnt is roughly symmetric: mean 4504.3, median 4548.0, skew -0.05, standard deviation 1937.2, over 731 days. The most populated histogram bin holds 49 days and starts near 4078.

![Histogram of daily total rentals (cnt) with mean and median marked](tasks/eda_1/charts/cnt_histogram.png)

### Differences in cnt by group

Group means and medians (n in brackets):

- **Season:** 1: 2604.1 / 2209.0 (181); 2: 4992.3 / 4941.5 (184); 3: 5644.3 / 5353.5 (188); 4: 4728.2 / 4634.5 (178).
- **Year:** yr=0: 3405.8 / 3740.0 (365); yr=1: 5599.9 / 5927.0 (366).
- **Month:** January is lowest at 2176.3 (n=62). June is highest at 5772.4 (n=60), with September second at 5766.5 (n=60). November is 4247.2 and December is 3403.8.
- **Weekday (codes 0 to 6):** group means run from 4228.8 (code 0) to 4690.3 (code 5).
- **Workingday:** non-working day (0) 4330.2 (n=231); working day (1) 4584.8 (n=500).
- **Holiday:** not a holiday 4527.1 (n=710); holiday 3735.0 (n=21).
- **Weathersit:** clear 4876.8 (n=463); light precipitation 4035.9 (n=247); heavy weather 1803.3 (n=21).

Spread between the highest and lowest group mean, largest first: month 3596.0, weathersit 3073.5, season 3040.2, year 2194.2, holiday 792.1, weekday 461.5, workingday 254.7. Month and weathersit have the largest spreads, followed by season.

![Mean daily rentals (cnt) per group for each categorical-like feature](tasks/eda_1/charts/cnt_mean_by_group.png)

### Statistical tests and effect sizes (one feature at a time)

- **Year:** yr=1 minus yr=0 is +2194.2 (Welch 95% CI 1962.3 to 2426.1; t=18.578; p=1.05e-62; Cohen d=1.374; Mann-Whitney p=7.06e-54).
- **Season:** Kruskal-Wallis H=250.934, p=4.1e-54; ANOVA F=128.77, p=6.7e-67; eta-squared=0.347. Against season 1, Welch differences are: season 2 +2388.2 (Holm-adjusted p=4.1e-38); season 3 +3040.2 (Holm-adjusted p=5.5e-62); season 4 +2124.0 (Holm-adjusted p=2.4e-31). Confidence intervals are unadjusted.

![Mean daily cnt by season with Welch pairwise comparisons vs season 1](tasks/stat_1/charts/cnt_mean_by_season_stat.png)

- **Weathersit:** Kruskal-Wallis H=67.175, p=2.6e-15; ANOVA F=40.066, p=3.1e-17; eta-squared=0.099. Against clear weather, light precipitation is -840.9 (95% CI -1124.8 to -557.0; Holm-adjusted p=1.0e-08), and heavy weather is -3073.5 (95% CI -3660.0 to -2487.0; Holm-adjusted p=1.8e-10). The heavy-weather comparison rests on 21 days.
- **Workingday:** +254.7 (Welch 95% CI -57.9 to 567.2; p=0.110; Cohen d=0.132; Mann-Whitney p=0.119). Not significant.
- **Holiday:** -792.1 (95% CI -1758.4 to 174.2; p=0.103; Cohen d=-0.41; Mann-Whitney p=0.083). Not significant, and based on 21 holiday days. This is a non-significant association, not a causal effect.

### Joint model: effects controlling for each other

An OLS model with yr, season, weathersit, workingday and holiday (R² 0.743) was fitted without and with month (R² 0.807).

- **Year:** +2133.3 without month (95% CI 1989.6 to 2277.0; p=4.8e-124) and +2134.6 with month (95% CI 2009.0 to 2260.1; p=1.17e-147). Essentially unchanged by month.
- **Season (vs season 1):** without month, season 2 is +2366.0 (p=1.39e-87), season 3 is +2951.0 (p=7.85e-121), and season 4 is +2214.3 (p=6.16e-78). With month, the estimates fall to +903.5 (season 2, p=7.84e-06), +1167.0 (season 3, p=1.02e-06) and +1833.3 (season 4, p=7.38e-19). The analysis reports these as about 62%, 60% and 17% smaller than the no-month values, respectively. Season is the feature most confounded with month.
- **Weathersit (vs clear):** without month, light precipitation is -697.5 (p=4.33e-18) and heavy weather is -2647.0 (p=5.01e-30). With month, these are -711.2 (p=4.11e-23) and -2576.6 (p=1.49e-35). The heavy-weather estimate rests on 21 days.
- **Workingday:** without month, +204.8 (95% CI 45.3 to 364.4; p=0.0119). With month, +206.0 (95% CI 66.4 to 345.6; p=0.00388). Significant in the joint model, though small (about 200 rentals per day). This disagrees with the one-feature result (p=0.110). The analysis reports both and does not resolve the difference; the joint estimate is the one that adjusts for the other features.
- **Holiday:** without month, -558.8 (95% CI -1002.7 to -114.9; p=0.0137). With month, -400.7 (95% CI -791.6 to -9.7; p=0.0446). The joint interval excludes zero only narrowly and rests on 21 holiday days, so the analysis calls this fragile.

### Interactions

- **Weathersit x season:** significant at the 0.05 level (ANOVA F=2.425 on 6 df, p=0.025), and adding it raises R² from 0.436 to 0.447. Cell means: in season 1, clear 2811.1 (n=111) and mist 2357.2 (n=66); in season 2, clear 5548.5 (n=113) and mist 4236.7 (n=68). Weathersit 3 cells have n=4 to 5 and are unstable.
- **Weathersit x season after adjustment:** with temp, hum and month as covariates, the interaction gives F=1.452 on 6 df, p=0.192, and R² rises only from 0.564 to 0.569. The interaction does not hold at the 0.05 level once these covariates are included. The analysis suggests the earlier association is largely carried by temperature, humidity and month, but did not test this directly with a mediation analysis.
- **Weathersit x workingday:** not significant (F=0.515 on 2 df, p=0.598; R² 0.105 to 0.107). This is a non-detection at this sample size, not evidence that the weather effect is the same on both day types. Cell means: non-working days, clear 4587.3 (n=156), mist 3936.8 (n=70), heavy 1815.4 (n=5); working days, clear 5023.9 (n=307), mist 4075.0 (n=177), heavy 1799.5 (n=16).

![Mean daily cnt by weathersit within each season (left) and workingday (right)](tasks/stat_2/charts/stat2_interaction_means.png)

### Prediction on one shared split

The split is a single train/test split with seed 42: 584 training rows and 147 test rows, using the 11 features.

| Model | Test RMSE | Test MAE | Test R² | Train R² |
|---|---|---|---|---|
| Mean baseline (train mean 4561.0) | 2022.2 | 1712.0 | n/a | n/a |
| Linear regression | 831.3 | 617.4 | 0.828 | 0.791 |
| Random forest (300 trees, min leaf 2) | 690.3 | 435.0 | 0.881 | 0.970 |

- The random forest's test RMSE is 17.0% lower than linear regression's. The analysis prefers the random forest, but notes it overfits more (train R² 0.970 versus test 0.881).
- **Random forest importance:** temp 0.365, yr 0.287, atemp 0.143, hum 0.058, season 0.054, windspeed 0.029, mnth 0.028, weekday 0.016, weathersit 0.016, workingday 0.005.
- **Linear regression coefficients (largest magnitude):** atemp +3488.0, temp +2097.2, windspeed -2080.5, yr +2024.0, hum -865.4, weathersit -632.9, season +524.7, holiday -391.6, workingday +160.8, weekday +72.9. Both atemp and temp carry large positive coefficients; the analysis flags their collinearity as an open question.

![Test RMSE of predicting cnt on the 147-row test set: mean baseline vs linear regression vs random forest](tasks/ml_2/charts/ml2_test_rmse.png)

### Data quality

- **Zero values:** hum=0 occurs in 1 row, with cnt 623 against a mean of 4509.7 for the other rows. One row cannot establish a relationship. windspeed has no exact zeros. Windspeed below 0.05 covers 6 rows, with mean cnt 4229.7 versus 4506.6 for the others, a difference the analysis describes as small and based on 6 rows.
- **Category codes:** zeros in yr (365), holiday (710), weekday (105) and workingday (231) are category codes, not sentinels.
- temp, atemp, casual, registered and cnt have no zeros.

![Mean cnt for the single hum=0 row compared with all other rows](tasks/eda_2/charts/hum_zero_mean_cnt.png)

## Limitations

- **Association, not causation.** All findings are associations in observational daily data. Statements about holidays, weather and season do not establish causes.
- **Small groups.** Heavy weather (weathersit 3) and holiday each have 21 days. Weathersit 3 cells within season have n=4 to 5, and the non-working weathersit 3 cell has n=5. Estimates for these groups are unstable.
- **Fragile holiday and working-day results.** The holiday effect is not significant in the one-feature test and only narrowly significant in the joint model. Workingday changes from non-significant (one feature) to significant (joint model).
- **Interaction results depend on covariates.** The weathersit x season interaction is significant without covariates and not with them. The weathersit x workingday test is a non-detection.
- **Collinearity.** temp and atemp are highly collinear, which affects how their linear coefficients should be read. Season and month are also strongly related, so the season effect shrinks sharply when month is added.
- **Feature count discrepancy.** The ML task text states 12 features, but dropping instant, dteday, casual, registered and cnt leaves 11. The 11-feature list was used.
- **Single zero-value row.** The hum=0 row is one observation and was not removed or tested.
- **Unresolved review issues (eda_1).** The lead's review found two errors in the eda_1 write-up. June (5772.4), not September (5766.5), has the highest monthly mean, and the largest spreads are month (3596.0) and weathersit (3073.5), ahead of season (3040.2). This report states both correctly. The review also asked that the holiday result be stated as an association given only 21 holiday days; this report does so. The eda_1 task record still carries the uncorrected text.
- **No failed tasks** are recorded in the accepted results.

## Open questions

- Does the yr=0 to yr=1 gap persist after controlling for season and month, and does it reflect growth in the system? The joint model keeps the year effect near +2134.6 with month included, but the analysis did not examine growth directly.
- Are the weathersit 3 (21 days) and holiday (21 days) groups large enough for reliable separate estimates or a model? Should heavy weather be pooled with mist?
- Do temperature and humidity explain the season and weather effects better than the categorical labels? The interaction result suggests they may, but this was not tested directly.
- Does the weathersit x season effect differ within narrow temperature bands?
- Is the season effect identifiable separately from month, given that season is nearly a function of month?
- Is the holiday effect stable across the 21 holiday days, for example by leave-one-out or permutation testing?
- Does adding month and weekday effects, or a continuous time index in place of the binary yr flag, reduce random forest or linear test RMSE further?
- Are the near-zero windspeed readings a measurement floor, and do they cluster by date or season? Is the single hum=0 row a data-entry error, and does removing it change the models?
- Do the holiday and weekday zeros carry different cnt levels, which would make them informative rather than sentinels?