# Daily Rental Count (cnt) Analysis: Distribution, Group Differences, Interactions and Predictive Models

## Summary

- **Season, year and weather are significant; holiday and working day are not.** Season, yr and weathersit each survive Holm correction in both ANOVA and Kruskal-Wallis tests. Season and year explain about a third of the variance in cnt (eta squared 0.347 and 0.321), and weathersit about 0.10 (0.099). Holiday and workingday each have eta squared under 0.005 and are not significant after correction.
- **The year effect persists within every season.** Mean cnt rises from yr 0 to yr 1 in all four seasons, each within-season Welch test is significant after Holm correction, and the seasonal mix does not account for the raw difference (raw 2194.2, mix-adjusted 2199.4).
- **Effects are not simply additive.** The temperature slope differs by season (interaction F=10.28, p=1.2e-06), and the within-season slope for season 3 is -676 with a 95% CI of -3655 to 2303.
- **Gradient boosting predicts cnt best on the held-out split.** On the 147-day test split it reaches test MAE 462.77 and test R² 0.8906, against 617.39 and 0.8277 for linear regression, and 1711.99 and -0.0198 for the mean baseline.
- **Results are conditional on the data and models used.** The data cover 731 days. The regression estimates assume independent days and a temperature effect that is the same in every season, and the accepted interaction finding contradicts that second assumption.

## Data

- **Size:** 731 rows, 16 columns.
- **Target:** cnt, a daily count of rentals. Range 22 to 8714, mean 4504.3.
- **Missing values:** none in any column.
- **Features used in models (11):** season, yr, mnth, holiday, weekday, workingday, weathersit, temp, atemp, hum, windspeed.
- **Excluded:** casual and registered, because cnt equals casual plus registered on every row, so both leak the target. instant and dteday are an identifier and free text, and are not used as features.

## Findings

### Distribution of cnt and group differences (EDA)

Overall, cnt has mean 4504.3, median 4548.0, SD 1937.2, and quartiles 3152 and 5956. In the 30-bin histogram, the fullest bin holds 49 days.

![Histogram of daily cnt across 731 days](tasks/eda_1/charts/cnt_histogram.png)

The table below gives count, mean and median cnt for every level of the seven features.

| Feature | Level | Count | Mean cnt | Median cnt |
|---|---|---|---|---|
| season | 1 | 181 | 2604.1 | 2209.0 |
| season | 2 | 184 | 4992.3 | 4941.5 |
| season | 3 | 188 | 5644.3 | 5353.5 |
| season | 4 | 178 | 4728.2 | 4634.5 |
| yr | 0 | 365 | 3405.8 | 3740.0 |
| yr | 1 | 366 | 5599.9 | 5927.0 |
| mnth | 1 | 62 | 2176.3 | 1939.0 |
| mnth | 2 | 57 | 2655.3 | 2402.0 |
| mnth | 3 | 62 | 3692.3 | 3216.5 |
| mnth | 4 | 60 | 4484.9 | 4293.5 |
| mnth | 5 | 62 | 5349.8 | 4890.5 |
| mnth | 6 | 60 | 5772.4 | 5308.5 |
| mnth | 7 | 62 | 5563.7 | 5446.5 |
| mnth | 8 | 62 | 5664.4 | 5229.5 |
| mnth | 9 | 60 | 5766.5 | 5384.0 |
| mnth | 10 | 62 | 5199.2 | 5013.0 |
| mnth | 11 | 60 | 4247.2 | 4081.0 |
| mnth | 12 | 62 | 3403.8 | 3444.0 |
| holiday | 0 | 710 | 4527.1 | 4558.0 |
| holiday | 1 | 21 | 3735.0 | 3351.0 |
| weekday | 0 | 105 | 4228.8 | 4334.0 |
| weekday | 1 | 105 | 4338.1 | 4359.0 |
| weekday | 2 | 104 | 4510.7 | 4576.5 |
| weekday | 3 | 104 | 4548.5 | 4642.5 |
| weekday | 4 | 104 | 4667.3 | 4721.0 |
| weekday | 5 | 104 | 4690.3 | 4601.5 |
| weekday | 6 | 105 | 4550.5 | 4521.0 |
| workingday | 0 | 231 | 4330.2 | 4459.0 |
| workingday | 1 | 500 | 4584.8 | 4582.0 |
| weathersit | 1 | 463 | 4876.8 | 4844.0 |
| weathersit | 2 | 247 | 4035.9 | 4040.0 |
| weathersit | 3 | 21 | 1803.3 | 1817.0 |

