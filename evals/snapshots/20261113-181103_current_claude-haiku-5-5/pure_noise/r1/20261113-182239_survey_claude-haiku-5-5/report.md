# Outcome Analysis of an 800-Row Survey: Group, Five Numeric Features, and Predictive Models

## Summary

- **No statistically supported association between outcome and group or the numeric features.** Outcome rates descend across groups from 46.2% (g1) to 36.8% (g4), but the chi-square test gives p = 0.289 (Cramér's V = 0.068). No numeric feature differs between outcome classes after Holm correction (all adjusted p = 1.0), and all effect sizes are negligible (|Cohen's d| ≤ 0.090).
- **No feature-by-group interaction survives correction.** The lowest raw interaction p-value is 0.030 (feat_3), which becomes 0.148 after Holm correction.
- **No model beats the majority-class baseline.** On the single 160-row test split, logistic regression reaches 55.0% accuracy and gradient boosting 53.1%, against a 58.75% baseline. Repeated stratified 5×10 cross-validation on all 800 rows gives a mean ROC AUC of 0.500 for logistic regression (chance) and 0.4732 for gradient boosting.
- **Feature importances do not indicate genuine predictive signal.** feat_3 ranks first under permutation importance, but the logistic model's test ROC AUC (0.391) is below chance, so the ranking describes what the fitted model uses, not out-of-sample contribution.

## Data

- **Size:** 800 rows × 7 columns: five numeric features (feat_1 to feat_5), one categorical column (group, four levels: g1 n = 182, g2 n = 206, g3 n = 200, g4 n = 212), and a binary target (outcome).
- **Target:** 329 rows have outcome = 1 (41.1%) and 471 have outcome = 0 (58.9%).
- **Missing values:** None. All seven columns have zero missing entries.
- **Other features:** No date/time or identifier columns, and no free-text columns.

## Findings

### Distributions and outcome rates by group

The five numeric features are roughly standardized. Means range from 0.001 (feat_2) to 0.060 (feat_4), and standard deviations from 0.985 (feat_4) to 1.021 (feat_1).

![Histograms of the five numeric features (counts of rows per bin)](tasks/eda_1/charts/feature_histograms.png)

Outcome rates by group were g1 46.2%, g2 42.2%, g3 40.0% and g4 36.8%.

![Outcome rate by group (share of rows with outcome=1)](tasks/eda_1/charts/outcome_rate_by_group.png)

Group-level feature means differ descriptively from the overall means. Group g3 has a feat_4 mean of 0.204 (overall 0.060) and a feat_5 mean of 0.125. Group g4 has a feat_1 mean of 0.121 and a feat_3 mean of 0.123 (overall 0.006 and 0.021). Groups g1 and g2 sit near zero on most features. These are descriptive only; no test was run at this stage.

### Association of outcome with group

- Chi-square test of outcome by group: χ² = 3.754, df = 3, p = 0.289, Cramér's V = 0.068 (n = 800). This is a negligible association, and the outcome-rate differences across groups are not statistically significant.
- The chi-square test is a single omnibus test and was not corrected for multiple comparisons.

### Numeric features by outcome class

Welch t-tests compared outcome = 1 with outcome = 0 for each feature, with Holm correction across the five tests.

| Feature | Mean difference | 95% CI | Cohen's d | Raw p | Holm p |
|---|---|---|---|---|---|
| feat_1 | -0.014 | (-0.160, 0.132) | -0.013 | 0.855 | 1.0 |
| feat_2 | 0.017 | (-0.124, 0.158) | 0.017 | 0.813 | 1.0 |
| feat_3 | -0.082 | (-0.222, 0.057) | -0.083 | 0.246 | 1.0 |
| feat_4 | -0.005 | (-0.143, 0.133) | -0.005 | 0.944 | 1.0 |
| feat_5 | 0.091 | (-0.051, 0.233) | 0.090 | 0.207 | 1.0 |

- No feature differs between outcome classes after correction. The raw p-values range from 0.207 (feat_5) to 0.944 (feat_4).
- All effect sizes are near zero, and all five confidence intervals include zero.

### Feature-by-group interactions

Logistic regression likelihood-ratio tests (3 df) assessed whether each feature's effect on outcome differs by group.

| Feature | LR χ² | Raw p | Holm p |
|---|---|---|---|
| feat_1 | 0.951 | 0.813 | 1.0 |
| feat_2 | 6.287 | 0.098 | 0.394 |
| feat_3 | 8.985 | 0.030 | 0.148 |
| feat_4 | 1.301 | 0.729 | 1.0 |
| feat_5 | 3.485 | 0.323 | 0.968 |

- No interaction is significant after Holm correction.
- feat_3 is the closest to a group-dependent effect, but the evidence is weak. Exploratory per-unit odds ratios by group for feat_3 were g1 1.02 (95% CI 0.754 to 1.38), g2 0.672 (0.504 to 0.896), g3 0.899 (0.679 to 1.19) and g4 1.219 (0.914 to 1.628). The nominal drop in g2 should not be treated as an established effect.
- Per-group odds ratios for feat_2 (g1 0.895, g2 1.266, g3 1.151, g4 0.815) all have confidence intervals that include 1. These per-group odds ratios are exploratory and are not reported as primary results for any feature.

