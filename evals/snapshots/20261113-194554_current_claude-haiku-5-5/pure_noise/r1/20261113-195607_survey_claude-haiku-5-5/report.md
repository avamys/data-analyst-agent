# Outcome Analysis of an 800-Row Survey: Binary Outcome, Five Numeric Features and One Group Column

## Summary

- **Group and the numeric features show no significant association with outcome.** Outcome rates fall across group levels from 46.2% (g1) to 36.8% (g4), but the chi-square test gives p = 0.289 and the adjusted joint likelihood-ratio test gives p = 0.280. Every numeric feature has a Holm-adjusted p of 1.0 in the t-tests, and every adjusted odds ratio has a 95% CI spanning 1.
- **The only visible pattern is a low outcome rate in the top feat_3 quartile (34.5% vs 42.5–44.0% in Q1–Q3).** It is nominal (Q4 vs Q1–Q3 p = 0.028, unadjusted) and was selected after viewing the quartile rates. The omnibus test across feat_3 quartiles is not significant (p = 0.177, Holm-adjusted 0.885).
- **No group × feature interaction survives correction.** The strongest is group × feat_3 (p = 0.026 unadjusted, Holm-adjusted 0.132). The joint test of all 15 interaction terms gives p = 0.124.
- **Predictive models do not beat the majority-class baseline (58.9%).** Logistic regression reaches test AUC 0.391 on the seed-42 split. Across 20 splits the mean test AUC is 0.506. Gradient boosting reaches test AUC 0.445 and overfits. The signal in these features is weak.

## Data

- The dataset has 800 rows and 7 columns.
- The target is `outcome`, a binary variable: 58.9% zeros and 41.1% ones, so the classes are moderately imbalanced.
- Numeric features are feat_1 to feat_5. The categorical feature is `group`, with levels g1 (n=182), g2 (n=206), g3 (n=200) and g4 (n=212).
- There are no missing values, no date or time features, and no id or free-text columns.
- The numeric features are standardised-looking: means near 0, standard deviations between 0.985 and 1.021.

## Findings

### Overall outcome and group

Outcome rates by group level were g1 46.2%, g2 42.2%, g3 40.0% and g4 36.8%.

![Outcome rate (share of outcome=1) per group level](tasks/eda_1/charts/group_outcome_rates.png)

- The chi-square test of group × outcome gives χ²(3) = 3.75, p = 0.289, Cramér's V = 0.068, a negligible association.
- Adjusted for feat_1 to feat_5, the joint likelihood-ratio test of the group dummies gives LR = 3.83 on 3 df, p = 0.280.
- Adjusted odds ratios against g1 are g2 0.849 (95% CI 0.567 to 1.270, p = 0.425), g3 0.760 (0.505 to 1.145, p = 0.189) and g4 0.678 (0.452 to 1.018, p = 0.061). No level's CI excludes 1.
- The direction of the group differences is consistent across the EDA rates, the standardised drop-first logistic coefficients and the adjusted odds ratios. Because the association is not significant, the g4 difference should be treated as unresolved.

### Numeric features: quartile rates and tests

Quartile outcome rates for each numeric feature (n=200 per bin unless noted):

![Outcome rate (share of outcome=1) per feature quartile bin, feat_1 to feat_5](tasks/eda_1/charts/quartile_outcome_rates.png)

- feat_1: 44.0%, 39.5%, 38.5%, 42.5%. No monotonic trend.
- feat_2: 39.5%, 43.5%, 41.5%, 40.0%. No clear trend.
- feat_3: 42.5%, 43.5%, 44.0%, 34.5%. Q4 is the only clear departure.
- feat_4 (n=201, 199, 200, 200): 39.8%, 42.2%, 44.0%, 38.5%. No clear trend.
- feat_5: 38.5%, 40.0%, 43.5%, 42.5%. A mild rise that is not strictly monotone.

Welch t-tests of outcome=1 against outcome=0 found no significant mean difference. Raw p-values range from 0.207 (feat_5) to 0.944 (feat_4), and all Holm-adjusted p-values are 1.0. Cohen's d is at most 0.09 in absolute value. The 95% CIs for the mean differences (outcome=1 minus outcome=0) all include zero: feat_1 −0.014 (−0.160 to 0.133), feat_2 0.017 (−0.124 to 0.158), feat_3 −0.082 (−0.222 to 0.057), feat_4 −0.005 (−0.143 to 0.133), feat_5 0.091 (−0.051 to 0.233).

Quartile chi-square tests, Holm-adjusted across the five features, were all non-significant: feat_1 p = 0.653 (Holm 1.0), feat_2 p = 0.849 (Holm 1.0), feat_3 p = 0.177 (Holm 0.885), feat_4 p = 0.684 (Holm 1.0), feat_5 p = 0.730 (Holm 1.0). Cramér's V ranges from 0.032 to 0.079.

### The feat_3 top quartile

![Outcome rate by feat_3 quartile](tasks/stat_4/charts/feat_3_quartile_rate.png)

- The omnibus chi-square across feat_3 quartiles gives χ²(3) = 4.93, p = 0.177, Cramér's V = 0.079, Holm-adjusted p = 0.885.
- The Q4 versus Q1–Q3 contrast gives χ²(1) = 4.83, p = 0.028, φ = 0.078, unadjusted. The Q4 rate is 34.5% (n=200) against 43.3% (n=600) for Q1–Q3, a difference of −0.088 with a 95% Wald CI of −0.165 to −0.011.
- This contrast was chosen after the quartile rates were examined. It was not adjusted for the selection among quartiles and features, and no adjusted p-value is reported for it.
- In the multivariable logistic model, feat_3 as a linear term has OR 0.918 (95% CI 0.796 to 1.060, p = 0.244). The quartile-specific effect was not tested in that model.

