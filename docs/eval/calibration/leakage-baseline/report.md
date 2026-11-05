# Data Analysis Report: Subscriptions

## Executive Summary

- **Refund status is the strongest reported predictor of churn, but its causal role is unverified.** Logistic regression gives `refund_issued` the largest standardized coefficient (+3.32), and permutation testing on a tree-based model shows that shuffling it lowers test ROC-AUC by 0.51. Refunds may drive churn, follow from it, or both. Until the timing of refunds relative to cancellation is confirmed, refund policy should not be treated as a retention lever.
- **Lower usage is associated with higher churn.** Churned customers averaged 17.3 usage hours versus 21.8 for retained customers (medians 16.2 vs. 20.5). The gap is about 4.5 hours, roughly a 0.46 standardized difference (derived, see Statistical Evidence). This is the clearest directional finding that does not depend on the disputed refund variable.
- **Churn affects 36.3% of customers.** Of 1,000 subscribers, 363 churned and 637 were retained. This is a substantial share, so retention work is justified, and accuracy alone would be a misleading evaluation metric.
- **The predictive model performs very well, which raises a warning as much as a result.** Logistic regression reaches a test ROC-AUC of 0.9914. That level is unusually high for churn on five raw columns and is consistent with either a near-deterministic signal or target leakage. It should not be deployed until it is validated.
- **Several results are incomplete.** Plan-level churn rates, chi-square statistics, effect sizes for the categorical tests, and gradient boosting metrics were not reported. Decisions about plan pricing or targeting cannot yet be supported by the evidence.

## Dataset Overview

| Attribute | Value |
|---|---|
| Source | `/workspaces/agents/evals/data/subscriptions.csv` |
| Size | 1,000 rows × 5 columns |
| Target | `churned` (binary: 1 = churned, 0 = retained) |
| Numeric features | `usage_hours` (float), `tenure_months` (int), `refund_issued` (binary int) |
| Categorical feature | `plan` (one-hot encoded for modeling) |
| Missing values | None in any column |
| Class balance | 363 churned (36.3%), 637 retained (63.7%) |

The dataset is small and simple. Five columns limit the number of potential drivers, and 1,000 rows give adequate power for large effects but limited power for small ones or for complex models.

## Analysis Methodology

### Strategic Approach

The analysis proceeded in three stages:

1. **Exploratory analysis** came first to check data quality, distributions, class balance, plan mix, raw churn patterns, and correlations with the target. The data was clean, so this stage focused on understanding the shape of the variables before testing.
2. **Statistical testing** followed to check whether observed differences were unlikely to be chance. The plan: chi-square tests for plan and refund status against churn, and Welch t-tests or Mann-Whitney U tests for usage and tenure, chosen by normality.
3. **Predictive modeling** came last. A stratified train/test split supported logistic regression and gradient boosting classifiers, with feature importance used to rank drivers.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory Data Analysis | 2 |
| Statistical Analysis | 2 |
| Machine Learning | 2 |
| **Total** | **6 of 6 (100% completion, 0 failures)** |

Total execution time was 23.8 seconds. Completion status does not guarantee complete reporting. Several requested outputs (listed under Limitations) were not returned.

## Key Findings

### Exploratory Analysis

**Data quality.** All five columns are complete, with zero missing values. Data types are as expected.

**Class balance.** Churn is 36.3% (363 of 1,000). This is a moderate imbalance: not severe enough to require resampling, but enough that accuracy is not a meaningful headline metric.

**Usage hours.**

| Group | n | Mean | Median | SD | Skew |
|---|---|---|---|---|---|
| Churned | 363 | 17.30 | 16.20 | 8.13 | 0.73 |
| Retained | 637 | 21.77 | 20.50 | 10.51 | 0.92 |

Both groups are right-skewed. Churned customers use the product less, and their distribution is tighter. Mean and median both sit lower for churned customers, so the difference is not driven by a few extreme values.

**Plan mix and raw churn rates by plan.** Plan frequencies and churn rates by plan were requested but not reported. Plan is known to be associated with churn (see Statistical Evidence), but the direction and size of each plan's effect are unknown.

**Refund status and raw churn rates.** Churn rates by refund status were requested but not reported. The model results suggest refunded customers churn at higher rates, but this has not been confirmed with raw counts.

**Tenure and outliers.** Tenure distribution summaries, outlier counts for usage and tenure, and the correlation matrix were requested but not returned. No statements about tenure's distribution, outliers, or linear relationships with churn can be made from the evidence.

### Statistical Evidence

**Normality check (Shapiro-Wilk)**

| Variable × Group | p-value | Result |
|---|---|---|
| Usage hours, churned | 2.4 × 10⁻⁷ | Non-normal |
| Usage hours, retained | 1.2 × 10⁻¹³ | Non-normal |

