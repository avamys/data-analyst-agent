# Outcome Analysis of an 800-Row Dataset: Group, Five Numeric Features, and a Binary Target (`outcome`)

## Summary

- **Group and outcome:** The outcome is 41.1% positive. Outcome rates fall from 46.2% in g1 to 36.8% in g4, but this difference is not statistically significant (chi-square p=0.289, Cramér's V=0.068).
- **Numeric features and outcome:** No numeric feature differs significantly between outcome classes. The largest raw difference, feat_5 (outcome=1 minus outcome=0: +0.091, Welch p=0.207), is not significant after multiplicity correction (BH p=0.579).
- **Interactions and linearity:** Group does not significantly modify the feature–outcome associations (LR 21.41 on 15 df, p=0.124). Tests for nonlinearity on the logit scale show no significant departure from linearity.
- **Prediction:** Neither model beats the majority-class baseline (accuracy 0.5875) on the 160-row test split: logistic regression reaches 0.550 and gradient boosting 0.531. Repeated cross-validated ROC AUC is 0.505 for logistic regression on all features, 0.522 for group alone, and 0.465 for gradient boosting. The features carry little out-of-sample signal for the outcome.

## Data

- **Size:** 800 rows, 7 columns.
- **Target:** `outcome`, binary. Class 0 is 58.9% and class 1 is 41.1%.
- **Features:** Five numeric features (feat_1 to feat_5) and one categorical feature, `group` (g1, g2, g3, g4). No date/time features and no identifier or free-text columns.
- **Missing values:** None in any column.

## Findings

### Outcome rate and feature averages by group

The outcome rate and row count for each group were:

| Group | Outcome rate | n |
|---|---|---|
| g1 | 46.2% | 182 |
| g2 | 42.2% | 206 |
| g3 | 40.0% | 200 |
| g4 | 36.8% | 212 |

![Share of rows with outcome=1 in each group (g1 to g4)](tasks/eda_1/charts/outcome_rate_by_group.png)

These are descriptive differences; the significance test is reported under the next topic.

Feature means were standardized overall (means near 0, standard deviations near 1). Across the four groups, feat_4 has the largest spread in group means (0.263; g3 0.204 versus g1 −0.059). The other spreads are feat_1 (0.191), feat_3 (0.174), feat_5 (0.150) and feat_2 (0.042). Group standard deviations range from about 0.96 to 1.07. No significance test was run at this stage.

By outcome class, the descriptive differences in means were:

- feat_5: 0.092 when outcome=1 versus 0.001 when outcome=0, the largest difference.
- feat_3: −0.027 versus 0.055.
- feat_1: −0.002 versus 0.011.
- feat_2: 0.011 versus −0.006.
- feat_4: 0.057 versus 0.062, nearly identical.

Standard deviations per class are close to 1. For outcome=1, feat_3 (0.967 versus 1.015) and feat_4 (0.958 versus 1.005) are somewhat smaller, and feat_1 is larger (1.067 versus 0.989).

### Significance of group and numeric features against outcome

**Numeric features.** Five Welch t-tests and one chi-square test were run and corrected for multiplicity across the six tests. No test is significant: Holm-adjusted p=1.0 for all, and the smallest BH-adjusted p is 0.579.

| Feature | Mean diff (1 minus 0) | 95% CI | Welch p | Cohen's d | Mann-Whitney p | BH p |
|---|---|---|---|---|---|---|
| feat_1 | −0.014 | −0.160 to 0.132 | 0.855 | −0.013 | 0.740 | 0.944 |
| feat_2 | +0.017 | −0.124 to 0.158 | 0.813 | 0.017 | 0.978 | 0.944 |
| feat_3 | −0.082 | −0.222 to 0.057 | 0.246 | −0.083 | 0.179 | 0.579 |
| feat_4 | −0.005 | −0.143 to 0.133 | 0.944 | −0.005 | 0.864 | 0.944 |
| feat_5 | +0.091 | −0.051 to 0.233 | 0.207 | 0.090 | 0.210 | 0.579 |

The rank-biserial effects are small: about 0.052 in magnitude for feat_5 and 0.056 for feat_3. The records disagree on their sign. One record lists feat_5 as +0.052 and feat_3 as −0.056. The per-feature test record lists feat_5 as −0.052 and feat_3 as +0.056. The direction of these effects is therefore unresolved, and only magnitudes are reported.

The EDA finding that feat_5 differs most between outcome classes is consistent with the raw difference above. That difference is not statistically significant.

**Group.** The outcome rate differs by group, but not significantly: chi-square=3.75, df=3, p=0.289, Cramér's V=0.068 (negligible association), BH-adjusted p=0.579. The 95% Wilson confidence intervals are 39.1% to 53.4% for g1 and 30.6% to 43.5% for g4, and these intervals overlap.

![Share of rows with outcome=1 in each group g1 to g4, with 95% Wilson confidence intervals](tasks/stat_1/charts/stat1_rate_by_group.png)

### Interaction of group with the numeric features

Adding the five feature-by-group interaction terms (15 df) does not significantly improve the logistic model over main effects: LR 21.41, df 15, p=0.124. The data give no evidence that group modifies the feature–outcome association at the 0.05 level. This does not establish that the main-effects model fits well.

The coefficients for this topic were read from the printed model summary and are not recorded as facts, so they are not reported here. Within that printed output:

- Two interaction terms were borderline: feat_3 × g2 and feat_2 × g2. Neither was significant, and neither would survive correction for the 15 terms tested.
- No other interaction term was significant at 0.05.

Per-group feature effects with confidence intervals were not estimated, because no interaction reached significance.

### Nonlinearity (logit-linearity) checks

- **Quadratic terms:** Adding quadratic terms for all five numeric features does not significantly improve the main-effects logit model: LR 5.72, df 5, p=0.335. Individual quadratic-term p-values were not reported.
- **Natural cubic splines (df=4 per feature):** No significant improvement over the linear model: LR 8.84, p=0.548. The reported df of 10 is unverified (see Limitations). The p-value is large, so the conclusion of no significant nonlinearity holds regardless of the exact df.
- **Interaction test under nonlinearity:** With quadratic terms included, the group-interaction LR test gives LR 23.04, df 15, p=0.083. This is against a different reference model from the linear test above (LR 21.41, p=0.124), so the two p-values are not directly comparable. Both remain above 0.05, so there is still no significant evidence that group modifies the feature–outcome associations.

### Predictive models against the majority-class baseline

All scores below use a single 160-row test split unless stated otherwise.

| Model | Test accuracy | Precision | Recall | F1 | Test ROC AUC | Train accuracy | Test log loss |
|---|---|---|---|---|---|---|---|
| Majority-class baseline | 0.5875 | — | — | — | — | — | — |
| Logistic regression | 0.550 | 0.313 | 0.076 | 0.122 | 0.391 | 0.584 | 0.708 |
| Gradient boosting | 0.531 | 0.400 | 0.273 | 0.324 | 0.467 | 0.836 | 0.754 |

- Neither model beats the majority-class baseline on accuracy.
- Both are worse than a constant predictor at the training outcome rate, which scores log loss 0.678 on the test split.
- Gradient boosting overfits: train accuracy 0.836 against test accuracy 0.531.
- The test ROC AUC values are noisy with 160 rows and are not strong evidence of worse-than-random ranking.

**Five-fold cross-validation on the full data.** Mean ROC AUC was 0.533 (SD 0.040) for logistic regression and 0.458 (SD 0.027) for gradient boosting. Gradient boosting is slightly below chance; logistic regression is only marginally above it. The repeated CV results in the next topic use 25 folds and are reported alongside these figures.

**Feature importance.** Logistic regression's largest absolute coefficients are group_g4 (0.356), group_g1 (0.202), feat_5 (0.137), group_g2 (0.133), feat_1 (0.064), feat_4 (0.054), feat_3 (0.049), feat_2 (0.034) and group_g3 (0.024). These coefficients come from a model with near-chance accuracy and do not show reliable effects.

Grouped permutation importance on gradient boosting, by mean drop in test ROC AUC, was: feat_3 (0.014), feat_4 (0.011), feat_2 (0.010), feat_1 (−0.007), feat_5 (−0.009) and group (−0.012). Only the top three have positive drops, and they are small. No input can be called reliably important.

![Mean drop in test ROC AUC when each input is shuffled](tasks/ml_1/charts/ml_1_perm_importance.png)

### Repeated stratified cross-validation and group-only model

Repeated 5×5 stratified CV was run with two CV seeds.

- **Gradient boosting (all features):** Mean ROC AUC 0.465 (SD 0.041) with seed 42. Per-repeat means ranged from 0.454 to 0.473. With seed 7, mean ROC AUC was 0.471 (SD 0.040), with per-repeat means from 0.458 to 0.486. The seed-42 mean differs from the five-fold value in the previous topic (0.458) because it uses 25 folds over 5 repeats. The split alone moves the mean by about 0.006, so the level is only roughly stable.
- **Logistic regression, all features:** Mean ROC AUC 0.505 (SD 0.039), at chance.
- **Logistic regression, group only:** Mean ROC AUC 0.522 (SD 0.037). This is the highest mean of the three models.
- **Paired difference (all features minus group only):** −0.018 (paired SD 0.046). The fold-level paired p is 0.065, and the repeat-level paired p is 0.275. The data do not show that the features add signal over group alone, but this does not show that they add none.

Whether gradient boosting is significantly below 0.5 is unresolved. The fold-level one-sample test (t=−4.25, p=0.0003) treats 25 correlated folds as independent and is invalid. The repeat-level test on the five seed-42 means (t=−9.10, p=0.0008) has only 4 degrees of freedom and reflects only CV-split variation, not the sampling uncertainty of the 800 rows. Both point the same way, but neither is a valid basis for a firm significance claim. The group-only model's fold-level one-sample p-value (0.006) has the same validity problem, so the significance of the group signal is also unresolved.

![Repeated 5x5 stratified CV ROC AUC per fold for gradient boosting and logistic regression (all features and group only)](tasks/ml_2/charts/ml_2_cv_auc_boxplot.png)

## Limitations

- **Sample size and noise.** The test split has 160 rows, so ROC AUC and accuracy on it are noisy. Repeated CV reduces but does not remove this noise. The study's power to detect the small feat_5 (d≈0.09) and feat_3 (d≈−0.08) differences was not assessed, and the power for the borderline interactions was not assessed either.
- **Unsettled significance tests.** The fold-level tests in the repeated CV analysis treat correlated folds as independent. The repeat-level tests have 4 degrees of freedom and capture only CV-split variation. Neither gives a valid significance claim for gradient boosting being below 0.5, or for the group-only signal.
- **Unresolved review issue: spline degrees of freedom (stat_3).** The spline test reports LR 8.84 with df 10. The explanation given (one basis column per feature absorbed by the intercept) was not verified and does not match the arithmetic, since 5 features × 3 extra columns would give 15. The df was not verified, so the p-value (0.548) depends on an unconfirmed df. The conclusion of no significant nonlinearity is retained, because the p-value is large.
- **Unresolved review issue: hardcoded ml_1 values in ml_2.** The ml_1 gradient boosting values used for comparison in ml_2 (mean 0.458, SD 0.027) were hardcoded from the ml_1 record and were not recomputed in ml_2. This task cannot be redone, so the issue remains unresolved.
- **Unresolved review issue: per-repeat ranges (ml_2).** The seed-7 per-repeat range is 0.458 to 0.486, and the seed-42 maximum is 0.473. These corrected figures are used above. The corrections were made on review and could not be confirmed by rerunning the task.
- **Rank-biserial sign disagreement (stat_1).** The records disagree on the sign of the rank-biserial effects for feat_3 and feat_5. Only magnitudes are reported.
- **Coefficients from printed output.** The interaction and main-effect coefficients in stat_2 and the logistic regression coefficients in ml_1 were read from printed model summaries and are not recorded as facts. For this reason, no coefficient values or interaction p-values are reported.
- **Model specification.** Logit linearity was checked only with omnibus tests (quadratic and spline terms). Individual terms were not examined, and the main-effects model's overall fit was not assessed.
- **Not estimated.** Per-group feature effects with confidence intervals were not estimated. The hypothesis that feature-mean differences across groups explain the group outcome-rate gap (mediation) was not tested.
- **Failed tasks.** None. All six tasks (eda_1, stat_1, stat_2, stat_3, ml_1, ml_2) are recorded as complete, though stat_3 and ml_2 carry the unresolved issues listed above.

## Open questions

- Does feat_5 remain a predictor of outcome after adjusting for group in a joint logistic model with group dummies and features? The adjusted feat_5 effect was not formally reported.
- Do the feature-mean differences across groups (feat_4 and feat_1 in particular) explain the group outcome-rate gap, through a mediation or adjusted model?
- Is the study powered to detect the feat_3 × g2 and feat_2 × g2 interactions, or the small feat_5 and feat_3 per-class differences?
- Does the feat_5 × g4 slope differ meaningfully from the other groups once sample size is considered?
- Would a bootstrap over rows, or a larger dataset, give a valid test of whether gradient boosting is below 0.5?
- Does the group-only advantage over the full feature set hold across more CV seeds, more repeats, and nested tuning?
- Is there leakage, a different outcome definition, or missing information that would explain why no model beats the majority-class baseline and gradient boosting ranks below chance? The outcome definition and data collection were not examined.
- Do the quadratic and spline results hold for individual terms, and does the logit-linearity assumption hold for each feature separately?