Across the levels of each feature, the group mean ranges are:
- **Month:** 2176.3 (January) to 5772.4 (June). This is the widest range.
- **Season:** 2604.1 (season 1) to 5644.3 (season 3).
- **Year:** 3405.8 (yr 0) to 5599.9 (yr 1).
- **Weathersit:** 1803.3 (level 3) to 4876.8 (level 1).

These are unadjusted group-mean ranges, so they do not establish which effect is significant (see Limitations).

![Mean daily cnt by season (left) and by weathersit (right)](tasks/eda_1/charts/mean_cnt_season_weathersit.png)

Holidays and working days show small differences in the means. Holidays average 3735.0 against 4527.1 on non-holidays. Non-working days average 4330.2 against 4584.8 on working days.

### Significance and effect sizes (statistical tests)

Holm correction is applied across the five features tested.

**Season.** One-way ANOVA F=128.77, p=6.7e-67 (Holm 3.4e-66), eta squared 0.347. Kruskal-Wallis H=250.93, p=4.1e-54. Significant after correction.

**Year.** Welch t=18.58, p=1.0e-62, Cohen d=1.37 (yr 1 minus yr 0). ANOVA F=344.89, p=2.5e-63 (Holm 9.9e-63), eta squared 0.321. Kruskal-Wallis H=238.84, p=7.0e-54. Significant after correction.

**Weathersit.** ANOVA F=40.07, p=3.1e-17 (Holm 9.3e-17), eta squared 0.099. Kruskal-Wallis H=67.18, p=2.6e-15. Significant after correction. The level 3 mean rests on 21 days, so its interval is wide.

**Holiday.** Welch t=-1.70, p=0.103, Cohen d=-0.41 (holiday 1 minus holiday 0). ANOVA p=0.065 (Holm 0.130, eta squared 0.005). Kruskal-Wallis p=0.083. Not significant after correction.

**Workingday.** Welch t=1.60, p=0.110, Cohen d=0.13 (working day minus non-working day). ANOVA p=0.098 (Holm 0.130, eta squared 0.004). Kruskal-Wallis p=0.119. Not significant after correction.

The 95% confidence intervals for group means are below.

| Feature | Level | n | Mean cnt | 95% CI | Median |
|---|---|---|---|---|---|
| season | 1 | 181 | 2604.1 | 2398.8 to 2809.5 | 2209.0 |
| season | 2 | 184 | 4992.3 | 4745.6 to 5239.0 | 4941.5 |
| season | 3 | 188 | 5644.3 | 5434.3 to 5854.3 | 5353.5 |
| season | 4 | 178 | 4728.2 | 4476.8 to 4979.6 | 4634.5 |
| yr | 0 | 365 | 3405.8 | 3263.8 to 3547.7 | 3740.0 |
| yr | 1 | 366 | 5599.9 | 5416.1 to 5783.8 | 5927.0 |
| holiday | 0 | 710 | 4527.1 | 4385.0 to 4669.2 | 4558.0 |
| holiday | 1 | 21 | 3735.0 | 2777.6 to 4692.4 | 3351.0 |
| workingday | 0 | 231 | 4330.2 | 4064.1 to 4596.2 | 4459.0 |
| workingday | 1 | 500 | 4584.8 | 4419.8 to 4749.9 | 4582.0 |
| weathersit | 1 | 463 | 4876.8 | 4705.1 to 5048.4 | 4844.0 |
| weathersit | 2 | 247 | 4035.9 | 3809.1 to 4262.6 | 4040.0 |
| weathersit | 3 | 21 | 1803.3 | 1238.7 to 2367.9 | 1817.0 |

![Mean daily cnt with 95% CI by season (left) and by weathersit (right)](tasks/stat_1/charts/stat1_mean_ci_season_weathersit.png)

