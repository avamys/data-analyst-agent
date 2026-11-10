# Diabetes Screening Dataset (768 rows): Predictors of Binary Outcome

## Summary

- **Outcome is imbalanced and has implicit missing values.** 268 of 768 rows (34.9%) are positive. Zeros in Insulin (374 rows), SkinThickness (227), BloodPressure (35), BMI (11) and Glucose (5) are physiologically impossible and were treated as missing.
- **Glucose is the strongest single feature.** Outcome rates rise from 8.1% in the lowest quartile to 68.8% in the highest, with Cohen d 1.19. Glucose is also the top permutation-importance feature in the gradient boosting model.
- **Gradient boosting beats the majority baseline clearly; logistic regression only suggestively.** Gradient boosting reaches 76.0% test accuracy against 64.9% for the baseline, with ROC AUC 0.831. Logistic regression reaches 70.8% on the same single 154-row split, a gain the team describes as suggestive rather than clear.
- **Feature interactions are weak.** A joint test of three pairwise interaction terms gives p = 0.13. The only term near significance, Glucose x Age, has p = 0.049 and would not survive correction.
- **Zero-Insulin status is not missing completely at random.** It is associated with Age, Pregnancies and BMI. Its adjusted association with Outcome is small and not detected (OR 1.121, 95% CI 0.801 to 1.568).

## Data

- **Size:** 768 rows × 9 columns (8 numeric features, 1 binary target). No categorical, date/time, id or free-text columns.
- **Target:** Outcome, 0 for 65.1% and 1 for 34.9% of rows.
- **Missing values:** None declared. Zeros in Glucose, BloodPressure, SkinThickness, Insulin and BMI were treated as implicit missing values, with counts of 5, 35, 227, 374 and 11 respectively.

## Findings

### Implicit missing values

- Zeros are common. Insulin has 374 zeros (about 49% of rows), SkinThickness 227, BloodPressure 35, BMI 11 and Glucose 5.
- Zero-Glucose (n=5) and zero-BMI (n=11) groups are too small for firm conclusions. Their rates and medians are descriptive only.
- Outcome rates for zero versus non-zero rows: Glucose 40.0% (n=5) vs 34.9%; BloodPressure 45.7% (n=35) vs 34.4%; SkinThickness 38.8% (n=227) vs 33.3%; Insulin 36.9% (n=374) vs 33.0%; BMI 18.2% (n=11) vs 35.1%.
- Medians of other features differ between zero and non-zero rows (see the missingness section below for the tested comparisons on Insulin and SkinThickness).

### Outcome rates across features

- **Glucose** has the steepest gradient. Rates by quartile are 8.1% (≤99, n=197), 24.7% (99–117, n=194), 38.9% (117–140, n=185) and 68.8% (140–199, n=192).
- **BMI** rises across quartiles: 10.3% (≤27.3), 35.9% (27.3–32.0), 45.4% (32.0–36.6) and 48.4% (36.6–67.1). By clinical bins with zero BMI excluded: 6.5% (18.5–25, n=108), 24.4% (25–30, n=180), 45.3% (30–35, n=221) and 47.1% (above 35, n=244). A BMI bin of (0, 18.5] has n=4 and a 0.0% rate; it is too small to interpret.
- **Age** rates by bin: 21.6% (20–30, n=417), 48.4% (30–40, n=157), 56.6% (40–50, n=113), 57.4% (50–60, n=54) and 25.9% (60–90, n=27). The rate rises to about age 50 and then falls. The 60–90 bin is small.

  ![Share of Outcome=1 by Age bin and by BMI bin (BMI zeros excluded)](tasks/eda_1/charts/outcome_rate_by_age_bmi.png)

- **Pregnancies** quartile rates are 27.2% (0–1, n=246), 25.8% (1–3, n=178), 34.3% (3–6, n=175) and 56.2% (6–17, n=169). The rate is not strictly monotone: it dips between the first two bins.
- **DiabetesPedigreeFunction** quartile rates are 25.5% (≤0.244), 33.3% (0.244–0.372), 32.3% (0.372–0.626) and 48.4% (0.626–2.42). The rate is not strictly monotone: it dips between the second and third bins.
- **BloodPressure** quartile rates are 25.4% (≤62), 33.6% (62–72), 35.9% (72–80) and 46.7% (80–122).
- **SkinThickness** quartile rates are 28.8% (≤23), 35.9% (23–32) and 46.8% (32–99).
- **Insulin** is non-monotone. Rates are 36.5% (≤30.5, n=384), 16.1% (30.5–127.25, n=192) and 50.5% (127.25–846, n=192). The lowest bin contains 374 zero values out of 384 rows, so its rate mainly reflects the zero-Insulin group rather than a quartile of measured values.

