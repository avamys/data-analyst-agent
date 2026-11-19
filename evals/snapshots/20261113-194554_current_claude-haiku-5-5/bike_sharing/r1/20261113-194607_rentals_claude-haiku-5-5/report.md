# Bike Rental Demand: Daily Total Rentals (cnt) Across Season, Year, Weather and Calendar Features

## Summary

- **cnt is roughly symmetric.** Daily cnt has a mean of 4504.3, a median of 4548, and a range of 22 to 8714 over 731 days. Season, yr, mnth and weathersit differ significantly in cnt (epsilon-squared 0.090 to 0.380). Weekday, holiday and workingday do not differ significantly.
- **Year is the largest permutation-importance feature.** 2012 averages 2194 more rentals than 2011 (95% CI 1962 to 2426). In the gradient boosting model, yr has the highest permutation importance (889.3).
- **Season is associated with cnt after weather adjustment, tentatively.** Temp has the largest binned effect on cnt. In a regression adjusting for temp, atemp, hum and windspeed, season is jointly associated with cnt (F(3, 723) = 37.27, p = 2.1e-22). This model does not control for yr or mnth, so the season effect is not yet established as independent of year.
- **Interactions are significant but small.** The season x workingday interaction (partial eta-squared 0.022) and the yr x weathersit interaction (partial eta-squared 0.013) are both statistically significant and small. The yr x weathersit heavy-weather cells rest on 15 and 6 days.
- **Gradient boosting predicts cnt best.** On the seeded test split it reaches RMSE 662.3 and R² 0.891, against RMSE 2022.2 and R² -0.020 for the mean baseline, and RMSE 831.3 and R² 0.828 for linear regression.

## Data

- 731 daily rows and 16 columns.
- Target: cnt (daily total rentals).
- Missing values: none in any column.
- Excluded from model features:
  - casual and registered, because they sum exactly to cnt on every row. This is leakage: the dataset profile flags registered as predicting the target almost perfectly (0.946).
  - instant and dteday, which are identifiers.
- Model features: 11 legitimate columns (season, yr, mnth, holiday, weekday, workingday, weathersit, temp, atemp, hum, windspeed).
- The 16 columns are 13 numeric columns (including casual and registered), plus instant, dteday and cnt.
- The dataset has no categorical or date/time features.

## Findings

### Distribution of cnt

cnt is roughly symmetric and unimodal (skew -0.05). The 30-bin histogram peaks at 49 days in the bin 4078 to 4368, with a long but thin left tail of low-count days.

![Histogram of daily total rentals (cnt), 731 days](tasks/eda_1/charts/cnt_histogram.png)

### Group differences and significance

**Omnibus tests (Kruskal-Wallis, Bonferroni correction across 7 tests):**

| Feature | k | H | p | Epsilon-squared | Survives correction |
|---|---|---|---|---|---|
| season | 4 | 250.9 | 4.1e-54 | 0.341 | Yes |
| yr | 2 | 238.8 | 7.0e-54 | 0.326 | Yes |
| mnth | 12 | 284.3 | 1.8e-54 | 0.380 | Yes |
| weathersit | 3 | 67.2 | 2.6e-15 | 0.090 | Yes |
| weekday | 7 | 4.3 | 0.63 | -0.002 | No |
| holiday | 2 | 3.0 | 0.083 | 0.003 | No |
| workingday | 2 | 2.4 | 0.119 | 0.002 | No |

**Season.** Mean cnt is 2604 (median 2209, n=181) in season 1, 4992 (median 4942, n=184) in season 2, 5644 (median 5354, n=188) in season 3 and 4728 (median 4635, n=178) in season 4.

**Year.** 2011 averages 3406 (median 3740, n=365) and 2012 averages 5600 (median 5927, n=366). The 2012 minus 2011 difference is 2194 (95% CI 1962 to 2426; Welch p=1.0e-62; Mann-Whitney p=7.1e-54; rank-biserial 0.66), described in the source as a very large effect.

**Month.** Mean cnt is lowest in January (2176, median 1939, n=62) and February (2655, median 2402, n=57). It peaks around June to September (5772 in June, 5564 in July, 5664 in August, 5767 in September) and falls to 3404 in December (n=62). The pattern is a smooth seasonal hump.

**Weather.** Clear days average 4877 (median 4844, n=463), mist days 4036 (median 4040, n=247), and heavy-weather days 1803 (median 1817, n=21).

**Weekday.** Means range from 4229 (median 4334, n=105) on weekday 0 to 4690 (median 4602, n=104) on weekday 5. The weekday gap is small relative to the month gap, and the test is not significant.

**Holiday.** Holidays (n=21) average 792 cnt lower than other days (95% CI -1758 to +174; Welch p=0.103; Mann-Whitney p=0.083; rank-biserial -0.22). This is not significant at 0.05 and does not survive correction. The estimate rests on 21 holidays.

