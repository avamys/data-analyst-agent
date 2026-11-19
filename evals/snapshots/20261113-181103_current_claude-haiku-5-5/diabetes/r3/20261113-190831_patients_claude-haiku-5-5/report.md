# Pima-Style Diabetes Dataset (768 Rows): Outcome Rates, Zero-Coded Values, Feature Effects and Model Performance

## Summary

- **Feature effects are large and significant, but the zero-coded features are sensitive to how zeros are handled.** Glucose (median-split odds ratio 6.16) and BMI are unchanged when zeros are kept as values. BloodPressure, SkinThickness and Insulin weaken or lose significance (Insulin keeps only a Welch test significant). Their NaN-rule effects should not be taken at face value.
- **Glucose is the strongest predictor across methods.** It has the largest effect size (Cohen d 1.19) and the largest test-fold permutation importance for both models. It stays significant after adjusting for the other features (OR 1.039 per mg/dL, n=392 complete cases).
- **Both classifiers beat the 64.9% majority baseline on a 154-row test fold.** The random forest reaches accuracy 0.7468 (gain 0.0974, ROC AUC 0.8061). Logistic regression reaches 0.6883 (gain 0.0389, ROC AUC 0.8104). The ROC AUC difference is small (0.0043) and was not tested.
- **Interaction evidence is limited.** Only Pregnancies×Age is significant after Holm correction (adjusted p=0.0067), and it comes from the logistic model alone. The Glucose×BMI and Glucose×Age interactions are not significant.

## Data

- 768 rows × 9 columns: 8 numeric features (Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age) and a binary target, Outcome. There are no categorical, date/time, id or free-text columns.
- Outcome: 500 rows (65.1%) are 0 and 268 (34.9%) are 1.
- The profile reports no missing values. However, zeros in Glucose, BloodPressure, SkinThickness, Insulin and BMI are physiologically implausible and were treated as hidden missing values in the analysis (see Findings, zero handling). Zero counts: Insulin 374 (48.7%), SkinThickness 227 (29.56%), BloodPressure 35 (4.56%), BMI 11 (1.43%), Glucose 5 (0.65%).

## Findings

### Outcome distribution and rates by feature group

Outcome rate rises across quartiles of most features (quartile bins from qcut with duplicates dropped):

| Feature | Lowest quartile rate | Highest quartile rate |
|---|---|---|
| Glucose | 8.1% (mean 84.7) | 68.8% (mean 164.3) |
| BMI | 10.3% (mean 22.7) | 48.4% (mean 41.6) |
| Age | 14.2% (mean 22.3) | 51.7% (mean 51.5) |
| Pregnancies | 27.2% | 56.2% |
| SkinThickness | 28.8% | 46.8% |
| BloodPressure | 25.4% | 46.7% |
| DiabetesPedigreeFunction | 25.5% | 48.4% |

Insulin is non-monotonic: 36.5%, 16.2%, then 50.5% across its quartiles. The lowest Insulin quartile is dominated by zeros, so its low and high ends behave differently.

Distribution medians: Glucose 117, BMI 32.0, Age 29, Insulin 30.5, SkinThickness 23.0, BloodPressure 72.0.

![Box plots of each feature split by Outcome 0 and Outcome 1, showing value distributions per group](tasks/eda_1/charts/eda1_feature_boxplots_by_outcome.png)

### Zero-coded values and their link to Outcome

- Rows with a zero differ in Outcome rate from rows without one: BloodPressure 45.7% vs 34.4%; SkinThickness 38.8% vs 33.3%; Insulin 36.9% vs 33.0%; BMI 18.2% vs 35.1%. Glucose has only 5 zero rows (40.0% vs 34.9%), which is too few to interpret.
- Zeros also co-occur with other columns' values. For example, BloodPressure zero rows have mean Age 30.7 vs 33.4 and mean BMI 25.7 vs 32.3 for nonzero rows.
- Correlations between zero indicators: SkinThickness–Insulin 0.665 (strong); BMI–BloodPressure 0.341; SkinThickness–BloodPressure 0.310. Glucose zeros are essentially uncorrelated with the others (|r| ≤ 0.052).
- Rows with zeros in k of the five columns: 392 rows (51.04%) have none, 142 (18.49%) have one, 199 (25.91%) have two, 28 (3.65%) have three and 7 (0.91%) have four.

