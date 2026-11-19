# Delivery Hours Analysis of 1,000 Deliveries: Target delivery_hours

## Summary

- **The target is right-skewed.** delivery_hours has a mean of 39.66 and a median of 36.65 hours (skew 1.20, SD 13.10). The IQR rule flags 89 of 1,000 rows (8.9%) above the upper fence of 63.15 hours, all on the high side.
- **Depot and weekday differences are not statistically significant.** Depot ANOVA gives p = 0.183 and weekday ANOVA gives p = 0.455. Effect sizes are negligible (eta squared 0.0049 for depot, 0.0057 for weekday), and no depot pair is significant after correction.
- **Distance has the clearest linear association with delivery time; parcel weight is weakly negative.** distance_km has Pearson r = 0.314, parcel_weight_kg r = -0.172, and items r = -0.042 (not significant). In a linear multiple regression that explains 13.2% of variance, the parcel weight coefficient stays significant (-0.680 hours per kg, p = 1.6e-08), within that linear specification.
- **A gradient boosting model predicts far better than linear regression.** On a single 200-row test set, boosting reaches RMSE 4.70 hours and R² 0.861, against 12.62 hours for the mean baseline and 11.74 hours (R² 0.135) for linear regression. The two models rank features differently: boosting ranks parcel_weight_kg first, while linear regression ranks distance_km first. The findings do not resolve this.

## Data

- **Size:** 1,000 rows and 6 columns.
- **Target:** delivery_hours (numeric, regression).
- **Numeric features:** parcel_weight_kg, distance_km, items.
- **Categorical features:** depot (alpha, beta, delta, gamma; 238 to 263 rows each) and weekday (seven levels; 125 to 152 rows each).
- **Date/time features, identifiers and free text:** none.
- **Missing values:** none.

## Findings

### Distribution of the target

delivery_hours has a mean of 39.66, median 36.65, SD 13.10, minimum 15.7, Q1 30.9, Q3 43.8 and maximum 90.6 hours. It is right-skewed (skew 1.20), with the mean about 3 hours above the median. The IQR fences are 11.55 and 63.15 hours. The rule flags 89 rows (8.9%) as outliers, all above the upper fence.

![Histogram of delivery_hours across all 1,000 rows](tasks/eda_1/charts/delivery_hours_hist.png)

### Group means and medians by depot and weekday

**Depot** (count, mean and median in hours):

| Depot | n | Mean | Median |
|---|---|---|---|
| alpha | 249 | 38.28 | 35.6 |
| beta | 250 | 40.71 | 37.45 |
| delta | 263 | 39.46 | 36.3 |
| gamma | 238 | 40.21 | 37.5 |

- By **mean**, the ranking is alpha (38.28) < delta (39.46) < gamma (40.21) < beta (40.71).
- By **median**, the ranking is alpha (35.6) < delta (36.3) < beta (37.45) < gamma (37.5).
- Beta and gamma swap places between the two measures, so the mean and median orders do not agree.

**Weekday** (count, mean and median in hours):

| Weekday | n | Mean | Median |
|---|---|---|---|
| Fri | 125 | 38.30 | 35.2 |
| Mon | 152 | 38.60 | 35.85 |
| Sat | 148 | 41.47 | 38.1 |
| Sun | 142 | 39.17 | 36.65 |
| Thu | 141 | 39.81 | 36.8 |
| Tue | 140 | 39.76 | 36.7 |
| Wed | 152 | 40.28 | 37.0 |

Saturday is highest and Friday is lowest on both mean and median. The group differences are small relative to the spread within groups.

![Mean delivery_hours per depot with 95% t-based confidence intervals](tasks/stat_1/charts/stat1_depot_mean_ci.png)

### Significance and effect sizes of depot and weekday

- **Depot:** one-way ANOVA F = 1.62, p = 0.183; Kruskal-Wallis H = 4.48, p = 0.214; eta squared 0.0049, epsilon squared 0.0019 (about 0.2% of variance).
- **Weekday:** one-way ANOVA F = 0.955, p = 0.455; Kruskal-Wallis H = 6.19, p = 0.402; eta squared 0.0057, epsilon squared -0.0003 (effectively zero).
- **Depot pairwise comparisons** (mean difference as first minus second depot; Tukey HSD 95% CI; Tukey p; Holm-corrected Welch p). No pair is significant under either correction.

| Pair | Mean diff. (h) | Tukey 95% CI | Tukey p | Holm Welch p |
|---|---|---|---|---|
| alpha - beta | -2.43 | -5.45 to 0.58 | 0.162 | 0.233 |
| alpha - delta | -1.18 | -4.16 to 1.80 | 0.738 | 1.000 |
| alpha - gamma | -1.93 | -4.98 to 1.13 | 0.365 | 0.469 |
| beta - delta | +1.25 | -1.72 to 4.23 | 0.700 | 1.000 |
| beta - gamma | +0.50 | -2.55 to 3.55 | 0.974 | 1.000 |
| delta - gamma | -0.75 | -3.76 to 2.26 | 0.919 | 1.000 |

