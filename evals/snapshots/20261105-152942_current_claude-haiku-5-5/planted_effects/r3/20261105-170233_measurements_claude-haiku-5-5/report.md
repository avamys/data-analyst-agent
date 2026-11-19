# Outcome Drivers and Predictability in a 1,000-Row Binary Dataset (Target: `outcome`)

## Summary

- **feat_a is the dominant association with outcome.** Its odds ratio is 3.30 per SD (95% CI 2.76 to 3.95, Holm p = 6.6e-38). After adjusting jointly for feat_b, feat_c and feat_d, the feat_a effect stays strong and monotone across quartiles, with an adjusted OR of 22.49 for Q4 versus Q1 (complete cases, n=850).
- **feat_b and feat_d have smaller but significant associations; feat_c has none.** feat_b OR is 1.35 per SD (Holm p = 1.4e-5), and feat_d OR is 1.81 per SD on the 850 complete rows (Holm p = 1.2e-13). feat_c OR is 1.00 per SD (Holm p = 0.95).
- **No pairwise interaction among the four features is significant after correction.** Missingness in feat_d shows no marginal or joint association with the outcome or with feat_a, feat_b or feat_c (joint model likelihood-ratio p = 0.696).
- **Logistic regression predicts the outcome better than the baselines.** Across 25 repeated CV folds, its mean log-loss is 0.514 against 0.672 for the class-prior baseline, and its mean ROC AUC is 0.812. Tuned gradient boosting is close behind (mean log-loss 0.538) but loses to logistic regression on 23 of 25 folds.

## Data

- 1,000 rows, 5 columns: outcome (binary target) and four numeric features (feat_a, feat_b, feat_c, feat_d). No categorical, date/time, identifier or free-text columns.
- Outcome: 603 rows with outcome=0 (60.3%) and 397 with outcome=1 (39.7%).
- Missing values: feat_d is missing in 150 rows (15.0%). No other column has missing values.

## Findings

### 1. Outcome rate across quartile bins (eda_1)

The overall outcome rate is 39.7%. Rates by quartile bin of each feature (feat_d missing rows shown as their own group):

- **feat_a** shows the steepest gradient: 11.6% (Q1, n=251), 32.5% (Q2, n=249), 44.0% (Q3, n=250), 70.8% (Q4, n=250).
- **feat_d** rises in its top quartile: 24.9% (Q1, n=213), 35.4% (Q2, n=212), 39.2% (Q3, n=212), 58.2% (Q4, n=213). Rows with feat_d missing (n=150) have a rate of 41.3%, close to the overall rate.
- **feat_b** is weaker and non-monotone: 26.8% (Q1), 44.4% (Q2), 37.6% (Q3), 50.0% (Q4), each n=250. The Q2 rate sits above Q3 and this has not been tested against sampling noise.
- **feat_c** shows little pattern: 38.8%, 42.8%, 35.6%, 41.6% across Q1 to Q4, each n=250.

![Histograms of the four numeric features (count of rows)](tasks/eda_1/charts/feature_histograms.png)

![Proportion of outcome=1 per quartile bin of each feature (dashed line: overall rate)](tasks/eda_1/charts/outcome_rate_by_bin.png)

### 2. Significance and effect sizes (stat_1)

p-values are Holm-adjusted across the four features. Odds ratios are unadjusted and fitted one feature at a time, so they overlap and are not independent effects.

- **feat_a:** OR 3.30 per SD (95% CI 2.76 to 3.95), logistic p = 1.6e-38 (Holm 6.6e-38). Quartile chi-square 191.3 on 3 df, p = 3.1e-41. The outcome rate rises by 0.592 from Q1 to Q4.
- **feat_b:** OR 1.35 per SD (95% CI 1.18 to 1.54), logistic p = 7.0e-6 (Holm 1.4e-5). Quartile chi-square 31.2 on 3 df, p = 7.6e-7. Q4 minus Q1 rate difference is 0.232.
- **feat_c:** OR 1.00 per SD (95% CI 0.88 to 1.14), logistic p = 0.951. Quartile chi-square 3.2 on 3 df, p = 0.359. Q4 minus Q1 rate difference is 0.028.
- **feat_d:** OR 1.81 per SD (95% CI 1.55 to 2.12) on the 850 complete rows, logistic p = 4.0e-14 (Holm 1.2e-13). Quartile chi-square with missing as its own bin is 51.9 on 4 df, p = 1.5e-10. Q4 minus Q1 rate difference is 0.333.

