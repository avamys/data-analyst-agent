# Outcome Prediction in a 768-Row Diabetes Dataset: Feature Rates, Zero-Coded Values, Effects, Interactions and Models

## Summary

- **Glucose is the strongest single feature.** The Outcome=1 rate rises from 8.1% in the lowest Glucose quartile to 68.8% in the highest. Its rank-biserial effect is 0.576 (95% CI 0.513 to 0.645), and it is the top predictor in both models.
- **Zero values in Insulin and SkinThickness are common (48.7% and 29.56% of rows) and are likely missing-value codes.** Once zeros are excluded, the Outcome=1 rate still rises across the non-zero Insulin and SkinThickness bins. The SkinThickness rank-biserial effect is 0.107 on all rows and 0.325 on non-zero rows. The zero-coding interpretation rests on physiology and mean differences, not on a formal test.
- **Of the two interactions tested, only Age × Pregnancies is significant** (Wald p = 0.003). Glucose × BMI is not significant, including in the non-zero-only sensitivity check.
- **A standardized logistic regression reached 71.4% test accuracy against a 64.9% majority-class baseline** (ROC AUC 0.823). A random forest reached 73.4% but overfits heavily (train accuracy 1.0), so its scores are optimistic.

## Data

- 768 rows and 9 columns: the target `Outcome` and 8 numeric features (Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age). There are no categorical, date/time or identifier columns.
- Target split: Outcome=0 is 65.1% (500 rows) and Outcome=1 is 34.9% (268 rows).
- No cells are empty. Five columns contain zeros, which are physiologically implausible for Glucose, BloodPressure, SkinThickness, Insulin and BMI. They are treated as suspected missing-value codes:
  - Insulin: 374 zeros (48.7%)
  - SkinThickness: 227 zeros (29.56%)
  - BloodPressure: 35 zeros (4.56%)
  - BMI: 11 zeros (1.43%)
  - Glucose: 5 zeros (0.65%)
- Pregnancies has 111 zeros, and these were not among the columns flagged as suspect. DiabetesPedigreeFunction and Age have no zeros.

## Findings

### 1. Outcome=1 rate across each feature's range

Outcome=1 rates within quartile bins of each feature (eda_1):

- **Glucose:** 8.1% (up to 99), 24.7% (99 to 117), 38.9% (117 to 140.25), 68.8% (140.25 to 199). The rate rises steeply across bins.
- **BMI:** 10.3% (up to 27.3), 35.9% (27.3 to 32.0), 45.4% (32.0 to 36.6), 48.4% (36.6 to 67.1).
- **Age:** 14.2% (21 to 24), 29.9% (24 to 29), 47.5% (29 to 41), 51.7% (41 to 81). The rate rises with age.
- **Pregnancies:** 27.2% (0 to 1), 25.8% (1 to 3), 34.3% (3 to 6), 56.2% (6 to 17). The second bin is slightly lower than the first.
- **BloodPressure:** 25.4% (up to 62), 33.6% (62 to 72), 35.9% (72 to 80), 46.7% (80 to 122). The rate rises with each bin.
- **SkinThickness:** 28.8% (up to 23), 35.9% (23 to 32), 46.8% (32 to 99). The lowest bin includes the zero-coded rows.
- **DiabetesPedigreeFunction:** 25.5%, 33.3%, 32.3%, 48.4% across the quartile bins. The rate rises overall but not between the middle two bins.
- **Insulin:** 36.5% (up to 30.5, a bin that is largely zeros), 16.1% (30.5 to 127.25), 50.5% (127.25 to 846). The pattern is non-monotonic. eda_1 judged the lowest bin likely to be driven by zero coding, and the non-zero pattern is examined in Section 3.

Note: the eda_1 text and its bin table give different counts for the top Glucose bin (194 vs 192) and the top BMI bin (192 vs 188). Bin counts are therefore omitted here, and the rates are reported as recorded.

![Share of Outcome=1 (%) within quartile bins of Glucose, BMI and Age](tasks/eda_1/charts/eda1_rate_by_quartile.png)

### 2. Zero values as missing data

