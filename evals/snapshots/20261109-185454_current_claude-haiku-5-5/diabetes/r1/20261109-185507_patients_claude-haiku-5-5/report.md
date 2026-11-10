# Diabetes Outcome Analysis: Predictors of Outcome in 768 Patients

## Summary

- **Glucose is the strongest single separator of Outcome.** Its rank-biserial effect is 0.586 (Outcome 1 vs 0, Holm-adjusted Mann-Whitney p about 1e-39), and it is the most important feature in both predictive models. Outcome rate rises from 7.3% in the lowest Glucose quartile to 69.5% in the highest.
- **Every numeric feature differs significantly between Outcome groups after Holm correction, but effect sizes range from small to large.** Insulin, BMI and Age follow Glucose in the rank-biserial ranking. BloodPressure and DiabetesPedigreeFunction are the smallest, at about 0.21 each.
- **Zeros in Insulin, SkinThickness, BloodPressure, BMI and Glucose are treated as implicit missing values.** Insulin (48.7% of rows) and SkinThickness (29.6%) are the most affected. Their effect sizes and ranking depend on how the zeros are handled. Under raw zeros, Insulin is not significant.
- **Gradient boosting (test ROC AUC 0.831) and logistic regression (0.813) both beat the majority-class baseline (accuracy 0.649).** Logistic regression scored 0.708 and gradient boosting 0.760 on test accuracy. Gradient boosting overfits (train accuracy 0.925 vs test 0.760), and the test set has only 154 rows, so the gap between the two models is not established.
- **The Pregnancies x Age interaction is not robust.** It is significant with a linear Age term (p=0.002) but not with a quadratic Age term (p=0.21). Glucose x BMI shows no interaction.

## Data

- 768 rows, 9 columns: 8 numeric features (Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age) and the binary target Outcome. There are no categorical, date or identifier columns.
- Outcome classes: 0 for 500 rows (65.1%) and 1 for 268 rows (34.9%).
- The profile reports no missing values. However, zeros in Glucose (5 rows), BloodPressure (35), SkinThickness (227), Insulin (374) and BMI (11) are physiologically implausible and are treated as missing throughout this report.

## Findings

### Outcome distribution and implicit-missing zeros

Outcome is imbalanced, with 34.9% of rows in class 1.

Rows with any implicit-missing zero number 376 (49%), with an outcome rate of 36.7%, compared with 33.2% for rows with no zero. Zero-versus-nonzero outcome rates by column:

| Column | Zero rows (n) | Outcome rate, zero | Outcome rate, nonzero |
|---|---|---|---|
| Glucose | 5 | 0.40 | 0.349 |
| BloodPressure | 35 | 0.457 | 0.344 |
| SkinThickness | 227 | 0.388 | 0.333 |
| Insulin | 374 | 0.369 | 0.330 |
| BMI | 11 | 0.182 | 0.351 |

The BloodPressure gap of about 11 points is worth testing but is not established. The SkinThickness and Insulin gaps are about 4 to 5 points. The Glucose zero group (n=5) is too small to interpret. The BMI zero rows have a lower outcome rate.

Outcome rate and feature averages across quartile bins:

- **Glucose:** 7.3% (mean 86.9) to 69.5% (mean 164.9).
- **Insulin:** 8.1% (mean 53.6) to 52.6% (mean 314.9).
- **BMI:** 11.4% (mean 24.2) to 48.4% (mean 41.6).
- **Age:** 14.2% (mean 22.3) to 51.7% (mean 51.5).
- **Pregnancies:** 34.2% at 0, 18.4% at 2, and 50.7% at 6 or more (mean 8.36).
- **BloodPressure:** 22.9% (mean 57.8) to 46.7% (mean 88.9).
- **SkinThickness:** 15.3% (mean 16.8) to 45.8% (mean 42.8).
- **DiabetesPedigreeFunction:** 25.5% to 48.4%.

Distributions by Outcome for each numeric feature (zeros excluded):

![Count of rows per value of each numeric feature, split by Outcome (zeros treated as NaN and excluded)](tasks/eda_1/charts/eda1_distributions_by_outcome.png)

Outcome rate per quartile bin of each feature (dashed line = overall rate):

