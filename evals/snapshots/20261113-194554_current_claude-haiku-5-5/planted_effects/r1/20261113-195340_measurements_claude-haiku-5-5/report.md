# Outcome Analysis of a 1,000-Row Dataset: Predictors of the Binary `outcome` Target

## Summary

- **feat_a is the strongest association with outcome.** Its outcome rate rises from 11.6% in the bottom quartile to 70.8% in the top quartile. Its adjusted odds ratio is 3.63 per unit (95% CI 2.99 to 4.41), and it is the top-ranked feature in both models.
- **feat_d and feat_b are significant but weaker.** feat_d has an adjusted OR of 2.07 per unit (1.73 to 2.47) and feat_b has 1.38 (1.19 to 1.61). feat_c shows no association (adjusted OR 0.97, p = 0.70).
- **Prediction beats the majority-class baseline on one split.** On 200 test rows, logistic regression reaches accuracy 0.750 and ROC AUC 0.817, against 0.605 accuracy and 0.500 AUC for the baseline. Gradient boosting performs about the same (accuracy 0.755, AUC 0.807). The comparison rests on a single split.
- **No feature interactions were detected** (joint LR p = 0.664, n = 850 complete cases). The feat_b pattern across quartiles departs from linearity (LR p = 0.0001 on full sample), but a smooth spline term does not improve on the linear term (p = 0.49, complete cases).
- **feat_d missingness shows no detected association** with the other features or with outcome (chi-square p = 0.72). The missing group's outcome rate is 41.3%, against 39.4% for the present group.

## Data

- **Size:** 1,000 rows and 5 columns.
- **Target:** `outcome`, binary. Class 0 is 60.3% of rows and class 1 is 39.7%.
- **Features:** four numeric features (feat_a, feat_b, feat_c, feat_d). There are no categorical, date/time, identifier or free-text features.
- **Missing values:** feat_d is missing for 15.0% of rows (150 rows). No other feature has missing values.

## Findings

### Outcome rate by feature quartile (eda_1)

- **feat_a:** the outcome rate rises across quartiles: 11.6% (Q1, n = 251), 32.5% (Q2, n = 249), 44.0% (Q3, n = 250) and 70.8% (Q4, n = 250).
- **feat_b:** 26.8% (Q1), 44.4% (Q2), 37.6% (Q3) and 50.0% (Q4), all n = 250. The pattern is non-monotone, with a dip in Q3, and the overall increase is modest.
- **feat_c:** 38.8%, 42.8%, 35.6% and 41.6% across Q1 to Q4 (n = 250 each). No quartile pattern is visible.
- **feat_d:** 24.9% (Q1, n = 213), 35.4% (Q2, n = 212), 39.2% (Q3, n = 212) and 58.2% (Q4, n = 213). The 150 missing rows have an outcome rate of 41.3%, between the middle and top quartiles.

Summary statistics: feat_a mean -0.013, SD 0.990; feat_b mean 0.062, SD 1.016; feat_c mean -0.006, SD 1.013; feat_d mean 0.047, SD 1.001 (150 missing).

![Outcome rate (share with outcome = 1) by quartile bin of each feature; feat_d Missing shown separately](tasks/eda_1/charts/eda1_outcome_rate_by_quartile.png)

### feat_d missingness (eda_2)

- feat_d is missing in 14.6% of outcome-0 rows and 15.6% of outcome-1 rows.
- The outcome rate is 41.3% for rows with feat_d missing (n = 150) and 39.4% for rows with feat_d present (n = 850). A chi-square test gives p = 0.72.
- Missing and present rows do not differ detectably on feat_a (mean -0.073 vs -0.002, Mann-Whitney p = 0.28), feat_b (mean 0.128 vs 0.050, p = 0.35) or feat_c (mean 0.009 vs -0.009, p = 0.98).
- These tests show no association between missingness and the observed variables or outcome. MCAR cannot be confirmed from the observed variables, so MAR or MNAR remains possible. With 150 missing rows, small effects cannot be excluded.

