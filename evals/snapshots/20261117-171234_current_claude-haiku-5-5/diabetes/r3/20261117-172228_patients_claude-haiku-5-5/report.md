# Diabetes Screening Dataset (768 rows): Predictors of the Outcome Target

## Summary

- **Glucose is the strongest univariate separator of Outcome.** Its rank-biserial effect is 0.586 (95% CI 0.517 to 0.645). BMI and Age follow at 0.374 each, then SkinThickness (0.325), Pregnancies (0.239), BloodPressure (0.215) and DiabetesPedigreeFunction (0.212). All eight features are significant after Holm correction, but the Insulin and SkinThickness effects were measured only on rows with non-zero values.
- **In one adjusted logistic model, Glucose, BMI and DiabetesPedigreeFunction stay associated with Outcome.** Age (p=0.065) and Pregnancies (p=0.138) do not reach significance in that additive model. Age × Pregnancies is significant as an interaction (p=0.003). The adjusted model used 392 complete cases with 130 events, so it describes only that subset.
- **Both models beat the majority-class baseline on a single 154-row test split.** The baseline accuracy is 64.9%. Logistic regression reaches 71.4% accuracy and ROC AUC 0.818. The random forest reaches 73.4% accuracy and ROC AUC 0.807. Neither model dominates, and recall for Outcome=1 is 53.7% (logistic regression) and 55.6% (random forest).
- **Zeros are the central data problem.** 49.0% of rows (376) have a zero in at least one of Glucose, BloodPressure, SkinThickness, Insulin or BMI. The Insulin and SkinThickness effects depend on how those zeros are handled: the rank-biserial rises from 0.463 to 0.670 for Insulin when zeros are imputed within Outcome group. That imputation uses the target label, so the imputed magnitudes are not reliable.

## Data

- **Size:** 768 rows × 9 columns (8 numeric features, 1 binary target). There are no categorical, date/time, identifier or free-text features, and no empty cells.
- **Target:** Outcome. Class 0 is 65.1% and class 1 is 34.9%.
- **Implicit missing values:** Zeros in Glucose (5 rows), BloodPressure (35), SkinThickness (227), Insulin (374) and BMI (11) are physiologically impossible and were treated as missing in the analysis. Pregnancies, DiabetesPedigreeFunction and Age were not treated as missing.
- **Feature ranges (profile):** Pregnancies 0 to 17 (median 3); Glucose 0 to 199 (median 117); BloodPressure 0 to 122 (median 72); SkinThickness 0 to 99 (median 23); Insulin 0 to 846 (median 30.5); BMI 0 to 67.1 (median 32); DiabetesPedigreeFunction 0.078 to 2.42 (median 0.3725); Age 21 to 81 (median 29).

## Findings

### Where zeros occur and whether they relate to Outcome

Zeros are common in Insulin (374 rows, 48.7%) and SkinThickness (227 rows, 29.6%). BloodPressure has 35 (4.6%), BMI 11 (1.4%) and Glucose 5 (0.7%). Zeros overlap strongly. Every SkinThickness zero is also an Insulin zero, and every BloodPressure zero is also an Insulin zero. Four of the five Glucose zeros are Insulin zeros. The zeros most likely mark missing values, since a value of 0 is physiologically impossible for these measurements.

![Share of rows with a zero value in each column](tasks/eda_1/charts/zero_shares.png)

Outcome rates for zero versus non-zero rows, with 95% Wilson intervals:

| Column | Zero rows: Outcome=1 rate (n) | Non-zero rows: rate (n) |
|---|---|---|
| Glucose | 40.0% (5) | 34.9% (763) |
| BloodPressure | 45.7% (35) | 34.4% (733) |
| SkinThickness | 38.8% (227) | 33.3% (541) |
| Insulin | 36.9% (374) | 33.0% (394) |
| BMI | 18.2% (11) | 35.1% (757) |

The intervals overlap heavily for SkinThickness and Insulin, and the BloodPressure zero interval overlaps the non-zero interval. The Glucose and BMI zero groups are too small to interpret. No reliable association between zeros and Outcome is shown.

