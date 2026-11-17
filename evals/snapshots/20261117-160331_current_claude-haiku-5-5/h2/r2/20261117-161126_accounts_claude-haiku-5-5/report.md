# Renewal Analysis of 1,600 Accounts: Drivers of the `renewed` Target

## Summary

- **Discount and support tickets are the strongest associations with renewal, and both survive correction for multiple testing.** Renewal falls from 80% at 0% discount to 35% at 30%. It rises from 18.8% at 0 tickets to 71.9% at 4 tickets. Tickets capped at 4 have an adjusted odds ratio of 2.052 per ticket, and discount has an adjusted odds ratio of 0.455 per 10 points.
- **Seats is also significantly associated with renewal.** Renewal rises from 35.0% in the lowest seats quartile to 74.7% in the highest. The adjusted odds ratio is 2.045 per 10 seats (95% CI 1.785 to 2.343), and the association does not disappear after adjusting for discount and tickets. Seats is right-skewed (max 214, median 10).
- **Region and contract length show no significant association with renewal.** Region gives p=0.617 and contract length gives p=0.414, and neither discount nor region interactions were significant.
- **Predictive models beat the majority-class baseline of 57.5% accuracy.** Logistic regression reaches 77.5% test accuracy and a test ROC AUC of 0.834. The random forest reaches 74.5% test accuracy and an AUC of 0.831, but it overfits (train accuracy 84.6%).
- **The 7–9 month signup band is a borderline result that disagrees across tests.** It is not significant after Holm correction in the univariate test (adjusted p=0.43 for the binned test), but its adjusted odds ratio is 1.481 (95% CI 1.071 to 2.048, p=0.018) in the multivariable model.

## Data

- **Size:** 1,600 rows and 7 columns.
- **Target:** `renewed` (binary). 57.5% of rows are renewed=1 and 42.5% are renewed=0. Accuracy should therefore be compared with a majority-class baseline of 57.5%.
- **Features:** five numeric features (discount_pct, seats, support_tickets, contract_months, signup_month) and one categorical feature (region). There are no date/time features and no id or free-text columns.
- **Missing values:** none. All 7 columns have zero empty cells, so missingness cannot relate to renewal.

## Findings

### Overall renewal and region

- Overall renewal is 57.5%.
- Renewal by region ranges from 55.5% (east, n=389) to 60.2% (west, n=389), with north at 57.4% (n=406) and south at 57.0% (n=416).
- The region chi-square test gives χ²=1.79 (df 3), p=0.617, Cramér's V=0.033, and Holm-adjusted p=1.0. The west vs east difference is 4.6 points (95% CI −2.3 to 11.6), which includes zero.
- In the adjusted logit, region odds ratios versus east are north 1.003 (p=0.985), south 1.168 (p=0.345) and west 1.128 (p=0.470). None is significant.

### Contract length

- Renewal is 56.5% for 12-month contracts (n=821) and 58.5% for 24-month contracts (n=779).
- The chi-square test gives χ²=0.67 (df 1), p=0.414, V=0.020, and Holm-adjusted p=1.0. The 24 vs 12 month difference is 2.0 points (95% CI −2.8 to 6.9).
- The adjusted contract odds ratio is 1.008 per month (95% CI 0.989 to 1.028, p=0.391).

![Renewal rate by region; each bar is the share of rows with renewed=1 in that group](tasks/eda_1/charts/renewal_by_region.png)

![Renewal rate by contract_months; each bar is the share of rows with renewed=1 in that group](tasks/eda_1/charts/renewal_by_contract_months.png)

### Discount

- Renewal falls steadily with discount: 80% at 0%, 65% at 10%, 50% at 20% and 35% at 30%. Each discount group has 400 rows.
- The chi-square test gives χ²=184.1 (df 3), V=0.339, and Holm-adjusted p≈0. The 0% vs 30% difference is 45 points (95% CI 38.9 to 51.1).
- In the joint model (adjusted for region, contract length and signup band), the odds ratio is 0.455 per 10 points of discount (95% CI 0.406 to 0.509, p<0.001).
- Removing the 25 accounts with 8+ tickets gives an odds ratio of 0.451.
- The logit slope for discount as a numeric variable is −0.066 per point in the main-effects model and −0.053 in the full interaction model.

![Renewal rate by discount_pct; each bar is the share of rows with renewed=1 in that group](tasks/eda_1/charts/renewal_by_discount_pct.png)

### Support tickets

- Renewal rises with tickets: 18.8% at 0 (n=69), 36.4% at 1 (n=264), 47.6% at 2 (n=355), 59.9% at 3 (n=362), 71.9% at 4 (n=256), and 74.4% at 5 (n=156). Groups with 6 or more tickets are small: 75 at 6, 38 at 7, and 20, 4 and 1 at 8, 9 and 10. Those groups renew at 89.3%, 86.8%, 100%, 100% and 100%.
- The binned test (4+ capped) gives χ²=193.6 (df 4), V=0.348, and Holm-adjusted p≈0. The Mann–Whitney rank-biserial is −0.407 (p≈0).
- Renewal for 4+ tickets exceeds 0 tickets by 58.4 points (95% CI 48.6 to 68.3).
- The adjusted odds ratio per additional ticket (capped at 4) is 2.052 (95% CI 1.855 to 2.271, p<0.001). The interaction with discount is not significant (LR=0.075, p=0.784, interaction OR 1.013).