![Share of rows with feat_d missing within each outcome class, computed from df](tasks/eda_2/charts/eda2_missing_rate_by_outcome_v2.png)

### Significance and effect sizes (stat_1)

Mann-Whitney tests and mean differences (outcome 1 minus outcome 0), with Holm correction across the four features:

| Feature | Rows | Mean difference (95% CI) | Cohen d | MWU p | Holm p | Result |
|---|---|---|---|---|---|---|
| feat_a | 1,000 | 0.922 (0.812 to 1.032) | 1.046 | 8.1e-48 | 3.2e-47 | Significant, large |
| feat_d | 850 (non-missing) | 0.551 (0.415 to 0.686) | 0.571 | 1.8e-14 | 5.3e-14 | Significant, moderate |
| feat_b | 1,000 | 0.298 (0.171 to 0.425) | 0.296 | 5.0e-06 | 1.0e-05 | Significant, small to moderate |
| feat_c | 1,000 | 0.004 (-0.124 to 0.132) | 0.004 | 0.899 | 0.899 | Not significant |

After Holm correction, feat_a, feat_b and feat_d remain significant at alpha 0.05, and feat_c does not.

![Mean difference in each feature between outcome=1 and outcome=0 with 95% CI; feat_d uses non-missing rows only](tasks/stat_1/charts/stat1_mean_difference_by_outcome.png)

### Interactions (stat_2)

- The six pairwise interaction terms do not jointly improve fit over the main-effects logistic model: LR = 4.097 on 6 df, p = 0.664 (n = 850 complete cases).
- No individual interaction is significant. The smallest p-value is 0.209 (feat_c x feat_d, OR 1.115). The other interactions have p-values from 0.326 to 0.921.
- Because no interaction was significant, the 2x2 outcome-rate split was not computed.
- The test used complete cases only. At n = 850, small interactions cannot be excluded, so additivity on the log-odds scale is not established.

Main effects in the full logistic model with all interaction terms: feat_a OR 3.69 (p < 0.001), feat_d OR 2.12 (p = 2.4e-15), feat_b OR 1.38 (p = 0.0004), feat_c OR 0.98 (p = 0.859).

### Adjusted associations (stat_3)

Multivariable logistic model on all 1,000 rows, with feat_d missing set to 0 and a missing-indicator term. Adjusted ORs per unit increase:

| Feature | Crude OR | Adjusted OR (95% CI) | p |
|---|---|---|---|
| feat_a | 3.34 | 3.63 (2.99 to 4.41) | < 0.001 |
| feat_b | 1.34 | 1.38 (1.19 to 1.61) | 3.2e-05 |
| feat_c | 1.00 | 0.97 (0.83 to 1.13) | 0.70 |
| feat_d | 1.81 (complete case, n = 850) | 2.07 (1.73 to 2.47) | < 0.001 |

- The missing-indicator term has OR 1.31 (p = 0.20), which is not significant.
- The complete-case model (n = 850) gives feat_d OR 2.07 (1.73 to 2.47, p < 0.001), matching the full-sample estimate.
- From crude to adjusted, feat_a's OR rises from 3.34 to 3.63 and feat_d's from 1.81 (complete case) to 2.07. feat_b's OR is essentially unchanged, from 1.34 to 1.38. feat_c stays null (1.00 to 0.97). The team describes the eda_1 crude quartile pattern for feat_c as not persisting as an association.
- The adjusted feat_b OR describes the average linear trend and does not test the Q3 dip.

### feat_b non-linearity (stat_4)

