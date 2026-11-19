# Repeat Visit Analysis: 2,000-Row Dataset, Binary Target repeat_visit

## Summary

- **Tier is the dominant association with repeat_visit.** Repeat rates are 89.6% for gold, 38.8% for silver and 6.7% for bronze (chi-square = 1113.70, df = 2, p = 1.45e-242, Cramér's V = 0.746). Tier is also the top feature in both ML models, and its adjusted odds ratios are large (silver 11.21, gold 222.97, both versus bronze).
- **Quarter is associated with repeat_visit, but the crude trend and the tier-adjusted pattern point in different directions.** The crude repeat rate rises from 22.0% in quarter 1 to 59.2% in quarter 8. Within tiers, rates do not rise. After adjusting for tier and the numeric features, quarters 5, 7 and 8 have odds ratios below 1 relative to quarter 1, and these are significant.
- **age, distance_km and staff_on_shift show no significant association** with repeat_visit in unadjusted tests (Holm-adjusted p = 1.0, 1.0 and 0.167) or after adjustment for tier and the other features (p = 0.578, 0.585 and 0.222). Their effects are small, and the confidence intervals do not rule out small effects.
- **Machine learning beats the majority-class reference (57% accuracy) clearly.** Logistic regression reaches 85.75% test accuracy and ROC AUC 0.925. Gradient boosting reaches 87.25% accuracy and ROC AUC 0.903. Shuffling tier lowers test ROC AUC by about 0.42 to 0.46, and the other features contribute little.
- **No significant tier interactions were found.** The tier × distance_km and tier × age likelihood-ratio tests are not significant (p = 0.343 and 0.633). The tier × staff_on_shift interaction was not tested.

## Data

- **Size:** 2,000 rows and 6 columns.
- **Target:** repeat_visit (binary). 859 rows (43.0%) are 1 and 1,141 rows (57.0%) are 0.
- **Features:** quarter, age, distance_km and staff_on_shift are numeric. tier is categorical. There are no date/time features, and no ids or free-text columns.
- **Missing values:** none in any of the six columns (0 missing cells).

## Findings

### Overall distribution and tier and quarter rates

Overall, 859 of 2,000 rows (43.0%) have repeat_visit = 1.

Repeat rate by tier:

| Tier | Repeat rate | Count |
|---|---|---|
| Gold | 89.6% | 645 of 720 |
| Silver | 38.8% | 155 of 400 |
| Bronze | 6.7% | 59 of 880 |

Repeat rate by quarter (250 rows per quarter):

| Quarter | Repeat rate | Quarter | Repeat rate |
|---|---|---|---|
| 1 | 22.0% | 5 | 42.4% |
| 2 | 33.2% | 6 | 51.6% |
| 3 | 38.0% | 7 | 54.4% |
| 4 | 42.8% | 8 | 59.2% |

The rate rises across quarters but is not strictly monotonic: quarter 5 (42.4%) is slightly below quarter 4 (42.8%).

![Repeat visit rate by tier (left) and by quarter (right)](tasks/eda_1/charts/repeat_rate_by_tier_and_quarter.png)

### Tier and quarter: significance and effect size

- **tier:** chi-square = 1113.70 on 2 df, p = 1.45e-242 (Holm p = 7.27e-242), Cramér's V = 0.746. Gold minus bronze is a difference of 0.829 (95% CI 0.801 to 0.857). Silver minus bronze is a difference of 0.320 (95% CI 0.270 to 0.371). These are unadjusted differences in proportions.
- **quarter:** chi-square = 104.96 on 7 df, p = 1.01e-19 (Holm p = 4.06e-19), Cramér's V = 0.229, a small-to-moderate effect. Quarter 8 minus quarter 1 is a difference of 0.372 (95% CI 0.292 to 0.452). This interval is the recomputed Wald interval (see Limitations).

![Repeat visit rate by tier (left) and by quarter (right)](tasks/stat_1/charts/stat1_rate_by_tier_quarter.png)

### Tier mix by quarter, and rates within tiers

Tier composition shifts strongly across quarters:

- **Bronze** share falls from 72% in quarter 1 (180 rows) to 16% in quarter 8 (40 rows).
- **Gold** share rises from 8% in quarter 1 (20 rows) to 64% in quarter 8 (160 rows).
- **Silver** is fixed at 20% (50 rows) in every quarter.

Repeat rate within each tier, by quarter:

- **Bronze:** 7.8% in quarter 1, 10.0% in quarter 2, 7.9%, 7.5%, 4.0%, 3.8%, 3.3%, and 0% in quarter 8.
- **Gold:** 90.0% in quarter 1, 95.0%, 98.3%, 93.8%, 88.0%, 90.8%, 87.9%, and 84.4% in quarter 8.
- **Silver:** 46% in quarter 1, 58%, 50%, 46%, 28%, 34%, 22%, and 26% in quarter 8. The path is not monotonic.

Within tiers, the quarter trend does not persist. Bronze falls from 7.8% to 0%. Gold stays high, between 84.4% and 98.3%, with no rise. Silver falls from 46% to 26%. The tier-mix shift toward gold is a candidate explanation for the overall rise from 22.0% to 59.2%. The data do not quantify its share. A tier-standardized repeat rate per quarter is needed to measure it.

![Left: tier share by quarter. Right: repeat visit rate by quarter within each tier.](tasks/eda_3/charts/tier_mix_and_within_tier_repeat_by_quarter.png)

### Adjusted quarter effects

Adjusted for tier, age, distance_km and staff_on_shift, the odds ratios for each quarter relative to quarter 1 are:

| Quarter | Adjusted OR | 95% CI | p |
|---|---|---|---|
| 2 | 1.506 | 0.880 to 2.576 | 0.135 |
| 3 | 1.228 | 0.710 to 2.125 | 0.462 |
| 4 | 0.994 | 0.568 to 1.739 | 0.983 |
| 5 | 0.457 | 0.255 to 0.819 | 0.009 |
| 6 | 0.583 | 0.327 to 1.039 | 0.067 |
| 7 | 0.392 | 0.219 to 0.701 | 0.002 |
| 8 | 0.332 | 0.186 to 0.593 | 0.0002 |

The crude rise and the adjusted quarter odds ratios point in opposite directions. The crude repeat rate rises with quarter. Holding tier fixed, the later-quarter odds ratios are below 1. The adjusted odds ratios describe the quarter effect with tier held constant. The crude rise is a difference in proportions, which is a different comparison. The report does not resolve this disagreement. Tier mix is a partial explanation, the share is not quantified, and within-tier rates do not reproduce the crude rise.

### Age, distance_km and staff_on_shift: distributions and unadjusted tests

Mean and median values are nearly identical across the two outcome classes:

- **age:** mean 41.21 (repeat_visit = 0) vs 41.38 (repeat_visit = 1); median 41.0 vs 42.0.
- **distance_km:** mean 12.12 vs 11.71; median 10.0 vs 9.9.
- **staff_on_shift:** mean 7.68 vs 7.44; median 8.0 vs 7.0.

![Box plots of age, distance_km and staff_on_shift split by repeat_visit (0 vs 1)](tasks/eda_2/charts/eda2_box_by_repeat.png)

Mann-Whitney tests:

- **age:** p = 0.628 (Holm p = 1.0), rank-biserial 0.013, mean difference 0.18 years (95% CI −0.87 to 1.23).
- **distance_km:** p = 0.537 (Holm p = 1.0), rank-biserial −0.016, mean difference −0.41 km (95% CI −1.16 to 0.34).
- **staff_on_shift:** p = 0.056 (Holm p = 0.167), rank-biserial −0.050, mean difference −0.25 staff (95% CI −0.50 to 0.004).

None of these three tests is significant after correction. The confidence intervals include small effects.

Repeat rates by binned ranges:

- **age quintiles:** from 39.9% (age 30 to 38) to 45.5% (age 45 to 52), against an overall rate of 43.0%.
- **distance_km quintiles:** from 40.5% (18 to 77 km) to 46.3% (8.3 to 12 km), with no monotonic trend.
- **staff_on_shift bins:** from 39.5% to 46.4%, with no monotonic trend. The lowest-staffed bin (3 to 5) has the highest rate, at 46.4%.

### Interactions with tier

- **tier × distance_km:** likelihood-ratio = 2.142 on 2 df, p = 0.343. The test does not show that the distance effect is the same in every tier, and it does not show that silver has no distance effect.
- **tier × age:** likelihood-ratio = 0.913 on 2 df, p = 0.633.

Within-tier repeat rates, split at the 10 km median:

- **Silver:** 35.5% at or below 10 km (95% CI 28.9% to 42.1%, n = 200) vs 42.0% above 10 km (35.2% to 48.8%, n = 200). The stated high-minus-low gap is about 6.5 points, with overlapping intervals. This is the largest within-tier gap, but the overall interaction test is not significant.
- **Bronze:** 6.5% low (4.2% to 8.9%, n = 429) vs 6.9% high (4.5% to 9.2%, n = 451). The stated gap is about +0.4 points.
- **Gold:** 89.0% low (85.9% to 92.1%, n = 382) vs 90.2% high (87.1% to 93.4%, n = 338). The stated gap is about +1.2 points.

![Repeat visit rate by tier for low and high distance_km, with 95% Wald CIs](tasks/stat_2/charts/stat2_rates_by_tier_distance.png)

### Adjusted associations of the numeric features

Adjusted logistic regression, with tier and quarter as categorical covariates:

- **staff_on_shift:** OR 0.971 per additional staff member (95% CI 0.925 to 1.018), p = 0.222. This is conditional on tier, quarter, age and distance_km.
- **age:** OR 1.003 per year (95% CI 0.992 to 1.015), p = 0.578.
- **distance_km:** OR 1.004 per km (95% CI 0.989 to 1.020), p = 0.585.
- **Tier:** silver OR 11.21 (95% CI 7.89 to 15.92) and gold OR 222.97 (95% CI 144.71 to 343.54), both versus bronze, both p < 0.001.

The model has n = 2,000 and 859 repeat visits, with pseudo R² = 0.488. The numeric-feature odds ratios are conditional on tier. The adjustment does not establish that tier confounding is absent. The crude silver-minus-bronze difference (0.320) is a proportion difference and is not comparable to the adjusted odds ratio of 11.21.

### Machine learning

Setup: stratified 80/20 split with random_state 42, giving 1,600 training rows and 400 test rows. Tier is one-hot encoded, and the four numeric features are standardized.

| Model | Test accuracy | Precision | Recall | F1 | ROC AUC |
|---|---|---|---|---|---|
| Majority-class reference | 0.57 | 0.0 | 0.0 | 0.0 | 0.5 |
| Logistic regression | 0.8575 | 0.8528 | 0.8081 | 0.8299 | 0.9246 |
| Gradient boosting | 0.8725 | 0.8497 | 0.8547 | 0.8522 | 0.9029 |

The majority-class row is a reference rule, not a model. Its 0.57 accuracy equals the share of repeat_visit = 0. Both models clearly beat it. The two models disagree on ranking: gradient boosting has the higher accuracy and F1, and logistic regression has the higher ROC AUC.

Permutation importance (mean drop in test ROC AUC over 30 repeats):

- **tier:** 0.463 for logistic regression and 0.425 for gradient boosting. This is by far the largest.
- **quarter:** 0.020 for logistic regression and 0.006 for gradient boosting. This is a small secondary feature.
- **age, distance_km and staff_on_shift:** all values lie between −0.0043 and 0.0001. These are negligible on this 400-row test set. This does not rule out small effects.

![Permutation importance of each feature for gradient boosting, measured as the drop in test ROC AUC when the feature is shuffled](tasks/ml_1/charts/ml1_permutation_importance.png)

## Limitations

- **Unresolved review issue, quarter 8 vs quarter 1 interval.** The stat_1 finding reports a confidence interval for the quarter 8 minus quarter 1 difference that does not match the Wald interval computed from the counts 148/250 and 55/250. The recomputed interval, 0.292 to 0.452, is the one used in this report, and it also appears in stat_3. This affects the quarter findings in stat_1 and stat_3.
- **Unresolved review issue, eda_3 interpretation.** The within-tier trend does not persist, so the wording "partly persists" is removed. The report states that tier-mix composition is a candidate explanation for the overall rise, that its share is not quantified, and that a tier-standardized rate is needed to measure it. The lead's objection still stands.
- **Unresolved review issue, stat_3 wording.** The phrase "the crude rise mostly reflects tier mix" is replaced. Tier mix is a partial explanation of the crude quarter rise, within-tier rates do not reproduce it, and its share is not quantified.
- **Power.** The age, distance_km and staff_on_shift tests do not rule out small effects. The staff_on_shift result (raw p = 0.056) is not significant after correction. The 400-row test set cannot resolve small effects in the ML permutation importances.
- **Silver distance gap.** The silver high-minus-low gap (about 6.5 points) is not significant as an interaction, and it has not been tested within silver alone.
- **Bronze.** The low bronze repeat rate (6.7%) is not explained by the data. Whether age, distance_km or staff_on_shift vary with tier or quarter was not tested.
- **Confounding.** The quarter effect is confounded with tier mix in the crude analysis. The adjusted models hold tier fixed, but the tier × quarter interaction was not fitted.
- **Quarter coding.** Quarter is numeric in the ML models and categorical in the logistic model. Results are not directly comparable across these approaches.
- **Failed tasks.** None. All tasks (eda_1, eda_2, eda_3, stat_1, stat_2, stat_3, ml_1) are complete.

## Open questions

- Is the quarter effect confounded by tier mix? Does the quarter trend hold within each tier when tested formally (stratified analysis or a tier-by-quarter interaction)?
- How much of the overall rise from 22.0% to 59.2% does tier mix explain? A tier-standardized repeat rate per quarter is needed to quantify it.
- Is the within-silver decline from 46% to 26% statistically meaningful, given 50 rows per quarter?
- Does staff_on_shift interact with tier in predicting repeat_visit? This was asked in several tasks and was not tested.
- Why are bronze repeat visits so low (6.7%)? Do age, distance_km or staff_on_shift vary with tier or quarter?
- Is the silver distance gap real? A test of distance within silver alone, or a power analysis, is needed.
- Would tier-by-quarter interactions, tuned gradient boosting, or repeated cross-validation on the full data change the ML results or resolve the small age, distance_km and staff_on_shift effects?
- Are the quarter odds ratios unstable because of collinearity between tier and quarter? Variance inflation factors and interval widths were not checked.