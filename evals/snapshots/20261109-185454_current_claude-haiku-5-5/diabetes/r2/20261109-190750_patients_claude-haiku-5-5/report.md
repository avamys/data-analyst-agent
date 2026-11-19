# Pima Diabetes Data (768 rows): Predictors of the Outcome Target

## Summary

- **Glucose is the strongest feature in every analysis.** Outcome=1 rates rise from 7.3% in the lowest Glucose quartile to 69.5% in the highest. Glucose has the largest group difference (Cohen's d 1.105) and the largest adjusted association (OR 3.26 per SD, 95% CI 2.30 to 4.62, n=392 complete cases).
- **After adjusting for the other features, Glucose, BMI and DiabetesPedigreeFunction remain significant.** Age (p=0.065) and Pregnancies (p=0.138) do not reach significance, and BloodPressure, SkinThickness and Insulin are not significant. These results apply only to the 392-row complete-case subsample, which excludes 376 rows with zeros.
- **No Glucose interaction was detected.** The joint likelihood-ratio test of the three interaction terms gives p=0.131. The Glucose×Age term alone is borderline (p=0.049).
- **Models beat the majority-class baseline, but the margin is uncertain.** On a 154-row test split, the baseline accuracy is 64.9%. Logistic regression reaches 70.8% and random forest 74.0%, with ROC AUC of 0.813 and 0.816. A refit random forest on the same split reports 76.6%, which disagrees with the 74.0% figure and is unresolved.
- **Zeros treated as missing did not improve prediction.** Replacing zeros with NaN and median-imputing them gave 72.4% test accuracy against 73.4% with zeros kept. The 5-fold cross-validated gap was 0.3 points (77.2% vs 77.5%), within fold-to-fold variation.

## Data

- **Size:** 768 rows and 9 columns: 8 numeric features and the binary target Outcome. There are no categorical, date/time, or identifier/free-text columns.
- **Target:** Outcome is imbalanced. 65.1% of rows have Outcome=0 and 34.9% have Outcome=1.
- **Missing values:** The profile reports none. However, the analysis found zeros in Glucose, BloodPressure, SkinThickness, Insulin and BMI that are physiologically implausible and likely encode missing values. Zero counts are: Insulin 374, SkinThickness 227, BloodPressure 35, BMI 11, Glucose 5. Pregnancies has 111 zeros, which are plausible. DiabetesPedigreeFunction and Age have none. The likely-missing interpretation is a working assumption, not a tested mechanism.

## Findings

### Outcome rates by feature bin (eda_1)

Rates below are Outcome=1 shares within bins. Zeros are shown as their own bin where relevant.

- **Glucose** (strongest gradient): 7.3% (44 to 99, n=192), 24.7% (99 to 117, n=194), 38.9% (117 to 141, n=190), 69.5% (141 to 199, n=187). The 5 zero rows show 40%.

![Distribution of Glucose and Outcome=1 rate per bin](tasks/eda_1/charts/eda1_Glucose.png)

- **BMI:** 11.4% (under 27.5, n=193), 36.4% (27.5 to 32.3, n=187), 45.0% (32.3 to 36.6, n=189), 48.4% (above 36.6, n=188). The 11 zero rows show 18.2%.

![Distribution of BMI and Outcome=1 rate per bin](tasks/eda_1/charts/eda1_BMI.png)

- **Age:** 14.2% (21 to 24, n=219), 29.9% (24 to 29, n=177), 47.5% (29 to 41, n=200), 51.7% (41 to 81, n=172).

![Distribution of Age and Outcome=1 rate per bin](tasks/eda_1/charts/eda1_Age.png)

- **Pregnancies:** 27.2% (0 to 1, n=246), 25.8% (1 to 3, n=178), 34.3% (3 to 6, n=175), 56.2% (6 to 17, n=169). The rise is not monotone in the lower bins.

![Distribution of Pregnancies and Outcome=1 rate per bin](tasks/eda_1/charts/eda1_Pregnancies.png)

- **DiabetesPedigreeFunction:** 25.5% (0.077 to 0.244, n=192), 33.3% (0.244 to 0.372, n=192), 32.3% (0.372 to 0.626, n=192), 48.4% (0.626 to 2.42, n=192). The gradient is weaker than Glucose and not monotone in the middle bins.

![Distribution of DiabetesPedigreeFunction and Outcome=1 rate per bin](tasks/eda_1/charts/eda1_DiabetesPedigreeFunction.png)

- **BloodPressure** (nonzero values): 22.9% (24 to 64, n=201), 34.4% (64 to 72, n=183), 35.9% (72 to 80, n=184), 46.7% (80 to 122, n=165). The Outcome=1 rate rises monotonically across these four bins, from 22.9% to 46.7%. The zero bin is 45.7% (n=35).

![Distribution of BloodPressure and Outcome=1 rate per bin](tasks/eda_1/charts/eda1_BloodPressure.png)

- **SkinThickness** (nonzero values): 15.3% (7 to 22, n=150), 31.7% (22 to 29, n=126), 42.5% (29 to 36, n=134), 45.8% (36 to 99, n=131). The zero bin is 38.8% (n=227).

![Distribution of SkinThickness and Outcome=1 rate per bin](tasks/eda_1/charts/eda1_SkinThickness.png)

- **Insulin** (nonzero values): 8.1% (14 to 76, n=99), 23.2% (76 to 125, n=99), 48.5% (125 to 190, n=99), 52.6% (190 to 846, n=97). The zero bin is 36.9% (n=374).

![Distribution of Insulin and Outcome=1 rate per bin](tasks/eda_1/charts/eda1_Insulin.png)

**Zero rows and Outcome.** The Outcome=1 rate differs for zero rows in each column:

- BMI=0: 18.2% (n=11), versus 35.1% for nonzero rows.
- BloodPressure=0: 45.7% (n=35), versus 34.4%.
- SkinThickness=0: 38.8% (n=227), versus 33.3%.
- Insulin=0: 36.9% (n=374), versus 33.0%.
- Glucose=0: 40% (n=5), versus 34.9%.

Zero rows also differ on other columns. Mean SkinThickness is 11.5 in Insulin=0 rows and 29.1 in nonzero Insulin rows. Zeros in Insulin and SkinThickness, and in BMI and SkinThickness, co-occur in the same rows. This is a pattern only; no test of the missingness mechanism was run.

### Group differences (stat_1)

Comparisons are Outcome=1 vs Outcome=0. Holm correction was applied across the eight features.

| Feature | Mean (Outcome 0 → 1) | Difference (95% CI) | Cohen's d | Holm p (Welch / Mann-Whitney) |
|---|---|---|---|---|
| Glucose | 110.0 → 141.3 | 31.3 (26.8 to 35.7) | 1.105 | <0.001 / <0.001 |
| BMI | 30.3 → 35.1 | 4.84 (3.74 to 5.94) | 0.641 | <0.001 / <0.001 |
| Age | 31.2 → 37.1 | 5.88 (4.21 to 7.55) | 0.514 | <0.001 / <0.001 |
| Pregnancies | 3.30 → 4.87 | 1.57 (1.05 to 2.09) | 0.477 | <0.001 / <0.001 |
| DiabetesPedigreeFunction | 0.430 → 0.551 | 0.121 (0.069 to 0.173) | 0.370 | 2.4e-5 / <0.001 |
| Insulin | 68.8 → 100.3 | 31.5 (12.8 to 50.3) | 0.276 | 0.003 / 0.066 |
| SkinThickness | 19.7 → 22.2 | 2.50 (0.007 to 4.99) | 0.157 | 0.099 / 0.026 |
| BloodPressure | 68.2 → 70.8 | 2.64 (−0.39 to 5.67) | 0.137 | 0.099 / 0.0002 |

- **Glucose, BMI, Age, Pregnancies and DiabetesPedigreeFunction** are significant under both tests after Holm correction. Effects are small to moderate, except Glucose.
- **Insulin** is significant under Welch but not under Mann-Whitney. The Insulin medians are 0 for Outcome=1 and 39 for Outcome=0, which suggests the zeros may drive the rank-based result. This was not tested, so treat the Insulin effect as provisional.
- **BloodPressure and SkinThickness** are not significant under Welch but are significant under Mann-Whitney (BloodPressure p=0.0002, SkinThickness p=0.026). The two tests disagree, and the effects are small. The Welch and Mann-Whitney tests include zero values, while the bin analysis above excludes them.
- All Welch and Mann-Whitney results for Insulin, SkinThickness, BloodPressure and BMI include zeros, so their means, differences and effect sizes are provisional.

![Cohen's d between Outcome=1 and Outcome=0 for each of the 8 numeric features (positive = higher in Outcome=1)](tasks/stat_1/charts/stat1_effect_sizes.png)

### Interactions (stat_2)

- The joint likelihood-ratio test of the Glucose×BMI, Glucose×Age and BMI×Age terms against the main-effects model is not significant: LR = 5.62 on 3 df, p = 0.131 (n=752 rows with Glucose>0 and BMI>0).
- No single interaction term is significant at 0.05. Glucose×BMI: OR 0.9997 (95% CI 0.9986 to 1.0008, p=0.565). BMI×Age: OR 1.0015 (95% CI 0.9991 to 1.0039, p=0.220). Glucose×Age: OR 0.9994 (95% CI 0.9989 to 1.0000, p=0.049), borderline, and not supported by the joint test.
- Main effects in the interaction model, per unit on the centred scale: Glucose OR 1.0385 (95% CI 1.0309 to 1.0461), BMI OR 1.0921 (95% CI 1.0614 to 1.1236), Age OR 1.0344 (95% CI 1.0180 to 1.0510).
- In the median-split 2×2 (Glucose>0, BMI>0), Outcome=1 rates are: high Glucose and high BMI 62.6% (137/219); high Glucose and low BMI 42.6% (66/155); low Glucose and high BMI 23.7% (37/156); low Glucose and low BMI 10.8% (24/222). The raw rates are not clearly additive, although the model test does not detect an interaction.
- The analysis concludes that the test finds no detectable Glucose interaction with BMI or Age, consistent with additive effects on the log-odds scale. The Glucose×Age term at p=0.049 is a weak lead, not a finding.

![Outcome=1 rate in each Glucose by BMI median-split cell, with counts in labels](tasks/stat_2/charts/stat2_2x2_rates.png)

### Adjusted associations (stat_3)

This model used 392 complete cases of 768 rows, with 130 events. Zeros in Glucose, BloodPressure, SkinThickness, Insulin and BMI were treated as missing, which removed 376 rows; 374 of these are zero-Insulin rows. Pregnancies zeros were kept. All significance statements below apply only to this subsample.

| Feature | Adjusted OR per SD (95% CI) | p | Significant at 0.05 |
|---|---|---|---|
| Glucose | 3.26 (2.30 to 4.62) | <0.001 | Yes |
| BMI | 1.64 (1.13 to 2.39) | 0.010 | Yes |
| DiabetesPedigreeFunction | 1.48 (1.11 to 1.98) | 0.008 | Yes |
| Age | 1.41 (0.98 to 2.04) | 0.065 | No (borderline) |
| Pregnancies | 1.30 (0.92 to 1.85) | 0.138 | No |
| SkinThickness | 1.13 (0.79 to 1.60) | 0.511 | No |
| Insulin | 0.91 (0.67 to 1.23) | 0.528 | No |
| BloodPressure | 0.98 (0.74 to 1.31) | 0.904 | No |

- The Pregnancies association does not survive adjustment. Its unadjusted rank-biserial is 0.243 and its Mann-Whitney p is below 0.001. The adjusted CI is compatible with effects up to about 1.85 per SD, so the estimate is imprecise rather than shown to be explained away.
- The BloodPressure bins above show a rising Outcome=1 rate, but BloodPressure is not significant after adjustment (p=0.90). These two results point in different directions, and this report does not resolve the difference.

![Adjusted odds ratios per SD with 95% CIs from the multiple logistic regression of Outcome on the 8 numeric features (complete cases, n=392)](tasks/stat_3/charts/stat3_forest_odds_ratios.png)

### Predictive models (ml_1, ml_2, ml_3)

**Comparison with the baseline (ml_1).** The split is stratified 80/20 with random_state=42, giving 614 training and 154 test rows. Zeros were set to NaN in five columns and median-imputed (see Limitations).

| Model | Test accuracy | ROC AUC | F1 (Outcome=1) |
|---|---|---|---|
| Majority-class baseline | 64.9% | — | 0.0 |
| Logistic regression | 70.8% | 0.813 | 0.545 |
| Random forest | 74.0% | 0.816 | 0.592 |

- Logistic regression confusion matrix: TN 82, FP 18, FN 27, TP 27. Random forest: TN 85, FP 15, FN 25, TP 29.
- Random forest has higher accuracy and F1, but ROC AUC is essentially tied. The test set is small, and no repeated-split or cross-validation estimate supports the margin, so ranking random forest as the best model is provisional.
- The random forest overfits: training accuracy is 1.0 against 74.0% on test.

![Test-set accuracy and F1 for the majority baseline, logistic regression and random forest](tasks/ml_1/charts/ml1_model_comparison.png)

**Random forest refit (ml_2).** A refit random forest on the same split reports test accuracy 76.6%, precision 0.696, recall 0.593, F1 0.640 and ROC AUC 0.821. The ml_1 random forest reported 74.0% and 0.816 on the same split. These figures disagree and the disagreement is unresolved. The ml_2 analysis attributes it to input data: the ml_2 fits used zeros as recorded, with no imputation, while ml_1 imputed them. This cause was inferred and not verified. The logistic regression scores agree across both tasks (70.8%).

**Feature importance (ml_2).** The importances come from the refit random forest, which also has training accuracy 1.0. Permutation importance on the test set (drop in ROC AUC, 30 repeats):

- Glucose 0.101 (sd 0.021)
- BMI 0.051 (sd 0.017)
- Age 0.029 (sd 0.012)
- DiabetesPedigreeFunction 0.015 (sd 0.007)
- Pregnancies 0.013 (sd 0.010)
- Insulin 0.009 (sd 0.010)
- BloodPressure 0.006 (sd 0.007)
- SkinThickness 0.001 (sd 0.006)

Top three by model: random forest impurity ranks Glucose, BMI, DiabetesPedigreeFunction; logistic regression absolute coefficients rank Glucose, BMI, Pregnancies; random forest permutation ranks Glucose, BMI, Age. Glucose and BMI appear in all three rankings. Pregnancies and DiabetesPedigreeFunction move between rankings.

The top permutation features agree with the significant group differences in stat_1. Glucose, BMI and Age are significant under both tests. Pregnancies and DiabetesPedigreeFunction are significant but rank 4th and 5th. Insulin, which is significant only under Welch, ranks 6th. BloodPressure and SkinThickness, which are not significant under Welch, rank 7th and 8th.

![Drop in test ROC AUC when each feature is permuted, random forest](tasks/ml_2/charts/ml2_permutation_importance.png)

**Zero handling and prediction (ml_3).** This task used a different split: 576 training and 192 test rows. The majority baseline on this split is 65.1%.

| Zeros | Test accuracy | ROC AUC | F1 | 5-fold CV accuracy (SD) |
|---|---|---|---|---|
| Kept | 73.4% | 0.832 | 0.579 | 77.5% (0.015) |
| Set to NaN and median-imputed | 72.4% | 0.824 | 0.562 | 77.2% (0.017) |

- Replacing zeros did not improve held-out performance. The CV gap of 0.3 points is within fold-to-fold variation.
- These are single logistic regression models. Coefficients are standardized-scale values, not significance tests. With zeros kept, BloodPressure (0.204) is larger than Age (0.154). With NaN imputation, SkinThickness rises from 0.008 to 0.058, while BloodPressure (0.204 to 0.057) and Insulin (0.079 to 0.031) shrink. Glucose and BMI remain the largest in both.

## Limitations

- **Zeros are probably missing values, but this is unconfirmed.** Insulin, SkinThickness, BloodPressure, BMI and Glucose zeros were treated as likely missing codes, and no test of the missingness mechanism was run. The Outcome rate for zero rows does not follow one pattern (see Findings).
- **Provisional group effects.** Insulin's significance depends on its zeros and differs between the Welch and Mann-Whitney tests. The Welch and Mann-Whitney results for Insulin, SkinThickness, BloodPressure and BMI include zeros.
- **Adjusted models use a selected subsample.** The adjusted logistic model (stat_3) uses 392 of 768 rows, with 376 dropped for zeros, mainly 374 zero-Insulin rows. Its significance statements apply only to that subsample. The interaction test (stat_2) uses 752 rows, with zeros in Glucose and BMI dropped.
- **Small test sets and no repeated validation.** The ml_1 and ml_2 test set has 154 rows, and the ml_3 test set has 192. The random forest vs logistic regression ranking has no cross-validation support.
- **Unresolved: imputation outside a pipeline (ml_1).** Median imputation was fitted on the training split only and applied to both splits, so it does not leak test data. It was run outside a model pipeline, contrary to the brief. The model comparison was not re-run with imputation inside a pipeline.
- **Unresolved: random forest disagreement (ml_1 vs ml_2).** The same split gives 74.0% test accuracy in ml_1 and 76.6% in the ml_2 refit. The cause is inferred from input data and was not verified. Importances rest on the ml_2 fits.
- **ml_2 is partial.** Its robustness checks (repeated splits, imputation inside a pipeline, adjusted rankings) were not completed. Its rankings should be treated as provisional, and the random forest's training accuracy of 1.0 means its importances describe a model that fits the training data perfectly.
- **BloodPressure bins: review addition and provenance.** At review, the BloodPressure quartile bins were added to the Findings above as requested, and the zero bin is reported as recorded. The ml_3 script hard-coded these values from eda_1 without recomputing them from the cleaned table, so their provenance is the eda_1 values as entered.
- **Effects are not yet shown to hold after further adjustment.** The adjusted model includes only the eight numeric features. The interaction analysis uses a median split for the descriptive 2×2 and assumes linearity on the log-odds scale for the model test.
- **Limited scope of the data.** The dataset has no sex or age-group information, so differences by these groups cannot be assessed.

## Open questions

- Does replacing zeros with NaN and imputing them change model performance when imputation sits inside a cross-validated pipeline? The tasks compared only logistic regression under CV, and the ml_1 comparison was not re-run.
- Why do zero Insulin and zero SkinThickness rows co-occur, and what does that say about the missingness mechanism?
- Is the Outcome=1 rate for BMI=0 (18.2% on 11 rows) a real effect or noise?
- Do the Glucose, BMI, DiabetesPedigreeFunction and Age gradients hold after adjusting for the other features in a model that uses all rows, with zeros handled as missing?
- Does the Glucose×Age interaction (p=0.049) hold after adding Pregnancies and DiabetesPedigreeFunction, and when zeros are imputed rather than dropped?
- Does a repeated stratified split or k-fold cross-validation confirm the random forest's margin over logistic regression?
- Does random forest overfitting (training accuracy 1.0) shrink with tuned depth or leaf size, and does ROC AUC improve?
- Why does the ml_1 random forest report 74.0% test accuracy while the ml_2 refit reports 76.6% on the same split? Which input data did each fit receive?
- Do the importance rankings change when zeros are treated as missing and imputed inside a pipeline?
- Does the Pregnancies association become significant in a model that omits correlated features, and does the Age effect (p=0.065) reach significance without Pregnancies?
- Is the BloodPressure trend in the unadjusted bin rates consistent with its non-significance after adjustment, and does the Mann-Whitney BloodPressure signal reflect the zero rows?
- Do the Glucose, BMI and DiabetesPedigreeFunction associations differ by sex or age group? The data does not record sex.