- **Quartile terms improve fit over the linear term:** LR = 15.87 on 2 df, p = 0.0004 (complete cases, n = 850); LR = 18.11 on 2 df, p = 0.0001 (full sample, n = 1,000). This omnibus test shows departure from linearity but does not isolate the Q3 dip.
- **Adjusted quartile ORs vs Q1, full sample (n = 1,000):** Q2 2.76 (1.76 to 4.31, p < 0.001); Q3 1.54 (0.99 to 2.41, p = 0.058); Q4 3.26 (2.10 to 5.08, p < 0.001).
- **Adjusted quartile ORs vs Q1, complete cases (n = 850):** Q2 2.69 (1.65 to 4.38, p < 0.001); Q3 1.56 (0.96 to 2.54, p = 0.074); Q4 3.51 (2.16 to 5.70, p < 0.001).
- **Q3 contrasts:** full sample, Q3 vs Q2 OR ratio 0.56 (0.36 to 0.86, p = 0.008) and Q3 vs Q4 OR ratio 0.47 (0.31 to 0.72, p = 0.0006). Complete cases, Q3 vs Q2 0.58 (0.36 to 0.92, p = 0.022) and Q3 vs Q4 0.44 (0.28 to 0.71, p = 0.0007).
- **Spline:** a smooth B-spline term for feat_b (df = 4) does not improve on the linear term: LR = 2.43 on 3 df, p = 0.49 (complete cases only; not run on the full sample).
- **Linear adjusted OR for feat_b:** 1.40 in complete cases (n = 850) against 1.38 in the full sample.

The team's conclusion is that the evidence supports a departure from linearity in the feat_b quartile step pattern. The Q3 dip is supported by the contrasts against Q2 and Q4 in both samples, but Q3 against Q1 is not significant (p = 0.074 and 0.058). The spline null means the pattern is not established as a smooth nonlinearity. The quartile result and the spline result therefore point in different directions, and this report does not resolve that difference. Quartile cut points are a discrete choice.

![Adjusted ORs for feat_b quartiles vs Q1, full sample with feat_d missing indicator](tasks/stat_4/charts/stat4_quartile_or.png)

### Predictive performance (ml_1)

Setup: stratified 80/20 split (random_state 42), giving 800 training and 200 test rows. feat_d was imputed with the training median and a missing indicator was added. All models were scored on the same 200 test rows.

| Model | Test accuracy | Test ROC AUC | Precision | Recall | F1 | Test log loss | Train accuracy |
|---|---|---|---|---|---|---|---|
| Majority class | 0.605 | 0.500 | 0.0 | 0.0 | 0.0 | 14.24* | 0.603 |
| Logistic regression (standardized) | 0.750 | 0.817 | 0.710 | 0.620 | 0.662 | 0.505 | 0.740 |
| Gradient boosting | 0.755 | 0.807 | 0.688 | 0.696 | 0.692 | 0.528 | 0.869 |

*The majority-class log loss reflects hard 0/1 probabilities and is not comparable to the model log losses.

- Both models beat the majority-class baseline clearly. For logistic regression, test accuracy is 0.750 against 0.605 for the baseline, and test ROC AUC is 0.817 against 0.500.
- Gradient boosting overfits: its train accuracy is 0.869 against 0.755 on test. Logistic regression's train accuracy is 0.740 against 0.750 on test.
- On this split, logistic regression has the higher AUC (0.817 vs 0.807) and the lower log loss. The AUC gap of about 0.01 rests on one split of 200 rows and is not established as noise-free.

![Test ROC AUC for majority-class baseline, logistic regression and gradient boosting](tasks/ml_1/charts/ml1_model_auc.png)

### Feature importance (ml_2)

Gradient boosting, permutation importance on the test set (drop in ROC AUC, 30 shuffles, mean and SD):

| Feature | Mean AUC drop | SD |
|---|---|---|
| feat_a | 0.215 | 0.035 |
| feat_d | 0.087 | 0.022 |
| feat_b | 0.014 | 0.012 |
| feat_c | 0.009 | 0.006 |
| feat_d_missing | 0.001 | 0.001 |