![Odds ratio of outcome per 1 SD of each feature with 95% CI; dashed line at OR=1 (no association)](tasks/stat_1/charts/or_per_sd.png)

### 3. Interactions (stat_2)

On the 850 rows with feat_d present, no pairwise interaction among the four numeric features is significant after Holm correction; all six adjusted p-values are 1.0.

- feat_a × feat_b: OR 1.06 (95% CI 0.86 to 1.30), p = 0.60
- feat_a × feat_c: OR 0.99 (0.80 to 1.22), p = 0.92
- feat_a × feat_d: OR 0.90 (0.73 to 1.11), p = 0.33
- feat_b × feat_c: OR 0.94 (0.79 to 1.12), p = 0.47
- feat_b × feat_d: OR 1.03 (0.86 to 1.24), p = 0.72
- feat_c × feat_d (smallest p): OR 1.12 (0.94 to 1.33), p = 0.21

The intervals are wide. Moderate interactions (roughly ORs of 0.73 to 1.33 per SD-product) cannot be excluded.

In a 2×2 median split of feat_c and feat_d, the outcome rate rises with feat_d in both feat_c halves: from 33.3% to 47.6% when feat_c is below its median (n=216 and 210), and from 26.8% to 49.8% when feat_c is above its median (n=209 and 215). The interaction test does not establish that these two gains differ.

### 4. feat_a adjusted and monotone across quartiles (stat_3)

On the 850 complete cases, feat_a stays strongly associated with outcome after adjusting for feat_b, feat_c and feat_d:

- Per raw unit of feat_a: OR 3.61 (coefficient 1.283 log-odds; 95% CI 2.92 to 4.45; p = 8.4e-33). This is **not** the per-SD OR of 3.30 reported in stat_1.
- Other adjusted complete-case log-odds: feat_b 0.339 (95% CI 0.172 to 0.506, p = 7e-5); feat_c −0.014 (−0.177 to 0.149, p = 0.87); feat_d 0.727 (0.548 to 0.905, p = 1.7e-15).

Quartile cut-points were computed on the complete cases (−3.331, −0.699, 0.053, 0.706, 2.470), so they differ from the full-sample cut-points in eda_1. Unadjusted complete-case rates are 11.7%, 32.1%, 43.4% and 70.4%.

Adjusted ORs versus Q1:
- Q2: 3.95 (95% CI 2.32 to 6.73, p = 4.3e-7)
- Q3: 6.39 (3.78 to 10.78)
- Q4: 22.49 (13.04 to 38.76, p = 3.9e-29)

The step from Q2 to Q3 is OR 1.62 (p = 0.026), and the step from Q3 to Q4 is OR 3.52 (p = 1e-8). The unadjusted ORs versus Q1 were 3.55 (Q2), 5.77 (Q3) and 17.90 (Q4), so adjustment increases them.

Full-sample check with feat_d filled at 0 plus a missing indicator (n=1000): feat_a OR 3.63 (p = 1.8e-38). The missing-indicator coefficient is 0.269 (p = 0.20).

![Odds ratios of outcome=1 for feat_a quartiles Q2 to Q4 versus Q1, unadjusted and adjusted for feat_b, feat_c and feat_d (log scale, complete cases n=850)](tasks/stat_3/charts/feat_a_quartile_or.png)

### 5. feat_d missingness (eda_2, stat_4)

