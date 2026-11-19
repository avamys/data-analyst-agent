# Renewal Drivers in 1,600 Accounts: Analysis of the Binary `renewed` Target

## Summary

- **Discount, seats and support tickets are the features most clearly associated with renewal.** Renewal falls from 80% at 0% discount to 35% at 30% discount. It rises from 35% in the smallest seats quartile to 75% in the largest, and from 40% in the lowest support-tickets quartile to 82% in the highest. All three Mann-Whitney tests remain significant after Holm correction.
- **Contract length, signup month and region show no significant association with renewal.** Their Holm-adjusted p-values are 1.0. Region's Cramér's V is 0.033, which is negligible.
- **A logistic regression predicts renewal better than the majority-class baseline.** Test accuracy is 76.9% against a baseline of 57.5%, and test ROC AUC is 0.832 against 0.500. Gradient-boosted trees perform similarly on the same 320-row test split (accuracy 73.4%, ROC AUC 0.816). The two models are not reliably different on that split.
- **The discount effect does not depend detectably on contract length or region.** Neither interaction test is significant. Adjusting for seats and support tickets strengthens the discount coefficient in magnitude but does not remove it. Discount is nearly uncorrelated with seats and tickets.
- **The apparent signup-month pattern is not distinguishable from noise.** The overall chi-square test gives p=0.625, and no individual month is significant after Holm correction.

## Data

- 1,600 rows and 7 columns: five numeric features (discount_pct, seats, support_tickets, contract_months, signup_month), one categorical feature (region), and the binary target `renewed`.
- No date/time features and no identifier or free-text columns.
- Target balance: 57.5% renewed (920 of 1,600) and 42.5% not renewed.
- Missing values: none in any column.
- Distribution notes: discount_pct takes only four levels (0, 10, 20, 30), each with 400 accounts. Seats is heavily right-skewed (median 10, maximum 214). contract_months takes only the values 12 and 24.

## Findings

### Renewal rates by feature (descriptive)

Overall renewal is 57.5%. Rates by level are shown below.

- **Discount (pct):** 0% gives 80% (n=400), 10% gives 65% (n=400), 20% gives 50% (n=400), and 30% gives 35% (n=400). Renewal falls as discount rises.
- **Seats (quartiles, cut points 5, 10, 18):** ≤5 gives 35% (n=437), >5 to ≤10 gives 57% (n=410), >10 to ≤18 gives 67% (n=377), and >18 gives 75% (n=376).
- **Support tickets (quartiles, cut points 2, 3, 4):** ≤2 gives 40% (n=688), 3 gives 60% (n=362), 4 gives 72% (n=256), and >4 gives 82% (n=294).
- **Region:** east 56% (n=389), north 57% (n=406), south 57% (n=416), west 60% (n=389).
- **Contract length:** 12 months gives 57% (n=821) and 24 months gives 59% (n=779).
- **Signup month:** rates range from 53% (month 1) to 65% (month 9). Full per-month values are in the signup-month section below.

![Renewal rate by region and by discount_pct level](tasks/eda_1/charts/renewal_rate_region_discount.png)

### Which features are associated with renewal

Mann-Whitney tests compared renewed=1 with renewed=0. Holm correction was applied across the six primary tests.

- **discount_pct:** U=192,800, p=6.4e-42, Holm p≈3e-41, rank-biserial −0.38, point-biserial r −0.34. Medians are 10 for renewed accounts and 20 for non-renewed accounts.
- **seats:** U=427,846.5, p=1.9e-36, Holm p≈8e-36, rank-biserial 0.37, point-biserial r 0.24. Medians are 13 for renewed and 7 for non-renewed.
- **support_tickets:** U=440,190, p=1.3e-45, Holm p≈8e-45, rank-biserial 0.41, point-biserial r 0.35. Medians are 3 for renewed and 2 for non-renewed.
- **contract_months:** U=319,260, p=0.41, Holm p=1.0, point-biserial r 0.02. Not significant.
- **signup_month:** U=320,290.5, p=0.41, Holm p=1.0, point-biserial r 0.02. Not significant.
- **region:** chi-square(3)=1.79, p=0.617, Cramér's V=0.033 (negligible), Holm p=1.0. Not significant.

Wald 95% confidence intervals on rate differences (not Holm-adjusted):

