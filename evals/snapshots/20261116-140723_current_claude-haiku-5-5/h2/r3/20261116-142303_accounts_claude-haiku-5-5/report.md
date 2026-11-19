# Renewal in a 1,600-Account Dataset: Drivers, Interactions and Predictive Performance

## Summary

- **Seats, support tickets and discount are the features most clearly associated with renewal.** Each keeps a significant association after Holm correction and after adjustment for the other two. In the adjusted model, the discount odds ratio is 0.915 per percentage point, the ticket odds ratio is 1.896 per ticket and the seats odds ratio is 1.074 per seat.
- **Renewal falls steadily with discount.** The renewal rate is 80% at 0% discount and 35% at 30% discount (400 accounts per level). Renewal rises with support tickets, from 18.8% at 0 tickets to 74.4% at 5 tickets.
- **Region, contract length and signup month show no significant association with renewal** after Holm correction (adjusted p = 1.0 for each). The signup-month spread (53.5% to 64.7%) is within what the group sizes of about 125 to 141 accounts can produce.
- **A logistic regression reaches 77.3% test accuracy against the 57.5% majority-class baseline** (ROC AUC 0.834). A random forest reaches 75.0% (ROC AUC 0.832). Both rank seats, support tickets and discount as the top three features.
- **Neither tested interaction is significant.** Discount by contract length (LR p = 0.21) and seats by region (LR p = 0.27) show no evidence of effect modification. Linear log-odds coding of support tickets is adequate (LR p = 0.74).

## Data

- **Size:** 1,600 rows and 7 columns.
- **Target:** `renewed`, a binary variable. 920 accounts renewed (57.5%) and 680 did not (42.5%). The 57.5% positive rate is the majority-class baseline for accuracy.
- **Features:** numeric `discount_pct`, `seats`, `support_tickets`, `contract_months` and `signup_month`; categorical `region` (east, north, south, west).
- **Missing values:** none in any column. No rows were dropped or imputed.
- **Date/time and id/text columns:** none. No feature was excluded.

## Findings

### Descriptive renewal rates

Renewal rates by feature value (from EDA):

- **Region:** east 55.5% (n=389), north 57.4% (n=406), south 57.0% (n=416), west 60.2% (n=389).
- **Discount_pct:** 0% 80% (n=400), 10% 65% (n=400), 20% 50% (n=400), 30% 35% (n=400).
- **Support_tickets:** 0 tickets 18.8% (n=69), 1 36.4% (n=264), 2 47.6% (n=355), 3 59.9% (n=362), 4 71.9% (n=256), 5 74.4% (n=156), 6 89.3% (n=75), 7 86.8% (n=38), 8 100% (n=20), 9 100% (n=4), 10 100% (n=1). The 7-or-more groups total 63 accounts and are small.
- **Contract_months:** 12 months 56.5% (n=821), 24 months 58.5% (n=779).
- **Signup_month:** Jan 53.5% (n=129), Feb 55.0% (n=140), Mar 61.4% (n=127), Apr 55.3% (n=141), May 55.0% (n=129), Jun 53.9% (n=141), Jul 62.3% (n=130), Aug 60.8% (n=130), Sep 64.7% (n=139), Oct 55.2% (n=134), Nov 54.4% (n=125), Dec 58.5% (n=135).
- **Seats:** renewed accounts have a mean of 17.57 seats (median 13, IQR 7 to 21). Non-renewed accounts have a mean of 9.95 (median 7, IQR 4 to 13).

![Share of accounts renewed (renewal rate) for each value of region, discount_pct, support_tickets, contract_months and signup_month](tasks/eda_1/charts/renewal_rate_by_feature.png)

The signup-month rates do not establish September as a peak. The top months (Sep, Jul, Mar, Aug) are close together, and the group sizes are small.

### Significance tests and effect sizes (stat_1)

Holm correction was applied across 10 tests (one chi-square and one logistic regression per feature).

