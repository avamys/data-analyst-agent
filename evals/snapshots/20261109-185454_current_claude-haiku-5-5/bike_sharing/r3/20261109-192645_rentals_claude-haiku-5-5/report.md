# Bike Rental Demand: Distribution, Drivers and Model Benchmarks (Target: cnt)

## Summary

- **Demand differs most by year and season.** Mean daily rentals were 3405.8 in 2011 (yr=0) and 5599.9 in 2012 (yr=1), a difference of 2194 (95% CI 1962 to 2426, Welch p = 1.0e-62). Season has a large, significant effect (one-way ANOVA F = 128.8, p = 6.7e-67, eta-squared = 0.347). Season 1 has the lowest mean (2604.1) and season 3 the highest (5644.3).
- **Weather and temperature are the strongest measured correlates.** Mean cnt is 4876.8 in clear weather (weathersit 1), 4035.9 in misty weather (2) and 1803.3 in the heavy-weather level (3, n=21). Spearman rho with temp is 0.622 and with windspeed -0.217.
- **Working day and holiday effects are small and not significant at 5%.** The working-day difference is 255 (p = 0.110); the holiday difference is -792 (p = 0.103, only 21 holiday rows). Working day does vary by season: its effect is positive in seasons 1, 3 and 4 and negative in season 2, with a small interaction effect (partial eta-squared = 0.013 unadjusted, 0.0213 adjusted).
- **Without the leaky columns, the best model reaches test R² 0.887 on a random split, but does not generalise across years.** The random forest's test RMSE is 674.2 against 2022.2 for the mean baseline. On a time-ordered split (train 2011, test 2012), both models have negative test R² (-0.567 and -0.697), although they beat the training-mean baseline on error.
- **Adding casual and registered inflates the score.** The random forest reaches test R² 0.998 with them, but these columns are parts of the cnt total, so that score is not a forecasting result.

## Data

- 731 daily rows and 16 columns. Target: `cnt` (daily bike rentals).
- Missing values: none in any of the 16 columns.
- Excluded from modelling: `casual` and `registered` (leakage, since both are parts of the cnt total; registered correlates 0.9455 with cnt), and `instant` and `dteday` (identifiers). This leaves 11 features.
- No categorical or date/time features were identified in the profile.
- Mean cnt is 4504.3, median 4548.0, standard deviation 1937.2, range 22 to 8714.

## Findings

### Distribution and descriptive patterns (eda_1)

cnt is roughly symmetric across the 731 days, with mean 4504.3 and median 4548.0.

![Histogram of daily bike rentals (cnt) across 731 days](tasks/eda_1/charts/cnt_histogram.png)

**Season.** Means by season code are: season 1 mean 2604.1 (median 2209.0, n=181); season 2 mean 4992.3 (median 4941.5, n=184); season 3 mean 5644.3 (median 5353.5, n=188); season 4 mean 4728.2 (median 4634.5, n=178). Season codes are used throughout this report.

**Month.** Mean cnt rises from January (2176.3, median 1939.0, n=62) to March (3692.3) and April (4484.9, median 4293.5). It peaks in September (5766.5, median 5384.0) and falls to December (3403.8, median 3444.0, n=62).

![Mean daily bike rentals (cnt) by month (left) and by season (right)](tasks/eda_1/charts/cnt_mean_by_month_season.png)

**Year.** 2011 (yr=0, n=365) has mean 3405.8 and median 3740.0. 2012 (yr=1, n=366) has mean 5599.9 and median 5927.0.

**Holiday.** Non-holiday days (n=710) average 4527.1 (median 4558.0). Holidays (n=21) average 3735.0 (median 3351.0). The holiday group is small.

**Working day.** Non-working days (n=231) average 4330.2 (median 4459.0). Working days (n=500) average 4584.8 (median 4582.0).

**Weekday.** Means stay in a narrow band. Weekday 0 is lowest at 4228.8 (median 4334.0, n=105), and weekday 3 is 4548.5 (median 4642.5, n=104). Weekday 5 has mean 4690.3.

