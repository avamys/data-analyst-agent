# Outcome Prediction in a 768-Patient Numeric Dataset: Feature Associations, Interactions and Models

## Summary

- **Glucose is the strongest single feature.** Its Cohen d is 1.105 and its rank-biserial correlation is 0.576. BMI and Age follow. In the adjusted logistic model, Glucose keeps the largest association (OR 3.08 per SD with zeros as recorded; 3.25 with zeros set to missing and complete-case analysis).
- **Both models beat the majority-class baseline** (test accuracy 0.649). Logistic regression reached 0.708 accuracy and 0.813 ROC AUC; the random forest reached 0.734 and 0.816. The test set has only 154 rows, and the random forest overfits (train accuracy 1.0).
- **Age × Pregnancies is the interaction that holds up best.** It is significant after Holm correction in both the zeros-kept analysis (Holm p = 0.011) and the complete-case analysis (Holm p = 0.018). Glucose × DiabetesPedigreeFunction is borderline: Holm p = 0.048 on complete cases, 0.061 with zeros kept.
- **Implausible zeros are common in two columns.** Insulin is zero in 48.7% of rows and SkinThickness in 29.6%. Zero status is not significantly related to Outcome in any of the five columns. Age does predict whether Insulin and SkinThickness are both zero (OR 1.035 per year, p = 7.4e-6). Treating zeros as missing is recommended, but the sensitivity of the results to this choice was not tested.

## Data

- 768 rows × 9 columns: 8 numeric features (Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age) and a binary target, Outcome. There are no categorical, date or identifier columns.
- Outcome: 0 for 65.1% of rows and 1 for 34.9% (268 of 768), so the classes are moderately imbalanced.
- The profile reports no missing values. However, zeros in Glucose, BloodPressure, SkinThickness, Insulin and BMI are physiologically impossible and are treated here as probable missing values (see Findings, section 6).

## Findings

### 1. Univariate patterns by Outcome

- **Glucose:** median 107 for Outcome 0 versus 140 for Outcome 1. The positive rate rises from 8.8% in the lowest quintile to 74.3% in the highest.
- **BMI:** median 30.05 versus 34.25. The positive rate rises from 9.0% to 51.3%, with a plateau around 43–45% in the middle-upper bins.
- **Age:** median 27 versus 36. The positive rate rises from 13.3% to 53.2%.
- **Pregnancies:** median 2 versus 4. The positive rate is 27.2% in the lowest bin, 18.4% in the second, then rises to 56.5% in the highest.
- **DiabetesPedigreeFunction:** median 0.336 versus 0.449. The positive rate rises from 22.1% to 49.7%.
- **BloodPressure:** median 70 versus 74. The positive rate rises monotonically from 24.7% to 47.4%, a weaker gradient than Glucose, BMI and Age.
- **SkinThickness:** median 21 versus 27. Positive rates across the four bins are 31.3%, 26.7%, 38.9% and 46.9%. The lowest bin contains 320 rows, of which 227 are SkinThickness = 0, so that bin is mostly coded missing values and its low-end pattern is not a substantive finding.
- **Insulin:** the positive rate is 36.9% for zero rows and 33.0% for nonzero rows (chi-square χ² = 1.287, p = 0.257, not significant). Among nonzero values, the positive rate rises from 8.1% in the lowest quartile to 52.6% in the highest. The Outcome 1 median of Insulin is 0 because 51.5% of positives (138 of 268) have zero Insulin, against 47.2% of negatives (stat_1 recomputation; eda_1 reported 47.6%). The median reflects that zeros are about half of each class, not a higher zero rate.

![Distribution of each numeric feature for Outcome 0 and Outcome 1 (density histograms)](tasks/eda_1/charts/eda1_feature_distributions_by_outcome.png)

### 2. Significance and effect sizes

Outcome 1 minus Outcome 0. P-values are Holm-adjusted across the eight features. MWU = Mann-Whitney U; Welch = Welch t-test.

