# Repeat Visit Analysis: 2,000 Customer Records, Binary Target repeat_visit

## Summary

- **Tier is the dominant association with repeat_visit.** Repeat rates are 89.6% for gold, 38.8% for silver and 6.7% for bronze (chi-square = 1113.70 on 2 df, p = 1.45e-242, Cramér's V = 0.746). Permutation importance from gradient boosting also ranks tier first.
- **Quarter is significantly associated with repeat_visit, with a smaller effect.** Crude rates rise from 22.0% in Q1 to 59.2% in Q8 (Cramér's V = 0.229, Holm-adjusted p = 4.06e-19). Holding tier fixed, repeat odds fall with each quarter step (adjusted OR 0.817). This pattern is consistent with the crude rise reflecting a shift in tier mix across quarters, though the data do not establish why that shift occurs.
- **age, distance_km and staff_on_shift show no significant association** with repeat_visit after Holm correction across the five features. Their rank-biserial effects are negligible.
- **The tier effect holds after controlling for quarter and for continuous features.** The tier-by-quarter interaction is not significant (LR p = 0.989), and no tier interaction with distance_km or age is significant (joint LR p = 0.540).
- **Both predictive models far exceed the majority-class baseline of 57% accuracy.** Logistic regression reaches 86.75% test accuracy and ROC AUC 0.922. Gradient boosting reaches 86.5% and ROC AUC 0.902. On the 400-row test set the two are effectively tied.

## Data

- **Size:** 2,000 rows × 6 columns (one binary target, five candidate features).
- **Target:** repeat_visit. Class 0 is 57.0% and class 1 is 43.0%.
- **Features:** tier (categorical, three levels); quarter (numeric in the source, treated as categorical in the EDA, where eight levels appear in the data); age; distance_km; staff_on_shift.
- **Missing values:** none. There are no id or free-text columns and no date or time features.

## Findings

### Target distribution and descriptive rates

The class split is 57.05% repeat_visit = 0 and 42.95% repeat_visit = 1.

Repeat rates by tier (n in brackets):
- Gold: 89.6% (n = 720)
- Silver: 38.8% (n = 400)
- Bronze: 6.7% (n = 880)

Repeat rates by quarter (n = 250 per quarter): Q1 22.0%, Q2 33.2%, Q3 38.0%, Q4 42.8%, Q5 42.4%, Q6 51.6%, Q7 54.4%, Q8 59.2%. The rise is mostly monotone, but Q5 (42.4%) dips slightly below Q4 (42.8%).

Repeat rates by quartile bin of the numeric features:
- Age: 43.7%, 38.8%, 44.5%, 44.4%. Range 38.8% to 44.5%.
- distance_km: 42.7%, 44.1%, 44.2%, 40.8%. Range 40.8% to 44.2%.
- staff_on_shift: 46.4%, 41.4%, 44.1%, 39.4%. Range 39.4% to 46.4%.

Class means differ little relative to the spread of each feature. Age is 41.21 for class 0 and 41.38 for class 1. distance_km is 12.12 and 11.71. staff_on_shift is 7.68 and 7.44. For staff_on_shift, the class 1 median is 7 versus 8 overall.

![Repeat visit rate by tier (left) and by distance_km quartile (right)](tasks/eda_1/charts/eda1_rate_tier_distance.png)

These are descriptive rates only. The numeric quartile bins show much smaller spreads than tier and quarter. No significance is claimed here.

### Which features are significantly associated with repeat_visit

Holm correction was applied across the five features.

| Feature | Test | Statistic | p | Holm p | Effect | Significant (Holm 0.05) |
|---|---|---|---|---|---|---|
| tier | chi-square, 2 df | 1113.70 | 1.45e-242 | 7.27e-242 | Cramér's V 0.746 | Yes |
| quarter | chi-square, 7 df | 104.96 | 1.01e-19 | 4.06e-19 | Cramér's V 0.229 | Yes |
| age | Mann-Whitney | p = 0.628 | 0.628 | 1.0 | rank-biserial 0.013 | No |
| distance_km | Mann-Whitney | p = 0.537 | 0.537 | 1.0 | rank-biserial −0.016 | No |
| staff_on_shift | Mann-Whitney | p = 0.056 | 0.056 | 0.167 | rank-biserial −0.050 | No |

- **Tier** has the larger effect.
- **Quarter** is significant after correction, with a small-to-moderate association.
- **age:** the Welch 95% CI for the mean difference (class 1 minus class 0) is −0.87 to 1.23 years, around a difference of 0.18.
- **distance_km:** the 95% CI is −1.16 to 0.34 km, around a difference of −0.41.
- **staff_on_shift:** the 95% CI is −0.50 to 0.004, around a difference of −0.25. This is the closest to significance of the three numeric features, but it is not significant after Holm correction.

![Repeat visit rate by tier and by quarter; tests and p-values in stat1_results](tasks/stat_1/charts/stat1_rates_tier_quarter.png)

### Tier, quarter and the crude versus adjusted pattern

**Tier after controlling for quarter.** In a logistic regression with quarter as a linear control, the adjusted odds ratio for gold versus bronze is 209.45 (95% CI 136.97 to 320.28, p = 2.6e-134). The adjusted odds ratio for silver versus bronze is 11.20 (95% CI 7.90 to 15.88, p = 6.97e-42). The gold estimate differs from the 120.5 reported in the continuous-covariate model below. Adjusted estimates depend on which covariates are included, so 209.45 should not be read as the single tier effect.

**Tier-by-quarter interaction.** The likelihood-ratio test gives LR = 0.023 on 2 df, p = 0.989, with no evidence that the tier effect varies by quarter. This does not prove the within-quarter gaps are equal.

**Within-quarter gaps.** The gold-minus-bronze repeat-rate gap ranges from 0.822 to 0.905 across quarters. The silver-minus-bronze gap ranges from 0.187 to 0.480.

**Quarter effect, controlling for tier.** The adjusted odds ratio per quarter step is 0.817 (95% CI 0.764 to 0.874, p = 4.8e-9), so repeat odds fall with quarter within a tier. This points in the opposite direction from the crude rise across quarters. Both results are reported as recorded. The pattern is consistent with the crude rise reflecting the shift in tier mix across quarters. This describes the confounding pattern in this sample; it is not a causal finding.

Tier-by-quarter counts:

| Quarter | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Bronze | 180 | 160 | 140 | 120 | 100 | 80 | 60 | 40 |
| Silver | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 |
| Gold | 20 | 40 | 60 | 80 | 100 | 120 | 140 | 160 |

Bronze counts fall and gold counts rise across quarters. Silver is constant at 50 per quarter.

![Repeat visit rate by quarter, one line per tier (gold, silver, bronze)](tasks/stat_3/charts/stat3_rates_by_tier_within_quarter.png)

### Tier interaction with distance_km and age

The full logistic model used tier, centred distance_km and centred age, plus their tier interactions.

- **Within bronze:** the odds ratio per unit of distance_km is 0.999 (95% CI 0.968 to 1.032). The odds ratio per year of age is 1.013 (95% CI 0.991 to 1.036). Neither has a detectable effect in bronze.
- **Tier odds ratios relative to bronze (continuous covariates held):** silver 8.80 (95% CI 6.30 to 12.30); gold 120.5 (95% CI 84.2 to 172.4).
- **Interaction odds ratios:** silver × distance 1.016 (0.977 to 1.056); gold × distance 0.990 (0.950 to 1.031); silver × age 0.988 (0.961 to 1.016); gold × age 0.987 (0.957 to 1.017). All CIs span 1.
- **Joint LR test of the four tier × continuous terms:** chi-square = 3.11 on 4 df, p = 0.540. Tier × distance_km alone gives p = 0.343; tier × age alone gives p = 0.633.

Repeat rates within median halves:
- distance_km, low/high: bronze 6.5%/6.9%; silver 35.5%/42.0%; gold 89.0%/90.2%.
- age, low/high: bronze 5.3%/8.2%; silver 38.3%/39.3%; gold 88.9%/90.3%.

The silver rate is higher in the high distance half, but the LR test does not find this interaction significant.

![Repeat visit rate by tier within low and high halves of distance_km and of age (median split)](tasks/stat_2/charts/stat2_rates_tier_by_half.png)

### Predictive models

The data were split 80/20 with stratification and seed 42: 1,600 training rows and 400 test rows. Tier and quarter were one-hot encoded. The majority-class baseline (always predict 0) reaches 0.57 test accuracy.

| Model | Test accuracy | Precision | Recall | F1 | ROC AUC | Log loss |
|---|---|---|---|---|---|---|
| Majority-class baseline | 0.57 | – | – | – | – | – |
| Logistic regression | 0.8675 | 0.8521 | 0.8372 | 0.8446 | 0.9221 | 0.3435 |
| Gradient boosting | 0.865 | 0.8554 | 0.8256 | 0.8402 | 0.9015 | 0.3746 |

Train accuracy was 0.8575 for logistic regression and 0.8894 for gradient boosting.

The two models' test accuracies differ by one row of the 400-row test set. The ROC AUC values (0.9221 and 0.9015) and log loss values (0.3435 and 0.3746) are reported as recorded. The comparison does not establish that either model is better.

Feature importance:
- **Logistic regression** (standardised coefficients, absolute value): tier_gold 1.3435 and tier_bronze 1.2425 are the largest. The largest quarter coefficient is 0.2092 (quarter 7). staff_on_shift is 0.0732.
- **Gradient boosting, permutation importance (drop in test AUC):** tier_gold 0.3027, tier_bronze 0.0233, tier_silver 0.0093, quarter_8 0.0037, quarter_2 0.0020. distance_km is −0.0017, staff_on_shift is −0.0038 and age is −0.0064. The negative values mean permuting these features did not lower the AUC.
- **Impurity importances overstate the continuous features.** Gradient boosting's impurity importances give distance_km 0.0486 and age 0.0288, while permutation importance gives negative values for both. The permutation results are the more reliable guide.

![Test-set accuracy and ROC AUC of the majority-class baseline, logistic regression and gradient boosting](tasks/ml_1/charts/ml1_model_comparison.png)

## Limitations

- **Observational data with no stated design.** The findings are associations. Nothing in the analysis establishes a causal effect of tier, quarter or any other feature.
- **Quarter handling differs across tasks.** The EDA and the models treat quarter as categorical. The stat_3 adjustment treats quarter as linear. Adjusted estimates depend on these choices.
- **Linearity is assumed in the logit models.** No non-linear age or distance_km terms were fitted. The quartile and median-split checks are univariate or limited to tier interactions.
- **No interactions among the numeric features** (age, distance_km, staff_on_shift) were tested.
- **Holm correction covers the five features only.** The stat_2 and stat_3 tests were not corrected across families.
- **The 400-row test set cannot separate the two models on accuracy.** No cross-validation was run, so the model comparison rests on one split.
- **Sparse cells.** Gold counts are small in early quarters (20 in Q1) and bronze counts are small in late quarters (40 in Q8). Within-quarter tier rates rest on these cells.
- **Unresolved review issue on eda_1 (still standing).** The lead objected to two statements in the recorded EDA text: the phrase "a steady rise in repeat_visit rate across all eight levels", and the numeric-bin spread. The rise is mostly monotone, with Q5 (42.4%) slightly below Q4 (42.8%). The numeric bin ranges are age 38.8% to 44.5%, distance_km 40.8% to 44.2% and staff_on_shift 39.4% to 46.4%. This report uses the corrected description for the quarter trend and the ranges for the bins. The affected findings are the quarter trend and the numeric-bin spreads in the EDA section. The underlying EDA record has not been re-issued.
- **Unresolved review issues on stat_3 (still standing).** The lead's objections were: (1) the silver adjusted CI and p-value had to be reported; (2) the full tier-by-quarter counts including silver had to be shown; (3) the adjusted gold odds ratio (209.45, quarter-only control) differs from the 120.5 in stat_2 and depends on covariates; (4) "driven by tier mix" must be read as a description of the confounding pattern, not a causal statement. This report now gives the silver CI and p-value, the full counts, the covariate caveat and the descriptive wording. The affected findings are the adjusted tier odds ratios, the quarter effect and the tier-mix explanation of the crude rise. The underlying stat_3 record has not been re-issued.
- **No tasks failed.** All five recorded tasks are complete.

## Open questions

- **Why does the repeat rate rise across quarters, and is that a time trend or a seasonal effect?** The data contain no date or time field, so this cannot be checked.
- **Why do crude and tier-adjusted quarter effects point in opposite directions?** Crude repeat rates rise with quarter, while within-tier odds fall with quarter. The cause of this pattern is not established.
- **Is the shift in tier mix across quarters a sampling or operational change?** The tier-by-quarter counts show bronze falling and gold rising, but the reason is not in the data.
- **Is the tier-quarter confounding structural,** for example from changes in tier assignment over time, and does it need investigation before tier is used as a driver?
- **Are there non-linear effects of age or distance_km, or interactions among age, distance_km and staff_on_shift,** that the univariate quartile rates and linear logit terms miss?
- **Would the model comparison change under cross-validation or with more data,** given that the 400-row test set cannot distinguish logistic regression from gradient boosting on accuracy?