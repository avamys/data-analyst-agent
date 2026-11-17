# Repeat Visit Analysis: Predicting the Binary Target repeat_visit in 2,000 Rows

## Summary

- **Tier is the dominant separator.** Repeat rates are 89.6% for gold, 38.8% for silver and 6.7% for bronze (chi-square = 1113.7, dof 2, p = 1.5e-242, Cramér's V = 0.746). Tier is also the top permutation-importance feature in both fitted models.
- **Quarter is significantly associated with repeat_visit, but its marginal trend is driven by tier mix.** The pooled rate rises from 27.6% (quarters 1-2) to 56.8% (quarters 7-8). Within bronze and silver the rate falls across quarters, and within gold it is non-monotone and declines only modestly after quarters 3-4.
- **Age, distance_km and staff_on_shift show no significant association** with repeat_visit after Holm correction. Within tiers and in a gold-only multivariable model, age and distance_km show no detectable effect, though the gold estimates are imprecise.
- **Both models beat the majority-class baseline** (test accuracy 0.57). Logistic regression reached 0.8575 accuracy and 0.9247 ROC AUC; gradient boosting reached 0.8725 accuracy and 0.9029 ROC AUC. The two models disagree on which ranks better: gradient boosting has higher accuracy, while logistic regression has higher AUC and lower log loss.
- **Tier interactions were not detected.** The tier-by-distance_km and tier-by-age interaction tests were not significant (p = 0.34 and p = 0.62).

## Data

- **Size:** 2,000 rows × 6 columns.
- **Target:** repeat_visit (binary). 43.0% of rows are positive (repeat_visit = 1) and 57.0% are negative (repeat_visit = 0).
- **Features:** tier (categorical: bronze, silver, gold); quarter (range 1 to 8), age (range 18 to 85, median 41), distance_km (range 0.2 to 76.9, median 10) and staff_on_shift (range 3 to 12), all numeric.
- **Missing values:** none. No empty cells and no empty groups in any tier or bin grouping.
- **Date/time features:** none. **IDs or free-text columns:** none.

## Findings

### Repeat rate by tier and age

- Tier separates the target most strongly. Gold has a repeat rate of 89.6% (n = 720), silver 38.8% (n = 400) and bronze 6.7% (n = 880).
- Across five age bins the repeat rate stays within a narrow band, from 39.4% (31-40, n = 554) to 45.5% (51-60, n = 341). The bin rates are 44.6% (18-30, n = 406), 44.1% (41-50, n = 590) and 41.3% (61+, n = 109). No clear age trend appears.

![Rate of repeat_visit=1 by tier (left) and by age bin (right)](tasks/eda_1/charts/rate_by_tier_and_age.png)

### Repeat rate by distance, staff and quarter

- **Distance_km quartiles:** the rate is flat, from 40.8% (Q4, n = 500) to 44.1% (Q2, n = 501). Q1 is 42.7% (n = 510) and Q3 is 44.2% (n = 489).
- **Staff_on_shift bins:** the rate varies only between 39.4% and 46.4%, with no clear trend. The bins are 46.4% (3-5, n = 578), 41.4% (5-8, n = 609), 44.1% (8-10, n = 399) and 39.4% (10-12, n = 414).
- **Quarter bins:** the rate rises steadily, from 27.6% (quarters 1-2) to 40.4% (3-4), 47.0% (5-6) and 56.8% (7-8). Each bin has n = 500.

### Significance tests and effect sizes

Multiple-comparison correction used Holm step-down over the five tests (tier chi-square plus four numeric Mann-Whitney tests).

- **Tier:** chi-square = 1113.7 (dof 2), p = 1.5e-242, Holm-adjusted p = 7.3e-242, Cramér's V = 0.746. This is the only test with a very large effect size.

![Share of rows with repeat_visit=1 by tier](tasks/stat_1/charts/stat1_tier_rate.png)

- **Quarter:** Mann-Whitney p = 1.2e-23, Holm-adjusted p = 4.9e-23, rank-biserial = 0.259. The mean difference (repeat minus non-repeat) is 1.04 quarters (95% CI 0.84 to 1.23). The interval excludes zero, and repeat visits are concentrated in later quarters.
- **Age:** p = 0.63 raw, 1.0 Holm-adjusted, rank-biserial 0.013, mean difference 0.18 (95% CI −0.87 to 1.23). The interval includes zero.
- **Distance_km:** p = 0.54 raw, 1.0 Holm-adjusted, rank-biserial −0.016, mean difference −0.41 (95% CI −1.16 to 0.34). The interval includes zero.
- **Staff_on_shift:** p = 0.056 raw, 0.167 Holm-adjusted, rank-biserial −0.050, mean difference −0.25 (95% CI −0.50 to 0.004). The interval includes zero, though its upper bound is close to zero.
- Only tier and quarter remain significant at 0.05 after correction. The 95% CIs for the mean differences are Welch t-based intervals.

### Interactions of tier with distance_km and age

- **Tier × distance_km:** logit likelihood-ratio test LR = 2.15 (dof 2), p = 0.34. The tier × age test gave LR = 0.96 (dof 2), p = 0.62. Neither interaction is significant.

![Share of rows with repeat_visit=1 by tier, in low and high halves (split at tier median) of distance_km and of age](tasks/stat_2/charts/stat2_tier_halves_rate.png)

- **Within-tier distance_km** (odds ratio per SD): bronze 0.99 (95% CI 0.76 to 1.29), silver 1.13 (0.94 to 1.37), gold 0.91 (0.73 to 1.14). No detectable effect was found. Gold's rates sit near the 90% ceiling and its CI is fairly wide, so the within-tier test has limited power there. The gold estimates are consistent with a small effect but do not establish one.
- **Within-tier age** (odds ratio per SD): bronze 1.17 (95% CI 0.90 to 1.52), silver 1.01 (0.82 to 1.23), gold 1.00 (0.79 to 1.27). No detectable effect was found. For gold these estimates rule out only large effects and do not by themselves establish a small one.

### Gold tier: multivariable check

- In a logistic regression on gold-tier rows only (n = 720), with quarter and staff_on_shift as controls, distance_km shows no detectable effect: OR 0.93 per SD (95% CI 0.74 to 1.16, p = 0.51).
- With the same controls, age shows no detectable effect: OR 0.99 per SD (95% CI 0.78 to 1.26, p = 0.95).
- The CIs are about 0.4 to 0.5 log-odds wide per SD, so effects up to roughly 25% change in odds per SD in either direction are not ruled out. The absence of detection should not be read as proof of no effect.

### Predictive models

- **Split:** a stratified 80/20 split (random_state = 42) gives 1,600 training rows and 400 test rows. The test set keeps the overall balance of 57% class 0 and 43% class 1.
- **Baseline:** always predicting repeat_visit = 0 gives 0.57 test accuracy and a test log loss of 0.6833.
- **Tier encoding:** all three tier dummies (tier_bronze, tier_gold, tier_silver) were kept, with no drop_first, so they sum to 1 in every row. The logistic regression therefore relies on regularisation to handle the collinearity with the intercept. The split was not changed.

| Model | Test accuracy | Test ROC AUC | Test log loss |
|---|---|---|---|
| Majority-class baseline | 0.57 | not reported | 0.6833 |
| Logistic regression | 0.8575 | 0.9247 | 0.3452 |
| Gradient boosting | 0.8725 | 0.9029 | 0.3705 |

![Test accuracy of logistic regression and gradient boosting compared with the majority-class baseline on the 400-row test split](tasks/ml_2/charts/ml2_model_accuracy_vs_baseline.png)

- Both models are well above the baseline in accuracy and log loss. The two models disagree on ranking: gradient boosting has the higher accuracy, while logistic regression has the higher ROC AUC and lower log loss. Calibration was not assessed.

**Feature importance (permutation, drop in test AUC):**

- **Logistic regression:** tier_gold 0.2144 (sd 0.0215), tier_bronze 0.148 (sd 0.0154), quarter 0.0202 (sd 0.0064). tier_silver, age, distance_km and staff_on_shift are essentially zero.
- **Gradient boosting:** tier_gold 0.3058 (sd 0.0256), tier_bronze 0.026 (sd 0.0092). Quarter (0.0058, sd 0.0039) and tier_silver (0.0056, sd 0.003) are indistinguishable on this evidence. Age, distance_km and staff_on_shift are near zero or negative.

**Standardised logistic regression coefficients:** tier_gold 1.3254, tier_bronze −1.2292, quarter −0.4203, staff_on_shift −0.0722, distance_km −0.023, age −0.0174, tier_silver −0.0585. The quarter coefficient is negative, which is opposite to the positive marginal quarter association. It is conditional on tier, so the reversal is a conditional effect, not a contradiction. The three tier coefficients are split by the penalty because of collinearity and should not be read as separately identified effects.

### Quarter trend within tiers

- **Tier mix by quarter bin:** gold rises from 12% (1-2) to 28% (3-4), 44% (5-6) and 60% (7-8). Bronze falls from 68% to 52%, 36% and 20%. Silver is 20% in every bin.
- **Repeat rate by tier and quarter bin** (rate, n):

| Tier | 1-2 | 3-4 | 5-6 | 7-8 |
|---|---|---|---|---|
| Bronze | 8.8% (340) | 7.7% (260) | 3.9% (180) | 2.0% (100) |
| Silver | 52.0% (100) | 48.0% (100) | 31.0% (100) | 24.0% (100) |
| Gold | 93.3% (60) | 95.7% (140) | 89.5% (220) | 86.0% (300) |

- The pooled gradient (27.6%, 40.4%, 47.0%, 56.8%) is therefore associated with tier mix. Within bronze and silver, the rate declines across all four bins.
- Gold's pattern is non-monotone. It rises from 93.3% in bin 1-2 to 95.7% in bin 3-4, then declines to 89.5% in 5-6 and 86.0% in 7-8. Its decline is modest after bin 3-4. The 1-2 gold cell is small (n = 60), so its value is imprecise.
- The within-tier declines are descriptive and were not tested for significance.

![Repeat_visit rate by quarter_bin within each tier (bronze, silver, gold)](tasks/eda_2/charts/eda2_rate_by_quarter_within_tier.png)

## Limitations

- **Data:** the dataset has 2,000 rows with no missing values, no date features and no identifier or free-text columns. No data problems were reported beyond the points below.
- **Quarter-within-tier headline (eda_2, unresolved review issue):** the eda_2 headline "Within each tier the quarter association is negative" overstates the result. It holds for bronze and silver but not for gold, which is non-monotone. The corrected statement and the requested table appear in the Findings. The review objection stands for the record. The within-tier declines were not tested for significance.
- **Gold ceiling and power:** gold's repeat rate is near 90%, and its within-tier and multivariable CIs are wide (see the gold findings). The null results for gold distance_km and age are not proof of no effect.
- **Collinearity in the logistic regression:** the three tier dummies are collinear with the intercept, so the regularised tier coefficients are split by the penalty and are not separately identified. Tier-level coefficient values should not be interpreted individually.
- **Model disagreement:** the models rank differently (gradient boosting has higher accuracy; logistic regression has higher AUC and lower log loss). Calibration was not assessed.
- **Quarter in gradient boosting:** quarter's importance cannot be separated from tier_silver's in the gradient boosting model.
- **Quarter and tier confounding:** the tier mix changes across quarters. The quarter association was not tested conditional on tier in a fitted model with significance tests.
- **Task status:** all listed tasks (eda_1, stat_1, stat_2, ml_1, ml_2, eda_2, stat_3) are complete. No failed tasks were reported.

## Open questions

- Is the within-tier quarter decline statistically significant? A logistic model with tier, quarter and a tier-by-quarter interaction was suggested but not fitted.
- Does the within-tier quarter decline hold after controlling for age, distance_km and staff_on_shift?
- Why is tier composition uneven across quarters (bronze concentrated early, gold late), and is quarter confounded with the process that assigns tier? The data do not answer this.
- Does the gold-tier effect hold after controlling for quarter and age in a fitted model with confidence intervals? Stat_3 tested distance_km and age within gold, not the tier effect itself.
- Would a larger gold sample, or a pooled test of gold's numeric effects, narrow the CIs enough to establish whether gold's distance_km and age effects are small?
- Does a model with a tier-by-quarter interaction improve on the current models?
- Is the low bronze rate (6.7%) driven by a specific feature combination worth modelling?
- Would a different outcome scale or model reduce the limiting effect of the roughly 90% gold repeat rate?