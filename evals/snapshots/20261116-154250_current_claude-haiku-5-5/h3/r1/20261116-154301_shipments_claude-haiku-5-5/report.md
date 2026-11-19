# Delivery Hours in 1,000 Shipments: Distribution, Group Differences, Drivers and Prediction

## Summary

- **Distance is the clearest driver of delivery time.** Across all 1,000 rows, delivery_hours correlates with distance_km at Spearman rho 0.436. Among the 850 non-zero-weight rows the correlation is stronger, at rho 0.592. Depot and weekday show no statistically significant difference in delivery_hours (Kruskal-Wallis p = 0.214 and p = 0.402, both with negligible effect sizes).
- **The 150 rows with parcel_weight_kg = 0 are the main data concern.** They average 65.31 hours, against 35.13 hours for the other 850 rows. The gap of about 30 hours holds within every distance quartile and every depot, and after adjusting for distance, depot and weekday (30.19 hours). The findings describe the zero code as consistent with a recording artefact, but this is an inference the delivery data do not prove.
- **The parcel_weight_kg relationship reverses sign once the zero rows are removed.** Across all rows the association is weak and negative (Spearman rho -0.078). Among the 850 non-zero rows it is positive (rho 0.487).
- **Prediction depends on the zero rows.** On all 1,000 rows, gradient boosting cuts test RMSE from 12.62 to 4.70 hours against a mean baseline (test R² 0.861). On the 850 non-zero rows, linear regression reaches test R² 0.704 (RMSE 3.72 versus a baseline of 6.88). The gradient boosting model on those rows overfits, so its test scores are less reliable.
- **No significant interactions were found.** Distance does not significantly change the depot or weekday effect, and parcel weight does not significantly interact with distance. These tests used the full data including the zero rows and remain provisional.

## Data

- **Size:** 1,000 shipments, 6 columns.
- **Target:** delivery_hours (continuous regression target).
- **Features:** numeric parcel_weight_kg, distance_km and items; categorical depot (alpha, beta, delta, gamma) and weekday (seven levels). There are no date/time features, and no ids or free-text columns.
- **Missing values:** none. All 6 columns have 0 missing cells (0.0%), so no missingness analysis was needed beyond confirming this.
- **Value ranges:** parcel_weight_kg 0 to 35.12 kg (median 3.735); distance_km 5.6 to 300 (median 152.1); items 1 to 10 (median 6); delivery_hours 15.7 to 90.6 (median 36.65).
- **Zero weights:** 150 of 1,000 rows (15.0%) have parcel_weight_kg = 0, the most common weight value. They are retained and flagged in the cleaned data.

## Findings

### Distribution of delivery_hours

delivery_hours is right-skewed (skew 1.195). The mean is 39.66 hours, the median 36.65, and the standard deviation 13.10. The quartiles are 30.9 and 43.8 hours.

![Distribution of delivery_hours across 1000 shipments](tasks/eda_1/charts/delivery_hours_hist.png)

### Group differences by depot and weekday

**Depot.** Mean delivery_hours is similar across depots:

| Depot | n | Mean (hours) | Median (hours) | 95% CI for mean |
|---|---|---|---|---|
| alpha | 249 | 38.28 | 35.6 | [36.8, 39.8] |
| beta | 250 | 40.71 | 37.45 | [39.0, 42.4] |
| delta | 263 | 39.46 | 36.3 | [37.9, 41.0] |
| gamma | 238 | 40.21 | 37.5 | [38.5, 41.9] |

The Kruskal-Wallis test finds no significant depot effect (H = 4.48, df = 3, p = 0.214; epsilon-squared 0.0015, negligible). No pairwise depot comparison remains significant after Holm correction. The smallest raw p-value is 0.064 (alpha versus beta), with adjusted p = 0.386. These were pairwise Mann-Whitney tests, not Dunn's test.

**Weekday.** Saturday has the highest mean (41.47 hours, median 38.1, n = 148). Friday has the lowest mean (38.30 hours, median 35.2, n = 125). The other weekdays are:

| Weekday | n | Mean (hours) | Median (hours) |
|---|---|---|---|
| Mon | 152 | 38.60 | 35.85 |
| Tue | 140 | 39.76 | 36.7 |
| Wed | 152 | 40.29 | 37.0 |
| Thu | 141 | 39.81 | 36.8 |
| Sun | 142 | 39.17 | 36.65 |

The Kruskal-Wallis test finds no significant weekday effect (H = 6.19, df = 6, p = 0.402; epsilon-squared 0.0002, negligible). Every weekday's 95% confidence interval overlaps the others, including Friday and Saturday.

![Mean delivery_hours with 95% confidence intervals by depot and by weekday (all 1000 shipments)](tasks/stat_1/charts/delivery_mean_ci.png)