**Weather.** Clear weather (weathersit 1, n=463) averages 4876.8 (median 4844.0). Misty weather (2, n=247) averages 4035.9 (median 4040.0). Heavy weather (3, n=21) averages 1803.3 (median 1817.0).

### Significance and effect sizes (stat_1)

- **Year:** Welch t-test p = 1.0e-62. The 2012 mean is 2194 higher (95% CI 1962 to 2426).
- **Holiday:** Welch t-test p = 0.103. Holiday days average 792 fewer rentals (95% CI -1758 to 174). Only 21 rows are holidays, so this result cannot distinguish a small effect from none.
- **Working day:** Welch t-test p = 0.110. Working days average 255 more rentals (95% CI -58 to 567).
- **Season:** One-way ANOVA F = 128.8, p = 6.7e-67, eta-squared = 0.347. Kruskal-Wallis p = 4.1e-54.
- **Weathersit:** One-way ANOVA F = 40.1, p = 3.1e-17, eta-squared = 0.099. Kruskal-Wallis p = 2.6e-15. This is a significant effect, smaller than season's.
- **Temp:** Spearman rho = 0.622 (95% CI 0.575 to 0.665), p = 1.7e-79, n = 731.
- **Atemp:** Spearman rho = 0.623 (95% CI 0.576 to 0.665), p = 9.6e-80, n = 731.
- **Humidity:** Spearman rho = -0.098 (95% CI -0.169 to -0.026), p = 0.008. This is a weak negative correlation.
- **Windspeed:** Spearman rho = -0.217 (95% CI -0.285 to -0.147), p = 3.0e-9.

![Boxplots of daily bike rentals (count) by season and by weather situation](tasks/stat_1/charts/cnt_by_season_weathersit.png)

### Interactions (stat_2)

**Working day × season.** The unadjusted interaction is significant at 0.05 (F-test p = 0.023). It remains significant after Bonferroni correction over the two interaction tests. The partial eta-squared is 0.013, a small effect, so the result should be treated with caution and not as a headline finding.

Cell means by season code:

| Season | Non-working mean (n) | Working mean (n) |
|---|---|---|
| 1 | 2257.1 (61) | 2780.5 (120) |
| 2 | 5142.4 (56) | 4926.7 (128) |
| 3 | 5474.7 (57) | 5718.1 (131) |
| 4 | 4606.2 (57) | 4785.6 (121) |

The working-day gap is not uniform in direction: it is negative only in season 2.

![Mean cnt by season, split by workingday (counts of rentals per day)](tasks/stat_2/charts/wd_season_means.png)

**Working day × year.** The unadjusted interaction is significant at 0.05 (F-test p = 0.027). After Bonferroni correction over the two interaction tests, it is no longer significant at 0.05. The partial eta-squared is 0.0067, a negligible effect, so this interaction is not reported as a finding.

Cell means by year (non-working, working): yr 0 is 3363.8 (n=115) and 3425.1 (n=250); yr 1 is 5288.2 (n=116) and 5744.6 (n=250).

**Temp × weathersit.** The interaction is not significant (F-test p = 0.40). Within-weathersit slopes of cnt on temp are 6117 (weathersit 1, 95% CI 5413 to 6822, n=463), 6979 (weathersit 2, 95% CI 5938 to 8020, n=247) and 5725 (weathersit 3, 95% CI 2125 to 9325, n=21, too few to interpret).

Mean cnt by temperature tercile and weathersit:
- Weathersit 1: 3058.4 (low, n=144), 5580.2 (mid, n=147), 5798.0 (high, n=172).
- Weathersit 2: 2765.8 (low, n=95), 4485.8 (mid, n=82), 5232.4 (high, n=70).
- Weathersit 3: 1085.6 (low, n=5), 2039.9 (mid, n=15), 1842.0 (high, n=1). These cells are too thin to interpret.

### Working day × season after adjustment (stat_3)

