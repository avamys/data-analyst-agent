# Customer Churn Analysis: Drivers and Predictability of `churned` (1,000 rows)

## Summary

- **refund_issued dominates the data, and its role is unresolved.** Churn is 95.9% when a refund was issued (368 rows) and 1.6% when not (632 rows). Used alone, it predicts churn with accuracy 0.975. Whether refunds occur before or after cancellation is unknown, so this may be target leakage.
- **Without refund_issued, the models do not beat the majority baseline.** On the 200-row test split, logistic regression reaches ROC AUC 0.612 and accuracy 0.605, and gradient boosting reaches ROC AUC 0.533 and accuracy 0.570. The majority-class baseline is 0.635.
- **usage_hours and tenure_months are significantly lower for churned customers.** Median usage_hours is 16.2 for churned versus 20.5 for retained customers. Median tenure_months is 26 versus 41. Both differences are significant (Mann-Whitney p = 7.1e-11 and 3.0e-12), but the effects are small to medium.
- **The basic plan's higher churn (42.8%, versus 29.3% for plus and 29.8% for pro) persists after adjusting for usage_hours and tenure_months, but not after adjusting for refund_issued.** With refund excluded, the adjusted gaps are about −0.12 (plus) and −0.10 (pro). With refund included, neither gap is significant (plus OR 0.80, p = 0.65; pro OR 0.44, p = 0.14). This is a sensitivity analysis, not a causal estimate.
- **No plan interaction is supported.** The usage_hours and tenure_months effects do not differ detectably by plan (p = 0.556 and 0.703). The only borderline interaction is usage_hours × refund_issued (p = 0.049), and it rests on only 10 churners among 632 refund-0 rows.

## Data

- 1,000 rows and 5 columns: three numeric features (usage_hours, tenure_months, refund_issued), one categorical feature (plan), and the binary target `churned`.
- No identifier, free-text or date/time columns.
- Target distribution: 63.7% class 0 (stayed) and 36.3% class 1 (churned).
- No missing values in any column.
- Profile warning: possible target leakage, because refund_issued alone predicts churn at 0.975.

## Findings

### Overall churn and group rates (eda_1)

- The overall churn rate is 36.3% (363 of 1,000 rows churned).
- **By plan:** basic 42.8% (512 rows), plus 29.3% (297 rows), pro 29.8% (191 rows). Plus and pro are similar to each other.
- **By refund_issued:** 95.9% for refund_issued=1 (368 rows) versus 1.6% for refund_issued=0 (632 rows).
- **By usage_hours quartile** (bin edges 1.9, 12.5, 18.9, 25.525, 67.7): Q1 46.6% (253 rows), Q2 41.1% (248), Q3 36.1% (249), Q4 21.2% (250). Churn falls steadily across quartiles.
- **By tenure_months quartile** (bin edges 1, 18, 36, 53, 71): Q1 49.8% (257 rows), Q2 41.5% (246), Q3 29.1% (258), Q4 24.3% (239). Churn falls steadily across quartiles.

![Histogram counts of usage_hours and tenure_months, split by churned (0 vs 1)](tasks/eda_1/charts/numeric_dist_by_churn.png)

### Significance and effect sizes (stat_1)

- **plan:** significantly associated with churn. χ² = 19.03 (df = 2), p = 7.4e-05, Cramér's V = 0.138, a small effect.
- **refund_issued:** strongly associated with churn. χ² = 895.2 (df = 1), p = 1.1e-196. The risk difference is 0.943, and the odds ratio is 1463.8 (95% CI 650.7 to 3292.9). The finding notes that this effect is so large it likely reflects target leakage.
- **usage_hours:** lower for churned rows (Mann-Whitney p = 7.1e-11). The rank-biserial correlation is −0.248 (small to medium), using the corrected sign convention (negative means churned rows rank lower). The median difference is −4.3 hours (bootstrap 95% CI −5.5 to −2.5).
- **tenure_months:** lower for churned rows (Mann-Whitney p = 3.0e-12). The corrected rank-biserial is −0.265 (small to medium). The median difference is −15 months (bootstrap 95% CI −19 to −11).

![Churn rate (share of rows churned) by plan and by refund_issued](tasks/stat_1/charts/stat1_churn_rate_plan_refund.png)

![Boxplots of usage_hours and tenure_months values by churn group (0 = stayed, 1 = churned)](tasks/stat_1/charts/stat1_continuous_by_churn_boxplot.png)

### Interactions (stat_2)

