# Churn Analysis of 1,000 Customers: Target `churned`

## Summary

- **refund_issued is almost a perfect predictor of churn, and it is flagged as possible leakage.** Customers with refund_issued=1 churned at 95.9% (n=368), against 1.6% for refund_issued=0 (n=632). Used alone, it reaches accuracy 0.975 on the full data. Every model result below is reported with and without it.
- **Plan, usage_hours and tenure_months are significantly associated with churn, but the effects are small.** Plan has Cramér's V = 0.138. Usage and tenure have rank-biserial values of -0.248 and -0.265. All four primary tests remain significant after Holm correction.
- **Without refund_issued, logistic regression beats the majority baseline only modestly under repeated CV.** Its mean accuracy is 0.671 against 0.637 for the baseline, with mean ROC AUC 0.694. On the single 200-row test split it scored below the baseline (0.605 against 0.635), and the two results disagree.
- **Gradient boosting does not beat the baseline without refund_issued and overfits.** Its CV mean accuracy is 0.612, with a train-test gap of 0.280.
- **refund_issued does not significantly change the effects of plan, usage_hours or tenure_months on churn.** The joint likelihood-ratio test gives p = 0.246. This conclusion rests on a column whose timing relative to churn is unknown.

## Data

- 1,000 rows and 5 columns: `usage_hours`, `tenure_months` and `refund_issued` (numeric), and `plan` (categorical). `churned` is the target.
- Target classes: 0 at 63.7% and 1 at 36.3%.
- No missing values in any column.
- No date/time or id columns.
- Leakage warning from the profile: refund_issued alone predicts `churned` at 0.975.

## Findings

### Churn by plan

- Churn is highest on the basic plan at 42.8% (n=512). It is 29.3% on plus (n=297) and 29.8% on pro (n=191).
- Plan is significantly associated with churn: chi-square = 19.03, df = 2, p = 7.4e-05, Cramér's V = 0.138 (small). The Holm-adjusted p is also 7.4e-05.
- Basic-plan churn exceeds plus by 13.5 percentage points (95% CI 6.8 to 20.2) and exceeds pro by 12.9 points (95% CI 5.2 to 20.7).

![Churn rate by plan level (left) and by refund_issued (right); rate = share of customers with churned=1 in each group](tasks/eda_1/charts/churn_rate_by_plan_and_refund.png)

![Churn rate by plan and by refund_issued; error bars show 95% CIs; rate = share of customers with churned=1](tasks/stat_1/charts/stat1_churn_rates.png)

### refund_issued and leakage

- Churn is 95.9% (n=368) for refund_issued=1 and 1.6% (n=632) for refund_issued=0.
- The association is very large: chi-square = 895.2, df = 1, p = 1.1e-196, Cramér's V = 0.946. The Holm-adjusted p is 4.3e-196.
- The churn rate difference between refund_issued=1 and 0 is 94.3 percentage points (95% CI 92.1 to 96.6).
- The data do not show when refunds were issued relative to churn. The association may reflect refunds issued at cancellation rather than a driver of churn, so it should not be read as causal.

### Usage and tenure

- Churned customers have lower usage. Mean usage_hours is 21.8 for churned=0 and 17.3 for churned=1 (medians 20.5 and 16.2).
- The Mann-Whitney test gives p = 7.1e-11 (Holm-adjusted 1.4e-10), rank-biserial = -0.248 (small-to-medium). The Welch mean difference (churned=0 minus churned=1) is 4.47 hours (95% CI 3.30 to 5.64).
- Churned customers have shorter tenure. Mean tenure_months is 39.1 for churned=0 and 29.8 for churned=1 (medians 41 and 26).
- The Mann-Whitney test gives p = 3.0e-12 (Holm-adjusted 9.1e-12), rank-biserial = -0.265 (small-to-medium). The Welch mean difference is 9.27 months (95% CI 6.75 to 11.80).
- Churn falls across usage_hours quartiles: 46.6% in the lowest (n=253), 41.1% (n=248), 36.1% (n=249), and 21.2% in the highest (n=250).
- Churn falls across tenure_months quartiles: 49.8% in the shortest (n=257), 41.5% (n=246), 29.1% (n=258), and 24.3% in the longest (n=239).

### Test summary (Holm correction across four tests)