**Workingday.** Working days average 255 cnt higher (95% CI -58 to +567; Welch p=0.110; Mann-Whitney p=0.119; rank-biserial 0.07). This is not significant. Working days average 4585 (median 4582, n=500) and non-working days 4330 (median 4459, n=231).

**Continuous variables (Spearman correlation with cnt, and binned means):**
- temp: rho 0.622 (p=1.7e-79). Mean cnt is 2615 in the lowest temp quartile and 5631 in the highest.
- atemp: rho 0.623 (p=9.6e-80). Mean cnt is 2627 in the lowest atemp quartile and 5625 in the highest.
- windspeed: rho -0.217 (p=3.0e-9). Mean cnt falls from 4923 in the lowest quartile to 3978 in the highest.
- hum: rho -0.098 (p=0.008). This weak association survives Bonferroni correction for 4 tests. Mean cnt is 4378 in the lowest quartile, 4852 and 4914 in the two middle quartiles, and 3879 in the highest.

### Interactions

**Season x workingday.** The interaction is significant (F=5.41, p=0.0011) but small (partial eta-squared 0.022). The workingday difference (working minus non-working) changes sign between seasons 1 and 2.

| Season | Non-working mean cnt | Working mean cnt | Working minus non-working |
|---|---|---|---|
| 1 | 2257.1 | 2780.5 | +523.4 |
| 2 | 5142.4 | 4926.7 | -215.8 |
| 3 | 5474.7 | 5718.1 | +243.4 |
| 4 | 4606.2 | 4785.6 | +179.4 |

Cell counts for these season x workingday cells are not recorded in the findings. The sign reversal means a single pooled workingday effect would misstate the direction of the effect in at least one season. The interaction comes from a two-way OLS model with both interactions, which had R² 0.750.

**Year x weathersit.** The interaction is significant (F=4.61, p=0.010) but small (partial eta-squared 0.013). The year gain is smaller on heavy-weather days than on clear or mist days. Heavy-weather cells are thin.

| Weathersit | 2011 mean cnt (n) | 2012 mean cnt (n) |
|---|---|---|
| 1 (clear) | 3695.0 (n=226) | 6003.7 (n=237) |
| 2 (mist) | 3088.1 (n=124) | 4991.3 (n=123) |
| 3 (heavy) | 1674.1 (n=15) | 2126.2 (n=6) |

The heavy-weather year gap rests on 15 days in 2011 and 6 days in 2012 and should be treated as tentative.

![Mean daily cnt by season within workingday (left) and by weathersit within year (right); lines that are not parallel indicate interaction](tasks/stat_2/charts/interaction_means.png)

### Season within temperature quartiles

Mean cnt (n) by season within each temp quartile (Q1 coldest, Q4 warmest). Cells that the source flags as thin are marked "thin", and empty cells are marked "empty".

| Season | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| 1 | 2105.6 (n=123) | 3313.8 (n=49) | 5553.4 (n=9, thin) | empty (n=0) |
| 2 | 2277.6 (n=14, thin) | 4577.1 (n=49) | 5477.6 (n=88) | 5466.5 (n=33) |
| 3 | empty (n=0) | 4635.5 (n=2, thin) | 5704.1 (n=38) | 5642.6 (n=148) |
| 4 | 4080.0 (n=46) | 4460.4 (n=83) | 5719.4 (n=47) | 7450.0 (n=2, thin) |

The source reports max-minus-min season gaps within each quartile: Q1 1974, Q2 1322, Q3 242 and Q4 1984. These gaps use different season pairs in each quartile (Q4 uses seasons 2 to 4 only), so they are not comparable with each other and cannot be subtracted from the unconditioned season 1 to season 3 difference. The only quartiles where seasons 1 and 3 both have rows are Q2 (season 3 n=2) and Q3 (season 1 n=9), and both are thin. A substantial season gap remains within Q1, Q2 and Q4. This persistence conclusion is tentative until a regression with temp and other weather covariates is run.

![Mean cnt by season within each temp quartile](tasks/eda_2/charts/season_gap_by_temp_quartile.png)

### Season after adjusting for weather (regression)

Adjusting for temp, atemp, hum and windspeed, season is jointly associated with cnt (F(3, 723) = 37.27, p = 2.1e-22; adjusted R² 0.531, R² 0.536, n=731). This is an association, not a causal effect.

Coefficients relative to season 1:
- Season 2: +884 (95% CI 526 to 1242; p=1.6e-6)
- Season 3: +380 (95% CI -94 to 854; p=0.116; not significant at 0.05)
- Season 4: +1437 (95% CI 1132 to 1743; p=2.8e-19)

The model omits yr, the strongest predictor in the other analyses, and omits mnth. Season may be confounded with the year trend, so these coefficients are not adjusted for year.

### Predictive performance

