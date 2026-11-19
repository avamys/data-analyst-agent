# Customer Churn Analysis (churned_flag) of 800 Customers

## Summary

- **Contract, monthly_fee and support_calls are each significantly associated with churn; region is not.** Monthly contracts churned at 37.3% versus 21.2% for annual contracts (chi-square 22.84, Holm-adjusted p = 3.5e-6, Cramér's V = 0.169). Region's Holm-adjusted p is 0.448.
- **The contract association holds after adjustment.** In a multivariable logistic regression adjusted for region, monthly_fee and support_calls, monthly vs annual has an adjusted OR of 2.39 (95% CI 1.68 to 3.38).
- **Monthly_fee shows the largest unadjusted effect of the four tests.** Churners' mean fee was 79.9 versus 66.1 for non-churners (Mann-Whitney Holm-adjusted p = 1.8e-9, rank-biserial 0.275). Churn rose across every monthly_fee quartile, from 17.5% to 44.5%.
- **Logistic regression beats the majority-class baseline on the 160-row test set.** Balanced accuracy was 0.6145 versus 0.5, and ROC AUC was 0.712 versus 0.5. Gradient boosting overfit (train accuracy 0.8187, test accuracy 0.6937) and had a lower ROC AUC (0.6596). No interval or test was computed for the difference between the models.
- **No contract interaction was detected at the 0.05 level.** The contract-by-fee and contract-by-support_calls likelihood-ratio test gave p = 0.83, and the region-by-contract test gave p = 0.81. Stratified churn rates, however, differ across monthly_fee halves. The formal tests and the stratified rates point in different directions, and this report does not resolve the disagreement.

## Data

- **Size:** 800 rows, 5 columns. Numeric features: monthly_fee, support_calls. Categorical features: contract, region. No date/time features and no identifier or free-text columns.
- **Target:** churned_flag, imbalanced. 250 yes (31.25%) and 550 no (68.75%).
- **Missing values:** none. Zero missing values were found in every column, both in the raw file read as text (no NA filling) and in the loaded DataFrame, and the two counts matched.

## Findings

### Churn rates by group (exploratory)

- Overall churn is 31.25% (250 of 800).
- **Contract:** monthly 37.3% yes (n=498); annual 21.2% yes (n=302).
- **Region:** south 27.5% (n=200), east 30.2% (n=215), north 33.0% (n=191), west 34.5% (n=194).
- **monthly_fee quartiles:** 17.5% (n=200), 28.5% (n=200), 34.5% (n=200), 44.5% (n=200). Churn rises at every step, including through the top bin.
- **support_calls quartiles (rank-based):** 22.0%, 26.0%, 32.5%, 44.5%. Tied values are split across bins, so these are not pure per-value rates.

![Churn rate (% yes) by contract (left) and by support_calls quartile (right)](tasks/eda_1/charts/churn_rate_contract_support.png)

**Per-value support_calls rates (exact, no tie splitting):** 22.56% at 0 (37 of 164), 26.41% at 1 (75 of 284), 34.47% at 2 (71 of 206), 39.18% at 3 (38 of 97), 50.00% at 4 (18 of 36), and 90.91% at 5 (10 of 11). Values 6 and 7 have n=1 each and are not informative. Grouped as 0, 1, 2, 3+, churn is 22.56%, 26.41%, 34.47% and 45.89% (67 of 146). The per-value rates confirm the rank-based trend in direction and approximate level.

![Churn rate (% yes) by distinct support_calls value (left) and by grouped 0, 1, 2, 3+ (right)](tasks/eda_3/charts/churn_rate_by_support_calls.png)

### Significance tests and effect sizes (unadjusted)

Holm correction was applied across the four tests.

- **Contract:** chi-square 22.84 (df 1), raw p = 1.8e-6, Holm-adjusted p = 3.5e-6, Cramér's V = 0.169. Churn was 37.3% (95% Wilson CI 33.2 to 41.7) for monthly and 21.2% (95% CI 17.0 to 26.1) for annual.
- **Region:** chi-square 2.66 (df 3), raw p = 0.448, Holm-adjusted p = 0.448, Cramér's V = 0.058. Per-region Wilson CIs overlap heavily: east 30.2% (24.5 to 36.7), north 33.0% (26.7 to 39.9), south 27.5% (21.8 to 34.1), west 34.5% (28.2 to 41.5).
- **monthly_fee:** Mann-Whitney raw p = 4.4e-10, Holm-adjusted p = 1.8e-9, rank-biserial 0.275. Mean fee was 79.9 for churners and 66.1 for non-churners, a difference of 13.8 (95% CI 9.7 to 18.0). This is the largest of the four effects.
- **support_calls:** Mann-Whitney raw p = 8.5e-7, Holm-adjusted p = 2.6e-6, rank-biserial 0.209. Mean calls were 1.84 for churners and 1.34 for non-churners, a difference of 0.50 (95% CI 0.31 to 0.69).

Contract, monthly_fee and support_calls remain significant after Holm correction at the 0.05 level. Region does not.

![Churn rate (% yes) with 95% Wilson CI by contract (left) and region (right)](tasks/stat_1/charts/stat1_churn_rate_ci.png)

### Adjusted association (multivariable logistic regression, n=800, 250 churners)

Adjusted for the other terms in the model:

- **Contract (monthly vs annual):** OR 2.39 (95% CI 1.68 to 3.38), p ≈ 1.0e-6. The adjusted OR is somewhat larger than the crude difference, so adjustment does not explain the contract effect away.
- **monthly_fee (per unit):** OR 1.018 (95% CI 1.012 to 1.024), p ≈ 1.1e-9.
- **support_calls (per additional call):** OR 1.46 (95% CI 1.28 to 1.67), p ≈ 2.9e-8.
- **Region (vs east):** north OR 1.12 (95% CI 0.72 to 1.75), p = 0.613; south OR 0.77 (95% CI 0.49 to 1.21), p = 0.254; west OR 1.08 (95% CI 0.69 to 1.68), p = 0.731. No region differs from east.

### Interactions and stratified rates

- **Stratified rates by contract, monthly_fee median split:** within the low-fee half, annual 17.6% (n=153) vs monthly 26.3% (n=247). Within the high-fee half, annual 24.8% (n=149) vs monthly 48.2% (n=251).
- **Stratified rates by contract, support_calls median split:** low calls, annual 15.2% (n=164) vs monthly 30.6% (n=284); high calls, annual 28.3% (n=138) vs monthly 46.3% (n=214).
- **Likelihood-ratio tests:** contract with monthly_fee and support_calls gave LR = 0.369 (df 2), p = 0.83. Region with contract gave LR = 0.973 (df 3), p = 0.81.
- **Interaction odds ratios:** contract (monthly) by monthly_fee OR 1.002 (95% CI 0.990 to 1.015). Contract (monthly) by support_calls OR 1.078 (95% CI 0.808 to 1.437).

The formal tests support no interaction at the 0.05 level and do not rule out a modest one. The stratified rates differ across monthly_fee halves, with a contract gap in churn rate that is visibly larger in the high-fee half. The stratified rates and the formal tests disagree, and this report does not resolve that disagreement.

![Churn rate (%) by contract within low and high monthly_fee and support_calls groups](tasks/stat_2/charts/stat2_churn_by_contract_strata.png)

### Predictive models (shared stratified 80/20 split, random_state=42)

- **Split:** 640 training and 160 test rows, with churn at 31.25% in both.
- **Feature matrix:** monthly_fee and support_calls (standardised, scaler fitted on training rows), plus one-hot contract and region columns (encoder fitted on training rows).
- **Majority-class baseline** (always predict no churn): test accuracy 0.6875, balanced accuracy 0.5, ROC AUC 0.5.
- **Logistic regression:** test accuracy 0.725, balanced accuracy 0.6145, ROC AUC 0.712, F1 for yes 0.4211, precision 0.615, recall 0.32. Train accuracy was 0.7281. This is a point estimate; no confidence interval or significance test was computed.
- **Gradient boosting:** test accuracy 0.6937, balanced accuracy 0.5973, ROC AUC 0.6596, precision 0.515, recall 0.34, F1 0.4096. Train accuracy was 0.8187 against test accuracy 0.6937, so its test performance is not a reliable estimate of generalisation.
- **Feature importance:** monthly_fee and support_calls matter most in both models. Permutation drops in test ROC AUC were 0.0907 (monthly_fee) and 0.0706 (support_calls) for logistic regression, and 0.0886 and 0.0564 for gradient boosting. Region permutation values for logistic regression are close to zero. Gradient boosting's importance for monthly_fee is 0.7077.
- **Permutation of contract:** permutation of one contract dummy is uninformative because the other dummy carries the same information, so the contract effect cannot be assessed this way. Contract's association with churn is established by the statistical tests and the adjusted model above.

![Test balanced accuracy of logistic regression and gradient boosting vs majority-class baseline](tasks/ml_2/charts/ml2_balanced_accuracy.png)

## Limitations

- **No missing values to handle.** Missingness was checked in the raw file and the loaded data, and none was found. Missingness therefore could not be related to other columns or to churned_flag. The check should be rerun if the data is refreshed.
- **Associations, not causes.** All results describe association with churned_flag in this sample. The tests and models do not establish mechanisms.
- **Region is not significant** in either the unadjusted or the adjusted analysis. Its effect is not distinguished from zero at this sample size.
- **Interaction tests may lack power.** The interaction tests do not rule out modest interactions. The stratified rates differ across monthly_fee halves, but no test confirms an interaction.
- **Small test set.** The 160-row test set holds only about 50 churners. No cross-validation or repeated splits were run, so the stability of ROC AUC and balanced accuracy is unknown.
- **Model comparison is unquantified.** No confidence interval or significance test was computed for the difference between logistic regression and gradient boosting, so the difference cannot be judged from this report.
- **Gradient boosting overfits** (train accuracy 0.8187 vs test accuracy 0.6937). No tuning was reported.
- **support_calls quartile rates** in eda_1 split tied values across bins and are not pure per-value rates. The per-value and grouped rates in eda_3 are used for the trend instead.
- **Sparse high support_calls values.** Values 4 to 7 have small counts (n=36, 11, 1, 1), so rates at those values are unstable.
- **Linearity assumed.** The logistic model treats monthly_fee and support_calls as linear on the logit scale. This was not checked.
- **Unresolved review issue (ml_2), restated as the lead required.** Permutation of one contract dummy is uninformative because the other dummy carries the same information. The contract effect cannot be assessed by permutation importance. Contract's association with churn is established by the statistical tests (stat_1) and the stratified and adjusted analyses (stat_2, stat_3).
- **Unresolved review issue (ml_2), second point.** No interval or test was computed for the difference between the two models, so whether that difference is meaningful cannot be judged from this report.
- All tasks in the record are marked complete. None failed.

## Open questions

- Does the contract effect persist in a model without collinear dummies, or with a likelihood-ratio test? (The adjusted model in stat_3 partly addresses this, with contract coded as a single term.)
- Is the monthly_fee effect linear on the logit scale?
- Does the support_calls effect hold when grouped as 0, 1, 2, 3+ within a multivariable model, and is the rise at 3+ statistically significant given the small counts at values 4 to 7?
- Is there an interaction between contract and support_calls or monthly_fee that the current tests cannot detect? The stratified rates across monthly_fee halves suggest this should be examined further.
- Do cross-validation or repeated stratified splits give stable intervals for ROC AUC and balanced accuracy?
- Would tuning gradient boosting to reduce its train-test gap change its ranking against logistic regression?