### Group-level feature shifts and the group rate gaps

Welch tests compared each shifted feature in the named group against the other groups. These were run as four tests and were not corrected together.

- **feat_4 in g3:** higher by 0.193 (95% CI 0.032 to 0.353; d = 0.196; p = 0.019). This is nominally significant but does not survive a Bonferroni correction for the four shift tests.
- **feat_1 in g4:** higher by 0.157 (95% CI 0.001 to 0.312; d = 0.154; p = 0.049). This is borderline and does not survive correction for four tests.
- **feat_5 in g3:** higher by 0.115 (95% CI -0.049 to 0.279; d = 0.114; p = 0.169). Not significant.
- **feat_3 in g4:** higher by 0.139 (95% CI -0.016 to 0.294; d = 0.139; p = 0.079). Not significant.

![Mean differences of shifted features in the named group versus all other groups, with 95% Welch CIs](tasks/stat_3/charts/feature_shift_diffs.png)

Outcome rate gaps:
- **g3:** outcome rate 0.400 versus 0.415 in other groups (difference -0.015, 95% CI -0.094 to 0.064; chi-square p = 0.71). Not significant.
- **g4:** outcome rate 0.368 versus 0.427 in other groups (difference -0.059, 95% CI -0.135 to 0.017; chi-square p = 0.13). Not significant.

Adjustment for the shifted features:
- Unadjusted odds ratios were g3 0.846 (95% CI 0.598 to 1.197, p = 0.34) and g4 0.739 (95% CI 0.524 to 1.042, p = 0.084).
- Adjusted for feat_1, feat_3, feat_4 and feat_5, the g3 odds ratio is 0.829 (95% CI 0.585 to 1.176) and the g4 odds ratio is 0.739 (95% CI 0.523 to 1.045). Neither group effect is significant in either model.
- Per-SD odds ratios for the shifted features without group were feat_1 0.993 (p = 0.919), feat_3 0.915 (p = 0.223), feat_4 0.996 (p = 0.956) and feat_5 1.099 (p = 0.186). All confidence intervals span 1.
- The unadjusted group gaps were already non-significant, so the adjustment does not explain a significant gap.

### Predictive models (single 160-row test split)

The data were split 80/20, stratified, with random_state = 42, giving 640 training and 160 test rows. Group was one-hot encoded and numeric features were standardized on training statistics.

- **Majority-class baseline:** 58.75% test accuracy (94 of 160). Its test log-loss is 0.678, computed using the training positive rate as a constant probability. The 58.9% figure in the profile is the class-0 share of all 800 rows, not the test baseline.
- **Logistic regression:** 55.0% test accuracy, precision 0.313, recall 0.076, F1 0.122, ROC AUC 0.391, log-loss 0.708. Training accuracy was 58.4%.
- **Gradient boosting:** 53.1% test accuracy, precision 0.400, recall 0.273, F1 0.324, ROC AUC 0.466, log-loss 0.754. Training accuracy was 83.6%.

![Test accuracy of the majority-class baseline, logistic regression and gradient boosting on the 160-row stratified test set](tasks/ml_1/charts/model_test_accuracy.png)

Neither model beats the baseline on accuracy, log-loss or ROC AUC on this split.

### Feature importance

Permutation importance was computed for the logistic regression on the test set (50 repeats; change in ROC AUC).

| Feature | Mean drop | SD |
|---|---|---|
| feat_3 | 0.0214 | 0.0079 |
| group_g1 | 0.0082 | 0.0194 |
| feat_2 | 0.0052 | 0.0064 |
| group_g3 | -0.0037 | 0.0016 |
| feat_4 | -0.0112 | 0.0092 |
| group_g2 | -0.0151 | 0.0117 |
| feat_1 | -0.0192 | 0.0101 |
| feat_5 | -0.0389 | 0.0220 |
| group_g4 | -0.0587 | 0.0282 |

![Permutation importance on the 160-row test set for the logistic regression from ml_1; bars show mean ROC AUC drop per feature, error bars the SD over 50 permutations](tasks/ml_2/charts/ml2_permutation_importance.png)

- feat_3 is the only feature whose mean drop clearly exceeds its SD. The ranking beyond feat_3 is unstable, since group_g1's SD is more than twice its mean drop.
- The logistic regression was selected as the "best" model because it had the higher test accuracy (55.0% versus 53.1%). The selection criterion is not recorded, so this choice is an assumption.
- Gradient boosting's built-in importance ranked feat_3 first (0.249), followed by feat_4 (0.196) and feat_1 (0.181). Permutation importance was not computed for this model.
- **Disagreement:** the permutation result points to feat_3, which is the closest to a group-dependent effect in the statistical tests, but none of the statistical tests confirms a feature effect. The importances are computed on a model whose test ROC AUC (0.391) is below chance.

