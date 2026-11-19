# Data Analysis Report: Visits

## Executive Summary

- **Tier and quarter are the predictors supported by this analysis.** A logistic regression model using only these two variables achieved a held-out test ROC-AUC of 0.9218 and a cross-validated ROC-AUC of 0.9076. The close agreement between the two suggests the estimate is not badly overfit.
- **Tier has a statistically significant association with repeat visits.** A chi-square test of independence rejected the null hypothesis. The test statistic, p-value, and effect size were not captured in the available outputs, so the strength of the association is unquantified.
- **Numeric features (age, distance_km, staff_on_shift) add little demonstrated value.** None were retained in the final models, and only one of four group comparisons rejected the null. Whether they contribute in combination with tier and quarter has not been tested.
- **The data are clean and ready for use.** There are 2,000 rows, 6 columns, and no missing values. One duplicate row was found and needs a documented decision.
- **Before operational use, the team needs the missing numbers.** Odds ratios, per-tier and per-quarter repeat rates, and classification metrics at a chosen threshold are required to turn these findings into targeting or staffing decisions.

## Dataset Overview

| Attribute | Value |
|---|---|
| Source | `/workspaces/agents/evals/data/visits.csv` |
| Rows × columns | 2,000 × 6 |
| Target | `repeat_visit` (binary: 0/1) |
| Features | 5 numeric (`age`, `distance_km`, `staff_on_shift`, plus the integer-coded `quarter` and `repeat_visit`), 1 categorical (`tier`) |
| Quarter | Integer-coded; treated as categorical because the codes carry no inherent order |
| Missing values | 0 in every column |
| Duplicate rows | 1 |

*Note on feature types:* `quarter` is listed as `category` in one EDA output and `int64` in another. Encoding should be confirmed before any model is reproduced.

## Analysis Methodology

### Strategic Approach

The analysis followed a three-stage sequence, with each stage informing the next:

1. **Exploratory analysis** came first to check data quality, target distribution, outliers in `distance_km` and `age`, and tier category frequencies before any modeling.
2. **Statistical testing** came second to test whether tier, quarter, and the numeric features are related to `repeat_visit`, which guided feature selection.
3. **Predictive modeling** came last, using a train/test split with classification models and feature importance. With 2,000 rows, this was sufficient for a split and for comparing a small number of models.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory Data Analysis | 2 |
| Statistical Analysis | 2 |
| Machine Learning | 2 |
| **Total** | **6 of 6 (100% success, 0 failures)** |

Total execution time was 44.2 seconds.

## Key Findings

### Exploratory Analysis

- **Data completeness:** All 2,000 rows are complete across all six columns. No imputation is needed.
- **Duplicates:** One duplicate row was detected (0.05% of rows). It is immaterial to the results but its handling is undocumented.
- **Target distribution:** The outputs do not report the class split of `repeat_visit`. The statistical outputs did not flag severe imbalance, but the actual proportion of repeat visits is **not reported** and should be confirmed.
- **Tier categories:** Category frequencies were requested but not reported in the available outputs.
- **Outliers in `distance_km` and `age`:** Outlier counts and distribution shape were requested but not reported. Their status is unconfirmed.
- **Multicollinearity:** The diagnostic flagged "notable" collinearity among numeric features, but no VIF or condition-number values were reported. Because the final models exclude these features, this has limited impact on current conclusions.

### Statistical Evidence