| Feature | Cohen d | Rank-biserial | Mean difference (95% CI) | Median difference | MWU Holm p | Welch Holm p |
|---|---|---|---|---|---|---|
| Glucose | 1.105 | 0.576 | 31.28 (26.81 to 35.75) | 33 | 9.6e-39 | 2.1e-35 |
| BMI | 0.641 | 0.375 | 4.84 (3.74 to 5.94) | 4.2 | 6.8e-17 | 4.6e-16 |
| Age | 0.514 | 0.374 | 5.88 (4.21 to 7.55) | 9 | 6.9e-17 | 7.2e-11 |
| Pregnancies | 0.477 | 0.239 | 1.57 (1.05 to 2.09) | 2 | 1.9e-07 | 3.4e-08 |
| DiabetesPedigreeFunction | 0.370 | 0.212 | 0.121 (0.069 to 0.173) | 0.113 | 4.8e-06 | 2.4e-05 |
| Insulin | 0.276 | 0.076 | 31.54 (12.76 to 50.33) | −39 | 0.066 | 0.003 |
| SkinThickness | 0.157 | 0.107 | 2.50 (0.01 to 4.99) | 6 | 0.026 | 0.099 |
| BloodPressure | 0.137 | 0.173 | 2.64 (−0.39 to 5.67) | 4 | 0.0002 | 0.099 |

- The top five features are the same under Cohen d and rank-biserial. The bottom three swap order: by Cohen d the order is Insulin, SkinThickness, BloodPressure; by rank-biserial it is BloodPressure, SkinThickness, Insulin.
- **Insulin results disagree.** The Welch test is significant (Holm p = 0.003) but the Mann-Whitney test is not (Holm p = 0.066), and the median difference is −39. The finding's authors attribute the mean difference to the zero-heavy distribution rather than a rank shift, so the effect is weak and unsettled.
- **SkinThickness and BloodPressure results disagree.** Both are significant under Mann-Whitney after Holm correction but not under Welch (Holm p = 0.099 for each). The BloodPressure mean difference CI includes zero.
- All eight features are higher on average in Outcome 1.

![Rank-biserial effect size per feature, Outcome 1 vs Outcome 0; features ordered by absolute Cohen d, largest at top](tasks/stat_1/charts/stat1_effect_sizes.png)

### 3. Interactions between features

Ten pairwise logit interaction terms were tested among the top five features. Two were nominally significant on complete cases (LR p below 0.05).

**Age × Pregnancies (robust).**
- Complete cases: coefficient −0.0086 per unit product (SE 0.0028), Wald p = 0.002, LR p = 0.0018, Holm p = 0.018 across 10 pairs. OR per 1 SD of each feature 0.71 (95% CI 0.57 to 0.88).
- Zeros kept (n = 768): LR p = 0.0011, Holm p = 0.011.
- Positive rates split at medians (Age 29, Pregnancies 3), complete cases:

| | Low Pregnancies | High Pregnancies |
|---|---|---|
| Low Age | 20.6% (n = 321) | 28.1% (n = 64) |
| High Age | 50.0% (n = 94) | 48.7% (n = 273) |

  Age is associated with a higher positive rate when pregnancies are low, and the Age gap is smaller when pregnancies are high. The cells are unbalanced.

**Glucose × DiabetesPedigreeFunction (borderline).**
- Complete cases: coefficient −0.0254 per unit product (SE 0.0084), Wald p = 0.003, LR p = 0.0054, Holm p = 0.048 across 10 pairs. OR per 1 SD of each feature 0.77 (95% CI 0.65 to 0.91).
- Zeros kept: Holm p = 0.061, which does not survive correction at 0.05.
- Positive rates split at medians (Glucose 117, DiabetesPedigreeFunction 0.377), complete cases:
  - Low Glucose, low DiabetesPedigreeFunction: 12.1% (n = 198)
  - Low Glucose, high DiabetesPedigreeFunction: 20.6% (n = 180)
  - High Glucose, low DiabetesPedigreeFunction: 48.9% (n = 178)
  - High Glucose, high DiabetesPedigreeFunction: 59.2% (n = 196)

