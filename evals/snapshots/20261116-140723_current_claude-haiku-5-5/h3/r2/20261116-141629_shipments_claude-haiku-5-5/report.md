# Delivery Hours Analysis: 1,000 Parcels, Target delivery_hours

## Summary

- **Target distribution:** delivery_hours is right-skewed, with mean 39.66 h above median 36.65 h (range 15.7 to 90.6 h).
- **Depot and weekday:** Neither has a statistically significant effect on delivery_hours (depot Kruskal-Wallis p = 0.214; weekday Kruskal-Wallis p = 0.402). Each explains under 0.6% of variance.
- **Distance:** distance_km is the numeric feature most related to delivery_hours (Spearman 0.44, Pearson 0.31). Its depot interactions are not statistically supported (joint p = 0.395).
- **Models:** On a single 200-row test split, gradient boosting reached MAE 3.758 h and R² 0.861. Linear regression reached MAE 9.105 h and R² 0.135, against a mean baseline MAE of 9.460 h.
- **Saturday:** After adjustment, the Saturday excess over Monday is 2.32 h (95% CI −0.46 to 5.10, p = 0.102). It is directionally positive but not statistically significant.

## Data

- **Size:** 1,000 rows and 6 columns.
- **Target:** delivery_hours (continuous, regression).
- **Features:** Numeric: parcel_weight_kg, distance_km, items. Categorical: depot (4 levels), weekday (7 levels). No date/time features and no ids or free text.
- **Missing values:** None. All 6 columns have 0 missing values across 1,000 rows.

## Findings

### Distribution and group means

delivery_hours has mean 39.66, median 36.65, standard deviation 13.10, Q1 30.9 and Q3 43.8. The mean exceeds the median, consistent with right skew.

![Histogram of delivery_hours across 1,000 parcels](tasks/eda_1/charts/delivery_hours_hist.png)

**By depot** (mean / median / count):
- alpha: 38.28 / 35.6 / 249
- beta: 40.71 / 37.45 / 250
- delta: 39.46 / 36.3 / 263
- gamma: 40.21 / 37.5 / 238

**By weekday:** Saturday has the highest mean (41.47) and median (38.10). Friday has the lowest mean (38.30) and median (35.20). Counts range from 125 (Friday) to 152 (Monday and Wednesday).

**Correlations with delivery_hours** (Pearson / Spearman):
- distance_km: 0.31 / 0.44. The rank relation is stronger than the linear one.
- parcel_weight_kg: −0.17 / −0.08
- items: −0.04 / −0.01

![Scatter of delivery_hours against distance_km](tasks/eda_1/charts/delivery_vs_distance.png)

### Significance of depot and weekday differences

These tests are unadjusted: each factor is tested on its own.

**Depot:**
- Kruskal-Wallis H = 4.48, p = 0.214
- One-way ANOVA F = 1.62, p = 0.183
- Eta-squared 0.0049 and epsilon-squared (KW) 0.0015, i.e. under 0.5% of variance.
- Holm-adjusted pairwise Mann-Whitney tests (6 pairs): the smallest adjusted p is 0.386 (alpha vs beta). No pair differs significantly.

**Weekday:**
- Kruskal-Wallis H = 6.19, p = 0.402
- One-way ANOVA F = 0.96, p = 0.455
- Eta-squared 0.0057 and epsilon-squared (KW) 0.0002, i.e. under 0.6% of variance.
- Holm-adjusted pairwise tests (21 pairs): the smallest adjusted p is 0.581 (Friday vs Saturday). No pair differs significantly.

The 95% CIs of the group means overlap. For example, alpha is 38.28 [36.75, 39.81] and beta is 40.71 [38.98, 42.45]. Saturday is 41.47 [39.28, 43.66]. The overlaps agree with the non-significant tests.

![Mean delivery_hours with 95% confidence intervals by depot (left) and by weekday (right)](tasks/stat_1/charts/delivery_hours_group_means_ci.png)

**Numeric features (Spearman, Fisher-z 95% CI):**
- distance_km: ρ = 0.436 [0.384, 0.485], p = 1.2e-47, n = 1,000.
- parcel_weight_kg: ρ = −0.078 [−0.140, −0.016], p = 0.013. Statistically significant but very small.
- items: ρ = −0.010 [−0.072, 0.052], p = 0.753. No meaningful correlation.

### Interactions

**Depot interactions** were tested by adding each term to a main-effects model:
- Depot × distance_km: F = 1.64 (df 3), p = 0.178
- Depot × parcel_weight_kg: F = 1.24 (df 3), p = 0.295
- Depot × weekday: F = 0.95 (df 18), p = 0.512

The joint test of all depot interaction terms gives F = 1.05 (df 24), p = 0.395. R² rises from 0.136 to 0.158. No interaction is statistically supported at this sample size. This does not show that the effects are equal.

**Adjusted distance_km slope per depot** (hours per km, adjusted for weight, weekday and items, 95% CI):
- alpha: 0.055 [0.038, 0.071], n = 249
- beta: 0.040 [0.021, 0.059], n = 250
- gamma: 0.057 [0.039, 0.074], n = 238
- delta: 0.031 [0.013, 0.049], n = 263

All slopes are positive and their CIs overlap widely.

![Adjusted slope of delivery_hours on distance_km within each depot (hours per km) with 95% confidence intervals](tasks/stat_2/charts/distance_slope_by_depot.png)

### Saturday effect after adjustment

In an adjusted OLS model (distance_km, parcel_weight_kg, items and depot), the Saturday coefficient versus Monday is 2.32 h (95% CI −0.46 to 5.10, p = 0.102).

