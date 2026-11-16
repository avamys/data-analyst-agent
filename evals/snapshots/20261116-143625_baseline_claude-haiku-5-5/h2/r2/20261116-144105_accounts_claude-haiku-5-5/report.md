# Data Analysis Report: Accounts

**Status note:** Several specialist outputs were truncated or incomplete. The chi-square and t-test results, correlation matrix, cross-validation scores, logistic regression coefficients, permutation importances, and train/test metrics were not available for this report. Where a result could not be verified, this report says so rather than estimating it. Findings marked *provisional* should be confirmed once the missing outputs are reviewed.

---

## Executive Summary

- **Customer renewal is predictable from the available features.** The best reported model, a Random Forest, achieved a test ROC-AUC of 0.835 and F1 of 0.807. A second model reached 75.3% accuracy and ROC-AUC of 0.821. Both are well above chance (ROC-AUC 0.5). The model can support risk-ranking of accounts, subject to calibration checks.
- **`seats` is the leading candidate driver, but this is not yet validated.** It has the highest Random Forest impurity importance (0.314). Its direction of effect and statistical significance are not reported, and impurity importance can overstate continuous features.
- **The data is clean and the target is only mildly imbalanced.** There are no missing values in the six columns that were checked, and 57.5% of the 1,600 accounts renewed. A model that always predicts "renews" would score 57.5% accuracy, so the 75.3% reported accuracy is about 18 points better than that baseline.
- **Several numeric features are skewed and heavy-tailed.** Extreme values should be reviewed against business rules before any removal or capping, because they may represent genuine high-need or high-value accounts.
- **Decisions that can be made now:** Use the model to prioritize retention outreach in a pilot, with a threshold chosen by the business. Do not yet make claims about why customers renew, and do not act on the `seats` finding (for example, changing pricing by seat tier) until the statistical tests and permutation importance are reviewed.

---

## Dataset Overview

| Attribute | Value |
|---|---|
| Source | `/workspaces/agents/evals/data/accounts.csv` |
| Rows × columns | 1,600 × 7 |
| Target | `renewed` (binary: 1 = renewed, 0 = churned) |
| Target distribution | 920 renewed (57.5%), 680 churned (42.5%) |
| Numeric features (5) | `discount_pct`, `seats`, `support_tickets`, `contract_months`, `signup_month` |
| Categorical feature (1) | `region` (one-hot encoded for modeling) |
| Missing values | 0 in `region`, `renewed`, `discount_pct`, `seats`, `support_tickets`, `contract_months`. `signup_month` was not confirmed. |

**Feature count clarification:** The EDA brief referred to "six numeric features." The file contains five numeric features plus the binary target, which is also numeric, so the "six" count likely includes `renewed`. `signup_month` is a numeric column, but it is likely categorical or cyclical in meaning and needs appropriate encoding.

---

## Analysis Methodology

### Strategic Approach

The analysis followed a three-stage sequence:

1. **Exploratory analysis** came first to profile distributions, check data quality, confirm class balance, and inspect the categorical `region` feature.
2. **Statistical testing** followed to test whether features are associated with renewal. The planned tests were chi-square for `region` versus `renewed`, and t-tests or Mann-Whitney tests for numeric features. Mann-Whitney was flagged as more appropriate given the skew.
3. **Predictive modeling** came last, using a stratified train/test split on `renewed`. Logistic regression and tree-based models were used to provide feature importance that could confirm or extend the statistical results.

This order was sound. Profiling first prevented the models from being built on unexamined data, and the statistical tests were designed to be checked against model importance rather than used alone.

### Execution

| Specialist | Tasks Completed | Status |
|---|---|---|
| Exploratory (EDA) | 2 | Completed, outputs partly truncated |
| Statistical | 1 | Completed, results not reported in available output |
| Machine Learning | 3 | Completed, some metrics and coefficients not reported |
| **Total** | **6** | **100% completion (6/6)** |

Total execution time was 51.9 seconds. Completion status does not mean every planned output was captured. The statistical test results and several ML outputs are missing from the material reviewed.

---

## Key Findings

### Exploratory Analysis

**Target balance**
- Renewal rate is **57.5%** (920 of 1,600). Churn is 42.5% (680 accounts).
- This is mild imbalance. Accuracy remains interpretable, but precision and recall should be reported alongside it.

**Data quality**
- Zero missing values were recorded for the six columns in the validation output. The `signup_month` count and the remaining EDA missing-value table were truncated.

**Distributions**
- The EDA flagged **strong asymmetry** and **excess kurtosis above 3** for several numeric features. This indicates heavy tails.
- Several features have **few unique values**, which suggests they are discrete or ordinal (for example, `support_tickets` and `contract_months`). Exact per-feature summaries (means, medians, ranges) were not included in the available output.

**Correlations**
- The correlation matrix was requested but not reported. Multicollinearity (|r| > 0.8) could not be assessed.