Both groups fail normality. With n ≈ 1,000 the Shapiro-Wilk test is sensitive to small departures, so the skew values (0.73 and 0.92) are more informative: they indicate moderate right-skew, which a rank-based test handles well. The output designates Mann-Whitney U as the primary test for usage hours.

**Group comparison: usage hours (churned vs. retained)**

- **Test:** The output designates Mann-Whitney U as primary, but the section header reads "Welch's t-test," and the test statistic and p-value for the comparison were not reported. This inconsistency must be resolved before the result is cited formally.
- **Result:** The report states that H0 was rejected at α = 0.05. The exact p-value is not reported.
- **Effect size (derived, not reported):** Using the reported means and SDs, the mean difference is 4.47 hours and the pooled standard deviation is about 9.7 hours, giving Cohen's d ≈ 0.46. The Welch t-statistic implied by these descriptives is roughly 7.5, which corresponds to a p-value well below 0.001. These are approximations from summary statistics, not tested results, but they are consistent with the reported rejection.
- **Plain English:** Churned customers use about 4.5 fewer hours per period on average. The difference is statistically clear and of moderate practical size.

**Group comparison: tenure months.** The output reports H0 rejected at α = 0.05. No test statistic, p-value, group descriptives, or effect size were reported. The direction of the tenure difference is therefore unknown and should not be stated.

**Chi-square tests of independence**

