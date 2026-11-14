# Outcome Prediction Study of feat_a, feat_b and feat_c on a 1,000-Row Binary Outcome

## Summary

- **feat_b has a consistent positive association with outcome.** It is significant in group tests and in a multivariable logistic model (OR 1.50 per raw unit, 95% CI 1.31 to 1.73, p = 1.1e-8), and it survives Bonferroni correction. feat_c shows no association in any test.
- **feat_a has a nonlinear, U-shaped association that linear tests miss.** Its linear association is null (OR 0.98, p = 0.75 in the multivariable model). Adding a squared term is strongly supported (LR chi2 = 246.6, p = 1.4e-55; AIC 1,056.8 vs 1,301.5), and the adjusted curve has its minimum near feat_a = 0.
- **No pairwise interaction among the three features is significant** (smallest p = 0.323 for feat_b:feat_c), though non-significance does not establish that the features act independently.
- **The best model, gradient boosting, beats the majority-class baseline modestly.** On 200 test rows it reaches accuracy 0.695 vs 0.620 for the baseline and ROC AUC 0.690 vs 0.500. The AUC has no reported interval, and the model shows signs of overfitting.
- **The models disagree on feature importance.** Logistic regression ranks feat_b first; gradient boosting ranks feat_a first. This disagreement holds on both test splits examined, and feat_c has no reliable importance in either model.

## Data

- **Size:** 1,000 rows × 4 columns.
- **Target:** `outcome`, binary. 380 rows are positive (outcome = 1, 38.0%) and 620 are negative (outcome = 0, 62.0%).
- **Features:** three numeric features (feat_a, feat_b, feat_c). There are no categorical, date/time, identifier or free-text columns.
- **Missing values:** none in any column.

## Findings

### Outcome rate across each feature's range

- feat_a has a U-shaped relationship with outcome. The rate is 60% in the lowest quintile, falls to 16% in the third quintile (feat_a between -0.246 and 0.22), and rises to 60.8% in the highest quintile. Each bin holds about 200 rows.
- feat_b has a monotone increasing relationship with outcome. The rate rises from 26% in the lowest quintile to 36.5% in the middle quintile and 50% in the highest, with 200 rows per bin.
- feat_c shows no meaningful relationship. Quintile rates range only from 36.5% to 39.5%, close to the overall 38%.

![Share of rows with outcome=1 within each quintile bin of feat_a, feat_b and feat_c; dashed line is overall rate of 38%](tasks/eda_1/charts/eda1_rate_by_quintile.png)

### Group-wise association tests

- **feat_b is significantly associated with outcome.** Mean feat_b is 0.248 for outcome = 1 and -0.115 for outcome = 0. Welch p < 0.0001 and Mann-Whitney p < 0.0001. Cohen's d is 0.381 (95% CI 0.252 to 0.510). The logistic OR per SD is 1.475 (95% CI 1.289 to 1.687). The association remains significant after Bonferroni correction across the three features.
- **feat_a shows no significant linear association.** Welch p = 0.844, Mann-Whitney p = 0.949, Cohen's d = -0.015 (95% CI -0.142 to 0.113), and logistic OR per SD = 0.986 (95% CI 0.867 to 1.120). These linear tests do not rule out the nonlinear pattern seen in the binned rates.
- **feat_c shows no significant association.** Welch p = 0.621, Mann-Whitney p = 0.661, Cohen's d = 0.032 (95% CI -0.095 to 0.160), and logistic OR per SD = 1.033 (95% CI 0.909 to 1.174). Bonferroni-adjusted p-values are all 1.0.

![Mean of feat_a, feat_b and feat_c for outcome=0 and outcome=1; error bars are 95% CIs of the mean](tasks/stat_1/charts/stat1_group_means.png)

### Multivariable model and nonlinearity of feat_a

- **Base model (all three features, linear):** feat_b remains significant, OR 1.50 per raw unit (95% CI 1.31 to 1.73), p = 1.1e-8. feat_a has OR 0.98 (95% CI 0.86 to 1.11), p = 0.75. feat_c has OR 1.06 (95% CI 0.93 to 1.21), p = 0.35.
- **Model with a squared feat_a term:** The squared term is significant, with OR 2.80 per unit of feat_a squared (95% CI 2.36 to 3.32), Wald p = 1.2e-32. The likelihood-ratio test against the base model gives chi2 = 246.6, p = 1.4e-55. AIC is 1,301.46 for the base model and 1,056.84 for the squared-term model, so the squared-term model fits better.
- **Shape of the adjusted feat_a effect:** The linear feat_a term in this model is null (OR 1.003, 95% CI 0.853 to 1.180, p = 0.97). The vertex is at feat_a = -0.0015, inside the observed range of -3.267 to 2.804. The fitted curve rises on both sides of the vertex within that range, so the adjusted feat_a effect is U-shaped with its minimum near 0.
- **feat_b in the squared-term model:** feat_b remains strongly significant, OR 1.82 per raw unit (95% CI 1.54 to 2.14), p = 1.5e-12.

![Adjusted odds ratios with 95% CIs: base model (feat_a, feat_b, feat_c) and the feat_a squared term from the model that adds it (OR per unit of feat_a squared)](tasks/stat_3/charts/stat3_adjusted_or.png)

![Left: adjusted ORs of the base multivariable model per raw unit of each feature. Right: OR per unit of feat_a squared from the model that adds it. Separate panels, separate units.](tasks/stat_3/charts/stat3_adjusted_or_panels.png)

### Interactions

