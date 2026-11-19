# Pima Diabetes Dataset: Predicting Outcome, with Zero-Coded Missing Values

## Summary

- **Outcome is predictable from the cleaned features.** On one stratified 80/20 test split (n=154), logistic regression reached accuracy 0.7143 and ROC AUC 0.8178, against 0.6494 accuracy for the majority-class baseline. Gradient boosting scored highest (accuracy 0.7532, AUC 0.8300), but its accuracy margin over logistic regression (0.7532 vs 0.7143) is measured on a single split and is not established.
- **Glucose and BMI are the strongest signals.** Glucose has the largest Outcome-group effect (rank-biserial 0.586; medians 107 vs 140) and is the top permutation feature for both tree models. BMI is second in both. On cleaned data, the Outcome=1 rate is 7.3% in the lowest Glucose quartile and 69.5% in the highest.
- **Zeros in SkinThickness and Insulin are common and are associated with Age and Pregnancies.** SkinThickness has 227 zeros (29.6%) and Insulin has 374 (48.7%). Outcome=1 rates did not differ significantly between zero and non-zero rows, but the adjusted tests are too imprecise to establish independence from Outcome. Zeros in Glucose, BloodPressure and BMI are rare (5, 35 and 11 rows).
- **The Outcome-group differences for Insulin and SkinThickness hold under multiple imputation.** The Glucose × BMI interaction is not significant (p=0.51), and its confidence interval is too wide to rule out a meaningful interaction.

## Data

- 768 rows and 9 columns: 8 numeric features (Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age) and the binary target Outcome. There are no categorical, date, identifier or free-text columns.
- Outcome: 34.9% are 1 (268 rows) and 65.1% are 0 (500 rows). A majority-class model therefore starts at 65.1% accuracy on the full data.
- The profile reports no empty cells. However, zeros appear in Glucose, BloodPressure, SkinThickness, Insulin and BMI, which are physiologically implausible. The analysis treated these zeros as missing values. Zero counts are: Glucose 5 (0.7%), BloodPressure 35 (4.6%), SkinThickness 227 (29.6%), Insulin 374 (48.7%), BMI 11 (1.4%).
- 376 rows (49.0%) have at least one zero among these five columns, and 234 rows have two or more.
- The cleaned dataset `clean_patients` contains the same 768 rows with zeros replaced by NaN, plus five missing-indicator columns.

## Findings

### Outcome rates by binned feature (raw data, zeros kept)

Outcome=1 rates rise across quartiles of Glucose, BMI, Age and Pregnancies. DiabetesPedigreeFunction shows a smaller rise. These values are for the raw data, where zeros were retained, so the lowest-quartile figures for Glucose and BMI include zero-coded rows. The largest rate differences between lowest and highest bins are for Glucose, then BMI and Age, with Pregnancies and DiabetesPedigreeFunction smaller.

- **Glucose:** 8.1% (n=197, ≤99), 24.7% (n=194), 38.9% (n=185), 68.8% (n=192, >140.25).
- **BMI:** 10.3% (n=194, ≤27.3), 35.9% (n=192), 45.4% (n=194), 48.4% (n=188, >36.6).
- **Age:** 14.2% (n=219, ≤24), 29.9% (n=177), 47.5% (n=200), 51.7% (n=172, >41).
- **Pregnancies:** 27.2% (0–1, n=246), 25.8% (2–3, n=178), 34.3% (4–6, n=175), 56.2% (7–17, n=169). The rise is concentrated in the top quartile.
- **DiabetesPedigreeFunction:** 25.5%, 33.3%, 32.3%, 48.4% (n=192 each). The rise is mainly from the top quartile.

![Rate of Outcome=1 by quartile bin of Glucose and BMI (share of rows per bin)](tasks/eda_1/charts/outcome_rate_by_glucose_bmi.png)

### Zero-coded values and their relation to Outcome, Age and Pregnancies