| Test | Result | Test statistic | p-value | Effect size (Cramér's V) |
|---|---|---|---|---|
| Plan vs. churned | Reject H0 (p < 0.05) | Not reported | Not reported | Not reported |
| Refund status vs. churned | Reject H0 (p < 0.05) | Not reported | Not reported | Not reported |

The outputs do not attribute the five unlabeled "REJECT H0" statements to specific tests, so these two results are inferred. Expected cell counts were not checked, which matters if any plan category is sparse. Without Cramér's V, the strength of either association cannot be compared with the others.

**Summary of hypothesis results**

| Hypothesis | Test (inferred) | Significant at α = 0.05 | Effect size |
|---|---|---|---|
| Plan type is associated with churn | Chi-square | Yes | Not reported |
| Refund status is associated with churn | Chi-square | Yes | Not reported |
| Usage hours differ by churn status | Mann-Whitney U (or Welch t) | Yes | d ≈ 0.46 (derived) |
| Tenure differs by churn status | Mann-Whitney U (or Welch t) | Yes | Not reported |

### Predictive Models

**Models tested:** Logistic regression and gradient boosting classifiers, with one-hot encoded plan and scaled numeric features. The split was stratified; the exact train/test sizes were not reported.

**Performance**

| Model | Test ROC-AUC | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|---|
| Logistic regression | 0.9914 | Not reported | Not reported | Not reported | Not reported |
| Gradient boosting | Not reported | Not reported | Not reported | Not reported | Not reported |

Logistic regression has the highest reported ROC-AUC, but the comparison is incomplete. Gradient boosting's results are missing entirely, so no performance ranking can be confirmed.

**Feature importance**

- **Logistic regression coefficients:** `refund_issued` has the largest standardized coefficient (+3.32). The positive sign indicates higher churn odds when a refund was issued. Other coefficients were not reported.
- **Permutation importance (tree-based model):** Shuffling `refund_issued` reduces test ROC-AUC by 0.51, the largest reported effect. Other features' permutation effects were not reported. The output refers to a random forest, while the model setup refers to gradient boosting, so the model behind this result is uncertain.
- **Impurity importances (gradient boosting):** Not reported.

**Predictive insights**

- Refund status dominates both the linear and tree-based models, which suggests the signal is not an artifact of one modeling assumption.
- A ROC-AUC near 0.99, combined with a 0.51 drop when one feature is shuffled, suggests that `refund_issued` carries most of the predictive signal. If it separates churners almost perfectly, the other features add little.
- Usage and tenure do not appear among the reported top predictors, even though usage differs significantly between groups. This suggests their signal overlaps with refund status or is weaker in a multivariate setting.

## Synthesis

**Validated, cross-method findings**

1. **Refund status is the most consistently supported driver.** It appears as the top predictor in two model families and has a significant association with churn in the chi-square results. Its direction (higher refund, higher churn) is consistent across the reported outputs.
2. **Lower usage is linked to churn.** Descriptive statistics, a significant rank-based comparison, and a moderate effect size agree on direction and magnitude. This is the most defensible directional finding in the analysis.
3. **Plan type is associated with churn**, based on a significant chi-square result. Its magnitude and direction are unknown.

**Findings with limited support**

- Tenure differs significantly between groups, but its direction and size are unknown.
- Plan's contribution to prediction beyond refund status is unknown.

**Key caveat on synthesis.** The strongest model result (ROC-AUC 0.99, refund as the dominant driver) is also the result most exposed to the leakage concern. The statistical and model findings do not yet form a fully corroborated picture, because the most influential variable may not be a valid pre-churn predictor.

## Conclusions

**What we can say with confidence**

- Churn affects 36.3% of the 1,000 customers in this dataset.
- Churned customers use the product less than retained customers: about 17.3 vs. 21.8 hours on average, with a moderate effect size (d ≈ 0.46).
- Churn is significantly associated with plan type and refund status, and with tenure, based on the reported rejections of H0.
- Refund status is the strongest feature in the reported predictive models.

**What we cannot yet say**

- Whether refunds cause churn, result from it, or are caused by a third factor.
- Which plan has the highest churn, or whether plan matters beyond refund status.
- Whether tenure is protective or risky.
- Whether the 0.99 ROC-AUC will hold on new data or without refund status.
- Which model is best, since gradient boosting results are missing.

## Limitations & Caveats

**Data quality**
- No missing values were found in the dataset. The outlier analysis for usage and tenure was requested but not reported, so outlier influence is unknown.
- The dataset has five columns, which limits the scope of possible drivers.

**Statistical assumptions and limitations**
- The Shapiro-Wilk test rejects normality for usage hours in both groups. Mann-Whitney U is the appropriate choice, but the output's header refers to Welch's t-test, creating ambiguity about which test was run.
- Chi-square tests assume adequate expected cell counts; this was not verified.
- Five significance statements are not attributed to specific tests, and no p-values are reported for any comparison. Only the threshold (α = 0.05) is known.
- Observational data cannot establish causation. All findings are associations.

**Failed or incomplete analyses**
- All six specialist tasks completed, but the following outputs are missing or truncated: chi-square statistics and Cramér's V; Mann-Whitney or Welch statistics and confidence intervals; the correlation matrix; outlier counts; raw churn rates by plan and refund status; plan mix frequencies; gradient boosting metrics; and the train/test split details.
- The output does not confirm whether the missing-value check was actually run, though the results show zero missing values.

**Model risks**
- **Possible leakage (most important).** `refund_issued` may be recorded after a customer decides to cancel, in which case it is a consequence of churn rather than a predictor. If so, the 0.9914 ROC-AUC is inflated.
- The model's ROC-AUC has not been validated with cross-validation or repeated splits.
- The random forest vs. gradient boosting discrepancy in the permutation result is unresolved.
- No calibration or threshold analysis has been performed, so the model is not ready for scoring customers operationally.

## Recommendations

### Immediate Actions

1. **Verify the timing of refunds before using them in any decision.** Confirm whether `refund_issued` is recorded before or after cancellation. Until this is answered, do not change refund policy on the assumption that refunds drive churn, and do not deploy the current model.
2. **Pull the missing reports.** Obtain plan-level and refund-level churn rates, the chi-square statistics with Cramér's V, the group-comparison test statistics with p-values and confidence intervals, and the gradient boosting metrics. These are the numbers needed for stakeholder decisions.
3. **Investigate the usage-churn relationship as a retention signal.** Customers with low usage hours are more likely to churn (16.2 vs. 20.5 median hours). Usage-based engagement outreach is a reasonable, low-risk test, provided it is evaluated with a controlled experiment.
4. **Re-run the model under robustness checks.** Use cross-validation, drop `refund_issued`, and report precision, recall, and F1 at a defined threshold. Compare the result with a baseline that uses only usage and tenure.

### Future Analysis

**Questions to answer**
- Is refund status a pre-churn or post-churn event? This determines whether it is usable for prediction and whether it can be a retention lever.
- What are the churn rates by plan, and does plan add predictive value once refund status is controlled for?
- What is the direction of the tenure effect, and does it interact with usage or refund status?
- Does the usage effect persist after controlling for plan and refund status in a multivariable model?
- What decision threshold balances false positives and false negatives for retention outreach, given the cost of each?

**Analyses to add**
- Effect sizes and confidence intervals for all group comparisons
- Cramér's V and expected-count checks for the chi-square tests
- Interaction tests (refund × plan, usage × tenure)
- Calibration analysis and threshold selection
- Repeated cross-validation and a holdout test set reserved for final evaluation

**Data to collect**
- Timestamps for each refund and cancellation event, so that temporal ordering can be established
- Refund reason codes and amounts, to distinguish service-failure refunds from routine ones
- Usage trends over time (for example, 30-day change), not just a single usage total
- Customer demographics, acquisition channel, and support-ticket history, which could explain churn beyond the five current columns
- Cancellation reasons from exit surveys, to validate the model's findings against stated customer intent