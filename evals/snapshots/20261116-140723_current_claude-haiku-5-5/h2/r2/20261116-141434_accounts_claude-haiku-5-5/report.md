# Renewal Analysis of 1,600 Accounts: Predicting the Renewed Target

## Summary

- **Discount is the strongest and most robust association with renewal.** Renewal falls from 80% at 0% discount to 35% at 30%. The association holds on the Bonferroni-corrected test (p = 3.8e-41) and remains after adjustment. The adjusted coefficient is larger in magnitude (-0.089 per point) than the raw one (-0.066).
- **Support tickets and seat count are positively associated with renewal.** Renewal rises from 32.7% for 0 to 1 tickets to 90.6% for 6 to 10 tickets, and from 35.0% for 1 to 5 seats to 74.7% for 19 to 214 seats. Both survive Bonferroni correction.
- **Region, contract length and signup month show no significant association with renewal** after correction. The region rates range from 55.5% to 60.2%, and contract length shows a 2-point raw gap (56.5% vs 58.5%).
- **Models beat the majority baseline clearly.** On the 320-row test set, logistic regression reaches 76.9% accuracy and gradient boosting 75.6%, against 57.5% for the baseline. ROC AUC is 0.832 and 0.836 respectively, and the two are effectively tied. Support tickets and discount are the most important features for the gradient boosting model.
- **The discount-by-contract interaction is not significant** (p = 0.168). The data are consistent with a small contract benefit at low discount that disappears at high discount, but the evidence is weak.

## Data

- 1,600 rows and 7 columns: five numeric features (discount_pct, seats, support_tickets, contract_months, signup_month) and one categorical feature (region).
- Target: renewed (binary). 920 of 1,600 accounts renewed (57.5%) and 42.5% did not.
- No date/time features and no identifier or free-text columns.
- Missing values: none in any column. A check within the EDA task confirmed this, and the 9-column model feature matrix also has none.

## Findings

### Overall renewal and region

Renewal varies little by region. The rates were: west 60.2% (389 accounts), north 57.4% (406), south 57.0% (416) and east 55.5% (389). A chi-square test gave chi2 = 1.79, dof = 3, p = 0.617, Cramér's V = 0.033, a negligible effect. After Bonferroni correction across six tests, p = 1.0.

![Renewal rate by region and by discount_pct level](tasks/eda_1/charts/renewal_rate_region_discount.png)

![Rank-biserial effect size of each numeric feature on renewal, with 95% bootstrap CI; positive means higher values among renewed accounts](tasks/stat_1/charts/stat1_effects.png)

### Discount

Renewal falls steeply as discount rises. The rates were 80% at 0% (400 accounts), 65% at 10% (400), 50% at 20% (400) and 35% at 30% (400).

- Mann-Whitney comparison of renewed versus not renewed accounts: rank-biserial = -0.384 (95% bootstrap CI -0.432 to -0.332), p = 6.4e-42, Bonferroni p = 3.8e-41. Median discount was 10 for renewed accounts and 20 for those not renewed.
- Logistic regression, raw: coefficient -0.066 per point (95% CI -0.076 to -0.056). Odds ratio per 10 points: 0.517.
- Logistic regression, adjusted for seats, support_tickets, contract_months and region: coefficient -0.089 per point (95% CI -0.102 to -0.077). Odds ratio per 10 points: 0.409. The adjusted magnitude is 35.5% larger than the raw one.

The discount association is not explained away by account size or support load. Adjustment strengthened it. The analysis did not establish the mechanism behind the strengthening, because the discount distribution across seats and ticket bins was not recorded (see Limitations).

![Logistic regression coefficient for discount_pct on renewed (log-odds per percentage point, 95% CI), raw and adjusted for seats, support tickets, contract months and region](tasks/stat_3/charts/discount_coef_raw_vs_adjusted.png)

### Seats and support tickets

