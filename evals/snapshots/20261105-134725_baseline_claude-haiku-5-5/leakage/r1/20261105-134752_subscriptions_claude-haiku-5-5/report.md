# Data Analysis Report: Subscriptions

## Executive Summary

- **Churn is common, at 36.3%.** Of 1,000 subscribers, 363 churned and 637 were retained. This is a moderate imbalance that calls for stratified splitting and evaluation metrics beyond accuracy.
- **Refund issuance is the strongest churn signal, but it must be validated before action.** The logistic regression coefficient is +6.12 (odds ratio ≈ 456), and Gradient Boosting ranks it as the top feature. An effect this large is implausible as a causal effect and may reflect data leakage, such as refunds issued during the cancellation process. Confirming the timing of refunds relative to churn is the most important next step.
- **Engagement and tenure are associated with retention.** Churned customers average 17.3 usage hours versus 21.8 for retained customers (Welch t-test p = 1.6×10⁻¹³; Cohen's d = −0.46). Longer tenure and higher usage each lower the odds of churn after adjustment for the other variables.
- **The Pro plan is associated with lower churn.** Its odds ratio is 0.634 relative to an unnamed baseline plan. Plan-level churn rates and the chi-square test were not available in the outputs.
- **The model's near-perfect discrimination is a warning sign, not a success.** Logistic regression reaches ROC-AUC 0.9905 and accuracy 98.0% on a single test split. Values this high for churn prediction usually indicate leakage or an unrealistically easy label. Do not deploy the model until this is ruled out.

## Dataset Overview

| Attribute | Value |
|---|---|
| Source | `/workspaces/agents/evals/data/subscriptions.csv` |
| Size | 1,000 rows × 5 columns |
| Target | `churned` (binary: 1 = churned, 0 = retained) |
| Numeric features | `usage_hours` (float), `tenure_months` (integer), `refund_issued` (binary, 0/1) |
| Categorical feature | `plan` (text; levels other than Pro not named in the outputs) |
| Class split | 363 churned (36.3%), 637 retained (63.7%) |
| Missing values | Not confirmed (the data-check output is blank; completeness is assumed) |

The target is moderately imbalanced. The EDA output calls the segments both "balanced" and "large imbalance." The actual split is neither, and this report uses the 36/64 figures.

## Analysis Methodology

### Strategic Approach

The analysis used three strategies in sequence:

1. **Exploratory (first):** Examine distributions, skewness, outliers, plan frequencies, and correlations with churn. The goal was to understand the data before testing or modeling.
2. **Statistical (second):** Test whether churned and retained customers differ on usage and tenure, and whether refund issuance and plan are associated with churn. Use results to guide feature selection.
3. **Predictive (last):** Train classifiers (logistic regression, gradient boosting) on a train/test split and rank features to identify churn drivers.

This order was chosen because the target is binary, the sample size (n = 1,000) supports both hypothesis tests and a train/test split, and the statistical results were meant to inform the choice of features and models.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory data analysis (EDA) | 2 |
| Statistical | 2 |
| Machine learning | 2 |
| **Total** | **6 of 6 (100% completion rate)** |

Total execution time was 35.1 seconds. All tasks reported completion, but several outputs were truncated or incomplete, as described in the Limitations section. "Completed" means the task ran, not that every intended result was reported.

## Key Findings

### Exploratory Analysis

**Target distribution**
- 36.3% of customers churned (363 of 1,000). The majority class is retained at 63.7%.
- This imbalance is moderate. It is large enough to affect accuracy as a metric but does not require resampling by default.

**Usage hours (`usage_hours`)**

| Group | n | Mean | Median | SD |
|---|---|---|---|---|
| Churned | 363 | 17.30 | 16.20 | 8.13 |
| Retained | 637 | 21.77 | 20.50 | 10.51 |

- Both groups fail the Shapiro–Wilk normality test (churned W = 0.967, p = 2.4×10⁻⁷; retained W = 0.951, p = 1.2×10⁻¹³).
- Variances differ across groups (Levene's W = 17.76, p = 2.7×10⁻⁵). The retained group is more dispersed.
- The mean and median are close within each group, and the retained group is somewhat right-skewed, with a long upper tail.

**Tenure (`tenure_months`)**
- Tenure is an integer feature. The EDA output reports no summary statistics, skewness, or outlier counts for it. Its distribution is **not characterized** in the available outputs.

**Plan (`plan`)**
- Plan is categorical, and the example rows show values such as "pro" and "basic." Frequency counts by plan and churn rate by plan were **not reported**.

**Refunds (`refund_issued`)**
- Binary; the rate of refunds and their churn rate were not reported in the outputs.

**Correlations**
- The correlation matrix and significance tests for numeric features with `churned` are **not in the outputs**. Inter-feature correlation (e.g., usage vs. tenure) is therefore unconfirmed.

### Statistical Evidence

| Test | Purpose | Result | p-value | Effect Size | Interpretation |
|---|---|---|---|---|---|
| Shapiro–Wilk (each group) | Check normality of `usage_hours` | Non-normal in both groups | 2.4×10⁻⁷ (churned); 1.2×10⁻¹³ (retained) | — | Normality assumption violated |
| Levene's test | Check equality of variances | Unequal variances | 2.7×10⁻⁵ | — | Standard Student t-test inappropriate |
| **Welch's t-test** | Compare mean `usage_hours`, churned vs. retained | t = −7.49 | **1.6×10⁻¹³** | Cohen's d = −0.46; mean difference = −4.47 h (95% CI −5.64 to −3.30) | Churned customers use significantly fewer hours. The effect is small-to-moderate. |
| Distribution comparison (reported as "Reject H0") | Test whether `usage_hours` distributions differ | Significant | Not reported | Not reported | Supports a difference in distribution, but the test and p-value are unverified |
| Tenure comparison | Test whether `tenure_months` differs by churn | **No output** | — | — | Not validated |
| Chi-square | Association of `refund_issued` with churn | **Truncated** | — | — | Not formally tested |
| Chi-square | Association of `plan` with churn | **Truncated** | — | — | Not formally tested |
| Correlation significance | Numeric features vs. `churned` | **No output** | — | — | Not validated |

**Notes on the test choice**
- Both groups are non-normal and variances differ, so Welch's t-test (which does not assume equal variances) is a reasonable choice. With n = 363 and n = 637, the t-test is also fairly robust to non-normality through the central limit theorem.
- The output describes the choice as conditional on non-normality, but a Mann–Whitney test was **not** reported. Its result would strengthen the conclusion.

**Plain English interpretation**
- **Usage:** Churned customers log about 4.5 fewer hours than retained customers on average. This difference is statistically reliable, but it is modest relative to the spread in both groups (the two distributions overlap heavily).
- **Refunds, plan, and tenure:** The data suggests these are associated with churn, but the formal evidence is not in the outputs. Their statistical status should be treated as **unconfirmed**.

### Predictive Models

**Models tested**
1. Logistic regression (baseline; selected as best model by ROC-AUC)
2. Gradient boosting

**Performance on the held-out test set**

| Model | ROC-AUC | F1 | Accuracy | Precision | Recall |
|---|---|---|---|---|---|
| Logistic regression | 0.9905 | 0.9726 | 0.9800 | Not reported | Not reported |
| Gradient boosting | Lower than LR (exact value not reported) | Not reported | Not reported | Not reported | Not reported |

- Logistic regression's ROC-AUC, F1, and accuracy are high. Precision and recall are not reported, so we cannot tell whether the model misses churners or flags too many retained customers.
- The comparison between models is incomplete. Selecting logistic regression on ROC-AUC alone is not sufficient to claim it is the better model.
- All results come from a single train/test split, with no cross-validation.

**Feature importance (ranked)**

| Rank | Feature | Direction | Effect | Evidence |
|---|---|---|---|---|
| 1 | `refund_issued` | Increases churn | Coefficient +6.12; OR ≈ 456 | Top LR coefficient; top GB impurity importance; most sensitive under permutation importance |
| 2 | `usage_hours` | Decreases churn | Coefficient −0.81 per SD; OR = 0.446 per SD | LR coefficient |
| 3 | `tenure_months` | Decreases churn | Coefficient −0.42 per SD; OR = 0.657 per SD | LR coefficient |
| 4 | `plan_pro` | Decreases churn | Coefficient −0.46; OR = 0.634 | LR coefficient, relative to unnamed baseline plan |

- Gradient boosting importance measures magnitude only. Direction in this report comes from the logistic regression coefficients.
- The "per SD" interpretation applies to the scaled numeric features. For `refund_issued` and `plan_pro`, the odds ratio is the change from 0 to 1 and should not be described as "per SD."

**Predictive insights**
- Refund issuance dominates the model. Its effect size is roughly an order of magnitude larger than any other predictor, which is the main reason to suspect leakage.
- Usage and tenure contribute moderately, and their odds ratios are consistent with the direction of the statistical tests.
- The model's predictive power may come mostly from a single feature. Removing `refund_issued` and re-evaluating would show how much of the performance depends on it.

## Synthesis

**Validated or strongly supported findings**

| Hypothesis | Evidence | Status |
|---|---|---|
| H1: Usage hours differ between churned and retained customers | Welch t = −7.49, p = 1.6×10⁻¹³, d = −0.46 | **Supported** |
| H5: Usage and tenure are protective after adjustment | Negative LR coefficients for both | **Supported in direction**; adjusted p-values not reported |
| H3: Refund issuance is associated with churn | LR coefficient +6.12; GB rank 1; chi-square truncated | **Strongly suggested**; formal test not reported; timing unknown |
| H4: Plan type is associated with churn | LR OR = 0.634 for Pro; chi-square truncated | **Suggested**; baseline and formal test not reported |
| H2: Tenure differs between churned and retained customers | No test output | **Not validated** |

**Consistent patterns across methods**
- **Direction is consistent.** Usage, tenure, and Pro plan reduce churn odds, and refund issuance raises them. The t-test, logistic regression, and gradient boosting agree on the direction of the usage relationship and on refunds as a leading predictor.
- **A retention cluster may exist.** Engagement (usage), loyalty (tenure), and plan tier (Pro) all relate to lower churn. These may reflect one underlying factor (commitment to the service), but inter-feature correlations have not been checked, so this is a hypothesis.

**Open interactions and nonlinearities**
- No interaction terms were tested. Candidates include refund × plan and usage × tenure.
- Usage and tenure were modeled linearly. Nonlinear relationships have not been checked.

## Conclusions

**What we can say with reasonable confidence**
1. Churned customers use the service less than retained customers. The difference is statistically clear (p ≈ 10⁻¹³) but small-to-moderate in size (d = −0.46), so usage alone will not separate churners from non-churners.
2. Churn is common (36.3%) and the classes are moderately imbalanced. Evaluation should rely on precision, recall, and ROC-AUC, not accuracy alone.
3. Refund issuance is the most strongly associated feature in every model that was run.

**What we cannot yet conclude**
1. That refunds cause churn. The effect size is implausibly large, and the timing relative to churn is unknown.
2. That the model is ready for production. Its performance is suspiciously high, and precision, recall, and cross-validated results are missing.
3. How plan type, tenure, and refunds compare statistically, because their formal test results are missing.
4. Which model is better overall, since gradient boosting's metrics other than ROC-AUC are not reported.

## Limitations & Caveats

**Data quality**
- Data-check output is blank. Missing-value status is assumed, not confirmed.
- The `plan` categories beyond Pro are not named, and the baseline plan is unknown.
- Retained-group summaries for tenure and plan breakdowns are absent.
- Class labels are inconsistent: EDA calls the groups "balanced" and also reports a "large imbalance."

**Probable data leakage (highest priority)**
- An odds ratio of ~456 for refund issuance is implausible as a real-world effect.
- If refunds are issued during or after the cancellation decision, the feature encodes the outcome. This would also explain the near-perfect ROC-AUC (0.99).
- Refund timing relative to churn date has not been checked.

**Statistical assumptions and limitations**
- The usage distributions are non-normal and heteroscedastic. Welch's t-test handles unequal variances, but a Mann–Whitney test was not reported to confirm the result.
- Effect sizes are reported for usage only. Effects for tenure, refunds, and plan lack effect sizes (Cramér's V for chi-square; odds ratios with confidence intervals for the model).
- Model coefficients have no confidence intervals, and multicollinearity (VIF) was not checked, so coefficient magnitudes may be unstable.
- Odds ratios are associations, not causal effects.
- Interpreting "per SD" for binary variables is incorrect; their odds ratios describe a 0-to-1 change.

**Failed or incomplete analyses**
- No task reported outright failure, but these outputs are truncated or missing:
  - Chi-square results for refunds and plan
  - Tenure comparison test
  - Correlation significance tests
  - Distribution summaries and skewness for tenure
  - Gradient boosting F1, accuracy, precision, and recall

**Modeling limitations**
- A single train/test split makes the 0.99 AUC estimate unstable. Cross-validation is needed.
- No calibration assessment, and no confidence intervals on performance metrics.
- Default 0.5 classification threshold; business costs of false negatives and false positives were not considered.
- Time stability and cohort stability were not tested.

## Recommendations

### Immediate Actions

1. **Check refund timing before any operational use (highest priority).** Confirm whether each refund was issued before or after the churn date. If refunds occur during cancellation, remove the feature from the model and re-evaluate. Owner: data engineering with the product team.
2. **Hold model deployment.** Do not use the current model to target retention offers until leakage is ruled out and performance is validated with cross-validation.
3. **Fill the reporting gaps.** Obtain the chi-square statistics for refunds and plan, the tenure test, correlation p-values, and gradient boosting metrics. These are needed before any hypothesis is marked as validated.
4. **Clarify the plan field.** Document the plan categories and the baseline plan, and report churn rates by plan.
5. **Confirm data completeness.** Run and report a missing-value check, and document the data definitions (especially the meaning of `refund_issued` and the churn date).
6. **If the data is clean after these checks, pilot retention outreach focused on low-usage customers.** Usage is an actionable, observable signal with a clear direction. Measure the results against a control group rather than relying on the model's predictions.

### Future Analysis

**Analyses to run**
- Report precision, recall, and F1 at several thresholds, and choose a threshold based on the relative costs of missed churners and unnecessary retention offers.
- Run 5- or 10-fold cross-validation (stratified) for all models, with confidence intervals on each metric.
- Re-run the models without `refund_issued` to measure how much predictive power depends on it.
- Test interactions (refund × plan, usage × tenure) and nonlinear effects (splines or binned variables for usage and tenure).
- Check VIF and inter-feature correlations.
- Add a Mann–Whitney test and rank-biserial effect size for usage, and report chi-square statistics with Cramér's V for refunds and plan.
- Check whether relationships hold across time periods and customer cohorts.
- Compare gradient boosting and logistic regression fairly on the same metrics, and calibrate predicted probabilities.

**Data to collect**
- **Timestamps** for refunds, plan changes, cancellation requests, and churn events, so temporal ordering can be established.
- **Refund reason codes** to separate service-failure refunds from routine goodwill refunds.
- **Usage trend data** (change in usage over the last 1–3 months), since a recent drop may be more predictive than a lifetime average.
- **Support interaction history**, including ticket counts and resolution times, as a potential mechanism linking refunds and churn.
- **Customer demographics and acquisition channel**, to test whether the patterns hold across segments.
- **Clear definitions** of the plan tiers, the churn event, and the observation window.