Standardized logistic regression coefficients: feat_a 1.251, feat_d 0.610, feat_b 0.375, feat_d_missing 0.137, feat_c -0.025.

- In both models, feat_a and feat_d rank first and second, and feat_a, feat_d and feat_b are the significant features in stat_1. feat_c contributes least or near least in both models.
- feat_b ranks third in both models. In gradient boosting its drop is within noise of feat_c's, so its third place is not firmly separated from feat_c. In logistic regression it is third by coefficient, but no coefficient uncertainty is reported, so that ordering is not firmly established either.
- **The feat_d_missing measures disagree.** The gradient boosting permutation value is 0.001 and the logistic coefficient is 0.137. The two measures disagree, and the team does not resolve the difference here. A grouped-permutation follow-up is planned to test it.
- The gradient boosting importance of 0.51 for feat_a in ml_1 and the permutation drop of 0.215 in ml_2 come from different analyses and should not be compared directly.

## Limitations

- **Single split for model comparison.** The logistic regression and gradient boosting comparison rests on one 200-row test split. The AUC difference of about 0.01 is not established as stable, and no cross-validated comparison has been run.
- **feat_d missingness.** The 150 missing rows give limited power, so small associations cannot be excluded. MCAR cannot be confirmed; MAR and MNAR remain possible. The full-sample models code missing feat_d as 0 and add an indicator, so the feat_d estimate in that model depends on this coding. Complete-case results are reported alongside it.
- **Complete-case restriction.** The interaction tests (stat_2), the complete-case adjusted models (stat_3, stat_4) and the spline test (stat_4) use the 850 complete cases. The spline test was not run on the full sample.
- **feat_b nonlinearity.** The quartile result and the spline result disagree in what they show about smooth nonlinearity. The Q3 dip depends on discrete quartile cut points, and Q3 against Q1 is not significant.
- **Interaction power.** At n = 850, small interactions cannot be excluded.
- **Permutation and coefficient comparisons.** The gradient boosting and logistic regression importance measures differ, and no coefficient uncertainty is reported for the logistic model.
- **Unresolved review issue (eda_2).** The lead asked for two medians to be corrected: feat_b median_present (0.019 to 0.018) and feat_c median_missing (-0.082 to -0.081). The verified record and the summary value for these medians differ at the third decimal, so those medians are omitted from this report. The lead also asked that the hardcoded chart eda2_missing_rate_by_outcome be removed or replaced with the computed version; only the computed chart (v2) is embedded above.
- **Unresolved review issue (ml_2).** The claim that the feat_d_missing permutation importance is shared with imputed feat_d values, and that the GBM value understates the indicator's role, has been removed as the lead requested. The claim that ml_1's 0.51 is impurity-based is also removed, because ml_1's record does not state the method.
- **Unresolved review issue (ml_2, feat_b).** The statement that feat_b's third place in the logistic model is clear is qualified above, because no coefficient uncertainty is reported.
- No tasks failed.

## Open questions

- Does a cross-validated comparison show whether logistic regression's AUC edge over gradient boosting is real or split noise?
- Does a cross-validated permutation importance confirm the feat_b versus feat_c ordering in gradient boosting, given the SD of 0.012 on feat_b's drop?
- Is the feat_b Q3 dip robust to the quartile cut points (for example tertiles or quintiles)?
- Would a spline or quartile test on the full 1,000-row sample agree with the complete-case spline result?
- Is feat_d missingness informative about outcome in a multivariable model? Does the missing group's adjusted risk differ from the model prediction?
- Does a grouped permutation of feat_d and feat_d_missing change the indicator's gradient boosting importance, and does the indicator's contribution hold across repeated splits?
- Would a larger sample detect the feat_c x feat_d pattern (smallest interaction p = 0.209)?
- Do feat_a and feat_d interact in their effect on outcome, and does the feat_b pattern change with feat_a or feat_d interactions?