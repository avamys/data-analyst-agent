# Data Analysis Report: Customer Churn

## Executive Summary

- **Churn affects nearly one in three customers.** Of 800 customers, 250 (31.25%) churned and 550 (68.75%) were retained. Because of this imbalance, accuracy is a misleading metric. A model that predicts "retained" for everyone would score 68.75%.
- **Contract type is significantly associated with churn, but the effect is small.** The chi-square test gives χ² = 22.84, p = 1.76e-06. Cramér's V, derived from the reported statistic, is about 0.17. The association is real but modest in magnitude. Per-contract churn rates were not reported, so the direction of the effect is unconfirmed.
- **Region is not associated with churn.** The chi-square test gives p = 0.448, so there is no evidence that region should guide retention targeting.
- **The best model (class-weighted logistic regression) is useful for ranking risk but not for precise targeting.** On the held-out test set it reaches ROC-AUC 0.711, F1 0.609, and 70% churner recall. Precision was not reported. The random forest overfit (train/test AUC gap of 0.325) and caught only 40% of churners.
- **Decision readiness: moderate.** The model can support a risk-ranked outreach list, with a recall-first threshold. Before committing budget, the direction of the contract and fee effects should be confirmed and precision should be measured.

> **Verification note:** Several specialist outputs were truncated, and key values (per-category churn rates, exact monthly_fee and support_calls p-values, effect sizes, model coefficients, precision, and random forest test AUC) were not reported. This report states those gaps explicitly rather than filling them in. Figures marked *derived* were calculated from reported values, with assumptions noted.

---

## Dataset Overview

- **Source:** `/workspaces/agents/evals/data/customers.csv`
- **Size:** 800 rows × 5 columns, no missing values, no rows dropped
- **Target:** `churned_flag` (binary: yes/no, mapped to 1/0 with no unmappable values)
- **Features:**
  - *Numeric (2):* `monthly_fee` (float), `support_calls` (integer)
  - *Categorical (3):* `contract` (observed values include annual and monthly), `region` (observed values include north, south, east), plus the target
- **Class balance:** 550 retained (68.8%), 250 churned (31.2%). This is moderate imbalance.

---

## Analysis Methodology

### Strategic Approach

The analysis followed three strategies in priority order:

1. **Exploratory analysis** (first): to verify data quality, target balance, categorical frequencies, and feature distributions before any testing.
2. **Statistical testing** (second): chi-square tests for the categorical features and group comparisons (Welch t-test or Mann-Whitney U) for the numeric features, with attention to class imbalance.
3. **Predictive modeling** (third): a stratified train/test split with class weighting, evaluated on ROC-AUC, precision, recall, and F1 rather than accuracy. Model importances were to be checked against the statistical findings.

This order ensured that modeling decisions (stratification, weighting, metric choice) were grounded in the observed imbalance and tested relationships.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory (EDA) | 2 |
| Statistical | 2 |
| Machine Learning | 2 |
| **Total** | **6 of 6 (100%)** |

Total execution time was 74.9 seconds. All tasks completed, but several outputs were truncated, which limits the depth of the findings below.

---

## Key Findings

### Exploratory Analysis

**Target distribution**
- 250 of 800 customers churned (31.25%); 550 were retained (68.75%).
- The churn-to-retain ratio is about 1:2.2. The imbalance is moderate, but enough to make accuracy unreliable and to justify class weighting.

**Data quality**
- No missing values, no unmappable target values, and no coercion failures in `monthly_fee` or `support_calls`.
- The dataset is clean enough for direct analysis.

**Categorical features**
- Contract and region categories and their frequencies were examined, but the per-category counts and churn rates were **not reported**. The contract churn rates needed to interpret the chi-square result are therefore unavailable.

**Numeric features**
- Distribution summaries, outlier checks, and churned-vs-retained comparisons for `monthly_fee` and `support_calls` were requested, but the output was **not reported**. The correlation between the two was also not reported.

### Statistical Evidence

| Hypothesis | Test | Statistic | p-value | Significant at α = 0.05? | Effect size |
|---|---|---|---|---|---|
| Churn is associated with contract | Chi-square independence | χ² = 22.84, df = 1 | 1.76e-06 | **Yes** | Cramér's V ≈ 0.17 (*derived*) |
| Churn is associated with region | Chi-square independence | χ² not reported | 0.448 | No | Not reported |
| Churners and retained differ in monthly_fee | Welch t-test or Mann-Whitney U (not specified) | Not reported | < 0.05 (exact value not reported) | **Yes** | Not reported |
| Churners and retained differ in support_calls | Welch t-test or Mann-Whitney U (not specified) | Not reported | < 0.05 reported, output not shown | **Reported as yes; unverified** | Not reported |