- **usage_hours × plan:** not supported (LR χ² = 1.17, df = 2, p = 0.556). Interaction coefficients are −0.049 for plus (95% CI −0.146 to 0.048) and 0.015 for pro (95% CI −0.117 to 0.147), on the log-odds scale.
- **tenure_months × plan:** not supported (LR χ² = 0.70, df = 2, p = 0.703). Coefficients are 0.001 for plus (95% CI −0.046 to 0.048) and 0.022 for pro (95% CI −0.031 to 0.076).
- **tenure_months × refund_issued:** not supported (LR χ² = 0.15, df = 1, p = 0.699). The coefficient is −0.008 (95% CI −0.049 to 0.033).
- **usage_hours × refund_issued:** borderline (LR χ² = 3.89, df = 1, p = 0.049). The coefficient is −0.092 (95% CI −0.180 to −0.004), so the usage slope is steeper when a refund is issued. This does not survive correction for four tests. The finding calls it unreliable because only 10 of 632 refund-0 rows churned, which gives near-separation. It should not be trusted until the refund timing question is resolved.
- All four interaction models converged.
- Within plans, churn is about 1.4% to 1.7% when refund_issued=0 and 91.7% to 96.8% when refund_issued=1 (basic 1.7% and 96.8%; plus 1.4% and 96.6%; pro 1.5% and 91.7%, with n = 60 for pro refund-1). The finding presents the idea that basic's higher overall churn is driven by refund mix across plans as a hypothesis, not a tested result.

### Predictive models (ml_1)

Test split: stratified 80/20, random_state 42 (800 train, 200 test; test churn rate 36.5%). The majority-class baseline is 0.637 on all rows and 0.635 on the test split.

| Model | Features | Test ROC AUC | Test accuracy | Train accuracy |
|---|---|---|---|---|
| Logistic regression | All | 0.990 | 0.980 | 0.974 |
| Gradient boosting | All | 0.976 | 0.965 | 0.990 |
| Logistic regression | No refund_issued | 0.612 | 0.605 | 0.694 |
| Gradient boosting | No refund_issued | 0.533 | 0.570 | 0.796 |

- With all features, refund_issued is the top feature in both models (logistic coefficient 3.33; gradient boosting importance 0.936).
- Without refund_issued, neither model beats the majority baseline on the test split (0.605 and 0.570 against 0.635).
- The no-refund gradient boosting model overfits: train accuracy is 0.796 against test accuracy 0.570. The finding says its test result is unreliable and should not be used to judge predictability.
- Logistic regression without refund_issued ranks usage_hours (0.634), tenure_months (0.529), plan_basic (0.281), plan_plus (0.267) and plan_pro (0.012) by absolute coefficient.

![Test ROC AUC of logistic regression and gradient boosting with all features and without refund_issued; dashed line is chance (0.5)](tasks/ml_1/charts/ml1_roc_auc.png)

### Feature importance without refund_issued (ml_2)

- Gradient boosting without refund_issued has test ROC AUC 0.533 and accuracy 0.570 (baseline 0.635). It does not beat the baseline.
- The two importance measures disagree:
  - By built-in gradient boosting importance, usage_hours ranks first (0.611), then tenure_months (0.330), plan_plus (0.030), plan_basic (0.020) and plan_pro (0.010).
  - By test-set permutation importance (mean drop in ROC AUC over 30 repeats), tenure_months ranks first nominally (0.012, sd 0.028). usage_hours is −0.025 (sd 0.036), meaning permuting it did not lower AUC.
- The finding states that the gaps are within noise. Permutation effects for the plan dummies are all close to zero relative to their sd (plan_plus 0.007, sd 0.007; plan_pro 0.001, sd 0.002; plan_basic −0.001, sd 0.007).
- The finding concludes that neither usage_hours nor tenure_months is reliably predictive on this test set. It does not show that no feature predicts churn, and it names overfitting and the 200-row test split as likely reasons.

![Permutation importance on the test set for gradient boosting without refund_issued: mean drop in ROC AUC per feature, bars show 1 sd over 30 repeats](tasks/ml_2/charts/ml2_perm_importance.png)

### Basic-plan gap, refund excluded (stat_3)

Logit model of churn on plan, usage_hours and tenure_months, with refund_issued excluded:

- **plus vs basic:** OR 0.552 (95% CI 0.401 to 0.761), p = 0.00028.
- **pro vs basic:** OR 0.612 (95% CI 0.420 to 0.890), p = 0.010.
- Average marginal effects (AME): plus −0.122, pro −0.103.
- Linear probability model: plus −0.122 (HC1 p = 0.00022; 95% CI −0.186 to −0.057); pro −0.100 (HC1 p = 0.0084; 95% CI −0.175 to −0.026).

The gaps are adjusted only for usage_hours and tenure_months. They are not causal plan effects, and refund mix may partly explain them.

![Adjusted churn rate difference of plus and pro versus basic, controlling for usage_hours and tenure_months; refund_issued excluded](tasks/stat_3/charts/stat3_adjusted_plan_diff.png)

### Basic-plan gap, refund included (stat_4)

This is a sensitivity analysis. The timing of refunds relative to cancellation is unknown.