- **Marginal tests (eda_2):** outcome rate is 41.3% for missing rows (n=150, 62 with outcome=1) and 39.4% for present rows (n=850, 335 with outcome=1); chi-square p = 0.657. Welch tests for feat_a, feat_b and feat_c by missingness give p = 0.424, 0.400 and 0.835. The eda_2 analysis reports low power with 150 missing rows.
- **Joint model (stat_4):** logistic regression of the missing indicator on feat_a, feat_b, feat_c and outcome (n=1000) finds no significant term: feat_a OR 0.89 (95% CI 0.73 to 1.09, p = 0.252), feat_b OR 1.08 (0.90 to 1.28, p = 0.412), feat_c OR 1.02 (0.86 to 1.21, p = 0.826), outcome OR 1.18 (0.79 to 1.76, p = 0.419). The model as a whole is not significant (likelihood-ratio p = 0.696; McFadden pseudo R² 0.003).

These results indicate no detectable dependence of missingness on the observed variables. They do not establish random missingness, and dependence on unobserved variables is not tested. The intervals still permit moderate effects.

![Outcome rate for rows with feat_d missing vs present (proportion of outcome=1); chi-square p=0.66](tasks/eda_2/charts/feat_d_missing_outcome_rate.png)

### 6. Prediction against baselines (ml_1, ml_2, ml_3, ml_4)

**Single 250-row test split (ml_1), with median-imputed feat_d plus missing indicator:**
- Logistic regression: log-loss 0.517, accuracy 73.6%, ROC AUC 0.804. Class-prior baseline log-loss 0.671.
- Gradient boosting (default settings): log-loss 0.792, accuracy 62.8%, ROC AUC 0.696. Training accuracy 99.7%, which indicates overfitting.
- Majority-class baseline accuracy 60.4%, ROC AUC 0.5 by construction. No interval was computed on this single split.
- Permutation importance (drop in test negative log-loss, logistic regression): feat_a 0.233 (sd 0.034), feat_d 0.085 (sd 0.015), feat_b 0.017 (sd 0.006), feat_c 0.0001 (sd 0.0002).
- The feat_d missing-indicator coefficient is 0.332, against 0.651 for feat_d itself. This coefficient has no interval or significance test in ml_1.

![Permutation importance of each feature for the best model on the test set (mean drop in neg log-loss over 20 shuffles)](tasks/ml_1/charts/perm_importance.png)

**Repeated 5×5 stratified CV with default gradient boosting (ml_2):**
- Logistic regression: log-loss 0.514 (sd 0.034; 2.5–97.5 percentile range 0.464 to 0.584), ROC AUC 0.812 (sd 0.030; range 0.756 to 0.856), accuracy 74.4% (sd 0.026).
- Gradient boosting: log-loss 0.722 (sd 0.058), ROC AUC 0.743 (sd 0.022), accuracy 68.9%.
- Class-prior baseline: log-loss 0.672 (sd 0.001), accuracy 60.3%, AUC 0.5.
- Logistic regression beats the class-prior baseline on log-loss in 25 of 25 folds (mean paired reduction 0.158). Logistic regression beats default gradient boosting on both log-loss and AUC in 25 of 25 folds (mean paired log-loss gap 0.208).
- The ranges are spreads of the 25 fold values, not confidence intervals. The folds share training data, so they are not 25 independent samples.

![Repeated 5x5 stratified CV: per-fold test log-loss and ROC AUC for logistic regression and gradient boosting](tasks/ml_2/charts/cv_logreg_vs_gboost.png)

**Tuned gradient boosting over the same 25 folds (ml_3):**
- Tuning grid: learning rate, max depth, minimum samples per leaf and L2 regularisation, selected by an inner 3-fold search within each training fold.
- Tuned gradient boosting: log-loss 0.538 (sd 0.030), ROC AUC 0.792 (sd 0.030).
- Logistic regression: log-loss 0.514 (sd 0.032), ROC AUC 0.812 (sd 0.031).
- Logistic regression has lower log-loss in 23 of 25 folds (92%) and higher ROC AUC in 23 of 25 folds (92%). The mean paired log-loss gap is 0.024, down from 0.208 with default settings.
- The most frequently selected setting (6 of 25 folds) was L2 regularisation 1.0, learning rate 0.03, max depth 2, minimum samples per leaf 40.

![Per-fold test log-loss over 25 repeated CV folds: logistic regression vs gradient boosting tuned inside each training fold](tasks/ml_3/charts/ml3_ll_logreg_vs_tuned_gboost.png)