### Interactions

**Weathersit by working day.** The interaction gives F=0.52, p=0.60. This test is unadjusted for yr, holiday and season, so it describes the marginal rather than the adjusted effect. Within non-working days, mean cnt is 4587 (n=156) at weathersit 1, 3937 (n=70) at weathersit 2 and 1815 (n=5) at weathersit 3. Within working days, mean cnt is 5024 (n=307) at weathersit 1, 4075 (n=177) at weathersit 2 and 1800 (n=16) at weathersit 3. Weathersit 3 has too few days to estimate well.

![Mean daily cnt per weathersit level, separately for non-working and working days](tasks/stat_2/charts/stat2_ws_by_workingday.png)

**Temperature by season.** The interaction gives F=10.28, p=1.2e-06. This test is unadjusted for yr, holiday and weathersit, so it describes the marginal rather than the adjusted effect. Within-season OLS slopes of cnt on temp, with 95% CI and R²:

| Season | n | Slope (rides per unit of temp) | 95% CI | R² |
|---|---|---|---|---|
| 1 | 181 | 9119 | 7626 to 10613 | 0.45 |
| 2 | 184 | 6594 | 4817 to 8372 | 0.23 |
| 3 | 188 | -676 | -3655 to 2303 | 0.00 |
| 4 | 178 | 6268 | 4116 to 8419 | 0.16 |

Temperature has a moderate association with cnt in season 1 (R² 0.45) and a weak one in seasons 2 and 4. The season 3 slope is near zero, and its interval spans zero.

### Year effect within seasons (stat_3)

The yr effect is present in every season. The within-season Welch tests, Holm-corrected across the four seasons, are all significant:

| Season | Mean yr 0 | Mean yr 1 | Difference | Welch t | p (Holm) | Cohen d |
|---|---|---|---|---|---|---|
| 1 | 1666.7 | 3531.3 | 1864.6 | 12.05 | 2.0e-22 | 1.78 |
| 2 | 3775.2 | 6209.5 | 2434.3 | 13.98 | 4.0e-30 | 2.06 |
| 3 | 4464.4 | 6824.2 | 2359.9 | 18.87 | 3.6e-44 | 2.75 |
| 4 | 3664.5 | 5791.9 | 2127.4 | 10.69 | 4.4e-20 | 1.60 |

The seasonal mix does not explain the year effect. The share of each yr group in each season differs by less than one percentage point. The raw yr difference is 2194.2, and the mix-adjusted difference is 2199.4.

![Mean cnt per season for yr 0 and yr 1 with 95% t-based CIs](tasks/stat_3/charts/cnt_by_season_yr.png)

### Multiple regression: season and weathersit adjusted for yr and temp (stat_4)

The model is OLS cnt ~ season + weathersit + yr + temp on all 731 days, with season 1 and weathersit 1 as reference levels.

- **Season** (partial F=95.38, df=3, p=5.1e-52, Holm 1.0e-51). Adjusted differences from season 1: season 2 +1157.8 (95% CI 925.3 to 1390.4), season 3 +947.4 (641.6 to 1253.3), season 4 +1590.6 (1395.9 to 1785.2).
- **Weathersit** (partial F=105.39, df=2, p=6.9e-41, Holm 6.9e-41). Adjusted differences from weathersit 1: level 2 -614.7 (-748.5 to -480.8), level 3 -2410.9 (-2790.7 to -2031.0). The level 3 estimate rests on 21 days.
- **R²:** the base model (yr + temp) has R² 0.683. Adding season and weathersit gives 0.805, a change of 0.123. Season adds 0.077 and weathersit adds 0.057.

These estimates assume the temperature effect is the same in every season. The stat_2 interaction contradicts that assumption, so the adjusted estimates are conditional on this additive model and are not established as robust to the interaction. The confidence intervals and p-values assume independent daily observations, which likely understates uncertainty.

### Predictive models compared with a mean baseline (ml_1)

All models use the 11 non-leaking features and a fixed 80/20 split (584 training rows, 147 test rows, random_state 42).