- Discount 0% minus 30%: +0.45 (CI 0.39 to 0.51).
- Seats >18 minus ≤5: +0.40 (CI 0.33 to 0.46).
- Tickets >4 minus ≤2: +0.42 (CI 0.36 to 0.47).
- Contract 24 minus 12 months: +0.02 (CI −0.03 to 0.07). This interval spans zero.

![Renewal rate (share of accounts renewed) by discount_pct level, seats quartile and support_tickets quartile](tasks/stat_1/charts/stat1_renewal_rate_by_feature.png)

### Interactions: discount with contract length and region

- **Discount × contract_months:** not significant (logit coefficient −0.0012, Wald p=0.169; likelihood-ratio statistic 1.90, p=0.168).
- **Discount × region:** not significant (likelihood-ratio test with 3 df, LR=0.85, p=0.838).
- Renewal falls with discount at both contract lengths.
  - 12 months: 78%, 64%, 48%, 37% at 0%, 10%, 20%, 30% (n=193, 220, 206, 202).
  - 24 months: 82%, 67%, 52%, 33% at the same levels (n=207, 180, 194, 198).
  - The 24-month rate is higher than the 12-month rate at 0%, 10% and 20% discount and lower at 30%, so the direction is mixed and the gaps look like noise.
- Across regions, the renewal rate at 0% discount varies by at most 0.09 (east 74% to south 83%). At 30% discount, the spread is 0.05. No consistent regional pattern was found.
- The discount slope in the interaction model at 12 months is −0.045 log-odds per percentage point.

![Renewal rate by discount level for 12- and 24-month contracts](tasks/stat_2/charts/renewal_discount_by_contract.png)

![Renewal rate by discount level within each region](tasks/stat_2/charts/renewal_discount_by_region.png)

### Discount, seats and support tickets

- **Discount is nearly unrelated to seats and tickets.** Spearman rho is −0.026 (p=0.29) for seats and 0.016 (p=0.52) for tickets. Kruskal-Wallis p is 0.027 for seats and 0.066 for tickets, which the team describes as a weak, non-monotonic pattern rather than a trend.
- **Unadjusted discount effect:** OR 0.517 per 10 percentage points (95% CI 0.469 to 0.571, p=4e-39).
- **Adjusted for seats and support tickets:** OR 0.411 per 10 percentage points (95% CI 0.364 to 0.465). The coefficient is about 35% larger in magnitude after adjustment.
- The team judged confounding unlikely, because discount is almost uncorrelated with both seats and tickets. In its reading, the change in the coefficient reflects non-collapsibility of the logistic model rather than confounding. The discount effect is strengthened in magnitude, not reversed or removed.

![Mean discount_pct by seats bin (left) and support_tickets bin (right); counts per bin are 437/410/377/376 for seats and 688/362/256/294 for tickets](tasks/stat_3/charts/discount_by_seats_tickets.png)

### Signup month

- **Overall test:** chi-square with 11 df = 8.97, p=0.625, Cramér's V=0.075 (negligible), n=1,600. There is no evidence of an overall association.
- **Per-month binomial tests against the overall rate, Holm-corrected across 12 months:** no month is significant (all p_holm=1.0). The smallest raw p-value is 0.087, for month 9.
- **Highest month:** month 9, rate 65% (n=139, Wilson 95% CI 57% to 72%).
- **Lowest month:** month 1, rate 53% (n=129, Wilson 95% CI 45% to 62%).
- Months 3, 7, 8 and 9 have rates of 61%, 62%, 61% and 65%. The other months range from 53% to 59%. The team found this difference within the range expected by chance at this sample size.

![Renewal rate by signup month with 95% CI](tasks/stat_4/charts/stat4_renewal_by_signup_month.png)

### Predictive models

Models were evaluated on a stratified 80/20 split (random_state 42; 1,280 training rows and 320 test rows).

| Model | Test accuracy | Test ROC AUC | Test log loss |
|---|---|---|---|
| Majority-class baseline | 0.575 | 0.500 | 15.3 (not meaningful) |
| Constant prior probability | n/a | n/a | 0.682 |
| Logistic regression | 0.769 | 0.832 | 0.498 |
| Gradient-boosted trees | 0.734 | 0.816 | 0.553 |

