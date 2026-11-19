# repeat_visit Analysis of a 2,000-Row Dataset

## Summary

- **Tier is the dominant association.** Gold's repeat-visit rate is 0.896 and bronze's is 0.067. Tier is significant (chi-square p = 1.5e-242, Cramér's V = 0.746) and stays significant after adjustment for quarter, age, distance_km and staff_on_shift (gold vs bronze OR 222.97; silver vs bronze OR 11.21).
- **Quarter is significantly associated with repeat_visit in the marginal test, but only part of that survives adjustment.** The marginal chi-square test gives p = 1.0e-19. In the adjusted logistic regression, only quarters 7 and 8 remain significant versus quarter 1 after Holm correction.
- **Age, distance_km and staff_on_shift show no significant association** after Benjamini-Hochberg correction. No interaction among the three tested pairs was detected (LR p = 0.587), though this does not establish additivity.
- **Both models beat the majority-class baseline of 0.57 on the 400-row test set.** Logistic regression reaches accuracy 0.8575 and ROC AUC 0.9246; gradient boosting reaches accuracy 0.855 and ROC AUC 0.9087. Permutation importance ranks tier first by a wide margin, with a mean ROC AUC drop of 0.460.

## Data

- **Size:** 2,000 rows × 6 columns.
- **Target:** repeat_visit (binary). Class 0 is 57.0% and class 1 is 43.0%. Overall, 859 of 2,000 rows are positive (rate 0.4295), so the majority-class baseline accuracy is 0.57.
- **Features:** quarter, age, distance_km and staff_on_shift (numeric); tier (categorical). There are no date/time features and no identifier or free-text columns.
- **Missing values:** none. The profile reports no empty cells, and the EDA confirmed zero missing values in every column, including repeat_visit. Because no values are missing, missingness cannot be related to the target.

## Findings

### Distribution of repeat_visit across groups

The repeat-visit rate varies sharply by tier and quarter, and little by staff_on_shift, age or distance_km.

- **Tier:** gold 0.896 (n=720), silver 0.388 (n=400), bronze 0.067 (n=880).
- **Quarter:** the rate rises from 0.220 in quarter 1 to 0.592 in quarter 8, with a small dip between quarters 4 and 5 (0.428 to 0.424). There are 250 rows per quarter. The trend is not steady or monotone.
- **staff_on_shift:** rates range only from 0.393 to 0.483 across levels 3 to 12 (group sizes 184 to 219), with no clear monotone pattern.
- **Age quintiles:** rates are flat, from 0.399 to 0.455 (group sizes 352 to 444).
- **distance_km quintiles:** rates are weak, from 0.405 to 0.463. The highest band is (8.3, 12.04] at 0.463 (n=389).

![Rate of repeat_visit=1 by tier](tasks/eda_1/charts/rate_by_tier.png)

![Rate of repeat_visit=1 by distance_km quintile](tasks/eda_1/charts/rate_by_distance_band.png)

### Significance and effect sizes

- **Tier:** chi-square = 1113.70 on 2 df, p = 1.5e-242, Cramér's V = 0.746. Relative to bronze, gold's rate is 0.829 higher (95% CI 0.801 to 0.857) and silver's is 0.320 higher (95% CI 0.270 to 0.371). These are Wald intervals on rate differences.
- **Quarter:** chi-square = 104.96 on 7 df, p = 1.0e-19, Cramér's V = 0.229. Rate differences versus quarter 1 are: quarter 2 +0.112 (95% CI 0.034 to 0.190); quarter 3 +0.160 (0.081 to 0.239); quarter 4 +0.208 (0.128 to 0.288); quarter 5 +0.204 (0.124 to 0.284); quarter 6 +0.296 (0.216 to 0.376); quarter 7 +0.324 (0.244 to 0.404); quarter 8 +0.372 (0.292 to 0.452).
- **Age:** no significant association (Mann-Whitney p = 0.628; rank-biserial 0.013). Point-biserial r = 0.007 (p = 0.738).
- **distance_km:** no significant association (Mann-Whitney p = 0.537; rank-biserial −0.016). Point-biserial r = −0.024 (p = 0.283).
- **staff_on_shift:** Mann-Whitney p = 0.056 (rank-biserial −0.050); point-biserial r = −0.043 (p = 0.054). It does not survive correction.
- **Benjamini-Hochberg correction across the five tests:** tier (adjusted p = 7.3e-242) and quarter (adjusted p = 2.5e-19) remain significant. Age (0.628), distance_km (0.628) and staff_on_shift (0.093) do not.

![Rate of repeat_visit=1 by tier and by quarter, with the proportion of rows with repeat_visit=1 in each group](tasks/stat_1/charts/stat1_rates_tier_quarter.png)

### Adjusted tier and quarter effects (logistic regression)

A logistic regression of repeat_visit on tier, quarter, age, distance_km and staff_on_shift (2,000 rows; McFadden pseudo R² 0.488) gives:

- **Tier:** gold vs bronze OR 222.97 (95% CI 144.71 to 343.54, p = 9.9e-133). Silver vs bronze OR 11.21 (95% CI 7.89 to 15.92, p = 1.8e-41). After Holm correction across the 12 model terms, both remain significant (gold Holm-adjusted p ≈ 1.2e-131; silver ≈ 2.0e-40).
- **Quarter:** quarter 8 vs 1, OR 0.33 (95% CI 0.19 to 0.59, Holm p = 0.0019); quarter 7 vs 1, OR 0.39 (95% CI 0.22 to 0.70, Holm p = 0.014). Quarters 2 to 6 are not significant after correction.
- **Other terms:** age OR 1.003 (p = 0.578); distance_km OR 1.004 (p = 0.585); staff_on_shift OR 0.971 (95% CI 0.925 to 1.018, p = 0.222). None is significant.

The marginal quarter associations in the chi-square tests are all significant, but after adjustment only quarters 7 and 8 remain significant. The two results differ, and this report does not resolve the difference.

### Interactions

- **Joint test:** a likelihood-ratio test of the three specified interaction blocks (tier × distance_km, tier × staff_on_shift, distance_km × staff_on_shift; 5 df) against the main-effects model gives LR chi-square = 3.744, p = 0.587. No interaction was detected at this sample size. This does not establish additivity.
- **Individual terms:** none is significant. Wald p-values are 0.332 (silver × distance_km), 0.653 (gold × distance_km), 0.572 (silver × staff_on_shift), 0.622 (gold × staff_on_shift) and 0.886 (distance_km × staff_on_shift).
- **Scope:** the test covers only these three pairs. Quarter and age were not tested as modifiers of any effect.

### Within-tier quarter pattern

Within each tier, the quarter pattern is not a steady rise:

- **Gold:** 0.900 in Q1, rising to 0.950 in Q2 and a peak of 0.983 in Q3, then declining to 0.844 in Q8.
- **Silver:** 0.460 in Q1, rising to 0.580 in Q2, then declining to 0.260 in Q8.
- **Bronze:** between 0.000 and 0.100 in every quarter (Q1 0.078, Q2 0.100, Q3 0.079, Q4 0.075, Q5 0.040, Q6 0.038, Q7 0.033, Q8 0.000).

These within-tier figures are descriptive only. No within-tier significance test was run.

The tier mix changes sharply across quarters. Gold rises from 8% of rows in Q1 to 64% in Q8. Bronze falls from 72% to 16%. Silver is 20% of rows in every quarter. Tier mix is consistent with the overall quarter rise, but this comparison is unadjusted. The adjusted model above is the test that addresses it, and it shows that quarters 2 to 6 are not significant after tier and other terms are controlled.

![Repeat_visit rate by quarter, separately for each tier, with the overall rate](tasks/eda_2/charts/rate_by_quarter_within_tier.png)

### Predictive models

On the 400-row test set, with the majority-class baseline accuracy of 0.57:

- **Logistic regression (C=1):** accuracy 0.8575, ROC AUC 0.9246, F1 0.830 (precision 0.853, recall 0.808). CV ROC AUC was 0.912.
- **Gradient boosting (learning_rate 0.05, max_depth 2, n_estimators 100):** accuracy 0.855, ROC AUC 0.9087, F1 0.827. CV ROC AUC was 0.908.

Logistic regression scores marginally higher on every test metric. With 400 test rows, this gap is small and is not established as a real difference.

Tier dominates both models:

- **Logistic regression:** the gold and bronze dummies have the largest absolute coefficients (2.60 and 2.54). Quarter has 0.40, silver 0.26, and staff_on_shift, distance_km and age all have coefficients under 0.08.
- **Gradient boosting:** gold tier importance is 0.847. Quarter is 0.017, and the other numeric features are under 0.01.

No tier-free model was fitted, so the share of predictive accuracy attributable to tier is not established.

![Test-set accuracy, ROC AUC and F1 for logistic regression and gradient boosting, against the majority-class accuracy line](tasks/ml_1/charts/ml1_model_comparison.png)

### Permutation importance

For the logistic regression model (ROC AUC on the test set, averaged over 30 repeats, tier permuted as one feature), the mean drop in ROC AUC from baseline 0.9246 is:

- **tier:** 0.460 (sd 0.031)
- **quarter:** 0.023 (sd 0.006)
- **staff_on_shift:** 0.001 (sd 0.0015)
- **distance_km:** −0.0004 (sd 0.0004), no drop
- **age:** −0.0007 (sd 0.0003), no drop

The ranking is tier > quarter > staff_on_shift > distance_km > age. This agrees with the significance results: tier and quarter are the only features significant after correction, and staff_on_shift is borderline before correction and near zero here.

## Limitations

- **Unresolved review issue, eda_2:** the tier-quarter cell size range was misstated. The full range is 20 to 180 rows (gold 20 to 160, silver 50 in every quarter, bronze 40 to 180). Affected finding: the within-tier quarter pattern. The per-tier breakdown is correct and is given above.
- **Unresolved review issue, stat_3:** the gold Holm-adjusted p in the adjusted tier finding was misstated in the source. The recorded value is about 1.2e-131, which is the raw p of 9.9e-133 multiplied by 12 model terms. Affected finding: the adjusted tier effects. The corrected value is used above.
- **Within-tier results are descriptive.** Tier-quarter cells hold 20 to 180 rows, and no significance test was run within tiers. The early rises (gold Q1 to Q3, silver Q1 to Q2) and the bronze drop to 0.000 in Q8 (n=40) may be small-sample effects.
- **Interactions were only partly tested.** The joint test covers three pairs. Quarter and age were not tested as modifiers, and the result does not establish additivity.
- **No tier-free model was fitted,** so the share of predictive accuracy due to tier is not measured.
- **Test set size:** model scores rest on 400 test rows. The logistic regression and gradient boosting difference is not established as real.
- **staff_on_shift was treated as numeric** in the tests and models. It has 10 levels with no visible trend, and its categorical treatment was not tested.
- **Marginal and adjusted quarter results differ.** Quarter is significant marginally, but only quarters 7 and 8 remain significant after adjustment. This report does not resolve the difference.
- **No failed tasks.** All seven tasks were marked complete.

## Open questions

- Does the quarter trend persist within each tier, or is it driven by the shift in tier mix? The adjusted model addresses this in part, but the within-tier pattern was not tested for significance.
- Are the early within-tier rises (gold Q1 to Q3, silver Q1 to Q2) and later declines real or noise, given cell sizes of 20 to 50 rows in several cells?
- Is the drop in bronze to 0.000 in Q8 (n=40) a small-sample artifact?
- Why does tier mix shift so strongly across quarters, and is tier assignment itself changing over time?
- How much predictive accuracy does tier account for? A model without tier, and one with tier only, have not been fitted.
- Does quarter add predictive value beyond tier?
- Do quarter or age modify the effect of tier? Does the gold or silver effect size differ by quarter?
- Should staff_on_shift be treated as categorical, given 10 levels and no adjusted linear effect? Is it worth keeping as a feature?