| Feature | Chi-square (df) | p | Cramér's V | Logistic OR per unit (95% CI) | Holm-adjusted p |
|---|---|---|---|---|---|
| Discount_pct | 184.1 (3) | 1.1e-39 | 0.339 | 0.936 per point (0.927 to 0.946) | 1.0e-38 |
| Support_tickets | 208.3 (10) | 3.0e-39 | 0.361 | 1.633 per ticket (1.519 to 1.756) | 2.4e-38 |
| Seats | 148.9 on quartile bins (3) | 4.7e-32 | 0.305 | 1.055 per seat (1.044 to 1.067) | 1.8e-20 |
| Region | 1.79 (3) | 0.617 | 0.033 | n/a | 1.0 |
| Contract_months | 0.67 (1) | 0.414 | 0.020 | 1.007 per month (0.990 to 1.024) | 1.0 |
| Signup_month | 8.97 (11) | 0.625 | 0.075 | 1.012 per month (0.983 to 1.042) | 1.0 |

- **Discount and tickets** have moderate association strength (Cramér's V of 0.34 and 0.36).
- **Seats** shows moderate association in the quartile check (V = 0.305). The quartile renewal rates are 35.0% (1 to 5 seats, n=437), 57.3% (6 to 10, n=410), 66.6% (11 to 18, n=377) and 74.7% (19 to 214, n=376).
- **Region, contract_months and signup_month** show no significant association and negligible effect sizes.

![Odds ratios of renewal per unit increase with 95% CI, one logistic regression per feature](tasks/stat_1/charts/stat1_odds_ratios.png)

### Adjusted multivariable model (stat_3)

A single logistic model of renewal on discount_pct, support_tickets and seats (n=1,600) keeps all three associations:

- **Discount_pct:** OR 0.915 per point (95% CI 0.904 to 0.926), p = 4.4e-46, Holm p = 8.8e-46.
- **Support_tickets:** OR 1.896 per ticket (95% CI 1.741 to 2.066), p = 9.8e-49, Holm p = 3.0e-48.
- **Seats:** OR 1.074 per seat (95% CI 1.060 to 1.089), p = 6.9e-25, Holm p = 6.9e-25.

These adjusted ORs are in the same direction as the unadjusted ORs (0.936, 1.633 and 1.055). Each is slightly larger in magnitude after adjustment.

### Interactions (stat_2)

- **Discount by contract length:** the interaction coefficient is −0.015 per point (95% CI −0.038 to 0.008), Wald p = 0.21, and the likelihood-ratio test gives χ² = 1.57 on 1 df, p = 0.21. Renewal falls with discount in both contract lengths:

  | Discount | 0% | 10% | 20% | 30% |
  |---|---|---|---|---|
  | 12 months | 77.7% | 63.6% | 48.1% | 37.1% |
  | 24 months | 82.1% | 66.7% | 52.1% | 32.8% |

  Cells contain 180 to 220 accounts.

- **Seats by region:** the likelihood-ratio test gives χ² = 3.88 on 3 df, p = 0.27. The west term alone has coefficient 0.037 and p = 0.05, which does not survive the joint test. Within every region, renewal rises with seats:

  | Region | 0–5 seats | 18+ seats |
  |---|---|---|
  | East | 29.8% (n=94) | 69.7% (n=99) |
  | North | 33.0% (n=109) | 78.1% (n=96) |
  | South | 38.3% (n=120) | 74.4% (n=86) |
  | West | 37.7% (n=114) | 76.8% (n=95) |

  Cells contain 80 to 120 accounts.

Neither interaction is reported as a finding. The apparent slope differences are within the noise the group sizes allow.

![Renewal rate by discount_pct, separately for 12 and 24 month contracts](tasks/stat_2/charts/stat2_discount_by_contract.png)

### Linearity of the support-tickets effect (stat_4)

- A likelihood-ratio test of categorical against linear coding of tickets (0 to 6, plus 7 or more pooled) gives LR = 3.51 on 6 df, p = 0.74, adjusted for discount and seats. Linear coding is adequate on this test.
- The linear adjusted OR is 1.896 per ticket (95% CI 1.741 to 2.066). Refitting without the 7-or-more group (n=1,537) gives 1.882 (95% CI 1.718 to 2.063).
- Categorical adjusted ORs against 0 tickets rise from 2.818 at 1 ticket to 100.4 at 6 tickets and 168.5 at 7 or more (95% CI 51.3 to 552.8, n=63).
- For the 7-or-more group, mean predicted renewal from the linear model is 0.915 and observed renewal is 0.921. This check does not test the fit at individual high counts. Seven tickets renew at 86.8% (n=38), and 8 to 10 tickets renew at 100% (25 accounts in total).

![Renewal rate per support ticket group, n shown in table](tasks/stat_4/charts/stat4_ticket_rates.png)

### Predictive models (ml_1)

Test-set results against the majority-class baseline of 57.5% (n_train=1,200, n_test=400):

| Model | Train accuracy | Test accuracy | Precision | Recall | F1 | ROC AUC |
|---|---|---|---|---|---|---|
| Logistic regression | 0.766 | 0.773 | 0.781 | 0.839 | 0.809 | 0.834 |
| Random forest (300 trees, min leaf 5) | 0.847 | 0.750 | 0.760 | 0.826 | 0.792 | 0.832 |

- Both models beat the baseline. Logistic regression is higher on every test metric, though the margins are small.
- Feature ranking agrees across models. Logistic standardized coefficients are seats +1.179, support_tickets +1.081, discount_pct −1.012 and signup_month +0.069. Forest importances are seats 0.311, support_tickets 0.268, discount_pct 0.246 and signup_month 0.089. Contract_months has importance 0.026 in the forest, and region dummies have importance of about 0.015 each.
- The random forest's train accuracy (0.847) is well above its test accuracy (0.750). Logistic regression's train and test accuracies are close.

![Random forest impurity importance for the top 6 features predicting renewed](tasks/ml_1/charts/ml1_rf_feature_importance.png)

### Missingness (eda_2)

No column has missing values, and no rows have any. A missingness-versus-target analysis is not applicable.

## Limitations

- **Observational associations only.** All results describe association with renewal in this dataset. No result establishes cause.
- **Sparse high-ticket groups.** The groups of 7 or more tickets are small (38, 20, 4 and 1 accounts). Their rates are imprecise, and the linear fit at 8 to 10 tickets is not tested. The 8-to-10 group (25 accounts) has a 100% renewal rate, which is not tested with an exact or Firth method.
- **Small groups for interactions.** Interaction cells hold 80 to 220 accounts, which gives low power. A non-significant result does not show that no interaction exists.
- **Signup-month spread not formally tested at the individual-month level.** The 12-month chi-square (p = 0.625) and logistic result (p = 0.41) support the noise reading, but no per-month p-values are reported.
- **Holm table.** The correction table lists both raw and log-transformed versions of several features. The "10 tests" are therefore not all distinct features. Holm-adjusted values are reported as recorded.
- **Model evaluation.** Model scores come from a single 1,200/400 train-test split. No cross-validation is reported, so the test scores carry split-to-split uncertainty. The logistic model's margin over the forest is small.
- **Unresolved review issue (stat_2): resolved.** The lead's review asked for the stat_2 figures to be checked against the full records. The 24-month, 30%-discount renewal rate is 0.328 in the full record, and every north, west and south seat-bin rate and n matches the record. The figures in this report are the confirmed values.
- **Failed tasks:** none.

## Open questions

- Is the signup-month spread (53.5% to 64.7%) noise? A per-month test with individual p-values would settle it.
- Is the seats effect linear on the log-odds scale? The quartile rates (35.0% to 74.7%) suggest checking a spline or categorical seats term. This is not tested.
- Does the support-tickets effect differ by discount level? The discount-by-tickets interaction is not tested.
- Do the 8-to-10-ticket groups (25 accounts, all renewed) need an exact or Firth test?
- Do discount_pct, support_tickets and seats hold their effects in a model that includes the region and contract terms? stat_3 adjusts only for the other two of the three main features.