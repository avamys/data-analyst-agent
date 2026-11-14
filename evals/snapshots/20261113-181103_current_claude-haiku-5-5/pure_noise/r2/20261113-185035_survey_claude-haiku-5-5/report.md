# Survey Outcome Analysis: Binary Outcome in an 800-Row Survey

## Summary

- **The features show no reliable predictive signal for the outcome on this sample.** Neither model beats the majority-class baseline of 58.8% on the 160-row test split (logistic regression 55.0%, gradient boosting 53.1%). Repeated cross-validation gives mean ROC AUCs between 0.536 and 0.544 for the group-only, feat_5-only and full logistic models, which are not distinguishable from chance.
- **No numeric feature differs significantly between outcome classes.** Every Cohen's d is below 0.1 in absolute value, and the smallest Welch p-value is 0.207 (feat_5).
- **Group is not significantly associated with outcome.** The outcome rate runs from 36.8% (g4) to 46.2% (g1), with chi-square p = 0.289. The g1 vs g4 contrast is the closest to significance (raw p = 0.060) but does not survive multiplicity adjustment.
- **Feature-by-group interactions are not significant.** The likelihood-ratio test gives p = 0.124, and the test has limited power at this sample size.
- **There is no missing data.** The dataset has 0 missing cells across all 7 columns and 800 rows, so no missingness analysis was needed.

## Data

- **Size:** 800 rows, 7 columns: five numeric features (feat_1 to feat_5), one categorical column (group, levels g1 to g4), and the binary target (outcome).
- **Target:** outcome = 1 for 329 rows (41.1%) and outcome = 0 for 471 rows (58.9%).
- **Missing values:** none. Zero missing cells in all 7 columns, and zero rows with any missing value.
- **Date, time, id and text columns:** none.

## Findings

### Outcome rate by group

The positive rate falls across group levels, but these differences are descriptive. No test was run at this stage; the formal tests are in the next sections.

| Group | n | Outcome = 1 | Rate |
|---|---|---|---|
| g1 | 182 | 84 | 46.2% |
| g2 | 206 | 87 | 42.2% |
| g3 | 200 | 80 | 40.0% |
| g4 | 212 | 78 | 36.8% |

![Share of rows with outcome=1 within each group level, with overall rate as dashed line](tasks/eda_1/charts/outcome_rate_by_group.png)

### Numeric features by outcome class

Descriptive means and medians (outcome 0 vs outcome 1):

- **feat_5:** mean 0.0007 vs 0.0920; median 0.036 vs 0.083.
- **feat_3:** mean 0.0552 vs -0.0272; median 0.086 vs 0.002. The median gap is the largest of any feature.
- **feat_2:** mean -0.0063 vs 0.0107; median 0.029 vs -0.021. The mean and median point in opposite directions, so the apparent direction depends on the summary used.
- **feat_1:** mean 0.0114 vs -0.0022; median 0.011 vs -0.013. Differences are small.
- **feat_4:** mean 0.0618 vs 0.0569; median 0.035 vs 0.038. Nearly the same across classes.

Inferential tests (outcome 1 minus outcome 0):

| Feature | Mean diff | 95% CI | Welch p | Cohen's d | Mann-Whitney p |
|---|---|---|---|---|---|
| feat_1 | -0.0136 | -0.1597 to 0.1325 | 0.855 | -0.013 | 0.740 |
| feat_2 | 0.0170 | -0.1238 to 0.1577 | 0.813 | 0.017 | 0.978 |
| feat_3 | -0.0824 | -0.2216 to 0.0568 | 0.246 | -0.083 | 0.179 |
| feat_4 | -0.0049 | -0.1428 to 0.1330 | 0.944 | -0.005 | 0.864 |
| feat_5 | 0.0913 | -0.0506 to 0.2332 | 0.207 | 0.090 | 0.210 |

No feature differs significantly between outcome classes, and all effects are negligible by Cohen's d. The rank-biserial correlations run from -0.056 (feat_3) to 0.052 (feat_5).

![Cohen d with 95% CI for each numeric feature, outcome 1 minus outcome 0](tasks/stat_1/charts/stat1_effect_sizes.png)

### Feature distributions

All five features have means near zero and SDs between 0.985 (feat_4) and 1.021 (feat_1). Skew is negligible, between -0.06 (feat_3) and 0.14 (feat_1). Ten values across feat_1 to feat_5 (0.25% of values) lie beyond 3 SD, with a range of -3.37 (feat_3 minimum) to 3.67 (feat_3 maximum). These values were judged consistent with normal tails rather than data errors.

![Histograms of feat_1 to feat_5 (row counts) and box plot of their values](tasks/eda_2/charts/eda2_distributions.png)

### Group and outcome association

