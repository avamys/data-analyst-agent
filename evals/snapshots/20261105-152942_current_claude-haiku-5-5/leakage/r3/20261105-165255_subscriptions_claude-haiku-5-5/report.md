# Churn Analysis of a 1,000-Customer Dataset: Target `churned`

## Summary

- **Base rate and plan:** 36.3% of the 1,000 customers churned (363). Churn was highest on the basic plan (42.8%, 219 of 512), and plus (29.3%) and pro (29.8%) were similar. The plan association is statistically significant but small to moderate (chi-square p = 7.4e-5, Cramér's V = 0.138).
- **refund_issued is a likely leakage variable:** 95.9% of customers with a refund churned, against 1.6% without. Used alone it predicts churn with 97.5% accuracy. Whether a refund precedes churn is unverified, so this result cannot be treated as predictive performance.
- **Predictive performance without refund_issued is weak:** logistic regression reaches test ROC AUC 0.612 and accuracy 0.605, against a majority-class baseline of 0.635. Gradient boosting reaches ROC AUC 0.531 and accuracy 0.570, below the baseline.
- **Interaction:** plan does not significantly modify the usage_hours or tenure_months effects (LR p = 0.466). This is a low-power null.
- **Within refund_issued=1:** higher usage_hours is associated with lower churn odds (Firth OR 0.322 per 10 hours, profile CI 0.177 to 0.561). The pro contrast is unstable: its Firth profile interval excludes 1, but its bootstrap interval does not. Both rest on only 15 non-churners in this stratum, and the result is conditional on unverified refund timing.

## Data

- **Size:** 1,000 rows, 5 columns.
- **Target:** `churned` (binary). Class 0 (retained) is 63.7%; class 1 (churned) is 36.3%.
- **Features:** numeric `usage_hours`, `tenure_months`, `refund_issued`; categorical `plan`. No date/time features, and no ids or free text.
- **Missing values:** none. The profile reports zero missing values, and the EDA task confirmed zero missing entries in all five columns.
- **Leakage warning:** the profile flags `refund_issued` as possible target leakage (single-feature predictive strength 0.975).

## Findings

### Churn base rate and plan

Of 1,000 customers, 363 churned, a rate of 36.3%.

Churn by plan:

| Plan | Customers | Churned | Rate |
|---|---|---|---|
| Basic | 512 | 219 | 42.8% |
| Plus | 297 | 87 | 29.3% |
| Pro | 191 | 57 | 29.8% |

Plan is associated with churn: chi-square = 19.03 (df = 2, p = 7.4e-5), Cramér's V = 0.138, a small-to-moderate association. Basic has the highest churn.

### Usage hours and tenure

Churn rates by quartile bin (EDA):

- **usage_hours:** 46.6% in the lowest bin (1.9 to 12.5 hours), 41.1% (12.5 to 18.9), 36.1% (18.9 to 25.5), and 21.2% in the highest (25.5 to 67.7). The decline is not strictly steady, but the top quartile is the lowest.
- **tenure_months:** 49.8% in the shortest bin (up to 18 months), 41.5% (18 to 36), 29.1% (36 to 53), and 24.3% in the longest (53 to 71). The middle bins are 41.5% and 29.1%, so the pattern is generally falling.

Group differences (stat_1):

- **usage_hours:** churned customers averaged 17.30 hours, against 21.77 for retained customers (difference −4.47 hours, 95% CI −5.64 to −3.30, Welch t p = 1.6e-13; Mann-Whitney p = 7.1e-11).
- **tenure_months:** churned customers averaged 29.84 months, against 39.12 for retained customers (difference −9.27 months, 95% CI −11.80 to −6.75, Welch t p = 1.3e-12; Mann-Whitney p = 3.0e-12).

![Churn rate by plan level](tasks/eda_1/charts/churn_rate_by_plan.png)

![Churn rate by plan level: share of customers who churned, basic vs plus vs pro](tasks/stat_1/charts/churn_rate_by_plan_stat.png)

### refund_issued and possible leakage

- **Churn by refund status:** 95.9% of customers with refund_issued=1 churned (353 of 368), against 1.6% with refund_issued=0 (10 of 632). The risk difference is 0.943 (95% CI 0.921 to 0.966; z = 29.92, p ≈ 0).
- **Single-feature strength:** refund_issued alone has ROC AUC 0.974. As a rule (churned = refund_issued), it is 97.5% accurate (975 of 1,000).
- **Interpretation:** the refund rate is so extreme that a refund may follow from churning rather than precede it. Refund timing has not been verified. Until it is, refund_issued should not be used as a predictor, and its association cannot be read as predictive.

![Churn rate by refund_issued](tasks/eda_1/charts/churn_rate_by_refund.png)

### Stratified patterns (refund_issued and usage/tenure)

- **refund_issued=0 (632 customers, 10 churners):** the usage and tenure patterns cannot be tested. Each quartile bin holds 2 to 3 churners, with rates from 1.1% to 2.3%. None of the 24 plan-by-quartile bins (12 per binning) has 5 or more churners, so plan differences cannot be read within this stratum either.
- **refund_issued=1 (368 customers, 353 churners):** churn is high throughout. By usage quartile, rates are 98.3%, 100%, 96.7%, and 83.6%. By tenure quartile, rates are 97.7%, 96.2%, 94.8%, and 93.2%. The residual usage decline is concentrated in the top quartile.
- **Plan within refund_issued=1:** basic 214 of 221 churned, plus 84 of 87, pro 55 of 60. Plan differences in the overall data therefore cannot be separated from refund status here.

This stratification shows association only. The conclusion that usage and tenure patterns are mostly explained by refund_issued depends on refund being a valid pre-churn variable.

![Churn rate (share of customers churned) by usage_hours and tenure_months quartile, separately for refund_issued=0 and refund_issued=1](tasks/eda_2/charts/churn_rate_by_quartile_within_refund.png)

### Plan interactions

- **Interaction test:** adding the plan × usage_hours and plan × tenure_months terms does not significantly improve the logistic model (LR = 3.58, df = 4, p = 0.466). AIC is 1206.6 with the interaction terms and 1202.2 without. This is a low-power null, so it does not show that plan leaves the slopes unchanged.
- **Interaction odds ratios (basic as reference):** all four interaction CIs include 1. plus × usage_hours OR 1.004 (0.968 to 1.041); pro × usage_hours OR 0.972 (0.927 to 1.019); plus × tenure_months OR 0.992 (0.975 to 1.008); pro × tenure_months OR 1.006 (0.987 to 1.025).
- **Within-plan usage quartiles:** churn falls from Q1 to Q4 in every plan (basic 50.8% to 26.5%, plus 39.8% to 18.8%, pro 47.6% to 13.2%). These differences were not tested. The pro cells hold only 42 to 53 customers, and pro Q2 (31.9%) is below pro Q1 (47.6%).
- **Within-plan tenure quartiles:** churn falls from Q1 to Q4 for basic (54.9% to 29.1%), plus (44.3% to 17.3%) and pro (41.9% to 24.1%). Pro is non-monotone (21.2% in Q3, 24.1% in Q4).

### Predictive performance

Test set: one stratified 80/20 split (random_state = 42), giving 800 training and 200 test rows. Test churn rate is 36.5%.

| Model | Features | Test accuracy | Test ROC AUC |
|---|---|---|---|
| Majority-class baseline | — | 0.635 | 0.5 |
| Logistic regression | All, including refund_issued | 0.980 | 0.990 |
| Gradient boosting | All, including refund_issued | 0.965 | 0.976 |
| Logistic regression | Without refund_issued | 0.605 | 0.612 |
| Gradient boosting | Without refund_issued | 0.570 | 0.531 |

- **All-feature models:** these scores are inflated by refund_issued (largest coefficient 3.33; gradient-boosting importance 0.94). They are not a valid estimate of predictive performance while refund timing is unresolved.
- **No-refund models:** these are the only valid estimates here, and they are weak. The logistic model's accuracy (0.605) is below the 0.635 baseline. Its test precision is 0.435 and recall is 0.274. The gradient-boosting model overfits: train accuracy 0.796 against test accuracy 0.570.
- **Feature weights (no-refund logistic):** usage_hours (coefficient 0.63) and tenure_months (0.53) are the main features. Plan contributes little (plus 0.13, basic 0.13, pro 0.01). These features add little signal beyond the baseline.

![Test-set ROC AUC for logistic regression and gradient boosting on churned, with and without refund_issued, against the majority-class baseline of 0.5](tasks/ml_1/charts/ml_1_roc_auc.png)

### Within refund_issued=1: usage, tenure, and plan

This analysis uses 368 customers: 353 churners and 15 non-churners. Every estimate is conditional on refund being recorded before churn, which is unverified.

Standard logit (stat_3):

- **usage_hours:** OR 0.307 per 10 hours (95% CI 0.170 to 0.557, p = 0.0001). Higher usage goes with lower churn odds.
- **tenure_months:** OR 0.818 per 12 months (95% CI 0.588 to 1.137, p = 0.231). No clear association.
- **plus vs basic:** OR 0.773 (95% CI 0.185 to 3.234, p = 0.724).
- **pro vs basic:** OR 0.262 (95% CI 0.072 to 0.951, p = 0.042). This is indicative only, given 15 non-churners and no multiplicity adjustment.

The logit converged, but with 15 non-churners, quasi-separation is possible and the estimates are imprecise.

Firth penalized logit (stat_4), which reduces small-sample bias:

- **usage_hours:** OR 0.322 per 10 hours (Wald-type 95% CI 0.184 to 0.566; profile penalized-likelihood CI 0.177 to 0.561; p = 0.00008). Both intervals exclude 1.
- **tenure_months:** OR 0.823 per 12 months (Wald CI 0.603 to 1.123; profile CI 0.595 to 1.133; p = 0.220).
- **plus vs basic:** OR 0.726 (Wald CI 0.192 to 2.739; profile CI 0.198 to 3.150; p = 0.636).
- **pro vs basic:** OR 0.268 (Wald CI 0.079 to 0.913; profile CI 0.077 to 0.951; p = 0.035). The profile upper bound is just under 1.

Class-stratified bootstrap (stat_5, 1,000 replicates, 0 failures; standard logit refits):

- **usage_hours:** OR 0.140 to 0.512 per 10 hours (percentile 95% CI). The coefficient was negative in all 1,000 replicates. This supports the Firth result.
- **pro vs basic:** OR 0.058 to 1.137 (percentile 95% CI). This interval includes 1. The coefficient was negative in 96.5% of replicates.

**Disagreement on pro:** the Firth profile interval (upper bound 0.951) excludes 1, but the bootstrap interval (upper bound 1.137) includes it. The findings do not resolve this. The bootstrap therefore does not support the pro association as robust, and it is also a low-information estimate given 5 pro non-churners.

## Limitations

- **Refund timing is unverified (unresolved review issue).** All refund_issued results, including the 0.975 single-feature accuracy, the 97.5% rule accuracy, all all-feature model scores, and every refund_issued=1 estimate, depend on refund being recorded before churn. If refund follows churn, these results are not predictive. The lead's objection to using refund_issued stands.
- **Exact conditional logit not run (stat_5 partial).** The quasi-separation check relies on the bootstrap alone. The task is incomplete, and the pro result is unresolved.
- **Few non-churners in refund_issued=1.** There are 15 non-churners in total: 7 basic, 3 plus, 5 pro. Estimates are imprecise, quasi-separation is not ruled out, and the plus and pro intervals are wide.
- **No multiplicity adjustment.** Several terms were tested within the refund_issued=1 stratum; the pro result in particular is not adjusted.
- **Within refund_issued=0 untestable.** With 10 churners, the usage, tenure, and plan patterns cannot be tested there.
- **Small plan-by-bin cells.** Pro cells hold 42 to 54 customers per quartile, so bin-level rates are imprecise. Within-plan quartile differences were not tested.
- **Interaction test has low power.** The null result (p = 0.466) does not show that plan leaves the slopes unchanged.
- **Model scores on a small test set.** The 200-row test set gives a single split estimate, and the all-feature scores are invalid for the reasons above.
- **Missingness:** none found, confirmed by the EDA task.
- **Failed tasks:** none failed. stat_5 is partial, as stated above.

## Open questions

- Is refund_issued recorded before or after churn? This determines whether it can be used as a predictor and whether any refund_issued=1 result is predictive. It was raised by eda_1, eda_2, stat_1, stat_3, stat_4, and ml_1.
- Does an exact conditional logit on the refund_issued=1 stratum confirm the usage_hours and pro intervals? (stat_5)
- Does the pro association survive a multiplicity adjustment, and can more pro non-churners narrow its interval? (stat_4, stat_5)
- Does the plan × usage_hours interaction change once refund_issued is adjusted for, after its timing is confirmed? (stat_2)
- Is the basic-plan churn excess still present after adjusting for usage_hours, tenure_months, and refund_issued? (eda_1, stat_1)
- Does usage_hours or tenure_months predict churn at all within refund_issued=0, with more data or pooled churners? (eda_2)
- Can nonlinear terms or regularised gradient boosting improve the weak no-refund prediction (ROC AUC about 0.61)? (ml_1)