### How the Outcome rate varies across each feature

Rates are Outcome=1 shares across bins. The overall rate is 34.9%.

- **Glucose** has the steepest gradient. Across nonzero quintiles the rate rises from 7.7% (n=155) in the lowest group to 19.5% (n=154), 30.6% (n=157), 44.3% (n=149), and 74.3% (n=148) in the highest. Zero-Glucose rows show 40.0% (n=5).
- **Insulin** rises across nonzero quintiles, from 7.6% (n=79) to 54.7% (n=75). The zero-Insulin group (n=374) has 36.9%.
- **BMI** rises from 7.7% (n=155) in the lowest nonzero quintile to 51.3% (n=152) in the highest. The zero-BMI group (n=11) has 18.2%.
- **BloodPressure** rises from 20.9% (n=158) to 47.4% (n=135) across nonzero quintiles. The zero group (n=35) has 45.7%.
- **SkinThickness** rises from 13.5% (n=111) to 46.3% (n=108) across nonzero quintiles. The zero group (n=227) has 38.8%.
- **DiabetesPedigreeFunction** rises almost monotonically, from 22.1% (n=154) to 49.7% (n=153). The steepest step is into the top quintile.
- **Age** is not monotone on the decade-like bins: 21.2% (21 to 29, n=396), 46.1% (30 to 39, n=165), 55.1% (40 to 49, n=118), 59.6% (50 to 59, n=57), 28.1% (60+, n=32). The drop in the 60+ group rests on n=32 and may be sampling noise.
- **Pregnancies** is not a simple rise. Using natural levels, the Outcome=1 rates are 34.2% at 0 (n=111), 21.5% at 1 (n=135), 18.4% at 2 (n=103), 36.0% at 3 (n=75), 35.2% at 4 to 5 (n=125) and 50.7% at 6+ (n=219). Pooled bins give 34.2% at 0, 20.2% at 1 to 2 (n=238), 35.5% at 3 to 5 (n=200) and 50.7% at 6+. The rates are high at 0, dip at low counts, and rise at 6 or more. The pooled and unpooled bins are different groupings of the same data.

![Outcome rate by Glucose bin; n printed under each bin](tasks/eda_2/charts/eda2_rate_by_glucose_n.png)

![Outcome rate by Pregnancies bin; n printed under each bin](tasks/eda_2/charts/eda2_rate_by_pregnancies_n.png)

![Outcome rate by Age bin; n printed under each bin](tasks/eda_2/charts/eda2_rate_by_age_n.png)

![Outcome rate by Insulin bin; n printed under each bin](tasks/eda_2/charts/eda2_rate_by_insulin_n.png)

### Which features differ between Outcome=1 and Outcome=0

Tests are Mann-Whitney U with Holm correction across the eight features. Effects are rank-biserial (rb) with bootstrap 95% CIs, and Cohen's d. Insulin and SkinThickness use only non-zero rows.

- **Glucose** (median 140 vs 107; n=266 vs 497): rb 0.586 (0.517 to 0.645), d 1.19 (1.02 to 1.36), Holm p=1.0e-39.
- **Insulin** (observed subset, n=130 vs 264; median 169.5 vs 102.5): rb 0.463 (0.365 to 0.564), d 0.68 (0.48 to 0.92), Holm p=3.7e-13. This holds only for the observed rows; the 374 Insulin zeros (49% of values) are excluded.
- **BMI** (median 34.3 vs 30.1; n=266 vs 491): rb 0.374 (0.303 to 0.450), d 0.69 (0.55 to 0.84), Holm p=1.1e-16.
- **Age** (median 36 vs 27; n=268 vs 500): rb 0.374 (0.298 to 0.445), d 0.51 (0.36 to 0.68), Holm p=8.0e-17.
- **SkinThickness** (observed subset, n=180 vs 361; median 32 vs 27): rb 0.325 (0.230 to 0.418), d 0.57 (0.39 to 0.74), Holm p=2.8e-9.
- **Pregnancies** (median 4 vs 2; n=268 vs 500): rb 0.239 (0.153 to 0.322), d 0.48 (0.32 to 0.63), Holm p=1.1e-7. A binned chi-square (bins 0, 1–2, 3–5, 6+) gives chi² = 46.8, df=3, p=3.8e-10. This shows an overall difference. It does not show a monotone rise, and the per-bin rates above are non-monotone.
- **BloodPressure** (observed subset, n=252 vs 481; median 74.5 vs 70): rb 0.215 (0.128 to 0.298), d 0.36 (0.22 to 0.52), Holm p=2.4e-6.
- **DiabetesPedigreeFunction** (median 0.449 vs 0.336; n=268 vs 500): rb 0.212 (0.128 to 0.299), d 0.37 (0.22 to 0.53), Holm p=2.4e-6.

