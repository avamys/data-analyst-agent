# Churn Prediction for the `churned` Target: 1,000 Customers, 5 Columns

## Summary

- **Baseline churn is 36.3%** (363 of 1,000). Churn is higher on the basic plan (42.8%) than on plus (29.3%) and pro (29.8%). The plan association is significant but small (Cramér's V = 0.138).
- **refund_issued is the dominant association.** Churn is 95.9% when refund_issued = 1 and 1.6% when it is 0 (Cramér's V = 0.946). This pattern holds within every plan and usage stratum. Whether refund_issued is recorded before or after churn has not been verified, so it may be leakage rather than a usable predictor.
- **Without refund_issued, prediction is weak.** On a single 200-row test set, logistic regression reaches 60.5% accuracy and 0.612 ROC AUC, and gradient-boosted trees reach 57.0% and 0.530. Both are at or below the 63.5% majority-class baseline. With refund_issued, logistic regression reaches 98.0% accuracy, but this result depends on the unverified timing of that column.
- **usage_hours and tenure_months are significantly lower for churners** (small-to-medium effects, rank-biserial r of −0.248 and −0.265). Within refund_issued = 0, where only 10 churn events exist, neither shows a significant association, but those nulls are low-powered.

## Data

- **Size:** 1,000 rows × 5 columns.
- **Columns:** numeric features usage_hours, tenure_months and refund_issued; categorical feature plan; target churned. There are no date/time features and no identifier or free-text columns.
- **Target:** churned is binary. Class 0 (retained) is 63.7% and class 1 (churned) is 36.3%.
- **Missing values:** none in any of the five columns.
- **Leakage warning:** the profile flags refund_issued alone as predicting churned at 0.975. The profile does not specify the metric behind this score.

## Findings

### Churn rates by group

Overall churn is 36.3% (363 of 1,000).

- **plan:** basic 42.8% (219 of 512); plus 29.3% (87 of 297); pro 29.8% (57 of 191).
- **refund_issued:** 0 gives 1.6% (10 of 632); 1 gives 95.9% (353 of 368). This is a descriptive association only.
- **usage_hours quartiles** (lowest to highest): 46.6% (118 of 253), 41.1% (102 of 248), 36.1% (90 of 249), 21.2% (53 of 250). Churn falls as usage rises.
- **tenure_months quartiles** (shortest to longest): 49.8% (128 of 257), 41.5% (102 of 246), 29.1% (75 of 258), 24.3% (58 of 239). Churn falls as tenure rises.

![Churn rate by plan and refund_issued](tasks/eda_1/charts/churn_rate_by_plan_refund.png)

### Significance tests and effect sizes

All four primary tests remain significant after Holm correction. Each effect is reported on its own measure, and the measures are not ranked against each other.

- **plan:** chi-square = 19.03 (df 2), p = 7.4e-05, Cramér's V = 0.138 (small). The basic-minus-plus/pro churn difference is 0.133 (95% Wald CI 0.074 to 0.192).
- **refund_issued:** chi-square = 895.2 (df 1), p ≈ 1e-196, Holm-adjusted p = 4.3e-196, Cramér's V = 0.946 (very large). The churn difference, refund=1 minus refund=0, is 0.943 (95% Wald CI 0.921 to 0.966). This is descriptive only.
- **usage_hours:** Mann-Whitney p = 7.1e-11 (Holm-adjusted 1.4e-10). Median is 16.2 for churned and 20.5 for retained. Rank-biserial r = −0.248 (small-to-medium), in the direction of lower usage for churners.
- **tenure_months:** Mann-Whitney p = 3.0e-12 (Holm-adjusted 9.1e-12). Median is 26.0 for churned and 41.0 for retained. Rank-biserial r = −0.265 (small-to-medium), in the direction of shorter tenure for churners.

![Churn rate (share churned) by plan, split by refund_issued](tasks/stat_1/charts/stat1_churn_rate_plan_refund.png)

### Interactions

- **refund_issued × plan:** not significant. The refund × basic interaction is 1.167 logit (95% CI −0.94 to 3.27, p = 0.28). The refund × plus interaction is 2.429 (95% CI −0.82 to 5.68, p = 0.14). Both are relative to pro. The model is near-separated, so these estimates are valid only if refund_issued is recorded before churn.
- **Churn within plan × refund_issued cells:**
  - refund_issued = 1: pro 91.7% (n = 60), basic 96.8% (n = 221), plus 96.6% (n = 87).
  - refund_issued = 0: pro 1.5% (n = 131), basic 1.7% (n = 291), plus 1.4% (n = 210).
- **Tenure × refund_issued:** the tenure × refund coefficient is −0.114 logit (95% CI −1.02 to 0.79, p = 0.81). Within refund_issued = 1, churn is 97.0% for low tenure (n = 230) and 94.2% for high tenure (n = 138). Within refund_issued = 0, it is 1.9% (n = 260) and 1.3% (n = 372).
- **Usage × tenure:** the standardized tenure × usage coefficient is −0.076 logit (95% CI −0.53 to 0.38, p = 0.74). Tenure × usage cell churn rates were not computed.
- **Usage split within refund_issued (median split):**
  - refund_issued = 1: 99.1% for low usage (n = 216) and 91.4% for high usage (n = 152).
  - refund_issued = 0: 1.8% for low usage (n = 280) and 1.4% for high usage (n = 352).

  Within refund_issued = 1, churn is lower for high-usage customers (91.4%) than for low-usage customers (99.1%). This is a descriptive gap. The usage × refund_issued interaction was not estimated, so the data do not show whether it is a real effect modifier. A separate quartile split (see the next subsection) shows the same direction, with the top quartile at 83.6%. The two splits are different cuts of the data and should not be combined.

![Churn rate by plan within refund_issued groups](tasks/stat_2/charts/stat2_churn_rate_plan_refund.png)

### Stratified check: is refund_issued a proxy for plan or usage?

- **Within refund_issued = 0,** churn is flat across plans: basic 1.7% (5 of 291), plus 1.4% (3 of 210), pro 1.5% (2 of 131). It is also flat across usage quartiles: 1.5% (2 of 135), 2.0% (3 of 149), 1.9% (3 of 159), 1.1% (2 of 189). The overall plan and usage gradients disappear.
- **Within refund_issued = 1,** churn is high across plans: basic 96.8% (214 of 221), plus 96.6% (84 of 87), pro 91.7% (55 of 60). Across usage quartiles it is 98.3% (116 of 118), 100.0% (99 of 99), 96.7% (87 of 90), and 83.6% (51 of 61) in the top quartile. The pro figure and the top-quartile figure rest on 60 and 61 rows.
- Across all plan and usage strata, refund=0 churn ranges from 1.1% to 2.0%, and refund=1 churn ranges from 83.6% to 100.0%. Refund_issued still separates churn when plan and usage are held fixed. This is descriptive only, and it does not establish that refund_issued is usable as a predictor.

![Churn rate by plan within each refund_issued level](tasks/eda_2/charts/churn_rate_by_plan_within_refund.png)

### Within refund_issued = 0 (partial task)

This analysis is incomplete and its nulls are low-powered: the subgroup has 632 rows and only 10 churn events (1.6%).

- **Logit coefficients:** tenure_months coefficient −0.009 (95% CI −0.04 to 0.02, p = 0.57); usage_hours coefficient −0.023 (p = 0.49). The usage_hours CI bounds were truncated in the output and are not reported here.
- **Plan:** plus vs basic coefficient −0.18 (95% CI −1.63 to 1.26, p = 0.80); pro vs basic coefficient −0.07 (95% CI −1.73 to 1.59, p = 0.94). These intervals are very wide and do not rule out large plan effects.
- **Flat splits:** tenure halves are 1.6% (5 of 316) each; usage halves are 1.6% (5 of 313 high) and 1.6% (5 of 319 low). The equal tenure-half counts were checked against the data (median split at 41.5, no ties at the median, clean 0/1 churn column). The match is reproducible, but the check cannot establish whether it is chance.
- **All-rows model with refund_issued as a covariate:** usage_hours coefficient −0.081 (p = 0.0006), so the usage association partly persists. tenure_months coefficient −0.016 (p = 0.13), so tenure weakens. refund_issued has a coefficient of 7.45 (p ≈ 5e-57). The usage–refund interaction was not tested.

### Predictive models

The data were split once, stratified, into 800 training and 200 test rows (random_state 42). Churn is 36.25% in training (290 of 800) and 36.5% in test (73 of 200). The majority-class baseline (always predict 0) has 63.5% test accuracy. Features are usage_hours, tenure_months, refund_issued, and plan one-hot encoded as plan_basic, plan_plus and plan_pro.

**Without refund_issued** (single split, test set of 200):

| Model | Test accuracy | ROC AUC | F1 | Precision | Recall | Train accuracy |
|---|---|---|---|---|---|---|
| Logistic regression | 60.5% | 0.612 | 0.336 | 0.435 | 0.274 | 69.5% |
| Gradient-boosted trees | 57.0% | 0.530 | 0.317 | 0.377 | 0.274 | 79.6% |

- Both models fall below the 63.5% baseline on accuracy.
- Gradient-boosted trees overfit: train accuracy is 79.6% against test accuracy of 57.0%.
- Top features: logistic regression ranks usage_hours (0.634) and tenure_months (0.529) highest by absolute coefficient. Gradient-boosted importance is usage_hours 0.611 and tenure_months 0.330.
- These are the estimates of predictive power from usage_hours, tenure_months and plan. They come from one split and no cross-validation.

**With refund_issued** (same split):

| Model | Test accuracy | ROC AUC | F1 | Precision | Recall |
|---|---|---|---|---|---|
| Logistic regression | 98.0% | 0.990 | 0.973 | 0.973 | 0.973 |
| Gradient-boosted trees | 96.5% | 0.976 | 0.951 | 0.971 | 0.932 |

- Dropping refund_issued reduces test AUC by 0.378 for logistic regression and by 0.446 for gradient-boosted trees.
- Feature weight is concentrated on refund_issued: its standardized logistic coefficient is 3.33, against 0.73 for usage_hours and 0.24 for tenure_months. Its gradient-boosted importance is 0.936, against 0.042 for usage_hours.
- These scores should not be treated as valid predictive performance until the recording time of refund_issued is verified.

![Test accuracy and ROC AUC of logistic regression and gradient-boosted trees on churn_split, with and without refund_issued, against the majority-class baseline](tasks/ml_2/charts/ml2_model_comparison.png)

## Limitations

- **Possible leakage.** refund_issued separates churn almost completely (95.9% vs 1.6%) and alone gives a score of 0.975. Its recording time relative to churn has not been verified. Every refund-based result (the tests, the interactions, the models with refund_issued) is conditional on it being a pre-churn variable. The "without refund_issued" results are the only ones not affected by this question.
- **Unresolved review issue 1: tenure × usage cell churn rates are missing.** The brief asks for churn rates within each interaction cell. The tenure × usage cell rates were not computed, so this part of the brief is unanswered.
- **Unresolved review issue 2: the usage_hours × refund_issued interaction was not estimated.** The model formula has no such term. The conclusion that no interaction is worth breaking down covers usage, but usage × refund was never tested. Its coefficient, CI and p-value are therefore not available.
- **Unresolved review issue 3: the within-refund=1 usage gap is not interpreted in the findings.** Churn is 99.1% for low usage and 91.4% for high usage within refund_issued = 1. This gap is descriptive, rests on 216 and 152 rows, and is untested. It is not a confirmed effect modifier, and it is subject to the same refund timing caveat.
- **Failed or partial task: stat_3 is partial.** The within-refund=0 analysis rests on 10 churn events. Its nulls are low-powered and do not establish absence of effect. The usage_hours CI is truncated and not reported.
- **Small cells.** Some plan × refund cells are small: pro with refund_issued = 1 has 60 rows, and the top usage quartile within refund_issued = 1 has 61 rows. Plan differences within refund_issued = 1 cannot be tested reliably.
- **Model limitations.** Each model is a single stratified split with 200 test rows. No cross-validation was run. The gradient-boosted model overfits without refund_issued. The three plan dummies sum to one, so a model with an intercept is collinear and the coefficients for plan are not clean.
- **Multiple testing.** Holm correction was applied to the four primary tests, as reported in stat_1.

**Numbers not traced to a recorded fact.** The automatic check found no recorded value for these numbers:
- 290 in: "The data were split once, stratified, into 800 training and 200 test rows (random_state 42). Churn is 36.25% in training (290 of 800) and 36.5% in test (73 of 2"

## Open questions

- When is refund_issued recorded relative to churn? If it is recorded after churn, it is leakage and must be dropped. The current results do not answer this.
- Why do only 10 of 632 refund_issued = 0 customers churn? Is refund_issued a consequence of churn-related behaviour rather than a predictor of it? The data do not say.
- Does the refund × plan pattern (pro at 91.7% vs 96.8% and 96.6%) hold with a larger sample or an exact test within the refund = 1 group?
- Does the usage_hours × refund_issued interaction exist? The model has not been fitted with this term.
- What are the tenure × usage cell churn rates, and does their joint effect matter for the task?
- Does the usage_hours association in the all-rows model reflect a confound with refund_issued, or an independent association?
- Do the within-refund=0 usage and plan nulls hold with adequate power, using a Firth or penalised logit, or by pooling data?
- Do the predictive results without refund_issued hold under cross-validation, and does regularisation or fewer trees remove the gradient-boosted overfitting?
- Can engineered features improve prediction from usage_hours and tenure_months, which currently give AUC near 0.5–0.6?