- The majority-class baseline's log loss of 15.3 comes from hard 0/1 predictions and is not a meaningful baseline. The meaningful log-loss baseline is the constant prior of 0.682.
- **Logistic regression** bootstrap 95% intervals (1,000 test resamples): accuracy 0.722 to 0.816, ROC AUC 0.787 to 0.874, log loss 0.441 to 0.565. Its test scores are accuracy 0.769 against the baseline's 0.575, ROC AUC 0.832 against 0.500, and log loss 0.498 against the constant prior's 0.682.
- **Gradient-boosted trees** bootstrap intervals: accuracy 0.688 to 0.784, ROC AUC 0.769 to 0.861, log loss 0.465 to 0.642. Training accuracy is 0.922, so this model overfits more than logistic regression.
- **Logistic regression vs. gradient-boosted trees:** logistic regression is ahead on point estimates (accuracy +0.034, ROC AUC +0.017). The paired bootstrap intervals include zero (accuracy difference −0.009 to 0.075; AUC difference −0.013 to 0.046). Logistic regression scored higher in 93% of accuracy resamples and 85% of AUC resamples. The team advises against claiming a real advantage.
- **Logistic regression coefficients** (scaled numerics plus one-hot region, ranked by absolute coefficient): seats 1.178, support_tickets 1.108, discount_pct 1.012, then region dummies (0.07 to 0.11), signup_month 0.062 and contract_months 0.035.
- **Permutation importance** (drop in test ROC AUC, 30 shuffles, one split), which ranks features the same way in both models:
  - support_tickets: 0.159 (logistic regression), 0.158 (gradient-boosted trees).
  - discount_pct: 0.117 and 0.114.
  - seats: 0.073 and 0.082.
  - region, contract_months and signup_month: all near zero (between −0.008 and 0.002).
- The coefficient ranking places seats first, while the permutation ranking places support_tickets first. These are different measures, and the report does not resolve the difference.

![Permutation importance of each feature for both models: mean drop in test ROC AUC over 30 shuffles](tasks/ml_1/charts/ml1_permutation_importance.png)

### Missingness

- No missing values in any of the seven columns (total 0). No imputation or missingness handling was needed.

## Limitations

- **Observational data.** All results describe associations in this dataset. The findings do not establish causes, including the reason for the steep fall in renewal with discount. The team did not test whether discounts are assigned to lower-value accounts beyond the correlations reported above.
- **Single test split for model comparison.** The 320-row test set produces wide intervals. The logistic regression and gradient-boosted tree results do not separate reliably on this split. Permutation importance uses one split and 30 shuffles. The team notes that the near-zero values for region, contract length and signup month are consistent with no effect but do not prove none.
- **Confidence intervals are not corrected.** The Wald and Wilson intervals are outside the Holm-adjusted family and are reported unadjusted.
- **Non-significance is not evidence of absence.** Contract length, region and signup month were not significant at this sample size. The signup-month pattern (months 3, 7, 8, 9) was tested only within this sample, with no replication.
- **Discount-attribute association is weak but not null.** The Kruskal-Wallis tests for discount across seats (p=0.027) and tickets (p=0.066) are weak and non-monotonic. The team's reading of the coefficient change as non-collapsibility rather than confounding is an interpretation of the reported results, not a separately tested mechanism.
- **Discount has only four levels and contract_months has only two (12 and 24).** Analyses treat these as the full set of levels.
- **Seats is heavily right-skewed** (median 10, maximum 214).
- **No unresolved review issues or failed tasks** were recorded.

## Open questions

- Are the discount, seats and support-ticket effects independent of one another? The multivariable model adjusted for seats and tickets, but interaction terms for discount × seats and discount × tickets were not fitted.
- Is the signup-month pattern (months 3, 7, 8, 9) real? It needs replication in a separate sample or period, or a multivariable logistic model with signup month interacting with discount, seats or tickets. None of these has been run.
- Why does discount reduce renewal so sharply (80% to 35%)? Discount was shown to be nearly unrelated to seats and tickets. Its relationship with contract_months, region and signup_month was not tested.
- Are the near-zero permutation importances for region, contract length and signup month stable? Repeated stratified cross-validation has not been run.
- Does the logistic regression's advantage over gradient-boosted trees hold on other splits? The current evidence does not separate them.