# Churn Prediction Analysis of a 1,000-Customer Dataset: Target `churned`

## Summary

- **Churn is 36.3% (363 of 1,000), and refund_issued is the dominant association, but it is probably leakage.** Churn is 95.9% with a refund and 1.6% without. Refund alone reaches test ROC AUC 0.978, so this association cannot be read as evidence of predictive value until the timing of refunds relative to the churn decision is established.
- **Without refund_issued, the signal is weak.** Logistic regression reaches test ROC AUC 0.612 and accuracy 0.605, below the 0.635 majority-class baseline accuracy. Gradient-boosted trees reach ROC AUC 0.531 and accuracy 0.57, also below the baseline, with overfitting (train accuracy 0.7963).
- **usage_hours and tenure_months are associated with lower churn, and both survive adjustment for each other and for plan when refund_issued is excluded.** Adjusted odds ratios are 0.947 per hour and 0.976 per month. When refund_issued is added, usage_hours stays significant (OR 0.922) but tenure_months does not (OR 0.985, p 0.133).
- **The plan association does not hold up once refunds are considered.** Basic churns more than plus or pro (42.8% vs 29.3% and 29.8%), but within refund strata the plan gap nearly disappears, and with refund_issued in the logit the plan ORs are not significant.

## Data

- 1,000 rows and 5 columns: numeric features `usage_hours`, `tenure_months` and `refund_issued`; categorical feature `plan`; target `churned`.
- No date/time features, and no ids or free-text columns.
- Target: 0 for 63.7% of rows and 1 for 36.3%.
- Missing values: none in any column.
- **Leakage warning:** `refund_issued` alone predicts churn at 0.975 in the data profile. Every model and test in this report is therefore given with and without it.

## Findings

### Overall churn and group rates

- Overall, 363 of 1,000 customers churned (rate 0.363).
- **Plan:** basic churned at 0.428 (219 of 512), plus at 0.293 (87 of 297) and pro at 0.298 (57 of 191). No plan, refund or quartile group has fewer than 30 rows.
- **refund_issued:** customers with a refund churned at 0.959 (353 of 368), versus 0.016 (10 of 632) without a refund.
- **usage_hours quartiles** (lowest to highest usage): churn rates 0.466, 0.411, 0.361 and 0.212.
- **tenure_months quartiles** (shortest to longest tenure): churn rates 0.498, 0.415, 0.291 and 0.243.

![Churn rate by plan and by refund_issued, with the share of customers who churned in each group](tasks/eda_1/charts/churn_rate_by_plan_and_refund.png)

### Plan and churn

- Chi-square test of plan vs churned: χ² = 19.03 (df 2), p = 7.4e-05, Cramér's V = 0.138, a small effect.
- Pairwise churn-rate differences, Holm-corrected across 9 tests in stat_1:
  - Basic minus plus: difference 0.135 (95% CI 0.068 to 0.202), Holm-adjusted p = 0.00044.
  - Basic minus pro: difference 0.129 (95% CI 0.052 to 0.207), Holm-adjusted p = 0.0045.
  - Plus minus pro: difference −0.006 (95% CI −0.089 to 0.078), Holm-adjusted p = 1.0, not significant.
- These are unadjusted for refund_issued, usage_hours or tenure_months (see the adjusted models below).

### refund_issued and churn

- Chi-square test: χ² = 895.2 (df 1), p ≈ 1e-196, Cramér's V = 0.946.
- Churn-rate difference, refund=1 minus refund=0: 0.943 (95% CI 0.921 to 0.966).
- This association may be leakage. The refund could have been issued after the decision to churn. The data do not establish the timing, so the association should not be read as causal.

### usage_hours and tenure_months

