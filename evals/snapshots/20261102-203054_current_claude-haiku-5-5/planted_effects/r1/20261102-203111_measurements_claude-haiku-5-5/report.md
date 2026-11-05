# Outcome Analysis of a 1,000-Row Dataset: Predictors of the Binary Outcome

## Summary

- **feat_a is the strongest predictor of outcome.** Its outcome rate rises from 11.6% in the bottom quartile to 70.8% in the top quartile (chi-square p = 3.1e-41, Cramér's V = 0.437, Holm-corrected p = 1.2e-40).
- **feat_d is the second-strongest association, but only on the 850 rows where it is observed.** Its outcome rate rises from 24.9% to 58.2% across observed quartiles (chi-square p = 3.3e-11, Cramér's V = 0.247). Rows with feat_d missing have an outcome rate of 41.3%, not significantly different from the 39.4% of rows with it observed (p = 0.66).
- **feat_b has a smaller, non-monotone association** (Cramér's V = 0.177, Holm-corrected p = 1.5e-6). feat_c shows no significant association with outcome (p = 0.36).
- **No interaction was detected.** Adding feat_a × feat_b and feat_a × feat_c terms did not improve the logistic model (LR chi-square 1.00 on 2 df, p = 0.61). This is no significant evidence of effect modification in this data, not proof that none exists.
- **Both models beat the majority-class baseline on a 200-row test set.** Accuracy is 75.5% for logistic regression and 75.5% for gradient boosting, against 60.5% for the baseline. ROC AUC is 0.821 and 0.801, respectively. feat_a and feat_d carry most of the predictive signal; feat_b and feat_c add little once those two are included.

## Data

- **Size:** 1,000 rows × 5 columns.
- **Target:** `outcome` (binary). Class 0: 60.3%; class 1: 39.7%.
- **Features:** four numeric features (feat_a, feat_b, feat_c, feat_d). There are no categorical, date/time, identifier or free-text features.
- **Missing values:** feat_d is missing for 150 rows (15.0%). The other features have no missing values. For modelling, feat_d was imputed with its training-set median (0.043).

## Findings

### 1. Outcome rate across quantile bins

The overall outcome rate is 39.7% across all 1,000 rows.

**feat_a** has a strong, monotone relationship with outcome. Quartile bins contain 251, 249, 250 and 250 rows, with outcome rates of 11.6%, 32.5%, 44.0% and 70.8% (Q1 to Q4). Quartile edges are -3.331, -0.704, 0.056, 0.669 and 3.134.

**feat_b** has a weaker, non-monotone relationship. Each bin has 250 rows, with outcome rates of 26.8%, 44.4%, 37.6% and 50.0%. The dip in Q3 has not been tested for noise. Quartile edges are -3.066, -0.629, 0.051, 0.748 and 3.669.

**feat_c** shows little relationship with outcome. Each bin has 250 rows, with outcome rates of 38.8%, 42.8%, 35.6% and 41.6%, all close to the overall 39.7%. Quartile edges are -3.37, -0.653, -0.054, 0.674 and 3.297.

By quartile spread, feat_a is the most informative (about 59 percentage points), then feat_b (about 23 points), then feat_c (about 7 points).

![Share of rows with outcome=1 within each quartile bin of feat_a, feat_b and feat_c; dashed line is the overall rate of 39.7%](tasks/eda_1/charts/eda1_outcome_rate_by_quartile.png)

### 2. Significance and effect sizes

Chi-square tests were run on quartile bins against outcome, with Holm correction across the four features.

| Feature | Chi-square p | Holm-corrected p | Cramér's V | Q4 − Q1 rate difference (95% CI) |
|---|---|---|---|---|
| feat_a | 3.1e-41 | 1.2e-40 | 0.437 | +59.2 pp (52.4 to 66.1) |
| feat_d (observed rows, n = 850) | 3.3e-11 | 9.8e-11 | 0.247 | +33.3 pp (24.5 to 42.1) |
| feat_b | 7.6e-7 | 1.5e-6 | 0.177 | +23.2 pp (14.9 to 31.5) |
| feat_c | 0.36 | 0.36 | 0.057 | +2.8 pp (−5.8 to 11.4) |

- Ranked by Cramér's V: feat_a > feat_d > feat_b > feat_c.
- feat_a, feat_d and feat_b remain significant after Holm correction. feat_c does not.
- The feat_d result describes only the 850 rows where feat_d is observed. A separate recalculation from the data reproduced it (chi-square p = 3.27e-11, n = 850).
- The feat_b association is not monotone across bins.

![Share of rows with outcome=1 within each quartile bin of feat_a, feat_b, feat_c and feat_d (feat_d on observed rows only); dashed line is the overall rate of 39.7%](tasks/stat_1/charts/stat1_outcome_rate_by_quartile.png)

### 3. feat_d by quartile (observed rows only)

Of 1,000 rows, 850 have feat_d observed and 150 were excluded. Quartile edges on these rows are -3.047, -0.6212, 0.052, 0.6987 and 3.276, with bin sizes of 213, 212, 212 and 213.

The outcome rate rises with feat_d quartile: 24.9% (Q1), 35.4% (Q2), 39.2% (Q3) and 58.2% (Q4). The quartile test is reported in Section 2.

![Outcome rate by feat_d quartile among rows where feat_d is observed (150 rows with missing feat_d excluded)](tasks/eda_3/charts/eda_3_outcome_rate_by_feat_d_quartile.png)

### 4. feat_d missingness

- **Missingness and outcome:** The outcome rate is 41.3% when feat_d is missing (n = 150) and 39.4% when observed (n = 850). The difference is +1.9 pp (95% CI −6.6 to 10.5). Chi-square p = 0.66; Fisher exact p = 0.65.
- **The CI does not rule out a difference.** The interval runs from −6.6 to 10.5 pp. The non-significant result does not establish that outcome-linked missingness is absent.
- **Missingness and other features:** Rows with feat_d missing do not differ significantly on the other features (Welch t-test p-values: feat_a 0.42, feat_b 0.40, feat_c 0.83). Their means and standard deviations are close to those of observed rows.

### 5. Interactions

A logistic regression with main effects and interaction terms was fitted to all 1,000 rows.

- **Main effects:** feat_a has an odds ratio of 3.349 per unit (Wald p = 2.7e-37). feat_b has an odds ratio of 1.332 per unit (Wald p = 0.00015). feat_c has an odds ratio of 1.002 per unit (Wald p = 0.97), so it has no detectable main effect once feat_a and feat_b are in the model. The confidence intervals for these main-effect odds ratios were not recorded and are not reported here.
- **Interaction test:** Adding the feat_a × feat_b and feat_a × feat_c terms does not improve fit (LR chi-square 1.00 on 2 df, p = 0.61).
- **feat_a × feat_b:** coefficient 0.063, odds ratio 1.065 (95% CI 0.89 to 1.28), Wald p = 0.50.
- **feat_a × feat_c:** coefficient −0.066, odds ratio 0.936 (95% CI 0.78 to 1.12), Wald p = 0.47.
- **2×2 split at the feat_a median (0.056) and feat_c median (−0.054):**

| feat_a | feat_c | Outcome rate | n |
|---|---|---|---|
| At or below median | At or below median | 23.5% | 264 |
| At or below median | Above median | 20.3% | 236 |
| Above median | At or below median | 60.2% | 236 |
| Above median | Above median | 54.9% | 264 |

The feat_a effect is similar across feat_c strata, consistent with the non-significant feat_a × feat_c interaction.

### 6. Predictive models

Models were evaluated on a 200-row test set against a majority-class baseline.

| Model | Accuracy | ROC AUC | Log loss |
|---|---|---|---|
| Majority-class baseline | 60.5% | 0.5 | 0.671 (constant prior) |
| Logistic regression | 75.5% | 0.821 | 0.500 |
| Gradient boosting | 75.5% | 0.801 | 0.533 |

Both models beat the baseline. The two models have the same accuracy; logistic regression has the higher AUC and lower log loss. The 200-row test set gives wide uncertainty on these differences, and no interval or significance test was run on them.

Permutation importance (drop in test-set ROC AUC when the feature is shuffled):

| Feature | Logistic regression | Gradient boosting |
|---|---|---|
| feat_a | 0.222 (sd 0.0346) | 0.215 (sd 0.0349) |
| feat_d | 0.083 (sd 0.0187) | 0.086 (sd 0.0221) |
| feat_b | 0.0004 (sd 0.0084) | 0.007 (sd 0.0107) |
| feat_c | 0.0002 (sd 0.0011) | 0.005 (sd 0.0064) |

feat_a is the most important feature in both models. feat_d is second, and its importance is clearly above zero even though 15% of its values were imputed. feat_b and feat_c add almost no predictive value.

![Left: permutation importance of each feature on the test set for logistic regression and gradient boosting (drop in ROC AUC). Right: test-set ROC AUC of the majority-class baseline, logistic regression and gradient boosting; dashed line is chance (0.5).](tasks/ml_1/charts/ml1_model_comparison.png)

**Disagreement:** The stat_1 result (feat_b is significantly associated with outcome, p = 7.6e-7 unadjusted) and the stat_2 result (feat_b main effect Wald p = 0.00015 in the full logistic model) both show a feat_b association. The ml_1 result says feat_b adds almost no predictive value once feat_a and feat_d are included. These findings are reported as they stand and were not reconciled.

## Limitations

- **Missing feat_d values:** 150 rows (15%) lack feat_d. The feat_d association in Section 2 describes only the 850 observed rows. In the models, missing values were imputed with the training median.
- **Non-significant missingness result:** The test in Section 4 is non-significant, and its 95% CI (−6.6 to 10.5 pp) does not exclude a meaningful difference in outcome rate between missing and observed rows.
- **Unverified confidence intervals (unresolved review issue):** The 95% CIs for the stat_2 main-effect odds ratios were printed but not recorded, so they cannot be verified. They are omitted from this report, and the main-effect odds ratios are reported without intervals.
- **Interaction wording (unresolved review issue):** The stat_2 result is no significant evidence of effect modification of feat_b or feat_c by feat_a in this data (LR chi-square 1.00 on 2 df, p = 0.61). It does not establish that no interaction exists. Only linear interaction terms were tested.
- **Non-monotone feat_b pattern:** The Q3 dip in feat_b has not been tested for sampling noise.
- **Predictive models:** The test set has 200 rows, and no cross-validation or bootstrap intervals were computed. The model comparison therefore carries wide uncertainty.
- **feat_d not in the multivariable model:** The stat_2 logistic model did not include feat_d. The feat_d association has not been checked after adjustment for the other features.
- **Failed tasks:** None.

**Numbers not traced to a recorded fact.** The automatic check found no recorded value for these numbers:
- 0.0346 in: "| feat_a | 0.222 (sd 0.0346) | 0.215 (sd 0.0349) |"
- 0.0349 in: "| feat_a | 0.222 (sd 0.0346) | 0.215 (sd 0.0349) |"
- 0.0187 in: "| feat_d | 0.083 (sd 0.0187) | 0.086 (sd 0.0221) |"
- 0.0221 in: "| feat_d | 0.083 (sd 0.0187) | 0.086 (sd 0.0221) |"
- 0.0084 in: "| feat_b | 0.0004 (sd 0.0084) | 0.007 (sd 0.0107) |"
- 0.0107 in: "| feat_b | 0.0004 (sd 0.0084) | 0.007 (sd 0.0107) |"
- 0.0011 in: "| feat_c | 0.0002 (sd 0.0011) | 0.005 (sd 0.0064) |"
- 0.0064 in: "| feat_c | 0.0002 (sd 0.0011) | 0.005 (sd 0.0064) |"

## Open questions

- Is the non-monotone feat_b pattern (dip in Q3) real or sampling noise? A trend test or bin-level confidence intervals would answer this.
- Does the feat_d association hold after adjusting for feat_a, feat_b and feat_c in a logistic regression?
- Does the feat_d association hold when a missingness indicator is added, and does the indicator add anything?
- Does feat_a's effect remain after adjusting for feat_b, feat_c and feat_d together?
- Does feat_a change the effect of feat_b when feat_b is modelled non-linearly (splines or binned feat_b)?
- How far could the feat_d association move under plausible missingness mechanisms? Multiple imputation or bounds on the missing rows' outcome rates would quantify this.
- Are the model differences between logistic regression and gradient boosting stable under cross-validation or bootstrap?
- Does feat_d missingness depend on the unobserved feat_d value itself? This cannot be tested from the data and is a question for the data owner.