After adjusting for temp, weathersit and yr, the working day × season interaction is significant (F = 5.223, p = 0.0014). The partial eta-squared is 0.0213, a small effect. The adjusted result is stronger than the unadjusted one (p = 0.023 in stat_2). Both results are reported as found.

Adjusted working-minus-non-working gaps (covariates at sample values): +517 (season 1), -228 (season 2), +247 (season 3), +221 (season 4). Adjusted means are 3219.7 (season 1, non-working) and 3736.3 (season 1, working), and 4903.0 (season 2, non-working) and 4675.0 (season 2, working).

The adjusted and unadjusted patterns agree in direction. The working-day × year effect was not re-estimated after adjustment.

![Adjusted mean daily rentals (cnt) for non-working (0) and working (1) days within each season code, adjusted for temp, weathersit and yr](tasks/stat_3/charts/wd_season_adj_means.png)

### Predictive models (ml_1)

Models were trained on 584 rows and tested on 147 (80/20 random split, random_state 42). The 11 features are used; casual and registered are excluded.

| Model | Train R² | Test R² | Test RMSE | Test MAE |
|---|---|---|---|---|
| Mean baseline | – | – | 2022.2 | 1712.0 |
| Linear regression | 0.791 | 0.828 | 831.3 | 617.4 |
| Random forest (300 trees) | 0.982 | 0.887 | 674.2 | 426.2 |

Both models beat the mean baseline. The random forest beats linear regression on the test set. The random forest's train-test gap (0.982 vs 0.887) is larger than linear regression's (0.791 vs 0.828).

![Test RMSE of mean baseline, linear regression and random forest predicting daily bike rental count cnt](tasks/ml_1/charts/model_test_rmse.png)

**Feature importance.** Random-forest permutation importance (increase in test RMSE when shuffled, 20 repeats): yr 925.6, temp 608.4, hum 220.4, atemp 193.1, season 135.7, mnth 104.5, windspeed 59.3, weathersit 50.9, weekday 14.3, workingday 10.0, holiday 1.1.

Temp and atemp correlate at 0.9917, so their separate linear-regression coefficients (atemp 3488.0, temp 2097.2) cannot be read as individual effects. The permutation ranking is the more reliable guide.

### Leaky columns (ml_2)

On the same split, the random forest with casual and registered added (13 features) reaches test RMSE 99.9, R² 0.998. Without them (11 features), test RMSE is 674.2, R² 0.887. Adding the leaky columns lowers test RMSE by 574.3.

In the 13-feature forest, registered has importance 0.896 and casual 0.098; all other features are below 0.001. The 11-feature model's test RMSE is 33% of the baseline RMSE (2022.2). The leaky columns are parts of the cnt total, so the 13-feature score does not measure forecasting skill.

![Test RMSE of cnt for the mean baseline and random forest with and without casual and registered](tasks/ml_2/charts/ml2_leaky_rmse.png)

### Time-ordered split (ml_3)

Train on yr=0 (2011, n=365), test on yr=1 (2012, n=366).

| Model | Train R² | Test R² | Test RMSE | Test MAE |
|---|---|---|---|---|
| Training-mean baseline | – | – | 2829.3 | 2488.7 |
| Linear regression | 0.759 | -0.697 | 2326.6 | 2126.1 |
| Random forest | 0.981 | -0.567 | 2235.6 | 2080.3 |

Both fitted models have lower test RMSE and MAE than the baseline. Both have negative test R², so they do worse than predicting the 2012 mean. The random forest has lower RMSE and MAE than linear regression on this split. The gap is smaller than on the random split (2235.6 vs 2326.6, against 674.2 vs 831.3).

![Test RMSE of mean baseline, linear regression and random forest on the time-ordered split (train yr=0, test yr=1)](tasks/ml_3/charts/ts_model_test_rmse.png)

