# Customer Churn Analysis: Predicting churned_flag in an 800-Customer Table

## Summary

- **Monthly contracts churn more than annual ones.** Churn is 37.35% for monthly and 21.19% for annual contracts (chi-square 22.84, p = 1.76e-06, Cramér's V 0.169). The association persists after adjusting for monthly_fee and support_calls: adjusted OR 2.36 (95% CI 1.67 to 3.34).
- **Higher fees and more support calls go with churn, and region does not.** Churned customers have a mean monthly_fee of 79.94 versus 66.12 for retained (rank-biserial 0.275) and a mean of 1.84 support calls versus 1.34 (rank-biserial 0.209). Both differences are significant after Holm correction. Region is not significant (p = 0.448, Cramér's V 0.058).
- **Contract does not significantly change the effects of support_calls or monthly_fee on churn.** The interaction terms have p = 0.713 and p = 0.694.
- **Logistic regression ranks churners better than chance, but only modestly, and it misses most churners.** Test accuracy is 72.5% against a 68.75% majority baseline on 160 rows, where the gain was not tested. Under 5-fold cross-validation, mean ROC AUC is 0.695 (sd 0.030) against 0.5 for the baseline. Recall is 0.28 in cross-validation and 0.32 on the test set.
- **The random forest does not beat the baseline.** Its test accuracy is 63.1%, and it overfits (training accuracy 1.0).

## Data

- 800 rows and 5 columns: the target churned_flag (binary), numeric features monthly_fee and support_calls, and categorical features contract and region. The table has no date or time features and no ids or free text.
- Target distribution: 250 churned (31.25%) and 550 retained (68.75%). The target is imbalanced.
- Missing values: none in any column.

## Findings

### Overall churn and group-level rates

Churn is 31.25% overall (250 of 800). By contract, churn is 37.35% for monthly (186 of 498) and 21.19% for annual (64 of 302). By region, churn ranges from 27.50% in south (55 of 200) to 34.54% in west (67 of 194), with north at 32.98% (63 of 191) and east at 30.23% (65 of 215).

![Churn rate (%) by contract and by region](tasks/eda_1/charts/churn_rate_by_contract_region.png)

Churned customers have higher average monthly fees and make more support calls than retained customers. Mean monthly_fee is 79.94 for churned versus 66.12 for retained (medians 82.92 and 63.34). Mean support_calls is 1.84 versus 1.34 (medians 2 and 1).

![Histograms and box plots of monthly_fee and support_calls split by churned_flag](tasks/eda_1/charts/fee_calls_by_churn.png)

### Significance and effect sizes

Four univariate tests were run, with Holm correction across them.

- **Contract:** significant. Chi-square(1) = 22.84, p = 1.76e-06 (Holm-adjusted p = 3.51e-06), Cramér's V = 0.169, a small-to-medium association.
- **Region:** not significant. Chi-square(3) = 2.66, p = 0.448 (Holm-adjusted p = 0.448), Cramér's V = 0.058, a negligible association.
- **monthly_fee:** significant. Mann-Whitney p = 4.4e-10 (Holm-adjusted p = 1.8e-09), rank-biserial 0.275. The mean difference is 13.82 (95% CI 9.67 to 17.96). A randomly chosen churned customer has a higher fee than a randomly chosen retained customer about 64% of the time.
- **support_calls:** significant. Mann-Whitney p = 8.5e-07 (Holm-adjusted p = 2.55e-06), rank-biserial 0.209. The mean difference is 0.50 calls (95% CI 0.31 to 0.68). This is a small effect.

Monthly_fee has the largest effect among the numeric and categorical tests by rank-biserial. Contract (Cramér's V) and support_calls (rank-biserial) use different metrics, so they cannot be ranked against each other. These tests are univariate and do not control for one another.

![Churn rate (%) by contract and by region](tasks/stat_1/charts/stat1_churn_rate_categorical.png)

### Contract adjusted for fee and support calls

In a main-effects logistic model of churn on contract, monthly_fee and support_calls (n = 800), monthly contract has adjusted OR 2.3595 (95% CI 1.6688 to 3.3363), coefficient 0.8585, p < 0.0001, relative to annual contracts. Per additional support call, the adjusted OR is 1.4584 (95% CI 1.2754 to 1.6677). Per one-unit increase in monthly_fee, the adjusted OR is 1.0178 (95% CI 1.0120 to 1.0236). Both are p < 0.0001.

In a contract-only logistic model, the unadjusted OR for monthly contract is 2.2169 (95% CI 1.5933 to 3.0848). The unadjusted OR is 2.22 and the adjusted OR is 2.36. Adjustment for monthly_fee and support_calls leaves the contract association essentially unchanged in this model. This is an adjustment for those two variables only, not evidence about causes. The unadjusted OR and the stat_1 chi-square test are different measures of the same association, and both point the same way.

### Interaction: does contract modify the effects of support_calls or monthly_fee?

In the logistic model with interactions, neither interaction is significant:

- support_calls × monthly: coefficient 0.0536, OR 1.055 (95% CI 0.793 to 1.404), p = 0.713.
- monthly_fee × monthly: coefficient 0.0025, OR 1.002 (95% CI 0.990 to 1.015), p = 0.694.

Churn rates within support_calls groups split at the median (1):

- Low (≤1): annual 15.24% (n = 164), monthly 30.63% (n = 284). Gap 15.39 percentage points.
- High (>1): annual 28.26% (n = 138), monthly 46.26% (n = 214). Gap 18.00 percentage points.

The finding describes the monthly-minus-annual gap as similar across the two groups, and the interaction tests are not significant. Non-significance here does not establish that the effect is identical in the two groups.

![Churn rate (%) by contract within low (<= median) and high (> median) support_calls groups](tasks/stat_2/charts/churn_rate_by_calls_contract.png)

### Predictive models

**Single 160-row test split (ml_1).** Logistic regression reached 72.5% test accuracy against the 68.75% majority-class baseline, with ROC AUC 0.712. The 3.75-point accuracy gain was not tested for significance and is uncertain on 160 rows. At the default 0.5 threshold, precision is 0.615, recall 0.32 and F1 0.421. About 68% of churners are missed.

The random forest did not beat the baseline: test accuracy 63.1%, ROC AUC 0.627, positive-class F1 0.404. Its training accuracy is 1.0, which points to overfitting on 640 training rows.

Feature importance on the test set was measured by the drop in ROC AUC when each feature is permuted, with 30 repeats:

- Logistic regression: monthly_fee 0.091 (sd 0.026), support_calls 0.071 (sd 0.028), contract 0.027 (sd 0.028), region 0.006 (sd 0.005).
- Random forest: support_calls 0.073 (sd 0.036), monthly_fee 0.056 (sd 0.037), contract 0.044 (sd 0.028), region -0.014 (sd 0.035).

The two models swap the order of monthly_fee and support_calls, and the standard deviations overlap widely, so that order is not settled. Region shows no importance in either model. The sds reflect variability across permutation repeats on one test set, not sampling uncertainty, so these rankings are indicative only.

![Test-set accuracy and ROC AUC of the majority-class baseline (AUC fixed at 0.5), logistic regression and random forest](tasks/ml_1/charts/ml_1_model_comparison.png)

**Stratified 5-fold cross-validation over all 800 rows (ml_2, seed 42).** Logistic regression has mean ROC AUC 0.695 (sd 0.030; per fold 0.704, 0.694, 0.645, 0.718, 0.717) against 0.5 for the baseline. Mean positive-class F1 is 0.382 (sd 0.087) against 0 for the baseline, which never predicts churn.

Within cross-validation, mean recall is 0.28 (sd 0.079) and mean precision is 0.613 (sd 0.083). The low F1 is driven by low recall at the default threshold.

Mean held-out accuracy is 0.721 (sd 0.028) against 0.688 for the baseline, a mean fold-wise gain of 0.034 (sd 0.028). Four of five folds show a gain, ranging from 0.0125 to 0.069. Fold 3 shows no gain. The gain was not tested for significance.

These cross-validation figures come from a different evaluation than the single test split in ml_1 (AUC 0.712, F1 0.421). The two sets of figures are not the same estimate. The cross-validation spread (AUC sd 0.030, F1 sd 0.087) indicates how much single-split figures can vary.

![Held-out accuracy per fold (stratified 5-fold CV, seed 42), logistic regression vs majority-class baseline](tasks/ml_2/charts/ml2_fold_accuracy.png)

## Limitations

- **Small sample.** The dataset has 800 rows. The test set has 160 rows, and each cross-validation fold is a fifth of the data. Estimates are therefore imprecise.
- **Accuracy gains are untested.** The 3.75-point test accuracy gain (ml_1) and the 0.034 mean cross-validation gain (ml_2) were not tested for significance. Fold 3 of the cross-validation showed no gain.
- **Low recall.** At the default threshold, logistic regression identifies only about a third of churners (recall 0.32 on the test set, 0.28 in cross-validation). Threshold tuning was not performed.
- **Inconsistent model scores across evaluations.** The single-split and cross-validation results disagree in level: ROC AUC is 0.712 on the test set and 0.695 on average in cross-validation, and F1 is 0.421 and 0.382. The findings attribute the difference to the evaluation design. They are reported side by side here and not reconciled.
- **Univariate tests.** The significance tests in stat_1 do not control for one another. The adjusted model covers only contract, monthly_fee and support_calls. Region was not included in any adjusted model.
- **Permutation importance is indicative.** Its standard deviations come from repeats on one test set. The order of monthly_fee and support_calls is not settled, and the regression coefficient ranking (ml_1) is on scaled one-hot features and is not comparable to the permutation ranking.
- **Non-significance is not absence of effect.** The non-significant interactions and the non-significant region association do not establish that these effects are zero.
- **Associations only.** All results are associations in cross-sectional data. The findings do not establish why churn differs across groups.
- **Failed or unresolved tasks.** No task failed. No unresolved review objections were recorded.

## Open questions

- Is the west versus south churn difference statistically significant after pairwise comparison? This was raised but not tested.
- Does the monthly-contract association hold in a model adjusted for region? Region has not yet been tested as a confounder.
- Is the accuracy gain over the majority baseline statistically significant under repeated stratified cross-validation or a paired test across folds?
- Does the ROC AUC advantage hold with 10-fold or repeated stratified cross-validation?
- Would tuning the classification threshold raise recall (0.28 in cross-validation, 0.32 on the test set) and F1 without losing too much precision?
- Would tuning the random forest (depth, leaf size) reduce its overfitting and close the gap to logistic regression?
- Which contract or region levels drive the churn signal in the logistic regression coefficients?
- Do higher support_calls and monthly_fee jointly predict churn in a multivariable model with interaction terms, and how much predictive power does each contribute?