Renewal rises with seat count. The rates were 35.0% for 1 to 5 seats (437 accounts), 57.3% for 6 to 10 (410), 66.6% for 11 to 18 (377) and 74.7% for 19 to 214 (376). Among renewed accounts the median seat count was 13, against 7 among those not renewed. Rank-biserial = 0.368 (95% CI 0.318 to 0.420), p = 1.9e-36, Bonferroni p = 1.2e-35.

Renewal rises strongly with support tickets. The rates were 32.7% for 0 to 1 tickets (333 accounts), 53.8% for 2 to 3 (717), 72.8% for 4 to 5 (412) and 90.6% for 6 to 10 (138). Among renewed accounts the median was 3 tickets, against 2 among those not renewed. Rank-biserial = 0.407 (95% CI 0.361 to 0.455), p = 1.3e-45, Bonferroni p = 8.0e-45.

### Contract length and the discount interaction

The main effect of contract length is weak and not significant. Renewal was 56.5% for 12-month contracts (821 accounts) and 58.5% for 24-month contracts (779). Rank-biserial = 0.021 (95% CI -0.031 to 0.068), p = 0.414, Bonferroni p = 1.0.

Renewal by discount and contract length:

| Discount | 12-month | 24-month |
|---|---|---|
| 0% | 77.7% (n=193) | 82.1% (n=207) |
| 10% | 63.6% (n=220) | 66.7% (n=180) |
| 20% | 48.1% (n=206) | 52.1% (n=194) |
| 30% | 37.1% (n=202) | 32.8% (n=198) |

Renewal falls with discount in both contract groups.

- The interaction term is not significant: likelihood-ratio chi2 = 1.90 (df 1), p = 0.168. The coefficient is -0.0012 on the logit scale (SE 0.0008, p = 0.169).
- At low discount (0 and 10%), 24-month contracts renewed 4.7 points more often than 12-month contracts (74.9% vs 70.2%; 95% CI -1.5 to +10.9). This is not significant.
- At high discount (20 and 30%), the difference is -0.3 points (95% CI -7.2 to +6.6).
- The difference between these two effects is +5.0 points (95% CI -4.2 to +14.2).

![Renewal rate by discount_pct level, split by 12 and 24 month contracts](tasks/stat_2/charts/renewal_rate_discount_contract.png)

### Signup month

The signup-month pattern is weak and non-monotonic. Renewal by month ranged from 53.5% (month 1) to 64.7% (month 9, the highest), with 125 to 141 accounts per month. Rank-biserial = 0.024 (95% CI -0.035 to 0.081), p = 0.411, Bonferroni p = 1.0. The month-to-month differences are small relative to the sample sizes.

### Discount distribution across seats and tickets

Mean discount by seats bin: 16.0 (1 to 5 seats, n=437), 13.7 (6 to 10, n=410), 15.0 (11 to 18, n=377) and 15.3 (19+, n=376). The bin means do not show a clear monotone slope in seats.

Mean discount by tickets bin: 15.0 (0 to 1, n=333), 14.8 (2 to 3, n=717), 14.8 (4 to 5, n=412) and 16.9 (6 to 10, n=138). Only the top bin sits clearly above the others.

Logit coefficient for discount under different adjustments:

- Raw: -0.066 (95% CI -0.076 to -0.056)
- With seats: -0.070 (CI -0.081 to -0.060)
- With support_tickets: -0.082 (CI -0.093 to -0.070)
- With both: -0.089 (CI -0.101 to -0.077)

The coefficient becomes more negative when either variable is added, which the findings describe as consistent with suppression. The direction of the discount–tickets and discount–seats correlations is inferred from this coefficient change and is not confirmed by a recorded correlation (see Limitations).

![Mean discount_pct by seats bin and by support_tickets bin](tasks/stat_4/charts/stat4_discount_by_bins.png)

### Predictive models