**Interpretation in plain English**

- **Contract:** Churn is not independent of contract type. The evidence against independence is very strong. However, the effect is small. A Cramér's V of about 0.17 means contract explains only a small share of the variation in churn. Statistical significance here reflects a reliable pattern, not a large one. This was derived assuming an uncorrected 2×2 chi-square on two contract levels; if a continuity correction was applied, the value will be slightly lower.
- **Region:** No evidence of any association with churn. With the reported p-value, the sample gives no reason to think region differences in churn exist, though a small effect could still be missed at this sample size.
- **Monthly fee:** Churned and retained customers differ in monthly fee at the 5% level. The direction of the difference (whether churners pay more or less) was not reported, and the magnitude is unknown.
- **Support calls:** The significance result is reported but its supporting output is not shown, so treat it as provisional until verified.

**Assumption checks**
- The normality check that determined the choice of Welch's t-test vs. Mann-Whitney U was not reported.
- Expected cell counts for the chi-square tests were not reported. With 800 rows and two-level contract variables, counts are probably adequate, but this needs confirmation.
- Four univariate tests were run without multiple-comparison correction. With p-values this small for contract, this is unlikely to change conclusions, but it is worth noting for the two borderline-type results.

### Predictive Models

**Models tested**
- Class-weighted logistic regression
- Class-weighted random forest

**Validation design**
- Stratified train/test split (the 20% test split is assumed based on the methodology; the test size was not explicitly stated, so the test churner count of roughly 50 is an estimate).
- Metrics: ROC-AUC, F1, recall, and precision (accuracy was deliberately not used as the primary metric).

**Performance (held-out test set)**

| Metric | Logistic Regression (balanced) | Random Forest (balanced) |
|---|---|---|
| ROC-AUC | **0.711** | Below 0.711 (exact value not reported) |
| F1 (churn class) | **0.609** | Not reported; likely lower |
| Recall (churners) | **70%** | 40% |
| Precision (churners) | Not reported | Not reported |
| Accuracy | Not reported | Not reported |
| Train/test AUC gap | Not reported | 0.325 (overfitting) |

**What these numbers mean**
- **ROC-AUC 0.711:** A randomly chosen churner is ranked above a randomly chosen retained customer about 71% of the time. This is better than chance but modest.
- **Recall 70%:** Roughly seven of every ten churners are identified. At the test set's likely size of about 50 churners (*estimate*), this is roughly 35 caught and 15 missed. The random forest's 40% recall corresponds to roughly 20 caught.
- **Random forest overfitting:** A train/test AUC gap of 0.325 indicates the model memorized noise in an 800-row dataset. Since logistic regression scored higher on test AUC, the random forest's test AUC must be below 0.711, which is an inference, not a reported value.
- **Precision:** Unknown. Without it, the cost of false alarms (contacting customers who would not have churned) cannot be assessed.

**Feature importance**
- Logistic coefficients and random forest importances were **not reported**. Feature rankings within the models are therefore unconfirmed.
- Based on the univariate tests, contract, monthly_fee, and support_calls are the likely drivers, and region is likely weak. This alignment has not been verified against model outputs.

**Predictive insights**
- The signal in these four features is largely approximately linear and additive: the simpler model generalized better.
- The modest AUC indicates that important churn drivers are missing from the data (tenure, usage, complaints, and price changes are typical examples).

---

## Synthesis

**Validated across analyses**
- **Contract and churn are linked.** This is the most robust finding: a significant chi-square result, with the linear model relying on the same signals.
- **Region is not useful for targeting.** Consistent with the null chi-square result.
- **Monthly fee differs between churners and retained customers** (significant, direction and size unconfirmed).

**Tensions**
- **Statistical significance vs. predictive power.** Contract is highly significant (p ≈ 1.8e-06), but its effect is small (V ≈ 0.17), and overall predictive power is modest (AUC 0.711). Significant group differences do not translate into strong individual-level prediction.
- **Recall vs. precision.** Logistic regression wins on recall and F1, so the models do not conflict. But the trade-off against precision cannot be quantified without the reported value.

**Caution on direction:** The analysis does not establish whether month-to-month (or any specific) contract type carries higher churn risk. The direction of the contract and fee effects must be confirmed from the per-category rates and model coefficients before any targeting rule is built on them.

---

## Conclusions