Models were trained on 584 rows and tested on 147 rows (seeded split, random_state=42), using the 11 legitimate features.

| Model | RMSE | MAE | R² |
|---|---|---|---|
| Mean baseline | 2022.2 | 1712.0 | -0.020 |
| Linear regression | 831.3 | 617.4 | 0.828 |
| Gradient boosting | 662.3 | 462.8 | 0.891 |

Gradient boosting has the lowest error on all three measures. Both models have much lower RMSE than the mean baseline. These scores come from a single split with no tuning reported.

![Test RMSE of predicting daily cnt for the mean baseline, linear regression and gradient boosting](tasks/ml_1/charts/ml1_model_rmse.png)

### Feature importance (gradient boosting, permutation on test split)

Increase in test RMSE when each feature is permuted (30 repeats; sd in brackets):

1. yr: 889.3 (53.6)
2. temp: 656.5 (55.8)
3. hum: 224.5 (25.2)
4. season: 222.7 (31.0)
5. weathersit: 110.3 (16.8)
6. windspeed: 88.7 (24.0)
7. atemp: 65.4 (22.0)
8. mnth: 39.0 (11.7)
9. weekday: 26.0 (13.6)
10. holiday: 12.1 (13.9)
11. workingday: 1.7 (9.2)

yr ranks first overall. temp ranks well above atemp, although the two are strongly correlated, so permuting one is partly offset by the other.

**Agreement with the significance tests:**
- **yr**: agrees. It ranks first and is strongly significant (Kruskal-Wallis p=7.0e-54).
- **season**: agrees. Importance 222.7 and significant (p=4.1e-54, epsilon-squared 0.341).
- **mnth**: agrees. Importance 39.0 and significant (p=1.8e-54, epsilon-squared 0.380).
- **weathersit**: agrees. Importance 110.3 and significant (p=2.6e-15, epsilon-squared 0.090).
- **weekday**: partly agrees. Importance is small compared with the top features (26.0, sd 13.6), and the test is not significant (p=0.63). The sd is large relative to the estimate, so this agreement is weak.
- **holiday**: agrees in direction. Importance is small (12.1), its sd (13.9) is larger than the estimate, and the test is not significant (p=0.083).
- **workingday**: agrees. Importance is near zero (1.7, sd 9.2) and the test is not significant (p=0.119).

## Limitations

- **Leakage.** casual and registered sum exactly to cnt and were excluded. The dataset profile flags registered as predicting the target almost perfectly (0.946), so any model using it would be invalid.
- **Thin cells.** Heavy-weather days number 21 in total (15 in 2011, 6 in 2012). The holiday estimate rests on 21 days. Several season x temp-quartile cells contain 2 to 14 rows, and two cells are empty (Q1 season 3 and Q4 season 1).
- **Confounding not resolved.** Season, month and temp are strongly correlated. The season regression omits yr and mnth, and the within-quartile comparison does not adjust for weathersit or yr. The season effect is therefore not established as independent of year, month or weather.
- **Small interactions.** Both interactions are significant but small (partial eta-squared 0.022 and 0.013). The yr x weathersit heavy-weather estimate is tentative.
- **Interaction cell counts.** The season x workingday cell counts are not recorded in the findings, so the table above reports means only.
- **Model evaluation.** Model scores come from one seeded split with no tuning and no cross-validation reported. Permutation importances are model-based, and correlated features (temp and atemp) share importance.
- **Unresolved review issues, and how this report handles them:**
  - *stat_2:* the clear-day counts are 226 in 2011 and 237 in 2012. The per-cell table above uses these counts. The heavy-weather year gap is kept as tentative.
  - *ml_1:* the scores were reported against 13 features. The model used 11 legitimate features, confirmed by ml_2. The 13 is the numeric column count including the excluded casual and registered columns. This report uses 11.
  - *ml_2:* the agreement check was incomplete in the source. The check above covers season, mnth, weathersit, weekday, holiday and workingday, and yr.
  - *eda_2:* the source claimed the season gap shrinks in every quartile, using season pairs that are not comparable. This report removes that claim, gives the full table with thin cells marked, and states that the persistence conclusion is tentative.
- **Failed tasks.** None recorded.

## Open questions

- Does the season effect persist after adding yr and mnth to the regression, and does weathersit explain the season gap?
- Does temp explain the season and month effects once controlled for, given their strong correlation? How does permutation importance divide between temp and atemp when one is removed?
- Do season effects differ by year?
- Is the month effect within temperature quartiles consistent with the season effect?
- Are the largest prediction residuals concentrated in the rare heavy-weather days, and does a model trained without them behave differently?
- Would tuning gradient boosting or adding interaction terms close the remaining gap to linear regression's error?
- Are the per-cell differences robust to a nonparametric or log-scale model?
- Is the holiday effect stable with a larger sample or with controls?
- Is the yr x weathersit interaction stable given only 15 and 6 heavy-weather days?