**Other pairs (no evidence of interaction at this sample size).** LR p values are given as complete-case (CC) and zeros-kept (ZK). Holm p values are 1.0 for all pairs except Age × Pregnancies, Glucose × DiabetesPedigreeFunction, and Glucose × Age (Holm 0.65 with zeros kept).
- Glucose × Age: CC LR p = 0.150; ZK LR p = 0.081 (Holm 0.65). Per-1-SD OR with zeros kept 0.83 (95% CI 0.68 to 1.02).
- Glucose × Pregnancies: CC 0.211; ZK 0.109 (Holm 0.76).
- Glucose × BMI: CC 0.596; ZK 0.248 (Holm 1.0). Complete-case per-unit-product OR 0.9997 (95% CI 0.9986 to 1.0008). Zeros-kept positive rates split at medians (descriptive only): 10.4%, 24.8%, 41.7% and 62.9% across the four cells (low–low, low Glucose/high BMI, high Glucose/low BMI, high–high). These do not establish an interaction, and a moderate interaction cannot be ruled out.
- BMI × DiabetesPedigreeFunction: CC 0.178; ZK 0.615.
- BMI × Pregnancies: CC 0.894; ZK 0.257.
- Pregnancies × DiabetesPedigreeFunction: CC 0.276; ZK 0.347.
- BMI × Age: CC 0.444; ZK 0.824.
- Age × DiabetesPedigreeFunction: CC 0.744; ZK 0.683.

### 4. Adjusted associations (partial task)

Adjusted odds ratios per SD from a multivariable logistic model of all eight features. Two runs: zeros as recorded (n = 768) and zeros set to missing with complete-case analysis (n = 392).

| Feature | OR, zeros as recorded (95% CI, p) | OR, zeros set to missing, complete case (95% CI, p) |
|---|---|---|
| Glucose | 3.08 (2.44 to 3.88), p = 2.5e-21 | 3.25 (2.30 to 4.61), p = 3.2e-11 |
| BMI | 2.03 (1.61 to 2.56), p = 2.8e-09 | 1.64 (1.13 to 2.39), p = 0.010 |
| Age | 1.19 (0.96 to 1.48), p = 0.11 | 1.41 (0.98 to 2.04), p = 0.065 |
| BloodPressure | 0.77 (0.63 to 0.94), p = 0.011 | 0.98 (0.74 to 1.31), p = 0.90 |

- Glucose ranks above BMI in both runs. The full ordering differs. With zeros as recorded: Glucose, BMI, Pregnancies, DiabetesPedigreeFunction, Age, SkinThickness, Insulin, BloodPressure. With zeros set to missing: Glucose, BMI, DiabetesPedigreeFunction, Age, Pregnancies, SkinThickness, BloodPressure, Insulin.
- Age is not significant after adjustment in either run. It ranks fifth in the first run and fourth in the second, so its place in the top three does not hold.
- BloodPressure has an OR below 1 with zeros as recorded, but the sign does not survive the zero recode. The reversal is therefore not established. These are associations conditional on the other features and say nothing about direct versus indirect effects.
- Model fit: pseudo R² 0.272 (zeros as recorded, LLR p = 9.7e-54) and 0.309 (zeros set to missing, n = 392, LLR p = 2.8e-29). The complete-case run drops 376 rows, about half the sample, so its estimates come from a selected subsample. No imputation was run for this task.
- Multicollinearity is low in both runs. In the zeros-set-to-missing run the condition number is 2.94 and all VIFs are below 2.2.

![Adjusted odds ratios with 95% CI per standardized feature, Outcome=1 vs 0](tasks/stat_3/charts/stat3_adjusted_or.png)

### 5. Predictive performance

Stratified 80/20 split (seed 42): 614 training rows and 154 test rows, with 35.1% positives in the test set. Zeros in the five columns were set to missing and median-imputed using the training data. The majority-class baseline test accuracy is 0.649.

| Model | Test accuracy | Precision | Recall | F1 | ROC AUC | Train accuracy |
|---|---|---|---|---|---|---|
| Logistic regression | 0.708 | 0.600 | 0.500 | 0.545 | 0.813 | 0.796 |
| Random forest (500 trees) | 0.734 | 0.644 | 0.537 | 0.586 | 0.816 | 1.000 |

