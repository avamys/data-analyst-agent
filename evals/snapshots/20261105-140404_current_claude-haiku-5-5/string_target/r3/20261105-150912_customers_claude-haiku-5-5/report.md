# Churn Analysis of an 800-Row Dataset (Target: churned_flag)

## Summary

- **Contract type is the clearest categorical difference.** Monthly contracts churn at 37.3% (n=498) versus 21.2% for annual contracts (n=302). The association is significant (chi-square 22.84, df 1, p = 1.8e-06, Cramér's V 0.169). After adjusting for monthly_fee and support_calls, the monthly-vs-annual odds ratio is 2.36 (95% CI 1.67 to 3.34).
- **Monthly_fee and support_calls are the strongest numeric associations.** Churned customers have a higher mean monthly_fee (79.9 vs 66.1, Cohen's d 0.49) and more support calls (mean 1.84 vs 1.34, Cohen's d 0.43), both significant. Churn rises with fee quartile, from 17.5% in Q1 to 44.5% in Q4. Monthly_fee's adjusted odds ratio is 1.018 per unit (p = 1.0e-09), essentially unchanged from its unadjusted value.
- **Region shows no meaningful association with churn.** Rates range from 27.5% (south) to 34.5% (west), but the chi-square test is not significant (p = 0.448, Cramér's V 0.058).
- **Predictive power is modest.** On a 160-row test split, logistic regression reaches accuracy 0.725 against a majority-class baseline of 0.6875, with test ROC AUC 0.712. Gradient boosting overfits and falls below the baseline on accuracy (0.675, ROC AUC 0.643). Monthly_fee has the largest permutation importance in both models.
- **The contract effect survives adjustment, and the support_calls effect does not differ detectably by contract.** The interaction test gives p = 0.789.

## Data

- **Size:** 800 rows, 5 columns. Numeric features: monthly_fee, support_calls. Categorical features: contract, region. No date/time features and no identifier or free-text columns.
- **Target:** churned_flag, binary. 68.8% "no" and 31.2% "yes" (250 yes, 550 no). The target is imbalanced.
- **Missing values:** none in any column (monthly_fee, support_calls, contract, region, churned_flag), confirmed in the exploratory task.

## Findings

### Overall churn and group differences

- Overall churn is 31.2% (250 of 800).
- **Contract:** Monthly contracts churn at 37.3% (n=498), against 21.2% for annual contracts (n=302), a gap of about 16 percentage points.

  ![Churn rate by contract type](tasks/eda_1/charts/churn_rate_by_contract.png)

- **Region:** Churn varies only modestly: west 34.5% (n=194), north 33.0% (n=191), east 30.2% (n=215), south 27.5% (n=200).
- **Monthly_fee:** Churned customers have a mean of 79.9 and median of 82.9. Retained customers have a mean of 66.1 and median of 63.3.
- **Monthly_fee quartiles** (200 customers each): churn is 17.5% in Q1, 28.5% in Q2, 34.5% in Q3 and 44.5% in Q4.
- **Support calls:** Churned customers have a mean of 1.84 calls (median 2) and retained customers a mean of 1.34 (median 1).
- **Churn by support_calls value:** 22.6% at 0 calls (n=164), 26.4% at 1 (n=284), 34.5% at 2 (n=206), 39.2% at 3 (n=97) and 50% at 4 (n=36). Groups with 5 or more calls are very small (5 calls: 90.9% of 11 customers; 6 calls: 0% of 1; 7 calls: 100% of 1), so these rates are unstable.

  ![Churn rate by number of support calls](tasks/eda_1/charts/churn_rate_by_support_calls.png)

### Significance and effect sizes

- **Contract and churn:** chi-square 22.84 (df 1), p = 1.8e-06, Cramér's V 0.169 (small to moderate). Computed without continuity correction.
- **Region and churn:** chi-square 2.66 (df 3), p = 0.448, Cramér's V 0.058 (negligible). The region gap is within sampling noise. Computed without continuity correction.
- **Monthly_fee by churn:** mean difference 13.82 (95% CI 9.67 to 17.96). Welch p = 1.4e-10, Mann-Whitney p = 4.4e-10, Cohen's d 0.49 (medium). This is the largest practical gap in the analysis.
- **Support_calls by churn:** mean difference 0.50 (95% CI 0.31 to 0.68). Welch p = 3.6e-07, Mann-Whitney p = 8.5e-07, Cohen's d 0.43 (small to medium).
- **Contract × support_calls interaction:** in a logistic regression, LR chi-square 0.072 (df 1), p = 0.789. Log-odds slopes per support call are 0.342 for annual and 0.381 for monthly contracts. The data are consistent with a common slope.
- **Within-contract pattern:** churn rises with support calls in both contract types. Annual rates by call count (0, 1, 2, 3+) are 17.2%, 14.2%, 25.0% and 32.8%. Monthly rates are 25.5%, 33.7%, 40.5% and 54.5%. Group sizes are small at higher call counts, so upper-end rates are noisy.

  ![Churn rate by support calls, split by contract type](tasks/stat_1/charts/churn_rate_by_support_calls_contract.png)

### Contract effect after adjustment

- The monthly-vs-annual difference holds after adjusting for monthly_fee and support_calls.
  - Adjusted odds ratio: 2.36 (95% CI 1.67 to 3.34, p = 1.2e-06).
  - Unadjusted odds ratio: 2.22 (95% CI 1.59 to 3.08).
- Standardised adjusted churn is 37.3% if all customers were monthly and 21.3% if all were annual, a gap of 15.9 points (95% bootstrap CI 10.1 to 21.8). The unadjusted gap is 16.2 points (95% bootstrap CI 10.1 to 22.3). The intervals overlap almost completely, so the gap does not shrink materially after adjustment.
- Both covariates are positively associated with churn in the adjusted model: 0.018 log-odds per unit of monthly_fee and 0.377 per support call. The contract coefficient is 0.858.

  ![Odds ratio of churn for monthly vs annual contract, unadjusted and adjusted for monthly_fee and support_calls, with 95% CI](tasks/stat_2/charts/contract_or_adjusted.png)

### Monthly_fee after adjustment

- In a multivariable logistic regression adjusting for contract and support_calls, monthly_fee remains significant: OR 1.018 per unit (95% CI 1.012 to 1.024), p = 1.0e-09. Per 10 currency units, the adjusted OR is 1.19 (95% CI 1.13 to 1.26).
- The unadjusted OR is 1.017 per unit, p = 8.1e-10. Per 10 currency units, the unadjusted OR is 1.19 (95% CI 1.12 to 1.25).
- The monthly_fee coefficient moves from 0.01714 unadjusted to 0.01763 adjusted, a change of about 2.9%. The analysis describes the fee association as essentially unconfounded by contract and support_calls.
- Other adjusted terms: the monthly contract OR is 2.36 (p = 1.2e-06), and the support_calls OR is 1.46 per call (95% CI 1.28 to 1.67, p = 3.5e-08).
- Collinearity is negligible. VIFs are 1.00 for monthly_fee, the monthly contract dummy and support_calls. R² of monthly_fee on contract is 0.0006.

### Predictive models

- **Baseline:** on the 160-row stratified test split, the majority-class model has accuracy 0.6875 and balanced accuracy 0.5.
- **Logistic regression:** accuracy 0.725, train accuracy 0.728, precision 0.615, recall 0.32, F1 (yes class) 0.421, test ROC AUC 0.712.
- **Gradient boosting:** accuracy 0.675 (below baseline), train accuracy 0.877, precision 0.471, recall 0.32, F1 0.381, test ROC AUC 0.643.
- Logistic regression is the better model on the test split. Gradient boosting overfits, with a large gap between train and test accuracy. The ROC AUC gap of about 0.07 is suggestive, but it has not been tested for significance.

  ![Test ROC AUC of the majority baseline (0.5 by construction), logistic regression and gradient boosting](tasks/ml_1/charts/ml1_model_auc.png)

- **Feature importance (drop in test ROC AUC when permuted):**
  - Logistic regression: monthly_fee 0.091 (sd 0.026), support_calls 0.071 (sd 0.028), contract 0.027 (sd 0.028), region 0.006 (sd 0.005).
  - Gradient boosting: monthly_fee 0.081 (sd 0.045), contract 0.054 (sd 0.027), support_calls 0.052 (sd 0.027), region -0.006 (sd 0.013).
- Monthly_fee ranks first in both models. The ordering of support_calls and contract after it differs between the models. For gradient boosting, the contract and support_calls values are close, so that ordering is not firm.
- Region is indistinguishable from zero in both models.

## Limitations

- **Small groups at high support_calls counts.** Groups with 5 or more calls are small (5 calls: 11 customers; 6 calls: 1; 7 calls: 1), so their rates are unstable. The 4+ call rates in the within-contract breakdown are also noisy.
- **Chi-square tests without continuity correction** (contract and region tests, stat_1). The findings do not assess how this affects the p-values.
- **Small test set for model comparison.** Model scores rest on 160 test rows. The ROC AUC difference between models has not been tested for significance. Permutation importances for gradient boosting have large standard deviations (monthly_fee sd 0.045).
- **Gradient boosting was not tuned or regularised, and no cross-validation was run** on the full 800 rows. Its comparison with logistic regression therefore reflects this single configuration and split.
- **Adjusted estimates come from the logistic models as specified.** The adjustment covers only monthly_fee, support_calls and (for the fee model) contract. Other factors were not included.
- **Associations only.** The analysis measures association with churned_flag; it does not establish causes.
- **Failed tasks:** none. All four analysis tasks completed and were accepted. There are no unresolved review issues.

## Open questions

- Does the monthly-vs-annual contract effect differ by monthly_fee level? The contract × fee interaction was not tested.
- Is the monthly_fee effect stable within each contract type? The tasks raised this but did not test it.
- Are the high churn rates at 4+ and especially 5+ support calls real, or noise from small groups?
- Is the logistic regression's ROC AUC advantage over gradient boosting statistically significant, and would tuning or cross-validation change the model ranking?
- Does the support_calls effect remain stable at 4 or more calls, given the small group sizes?