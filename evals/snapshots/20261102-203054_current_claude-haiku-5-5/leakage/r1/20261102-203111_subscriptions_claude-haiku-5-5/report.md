# Customer Churn Analysis: 1,000 Customers, Binary Target `churned`

## Summary

- **refund_issued almost perfectly separates churn, which makes it a probable leak.** Churn is 95.9% when a refund was issued and 1.6% when not. The data has no date column, so the timing of refunds relative to cancellation cannot be checked. Every all-feature model result depends on this variable.
- **Without refund_issued, the models do not beat the majority-class baseline.** Logistic regression reaches 60.0% test accuracy and gradient boosting 56.5%, against a baseline of 63.5%. Their ROC AUCs are 0.612 and 0.539.
- **With refund_issued, the models look near-perfect.** Logistic regression reaches ROC AUC 0.991 and gradient boosting 0.975. Permutation importance attributes almost all of this to refund_issued.
- **usage_hours, tenure_months and plan are associated with churn, with smaller effects than refund_issued.** Churn is 42.8% on the basic plan versus 29.3% (plus) and 29.8% (pro). Higher usage and longer tenure are associated with lower churn in adjusted models without refund_issued. When refund_issued is added, usage_hours stays significant with a larger coefficient, while tenure_months and both plan contrasts lose significance.
- **Plan does not significantly change the effect of usage_hours or tenure_months on churn** (interaction likelihood-ratio p = 0.47).

## Data

- **Size:** 1,000 rows, 5 columns.
- **Target:** `churned`, binary. 36.3% churned (1), 63.7% not churned (0).
- **Features:** numeric `usage_hours`, `tenure_months` and `refund_issued`; categorical `plan`.
- **Date/time features:** none.
- **Identifiers or free text:** none.
- **Missing values:** none in any column.
- **Leakage warning from the profile:** refund_issued alone predicts churn at 0.975.

## Findings

### Churn rates by group

Overall churn is 36.3%. Churn rates by plan are:

- basic: 42.8% (n = 512)
- plus: 29.3% (n = 297)
- pro: 29.8% (n = 191)

Churn falls steadily across usage_hours quartiles, from 46.6% in Q1 to 21.2% in Q4. It also falls across tenure_months quartiles, from 49.8% in Q1 to 24.3% in Q4.

![Churn rate by plan level](tasks/eda_1/charts/churn_rate_by_plan.png)

![Churn rate by tenure quartile](tasks/eda_1/charts/churn_rate_by_tenure_quartile.png)

Churned customers average 17.3 usage_hours and 29.8 tenure_months. Retained customers average 21.8 usage_hours and 39.1 tenure_months. No column has missing values.

### refund_issued and possible leakage

Churn is 95.9% when refund_issued = 1 (n = 368) and 1.6% when refund_issued = 0 (n = 632). The difference is 94.3 percentage points (95% Wald CI 92.1 to 96.6). The chi-square statistic is 895.2 (p ≈ 1e-196), and Cramér's V is 0.946.

This is a leakage risk, not an established driver. The data has no date column, so it cannot show whether refunds happen before or because of cancellation.

![Share of customers churned, by plan (left) and by refund_issued (right)](tasks/stat_1/charts/churn_rate_by_plan_refund.png)

### Plan and churn

Plan is significantly associated with churn, but the effect is small: chi-square 19.03, p = 7.4e-05, Cramér's V 0.138. Each plan is compared with the pooled other plans. These comparisons overlap and are not independent pairwise tests. The Holm correction covers only these three comparisons.

- **Basic** churns 13.3 percentage points more than the other plans (95% CI 7.4 to 19.2; Holm p = 3.9e-05).
- **Plus** churns 10.0 points less (95% CI −16.3 to −3.7; Holm p = 0.0055).
- **Pro** churns 8.0 points less (95% CI −15.3 to −0.7; Holm p = 0.039).

### usage_hours and tenure_months (unadjusted)

- **usage_hours** is lower for churned customers: Welch t = −7.49, p = 1.6e-13 (Holm 4.9e-13), Cohen's d = −0.475, Mann-Whitney p = 7.1e-11. These results are not adjusted for plan or refund_issued.
- **tenure_months** is also lower for churned customers: Welch t = −7.21, p = 1.3e-12 (Holm 2.6e-12), Cohen's d = −0.473, Mann-Whitney p = 3.0e-12. These results are not adjusted for plan or refund_issued.

### Plan and the usage and tenure effects

The likelihood-ratio test of the two plan × covariate interaction terms gives LR χ² = 3.58 on 4 df, p = 0.47. The plan × usage_hours and plan × tenure_months coefficients all have 95% CIs that include zero, so their slopes do not differ detectably across plans.

Within both tenure halves and both usage halves, basic has the highest churn rate:

| Stratum | Basic | Plus | Pro |
|---|---|---|---|
| Low tenure half | 51.3% | 39.9% | 38.8% |
| High tenure half | 33.6% | 18.1% | 22.6% |
| Low usage half | 49.6% | 36.5% | 39.3% |
| High usage half | 35.5% | 22.1% | 21.6% |

![Share churned by plan within low and high tenure halves (left) and low and high usage halves (right), split at medians](tasks/stat_2/charts/churn_rate_by_plan_within_halves.png)

### Adjusted logistic models

