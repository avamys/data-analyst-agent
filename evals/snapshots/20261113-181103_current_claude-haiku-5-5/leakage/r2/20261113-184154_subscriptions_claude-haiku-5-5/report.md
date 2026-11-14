# Churn Analysis of 1,000 Customers: Predicting `churned`

## Summary

- **Churn is 36.3% overall (363 of 1,000), and plan is associated with it, but weakly.** Basic-plan customers churn at 42.8%, versus 29.3% on plus and 29.8% on pro (chi-square p = 7.4e-05, Cramér's V = 0.138). After adjusting for usage_hours, tenure_months and refund_issued, plan is not significant (LR p = 0.34). The two results disagree, and the adjusted result depends on refund_issued, which is under a leakage warning.
- **Usage and tenure are associated with churn at small-to-moderate effect sizes.** Churned customers have median usage of 16.2 hours versus 20.5 for retained customers, and median tenure of 26 versus 41 months. Churn falls steadily across usage and tenure quartiles, from 46.6% to 21.2% for usage and from 49.8% to 24.3% for tenure.
- **refund_issued is almost deterministic for churn, and the leakage question is unresolved.** Churn is 95.9% when refund_issued = 1 and 1.6% when it is 0. With all features, models reach test ROC AUC 0.981–0.990 against a majority-class accuracy baseline of 0.635. Without refund_issued, the models fall to ROC AUC 0.529–0.612, and the logistic regression's accuracy (0.605) is below the baseline. No check established when refund_issued is recorded.
- **The refund_issued × usage_hours interaction is nominal and not established.** The Firth Wald test gives p = 0.028, but the unpenalized test gives p = 0.051, and the earlier p = 0.049 result was unstable. Plan does not modify the usage or tenure associations (plan interaction p = 0.56 and 0.70).

## Data

- **Size:** 1,000 rows × 5 columns.
- **Target:** `churned` (binary). Class 0 is 63.7% (637 rows); class 1 is 36.3% (363 rows).
- **Features:** `usage_hours`, `tenure_months` and `refund_issued` (numeric); `plan` (categorical, levels basic, plus, pro).
- **Missing values:** none in any column.
- **Excluded:** no date/time features and no identifier or free-text columns.
- **Profile warning:** `refund_issued` alone predicts `churned` at 0.975, flagged as possible target leakage.

## Findings

### 1. Churn rates by group

**Plan.** Basic customers churn at 42.8% (n = 512), plus at 29.3% (n = 297) and pro at 29.8% (n = 191).

![Churn rate by plan level](tasks/eda_1/charts/churn_rate_by_plan.png)

**refund_issued.** Customers with refund_issued = 0 churn at 1.6% (n = 632). Customers with refund_issued = 1 churn at 95.9% (n = 368). This split is the basis of the leakage concern in Section 5.

**usage_hours quartiles.** Churn is 46.6% in Q1 (n = 253), 41.1% in Q2 (n = 248), 36.1% in Q3 (n = 249) and 21.2% in Q4 (n = 250).

**tenure_months quartiles.** Churn is 49.8% in Q1 (n = 257), 41.5% in Q2 (n = 246), 29.1% in Q3 (n = 258) and 24.3% in Q4 (n = 239).

![Histograms of numeric features split by churned (counts of customers)](tasks/eda_1/charts/histograms_by_churned.png)

### 2. Significance and effect sizes

**Plan.** Chi-square = 19.03 (df = 2), p = 7.4e-05, Cramér's V = 0.138 (small effect), n = 1,000.

![Churn rate by plan level, proportion of customers churned](tasks/stat_1/charts/stat1_churn_rate_by_plan.png)

**refund_issued.** Fisher exact p = 5.3e-236. Odds ratio = 1463.8 (Woolf 95% CI 650.7 to 3292.9). The finding states this is too strong to trust as a predictor until the leakage check is done.

**usage_hours.** Mann-Whitney p = 7.1e-11, rank-biserial r = -0.248 (small-to-moderate). Median usage is 16.2 hours for churned versus 20.5 for retained, a difference of -4.3 hours (bootstrap 95% CI -5.5 to -2.6).

**tenure_months.** Mann-Whitney p = 3.0e-12, rank-biserial r = -0.265 (small-to-moderate). Median tenure is 26 months for churned versus 41 for retained, a difference of -15 months (bootstrap 95% CI -19 to -11).

### 3. Interactions

- **Plan × usage_hours:** LR = 1.17 (df = 2), p = 0.56. Plan does not change the usage association.
- **Plan × tenure_months:** LR = 0.70 (df = 2), p = 0.70. Plan does not change the tenure association.
- **refund_issued × tenure_months:** LR = 0.15 (df = 1), p = 0.70. Refund does not change the tenure association.
- **refund_issued × usage_hours:** LR = 3.89 (df = 1), p = 0.049. This is borderline and was found to be unstable (see below).

Within-stratum slopes from the logistic models (stat_2):
- refund_issued = 0: coefficient -0.022, p = 0.52, n = 632.
- refund_issued = 1: coefficient -0.112, p = 0.0001, n = 368.

Churn rates split by refund_issued and usage_hours at the median of 18.9 hours:

| refund_issued | usage_hours | Churn rate | n |
|---|---|---|---|
| 0 | low | 1.8% | 284 |
| 0 | high | 1.4% | 348 |
| 1 | low | 99.1% | 217 |
| 1 | high | 91.4% | 151 |

stat_2 cautions that refund = 1 rates sit near the ceiling, so these strata describe near-separated data and do not establish a usage modifier. The L2-penalized fit (C = 1) gives an interaction coefficient of -0.66 on standardized usage_hours, with no p-value.

**Firth re-analysis (stat_4).** The team refit the near-separated strata with Firth penalization, on a per-standard-deviation scale (SD = 9.95 hours):

- **refund_issued = 0** (n = 632, 10 churned): the Firth coefficient is -0.0168 per hour (SE 0.0314), Wald p = 0.59. On the SD scale, the penalized LR gives chi-square = 2.73, p = 0.098. The hour-scale result (chi-square = 7.33, p = 0.0068) is withdrawn because it is inflated by a scale artifact. The stratum shows no significant usage association.
- **refund_issued = 1** (n = 368, 353 churned): the Firth coefficient is -0.110 per hour (SE 0.028), Wald p < 0.001. On the SD scale, the coefficient is -1.089 (SE 0.279), penalized LR chi-square = 18.06, p = 2e-5. stat_4 notes the magnitude is imprecise because of near-separation.
- **Interaction, full sample (n = 1,000):** Firth Wald z = -2.20, p = 0.028 (SD-scale coefficient -0.922, SE 0.419). SD-scale Firth LR chi-square = 5.63, p = 0.018. The unpenalized MLE LR gives chi-square = 3.81, p = 0.051. The hour-scale Firth result (p = 0.0014) is inflated by the same artifact and should not be cited.

stat_4 concludes the interaction is at most as strong as stat_2's p = 0.049 and is not a validated modifier effect while the leakage question is open.

![Share of customers churned in each usage_hours quintile, shown separately for refund_issued=0 and refund_issued=1](tasks/stat_4/charts/churn_rate_usage_by_refund.png)

### 4. Plan after adjustment

Adjusting for usage_hours, tenure_months and refund_issued, a likelihood-ratio test gives chi-square = 2.15 (df = 2), p = 0.34 (n = 1,000). Plan is not significantly associated with churn after this adjustment.

Adjusted odds ratios against basic:
- Plus: OR = 0.80 (95% CI 0.31 to 2.08), p = 0.65.
- Pro: OR = 0.44 (95% CI 0.15 to 1.31), p = 0.14.

Both confidence intervals include 1. The adjusted estimates include refund_issued, so these conclusions are conditional on that adjustment. stat_3 makes no claim about whether usage, tenure or refund_issued differ by plan.

**Disagreement:** the unadjusted test (Section 2, significant) and the adjusted test (this section, not significant) disagree. This report does not resolve the disagreement.

### 5. Predictive performance and the refund_issued leakage check

**Setup.** Stratified 80/20 split (800 train, 200 test, random_state = 42). Majority-class baseline accuracy on the test set is 0.635 (predicting churned = 0). Candidate features: usage_hours, tenure_months, plan (one-hot) and refund_issued.

**Test-set scores, all features:**

| Model | ROC AUC | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|---|
| Logistic regression | 0.990 | 0.980 | 0.973 | 0.973 | 0.973 |
| Gradient boosted trees | 0.981 | 0.965 | 0.971 | 0.932 | 0.951 |

![Test-set ROC AUC and accuracy of logistic regression and gradient boosted trees, with and without refund_issued, against the majority-class baseline accuracy (0.635) on the same test set](tasks/ml_1/charts/ml1_model_comparison.png)

In the logistic regression, refund_issued has the largest absolute coefficient (3.331), followed by usage_hours (0.729). In the gradient boosted model, refund_issued has importance 0.936 and usage_hours 0.044.

**Test-set scores, refund_issued removed:**
- Logistic regression: ROC AUC 0.612, accuracy 0.605, precision 0.435, recall 0.274. Its accuracy is **below** the 0.635 majority-class baseline, so it does no better than always predicting churned = 0.
- Gradient boosted trees: ROC AUC 0.529, accuracy 0.560, which is below the 0.635 baseline. Train accuracy is 0.8, so this model overfits, and its test scores are unreliable.

Test ROC AUC falls from 0.990 to 0.612 for logistic regression and from 0.981 to 0.529 for gradient boosted trees when refund_issued is removed.

**Permutation importance (test-set ROC AUC drop, 20 repeats).**

All-features gradient boosted model:
- refund_issued: 0.511 (sd 0.041).
- usage_hours: 0.011 (sd 0.005).
- tenure_months: -0.002 (sd 0.005).
- plan_pro: 0.0011 (sd 0.0021).
- plan_plus: -0.0009 (sd 0.0005).

Refund-free gradient boosted model:
- usage_hours: -0.033 (sd 0.033).
- tenure_months: 0.019 (sd 0.031).
- plan_pro: 0.0075 (sd 0.0063), from the refund-free plan importance record.
- plan_plus: 0.003 (sd 0.010).

All refund-free values are small relative to their spread on 200 test rows, so they are not clearly meaningful.

**Leakage verdict from ml_2.** The finding states that refund_issued should be excluded from any deployed churn model unless it is shown to be recorded before churn. Its permutation importance accounts for almost all of the all-features model's AUC, and the pattern fits a post-churn or leaked field. No task established when refund_issued is recorded, so the leakage question remains open.

## Limitations

- **refund_issued leakage is unresolved.** The profile warns of target leakage (single-feature predictive value 0.975). No task checked whether refund_issued is recorded before churn. All all-features model scores (AUC 0.981–0.990, accuracy 0.965–0.980) depend on this feature and are not valid predictive results until the check is done. The stat_1, stat_3 and stat_4 conclusions that involve refund_issued are conditional on it.
- **Refund-free model performance is weak and partly unreliable.** The refund-free logistic regression has test accuracy 0.605, below the 0.635 baseline, and ROC AUC 0.612. The refund-free gradient boosted model overfits (train 0.8, test 0.56). The test set cannot show what usage_hours, tenure_months and plan predict once refund_issued is removed.
- **Review issue 3 (ml_2) is open.** The refund_issued × usage_hours interaction is borderline (p = 0.049 in stat_2) and unstable. The claim that usage_hours may carry signal within refund groups therefore rests on stat_4, whose results are themselves limited: the interaction is nominal (Firth Wald p = 0.028; unpenalized MLE p = 0.051), and the refund = 1 magnitude is imprecise because of near-separation.
- **Thin churn events in the refund = 0 stratum.** Only 10 churn events occur among 632 refund = 0 customers. The stat_2 unpenalized slope is unstable, and stat_4 prefers the Firth estimate. Two stat_4 penalized refits (refund = 0 stratum and the interaction block, hour scale) were flagged as not converged. The SD-scale results reported above are the ones stat_4 relies on.
- **Adjusted plan results depend on refund_issued.** The non-significant plan adjustment (Section 4) includes refund_issued, which is under the leakage warning.
- **Unadjusted and adjusted plan results disagree.** Section 2 finds plan significant; Section 4 finds it not significant after adjustment. This is reported, not resolved.
- **Bootstrap interval reported with two values.** The usage_hours bootstrap upper limit of the median difference appears as -2.5 in one record and -2.6 in another. This report uses -2.6, the value given in the findings text and the median-difference record.
- **Small test set.** The predictive results use 200 test rows, and the permutation importance values have wide spreads relative to their means.
- **Partial task.** stat_2 has status "partial". Its plan-interaction results are complete, but the refund × usage_hours result is unresolved (see above). No plan-stratified churn rates are reported because no plan interaction was significant.
- **Not tested:** whether usage_hours, tenure_months or refund_issued differ by plan, which could confound the plan association. The interaction was not re-tested after adjusting for tenure_months and plan.

## Open questions

- Is refund_issued recorded before or after churn, and can it be known at prediction time? Is it a consequence of churn rather than a cause?
- Why do 353 of 368 refund_issued = 1 customers churn?
- Once the refund_issued question is resolved, does the plan effect hold? Refit the plan model with and without refund_issued and compare the adjusted pro and plus odds ratios.
- Do usage_hours and tenure_months carry signal within refund_issued groups once that feature is controlled for? Does a regularised or shallower refund-free model change the test AUC?
- Do usage_hours and tenure_months interact in their effect on churn within the refund_issued = 0 group? Does the refund × usage interaction survive adjustment for tenure_months and plan?
- Does the usage_hours effect on churn differ by plan within refund_issued = 0 customers only?
- Do usage_hours, tenure_months or refund_issued differ by plan, and do they confound the plan association?