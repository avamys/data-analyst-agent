# Pima Diabetes Dataset: Clinical Predictors of Outcome (Diabetes, Binary)

## Summary

- **Glucose separates the two outcome groups most strongly.** The Outcome=1 rate rises from 7.3% in the Glucose <100 band to 59.3% in the 126-199 band. The rank-biserial effect for Glucose is 0.586 (95% CI 0.526 to 0.639, Bonferroni p = 1.0e-39). Age, BMI, Insulin and SkinThickness also differ significantly, with smaller effects.
- **Zero values are common and are treated as missing.** 376 of 768 rows (49%) have at least one physiologically impossible zero. Insulin has 374 zeros (48.7%). The zero-coded rows differ from other rows on Age, BMI, Pregnancies and DiabetesPedigreeFunction.
- **Two models beat the majority-class baseline (0.649) on one 154-row test split.** Random forest reaches test accuracy 0.740 and AUC 0.816, but its train accuracy is 1.0, so these scores are optimistic. Logistic regression reaches test accuracy 0.708 and AUC 0.813. Glucose ranks first in both models.
- **Neither BMI nor Age changes the Glucose-Outcome association in a jointly significant way.** The joint likelihood-ratio test gives p = 0.130 (n = 752). The Glucose x Age term alone is nominally significant (p = 0.040) and should be treated as exploratory.
- **Some band differences are robust and others are not.** The Pregnancies 1-2 dip is statistically distinguishable from neighbouring bands, but it is post hoc. The Age 50+ drop below 40-49 is not distinguishable from noise (p = 0.33).

## Data

- 768 rows and 9 columns: 8 numeric clinical features (Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age) and one binary target, Outcome.
- The dataset has no categorical, date/time, identifier or free-text columns, and no missing values in the frame.
- Outcome is 65.1% 0 (500 rows) and 34.9% 1 (268 rows).
- Zeros in Glucose, BloodPressure, SkinThickness, Insulin and BMI are physiologically impossible and act as disguised missing values. The "Zero-coded values" subsection gives the counts.

## Findings

### Feature means by Outcome

The means below are computed on all values, including zeros. For the zero-coded columns (Glucose, BloodPressure, SkinThickness, Insulin, BMI), these means are biased low and should not be read as true means.

| Feature | Outcome=0 | Outcome=1 |
|---|---|---|
| Pregnancies | 3.30 | 4.87 |
| Glucose | 109.98 | 141.26 |
| BloodPressure | 68.18 | 70.82 |
| SkinThickness | 19.66 | 22.16 |
| Insulin | 68.79 | 100.34 |
| BMI | 30.30 | 35.14 |
| DiabetesPedigreeFunction | 0.430 | 0.551 |
| Age | 31.19 | 37.07 |

Glucose medians are 107 for Outcome=0 and 140 for Outcome=1 (zeros included).

### Outcome rates across bands

- **Glucose** (5 zeros excluded, 763 rows banded; no rows at 200+):
  - <100: 7.3% (n = 192)
  - 100-125: 27.7% (n = 274)
  - 126-199: 59.3% (n = 297)
- **BMI** (11 zeros excluded, 757 rows banded):
  - <18.5: 0.0% (n = 4; too few rows to interpret)
  - 18.5-24.9: 6.9% (n = 102)
  - 25-29.9: 22.3% (n = 179)
  - 30+: 46.4% (n = 472, 219 cases; this band uses >=30, whereas the test in stat_1 uses >30)
- **Age:**
  - <30: 21.2% (n = 396)
  - 30-39: 46.1% (n = 165)
  - 40-49: 55.1% (n = 118)
  - 50+: 48.3% (n = 89, 43 cases)
  - The 50+ rate is below the 40-49 rate. An earlier "higher again" description is withdrawn.
- **Pregnancies:**
  - 0: 34.2% (n = 111)
  - 1-2: 20.2% (n = 238)
  - 3-5: 35.5% (n = 200)
  - 6+: 50.7% (n = 219)
  - The rate is not monotonic and dips at 1-2. Wilson intervals and tests for this dip are in the band-uncertainty section.

