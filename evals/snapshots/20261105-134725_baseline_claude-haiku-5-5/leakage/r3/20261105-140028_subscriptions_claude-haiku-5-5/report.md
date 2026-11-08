# Data Analysis Report: Subscriptions

## Executive Summary

- **Churn is common and concentrated in the Basic plan.** 36.3% of the 1,000 subscribers churned. Basic subscribers churn at 42.8%, compared with 29.3% on Plus and 29.8% on Pro. The plan difference is statistically significant (χ² ≈ 19.0, df = 2, p ≈ 0.0001), though the effect is small (Cramér's V ≈ 0.14). Basic is the clearest starting point for retention work.
- **The reported predictive performance is too strong to deploy as-is.** The model reports ROC-AUC 0.990 and accuracy 0.980, but nearly all predictive weight sits on `refund_issued` (permutation importance drop of 0.449 in ROC-AUC). If refunds are recorded at or after cancellation, the model is learning the outcome, not predicting it.
- **Refund issuance is significantly associated with churn, but its direction and size are not yet documented.** The test rejected independence, but the reports omit the p-value, the effect size, and the churn rate for refunded versus non-refunded customers. Establishing the timing of refunds relative to cancellation is the top priority.
- **Usage and tenure are significantly associated with churn, but their direction is unknown.** Both tests were significant, but the reports do not state whether heavier-using or longer-tenured customers churn more or less. Until that is known, these variables cannot guide retention actions.
- **Decision now:** Use the Basic-plan churn gap to prioritize retention outreach. Hold any automated churn-scoring deployment until the refund leakage check and a cross-validated, refund-free model are complete.

---

## Dataset Overview

| Attribute | Value |
|---|---|
| Source | `/workspaces/agents/evals/data/subscriptions.csv` |
| Rows × columns | 1,000 × 5 |
| Target | `churned` (binary: 1 = churned, 0 = retained) |
| Numeric features | `usage_hours` (float), `tenure_months` (int), `refund_issued` (binary int) |
| Categorical features | `plan` (basic, plus, pro) |
| Missing values | None reported for `usage_hours`, `tenure_months`, or `churned` (status for `plan` and `refund_issued` was truncated in the output) |
| Class balance | 637 retained (63.7%), 363 churned (36.3%) |

`churned` was excluded from the feature set to prevent target leakage.

---

## Analysis Methodology

### Strategic Approach

The analysis followed a three-stage sequence:

1. **Exploratory analysis** came first to confirm the distributions of the numeric variables, check the categorical plan variable, and review each variable's relationship with churn. With no missing values in the core fields, the data was ready for direct examination.
2. **Statistical testing** came next to validate the relationships before modeling. Chi-square tests were applied to the categorical variables (`plan`, `refund_issued`), and Welch's t-test and point-biserial correlation to the numeric variables (`usage_hours`, `tenure_months`).
3. **Predictive modeling** came last. Because the target is binary and 1,000 rows is adequate for a train/test split, classification models with permutation-based feature importance were used to measure how well the features predict churn.

Testing before modeling ensures that model results can be compared with independent statistical evidence. It also surfaces disagreements between the two, as the plan variable did here.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory Data Analysis | 2 |
| Statistical Testing | 2 |
| Machine Learning | 2 |
| **Total** | **6 of 6 (100% success, 0 failures)** |

Total execution time was 58.4 seconds.

---

## Key Findings

### Exploratory Analysis

**Target distribution**
- 363 of 1,000 customers churned (36.3%). The majority-class baseline accuracy is therefore 63.7%.

**Plan and churn (cross-tabulation)**

| Plan | Retained | Churned | Total | Churn Rate |
|---|---|---|---|---|
| Basic | 293 | 219 | 512 | **42.8%** |
| Plus | 210 | 87 | 297 | 29.3% |
| Pro | 134 | 57 | 191 | 29.8% |
| **All** | **637** | **363** | **1,000** | **36.3%** |

Basic accounts for 51.2% of customers but 60.3% of churners (219 of 363). Plus and Pro churn at similar rates, so the difference is mainly between Basic and the other two tiers.

**Numeric features**
- `usage_hours` and `tenure_months` were examined for distribution, outliers, and correlation with churn. The output for these checks was not reported, so no means, medians, skewness values, outlier counts, or correlation coefficients can be stated.

**Refund issuance**
- Refund frequencies and churn rates by refund status were requested but not reported.

### Statistical Evidence

All tests were run at α = 0.05.

**1. Chi-square test of independence: Plan vs. Churn**
- **Purpose:** Determine whether churn rates differ across plans.
- **Result:** Reject H0. Plan and churn are not independent.
- **Test statistic (recomputed from the reported contingency table):** χ² ≈ 19.0, df = 2, p ≈ 0.0001.
- **Effect size (recomputed):** Cramér's V ≈ 0.14, a small effect.
- **Interpretation:** Basic-plan customers churn at a higher rate than customers on the other two plans. The association is real but modest, and plan alone explains little of the variation in churn.
- *Note: The original report did not state the p-value or effect size. These figures were calculated from the reported counts and should be confirmed against the source output.*

**2. Chi-square test of independence: Refund Issued vs. Churn**
- **Purpose:** Determine whether refund status is associated with churn.
- **Result:** Reject H0 at α = 0.05.
- **Test statistic, p-value, effect size, and direction:** Not reported.
- **Interpretation:** Refund status and churn are associated. Whether refunds increase or decrease churn cannot be determined from the available output.

**3. Welch's t-test: Usage Hours by Churn Status**
- **Purpose:** Test whether mean `usage_hours` differs between churned and retained customers.
- **Result:** Reject H0. The difference is statistically significant.
- **Test statistic, p-value, confidence interval, and direction:** Not reported.
- **Interpretation:** Usage differs by churn status, but the direction is unknown.
- *Note: The source output for this test was truncated and contained contradictory log lines (for example, a line describing a "correlation" under a t-test heading). Treat this result as provisional.*

**4. Point-biserial correlation: Tenure Months vs. Churn**
- **Purpose:** Test whether `tenure_months` is correlated with churn.
- **Result:** Reject H0. The correlation is statistically significant.
- **Correlation coefficient, p-value, and confidence interval:** Not reported.
- **Interpretation:** Tenure is associated with churn, but the strength and direction are unknown.

**Summary of hypothesis tests**

| Hypothesis | Test | Result | Effect Size Reported |
|---|---|---|---|
| Plan is independent of churn | Chi-square | Rejected | Yes (recomputed: V ≈ 0.14) |
| Refund status is independent of churn | Chi-square | Rejected | No |
| No mean difference in usage hours by churn | Welch's t-test | Rejected | No |
| Tenure is uncorrelated with churn | Point-biserial | Rejected | No |

All four hypotheses were rejected, but only one effect size could be stated. With multiple tests and no stated correction, the p-values should be adjusted (for example, with Holm or Benjamini-Hochberg) before being cited as final.

### Predictive Models

**Models**
- The task specified a comparison of logistic regression and random forest. Only logistic regression feature importance was reported explicitly. The random forest results were not provided, so a side-by-side comparison is not possible.

**Performance (test set, as reported in the synthesis; model attribution not confirmed)**

| Metric | Value | Context |
|---|---|---|
| ROC-AUC | 0.990 | Near-perfect ranking of churners above non-churners |
| Accuracy | 0.980 | 34 points above the 63.7% majority baseline |
| Recall | 0.973 | Captures about 97% of churners |
| F1 | 0.973 | Balanced precision and recall |
| Precision | Not reported | Because recall and F1 are equal, precision is approximately 0.973 by arithmetic, subject to rounding |

**Feature importance (logistic regression, permutation-based, drop in ROC-AUC when shuffled)**

| Rank | Feature | Importance | Notes |
|---|---|---|---|
| 1 | `refund_issued` | 0.449 | Dominant; far larger than any other feature |
| 2 | `usage_hours` | Not reported | |
| 2 | `tenure_months` | Not reported | |
| 4 | `plan` | Near zero | Adds little predictive power despite its significant association with churn |

**Predictive insights**
- Predictive power is concentrated in a single feature. Removing refund status would likely reduce performance substantially. The size of that reduction is the key robustness check.
- The very high ROC-AUC is inconsistent with a 1,000-row, four-feature dataset unless a strong signal (possibly leakage) is present. Cross-validation results were not reported.
- Plan is significant in isolation but unimportant in the model, which suggests its association with churn is explained by other variables, such as usage or tenure. This was not tested directly.

---

## Synthesis

**Consistent patterns**
- **Refund status, usage, tenure, and plan are all associated with churn** in the statistical tests, and the ML model uses the same variables. Statistical and predictive evidence agree on which variables matter.
- **Refund status is the strongest predictor** in the model, which is consistent with its significant association in the chi-square test.
- **Basic-plan customers churn at a higher rate** (42.8% vs. about 29% on other plans), confirmed by the chi-square test.

**Points of disagreement**
- **Plan:** The statistical test shows a significant association, but the model assigns it almost no importance. The most likely explanation is confounding with usage or tenure, though this has not been tested.

**Concerns that affect interpretation**
- The headline model performance depends heavily on one variable whose timing relative to churn is unknown.
- Several key statistics (p-values, effect sizes, directions, confidence intervals, and the random forest results) are missing from the outputs, so the synthesis relies on significance decisions rather than quantified effects.

---

## Conclusions

**What we can say with confidence**
1. **Churn is concentrated in the Basic plan.** Basic customers churn at 42.8%, compared with about 29% on Plus and Pro. This difference is statistically significant (p ≈ 0.0001) and is the most reliable actionable finding.
2. **Refund status, usage, and tenure are associated with churn.** All three are statistically significant, though their direction and magnitude have not been reported.
3. **The model's headline performance cannot yet be trusted for deployment.** The 0.990 ROC-AUC is driven largely by one variable whose timing relative to churn is unverified.

**What we cannot yet conclude**
- Whether refunds cause churn, result from it, or are a leaky proxy for it
- Whether heavier-using or longer-tenured customers churn more or less
- How well the model performs without `refund_issued`
- Which model (logistic regression or random forest) performs better
- The false-positive rate and the precision of the model

---

## Limitations & Caveats

**Data quality**
- **Possible target leakage:** `refund_issued` may be recorded at or after cancellation. This is the most serious issue in the analysis.
- **Missing status for `plan` and `refund_issued`:** The data check output was truncated before these columns were reported. Missingness should be confirmed.
- **Undocumented data timing:** No information is available on when observations were recorded or whether the sample covers a single period.

**Statistical limitations**
- **Incomplete reporting:** P-values, effect sizes, confidence intervals, and directions are missing for three of the four tests. Only the plan effect size could be calculated, and that calculation used reported counts.
- **Chi-square assumptions:** Expected cell counts were not reported. Expected counts for the plan table are all above 5, so the test is valid there. Refund-table counts were not available.
- **Assumption checks for t-tests:** Normality and equal variance of `usage_hours` were not assessed. With n = 1,000, Welch's t-test is reasonably robust to non-normality, but a Mann-Whitney test would provide a useful check if the distribution is skewed.
- **Multiple comparisons:** No correction was applied across the four primary tests or the exploratory comparisons.
- **Association, not causation:** None of the tests establish causal effects.

**Modeling limitations**
- **Incomplete model comparison:** Random forest results are missing, so the requested comparison was not completed.
- **No cross-validation reported:** A single train/test split on 1,000 rows yields unstable estimates, especially for ROC-AUC near 1.0.
- **Attribution unclear:** The reported metrics do not specify which model produced them.
- **No confusion matrix or calibration analysis:** False-positive and false-negative counts and the reliability of predicted probabilities are unknown.
- **Interactions untested:** Whether refund or plan effects vary by tenure or usage was not examined.

**Failed or incomplete analyses**
- Outlier analysis, distribution statistics, and the correlation matrix produced no reported findings.
- Cross-tabulations for refund status were not reported.
- The t-test output was truncated and contained inconsistent log lines.
- The random forest comparison was not reported.

All six tasks completed without execution failures, but several outputs were incomplete at the reporting stage.

---

## Recommendations

### Immediate Actions

1. **Target Basic-plan retention now.** Basic customers churn at 42.8%, versus about 29% on other plans. Retention offers or onboarding outreach directed at Basic subscribers can proceed without waiting for the model to be validated. Measure impact through a controlled test.
2. **Do not deploy the current model for automated churn scoring.** The 0.990 ROC-AUC may reflect leakage. Until the refund check is complete, the model should not drive customer-facing decisions.
3. **Verify when `refund_issued` is recorded relative to cancellation.** Confirm with the data owners whether refunds occur before, at, or after the cancellation date. If refunds occur at or after cancellation, exclude the variable from the model.
4. **Rerun the model without `refund_issued`.** Report ROC-AUC, recall, precision, and calibration. This is the key robustness test. Use stratified k-fold cross-validation.
5. **Report the missing statistics.** Obtain p-values, test statistics, effect sizes, confidence intervals, and churn rates by refund status and by usage and tenure quartiles.

### Future Analysis

**Questions to investigate**
- What is the direction and size of the refund, usage, and tenure effects? Do refunds increase churn, and do heavy users churn less?
- Is plan's association with churn explained by usage or tenure? Fit a logistic regression with plan, usage, and tenure together and compare coefficients.
- Do predictors interact? For example, does the refund effect differ by plan?
- How do logistic regression and random forest compare on cross-validated ROC-AUC, precision, recall, and calibration?
- Is the model calibrated? Predicted probabilities matter for allocating retention budgets, not just for ranking.
- What is the cost trade-off? Estimate the cost of a retention offer against the value of a retained customer to set the decision threshold.
- Is the 36.3% churn rate stable over time? Temporal validation would show whether the model generalizes.

**Data to collect**
- **Timestamps** for refund issuance, cancellation, plan changes, and usage, so that leakage and causal ordering can be checked
- **Cancellation reason codes** to distinguish voluntary churn from involuntary churn (such as payment failure)
- **Plan change history** to see whether customers downgrade into Basic before churning
- **Engagement and support data** (support tickets, complaints, feature adoption) to explain why Basic customers churn more
- **Customer acquisition channel and cohort** to test whether churn differences reflect who was acquired rather than what plan they chose
- **Revenue or contract value per plan** to translate churn differences into financial impact