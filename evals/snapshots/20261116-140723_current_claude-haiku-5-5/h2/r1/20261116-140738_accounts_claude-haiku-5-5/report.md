# Renewal Drivers in a 1,600-Account Dataset: Target `renewed`

## Summary

- **Discount and support tickets are the strongest renewal signals.** Renewal falls steadily as discount rises: 80% at 0%, 65% at 10%, 50% at 20%, 35% at 30%. Discount has a Cramér's V of 0.339. Renewal rises with support tickets, with a rank-biserial effect of 0.407 and an odds ratio of 1.633 per additional ticket.
- **Seats is also significantly associated with renewal** (rank-biserial 0.368). Region and contract length show no significant association.
- **The discount effect does not differ detectably by contract length or region** (interaction p = 0.16 and p = 0.85). Discount and support tickets are not significantly associated with each other (Spearman p = 0.52), and the discount effect remains after adjusting for tickets.
- **Logistic regression beats the majority-class baseline.** Test accuracy is 0.7688 and ROC AUC is 0.8323, against 0.575 accuracy and 0.5 AUC for the baseline. Permutation importance points to support tickets and discount, with all other features near zero. The ranking of seats differs between the methods.
- **The gain for 6 or more tickets is not an artefact of the 8–10 ticket levels.** Accounts with 6 or 7 tickets renewed at 88.5%, against 66.8% for 3 to 5 tickets, but these groups are small and the size of the gain is imprecise.

## Data

- **Size:** 1,600 rows × 7 columns.
- **Target:** `renewed` (binary). 57.5% of accounts renewed (920 of 1,600) and 42.5% did not (680).
- **Features:** numeric `discount_pct`, `seats`, `support_tickets`, `contract_months`, `signup_month`; categorical `region`. There are no date/time features, identifiers or free-text columns.
- **Missing values:** none. The missing-value count is 0 for all seven columns.

## Findings

### Overall renewal and renewal by group

Renewal varies most with discount and support tickets. Region and contract length deviate little from the overall 57.5% rate.

- **Discount (n = 400 per level):** 0% 80%, 10% 65%, 20% 50%, 30% 35%. The 0% and 30% groups deviate most, each by 22.5 points from the overall rate.
- **Support tickets:** renewal rises from 18.8% at 0 tickets to 74.4% at 5 tickets. The 8-ticket group shows 100%, but it has only 20 accounts. Rates by level are given in the support-ticket section below.
- **Region:** east 55.5% (n = 389), north 57.4% (n = 406), south 57.0% (n = 416), west 60.2% (n = 389). The largest deviation is west, at 2.7 points.
- **Contract months:** 12 months 56.5% (n = 821), 24 months 58.5% (n = 779). Both deviate by 1.0 point from the overall rate.

![Renewal rate by discount_pct level](tasks/eda_1/charts/renewal_by_discount.png)

![Renewal rate by region](tasks/eda_1/charts/renewal_by_region.png)

### Numeric features by renewal class

- **Seats:** renewed accounts have a mean of 17.57 and median of 13. Non-renewed accounts have a mean of 9.95 and median of 7. Seats is strongly right-skewed (skew 4.19) with 105 IQR outliers, so the medians are the safer comparison.
- **Support tickets:** renewed accounts have a mean of 3.52 and median of 3. Non-renewed accounts have a mean of 2.27 and median of 2. Skew is 0.64, with 25 IQR outliers.
- **Signup month:** mean 6.55 (renewed) vs 6.41 (not renewed); medians 7 vs 6. Distribution is symmetric, with no outliers.
- **Contract months:** mean 17.95 (renewed) vs 17.70 (not renewed); medians are 12 in both classes. Distribution is symmetric, with no outliers.

This comparison covers only these four columns. Discount was not included in it, and the discount pattern in the first section is the stronger one.

![Box plots of seats and support_tickets for renewed=0 and renewed=1 accounts](tasks/eda_2/charts/numeric_by_renewed.png)

### Feature associations and significance

Tests were run with Holm correction across all seven features. Effect sizes are Cramér's V for the chi-square tests and rank-biserial for the Mann-Whitney tests. These two scales cannot be compared directly, so the cross-family ordering is indicative only.

- **Chi-square family:**
  - Discount: V = 0.339 (95% CI 0.294 to 0.381), Holm-adjusted p = 6.7e-39. Significant.
  - Region: V = 0.033 (95% CI 0.018 to 0.091), Holm-adjusted p = 1.0. Not significant.
  - Contract months: V = 0.020 (95% CI 0.001 to 0.070), Holm-adjusted p = 1.0. Not significant.