- Depot 95% t-based confidence intervals for group means overlap heavily: alpha 36.75 to 39.81, beta 38.98 to 42.45, delta 37.87 to 41.05, and gamma 38.54 to 41.88 hours.
- Saturday's mean is 41.47 hours (95% CI 39.28 to 43.66). Its interval overlaps every other weekday's interval. No weekday pairwise tests were recorded.

### Correlations and simple slopes with distance_km, parcel_weight_kg and items

- **distance_km:** Pearson r = 0.314 (95% CI 0.257 to 0.369, p = 2.2e-24); Spearman rho = 0.436 (p = 1.2e-47); OLS slope 0.0473 hours per km (p = 2.2e-24). This is a moderate positive association.
- **parcel_weight_kg:** Pearson r = -0.172 (95% CI -0.231 to -0.111, p = 4.7e-08); Spearman rho = -0.078 (p = 0.013); OLS slope -0.691 hours per kg (p = 4.7e-08). This is a weak negative association.
- **items:** Pearson r = -0.042 (95% CI -0.103 to 0.020, p = 0.187); Spearman rho = -0.010 (p = 0.753); OLS slope -0.188 hours per item (p = 0.187). No meaningful association.

### Distance by depot

- The distance_km x depot interaction is not significant: F = 1.61 on 3 df, p = 0.185.
- Per-depot simple slopes of delivery_hours on distance_km are all positive:

| Depot | Slope (h/km) | p | n |
|---|---|---|---|
| alpha | 0.0553 | 1.4e-10 | 249 |
| beta | 0.0405 | 4.5e-05 | 250 |
| delta | 0.0344 | 0.00025 | 263 |
| gamma | 0.0582 | 2.2e-10 | 238 |

- Split at the median distance of 152.05 km, the depot means are:

| Depot | Low distance: mean (n) | High distance: mean (n) |
|---|---|---|
| alpha | 34.06 (137) | 43.44 (112) |
| beta | 38.23 (127) | 43.27 (123) |
| delta | 37.40 (123) | 41.27 (140) |
| gamma | 35.05 (113) | 44.87 (125) |

### Multiple regression: does the weight association survive adjustment?

Multiple OLS of delivery_hours on distance_km, parcel_weight_kg, items and depot dummies (n = 1,000):

- **parcel_weight_kg:** -0.680 hours per kg (95% CI -0.914 to -0.446, p = 1.6e-08). The unadjusted slope is -0.691 (p = 4.7e-08). Within this linear specification, the weight association is largely unchanged after adjustment.
- **distance_km:** 0.0464 hours per km (95% CI 0.0377 to 0.0552, p = 3.4e-24).
- **items:** -0.119 hours per item (95% CI -0.380 to 0.143, p = 0.373); not significant after adjustment.
- **Depot contrasts versus alpha:** beta +2.22 hours (95% CI 0.065 to 4.373, p = 0.043); gamma +1.86 (95% CI -0.322 to 4.050, p = 0.095); delta +0.84 (95% CI -1.291 to 2.965, p = 0.440).
- **Model fit:** R² 0.132, adjusted R² 0.126, F-test p = 7.8e-28.

The beta versus alpha difference (p = 0.043) appears only in this adjusted model. The unadjusted depot tests in stat_1 were not significant, so this result should be treated as fragile.

### Predictive models compared with a mean baseline

On a single 80/20 split (800 training rows, 200 test rows, seed 42):

| Model | Test RMSE (h) | Test MAE (h) | Test R² |
|---|---|---|---|
| Mean-value baseline | 12.62 | 9.46 | 0.00 |
| Linear regression | 11.74 | 9.11 | 0.135 |
| Gradient boosting | 4.70 | 3.76 | 0.861 |

Gradient boosting training R² is 0.927. The recorded finding states that boosting cuts test RMSE by about 63% relative to the baseline, and linear regression by about 7%. The recorded finding concludes that the relationship between the features and delivery_hours is strongly nonlinear or interactive.

![Test RMSE in hours of delivery_hours for the mean-value baseline, linear regression and gradient boosting regressor on the 200-row test set](tasks/ml_1/charts/ml1_model_test_rmse.png)

**Feature importance:**

- **Gradient boosting, permutation importance** (increase in test RMSE when shuffled): parcel_weight_kg 11.78 hours, distance_km 3.22, items 0.046. All depot and weekday indicators are below 0.02 hours. The largest is depot_alpha at 0.014; weekday_Sat is -0.064.
- **Linear regression, permutation importance:** distance_km 1.40, parcel_weight_kg 0.44, weekday_Sat 0.038, depot_alpha 0.031. This ranking differs from boosting mainly in the weight of parcel_weight_kg relative to distance_km.
- **Linear regression, coefficient magnitude:** the largest absolute coefficients are on weekday and depot indicators (weekday_Sun 1.66, weekday_Wed 1.43).