The data were split 80/20 with stratification and random_state = 42, giving 1,280 training rows and 320 test rows. The renewal rate was 57.5% in both splits. The feature table has 9 columns: the five numeric features plus four region dummies.

| Model | Test accuracy | ROC AUC | Log loss |
|---|---|---|---|
| Majority baseline | 0.575 | 0.500 | 0.682 |
| Logistic regression | 0.769 | 0.832 | 0.498 |
| Gradient boosting | 0.756 | 0.836 | 0.492 |

Both models gain about 18 to 19 points of accuracy over the baseline. The AUC gap between the two models is about 0.003 on 320 rows, which the findings describe as effectively tied. Logistic regression has slightly higher accuracy, and gradient boosting has slightly higher AUC and lower log loss.

![Test accuracy of logistic regression, gradient boosting and majority baseline](tasks/ml_2/charts/ml2_model_vs_baseline.png)

For gradient boosting, permutation importance on the test set (mean drop in ROC AUC, sd over 20 repeats) ranks:

1. support_tickets: 0.1500 (sd 0.0172)
2. discount_pct: 0.1266 (sd 0.0174)
3. seats: 0.0872 (sd 0.0138)

The remaining features are near zero: region_east 0.0026 (sd 0.0014), signup_month 0.0001 (sd 0.0030), and contract_months -0.0016 (sd 0.0022). The other region dummies are also near zero.

## Limitations

- **Unresolved review issue on the stat_4 direction claims.** The lead's review of stat_4 objects to the stated direction. The finding says discount is positively correlated with support_tickets and with seats, inferred from the change in the coefficient. The review argues that the implied direction is negative, and that the tickets bin means do not clearly show a positive relation (only the 6 to 10 bin is higher, at 16.9). The direct correlation or slope of discount on seats and on tickets was computed but not recorded, so the direction is not confirmed. This report does not resolve the disagreement. The suppression reading of the adjusted coefficient change is conditional on the direction, and the claim is affected accordingly. The renewal-by-bin rates cited above come from the EDA task, not from stat_3.
- **Causal reading is not established.** The findings describe associations. The adjusted discount effect does not show the mechanism, and the stat_3 finding notes that high-discount accounts may be assigned by a policy linked to unobserved account quality. Whether discount causes changes in renewal is not tested.
- **Interaction results are underpowered.** The discount-by-contract interaction is not significant. With about 200 accounts per cell, the finding notes a larger sample may be needed to detect an interaction of around 5 points. The confidence intervals for the low- and high-discount contract effects are wide.
- **Small differences are not separable from noise.** The signup-month and region differences, and the gradient boosting versus logistic regression difference, are within the sampling variability of 125 to 141 accounts per month, 389 to 416 accounts per region and 320 test rows.
- **Model evaluation uses a single split.** The model scores come from one stratified 80/20 split (random_state = 42) and one test set of 320 rows. The baseline AUC of 0.500 is by construction.
- **Subgroup effects were not tested.** Whether the discount effect differs by seat size or ticket level, and whether high discount is nonlinear, were raised as questions but not analysed.
- No tasks failed. All seven tasks reported as complete.

## Open questions

- Does the discount effect persist within seat-size and support-ticket groups, or does it differ across them (interaction terms)?
- What are the direct correlations of discount_pct with seats and with support_tickets, and do they confirm the direction of the adjustment effect?
- Is the discount effect nonlinear, for example with a threshold near 20%?
- Is the 35% renewal rate for the smallest seat group explained by its low support-ticket counts, and is the tickets effect driven by a few heavy-ticket accounts?
- Is the signup-month peak at month 9 (64.7%) a real seasonal or cohort effect, or noise over about 130 accounts per month?
- Does the contract-length effect at low discount depend on region or signup month?
- Is high discount assigned to high-ticket accounts by a support-driven policy, and does that policy confound the discount effect?
- With about 200 accounts per cell, is a larger sample needed to detect a discount-by-contract interaction of around 5 points?