**Region**
- Category frequencies for `region` were not reported, so the sizes of the regional groups are unknown. This matters because small regions can produce unstable estimates and invalid chi-square results.

### Statistical Evidence

**Status: No hypothesis test results are available in the material provided.**

| Planned test | Purpose | Result | Status |
|---|---|---|---|
| Chi-square test of independence (`region` × `renewed`) | Tests whether renewal rates differ by region | No χ², df, p-value, or Cramér's V reported | **Not reported** |
| t-tests or Mann-Whitney U (`discount_pct`, `seats`, `support_tickets`, `contract_months` by `renewed`) | Tests whether feature distributions differ between renewed and churned accounts | No test statistics, p-values, or effect sizes reported | **Not reported** |
| Correlation significance tests | Tests linear or rank association with renewal | Not reported | **Not reported** |
| Permutation importance (test set) | Confirms whether model-identified features matter | Not reported | **Not reported** |

**Plain-English interpretation:** We cannot say from the available evidence whether any individual feature is statistically associated with renewal. The model results show that the features *together* predict renewal, but they do not identify which features drive it or in what direction.

**Methodological requirements for completing these tests:**
- Use **Mann-Whitney U** or bootstrapped mean differences for numeric features, because heavy tails violate t-test normality assumptions.
- Use **chi-square** only if expected cell counts are at least 5. Check this for smaller regions, and use Fisher's exact test where it is not met.
- Report **effect sizes** (for example, rank-biserial correlation for Mann-Whitney, Cramér's V for chi-square) alongside p-values. With 1,600 rows, very small effects can reach statistical significance.

### Predictive Models

**Task:** Binary classification of renewal (57.5% positive class).

**Models tested**

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | Notes |
|---|---|---|---|---|---|---|
| Random Forest | Not reported | Not reported | Not reported | **0.807** | **0.835** | Labeled best test model. Reported to overfit. |
| Unidentified model (probably logistic regression) | **75.3%** | **0.764** | **0.826** | **0.794** | **0.821** | Internally consistent: F1 equals 2PR/(P+R) |

**Interpreting the performance**

- **Baseline comparison:** A majority-class classifier scores 57.5% accuracy. The 75.3% accuracy of the second model is about 18 percentage points above that baseline. Both models are well above the chance ROC-AUC of 0.5.
- **Model comparison:** The Random Forest leads by about 0.013 in ROC-AUC and 0.013 in F1. On a test set of roughly 320 rows (assumed from an 80/20 split, not confirmed), the standard error of an AUC near 0.83 is roughly 0.02. The difference between the two models is therefore within the range of sampling noise and should not be treated as a meaningful ranking.
- **Accuracy uncertainty:** At about 320 test rows, a 75% accuracy carries an approximate 95% confidence interval of ±4–5 points.
- **Precision/recall trade-off:** The second model catches 82.6% of renewing accounts (recall) and its positive predictions are correct 76.4% of the time (precision). Which of these matters more depends on the cost of an unnecessary retention offer versus a missed opportunity, and that trade-off has not been defined.
- **Overfitting:** Three reports note a "noticeable train-test gap," but no training or cross-validation scores were provided, so its size is unknown.

**Feature importance**

| Feature | Importance (Random Forest, impurity-based) | Direction | Status |
|---|---|---|---|
| `seats` | **0.314** (highest) | Not reported | Impurity-based; not confirmed by permutation importance |
| Other features | Not reported | Not reported | Not available |

- Impurity importance favors continuous or high-cardinality features. `seats` may be ranked highly partly for that reason. Permutation importance on the test set is needed to confirm.
- Logistic regression coefficients were described only in terms of sign convention. The actual coefficients and directions are missing.
- `region`'s contribution to prediction is unknown.

**Predictive insights**
- The features collectively carry real signal for renewal. The model can rank accounts by likely renewal, which is useful for prioritization.
- The ranking's reliability is not yet established, because it depends on unverified calibration and on importance measures that have not been cross-checked.

---

## Synthesis

**Validated hypotheses:** None. No statistical test results were available for review, so no relationship between a specific feature and renewal can be confirmed.

**Consistent patterns across analyses:**

1. **Predictive signal exists.** Both models perform well above baseline. This is the most robust finding in the report.
2. **`seats` is the most prominent feature in the model.** It is the only feature with a reported importance value, but its statistical status and direction are unknown, so this is a lead to investigate, not a conclusion.
3. **Distributional issues are present.** Heavy tails and skew were flagged in the EDA. These affect both statistical test choice and impurity-based importance, so they could inflate the apparent importance of continuous features like `seats`.

**Unresolved tension:** The model's top feature may reflect its scale or distribution rather than its business importance. Until permutation importance and the statistical tests are reviewed together, the two cannot be reconciled.

---

## Conclusions

**What we can say with reasonable confidence**

- The 1,600-account dataset is complete for the columns checked, with no missing values recorded.
- Renewal is a mildly imbalanced outcome: 57.5% renew, 42.5% churn.
- Account features predict renewal well above chance. The best model reaches ROC-AUC of about 0.82–0.84.
- The predictive signal is strong enough to support a risk-ranking pilot.

**What we cannot yet say**

- Which individual features drive renewal, or in which direction.
- Whether `seats` is a true driver of renewal or an artifact of its distribution.
- Whether `region` or `discount_pct` is associated with renewal.
- Which of the two models is genuinely better, given the size of the difference relative to sampling noise.
- How well predicted probabilities match actual renewal rates (calibration).

**Bottom line:** The data supports *prediction* of renewal. It does not yet support *explanation* of renewal. Decisions about pricing, discounts, or account management should wait until the explanatory analyses are complete.

---

## Limitations & Caveats

**Data quality**
- Missing-value counts for `signup_month` and the remaining EDA checks were truncated. Full completeness is confirmed only for the six columns in the validation output.
- The feature count is inconsistent across reports: "six numeric features" versus five numeric features plus a categorical feature.
- Heavy tails and excess kurtosis were flagged. Extreme values have not been checked for business validity. They should not be removed or capped without review.
- `signup_month` is numeric in the file but is likely categorical or cyclical. Treating it as a plain integer implies a false ordering (December is not "greater" than January).

**Statistical assumptions**
- Parametric tests (t-tests) are inappropriate for skewed, heavy-tailed features without transformation. Non-parametric alternatives are needed.
- Chi-square results depend on adequate expected cell counts, which may not hold for small regions.
- With 1,600 rows, statistical significance is easy to reach for small effects. Effect sizes are necessary for interpretation.

**Failed or incomplete analyses**
- No chi-square, t-test, Mann-Whitney, or correlation results were available.
- The correlation matrix was not reported, so multicollinearity cannot be assessed.
- Permutation importance on the test set was not reported.
- Logistic regression coefficients are missing.
- No cross-validation scores or train-test metrics were reported, so overfitting cannot be quantified.

**Conflicting metrics**
- Two sets of headline metrics appear (ROC-AUC 0.821 vs. 0.835; F1 0.794 vs. 0.807). It is unclear whether they come from different models or different runs.
- The 75.3% accuracy is attached to an unidentified model.

**Modeling limitations**
- A single train/test split with no reported variance. The Random Forest's advantage may not hold across repeated splits.
- No calibration analysis. ROC-AUC shows ranking ability but not whether predicted probabilities are accurate.
- No threshold analysis. The default 0.5 cutoff may not suit the business objective.
- One-hot encoding of `region` may produce unstable coefficients for sparse regions.

---

## Recommendations

### Immediate Actions

1. **Retrieve and review the statistical output.** Obtain the chi-square and Mann-Whitney (or bootstrap) results with p-values and effect sizes for all planned features. This is the highest-priority gap.
2. **Reconcile the model metrics.** Confirm which model produced each metric set, and whether the two sets come from the same split.
3. **Run permutation importance on the held-out test set** for all features, and compare the ranking with the impurity-based ranking. Treat `seats` as unconfirmed until this is done.
4. **Report training, cross-validation, and test scores together**, and repeat the split (or use repeated stratified CV) to estimate variance in the model comparison.
5. **Define the decision threshold with the business.** Specify the relative cost of a missed churner versus an unnecessary retention offer. Use that cost to choose between the recall-favoring and precision-favoring operating points.
6. **Pilot risk-based outreach cautiously.** The model can prioritize accounts for retention contact in a limited test with a control group, so the business impact can be measured. Do not use it to change pricing or discounts yet.
7. **Review extreme values** in `seats` and `support_tickets` with business stakeholders before any capping or removal.

### Future Analysis

**Questions to investigate**
- Why does `seats` matter? Is it a proxy for account size, pricing tier, or engagement? What is its direction of effect?
- Is `discount_pct` associated with renewal, and does the association reflect retention value or a signal of lower-value accounts?
- Does `region` matter after controlling for other features?
- Is there seasonality in `signup_month`? Do accounts acquired in certain months renew at different rates?
- Are extreme `support_tickets` values high-need customers or data errors?
- How large is the overfitting gap, and does hyperparameter tuning reduce it?

**Analyses to add**
- Calibration curves and Brier scores, to determine whether predicted probabilities can be used directly for ranking or expected-value calculations.
- Partial dependence or SHAP analysis, to show how renewal probability changes with each feature.
- Interaction tests (for example, `seats` × `contract_months`), since the Random Forest may capture interactions that the statistical tests miss.
- Cost-sensitive threshold analysis, once the business cost ratio is defined.

**Data that would help**
- Account revenue or contract value, to distinguish account size from seat count.
- Product usage or engagement metrics (logins, feature adoption), which may explain renewal more directly than the current features.
- Customer tenure and prior renewal history.
- Reason codes for churn, where available, to validate model predictions against stated reasons.
- Explicit definitions of `region` and `signup_month` encoding, plus a data dictionary for all seven columns.
- Timestamps for the renewal decision, so the model can be tested on future cohorts rather than a random split.