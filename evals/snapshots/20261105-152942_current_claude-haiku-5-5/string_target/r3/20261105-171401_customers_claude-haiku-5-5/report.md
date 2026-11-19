# Churn Analysis of an 800-Customer Dataset: Contract, Fee, Support Calls and Model Performance

## Summary

- **Churn is a minority outcome, and contract type is the clearest difference.** 250 of 800 customers churned (31.25%). Monthly-contract customers churned at 37.35% (186 of 498), against 21.19% (64 of 302) for annual contracts. The difference is significant (chi-square 22.84, df 1, p = 1.8e-06; Cramér's V 0.169), with a monthly-minus-annual difference of 16.2 percentage points (95% CI 9.9 to 22.4).
- **Region is not significantly associated with churn** (chi-square 2.66, df 3, p = 0.448). Churn rates range from 27.50% (south) to 34.54% (west), but no pairwise comparison is significant after Bonferroni correction.
- **Churned customers pay higher fees and make more support calls, and both associations remain after adjusting for contract.** Median monthly fee is 82.92 for churned versus 63.34 for retained customers (Mann-Whitney p = 4.4e-10, rank-biserial 0.275). Median support calls are 2.0 versus 1.0 (p = 8.5e-07, rank-biserial 0.209). In a logistic model adjusted for contract, the odds ratio is 1.19 per 10 currency units of fee and 1.46 per additional call.
- **Contract does not significantly modify the fee or calls effects, but the data are too imprecise to show that the effects are equal.** The interaction p-values are 0.69 (fee) and 0.71 (calls), with wide confidence intervals.
- **Logistic regression beats the majority-class baseline in repeated cross-validation.** Its balanced accuracy is 0.599 against 0.500, and it beats the baseline in all 25 folds. Gradient boosting also beats the baseline, by less, and its training accuracy (0.8187) well above its test accuracy (0.6937) points to overfitting. On the single 160-row test split, the logistic model's accuracy is 0.7188 against 0.6875 for the baseline.

## Data

- **Size:** 800 rows, 5 columns.
- **Target:** `churned_flag` (binary). 550 customers were retained (68.75%) and 250 churned (31.25%), so the classes are imbalanced.
- **Features:** numeric `monthly_fee` and `support_calls`; categorical `contract` and `region`. There are no date/time features and no identifier or free-text columns.
- **Missing values:** none in any column, so no imputation was needed.

## Findings

### Churn by contract and region

Churn is higher for monthly contracts than for annual contracts. Churn rates across regions are similar.

- **Contract:** Monthly contracts churned at 37.35% (186 of 498) and annual contracts at 21.19% (64 of 302). The chi-square test of independence gives chi-square 22.84 (df 1), p = 1.8e-06, Cramér's V = 0.169, a small-to-moderate association. The monthly-minus-annual difference is 16.2 percentage points (95% Wald CI 9.9 to 22.4).

  ![Churn rate (%) by contract and by region](tasks/eda_1/charts/churn_rate_by_contract_and_region.png)

  ![Churn rate (%) with 95% Wald CI by contract and by region; churned = yes](tasks/stat_1/charts/churn_rate_by_contract_region_ci.png)

- **Region:** Churn rates were 30.23% for east (65 of 215), 32.98% for north (63 of 191), 27.50% for south (55 of 200) and 34.54% for west (67 of 194). The chi-square test gives chi-square 2.66 (df 3), p = 0.448, Cramér's V = 0.058. Pairwise region differences are small, and their 95% CIs include zero. Bonferroni-corrected p-values over the six pairs are not significant (the smallest, south–west, is 0.78).

### Monthly fee and support calls compared with churn

- **Monthly fee:** Churned customers have a mean fee of 79.94 (median 82.92) and retained customers 66.12 (median 63.34). The Mann-Whitney test gives p = 4.4e-10 (Bonferroni over four tests: 1.8e-09), with rank-biserial 0.275 (bootstrap 95% CI 0.196 to 0.356), a small-to-medium effect. These are unadjusted results.
- **Support calls:** Churned customers have a mean of 1.84 calls (median 2.0) and retained customers 1.34 (median 1.0). The Mann-Whitney test gives p = 8.5e-07 (Bonferroni over four tests: 3.4e-06), with rank-biserial 0.209 (bootstrap 95% CI 0.125 to 0.294), a small effect. These are also unadjusted results.

### Fee and contract

- **Fee by contract:** Monthly contracts have a mean fee of 70.99 (median 71.41, n = 498) and annual contracts 69.53 (median 70.23, n = 302), a difference of about 1.5 in means. No significance test was run on this difference.
- **Fee by churn within contract:** The churned-versus-retained gap is present within each contract level. Among monthly contracts, churned customers have a mean fee of 80.18 (median 83.35, n = 186) and retained customers 65.51 (median 62.31, n = 312). Among annual contracts, churned customers have a mean of 79.22 (median 81.96, n = 64) and retained customers 66.93 (median 68.05, n = 238). These are descriptive results, and no test was run.

  ![Mean monthly fee by contract level and churn status (retained vs churned)](tasks/eda_2/charts/fee_by_contract_and_churn.png)

### Adjusted associations with churn (logistic regression)

- **Monthly fee:** After adjusting for contract type, the odds ratio is 1.19 per 10 currency units (95% CI 1.13 to 1.26), p = 1.0e-09.
- **Support calls:** After adjusting for contract type, the odds ratio is 1.46 per additional call (95% CI 1.28 to 1.67), p = 3.5e-08.
- **Monthly contract:** After adjusting for fee and support calls, the monthly-versus-annual odds ratio is 2.36 (95% CI 1.67 to 3.34), p = 1.2e-06.
- **Model fit:** The model has n = 800 and a McFadden pseudo R-squared of 0.096, so the predictors explain a modest share of churn variation.

The fee and support-call associations do not disappear after adjusting for contract. The unadjusted and adjusted results are on different scales and are not directly comparable, so the size of the change is only qualitative.

### Interactions between contract and fee or calls

A second logistic specification includes interaction terms, with monthly contracts as the reference group and fee and calls centred.

- **Fee interaction:** The annual × fee interaction has coefficient −0.025, OR 0.98 (95% CI 0.86 to 1.10), p = 0.69. Contract does not significantly modify the fee effect.
- **Calls interaction:** The annual × calls interaction has coefficient −0.054, OR 0.95 (95% CI 0.71 to 1.26), p = 0.71. Contract does not significantly modify the calls effect.
- **Interpretation:** The interaction confidence intervals are wide, so the data do not rule out moderate differences between monthly and annual contracts in either effect. The non-significant results are not evidence that the effects are equal, and the effects should not be described as similar.
- **Main effects in this specification (monthly reference group):** Holding contract constant, the odds ratio is 1.20 per 10 units of fee (95% CI 1.12 to 1.29, p = 1e-07) and 1.48 per additional support call (95% CI 1.26 to 1.75, p = 2e-06). The model does not establish how these effects differ for annual contracts.
- **Annual contract:** At average fee and calls, annual contracts have lower churn odds than monthly contracts (OR 0.43, 95% CI 0.30 to 0.62, p = 5e-06), so contract remains a strong predictor after adjusting for fee and calls.

### Predictive models against the majority-class baseline

The majority-class baseline always predicts "no" and has test accuracy 0.6875. The data were split 80/20, stratified, with random_state = 42. The split gives 640 training rows and 160 test rows, with a test churn rate of 0.3125. The scaler was fit on the training rows only.

**Single test split (160 rows):**

| Model | Test accuracy | Balanced accuracy | ROC AUC | Precision | Recall | F1 | Train accuracy |
|---|---|---|---|---|---|---|---|
| Majority baseline | 0.6875 | 0.50 | n/a | n/a | n/a | n/a | n/a |
| Logistic regression | 0.7188 | 0.61 | 0.7124 | 0.5926 | 0.32 | 0.4156 | 0.7281 |
| Gradient boosting | 0.6937 | 0.5973 | 0.6596 | 0.5152 | 0.34 | 0.4096 | 0.8187 |

- Logistic regression's test accuracy is 0.7188 against 0.6875, a gain of about 5 of 160 test rows. These are single-split estimates and should be read with caution.
- Gradient boosting's test accuracy (0.6937) is essentially equal to the baseline, a difference of one test row. Its training accuracy (0.8187) against test accuracy (0.6937) points to overfitting. Its balanced accuracy (0.5973) and ROC AUC (0.6596) are below logistic regression's (0.61 and 0.7124).

  ![Balanced accuracy and F1 on the 20% test split for the majority baseline, logistic regression and gradient boosting](tasks/ml_1/charts/ml1_model_comparison.png)

**Permutation importance (drop in test ROC AUC, 30 repeats):**

- Logistic regression: monthly_fee 0.0913, support_calls 0.0707, contract_annual 0.0252.
- Gradient boosting: monthly_fee 0.0886, support_calls 0.0565, contract_annual 0.0382.
- The region indicators contribute almost nothing. The largest mean region importance is 0.0052 (south) for logistic regression and 0.0030 (west) for gradient boosting. Some region values are negative.

**Repeated stratified 5-fold cross-validation (25 folds):**

- **Logistic regression:** Balanced accuracy is 0.599 (SD 0.026) against 0.500 for the baseline. The per-fold gain averages 0.099 (SD 0.026, range 0.055 to 0.149) and is positive in all 25 folds. ROC AUC is 0.698 (SD 0.036). F1 is 0.381 (SD 0.058), against 0 for the baseline, which never predicts churn.

  ![Balanced accuracy across 25 repeated stratified CV folds for the majority baseline, logistic regression and gradient boosting](tasks/ml_2/charts/ml2_cv_balanced_accuracy.png)

- **Gradient boosting:** Balanced accuracy is 0.566 (SD 0.032), a per-fold gain of 0.066 (SD 0.032) over the baseline, positive in all 25 folds. ROC AUC is 0.634 (SD 0.034) and F1 is 0.336 (SD 0.061). Both are below logistic regression's means on the same folds.

The single-split balanced accuracy (0.61 for logistic regression against 0.50 for the baseline) is consistent with the cross-validated gain of 0.099, though the single-split estimate is less precise.

## Limitations

- **Sample size and precision:** The dataset has 800 rows. The 160-row test split gives imprecise model estimates, and the findings say so explicitly. The interaction confidence intervals are wide.
- **Associations only:** All results describe associations in a cross-sectional dataset. The findings do not establish causes or mechanisms.
- **Unadjusted tests:** The Mann-Whitney results for fee and support calls are unadjusted for contract. The rank-biserial values for the two variables are not directly comparable.
- **Fee and contract:** The statement that contract does not explain the higher fee among churned customers rests on descriptive means (eda_2). No test was run, and no regression of fee on contract was fitted.
- **Monthly–annual difference within regions:** This was not tested. The pairwise region tests compare churn rates across all contracts.
- **Model fit:** The logistic model's pseudo R-squared is 0.096, so the predictors explain a modest share of churn variation.
- **Model comparison:** Gradient boosting was evaluated with the settings used in the analysis; the findings do not show whether tuning would change its gap to logistic regression.
- **Class imbalance:** The target is imbalanced (31.25% churn). Accuracy alone is misleading here, so balanced accuracy, ROC AUC and F1 are reported alongside it.
- **Review issues:** No unresolved review issues are recorded. The ML figures above are the corrected versions, with the scaler fit on training rows only.
- **Failed tasks:** None recorded.

## Open questions

- Is the monthly-versus-annual churn difference statistically significant within each region?
- Is the higher fee among churned customers explained by contract type? The current evidence is descriptive, and no regression of fee on contract has been fitted.
- Do the fee and support-call effects differ between monthly and annual contracts? A joint likelihood-ratio test of both interactions has not been run, so the joint result is not known.
- Do the fee and support-call effects differ by region after adjusting for contract?
- Would tuning gradient boosting regularisation close its gap to logistic regression across the repeated folds? A paired test on the per-fold balanced-accuracy differences has not been run.
- Is the churn-fee relationship different by region?