![Glucose histogram (counts) for Outcome=0 and Outcome=1](tasks/eda_1/charts/glucose_by_outcome.png)

### Zero-coded values

Counts of zeros, and the Outcome=1 rate for zero versus nonzero rows:

| Column | Zeros (% of 768) | Outcome=1 rate, zero rows | Outcome=1 rate, nonzero rows |
|---|---|---|---|
| Glucose | 5 (0.65%) | 0.400 | 0.349 |
| BloodPressure | 35 (4.56%) | 0.457 | 0.344 |
| SkinThickness | 227 (29.56%) | 0.388 | 0.333 |
| Insulin | 374 (48.70%) | 0.369 | 0.330 |
| BMI | 11 (1.43%) | 0.182 | 0.351 |

- These are descriptive comparisons. No significance test was run for each column. The Glucose zero group (n = 5) and the BMI zero group (n = 11) are too small to support any conclusion.
- Zeros overlap strongly. 376 rows (49%) have at least one zero, 392 rows have none, and 227 rows have both SkinThickness and Insulin at zero. Under independence, the expected SkinThickness-and-Insulin co-zero count is 110.5, based on the marginal counts of 227 and 374 out of 768. The data do not show the cause of this clustering.
- The team recommends converting these zeros to NaN and imputing the median fitted on the training split only. Rows are not dropped.
- For the 227 rows with both SkinThickness and Insulin at zero, the Outcome=1 rate is 38.8%, compared with 33.3% in the remaining rows (see "Missingness of zero-coded rows").

### Which features separate Outcome=0 from Outcome=1

Mann-Whitney U tests, two-sided, with zeros set to NaN. Each test uses only non-missing rows. Rank-biserial effects have approximate 95% CIs. Bonferroni p-values are over 8 features.

| Feature | n (Outcome 0 / 1) | Rank-biserial (95% CI) | Bonferroni p |
|---|---|---|---|
| Glucose | 497 / 266 | 0.586 (0.526 to 0.639) | 1.0e-39 |
| Insulin | 264 / 130 | 0.463 (0.363 to 0.553) | 6.0e-13 |
| Age | 500 / 268 | 0.374 (0.298 to 0.445) | 9.1e-17 |
| BMI | 491 / 266 | 0.374 (0.298 to 0.446) | 1.5e-16 |
| SkinThickness | 361 / 180 | 0.325 (0.230 to 0.414) | 5.6e-9 |
| Pregnancies | 500 / 268 | 0.239 (0.157 to 0.318) | 3.0e-7 |
| BloodPressure | 481 / 252 | 0.215 (0.130 to 0.297) | 1.3e-5 |
| DiabetesPedigreeFunction | 500 / 268 | 0.212 (0.129 to 0.293) | 9.6e-6 |

All eight features are significant after Bonferroni adjustment. Insulin has the most missingness, so its estimate rests on 264 vs 130 rows. Glucose median is 107 vs 140 (zeros set to NaN, n = 497 vs 266).

Binned tests:
- **Age over 40 (strict >40):** Outcome=1 rate 52.6% (n = 194) vs 28.9% (n = 574). Difference 0.237 (Wald 95% CI 0.157 to 0.316), chi-square 35.7, p = 2.3e-9, Bonferroni p = 4.6e-9 (2 bins).
- **BMI over 30 (strict >30, 11 zero-coded rows excluded):** Outcome=1 rate 46.2% (n = 465) vs 17.5% (n = 292). Difference 0.288 (Wald 95% CI 0.225 to 0.351), chi-square 65.1, p = 7.0e-16, Bonferroni p = 1.4e-15 (2 bins). The upper CI bound is 0.3506 in the full record and is reported here as 0.351. The 472-row, 219-case count from eda_1 uses a different cutoff and is not directly comparable.