All four primary tests remain significant at alpha 0.05 after Holm correction: plan, refund_issued, usage_hours and tenure_months. The refund effect is by far the largest. The plan, usage and tenure effects are small.

### Does refund_issued change the effect of other features?

- **Plan within refund groups.** Churn with refund_issued=1 is 96.8% on basic (n=221), 96.6% on plus (n=87) and 91.7% on pro (n=60). With refund_issued=0 it is 1.7% (n=291), 1.4% (n=210) and 1.5% (n=131).
- **Usage quartiles within refund groups.** With refund_issued=1, churn is 98.3% in Q1 (n=118), 100% in Q2 (n=99), 96.7% in Q3 (n=90) and 83.6% in Q4 (n=61). With refund_issued=0 it is 1.1% to 2.0% in every quartile (Q4: 1.1%, n=189). The 83.6% figure is a descriptive dip. It is not supported by a significant interaction (Holm-adjusted p = 0.152).
- **Tenure quartiles within refund groups.** With refund_issued=1, churn is 93.2% to 97.7% (n=59 to 128). With refund_issued=0 it is 1.1% to 2.3%. The refund association does not vary clearly with tenure.
- **Interaction tests.** The likelihood-ratio test for the three refund_issued interaction terms jointly gives LR = 5.43, df = 4, p = 0.246. The individual Wald p-values are 0.943 for refund x plus, 0.235 for refund x pro, 0.038 for refund x usage_hours and 0.717 for refund x tenure_months (coefficient -0.0077). After Holm correction across the four terms, the adjusted p-values are 1.0, 0.705, 0.152 and 1.0. None is significant.
- **Conclusion.** No interaction is reported as a moderation effect. Because refund=0 customers almost never churn, the logit is quasi-separated, and the likelihood-ratio test is the more reliable evidence.

### Predictive models: single split (ml_1)

The data were split 80/20 with stratification (800 training rows, 200 test rows).

| Model | Test accuracy | ROC AUC | F1 |
|---|---|---|---|
| Majority baseline | 0.635 | 0.500 | 0.000 |
| Logistic regression, with refund_issued | 0.980 | 0.990 | 0.973 |
| Gradient boosting, with refund_issued | 0.965 | 0.976 | 0.951 |
| Logistic regression, without refund_issued | 0.605 | 0.612 | 0.336 |
| Gradient boosting, without refund_issued | 0.570 | 0.533 | 0.317 |

- The majority baseline's test accuracy is 0.635. The full-data share is 63.7%.
- Without refund_issued, both models score below the 0.635 baseline on this split.
- Gradient boosting without refund_issued overfits: train accuracy is 0.796 and test accuracy is 0.570. Its test figures are unreliable. The logistic model without refund_issued has train 0.694 and test 0.605.
- Permutation importance (drop in test ROC AUC, 20 repeats): refund_issued is 0.459 in the logistic model and 0.497 in gradient boosting. usage_hours is 0.011 and tenure_months is 0.003 in the logistic model.
- The gradient boosting impurity importance for refund_issued is 0.936. This is not a permutation importance and should not be compared directly with the permutation drops.
- The collapse in performance without refund_issued indicates that refund_issued is leakage-like. The analysis cannot establish whether it causes churn.

![Test-set accuracy, ROC AUC and F1 for the majority baseline, logistic regression and gradient boosting, with and without refund_issued](tasks/ml_1/charts/ml1_model_comparison.png)

### Predictive models: repeated stratified CV without refund_issued (ml_2)

Repeated stratified 5x5 CV gives 25 folds.

- **Majority baseline:** accuracy 0.637 (SD 0.003), ROC AUC 0.500, F1 0.000.
- **Logistic regression:** accuracy 0.671 (SD 0.027), ROC AUC 0.694 (SD 0.032), F1 0.435 (SD 0.048). It beats the baseline by a mean of 0.034 accuracy and on 22 of 25 folds (88%), using paired per-fold differences. No formal significance test was run, so the margin is modest.
- **Gradient boosting:** accuracy 0.612 (SD 0.026), ROC AUC 0.601 (SD 0.029), F1 0.415 (SD 0.048). It falls below the baseline by a mean of 0.025 and beats it on 6 of 25 folds (24%).
- **Train-test gap:** gradient boosting has a mean train accuracy of 0.891 against test 0.612, a gap of 0.280. Logistic regression has train 0.678 and test 0.671, a gap of 0.007.
- **Leakage check:** refund_issued used alone reaches accuracy 0.975 and ROC AUC 0.974 on the full data. All results in this subsection exclude it.