- Corrected logit AMEs versus basic: with refund excluded, plus −0.122 and pro −0.103 (matching stat_3). With refund included, plus −0.005 and pro −0.020. The change is +0.117 for plus and +0.082 for pro. The stat_4 values first reported before a coding fix were superseded and should not be cited.
- Adjusted odds ratios with refund included: plus 0.804 (95% CI 0.310 to 2.084, p = 0.654); pro 0.438 (95% CI 0.146 to 1.309, p = 0.139).
- Refund coefficient: 7.45 (SE 0.47), OR 1712.3, p = 4.8e-57, AME 0.920.
- Share with refund_issued=1 by plan: basic 43.2%, plus 29.3%, pro 31.4%.
- The finding states that the plan contrasts are no longer significant once refund is included, that the CIs are wide, and that the model is near-separated. It also states that absence of significance is not evidence of no plan effect, and that refund mix is a plausible explanation for the basic-plan gap.

![Logit average marginal effects of plus and pro versus basic on churn probability, adjusted for usage_hours and tenure_months, with refund_issued excluded and included](tasks/stat_4/charts/stat4_refund_sensitivity_ame.png)

### Firth penalized logit with refund included (stat_5)

- **plus vs basic:** OR 0.80 (95% CI 0.32 to 1.99), penalized LR p = 0.19.
- **pro vs basic:** OR 0.44 (95% CI 0.16 to 1.26), penalized LR p = 0.067.
- Neither is significant at 0.05.
- Covariates: usage_hours OR 0.924 (penalized LR p = 8e-06); tenure_months OR 0.985 (penalized LR p = 0.0007); refund_issued OR 1359.4 (penalized LR statistic 972).
- The unpenalized logit gives plus OR 0.80 (p = 0.65) and pro OR 0.44 (p = 0.14), so penalization does not change the conclusion.
- For pro, the penalized LR p (0.067) and the Wald p (0.127) differ. The finding calls the pro result borderline. The Firth CIs are Wald-based.

![Odds ratios of churn vs basic plan with refund_issued in the model: Firth penalized (blue) vs unpenalized logit (orange), 95% CI](tasks/stat_5/charts/firth_vs_unpenalized_or.png)

## Limitations

- **Unresolved leakage question (open review issue).** The data cannot show whether refund_issued is recorded before or after cancellation. My objection stands: refund_issued must not be treated as a causal driver or a legitimate predictor until this is resolved. This affects every finding that includes refund_issued: the EDA, stat_1, stat_2 (including the usage_hours × refund_issued result), ml_1, stat_4 and stat_5.
- **Refund-excluded models do not beat the baseline.** The no-refund logistic regression and gradient boosting models score below the majority baseline on the test split. This does not show that no feature predicts churn.
- **Overfitting.** The no-refund gradient boosting model has train accuracy 0.796 against test accuracy 0.570. The finding considers its test result unreliable.
- **Small test split.** All model scores come from a single 200-row test split. Permutation importance rankings disagree and fall within noise.
- **Near-separation.** refund_issued separates churners almost perfectly (10 churners among 632 refund-0 rows). This makes the usage_hours × refund_issued interaction (p = 0.049) and the refund-included plan estimates unstable.
- **Plan effects are not causal.** The refund-excluded plan gaps are conditional only on usage_hours and tenure_months. The refund-included estimates are sensitivity checks, and refund mix may account for the basic-plan gap.
- **Hypothesis not tested directly.** The claim that refund mix drives basic's higher churn is a hypothesis. stat_4 is consistent with it but does not establish it.
- **Pro result is borderline.** The pro plan p-values differ between penalized LR (0.067) and Wald (0.127) methods.
- No task failed. Every task reported status complete, and the review issues above are the only unresolved items.

## Open questions

- Is refund_issued recorded before or after cancellation? If after, it is leakage and should be excluded from predictive models and from the plan analysis.
- Do event dates for refunds and churn exist, so refund timing can be modelled explicitly to separate refund effects from plan effects?
- Why are basic customers refunded more often (43.2% versus 29.3% for plus and 31.4% for pro)?
- Does basic's higher churn persist after adjusting for usage_hours, tenure_months and refund_issued together, with a sensitivity model that includes refund? (stat_4 partly addresses this, but the estimates are near-separated.)
- Which features predict churn among refund_issued=0 customers (10 churners of 632)?
- Do the no-refund results hold under cross-validation rather than a single 200-row split?
- Would tuning the gradient boosting model without refund_issued (fewer trees, shallower depth, subsampling) reduce overfitting, and would the permutation importance then agree with the built-in importance?
- Would richer behavioural features, such as usage trends, carry predictive signal that the current features do not?
- Do usage_hours and tenure_months keep independent effects on churn once plan is accounted for, with refund excluded?