The largest Holm-adjusted p-value is 2.4e-6, and every bootstrap CI excludes zero.

![Rank-biserial effect size per feature, Outcome=1 vs 0, with 95% bootstrap CI; zeros treated as missing](tasks/stat_1/charts/stat1_effect_sizes.png)

### Sensitivity of the Insulin and SkinThickness effects to imputation

On the complete-case frame, the estimates match the main comparison: Insulin rb 0.463 (bootstrap CI 0.360 to 0.562, p=7.48e-14) and SkinThickness rb 0.325 (CI 0.226 to 0.416, p=6.96e-10). The CI endpoints differ slightly from the earlier run because of bootstrap resampling.

When zeros are replaced by within-Outcome medians on the full 768-row frame (n=268 vs 500), the estimates rise. Insulin rb is 0.670 (CI 0.604 to 0.739, p=8.29e-55), with medians unchanged at 169.5 vs 102.5. SkinThickness rb is 0.432 (CI 0.351 to 0.508, p=2.92e-23), with medians unchanged at 32 vs 27.

The direction and significance are the same on both frames. The magnitude is not: the effect sizes depend on the imputation choice. This imputation uses the Outcome label, so each imputed zero is moved toward its own group's median. That construction adds group separation by design. The imputed-frame p-values and CIs also treat imputed values as independent observations and are overconfident. The complete-case results are the more reliable comparison. Whether the complete-case values are biased in either direction is not established, because the zeros may not be missing at random.

![Rank-biserial effect of Insulin and SkinThickness, complete-case vs within-Outcome median imputation, with 95% bootstrap CIs](tasks/stat_3/charts/stat3_imputation_sensitivity.png)

### Interactions between features

- **Glucose × BMI** is not supported: interaction OR 0.97 per SD² unit (95% CI 0.77 to 1.21), p=0.77, on 752 complete-case rows.
- **Age × Pregnancies** is significant and negative: OR 0.72 per SD² unit (95% CI 0.58 to 0.89), p=0.003. The likelihood-ratio test for both interaction terms gives chi² = 9.52, df=2, p=0.009. The result rests mainly on Age × Pregnancies.
- In the median-split 2×2 (Age median 29, Pregnancies median 3), the Outcome=1 rate at or below median age is 20.6% for Pregnancies at or below 3 (n=321) and 28.1% for Pregnancies above 3 (n=64). Above median age, it is 50.0% at or below 3 (n=94) and 48.7% above 3 (n=273). The Pregnancies gap nearly vanishes in the older group.

![Left: Outcome rate by Pregnancies bin. Right: Outcome rate in the 2×2 Age × Pregnancies median split](tasks/stat_2/charts/stat2_outcome_rates.png)

### Adjusted association of each feature with Outcome

One multivariable logistic model included all eight features with zeros treated as missing. It used 392 complete cases (130 events); 376 rows were dropped, mostly because of the 374 Insulin zeros. Odds ratios are per unit.

