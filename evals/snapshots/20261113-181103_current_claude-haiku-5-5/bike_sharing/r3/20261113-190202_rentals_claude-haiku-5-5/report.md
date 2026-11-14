# Daily Bike Rental Count (cnt): Analysis of 731 Days

## Summary

- **Predictive model:** A random forest on 11 features (leaked and ID columns removed) reached test R² 0.887 and RMSE 674, against RMSE 2022 for a predict-the-mean baseline. Linear regression reached test R² 0.828 and RMSE 831. Temperature and year carried most of the predictive signal.
- **Year and season are the strongest group differences:** mean cnt was 5600 in 2012 against 3406 in 2011 (difference 2194, 95% CI 1962 to 2426, Cohen's d 1.37). Season had a large association with cnt (eta-squared 0.347).
- **The 2012 uplift persists within every season and month checked.** All 16 season and month gaps are positive. Adjusted for season and month, the year coefficient is 2197 rides per day (95% CI 1997 to 2397). Whether the uplift is a step or a steady trend is not settled: adding a day index gives a different year estimate, and the data cannot reliably separate the two.
- **Holiday and working day are not significant after Holm correction** (both adjusted p = 0.206). No workingday interaction with season or weathersit was detected (p = 0.21 and p = 0.60).
- **Weather matters:** mean cnt was 4877 in weathersit 1, 4036 in weathersit 2 and 1803 in weathersit 3 (n = 21 days). Temperature was positively and windspeed negatively correlated with cnt.

## Data

- **Size:** 731 rows × 16 columns.
- **Target:** cnt (daily total rides), with mean 4504 and median 4548.
- **Missing values:** none. Zero of 731 rows are missing in every column, including cnt, temp, hum, windspeed and the categorical features.
- **Leakage:** cnt equals casual plus registered in all 731 rows. registered alone correlates with cnt at r = 0.946 (r² = 0.894). casual and registered were excluded from all predictive modelling.
- **Identifiers:** instant and dteday were not used as features.
- **Feature types:** the profile lists no categorical features. The analysis treated season, yr, mnth, holiday, weekday, workingday and weathersit as grouping levels, and temp, atemp, hum and windspeed as continuous variables.

## Findings

### Distribution and group differences (EDA)

- **Overall distribution:** cnt has mean 4504.3, median 4548, standard deviation 1937.2, minimum 22, maximum 8714 and skew -0.05, so it is close to symmetric.
- **Season:** mean cnt was 2604 in season 1 (n = 181, median 2209), 4992 in season 2 (n = 184, median 4942), 5644 in season 3 (n = 188, median 5354) and 4728 in season 4 (n = 178, median 4635).
- **Year:** mean cnt was 3406 in yr 0 (2011, n = 365, median 3740) and 5600 in yr 1 (2012, n = 366, median 5927).
- **Month:** mean cnt rose from 2176 in month 1 (n = 62) to a peak of 5767 in month 9 (n = 60), then fell to 3404 in month 12 (n = 62). Across the two years, the highest single-month mean is September 2012 at 7286.
- **Weather situation:** mean cnt was 4877 for weathersit 1 (n = 463, median 4844), 4036 for weathersit 2 (n = 247, median 4040) and 1803 for weathersit 3 (n = 21, median 1817).
- **Holiday:** mean cnt was 3735 on holidays (n = 21, median 3351) against 4527 on non-holidays (n = 710, median 4558).
- **Working day:** mean cnt was 4585 on working days (n = 500, median 4582) against 4330 on non-working days (n = 231, median 4459).
- **Weekday:** group means ranged from 4229 (weekday 0, n = 105) to 4690 (weekday 5, n = 104), a small spread.
- **Temperature quartiles:** mean cnt was 2615 in Q1 (n = 183, median 2252), 4187 in Q2 (n = 183, median 4189), 5591 in Q3 (n = 182, median 5236) and 5631 in Q4 (n = 183, median 5463). Q1 covers temp up to 0.337 (normalised scale).
- **Humidity quartiles:** mean cnt was 4378 in Q1 (median 4587), 4852 in Q2 (median 4763), 4914 in Q3 (median 4711) and 3879 in Q4 (median 4035). The highest-humidity quartile had the lowest mean.
- **Windspeed quartiles:** mean cnt was 4923 in Q1 (median 4854), 4952 in Q2 (median 4835), 4159 in Q3 (median 4154) and 3978 in Q4 (median 4046).

![Daily cnt over time (left) and mean daily cnt by season (right)](tasks/eda_1/charts/cnt_over_time_and_season.png)

The series starts low in January 2011 (mean 1232) and rises to 4559 in July 2011. In 2012 the level is higher in every matched month: January 2012 averages 3121 and December 2012 averages 3991.

### Significance tests and effect sizes

- **Season:** one-way ANOVA F = 128.8, p = 6.7e-67, Holm-adjusted p = 3.4e-66, eta-squared = 0.347. Kruskal-Wallis agrees (H = 250.9, p = 4.1e-54).
- **Year:** Welch t = 18.58, p = 1.0e-62, Holm-adjusted p = 4.2e-62. The 2012 minus 2011 difference is 2194 (95% CI 1962 to 2426), Cohen's d = 1.37.
- **Weather situation:** one-way ANOVA F = 40.07, p = 3.1e-17, Holm-adjusted p = 9.3e-17, eta-squared = 0.099, a small-to-medium effect. Kruskal-Wallis agrees (H = 67.2, p = 2.6e-15). The weathersit 3 group has n = 21.
- **Holiday:** Welch t = -1.70, p = 0.103, Holm-adjusted p = 0.206. The difference is -792 (95% CI -1758 to 174), which includes zero. Cohen's d = -0.41, estimated from only 21 holiday days.
- **Working day:** Welch t = 1.60, p = 0.110, Holm-adjusted p = 0.206. The difference is 255 (95% CI -58 to 567), which includes zero. Cohen's d = 0.13, negligible.
- **Correlations with cnt (Pearson, with Spearman in brackets):**
  - temp: r = 0.627 (95% CI 0.581 to 0.670), Spearman 0.622.
  - atemp: r = 0.631 (95% CI 0.585 to 0.673), Spearman 0.623.
  - hum: r = -0.101 (95% CI -0.172 to -0.028), Spearman -0.098, p = 0.006. This is significant but explains about 1% of variance.
  - windspeed: r = -0.235 (95% CI -0.302 to -0.165), Spearman -0.217.
- **Multiple comparisons:** across the five group tests, Holm gives 0.206 for holiday and working day. Across all nine tests (five group tests plus four correlations), Holm-adjusted p-values are 1.6e-16 for weathersit, 4.7e-66 for season, 6.3e-62 for yr, 2.2e-80 for temp, 1.7e-81 for atemp and 5.4e-10 for windspeed. Humidity has adjusted p = 0.019. Holiday and working day remain non-significant.

![Mean daily cnt with 95% confidence intervals for each level of season, yr, weathersit, holiday and workingday](tasks/stat_1/charts/stat1_group_means.png)

### Interactions and pairwise comparisons

- **Workingday × season:** the interaction F-test gives F(3, 723) = 1.50, p = 0.21, so no interaction was detected. Within-season working-day differences (working minus non-working) were:
  - season 1: +523 (95% CI 95 to 952, p = 0.017).
  - season 2: -216 (95% CI -779 to 347).
  - season 3: +243 (95% CI -211 to 698).
  - season 4: +179 (95% CI -378 to 737).

  Season 1 has the largest estimate and differs in sign from season 2. The test does not show that the working-day effect is similar across seasons.
- **Workingday × weathersit:** the interaction F-test gives F(2, 725) = 0.52, p = 0.60, so no interaction was detected. Within-level working-day differences were +437 in weathersit 1 (95% CI 57 to 816, p = 0.024), +138 in weathersit 2 (95% CI -388 to 664) and -16 in weathersit 3 (95% CI -1954 to 1922). The weathersit 3 estimate is uninformative: it rests on 5 non-working and 16 working days.
- **Season pairwise differences (Welch, Holm-adjusted):**
  - Season 1 is lower than season 2 by 2388 (95% CI 2068 to 2708), Holm p = 1.0e-37.
  - Season 1 is lower than season 3 by 3040 (95% CI 2747 to 3333), Holm p = 1.1e-61.
  - Season 1 is lower than season 4 by 2124 (95% CI 1800 to 2448), Holm p = 9.6e-31.
  - Season 2 is lower than season 3 by 652 (95% CI 329 to 975), Holm p = 1.7e-4.
  - Season 2 vs season 4 is -264 (95% CI -615 to 87), Holm p = 0.14. This is the only season pair not significant after correction.
  - Season 3 is higher than season 4 by 916 (95% CI 590 to 1243), Holm p = 2.0e-7.
- **Weathersit pairwise differences (Welch, Holm-adjusted):**
  - Weathersit 2 is lower than weathersit 1 by 841 (95% CI -1125 to -557), Holm p = 2.1e-8.
  - Weathersit 3 is lower than weathersit 1 by 3074 (95% CI -3660 to -2487), Holm p = 2.6e-10.
  - Weathersit 3 is lower than weathersit 2 by 2233 (95% CI -2835 to -1630), Holm p = 3.0e-8.

  The weathersit 3 contrasts rest on 21 days.
- **temp and atemp:** their Pearson correlation with each other is r = 0.992, so either can stand in for the other in a model.

![Mean daily bike count (cnt) with 95% CI by season and by weathersit, split by workingday](tasks/stat_2/charts/stat2_interaction_means.png)

### Predictive models

- **Setup:** 11 features (season, yr, mnth, holiday, weekday, workingday, weathersit, temp, atemp, hum, windspeed). One fixed 80/20 split with seed 42 gives 584 training rows and 147 test rows.
- **Mean baseline (test set):** RMSE 2022, MAE 1712, R² -0.020. The training mean of cnt is 4561.
- **Linear regression:** test RMSE 831, MAE 617, R² 0.828 (training R² 0.791). The largest absolute coefficients were atemp (3488), temp (2097), windspeed (2081) and yr (2024). The atemp and temp weights point to collinearity, so their individual coefficients should not be read as separate effects.
- **Random forest (300 trees):** test RMSE 674, MAE 426, R² 0.887. It beats linear regression on all three metrics. Its training R² of 0.982 against test 0.887 shows some overfitting.
- **Permutation importance (random forest, test set; RMSE increase when shuffled):** yr 926 (sd 56), temp 608 (sd 63), hum 220 (sd 25), atemp 193 (sd 29), season 136 (sd 24).

![Test RMSE of predicting daily cnt: mean baseline vs linear regression and random forest, same split](tasks/ml_1/charts/ml1_test_rmse.png)

### Does the 2011 to 2012 increase hold within season and month? (partial)

- **Within seasons:** the 2012 minus 2011 gap in mean cnt is 1865 in season 1 (2011 mean 1667, n = 90; 2012 mean 3531, n = 91), 2434 in season 2 (3775 with n = 92; 6210 with n = 92), 2360 in season 3 (4464 with n = 94; 6824 with n = 94) and 2127 in season 4 (3665 with n = 89; 5792 with n = 89).
- **Within months:** the gap is 1889 in January (1232 with n = 31; 3121 with n = 31) and 1834 in February (1722 with n = 28; 3556 with n = 29). Across all twelve months the gap ranges from 1174 (December) to 3253 (March).
- **Consistency:** the gap is positive in all 16 levels checked (4 seasons and 12 months). Across seasons it runs from 1865 to 2434, and across months from 1174 to 3253. The size of the uplift therefore varies by level and is not one fixed amount.
- **Cell sizes:** season-by-year cells hold 89 to 94 rows and month-by-year cells hold 28 to 31 rows.

![Mean daily cnt in 2011 vs 2012 within each season (left) and month (right)](tasks/eda_2/charts/eda2_year_gap_by_season_month.png)

![Mean daily cnt in 2011 vs 2012 within each season (left) and month (right)](tasks/eda_2/charts/eda2_year_gap_by_season_month_v2.png)

### Step change or steady trend? (model comparison)

- **Model 1** (cnt ~ season + mnth + yr): the yr coefficient is 2197 rides per day (95% CI 1997 to 2397, p about 3e-80), R² = 0.498.
- **Model 2** (adds a continuous day index): the yr coefficient is 5493 (95% CI 1341 to 9645, p = 0.0096). The day-index coefficient is -9.0 per day (95% CI -20.3 to 2.3, p = 0.119). R² rises to 0.499.
- **Disagreement between the two models:** the yr estimate is 2197 in model 1 and 5493 in model 2. The second is conditional on the trend term and is imprecise. The two estimates are reported here as they stand and are not reconciled.
- **Collinearity:** yr and the day index have correlation 0.866, with VIFs of 432.6 (yr) and 574.3 (day index).
- **Nested F-test** (model 2 vs model 1): F = 2.43, df = 1, p = 0.119. This shows no detected improvement from adding the day index. It does not show that a steady trend is absent: with VIFs above 400 the test has low power to separate a step from a trend, so this data cannot reliably distinguish the two.

![yr coefficient and 95% CI in model 1 (season, mnth, yr) and model 2 (adds day index)](tasks/stat_3/charts/stat3_yr_coef_ci.png)

## Limitations

- **Leakage:** casual and registered were excluded from all models because they sum to cnt. registered alone would predict cnt almost perfectly (r = 0.946).
- **Small groups:** the holiday sample has 21 days and weathersit 3 has 21 days. The weathersit 3 working-day cells have 5 and 16 days. Estimates for these groups are imprecise, and the holiday effect is estimated from 21 days.
- **Two years only:** the year effect compares 2011 with 2012. The data cannot separate a step from a trend reliably (see the collinearity above).
- **Collinear predictors:** temp and atemp correlate at r = 0.992. Linear coefficients for both are unstable and should not be read as separate effects.
- **Holm correction applied two ways:** across five group tests, holiday and working day are 0.206. Across nine tests, humidity is significant at 0.019. Both are reported.
- **Model evaluation:** all model scores come from one 147-row test split. The random forest shows overfitting (training R² 0.982). No repeated cross-validation or tuned gradient boosting was run.
- **Weak humidity effect:** humidity's correlation with cnt is about 1% of variance explained.
- **Partial task:** the eda_2 task (within-season and within-month year effect) is recorded as partial. The within-season and within-month gaps are reported above, but the model-based check in the open questions was not completed.
- **Unresolved review issue (stat_1):** the review asked for pairwise differences in mean cnt with 95% CIs and Holm-adjusted p-values for season and weathersit, and for a stated basis for the claim that temp and atemp are nearly identical. The material now appears in stat_2 (all-pairs season and weathersit comparisons; temp–atemp r = 0.992). The objection is recorded here as raised against stat_1 and is not marked closed.
- **Failed tasks:** none reported.

## Open questions

- Does a trend fitted within each year (day index centred separately for 2011 and 2012) separate the step from the trend without the collinearity problem?
- Does the year effect persist within each season after adjusting for month and weather, in a regression model?
- Does the workingday effect within season 1 (+523, p = 0.017) hold after adjusting for year, temperature and weather?
- Would a model with workingday, season and weathersit main effects plus controls for yr and temp give a more precise working-day estimate than the 21-day holiday sample?
- Are the holiday and working-day effects masked by the small holiday sample (n = 21)?
- Does weathersit 3 (n = 21) drive the weather effect, or is it confounded with season or humidity?
- Given that temp and atemp are almost equally correlated with cnt, which should be kept, and does temp still matter after adjusting for season and year?
- Do repeated cross-validation or a tuned gradient boosting model change the random forest's advantage over linear regression, given the single 147-row test split?
- Is the holiday effect stable across years within season?
- How much of the temp effect is shared with atemp?