The analysis recommends treating these zeros as missing, keeping Pregnancies and Age unchanged, and avoiding simple deletion or global-mean imputation. Missingness mechanism (MCAR, MAR or MNAR) was not tested.

### Which features differ between Outcome groups (stat_1)

Zeros in the five columns were set to NaN. Pregnancies and Age used n = 268 (Outcome 1) and 500 (Outcome 0). Other feature sample sizes are given in the median-split tests below. Shapiro tests rejected normality in both groups for most features, so Mann-Whitney was the primary test; Welch was reported alongside. Every feature is significant after Holm correction at 0.0001 or below, except as noted.

| Feature | n (Outcome 1 / 0) | Cohen d | Rank-biserial | Mean difference (95% CI) |
|---|---|---|---|---|
| Glucose | 266 / 497 | 1.193 | 0.586 | 31.68 (27.49 to 35.86) |
| Insulin | 130 / 264 | 0.676 | 0.463 | 76.56 (50.46 to 102.66) |
| BMI | 266 / 491 | 0.691 | 0.374 | 4.55 (3.56 to 5.53) |
| Age | 268 / 500 | 0.514 | 0.374 | 5.88 (4.21 to 7.55) |
| SkinThickness | 180 / 361 | 0.569 | 0.325 | 5.76 (3.93 to 7.60) |
| Pregnancies | 268 / 500 | 0.477 | 0.239 | 1.57 (1.05 to 2.09) |
| BloodPressure | 252 / 481 | 0.364 | 0.215 | 4.44 (2.57 to 6.32) |
| DiabetesPedigreeFunction | 268 / 500 | 0.370 | 0.212 | 0.121 (0.069 to 0.173) |

BloodPressure and DiabetesPedigreeFunction have the weakest Holm-adjusted p-values (below 0.0001 for both Welch and Mann-Whitney), while the others are at or below 0.0001 on each test.

Median-split Fisher exact tests (high vs low median, Woolf 95% CI). Sample sizes differ by feature: Glucose 763, BloodPressure 733, SkinThickness 541, Insulin 394, BMI 757, and Pregnancies, DiabetesPedigreeFunction and Age 768.

| Feature | Odds ratio (95% CI) |
|---|---|
| Glucose | 6.16 (4.39 to 8.65) |
| Insulin | 5.50 (3.42 to 8.84) |
| Age | 3.64 (2.65 to 4.98) |
| BMI | 2.82 (2.07 to 3.85) |
| SkinThickness | 2.67 (1.84 to 3.87) |
| Pregnancies | 2.26 (1.67 to 3.05) |
| BloodPressure | 1.75 (1.29 to 2.38) |
| DiabetesPedigreeFunction | 1.62 (1.20 to 2.19) |

All of these are significant after Holm correction. The weakest is DiabetesPedigreeFunction (Holm p 0.001883); BloodPressure is 0.000896. The quartile chi-square tests are also significant for all eight features, with BloodPressure and DiabetesPedigreeFunction the weakest (Holm p 0.000058 each).

These are associations, not causal effects.

![Mean difference in each feature between Outcome=1 and Outcome=0 with Welch 95% CI (zeros in Glucose, BloodPressure, SkinThickness, Insulin, BMI treated as NaN)](tasks/stat_1/charts/stat1_mean_diff_ci.png)

### Adjusted associations (stat_3)

A logistic regression on all eight features was fitted to the 392 complete cases (130 Outcome 1, 262 Outcome 0), which are the rows with no zero-coded values. This is about half the data. Adjusted results:

| Feature | Odds ratio (95% CI) | p |
|---|---|---|
| Glucose (per mg/dL) | 1.039 (1.027 to 1.051) | <0.0001 |
| BMI (per unit) | 1.073 (1.017 to 1.132) | 0.010 |
| DiabetesPedigreeFunction (per unit) | 3.130 (1.354 to 7.233) | 0.008 |
| Age (per year) | 1.035 (0.998 to 1.072) | 0.065 |
| Pregnancies | 1.086 (0.974 to 1.210) | 0.138 |
| SkinThickness | 1.011 (0.978 to 1.046) | 0.511 |
| Insulin (per unit) | 0.999 (0.997 to 1.002) | 0.528 |
| BloodPressure | 0.999 (0.976 to 1.022) | 0.904 |