![Mean and median delivery_hours by depot](tasks/eda_1/charts/delivery_by_depot.png)

![Mean and median delivery_hours by weekday](tasks/eda_1/charts/delivery_by_weekday.png)

### Association with distance, weight and items

**All 1,000 rows:**

- **distance_km:** Pearson r = 0.314 and Spearman rho = 0.436 (95% CI 0.384 to 0.485; rho² = 0.19; p = 1.2e-47). This is the strongest association over the full data.
- **parcel_weight_kg:** Pearson r = -0.172 (p < 1e-7) and Spearman rho = -0.078 (95% CI -0.140 to -0.016; rho² = 0.006; p = 0.013). The association is weak and negative.
- **items:** Pearson r = -0.042 (p = 0.19) and Spearman rho = -0.010 (95% CI -0.072 to 0.052; p = 0.753). No relationship.

**Zero-weight versus other rows:** The 150 zero-weight rows have a mean delivery time of 65.31 hours (median 64.6), against 35.13 hours (median 34.9) for the other 850 rows (Mann-Whitney p = 7e-84).

**The 850 non-zero-weight rows:**

- **distance_km:** Pearson r = 0.562 (p = 6.1e-72) and Spearman rho = 0.592 (p = 1.1e-81). Both are stronger than the full-data values.
- **parcel_weight_kg:** Pearson r = 0.612 (p = 1.3e-88) and Spearman rho = 0.487 (p = 7.1e-52). The sign reverses from the full-data result. The findings read this as consistent with the zero rows driving the negative full-data association, but this is a reading of the split, not an established cause.
- **items:** Pearson r = 0.006 (p = 0.87) and Spearman rho = 0.025 (p = 0.47). Still no relationship.

**Disagreement on predictor ranking.** The statistics task reports that parcel_weight_kg is the stronger predictor among the non-zero rows (rho 0.487). The EDA task reports a higher rank correlation for distance_km on the same 850 rows (rho 0.592 versus 0.487). Both are reported here; the disagreement is not resolved.

### Whether the zero-weight gap reflects mix or recording

- **Mix:** The zero-weight rows have a similar distance profile to the other rows (mean distance 153.10 km versus 154.42 km; median 147.9 km versus 152.3 km). Their depot and weekday shares are close to those of the other rows.
- **Within distance quartiles:** Zero-weight rows take longer in every quartile: q1 60.09 versus 29.34 hours (gap 30.75); q2 63.95 versus 33.57 (gap 30.37); q3 66.34 versus 37.35 (gap 28.99); q4 71.48 versus 40.12 (gap 31.36).

![Mean delivery_hours for zero-weight vs non-zero-weight parcels within distance_km quartiles](tasks/eda_4/charts/eda4_gap_by_distance.png)

- **Within depots:** The gap is 28.76 hours (alpha), 31.37 (beta), 29.77 (delta) and 30.68 (gamma).
- **Adjusted:** In an OLS model controlling for distance_km, depot and weekday, the zero-weight coefficient is 30.19 hours (SE 0.55, p about 4e-305).
- **Interpretation:** The uniform gap of about 30 hours, in a setting where a physical parcel cannot weigh zero, is consistent with a recording artefact such as a missing-value code. The findings state this is an inference, not proven by the delivery data.

### Interactions

Each interaction was tested by dropping its group from one OLS model that also included weekday, depot, parcel_weight_kg and items:

- **distance_km × depot:** F = 1.72 (df = 3), p = 0.161. No significant interaction.
- **distance_km × weekday:** F = 1.71 (df = 6), p = 0.116. No significant interaction.
- **parcel_weight_kg × distance_km:** coefficient 0.0003 hours per km per kg (95% CI -0.0025 to 0.0032; t = 0.23, p = 0.818). No significant interaction.

Per-depot distance slopes, adjusted for weekday, parcel_weight_kg and items (hours per km):

| Depot | Slope | 95% CI | p | n |
|---|---|---|---|---|
| alpha | 0.055 | [0.038, 0.071] | 2.1e-10 | 249 |
| beta | 0.040 | [0.021, 0.059] | 5.1e-5 | 250 |
| delta | 0.031 | [0.013, 0.049] | 1.0e-3 | 263 |
| gamma | 0.057 | [0.039, 0.074] | 9.3e-10 | 238 |

Every depot has a positive distance slope. Delta's slope (0.031) is the lowest of the four, compared with 0.055 for alpha and 0.057 for gamma. The confidence intervals overlap widely, and no direct contrast of the slopes was run, so the pattern is not established.

### Predicting delivery_hours

**All 1,000 rows (800 train, 200 test):**