### Group differences and effect sizes

All eight numeric features differ significantly between Outcome=0 and Outcome=1 (Mann-Whitney tests, Holm-corrected across eight tests). All adjusted p-values are below 0.001. Six are below 1e-6, and the largest adjusted p is 2.39e-06 (BloodPressure and DiabetesPedigreeFunction). Zeros were dropped per feature, so n varies. Pregnancies, DiabetesPedigreeFunction and Age use n=500 vs 268.

| Feature | Mean (Outcome 0 vs 1) | Median | Cohen d | Rank-biserial |
|---|---|---|---|---|
| Glucose | 110.6 vs 142.3 | 107 vs 140 | 1.19 | 0.59 |
| BMI | 30.9 vs 35.4 | 30.1 vs 34.3 | 0.69 | 0.37 |
| Insulin (non-zero rows) | 130.3 vs 206.8 | 102.5 vs 169.5 | 0.68 | 0.46 |
| SkinThickness | 27.2 vs 33.0 | 27 vs 32 | 0.57 | 0.33 |
| Age | 31.2 vs 37.1 | 27 vs 36 | 0.51 | 0.37 |
| Pregnancies | 3.3 vs 4.9 | 2 vs 4 | 0.48 | 0.24 |
| DiabetesPedigreeFunction | 0.430 vs 0.551 | 0.336 vs 0.449 | 0.37 | 0.21 |
| BloodPressure | 70.9 vs 75.3 | 70 vs 74.5 | 0.36 | 0.22 |

- Glucose mean difference is 31.7 (95% CI 27.5 to 35.9). BMI mean difference is 4.5 (95% CI 3.6 to 5.5). Age mean difference is 5.9 (95% CI 4.2 to 7.5).
- The Insulin comparison uses only recorded (non-zero) measurements and describes only those rows.
- The Age mean difference is a summary of the shift in distribution. The Outcome rate peaks around ages 40–60 and falls after 60, so the difference should not be read as a monotone trend.
- The Pregnancies and DiabetesPedigreeFunction effects are shifts in distribution, not strict monotone trends.
- Ordering by rank-biserial differs from Cohen d, mainly for Insulin, which ranks second on rank-biserial but third on Cohen d.

  ![Cohen d by feature for Outcome=1 vs Outcome=0; zeros in Glucose, BloodPressure, SkinThickness, Insulin, BMI treated as missing; all Holm-adjusted p < 0.001](tasks/stat_1/charts/stat_effect_sizes.png)

### Interactions

- A likelihood-ratio test of the three pairwise interaction terms (Glucose x BMI, Glucose x Age, BMI x Age) against the main-effects logit gives chi2 = 5.62 on 3 df, p = 0.13 (n=752; zero Glucose and BMI excluded). The evidence for any interaction is weak.
- Glucose x Age has coefficient -0.000563 per unit, OR 0.9994 (95% CI 0.9989 to 1.0000), p = 0.049. It would not survive correction for three tests (about p = 0.15). The direction is that the Glucose effect weakens with age.
- Glucose x BMI: OR 0.9997 (95% CI 0.9986 to 1.0008), p = 0.56. BMI x Age: OR 1.0015 (95% CI 0.9991 to 1.0039), p = 0.22.
- Descriptive Glucose gradients by Age group are not a monotone weakening. The low-to-mid tertile difference is about 12 points at ages 21–30 (6.0% to 18.3%, n=166 and 142), about 27 points at ages 31–45 (22.2% to 49.4%, n=63 and 79) and about 11 points at ages 46–90 (25.0% to 35.7%, n=24 and 28). The 46–90 cells are small, so their gradients are imprecise.
- Glucose gradients are similar across BMI groups: low-to-mid differences of about 16 points (BMI ≤30), 21 points (BMI 30–35) and 15 points (BMI above 35).

  ![Share of Outcome=1 by Glucose tertile, for Age groups (left) and BMI groups (right); zero Glucose and BMI excluded](tasks/stat_2/charts/stat2_glucose_x_age_bmi.png)

### Predictive models

