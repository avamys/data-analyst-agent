# Outcome Analysis of an 800-Row Binary Dataset: Group, Five Numeric Features and Predictive Models

## Summary

- **No group or numeric feature is significantly associated with outcome.** The group chi-square gives p = 0.289, and no feature survives Holm correction. The largest effect size is feat_5 (Cohen's d 0.090, Mann-Whitney p = 0.210). Group is still not significant after adjusting for feat_1 to feat_5 (joint LR p = 0.280), and no feature is significant in that adjusted model (lowest raw p is feat_5 at 0.158).
- **Neither predictive model beats the majority-class baseline.** On the 200-row test split, the baseline scores 0.59, logistic regression 0.56 and gradient boosting 0.49. Repeated 5-fold cross-validation on all 800 rows gives the same picture: logistic regression averages 0.572 and gradient boosting 0.550, against a baseline of 0.589.
- **Discrimination is at or near chance.** Test ROC AUC is 0.411 for logistic regression and 0.462 for gradient boosting. The logistic regression test AUC is borderline below chance (permutation one-sided p = 0.055) and is not significant at 0.05. Repeated-CV AUC is 0.504 for logistic regression and 0.478 for gradient boosting.
- **Interactions are not significant after correction.** No feat_k × group interaction survives Holm correction. The smallest raw interaction (feat_3, p = 0.030) becomes p = 0.147 after correction.
- **Two results are unresolved.** The lower logistic regression test AUC conflicts with its higher repeated-CV mean, and the cause is not established. The data contain no missing values and the feature distributions in the test split are close to those in the training split, but a joint multivariate shift was not tested.

## Data

- 800 rows and 7 columns.
- Target: `outcome`, binary. 41.1% of rows are positive (outcome = 1) and 58.9% are negative (outcome = 0).
- Numeric features: feat_1, feat_2, feat_3, feat_4, feat_5.
- Categorical feature: `group`, with levels g1, g2, g3 and g4.
- No date/time features and no id or free-text columns.
- Missing values: none in any column.

## Findings

### Outcome distribution and group

The overall outcome rate is 41.1% (0.41125 across 800 rows). Outcome rates by group are shown below.

| Group | Outcome rate | n |
|---|---|---|
| g1 | 46.2% | 182 |
| g2 | 42.2% | 206 |
| g3 | 40.0% | 200 |
| g4 | 36.8% | 212 |

![Outcome rate by group level (last panel) and by quintile of each numeric feature feat_1 to feat_5](tasks/eda_1/charts/eda1_outcome_rate_by_group_and_quintile.png)

The chi-square test of group against outcome gives χ² = 3.754 on 3 df, p = 0.289, Holm-adjusted p = 1.0 (across six tests), Cramér's V = 0.068 (negligible). The rates fall from g1 to g4, but the difference is not statistically significant.

![Outcome rate by group level](tasks/stat_1/charts/stat1_group_rate.png)

### Numeric features: marginal associations

Each feature was compared between outcome = 1 and outcome = 0 (difference in means, 95% CI, Cohen's d, Mann-Whitney p; Holm-adjusted p = 1.0 for all, across six tests):

| Feature | Mean diff (1 − 0) | 95% CI | Cohen's d | MW p |
|---|---|---|---|---|
| feat_1 | −0.014 | −0.160 to 0.132 | −0.013 | 0.740 |
| feat_2 | 0.017 | −0.124 to 0.158 | 0.017 | 0.978 |
| feat_3 | −0.082 | −0.222 to 0.057 | −0.083 | 0.179 |
| feat_4 | −0.005 | −0.143 to 0.133 | −0.005 | 0.864 |
| feat_5 | 0.091 | −0.051 to 0.233 | 0.090 | 0.210 |

None of these is significant. feat_3 has the smallest raw p-value of the five but a smaller effect size than feat_5; its sign is negative and feat_5's is positive.

Outcome rates by quintile of each feature are not monotonic for any feature:

- **feat_1:** 45.6% (Q1) to 37.1% (Q4) to 44.4% (Q5).
- **feat_2:** 38.1% (Q1) to 44.4% (Q2); 40.9% in Q5.
- **feat_3:** 42.5%, 42.2%, 45.3%, 42.5%, then 33.1% in Q5 (n = 160).
- **feat_4:** 40.0% (Q1) to 45.6% (Q4); 38.1% in Q5.
- **feat_5:** 38.8%, 39.4%, 39.4%, 45.6% (Q4), then 42.5% (Q5).

Each quintile has about 160 rows.

![Outcome rate by group level (last panel) and by quintile of each numeric feature feat_1 to feat_5](tasks/eda_1/charts/eda1_outcome_rate_by_group_and_quintile.png)

### Adjusted association (logistic regression)

After adjusting for feat_1 to feat_5, the joint likelihood-ratio test for group gives χ² = 3.832 on 3 df, p = 0.280. Adjusted odds ratios versus g1 are:

- g2: 0.849 (95% CI 0.567 to 1.270), p = 0.426
- g3: 0.760 (0.505 to 1.145), p = 0.189
- g4: 0.678 (0.452 to 1.018), p = 0.061

Odds ratios per unit for the numeric features are:

- feat_1: 0.998 (0.868 to 1.147), p = 0.978
- feat_2: 1.017 (0.883 to 1.170), p = 0.817
- feat_3: 0.918 (0.796 to 1.060), p = 0.244
- feat_4: 1.003 (0.868 to 1.159), p = 0.965
- feat_5: 1.107 (0.961 to 1.274), p = 0.158

Holm-adjusted across the five feature p-values, feat_3 is 0.975 and feat_5 is 0.791; the others are 1.0. Across all six tests (group plus five features), no result is significant. The model has a McFadden pseudo R² of 0.006 (n = 800). Adjustment changes little from the marginal results.

### Feature × group interactions

For each feat_k × group interaction (logistic model, 3 df), the raw and Holm-adjusted p-values are:

| Feature | LR | Raw p | Holm p |
|---|---|---|---|
| feat_1 | 0.951 | 0.813 | 1.0 |
| feat_2 | 6.287 | 0.098 | 0.394 |
| feat_3 | 8.985 | 0.029 | 0.147 |
| feat_4 | 1.301 | 0.729 | 1.0 |
| feat_5 | 3.485 | 0.323 | 0.968 |

No interaction is significant after correction. feat_3 has the smallest raw p, and its per-group odds ratios per raw unit are g1 1.020 (95% CI 0.754 to 1.380), g2 0.672 (0.504 to 0.896), g3 0.899 (0.679 to 1.190) and g4 1.219 (0.914 to 1.628). The direction varies by group, but the differences do not survive correction. The per-group odds ratios are per raw (unstandardized) unit; an earlier version of the labelling incorrectly said per 1 SD.

### Predictive models: test split

The data were split 75/25 with stratification into 600 training and 200 test rows, using nine features (feat_1 to feat_5 and one-hot group_g1 to group_g4). The outcome rate is 41.2% in train (247 of 600) and 41.0% in test (82 of 200). The majority-class baseline reaches 0.59 test accuracy.

| Model | Train acc. | Test acc. | Test precision | Test recall | Test F1 | Test ROC AUC |
|---|---|---|---|---|---|---|
| Majority baseline | — | 0.59 | — | — | — | — |
| Logistic regression | 0.583 | 0.56 | 0.333 | 0.073 | 0.12 | 0.411 |
| Gradient boosting | 0.85 | 0.49 | 0.333 | 0.244 | 0.282 | 0.462 |

![Test accuracy of the majority-class baseline (always predict 0) and the two classifiers on the 200-row test split](tasks/ml_2/charts/ml2_accuracy_vs_baseline.png)

Both models have worse test log loss than a constant prediction at the training prevalence: 0.702 (logistic regression) and 0.765 (gradient boosting), against 0.677. Gradient boosting overfits, with train accuracy 0.85 against test accuracy 0.49.

**Feature importance is weak and inconsistent across methods.**

- Gradient boosting permutation importance (drop in test ROC AUC) ranks feat_3 first at 0.031 (sd 0.019). It is the only feature whose drop is clearly larger than its sd. All other features are near zero or negative.
- Gradient boosting built-in importance ranks feat_4 (0.226) and feat_3 (0.225) highest, so the feat_3 first place is specific to permutation importance.
- Logistic regression permutation importance ranks group_g1 first (0.014, sd 0.012), then feat_3 (0.009, sd 0.008). Each positive drop is small relative to its sd, so this ranking is not reliable.
- Logistic regression standardized absolute coefficients rank group_g4 (0.148) and feat_5 (0.122) highest. This disagrees with its own permutation ranking, where feat_1 and group_g4 are the most negative.

### Model performance: repeated cross-validation on all 800 rows

Repeated stratified 5-fold CV (10 repeats, 50 folds):

| Model | Accuracy (sd) | ROC AUC (sd) | Log loss (sd) |
|---|---|---|---|
| Majority baseline | 0.589 (0.002) | 0.500 | 0.677 (0.001) |
| Logistic regression | 0.572 (0.022) | 0.504 (0.038) | 0.684 (0.008) |
| Gradient boosting | 0.550 (0.025) | 0.478 (0.038) | 0.714 (0.017) |

Paired against the baseline over the 50 splits:

- **Logistic regression:** accuracy gap −0.017 (paired t = −5.35, p = 2.3e-6); log loss worse by 0.007 (t = 5.56). AUC is 0.004 above 0.5 (t = 0.74, p = 0.46).
- **Gradient boosting:** accuracy gap −0.039 (paired t = −10.99, p = 8e-15); log loss worse by 0.036 (t = 15.05). AUC is 0.022 below 0.5 (t = −4.01, p = 0.0002).

The authors' own reading: the gradient boosting gaps are larger than their paired fold-to-fold sd. For logistic regression, the accuracy and log-loss gaps are smaller than their paired sds. The p-values rest on overlapping folds and are optimistic, so the reliability of these conclusions is not established.

![Fold-to-fold test accuracy of the majority-class baseline, logistic regression and gradient boosting over 50 repeated stratified CV folds](tasks/ml_4/charts/ml4_cv_accuracy_by_model.png)

### Are the test AUCs distinguishable from chance?

A label-permutation null was used (training labels shuffled and models refit, scored on the fixed test split):

- **Logistic regression:** observed test AUC 0.411 (unscaled refit 0.412). Null mean 0.499, sd 0.049, from 200 permutations. One-sided p for below chance = 0.055; two-sided p = 0.080. Not significant at 0.05.
- **Gradient boosting:** observed test AUC 0.462. Null mean 0.503, sd 0.046, from 100 permutations. One-sided p = 0.208; two-sided p = 0.426. Consistent with chance.

Repeated 5-fold CV on the training set (25 scores, 5 repeats):

- **Logistic regression:** mean 0.536 (sd 0.045, range 0.473 to 0.640). The test AUC of 0.411 lies below the minimum repeated-CV score.
- **Gradient boosting:** mean 0.460 (sd 0.035, range 0.404 to 0.517). The test AUC of 0.462 lies inside this range.

The sd values describe the spread of scores from overlapping folds; they are not standard errors.

![Test ROC AUC under label-permutation null (counts of shuffled refits) with observed test AUC in red, for logistic regression and gradient boosting](tasks/ml_5/charts/ml5_perm_null.png)

**Superseded earlier claims.** An earlier task (ml_3) stated that the logistic regression test AUC was reliably below chance (bootstrap interval 0.331 to 0.492, which excludes 0.5) and outside the CV range. That task also gave single-run CV means of 0.547 for logistic regression and 0.474 for gradient boosting. The permutation analysis (ml_5) supersedes the "reliably below chance" claim, and the repeated-CV figures (0.536 and 0.460) supersede the single-run figures for this comparison. The cause of the difference between the single-run and repeated-CV means is not recorded and is not explained here. The chart below is from the earlier task and shows its superseded single-run figures.

![Cross-validated and test ROC AUC for logreg and gboost, with bootstrap 95% interval on test; dashed line is chance 0.5](tasks/ml_3/charts/ml3_auc_vs_chance.png)

### Test split versus training split

Standardized mean differences (test minus train, pooled sd) are: feat_1 −0.091, feat_2 −0.160, feat_3 0.076, feat_4 −0.059, feat_5 0.038. feat_2 is the largest. Group proportions differ most for g3 (23.8% train, 28.5% test; SMD 0.106) and g4 (27.7% train, 23.0% test; SMD −0.108).

![SMD of feat_1 to feat_5 between test (200 rows) and train (600 rows); dashed lines at +/-0.1](tasks/eda_2/charts/eda2_feature_smd.png)

The outcome rate is 41.2% in train (0.4117) and 41.0% in test (0.410). Within the training split, the Cohen's d for each feature with outcome is: feat_1 −0.112, feat_2 0.039, feat_3 −0.053, feat_4 −0.071, feat_5 0.118. These differ from the stat_1 values for feat_2 (0.017) and feat_5 (0.090). Both sets are reported here; the source does not resolve the difference.

These univariate checks do not establish that the split caused the logistic regression test AUC to fall below the CV range. The check did not test a joint multivariate shift.

## Limitations

- **Small test split.** All test-set figures (accuracy, precision, recall, AUC) come from 200 rows with 82 positives. The bootstrap intervals resample those rows around one fitted model and ignore training variability.
- **Unresolved test-versus-CV disagreement for logistic regression.** The test AUC (0.411) lies below the repeated-CV minimum (0.473), while the repeated-CV mean is 0.536. The split-artifact hypothesis is open: univariate checks found modest shifts, but a joint multivariate shift was not tested. Under the lead's review, the feature shift is best described as modest, with feat_2 the largest (SMD −0.160, above the 0.1 threshold); the earlier wording "small on each univariate check" is softened accordingly. The group SMDs for g3 (0.106) and g4 (−0.108) are also above 0.1.
- **Outcome-rate wording.** An earlier statement that the train–test outcome-rate difference is about 0.001 conflicts with the recorded rates (0.4117 train, 0.410 test). The lead's review states the difference should be stated as the recorded rates indicate, so this report gives the rates directly.
- **Overlapping CV folds.** The paired tests in repeated CV use 50 overlapping folds. Their p-values are optimistic. No corrected resampled t-test (for example Nadeau-Bengio) was applied, so the reliability of the accuracy and log-loss conclusions is not established.
- **Permutation test size.** The permutation nulls use 200 (logistic regression) and 100 (gradient boosting) shuffles. The logistic regression p-value (0.055) sits close to 0.05, and more permutations would tighten it.
- **Weak power.** Quintile groups have about 160 rows each. The non-monotonic quintile patterns (feat_3 Q5 at 33.1%, feat_5 Q4 at 45.6%) are not tested as thresholds or interactions beyond the findings above, and no finding establishes them as real.
- **Multiple comparisons.** The stat_1 and stat_3 corrections (Holm) cover the tests within each analysis. No result is significant after correction.
- **Interaction test.** The feat_3 group-specific pattern is not significant (Holm p = 0.147), and the interaction tests have modest power at this sample size.
- **Units.** Per-group odds ratios are per raw unit of each feature. Earlier labelling as per 1 SD was incorrect.
- **Failed tasks.** None of the listed tasks failed; all are marked complete.

## Open questions

- Does the group effect (g4 lower odds than g1, adjusted p = 0.061) become significant with more data or a different reference level?
- Does the group difference persist after adjusting for feat_1 to feat_5 in a repeated-split or outer-resampled analysis? (The adjusted analysis was run once on the full data.)
- Is the feat_3 Q5 drop (33.1%) a threshold effect or noise, and does feat_3 interact with group? The interaction is not significant after correction.
- Is the feat_5 Q4 peak (45.6%) followed by a Q5 dip (42.5%) real, or noise at about 160 rows per quintile? Are the non-monotonic patterns for feat_1, feat_2 and feat_4 consistent with noise?
- Do the feat_3 and feat_5 effects change after adding a group-by-feature interaction in the adjusted model?
- Does the test split differ from the training split in a joint multivariate sense? Adversarial validation (train versus test classifier) would test this.
- Does reweighting the training data to match the test group proportions (especially g3 and g4) change the test AUC?
- Why do the single-run 5-fold CV means (0.547 and 0.474) differ from the repeated-CV means (0.536 and 0.460)?
- Would outer repeated resampling of the full dataset show whether logistic regression is below chance?
- Do a more strongly regularized or shallower gradient boosting model, and a larger or more repeated CV scheme, close the accuracy, log-loss and AUC gaps?
- Do the outcome-to-feature associations differ between the stat_1 analysis and the training split (feat_2 d 0.017 versus 0.039; feat_5 d 0.090 versus 0.118)?