**What we can say with confidence**
1. Churn is a minority outcome (31%) in this customer base.
2. Churn is associated with contract type, though the association is small in magnitude.
3. Region has no detectable association with churn.
4. A class-weighted logistic regression on these four features can rank customers by churn risk better than chance (AUC 0.711) and identifies about 70% of churners at the default threshold.
5. A random forest on these features overfits and performs worse on the held-out set.

**What we cannot yet say**
- Which contract types churn more, and by how much.
- Whether churners pay higher or lower fees, or call support more often.
- How precise the model's flags are, and therefore how much retention budget would be wasted.
- Whether the modest predictive performance can be improved with better features or non-linear methods.
- Whether any retention offer would actually reduce churn. The data is cross-sectional and cannot establish causation.

---

## Limitations & Caveats

**Data quality and reporting gaps**
- The dataset itself is clean (no missing values or coercion issues).
- Several analysis outputs were truncated or contain artifacts (e.g., stray "driving cell):" fragments), and key numbers are missing.
- Missing: per-category churn rates, chi-square degrees of freedom for region, Cramér's V as reported, exact monthly_fee and support_calls p-values, test choice for numeric comparisons, group means/medians, effect sizes (Cohen's d or rank-biserial r), correlation between monthly_fee and support_calls, outlier summaries, coefficients, feature importances, precision, accuracy, and the random forest test AUC.
- Region has at least three levels (north, south, east were observed), so its chi-square degrees of freedom should be greater than 1. The contract test was reported with df = 1, consistent with two levels.

**Statistical and methodological limitations**
- **Small test-set counts:** With roughly 50 churners in the test set (*estimate*), the 70% vs. 40% recall difference rests on a small number of cases. Confidence intervals are needed.
- **Single split:** Results come from one train/test split. Cross-validation or repeated splits are needed to confirm that AUC 0.711 is stable.
- **Default threshold:** The 0.5 threshold was probably used. Recall-oriented threshold tuning was not explored.
- **Limited features:** Only four features were available. Important churn drivers are absent.
- **No interaction terms:** Whether contract effects vary by fee level or support-call volume is untested.
- **Multiple testing:** Four univariate tests without correction. Low risk for the contract result, but noted.
- **Causality:** Cross-sectional data can show association, not cause.

**Failed analyses:** None failed outright, but the reporting gaps above mean several planned checks (feature-importance cross-validation against statistical findings, normality-driven test selection, and per-category rate reporting) could not be verified.

---

## Recommendations

### Immediate Actions

1. **Use the logistic model as a risk-ranking tool, not a final decision.** Its 70% recall and 0.711 AUC make it suitable for prioritizing outreach lists, especially where missing a churner is more costly than a false alarm.
2. **Do not use region for targeting.** The evidence shows no association with churn.
3. **Before launching any contract-based targeting, pull the churn rate by contract type and the logistic coefficients.** This confirms the direction of the effect. Targeting decisions should not be made on the assumption that a specific contract type is the high-risk group.
4. **Measure precision at the planned threshold** so the cost of false positives is known before the retention budget is committed.
5. **Run a controlled pilot.** Randomly assign high-risk customers to retention offers and a holdout group. This is the only way to determine whether the offers reduce churn, as opposed to merely identifying who is likely to churn.

### Future Analysis

**Re-run and complete the current analysis**
- Regenerate the missing outputs: per-category churn rates, exact p-values, effect sizes (Cohen's d or rank-biserial r), coefficients, feature importances, and precision/accuracy.
- Report confidence intervals for recall, precision, and AUC.
- Verify the support_calls result, which is currently reported without supporting output.

**Improve model robustness**
- Use repeated stratified cross-validation to test the stability of AUC 0.711.
- Test a shallower or regularized random forest, and gradient boosting, to see whether the overfitting gap can be closed without losing performance.
- Tune the decision threshold against the retention budget and cost of false positives.
- Test interaction terms (contract × monthly_fee, contract × support_calls).

**Investigate further questions**
- Does churn risk rise non-linearly with support calls, for example above a threshold?
- Is the null region result real, or does it mask regional differences in pricing or service?
- What is the causal effect of retention offers? Uplift modeling or an A/B test is required.

**Data to collect**
- **Tenure:** how long the customer has been with the company (often the strongest churn predictor).
- **Usage and engagement:** product or service usage levels, trends over time.
- **Complaint details:** nature and resolution of support calls, not just their count.
- **Price history:** recent fee increases or discounts.
- **Competitive context:** competitor offers or market events.
- **Time-based data:** churn dates and observation windows, to support survival analysis and to separate early from late churn.
- **Larger sample:** more churners would narrow confidence intervals and make the model comparison more reliable.