![Rank-biserial effect size per feature, zeros as NaN](tasks/stat_1/charts/effect_sizes.png)

### Glucose, BMI and Age interaction

Analysis sample: rows with zero-coded Glucose or BMI were dropped, and rows with any missing value among Glucose, BMI, Age or Outcome were excluded, leaving n = 752. Logistic regression with standardized predictors; odds ratios are per standard deviation.

- **Main effects (adjusted):** Glucose OR 3.149 (95% CI 2.517 to 3.939), BMI OR 1.844 (1.513 to 2.248), Age OR 1.465 (1.220 to 1.759). All p < 0.001.
- **Glucose x BMI:** OR 0.946 (0.754 to 1.188), p = 0.635. Not significant.
- **Glucose x Age:** OR 0.814 (0.668 to 0.991), p = 0.040 on its own. Jointly with the BMI term, the likelihood-ratio test gives chi-square 4.087 on 2 df, p = 0.130. It would not survive correction for the two tests and is exploratory.
- **Tertile rates** (Glucose tertile cut-points from the analysis sample; BMI split at its median):

| Glucose tertile | BMI-low stratum | BMI-high stratum |
|---|---|---|
| Low | 6.7% (n = 150) | 19.4% (n = 103) |
| Mid | 24.0% (n = 129) | 36.7% (n = 120) |
| High | 50.0% (n = 98) | 72.4% (n = 152) |

The Outcome=1 rate rises across Glucose tertiles in both BMI strata. The high-vs-low gap is larger in the BMI-high stratum (0.53 vs 0.43, as stated in the stat_2 finding). This is consistent with the non-significant Glucose x BMI term but was not tested.

![Outcome=1 rate by Glucose tertile, split by median BMI](tasks/stat_2/charts/tertile_bmi_rates.png)

### Band uncertainty: Age and Pregnancies

Wilson 95% CIs for the Outcome=1 rate:

- **Age:** <30: 21.2% (17.5 to 25.5, n = 396); 30-39: 46.1% (38.6 to 53.7, n = 165); 40-49: 55.1% (46.1 to 63.8, n = 118); 50+: 48.3% (38.2 to 58.5, n = 89). Bands differ overall (chi-square 69.9, 3 df, p < 0.001).
  - 40-49 minus 50+: +6.8 points (95% CI -7.0 to +20.5, p = 0.33). Not distinguishable from noise.
  - 40-49 minus 30-39: +9.0 points (95% CI -2.7 to +20.8, p = 0.13). Not distinguishable from noise.
  - Both pairwise tests are unadjusted and exploratory.
- **Pregnancies:** 0: 34.2% (26.1 to 43.5, n = 111); 1-2: 20.2% (15.6 to 25.7, n = 238); 3-5: 35.5% (29.2 to 42.3, n = 200); 6+: 50.7% (44.1 to 57.2, n = 219). Bands differ overall (chi-square 46.8, 3 df, p < 0.001).
  - 1-2 minus 0: -14.1 points (95% CI -24.3 to -3.9), unadjusted p = 0.007.
  - 1-2 minus 3-5: -15.3 points (95% CI -23.7 to -7.0), unadjusted p = 0.0003.
  - The stat_3 finding states that both comparisons would pass a Bonferroni correction over the two comparisons; the adjusted values are not in the facts record. The dip is post hoc and was not adjusted for Age or Glucose. It should be confirmed on new data.

![Outcome=1 rate by Age and Pregnancies band, with 95% Wilson confidence intervals (rates, not counts)](tasks/stat_3/charts/band_rates_ci.png)

### Missingness of zero-coded rows

Rows with zero-coded SkinThickness and Insulin (n = 227) compared with the other rows:

- **Outcome:** 38.8% vs 33.3%. Risk difference +5.5 points (Wald 95% CI -2.0 to +13.0), chi-square p = 0.17. Not distinguishable from zero, but the CI does not rule out a sizable effect in either direction.
- **Other features** (medians, zero-coded rows vs rest; bootstrap CI of the median difference; rank-biserial; Mann-Whitney p):
  - Age: 34 vs 28; difference 6 (CI 4.0 to 10.0); rank-biserial 0.28; p < 0.001.
  - Pregnancies: 4 vs 2; difference 2 (CI 1 to 3); rank-biserial 0.21; p < 0.001.
  - BMI: 30.4 vs 32.8; difference -2.4 (CI -3.4 to -0.9); rank-biserial -0.17; p < 0.001.
  - DiabetesPedigreeFunction: 0.282 vs 0.417; difference -0.135 (CI -0.172 to -0.086); rank-biserial -0.23; p < 0.001.
  - Glucose: 120 vs 115; difference 5 (CI 0 to 12); rank-biserial 0.09; p = 0.057. No clear difference.
  - BloodPressure: 72 vs 72; difference 0 (CI -2 to 4); rank-biserial -0.01; p = 0.81. No clear difference.

The values for Age, BMI, DiabetesPedigreeFunction, Glucose and BloodPressure match the stat_4 comparison record.

The zero-coded rows differ systematically on Age, BMI, Pregnancies and DiabetesPedigreeFunction. The team describes this as consistent with missingness at random conditional on those variables. MNAR cannot be established from observed data.

Implications for earlier results:
- The stat_1 Mann-Whitney results for SkinThickness and Insulin are computed on a non-random subset (rows with a real value), not on zero-coded values. Because the zero-coded rows differ on Age, BMI, Pregnancies and DiabetesPedigreeFunction, those estimates may be biased by that selection.
- Zero-coded means for SkinThickness and Insulin are biased downward if zeros are included. If only nonzero rows are averaged, the estimate reflects the younger, higher-BMI subgroup.

### Predictive models

One stratified 80/20 split (random_state = 42): 614 training rows, 154 test rows. Majority-class baseline on the test split: 0.649.

| Model | Train accuracy | Test accuracy | Precision | Recall | F1 | ROC AUC |
|---|---|---|---|---|---|---|
| Random forest (300 trees) | 1.0 | 0.740 | 0.659 | 0.537 | 0.592 | 0.816 |
| Logistic regression (standardized) | 0.796 | 0.708 | 0.600 | 0.500 | 0.545 | 0.813 |

- The random forest's train-test gap (1.0 vs 0.740) means its test metrics and importances are optimistic. Both models give modest discrimination.
- Random forest permutation importance (drop in test ROC AUC, 30 repeats; mean and sd): Glucose 0.095 (0.020); BMI 0.046 (0.019); Age 0.029 (0.011); Insulin 0.012 (0.010); DiabetesPedigreeFunction 0.009 (0.007); Pregnancies 0.008 (0.009); BloodPressure 0.002 (0.006); SkinThickness 0.0001 (0.006).
- Logistic regression standardized coefficients (absolute value): Glucose 1.183; BMI 0.689; Pregnancies 0.377; DiabetesPedigreeFunction 0.233; Age 0.148; Insulin 0.066; BloodPressure 0.044; SkinThickness 0.028.
- Glucose and BMI rank first and second in both models, but the two models use different importance measures.
- The orders disagree beyond the top two. Age is fifth in logistic regression but third in random forest permutation importance. Pregnancies and DiabetesPedigreeFunction also rank differently.
- No uncertainty is given for the accuracy or AUC estimates. The difference between the random forest (AUC 0.816) and logistic regression (0.813) is not established as reliable.

![Random forest permutation importance, test split, ROC AUC drop per feature](tasks/ml_1/charts/ml1_permutation_importance.png)

## Limitations