- **Majority-class baseline** (predict 0 for all 154 test rows): 64.9% test accuracy (100 of 154). ROC AUC 0.5, F1 for class 1 is 0.
- **Gradient boosting:** test accuracy 76.0% (0.7597), a gain of 11.0 points over the baseline (17 more correct rows). ROC AUC 0.831, F1 for class 1 0.626. Confusion matrix [[86,14],[23,31]]: 31 of 54 positives caught (recall 57.4%), precision 68.9%. Train accuracy 92.5%.
- **Logistic regression:** test accuracy 70.8% (0.7078), a gain of 5.8 points over the baseline (109 vs 100 correct rows). ROC AUC 0.813, F1 for class 1 0.545. Confusion matrix [[82,18],[27,27]]. Train accuracy 79.6%.
- On the test split, gradient boosting compares with logistic regression as follows: accuracy 76.0% vs 70.8%, ROC AUC 0.831 vs 0.813, F1 for class 1 0.626 vs 0.545.
- The gradient boosting gain over the baseline is clear. The logistic regression gain is modest and suggestive on one 154-row split, with wide uncertainty.
- The advantage of gradient boosting over logistic regression is optimistic and not an unbiased estimate, because the model was chosen by comparing scores on the same test set. With one split the gap is small and not conclusive.
- Gradient boosting fits the training set much better than the test set (92.5% vs 76.0%), which points to overfitting.

  ![Test-set accuracy and F1 for class 1 (n=154) for the majority-class baseline, logistic regression and gradient boosting. Baseline F1 is 0 because it never predicts class 1.](tasks/ml_1/charts/ml_1_model_comparison.png)

### Feature importance

- **Permutation importance** (gradient boosting, test split, accuracy drop, 30 repeats): Glucose 0.063 (SD 0.021), Age 0.042 (SD 0.014), BMI 0.037 (SD 0.024), DiabetesPedigreeFunction 0.024 (SD 0.023), Insulin 0.022 (SD 0.016), Pregnancies 0.021 (SD 0.012), SkinThickness 0.003 (SD 0.009), BloodPressure 0.002 (SD 0.010).
- Glucose is about 1.5 times the next feature, Age. The gap of 0.021 is about the size of Glucose's own SD, so the lead over Age is suggestive rather than secure. The order of Age and BMI is not reliable on 154 test rows.
- SkinThickness and BloodPressure add almost nothing to accuracy in this model.
- **Standardised logistic regression coefficients:** Glucose +1.18, BMI +0.69, Pregnancies +0.38, DiabetesPedigreeFunction +0.23, Age +0.15, SkinThickness +0.03, Insulin -0.07, BloodPressure -0.04. The negative Insulin and BloodPressure signs are small and may reflect correlation among features or median imputation. They should not be read as clinical effects.
- Glucose and BMI are the two largest logistic coefficients, which agrees with their high permutation ranks. Age has a small logistic coefficient but ranks second in permutation importance, so the two methods disagree on its strength.
- Permutation importance is measured on the test split of an overfit model, so the ranking may also reflect that overfit.

  ![Permutation importance of each feature for the gradient boosting model on the 154-row test split; bars show mean accuracy drop, whiskers show SD over 30 shuffles.](tasks/ml_2/charts/ml_2_permutation_importance.png)

### Missingness of zero-Insulin and zero-SkinThickness rows

- **Outcome association (unadjusted):** zero-Insulin rows have an Outcome rate of 36.9% (Wilson 95% CI 32.2% to 41.9%) vs 33.0% for non-zero rows; chi-square p = 0.26, phi = 0.04. Zero-SkinThickness rows have 38.8% (95% CI 32.7% to 45.2%) vs 33.3%; chi-square p = 0.14, phi = 0.05. No detectable association was found, but a non-significant test does not establish independence at these group sizes.

  ![Share of Outcome=1 for rows with a zero versus non-zero Insulin or SkinThickness value](tasks/stat_3/charts/stat3_outcome_rate_zero_vs_nonzero.png)

- **Other columns (unadjusted):** zero-Insulin rows have median Age 32 vs 27 (p < 0.001, rank-biserial -0.23), median Pregnancies 4 vs 2 (p < 0.001, rank-biserial -0.20) and median BMI 31.2 vs 33.2 (p = 0.001, rank-biserial +0.14). Zero-SkinThickness rows have median Age 34 vs 28 (p < 0.001, rank-biserial -0.28), median Pregnancies 4 vs 2 (p < 0.001, rank-biserial -0.21) and median BMI 30.4 vs 32.8 (p < 0.001, rank-biserial +0.17). Negative rank-biserial means the zero group is higher.
- **Adjusted logistic regression** (zero-Insulin indicator on Age, Pregnancies, BMI and Outcome; all 768 rows; 374 zero-Insulin): Age OR 1.032 per year (95% CI 1.016 to 1.049, p < 0.001); BMI OR 0.960 per unit (95% CI 0.941 to 0.980, p < 0.001); Pregnancies OR 1.046 (95% CI 0.992 to 1.103, p = 0.096); Outcome OR 1.121 (95% CI 0.801 to 1.568, p = 0.505). McFadden pseudo R2 is 0.051.
- With the 11 zero-BMI rows excluded (n=757, 364 zero-Insulin), BMI OR is 0.968 per unit (95% CI 0.946 to 0.990, p = 0.005), Age OR 1.033 (95% CI 1.016 to 1.049, p < 0.001), Pregnancies OR 1.044 (95% CI 0.990 to 1.101), Outcome OR 1.090 (95% CI 0.778 to 1.528). Pseudo R2 is 0.045. The excluded-zero estimate is the one to cite for BMI.
- The zero-Insulin missingness is not missing completely at random. After adjustment, Age and BMI remain clearly associated with it, while Pregnancies is weak. Whether the data are missing at random given the observed columns cannot be confirmed or ruled out.
- Age, Pregnancies and BMI are the columns associated with zero-Insulin missingness. Outcome should be included in any imputation model, because Insulin is strongly associated with Outcome (see the group differences above); omitting Outcome would bias the Insulin-Outcome relationship. A sensitivity check on Pregnancies is advisable, because its unadjusted difference is strong (p < 0.001) while its adjusted association is not significant (p = 0.096).