Glucose and BMI remain significant positive associations after mutual adjustment. DiabetesPedigreeFunction becomes significant after adjustment. Age (p=0.065), Insulin, Pregnancies, SkinThickness and BloodPressure are not significant at 0.05.

The adjusted per-unit odds ratios and the unadjusted median-split odds ratios use different scales and different samples, so only direction and significance can be compared. The unadjusted median-split results for Insulin (5.50) and Age (3.64) are not significant at 0.05 once the other features are included in the model.

### Interactions (stat_2)

The interaction models use 752 rows, because rows with zero Glucose or zero BMI were dropped. Coefficients are per one standard deviation of each standardized term.

| Interaction | Odds ratio (95% CI) | p | Holm p (3 tests) |
|---|---|---|---|
| Glucose × BMI | 0.93 (0.74 to 1.18) | 0.56 | 0.56 |
| Glucose × Age | 0.84 (0.68 to 1.02) | 0.076 | 0.15 |
| Pregnancies × Age | 0.72 (0.58 to 0.89) | 0.0022 | 0.0067 |

- **Glucose × BMI and Glucose × Age:** no evidence that the Glucose effect changes with BMI or Age. The Pregnancies×Age interaction is the only one significant after correction. It means the Pregnancies association weakens as Age rises, or equivalently that the Age association weakens with more pregnancies. This significance comes from the logistic model only; no stratified table supports it, and it carries the same zero-dropping caveat as the other coefficients.

Outcome rate (%) by Glucose tertile within each BMI tertile (zeros dropped):

| BMI tertile | Glucose low | Glucose mid | Glucose high | High-minus-low |
|---|---|---|---|---|
| Low | 2.8 | 19.4 | 34.0 | 0.31 |
| Mid | 16.9 | 39.0 | 67.4 | 0.50 |
| High | 20.0 | 33.8 | 75.5 | 0.55 |

Outcome rate (%) by Glucose tertile within each Age tertile (zeros dropped):

| Age tertile | Glucose low | Glucose mid | Glucose high | High-minus-low |
|---|---|---|---|---|
| Low | 3.4 | 14.0 | 52.7 | 0.49 |
| Mid | 15.2 | 35.2 | 68.0 | 0.53 |
| High | 24.1 | 43.1 | 65.8 | 0.42 |

The raw high-minus-low differences rise across BMI tertiles, but the model test does not support a slope difference (p=0.56), so this pattern is not established. Across Age tertiles there is no monotone trend, consistent with the non-significant Glucose×Age term.

![Proportion with Outcome=1 across Glucose tertiles, drawn separately for each BMI tertile (zeros in Glucose and BMI dropped)](tasks/stat_2/charts/stat2_glucose_rate_by_bmi.png)

### Effect of the zero rule (stat_4)

Zeros were kept as values and compared with the NaN rule. The split medians are shown for each rule.

| Feature | Rule | Mean diff (95% CI) | Cohen d | Rank-biserial | Holm p (Welch / MWU / Fisher) | Median-split OR (95% CI) |
|---|---|---|---|---|---|---|
| Glucose | Kept | 31.28 (26.81 to 35.75) | 1.11 | 0.576 | 0 / 0 / 0 | 6.02 (4.31 to 8.43) |
| Glucose | NaN | 31.68 (27.49 to 35.86) | 1.19 | 0.586 | 0 / 0 / 0 | 6.16 (4.39 to 8.65) |
| BMI | Kept | 4.84 (3.74 to 5.94) | 0.64 | 0.375 | 0 / 0 / 0 | 2.94 (2.16 to 4.01) |
| BMI | NaN | 4.55 (3.56 to 5.53) | 0.69 | 0.374 | 0 / 0 / 0 | 2.82 (2.07 to 3.85) |
| BloodPressure | Kept | 2.64 (−0.39 to 5.67) | 0.137 | 0.173 | 0.0987 / 0.0002 / 0.0028 | 1.63 (1.21 to 2.20) |
| BloodPressure | NaN | 4.44 (2.57 to 6.32) | 0.364 | 0.215 | 0.000004 / 0.000002 / 0.0004 | 1.75 (1.29 to 2.38) |
| SkinThickness | Kept | 2.50 (0.01 to 4.99) | 0.157 | 0.107 | 0.0987 / 0.026 / 0.0008 | 1.75 (1.30 to 2.36) |
| SkinThickness | NaN | 5.76 (3.93 to 7.60) | 0.569 | 0.325 | 0 / 0 / 0 | 2.67 (1.84 to 3.87) |
| Insulin | Kept | 31.54 (12.76 to 50.33) | 0.276 | 0.076 | 0.0031 / 0.066 / 0.405 | 0.87 (0.65 to 1.17) |
| Insulin | NaN | 76.56 (50.46 to 102.66) | 0.676 | 0.463 | 0 / 0 / 0 | 5.50 (3.42 to 8.84) |

