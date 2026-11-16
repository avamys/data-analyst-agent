# Delivery Hours Analysis: Drivers of delivery_hours in a 1,000-Shipment Dataset

## Summary

- **parcel_weight_kg and distance_km carry the predictive signal.** The random forest reached test R² 0.861 and MAE 3.65 hours, against R² of about 0 and MAE 9.46 hours for the mean-of-target baseline. Shuffling parcel_weight_kg raised test MAE by 8.05 hours, and distance_km was the only other feature with a large effect (2.60 hours). The 150 zero-weight parcels have much longer delivery times (mean 65.31 hours, against 35.13 for the other 850). The forest's test scores are optimistic, since its training R² was 0.981.
- **The weight association reverses direction depending on whether zero-weight rows are included.** Across all 1,000 rows the Spearman correlation is negative (rho -0.078, p 0.013). Across the 850 nonzero-weight rows it is positive (rho +0.487, p 7.1e-52). stat_3 attributes the all-rows result to the zero-weight parcels, but this attribution was not tested directly.
- **Distance is the main continuous driver.** delivery_hours rises with distance_km (Pearson 0.314, Spearman 0.436). Among the depot-adjusted candidates tested, the linear distance term was adequate: spline, quadratic and log-distance terms did not improve on it. The depot-by-distance interaction was not significant (p = 0.185). These tests did not include parcel_weight_kg.
- **Depot and weekday differences are small.** The Kruskal-Wallis tests were not significant for depot (p = 0.214) or weekday (p = 0.402). An adjusted all-rows model found a small significant depot effect (p = 0.0095, partial eta squared 0.012), but this was not significant on nonzero-weight rows (p = 0.128). Weekday was not significant in any model.
- **Missing values: none.** All six columns are complete.

## Data

- **Size:** 1,000 rows × 6 columns. Numeric features: parcel_weight_kg, distance_km, items. Categorical features: depot, weekday. No date or time features.
- **Target:** delivery_hours (regression), range 15.7 to 90.6, median 36.65.
- **Missing values:** none in any column (total 0).
- **Zero-valued weights:** 150 rows (15%) have parcel_weight_kg equal to 0. The median parcel_weight_kg is 3.735 kg.

## Findings

### Overall distribution of the target

delivery_hours is right-skewed (skew 1.20). Its mean is 39.66 hours, median 36.65, quartiles 30.9 and 43.8, and standard deviation 13.10. The 10-bin histogram peaks in the 30.7 to 38.2 hour bin with 334 shipments, and only 2 shipments exceed 83 hours.

![Histogram of delivery_hours for all 1000 shipments](tasks/eda_1/charts/hist_delivery_hours.png)

### Depot and weekday (descriptive)

- **Depot:** Mean delivery_hours was beta 40.71 (median 37.45, n=250), gamma 40.21 (median 37.50, n=238), delta 39.46 (median 36.30, n=263) and alpha 38.28 (median 35.60, n=249). Medians span only 35.6 to 37.5 hours.
- **Weekday:** Saturday had the highest mean (41.47, median 38.10, n=148) and Friday the lowest (38.30, median 35.20, n=125). The other weekdays had means of 38.60 (Mon), 39.17 (Sun), 39.76 (Tue), 40.28 (Wed) and 39.81 (Thu). The mean-median gap is about 3 hours in every group.

![Boxplot of delivery_hours for each depot](tasks/stat_1/charts/depot_delivery_boxplot.png)

![Boxplot of delivery_hours for each weekday](tasks/stat_1/charts/weekday_delivery_boxplot.png)

### Significance tests for depot and weekday (stat_1)

- **Depot:** Kruskal-Wallis H = 4.48 (df 3), p = 0.214, epsilon-squared 0.0045 (negligible). No significant depot difference.
- **Weekday:** Kruskal-Wallis H = 6.19 (df 6), p = 0.402, epsilon-squared 0.0062 (negligible). No significant weekday difference.
- **Depot pairwise tests:** Two-sided Mann-Whitney tests with Holm correction found no significant pair. The alpha vs beta raw p was 0.064 (Holm p 0.386). Alpha vs delta had Holm p = 1.0.
- **Bootstrap, beta vs alpha:** The mean difference was 2.43 hours (95% CI 0.17 to 4.80, 2,000 resamples). The interval excludes zero, but it is not adjusted for choosing the most extreme pair and conflicts with the non-significant omnibus test. It should be read as a weak, descriptive signal.

### Depot and weekday after adjusting for distance and zero weight (stat_3)