- **Overall test:** chi-square = 3.754, 3 df, p = 0.289, Cramér's V = 0.068 (n = 800). The spread in group rates is consistent with chance.
- **Pairwise tests (chi-square on outcome, six pairs, Holm-adjusted):** none is significant after adjustment. g1 vs g4 has raw p = 0.060 and Holm p = 0.358. The other raw p-values run from 0.225 to 0.648.

### Feature-by-group interactions

- **Main-effects model:** no group contrast is significant at 0.05. g4 vs g1 has coefficient -0.388 (95% CI -0.794 to 0.017, p = 0.061). No numeric feature is significant in this model.
- **Interaction terms:** the likelihood-ratio test of the 15 feature-by-group terms against main effects gives chi-square = 21.41 on 15 df, p = 0.124. The smallest individual interaction p-values are feat_3:g2 (p = 0.054), feat_2:g2 (p = 0.067) and feat_5:g4 (p = 0.098). None is significant at 0.05.
- **Split at the median of feat_5 (0.0515):** within each half, group rates were compared with a chi-square test.

| Group | High half rate (n) | Low half rate (n) |
|---|---|---|
| g1 | 46.5% (86) | 45.8% (96) |
| g2 | 41.6% (101) | 42.9% (105) |
| g3 | 43.8% (105) | 35.8% (95) |
| g4 | 40.7% (108) | 32.7% (104) |

The four-group test is not significant in either half (high half p = 0.857; low half p = 0.198). The low-half g1 vs g4 gap was not tested pairwise.

![Outcome rate by group, split at median of feat_5 (low = at or below median)](tasks/stat_2/charts/stat2_rate_by_group_half.png)

### Adjusted associations

A logistic model with all five features and group was fitted. Holm adjustment was applied across the eight terms: three group contrasts against g1 and the five numeric features.

| Term | Adjusted OR | 95% CI | Raw p | Holm p |
|---|---|---|---|---|
| feat_1 (per unit) | 0.998 | 0.868 to 1.147 | 0.978 | 1.0 |
| feat_2 (per unit) | 1.017 | 0.883 to 1.170 | 0.817 | 1.0 |
| feat_3 (per unit) | 0.918 | 0.796 to 1.060 | 0.244 | 1.0 |
| feat_4 (per unit) | 1.003 | 0.868 to 1.159 | 0.965 | 1.0 |
| feat_5 (per unit) | 1.107 | 0.961 to 1.274 | 0.158 | 1.0 |
| g2 vs g1 | 0.849 | 0.567 to 1.270 | 0.425 | 1.0 |
| g3 vs g1 | 0.760 | 0.505 to 1.145 | 0.189 | 1.0 |
| g4 vs g1 | 0.678 | 0.452 to 1.018 | 0.061 | 0.485 |

No term is significant after adjustment. The group term as a whole gives a likelihood-ratio chi-square of 3.832 on 3 df (p = 0.280).

### Predictive models against the majority baseline

**Single 160-row test split:**

| Model | Test accuracy | ROC AUC | Log loss | Train accuracy |
|---|---|---|---|---|
| Majority-class baseline | 58.8% | n/a | 0.678 (constant at 41.1%) | n/a |
| Logistic regression | 55.0% | 0.391 | 0.708 | 58.4% |
| Gradient boosting | 53.1% | 0.466 | 0.754 | 83.6% |

- Both models score below the baseline accuracy. Logistic regression has test precision 31.3% and recall 7.6%. Gradient boosting has precision 40.0% and recall 27.3%.
- Both test ROC AUCs are below 0.5. On a single 160-row split this is not reliably below chance and may reflect noise, so it is read as no detectable signal rather than systematically inverted ranking.
- Gradient boosting overfits: 83.6% train accuracy against 53.1% on test.
- On the 80% training split, 5-fold cross-validated ROC AUC is 0.546 ± 0.050 for logistic regression and 0.472 ± 0.040 for gradient boosting. The logistic regression value is within one SD of 0.5 and is not distinguishable from chance. The gradient boosting value is also within one SD of 0.5.

**Repeated stratified CV on the 80% training split (5 × 5 folds, seed 0):**

| Model | ROC AUC (mean ± SD) | Log loss (mean ± SD) | Folds with AUC > 0.5 |
|---|---|---|---|
| Majority class | 0.500 | 0.677 ± 0.001 | 0 of 25 |
| Group only | 0.544 ± 0.037 | 0.675 ± 0.008 | 22 of 25 |
| feat_5 only | 0.536 ± 0.053 | 0.677 ± 0.006 | 18 of 25 |
| Full logistic | 0.536 ± 0.039 | 0.682 ± 0.012 | 21 of 25 |

- Group only has the highest mean ROC AUC. Its mean is about 1.2 SD above chance, and its log loss is not clearly below the majority reference.
- feat_5 only and the full logistic model have ROC AUCs not distinguishable from chance. The full logistic model has the worst log loss of the four, above the majority reference.
- No model improves log loss beyond the majority reference by more than its SD.