### Interactions

Likelihood-ratio tests of group × numeric feature interactions, each with 3 df against the main-effects model:

- feat_3: LR = 9.22, p = 0.026 unadjusted, Holm-adjusted 0.132.
- feat_2: LR = 6.71, p = 0.082.
- feat_5: LR = 3.43, p = 0.330.
- feat_1: LR = 1.12, p = 0.772.
- feat_4: LR = 1.42, p = 0.701.
- Joint test of all 15 interaction terms: LR = 21.41, 15 df, p = 0.124.

No interaction is significant after correction. Per-group odds ratios were not reported because no interaction was significant. The feat_3 result is exploratory.

### Multivariable model

- Adjusted odds ratios for the numeric features, all with CIs spanning 1: feat_1 0.998 (p = 0.978), feat_2 1.017 (p = 0.817), feat_3 0.918 (p = 0.244), feat_4 1.003 (p = 0.965), feat_5 1.107 (95% CI 0.961 to 1.274, p = 0.158).
- The overall likelihood-ratio test of the multivariable model gives p = 0.537.
- Variance inflation factors for feat_1 to feat_5 lie between 1.0 and 1.01, so the features are not collinear.

### Predictive models

**Logistic regression (seed-42 stratified 80/20 split, 160 test rows).** Test accuracy is 0.550 against 0.5875 for the majority baseline. Test ROC AUC is 0.391 against 0.500. Test log loss is 0.708 against 0.678 for the class-prior baseline. Test precision is 0.313, recall 0.076 and F1 0.122.

- The AUC of 0.39 is a single-split result. Across 20 stratified splits (seeds 0–19), test AUC has mean 0.506, sd 0.025, range 0.467 to 0.551. Seed 42 sits at the low tail.
- Training AUC is 0.586. Five-fold CV AUC within the training split is 0.547 (sd 0.050).
- Standardised coefficients from the full-dummy fit are largest for feat_5 (+0.139) and g4 (−0.356). None has been tested for significance, and they are not evidence of a real effect.
- Under the g1-reference fit, the group contrasts are g2 −0.048, g3 −0.157 and g4 −0.538. These point the same way as the EDA rates, but the group association is not significant (p = 0.289).

**Gradient boosting (200 trees, depth 2, same split).** Test ROC AUC is 0.445 against 0.391 for logistic regression and 0.500 for the baseline. Test accuracy is 0.519 and test log loss 0.744. Training AUC is 0.862, so the model overfits. The gain over logistic regression is not meaningful, given the spread across splits.

![Test ROC AUC of gradient boosting, logistic regression and the majority-class baseline on the seed-42 test set](tasks/ml_2/charts/ml_2_auc_compare.png)

**Permutation importance (gradient boosting, test ROC AUC drop, 30 repeats).** Mean importance is feat_1 0.001 (sd 0.025), feat_2 −0.022 (sd 0.020), feat_3 0.030 (sd 0.027), feat_4 0.002 (sd 0.016) and feat_5 −0.018 (sd 0.018). Each is within about one sd of zero. Shuffling the group block gives −0.021 (sd 0.017). No feature is reliably important, and no significance test was run.

## Limitations

- **Weak signal throughout.** No numeric feature, group level or interaction is significant after correction. The predictive models do not beat the majority-class baseline in accuracy or AUC. Several tests are unadjusted for multiple comparisons, and effect sizes are small.
- **Sample size.** Each quartile bin has about 200 rows and each group level has 182 to 212, so the study has limited power to detect small effects.
- **Post hoc feat_3 contrast.** The Q4 contrast (p = 0.028) was chosen after viewing the quartile rates and is not adjusted for that selection. The omnibus feat_3 test is non-significant before and after Holm adjustment (p = 0.177, Holm 0.885). The Q4 finding is a hypothesis to check, not an established effect.
- **Unresolved review issue: signed coefficients and group findings (ml_1, carried into ml_2).** No coefficient has been tested for significance. The model has little predictive signal (test AUC 0.39, seed-spread mean 0.506, CV AUC 0.547). The largest numeric coefficient, feat_5, is not a real effect in this model. The statement that g4 has the lowest predicted outcome must be read with the non-significant group association (p = 0.289) in mind.
- **Unresolved review issue: the Q4 contrast (stat_4).** The Q4 contrast is nominal (p = 0.028, unadjusted). It was selected after viewing the quartile rates and was not adjusted for the selection among quartiles and features. No adjusted p-value is reported for it. Holm values (0.885 for feat_3) apply only to the omnibus quartile tests.
- **Single split for the models.** Model scores on the seed-42 split vary widely across seeds. The 20-seed spread is reported alongside the seed-42 scores.
- **Failed tasks.** None. All eight tasks completed.

## Open questions

- Does the feat_3 top-quartile effect hold in a logistic regression that adjusts for group and the other features? The multivariable model used feat_3 as a linear term only.
- Does the feat_3 Q4 drop differ across group levels? The interaction tests used the linear feat_3 term, not the quartile.
- Is the Q4 drop stable in a pre-specified threshold or a held-out sample?
- Does the lower outcome rate in g4 relative to g1 hold with a larger sample or a pre-specified contrast?
- Does a tuned random forest with proper cross-validation confirm the absence of a gain over logistic regression?