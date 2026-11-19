# Delivery Hours: Distribution, Depot and Weekday Effects, Drivers and Predictive Models (n = 1,000 parcels)

## Summary

- **Depot and weekday show no statistically significant effect on delivery_hours.** Depot: ANOVA p = 0.183, Kruskal-Wallis p = 0.214. Weekday: ANOVA p = 0.455, Kruskal-Wallis p = 0.402. Together the two factors explain about 1.03% of the variance.
- **Distance and parcel weight are the numeric associations that matter.** distance_km has a moderate positive association (Pearson r = 0.314). parcel_weight_kg has a weak negative linear association (Pearson r = -0.172). items shows no detectable association.
- **Gradient boosting predicts well on the 200-row test set.** Test R² is 0.861 and test MAE is 3.763 hours, against 9.460 hours for the mean baseline. Linear regression reaches test R² 0.135. Permutation importance ranks parcel_weight_kg first and distance_km second.
- **The boosted model and the adjusted linear model disagree on the direction of the weight effect.** The adjusted linear coefficient for parcel_weight_kg is negative (-0.685 h per kg). The boosted model's partial dependence rises with weight above 0.5 kg. The curve also drops sharply at 0 kg, where 121 training rows sit. This disagreement is unresolved.
- **The distance effect shows no significant depot interaction and is nearly identical across two seeds.** The distance_km by depot interaction gives p = 0.185. The brute-method distance curve differs by at most 0.090 h between seeds 42 and 7.

## Data

- 1,000 rows and 6 columns: parcel_weight_kg, distance_km and items (numeric); depot and weekday (categorical); delivery_hours (continuous target, regression).
- No date/time features, and no ids or free-text columns.
- No missing values in any column (0 of 1,000 for all six columns).

## Findings

### Distribution of delivery_hours and group means (EDA)

delivery_hours has a mean of 39.66 h, a median of 36.65 h and an sd of 13.10 h. The range is 15.7 h to 90.6 h, with quartiles of 30.9 h and 43.8 h. The mean exceeds the median, so the distribution is right-skewed with a long tail toward slow deliveries.

![Histogram of delivery_hours across all 1,000 parcels](tasks/eda_1/charts/delivery_hours_histogram.png)

By depot, mean delivery_hours ranges from 38.28 h (alpha, n = 249) to 40.71 h (beta, n = 250). Medians range from 35.60 h (alpha) to 37.50 h (gamma). Beta and gamma are slowest on both measures, and alpha is fastest. By weekday, the mean ranges from 38.30 h (Fri, n = 125) to 41.47 h (Sat, n = 148). Medians range from 35.20 h (Fri) to 38.10 h (Sat). Saturday is slowest and Friday fastest on both measures.

![Mean delivery_hours by depot and by weekday](tasks/eda_1/charts/delivery_hours_mean_by_group.png)

### Significance and effect sizes of depot and weekday (stat_1)

Neither factor has a statistically significant effect.

- **Depot:** one-way ANOVA F = 1.62, p = 0.183; Kruskal-Wallis H = 4.48, p = 0.214. Eta-squared is 0.0049 (epsilon-squared 0.0015).
- **Weekday:** one-way ANOVA F = 0.955, p = 0.455; Kruskal-Wallis H = 6.19, p = 0.402. Eta-squared is 0.0057 (epsilon-squared 0.0002).
- **Joint two-way OLS model (both factors):** eta-squared is 0.0047 for depot and 0.0056 for weekday, together about 1.03% of delivery_hours variance (joint R² 0.0105). Depot p = 0.194 and weekday p = 0.470.

Neither factor explains more than about 0.6% of the variance on its own.

Tukey HSD found no depot pair that differs. The largest gap is beta minus alpha at 2.43 h (adjusted p = 0.162, 95% CI -0.58 to 5.45 h). The smallest adjusted p among the other depot pairs is 0.3647 (alpha-gamma).

No weekday pair differs after Tukey correction. Saturday is 3.17 h above Friday (adjusted p = 0.422), and all 21 weekday pairs have adjusted p above 0.42.

Mean delivery_hours with 95% CIs, by depot: alpha 38.28 h (36.75 to 39.81), beta 40.71 h (38.98 to 42.45), delta 39.46 h (37.87 to 41.05), gamma 40.21 h (38.54 to 41.88). By weekday: Fri 38.30 h (36.15 to 40.46), Mon 38.60 h (36.54 to 40.65), Sat 41.47 h (39.28 to 43.66), Sun 39.17 h (37.03 to 41.31), Thu 39.81 h (37.58 to 42.04), Tue 39.76 h (37.63 to 41.88), Wed 40.28 h (38.05 to 42.52).

![Mean delivery_hours with 95% confidence intervals by depot and by weekday](tasks/stat_1/charts/delivery_hours_mean_ci_by_group.png)