## Limitations

- **Implicit missing values.** Zeros were treated as missing. Insulin is about 49% zeros, so Insulin-based results (including the Insulin comparison and model importance) depend heavily on this choice. Imputation has not been tested; the models used median imputation, and sensitivity to this is untested.
- **Small groups.** The zero-Glucose group (n=5) and zero-BMI group (n=11) are too small for firm conclusions. The BMI bin (0, 18.5] has n=4 and is too small to interpret; it is reported only for completeness.
- **Non-monotone patterns.** Pregnancies and DiabetesPedigreeFunction rates are not strictly monotone across quartiles. Age rates fall after about 50, with the 60–90 bin at n=27. Insulin's lowest bin is almost entirely zeros (374 of 384 rows), so its rate reflects the zero-Insulin group rather than a quartile.
- **Interactions.** Glucose x Age (p = 0.049) is borderline and not significant after correction. The Glucose x Age subgroup cells for ages 46–90 are small.
- **Model evaluation.** All model scores come from one stratified 80/20 split with 154 test rows. The gradient boosting vs logistic regression comparison used the same test set for selection and is optimistic. Gradient boosting shows an overfitting gap (92.5% train vs 76.0% test). The logistic regression gain over the baseline (+5.8 points) is suggestive, not clear.
- **Feature importance.** Based on the same single test split. The Age vs BMI order is not reliable. Negative Insulin and BloodPressure logistic coefficients may reflect collinearity or imputation and are not interpreted as effects.
- **Missingness.** The zero-Insulin and zero-SkinThickness tests are cross-sectional and do not establish independence. The adjusted Outcome estimate has a wide confidence interval that includes meaningful effects in both directions.
- **Unresolved review issues (lead objections still standing):**
  - *eda_1:* The Pregnancies and DiabetesPedigreeFunction statements were to be reworded so they do not claim a monotone rise; this report describes them as not strictly monotone. The Insulin lowest-bin caveat (374 of 384 zeros) and the BMI (0, 18.5] bin (n=4, 0.0%) note are included above.
  - *ml_1:* The logistic regression gain is corrected to +5.8 points (109 vs 100 correct rows). The claim that both models clearly beat the baseline has been softened: gradient boosting's gain is clear; logistic regression's is suggestive on a single split. The gradient boosting overfitting statement is kept.
  - *stat_4:* The claim that Outcome is not needed as a conditioning variable for imputation has been removed. Outcome should be included in any imputation model for the reason given above, and the Pregnancies sensitivity check is still advisable. The BMI and Outcome confidence intervals quoted above are the full-precision values.
- **Failed tasks:** None reported.

## Open questions

- Is the zero-Insulin pattern missing at random after controlling for Age, Pregnancies, BMI and Glucose and BloodPressure, which may also relate to missingness?
- How sensitive are imputed Insulin values to including or dropping Pregnancies as a conditioning variable, and to missing-indicator features?
- Does zero-Insulin status relate to Outcome within age strata, given the small adjusted Outcome effect?
- Does the lower Outcome rate for zero-BMI rows persist after adjusting for Age and Glucose, given the group size of 11?
- Is the Glucose x Age interaction (p = 0.049) stable under a bootstrap or a model with age splines, given that the Age effect is non-monotone?
- Do Age and BMI interact in their effect on Outcome, given the Age rate falls after 60?
- Does the Glucose effect depend on Insulin or SkinThickness, given that zero-value patterns in those columns may be non-random?
- Does the model comparison hold under stratified cross-validation over all 768 rows, with model selection inside the folds? Does the feature ranking hold after tuning gradient boosting regularisation to reduce the train/test gap?
- Do the Insulin, SkinThickness and BMI differences hold after adjusting for Age and Glucose, for example in a logistic regression of Outcome?