![Renewal rate by support_tickets; each bar is the share of rows with renewed=1 in that group](tasks/eda_1/charts/renewal_by_support_tickets.png)

### Seats

- Seats is strongly right-skewed (skew 4.19), with median 10, mean 14.3 and max 214.
- Renewed accounts average 17.57 seats (median 13), against 9.95 (median 7) for non-renewed accounts. The standard deviation is 18.2 for renewed accounts and 9.8 for non-renewed accounts.
- The Mann–Whitney test gives p≈0 with rank-biserial −0.368, and the result survives Holm correction. Seats was outside the five requested features but was included in the eight-test family.
- Renewal by seats quartile is 35.0% (Q1), 57.3% (Q2), 66.6% (Q3) and 74.7% (Q4). These are unadjusted rates.
- Unadjusted, the logit coefficient is 0.0538 per seat (odds ratio 1.712 per 10 seats, 95% CI 1.532 to 1.914).
- Adjusted for discount and support tickets, the coefficient is 0.0715 per seat (odds ratio 2.045 per 10 seats, 95% CI 1.785 to 2.343), a 33% increase in the coefficient. The adjusted and unadjusted 95% CIs barely overlap. No formal test of the difference was run, so the strengthening after adjustment is descriptive.
- In the model that includes seats, support tickets has a coefficient of +0.64 per ticket and discount has −0.0889 per point. Both are strongly significant.

![Histograms of seats (count of rows per bin) and signup_month (count of rows per month)](tasks/eda_2/charts/seats_signup_histograms.png)

![Renewal rate rises with seats quartile: Q1 35.0% to Q4 74.7%](tasks/stat_3/charts/renewal_by_seats_quartile.png)

### Signup month

- Signup month barely differs by renewal status: mean 6.55 (median 7) for renewed accounts and 6.41 (median 6) for non-renewed accounts.
- The Mann–Whitney test gives p=0.411, rank-biserial −0.024, and Holm-adjusted p=1.0.
- Binned by quarter, renewal is 56.6% for months 1–3 (n=396), 54.7% for months 4–6 (n=411), 62.7% for months 7–9 (n=399) and 56.1% for months 10–12 (n=394). The binned chi-square gives p=0.108, V=0.062, and Holm-adjusted p=0.43.
- The 7–9 vs 4–6 gap is 7.9 points (95% CI 1.2 to 14.7). It does not survive correction in the univariate analysis.
- **Disagreement:** in the multivariable logit (adjusted for region, contract length, discount and tickets), the 7–9 band has an odds ratio of 1.481 vs 4–6 (95% CI 1.071 to 2.048, p=0.018). The other bands are not distinguishable from 4–6: months 1–3 has an odds ratio of 1.108 (p=0.532) and months 10–12 has 1.051 (p=0.762). I report both results without resolving them. The univariate result does not survive correction, and the adjusted result is nominally significant at 0.05.

![Renewal rate by discount, region and signup band, with the stat_1 features; bar height is the share of rows with renewed=1](tasks/stat_1/charts/renewal_rate_by_feature_stat1.png)

### Interactions: does the discount effect depend on contract or region?

- **Contract length:** the discount × contract interaction gives LR χ²=2.51 (df 3), p=0.474. Renewal rates by discount band are:

| Discount | 12 months | 24 months |
|---|---|---|
| 0% | 77.7% | 82.1% |
| 10% | 63.6% | 66.7% |
| 20% | 48.1% | 52.1% |
| 30% | 37.1% | 32.8% |

  The 24-month rate is higher at 0%, 10% and 20%, but lower at 30%. The gap is therefore not uniform across bands, although the interaction test is not significant.

- **Region:** the discount × region interaction gives LR χ²=4.80 (df 9), p=0.851. At 0% discount, rates range from 74.2% (east) to 83.5% (south). At 10%, they range from 60.0% (south) to 68.9% (north). Renewal falls from 0% to 10% in every region.
- **Both together:** adding both two-way discount interactions and contract × region gives LR χ²=11.54 (df 15), p=0.714.
- **Numeric discount:** the joint test of the discount interactions with contract and region gives LR χ²=2.84 (df 4), p=0.586.


### Predictive models

- Split: stratified train/test split on `renewed` (test size 0.25, random state 42). This gives 1,200 training rows and 400 test rows. Region is one-hot encoded with east as the reference.

| Model | Test accuracy | Test precision | Test recall | Test F1 | Test ROC AUC | Train accuracy |
|---|---|---|---|---|---|---|
| Majority-class baseline | 0.575 | 0.575 | 1.000 | 0.730 | 0.500 | 0.575 |
| Logistic regression | 0.775 | 0.782 | 0.844 | 0.812 | 0.834 | 0.766 |
| Random forest (300 trees, min leaf 5) | 0.745 | 0.754 | 0.826 | 0.788 | 0.831 | 0.846 |