### Association of numeric features with delivery_hours (stat_2)

- **distance_km:** moderate positive association. Pearson r = 0.314 (95% CI 0.257 to 0.369, p = 2.2e-24). Spearman rho = 0.436 (bootstrap 95% CI 0.382 to 0.491; recorded p = 1.2e-47, see Limitations). Longer distances mean slower deliveries.
- **parcel_weight_kg:** weak negative association. Pearson r = -0.172 (95% CI -0.231 to -0.111, p = 4.7e-8). Spearman rho = -0.078 (bootstrap 95% CI -0.154 to -0.002, p = 0.013). Heavier parcels are slightly faster. The rank-based effect is much smaller than the linear one.
- **items:** no meaningful association. Pearson r = -0.042 (95% CI -0.103 to 0.020, p = 0.187). Spearman rho = -0.010 (bootstrap 95% CI -0.067 to 0.050, p = 0.753). The Pearson interval includes zero.

**Depot and distance interaction.** The effect of distance_km does not differ significantly by depot (F = 1.61 on 3 df, p = 0.185).

**Slope of delivery_hours per km within each depot.** The slope is positive in every depot, with p-values below 0.001 in all four:

- alpha: 0.055 h/km (95% CI 0.039 to 0.072, p = 1.4e-10)
- beta: 0.041 h/km (95% CI 0.021 to 0.060, p = 4.5e-05). The p-value supports "positive and significant" within beta.
- delta: 0.034 h/km (95% CI 0.016 to 0.053, p = 0.0002)
- gamma: 0.058 h/km (95% CI 0.041 to 0.075, p = 2.2e-10)

Gamma has the steepest slope. The slopes look different in size, but the interaction test does not confirm that the difference is real.

### Adjusted associations in one multiple regression (stat_3)

This OLS model includes parcel_weight_kg, distance_km, items, depot and weekday.

- **parcel_weight_kg:** -0.685 h per kg (95% CI -0.920 to -0.451, p = 1.3e-8). The negative association remains after adjustment.
- **distance_km:** 0.046 h per km (95% CI 0.037 to 0.055, p = 8.5e-24). The positive association remains.
- **items:** -0.115 h per item (95% CI -0.378 to 0.148, p = 0.391). No detectable association.
- **Depot and weekday jointly:** F = 1.107 on 9 df, p = 0.355. They add no significant explanatory power.
- **Model fit:** R² = 0.136, adjusted R² = 0.126 (n = 1,000).

### Predictive performance and feature importance (ml_1)

The split is 800 training and 200 test rows (seed 42, test size 0.2).

| Model | Test MAE (h) | Test RMSE (h) | Test R² |
|---|---|---|---|
| Mean baseline | 9.460 | 12.615 | about 0 |
| Linear regression | 9.105 | 11.735 | 0.135 |
| Gradient boosting | 3.763 | 4.705 | 0.861 |

Gradient boosting has a training R² of 0.927. Linear regression improves only slightly on the mean baseline. This suggests that the relationship is strongly non-linear or involves interactions that a linear model misses. That is an inference and was not tested.

![Test MAE in hours of the mean baseline, linear regression and gradient boosting on the seed-42 80/20 test split](tasks/ml_1/charts/ml1_test_mae.png)

Permutation importance for gradient boosting (increase in test MAE when a feature is shuffled, 20 repeats):

- parcel_weight_kg: 7.963 h (SD 0.373)
- distance_km: 2.663 h (SD 0.287)
- items: 0.020 h (SD 0.041)
- Depot and weekday dummies: all close to zero, between -0.036 and 0.001 h.

### Interaction terms in the gradient boosting model (ml_2)

Adding depot-by-weekday and distance-by-depot interaction terms does not improve held-out error. Test MAE rises from 3.763 to 3.813 h, test RMSE from 4.705 to 4.808 h, and test R² falls from 0.861 to 0.855. These results come from the seed-42 test split.

![Test MAE in hours of gradient boosting with main effects only and with depot-by-weekday and distance_km-by-depot interaction terms, same seed-42 test split](tasks/ml_2/charts/ml2_gb_mae_comparison.png)

### Shape of the parcel_weight_kg and distance_km effects in the boosted model (ml_3, partial)

**parcel_weight_kg.** Partial dependence (brute method, training rows) has a sharp drop at 0 kg: about 65.35 h at 0 kg, then 29.49 h at 0.55 kg and 29.43 h at 1.09 kg. Above about 0.5 kg the curve is roughly monotone increasing rather than U-shaped: 30.8 to 32.7 h across 1.64 to 3.28 kg, 34.8 h at 4.92 kg, 40.5 h at 8.2 kg, and a plateau at 42.38 h from 8.74 to 10.38 kg. Observed training means by weight bin agree with the curve: 65.38 h for the 121 rows at 0 to 0.5 kg, 31.04 h for 2 to 3 kg (131 rows), and 43.31 h for 9 to 10.5 kg (21 rows).

