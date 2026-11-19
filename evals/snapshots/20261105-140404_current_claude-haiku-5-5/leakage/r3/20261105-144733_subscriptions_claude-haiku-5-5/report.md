# Churn Analysis Report: Predicting `churned` in a 1,000-Row Dataset

## Summary

- **Base rate and plan:** 36.3% of the 1,000 rows churned (363). Churn is higher for the basic plan (42.8%) than for plus (29.3%) and pro (29.8%). The plan association is significant but small (chi-square p = 7.4e-5, Cramér's V = 0.138).
- **refund_issued is a likely leak:** refund_issued=1 churned at 95.9% versus 1.6% for refund_issued=0. Alone, it predicts churn with accuracy 0.975 and AUC 0.974. Whether refunds occur before or after churn is unconfirmed, so this separation cannot be treated as usable predictive evidence.
- **Models depend on refund_issued:** with refund_issued, logistic regression reaches test accuracy 0.98 and gradient boosting 0.965. Without it, test accuracy falls to 0.605 and 0.57, both below the 0.635 majority baseline on the 200-row test split.
- **Refund-free signal is small:** 5-fold stratified CV on all rows, without refund_issued, gives logistic regression accuracy 0.669 against a 0.637 baseline (ROC AUC 0.690). Gradient boosting matches the baseline in accuracy (0.637) with ROC AUC 0.640. Within refund_issued=0, neither usage_hours nor tenure_months separates churners (p = 0.61 and 0.66). Within refund_issued=1, usage_hours does (p = 0.0001).

## Data

- **Size:** 1,000 rows, 5 columns: usage_hours, tenure_months, refund_issued (numeric), plan (categorical), and churned (binary target). There are no date/time features and no id or free-text columns.
- **Target distribution:** churned=0 is 63.7% (637 rows) and churned=1 is 36.3% (363 rows).
- **Missing values:** none in any column.
- **Leakage warning:** the profile flags refund_issued as a possible target leak (accuracy 0.975 alone).

## Findings

### Churn base rate and plan

- Overall churn is 0.363 (363 of 1,000 rows).
- Churn rate by plan: basic 0.428 (n=512), plus 0.293 (n=297), pro 0.298 (n=191). Basic churns more; plus and pro are similar.
- Plan is significantly associated with churn: chi-square = 19.03, df = 2, p = 7.4e-5, Cramér's V = 0.138 (small effect).
- Within refund_issued strata, the plan difference largely disappears. Churn within refund_issued=0 is 0.017 (basic), 0.014 (plus) and 0.015 (pro). Within refund_issued=1 it is 0.968 (basic), 0.966 (plus) and 0.917 (pro, n=60). The plan × refund interaction is not significant (LR = 0.84, df = 2, p = 0.66).

![Churn rate (share of rows with churned=1) by plan level and by refund_issued value](tasks/eda_1/charts/churn_rate_plan_refund_bar.png)

![Churn rate (share churned=1) by plan, separately for refund_issued=0 and 1](tasks/stat_1/charts/churn_rate_plan_by_refund.png)

### refund_issued and possible leakage

- Churn is 0.016 for refund_issued=0 (n=632) and 0.959 for refund_issued=1 (n=368).
- Difference (refund=1 minus refund=0): 0.943, 95% Wald CI 0.921 to 0.966. Risk ratio 60.6 (95% CI 32.8 to 112.2).
- Refund_issued alone scores accuracy 0.975, AUC 0.974 and correlation 0.946 with churned.
- The data has no timing column. The EDA task treats refund_issued as a leakage candidate, and the statistics task says it should not be treated as a usable predictor until its timing is confirmed.

### Usage hours and tenure

- **Usage quartiles (mean churned):** Q1 0.466 (n=253), Q2 0.411 (n=248), Q3 0.361 (n=249), Q4 0.212 (n=250). Churn falls as usage rises.
- **Tenure quartiles (mean churned):** Q1 0.498 (n=257), Q2 0.415 (n=246), Q3 0.291 (n=258), Q4 0.243 (n=239). Churn falls as tenure rises.
- **Medians:** usage_hours is 20.5 for not churned and 16.2 for churned. tenure_months is 41 and 26.
- **Tests (pooled, all rows):**
  - usage_hours: median difference (churned minus not churned) −4.3, bootstrap 95% CI −5.5 to −2.5; Mann-Whitney p = 7e-11; rank-biserial 0.248 (unsigned), a small-to-medium effect.
  - tenure_months: median difference −15, bootstrap 95% CI −19 to −11; Mann-Whitney p = 3e-12; rank-biserial 0.265 (unsigned), a small-to-medium effect.

![Box plots of usage_hours and tenure_months split by churned (0 vs 1)](tasks/eda_1/charts/numeric_by_churned_box.png)

### Usage hours and tenure, stratified by refund_issued

- **Sign convention:** the stat_2 rank-biserials are signed (positive = churned higher, negative = churned lower). stat_1 reported the same direction as unsigned magnitudes.
- **refund_issued=0 (10 churned, 622 not churned):**
  - usage_hours: Mann-Whitney p = 0.61, rank-biserial −0.094, median difference −2.35, bootstrap CI −6.8 to 7.4.
  - tenure_months: p = 0.66, rank-biserial −0.082, median difference −3, bootstrap CI −26.5 to 14.
- **refund_issued=1 (353 churned, 15 not churned):**
  - usage_hours: p = 0.00013, rank-biserial −0.584, median difference −11.2, bootstrap CI −16.3 to −6.0.
  - tenure_months: p = 0.097, rank-biserial −0.253, median difference −11, bootstrap CI −28 to 3.
- The pooled usage_hours effect holds only within refund_issued=1. The pooled tenure_months effect holds in neither stratum. The pooled results are driven by the refund=1 group, which contains 353 of the 363 churners.
- **Interaction tests:** usage_hours × refund_issued gives LR = 3.81, p = 0.051 (borderline). Within refund=1, churn falls from 0.983 (Q1, n=118) to 0.836 (Q4, n=61). Within refund=0, churn stays between 0.011 and 0.020 across quartiles.

![Median difference in usage_hours and tenure_months, churned minus not churned, within refund_issued=0 and refund_issued=1; bars are bootstrap 95% CIs](tasks/stat_2/charts/stat2_median_diff_by_refund.png)

### Predictive models with refund_issued (leakage-affected)

Single stratified 80/20 split (random_state 42): 800 training rows and 200 test rows. Test churn rate 0.365. Majority-class baseline test accuracy 0.635.

| Model | Test accuracy | Test ROC AUC | Test F1 |
|---|---|---|---|
| Logistic regression, all features | 0.980 | 0.990 | 0.973 |
| Gradient boosting, all features | 0.965 | 0.976 | 0.951 |

- These scores are not valid predictive performance until refund timing is confirmed.
- In both models, refund_issued dominates the feature ranking. Logistic regression standardized |coefficient| is 3.33 for refund_issued, 0.73 for usage_hours, 0.24 for tenure_months, and at most 0.17 for plan dummies. Gradient boosting importance is 0.936, 0.042, 0.018 and at most 0.002. The two scales are not comparable across models.
- Removing refund_issued lowers test accuracy by 0.375 (logistic regression) and 0.395 (gradient boosting), ROC AUC by 0.378 and 0.446, and F1 by 0.637 and 0.634.

### Predictive models without refund_issued

Same single split, refund_issued excluded.

| Model | Train accuracy | Test accuracy | Test ROC AUC | Test F1 |
|---|---|---|---|---|
| Logistic regression | 0.695 | 0.605 | 0.612 | 0.336 |
| Gradient boosting | 0.796 | 0.570 | 0.531 | 0.318 |

- Both models score below the 0.635 majority baseline on test accuracy.
- The gradient boosting model overfits: its train accuracy is 0.796 against a test accuracy of 0.570, so its test scores are unreliable.
- Logistic coefficients are 0.63 for usage_hours and 0.53 for tenure_months. Gradient boosting importances are 0.61 and 0.33.

![Test-split scores of logistic regression and gradient boosting, all features vs without refund_issued, against the majority-class baseline](tasks/ml_2/charts/ml2_model_comparison.png)

### Cross-validation without refund_issued (full 1,000 rows)

5-fold stratified CV, features usage_hours, tenure_months and plan.

| Model | Accuracy (SD) | ROC AUC (SD) | F1 (SD) |
|---|---|---|---|
| Majority class | 0.637 (0.003) | 0.500 | 0.000 |
| Logistic regression | 0.669 (0.027) | 0.690 (0.019) | 0.427 (0.024) |
| Gradient boosting | 0.637 (0.020) | 0.640 (0.019) | 0.422 (0.042) |

- Logistic regression reaches mean accuracy 0.669 against 0.637 for the majority class in CV.
- Gradient boosting does not beat the majority accuracy in CV, though its ROC AUC is above 0.5.
- Conflict: gradient boosting ROC AUC is 0.640 in CV but 0.531 on the single 200-row test split. The two results disagree, and the ranking result is sensitive to how the data are split.
- These CV results are not yet shown to be independent of refund_issued. Within refund_issued=0, neither usage_hours nor tenure_months separates churners (p = 0.61 and 0.66), while within refund_issued=1 usage_hours does (p = 0.0001) and tenure_months marginally does (p = 0.097).

![Mean 5-fold cross-validated accuracy, ROC AUC and F1 for the majority baseline, logistic regression and gradient boosting, excluding refund_issued](tasks/ml_3/charts/ml3_cv_comparison.png)

## Limitations

- **refund_issued timing is unconfirmed.** The dataset has no timing column. Every result involving refund_issued, including the 0.975 separation, the all-feature model scores and the stratified separations, is conditional on this. The EDA and statistics findings say the leakage issue must be resolved before any refund-based result is used.
- **The refund-free signal may be a refund proxy.** The ml_3 findings state that the CV gain may reflect refund-related behaviour and cannot yet be attributed to usage_hours, tenure_months and plan alone.
- **Small strata.** Only 10 churners fall in refund_issued=0 and only 15 non-churners in refund_issued=1. Stratified tests in these groups are unstable.
- **Test-split instability.** The 200-row test split gives gradient boosting ROC AUC 0.531, while CV gives 0.640. Single-split estimates are not reliable here.
- **Borderline interaction.** The usage_hours × refund_issued interaction (p = 0.051) is borderline.
- **Overfitting.** The gradient boosting model without refund_issued overfits (train accuracy 0.796 vs test 0.570).
- **Baseline values differ slightly by sample.** The majority-class accuracy is 63.7% in the profile, 0.635 on the test split and 0.637 in CV. These are reported as computed on their respective samples.
- **Rank-biserial sign.** stat_1 reports unsigned magnitudes. stat_2 reports signed values. Both describe churned being lower.
- **Confounding not tested.** Whether the basic plan's higher churn is explained by refund status or tenure differences has not been tested.
- **No failed tasks.** All six tasks (eda_1, stat_1, ml_1, ml_2, stat_2, ml_3) completed and were accepted.

## Open questions

- Is refund_issued recorded before or after churn? If after, refund_issued should be dropped and the separation and model analyses rerun.
- Do usage_hours and tenure_months still separate churners within refund_issued=1 after adjusting for plan and tenure?
- What distinguishes the 10 churners within refund_issued=0 from the 622 non-churners?
- Why are there only 15 non-churners within refund_issued=1?
- Is the basic plan's higher churn explained by refund status or by tenure differences across plans?
- Do usage_hours and tenure_months predict churn within each refund_issued stratum when tested with cross-validation, and does the logistic gain survive stratification?
- Do regularized or simpler models give more stable gains over the majority baseline than gradient boosting does?