# Delivery Hours in 1,000 Shipments: Drivers of delivery_hours

## Summary

- **Distance and parcel weight carry the predictive signal.** Gradient boosting predicts delivery_hours on a 200-row test split with MAE 3.76 hours and R² 0.861, against 9.46 hours and R² 0.000 for the mean baseline. Permutation importance ranks parcel_weight_kg first and distance_km second.
- **The 150 zero-weight parcels form a much slower group.** Their mean is 65.31 hours against 35.13 for the other 850 rows. Among the non-zero rows, weight is positively related to delivery_hours (Pearson r = +0.612), while the overall correlation is negative (r = −0.172).
- **Delivery time rises with distance.** Correlation is +0.314 (Pearson) and Spearman ρ is 0.436. The OLS slope is +0.047 hours per km (95% CI 0.038 to 0.056). The distance effect does not differ significantly by depot (interaction p = 0.185).
- **Depot and weekday have no significant effect.** Kruskal-Wallis p = 0.214 for depot and p = 0.402 for weekday, with negligible effect sizes. No pairwise difference survives Holm correction.
- **Items has no detectable association** with delivery_hours (Spearman ρ = −0.010, p = 0.753), and it contributes nothing measurable to the gradient boosting model.

## Data

- 1,000 rows and 6 columns: three numeric features (parcel_weight_kg, distance_km, items), two categorical features (depot, weekday), and the target delivery_hours.
- No date/time features, ids, free text or missing values. No rows were dropped.
- delivery_hours ranges from 15.7 to 90.6, with median 36.65 and mean 39.66.
- parcel_weight_kg has 150 rows equal to zero (the most common value). This group is handled separately in the analysis below.

## Findings

### Distribution of delivery_hours

delivery_hours is right-skewed: the mean (39.66) exceeds the median (36.65), skew is 1.19, and the 5th to 95th percentile range is 24.5 to 68.9.

![Histogram of delivery_hours across all 1000 shipments](tasks/eda_1/charts/delivery_hours_hist.png)

### Depot and weekday

Mean and median delivery_hours by depot:

| Depot | n | Mean | Median |
|---|---|---|---|
| alpha | 249 | 38.28 | 35.6 |
| beta | 250 | 40.71 | 37.45 |
| delta | 263 | 39.46 | 36.3 |
| gamma | 238 | 40.21 | 37.5 |

Depot means are close together. Beta has the highest mean and alpha the lowest.

![Mean delivery_hours for each depot level](tasks/eda_1/charts/delivery_by_depot.png)

Mean and median delivery_hours by weekday:

| Weekday | n | Mean | Median |
|---|---|---|---|
| Fri | 125 | 38.30 | 35.2 |
| Mon | 152 | 38.60 | 35.85 |
| Tue | 140 | 39.76 | 36.7 |
| Wed | 152 | 40.28 | 37.0 |
| Thu | 141 | 39.81 | 36.8 |
| Sat | 148 | 41.47 | 38.1 |
| Sun | 142 | 39.17 | 36.65 |

Saturday has the highest mean and Friday the lowest.

![Mean delivery_hours for each weekday level](tasks/eda_1/charts/delivery_by_weekday.png)

**Significance tests (stat_1):**
- Depot: Kruskal-Wallis H = 4.479, p = 0.214, eta-squared = 0.0015 (negligible). The omnibus test is not significant.
- Weekday: Kruskal-Wallis H = 6.193, p = 0.402, eta-squared = 0.0002 (negligible). The omnibus test is not significant.
- Depot pairwise Mann-Whitney tests: the smallest raw p-value is alpha vs beta (p = 0.064 raw, 0.386 Holm). No pair survives Holm correction.
- Weekday pairwise Mann-Whitney tests: the smallest raw p-value is Fri vs Sat (p = 0.028 raw, 0.581 Holm). No pair survives Holm correction. Because the omnibus test is not significant, no weekday post-hoc result is treated as established.
- Unadjusted Welch 95% CI for the highest minus lowest depot group (beta minus alpha): 2.43 hours (0.13 to 4.74). The interval excludes zero, but it is not adjusted for choosing the extreme pair and the omnibus test is not significant, so it is exploratory only.
- Unadjusted Welch 95% CI for the highest minus lowest weekday group (Sat minus Fri): 3.17 hours (0.11 to 6.22). The same caveats apply.