- The analysis judged zeros in Glucose, BloodPressure, SkinThickness, Insulin and BMI to be missing-value codes, based on physiology and on differences in other features between zero and non-zero rows. This is a judgement, not a tested result. No test of co-occurrence or randomness was run.
- Zero rows differ from non-zero rows on other features in mean. For example, zero BloodPressure rows have mean SkinThickness 1.514 against 21.445 for non-zero rows, and zero BMI rows have mean BloodPressure 28.8 against 69.7.
- Outcome=1 rates for zero vs non-zero rows are descriptive only, with no significance test:
  - Glucose: 40.0% vs 34.9% (5 zero rows; too few to be reliable)
  - BloodPressure: 45.7% vs 34.4% (35 zero rows)
  - SkinThickness: 38.8% vs 33.3% (227 zero rows)
  - Insulin: 36.9% vs 33.0% (374 zero rows)
  - BMI: 18.2% vs 35.1% (11 zero rows; the direction reverses, but the count is too small to be reliable)

![Outcome=1 rate for rows where each column is zero vs non-zero](tasks/eda_2/charts/outcome_rate_zero_vs_nonzero.png)

### 3. Insulin and SkinThickness after zeros are treated as missing

- **Insulin (non-zero rows, n=394):** the Outcome=1 rate still rises across quartile bins: 8.1% (14 to 76, n=99), 23.2% (76 to 125, n=99), 48.5% (125 to 190, n=99), 52.6% (190 to 846, n=97). The largest step is between the second and third bins. No significance test was run.
- **SkinThickness (non-zero rows, n=541):** the rate also rises: 15.3% (7 to 22, n=150), 31.8% (22 to 29, n=126), 42.5% (29 to 36, n=134), 45.8% (36 to 99, n=131). The largest gain is in the first two bins. No significance test was run.
- The zero-row rates (36.9% for Insulin, 38.8% for SkinThickness) fall within the non-zero bin range. Only the lowest non-zero bin is clearly lower. eda_3 concludes that the zero codes do not explain the rising pattern. Treating zeros as a separate group or imputing them is described as a judgement based on this, not a demonstrated result.

![Outcome=1 rate by quartile of non-zero Insulin and SkinThickness, zeros treated as missing](tasks/eda_3/charts/eda3_nonzero_bins.png)

### 4. Which features differ between Outcome=1 and Outcome=0

Mann-Whitney tests with rank-biserial effect sizes on all rows (positive means higher in Outcome=1). Seven of the eight features remain significant after Holm correction across the eight tests.

- **Glucose:** rank-biserial 0.576 (95% bootstrap CI 0.513 to 0.645). Medians 140 vs 107, p = 1.2e-39. The largest separation of the eight features.
- **BMI:** 0.375 (95% bootstrap CI 0.293 to 0.445). Medians 34.25 vs 30.05, p = 9.7e-18.
- **Age:** 0.374 (95% bootstrap CI 0.297 to 0.448). Medians 36 vs 27, p = 1.1e-17.
- **Pregnancies:** 0.239 (95% bootstrap CI 0.153 to 0.322). Medians 4 vs 2, p = 3.7e-8.
- **DiabetesPedigreeFunction:** 0.212 (95% bootstrap CI 0.133 to 0.299). Medians 0.449 vs 0.336, p = 1.2e-6.
- **BloodPressure:** 0.173 (95% bootstrap CI 0.086 to 0.255). Medians 74 vs 70, p = 7.6e-5.
- **SkinThickness:** 0.107 (95% bootstrap CI 0.022 to 0.199). Medians 27 vs 21, p = 0.013. Adjusted p = 0.026, significant only just.
- **Insulin:** 0.076 (95% bootstrap CI -0.009 to 0.160), p = 0.066. Not significant after Holm correction. Raw medians are 0 vs 39.

![Rank-biserial effect size with 95% bootstrap CI for each of the 8 numeric features, Outcome=1 versus Outcome=0. Positive values mean higher values in Outcome=1.](tasks/stat_1/charts/stat1_rank_biserial.png)

**Non-zero rows only (sensitivity check).** Excluding zero-coded rows changes the picture for some features:

- **Glucose:** 0.586 (95% bootstrap CI 0.516 to 0.652), p = 1.3e-40. Unchanged from the all-rows estimate.
- **BMI:** 0.374 (95% bootstrap CI 0.301 to 0.448), p = 1.8e-17. Unchanged.
- **BloodPressure:** 0.215 (95% bootstrap CI 0.133 to 0.300), p = 1.6e-6. Larger than the all-rows estimate; the conclusion of a small but significant effect holds.
- **SkinThickness:** 0.325 (95% bootstrap CI 0.233 to 0.417), p = 7.0e-10. Larger than the all-rows estimate, which stat_3 describes as about three times as large. On non-zero rows the effect is small to medium, not "very small, barely significant."

These estimates describe the non-zero subsets. Excluding zeros removes rows selectively and is not a correction for zero-coded missing values.

![Rank-biserial effect with 95% bootstrap CI on non-zero rows for BloodPressure, SkinThickness, Glucose and BMI, Outcome=1 versus Outcome=0](tasks/stat_3/charts/stat3_rank_biserial_nonzero.png)

### 5. Feature interactions

- **Glucose × BMI: not significant.** On the main fit, which includes zero-coded rows, the interaction coefficient is -0.168 on z-scored predictors (95% CI -0.415 to 0.079), Wald p = 0.18, LR p = 0.18. AIC is 777.4 without the term and 777.6 with it. On non-zero rows only, the coefficient is -0.074 (95% CI -0.297 to 0.148), Wald p = 0.51. The 2×2 median-split rates on the main fit are 10.4% (low Glucose/low BMI), 24.8% (low Glucose/high BMI), 41.7% (high Glucose/low BMI) and 62.9% (high/high). On non-zero rows they are 10.8%, 23.7%, 42.6% and 62.6%. Each feature's effect is similar across levels of the other.
- **Age × Pregnancies: significant.** The coefficient is -0.270 on z-scored predictors (95% CI -0.449 to -0.090), Wald p = 0.003, LR p = 0.003. AIC falls from 947.1 without the term to 940.3 with it. The 2×2 median-split rates (median Age 29, median Pregnancies 3) are 20.0% (low Age/low Pregnancies, n=330), 27.3% (low Age/high Pregnancies, n=66), 50.0% (high Age/low Pregnancies, n=94) and 49.3% (high Age/high Pregnancies, n=278). Above the median age, the rate is high regardless of Pregnancies. The negative interaction means the Pregnancies association is weaker at older ages. The analysis notes that this interaction is worth breaking down further.

![Proportion of Outcome=1 in each high/low median-split cell (high = above median) for Glucose x BMI and Age x Pregnancies](tasks/stat_2/charts/stat2_2x2_rates.png)

### 6. Predicting Outcome against the majority-class baseline

Evaluated on a stratified 20% test split (n=154; training n=614). The majority-class baseline on the test split is 64.9%.

- **Standardized logistic regression:** test accuracy 71.4% (train 79.2%), precision 60.9%, recall 51.9%, F1 0.560, ROC AUC 0.823.
- **Random forest (500 trees):** test accuracy 73.4% (train 100%), precision 62.8%, recall 59.3%, F1 0.610, ROC AUC 0.814. The forest overfits, so its test metrics and importances are less reliable than the logistic results.

Standardized logistic coefficients as recorded: Glucose 1.144, BMI 0.714, Pregnancies 0.373, DiabetesPedigreeFunction 0.256, Age 0.184, Insulin -0.127, SkinThickness 0.067, BloodPressure -0.198. The finding text describes seven coefficients as positive and BloodPressure as negative, but the recorded values also show Insulin as negative. This disagreement is reported under Limitations.

Random forest permutation importance (mean drop in test ROC AUC over 30 repeats, with SD):

- Glucose 0.101 (SD 0.023)
- BMI 0.041 (SD 0.018)
- Age 0.029 (SD 0.013)
- Insulin 0.009 (SD 0.005)
- Pregnancies 0.007 (SD 0.010)
- DiabetesPedigreeFunction 0.006 (SD 0.007)
- BloodPressure 0.005 (SD 0.007)
- SkinThickness -0.004 (SD 0.005)