**Reproduction of logistic regression (ml_4):**
- With the missing indicator: log-loss 0.514 (sd 0.032; range 0.465 to 0.568), ROC AUC 0.812 (sd 0.031; range 0.756 to 0.859).
- Without the indicator: log-loss 0.514 (sd 0.032; range 0.458 to 0.568), ROC AUC 0.812 (sd 0.032; range 0.755 to 0.863).
- Neither variant reproduces the ml_2 logistic regression figures (log-loss sd 0.034; AUC range 0.756 to 0.856). The source of this difference is not identified.

## Limitations

- **Single-split results are noisy.** The 250-row test set in ml_1 gives an AUC of 0.804 and an accuracy of 73.6% with no computed interval. The repeated-CV figures in ml_2 to ml_4 are more stable, but folds share training data and are not independent.
- **Odds ratios are unadjusted and overlapping** (stat_1). Adjusted estimates come only from stat_3 and are restricted to complete cases.
- **Ranking of logistic regression over gradient boosting is conditional.** The ml_2 advantage was measured with default gradient boosting settings. The ml_3 advantage is conditional on a small grid and an inner 3-fold search. A wider search was not tested.
- **Unresolved review issue on stat_3 (lead objection still stands).**
  - The stat_3 finding states that the feat_a estimate "does not depend on how the 150 missing feat_d rows are handled." This wording is not accepted. The two figures compared are OR 3.61 on the 850 complete cases and OR 3.63 on the full sample with a missing indicator. Those two figures are what the finding supports.
  - The stat_3 object `adj_model_cc` is labelled as per SD in its comment, but its values are per raw unit of feat_a. The 3.61 is per raw unit and must not be compared with the per-SD OR of 3.30 in stat_1.
- **Conflicting evidence on the feat_d missing indicator.** ml_1 reports a missing-indicator coefficient of 0.332 in the predictive model, with no interval or test. stat_3 gives 0.269 (p = 0.20) in the full-sample adjusted model. stat_4 and eda_2 find no evidence that missingness relates to outcome. These results disagree on whether the indicator carries signal; this report does not resolve that disagreement.
- **Unresolved discrepancy in ml_2 logistic regression figures.** ml_2 reports log-loss sd 0.034 and AUC range 0.756 to 0.856. The reproductions in ml_3 and ml_4 give sd 0.032 and AUC range 0.756 to 0.859 (with indicator) or 0.755 to 0.863 (without indicator). ml_4 could not reproduce the ml_2 figures, and the cause is unexplained.
- **Quartile cut-points differ between tasks.** eda_1 uses full-sample cut-points; stat_3 uses complete-case cut-points. Rates therefore differ slightly across tasks.
- **Missingness analysis has limited power.** With 150 missing rows, the eda_2 and stat_4 tests can detect only sizeable effects. The joint model tests observed variables only.
- **Log-loss of the majority-class baseline is not meaningful** because hard 0/1 predictions are scored with log-loss. It is omitted from the comparisons above.

## Open questions

- Is the feat_a effect monotone and does it hold after adjusting for feat_b, feat_c and feat_d jointly? (Answered for complete cases in stat_3; not tested on the full sample without the indicator approach.)
- Is the feat_d Q4 effect driven by a threshold, and does it interact with feat_a? (The threshold question was not tested; the feat_a × feat_d interaction is non-significant but wide.)
- Is the non-monotone feat_b pattern (Q2 above Q3) within sampling noise, or does a linear term fit adequately? (Not tested.)
- Does feat_d missingness depend on the features non-linearly or through interactions? (Not tested beyond the linear logit in stat_4.)
- Does the feat_d missing indicator contribute to logistic regression performance across resamples, and does its coefficient remain stable? (The ablation in ml_3 and ml_4 shows the log-loss means are identical, 0.514 with and without the indicator. Its coefficient stability was not tested.)
- Does a wider gradient boosting search, or a nested search with more outer repeats, change the 23 of 25 win share for logistic regression?
- Why do the ml_2 logistic regression figures not reproduce on the ml_3 and ml_4 splits?
- Does the feat_a effect differ across levels of feat_b or feat_d after adjustment? (Interaction terms were tested only without the adjusted model.)