| Feature | OR | 95% CI | p |
|---|---|---|---|
| Glucose (per mg/dL) | 1.039 | 1.027 to 1.051 | <0.001 |
| BMI (per kg/m²) | 1.073 | 1.017 to 1.132 | 0.010 |
| DiabetesPedigreeFunction | 3.130 | 1.354 to 7.233 | 0.008 |
| Age (per year) | 1.035 | 0.998 to 1.072 | 0.065 |
| Pregnancies (per pregnancy) | 1.086 | 0.974 to 1.210 | 0.138 |
| SkinThickness (per mm) | 1.011 | 0.978 to 1.046 | 0.511 |
| Insulin (per unit) | 0.999 | 0.997 to 1.002 | 0.528 |
| BloodPressure (per mmHg) | 0.999 | 0.976 to 1.022 | 0.904 |

Glucose, BMI and DiabetesPedigreeFunction remain associated with Outcome in this model. Age and Pregnancies do not reach significance. This model is additive and omits the Age × Pregnancies interaction, which is significant in the interaction analysis, so the non-significance is conditional on the additive specification and is not evidence of no association. The DiabetesPedigreeFunction estimate is wide and rests on the observed-complete subset. The Insulin estimate describes only the 130-event observed subset and does not establish a null effect in the full population.

### Predictive performance against the majority-class baseline

Zeros were replaced by missing values, with median imputation and standardisation fitted on training rows only, and missing-indicator columns were added for the five columns (13 features in total). One stratified 80/20 split (seed 42) gave 614 training and 154 test rows. Class-1 share was 34.9% overall, 34.9% in training and 35.1% in test.

| Model | Test accuracy | Test ROC AUC | Precision (class 1) | Recall (class 1) | F1 (class 1) | Train accuracy |
|---|---|---|---|---|---|---|
| Majority-class baseline | 64.9% | 0.500 | — | — | — | — |
| Logistic regression | 71.4% | 0.818 | 0.604 | 0.537 | 0.569 | 0.795 |
| Random forest | 73.4% | 0.807 | 0.638 | 0.556 | 0.594 | 1.000 |

Both models beat the baseline on accuracy. The random forest has slightly higher accuracy and slightly lower AUC than logistic regression, so neither dominates. Their test confusion matrices, as [[TN, FP], [FN, TP]], are [[81, 19], [25, 29]] for logistic regression and [[83, 17], [24, 30]] for the random forest. The random forest fits the training set perfectly, a gap of 0.266 to its test accuracy.

![Test-set accuracy and ROC AUC of the majority baseline, logistic regression and random forest](tasks/ml_1/charts/ml1_model_comparison.png)

### Feature importance in the fitted models

- **Random forest permutation importance** (mean drop in test ROC AUC, 30 shuffles): Glucose 0.096 (SD 0.022), BMI 0.032 (SD 0.018), Age 0.022 (SD 0.012), Insulin 0.006 (SD 0.010), DiabetesPedigreeFunction 0.005 (SD 0.008), Pregnancies 0.003 (SD 0.009).
- **Logistic regression standardised coefficients** (absolute values): Glucose 1.199, BMI 0.700, Pregnancies 0.372, DiabetesPedigreeFunction 0.254, BloodPressure_missing 0.201, Insulin_missing 0.182, Age 0.148, SkinThickness_missing 0.109 (signed −0.109), BMI_missing 0.088 (signed −0.088), Glucose_missing 0.061.

Glucose and BMI are the top two in both models. Age is third for the random forest but seventh for logistic regression. Pregnancies is third for logistic regression but sixth for the random forest. The random forest's permutation SDs are as large as its means for the lower-ranked features, so those positions are uncertain.

The missing indicators overlap heavily: every BloodPressure zero and every SkinThickness zero is also an Insulin zero. Their large logistic coefficients may therefore reflect collinearity rather than separate signal. In the random forest, the missing indicators rank 7 to 11 of 13 features. Insulin_missing has mean 0.0018 (SD 0.0023). BMI_missing has mean 0.0009 (SD 0.0005), the largest of the missing-indicator means relative to its SD, so it is the clearest exception to the claim that the missing-indicator importances are small relative to their SDs.