- Outcome=1 rates did not differ significantly between zero and non-zero rows for any of the five columns (Fisher p: Glucose 1.00, BloodPressure 0.203, SkinThickness 0.159, Insulin 0.289, BMI 0.346). The BMI zero-row rate (18.2%, n=11) is not reliable.
- SkinThickness and Insulin zeros are associated with Age and Pregnancies. Zero-coded SkinThickness rows have median Age 34 vs 28 (Mann-Whitney p=1.1e-09) and median Pregnancies 4 vs 2 (p=3.1e-06). Zero-coded Insulin rows have median Age 32 vs 27 (p=2.1e-08) and median Pregnancies 4 vs 2 (p=8.9e-07).
- Glucose, BloodPressure and BMI zeros show no significant Age or Pregnancies association, but these groups are small (5, 35 and 11 rows).
- Every SkinThickness zero is also an Insulin zero (227 rows). Insulin zeros include all of them.
- Adjusted for Age and Pregnancies only, the odds of zero-coded missingness for Outcome=1 were 0.92 for Insulin (95% CI 0.67 to 1.26, p=0.60) and 0.99 for SkinThickness (95% CI 0.71 to 1.39, p=0.96). The intervals allow an association in either direction, so this is not evidence of independence. The adjustment set is incomplete.

![Percent of Outcome=1 among rows where each column is zero versus non-zero](tasks/eda_2/charts/outcome_rate_zero_vs_nonzero.png)

### Cleaned-data quartile rates for Glucose and BMI

These figures come from `clean_patients`, with NaN excluded. They are reported by eda_3 only (see Limitations).

- **Glucose** cutoffs 99, 117 and 141. Outcome=1 rates: Q1 (n=192) 7.3%, Q2 (n=194) 24.7%, Q3 (n=190) 38.9%, Q4 (n=187) 69.5%.
- **BMI** cutoffs 27.5, 32.3 and 36.6. Outcome=1 rates: Q1 (n=193) 11.4%, Q2 (n=187) 36.4%, Q3 (n=189) 45.0%, Q4 (n=188) 48.4%.
- eda_3 states that the eda_1 extreme-quartile gaps approximately hold on cleaned data. It did not re-verify the eda_1 bin definitions, so exact reproduction is not established.
- Lowest quartile versus rest: Glucose 7.3% (n=192) vs 44.1% (n=571), a gap of −0.368. BMI 11.4% (n=193) vs 43.3% (n=564), a gap of −0.319.
- For Glucose, the raw lowest-quartile rate (8.1%, n=197) and the cleaned rate (7.3%, n=192) are both reported. The five zero rows in the raw bin had a 40% rate.
- For BMI, the raw bin (n=194, cutoff 27.3, rate 10.3%) and the cleaned bin (n=193, cutoff 27.5) differ. eda_3 attributes the cutoff shift to zeros being set to NaN before quantiles are computed. The review of the eda_2 task states that the difference comes from the cutoff moving, not from the 11 zeros. These two statements disagree, and this report does not resolve the disagreement.

![Outcome=1 rate (percent) per quartile of cleaned Glucose and BMI, NaN rows excluded; n shown above each bar](tasks/eda_3/charts/eda_3_quartile_rates.png)

### Outcome-group differences on cleaned data (complete cases)

Zeros were set to NaN, so each test uses only non-missing rows. As reported, all eight numeric features differ between Outcome groups under Mann-Whitney tests with Holm correction, with adjusted p-values below 0.0001 (largest adjusted p 2.4e-06, for BloodPressure). Effect sizes are rank-biserial correlations with bootstrap 95% CIs.

- **Glucose:** median 107 (Outcome 0) vs 140 (Outcome 1); rank-biserial 0.586 (0.523 to 0.649); Cohen's d 1.19 (1.03 to 1.37). n=497 and 266.
- **Insulin:** medians 102.5 vs 169.5; rank-biserial 0.463 (0.364 to 0.563). n=264 and 130.
- **BMI:** medians 30.1 vs 34.3; rank-biserial 0.374 (0.294 to 0.453). n=491 and 266.
- **Age:** medians 27 vs 36; rank-biserial 0.374 (0.305 to 0.448). n=500 and 268.
- **SkinThickness:** medians 27 vs 32; rank-biserial 0.325 (0.230 to 0.416). n=361 and 180.
- **Pregnancies:** medians 2 vs 4; rank-biserial 0.239 (0.151 to 0.323).
- **BloodPressure:** medians 70 vs 74.5; rank-biserial 0.215 (0.129 to 0.302). n=481 and 252.
- **DiabetesPedigreeFunction:** medians 0.336 vs 0.449; rank-biserial 0.212 (0.131 to 0.293).