![Repeated stratified 5x5 CV without refund_issued: mean and SD of test accuracy, ROC AUC and F1 for majority, logistic regression and gradient boosting](tasks/ml_2/charts/ml2_cv_model_comparison.png)

### Disagreement between the single split and repeated CV

The single 200-row split (ml_1) and the 25-fold CV (ml_2) disagree on logistic regression without refund_issued. On the single split it scored 0.605 accuracy and 0.612 ROC AUC, below the 0.635 baseline. Under repeated CV it scored 0.671 accuracy and 0.694 ROC AUC, above the 0.637 baseline. The review of this work judges the CV figures the more reliable estimate, because the single test split has only 200 rows and the CV averages 25 folds. On that basis the below-baseline single-split result should not be read as the model's performance. Both results are reported here as they stand.

## Limitations

- **Leakage and timing.** refund_issued is flagged as leakage-like. The data do not establish when refunds were issued relative to churn. Every model and association involving it is non-causal and may not be available before cancellation.
- **Quasi-separation.** Refund=0 customers almost never churn, so the logit is quasi-separated. Wald estimates for the interaction terms are unstable. The refund x usage_hours term (Holm 0.152) is nominal only.
- **Missing interaction coefficients (unresolved review issue 1).** The review asked for the coefficients and p-values of the four interaction terms, and the LR-test degrees of freedom. The coefficient and p-value for refund x tenure_months (-0.0077, p = 0.717) and the Wald p-values for the other three terms are reported above. The coefficients for refund x plus, refund x pro and refund x usage_hours were not part of the accepted results, so they are not reported. The LR-test df = 4 is reported.
- **Usage Q4 dip (unresolved review issue 2).** The 83.6% churn for refund_issued=1 in the highest usage quartile (n=61) is a descriptive dip. It is not supported by a significant interaction (Holm 0.152) and rests on a small group. The review asked that it not be described as a substantial gap, and this report follows that instruction.
- **Single test split.** The 200-row test split in ml_1 is noisy. Its below-baseline result is in conflict with the CV result (see above).
- **Beats-baseline claim.** The claim that logistic regression beats the baseline without refund_issued rests on paired fold differences (88% of folds). It has no formal significance test and the margin is modest (+0.034 accuracy).
- **Gradient boosting.** Gradient boosting overfits strongly in both the single split and the CV (train-test gap 0.280 under CV). Its scores are not reported as valid predictive results.
- **Small sample.** The data have 1,000 rows, which limits the power of subgroup and interaction analyses.
- **Baseline figures.** The majority baseline is reported as 63.7% (full data), 63.5% (single test split) and 63.7% (CV mean). These differ only because of the split.
- **Failed tasks.** None. All four tasks (eda_1, stat_1, ml_1, stat_2) and the repeated-CV task (ml_2) completed.

## Open questions

- Is refund_issued recorded only after cancellation, and should it be excluded from any model meant to predict churn in advance? The timing of refunds relative to churn has not been established.
- Is the refund association causal, or do refunds follow from the cancellation decision?
- Does refund_issued carry information about churn that is only available after cancellation?
- Does a multivariable logistic regression with controls show whether refund_issued drives churn independently of plan, usage and tenure, or whether the three overlap? Is the basic-plan churn gap explained by refund_issued or by usage and tenure differences?
- Do usage_hours and tenure_months predict churn better once plan is controlled for? Logistic regression reaches only about 0.69 ROC AUC without refund_issued.
- Does a Firth or penalized logit, fitted to handle quasi-separation, still show the refund x usage_hours signal (Holm 0.152)?
- Does the usage Q4 refund=1 dip (83.6%, n=61) reflect a real subgroup or sampling noise?
- Would stronger regularisation or fewer boosting iterations close the gradient boosting train-test gap?
- Would repeated cross-validation of the moderation analysis give more stable estimates, and does the moderation picture change when refund_issued is excluded or replaced by a non-leaky proxy?