Boosting ranks parcel_weight_kg first, even though its simple correlation with delivery_hours is weak and negative (r = -0.172). The linear model's permutation ranking puts distance_km first. The findings do not resolve these differing rankings.

### Tail above the IQR upper fence (63.15 hours)

- **Share:** 89 of 1,000 rows (8.9%).
- **distance_km:** tail median 217.6 (IQR 131.3 to 269.2) versus 145.9 (IQR 76.15 to 225.6) for the rest.
- **parcel_weight_kg:** tail median 0.0 (IQR 0.0 to 0.0) versus 4.0 (IQR 2.65 to 5.775) for the rest. Most tail parcels weigh zero.
- **items:** tail median 5 (IQR 3 to 7) versus 6 (IQR 3 to 8), a small difference.
- **Depot counts and rates:** beta 28 (11.2%), gamma 24 (10.1%), delta 22 (8.4%), alpha 15 (6.0%). These are descriptive only. No test was run, the beta and gamma counts are small, and stat_1 found no significant depot effect.
- **Weekday counts and rates:** Wed 17 (11.2%), Sun 14, Thu 14, Sat 13, Mon 12, Tue 11, Fri 8 (6.4%). These are descriptive only. No test was run, and the Wed concentration rests on 17 rows.

![Boxplots of distance_km, parcel_weight_kg and items for delivery_hours tail (>63.15 h) vs rest](tasks/eda_2/charts/tail_vs_rest_boxplots.png)

## Limitations

- **Linear fit is weak; the models disagree.** The multiple regression explains 13.2% of variance (R² 0.132), while gradient boosting reaches R² 0.861 on the test set. The linear coefficients are a limited summary of the relationship. The two models also rank features differently (see Predictive models). This report does not resolve either disagreement.
- **Regression assumptions are unchecked.** Residual diagnostics (normality, heteroscedasticity, influence) were not run, so the p-values and CIs in the multiple regression rest on unverified OLS assumptions.
- **Zero-weight tail.** Most tail rows have zero parcel weight. The weight slope may be driven by this zero-heavy subset rather than by weight across the range. This was not tested.
- **Fragile depot result.** The beta versus alpha difference in the adjusted model (p = 0.043) does not appear in the unadjusted depot tests, where no pair is significant.
- **Weekday post-hoc tests not recorded.** The weekday omnibus tests are not significant, and no weekday pairwise results are in the findings.
- **Single split.** All model scores come from one 200-row test split (seed 42). Cross-validation was not run.
- **Skew not addressed.** No log transform of delivery_hours was tested.
- **Sign convention in stored pairwise values.** The stored pairwise mean differences and CIs have the opposite sign to the first-minus-second convention used in the table above. The table uses the stated convention, which matches the group means.
- **stat_2 is marked partial, and its text conflicts with its recorded values.**
  - The stat_2 text says the delta and gamma per-depot slope p-values, their n, and their low/high distance group means are unavailable. The recorded values for these are present and are reported above. The lead's objection that the depot-by-distance table is incomplete as a finding still stands until the stat_2 text matches the recorded values.
  - The stat_2 text says the Spearman p-value for distance_km was not reported. A recorded value (1.2e-47) exists and is reported above. The lead's objection that the finding omitted it still stands.
  - The stat_2 text says the depot ranking was unavailable. The accepted eda_1 depot table contains it, and the ranking above follows that table. The lead's objection stands until the stat_2 finding cites the stat_1 ranking correction.
- **Missingness.** Not applicable; the dataset has no missing values.

## Open questions

- Is the Saturday mean (41.47 hours) higher than the other weekdays after adjusting for distance_km, parcel_weight_kg and items, or is it explained by the mix of other variables? No weekday pairwise test was recorded.
- Are the Saturday and Friday weekday differences, and the beta and gamma versus alpha depot differences, statistically significant under post-hoc tests? Depot pairwise tests were run; weekday pairwise tests were not.
- What drives the tail above 63.15 hours? The tail descriptives have not been tested against distance_km, parcel_weight_kg or items.
- Why does parcel_weight_kg dominate the boosting model when its simple correlation with delivery_hours is weak and negative? Is there an interaction with distance_km or a nonlinear shape?
- Does a log transform of delivery_hours change the correlation, interaction and linear model results, given the skew of 1.20?
- Do the linear model's weak fit and the boosting model's strong fit hold under cross-validation rather than a single 200-row test split?
- Does the weight association persist when the zero-weight rows are examined separately from the rest of the range?