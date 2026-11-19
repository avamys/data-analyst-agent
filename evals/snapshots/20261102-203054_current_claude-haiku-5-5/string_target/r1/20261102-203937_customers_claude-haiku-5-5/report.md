# Churn Analysis of 800 Customers: Predictors of churned_flag

## Summary

- **Contract type is the strongest categorical association.** Monthly contracts churned at 37.3% versus 21.2% for annual contracts, a difference of 16.2 percentage points (95% Wald CI 9.9 to 22.4). The association is significant (chi-square = 22.84, p = 1.8e-6, Cramér's V = 0.169).
- **Monthly fee and support calls are significantly associated with churn, and both survive the Bonferroni threshold.** Churned customers averaged a monthly fee of 79.94 versus 66.12 for retained customers (Cohen's d = 0.49). They averaged 1.84 support calls versus 1.34 (Cohen's d = 0.43). In the additive logistic model, each SD of monthly fee has an odds ratio of 1.67 and each additional call has an odds ratio of 1.46.
- **Region shows no significant association with churn** (chi-square = 2.66, p = 0.45, Cramér's V = 0.058). Its raw churn rates range from 27.5% to 34.5%, which the tests treat as consistent with noise.
- **No interactions were detected.** Contract does not change the effects of fee or calls (LR p = 0.83), and region does not interact with contract (LR p = 0.81). Small interactions cannot be ruled out at this sample size.
- **Churn is only weakly predictable from these four features.** The best model, logistic regression, reaches a test ROC AUC of 0.712 on 160 rows, with accuracy 0.725 against a majority-class baseline accuracy of 0.6875. The random forest does not beat the baseline on accuracy.

## Data

- **Size:** 800 rows and 5 columns.
- **Target:** `churned_flag`, binary. 250 customers churned (31.25%) and 68.8% did not. The target is imbalanced.
- **Features:** `monthly_fee` and `support_calls` (numeric); `contract` and `region` (categorical). The dataset has no date or time features and no identifier or free-text columns.
- **Missing values:** none in any column.

## Findings

### Overall churn and group rates

- Of 800 customers, 250 churned, a rate of 31.25%.
- **Contract:** monthly contracts churned at 37.3% (n = 498) and annual contracts at 21.2% (n = 302).

![Churn rate by contract type (left) and by number of support calls (right), share of customers churned](tasks/eda_1/charts/churn_by_contract_and_support_calls.png)

- **Region:** south 27.5% (n = 200), east 30.2% (n = 215), north 33.0% (n = 191), west 34.5% (n = 194). The spread is modest compared with contract.
- **Monthly fee quartiles:** churn was 17.5% in Q1, 28.5% in Q2, 34.5% in Q3 and 44.5% in Q4.
- **Support calls:** churn was 22.6% at 0 calls (n = 164), 26.4% at 1 (n = 284), 34.5% at 2 (n = 206), 39.2% at 3 (n = 97), 50% at 4 (n = 36) and 90.9% at 5 (n = 11). The rates at 6 and 7 calls each rest on one customer and are not reliable. The 4-call and 5-call rates rest on small counts and are not reliable for firm conclusions.

### Significance and effect sizes

Four tests were run, so the Bonferroni-adjusted alpha is 0.0125.

- **Contract:** significant (chi-square = 22.84, p = 1.8e-6, Cramér's V = 0.169, small to moderate). The monthly-minus-annual difference is 16.2 percentage points (95% Wald CI 9.9 to 22.4). This passes the Bonferroni threshold. The Wald interval is approximate given the group sizes.
- **Region:** not significant (chi-square = 2.66, p = 0.45, Cramér's V = 0.058, negligible). It does not pass the Bonferroni threshold.

![Churn rate by contract type (left) and by region (right), share of customers churned. Contract difference is significant (chi-square p=1.8e-6); region difference is not (p=0.45).](tasks/stat_1/charts/stat_churn_rate_contract_region.png)

- **Monthly fee:** Mann-Whitney p = 4.4e-10, Cohen's d = 0.49 (medium). Mean fee is 79.94 for churned and 66.12 for retained customers. Medians are 82.92 and 63.35. This passes the Bonferroni threshold.
- **Support calls:** Mann-Whitney p = 8.5e-7, Cohen's d = 0.43 (small to medium). Mean calls are 1.84 for churned and 1.34 for retained customers. Medians are 2.0 and 1.0. This passes the Bonferroni threshold.

### Pooled support-call bins

Pooling calls into 0, 1, 2 and 3+ gives bins of at least 30 customers each. The counts sum to 800.

| Support calls | Customers | Churned | Churn rate |
|---|---|---|---|
| 0 | 164 | 37 | 22.6% |
| 1 | 284 | 75 | 26.4% |
| 2 | 206 | 71 | 34.5% |
| 3+ | 146 | 67 | 45.9% |

![Churn rate per pooled support_calls bin (0, 1, 2, 3+)](tasks/eda_2/charts/churn_by_pooled_support_calls.png)

No formal significance test on the pooled bins was reported.

### Interactions

- **Contract with fee and calls:** adding both interactions to the additive model gives LR = 0.37 on 2 df, p = 0.83. Contract does not change the effect of fee or calls.
- **Contract with region:** adding the interaction gives LR = 0.98 on 3 df, p = 0.81. Region does not interact with contract.
- **Full interaction model:** contract with fee, calls and region, plus fee × calls, gives LR = 4.99 on 6 df, p = 0.54. It is not better than the additive model.
- **Interaction odds ratios (full model):** contract × fee 1.10 (0.77 to 1.59), contract × calls 1.11 (0.82 to 1.49), fee × calls 1.16 (0.99 to 1.35). All intervals include 1.
- **Contract × region odds ratios (full model):** north 0.68 (0.26 to 1.76), south 0.69 (0.25 to 1.91), west 0.61 (0.23 to 1.62). All intervals include 1.
- **Additive model main effects:** monthly vs annual contract OR 2.39 (1.68 to 3.38). Each SD of monthly fee OR 1.67 (1.42 to 1.97). Each additional support call OR 1.46 (1.28 to 1.67). Region main effects are not significant: north 1.12, south 0.77 and west 1.08 versus east, all with intervals including 1.

Churn rates within contract and fee quartile were: annual Q1 8.5% (n = 82), Q2 28.2% (n = 71), Q3 19.7% (n = 76), Q4 30.1% (n = 73); monthly Q1 23.7% (n = 118), Q2 28.7% (n = 129), Q3 43.5% (n = 124), Q4 52.8% (n = 127).

Within contract and call group, churn was: annual 0 calls 17.2% (n = 58), 1 call 14.2% (n = 106), 2 calls 25.0% (n = 80), 3+ calls 32.8% (n = 58); monthly 0 calls 25.5% (n = 106), 1 call 33.7% (n = 178), 2 calls 40.5% (n = 126), 3+ calls 54.5% (n = 88).

The two sets of descriptive rates read differently. The fee-quartile rates suggest monthly churn rises more steeply across fee quartiles, and the call-group rates suggest monthly churn is higher at every call level. The interaction tests do not support a real difference. The next section reports a borderline result for the fee-by-contract pattern.

![Churn rate by monthly_fee quartile, split by contract type](tasks/stat_2/charts/stat2_churn_fee_by_contract.png)

### Non-linearity and fee slope by contract

- **Linear fee term:** adding a quadratic fee term gives LR = 0.72 on 1 df, p = 0.40. Adding quadratic and cubic terms gives LR = 0.78 on 2 df, p = 0.68. The quadratic odds ratio per SD² is 0.92 (0.76 to 1.11). The linear logit assumption holds for fee in the additive model.
- **Curvature by contract:** adding contract-specific quadratic terms gives LR = 1.59 on 2 df, p = 0.45. This is absence of evidence at n = 800, not proof of linearity within each contract.
- **Fee slope by contract:** LR = 0.11 on 1 df, p = 0.74. The annual slope is OR 1.60 per SD (1.18 to 2.16) and the monthly slope is OR 1.70 per SD (1.40 to 2.07).
- **Fee quartile by contract:** LR = 7.44 on 3 df, p = 0.059. This is borderline and not conclusive.
- **Fee quartile odds ratios (additive model, versus Q1):** Q2 1.90 (1.16 to 3.12), Q3 2.58 (1.60 to 4.18), Q4 3.88 (2.41 to 6.24). These are consistent with the linear per-SD estimate.

The fee-by-contract pattern therefore has two readings. The slope test finds no contract difference, while the borderline quartile-by-contract test (p = 0.059) is not conclusive either way. Neither result establishes a contract difference in the fee pattern.

### Predictive models

The evaluation used a stratified 20% test set (160 rows, 50 churned), seed 42. Models were trained on 640 rows.

| Model | Test ROC AUC | Accuracy | Balanced accuracy | Yes-class F1 |
|---|---|---|---|---|
| Majority-class baseline | – | 0.6875 | 0.500 | – |
| Logistic regression | 0.712 | 0.725 | 0.615 | 0.421 (precision 0.615, recall 0.32) |
| Random forest | 0.616 | 0.619 | 0.548 | 0.371 |

- Logistic regression beats the baseline on accuracy and ranking. Its training accuracy is 0.728.
- The random forest is below the baseline accuracy (0.619 versus 0.6875). It overfits strongly, with training accuracy 1.0.
- Permutation importance for logistic regression (drop in test ROC AUC): monthly_fee 0.091, support_calls 0.071, contract 0.027, region 0.006.
- Permutation importance for the forest: support_calls 0.065, monthly_fee 0.041, contract 0.038, region −0.017.

The two models agree that monthly fee and support calls are the main drivers, and both rank contract third. They differ in the order of the top two: logistic regression ranks monthly_fee first, while the forest ranks support_calls first. Both assign region little or no importance.

![Test ROC AUC and balanced accuracy of logistic regression and random forest vs majority-class baseline (160 test rows)](tasks/ml_1/charts/ml1_model_comparison.png)

## Limitations

- **Sample size and imbalance.** The dataset has 800 rows with 31.25% churn. The interaction and non-linearity tests have limited power. The analysis cannot rule out small interactions or small departures from linearity.
- **Sparse high-call tail.** The 4-call group has 36 customers, the 5-call group has 11, and the 6-call and 7-call groups have one each. Rates at these levels are not reliable. The pooled 3+ bin (146 customers) mixes several call levels and was not tested for significance.
- **Model evaluation.** The test set has 160 rows and 50 churned customers, so the ROC AUC estimates are noisy. No cross-validation interval was produced.
- **Approximate interval.** The contract difference CI is a Wald interval, which is approximate at these group sizes.
- **Multiple comparisons.** The Bonferroni adjustment covers only the four significance tests in stat_1.
- **Non-nested comparison.** The linear-versus-quartile likelihood-ratio statistic is not valid because the models are not nested, so it is not used as evidence.
- **Borderline and conflicting signals.** The quartile-by-contract interaction (p = 0.059) is not conclusive. The descriptive fee and call-group rates suggest steeper monthly patterns, while the formal interaction tests do not support a difference.
- **Associations only.** All results describe associations in this sample. They are not causal estimates.
- **Failed tasks and unresolved review issues.** None were recorded.

## Open questions

- Is the high churn at 4 or more support calls a real effect? The pooled 3+ bin was not tested. Would splitting it into 3, 4–5 and 6+ keep each bin at 30 or more customers?
- Does the monthly-contract fee slope differ from the annual slope with more data? The contract-by-fee interval is wide (0.77 to 1.59), and the quartile-by-contract result (p = 0.059) is inconclusive.
- Is support_calls linear on the logit scale? Only monthly_fee was tested for non-linearity.
- Does a natural cubic spline for monthly_fee with quartile knots improve on the linear term? Only quadratic and cubic terms were tested.
- Would a tuned or gradient-boosted model, or a cross-validated comparison, improve on the logistic regression ROC AUC of 0.71?
- Is there a monthly-fee threshold within each contract type?