### Repeated cross-validation

Repeated stratified 5×10 cross-validation was run on all 800 rows, with preprocessing inside each fold. The 50 folds are not independent, so the SDs understate uncertainty about the means.

| Model | Accuracy (SD) | ROC AUC (SD) | Log-loss (SD) |
|---|---|---|---|
| Logistic regression | 57.1% (2.1) | 0.500 (0.041) | 0.685 (0.009) |
| Gradient boosting | 53.9% (3.2) | 0.4732 (0.0395) | 0.752 (0.030) |
| Constant prior (majority) | 58.9% (0.3) | 0.500 (0.0) | 0.677 (0.001) |

![Mean ROC AUC per model over repeated stratified 5x10 CV on all 800 rows; error bars are SD across folds; dashed line is chance (0.5).](tasks/ml_3/charts/cv_roc_auc_by_model.png)

- Logistic regression's mean ROC AUC of 0.500 is chance level. The single-split value of 0.391 lies about 2.7 fold-SDs below this mean, so the single-split result is consistent with a chance-level model.
- Gradient boosting's mean ROC AUC of 0.4732 is below 0.5. Because the folds are correlated, this does not establish a reliable below-chance effect. The single-split value of 0.466 is close to the CV mean.
- Neither model's accuracy reaches the majority baseline, and both models' log-loss is worse than the constant-probability value.
- This CV run reports only held-out metrics. It contains no training-fold scores, so it does not test overfitting. The 83.6% training accuracy of gradient boosting from the single split is the only overfitting evidence, and it comes from that split.

## Limitations

- **Weak signal throughout.** No group, feature or interaction effect is statistically significant after correction, and all effect sizes are negligible. The non-significant results do not establish absence of effects.
- **Single test split is small.** The 160-row test split is too small to show whether the models carry any signal. The single-split results are consistent with the repeated-CV results but are not a substitute for them.
- **Logistic regression model selection is assumed.** It was chosen for permutation importance on test accuracy, and the recorded selection rule is absent.
- **Permutation importance is on a sub-chance model.** The logistic regression's test ROC AUC is 0.391, so its importances do not show genuine predictive contribution.
- **Exploratory feature-by-group odds ratios.** The per-group feat_3 and feat_2 odds ratios come from exploratory fits and rest on non-significant interactions.
- **Group-shift tests were not corrected jointly.** The g3 feat_4 and g4 feat_1 shifts are borderline and do not survive correction for the four shift tests.
- **Gradient boosting claim softened (unresolved review issue).** The lead objected to the wording that gradient boosting shows "genuinely no discrimination and is worse than chance." The supported statement is that the mean CV ROC AUC of 0.4732 is below 0.5, and because the 50 folds are correlated, this does not establish a reliable below-chance effect. The SD understates uncertainty about the mean. This affects the gradient boosting results in the cross-validation section.
- **Summary values transcribed (unresolved review issue).** The lead objected that the cv_auc_vs_chance values should come from the computed CV results or be stated as transcribed. These values were transcribed rather than computed directly in that task; only the single-split values 0.391 and 0.466 are literal inputs from the earlier task. This affects the comparison of CV and single-split AUCs.
- **Overfitting not tested in CV.** No training-fold scores were recorded, so gradient boosting's worse log-loss cannot be separated into overfitting or miscalibration from the CV run.
- **Descriptive group comparisons.** The group-level feature means in the EDA were descriptive only; the later shift tests in stat_3 are the tests of those differences.
- **Missingness:** not a concern, as no values are missing in any column.
- **Failed tasks:** none reported.

## Open questions

- Are the group-level outcome-rate differences (0.368 to 0.462) real? The chi-square test gives p = 0.289, and the CIs for the group gaps include zero.
- Do the g3 feat_4 shift and the g4 feat_1 shift replicate in new data, given that they do not survive correction?
- Is the feat_3 by group pattern real (weaker effect in g2)? The uncorrected interaction p is 0.030, and a larger sample or a pre-specified contrast is needed to check it.
- Do any of feat_1 to feat_5 or group carry signal at all? A permutation test on the CV AUC would show whether the logistic regression's 0.500 differs from chance.
- Why does gradient boosting fall below chance in AUC and log-loss? Its tuning (depth, learning rate, number of trees) and per-fold train-versus-CV scores were not examined.
- Do non-linear feature effects (splines, quadratic terms) or feature-by-feature interactions improve on the linear models tested here?
- Do regularized or shallower gradient boosting, or spline features, improve log-loss relative to the constant baseline?
- Do the group-level outcome-rate differences remain after adjusting for the numeric features in a logistic model? The adjusted g3 and g4 odds ratios (0.829 and 0.739) are not significant, but a fuller model with interactions was not fitted.
- Is the feat_3 permutation importance stable for gradient boosting, which ranked feat_3 first by built-in importance?