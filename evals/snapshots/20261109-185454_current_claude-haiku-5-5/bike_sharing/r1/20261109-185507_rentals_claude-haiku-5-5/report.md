# Daily Bike Rentals: Patterns, Significance and Prediction of the Daily Count (cnt)

## Summary

- **Year and weather show the largest associations with cnt.** Mean cnt was 2194.2 higher in yr 1 than yr 0 (Welch p = 1.0e-62, Cohen's d = 1.37). Weathersit level 3 averaged 3073.5 below level 1 (p = 8.8e-11), but this rests on only 21 days. Season was the largest categorical factor (ANOVA eta squared 0.347, about 35% of variance).
- **The yr effect survives adjustment for season and weathersit.** The adjusted coefficient is 2132.5 (all three weathersit levels) or 2175.8 (weathersit 3 pooled into 2). Whether the yr effect varies across season-weather strata is unresolved: the two analyses disagree (p = 0.0057 against p = 0.208), and the first test's construction is unverified.
- **Holiday and workingday differences were not statistically significant.** Holiday: p = 0.103, based on 21 holiday days. Workingday: p = 0.110. Neither survives Bonferroni correction.
- **Interactions were not detected at 0.05.** Workingday x weathersit: F = 0.52, p = 0.598, with only 5 and 16 days in the level-3 cells, so the test has little power there. Season x yr: F = 2.43, p = 0.064, borderline.
- **A random forest on 11 non-leaky features predicts cnt well on a held-out test set.** Test R² is 0.887 and RMSE 674.2, against 2022.2 for a mean-value baseline (R² -0.020). Linear regression reached R² 0.828. The leaky columns casual and registered were excluded.

## Data

- 731 daily records and 16 columns. The target is cnt, the daily count of rentals.
- There are no missing values in any column (0 missing cells), so all 731 rows are usable.
- Thirteen columns are numeric features (season, yr, mnth, holiday, weekday, workingday, weathersit, temp, atemp, hum, windspeed, casual, registered). There are no categorical or date/time features. instant and dteday are identifiers and were not used as features.
- **Leakage:** casual + registered equals cnt exactly (maximum absolute difference 0.0). The profile also flags registered as predicting cnt almost perfectly (0.946). Both were excluded from every model.

## Findings

### Distribution and group comparisons (eda_1)

**Distribution of cnt.** Mean 4504.3, median 4548, standard deviation 1937.2, minimum 22, maximum 8714, skewness -0.047, so the distribution is close to symmetric. The histogram is broad and roughly unimodal, with a longer low tail. The most populated of the 30 bins (49 days) spans 3788.5 to 4078.3 rentals.

![Histogram of daily total rentals (cnt) across 731 days](tasks/eda_1/charts/cnt_histogram.png)

**Season.** Season 1 has the lowest mean (2604.1, median 2209.0, n = 181). Season 3 has the highest (mean 5644.3, median 5353.5, n = 188). Season 2 has mean 4992.3 (median 4941.5, n = 184) and season 4 has mean 4728.2 (median 4634.5, n = 178). The season 3 minus season 1 mean gap is 3040.2.

**Year.** yr 0 has mean 3405.8 (median 3740.0, n = 365). yr 1 has mean 5599.9 (median 5927.0, n = 366).

**Holiday.** Non-holiday days (n = 710) have mean 4527.1 and median 4558.0. Holiday days (n = 21) have mean 3735.0 and median 3351.0.

**Workingday.** Non-working days (n = 231) have mean 4330.2 and median 4459.0. Working days (n = 500) have mean 4584.8 and median 4582.0.

**Weekday.** Means by weekday level (0–6 as coded) range from 4228.8 (level 0, median 4334.0) to 4690.3 (level 5, median 4601.5). This spread is small compared with the season and weather differences.

**Weathersit.** Level 1 (n = 463) has mean 4876.8 and median 4844.0. Level 2 (n = 247) has mean 4035.9 and median 4040.0. Level 3 (n = 21) has mean 1803.3 and median 1817.0. Level 3 is 3073.5 below level 1 in mean.

**Month.** Mean and median cnt by month, with group sizes:

| Month | n | Mean | Median |
|---|---|---|---|
| 1 | 62 | 2176.3 | 1939.0 |
| 2 | 57 | 2655.3 | 2402.0 |
| 3 | 62 | 3692.3 | 3216.5 |
| 4 | 60 | 4484.9 | 4293.5 |
| 5 | 62 | 5349.8 | 4890.5 |
| 6 | 60 | 5772.4 | 5308.5 |
| 7 | 62 | 5563.7 | 5446.5 |
| 8 | 62 | 5664.4 | 5229.5 |
| 9 | 60 | 5766.5 | 5384.0 |
| 10 | 62 | 5199.2 | 5013.0 |
| 11 | 60 | 4247.2 | 4081.0 |
| 12 | 62 | 3403.8 | 3444.0 |

Monthly means for June to September range from 5563.7 (July) to 5772.4 (June), and the winter months are lowest. Medians follow the same pattern.

![Mean daily rentals by month](tasks/eda_1/charts/cnt_mean_by_month.png)

**Leakage check.** casual + registered equals cnt exactly (maximum absolute difference 0.0).

### Significance and effect sizes (stat_1)

- **yr (yr 1 minus yr 0):** Welch p = 1.0e-62; Cohen's d = 1.37 (large). The mean difference is 2194.2, 95% CI [1962.3, 2426.1]. Significant after Bonferroni correction over 5 features (adjusted p about 5e-62). Mann-Whitney p = 7.1e-54.
- **season:** one-way ANOVA F = 128.8, p = 6.7e-67, eta squared = 0.347 (about 35% of variance). Kruskal-Wallis p = 4.1e-54 agrees. Season 3 minus season 1 is 3040.2, 95% CI [2747.4, 3332.9] (Welch p = 1.8e-62, Cohen's d = 2.12). Significant after Bonferroni correction.
- **weathersit:** one-way ANOVA F = 40.07, p = 3.1e-17, eta squared = 0.099 (medium). Kruskal-Wallis p = 2.6e-15 agrees.
  - Level 3 minus level 1: -3073.5, 95% CI [-3660.0, -2487.0], Welch p = 8.8e-11, Cohen's d = -1.65. Significant after Bonferroni correction.
  - Level 2 minus level 1: -840.9, 95% CI [-1124.8, -557.0], Welch p = 1.0e-8, Cohen's d = -0.45. Significant after Bonferroni correction (adjusted p about 5.2e-8).
- **holiday (1 minus 0):** mean difference -792.1, 95% CI [-1758.4, 174.2], Welch p = 0.103 (Mann-Whitney p = 0.083), Cohen's d = -0.41 (based on 21 holiday days). Not significant after Bonferroni correction (adjusted p = 0.51).
- **workingday (1 minus 0):** mean difference 254.7, 95% CI [-57.9, 567.2], Welch p = 0.110 (Mann-Whitney p = 0.119), Cohen's d = 0.13 (negligible). Not significant after Bonferroni correction (adjusted p = 0.55).

![Mean daily cnt by level of holiday, workingday, yr, weathersit and season, with 95% confidence intervals of the mean](tasks/stat_1/charts/stat1_group_means.png)

### Interactions (stat_2)

- **workingday x weathersit:** two-way OLS ANOVA (Type II sums of squares) F = 0.52, df = 2, p = 0.598. The test found no significant interaction. Cell means for workingday 0 vs 1 are 4587.3 vs 5023.9 at weathersit 1 (n = 156 and 307) and 3936.8 vs 4075.0 at weathersit 2 (n = 70 and 177). The workingday gap is larger at weathersit 1, but the test does not find this difference in gap size significant. At weathersit 3 the cell means are 1815.4 (workingday 0, n = 5) and 1799.5 (workingday 1, n = 16). With 5 and 16 days in these cells the test has little power to detect an interaction, so the weathersit 3 cells cannot be interpreted.

![Mean daily cnt for each cell of the two interaction pairs (weathersit x workingday; season x yr)](tasks/stat_2/charts/stat2_interaction_means.png)

- **season x yr:** two-way OLS ANOVA (Type II sums of squares) F = 2.43, df = 3, p = 0.064. This is not significant at 0.05 and is borderline. Cell means for yr 0 and yr 1 by season are: season 1, 1666.7 and 3531.3; season 2, 3775.2 and 6209.5; season 3, 4464.4 and 6824.2; season 4, 3664.5 and 5791.9.

### Year effect after adjustment (stat_3 and stat_4)

- **stat_3 (weathersit at three levels):** in an OLS model of cnt on yr, season and weathersit, the yr 1 coefficient is 2132.5, 95% CI [1987.4, 2277.6], p = 2.1e-122 (365 days in yr 0, 366 in yr 1; R² = 0.738). The yr effect remains after controlling for season and weathersit.
- **stat_3 heterogeneity test:** the yr x (season, weathersit) interaction F-test gives p = 0.0057. Within-stratum yr 1 minus yr 0 differences range from -213 (season 2, weathersit 3; 2 days in yr 0, 1 in yr 1) to 2429.6 (season 2, weathersit 1; 52 in yr 0, 61 in yr 1). Of the 24 season x weathersit x yr cells, 7 have fewer than 5 days, and the smallest has 1 day. Dropping the 21 weathersit 3 days (n = 710) leaves the interaction at p = 0.046 and the adjusted yr coefficient at 2162.0.
- **stat_4 (weathersit 3 pooled into 2, n = 731):** the yr x (season, pooled weathersit) interaction gives F = 1.39 on 7 df, p = 0.208. The yr effect does not differ significantly across strata under this pooling. The adjusted yr coefficient is 2175.8, 95% CI [2024.2, 2327.5], p = 1.7e-118.
- **Disagreement between stat_3 and stat_4:** applying the same yr-only interaction test to the unpooled three-level weathersit gives p = 0.036 (df = 11), not the stat_3 value of 0.0057. stat_4 suggests that stat_3's test may use a different construction. This has not been confirmed, and the two results are reported here as disagreeing. The pooled result (p = 0.208) and the unpooled check (p = 0.036) also differ because of the pooling itself.

The corrected stratum chart (all 12 strata, with every stratum having days in both years) is:

![Mean cnt difference between yr 1 and yr 0 for each of the 12 season x weathersit strata; every stratum has days in both years, so none is omitted; per-stratum day counts are in stat3_strata_diff](tasks/stat_3/charts/stat3_yr_within_strata_v2.png)

### Prediction (ml_1 and ml_2)

**Feature table.** The 11 features are season, yr, mnth, holiday, weekday, workingday, weathersit, temp, atemp, hum and windspeed. Excluded columns are casual and registered (leaky), and instant and dteday (identifiers). No imputation was needed. An 80/20 split with random_state=42 gives 584 training rows and 147 test rows.

**Leakage.** registered alone predicts cnt with in-sample R² 0.894 over all 731 rows. Both leaky columns were excluded from all models.

**Scores on the 147-row test set:**

| Model | Test RMSE | Test MAE | Test R² | Train R² |
|---|---|---|---|---|
| Mean-of-training-target baseline (mean 4561) | 2022.2 | 1712.0 | -0.020 | — |
| Linear regression | 831.3 | 617.4 | 0.828 | 0.791 |
| Random forest (300 trees) | 674.2 | 426.2 | 0.887 | 0.982 |

The random forest is the best of the three. Its training R² of 0.982 indicates some overfitting. These scores come from one split (random_state=42).

**Feature importance.**
- Random forest impurity importance: temp (0.362), yr (0.282), atemp (0.142), hum (0.059), season (0.053).
- Random forest permutation importance on the test set (mean drop in R²): yr 0.526, temp 0.298, hum 0.086, atemp 0.074, season 0.050, mnth 0.038. holiday contributes 0.0004.
- Linear regression ranks atemp (coefficient 3488.0), temp (2097.2) and windspeed (2080.5) highest by absolute coefficient, followed by yr (2024.0). These are correlated temperature terms, so the coefficients are not directly comparable.

![Random forest permutation importance on the rental_split test set: mean drop in test R^2 when each feature is shuffled](tasks/ml_2/charts/ml2_rf_permutation_importance.png)

## Limitations

**Review issues, unresolved at the time of writing:**

- **eda_1 (weathersit):** the earlier statement that level 3 is about 2,800 below level 1 is wrong. The correct figure is 3,073.5 (4876.8 vs 1803.3). The corrected figure is used above. The month table was missing its medians and group sizes, and these are now included.
- **stat_2 (interpretation):** the wording "clearly absent" for the workingday x weathersit interaction is withdrawn. The finding is only that no significant interaction was detected (F = 0.52, df = 2, p = 0.598). With 5 and 16 days in the weathersit 3 cells, the test has little power to detect one. For season x yr (p = 0.064), the finding is not significant at 0.05 and is borderline; it is not evidence that the interaction is absent. The analysis used Type II sums of squares. Type III is the usual choice when interaction terms are present, and it was not run.
- **stat_3 (interaction test):** the stat_3 interaction p-value (0.0057) is not verified. stat_4's check gives p = 0.036 under a yr-only test with the same unpooled levels, so stat_3's test should be re-checked. The stat_3 weathersit-3-dropped result (p = 0.046) depends on the same test and carries the same doubt. The stat_3 conclusion that heterogeneity holds marginally is superseded by stat_4's pooled result (p = 0.208).
- **stat_3 (chart):** the caption on stat3_yr_within_strata claimed that single-day cells were omitted. This is incorrect, since no stratum was dropped. The corrected chart (stat3_yr_within_strata_v2) is the one embedded above, and the earlier chart is not used.
- **stat_4 (pooling):** the pooled interaction test was not run as a permutation test, so its robustness to the small cell counts (7 of the 24 season x weathersit x yr cells have fewer than 5 days) is unknown.

**Other caveats:**

- Holiday (21 days) and weathersit level 3 (21 days) rest on small groups, so their estimates are less stable.
- The holiday and workingday results are not significant. This does not show that these effects are absent.
- Group comparisons are unadjusted, except where stated as OLS adjustment for season and weathersit. The adjusted yr effect rests on a model with only these controls and does not include temperature or humidity.
- The stratum-level yr differences are imprecise, and the adjusted yr coefficient is an average across strata that differ.
- The random forest and linear regression results come from a single 80/20 split.
- No failed tasks were reported.

## Open questions

- Does the yr effect reflect real ridership growth after controlling for season and weather? The adjusted models show a yr difference, but the analysis does not establish what drives it.
- Does the season x yr interaction (p = 0.064) change once temperature and humidity are controlled for?
- Does the yr x (season, weathersit) heterogeneity hold? stat_3 (p = 0.0057) and stat_4 (p = 0.036 unpooled, p = 0.208 pooled) disagree, and stat_3's test needs re-checking. A permutation test on the stratum interaction has been suggested.
- Does the yr effect hold when weathersit 3 is pooled into level 2 rather than dropped? stat_4 has answered this: the interaction is not significant under pooling (p = 0.208).
- Does adding temperature or other weather variables change the adjusted yr coefficient and the interaction result?
- Are the workingday effects within weathersit level 3 estimable with more data, given 5 and 16 days in those cells?
- Is the holiday effect real, or within noise given 21 holiday days? A larger sample or a model with controls is needed.
- Would a day-index feature derived from dteday improve prediction beyond the 11 features?