| Test | Purpose | Result | P-value | Effect Size | Interpretation |
|---|---|---|---|---|---|
| Chi-square test of independence | Does repeat-visit rate depend on tier? | **Rejected H₀** | Not reported | Not reported (e.g., Cramér's V) | Repeat-visit rates differ across tiers. The size of the difference is unknown. |
| Group comparisons, numeric features by `repeat_visit` (t-test or Mann-Whitney, 4 comparisons) | Do numeric features differ between repeat and non-repeat visitors? | **1 rejected, 3 failed to reject** | Not reported | Not reported | Only one numeric feature shows a group difference. Which one is not identified. |
| Pearson and Spearman correlations, numeric features vs. `repeat_visit` | Are numeric features linearly or monotonically related to the target? | **Rejected H₀ for at least one feature** | Not reported | Not reported | A weak relationship exists for at least one feature. The feature is not identified. |
| Holm-adjusted screen (training data) | Does quarter contribute signal after correcting for multiple comparisons? | **Retained** | Adjusted p-value not reported | Not reported | Quarter's signal survives multiple-testing correction. |

**Plain-English summary:** Tier and quarter are the most reliable signals. Tier's association is statistically significant, and quarter survived a conservative screen. The numeric features show weak or unclear marginal relationships, and the outputs do not say which feature drove each result.

### Predictive Models

**Models tested:** Logistic regression and random forest, evaluated with cross-validation and a held-out test set. Both used tier and quarter.

| Model | CV ROC-AUC | Test ROC-AUC | Status |
|---|---|---|---|
| Logistic regression | **0.9076** | **0.9218** | Selected |
| Random forest | Similar to logistic regression (value not reported) | Not reported | Flagged for overfitting; train/test scores not provided |

**Other metrics:** Accuracy, precision, recall, and F1 were requested but **not reported**. For a repeat-visit target, these determine operational value. A threshold must be chosen based on the relative cost of false positives and false negatives before these numbers can be interpreted.

**Feature importance:**
- Tier and quarter are the only features in the final models.
- Logistic regression odds ratios were not reported, so the direction and magnitude of each effect are unknown.

**Predictive insights:**
- A two-variable model reaches an AUC above 0.90, which indicates that repeat visits are strongly concentrated in tier and quarter. An AUC this high from two categorical variables is unusually strong and should be checked for leakage or artifacts in how the data were generated before it is relied on.
- The test AUC (0.9218) is close to the CV estimate (0.9076), which is reassuring. Both come from a single split, however, so their stability is not established.

## Synthesis

**Validated across analyses:**
- **Tier is associated with repeat visits.** This is the most clearly supported finding. It was confirmed by the chi-square test and by its retention in the predictive models.
- **Quarter carries independent predictive signal.** It survived Holm-adjusted screening on training data and was retained in the final model.
- **Tier and quarter together produce strong discrimination.** The model's AUC of 0.92 on held-out data is consistent with the statistical findings.

**Consistent patterns:**
- The statistical and predictive results point the same way: the outcome is concentrated in tier and quarter.
- The numeric features were weak in the statistical tests and were excluded from the models. This is consistent, though the specific features behind the single significant group comparison and the correlation result are not identified.

**Unresolved inconsistency:**
- The correlation tests rejected H₀ for at least one numeric feature, yet no numeric feature was retained. Either the Holm-adjusted screen was stricter than the unadjusted tests, or the correlation was too weak to matter. The team should identify the feature and its adjusted p-value to resolve this.

## Conclusions

**What we can say with confidence:**
1. Repeat-visit rates differ by tier (chi-square rejected independence).
2. Quarter contributes predictive signal beyond chance after multiple-testing correction.
3. A logistic regression model using tier and quarter discriminates well on held-out data (test ROC-AUC 0.92).
4. The dataset is complete and usable.

**What we can say only provisionally:**
1. The numeric features add little value on their own. This is based on exclusion from the final models, not on a nested comparison.
2. The strength of the tier effect is positive but its magnitude is unknown.
3. Logistic regression is preferable to random forest. The random forest comparison is incomplete, and the overfitting claim lacks supporting numbers.

**What we cannot say:**
1. The size of any effect in operational terms (odds ratios and repeat rates are missing).
2. Why quarter matters. Seasonality, staffing cycles, and campaign timing are all plausible, but the data cannot distinguish among them.
3. Whether any intervention would change repeat behavior. These are predictive associations, not causal effects.

## Limitations & Caveats

**Data quality:**
- One duplicate row; handling is undocumented.
- Inconsistent data type for `quarter` (`category` vs. `int64`) across outputs.
- Class balance, tier frequencies, and outlier counts were not reported.

**Statistical assumptions and limitations:**
- The t-tests assume approximate normality. Mann-Whitney alternatives were available, but which test was applied to each feature is not stated.
- Chi-square validity depends on adequate expected cell counts, which were not verified.
- Multiple comparisons were corrected for quarter (Holm) but the handling of the other tests is not documented.
- Correlations and group differences do not establish causation.

**Modeling limitations:**
- Test performance comes from a single stratified split. Confidence intervals or repeated cross-validation are needed to judge stability.
- An AUC above 0.90 from two variables warrants a leakage check.
- Random forest's test results are missing, so the model comparison is incomplete.

**Failed analyses:** None. All six tasks completed. However, several outputs are truncated summaries, and key statistics (p-values, effect sizes, coefficients, confusion-matrix metrics, VIF values) are missing from the record.

**Missing information (summary):**
- Chi-square statistic, degrees of freedom, p-value, and effect size
- Identity of the numeric features in the group comparisons and correlations, with their test statistics
- Logistic regression coefficients and odds ratios
- Accuracy, precision, recall, F1, and confusion matrix
- Random forest test AUC and train/test gap
- Class balance, tier frequencies, outlier counts, and VIF values

## Recommendations

### Immediate Actions

1. **Extract the missing statistics before making decisions.** Priority items:
   - Chi-square statistic, p-value, and Cramér's V for tier
   - Logistic regression odds ratios for tier levels and quarter
   - Repeat-visit rate by tier and by quarter
2. **Choose an operating threshold and report precision and recall.** The threshold should reflect the business cost of false positives versus false negatives.
3. **Check the 0.92 AUC for leakage.** Confirm that no outcome-derived information entered the features and that the data-generation process is as expected.
4. **Resolve the duplicate row.** Determine whether it is a true duplicate record or a valid repeated event, and document the decision.
5. **Confirm `quarter`'s data type and encoding** and use one encoding consistently across all analyses.
6. **Identify the numeric feature behind the significant correlation** and reconcile its exclusion with the statistical result.

Once items 1 and 2 are complete, the tier and quarter model can support decisions about where to focus retention efforts and when. Until then, the findings should inform hypotheses rather than resource allocation.

### Future Analysis

**Questions to investigate:**
1. **Effect sizes:** How much does repeat probability change across tiers and quarters, after adjusting for each other?
2. **Incremental value of numeric features:** Do `age`, `distance_km`, or `staff_on_shift` improve the model when added to tier and quarter? A nested model comparison would answer this.
3. **Interaction:** Does the tier effect vary by quarter? An interaction term or partial-dependence analysis would test this.
4. **Model stability:** Repeated cross-validation or bootstrap confidence intervals for AUC.
5. **Model comparison:** Does a tuned random forest outperform logistic regression on held-out data?
6. **Mechanism for quarter:** Is the quarter effect driven by seasonality, staffing cycles, or campaign timing? Answering this requires either additional variables or a designed experiment.

**Data to collect:**
- **Outcome timing:** The date or sequence of visits, so that repeat behavior can be measured over a defined window rather than as a single flag. This would also clarify what "repeat" means.
- **Campaign and promotion records:** To test whether quarter effects reflect marketing activity.
- **Staffing details:** Beyond `staff_on_shift`, such as staff tenure or turnover, if staffing is suspected to drive repeat behavior.
- **Customer identifiers:** To account for customers who appear in the data more than once and to avoid inflating model performance through repeated records.
- **Intervention data:** If the business plans to act on repeat-visit predictions, record which customers received which intervention. This is the only way to measure causal impact.