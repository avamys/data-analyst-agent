# Customer Churn Analysis: Drivers of churned_flag in 800 Customers

## Summary

- **Monthly contracts churn more than annual ones.** Churn is 37.3% for monthly contracts versus 21.2% for annual (chi-square p=1.76e-6, Cramer's V=0.169). The difference stays significant after Bonferroni correction across four tests, and the adjusted odds ratio for monthly contract is 2.36 (95% CI 1.67 to 3.34).
- **Monthly fee and support calls are both associated with churn, and both associations survive adjustment.** Churners pay higher fees (mean 79.94 vs 66.12, Mann-Whitney p=4.4e-10) and make more support calls (mean 1.84 vs 1.34, p=8.5e-7). In a multivariable logit, the adjusted OR is 1.19 per 10 units of fee and 1.46 per additional support call.
- **Region is not significantly associated with churn.** Rates range from 27.5% to 34.5% across regions, but the chi-square test gives p=0.448.
- **Contract does not significantly modify the effects of fee or support calls.** The interaction tests give p=0.734 (support calls), p=0.128 (fee, binned) and p=0.730 (fee, continuous). The binned fee analysis and the continuous fee analysis disagree in their odds-ratio pattern, and this is reported below without resolution.
- **The model beats the majority-class baseline only modestly.** Logistic regression reaches 72.5% test accuracy against a 68.75% baseline, with balanced accuracy 0.615 vs 0.5 and ROC AUC 0.712 (bootstrap 95% CI 0.617 to 0.797). The random forest does worse than logistic regression (test accuracy 65.0%, ROC AUC 0.626).

## Data

- **Size:** 800 rows and 5 columns.
- **Target:** `churned_flag`, binary. 31.2% yes (250 customers) and 68.8% no. The classes are imbalanced.
- **Features:** Numeric: `monthly_fee`, `support_calls`. Categorical: `contract`, `region`.
- **Date/time features and identifier or free-text columns:** none.
- **Missing values:** none in any column (zero-missing check reported in the EDA). No imputation was needed.

## Findings

### Overall churn and descriptive patterns

Overall churn is 31.25% (250 of 800). Churn rates and feature averages vary across contract, region, and binned fee and support-call levels as follows.

- **Contract:** Monthly contracts churn at 37.3% (186 of 498). Annual contracts churn at 21.2% (64 of 302).
- **Region:** South 27.5% (55 of 200), east 30.2% (65 of 215), north 33.0% (63 of 191), west 34.5% (67 of 194).
- **Monthly fee, by quartile:** Q1 17.5%, Q2 28.5%, Q3 34.5%, Q4 44.5%. Churn rises with each quartile.
- **Support calls:** 22.6% at 0 calls, 26.4% at 1, 34.5% at 2, 39.2% at 3, 50.0% at 4. Levels 5 and above rest on very few customers: 5 calls is 90.9% churn (10 of 11), 6 calls is 0 of 1, and 7 calls is 1 of 1.
- **Class means:** Churned customers average 79.94 monthly fee and 1.84 support calls. Retained customers average 66.12 and 1.34.

![Churn rate (%) by contract type (left) and by monthly_fee quartile (right)](tasks/eda_1/charts/churn_rate_contract_fee.png)

### Statistical significance and effect sizes

**Contract.** Churn differs significantly by contract type: chi-square(1)=22.84, p=1.76e-6, Bonferroni-adjusted p=7.0e-6 across four tests, Cramer's V=0.169. The 95% Wilson intervals are 33.2% to 41.7% for monthly (186 of 498) and 17.0% to 26.1% for annual (64 of 302).

**Region.** Churn does not differ significantly by region: chi-square(3)=2.66, p=0.448 (Bonferroni p=1.0), Cramer's V=0.058. The 95% Wilson intervals are 21.8% to 34.1% for south, 24.5% to 36.7% for east, 26.7% to 39.9% for north, and 28.2% to 41.5% for west. The intervals overlap heavily.

![Churn rate (%) by region with Wilson 95% CI in data table](tasks/stat_1/charts/churn_rate_region_ci.png)

**Monthly fee.** Churners pay significantly higher fees: Mann-Whitney U=87649.5, p=4.4e-10 (Bonferroni p=1.8e-9), rank-biserial r=0.275. The mean difference is 13.82 (95% CI 9.68 to 17.96).

**Support calls.** Churners make significantly more support calls: Mann-Whitney U=83116.5, p=8.5e-7 (Bonferroni p=3.4e-6), rank-biserial r=0.209. The mean difference is 0.50 (95% CI 0.31 to 0.68).

With Bonferroni correction across the four tests, contract, fee and support calls remain significant, and region does not. Effect sizes are small to moderate.

### Interactions between contract and the other features

**Support calls.** Contract does not significantly modify the effect of support calls: LR chi-square(1)=0.115, p=0.734.
- Low bin (≤1 calls): monthly churn is 30.6% (87 of 284) and annual is 15.2% (25 of 164). OR 2.46 (95% CI 1.50 to 4.03).
- High bin (≥2 calls): monthly churn is 46.3% (99 of 214) and annual is 28.3% (39 of 138). OR 2.19 (95% CI 1.38 to 3.45).

**Monthly fee, binned at the median.** Contract does not significantly modify the effect of fee at the 0.05 level: LR chi-square(1)=2.32, p=0.128.
- Low-fee bin (≤ median): monthly churn is 26.3% (65 of 247) and annual is 17.6% (27 of 153). OR 1.67 (95% CI 1.01 to 2.76).
- High-fee bin: monthly churn is 48.2% (121 of 251) and annual is 24.8% (37 of 149). OR 2.82 (95% CI 1.80 to 4.40).

The fee-bin point estimates differ more than the support-call estimates, but the test does not support a real interaction.

**Overall reading of stat_2.** No significant contract interaction appears with either support calls or binned fee. The monthly-versus-annual gap can therefore be described as a common effect, with odds ratios of about 2.2 to 2.5 across the support-call bins.

![Churn rate (%) by contract type within low and high support_calls (low = <=1) and monthly_fee (low = <= median) bins](tasks/stat_2/charts/stat2_churn_by_contract_bins.png)

**Disagreement on the fee pattern.** The binned fee analysis (stat_2) and the continuous fee analysis (stat_4) do not agree on the shape of the contract effect across fee levels.
- stat_2 shows odds ratios of 1.67 in the low-fee bin and 2.82 in the high-fee bin.
- stat_4 models fee continuously and finds monthly-vs-annual odds ratios of 2.10 at the 25th percentile fee (45.19), 2.22 at the median (71.20) and 2.34 at the 75th percentile (96.99). The interaction is non-significant (LR chi-square(1)=0.119, p=0.730).

stat_4 reports that the continuous analysis does not reproduce the binned pattern. The fee-bin difference is not supported as a real interaction, though it is not ruled out. The two results are reported side by side here and are not reconciled.

**Continuous fee with support calls included.** The null result holds when support calls are also continuous: LR chi-square(1)=0.142, p=0.706. Support calls remain a positive predictor (coefficient 0.378 per call).

### Adjusted associations (multivariable logit)

The model includes monthly contract, monthly fee and support calls (n=800). Region was excluded because it was not significant in stat_1.

- **Monthly fee:** adjusted coefficient 0.0176 per unit (p=1.0e-9), OR 1.018 per unit (95% CI 1.012 to 1.024). Per 10 units, the adjusted OR is 1.19 (95% CI 1.13 to 1.26).
- **Support calls:** adjusted coefficient 0.377 (p=3.5e-8), OR 1.458 per call (95% CI 1.275 to 1.668).
- **Monthly contract:** adjusted OR 2.36 (95% CI 1.67 to 3.34), p=1.2e-6.

Adjustment does not shrink either main effect. Compared with univariate logit fits, the fee coefficient moves from 0.0171 to 0.0176 (+2.9%), and the support-call coefficient moves from 0.350 to 0.377 (+7.8%). The associations are conditional on the other predictors in the model and are not causal estimates.

### Predictive model vs. majority-class baseline

Models were fit on a single stratified 80/20 split (random_state 42). The training set has 640 rows. The test set has 160 rows, 50 of them churners. Features were monthly_fee, support_calls, contract and region (one-hot).

| Model | Test accuracy | Balanced accuracy | ROC AUC (bootstrap 95% CI) | F1 (yes) | Test confusion [rows true no/yes; cols pred no/yes] |
|---|---|---|---|---|---|
| Majority-class baseline | 68.75% | 0.500 | n/a | n/a | n/a (never predicts churn) |
| Logistic regression | 72.5% | 0.615 | 0.712 (0.617 to 0.797) | 0.421 | [[100, 10], [34, 16]] |
| Random forest | 65.0% | 0.571 | 0.626 (0.529 to 0.716) | 0.391 | [[86, 24], [32, 18]] |

- Logistic regression has test precision 0.615 and recall 0.32 for churners. It catches 16 of 50 churners.
- The random forest reaches training accuracy 1.0 and its test accuracy is below the baseline. It overfits.
- The logistic regression ROC AUC interval is wide.

### Feature importance

- **Logistic regression (standardized coefficient magnitudes):** monthly_fee 0.4975, contract_monthly 0.4636, support_calls 0.4522. These three are similar. The largest region term is south at 0.1033, followed by west at 0.0271 and north at 0.008.
- **Random forest impurity importance:** monthly_fee 0.7589, support_calls 0.1383, contract_monthly 0.0451. Region terms are 0.019 or lower.
- **Random forest permutation importance (mean drop in test ROC AUC):** support_calls 0.0757, monthly_fee 0.0513, contract_monthly 0.0429. Region terms are negative (west -0.0054, south -0.011, north -0.0184).

The impurity and permutation rankings disagree on the top feature. Monthly fee ranks first under impurity importance, and support calls ranks first under permutation importance. The three main features (monthly_fee, support_calls, contract_monthly) form the top group under both measures, but their order is not agreed. The region permutation values are consistent with stat_1's finding that region is not significant.

![Random forest permutation importance (mean drop in test ROC AUC) by feature](tasks/ml_1/charts/ml1_feature_importance.png)

## Limitations

- **Data source for ml_1.** The ml_1 models used the df fallback because the eda_1 clean feature table does not contain `churned_flag`. df was verified to contain the target (250 yes, 800 rows), so the models used the correct target, but the source path differs from the EDA table.
- **Small test set.** The test set has only 50 churners. Model rankings and scores may shift on a different split. The logistic regression ROC AUC interval (0.617 to 0.797) is wide.
- **Weak random forest.** The random forest overfits (training accuracy 1.0) and performs below the baseline on accuracy. Its importance values should be read with that in mind.
- **Feature-importance conclusion is tentative.** The main predictors are identified as a group, not as a firm order.
- **Sparse high support-call levels.** Support-call values of 5 and above total 13 customers (11 at 5, 1 at 6, 1 at 7). The linear support-call effect is driven mostly by values 0 to 4, and the high-count tail is unreliable.
- **Linearity not checked.** Linearity of monthly_fee and support_calls on the logit scale was assumed, not tested.
- **Fee-pattern disagreement.** The binned analysis (stat_2) and the continuous analysis (stat_4) disagree on the contract-by-fee pattern. The interaction is not significant in either test.
- **Associational, not causal.** All adjusted estimates are conditional on the other predictors and do not establish causes.
- **Region excluded from the adjusted model.** Region was dropped from the multivariable logit because it was not significant in stat_1.
- **Unadjusted region comparison.** The region chi-square test is unadjusted and was tested across four comparisons, with a Bonferroni p of 1.0.
- **Bonferroni scope.** Corrections in stat_1 cover four tests. The stat_2 and stat_4 interaction tests are reported without a stated multiple-comparison adjustment.
- **Failed tasks and unresolved review issues.** None recorded.

## Open questions

- Do monthly_fee, support_calls and contract remain the top predictors under repeated stratified cross-validation, given only 50 churners in the test set?
- Would a shallower or regularized random forest, or gradient boosting, beat logistic regression on ROC AUC?
- Is the fee-bin difference in the monthly-vs-annual odds ratio (1.67 vs 2.82) real when fee is modelled continuously? The continuous analysis does not reproduce it.
- Is the fee effect linear on the logit scale, or do a spline or binned-fee model fit better?
- Is the nonlinearity of monthly_fee hiding a contract-specific shape that a linear fee term misses?
- Is the monthly-versus-annual churn gap explained by fee level, given that fee is higher among churners?
- Should support_calls values of 5 and above be pooled, or is the support-call effect linear across its range?
- Do monthly_fee and support_calls remain predictive after controlling for contract, with calibration checked?