On the logistic regression, BloodPressure_missing (0.201) and Insulin_missing (0.182) have larger absolute coefficients than Age (0.148). SkinThickness_missing (0.109) is below Age but above BMI_missing (0.088) and Glucose_missing (0.061). Coefficients are on standardised features and are comparable within the model.

![Permutation importance of each feature for the random forest on the 154-row test set](tasks/ml_2/charts/ml2_permutation_importance.png)

## Limitations

- **Zeros are treated as missing, not measured values.** This is an assumption from physiology and the co-occurrence pattern. Zeros appear in at least one of the five columns for 49.0% of rows. The complete-case adjusted model drops 376 of 768 rows. Insulin and SkinThickness results describe the observed subset.
- **Imputation choice changes effect sizes.** The Insulin rank-biserial moves from 0.463 (complete case) to 0.670 (within-Outcome imputation), and SkinThickness from 0.325 to 0.432. The imputation uses the Outcome label, so its effect sizes are inflated by construction. The imputed-frame p-values (for example 8.29e-55) treat imputed values as independent observations and are overconfident. Significance on the complete-case frame is the reliable comparison.
- **Pregnancies is reported as non-monotone, not as a rise.** The per-bin rates differ with the binning used (natural levels or pooled 1–2 and 3–5). The chi-square and Mann-Whitney results show an overall difference only.
- **Adjusted model is additive.** The non-significance of Age and Pregnancies depends on leaving out the Age × Pregnancies interaction. The Glucose × BMI interaction was tested only in its linear form.
- **Small groups are unreliable.** The Glucose zero group (n=5) and BMI zero group (n=11) are too small for their rate comparisons. The Age 60+ group (n=32) may be sampling noise.
- **Single test split.** The model results rest on one 154-row test set. The gap between the models (about 2 points of accuracy) has not been checked against sampling noise. Random forest permutation importances are measured on that same small test set.
- **Missing-indicator collinearity.** The BloodPressure and Insulin missing indicators overlap, so their coefficients and importances may be unstable. The logistic coefficient for Insulin and the random forest importance for BloodPressure_missing could not be verified against the full model output and are not reported here.
- **Unresolved review issues.** The review of the Pregnancies finding asked that the per-bin rates be reported and that the association not be described as a simple rise; both are done above. The review of the logistic coefficient ranking asked that the ranking be restated from the fitted values; this is done above, with the caveat that coefficients are on standardised features. The review of the random forest missing-indicator claim asked that the "within one SD of zero" statement be restricted, with BMI_missing as the exception; this is done above.
- No task failed. All eight analyses are complete.

## Open questions

- Do the Insulin and SkinThickness effects hold under an imputation that does not use the Outcome label, such as regression on non-outcome features or multiple imputation that keeps within-class spread?
- Are the Insulin and SkinThickness zeros related to Outcome strongly enough to bias the observed-subset effects?
- Do the Glucose, BMI and DiabetesPedigreeFunction adjusted effects hold after median or model-based imputation of the zeros, rather than dropping 376 rows?
- Do the Age and Pregnancies effects change when the Age × Pregnancies interaction is added to the adjusted model?
- Is the dip at 1 to 2 pregnancies explained by age or other confounders, or does a non-linear Pregnancies term fit better?
- Does the Age pattern (drop at 60+) hold with a larger sample or a bootstrap interval?
- Do the large logistic coefficients on BloodPressure_missing and Insulin_missing reflect real signal, or the shared missingness pattern? Dropping them and refitting would test this.
- Does a recall-tuned threshold or class weighting raise F1 for class 1 without losing too much accuracy?
- Is the test-set gap between the logistic regression and random forest larger than sampling noise? Repeated cross-validation would tell.
- Does the random forest's lower-ranked permutation importance differ from zero on a larger test set?
- Do the Glucose, BMI and Age effect sizes change on the same imputed frame used for Insulin and SkinThickness, so that the feature ranking compares like with like?