| Model | Test MAE | Test RMSE | Test R² | Train R² |
|---|---|---|---|---|
| Mean-value baseline | 1711.99 | 2022.17 | -0.0198 | 0.0 |
| Linear regression | 617.39 | 831.29 | 0.8277 | 0.7911 |
| Gradient boosting | 462.77 | 662.32 | 0.8906 | 0.9535 |

Linear regression reduces test MAE from 1711.99 for the baseline to 617.39. Gradient boosting reduces it further, to 462.77, which is lower than linear regression's 617.39. Its train R² of 0.9535 against a test R² of 0.8906 indicates some overfitting remains.

Gradient boosting feature importances:
- temp 0.386, yr 0.304 and season 0.096 carry the largest importances.
- Next are atemp (0.073) and hum (0.056). Holiday is not in the top 10.

Linear regression ranks atemp highest by absolute coefficient (3488.0), followed by temp (2097.2), windspeed (2080.5) and yr (2024.0). The two temperature variables are likely collinear, so their individual importances should be read with caution.

![Left: test MAE of daily cnt for the mean baseline, linear regression and gradient boosting. Right: top 10 gradient boosting feature importances on the test split.](tasks/ml_1/charts/ml1_model_comparison.png)

**Leakage check.** The profile's automatic check reports a single-feature R² of 0.946 for registered. The squared correlation calculated by the team gives 0.894 for registered and 0.453 for casual. These two figures disagree, and the cause has not been resolved. Both columns were excluded from all models, so the model scores do not use them.

## Limitations

- **Timing statement in the EDA (review issue 1).** The EDA stated that year and month show the largest timing differences. By the group means, month has the widest range (2176.3 to 5772.4), season is next (2604.1 to 5644.3), and year is smaller (3405.8 to 5599.9). The Findings above restate the ranges in that order. This objection stands and affects the EDA timing statement.
- **Spread comparison of season and weathersit (review issue 2).** The EDA treated the season and weathersit group-mean ranges as similar in size, so that neither dominates. This is unresolved. The ranges are unadjusted, the two variables have different numbers of levels, weathersit level 3 has only 21 days, and the EDA ran no test. Which effect is significant is answered only by the stat_1 tests, where season (eta squared 0.347) and weathersit (eta squared 0.099) are both significant.
- **Holiday and workingday.** Holiday has only 21 days in the holiday = 1 group, so these tests may lack power. The null results mean no significant difference was detected, not that none exists.
- **Interaction tests are unadjusted.** The weathersit-by-workingday and temp-by-season tests do not control for yr, holiday, season or weathersit. Weathersit level 3 has 5 non-working and 16 working days in the interaction analysis.
- **Additive regression assumption.** The stat_4 estimates assume the temperature effect is the same in every season. The stat_2 interaction contradicts this.
- **Independence.** Confidence intervals and p-values assume independent daily observations, which likely understates uncertainty for daily data.
- **Model evaluation.** Scores come from one fixed split. The gradient boosting model shows train R² 0.9535 against test R² 0.8906, so some overfitting remains. No cross-validation or tuning was run. Feature importances are affected by collinearity between temp and atemp.
- **Leakage warning discrepancy.** The profile reports registered R² 0.946, while the team's squared-correlation calculation gives 0.894. This is unresolved.
- **Failed tasks.** None reported.

## Open questions

- Does the winter drop in cnt persist after controlling for temperature and weather? (Partly addressed by stat_4, under its additive assumption.)
- Is the yr effect a trend or a seasonal-mix artefact? The within-season and mix-adjusted results show the year effect persists across seasons, but they do not tell whether it reflects trend.
- Do the season and weathersit effects persist after adding a season-by-temp interaction, or after adding holiday and workingday?
- Do the season and weathersit effects change when temp is replaced by atemp?
- Does the weathersit result hold without the 21-day level 3, and does weathersit 3 drive the weathersit-by-workingday pattern?
- Is the near-zero season 3 temperature slope real, or does it reflect a nonlinear temperature effect or the summer peak?
- Do the results hold under cross-validation or a tuned gradient boosting model, and does the feature ranking change?
- What drives the growth in rentals between yr 0 and yr 1 within seasons, such as registered versus casual users?
- Why does the leakage warning report a registered R² of 0.946 when the squared correlation gives 0.894?