**Without refund_issued** (adjusted for plan):
- usage_hours: OR 0.947 per hour (95% CI 0.933 to 0.962), p = 1.8e-11.
- tenure_months: OR 0.976 per month (95% CI 0.969 to 0.983), p = 7.1e-12.
- Plan (reference = basic): plus OR 0.552 (95% CI 0.401 to 0.761), p = 2.8e-04; pro OR 0.612 (95% CI 0.420 to 0.890), p = 0.010.

**With refund_issued added:**
- usage_hours remains significant at OR 0.922 per hour (95% CI 0.881 to 0.966), p = 5.9e-04. Its coefficient is about 50% larger in magnitude than without refund_issued, so the adjusted association is stronger, not weaker. This result is conditional on refund_issued being a valid control.
- tenure_months is no longer significant: OR 0.985 per month (95% CI 0.965 to 1.005), p = 0.13. Its coefficient is about 36% smaller in magnitude than without refund_issued. This attenuation is conditional on refund_issued being a valid control and cannot be read as an explanation of the tenure association.
- Both plan contrasts lose significance: plus OR 0.804 (95% CI 0.310 to 2.084), p = 0.65; pro OR 0.438 (95% CI 0.146 to 1.309), p = 0.14. Their CIs widen substantially.
- refund_issued dominates this model: OR 1,712 (95% CI 685 to 4,283), p = 4.8e-57. This is a leakage risk, not an established driver.

### Predictive models

The evaluation used a stratified 80/20 split (seed 42): 800 training rows and 200 test rows. The test churn rate is 36.5%.

**Baselines:**
- Majority-class (hard-prediction) baseline: test accuracy 63.5%.
- Prevalence-based constant-probability baseline: test log loss 0.656, using the training churn rate of 36.25%.

**All features:**

| Model | Test accuracy | F1 | ROC AUC |
|---|---|---|---|
| Logistic regression | 98.0% | 0.973 | 0.991 |
| Gradient boosting | 96.5% | 0.952 | 0.975 |

**refund_issued removed:**

| Model | Train accuracy | Test accuracy | Recall | F1 | ROC AUC |
|---|---|---|---|---|---|
| Logistic regression | 69.5% | 60.0% | 0.274 | 0.333 | 0.612 |
| Gradient boosting | 90.1% | 56.5% | 0.301 | 0.336 | 0.539 |

Neither model without refund_issued beats the majority-class baseline accuracy. Gradient boosting overfits: its train accuracy is 90.1% against a test accuracy of 56.5%.

**Permutation importance in the full gradient boosting model** (drop in test ROC AUC when shuffled):
- refund_issued: 0.505
- usage_hours: 0.005
- tenure_months: −0.006
- plan: −0.001

The logistic regression coefficients in the all-feature model are unscaled. refund_issued has coefficient 6.14, plan basic 0.285 and usage_hours 0.066.

![Test-split ROC AUC of four models; blue = all features, orange = refund_issued removed; dashed line = chance (0.5)](tasks/ml_1/charts/ml1_model_roc_auc.png)

## Limitations

- **Probable target leakage.** refund_issued predicts churn almost perfectly (95.9% vs 1.6%). The data has no date column, so refund timing relative to cancellation cannot be established. Every all-feature model result (ROC AUC 0.991 and 0.975) and every adjusted estimate that includes refund_issued depends on this. The all-feature scores should not be read as a forecast of churn.
- **Models without refund_issued show little signal.** They do not beat the majority-class baseline on the 200-row test split.
- **Unresolved review issue: log-loss baselines.** The review asked for the majority-class (hard-prediction) baseline log loss to be reported and labelled, and for 0.656 to be described as the prevalence-based constant-probability baseline rather than the only log-loss baseline. No majority-class log loss is available in the findings, so it is not reported. The 0.656 value is described only as the prevalence-based constant-probability baseline. Model log losses were not reported, so no model log loss is compared with 0.656.
- **Unresolved review issue: coefficient ranking.** The logistic regression coefficients are unscaled. Their ranking (plan basic and plus, then usage_hours) reflects feature units as well as effect size.
- **Plan comparisons overlap.** Each plan is compared with the pooled other plans, so the three comparisons are not independent. The Holm correction covers only these three.
- **Interaction result.** Non-significant interaction terms show that slopes do not differ detectably across plans. They do not establish that the slopes are equal.
- **Unadjusted tests.** The usage_hours and tenure_months tests in stat_1 are not adjusted for plan or refund_issued.
- **Small test set and overfitting.** The predictive results rest on 200 test rows. Gradient boosting overfits, and the logistic regression was not regularised.
- **Adjusted estimates depend on refund_issued.** The adjusted results with refund_issued are conditional on it being a valid control.
- **Tasks.** All four tasks (eda_1, stat_1, stat_2, ml_1) and stat_3 completed.

## Open Questions

- When does refund_issued occur relative to churn? Without a date column or an outside source, this cannot be settled, and it determines whether the all-feature ROC AUC of 0.991 is usable.
- Do the usage_hours and tenure_months effects hold when models are refit on customers with no refund, or excluding refund-driven churn?
- Are usage_hours and tenure_months correlated? This was raised but not tested.
- Do regularised or tuned models change the results without refund_issued? The current models overfit, and the logistic regression was not regularised.
- Within the basic plan, is the higher churn explained by usage_hours or tenure_months differences? The adjusted models show lower odds of churn for plus and pro versus basic when usage and tenure are controlled, but no test specific to the basic plan's churn was run.