- No pairwise interaction in the logistic regression is significant. Coefficients are per raw unit of each feature.
  - feat_b:feat_c: coefficient 0.073, p = 0.323, 95% CI -0.071 to 0.216.
  - feat_a:feat_b: coefficient 0.053, p = 0.440, 95% CI -0.082 to 0.189.
  - feat_a:feat_c: coefficient -0.010, p = 0.885, 95% CI -0.140 to 0.121.
- Because no interaction is significant, the 2×2 median-split analysis was not run.
- There is no evidence that feat_b's association depends on feat_a or feat_c. Non-significance does not establish independence.

### Predictive modeling

- **Setup:** A single stratified 80/20 split (random_state = 42) gives 800 training rows (304 positive, 38%) and 200 test rows (76 positive, 38%). Features were standardized using training-set statistics only.
- **Test-split scores:**

| Model | Accuracy | ROC AUC | Log loss |
|---|---|---|---|
| Majority-class baseline | 0.620 | 0.500 | 13.70 (unusable; assigns probability 0 to the positive class) |
| Logistic regression | 0.625 | 0.588 | 0.649 |
| Gradient boosting | 0.695 | 0.690 | 0.631 |

- Logistic regression's accuracy is no better than predicting the majority class. Its gain is in probability quality. A constant prediction at the training positive rate (0.38) has log loss 0.664.
- Gradient boosting's test precision is 0.667, recall 0.395 and F1 0.496. Its training accuracy is 0.864, against 0.695 on test.
- The gain is real but modest and uncertain. The gradient boosting ROC AUC comes from 200 test rows, and no interval is reported. Its log loss of 0.631 is only modestly below the constant-prior value of 0.664.

![Test-split ROC AUC of the majority-class baseline, logistic regression and gradient boosting](tasks/ml_2/charts/ml2_model_auc.png)

### Feature importance: the two models disagree

- **Logistic regression (standardized coefficients):** feat_b 0.397, feat_c 0.043, feat_a -0.035.
- **Gradient boosting (impurity importance, which sums to one):** feat_a 0.632, feat_b 0.238, feat_c 0.130.
- These two measures are on different scales and cannot be compared directly. The task recorded that gradient boosting's large feat_a importance is consistent with the nonlinear feat_a pattern, and that feat_b is the strongest linear predictor. These are interpretations from the team and are not established by the test.
- **Permutation importance (drop in test ROC AUC, 30 repeats), seed-0 split:**
  - Logistic regression: feat_b 0.094, feat_a 0.000, feat_c -0.016.
  - Gradient boosting: feat_a 0.200, feat_b 0.050, feat_c -0.008.
- **Permutation importance, ml_1 split (random_state = 42), seed 0:**
  - Logistic regression: feat_b 0.088, feat_c 0.003, feat_a -0.002.
  - Gradient boosting: feat_a 0.148, feat_b 0.037, feat_c 0.008.
- **Stability:** Across permutation seeds 0 to 2, the mean values move little. On the seed-0 split, logistic feat_b ranges from 0.094 to 0.110 and gradient boosting feat_a from 0.196 to 0.204. The SD across 30 repeats is about 0.03 to 0.04 for the top features.
- **Ordering below the top feature:** The order of the lower-ranked features changes between the two splits, so the full ranking is not stable.
- **feat_c:** On the seed-0 split its mean drop is negative in both models, meaning permuting it slightly raised test ROC AUC. On the ml_1 split it is slightly positive, with repeat SDs of 0.005 to 0.009. Its position in either ranking is noise.

![Mean drop in test ROC AUC when each feature is permuted (bars: mean over 30 repeats, error bars: SD), for logistic regression and gradient boosting on the test split](tasks/ml_3/charts/ml3_perm_importance.png)

## Limitations

- **Small test sets:** All model scores and permutation importances come from 200-row test splits. The gradient boosting ROC AUC of 0.690 has no reported interval.
- **Single splits:** Model comparison and permutation importance were computed on one or two splits. Results were not checked with cross-validation or bootstrap resampling.
- **Overfitting:** Gradient boosting's training accuracy (0.864) well exceeds its test accuracy (0.695). No tuning was done.
- **Model form:** The logistic model is linear in the features except for the squared feat_a term examined in stat_3. The interaction tests use raw, unstandardized features in a linear logit.
- **Inconsistent feat_a results across analyses:** Linear tests show no association for feat_a, while the squared-term model and the binned rates show a U-shape. Both results are reported; they are not reconciled.
- **Association only:** All findings describe associations within this dataset.
- **Interaction non-significance:** The interaction tests do not establish that the features act independently.
- **Importance scales:** Logistic coefficients and gradient boosting impurity importances are not comparable, and permutation importance was measured only as the drop in ROC AUC.
- **Unresolved review issues and failed tasks:** None recorded.

## Open questions

- Does the feat_a U-shape hold up under a spline, and does a logistic model with a quadratic or spline term for feat_a match gradient boosting's test performance? If so, does it reproduce gradient boosting's feat_a importance?
- Do feat_a and feat_b interact, or feat_a and feat_c, once feat_a is modeled nonlinearly? The interaction tests so far used only linear feat_a terms.
- Does feat_b's effect hold after adjusting for the nonlinear feat_a term? The stat_3 squared-term model suggests it does (OR 1.82, p = 1.5e-12), but no interaction term was tested.
- What confidence intervals do the ROC AUC values and permutation importances have under bootstrap resampling or cross-validation? Does the gain over the constant prior hold across resamples?
- Does permutation importance computed on cross-validation folds, rather than one 200-row split, give a stable ordering of feat_a, feat_b and feat_c?
- Does tuning gradient boosting (depth, learning rate, early stopping) reduce the train-test gap and improve test log loss?