# Churn Analysis of 800 Customers: Predictors of churned_flag

## Summary

- **Contract type is the clearest churn difference.** Monthly contracts churn at 37.3% (186 of 498) versus 21.2% for annual (64 of 302), a 16.2-point difference (Wald 95% CI 9.9 to 22.4; p = 4.4e-07). The association stays after adjusting for monthly_fee, support_calls and region, with adjusted odds of 2.39 (95% CI 1.68 to 3.38).
- **Churned customers pay more and call support more.** Mean monthly_fee is 79.94 for churned vs 66.12 for non-churned (difference 13.82, 95% CI 9.67 to 17.96; Cohen's d = 0.49). Mean support_calls is 1.84 vs 1.34 (difference 0.50, 95% CI 0.31 to 0.68; d = 0.43).
- **Region is not significantly associated with churn.** Regional rates range from 27.5% to 34.5%, but the test gives chi-square(3) = 2.66, p = 0.448, and no region term is significant after adjustment.
- **The best model beats the baseline on ranking, not on accuracy.** Logistic regression reaches test ROC AUC 0.712 (recall 0.32, F1 0.416) against 0.5 for the majority-class baseline, whose accuracy of 68.75% is matched by gradient boosting. Logistic regression's accuracy is 71.9%. Gradient boosting's test ROC AUC is 0.649. Both were observed on one 160-row test split, and whether the difference between them is real is not established.

## Data

- 800 rows, 5 columns: monthly_fee and support_calls (numeric); contract and region (categorical); churned_flag (binary target).
- No date/time or id columns, and no free-text fields, so none were excluded.
- Target balance: no 68.8%, yes 31.2% (250 of 800 churned). The target is imbalanced.
- Missing values: none in any column, so no rows were dropped and the clean table has 800 rows.

## Findings

### Overall churn and churn by contract

Overall churn is 31.2% (250 of 800). Monthly contracts churn at 37.3% (186 of 498) and annual contracts at 21.2% (64 of 302), about 1.8 times the annual rate.

![Churn rate by contract type and by region, fraction of customers churned](tasks/eda_1/charts/churn_rate_by_contract_region.png)

Contract is significantly associated with churn: chi-square(1) = 22.84, p = 1.8e-06, Cramér's V = 0.17 (small-to-medium).

- Monthly churn: 37.3% (95% Wilson CI 33.2% to 41.7%).
- Annual churn: 21.2% (95% Wilson CI 17.0% to 26.1%).
- Monthly minus annual: 16.2 points (Wald 95% CI 9.9 to 22.4; two-proportion z-test p = 4.4e-07).

### Churn by region

Churn rates by region are south 27.5% (55 of 200), east 30.2% (65 of 215), north 33.0% (63 of 191) and west 34.5% (67 of 194). The spread is about 7 points, but region is not significantly associated with churn: chi-square(3) = 2.66, p = 0.448, Cramér's V = 0.058.

### Monthly fee and support calls by churn status

Churned customers have higher monthly fees. The mean is 79.94 vs 66.12 (median 82.92 vs 63.35). The difference is 13.82 (95% CI 9.67 to 17.96; Welch t = 6.55, p < 0.0001; Mann-Whitney p = 4.4e-10). Cohen's d is 0.49 (medium) and rank-biserial is 0.27.

Churned customers also make more support calls. The mean is 1.84 vs 1.34 (median 2 vs 1). The difference is 0.50 (95% CI 0.31 to 0.68; Welch t = 5.17, p = 3.6e-07; Mann-Whitney p = 8.5e-07). Cohen's d is 0.43 (small-to-medium) and rank-biserial is 0.21.

![Distribution of monthly_fee and support_calls for churned (1) vs not churned (0) customers](tasks/stat_1/charts/numeric_by_churn_tests.png)

![Monthly fee and support calls by churn status (0=no, 1=yes)](tasks/eda_1/charts/numeric_by_churn.png)

### Monthly fee and support calls by contract level

Fees and support load are similar for monthly and annual contracts.

- Monthly fee: mean 70.99 (median 71.41) for monthly (n = 498) vs mean 69.53 (median 70.23) for annual (n = 302). The difference is 1.46 (Welch p = 0.49).
- Support calls: mean 1.48 (median 1.0) for monthly vs mean 1.53 (median 1.0) for annual. The difference is -0.05 (Mann-Whitney p = 0.41).

![Mean and median monthly_fee and support_calls for annual and monthly contracts](tasks/eda_2/charts/numeric_by_contract.png)

### Adjusted effects of contract, fee, support calls and region

A logistic regression adjusted for monthly_fee, support_calls and region (n = 800) gives these results.

- **Contract:** monthly contracts have adjusted odds of churn 2.39 times those of annual (95% CI 1.68 to 3.38, p = 1.0e-06). The unadjusted odds ratio is 2.22 (95% CI 1.59 to 3.08, p = 2.3e-06). Adjustment did not weaken the contract association.
- **monthly_fee:** each additional unit raises the adjusted odds of churn by 1.8% (OR 1.018, 95% CI 1.012 to 1.024, p = 1.1e-09).
- **support_calls:** each additional call multiplies the adjusted odds by 1.46 (OR 1.463, 95% CI 1.279 to 1.673, p = 2.9e-08).
- **Region (vs east):** north OR 1.12 (95% CI 0.72 to 1.75, p = 0.61); south OR 0.77 (95% CI 0.49 to 1.21, p = 0.25); west OR 1.08 (95% CI 0.69 to 1.68, p = 0.73). None is significant, which agrees with the unadjusted region test.

### Interactions

- **Contract × region:** the logistic-regression interaction test (adjusted for monthly_fee and support_calls) gives LR chi-square 0.98 on 3 df, p = 0.81. The contract effect does not vary significantly by region.
- **Support_calls × contract:** the interaction test (adjusted for region and monthly_fee) gives LR chi-square 0.25 on 1 df, p = 0.62. The support_calls effect does not vary significantly by contract. No coefficient estimates for these interaction terms were recorded.

Churn rates by contract and region (churned/n):

| Region | Annual | Monthly |
|---|---|---|
| East | 18.8% (16/85) | 37.7% (49/130) |
| North | 24.1% (20/83) | 39.8% (43/108) |
| South | 16.9% (12/71) | 33.3% (43/129) |
| West | 25.4% (16/63) | 38.9% (51/131) |

Monthly churn exceeds annual churn in every region: east 37.7% vs 18.8%, north 39.8% vs 24.1%, south 33.3% vs 16.9%, and west 38.9% vs 25.4%.

![Churn rate by region for monthly and annual contracts (fraction of customers churned)](tasks/stat_2/charts/churn_rate_contract_by_region.png)

### Predictive models vs majority-class baseline

All models use a single train/test split: 640 training rows and 160 test rows, with 50 churners in the test set. Models are judged by ROC AUC, recall and F1, because accuracy is misleading at 68.75/31.25 classes.

| Model | Test accuracy | ROC AUC | Precision | Recall | F1 | Train accuracy |
|---|---|---|---|---|---|---|
| Majority class | 68.75% | 0.500 | 0.0 | 0.0 | 0.0 | 68.75% |
| Logistic regression | 71.9% | 0.712 | 0.593 | 0.32 | 0.416 | 72.8% |
| Gradient boosting | 68.75% | 0.649 | 0.500 | 0.32 | 0.390 | 81.9% |

The majority-class baseline never predicts churn. Logistic regression's accuracy is about 3 points above the baseline, which is not the main evidence for it. Gradient boosting's training accuracy of 81.9% points to overfitting.

Test ROC AUC is 0.712 for logistic regression and 0.649 for gradient boosting. These values come from a single 160-row test split, and no interval or paired test was computed, so whether the difference between the two models is real is not established.

### Feature importance

- **Permutation importance (drop in test ROC AUC when a feature is shuffled, mean over 20 repeats):**

| Feature | Logistic regression (sd) | Gradient boosting (sd) |
|---|---|---|
| monthly_fee | 0.090 (0.029) | 0.084 (0.050) |
| support_calls | 0.067 (0.030) | 0.048 (0.021) |
| contract | 0.029 (0.018) | 0.039 (0.020) |
| region | 0.007 (0.005) | -0.008 (0.006) |

Both models rank monthly_fee first, support_calls second, contract third, and region near zero.

![Drop in test ROC AUC when one raw feature is shuffled, logistic regression vs gradient boosting](tasks/ml_1/charts/ml1_permutation_importance.png)

- **Logistic regression coefficients (absolute value):** contract_monthly 0.934, monthly_fee 0.497, support_calls 0.451, region_south 0.229, region_west 0.068, region_north 0.016.
- **Gradient boosting importance:** monthly_fee 0.710, support_calls 0.156, contract_monthly 0.104, region terms 0.019 or less.

The two measures disagree on the rank of contract. Coefficients give each term's size holding the others fixed. Permutation drop measures how much AUC is lost when a feature's information is removed, including information shared with correlated features. The coefficients compare standardized numeric terms with binary one-hot terms, so their magnitudes are not strictly like-for-like.

The model work suggests that contract's effect may be partly carried by fee and support load. This is an untested hypothesis, not a finding. The adjusted analysis above found that adjusting for fee and support calls did not reduce the contract association (OR 2.22 unadjusted, 2.39 adjusted).

## Limitations

- **Imbalanced target.** Churn is 31.2%, so accuracy alone is misleading, and the baseline's accuracy of 68.75% is not a meaningful benchmark.
- **Modest sample.** The dataset has 800 rows. The model comparison uses one 160-row test split with 50 churners, with no cross-validation.
- **Model comparison not established.** The test ROC AUCs of 0.712 (logistic regression) and 0.649 (gradient boosting) are not confirmed by an interval or paired test.
- **Overfitting in gradient boosting.** Its training accuracy of 81.9% exceeds its test performance.
- **Linearity assumed in logistic models.** The adjusted models treat monthly_fee and support_calls as linear on the logit scale. This was not checked.
- **Interaction results.** Neither interaction test is significant. No coefficients or confidence intervals for the interaction terms were recorded.
- **Coefficient comparison.** Standardized numeric coefficients are compared with binary one-hot coefficients, so the magnitudes are not strictly comparable.
- **Unresolved review issues (applied in this report):**
  - *stat_2:* The monthly-vs-annual gap is reported per region from the contract × region counts, not as a computed range. The statement that each additional support call raises churn odds by a similar amount for both contract types is removed, since no coefficients for those terms were recorded.
  - *ml_1:* The AUC comparison is reported as the two test ROC AUC values (0.712 and 0.649) without a computed gap, and it is unconfirmed as described above. The claim that contract's effect is partly carried by fee and support load is reported as an untested hypothesis. The caveat about comparing standardized numeric and binary coefficients is included above.
- **Failed tasks.** None. All tasks completed.

## Open questions

- Do cross-validated ROC AUC and a paired comparison confirm that logistic regression outperforms gradient boosting (test ROC AUC 0.712 vs 0.649), or is the difference a split artifact?
- Is monthly_fee linear on the logit scale, or do a spline or binned fee fit better?
- Is monthly_fee strongly associated with contract type in the adjusted model, i.e. is there collinearity?
- Do monthly_fee and support_calls predict churn within each contract level?
- Does region carry any real signal, or is its near-zero importance noise?
- Is the hypothesis that contract's effect is partly carried by fee and support load supported by a direct test?