- Both models beat the baseline. ROC AUC is nearly identical for the two models, so the random forest's extra accuracy and F1 are modest on 154 test rows.
- The random forest overfits (train–test accuracy gap 0.27, versus 0.09 for logistic regression), so its test metrics are optimistic relative to its fit.
- Random forest permutation importance (drop in test ROC AUC, 20 repeats): Glucose 0.099 (sd 0.022), BMI 0.047 (sd 0.018), Age 0.027 (sd 0.011). Insulin, DiabetesPedigreeFunction, Pregnancies, BloodPressure and SkinThickness have drops of 0.011 or less. SkinThickness has no measurable importance (−0.001, sd 0.005).
- Logistic regression ranks Glucose (coefficient 1.18), BMI (0.69) and Pregnancies (0.38) highest by absolute coefficient.

![Random forest permutation importance: mean drop in test ROC AUC when each feature is shuffled (20 repeats, error bars = sd)](tasks/ml_1/charts/rf_permutation_importance.png)

### 6. Implausible zeros and missingness

**Counts.** Insulin 374 zeros (48.7%); SkinThickness 227 (29.6%); BloodPressure 35 (4.6%); BMI 11 (1.4%); Glucose 5 (0.7%). The BMI and Glucose counts are small.

**Link to Outcome.** No column shows a significant link between zero status and Outcome (Fisher exact test). Positive rates for zero versus nonzero rows:
- Insulin: 36.9% vs 33.0% (p = 0.289, OR 0.84)
- SkinThickness: 38.8% vs 33.3% (p = 0.159, OR 0.79)
- BloodPressure: 45.7% vs 34.4% (35 zero rows, p = 0.203, OR 0.62)
- BMI: 18.2% vs 35.1% (11 zero rows, p = 0.346, OR 2.44; direction reversed)
- Glucose: 40.0% vs 34.9% (5 zero rows, p = 1.0, OR 0.80)

These differences are descriptive. None reaches significance.

**Co-occurrence.** Zeros are not random across columns. 376 of 768 rows (49.0%) have at least one zero among the five columns: 142 rows have one, 199 have two, 28 have three and 7 have four. Every SkinThickness zero row is also an Insulin zero row (227 of 227). Other pair overlaps: BloodPressure and Insulin 35 rows, BloodPressure and SkinThickness 33, BloodPressure and BMI 7, SkinThickness and BMI 9, Insulin and BMI 10, Glucose and Insulin 4. Glucose does not overlap with BloodPressure, SkinThickness or BMI.

**Age and Pregnancies (descriptive).** Mean Age and Pregnancies are higher in zero rows than in nonzero rows for SkinThickness (Age 37.25 vs 31.56; Pregnancies 4.64 vs 3.51) and Insulin (Age 35.8 vs 30.81; Pregnancies 4.43 vs 3.29). No significance test was run on these differences at this stage. Section 6 below (stat_4) tests them.

**Test of predictability (stat_4).**
- Both-zero status (Insulin and SkinThickness both 0) affects 227 of 768 rows (29.6%), the base rate used as the reference.
- Age predicts both-zero status: OR 1.035 per year (95% CI 1.020 to 1.051, p = 7.4e-6).
- Pregnancies does not add significant information once Age is included: OR 1.033 (95% CI 0.980 to 1.089, p = 0.23).
- Age and Pregnancies together give a 5-fold cross-validated AUC of 0.644 against chance 0.5. This AUC has no confidence interval or test against 0.5. The claim that zero status is predictable beyond chance rests on the Age coefficient, not on the AUC.
- Outcome adds no detectable information about both-zero status: OR 0.992 (95% CI 0.706 to 1.394), likelihood-ratio χ² = 0.002, p = 0.964. The CI is compatible with effects from about 0.71 to 1.39, so a moderate association is not excluded. Cross-validated AUC moved from 0.644 to 0.639 after adding Outcome; this change was not tested.

**Handling.** Zeros in all five columns are treated as missing (NaN) in the later tasks, since a zero is physiologically impossible for these measurements. Imputation with the training median was used in the predictive models. For Insulin and SkinThickness, whether the results would change under the alternative handling was not tested.

![Outcome positive rate for rows with a zero versus a non-zero value in each column](tasks/eda_2/charts/zero_outcome_rate.png)

## Limitations