| Model | Test RMSE (hours) | Test MAE (hours) | Test R² | Train R² |
|---|---|---|---|---|
| Mean baseline | 12.62 | 9.46 | about 0 | 0.0 |
| Linear regression | 11.74 (7.0% lower than baseline) | 9.11 | 0.135 | 0.134 |
| Gradient boosting | 4.70 (62.8% lower than baseline) | 3.76 | 0.861 | 0.927 |

Gradient boosting overfits somewhat on these rows but generalises to the held-out shipments. The low linear R² is largely driven by the zero-weight rows.

**Permutation importance, gradient boosting, all rows** (RMSE increase in hours, mean over 30 shuffles): parcel_weight_kg 11.92 (sd 0.58); distance_km 3.24 (sd 0.23); depot 0.006 (sd 0.05); weekday -0.063 (sd 0.06); items 0.05 (sd 0.05). Only parcel_weight_kg and distance_km show meaningful importance. These values include the zero rows.

**Permutation importance, linear regression, all rows:** distance_km 1.38 (sd 0.29); parcel_weight_kg 0.48 (sd 0.17); depot 0.05; weekday -0.10; items 0.008. The linear model's large individual weekday coefficients (for example Sunday at 1.66) are not interpreted as importance, because the one-hot dummies are collinear with the intercept and the weekday effects are small relative to noise.

**Non-zero-weight rows (850; 680 train, 170 test):**

| Model | Test RMSE (hours) | Test MAE (hours) | Test R² | Train R² |
|---|---|---|---|---|
| Mean baseline | 6.88 | not reported | about 0 | n/a |
| Linear regression | 3.72 (about 46% lower than baseline) | 2.99 | 0.704 | 0.711 |
| Gradient boosting | 3.93 (about 43% lower than baseline) | 2.99 | 0.669 | 0.817 |

On these rows, linear regression is the better-supported model. Permutation importance for the linear model: parcel_weight_kg 4.20 (sd 0.21), distance_km 3.07 (sd 0.27), with depot, weekday and items near zero. Gradient boosting: distance_km 3.08 (sd 0.28), parcel_weight_kg 3.29 (sd 0.20), with the others near zero. The zero rows inflate the gradient boosting importance of parcel_weight_kg from 3.29 to 11.92 hours.

![Test RMSE of the mean baseline, linear regression and gradient boosting for delivery_hours](tasks/ml_1/charts/ml_1_model_rmse.png)

## Limitations

- **Zero-weight code.** 150 rows (15.0%) have parcel_weight_kg = 0. The findings do not establish whether this is a true weight or a recording artefact. Every result that includes parcel_weight_kg, including the full-data correlations, the interaction tests and the permutation importances on all rows, is affected by these rows. The sign of the parcel_weight_kg correlation changes depending on whether they are included.
- **Interaction tests are provisional.** The interaction models include the 150 zero-weight rows, which may distort the parcel_weight_kg terms. The depot and weekday interaction results have not yet been refitted on the 850 non-zero rows.
- **Gradient boosting on non-zero rows overfits (unresolved review issue).** Train R² is 0.817 against test R² 0.669, a gap of 0.15. Its non-zero test performance is therefore less reliable than the linear model's (test R² 0.704) when the two are compared. The mean baseline's test R² on the non-zero rows is about 0, and the linear model's test MAE is 2.99 hours.
- **Delta versus gamma slope (unresolved review issue).** Delta's distance slope (0.031 hours per km) is lower than gamma's (0.057). The difference is not significant and no direct contrast was run, so delta's lower slope should not be treated as established.
- **Depot and weekday analyses use pairwise tests.** The depot pairwise comparisons are Mann-Whitney tests with Holm correction, not Dunn's test. Confidence intervals for group means are t-based.
- **Linearity not tested.** Whether the distance relationship is linear within depots, or better fitted by a spline or log term, was not examined.
- **Predictor ranking disagreement.** The statistics and EDA tasks differ on whether parcel_weight_kg or distance_km ranks higher among the non-zero rows (see Findings). Both are reported; the disagreement is not resolved.
- **Task status.** Four tasks (eda_1 through eda_4) and ml_1 are complete. The interaction task (stat_2) is partial, and its conclusion is provisional as noted above.

## Open questions

- Is the parcel_weight_kg value of 0 a missing-value code, and can the source system be checked for how weight is recorded?
- Does the distance_km effect hold after controlling for depot and weekday in a regression on the 850 non-zero rows, with confidence intervals?
- Is the positive parcel_weight_kg correlation among non-zero rows confounded by distance_km or depot?
- Is the Saturday delivery-time gap statistically meaningful once depot and distance are accounted for?
- Is delta's lower distance slope significantly different from alpha's and gamma's, based on a direct contrast?
- Is the distance-delivery relationship linear within depots, or does a spline or log term fit better?
- Does tuning gradient boosting regularisation or using cross-validation reduce the train/test gap (R² 0.927 versus 0.861 on all rows, and 0.817 versus 0.669 on non-zero rows)?