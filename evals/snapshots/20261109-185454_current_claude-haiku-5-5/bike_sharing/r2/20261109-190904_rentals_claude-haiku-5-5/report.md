# Bike Rental Demand: Daily Rental Count (cnt) Analysis

## Summary

- **Season, year and weather are the clearest associations with daily rentals.** Season (ANOVA F=128.77, p=6.7e-67, eta squared 0.347), yr (Welch t p=1.0e-62, Cohen's d=1.37) and weathersit (ANOVA F=40.07, p=3.1e-17, eta squared 0.099) all stay significant after Holm correction. Holiday and workingday do not.
- **A random forest predicts cnt best on the shared test split.** It reaches test MAE 434.96 and R² 0.881, against 617.39 and R² 0.828 for linear regression and 1711.99 for the mean baseline.
- **Temperature keeps a significant association with cnt after controlling for season and yr.** The OLS coefficient is 5338.96 rentals per unit of temp (95% CI 4644.50 to 6033.41, p=5.8e-45). The partial Spearman correlation is 0.486, lower than the raw Spearman rho of 0.622.
- **The only significant interaction is yr × weathersit, and it is not robust.** It is significant under the original coding (F=4.22, p=0.015) but not after merging weathersit 2 and 3 (F=2.70, p=0.101). The season × workingday interaction is not significant (p=0.213).
- **The data are clean, but the target has a leakage risk.** There are no missing values. cnt equals casual plus registered in every row, so both were excluded from all features and models.

## Data

- **Size:** 731 rows × 16 columns.
- **Target:** cnt, a daily count of bike rentals (regression).
- **Features:** 13 numeric columns (season, yr, mnth, holiday, weekday, workingday, weathersit, temp, atemp, hum, windspeed, casual, registered). There are no categorical or date/time features.
- **Excluded:** instant and dteday are identifiers and were not used as features. casual and registered were excluded because cnt equals casual plus registered in every row. registered alone correlates 0.946 with cnt, so it is a leakage risk.
- **Missing values:** none (0 total across all columns).

## Findings

### Distribution and descriptive differences

Daily cnt has mean 4504.35, median 4548, standard deviation 1937.21, minimum 22, maximum 8714, Q1 3152 and Q3 5956. The distribution is roughly centred, with a long tail toward low counts.

![Histogram of daily total rentals (cnt), counts of days per bin](tasks/eda_1/charts/cnt_histogram.png)

**Season.** Season 1 has the lowest mean (2604.13, median 2209, n=181). Season 2 has mean 4992.33 (median 4941.5, n=184), season 3 the highest mean at 5644.3 (median 5353.5, n=188), and season 4 has mean 4728.16 (median 4634.5, n=178).

**Year.** Mean cnt is 3405.76 (median 3740, n=365) in yr 0 and 5599.93 (median 5927, n=366) in yr 1. The 2012 level is much higher than 2011. This descriptive finding does not show whether the growth is steady or a step change.

**Month.** January is the lowest (mean 2176.34, median 1939, n=62). Mid-year months are much higher; for example, month 4 has mean 4484.9 (median 4293.5, n=60).

**Holiday.** Non-holidays have mean 4527.1 (median 4558, n=710). Holidays have mean 3735 (median 3351, n=21). The holiday group is small.

**Weekday.** Mean cnt by weekday ranges from 4228.83 (weekday 0, median 4334, n=105) to 4690.29 (weekday 5, median 4601.5, n=104). The spread across weekdays is modest.

**Working day.** Non-working days have mean 4330.17 (median 4459, n=231). Working days have mean 4584.82 (median 4582, n=500).

**Weather.** Clear weather (1) has mean 4876.79 (median 4844, n=463). Mist (2) has mean 4035.86 (median 4040, n=247). Heavy rain or snow (3) has mean 1803.29 (median 1817, n=21).

![Mean and median daily rentals (cnt) by season, mnth, weathersit and weekday](tasks/eda_1/charts/cnt_by_groups.png)

**Continuous weather variables (binned, descriptive).**
- **Temperature:** mean cnt rises with temperature. The lowest bin (0.058 to 0.26) has mean 1819.7 (n=73). The 0.26 to 0.46 bin has mean 3596.72 (n=257), the 0.46 to 0.661 bin 5547.67 (n=228), and the 0.661 to 0.862 bin 5610.49 (n=173).
- **Humidity:** the pattern is weaker. The 0.243 to 0.486 bin has mean 4269.67 (n=116), the 0.486 to 0.729 bin 4859.78 (n=426), and the 0.729 to 0.972 bin 3876.33 (n=187). The lowest bin has only 2 days.
- **Windspeed:** mean cnt falls as windspeed rises. The calmest bin (0.022 to 0.144) has mean 4911.75 (n=220). The 0.265 to 0.386 bin has mean 3849.58 (n=106).

### Significance tests and effect sizes

Holm correction was applied across the five categorical tests.

| Feature | Test | Result | Holm-adjusted p | Significant at 0.05 |
|---|---|---|---|---|
| season | ANOVA | F=128.77, p=6.7e-67; Kruskal-Wallis p=4.1e-54; eta squared 0.347 | 3.4e-66 | Yes |
| weathersit | ANOVA | F=40.07, p=3.1e-17; Kruskal-Wallis p=2.6e-15; eta squared 0.099 | 9.3e-17 | Yes |
| yr | Welch t | p=1.0e-62; Mann-Whitney p=7.1e-54; Cohen's d=1.37 | 4.2e-62 | Yes |
| holiday | Welch t | p=0.103; Mann-Whitney p=0.083; Cohen's d=-0.41 (holiday group n=21) | 0.206 | No |
| workingday | Welch t | p=0.110; Mann-Whitney p=0.119; Cohen's d=0.13 | 0.206 | No |

The season group means with 95% CIs are: season 1 2604.13 (2398.80 to 2809.46), season 2 4992.33 (4745.65 to 5239.02), season 3 5644.30 (5434.27 to 5854.33), season 4 4728.16 (4476.76 to 4979.56).

The weathersit group means with 95% CIs are: clear 4876.79 (4705.14 to 5048.43), mist 4035.86 (3809.13 to 4262.59), heavy rain or snow 1803.29 (1238.72 to 2367.86, n=21).

The year means with 95% CIs are: 2011 3405.76 (3263.84 to 3547.68), 2012 5599.93 (5416.08 to 5783.79).

Holiday means are 4527.10 (4384.97 to 4669.24) for non-holidays and 3735.00 (2777.57 to 4692.43) for holidays. Working-day means are 4330.17 (4064.13 to 4596.20) for non-working days and 4584.82 (4419.77 to 4749.87) for working days.

![Mean daily rentals (cnt) with 95% confidence intervals by season and weather situation](tasks/stat_1/charts/stat1_cnt_means_ci.png)

**Continuous variables (Spearman, exploratory, not corrected for multiple comparisons).**
- temp: rho=0.622 (p=1.7e-79)
- atemp: rho=0.623 (p=9.6e-80)
- windspeed: rho=-0.217 (p=3.0e-9), a weak negative association
- hum: rho=-0.098 (p=0.008), a very weak negative association

### Interactions

**season × workingday.** The interaction is not significant (nested F=1.50, p=0.213). Adding it raises R² only from 0.349 to 0.353, so it is not worth reporting. Within seasons, the working-day gaps are small. Season 1 has 2257 (non-working) vs 2781 (working). Season 2 has 5142 vs 4927. Season 3 has 5475 vs 5718. Season 4 has 4606 vs 4786.

**yr × weathersit.** The interaction is significant under the original three-category coding (nested F=4.22, p=0.015), with R² rising from 0.399 to 0.406. The weathersit 3 cells are very small: 15 days in 2011 and 6 days in 2012. Mean cnt for weathersit 1, 2 and 3 is 3695, 3088 and 1674 in 2011, and 6004, 4991 and 2126 in 2012. The drop from clear to mist is larger in 2012 than in 2011, and the heavy-weather drop is also larger in 2012.

![Mean daily rentals (cnt) by season and workingday, and by yr and weathersit; non-parallel lines indicate an interaction](tasks/stat_2/charts/interaction_means.png)

**Robustness of yr × weathersit.** The two checks disagree on significance, so both results are reported:
- Under the original coding, the interaction is significant (F=4.22, p=0.015).
- With weathersit 2 and 3 merged (139 days in 2011 and 129 in 2012), it is not significant (F=2.70, p=0.101). R² moves only from 0.377 to 0.379. This merge also weakens the heavy-weather contrast, so it is not a pure test of the same question.
- A bootstrap resampling each yr × weathersit cell gives an observed difference of 1857 in the clear-to-heavy drop (2012 minus 2011), with a 95% CI of 282 to 3337. Only 0.9% of 2000 resamples were non-positive. The 6-day 2012 heavy-weather cell drives the wide interval, so the bootstrap supports a direction but not a precise size.

The overall conclusion is that the yr × weathersit interaction is a tentative pattern, not a firm claim.

### Temperature after controlling for season and year

In an OLS model of cnt on temp with season dummies and yr, temp has a coefficient of 5338.96 rentals per unit (95% CI 4644.50 to 6033.41, p=5.8e-45), with model R² 0.749 (n=731). The R² describes the whole model, including season and yr, so it does not isolate temp's own contribution.

Observed temp values run from 0.059 to 0.862 (mean 0.495). Temp appears to be min-max normalised to a 0-to-1 scale, but this is inferred from the observed range and not confirmed. The OLS estimate assumes a linear effect, and residual checks (linearity, homoscedasticity, normality) were not reported.

The partial Spearman correlation between temp and cnt, controlling for season and yr, is rho=0.486 (approximate 95% CI 0.428 to 0.540, p=1.4e-44). This is lower than the raw Spearman rho of 0.622, so part of the raw rank association is accounted for by season and yr. The p-value and CI are uncorrected and exploratory, and the CI is a Fisher approximation.

### Predictive models

**Shared split and baseline.** An 80/20 split with random_state 42 gives 584 training rows and 147 test rows. The 11 features are season, yr, mnth, holiday, weekday, workingday, weathersit, temp, atemp, hum and windspeed. Predicting the training mean (4560.98) for every test day gives test MAE 1711.99 and RMSE 2022.17.

**Model comparison.**

| Model | Train R² | Test R² | Test RMSE | Test MAE |
|---|---|---|---|---|
| Mean baseline | n/a | n/a | 2022.17 | 1711.99 |
| Linear regression | 0.791 | 0.828 | 831.29 | 617.39 |
| Random forest | 0.970 | 0.881 | 690.29 | 434.96 |

Both models beat the baseline. The random forest is the stronger model, but it is moderately overfitted (train R² 0.970 against test R² 0.881). Linear regression is more stable across train and test (train R² 0.791, test R² 0.828).

![Test MAE and RMSE of cnt: mean baseline vs linear regression vs random forest](tasks/ml_2/charts/ml2_model_comparison.png)

**Leakage check.** registered (Pearson r 0.946 with cnt) and casual (r 0.673) are excluded from both models, so neither uses the target's components.

**Feature importance.**
- Linear regression's largest absolute coefficients are atemp (3488.04), temp (2097.25), windspeed (2080.54) and yr (2024.00).
- Random forest permutation importance (drop in test MAE) is yr 800.0, temp 563.0, atemp 219.9, season 141.6, hum 139.9 and mnth 117.0. Windspeed contributes 41.1. The small contributors are weekday 26.9, weathersit 24.3 and workingday 11.8. Holiday contributes 0.3.
- Random forest impurity importance puts temp (0.365) and yr (0.287) first.

**Weather versus calendar features.** The summed permutation importance is 1098 for calendar features (yr, season, mnth, weekday, workingday, holiday) and 988 for weather features (temp, atemp, hum, windspeed, weathersit). Weather features account for 47% of the total. Neither group clearly dominates. The result depends on yr, which is classed as a calendar feature here and is the single largest permutation importance (800.0). The largest weather feature is temp alone (563.0). Because temp and atemp are correlated, the group sums are approximate.

## Limitations

- **Leakage:** cnt equals casual plus registered in every row, and registered correlates 0.946 with cnt. Both were excluded from all models, but a model that included them would not be a valid predictor of cnt.
- **Small groups:** the holiday group has 21 days and the weathersit 3 group has 21 days. Split by year, the weathersit 3 cells have only 15 and 6 days. Group estimates for these levels are unstable.
- **Interaction evidence:** the yr × weathersit interaction is significant only under the original coding. It is not significant after merging weathersit 2 and 3, and the bootstrap interval is very wide. It should be treated as tentative. The season × workingday interaction is not significant.
- **Non-significant workingday and holiday effects:** neither survives Holm correction (both adjusted p=0.206). Their descriptive differences should not be read as established effects.
- **Exploratory tests:** the Spearman results were not corrected for multiple comparisons. The partial Spearman CI is a Fisher approximation.
- **Temperature model assumptions:** the temp OLS estimate assumes a linear effect. Residual checks (linearity, homoscedasticity, normality) were not reported. The 0-to-1 scale of temp is inferred from its observed range, not confirmed.
- **Confounding:** temp, season and month are strongly related, and the descriptive group differences are not adjusted for each other.
- **Weather versus calendar importance (unresolved review issue):** the lead's objection still stands. The 47% weather share and the 53% calendar share are close, so the groups should not be described as unequal, and calendar features should not be described as clearly dominant. The result depends on yr, which is classed as calendar here and is the single largest permutation importance (800.0). Temp alone (563.0) is the largest weather feature. This affects the feature-importance findings in the predictive models section.
- **Failed tasks:** none. All tasks (eda_1, stat_1, stat_2, ml_1, ml_2, stat_3, stat_4) completed.

**Numbers not traced to a recorded fact.** The automatic check found no recorded value for these numbers:
- 53% in: "- **Weather versus calendar importance (unresolved review issue):** the lead's objection still stands. The 47% weather share and the 53% calendar share are clos"

## Open questions

- Does the temp effect differ by season (a temp × season interaction)?
- Is the temp association stable when hum and windspeed are added to the model? Do residuals show non-linearity, and would a non-linear temp term improve fit?
- Does temp still explain cnt after controlling for season and yr once the other variables are included? The association holds with season and yr controlled, but it was not tested with the other weather variables in the model.
- Is the 2011 to 2012 increase a steady trend or a step change? Does the 2012 growth differ by season after controlling for temperature?
- Do weekday differences matter once workingday is controlled for? The weekday effect was described but not tested.
- Are the holiday (21 days) and weathersit 3 (21 days) means stable enough to rely on? The yr × weathersit results suggest the heavy-weather estimates are unstable, and more heavy-weather days would be needed to settle the question.