- **Zero-coded values.** Zeros in Glucose, BloodPressure, SkinThickness, Insulin and BMI are physiologically impossible and were treated as missing. The profile reports no missing values, so this recode changes the data. The results depend on the handling:
  - The adjusted model (section 4) gives different BMI, Age and BloodPressure estimates with zeros as recorded and with zeros set to missing. The BloodPressure sign reversal does not survive the recode.
  - The predictive models (section 5) used zeros set to missing with median imputation. Kept-versus-imputed sensitivity was not tested, so whether the Insulin and SkinThickness results would change is unknown.
- **SkinThickness low-bin pattern (unresolved review issue).** In the lowest SkinThickness bin (−0.001, 18.0], 227 of 320 rows are zero, so that bin is mostly coded missing values. The "dips at the low end" pattern is not a substantive finding and is not claimed here.
- **Insulin binning (unresolved review issue).** On the full data, quantile bins give only 3 bins because of ties at zero. The 4-bin requirement is met only on the nonzero subset (positive rates 8.1%, 23.2%, 48.5% and 52.6% by quartile of nonzero values). The full-data bins are not reported.
- **Interaction results (unresolved review issue, corrected).** Age × Pregnancies survives multiplicity correction in both analyses (complete-case Holm 0.018; zeros kept Holm 0.011). Glucose × DiabetesPedigreeFunction survives on complete cases (Holm 0.048) but not with zeros kept (Holm 0.061). Both are reported above, with the analysis labelled. The Glucose × BMI 2x2 rates are zeros-kept and descriptive only; the complete-case CI is given with them.
- **Complete-case sample sizes.** The complete-case interaction findings give a sample size that does not match the n = 392 complete-case run in section 4. This discrepancy is not resolved here.
- **Insulin and Glucose × DiabetesPedigreeFunction results are nominal.** Insulin's Welch and Mann-Whitney results disagree. The Glucose × DiabetesPedigreeFunction interaction is marginal after correction and needs confirmation.
- **Small counts.** BMI (11 zeros) and Glucose (5 zeros) are too small to support conclusions about their zero rows. The BloodPressure zero group (35 rows) is also small.
- **Complete-case subsample.** The complete-case analysis in section 4 uses about half the sample (n = 392), so its estimates come from a selected subsample.
- **Predictive estimates.** The test set has 154 rows, and the random forest overfits (train accuracy 1.0). Model differences are small and may not be reliable.
- **Missingness association.** The Age association with both-zero status is tested, but the cross-validated AUC of 0.644 has no confidence interval. The Outcome test is compatible with a moderate association.
- **Partial task.** Section 4 (stat_3) is marked partial. The adjusted results are reported as completed, but the Age estimate moves between runs and is not significant in either.
- **Scope.** All results are associations in a single dataset. The adjusted odds ratios describe associations conditional on the other features; they do not indicate causes or direct versus indirect effects.

**Numbers not traced to a recorded fact.** The automatic check found no recorded value for these numbers:
- 47.6% in: "- **Insulin:** the positive rate is 36.9% for zero rows and 33.0% for nonzero rows (chi-square χ² = 1.287, p = 0.257, not significant). Among nonzero values, th"

## Open questions

- Do the zeros in Glucose, BloodPressure, SkinThickness, Insulin and BMI behave as missing values? How does imputing them change the feature-outcome relationships, the effect sizes and the adjusted estimates?
- Does dropping or imputing the Insulin and SkinThickness zeros change model performance and feature importance compared with keeping them?
- Is the Insulin and SkinThickness zero pattern structural? Would a model with more predictors than Age and Pregnancies explain it? Would age-stratified imputation change downstream performance?
- Does the Glucose × BMI interaction exist? The current CI is wide enough that a moderate interaction cannot be ruled out. Would a larger or resampled dataset narrow the interaction CIs for Glucose × BMI and Glucose × Age?
- Does the Age × Pregnancies interaction survive a stratified or bootstrap analysis, or is it driven by unequal cell sizes in the 2x2 split?
- Does the Glucose × DiabetesPedigreeFunction interaction hold under a bootstrap or a model with a different functional form?
- How much of the Glucose, BMI and Age signal remains after adjusting for the other features, using imputed rather than complete-case data? Is the Age association stable across specifications?
- Would repeated cross-validation or a bootstrap give more reliable estimates of the small model differences on the 154-row test set? Does the random forest's train–test gap affect the comparison with logistic regression?
- Is the 0.644 cross-validated AUC for zero status reliably above 0.5?