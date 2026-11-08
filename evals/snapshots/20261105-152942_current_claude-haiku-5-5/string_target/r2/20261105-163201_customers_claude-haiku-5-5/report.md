# Customer Churn Analysis: Predicting churned_flag in an 800-Customer Dataset

## Summary

- **Contract type is the clearest association with churn.** Monthly contracts churn at 37.35% versus 21.19% for annual contracts (difference 16.2 points, 95% CI 9.9 to 22.4). The association stays after adjusting for region, monthly_fee and support_calls (adjusted OR 0.42 for annual versus monthly, 95% CI 0.30 to 0.59).
- **Higher monthly fees and more support calls are both associated with churn.** Churned customers have a higher mean monthly_fee (79.94 vs 66.12) and more support calls (mean 1.84 vs 1.34). Both differences are significant after Holm correction, and both remain associated with churn after adjustment for the other features.
- **Region is not associated with churn.** Region rates range from 27.50% to 34.54%, but the chi-square test gives p = 0.448 (Holm-adjusted p = 0.448).
- **Logistic regression is the preferred model, and its gain over the baseline is modest.** On the 160-row test set it reaches accuracy 0.725 against a majority-class baseline of 0.6875, with balanced accuracy 0.615 (baseline 0.500) and ROC AUC 0.712. Repeated cross-validation on the training split gives a mean ROC AUC of 0.692. The random forest scores below the baseline on accuracy (0.631), and neither non-linear model beat logistic regression under cross-validation.
- **No interaction between fee, support calls, contract or region was detected**, but the tests are not powered to rule out moderate interactions. A small high-churn group at 4 or more support calls appears in the stratified analysis, with wide confidence intervals.

## Data

- **Size:** 800 rows, 5 columns.
- **Target:** `churned_flag`, binary. 250 customers churned (31.25%, "yes") and 550 did not (68.75%, "no"). The classes are imbalanced.
- **Numeric features:** `monthly_fee`, `support_calls`.
- **Categorical features:** `contract`, `region`.
- **Excluded:** no date/time features, and no ids or free text.
- **Missing values:** none in any of the five columns.

## Findings

### Churn rates by contract and region

Overall, 250 of 800 customers churned. Churn rates by group:

| Group | Churn rate | n |
|---|---|---|
| Contract: annual | 21.19% | 302 |
| Contract: monthly | 37.35% | 498 |
| Region: east | 30.23% | 215 |
| Region: north | 32.98% | 191 |
| Region: south | 27.50% | 200 |
| Region: west | 34.54% | 194 |

Monthly contracts churn about 16 percentage points more than annual contracts. Region rates span 27.50% (south) to 34.54% (west).

![Churn rate (% of customers churned) by contract type and by region](tasks/eda_1/charts/churn_rate_by_contract_and_region.png)

### Monthly fee and support calls

**Monthly fee.** Churned customers have higher fees: mean 79.94 (median 82.92, SD 27.14) against mean 66.12 (median 63.35, SD 28.76) for non-churned customers. Churn rises across fee quartiles, each containing 200 customers:

| Fee quartile | Churn rate |
|---|---|
| Q1 (lowest) | 17.5% |
| Q2 | 28.5% |
| Q3 | 34.5% |
| Q4 (highest) | 44.5% |

**Support calls.** Churned customers make more calls: mean 1.84 (median 2.0, SD 1.33) against mean 1.34 (median 1.0, SD 1.08). Churn rises with each call count:

| Support calls | Churn rate | n |
|---|---|---|
| 0 | 22.6% | 164 |
| 1 | 26.4% | 284 |
| 2 | 34.5% | 206 |
| 3 | 39.2% | 97 |
| 4 | 50% | 36 |
| 5 | 90.9% | 11 |

Values 6 and 7 each have one customer (0% and 100%) and are not reliable.

![Distributions of monthly_fee and support_calls split by churned_flag: histograms (count of customers) and box plots](tasks/eda_2/charts/fee_calls_by_churn.png)

### Statistical significance and effect sizes

Four primary tests were corrected with Holm's step-down method.

- **Contract and churn:** chi-square = 22.84, df = 1, p = 1.76e-06, Cramér's V = 0.169 (small to medium). Holm-adjusted p = 3.5e-06. Significant.
- **Region and churn:** chi-square = 2.66, df = 3, p = 0.448, Cramér's V = 0.058 (negligible). Holm-adjusted p = 0.448. Not significant. The region gaps are within sampling noise at these group sizes.
- **Monthly fee and churn:** Mann-Whitney p = 4.4e-10, rank-biserial = 0.275 (higher in churned customers). Holm-adjusted p = 1.8e-09. Significant.
- **Support calls and churn:** Mann-Whitney p = 8.5e-07, rank-biserial = 0.209 (higher in churned customers). Holm-adjusted p = 2.6e-06. Significant.

The monthly-minus-annual churn difference is 16.2 percentage points (95% Wald CI 9.9 to 22.4). This single pre-specified comparison was not included in the Holm adjustment.

![Churn rate (% churned) for annual and monthly contracts, n=302 annual and n=498 monthly](tasks/stat_1/charts/churn_rate_by_contract_stat.png)