- **Mann-Whitney family:**
  - Support tickets: rank-biserial 0.407 (95% CI 0.355 to 0.454), Holm-adjusted p = 9.3e-45. Renewed accounts have more tickets.
  - Seats: rank-biserial 0.368 (95% CI 0.310 to 0.417), Holm-adjusted p = 9.7e-36. Renewed accounts tend to have more seats.
  - Signup month: rank-biserial 0.024 (95% CI −0.035 to 0.082), not significant. The direction is not meaningful.
  - Contract months: rank-biserial 0.021 (95% CI −0.029 to 0.069), not significant.

Only discount, support tickets and seats remain significant after correction.

![Ranked absolute effect sizes of features against renewal](tasks/stat_1/charts/stat1_effect_ranking.png)

### Discount effect by contract length and region

Renewal falls as discount rises in every contract-length and region subgroup. Across all groups the rate is non-increasing from 0% to 10% to 20% to 30%.

- **Contract length, 0% to 30% renewal:** 12 months 77.7% to 37.1% (n = 193 and 202); 24 months 82.1% to 32.8% (n = 207 and 198). The 0-to-30 gap is 0.406 for 12 months and 0.493 for 24 months.
- **Region, 0% to 30% renewal:** east 74.2% to 33.3%; north 80.6% to 33.0%; south 83.5% to 35.7%; west 80.9% to 38.2%. The 0-to-30 gaps are 0.408, 0.476, 0.478 and 0.427 respectively.
- **Interaction tests:** discount × contract length LR χ² = 1.97 (df 1, p = 0.16). Discount × region LR χ² = 0.80 (df 3, p = 0.85). Neither is significant.

The smallest step in any subgroup is east at 24 months, from 76.6% at 0% to 75.5% at 10%. Subgroups in the region × contract-length cells contain 37 to 62 accounts each.

![Renewal rate by discount_pct within each contract_months group (left) and region group (right); shares of accounts renewed](tasks/stat_2/charts/stat2_rates_by_group.png)

### Discount and support tickets

- **Association:** no significant association between discount and tickets (Spearman ρ = 0.016, p = 0.52; χ² = 41.1 on 30 df, p = 0.085). The χ² test is weak evidence because the crosstab is sparse.
- **Tickets and renewal:** logit odds ratio 1.633 per additional ticket (95% CI 1.519 to 1.756, p = 3e-40).
- **Discount within ticket bands:** renewal falls as discount rises in each band.
  - 0–2 tickets (group n = 163, 179, 174, 172 at 0%, 10%, 20%, 30%): renewal 68.7%, 43.6%, 37.4%, 13.4%.
  - 3–4 tickets (group n = 166, 161, 156, 135): renewal 84.9%, 78.3%, 52.6%, 38.5%.
  - 5+ tickets (group n = 71, 60, 70, 93): renewal 94.4%, 93.3%, 75.7%, 69.9%.
- **Discount odds ratio per 10 points:** raw 0.517 (95% CI 0.469 to 0.571, p = 4e-39). Adjusted for tickets, 0.441 (95% CI 0.394 to 0.494, p = 4e-45).

The discount gradient looks flatter in the 5+ band than in the 0–2 band. This pattern was not tested formally.

### Accounts with 6 or more support tickets

Renewal by support-ticket level (n, rate, Wilson 95% CI):

| Tickets | n | Rate | 95% CI |
|---|---|---|---|
| 0 | 69 | 18.8% | 11.4% to 29.6% |
| 1 | 264 | 36.4% | 30.8% to 42.3% |
| 2 | 355 | 47.6% | 42.5% to 52.8% |
| 3 | 362 | 59.9% | 54.8% to 64.9% |
| 4 | 256 | 71.9% | 66.1% to 77.0% |
| 5 | 156 | 74.4% | 67.0% to 80.6% |
| 6 | 75 | 89.3% | 80.3% to 94.5% |
| 7 | 38 | 86.8% | 72.7% to 94.2% |
| 8 | 20 | 100% | 83.9% to 100% |
| 9 | 4 | 100% | 51.0% to 100% |
| 10 | 1 | 100% | 20.7% to 100% |

