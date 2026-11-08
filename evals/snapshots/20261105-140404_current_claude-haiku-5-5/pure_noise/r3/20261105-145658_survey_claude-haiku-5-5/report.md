# Outcome Analysis of an 800-Row Survey (Binary Outcome, Groups g1 to g4, Five Numeric Features)

## Summary

- **Group and outcome:** The outcome rate falls from 46.2% in g1 to 36.8% in g4, but the chi-square test (χ² = 3.754, 3 df, p = 0.289, Cramér's V = 0.068) finds no significant relationship. No pairwise group comparison survives Holm correction; the smallest adjusted p is 0.390 (g1 vs g4).
- **Numeric features:** No feature differs significantly between outcome classes (smallest Welch p = 0.207, for feat_5). After adjusting for group, no feature is significantly associated with outcome (smallest Holm p = 0.90, for feat_5).
- **Interaction:** The feat_3 × group interaction is nominally significant (p = 0.029) but does not survive correction across the five features. Within g2 alone, feat_3 has an odds ratio of 0.67 per unit (p = 0.007), a post hoc finding that has not been confirmed.
- **Prediction:** No model beats the 58.8% majority-class baseline on the 160-row test set. Logistic regression reaches 55.0% accuracy and random forest 50.6%. Test ROC AUC is below 0.5 for both models on the seed-42 split, but across 30 other splits the mean is near chance (0.503 for logistic regression, 0.482 for random forest).
- **Missing data:** None. All 800 rows and 7 columns are complete, so no missingness analysis was needed.

## Data

- **Size:** 800 rows × 7 columns: five numeric features (feat_1 to feat_5), one categorical group column (g1 to g4), and the binary outcome.
- **Target:** outcome. 329 of 800 rows are positive (41.1%); 471 are negative (58.9%).
- **Group sizes:** g1 = 182, g2 = 206, g3 = 200, g4 = 212.
- **Missing values:** None in any column.
- **Date/time features and free-text or ID columns:** None.

## Findings

### Overall outcome and rates by group

The overall positive rate is 41.1% (329 of 800). Outcome rates by group are:

| Group | n | Positives | Rate |
|---|---|---|---|
| g1 | 182 | 84 | 46.2% |
| g2 | 206 | 87 | 42.2% |
| g3 | 200 | 80 | 40.0% |
| g4 | 212 | 78 | 36.8% |

![Outcome rate by group, with row counts per group](tasks/eda_1/charts/outcome_rate_by_group.png)

Feature means and SDs are near 0 and 1 for all five features. By outcome class, feat_5 shows the largest gap (mean 0.092 for outcome 1 vs 0.001 for outcome 0), followed by feat_3 (−0.027 vs 0.055). feat_1 and feat_2 differ very little, and feat_4 barely differs (0.057 vs 0.062).

### Group and outcome

- Chi-square test of outcome vs group: χ² = 3.754, 3 df, p = 0.289, Cramér's V = 0.068 (n = 800). The decline from g1 to g4 is not statistically significant.
- Pairwise outcome-rate risk differences (first minus second group, 95% CI, Holm-adjusted Fisher p):

| Comparison | Risk difference | 95% CI | Holm p |
|---|---|---|---|
| g1 vs g2 | 3.9 points | −6.0 to 13.8 | 1.0 |
| g1 vs g3 | 6.2 points | −3.8 to 16.1 | 1.0 |
| g1 vs g4 | 9.4 points | −0.4 to 19.1 | 0.390 |
| g2 vs g3 | 2.2 points | −7.3 to 11.8 | 1.0 |
| g2 vs g4 | 5.4 points | −3.9 to 14.8 | 1.0 |
| g3 vs g4 | 3.2 points | −6.2 to 12.6 | 1.0 |

The unadjusted Fisher p for g1 vs g4 is 0.065.

### Numeric features and outcome (unadjusted)

Outcome 1 minus outcome 0, with Welch and Mann-Whitney tests:

| Feature | Mean difference | 95% CI | Cohen's d | Welch p | Mann-Whitney p |
|---|---|---|---|---|---|
| feat_1 | −0.014 | −0.160 to 0.132 | −0.013 | 0.855 | 0.740 |
| feat_2 | 0.017 | −0.124 to 0.158 | 0.017 | 0.813 | 0.978 |
| feat_3 | −0.082 | −0.222 to 0.057 | −0.083 | 0.246 | 0.179 |
| feat_4 | −0.005 | −0.143 to 0.133 | −0.005 | 0.944 | 0.864 |
| feat_5 | 0.091 | −0.051 to 0.233 | 0.090 | 0.207 | 0.210 |

No feature shows a detectable difference. Bonferroni alpha across the five tests is 0.01. The CIs do not exclude moderate effects.

### Adjusted association with outcome (controlling for group)

Logistic regression on standardized features with group dummies (reference g1), odds ratio per 1 SD:

| Feature | OR per SD | 95% CI | p | Holm p |
|---|---|---|---|---|
| feat_1 | 0.99 | 0.86 to 1.14 | 0.922 | 1.0 |
| feat_2 | 1.02 | 0.88 to 1.17 | 0.824 | 1.0 |
| feat_3 | 0.92 | 0.80 to 1.06 | 0.275 | 1.0 |
| feat_4 | 1.00 | 0.87 to 1.15 | 0.984 | 1.0 |
| feat_5 | 1.10 | 0.96 to 1.27 | 0.180 | 0.90 |

No association survives correction. These are null results, not evidence of no association.

### Interaction: does a feature's association differ by group?

Likelihood-ratio tests of feature × group interaction in logistic regression (3 df):

- **feat_3:** LR χ² = 8.99, p = 0.029. Nominal only; it does not survive Bonferroni correction across the five features.
- **feat_2:** LR χ² = 6.29, p = 0.098. Borderline.
- **feat_1:** p = 0.81. **feat_4:** p = 0.73. **feat_5:** p = 0.32.

Per-group odds ratios per unit of feat_3, from univariate logistic regression within each group:

- g1: OR 1.02 (95% CI 0.75 to 1.38, p = 0.90, n = 182)
- g2: OR 0.67 (0.50 to 0.90, p = 0.007, n = 206)
- g3: OR 0.90 (0.68 to 1.19, p = 0.46, n = 200)
- g4: OR 1.22 (0.91 to 1.63, p = 0.18, n = 212)

The g2 result is a post hoc subgroup finding. Its Bonferroni check covered only the four groups, not the five features. It is the only group whose odds ratio is clearly below 1. Within g2, the odds ratio per overall SD of feat_3 is 0.67 (95% CI 0.51 to 0.90, p = 0.007).

Per-group odds ratios per unit of feat_2: g1 0.90 (p = 0.43), g2 1.27 (p = 0.093), g3 1.15 (p = 0.35), g4 0.82 (p = 0.16). No individual group is significant.

![Per-group odds ratios of outcome per unit of feat_2 and feat_3, with 95% CI](tasks/stat_2/charts/stat_2_per_group_or.png)

### Predictive models (shared 80/20 stratified split, seed 42; n_train = 640, n_test = 160)

| Model | Train accuracy | Test accuracy | Test precision | Test recall | Test F1 | Test ROC AUC | Test log loss |
|---|---|---|---|---|---|---|---|
| Majority-class baseline | 0.589 | 0.588 | 0.0 | 0.0 | 0.0 | 0.5 | 0.678* |
| Logistic regression | 0.586 | 0.550 | 0.313 | 0.076 | 0.122 | 0.392 | 0.709 |
| Random forest | 0.908 | 0.506 | 0.333 | 0.197 | 0.248 | 0.476 | 0.711 |

*The baseline log loss uses the training positive rate.

- No model beats the majority-class baseline on test accuracy.
- The random forest overfits: a train accuracy of 0.908 against a test accuracy of 0.506 (gap 0.40).
- Both models have worse test log loss than the baseline.
- Test ROC AUC bootstrap 95% CIs (160-row test set, 1000 resamples): logistic regression 0.303 to 0.483; random forest 0.389 to 0.565.
- Five-fold stratified CV on the full data: logistic regression ROC AUC 0.533 (SD 0.040); random forest 0.483 (SD 0.021).

**Stability across splits (30 stratified 80/20 splits, seeds 1 to 30):**

- Logistic regression test ROC AUC: mean 0.503, SD 0.035; 14 of 30 splits (46.7%) below 0.5.
- Random forest test ROC AUC: mean 0.482, SD 0.044; 19 of 30 splits (63.3%) below 0.5.

The seed-42 logistic regression AUC (0.392) lies below the 30-split mean of 0.503 (SD 0.035). Seed 42 is outside the seeds 1 to 30 range used for the spread.

![Test ROC AUC of logistic regression and random forest across 30 stratified 80/20 splits; dashed line marks chance (0.5)](tasks/ml_2/charts/split_auc_per_seed.png)

The random forest mean (0.482) leans slightly below chance. The evidence for this is weak, since the SD is 0.044 and 19 of 30 splits are below 0.5 while the rest are not.

### Feature importance

Permutation importance on the seed-42 test set, drop in ROC AUC (mean, SD), for every feature. The first table is from the 160-row test set in the original model run; the second table is from 30 repeats on the same split.

**Logistic regression (original run)**

| Feature | Mean | SD |
|---|---|---|
| feat_3 | 0.023 | 0.008 |
| group_g1 | 0.009 | 0.021 |
| feat_2 | 0.005 | 0.006 |
| group_g3 | −0.005 | 0.002 |
| feat_4 | −0.010 | 0.009 |
| group_g2 | −0.015 | 0.014 |
| feat_1 | −0.017 | 0.009 |
| feat_5 | −0.039 | 0.022 |
| group_g4 | −0.053 | 0.029 |

**Random forest (original run)**

| Feature | Mean | SD |
|---|---|---|
| feat_4 | 0.022 | 0.022 |
| feat_3 | 0.001 | 0.027 |
| group_g1 | −0.001 | 0.006 |
| group_g2 | −0.002 | 0.010 |
| group_g3 | −0.005 | 0.006 |
| feat_1 | −0.007 | 0.031 |
| group_g4 | −0.011 | 0.019 |
| feat_5 | −0.016 | 0.020 |
| feat_2 | −0.019 | 0.017 |

**30-repeat values, seed-42 split**

- Logistic regression: feat_1 −0.018 (SD 0.010), feat_2 0.004 (SD 0.006), feat_3 0.022 (SD 0.007), feat_4 −0.011 (SD 0.010), feat_5 −0.040 (SD 0.022), group_g2 0.002 (SD 0.007), group_g3 0.005 (SD 0.010), group_g4 −0.094 (SD 0.036).
- Random forest: feat_1 −0.027 (SD 0.029), feat_2 −0.032 (SD 0.020), feat_3 −0.013 (SD 0.028), feat_4 −0.001 (SD 0.022), feat_5 −0.028 (SD 0.020), group_g2 0.004 (SD 0.016), group_g3 −0.008 (SD 0.012), group_g4 −0.036 (SD 0.022).

For logistic regression, feat_3 is the only feature whose mean drop is clearly above zero relative to its SD, in both runs. No random forest feature is clearly important in either run.

![Permutation importance on the 160-row test set, by feature and model, measured as mean drop in ROC AUC](tasks/ml_1/charts/permutation_importance.png)

The EDA signal does not carry over to prediction. feat_5 and feat_3 have the largest class-mean gaps (Welch p = 0.207 and 0.246), and neither is significant.

## Limitations

- **Sample size and power:** The 800-row sample gives wide confidence intervals. Several null results leave moderate effects open.
- **Multiple comparisons:** No unadjusted result survives correction across the five features or the six pairwise group comparisons.
- **Subgroup finding:** The feat_3 result in g2 is post hoc. It was not pre-specified, its Bonferroni check covered only the four groups, and the feat_3 × group interaction (p = 0.029) does not survive correction across five features.
- **Test-set size:** Each model's test metrics come from one 160-row split. The logistic regression test ROC AUC ranges from below 0.5 on seed 42 to near chance across other splits, so single-split estimates are unstable.
- **Interpretation of the AUC below 0.5:** On seed 42, the logistic regression bootstrap CI (0.303 to 0.483) does not include 0.5. This is a single split. Five-fold CV gives 0.533 (SD 0.040), and the 30-split mean is 0.503. The evidence is unstable across splits: below chance on seed 42, around chance on average over 30 splits. It does not establish a reliable inverse relationship.
- **Random forest overfitting:** The random forest memorises the training data (train accuracy 0.908). Its test performance is no better than the baseline.
- **Distance of the seed-42 value from the 30-split mean:** The recorded facts give the seed-42 value, the 30-split mean and SD, but not the distance in SD units, so only the qualitative comparison is reported.
- **Missingness:** No missing values were found, so the missingness check was trivial and no relationship to outcome could be examined.
- **Failed tasks:** None. All tasks completed.

## Open questions

- Does the feat_3 association in g2 (OR 0.67 per unit) replicate in an independent or pre-specified sample? Is the feat_3 × group interaction real?
- Is the feat_2 × group interaction (p = 0.098) real with more data, given that no per-group odds ratio is individually significant?
- Do feat_3 and feat_5 remain associated with outcome after controlling for group, using a likelihood-ratio test in a logistic model? The adjusted per-SD tests are reported above; a likelihood-ratio test was not among the recorded results.
- Is the decline in outcome rate from g1 to g4 real with a larger sample? The unadjusted g1 vs g4 Fisher p is 0.065, and the chi-square test is not significant.
- Would a repeated or nested CV with more folds give a tighter estimate of the true test ROC AUC than 30 single splits?
- Would stronger regularisation or a shallower forest reduce the overfitting and improve test log loss relative to the baseline?
- Do non-linear terms for the features change the adjusted picture?
- Would a larger sample show a feat_5 association (adjusted OR 1.10 per SD), or is the effect too small to matter?