Split medians: Glucose 117 under both rules; BloodPressure 72 under both; SkinThickness 23 kept vs 29 NaN; Insulin 30.5 kept vs 125 NaN; BMI 32.0 kept vs 32.3 NaN.

- **Glucose and BMI:** conclusions unchanged.
- **BloodPressure:** Welch is no longer significant at 0.05 with zeros kept. Mann-Whitney and Fisher remain significant.
- **SkinThickness:** the association is much weaker. Welch is not significant (Holm p 0.0987). Mann-Whitney is marginal (Holm p 0.026), and Fisher is clearly significant (Holm p 0.0008). The split median moves from 29 to 23, so the odds-ratio change mixes the zero rule with a different split.
- **Insulin:** only the Welch test is significant with zeros kept. Mann-Whitney (Holm p 0.066) and Fisher (Holm p 0.405) are not. The kept-zero median of 30.5 lies just above the zero block, which accounts for 48.7% of values, in the low positive range. The median split therefore mixes zeros with low positive values, so the odds-ratio change partly reflects the split.

![Cohen d of Outcome 1 vs 0 for Glucose, BloodPressure, SkinThickness, Insulin and BMI, under the NaN rule and with zeros kept](tasks/stat_4/charts/stat4_cohen_d_nan_vs_kept.png)

### Classifier performance (ml_1, ml_2)

- **Split:** stratified 80/20 split with random_state 42 gives 614 training rows and 154 test rows. Class-1 share is 34.85% in training and 35.06% in test. The majority-class baseline on the test fold is 0.6494.
- **Preprocessing:** zeros in the five columns were set to NaN and median-imputed, with the imputer and scaler fitted on the training fold only.
- **Hyperparameters** were chosen by 5-fold stratified CV on the training fold.

| Model | Test accuracy | Gain over baseline | Test ROC AUC | Precision | Recall | F1 (class 1) | Train accuracy | CV ROC AUC |
|---|---|---|---|---|---|---|---|---|
| Random forest (200 trees, max_depth 5, min_samples_leaf 5) | 0.7468 | 0.0974 | 0.8061 | 0.6744 | 0.537 | 0.5979 | 0.8453 | 0.8393 |
| Logistic regression (C=0.1) | 0.6883 | 0.0389 | 0.8104 | 0.5652 | 0.4815 | 0.52 | 0.7899 | 0.8443 |

Both models show a train–test accuracy gap (logistic regression 0.1016, random forest 0.0985). The test metrics are the reliable comparison. The two models have nearly the same test ROC AUC (difference 0.0043). The random forest's higher accuracy, precision and recall at threshold 0.5 may reflect a different class-1 threshold. This is an untested hypothesis; no interval or test was computed for the accuracy or ROC AUC gaps on 154 rows.

**Feature importance:**

- Permutation importance on the test fold (drop in ROC AUC, 30 repeats): logistic regression ranks Glucose 0.1556, Pregnancies 0.0263 and BMI 0.0253. The random forest ranks Glucose 0.0951, BMI 0.0345 and Age 0.0272. SkinThickness (−0.0013) and BloodPressure (−0.0043) are near zero for the random forest.
- Model-native ranking: logistic regression absolute standardized coefficients are Glucose 1.019, BMI 0.5799, Pregnancies 0.322. Random forest impurity importances are Glucose 0.3918, BMI 0.1688, Age 0.1225.
- Glucose ranks first by every method reported. BloodPressure and Insulin have near-zero coefficients in logistic regression (0.0041 and 0.0033).

