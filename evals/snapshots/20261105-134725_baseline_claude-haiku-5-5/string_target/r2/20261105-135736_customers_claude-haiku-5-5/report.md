# Data Analysis Report: Customer Churn

**Dataset:** `/workspaces/agents/evals/data/customers.csv`
**Scope:** 800 customers, 5 columns, binary target `churned_flag`

> **Note on completeness:** Several specialist outputs were truncated before their key statistics. The p-values, test statistics, effect-size estimates, and confidence intervals for the numeric tests, the chi-square results for contract and region, feature importances, and PR-AUC/F1 are not in the available outputs. This report does not estimate them. Where a value is derived from reported descriptive statistics, it is labeled as calculated. Missing items are flagged in the text and in Limitations.

---

## Executive Summary

- **Churn is common at 31.25%, and the data is clean.** 250 of 800 customers churned, roughly 1 churner for every 2.2 retained customers. All 800 rows were retained with no missing values, so the results are not distorted by data loss.
- **Churners pay more and call support more often.** Churned customers average $79.94 monthly versus $66.12 for retained customers, a $13.82 gap (median gap of about $19.58). They average 1.84 support calls versus 1.34. These are the strongest descriptive signals in the data. Formal significance tests for both were not reported, so this is a pattern to confirm, not a proven driver.
- **Contract type and region do not show a significant link to churn.** The chi-square tests failed to reject the null hypothesis for both. Retention efforts built on contract type or region are unlikely to be the main lever, based on this data.
- **The available features predict churn only modestly.** The model reaches a test ROC-AUC of 0.685 (cross-validated: 0.630). That is better than chance, but not sufficient for confident individual-level targeting on its own.
- **Decision implication:** Prioritize a fee and support-experience review for at-risk customers, and collect richer behavioral data before building a production churn score.

---

## Dataset Overview

| Attribute | Value |
|---|---|
| Rows / columns | 800 / 5 |
| Target | `churned_flag` (binary: 0 = retained, 1 = churned) |
| Numeric features | `monthly_fee` (float), `support_calls` (integer count) |
| Categorical features | `contract`, `region` |
| Missing values | 0 (no rows dropped) |
| Churn class balance | 550 retained (68.75%) / 250 churned (31.25%) |

The dataset is small and has only four predictors. It does not include tenure, usage, payment history, or competitor offers, which are common churn drivers. This constrains how far the predictive results can go.

---

## Analysis Methodology

### Strategic Approach

The analysis followed a sequence of exploratory, statistical, and predictive work:

1. **Exploratory first:** Characterize the class imbalance and the distributions of `monthly_fee` and `support_calls`, and examine how contract and region are distributed. This establishes the foundation for the tests and models.
2. **Statistical second:** Test whether the numeric features differ between churned and retained customers (Welch t-test or Mann-Whitney U), and whether churn rates vary by contract and region (chi-square tests of independence with Cramér's V).
3. **Predictive last:** Train classifiers on the binary target using stratified splits and cross-validation. With 31% churn, the evaluation relies on PR-AUC and F1 rather than accuracy, and feature importance is compared against the statistical results.

The dataset is small, so cross-validation was used to keep estimates stable.

### Execution

| Specialist | Tasks Completed | Status |
|---|---|---|
| Exploratory Data Analysis | 2 | Completed |
| Statistical Analysis | 2 | Completed |
| Machine Learning | 2 | Completed |
| **Total** | **6** | **100% success, 0 failed** |

Total execution time was 49.1 seconds.

---

## Key Findings

### Exploratory Analysis

**Class distribution**
- Churned: 250 customers (31.25%)
- Retained: 550 customers (68.75%)
- Imbalance ratio: about 2.2 : 1. This is moderate. Accuracy alone would be misleading, since a model that predicts "retained" for everyone would score 68.75%.
- The train/test split (640/160) preserved this ratio exactly, at 31.25% in each set. The test set therefore contains roughly 50 churners.

**Monthly fee by churn status** (reported descriptive statistics)

| Group | n | Mean | Median | Std. Dev. |
|---|---|---|---|---|
| Retained | 550 | $66.12 | $63.35 | $28.76 |
| Churned | 250 | $79.94 | $82.92 | $27.14 |

Churned customers pay about $13.82 more on average, and the median gap is about $19.58. The spread is similar in both groups, and the churned group's distribution is shifted upward.

**Support calls by churn status**

| Group | n | Mean | Median | Std. Dev. |
|---|---|---|---|---|
| Retained | 550 | 1.34 | 1.0 | 1.08 |
| Churned | 250 | 1.84 | 2.0 | 1.33 |

Churned customers average about 0.50 more support calls. The churned group also has more variance, so high-contact customers are more concentrated among churners. Because `support_calls` is a count variable, the medians are whole numbers.

**Contract and region**
- Frequency and churn-rate breakdowns by contract and region were run, but the group-level counts and rates were not reported in the available outputs. The EDA insight on this point was generic and is not used as evidence.

### Statistical Evidence

**Hypothesis test results**

| Hypothesis | Test | P-value | Significance (α = 0.05) | Effect size | Result |
|---|---|---|---|---|---|
| Churn rate differs by contract type | Chi-square test of independence | Not reported | Not reported | Cramér's V not reported | **Fail to reject H₀** |
| Churn rate differs by region | Chi-square test of independence, multiple-comparison correction | Not reported | Not reported | Cramér's V not reported | **Fail to reject H₀** |
| `monthly_fee` differs by churn status | Welch t-test or Mann-Whitney U | Not reported | Not reported | Not reported | **Unresolved** |
| `support_calls` differs by churn status | Welch t-test or Mann-Whitney U | Not reported | Not reported | Not reported | **Unresolved** |

**What can be said**

- **Contract and region:** The chi-square tests found no statistically significant association with churn. Their p-values and effect sizes are not available, so the strength of this null result cannot be judged. It is a non-finding, not evidence that the variables have zero effect.
- **Monthly fee and support calls:** The descriptive gaps are large, but the formal test results are not in the available outputs. For reference only, the standardized difference in means (Cohen's d) calculated from the reported descriptives is about **0.49 for monthly fee** and about **0.43 for support calls**. These are moderate effects. They are not a substitute for the missing test results and should not be presented as validated significance.

**Plain-English interpretation:** Churned customers look different from retained customers on fees and support contact. Contract type and region do not show a detectable link to churn in this dataset.

### Predictive Models

**Model types tested:** Logistic regression and random forest, using stratified splits and cross-validation with class weighting or resampling.

**Performance metrics**

| Metric | Value | Notes |
|---|---|---|
| ROC-AUC (cross-validated) | 0.630 | Average across folds |
| ROC-AUC (test holdout) | 0.685 | 160 rows, about 50 churners; wide uncertainty |
| PR-AUC | Not reported | Primary metric under imbalance |
| F1 | Not reported | Needed with PR-AUC |
| Accuracy | Not reported | Not meaningful at 31% churn |
| Per-model comparison | Not reported | Logistic regression vs. random forest |

A test ROC-AUC of 0.685 means the model ranks a randomly chosen churner above a randomly chosen retained customer about 68% of the time. That is useful but limited. The cross-validated score (0.630) is somewhat lower, so the holdout result is probably optimistic, and the test set is small enough that its estimate is noisy.

**Feature importance:** Not available. The ML output described how importance should be interpreted but did not deliver a ranking. This means the models have not yet been shown to rely on fee and support calls, or on the contract and region features that the statistical tests found uninformative.

**Overfitting:** One specialist flagged possible overfitting in the random forest and recommended a larger `min_samples_leaf` or fewer trees. The output does not identify the model or show a training-versus-validation gap. Because the test score is higher than the cross-validated score, this flag needs verification before any action.

**Predictive insight:** The model has limited discrimination. It can help rank customers by risk, but it should not drive individual-level decisions without PR-AUC, F1, calibration, and threshold analysis.

---

## Synthesis

**Consistent patterns across analyses**
- **Fees and support contact are the most promising drivers.** The descriptive gaps are large and consistent across the mean and median, and the predictive model achieves above-chance performance using the features that include them. The formal tests, however, remain unconfirmed.
- **Contract and region are not supported as drivers.** The chi-square tests fail to reject the null, and this is consistent with the view that contract type and region do not separate churners in this sample. This runs against common industry assumptions and should be explored further.

**Validated hypotheses**
- None of the four hypotheses is fully validated in the available outputs.
- Two are **not supported** (contract and region), with the caveat that their statistics are missing.
- Two are **unresolved** (fee and support calls), despite strong descriptive differences.

**Cross-check gap:** The planned consistency check, which identifies robust drivers as features that are both statistically significant and high in permutation importance, cannot be performed yet because the test results and importances are missing.

---

## Conclusions

**What we can say with confidence**
1. Churn is 31.25% in this sample (250 of 800), and the stratified split preserved this rate.
2. The data is complete, with no missing values and no rows dropped.
3. Churned customers have higher average monthly fees ($79.94 vs. $66.12) and more support calls (1.84 vs. 1.34) than retained customers. These are large descriptive differences.
4. Contract type and region show no statistically significant association with churn.
5. The available predictors yield modest predictive performance (test ROC-AUC 0.685, CV ROC-AUC 0.630).

**What we cannot yet conclude**
- That fees or support calls cause churn, or that formal tests confirm the differences. Significance and effect-size results are missing.
- Which model performed better, or which features the models rely on.
- The precision, recall, and F1 achievable at a practical operating threshold.

**Interpretation:** Customers who churn tend to be the ones paying more and contacting support more. This is an association in cross-sectional data. It suggests where to look, but reducing fees or support calls would not necessarily reduce churn.

---

## Limitations & Caveats

**Data quality issues**
- **Pipeline inconsistency in `churned_flag`:** In one EDA output, `churned_flag` appears as float with NaN for a row whose raw value is "no," while the statistical output shows a clean 0/1 split (550/250). The target encoding should be verified in the source pipeline to confirm that the 250 churners are correctly labeled. The reported "0 missing" conclusion relies on the statistical run, not the EDA run.

**Statistical limitations**
- **Missing results:** Test statistics, p-values, effect sizes, confidence intervals, chi-square statistics, Cramér's V, and multiple-comparison adjustments are not in the available outputs.
- **Test choice unclear:** Welch t-test vs. Mann-Whitney U was not stated. The Shapiro-Wilk normality results were truncated. The choice matters because the t-test assumes approximate normality, while Mann-Whitney tests stochastic dominance rather than the mean difference.
- **Expected cell counts:** Chi-square tests require adequate expected counts (commonly at least 5). This is likely met for contract and region at n = 800, but small region groups were not checked.
- **Discrete variable:** `support_calls` is a count, and a t-test may be less suitable than a count-appropriate or rank-based method.

**Modeling limitations**
- **Limited features:** Only four predictors are available. Tenure, usage, payment history, and complaint type are absent, which probably explains much of the modest performance.
- **Small test set:** About 50 churners in the test set means PR-AUC and F1 would have wide confidence intervals.
- **Unverified overfitting:** The flag is unconfirmed and the affected model is unidentified.
- **Missing model details:** Per-model scores, feature importances, calibration, and threshold analysis are absent.

**Causal limitations**
- All findings are cross-sectional associations. Even a significant fee or support-call effect would not establish that changing these values would reduce churn.

**Failed analyses:** None. All six tasks completed. The gaps above reflect truncated output, not task failures.

---

## Recommendations

### Immediate Actions

1. **Verify the target encoding** in the source pipeline and confirm the 250/550 split before using these results for decisions.
2. **Recover the full statistical outputs** (stat_1 and stat_2 in particular) so the fee and support-call differences can be formally confirmed or rejected before any targeting decision relies on them.
3. **Launch a fee and support-experience review for high-contact and high-fee customers.** The descriptive gaps justify a targeted investigation, such as checking whether high-fee customers receive poor value or whether repeat support contacts signal unresolved issues. Treat this as a hypothesis test, not a validated retention lever.
4. **Do not base retention campaigns on contract type or region** until the associated statistics are reviewed. The current evidence does not support them.
5. **Use the current model only for ranking**, not for individual decisions. Report PR-AUC and F1 before any deployment.

### Future Analysis

**Questions to investigate**
- Do fees and support calls differ significantly between churners and retained customers, and what are the effect sizes with confidence intervals?
- Is the relationship between support calls and churn nonlinear, such as a threshold effect after a certain number of calls?
- Does the churn-risk ranking hold across regions, or do region-specific effects average out in the pooled analysis?
- Which model performs better, and does the random forest overfit? Compare training and validation performance directly.
- What precision and recall are achievable at a retention-campaign budget, and what is the expected return?
- Do fee and support calls interact (for example, high fees combined with high support contact)?

**Data to collect**
- **Tenure:** Time since sign-up is among the strongest churn predictors in most settings.
- **Usage metrics:** Frequency and volume of product use, which signal engagement.
- **Payment history:** Late payments, failed charges, and billing disputes.
- **Support detail:** Reason for each call, resolution status, and time to resolution.
- **Competitive and offer data:** Price comparisons, promotions, and competitor offers.
- **Customer demographics** beyond region, if available and appropriate for the use case.
- **Outcome timing:** The date of churn, which would allow survival analysis and a more detailed view of when customers leave.

Adding behavioral variables would be the most likely way to materially improve predictive performance beyond the current ROC-AUC of about 0.68.