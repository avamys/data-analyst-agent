# Data Analysis Report: Subscriptions

## Executive Summary

- **More than one in three customers churned.** Of 1,000 subscribers, 363 (36.3%) churned. The target is moderately imbalanced, so accuracy alone is a weak measure of model quality.
- **Basic-plan customers churn at a notably higher rate.** 42.8% of basic subscribers churned, compared with 29.3% on Plus and 29.8% on Pro (derived from reported counts). That is a gap of about 13 percentage points. The association is statistically significant (χ² ≈ 19.0, df = 2, p ≈ 0.00007, derived by us), but the effect is small (Cramér's V ≈ 0.14). Plan alone does not explain most churn.
- **Usage, tenure, and refund status are all significantly associated with churn**, according to the specialist tests. Refund status is the most directly actionable lever, but the direction of its effect has not been confirmed, so we cannot yet say whether refunds reduce churn or signal dissatisfaction.
- **A logistic regression reached a test ROC-AUC of 0.9903.** This is exceptionally high for churn data and should be verified (through a leakage audit and cross-validation) before it informs any deployment decision.
- **Several key statistics are missing from the outputs.** Chi-square statistics for refund, all t-test statistics, all effect sizes except the one we derived, and the random forest results were not reported. Directional conclusions for usage, tenure, and refund therefore remain provisional.

## Dataset Overview

| Attribute | Value |
|---|---|
| Source | `/workspaces/agents/evals/data/subscriptions.csv` |
| Size | 1,000 rows × 5 columns |
| Target | `churned` (binary: 1 = churned, 0 = retained) |
| Numeric features | `usage_hours` (float), `tenure_months` (integer), `refund_issued` (binary 0/1) |
| Categorical feature | `plan` (basic, plus, pro) |
| Missing values | 0 |
| Duplicate rows | 3 (0.3%) |
| Class balance | 36.3% churned / 63.7% retained |

`churned` is the target and was excluded from predictors to prevent leakage. `refund_issued` is binary, so it is a numeric column in storage but a categorical in meaning.

## Analysis Methodology

### Strategic Approach

Three strategies were applied in this order:

1. **Exploratory analysis** came first. The dataset is small and clean, so distributions, outliers, category counts, and the churn cross-tabulation could be checked quickly and used to validate the target.
2. **Statistical testing** came second, to establish which relationships are significant before modeling. The tests were chi-square tests of independence (plan and refund vs. churn), t-tests and point-biserial correlations (usage and tenure vs. churn).
3. **Predictive modeling** came last. The binary target and 1,000 rows support a stratified 80/20 train/test split with logistic regression and tree-based models, with feature importance informed by the statistical results.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory (EDA) | 2 |
| Statistical | 2 |
| Machine Learning | 2 |
| **Total** | **6 of 6 (100% success)** |

Total execution time was 26.7 seconds. All tasks completed, but several specialist outputs were truncated, which limits the statistical detail available.

## Key Findings

### Exploratory Analysis

**Churn rate and class balance**
- Overall churn is 36.30% (363 of 1,000). Retention is 63.70% (637).
- The imbalance is moderate, not severe. A model that predicted "retained" for everyone would score 63.7% accuracy, so precision, recall, and ROC-AUC are the appropriate evaluation metrics.

**Plan distribution and churn by plan**

| Plan | Customers | Retained | Churned | Churn Rate | Difference from Overall |
|---|---|---|---|---|---|
| Basic | 512 (51.2%) | 293 | 219 | **42.77%** | +6.5 pp |
| Plus | 297 (29.7%) | 210 | 87 | 29.29% | −7.0 pp |
| Pro | 191 (19.1%) | 134 | 57 | 29.84%* | −6.5 pp |
| **Total** | **1,000** | **637** | **363** | **36.30%** | |

*Pro's churn rate was derived from the reported contingency counts; the specialist output truncated that row.

- Basic is the largest plan and the highest-churn plan. Plus and Pro churn at similar rates. Combined, Plus and Pro churn at 29.5% (144 of 488).

**Numeric features and outliers**
- `usage_hours` has the most IQR outliers: 19 rows (1.90%).
- Outliers are few and may represent genuine heavy users rather than data errors. Their churn rate has not been checked.
- Outlier counts for `tenure_months` were not reported.
- The EDA output says "four numeric features" but lists three. The count is consistent with the dataset if `churned` is counted as the fourth numeric column, which the prompt also implies.

**Data quality**
- No missing cells.
- Three duplicate rows (0.3%). The impact is minor, but these should be checked to determine whether they are data-entry duplicates or legitimate repeated records.

### Statistical Evidence

**1. Chi-square test of independence: plan vs. churn**
- **Purpose:** Test whether churn status is independent of plan tier.
- **Result:** Rejected H0 (significant at p < 0.05, per the specialist output).
- **Test statistic and p-value (reported):** Not in the provided output. We computed them from the reported contingency table to fill this gap: **χ² ≈ 19.0, df = 2, p ≈ 0.00007**.
- **Effect size (derived):** Cramér's V ≈ **0.14**, which is a small effect by conventional thresholds (0.1 small, 0.3 medium).
- **Interpretation:** Plan tier and churn are clearly related. Basic-plan customers are overrepresented among churners. The association is real, but plan tier alone explains only a small share of the variation in churn.
- **Cell contributions:** The specialist output truncated the cell-level detail. Based on our calculation, the largest contributions come from the basic-plan cells (basic churned contributes about 5.9 of the 19.0 total; basic retained about 3.4), which is consistent with the basic-plan finding.

**2. Chi-square test of independence: refund_issued vs. churn**
- **Result:** Rejected H0 (significant at p < 0.05).
- **Test statistic, p-value, and effect size:** Not reported. The contingency table was not provided, so we could not compute them.
- **Interpretation:** Refund status is associated with churn. The direction is not established. Refunds could reduce churn (a remedy) or occur because a customer is already dissatisfied (a warning sign). This distinction determines the appropriate business response.

**3. t-test and point-biserial correlation: usage_hours vs. churn**
- **Result:** Significant at p < 0.05 for both tests.
- **Group means, t-statistic, effect size (Cohen's d), and correlation coefficient (r):** Not reported.
- **Interpretation:** Usage differs between churned and retained customers. The direction (whether churners use more or less) was not stated and must be confirmed from group means before any business interpretation.
- **Method caveat:** Usage has outliers, so a Welch t-test or Mann-Whitney U test should be used to confirm the result is not driven by extreme values.

**4. t-test and point-biserial correlation: tenure_months vs. churn**
- **Result:** Significant at p < 0.05 for both tests.
- **Test statistics and effect sizes:** Not reported.
- **Interpretation:** Tenure differs between churned and retained customers. As with usage, the direction must be confirmed. Intuitively, longer-tenured customers would churn less, but this is an assumption until the group means are checked.

**Hypothesis summary**

| Hypothesis | Test | Result | Effect Size | Status |
|---|---|---|---|---|
| H1: Churn independent of plan | Chi-square | Rejected (p < 0.05) | V ≈ 0.14 (derived) | **Supported** |
| H2: Churn independent of refund | Chi-square | Rejected (p < 0.05) | Not reported | **Supported** (direction unknown) |
| H3: usage equal across churn groups | t-test | Rejected (p < 0.05) | Not reported | **Supported** (direction unknown) |
| H4: tenure equal across churn groups | t-test | Rejected (p < 0.05) | Not reported | **Supported** (direction unknown) |
| H5: usage uncorrelated with churn | Point-biserial | Rejected (p < 0.05) | r not reported | **Supported** |
| H6: tenure uncorrelated with churn | Point-biserial | Rejected (p < 0.05) | r not reported | **Supported** |

All six hypotheses are supported at the significance level. None of the numeric tests can yet be interpreted for magnitude or direction.

### Predictive Models

**Models tested**
- Logistic regression
- Random forest (results not reported in the provided outputs)

**Setup**
- Predictors: `usage_hours`, `tenure_months`, `plan` (one-hot encoded), `refund_issued`
- Excluded: `churned` (target)
- Split: 80/20 stratified train/test (about 200 test rows)

**Performance**

| Model | Test ROC-AUC | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|---|
| Logistic Regression | **0.9903** | Not reported | Not reported | Not reported | Not reported |
| Random Forest | Not reported | Not reported | Not reported | Not reported | Not reported |

Logistic regression was selected on test ROC-AUC. The ML summary also concluded that the simpler model is sufficient, but that conclusion cannot be verified without the random forest results.

**Overfitting diagnosis:** The ML summary reports both "overfitting" and "a small gap with similar test" performance. These statements conflict. Train metrics were not provided, so this cannot be resolved.

**Feature importance:** No coefficients, odds ratios, or permutation importance values were reported. Based on the significant bivariate tests, usage, tenure, plan, and refund are the likely drivers. This is a hypothesis and should not be presented as a ranked finding until coefficients are extracted.

**Predictive insights**
- The four features carry strong predictive signal in combination. A test ROC-AUC near 0.99 means the model ranks churners above retained customers almost every time.
- The AUC is unusually high. It may reflect a highly separable dataset, a leakage pathway, or sampling noise on a small test set. It should not be used for decisions until verified.

## Synthesis

**Validated, consistent patterns**
1. **Churn is common (36.3%)** and concentrated in the basic plan (42.8%).
2. **Four features are significantly associated with churn:** plan, refund status, usage hours, and tenure. Each was significant in its own univariate test.
3. **The multivariate model achieved very high discrimination (AUC 0.99)**, which is consistent with those four features jointly carrying most of the signal. Univariate tests cannot establish joint effects, so this is supportive, not proof.

**Where the analyses agree and where they don't**
- Plan is the only factor with a fully quantified effect size (V ≈ 0.14). Its effect is significant but small on its own.
- Usage, tenure, and refund are significant but unquantified. Until their effect sizes and directions are reported, we cannot compare their importance to plan.

**Open interactions**
- No interaction terms (for example, plan × tenure or refund × usage) were tested. We cannot say whether the basic-plan churn gap is the same across tenure or usage levels.

**Possible segment**
- The 19 high-usage outliers may form a distinct segment. Their churn rate has not been checked.

## Conclusions

**What we can say with confidence**
- Churn is 36.3% in this sample, and basic-plan customers churn at 42.8%, about 13 percentage points above Plus and Pro combined (29.5%).
- The plan-churn association is statistically significant (χ² ≈ 19.0, df = 2, p ≈ 0.00007), but small in size (Cramér's V ≈ 0.14).
- Usage, tenure, and refund status are each significantly associated with churn.
- Churn can be predicted from these four features far better than chance on this data (AUC 0.99), subject to validation.

**What we cannot yet say**
- The direction of the usage, tenure, and refund effects. We cannot say whether low usage or short tenure drives churn, or whether refunds help or harm retention.
- Which feature is most important. No coefficients or importance values were reported.
- Whether the 0.99 AUC is real. It may be inflated by leakage or sampling variability.
- Whether the basic-plan gap is caused by price, service level, or who selects that plan.

## Limitations & Caveats

**Data quality**
- Three duplicate rows (0.3%). Need to confirm whether they are true duplicates.
- Outlier analysis covers only `usage_hours`. Outliers in `tenure_months` were not reported.
- The dataset appears cross-sectional, so temporal stability cannot be assessed.

**Statistical assumptions**
- The t-tests assume approximate normality and equal variances. `usage_hours` has outliers, so Welch or Mann-Whitney tests should confirm the results.
- Chi-square tests require expected cell counts of at least 5. We checked the plan table (smallest expected count is about 69 for the churned Pro cell, so the assumption holds for plan). The refund table was not provided, so this was not verified for refund.
- Point-biserial correlation is a special case of Pearson correlation and carries the same normality concerns.

**Failed or incomplete analyses**
- Refund chi-square statistic, p-value, and effect size: not reported.
- All t-test statistics, group means, and Cohen's d: not reported.
- All correlation coefficients (r): not reported.
- Random forest results: not reported.
- Correlation matrix among numeric features (requested in EDA; not reported).
- Correlation significance tests (requested of the statistical specialist; not reported).
- Feature importances and model coefficients: not reported.
- Precision, recall, F1, and accuracy for both models: not reported.
- Train vs. test metrics for the overfitting diagnosis: not reported.

**Contradictions and inconsistencies**
- Overfitting vs. "small gap with similar test" (the ML summary states both).
- The EDA output lists three numeric features while describing four.
- The EDA outlier analysis treated `refund_issued` as a numeric feature, which is inappropriate for a binary variable. Outlier results for `refund_issued` should be disregarded.

**Model validity**
- The ROC-AUC of 0.9903 is very high for churn prediction. The test set is about 200 rows, so a confidence interval is needed. The model was evaluated on a single split, so cross-validation is needed.
- A leakage audit is needed. Confirm that no feature, particularly `refund_issued`, was recorded after the customer had already decided to leave.
- No threshold or calibration analysis was performed, so the model cannot yet guide a retention budget.

## Recommendations

### Immediate Actions

1. **Do not deploy the churn model yet.** Verify the 0.99 AUC first through a leakage audit and 5-fold stratified cross-validation. If the score holds, the model is a candidate for risk ranking.
2. **Target basic-plan retention efforts as a test, not a full rollout.** The basic-plan churn rate (42.8%) is the clearest actionable segment. Run a controlled pilot (for example, a plan-upgrade offer or onboarding check-in) and measure churn against a holdout group.
3. **Pull the missing statistics before interpreting refunds.** Report the refund chi-square statistic and contingency table, and the group means for usage and tenure. The direction of these effects determines what action to take.
4. **Review the three duplicate rows** and decide whether to remove them.
5. **Check whether the high-usage outliers churn at a different rate** before treating them as noise.

### Future Analysis

**Questions to investigate**
- What is the direction and size of the usage, tenure, and refund effects? Report Cohen's d and point-biserial r.
- Do plan, refund, and usage interact? Test whether the refund effect differs by plan, and whether the usage effect differs by tenure.
- Why do basic-plan customers churn more? Separate price, service level, and selection effects.
- Which customers should be contacted, and at what risk threshold? Evaluate precision and recall at candidate thresholds, and weigh retention value against intervention cost.
- Does the churn pattern hold over time? A cohort or time-based split would test temporal stability.

**Data to collect**
- **Refund timing** relative to the churn decision, to resolve the direction question and rule out leakage.
- **Reason for churn** (price, product, service, competitor), to explain the basic-plan gap.
- **Plan change history** (upgrades and downgrades), to see whether basic-plan customers were previously on other tiers.
- **Customer demographics and acquisition channel**, to test whether the basic-plan gap reflects who selects that plan.
- **Support interactions and satisfaction scores**, to distinguish dissatisfaction from price-driven churn.
- **Timestamps** for subscription start, churn, and observation windows, to enable survival analysis and temporal validation.