- Both models beat the baseline. Logistic regression is best on test accuracy and F1, and the two models are essentially tied on ROC AUC.
- The random forest overfits: its train accuracy (0.846) is about 0.10 above its test accuracy (0.745). Logistic regression shows no such gap.
- Random forest permutation importance (mean drop in test ROC AUC, 20 repeats) ranks support_tickets 0.139 (sd 0.020), discount_pct 0.107 (sd 0.014) and seats 0.102 (sd 0.015).
- Logistic regression by standardized coefficient magnitude ranks seats 1.18, support_tickets 1.08 and discount_pct 1.01. Region_south (0.073), region_west (0.071) and signup_month (0.069) follow, then contract_months (0.022) and region_north (0.002).
- Random forest permutation values for region and contract length are within about one sd of zero: region_south −0.0017 (sd 0.0019), region_west 0.0012 (sd 0.0021), region_north −0.0024 (sd 0.0026) and contract_months −0.0014 (sd 0.0034). No clear contribution is detected for these features.
- Signup month ranks fourth by random forest impurity importance (0.096). It ranks sixth by logistic standardized coefficient (0.069). Its permutation value is −0.0040 (sd 0.0040), also within about one sd of zero.

![Left: test accuracy, ROC AUC and F1 for the majority baseline, logistic regression and random forest. Right: random forest permutation importance as the mean drop in test ROC AUC.](tasks/ml_1/charts/ml1_model_comparison.png)

### Joint adjusted model

- In the logit adjusted for region, contract length and signup band, the discount and ticket effects both remain significant (odds ratios given above). This model does not include seats.
- The joint model is consistent with additive effects. A non-significant interaction test does not establish that there is no interaction.

## Limitations

- **Associations, not causes.** All results are associations. The tasks did not test whether discount was assigned to accounts already less likely to renew (confounding). Whether the discount effect is causal is an open question.
- **Seats outliers and linearity are untested.** Seats has max 214 against median 10 and skew 4.19. The linear seats term has not been checked against outliers, nonlinearity, a log transform, capping or a spline, so the adjusted odds ratio may be influenced by a few very large accounts.
- **Seats adjustment is descriptive.** The change from 0.0538 to 0.0715 per seat after adjustment was not formally tested.
- **Signup 7–9 result is not robust.** It does not survive Holm correction in the univariate test but is nominally significant (p=0.018) in the multivariable model. The two results disagree, and the multivariable result has not been checked by bootstrap or stratified analysis.
- **Eight-plus ticket groups are small.** There are 25 rows with 8+ tickets. Removing them changes the odds ratios only slightly (discount 0.451 vs 0.455, tickets 2.013 vs 2.052), but the high renewal rates in these groups rest on very few accounts.
- **Interaction power (corrected).** The discount-interaction tests use 400 rows per discount band. Per-region cells are about 100 rows per band, and per-contract cells are about 200 per band. The nulls for region and contract interactions therefore have limited power to detect modest differences at this cell size. The earlier statement that the 20–30% cells are small is withdrawn, because every discount band has 400 rows. The 30% band also shows a reversed contract difference (32.8% for 24 months vs 37.1% for 12 months), which the interaction test does not detect.
- **Model validation is a single split.** All model scores come from one 400-row test split. Scores and the ranking of features could change under repeated cross-validation.
- **Random forest overfits.** The forest's train/test gap is about 0.10. No tuned or regularized alternative was tested.
- **Feature-ranking claim corrected.** The earlier claim that signup month "ranks fourth in both models" is withdrawn. It ranks fourth in random forest impurity importance and sixth in logistic standardized coefficients. Its permutation importance is also within about one sd of zero. The ML task's note said signup month was not in the permutation check, but the recorded values include it, so the permutation result is reported here.
- **Region and contract wording softened.** Region and contract-length permutation values are within about one sd of zero, so no clear contribution is detected. This does not establish that they have no effect.
- **Tasks.** All eight tasks (eda_1, eda_2, stat_1 to stat_4, ml_1) were completed. None failed.

## Open questions

- Is the discount effect causal, or were discounts assigned to accounts already less likely to renew?
- Do the very large seats accounts (up to 214) drive the seats effect? Does a log transform, capping or spline change the adjusted odds ratio? Is the seats–renewal relation linear on the logit scale?
- Are the adjusted and unadjusted seats coefficients significantly different?
- Is the 7–9 month signup effect real? It is nominally significant in the multivariable model but not after correction in the univariate test. Does it hold under a bootstrap or stratified check?
- Does the support-ticket effect hold after fuller adjustment, including seats? Is the ticket effect linear on the log-odds scale? Why does a higher ticket count raise renewal odds, and does ticket volume reflect engagement or account size? The data cannot answer these.
- Does the discount effect differ by contract length or region with more data? Would a bootstrap of the region and contract contrasts change the null results?
- Would a tuned gradient-boosted model or regularized random forest improve test ROC AUC beyond 0.83 without the train/test gap?
- Do the signup-month and region/contract importance results hold under repeated cross-validation rather than one 400-row test split?