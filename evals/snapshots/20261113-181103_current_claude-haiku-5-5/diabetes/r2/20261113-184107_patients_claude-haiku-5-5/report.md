# Pima Diabetes Dataset: Predictors of the Binary Outcome, with Zero-as-Missing Checks

## Summary

- **Glucose is the strongest single correlate of Outcome.** The outcome rate rises from 8.1% in the lowest Glucose quartile to 68.8% in the top quartile. Glucose has the largest group difference (Cohen's d 1.11) and the largest joint logistic odds ratio per SD (3.08, 95% CI 2.44 to 3.88). BMI is second (OR per SD 2.03). Age's association is not significant after adjustment for the other features.
- **Five columns contain physiologically impossible zeros, most heavily Insulin (48.7% of rows) and SkinThickness (29.6%).** For Insulin and SkinThickness, zero rows show no detected association with Outcome, either unadjusted or adjusted for Age and Pregnancies. This is absence of detection, not evidence of absence, and the Glucose and BMI tests have very low power.
- **The Glucose × Age interaction is significant on the logit scale (p=0.006), while the Glucose × BMI interaction is not (p=0.51).** The Age interaction p-value is not adjusted for the two interaction tests.
- **Both predictive models beat the majority-class baseline (0.649 test accuracy).** Logistic regression reaches 0.708 and the random forest 0.734. Test ROC AUC is 0.813 and 0.816, respectively, on a single 154-row test set.
- **The non-monotonic Pregnancies pattern is partly explained by Age composition, but this is only partly resolved.** The 1-2 pregnancies group has a lower outcome rate in the two younger age bands. The within-band evidence for the older bands rests on small cells and is flagged as unresolved.

## Data

- 768 rows, 9 columns (8 numeric features, 1 binary target). No categorical, date/time, identifier or free-text features.
- Target Outcome: 500 patients (65.1%) with Outcome 0 and 268 (34.9%) with Outcome 1.
- Missing values: none recorded in the profile. However, the analysis treats zeros in Glucose, BloodPressure, SkinThickness, Insulin and BMI as disguised missing values. Zero counts are: Insulin 374 (48.7%), SkinThickness 227 (29.6%), BloodPressure 35 (4.6%), BMI 11 (1.4%), Glucose 5 (0.7%). In total, 376 rows have at least one zero in these five columns.

## Findings

### Outcome distribution and rates by feature

The outcome rate varies strongly across Glucose and BMI groups, and more modestly across Age and Pregnancies.

- **Glucose:** Outcome rates are 8.1% (≤99, n=197), 24.7% (99-117, n=194), 38.9% (117-140, n=185) and 68.8% (>140, n=192).
- **BMI:** Rates are 10.3% (≤27.3), 35.9% (27.3-32.0), 45.4% (32.0-36.6) and 48.4% (>36.6). The gain is concentrated below BMI 32 and flattens above it.
- **Age:** Rates are 14.2% (21-24), 29.9% (25-29), 47.5% (30-41) and 51.7% (42-81).
- **Pregnancies:** Rates are 34.2% (0, n=111), 20.2% (1-2, n=238), 35.5% (3-5, n=200) and 50.7% (6+, n=219). The pattern is not monotonic.

Per-outcome means for diabetic (Outcome 1) versus non-diabetic (Outcome 0) patients: Glucose 141.3 vs 110.0, BMI 35.1 vs 30.3, Age 37.1 vs 31.2, Pregnancies 4.9 vs 3.3. BloodPressure and SkinThickness differ less. Medians follow the same direction.

![Histograms of patient counts by Glucose, BMI, Age and Pregnancies, split by Outcome](tasks/eda_1/charts/key_feature_histograms.png)

![Share of patients with Outcome=1 in each Glucose, BMI, Age and Pregnancies group](tasks/eda_1/charts/outcome_rate_by_group.png)

### Zero values and their relation to Outcome

**Prevalence.** Insulin and SkinThickness have many zeros. BloodPressure, BMI and Glucose have few.

**Outcome rate, zero vs non-zero rows (unadjusted):**

| Column | Zero rows (n) | Outcome rate, zero | Outcome rate, non-zero | Test | p |
|---|---|---|---|---|---|
| Glucose | 5 | 40.0% | 34.9% | Fisher exact (OR 1.25) | 1.0 |
| BloodPressure | 35 | 45.7% | 34.4% | Chi-square | 0.23 |
| SkinThickness | 227 | 38.8% | 33.3% | Chi-square | 0.17 |
| Insulin | 374 | 36.9% | 33.0% | Chi-square | 0.29 |
| BMI | 11 | 18.2% | 35.1% | Fisher exact (OR 0.41) | 0.35 |

No association with Outcome was detected in any of the five columns. The Glucose test has only 5 zero rows and the BMI test has only 11, so both have very low power. The BMI zero-row outcome rate (18.2%) against 35.1% for non-zero rows is a large difference that is not statistically resolved.

**Zero rows and Age/Pregnancies.** Zero rows in SkinThickness and Insulin are associated with higher Age and Pregnancies:
- SkinThickness zeros: mean Age 37.3 vs 31.6 (p=1.5e-8); mean Pregnancies 4.6 vs 3.5 (p=2.5e-5).
- Insulin zeros: mean Age 35.8 vs 30.8 (p=3.8e-9); mean Pregnancies 4.4 vs 3.3 (p=2e-6).

This is an association, not a cause. For Glucose, BloodPressure and BMI, zero and non-zero rows do not differ in Age or Pregnancies (all p>0.1).

**Adjusted zero-row association (Insulin and SkinThickness).** Logistic regression of Outcome on the zero indicator, adjusted for Age and Pregnancies:
- Insulin zeros: adjusted OR 0.927 (95% CI 0.675 to 1.271), p=0.64.
- SkinThickness zeros: adjusted OR 0.985 (95% CI 0.700 to 1.385), p=0.93.

Both intervals include 1 and are wide, so they do not exclude moderate effects in either direction. No power calculation was run.

![Outcome rate (share with Outcome=1) for rows with a zero versus a non-zero value, per column](tasks/eda_2/charts/zero_outcome_rate.png)

![Adjusted odds ratio (95% CI) of Outcome for zero vs non-zero Insulin and SkinThickness, adjusted for Age and Pregnancies; reference line at OR=1](tasks/stat_3/charts/stat3_adjusted_or.png)

### Features that differ between Outcome groups

**Effect sizes and joint logistic models** (joint model = all features together, OR per SD):

- **Glucose:** Cohen's d 1.11 (95% CI 0.95 to 1.26). Welch and Mann-Whitney p < 1e-6. Bonferroni significant. Joint OR 3.08 (95% CI 2.44 to 3.88).
- **BMI:** Cohen's d 0.64 (95% CI 0.49 to 0.79). Bonferroni significant. Joint OR 2.03 (95% CI 1.61 to 2.56).
- **Age:** Cohen's d 0.51 (95% CI 0.36 to 0.66). Bonferroni significant univariately. Joint OR 1.19 (95% CI 0.96 to 1.48), p=0.11, so not significant after adjustment for the other features.
- **Pregnancies:** Cohen's d 0.48 (95% CI 0.33 to 0.63). Bonferroni significant. Joint OR 1.51 (95% CI 1.23 to 1.87), p=0.0001.
- **DiabetesPedigreeFunction:** Cohen's d 0.37 (95% CI 0.22 to 0.52). Bonferroni significant. Joint OR 1.37 (95% CI 1.13 to 1.66), p=0.002.
- **Insulin:** Welch test Bonferroni significant (mean 68.8 vs 100.3, d 0.28, 95% CI 0.13 to 0.42). The full-data Mann-Whitney p is 0.066, not significant, because zeros dominate the column. After dropping zeros (n=394), the Mann-Whitney p is 7.5e-14. Joint OR 0.87 (95% CI 0.71 to 1.07), not significant.
- **SkinThickness:** d 0.16 (95% CI 0.01 to 0.31), Welch p 0.049, not Bonferroni significant. Joint OR 1.01 (95% CI 0.81 to 1.25).
- **BloodPressure:** d 0.14 (95% CI -0.01 to 0.29). Welch p 0.087 (not significant), but Mann-Whitney p 7.6e-5 (Bonferroni-adjusted about 6e-4, significant). Joint OR 0.77 (95% CI 0.63 to 0.94), which points opposite to its raw difference.

The two tests disagree for BloodPressure, and the joint-model direction disagrees with the raw difference. Both are reported as found. The reversal is unexplained; confounding or collinearity was not tested.

Sensitivity analysis after dropping zero values (Welch p-values): Glucose 2.8e-41, BloodPressure 4.0e-6, SkinThickness 1.8e-9, Insulin 2.7e-8, BMI 2.5e-18.

![Cohen d with 95% CI for each feature, Outcome 1 vs Outcome 0](tasks/stat_1/charts/stat1_cohens_d.png)

### Interactions

- **Glucose × BMI:** Not significant on the logit scale (coefficient -0.074 per SD×SD, p=0.51, OR 0.93, 95% CI 0.74 to 1.16, n=752). The data do not show that Glucose changes how BMI relates to Outcome on the logit scale. In the split by median Glucose (117) and median BMI (32.3), outcome rates are 10.8% (low Glucose, low BMI), 23.7% (low Glucose, high BMI), 42.6% (high Glucose, low BMI) and 62.6% (high Glucose, high BMI). The BMI gap is larger at high Glucose, but the logistic test is non-significant, so the split does not establish an interaction.
- **Glucose × Age:** Significant on the logit scale (coefficient -0.259 per SD×SD, p=0.006, OR 0.77, 95% CI 0.64 to 0.93, n=752). The positive Age slope is weaker at higher Glucose. The 2x2 split by median Glucose (117) and median Age (29) gives rates of 8.2% (low Glucose, young), 28.8% (low Glucose, older), 42.5% (high Glucose, young) and 62.4% (high Glucose, older). The split rates alone do not show the interaction; the judgement rests on the logistic model. The p-value is not adjusted for the two interaction tests.

### Predictive models

Setup: stratified 80/20 split (random_state 42; 614 training, 154 test rows). Zeros in the five columns were treated as missing and imputed with the training median, not dropped.

| Model | Test accuracy | Precision | Recall | F1 | ROC AUC | Train accuracy |
|---|---|---|---|---|---|---|
| Majority-class baseline | 0.649 | – | – | – | – | – |
| Logistic regression | 0.708 | 0.600 | 0.500 | 0.545 | 0.813 | 0.796 |
| Random forest (500 trees) | 0.734 | 0.644 | 0.537 | 0.586 | 0.816 | 1.000 |

Both models beat the baseline. The random forest is slightly ahead on accuracy and F1, but the AUC difference is negligible. The random forest's training accuracy of 1.0 against 0.734 on test indicates overfitting, so only its test metrics are a fair comparison. The 154-row test set carries substantial sampling error.

**Feature importance.**
- Logistic regression (standardised absolute coefficients): Glucose 1.18, BMI 0.69, Pregnancies 0.38, DiabetesPedigreeFunction 0.23, Age 0.15, Insulin 0.07, BloodPressure 0.04, SkinThickness 0.03.
- Random forest permutation importance (drop in test ROC AUC, 20 repeats): Glucose 0.099 (sd 0.022), BMI 0.047 (sd 0.018), Age 0.027 (sd 0.011), Insulin 0.011, DiabetesPedigreeFunction 0.007, Pregnancies 0.007, BloodPressure 0.003, SkinThickness -0.001 (no measurable contribution).

![Random forest permutation importance on the test set, ranked by drop in ROC AUC](tasks/ml_1/charts/ml_1_permutation_importance.png)

### Pregnancies pattern within Age bands (partial)

Outcome rate by Pregnancies group within each Age band (age bands from quartiles; n in parentheses):

| Age band | 0 | 1-2 | 3-5 | 6+ |
|---|---|---|---|---|
| 21-24 | 23.6% (n=55) | 7.3% (n=123) | 21.6% (n=37) | 25.0% (n=4) |
| 25-29 | 40.6% (n=32) | 20.3% (n=69) | 36.1% (n=61) | 26.7% (n=15) |
| 30-41 | 71.4% (n=14) | 50.0% (n=26) | 36.6% (n=71) | 51.7% (n=89) |
| 42-81 | 20.0% (n=10) | 60.0% (n=20) | 48.4% (n=31) | 54.1% (n=111) |

Within the two youngest bands, the 1-2 group's rate is below the average of the 0 and 3-5 groups by 15.3 points (21-24) and 18.1 points (25-29). In the 30-41 band the gap is 4.0 points, and in the 42-81 band the 1-2 group is higher by 25.8 points. The 0-group cells in the two oldest bands contain only 14 and 10 patients, so their rates are unstable.

Composition: the crude 1-2 rate is 20.2%, while the age-standardised 1-2 rate is 33.2%. The 1-2 group is 51.7% in the youngest band, against 28.5% of all patients. On this basis, age composition accounts for most of the overall 1-2 dip, though the standardised figure rests on small older-band 1-2 cells (n=20 to 26).

![Outcome rate by Pregnancies group (0, 1-2, 3-5, 6+) within each Age quartile band; n = patients in each cell](tasks/eda_3/charts/eda3_rate_by_preg_within_age.png)

## Limitations

- **Zeros are treated as missing, which is an assumption.** The data alone cannot prove missingness. Zeros in Glucose, BloodPressure and BMI are physiologically implausible, and the zeros concentrate in Insulin and SkinThickness, which supports but does not establish the disguised-missing interpretation.
- **Outcome relation of zeros (eda_2, review issue applied).** The result is "no association detected" for all five columns, not evidence that zeros carry no outcome information. The Glucose test (5 zero rows) and BMI test (11 zero rows) have very low power. The BMI zero-row outcome rate of 18.2% vs 35.1% is a large difference that is not statistically resolved (Fisher p=0.35). Fisher's exact test is used for Glucose and BMI because chi-square expected counts are below 5.
- **Adjusted zero-row results (stat_3).** The no-association results for Insulin and SkinThickness rest on confidence intervals that include 1 and are wide. No power calculation was run. The odds-ratio intervals are on the odds-ratio scale: Insulin 0.675 to 1.271 and SkinThickness 0.700 to 1.385.
- **Insulin zeros affect 48.7% of rows.** Whether to impute, drop or flag them was not settled. The model results use median imputation, and the effect of this choice was not tested.
- **BloodPressure disagreement (stat_1).** Welch and Mann-Whitney tests disagree (p=0.087 vs 7.6e-5). The joint logistic OR (0.77) points opposite to the raw difference. This reversal is unexplained; confounding and collinearity were not tested.
- **Interaction evidence (stat_2).** The Glucose × Age p-value is not adjusted for the two interaction tests. The interaction is judged on the logit scale from one model. The Glucose × BMI split shows a larger probability gap at high Glucose, but the logistic test does not support an interaction.
- **Pregnancies within-band analysis (eda_3, partial; review issue stands).** The full 16-cell table is now reported from the recorded cell facts. The lead's objection still stands: several cells are very small (n=4, 10, 14, 20, 26), and the within-band conclusions for the older bands and the 6+ group are not established. No interaction model or per-cell confidence intervals were fitted, so the robustness of the 1-2 dip to small cells is untested. The age-standardised figure depends on these small cells.
- **Predictive model limitations (ml_1).** A single stratified split with a 154-row test set, so metrics carry substantial sampling error. No cross-validation was run. The random forest overfits (train accuracy 1.0). Importance rankings were not checked for seed sensitivity.
- **Task status.** No task failed. eda_3 is partial, as described above.

## Open questions

- Should the zeros in Insulin and SkinThickness be imputed, dropped, or kept as a missingness indicator before modelling, given they affect 48.7% and 29.6% of rows? Does the choice change the model ranking or test AUC?
- Does the outcome rate for zero Insulin and SkinThickness rows change after adjusting for Age and Pregnancies, and is any zero-to-Outcome relation hidden by those variables? (Partly addressed by stat_3, with the no-association result described above.)
- Is the non-monotonic Pregnancies pattern robust to small cell sizes? A logistic model of Outcome on Pregnancies group, Age and their interaction, with per-cell confidence intervals, was proposed but not run.
- Why does BloodPressure reverse direction in the joint logistic model? Is this confounding or collinearity with BMI and Age?
- Does Age's raw association disappear after adjusting for Pregnancies and BMI? Does the Glucose effect hold after adjusting for BMI and Age?
- Does the Glucose × Age interaction hold after adjusting for Pregnancies, BloodPressure and Insulin, and is it driven by a non-linear Age or Glucose effect (for example, a spline or quadratic term)?
- Does the BMI association differ across Glucose strata when BMI is modelled on the logit scale with per-stratum confidence intervals?
- How sensitive are the Glucose and BMI importances to the random seed or a cross-validated split? How much do test metrics change if Insulin zeros are dropped rather than imputed?