The Insulin and SkinThickness effects rest on complete cases, and their zeros are linked to Age and Pregnancies. The Insulin effect may be confounded or selection-biased.

![Rank-biserial effect of Outcome=1 versus Outcome=0 per feature; positive means higher in Outcome=1; whiskers show 95% bootstrap CI](tasks/stat_1/charts/stat1_effect_sizes.png)

### Glucose × BMI interaction

- In a logistic model on 752 complete cases, centred at means, the interaction coefficient is −0.00035 per mg/dL × kg/m² (95% CI −0.0014 to 0.0007, p=0.513). The result is inconclusive: a clinically meaningful interaction is not excluded.
- Within BMI tertiles, the odds ratio per 10 mg/dL of Glucose is 1.44 (1.26 to 1.66) in the low tertile (BMI 18.2 to 29.0, n=252), 1.44 (1.30 to 1.60) in the middle tertile (BMI 29.2 to 34.9, n=254), and 1.51 (1.35 to 1.69) in the high tertile (BMI 35.0 to 67.1, n=246). The tertiles are not a formal test of change.

### Multiple imputation of zero-coded Insulin and SkinThickness

- Using 20 IterativeImputer draws, with zeros treated as missing and the imputation model including Outcome and all other features, the pooled Outcome=1 minus Outcome=0 mean difference is 72.6 for Insulin (95% CI 52.6 to 92.6, p=7e-12) and 5.58 for SkinThickness (95% CI 3.87 to 7.29, p=3e-10), in feature units.
- Both agree with the complete-case results in direction and significance. The two estimates are on different scales and are not directly comparable in magnitude.
- The pooled Glucose × BMI interaction with imputed Insulin and SkinThickness is −0.00036 (95% CI −0.0014 to 0.0007, p=0.51), close to the complete-case estimate. A BMI spline has not been tested.

![Pooled mean differences (Outcome=1 minus Outcome=0) for Insulin and SkinThickness after multiple imputation of zero-coded values, with 95% CIs](tasks/stat_2/charts/stat2_mi_outcome_diffs.png)

### Logistic regression prediction (cleaned features, one split)

- Split: stratified 80/20, seed 42; 614 training rows and 154 test rows. Median imputation was fit on the training set. The model used the eight cleaned features plus five missing-indicator columns.
- Majority-class baseline on the test set: accuracy 0.6494, log-loss 0.6479.
- Standardized logistic regression: accuracy 0.7143, log-loss 0.5090, ROC AUC 0.8178, precision 0.6042, recall 0.537, F1 0.5686. Training accuracy is 0.7948.
- Confusion matrix (rows true, columns predicted): 81 of 100 Outcome=0 rows and 29 of 54 Outcome=1 rows correctly classified.
- Absolute standardized coefficients, largest first: Glucose 1.1994, BMI 0.70, Pregnancies 0.3722, DiabetesPedigreeFunction 0.2542, BloodPressure_missing 0.2005, Insulin_missing 0.1823, Age 0.1479, SkinThickness_missing 0.1094, BMI_missing 0.0875, Glucose_missing 0.0613. The indicator coefficients are conditional on the other features and are not treated as established signal.

### Tree models on the same test split

- Random forest: accuracy 0.7338, precision 0.6383, recall 0.5556, F1 0.5941, ROC AUC 0.8079, log-loss 0.4996. Training accuracy 1.0.
- Gradient boosting: accuracy 0.7532, precision 0.66, recall 0.6111, F1 0.6346, ROC AUC 0.8300, log-loss 0.4977. Training accuracy 0.9235.
- Both tree models overfit. Training-to-test accuracy gaps are 0.27 (random forest) and 0.17 (gradient boosting).
- Against logistic regression (accuracy 0.7143), the random forest scores 0.7338 and gradient boosting 0.7532 on the same split. This advantage is measured on one 154-row split and is uncertain.
- Among the four models compared, gradient boosting is best on accuracy, AUC and log-loss.