![Mean delivery_hours per depot and weekday level with approximate 95% CI; no grouping is significant overall (Kruskal-Wallis p=0.214 depot, p=0.402 weekday)](tasks/stat_1/charts/stat1_group_means.png)

### Parcel weight and the zero-weight group

Quartile means of parcel_weight_kg (the lowest quartile is labelled Q1):

| Quartile | Mean | Median |
|---|---|---|
| Q1 | 51.57 | 58.0 |
| Q2 | 32.29 | 32.2 |
| Q3 | 34.3 | 34.45 |
| Q4 | 40.46 | 40.25 |

The high Q1 mean reflects the zero-weight rows. I have not tabulated how many zero-weight rows fall in each quartile bin.

![Mean delivery_hours per quartile bin of parcel_weight_kg](tasks/eda_1/charts/delivery_by_parcel_weight_kg_quartile.png)

Zero-weight rows (n = 150) versus the other 850 rows:
- Mean delivery_hours is 65.31 for zero-weight rows and 35.13 for the rest. The medians are 64.6 and 34.9.
- The zero-weight rows are about 30 hours slower on average, based on these means.
- In the adjusted model (stat_3), the zero-weight indicator adds about 37.8 hours, with the same covariates (distance_km, depot, weekday) included.

Profile of the zero-weight rows (eda_2):
- Distance: mean 153.1 km (median 147.9) for zero-weight rows, against 154.42 km (median 152.3) for the other rows.
- Items: mean 5.25 (median 5.0) for zero-weight rows, against 5.56 (median 6.0) for the other rows.
- Depot mix does not differ significantly between the groups (chi-square 0.87, p = 0.83). Weekday mix does not either (chi-square 1.80, p = 0.94).

![Mean distance_km and mean items for zero-weight rows (150) versus other rows (850)](tasks/eda_2/charts/eda_2_zero_weight_profile.png)

The sign of the weight relationship depends on whether the zero-weight rows are included:
- Among the 850 non-zero rows, the Pearson correlation of parcel_weight_kg with delivery_hours is +0.612. The Spearman ρ is +0.487 (95% CI 0.432 to 0.540). The OLS slope is +1.525 hours per kg (95% CI 1.393 to 1.658).
- Over all 1000 rows, the Pearson correlation is −0.172. The Spearman ρ is −0.078 (95% CI −0.154 to −0.002, p = 0.013). The OLS slope is −0.691 hours per kg (95% CI −0.937 to −0.445).
- These results disagree in sign. The all-row results reflect the zero-weight rows. The analysis shows that these rows change the relationship. It does not establish a mechanism.

Adjusted weight effect among non-zero rows (stat_3): after adjusting for distance_km, depot and weekday, the slope is +1.557 hours per kg (95% CI 1.466 to 1.648, p = 8e-157, n = 850, R² = 0.712). This is close to the unadjusted +1.525, so the positive sign holds after adjustment. On all 1000 rows with a zero-weight indicator and the same covariates, the weight slope is +1.553 hours per kg (95% CI 1.453 to 1.654, R² = 0.887). In the adjusted non-zero model, distance_km keeps a positive slope of 0.050 hours per km (p = 4e-141).

### Distance and items

Quartile means of distance_km:

| Quartile | Mean | Median |
|---|---|---|
| Q1 | 34.63 | 30.05 |
| Q2 | 37.70 | 34.05 |
| Q3 | 41.41 | 38.35 |
| Q4 | 44.89 | 41.10 |

![Mean delivery_hours per quartile bin of distance_km](tasks/eda_1/charts/delivery_by_distance_km_quartile.png)

Distance is the strongest association with delivery_hours among the features apart from the zero-weight effect:
- Pearson r = +0.314.
- Spearman ρ = 0.436 (95% CI 0.382 to 0.491, p < 1e-46).
- OLS slope = +0.047 hours per km (95% CI 0.038 to 0.056, p < 1e-23).

Distance effect by depot (stat_2): the interaction F-test gives F = 1.61, p = 0.185, so the distance effect does not differ significantly by depot. Per-depot slopes (hours per km, 95% CI):