- **All 1,000 rows** (OLS of delivery_hours on depot, weekday, distance_km and zero_weight; Type II F tests): Depot F = 3.84, p = 0.0095, partial eta squared 0.012. Weekday F = 0.70, p = 0.646, partial eta squared 0.004. Model R² was 0.782. The zero_weight coefficient was 30.19 hours.
- **850 nonzero-weight rows** (OLS of delivery_hours on depot, weekday, distance_km and parcel_weight_kg): Depot F = 1.90, p = 0.128, partial eta squared 0.007. Weekday F = 0.40, p = 0.880, partial eta squared 0.003. Model R² was 0.712.
- **Interpretation:** The depot result differs between the two samples. The loss of depot significance cannot be attributed to the zero-weight rows alone, because the nonzero-rows model changes two things at once: it drops the zero-weight rows and replaces zero_weight with parcel_weight_kg as the covariate. Weekday is not significant in either analysis.

### Items (stat_1)

Spearman rho for items with delivery_hours is -0.010 (p = 0.753), with no meaningful association. Pearson is -0.042.

### Parcel weight

- **All 1,000 rows (stat_1):** Spearman rho -0.078 (p = 0.013), statistically significant but small (rho² about 0.006). Pearson is -0.172.
- **Zero-weight versus other parcels (eda_2):** The zero-weight group has mean delivery_hours 65.31 and median 64.6 (n=150). The other 850 rows have mean 35.13 and median 34.9. The Welch t-test gives p = 2.2e-107 and the Mann-Whitney test p = 7.0e-84. Zero-weight rows do not differ from the others in distance_km (mean 153.10 vs 154.42, Welch p = 0.87) or items (mean 5.25 vs 5.56, Welch p = 0.23). The depot distribution does not differ (chi-square 0.87, df 3, p = 0.83), nor does the weekday distribution (chi-square 1.80, df 6, p = 0.94).

![Boxplot of delivery_hours (hours) for shipments with parcel_weight_kg equal to 0 (n=150) vs other shipments (n=850)](tasks/eda_2/charts/zero_weight_delivery_hours_box.png)

- **Nonzero-weight rows (stat_3):** Spearman rho +0.487 (n=850, p = 7.1e-52, rho² 0.237). In the nonzero-weight OLS model, adjusted for depot, weekday and distance_km, the parcel_weight_kg coefficient is positive: 1.557 hours per kg, p = 8.3e-157. Its partial eta squared is 0.573.
- **Disagreement:** The all-rows Spearman association is negative (stat_1) and the nonzero-rows association is positive (stat_3). These findings disagree in direction. stat_3 attributes the all-rows negative association to the zero-weight parcels. The reported facts do not test that attribution directly.

### Distance and the depot interaction (stat_2)

- **Interaction:** The depot-by-distance_km partial F-test gives F = 1.61 (df 3 and 992), p = 0.185. Adding the interaction changes R² by 0.004, from 0.102 to 0.107. The interaction is not significant and, per stat_2, not worth breaking down by depot. The common distance effect is the more defensible summary.
- **Within-depot slopes (descriptive only):** alpha 0.055 hours per km (95% CI 0.039 to 0.072), beta 0.041 (0.021 to 0.060), delta 0.034 (0.016 to 0.053), gamma 0.058 (0.041 to 0.075). The CIs overlap.
- **Overall correlation with distance (EDA):** Pearson 0.314, Spearman 0.436.

![Per-depot linear fits of delivery hours on distance](tasks/stat_2/charts/slopes_by_depot.png)

![Scatter of delivery_hours against distance_km for all 1000 shipments](tasks/eda_1/charts/scatter_delivery_vs_distance.png)

### Non-linearity of distance (stat_4)

These models include depot as the only covariate. parcel_weight_kg was not included.

- **Spline versus linear:** Partial F = 0.85 (df 2 and 993), p = 0.43. The spline R² was 0.1039 against 0.1023 for linear. Its AIC was 7886.9 against 7884.6 for linear.
- **Quadratic versus linear:** F = 1.64, p = 0.20. The quadratic AIC was 7885.0.
- **Log distance:** R² 0.082 against 0.102 for linear. AIC was 7907.4, 22.7 higher than linear.
- **Conclusion:** Among these candidates the linear distance term has the best AIC, and the quadratic and spline differences are near ties. This conclusion does not include parcel_weight_kg, so it has not been checked once weight is controlled.

![Fitted delivery-hours curves for linear, spline and log-distance models, depot fixed at its modal level](tasks/stat_4/charts/stat_4_distance_models.png)