### Interactions between fee, support calls, contract and region

**Fee within contract (descriptive).** Split at the median fee of 71.2:

- Monthly contracts: 48.2% churn in the high-fee group (n=251) versus 26.3% in the low-fee group (n=247).
- Annual contracts: 24.8% churn in the high-fee group (n=149) versus 17.6% in the low-fee group (n=153).

The gap between these differences was not tested formally.

**Formal interaction tests.** These do not agree with the descriptive gap:

- monthly_fee × contract: log-odds coefficient 0.0025 (OR 1.002 per unit, 95% CI 0.990 to 1.015, p = 0.70). The joint likelihood-ratio test of all five interaction terms gives chi-square = 0.62, df = 5, p = 0.987.
- support_calls × contract or region: no interaction detected (contract OR 1.089, 95% CI 0.813 to 1.459, p = 0.57; north OR 1.041, p = 0.83; south OR 0.946, p = 0.77; west OR 1.009, p = 0.96; reference region east).

These results show the absence of a detected interaction, not evidence of no interaction. The confidence intervals still allow moderate interactions.

The reference-level main effects from the full interaction logit are monthly_fee OR 1.016 per unit (p = 0.0025) and support_calls OR 1.386 per call (p = 0.039). These are conditional on the reference levels (annual contract, east region) with interaction terms set to zero. They are not population-average effects.

![Churn rate (% churned) for annual and monthly contracts within low and high monthly_fee groups (split at median 71.2)](tasks/stat_2/charts/churn_rate_fee_by_contract.png)

### Adjusted associations

A logistic regression with all four features (n=800) gives these results. Reference levels are monthly contract and east region.

- **Contract:** annual OR 0.42 (95% CI 0.30 to 0.59), p < 0.001. The unadjusted OR was 0.45 (95% CI 0.32 to 0.63), so the association survives adjustment with slight attenuation.
- **Monthly fee:** OR 1.018 per unit (95% CI 1.012 to 1.024), p < 0.001. The unadjusted OR was 1.017.
- **Support calls:** OR 1.463 per call (95% CI 1.279 to 1.673), p < 0.001. The unadjusted OR was 1.419.
- **Region:** no independent association. North OR 1.12 (95% CI 0.72 to 1.75, p = 0.61), south OR 0.77 (95% CI 0.49 to 1.21, p = 0.25), west OR 1.08 (95% CI 0.69 to 1.68, p = 0.73), all versus east. Unadjusted region ORs were also close to 1.

### Support calls coded as categories, and the 4+ segment

Coding support calls as 0, 1, 2, 3 and 4+ and testing interactions with contract and region gives these results:

- **Categorical support calls:** the 16-df test of interactions gives LR chi-square = 10.63, p = 0.83. The linear support-calls interaction block gives chi-square = 0.46, df = 4, p = 0.98. The two codings have different degrees of freedom, so they are compared on conclusion only. Both fail to detect an interaction.
- **Fee interactions in the categorical model:** the monthly_fee × contract coefficient gives OR 1.003 per unit (95% CI 0.990 to 1.016, p = 0.65). The fee interaction block gives LR chi-square = 1.34, df = 4, p = 0.85. No fee interaction is detected.
- **4+ calls, reference-level estimate:** OR 5.10 versus 0–1 calls (95% CI 1.08 to 24.05, p = 0.039), conditional on annual contract and east region.
- **4+ calls, stratified:** OR versus 0–1 calls, with monthly_fee and the other factor adjusted:

| Segment | OR | 95% CI | p | Customers with 4+ calls |
|---|---|---|---|---|
| Annual contract | 3.94 | 1.38 to 11.29 | 0.011 | 18 (of n=302) |
| Monthly contract | 5.24 | 2.30 to 11.94 | < 0.001 | 31 (of n=498) |
| East | 6.49 | 1.89 to 22.29 | 0.003 | 14 |
| North | 2.60 | 0.71 to 9.52 | 0.15 | 11 |
| South | 5.48 | 1.52 to 19.70 | 0.009 | 13 |
| West | 4.86 | 1.23 to 19.18 | 0.024 | 11 |

- The 4+ × contract interaction is OR 1.82 (95% CI 0.38 to 8.64, p = 0.45). The 4+ × region interactions versus east are not significant, with very wide intervals.

The 4+ estimates rest on 11 to 31 customers per level. The data cannot rule out a substantial difference in the 4+ effect by contract or region.

### Predictive models

**Test-set comparison (n=160, stratified 80/20 split, seed 42).**

| Model | Accuracy | Balanced accuracy | ROC AUC | F1 (churn) | Precision | Recall |
|---|---|---|---|---|---|---|
| Majority-class baseline | 0.6875 | 0.500 | — | — | — | — |
| Logistic regression | 0.725 | 0.615 | 0.712 | 0.421 | 0.615 | 0.32 |
| Random forest | 0.631 | 0.568 | 0.626 | 0.404 | 0.408 | 0.40 |