- **usage_hours:** churned customers have lower usage. Mann-Whitney U p = 7.1e-11, rank-biserial −0.248. Mean usage is 17.30 hours for churned vs 21.77 for retained, a difference of −4.47 hours (95% CI −5.64 to −3.30; Welch p = 1.6e-13; Cohen's d = −0.460). Holm-adjusted MWU p is below 0.001.
- **tenure_months:** churned customers have shorter tenure. Mann-Whitney U p = 3.0e-12, rank-biserial −0.265. Mean tenure is 29.84 months for churned vs 39.12 for retained, a difference of −9.27 months (95% CI −11.80 to −6.75; Welch p = 1.3e-12; Cohen's d = −0.472). Holm-adjusted MWU p is below 0.001.

![Churn rate by usage_hours half (median split) and refund_issued](tasks/stat_1/charts/churn_rate_usage_by_refund.png)

### Interactions

- **refund_issued × usage_hours:** logit LR = 3.89, p = 0.049 uncorrected, Holm-adjusted p = 0.146 across 9 tests. The evidence that refund changes the usage effect is weak.
  - Among refund=1 customers, churn is 0.991 in the low-usage half and 0.914 in the high-usage half.
  - Among refund=0 customers, churn is 0.018 in the low-usage half and 0.014 in the high-usage half.
- **plan × refund_issued:** LR = 1.31 (df 2), p = 0.52, Holm-adjusted p = 1.0. There is no clear evidence that refund changes the plan effect.
  - Churn with refund=0 is 0.017 for basic, 0.014 for plus and 0.015 for pro.
  - Churn with refund=1 is 0.968 for basic, 0.966 for plus and 0.917 for pro. (The stat_2 narrative describes pro as "about 0.97". The recorded value is 0.9167, and this report uses the recorded value. See Limitations.)
  - The strata show that the unadjusted plan difference is largely accounted for by how refunds are distributed across plans.

### Adjusted logit without refund_issued (stat_2)

Logit of churn on plan (vs basic), usage_hours and tenure_months, with refund_issued omitted. Holm correction across the 4 non-intercept terms:

| Term | OR | 95% CI | p | Holm p |
|---|---|---|---|---|
| plus vs basic | 0.552 | 0.401 to 0.761 | 0.00028 | 0.00057 |
| pro vs basic | 0.612 | 0.420 to 0.890 | 0.010 | 0.010 |
| usage_hours (per hour) | 0.947 | 0.933 to 0.962 | 1.8e-11 | 5.3e-11 |
| tenure_months (per month) | 0.976 | 0.969 to 0.983 | 7.1e-12 | 2.8e-11 |

- All four terms remain significant after correction.
- The plan ORs are confounded by refund distribution, because refund_issued is omitted. They should not be presented as independent plan effects.
- These are associations, not causal estimates.

### Multivariable logit with refund_issued (stat_3)

| Term | OR with refund | 95% CI | p | Holm p (5 terms) | OR without refund |
|---|---|---|---|---|---|
| plus vs basic | 0.804 | 0.310 to 2.084 | 0.654 | 0.654 | 0.552 |
| pro vs basic | 0.438 | 0.146 to 1.309 | 0.139 | 0.398 | 0.612 |
| usage_hours (per hour) | 0.922 | 0.881 to 0.966 | 0.0006 | 0.0023 | 0.947 |
| tenure_months (per month) | 0.985 | 0.965 to 1.005 | 0.133 | 0.398 | 0.976 |
| refund_issued | 1712.3 | 684.5 to 4282.9 | 4.8e-57 | 2.4e-56 | — |

- **Plan:** the plan effects are no longer significant once refund_issued is included.
- **usage_hours:** the association persists. The OR moves away from 1 (0.947 to 0.922), so it does not attenuate. The recorded log-OR shrink is −50.1%, which is consistent with the OR moving away from 1.
- **tenure_months:** the association loses significance. The OR moves toward 1 (0.976 to 0.985), and the recorded log-OR shrink is 36.5%.
- **refund_issued:** OR about 1712, which is near-separation. This is a strong sign of leakage. Because refund timing is unknown, the with-refund model cannot support causal statements about plan, usage or tenure.

![Odds ratios with 95% CIs for plan, usage_hours and tenure_months, from the logit without refund_issued (blue) and with refund_issued (red)](tasks/stat_3/charts/stat3_or_comparison.png)

### Predictive models (ml_1)

Models use a shared 80/20 stratified split (800 train, 200 test). The majority-class baseline has test accuracy 0.635, ROC AUC 0.5 and F1 0.0.

**With all features, including refund_issued:**

- Logistic regression: test accuracy 0.98, ROC AUC 0.990, F1 0.973.
- Gradient-boosted trees: test accuracy 0.965, ROC AUC 0.976, F1 0.951.
- Refund alone as a score: test ROC AUC 0.978 (train 0.973).
- Permutation importance (drop in test ROC AUC) is 0.458 for logistic regression and 0.502 for gradient boosting for refund_issued. No other feature exceeds 0.011.
- These scores are likely inflated by leakage and are not evidence of predictive value for churn.

**Without refund_issued:**

- Logistic regression: test accuracy 0.605, ROC AUC 0.612, F1 0.336. Accuracy is below the 0.635 baseline. Permutation importance: tenure_months 0.059, usage_hours 0.022, plan dummies at most 0.016.
- Gradient-boosted trees: train accuracy 0.7963 vs test accuracy 0.57, a gap of 0.23 indicating overfitting. Test ROC AUC is 0.531, near chance. **Its test accuracy of 0.57 is below the 0.635 majority-class baseline accuracy, so the model does no better than always predicting the most frequent class.** Permutation importance: tenure_months 0.013, plan_plus 0.006, usage_hours −0.032 (negative).
- These are single results on 200 test rows, so they are not precise estimates of predictive power without refund_issued.

![Test ROC AUC on the 200-row test split: majority baseline, logistic regression and gradient-boosted trees, each with all features and without refund_issued](tasks/ml_1/charts/ml1_test_roc_auc.png)

## Limitations

- **Leakage:** refund_issued may be recorded after the churn decision. Its association with churn (OR about 1712 in the with-refund model, churn 95.9% vs 1.6%) is near-separation. Nothing in the analysis establishes refund timing, so no causal conclusion is drawn about any feature.
- **Confounding through refund:** the no-refund models omit the refund pathway, so the plan and tenure coefficients are affected by it. The with-refund model makes the plan and tenure ORs unstable (wide CIs, plan ORs not significant).
- **Associations only:** all adjusted estimates are associations from observational data.
- **Small test set for ML:** the no-refund model results rest on one 200-row split. The gradient-boosted model overfits and is near chance.
- **Interaction evidence is weak:** the refund × usage interaction is not significant after correction (Holm p 0.146), and the plan × refund interaction is not significant (Holm p 1.0).
- **Unresolved review issue (stat_1):** the plan × refund_issued finding needed the stratified churn rates by refund_issued and plan. These are now reported above from stat_2's recorded `strat_refund_plan_full` values, since no separate strat_refund_plan fact was recorded for stat_1. This addresses the request, but the objection remains noted here.
- **Conflicting values (stat_2):** the stat_2 narrative gives churn with refund=1 for pro as "about 0.97", while its recorded value is 0.9167. This report uses 0.917. The discrepancy is not resolved here.
- **Unresolved review issue (ml_1):** the no-refund gradient-boosted model's test accuracy (0.57) is below the majority-class baseline accuracy (0.635). This is stated in the findings above. The overfitting statement (train 0.7963 vs test 0.57, gap 0.23) and the near-chance ROC AUC (0.531) are retained.
- **Failed tasks:** none. All four tasks (eda_1, stat_1, ml_1, stat_2, stat_3) completed.

## Open questions

- Is refund_issued leakage? Were refunds issued before or after the customer decided to churn, and can refund timing be recorded?
- Does the plan effect persist when refund_issued is included, given that the with-refund plan ORs are not significant?
- Do usage_hours and tenure_months carry more signal when modelled non-linearly or with interactions, once refund_issued is removed?
- Are the no-refund model results stable under cross-validation or repeated splits, and can the gradient-boosted model be tuned to reduce overfitting?
- Does the usage_hours association persist within refund strata, and does tenure_months lose its association because it is confounded with refunds?
- Do the usage × refund interaction and the plan × refund interaction hold on more data or under a pre-registered test?
- Is the near-separation in refund_issued a data problem that calls for a penalized or Firth logit or a stratified analysis?