| Depot | Slope | 95% CI |
|---|---|---|
| alpha | 0.055 | 0.039 to 0.072 |
| beta | 0.041 | 0.021 to 0.060 |
| delta | 0.034 | 0.016 to 0.053 |
| gamma | 0.058 | 0.041 to 0.075 |

All four slopes are positive and their intervals overlap.

Items shows no detectable relationship:
- Quartile means are 40.93, 38.74, 39.72 and 39.23.
- Pearson r = −0.042.
- Spearman ρ = −0.010 (95% CI −0.067 to 0.050, p = 0.753).
- OLS slope = −0.188 hours per item (95% CI −0.467 to 0.091, p = 0.187), not significant.

![Mean delivery_hours per quartile bin of items](tasks/eda_1/charts/delivery_by_items_quartile.png)

### Predictive modelling

Models were fitted on an 80/20 split (800 training rows, 200 test rows). Test-set scores:

| Model | Test MAE (h) | Test RMSE (h) | Test R² |
|---|---|---|---|
| Mean baseline | 9.46 | 12.62 | 0.000 |
| Linear regression | 9.11 | 11.74 | 0.135 |
| Gradient boosting | 3.76 | 4.70 | 0.861 |

Gradient boosting training R² is 0.927, close to its test R² of 0.861, so there is no heavy overfitting. Linear regression explains only 13.5% of test variance. Its coefficients (distance_km 4.05, parcel_weight_kg 2.13, weekday and depot terms up to 1.66) describe direction and size within that linear model only. They are not a measure of predictive value and are not used to rank features.

![Test-set mean absolute error in hours for the mean baseline, linear regression and gradient boosting on the 200-row test split](tasks/ml_1/charts/ml_1_model_mae.png)

Permutation importance for gradient boosting on the test set (increase in MAE in hours, mean with sd over 20 shuffles):

| Feature | MAE increase (h) | SD |
|---|---|---|
| parcel_weight_kg | 7.96 | 0.37 |
| distance_km | 2.66 | 0.29 |
| items | 0.01 | 0.04 |
| weekday | −0.02 | 0.04 |
| depot | −0.06 | 0.04 |

Weight and distance are clearly non-zero. Items, weekday and depot are within about two sd of zero, so they cannot be distinguished from zero on this measure. No reduced model was fitted, so this result does not show whether items, weekday and depot add anything once weight and distance are included.

![Permutation importance on the 200-row test set for gradient boosting: mean increase in MAE in hours over 20 shuffles, all six original features](tasks/ml_1/charts/ml_1_permutation_importance.png)

## Limitations

- **Zero-weight rows.** The 150 zero-weight parcels are a large group with much longer delivery times. The data do not say why. The analysis reports the association and does not establish a cause. Their effect changes the sign of the weight relationship, so results with and without these rows differ.
- **Quartile composition.** I have not tabulated how many zero-weight rows fall in each parcel_weight_kg quartile, so the Q1 mean cannot be attributed precisely.
- **Multiple comparisons.** The depot and weekday extreme-pair confidence intervals are unadjusted for choosing the extreme pair. The omnibus tests are not significant, so no depot or weekday effect is established.
- **Model evaluation.** The predictive results rest on one 200-row test split. No reduced model was fitted. The importance of items, weekday and depot is therefore not tested against a model without them.
- **Linearity.** The distance effect was estimated as linear in the OLS slopes. Linearity was not tested.
- **Failed tasks and unresolved review issues.** None were recorded.

## Open questions

- Why do zero-weight parcels take about 30 hours longer (about 38 hours after adjustment), and should they be modelled as a separate process or as missing-weight records?
- Is the distance effect linear, or does it curve at longer distances?
- Does the positive weight effect among non-zero parcels hold after fuller control, and is it linear or does it saturate at heavier weights?
- Do the depot and weekday differences stay non-significant under a regression that includes distance_km and parcel_weight_kg, and do they change when the zero-weight rows are analysed separately?
- Do items, weekday and depot add predictive value beyond parcel_weight_kg and distance_km? A reduced model fitted on those two features and compared on test MAE would answer this.