![Mean ROC AUC over 25 CV folds (5x5 repeated stratified, seed 0) per model on the 80% training split, error bar = SD; dashed line = chance](tasks/ml_2/charts/ml2_cv_roc_auc.png)

**Permutation importance (single test split, ROC AUC drop; SD in brackets; negative values mean AUC rose when the feature was shuffled):**

Logistic regression:

- feat_1: -0.018 (0.010)
- feat_2: 0.004 (0.006)
- feat_3: 0.023 (0.007)
- feat_4: -0.011 (0.010)
- feat_5: -0.039 (0.022)
- group: -0.069 (0.041)

Among the numeric features, feat_3 shows the largest mean drop. The drop is small.

Gradient boosting:

- feat_1: -0.008 (0.026)
- feat_2: 0.007 (0.020)
- feat_3: 0.016 (0.034)
- feat_4: 0.011 (0.019)
- feat_5: -0.009 (0.016)
- group: -0.009 (0.022)

Gradient boosting also places feat_3 highest among the numeric features. Its SDs are similar to or larger than the means for every feature, so the gradient boosting ranking is unstable.

The logistic regression coefficient ranking (by absolute coefficient) placed group_g4 (0.356), group_g1 (0.203) and feat_5 (0.139) highest. These are absolute values, not signed effects, and the group dummies do not indicate a group effect given the chi-square result above.

![Mean drop in test ROC AUC (30 shuffles, error bar = SD) when each feature is permuted, for logistic regression and gradient boosting](tasks/ml_1/charts/ml1_permutation_importance.png)

### Missing values

Confirmed: no missing values in any column (0 missing cells across all 7 columns and 800 rows; 0 rows with any missing value). No missingness pattern analysis was performed or needed.

## Limitations

- **Small effects and wide intervals.** All feature effects are negligible. The adjusted odds-ratio intervals are wide, and the analysis is underpowered for effects of the size suggested by the g1 vs g4 contrast (adjusted OR 0.678, 95% CI 0.452 to 1.018).
- **Different multiplicity adjustments for g1 vs g4.** In the pairwise chi-square comparisons (six pairs), the Holm-adjusted p is 0.358. In the adjusted logistic model (eight terms), the Holm-adjusted p is 0.485. These are different analyses with different adjustment families. Both are reported, and they are not reconciled.
- **Conflicting model results.** The ml_1 test-split ROC AUC for logistic regression is 0.391, while the ml_1 cross-validated AUC for the same model is 0.546 and the ml_2 repeated-CV AUC for the full logistic model is 0.536. These come from different designs (a single 160-row split against CV on the training split), and they are reported side by side without reconciling them.
- **Permutation importance is unstable.** The logistic regression ranking rests on one model with small effects. Gradient boosting SDs are similar to or larger than their means for every feature, so neither ranking is robust. The logistic regression values for feat_4 and feat_5 are from the recomputed record, and gradient boosting means and SDs are reported for each feature.
- **Interaction test power.** The interaction likelihood-ratio test (p = 0.124) has limited power with 15 extra terms on 800 rows. A non-significant result does not show that group has no effect on feature slopes.
- **Post hoc split.** The feat_5 median split in the interaction analysis was selected as the "strongest" feature by Cohen's d, although that effect was negligible. The per-half group tests are exploratory.
- **Mean and median disagree for feat_2.** The feat_2 mean and median point in opposite directions. For feat_3, the mean and median differences point the same way, but the feat_3 median gap is the largest of any feature. The robustness of the feat_3 difference was not tested with a robust test.
- **Single survey sample.** All results apply to these 800 rows. The analysis cannot assess generalisation beyond them, and no external validation was performed.
- **Failed tasks:** none. All analysis tasks are reported complete.

## Open questions

- Does the outcome rate differ across the tails of each numeric feature (for example the top and bottom 5%)? This was raised but not tested.
- Do the 10 values beyond 3 SD belong to rows that are unusual on other features or on group, and do they change model coefficients when removed?
- Are feature distributions different across the levels of group?
- Is the g1 vs g4 outcome-rate difference (raw p = 0.060) real in a larger sample or after adjusting for all numeric features? The adjusted model gives Holm p = 0.485.
- Is the group-only CV AUC of 0.544 (22 of 25 folds above 0.5) a real group effect? A permutation test of the CV AUC against shuffled labels, or more repeats, was proposed but not run.
- Would a simpler model (group only, or the strongest single feature) do better on repeated cross-validation than the full models?
- Do repeated stratified splits give a more stable ROC AUC estimate than the single 160-row test split?
- Does feat_5 have a non-linear or interaction effect, and does a transformed term improve fit?
- Would a calibrated or regularised model reduce the log-loss penalty seen in the full logistic model relative to the majority-class reference?
- Is the feat_5 low-high difference in outcome rates real, given that its stat_1 effect was negligible?