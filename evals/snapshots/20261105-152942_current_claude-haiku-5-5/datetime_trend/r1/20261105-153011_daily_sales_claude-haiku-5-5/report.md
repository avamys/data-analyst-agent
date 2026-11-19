# Daily Sales Analysis: Promo, Temperature and Date Patterns in Sales (730 Days)

## Summary

- **Promo days have the largest association with sales in this data.** Promo days average 32.1 units more than non-promo days (Welch t = 7.79, p = 1.3e-12; 95% CI 24.0 to 40.3; Cohen's d = 0.81). Promo is also the top feature in both predictive models.
- **Temperature shows no meaningful linear relation with sales.** The Pearson r is 0.016 (95% CI -0.057 to 0.088, p = 0.67), and mean sales are nearly flat across temperature quartile bands.
- **Sales rise over time, and this trend, not calendar month, accounts for the monthly pattern.** The linear trend is about 55 units per year. Once it is removed, the 11 month indicators are jointly non-significant (F = 0.496 on 11 and 716 degrees of freedom, p = 0.906). Weekend days sell 38.22 units more than weekdays after adjusting for promo, temperature and trend (95% CI 35.75 to 40.68).
- **Temperature and promo predict sales only slightly better than a mean baseline.** Linear regression lowers test MAE from 31.68 to 29.60 and reaches a test R² of 0.069. The random forest does worse than the baseline on the test set.
- **Whether promo's effect changes with temperature is unresolved.** The interaction is not significant (p = 0.41), but its 95% CI (-0.68 to 1.67 units per degree) is wide enough to include changes that would matter.

## Data

- 730 rows × 4 columns (date, temperature, promo, sales).
- Target: sales (continuous, regression).
- Numeric features: temperature, promo (binary). No categorical features.
- The date column is not used as a raw feature. It was used only to derive time, month and weekday terms in the date analysis.
- Missing values: none in any column, so all 730 rows were used.

## Findings

### Sales distribution

Daily sales are roughly symmetric and unimodal: mean 270.84, median 270.25, std 41.13, skew 0.10, range 178.3 to 391.8. The peak histogram bin spans about 292.2 to 299.3 (50 days), and 65.8% of days fall within one standard deviation of the mean.

![Distribution of daily sales across all 730 rows](tasks/eda_1/charts/sales_histogram.png)

### Promo effect

- Promo = 0 (n = 626): mean 266.27, median 266.40.
- Promo = 1 (n = 104): mean 298.39, median 295.40.
- Welch test (promo = 1 minus promo = 0): difference 32.1 units, 95% CI 24.0 to 40.3, t = 7.79, p = 1.3e-12, Cohen's d = 0.81.

### Promo effect within temperature bands

Temperature quartile bands (edges in degrees): Q1 -4.0 to 6.4 (n = 184), Q2 6.4 to 12.4 (n = 183), Q3 12.4 to 18.1 (n = 181), Q4 18.1 to 28.1 (n = 182). Mean sales by band are 269.61, 273.74, 266.61 and 273.38, a spread of about 7 units.

Within each band, promo days sell more than non-promo days, and each difference is significant:

| Band | Promo n | Mean difference | p | Cohen's d |
|---|---|---|---|---|
| Q1 | 28 | 21.9 | 0.008 | 0.54 |
| Q2 | 31 | 40.6 | < 0.001 | 0.95 |
| Q3 | 19 | 29.4 | 0.003 | 0.76 |
| Q4 | 26 | 34.0 | 0.0004 | 0.95 |

The band estimates range from 21.9 to 40.6. The interaction test is not significant, and the subgroups are small (the smallest has 19 promo days), so these differences do not establish or rule out a real change in promo's effect across temperature.

![Mean sales difference between promo=1 and promo=0 days within each temperature quartile](tasks/stat_1/charts/promo_effect_by_temp_band.png)

### Temperature and sales

- Pearson r between temperature and sales across all 730 rows is 0.016 (95% CI -0.057 to 0.088, p = 0.67).
- Mean sales are nearly flat across temperature bands (see above).

### Promo × temperature interaction

In the OLS model sales ~ promo × temperature, the interaction coefficient is 0.49 units per degree (95% CI -0.68 to 1.67, p = 0.41). The CI includes changes in the promo effect large enough to matter across the observed temperature range (-4.0 to 28.1). The data therefore cannot rule out that promo's effect changes with temperature.

The promo coefficient in this model (26.4) is the effect at temperature 0, which lies outside the observed range. It is not the average promo effect. The average effect is the 32.1 Welch difference above.

### Per-promo temperature correlations

Pearson correlations of temperature with sales, computed within each promo group:

- Promo = 0 (n = 626): r = 0.013, essentially no trend.
- Promo = 1 (n = 104): r = 0.103, a weak positive slope.

The two groups overlap heavily along the temperature axis, and the promo = 1 group sits higher overall. No significance test is reported for the promo = 1 correlation.

![Scatter of daily sales against temperature, colored by promo flag](tasks/eda_1/charts/sales_vs_temp_by_promo.png)

### Predictive models

Test-set results on the same split (n_train = 584, n_test = 146), with features limited to temperature and promo:

| Model | Test MAE | Test RMSE | Test R² |
|---|---|---|---|
| Mean-sales baseline | 31.68 | 38.78 | n/a |
| Linear regression | 29.60 | 36.72 | 0.069 |
| Random forest | 32.07 | 39.82 | -0.095 |

- Linear regression improves slightly on the baseline. The features explain only a small share of sales variation.
- The random forest does not beat the baseline on the test set despite a train R² of 0.256, which indicates overfitting to the training split.
- Permutation importance (drop in test R²) ranks promo first in both models: promo 0.137 versus temperature 0.002 in the linear model, and promo 0.134 versus temperature -0.002 in the forest.
- The forest's impurity-based importance ranks temperature first (0.80 versus 0.20 for promo). This disagrees with its permutation ranking. The analysis judged impurity importance unsuitable for ranking these features, so the permutation ranking is the one reported.

![Test-set MAE and RMSE for the mean baseline, linear regression and random forest on temperature and promo](tasks/ml_1/charts/model_comparison_test_errors.png)

### Date patterns: trend, months and weekdays

- **Monthly means (pooled across 2023 and 2024):** range from 247.69 (January) to 294.01 (November). Monthly n ranges from 57 to 62.
- **Year-over-year level:** every 2024 month is higher than the matching 2023 month. For example, January is 275.71 in 2024 versus 219.66 in 2023, and December is 324.43 versus 262.69.
- **Trend:** the linear trend is about 55.9 units per year. Mean sales are 243.20 in the first year and 298.48 in the second.
- **Rolling mean:** the 30-day rolling mean ranges from 218.61 to 326.05.
- **Within-year pattern:** sales rise from January to July within 2023 and again within 2024. The analysis therefore treats the monthly ordering as possibly reflecting the trend rather than a yearly cycle.
- **Weekday pattern (unadjusted):** Monday 260.91, Tuesday 257.30, Wednesday 258.72, Thursday 259.47, Friday 261.91, Saturday 297.25, Sunday 300.15.
- **Weekend vs weekday (unadjusted):** weekend mean 298.70 (n = 209) versus weekday mean 259.66 (n = 521).
- **Promo share:** 15.8% of weekend days and 13.6% of weekday days have promo = 1.

![Daily sales with 30-day centered rolling mean over the date range](tasks/eda_2/charts/sales_rolling_trend.png)

![Mean daily sales by day of week and by calendar month over the full date range](tasks/eda_2/charts/sales_by_dow_month.png)

### Weekend effect after adjustment

In an OLS model of sales on weekend, promo, temperature and a linear time term (HC1 standard errors, n = 730, R² = 0.867):

- Weekend coefficient: 38.22 units (95% CI 35.75 to 40.68, p ≈ 1e-202). This is close to the unadjusted weekend–weekday gap (298.70 vs 259.66), so the weekend effect holds after adjustment and is separate from the upward trend.
- Promo coefficient: 30.59 (p ≈ 2e-86).
- Temperature coefficient: -0.029 (p = 0.70, not significant).
- Time coefficient: 55.86 units per year.
- Promo is not concentrated on weekends: chi-square = 0.57, p = 0.45. The analysis concludes that promo cannot explain the weekend gap.

### Calendar-month effects after trend and promo

In the model sales ~ time + month + promo:

- Joint F-test for the 11 month indicators (relative to January): F = 0.496 on 11 and 716 degrees of freedom, p = 0.906. Calendar-month effects do not remain once the trend and promo are included.
- Individual month coefficients are all small and non-significant. They range from 0.01 (May, p = 0.998) to 5.90 (September, 95% CI -2.62 to 14.42, p = 0.174). Every CI includes zero.
- Adding the 11 month indicators raises R² only from 0.691 to 0.693.
- In the full model the trend is 55.15 units per year, promo adds 31.95 units (95% CI 27.07 to 36.82), and the residual SD is 22.99.

These results agree with the earlier monthly pattern being explained by the trend and promo. They are not in conflict with the within-year rises noted above.

## Limitations

- **Observational data.** None of the associations are shown to be causal. The analysis itself asks whether promo is confounded with season or store, and this is not tested.
- **Promo subgroups are small.** Promo = 1 has 104 rows overall, and the temperature-band subgroups have 19 to 31 promo days each. The band-level promo estimates are imprecise.
- **Interaction unresolved.** The promo × temperature interaction is not significant, but its CI is wide enough to include changes in promo's effect large enough to matter across the observed temperature range. The question is open, not answered.
- **Temperature treated linearly in the adjusted models.** The weekend and month models assume a linear temperature term. The analysis raised whether a non-linear or banded term would change the temperature control, and this was not tested.
- **Monthly means are pooled across two years.** The month table mixes the 2023-to-2024 rise with any calendar pattern. The month-level conclusions rest on the later model that includes trend and promo, not on the pooled means.
- **Only two years of data.** The trend is estimated from 2023 and 2024. Its linearity across the period was not tested.
- **Weekday means are unadjusted.** The day-of-week means in the date analysis do not control for promo, temperature or trend. The adjusted weekend result is the one in the weekend model.
- **Predictive models are weak and use a limited feature set.** Temperature and promo alone give a test R² of 0.069. The models did not include the date terms that explain much more variation in the month and trend model (R² 0.69). These are different feature sets, so the two results are not directly comparable. The models were evaluated on a single split without cross-validation, and no tuned or regularised alternatives were tested.
- **Random forest overfits.** Its test error is worse than the baseline.
- **Feature-importance methods disagree.** For the forest, impurity importance ranks temperature first and permutation importance ranks promo first. The permutation result is the one reported. The disagreement is not resolved by a test.
- **Per-promo temperature correlation not tested.** The r of 0.103 for promo = 1 days is reported without a significance test, and the analysis flags that it may be noise given 104 rows.
- **Level shift between years unexplained.** The 2023 to 2024 increase is established, but the analysis does not establish whether it is a real change or reflects a missing driver.
- **No review issues were recorded and no tasks failed.**

## Open questions

- Does the promo effect hold after controlling for day of week or season in a single model with both terms? (The weekend model includes promo, but a full model with day-of-week and season terms was not fitted.)
- Does the promo effect change with temperature? The interaction CI is too wide to decide this with the current data. Would a larger sample or more promo days per temperature band narrow it enough?
- Is the weak positive temperature slope within promo = 1 days (r ≈ 0.10) real or noise given 104 promo rows?
- Does the weekend effect differ between 2023 and 2024 (a weekend-by-year interaction)?
- Is the temperature relationship non-linear, such that a banded or spline term would change the temperature control?
- Is the trend linear across the two years, or does a non-linear time term change the conclusion about month effects?
- Is the 2023 to 2024 level shift a real change or a sign of a missing driver such as marketing spend?
- Would a regularised or gradient-boosted model, tuned and evaluated by cross-validation, beat the linear model? Would adding date terms to the predictive models change the feature ranking?
- Is the promo effect causal, or confounded with season or store?