![Share of rows with Outcome=1 per quartile bin of each feature (dashed line = overall rate)](tasks/eda_1/charts/eda1_outcome_rate_by_bin.png)

### Differences between Outcome groups

All eight features differ significantly between Outcome groups after Holm correction. Normality (D'Agostino) was rejected in both groups for every feature, so Mann-Whitney U (MWU) is the primary test and rank-biserial the primary effect size. Welch results are secondary.

Effects on the zero-to-missing sample, ranked by absolute rank-biserial:

| Feature | Rank-biserial | Cohen d | Mean difference (95% Welch CI) | Holm MWU p (approx.) |
|---|---|---|---|---|
| Glucose | 0.586 | 1.19 | 31.7 (27.5 to 35.9) | 1e-39 |
| Insulin* | 0.463 | 0.68 | 76.6 (50.5 to 102.7) | 4e-13 |
| BMI | 0.374 | 0.69 | 4.55 (3.56 to 5.53) | 1e-16 |
| Age | 0.374 | 0.51 | 5.88 years (4.21 to 7.55) | 8e-17 |
| SkinThickness* | 0.325 | 0.57 | 5.76 (3.93 to 7.60) | 3e-9 |
| Pregnancies | 0.239 | 0.48 | 1.57 (1.05 to 2.09) | 1e-7 |
| BloodPressure | 0.215 | 0.36 | 4.44 (2.57 to 6.32) | 2e-6 |
| DiabetesPedigreeFunction | 0.212 | 0.37 | 0.121 (0.069 to 0.173) | 2e-6 |

*Insulin and SkinThickness are estimated on non-zero subsets (Insulin n=264 vs 130, about 49% of rows excluded; SkinThickness n=361 vs 180, about 30% excluded). The effect may not generalise to the full sample. Insulin's Welch p (about 3e-8) is much weaker than its MWU p, possibly because of skewness; this was not checked.

Additional result: for BMI at or above 30 vs below 30, chi-square is 65.1 (p about 7e-16) and the odds ratio of Outcome 1 is 4.06. The table has 241 Outcome 0 and 51 Outcome 1 for BMI below 30, and 250 Outcome 0 and 215 Outcome 1 for BMI at or above 30.

Effect sizes by feature:

![Rank-biserial effect size of each feature for Outcome 1 vs Outcome 0 (zeros treated as missing)](tasks/stat_1/charts/stat1_rank_biserial.png)

### Sensitivity of Insulin and SkinThickness to zero handling

The feature ranking depends on how the zeros are handled. Rank-biserial values for Insulin and SkinThickness:

| Approach | Insulin | SkinThickness |
|---|---|---|
| Complete case (zeros dropped) | 0.463 | 0.325 |
| Median imputation (non-zero median, n=500 vs 268) | 0.312 | 0.257 |
| Group-wise median imputation (uses Outcome) | 0.670 | 0.432 |
| Raw zeros kept as values | 0.076 | 0.107 |

Results for each approach:

- **Complete case:** both features significant. Insulin Holm p 1.5e-13; SkinThickness Holm p 7.0e-10 (Holm across these two features only).
- **Median imputation:** both significant. Insulin Holm p 5.9e-14 (mean difference 36.9, 95% CI 23.1 to 50.7); SkinThickness Holm p 2.3e-9 (mean difference 4.0, 95% CI 2.7 to 5.2).
- **Group-wise median imputation:** both significant (Insulin Holm p 1.7e-54; SkinThickness Holm p 2.9e-23). This approach fills zeros using Outcome, so its larger effects are partly mechanical and should not drive the ranking.
- **Raw zeros kept as values:** Insulin is not significant (Holm p 0.066). SkinThickness is significant (Holm p 0.026) but small.

Feature ranking by absolute rank-biserial under each approach. The other six features keep their complete-case values in every ranking:

- **Complete case:** Glucose, Insulin, BMI, Age, SkinThickness, Pregnancies, BloodPressure, DiabetesPedigreeFunction.
- **Median imputation:** Glucose, BMI, Age, Insulin, SkinThickness, Pregnancies, BloodPressure, DiabetesPedigreeFunction. Insulin falls to fourth.
- **Group-wise median imputation:** Insulin, Glucose, SkinThickness, BMI, Age, Pregnancies, BloodPressure, DiabetesPedigreeFunction.
- **Raw zeros:** Glucose, BMI, Age, Pregnancies, BloodPressure, DiabetesPedigreeFunction, SkinThickness, Insulin.

The Insulin position in the ranking therefore depends on the zero-handling choice.

![Rank-biserial effect size of Insulin and SkinThickness (Outcome 1 vs Outcome 0) under complete-case, median, group-wise median imputation and raw zeros](tasks/stat_3/charts/stat3_rank_biserial_by_approach.png)

### Interactions

Coefficients are from a logistic model on 752 complete cases with centred predictors.

- **Glucose x BMI:** no interaction (LR=0.086, p=0.77).
- **Glucose x Age:** not significant (LR=2.60, p=0.107; odds ratio 0.9995 per unit, 95% CI 0.9990 to 1.0001).
- **Pregnancies x Age:** significant with a linear Age term (LR=9.43, p=0.002; odds ratio 0.992 per centred unit, 95% CI 0.986 to 0.997). The negative sign means the Pregnancies effect weakens as Age rises. This is the only interaction the interaction tests supported.

Base main effects: Glucose odds ratio 1.037 per mg/dL, BMI 1.095 per unit, Pregnancies 1.116 per pregnancy, Age 1.012 per year (its 95% CI includes 1).

Median-split table (Pregnancies 3, Age 29): outcome rate is 20.6% (n=321) for low Pregnancies and young, 50.0% (n=94) for low Pregnancies and older, 28.1% (n=64) for high Pregnancies and young, and 48.7% (n=273) for high Pregnancies and older.

**Disagreement on the Pregnancies x Age interaction.** The linear-Age model gives p=0.002. With a quadratic Age term, the interaction is not significant (LR=1.57, p=0.21; odds ratio 0.996 per centred unit, 95% CI 0.990 to 1.002, n=752). The linear result does not survive the non-linear Age term. The two findings are reported as they stand and are not reconciled here.

Age gap by Pregnancies group (Age cut at 29; low Pregnancies is 3 or fewer, high is more than 3):

- Low Pregnancies: 48.2% for women 29 and older (n=110) vs 19.7% for younger women (n=305). Gap 0.285, SE 0.053.
- High Pregnancies: 49.0% for women 29 and older (n=286) vs 21.6% for younger women (n=51). Gap 0.274, SE 0.065.
- Difference in gaps: 0.011, 95% Wald CI -0.152 to 0.175, z=0.13, p=0.89. The Age gap does not differ between groups beyond chance. The high-Pregnancies younger group has only 51 women, so its gap is imprecise.

Proportion with Outcome=1 in the four Pregnancies x Age cells:

![Proportion with Outcome=1 for four Pregnancies x Age cells (median splits)](tasks/stat_4/charts/stat_4_age_gap_rates.png)

### Predictive models

All models use the stratified 80/20 split (random_state=42): 614 training rows and 154 test rows. Outcome=1 is 34.9% in training and 35.1% in test. Zeros were set to missing. Median imputation was fitted on training data only inside a pipeline. Training medians: Glucose 117, Insulin 125, SkinThickness 29, BMI 32.4, Age 29.

Test-set scores (154 rows):

| Model | Accuracy | ROC AUC | Precision | Recall | F1 |
|---|---|---|---|---|---|
| Majority class (always Outcome=0) | 0.649 | 0.500 | 0.0 | 0.0 | 0.0 |
| Logistic regression | 0.708 | 0.813 | 0.600 | 0.500 | 0.545 |
| Gradient boosting | 0.760 | 0.831 | 0.689 | 0.574 | 0.626 |

- Both models have higher test accuracy than the majority-class baseline (0.649). On 154 rows the logistic regression improvement is small relative to sampling error, so it is real in direction but not precisely estimated. ROC AUC is the more stable comparison.
- Gradient boosting has a train accuracy of 0.925 against test accuracy of 0.760, so its test scores are optimistic. The gap between the two models is small relative to sampling error and does not clearly establish that one is stronger.

Permutation importance on test ROC AUC drop (mean ± sd):

| Feature | Logistic regression | Gradient boosting |
|---|---|---|
| Glucose | 0.168 ± 0.029 | 0.101 ± 0.025 |
| BMI | 0.031 ± 0.014 | 0.060 ± 0.020 |
| Age | 0.004 ± 0.004 | 0.033 ± 0.009 |
| Pregnancies | 0.028 ± 0.011 | not reported (see Limitations) |
| DiabetesPedigreeFunction | 0.009 ± 0.006 | 0.016 ± 0.013 |
| Insulin | 0.001 ± 0.002 | 0.012 ± 0.009 |
| BloodPressure | 0.001 ± 0.001 | -0.002 ± 0.004 |
| SkinThickness | 0.000 ± 0.001 | 0.001 ± 0.003 |

Glucose is the most important feature in both models. BMI is second in both by rank, but its importance is much larger for gradient boosting (0.060) than for logistic regression (0.031). For gradient boosting, the Insulin importance (0.012 ± 0.009) is indistinguishable from zero on this test split. Its value may be affected by median imputation of Insulin, which has many zeros.

![Test-set accuracy and ROC AUC for the majority baseline, logistic regression and gradient boosting](tasks/ml_2/charts/ml2_model_comparison.png)

## Limitations

- **Implicit missing values.** Zeros in five columns are physiologically implausible and were treated as missing, though the profile reports none. Insulin (49% of rows) and SkinThickness (30%) are too heavily affected to drop casually. Their effect sizes, the feature ranking and Insulin's significance all depend on the zero-handling approach (see Sensitivity). Median imputation shrinks the effects. Raw zeros make Insulin non-significant. Group-wise imputation uses Outcome and is not a valid basis for the ranking.
- **Complete-case samples.** Several effect sizes (Insulin, SkinThickness) and the interaction models (752 complete cases) use reduced samples. Results may not generalise to the full sample.
- **Non-normality.** Normality was rejected in both groups for every feature. Welch results and mean-difference CIs assume approximate normality and are secondary. Insulin's Welch p is much weaker than its MWU p; skewness was not checked.
- **Pregnancies x Age interaction.** The linear-Age result (p=0.002) is not robust to a quadratic Age term (p=0.21). The interaction should not be treated as established.
- **Small high-Pregnancies younger group.** The Age-gap comparison by Pregnancies group rests on 51 younger women in the high-Pregnancies group, so the high-group gap is imprecise.
- **BloodPressure zero rows.** The 0.457 vs 0.344 outcome gap on 35 rows is not established. Zero-indicator flags were not created or tested, so it is unknown whether missingness carries outcome signal for BloodPressure, Insulin or SkinThickness.
- **Test-set size.** The test split has 154 rows. Model differences are small relative to sampling error. Gradient boosting overfits.
- **Unresolved review issue (ml_2): missing importance.** The gradient-boosting permutation importance for Pregnancies is not reported in the accepted findings. The lead's objection stands. Pregnancies is therefore missing from the gradient-boosting importance comparison above.
- **Unresolved review issue (ml_2): Insulin wording.** The gradient-boosting Insulin importance (0.012 ± 0.009) is only about 1.2 standard deviations from zero. It is indistinguishable from zero on this test split and should not be described as larger than noise.
- **No failed tasks.** All five analysis tasks (eda_1, stat_1, stat_2, stat_3, stat_4) and the two modelling tasks (ml_1, ml_2) completed.

## Open questions

- Does imputing Insulin and SkinThickness with training medians bias model performance compared with dropping them or adding missingness flags?
- Is missingness itself informative? Do the zero-indicator flags carry outcome signal beyond the imputed values, for BloodPressure (0.457 vs 0.344 on 35 rows), Insulin and SkinThickness?
- Do the Insulin and SkinThickness effects hold under model-based or multiple imputation that uses other covariates, rather than a single median?
- Is the Insulin Welch CI sensitive to skewness, given how much weaker its Welch p is than its MWU p?
- Is the Pregnancies x Age interaction explained by curvature in Age? A spline Age term and residual diagnostics were suggested but not run.
- Does Glucose x Age become significant with a non-linear Age term or with more data?
- Would tuning gradient boosting (depth, learning rate, regularisation) reduce its train-test accuracy gap?
- Would repeated cross-validation on the training split give more stable estimates of the model differences than the 154-row test split?
- Would a different Age cut, or more data, change the Age-gap comparison by Pregnancies group?