- **Sensitivity check (excluding 8, 9 and 10 tickets):** 6 or 7 tickets renewed at 88.5% (100 of 113, Wilson 95% CI 81.3% to 93.2%). Accounts with 3 to 5 tickets renewed at 66.8% (517 of 774).
- **Difference:** 21.7 points (Wald 95% CI 15.0 to 28.5). Two-proportion z = 4.68, p = 2.8e-6. Fisher exact p = 6.3e-7, odds ratio 3.82, Cohen's h = 0.54 (medium).
- **Pooled 6+ comparison (reference only):** 90.6% (125 of 138) against 66.8%. The difference is 23.8 points, z = 5.64, p = 1.7e-8. The 8–10 levels inflate this figure, so the sensitivity comparison is the main evidence.

Levels 9 and 10 (n = 4 and n = 1) should not be cited as effects. The 8-ticket level (n = 20) is too small for a precise rate.

![Renewal rate per support_tickets level with 95% Wilson intervals; n shown above each point](tasks/stat_4/charts/stat4_renewal_by_tickets.png)

### Predictive modelling

Models used region one-hot encoding and a stratified 80/20 split (seed 42): 1,280 training and 320 test rows.

| Model | Test accuracy | Test ROC AUC | Test F1 | Train accuracy |
|---|---|---|---|---|
| Majority-class baseline | 0.575 | 0.5 | — | — |
| Logistic regression | 0.7688 | 0.8323 | 0.8063 | 0.7695 |
| Gradient boosting | 0.7344 | 0.8158 | 0.7733 | 0.9219 |

- Gradient boosting overfits: train accuracy 0.9219 against test accuracy 0.7344.
- **Permutation importance (logistic regression, drop in test AUC, 30 repeats):**
  - Support tickets: 0.1585 (sd 0.0189).
  - Discount: 0.1166 (sd 0.0192).
  - Seats: 0.0730 (sd 0.0131).
  - All other features: 0.0012 or less (see Limitations).
- **Coefficient magnitudes (absolute):** seats 1.1782, support tickets 1.1084, discount 1.0128, then signup month 0.0619, and the region and contract-length terms at 0.0327 to 0.0495.

The two importance methods disagree on the order of the top features. Coefficient magnitude ranks seats first, while permutation importance ranks support tickets first and seats third. Both are reported here without resolving the difference.

![Test-set ROC AUC of the majority baseline and two models](tasks/ml_1/charts/ml1_model_auc.png)

## Limitations

- **Unresolved review issue, ml_1 (importance of other features).** The bullet stating that all other features have a mean AUC drop of 0.0010 or less is incorrect. region_east has a drop of 0.0012. The remaining features have drops of 0.0012 or less, with region_east the largest at 0.0012. The drops are near zero. Given their standard deviations (0.0005 to 0.0012), no importance was estimated as distinguishable from zero. This affects the statements about contract months, signup month and region in the predictive findings.
- **Small groups:** 8, 9 and 10 support-ticket levels (n = 20, 4 and 1). The 6 and 7 ticket levels (n = 75 and 38) are usable but imprecise. The 6-or-7 vs 3-to-5 gain is smaller than the pooled comparison and less precise than its direction.
- **Subgroup interaction tests:** the region × contract-length cells contain 37 to 62 accounts each. The non-significant interactions do not rule out differences in the discount effect.
- **Chi-square for tickets and discount:** the crosstab is sparse, so the non-significant result (p = 0.085) is weak evidence.
- **Cross-family effect sizes:** Cramér's V and rank-biserial are on different scales. The overall ordering of features is indicative only.
- **Single test split:** the model results rest on one 320-row test set. Permutation importance is computed on that set.
- **Gradient boosting** overfits (train 0.9219 vs test 0.7344).
- **Seats skew:** skew is 4.19 with 105 IQR outliers. The effect was not checked against a log transform or against outliers.
- **Association only:** the findings describe associations with renewal. They do not establish causes.

**Numbers not traced to a recorded fact.** The automatic check found no recorded value for these numbers:
- 680 in: "- **Target:**   (binary). 57.5% of accounts renewed (920 of 1,600) and 42.5% did not (680)."

## Open questions

- Does seats add renewal signal beyond discount and support tickets in a multivariable model? The findings give no answer, and the two importance methods disagree on its rank.
- Is there a formal discount × support-ticket interaction in the logit model? The flatter gradient in the 5+ band was not tested.
- Does the support-ticket effect remain strong after controlling for discount, and is it non-linear around 6 or more tickets?
- Does the 6-or-more gain hold after controlling for discount, and does seats explain renewal within the 6-or-more group?
- Would a model with discount × support-ticket interaction terms beat the current logistic regression on test AUC?
- Are the small subgroup differences in the discount effect (contract length 12 vs 24 months, east vs south) reproducible with more data? Confidence intervals on each 0-to-30 gap were not computed.
- Does a log transform of seats change its association with renewal?