![Permutation importance on the test fold (mean ROC AUC drop) for logistic regression and random forest](tasks/ml_2/charts/ml2_permutation_importance.png)

## Limitations

- **Zero-coded missingness is linked to Outcome and to other columns, and its mechanism was not tested.** Zeros are not random as far as the EDA shows, so the NaN-rule effects and coefficients for the five zero-coded features may be biased. The team did not test MCAR, MAR or MNAR.
- **The NaN rule reduces sample size.** The interaction models use 752 rows and the adjusted logistic model uses 392 complete cases (about half the data). Stat_1 median-split samples also differ by feature (Glucose 763, BloodPressure 733, SkinThickness 541, Insulin 394, BMI 757; Pregnancies, DiabetesPedigreeFunction and Age 768).
- **Conclusions change with the zero rule for three of the five zero-coded features** (BloodPressure, SkinThickness and Insulin; see the zero-rule table above). The zeros-kept comparison was run for univariate tests only. It was not run for the adjusted or interaction models.
- **Glucose zeros (5 rows) are too few to interpret.** The EDA did not link them to Outcome; only BMI zeros were linked to a lower Outcome rate in the EDA.
- **Model comparisons are limited.** The test fold has 154 rows and no intervals were computed for the accuracy, F1 or ROC AUC gaps. The models use median imputation only; model-based, KNN and no-imputation alternatives were not compared.
- **Adjusted and median-split odds ratios are not on the same scale.** Only their direction and significance can be compared.
- **Unresolved review issues, and how this report handles them:**
  - *stat_2 (three issues):* (1) The Outcome-rate tables for Glucose tertiles within BMI and Age tertiles are included above. (2) The EDA is not described as linking Glucose zeros to Outcome. (3) The Pregnancies×Age significance is stated as coming from the logistic model only, with the zero-dropping caveat.
  - *stat_3:* The comparison bullet is corrected: stat_1 sample sizes differ by feature, and the wording is "Insulin and Age are not significant at 0.05 after adjustment (Age p=0.065)".
  - *stat_4 (a):* The SkinThickness zeros-kept median-split odds ratio (1.75) and Welch Holm p (0.0987) were flagged as possible copy errors. The stat4 side-by-side table gives the same values (1.7493 and 0.0987), so they are reported as recorded. The same Welch Holm value (0.0987) also appears for BloodPressure, which should be verified against the source.
  - *stat_4 (b):* The SkinThickness description is corrected: Mann-Whitney (Holm p 0.026) is marginal, while Fisher (Holm p 0.0008) is clearly significant.
  - *stat_4 (c):* The Insulin description is corrected: zeros are 48.7% of values, so the median of 30.5 lies just above the zero block in the low positive range.
- **Associations are not causal effects.**
- No tasks failed; all eight tasks were marked complete and accepted.

## Open questions

- What is the missingness mechanism (MCAR, MAR or MNAR) for each zero-coded column, for example via a logistic model of each zero indicator on the other features and Outcome?
- Do the findings hold with zeros kept as values, imputed, or multiply imputed? For the models, this covers median, KNN, iterative and model-based imputation, and keeping zeros as values.
- Does a missing-indicator feature for Insulin zeros (48.7% of rows) improve model performance or change the Insulin association?
- Should the 5 Glucose zeros be dropped as data-entry errors?
- Do Insulin and SkinThickness associations survive mutual adjustment with zeros as NaN and with a zero-indicator?
- Does the Pregnancies×Age interaction hold after adjusting for Glucose, BMI and BloodPressure, and is it driven by the high-Age group?
- Are the Glucose×BMI and Glucose×Age interactions different from zero by likelihood-ratio test or bootstrap CIs?
- Are the two models' accuracy, F1 and ROC AUC gaps reliable under repeated cross-validation or bootstrap on the test fold?
- Are the adjusted coefficients stable given multicollinearity (VIF) and linearity of the logit (splines, log Insulin)?
- Is the DiabetesPedigreeFunction effect robust to the complete-case restriction?