**Permutation importance on the time split** (true increase in test RMSE when shuffled; negative means the test error fell): atemp 160.7, temp 159.2, season 92.8, mnth 76.5, windspeed 36.1, hum 30.9, weathersit 27.1, weekday 5.6, holiday 0.7, workingday -0.4. Yr is 0.0 because it is constant within the 2012 test set, so its importance cannot be assessed.

Atemp rose from fourth on the random split to first here. Temp stayed near the top, second on both splits (608.4 on the random split, 159.2 on the time split). Hum fell from third on the random split to sixth here. Yr was the highest-ranked feature on the random split (925.6), but its importance cannot be checked on the time split.

## Limitations

- **Two years only.** The data cover 2011 and 2012. The findings do not separate the yr effect from a growth trend or from seasonal patterns.
- **Time split breaks the models.** On the time split both models have negative test R², and yr cannot be assessed (see ml_3 above). The random-split scores (ml_1) therefore overstate performance on new years.
- **Small groups.** Holiday (n=21) and weathersit 3 (n=21) are thin. Several temp-by-weathersit cells have n of 1, 5 or 15, so their means are not interpretable. The holiday test has low power.
- **Interaction effects are small.** The working day × season effect is significant but has a small effect size (partial eta-squared 0.013 unadjusted, 0.0213 adjusted). The working day × year effect is not significant after Bonferroni correction and is negligible.
- **Collinearity.** Temp and atemp correlate at 0.9917, so linear-regression coefficients for them cannot be interpreted individually.
- **Overfitting and single splits.** The random forest's train R² is 0.982 on the random split and 0.981 on the time split. All model results come from a single split with no hyperparameter tuning or cross-validation. The test sets contain 147 and 366 rows.
- **Leakage.** The 13-feature model's score (R² 0.998) comes from leaky columns and must not be read as predictive skill.
- **Correlational results.** The findings report associations (means, correlations, interactions). They do not establish causes.
- **Unresolved review issue: season naming.** The eda_1 finding labels season 2 as spring and season 3 as summer, while the stat_2 chart and wording label season 2 as summer. This report uses numeric season codes only. The stat_2 chart carries the conflicting labels and should be read with that in mind. The stat_2 wording "the sign flips in summer" is corrected to: the sign flips in season 2.
- **Unresolved review issue: working-day gap for yr 1.** The stat_2 finding stated this gap as a rounded figure that the review corrected. This report gives the yr cell means instead of a gap, so the correction does not change any number reported here.
- **Unresolved review issue: ml_3 permutation statement.** The ml_3 finding stated that the random-split ranking of temp and atemp holds. The corrected reading is used here: atemp rose to first, temp stays near the top, and hum falls from third to sixth.
- **Unresolved review issue: ml_3 final finding.** The ml_3 claim that the models "explain little of the 2012 level of cnt" does not match the numbers. The corrected statement is used here: both models cut test RMSE below the training-mean baseline (2235.6 and 2326.6, against 2829.3), but both have negative test R² (-0.567 and -0.697), so they carry a large level offset for 2012.
- **Failed tasks.** None reported.

## Open questions

- Is the 2011 to 2012 jump a steady growth trend or a one-off level change? The current data cannot tell these apart.
- How much of the seasonal gap is explained by temp and hum, rather than by season itself?
- Do the working day × season and working day × year effects hold after also adjusting for the casual/registered split and atemp?
- Is the season 2 reversal of the working-day effect driven by a few observations? A per-season test with a confidence interval has not been run.
- Do casual and registered riders respond differently to holidays and working days?
- Do season and weathersit interact (for example, bad weather in winter)?
- Would a trend term or year-specific offset recover positive test R² on the time split?
- Would a rolling or expanding-window split give more stable results than a single train-2011, test-2012 split?
- Would removing yr and atemp from the features change the time-split error and the permutation ranking?
- Would regularising or tuning the random forest close the train-test gap without losing test accuracy?
- Is the weathersit 3 low mean stable enough to model, given only 21 rows? Would pooling weathersit 2 and 3, or dropping that category, change the results?