### Predictive models (ml_1)

Training set n = 800; test set n = 200.

| Model | Test R² | Test MAE (hours) |
|---|---|---|
| Mean-of-target baseline | about 0 | 9.46 |
| Linear regression (one-hot depot and weekday) | 0.135 | 9.11 |
| Random forest (300 trees) | 0.861 | 3.65 |

- The random forest's test RMSE was 4.71 hours, against 12.62 for the baseline.
- The forest overfits: its training R² was 0.981 and its test R² 0.861. The test figures are therefore optimistic.
- **Permutation importance (forest, test MAE increase):** parcel_weight_kg 8.05 hours (sd 0.66), distance_km 2.60 (sd 0.27), items 0.05 (sd 0.05), depot -0.03 (sd 0.03), weekday 0.01 (sd 0.06). Items, depot and weekday contribute essentially nothing once weight and distance are known.
- **Hypothesis, not a result:** The weight dependence is consistent with the zero-weight gap in eda_2, and the forest may be separating the zero-weight group. This was not tested in ml_1. The linear model's weak score may reflect the same non-linear weight effect, which is also untested.

![Test-set mean absolute error in hours for the mean baseline, linear regression and random forest](tasks/ml_1/charts/ml1_model_mae.png)

![Permutation importance of original features for the random forest, measured as test MAE increase in hours](tasks/ml_1/charts/ml1_perm_importance.png)

## Limitations

- **Zero-weight parcels are unexplained.** The findings do not establish whether the 150 zero-weight rows are a data-entry artifact (for example, missing weight recorded as 0) or a distinct shipment type. The all-rows depot and weight results depend on this question.
- **Conflicting weight results.** The all-rows Spearman (negative, stat_1) and the nonzero-rows Spearman (positive, stat_3) disagree in direction. The attribution of the all-rows result to the zero-weight group is stated in stat_3 but not tested.
- **Conflicting depot results.** The depot effect is not significant in stat_1 (p = 0.214) and not significant on nonzero rows in stat_3 (p = 0.128). It is significant in the adjusted all-rows model in stat_3 (p = 0.0095, small effect). These are not resolved. The nonzero-rows model changes both the sample and the covariate, so its loss of significance cannot be attributed to either alone.
- **Unresolved review issue (stat_3).** The first stat_3 finding was submitted with the literal placeholder "(weight_coef, weight_p)" in place of numbers. The lead's objection stands: the finding as written was incomplete. The values reported above (1.557 hours per kg, p = 8.3e-157) are taken from the weight_coef and weight_p fields of the nonzero-rows model. They affect the nonzero-rows weight finding and the weight conclusions drawn from it.
- **Pairwise and bootstrap depot results are unadjusted or weak.** No pairwise depot comparison is significant after Holm correction. The beta vs alpha bootstrap interval excludes zero, but it is unadjusted for pair selection and conflicts with the omnibus test.
- **Non-linearity tests omit weight.** The distance tests (stat_4) include depot only. The linear-adequacy conclusion has not been rechecked with parcel_weight_kg in the model. The Spearman-Pearson gap for distance (0.44 vs 0.31) was not tested, and outliers and the zero-weight group were not examined.
- **Interaction test omits weight.** The depot-by-distance interaction (stat_2) was tested without zero_weight or parcel_weight_kg in the model.
- **Model scores are optimistic.** The random forest's training R² (0.981) exceeds its test R² (0.861), and the test set has only 200 rows. The zero-weight explanation of the forest's weight dependence was not tested in ml_1.
- **Effect sizes.** stat_3 describes all depot and weekday effects as small. Distance and parcel weight are the only effects reported as large.

## Open questions

- Are the 150 zero-weight parcels a data-entry artifact or a distinct shipment type with longer handling? The answer bears on whether the all-rows depot effect and the all-rows weight correlation are meaningful.
- Does dropping zero_weight while keeping the nonzero rows, separately from changing the covariate, explain the loss of depot significance?
- Do depot and weekday differences remain significant in a single model that includes distance_km, zero_weight and parcel_weight_kg?
- Does the distance effect differ by depot once the zero-weight parcels are controlled for?
- Is the distance effect non-linear once parcel weight is in the model, and what accounts for the gap between the Spearman (0.44) and Pearson (0.31) correlations with distance?
- Is the positive parcel_weight_kg association on nonzero-weight rows linear, or better described by a non-linear or monotone fit?
- Does the random forest's weight dependence come from separating the zero-weight group? Re-scoring the models with zero_weight as an explicit feature, and with zero-weight rows excluded, would address this.