- **Zero handling differs across analyses.** The eda and stat_1 analyses set zeros to NaN and use non-missing rows. The stat_2 analysis drops rows (n = 752). The logistic regression in ml_1 uses median-imputed zeros. Results are not on a common sample.
- **Zero-coded rows are not missing at random in the observed data.** They differ on Age, BMI, Pregnancies and DiabetesPedigreeFunction. Estimates on the non-zero subset for SkinThickness and Insulin may be biased by this selection.
- **Very small groups.** The Glucose zero group (n = 5), the BMI zero group (n = 11) and the BMI <18.5 band (n = 4) are too small to support conclusions. The BMI zero-row rate of 0.182 (n = 11) may be noise.
- **Zero-column associations are descriptive.** No per-column significance test was run for the Outcome rates of zero and nonzero rows. The stat_4 test covers only the rows with both SkinThickness and Insulin at zero.
- **Glucose x Age is exploratory.** p = 0.040 does not survive correction, and the joint interaction test is p = 0.130.
- **Post hoc band comparisons.** The Pregnancies 1-2 dip and the Age 40-49 vs 50+ comparison were not adjusted for Age or Glucose. The 50+ band has n = 89. The Pregnancies comparisons are post hoc and need confirmation on new data.
- **Cutoff inconsistency.** The BMI 30+ band in eda_1 uses >=30. The test in stat_1 uses >30. The counts are not directly comparable.
- **Model evaluation.** All model results come from one 154-row split. The random forest overfits (train accuracy 1.0). No cross-validation or repeated splits were run, and no tuning was done.
- **Multiple comparisons.** Mann-Whitney tests are Bonferroni-adjusted over 8 features and binned tests over 2 bins. No correction was applied across the full family of tests in the report.
- **Failed or partial work.** The stat_4 task is partial. Its missingness conclusion is limited to the observed comparisons described above.
- **Unresolved review issues:**
  - **eda_1:** The lead asked for the Outcome=0 vs Outcome=1 means for every numeric feature, with zeros included. These means are reported in the Findings section, and they are biased for the zero-coded columns. The eda_1 output itself has not been revised.
  - **eda_2:** The lead asked for three changes: describe the Outcome-association findings as descriptive and say no test was run; flag the Glucose (n = 5) and BMI (n = 11) zero groups as too small; and report the expected SkinThickness-and-Insulin co-zero count under independence. The first two are reflected in the Findings. The third is reflected as 110.5 next to the observed 227. The eda_2 output itself has not been revised.
  - **stat_4:** The lead asked for a correction to the implications paragraph, stating that the stat_1 SkinThickness and Insulin results are computed on a non-random subset rather than comparing fake values. The corrected text is in the Findings. The lead also asked for confirmation of the Age, BMI, DiabetesPedigreeFunction, Glucose and BloodPressure statistics, which was done against the stat_4 record.
- **Unchecked upper CI bound.** The stat_1 BMI-over-30 upper bound was recorded as 0.350 in the summary text. The full record gives 0.3506, reported here as 0.351.

## Open questions

- Is the Pregnancies 1-2 dip robust after adjusting for Age and Glucose (for example, with logistic regression)?
- Is the Age 50+ drop from 40-49 real, or noise? More data is needed, since the 50+ band has n = 89.
- Is the Glucose x Age interaction (p = 0.040) robust to a different coding of Age, to splitting Age into bins, or to tertiles within age strata?
- Does the Glucose-Outcome association hold after median or model-based imputation of zero-coded Glucose and BMI, instead of dropping rows?
- Do zero-coded SkinThickness and Insulin values distort the Outcome relationship after imputation? This would require re-running on complete cases and with multiple imputation.
- Is missingness of the zero-coded rows explained by observed variables? A logistic model of the zero-both indicator on Age, BMI, Pregnancies and DiabetesPedigreeFunction has not been fitted.
- Do the zero-coded SkinThickness and Insulin rows cluster by Age group or BMI class?
- Do the zero-coded values indicate missing data that needs handling? The team recommends NaN conversion and median imputation, but the effect of that choice on the models has not been checked.
- Does the random forest vs logistic regression difference (AUC 0.816 vs 0.813) hold under cross-validation? Would tuning the random forest reduce the train-test gap and change the importance ranking?
- What are Cohen's d and its CI for Glucose after NaN conversion, as a cross-check of the rank-biserial result?