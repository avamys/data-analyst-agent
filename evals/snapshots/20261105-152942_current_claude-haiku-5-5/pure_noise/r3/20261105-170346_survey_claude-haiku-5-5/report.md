# Outcome Analysis of an 800-Row Survey: Binary Target `outcome` (41.1% Positive)

## Summary

- **Group and numeric features show no significant association with outcome after correction.** Outcome rate does not differ by group (chi-square = 3.75, 3 df, p = 0.289), and no numeric feature differs between outcome classes after Holm correction (all five Holm p = 1.0). All effect sizes are negligible (|Cohen's d| ≤ 0.09).
- **No feature × group interaction survives correction.** The smallest raw p is feat_3 (p = 0.0295), which has Holm p = 0.147.
- **The models do not beat the majority-class baseline.** Test accuracy is 0.588 for the baseline, 0.550 for logistic regression and 0.531 for gradient boosting. Cross-validated ROC AUC is 0.533 (logistic regression) and 0.458 (gradient boosting), both near chance.
- **The feat_3 Q4 dip is not established as a threshold.** The post hoc split at the Q3/Q4 boundary is nominally significant (p = 0.028). After correcting for the search over cutpoints, the best step is not significant (p = 0.154). Feat_3 is the most consistent positive numeric signal in the repeated permutation-importance check, but its effect is small.
- **Group-level rates are the largest visible differences but are not significant.** g1 has the highest outcome rate (46.2%) and g4 the lowest (36.8%). The g1 vs g4 gap has a raw p of 0.075 and a Holm-adjusted p of 0.450.

## Data

- **Size:** 800 rows, 7 columns: the target `outcome`, five numeric features (`feat_1` to `feat_5`) and one categorical column, `group`.
- **Target:** `outcome` is binary. Overall, 41.1% of the 800 rows are positive (329 positives, 471 negatives), and 58.9% are negative.
- **Group levels:** the data contains four levels (g1, g2, g3, g4), not the three the analysis was framed around. All results use four levels.
- **Missing values:** none in any of the seven columns, so no imputation was needed.
- **Date/time features:** none. **Identifier or free-text columns:** none.

## Findings

### Outcome rate by group

Outcome rates, with row counts and approximate 95% CI half-widths:

| Group | Outcome rate | n | CI half-width |
|---|---|---|---|
| g1 | 46.2% | 182 | ±7.2 pts |
| g2 | 42.2% | 206 | ±6.7 pts |
| g3 | 40.0% | 200 | ±6.8 pts |
| g4 | 36.8% | 212 | ±6.5 pts |

- The omnibus chi-square test shows no significant difference by group: chi-square = 3.75, 3 df, p = 0.289.
- Pairwise chi-square tests with Holm correction over all six pairs show no significant difference. The smallest raw p is g1 vs g4 (difference −9.4 points, raw p = 0.075, Holm p = 0.450). g1 vs g2 has raw p = 0.500, and g1 vs g3 has raw p = 0.267.

![Outcome rate (share with outcome=1) by group level and by feat_1 quartile bin](tasks/eda_1/charts/outcome_rate_by_group_and_feat1_quartile.png)

![Outcome rate (share with outcome=1) per group level, with 95% normal-approximation CIs](tasks/stat_1/charts/stat1_group_outcome_rate.png)

### Numeric features: quartile outcome rates and association with outcome

Outcome rate by quartile (Q1 lowest), each bin n = 200 except where noted:

| Feature | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| feat_1 | 44.0% | 39.5% | 38.5% | 42.5% |
| feat_2 | 39.5% | 43.5% | 41.5% | 40.0% |
| feat_3 | 42.5% | 43.5% | 44.0% | 34.5% |
| feat_4 | 39.8% (n=201) | 42.2% (n=199) | 44.0% | 38.5% |
| feat_5 | 38.5% | 40.0% | 43.5% | 42.5% |

The largest quartile gap is feat_3 Q4 (34.5%) against 42.5% to 44.0% in Q1 to Q3. The section "Feat_3 Q4 dip: location and threshold" covers this further.

Each feature was compared between outcome classes (difference = outcome 1 minus outcome 0):

| Feature | Mean diff (95% CI) | Welch p | Cohen's d | MWU p | Rank-biserial | Holm p |
|---|---|---|---|---|---|---|
| feat_1 | −0.014 (−0.160 to 0.132) | 0.855 | −0.013 | 0.740 | −0.014 | 1.0 |
| feat_2 | 0.017 (−0.124 to 0.158) | 0.813 | 0.017 | 0.978 | 0.001 | 1.0 |
| feat_3 | −0.082 (−0.222 to 0.057) | 0.246 | −0.083 | 0.179 | −0.056 | 1.0 |
| feat_4 | −0.005 (−0.143 to 0.133) | 0.944 | −0.005 | 0.864 | 0.007 | 1.0 |
| feat_5 | 0.091 (−0.051 to 0.233) | 0.207 | 0.090 | 0.210 | 0.052 | 1.0 |

- No numeric feature differs significantly between outcome classes after Holm correction. Raw Welch p-values range from 0.207 (feat_5) to 0.855 (feat_1).
- Effects are negligible for all features. Ranked by absolute Cohen's d: feat_5 (0.090), feat_3 (0.083), feat_2 (0.017), feat_1 (0.013), feat_4 (0.005).
- The rank-biserial values above are the corrected ones. An earlier computation with reversed signs for feat_1, feat_3 and feat_5 is superseded.
- For feat_4, the mean difference (−0.005) and rank-biserial (+0.007) have opposite signs. Both are reported as negligible (MWU p = 0.864).
- Feature means by outcome class (class 0 / class 1): feat_5 0.001 / 0.092; feat_3 0.055 / −0.027. Medians: feat_5 0.036 / 0.083; feat_3 0.086 / 0.002.

### Feat_3 Q4 dip: location and threshold

**Decile view.** Outcome rates by feat_3 decile, D1 to D10 (n = 79 to 81 each): 45.0%, 40.0%, 37.5%, 46.9%, 45.6%, 45.0%, 38.8%, 46.2%, 33.8%, 32.5%.

- The Q3/Q4 boundary (feat_3 = 0.706) falls inside D8 (range 0.551 to 0.842). The largest drop is from D8 (46.2%) to D9 (33.8%, range 0.852 to 1.231), so the decline appears to begin near feat_3 = 0.85. This is an approximate location from a 10-bin grid, not an estimated threshold.
- D3 (37.5%) and D7 (38.8%) also sit below the overall rate. No test has been run on decile-to-decile differences, so it is not established that the D9 and D10 drops exceed chance at n = 80 per decile.

![Outcome rate (%) per feat_3 decile with row counts (n=79 to 81 each). Colours: D1-D7 lie wholly below the Q3/Q4 boundary (feat_3 = 0.706), D8 (gold) contains the boundary, D9 and D10 lie wholly above it.](tasks/eda_2/charts/eda_2_feat3_decile_rates.png)

**Split at the boundary.** Outcome above versus below 0.706: chi-square = 4.83, p = 0.028. The split was chosen after the Q4 dip was seen in the quartile table, so the test is post hoc and uncorrected. The finding describes it as modest evidence for a difference.

**Within groups (exploratory).** Outcome rate below versus above the 0.706 boundary:

- g1: 48.9% (n=139) to 37.2% (n=43); within-group p = 0.178
- g2: 47.1% (n=153) to 28.3% (n=53); within-group p = 0.017
- g3: 42.3% (n=156) to 31.8% (n=44); within-group p = 0.210
- g4: 35.5% (n=152) to 40.0% (n=60); within-group p = 0.543

These within-group p-values are uncorrected across four group levels. The g2 result is consistent with the nominal g2 × feat_3 interaction (see "Feature × group interaction"), but that interaction is not significant after Holm correction.

**Cutpoint scan with permutation correction (stat_3, status: partial).**

- The scan, adjusted for group, selects a best cutpoint of 0.801 with observed LR statistic 5.95. After permutation correction for the search (200 permutations), p = 0.154. The step is not significant once the cutpoint choice is accounted for.
- The bootstrap 95% percentile interval for the best cutpoint is −1.008 to 0.919 (200 resamples). The threshold location is not estimated with useful precision.
- A naive group-adjusted logistic step at feat_3 > 0.85 gives coefficient −0.427, OR 0.65, p = 0.022. This p-value does not account for the scan or the post hoc choice of 0.85, so it overstates the evidence for a threshold.
- Within group g2, going above feat_3 0.706 gives an adjusted OR of 0.44 (95% CI 0.23 to 0.87, Wald p = 0.019). The group-by-boundary interaction is not significant (coefficient −0.600, p = 0.131), so the g2 drop is not clearly different from the other groups.

**Disagreement between findings.** The post hoc split at 0.706 (eda_2, p = 0.028, uncorrected) is nominally significant. The cutpoint scan with permutation correction (stat_3, p = 0.154) is not. The candidate boundaries also differ: 0.706 (quartile), 0.801 (scan optimum) and 0.85 (decile-based). The task does not resolve this. The overall conclusion of stat_3 is that the evidence does not establish a threshold effect near 0.85 after correcting for the search.

![Permutation null for the feat_3 cutpoint scan (counts)](tasks/stat_3/charts/stat3_perm_null.png)

### Feature × group interaction

Likelihood-ratio tests for feature × group interaction (3 df each), with Holm correction over the five numeric features:

| Feature | LR χ² | Raw p | Holm p |
|---|---|---|---|
| feat_1 | 0.951 | 0.813 | 1.0 |
| feat_2 | 6.287 | 0.098 | 0.394 |
| feat_3 | 8.985 | 0.029 | 0.147 |
| feat_4 | 1.301 | 0.729 | 1.0 |
| feat_5 | 3.485 | 0.323 | 0.968 |

- No interaction is significant after Holm correction. The feat_3 result is nominal only.
- For feat_3, the g2 × feat_3 Wald coefficient is −0.418 (p = 0.049), unadjusted. The other feat_3 interaction terms are g3 −0.127 (p = 0.546) and g4 0.178 (p = 0.403). The g2 term is not supported by the corrected omnibus test.
- The interaction test does not establish that slopes are equal across groups; it only fails to detect group differences in slope at the corrected level.
- In the five per-feature models, the interaction terms for feat_1, feat_2, feat_4 and feat_5 all have p of at least 0.08. The smallest are g2:feat_2 (0.347, p = 0.081) and g4:feat_5 (0.322, p = 0.128).

### Predictive modelling

Held-out test set (160 rows; 640 training rows; stratified 80/20 split, seed 42):

| Model | Accuracy | Balanced accuracy | ROC AUC | Precision | Recall | Train accuracy |
|---|---|---|---|---|---|---|
| Majority-class baseline | 0.588 | 0.500 | 0.500 | 0.0 | 0.0 | 0.589 |
| Logistic regression | 0.550 | 0.479 | 0.391 | 0.313 | 0.076 | 0.584 |
| Gradient boosting | 0.531 | 0.493 | 0.467 | 0.400 | 0.273 | 0.836 |

- Neither model beats the baseline on accuracy or balanced accuracy. The logistic regression test ROC AUC of 0.391 is below chance. With only 160 test rows, this single estimate is unstable and does not indicate a reliable inverse relationship.
- Five-fold stratified CV on all 800 rows: logistic regression mean ROC AUC 0.533 (sd 0.041); gradient boosting 0.458 (sd 0.027). Both are near chance.
- Gradient boosting overfits (train accuracy 0.836 against 0.531 on test). Logistic regression is more stable (0.584 train, 0.550 test), but neither model generalises.

![Balanced accuracy and ROC AUC on the 160-row test set for the majority-class baseline, logistic regression and gradient boosting](tasks/ml_1/charts/ml_1_model_scores.png)

**Permutation importance, single run (ml_1, superseded for stability).** In one permutation run on the test set, feat_3 had the largest positive importance in both models (logistic regression +0.023; gradient boosting +0.016). feat_5 (−0.040) and feat_1 (−0.018) were negative in logistic regression. These values are tentative because each comes from one run on 160 rows.

**Repeated stratified CV with per-fold permutation importance (ml_2, logistic regression).** This run used 3 seeds × RepeatedStratifiedKFold (5 splits, 3 repeats) = 45 folds, with 10 permutations per fold. It supersedes the earlier single-seed run.

- Baseline ROC AUC of logistic regression: 0.495 (sd 0.041), near chance.
- **feat_3** has a mean importance of +0.008 (95% interval +0.002 to +0.013). Its seed-level means are positive in all 3 seeds, and 71% of folds are positive. The interval assumes independent folds, so it is optimistic. The effect is small relative to the fold sd.
- **feat_5** has a mean of +0.005 (interval −0.001 to +0.011). The interval spans zero, so it is not consistently different from zero.
- **feat_1** (−0.008; −0.012 to −0.005), **feat_2** (−0.007; −0.011 to −0.003) and **feat_4** (−0.009; −0.013 to −0.006) are negative in every seed. Negative permutation importance here means permuting these features does not hurt and may slightly help. This is descriptive only.
- **Group levels** show positive importance for group_all (+0.013; +0.004 to +0.021), g1 (+0.012; +0.007 to +0.017) and g4 (+0.012; +0.007 to +0.017), all positive in every seed. g2 (−0.004) and g3 (−0.004) are negative in every seed (each interval −0.007 to −0.001). These group results are descriptive, since the model is near chance and the folds are treated as independent.

## Limitations

- **Group count differs from the framing.** The analysis was set up for three group levels; the data has four (g1 to g4). All results use four.
- **The feat_3 threshold is post hoc.** The 0.706 boundary was chosen after the Q4 dip was seen in the quartile table, and the 0.85 step was chosen after the decile view. The split test (p = 0.028) is uncorrected. The corrected cutpoint scan (p = 0.154) is not significant. The bootstrap interval for the cutpoint is very wide (−1.008 to 0.919) and rests on 200 resamples.
- **stat_3 is partial.** Its planned checks were not completed: a replication in a new sample, a multivariable logistic model with a spline in feat_3, and a test of the g2 drop across all group levels and several candidate boundaries.
- **Within-group p-values are uncorrected** across the four group levels. The g2 above-boundary drop (within-group p = 0.017; adjusted OR 0.44, p = 0.019) is not supported by the interaction test (p = 0.131).
- **Low power at this sample size.** Quartile bins contain about 200 rows and decile bins about 80. Non-significant results mean the data do not establish an effect; they do not show that no effect exists. Gaps of a few percentage points in outcome rate are within the CI half-widths (about ±7 points per group).
- **Model results are near chance.** Neither model beats the majority-class baseline, and CV AUCs are 0.533 and 0.458. Permutation importances are small and come from a near-chance model, so they are not reliable drivers of the outcome. The per-fold intervals treat folds as independent and are optimistic.
- **Earlier results superseded.** The single-seed permutation run (ml_1 test-set importances) and the earlier rank-biserial signs in the feature table are superseded by the corrected analyses above.
- **Interaction results do not establish equal slopes.** The LR tests fail to detect group differences in slope at the corrected level; they do not show that slopes are equal.

**Numbers not traced to a recorded fact.** The automatic check found no recorded value for these numbers:
- 329 in: "- **Target:**   is binary. Overall, 41.1% of the 800 rows are positive (329 positives, 471 negatives), and 58.9% are negative."
- 471 in: "- **Target:**   is binary. Overall, 41.1% of the 800 rows are positive (329 positives, 471 negatives), and 58.9% are negative."

## Open questions

- Does the feat_3 drop above about 0.85 replicate in a new sample or with pre-specified cutpoints? Is it a real threshold?
- Does the feat_3 effect hold after adjusting for group and feat_1 to feat_5 in a multivariable logistic model with a spline in feat_3 and a properly corrected feat_3 × group interaction test?
- Does the g2 above-boundary drop survive correction across all group levels and several candidate boundaries, or is it reproducible in a new sample?
- Is the feat_3 Q4 outcome rate (34.5%) different from the other quartile bins when tested directly as a localized comparison?
- Are the group differences in outcome rate (g1 46.2% versus g4 36.8%) real, given the non-significant corrected tests? Does the positive group contribution in permutation importance reflect real group differences or near-chance noise?
- Does feat_5 separate outcome classes well enough to be useful on held-out data (AUC)? Its effect is small (d = 0.09, CI spanning zero), and the held-out model AUCs found so far are near chance.
- Would a model using group and binned features, rather than raw numeric features, perform above chance under repeated stratified CV across seeds?