- Unadjusted, Saturday is 2.87 h above Monday (p = 0.058). The adjusted estimate is 2.32 h.
- The data are consistent with no effect and with a positive effect of up to about 5 hours. The study neither confirms nor rules out an excess.
- The 41.47 vs about 39 comparison uses raw means, not the adjusted model.
- The joint test of all weekday dummies after adjustment gives F = 0.82 (df 6), p = 0.553.
- In the adjusted model, each extra km adds 0.046 h (p = 8.5e-24).
- R² is 0.136 for the full adjusted model and 0.006 for weekday alone.

### Nonlinearity of distance_km

- A natural spline (4 df) adjusted for depot, parcel_weight_kg, weekday and items does not significantly improve on a linear distance_km term: F = 0.53 (df 2), p = 0.59.
- Adding depot-by-spline terms to the common spline model gives F = 1.03 (df 9), p = 0.42. No significant evidence that the curve shape differs by depot.
- Adding a quadratic term within each depot gives p = 0.82 (alpha), 0.54 (beta), 0.34 (gamma) and 0.78 (delta).

![Fitted spline curves of delivery_hours on distance_km per depot, adjusted at mean weight and items, Monday](tasks/stat_4/charts/stat4_spline_by_depot.png)

These results show no detectable curvature. They do not establish that the per-depot relations are straight lines. The Spearman (0.44) versus Pearson (0.31) gap for distance_km is not explained by this analysis.

### Missingness

Every column has zero missing values: 0 of 1,000 rows (0.0%) in all six columns. No missingness comparison with delivery_hours was needed.

### Predictive models

**Setup:** An 80/20 split with random_state 42 gives 800 training rows and 200 test rows. There are 14 features: parcel_weight_kg, distance_km, items, and one-hot columns for 4 depots and 7 weekdays.

**Test-set scores** (single 200-row split):

| Model | MAE (h) | RMSE (h) | R² |
|---|---|---|---|
| Gradient boosting | 3.758 | 4.699 | 0.861 |
| Linear regression | 9.105 | 11.735 | 0.135 |
| Mean baseline | 9.460 | 12.615 | 0.000 |

The linear model's training R² is 0.134. Gradient boosting leads the mean baseline by a wide margin on this split.

![Test-set MAE and RMSE in hours for the mean baseline, linear regression and gradient boosting](tasks/ml_2/charts/ml2_model_errors.png)

**Permutation importance, gradient boosting** (increase in test MAE when shuffled):
- parcel_weight_kg: 7.962 h
- distance_km: 2.666 h
- items: 0.018 h
- All depot and weekday dummies are between −0.034 and 0.003 h. Shuffling them does not raise test MAE.

**Permutation importance, linear regression:**
- distance_km: 1.256 h
- parcel_weight_kg: −0.088 h
- items: 0.001 h
- Depot and weekday dummies range from −0.066 to 0.035 h.

The linear model gets little from parcel weight, while gradient boosting relies on it most. This pattern suggests a nonlinear or interaction effect of parcel weight. That is a suggestion, not a proven cause.

## Limitations

- **Unadjusted group tests.** The depot and weekday tests in the stat_1 findings (Kruskal-Wallis, ANOVA and pairwise tests) are unadjusted. They do not account for distance_km or other features.
- **Adjusted main effects: conflicting statements.** The stat_3 findings report an adjusted joint weekday test (p = 0.553) with depot included as a covariate. The unresolved review issue states that adjusted main effects of depot and weekday were not tested, and that the only adjusted evidence is the stat_2 interaction results. These statements disagree. This report reports both and does not resolve the disagreement. No adjusted depot main-effect test is reported.
- **Linear regression dummy coefficients.** Because the one-hot dummies are included alongside an intercept, they are collinear and not uniquely identified. The largest weekday coefficients (weekday_Sun 1.66 h, weekday_Wed 1.43 h, weekday_Fri 1.38 h) must not be read as evidence of a weekday effect. This report does not interpret them.
- **Interaction non-significance** does not show that depot slopes or effects are equal. The depot-specific slopes are not statistically distinguishable at this sample size.
- **Saturday effect** is not statistically significant after adjustment. Its CI includes zero.
- **Spearman–Pearson gap** for distance_km (0.44 vs 0.31) is unresolved. The spline test did not detect a nonlinearity, and the cause of the gap is not identified.
- **Model evaluation** uses one 200-row test split. Gradient boosting's advantage has not been checked under cross-validation. Permutation importances are computed on that same test split.
- **Group sizes.** The eda_1 finding states depot group sizes of 249 to 263. Its own counts include 238 for gamma, so this report uses the listed counts.
- **Placeholder values.** Zero missing values does not rule out placeholder values (such as 0 or empty strings) in parcel_weight_kg, distance_km or delivery_hours. This has not been checked.
- **Failed tasks.** None reported.

## Open questions

- Does a nonlinear effect of parcel_weight_kg, distance_km, or their interaction explain the gap between linear regression and gradient boosting?
- Does gradient boosting's advantage hold under cross-validation rather than a single 200-row test split?
- Are the depot and weekday effects significant once distance_km and parcel_weight_kg are both controlled for? The depot main effect has not been tested in an adjusted model.
- Does the Saturday effect differ across depots or distance bands? The interaction test was not reported for this.
- What explains the Spearman (0.44) versus Pearson (0.31) gap for distance_km? Is it driven by outliers or by a monotone nonlinear pattern?
- Does the right skew in delivery_hours come from long-distance parcels or from outliers above 60 hours?
- Is the depot slope difference (delta about 0.031 h/km vs alpha about 0.055 h/km) real at a larger sample size?
- Do any zeros or empty values in parcel_weight_kg, distance_km or delivery_hours act as placeholders for missing data?