![Permutation importance on the test set (drop in ROC AUC) for random forest and gradient boosting, all 13 input features](tasks/ml_2/charts/ml2_permutation_importance.png)

### Feature importance in the tree models

- Permutation importance (drop in test ROC AUC): Glucose is the top feature for both models, at 0.097 (sd 0.022) for the random forest and 0.106 (sd 0.026) for gradient boosting.
- BMI is second: 0.034 (sd 0.018) for the random forest and 0.053 (sd 0.022) for gradient boosting.
- Age is third: 0.024 (sd 0.013) and 0.034 (sd 0.010).
- The missing-indicator columns contribute little. The largest is BloodPressure_missing in gradient boosting, at 0.0055 (sd 0.0037).
- Removing the indicators gives the random forest test log-loss 0.4930 (vs 0.4996) and AUC 0.8158 (vs 0.8079). For gradient boosting it gives log-loss 0.4957 (vs 0.4977) and AUC 0.8315 (vs 0.8300). These differences come from one split.

## Limitations

- **Zeros treated as missing.** The profile reports no empty cells. Treating zeros as missing is an assumption supported by the implausibility of zero values, not by a recorded missing-data code.
- **Zeros are linked to Age and Pregnancies.** SkinThickness and Insulin zeros are associated with Age and Pregnancies, so the Outcome-group effects for these features may be confounded or selection-biased. The Age and Pregnancies adjustment set in the missingness models is incomplete.
- **Small groups for some zero columns.** The Glucose (5 zeros), BloodPressure (35) and BMI (11) zero groups are too small for reliable group comparisons. The BMI zero-row Outcome rate rests on 11 rows.
- **Single test split.** All model scores come from one 154-row split. Differences between models of a few rows are not established. No repeated or cross-validated evaluation was performed.
- **Missing-indicator signal is unconfirmed.** Indicator coefficients are conditional on other features, and tree-model permutation importances are small. Whether they reflect signal or proxy Age and Pregnancies was not tested.
- **Glucose × BMI interaction is inconclusive.** The confidence interval includes meaningful interactions. Non-linear (spline) tests were not run.
- **Imputation was not compared for prediction.** The multiple-imputation results are inference-only. Model performance with imputation versus dropping rows was not tested.
- **Unresolved review issue on eda_2.** The lead's objection stands and affects the following findings:
  - The claim that the 11 BMI zeros move the lowest-quartile rate by about 0.5 points is withdrawn. No fact supports it, and it is not quoted.
  - The explanation of the BMI bins is corrected: the raw bin (n=194) and cleaned bin (n=193) differ because the cutoff moves from 27.3 to 27.5, not because of the 11 zeros. eda_3 attributes the cutoff shift to the zeros, which disagrees with this objection. The disagreement is left unresolved.
  - The cleaned-data lowest-quartile Outcome rate and gap versus the rest of the data for Glucose and BMI are not confirmed in this report. Neither eda_2 nor ml_1 establishes them. The cleaned-data figures above come from eda_3 alone, and this report does not independently verify them.
- **Task status.** eda_2 is marked partial. Its missing-indicator and co-occurrence results are reported as given, subject to the limits above. No other task failed.

## Open questions

- Are SkinThickness and Insulin zeros missing at random given Age and Pregnancies, or do they reflect a measurement protocol? A model of the missing indicator that includes Glucose and BMI as predictors has not been fitted.
- Should the zeros in Glucose, BloodPressure and BMI be treated as data-entry errors and handled separately from the SkinThickness and Insulin zeros?
- Does imputing Insulin and SkinThickness (by median or by Age group) change Outcome model performance compared with dropping rows?
- Do the missing-indicator columns carry real signal, or do they proxy for Age and Pregnancies? Compare models with and without them across several splits.
- Does the tree models' advantage over logistic regression hold across repeated splits or cross-validation?
- Do the Glucose and BMI quartile gaps hold within Age groups?
- Does the Glucose × BMI interaction change when BMI is modelled as a spline or when Insulin and SkinThickness are imputed?
- Do the eda_1 extreme-quartile gaps reproduce exactly when the bin definitions are re-verified on cleaned data?