- The random forest has train accuracy 1.0, indicating overfitting, and scores below the baseline on test accuracy.
- The logistic regression was chosen by test-set ROC AUC. The same test set is used for the permutation importances below, so those importances are not independent of the selection and are indicative only.

![Balanced accuracy on the held-out test set for the majority-class baseline, logistic regression and random forest predicting churned_flag](tasks/ml_1/charts/ml1_balanced_accuracy.png)

**Permutation importance (logistic regression, drop in test ROC AUC over 30 shuffles).**

| Feature | Mean drop | SD | Mean/SD |
|---|---|---|---|
| monthly_fee | 0.091 | 0.026 | 3.5 |
| support_calls | 0.071 | 0.028 | 2.5 |
| contract | 0.027 | 0.028 | 1.0 |
| region | 0.006 | 0.005 | 1.2 |

The SDs reflect shuffle variability only, not sampling error from the 160-row test set. Region's drop is not distinguishable from zero under this measure, and contract's is unclear.

**Repeated cross-validation on the training split (5×5 stratified, 25 folds, n=640).** SDs are population SDs.

| Model | Mean ROC AUC (SD) | Mean balanced accuracy (SD) | Paired ROC AUC difference vs logreg |
|---|---|---|---|
| Majority baseline | 0.500 | 0.500 | — |
| Logistic regression | 0.692 (0.039) | 0.600 (0.041) | — |
| Spline logistic regression | 0.682 (0.041) | 0.574 (0.037) | −0.010 (SD 0.009); lower in 21 of 25 folds |
| Histogram gradient boosting | 0.636 (0.045) | 0.568 (0.035) | −0.056 (SD 0.030); higher in 1 of 25 folds |

Neither non-linear model improves on logistic regression. The gradient boosting shortfall reflects fixed, untuned settings (max_iter=150, learning_rate=0.05, max_depth=3), so it applies to this configuration only. The test ROC AUC of 0.712 lies about 0.02 above the CV mean of 0.692, which the finding describes as consistent with the CV estimate given the 160-row test set.

![Mean ROC AUC across 25 stratified CV folds on the training split for the majority baseline, logistic regression, spline logistic regression and histogram gradient boosting; error bars show fold SD.](tasks/ml_2/charts/ml2_cv_roc_auc.png)

## Limitations

- **Sample size.** The dataset has 800 rows. The 160-row test set is too small to separate contract and region from zero in permutation importance. Several subgroup estimates rest on very few customers, notably 4+ support calls (11 to 31 per level) and support-call values 5 to 7 (one to 11 customers).
- **No time or cause information.** The dataset has no date features, so the analysis cannot address change over time. The findings are associations and do not establish causes.
- **Interaction tests have low power.** Non-significant interaction results do not show that no interaction exists. The monthly-versus-annual fee difference in the descriptive table (48.2% vs 26.3% for monthly; 24.8% vs 17.6% for annual) was not tested formally and was not found to be an interaction in the model.
- **Reference-level estimates.** The main-effect ORs in the interaction models and the 4+ call OR of 5.10 are conditional on reference levels and are not population-average effects. The adjusted main-effects ORs above are the population-level estimates.
- **Model selection.** The logistic regression was selected on test-set ROC AUC. Its test-set scores and permutation importances are therefore optimistic, and the CV results are the main evidence for model comparison.
- **Cross-validation uncertainty.** The 25 CV folds reuse the same 640 training rows, so the fold SD understates overall uncertainty. A bootstrap over rows or nested CV would give a better estimate, and the paired differences should be read as rough.
- **Hyperparameters.** The gradient boosting model used fixed, untuned settings. A tuned model could change the ranking.
- **Multiple comparisons.** The four primary tests were Holm-corrected. The contract difference CI was a single pre-specified comparison and was not adjusted.
- **Accuracy as a measure.** The positive rate is 31.25%, so accuracy is a weak measure. The logistic regression's accuracy is only about 0.04 above the baseline.
- **Unreviewed items.** No review issues were recorded as unresolved and no tasks failed.

## Open questions

- Does the monthly-versus-annual difference in the fee effect hold in a formal risk-difference test with a larger sample? (Raised by stat_2 and stat_4.)
- Does the effect of annual contract differ by support-call level in a formal interaction test? (Raised by stat_3.)
- Is the monthly_fee association linear on the logit scale, or does it need a spline or binned term? The spline model in ml_2 did not improve on logistic regression under CV, but the question of linearity across fee quartiles was not answered directly. (Raised by stat_1, stat_3 and stat_2.)
- Is high churn at 4+ support calls a distinct segment, and does its size differ by contract after adjusting for monthly_fee in a larger sample? (Raised by eda_2, stat_1 and stat_4.)
- Would tuning the gradient boosting hyperparameters under repeated CV change its ranking against logistic regression? (Raised by ml_2.)
- Would a bootstrap over training rows or nested CV give better uncertainty estimates for the model scores and permutation importances? (Raised by ml_1 and ml_2.)
- Do the region differences hold in a larger sample, or are they within sampling noise? (Raised by eda_1. stat_1 found them not significant at these group sizes.)
- Does adding a contract × monthly_fee interaction improve logistic regression under repeated CV? (Raised by ml_2.)