**distance_km.** The brute-method curve rises from 34.27 h at 19 km to 47.02 h at 287 km. The rise is close to linear, with slight steepening at longer distances and no saturation. It is not threshold-like within the observed range.

![Partial dependence of predicted delivery_hours on parcel_weight_kg and distance_km (gradient boosting, training rows; seeds 42 and 7)](tasks/ml_3/charts/ml3_partial_dependence.png)

**Seed robustness (brute method).**

- parcel_weight_kg: the maximum absolute difference between seed 42 and seed 7 is 0.006 h. The grid point at which this maximum occurs is not stored in the facts. The 0 kg drop and the rise beyond it appear at both seeds, so the threshold-like 0 kg effect holds across the two seeds tested.
- distance_km: the maximum absolute difference is 0.090 h, at the first grid point, 19.141 km (seed 42 gives 34.271 h, seed 7 gives 34.181 h). The near-linear distance effect holds across the two seeds tested.

**Disagreement between models on the weight effect.** The adjusted linear coefficient for parcel_weight_kg is negative (-0.685 h per kg, stat_3). The boosted model's partial dependence and the observed bin means rise with weight above 0.5 kg. The two results point in opposite directions over that range. This is reported as a disagreement and is not resolved here.

**Distance direction comparison.** The boosted model's distance curve is positive and close to linear. The adjusted linear coefficient is 0.046 h per km (stat_3), also positive.

## Limitations

- **Single dataset, associations only.** All results are associations in 1,000 rows. The findings do not identify causes or mechanisms.
- **Null depot and weekday results are not evidence of no effect.** Whether a larger sample would change them was not tested.
- **Small effect sizes.** Depot and weekday each explain about 0.6% of variance or less, and together about 1.03%. The adjusted model R² is 0.136.
- **Weak parcel weight association.** The linear association is weak (r = -0.172), and the rank-based association is smaller still (rho = -0.078, CI reaching -0.002).
- **Conflicting p-value for the distance Spearman correlation.** The stat_2 finding text gives p = 1.2e-4 for Spearman rho = 0.436. The recorded value for the same test is p = 1.2e-47, which is the value reported above. The two disagree and this report does not resolve the conflict.
- **Test-set scale.** The ML scores come from a single 200-row test split. The gradient boosting results are from one seed (42). The seed-7 refit has test MAE 3.757 h, against 3.763 h for seed 42.
- **Partial dependence levels.** The sklearn default partial-dependence method gave wrong levels (for example, a mean of -2.12 h against a manual 37.58 h). Only the brute-method and hand-computed curves are used in this report.
- **The 0 kg group may be a separate population (unresolved).** 121 training rows have parcel_weight_kg of 0 and a mean delivery_hours of 65.38 h. This group may be a separate population, such as a parcel type or a missing weight coded as zero. The 0 kg drop in the partial-dependence curve should not be read as a true low-weight effect until this is checked. The check has not been done.
- **Robustness of the weight curve, partly unresolved (ml_3 review issue).** The brute-method seed difference is reported above. The grid point of the maximum difference for parcel_weight_kg is not stored in the facts, so that part of the review request cannot be completed.
- **Two-way effects not tested.** A two-way partial dependence of distance_km and parcel_weight_kg was not produced. Whether the weight effect is steeper at long distances is therefore unknown.
- **Saturday effect not tested after adjustment.** No fact reports the Saturday coefficient in the multiple regression or in the boosted model.
- **Task status.** ml_3 is partial. The other tasks (eda_1, stat_1, stat_2, ml_1, ml_2, stat_3) are complete.

**Numbers not traced to a recorded fact.** The automatic check found no recorded value for these numbers:
- 1.2e-4 in: "- **Conflicting p-value for the distance Spearman correlation.** The stat_2 finding text gives p = 1.2e-4 for Spearman rho = 0.436. The recorded value for the s"

## Open questions

- Is the 0 kg group a separate population (for example, a parcel type or a missing weight coded as zero), or a true low-weight effect?
- Why does the boosted model show a rising weight effect above 0.5 kg when the adjusted linear coefficient is negative? Does the disagreement reflect non-linearity, the 0 kg group, or something else?
- Does the weight effect differ at long distances? A two-way partial dependence of distance_km and parcel_weight_kg has not been computed.
- Is the Saturday effect still present after controlling for depot, distance_km and parcel weight? The adjusted Saturday coefficient has not been estimated.
- Does the distance effect differ by weekday, given that depot and weekday add no joint explanatory power?
- Do the non-significant depot and weekday differences hold with a larger sample?
- What is the grid point at which the brute-method maximum seed difference for parcel_weight_kg occurs?