Glucose and BMI are the top two predictors in both models. The rankings of the other features differ between the models and should not be relied on for ordering. All models were fitted on the zero-coded values as recorded.

![Random forest permutation importance on the test set for the 8 numeric features; bars are the mean drop in ROC AUC when a feature is shuffled, error bars 1 SD over 30 repeats](tasks/ml_1/charts/ml1_rf_permutation_importance.png)

## Limitations

- **Zero-coded values were used as recorded in the main analyses.** The main logistic interaction fit, the univariate tests on all rows, and both models include zeros. The missing-value interpretation of zeros is a judgement from physiology and mean differences. The co-occurrence and randomness of zeros were not tested.
- **Zero-coded values may distort the model coefficients.** The Insulin and SkinThickness coefficients may reflect the zero coding and should not be read as real effects. The models have not been refitted with zeros treated as missing.
- **BloodPressure sign conflict (unresolved).** The logistic coefficient for BloodPressure is negative (-0.198), while its univariate association is positive (rank-biserial 0.173, p = 7.6e-5). The conflict is unexplained. Collinearity with BMI or Age, and distortion by zero values, have not been tested. The lead's review issue on the ml_1 finding is unresolved. It asks that the sentence stating all coefficients are in the Outcome=1 direction be removed, because BloodPressure is negative, and that the note say seven coefficients are positive and BloodPressure is negative. The recorded coefficients disagree with that note: Insulin is recorded as -0.127 as well as BloodPressure as -0.198, so two coefficients are negative, not one. The finding text lists Insulin as 0.127. The two sources disagree on Insulin's sign, and this report does not resolve it.
- **Descriptive-only rates.** The zero vs non-zero Outcome=1 rates (eda_2) and the non-zero quartile rates for Insulin and SkinThickness (eda_3) have no significance tests. The rising pattern in eda_3 was not tested for trend.
- **Small zero-BMI and zero-Glucose groups.** The lower Outcome=1 rate for zero-BMI rows (18.2%) rests on 11 rows and is not reliable. The zero-Glucose comparison (5 rows) is likewise too small to interpret.
- **Non-zero exclusions are selective.** The stat_3 estimates describe the non-zero subsets and do not correct for zero-coded missingness. Their differences from the all-rows estimates (notably SkinThickness) should be read with that in mind.
- **Interaction analyses were not adjusted for other features.** The Age × Pregnancies and Glucose × BMI interactions were tested with the two features only (z-scored). Their effects after adjusting for other features are not known.
- **Model limitations.** The test split has 154 rows and is a single split. The random forest overfits (train accuracy 1.0), so its metrics and permutation importances are optimistic.
- **Bin counts in eda_1.** The eda_1 text and bin table disagree on two bin counts (top Glucose and top BMI quartiles), so counts are omitted for those bins.
- **No tasks failed.** All seven analysis tasks completed.

## Open questions

- Does the Insulin and SkinThickness contribution change when zeros are imputed or kept as a separate indicator group, and how does each choice change model performance?
- Is the rise in Outcome=1 rate across non-zero Insulin and SkinThickness bins statistically significant (for example, under a trend test), and does it hold after adjusting for Glucose, BMI and Age?
- Do Insulin and SkinThickness carry overlapping signal, given that zero SkinThickness co-occurs with zero Insulin in some rows?
- Is the negative BloodPressure logistic coefficient explained by collinearity with BMI or Age in a multivariable model with adjusted odds ratios and confidence intervals?
- Does the Age × Pregnancies interaction hold after adjusting for Glucose, BMI and the other features? Is it driven by a few high-parity or older rows, and does it survive a non-median or spline-based split?
- How much of the Glucose, BMI, Age and Pregnancies effects remain after adjusting for each other, for example in a multivariable logistic regression?
- Does the large SkinThickness effect on non-zero rows persist after adjusting for BMI and other features?
- Do results on non-zero rows differ from a sensitivity analysis that imputes zeros as missing rather than dropping them?
- Are the zero-BloodPressure and zero-SkinThickness rows a distinct subgroup with a different Outcome rate, tested formally?
- Is the lower Outcome=1 rate in zero-BMI rows stable, given that only 11 rows are involved?