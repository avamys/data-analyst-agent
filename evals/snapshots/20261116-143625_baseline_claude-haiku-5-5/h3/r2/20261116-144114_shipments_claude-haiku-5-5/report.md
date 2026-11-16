# Data Analysis Report: Shipments

## Data Reliability Note

Several outputs needed for a complete statistical story are missing or inconsistent. This report separates **verified results** (numbers present in the outputs or directly computable from them) from **reported but unverified results** (conclusions stated in the synthesis without supporting numbers). Stakeholders should treat the unverified items as hypotheses to confirm, not established findings.

Specific gaps:
- No p-values, test statistics, or effect sizes appear for any test.
- The ANOVA and Kruskal-Wallis outputs for depot and weekday are empty in the raw logs. Their "fail to reject" conclusions come only from the synthesis.
- Feature importance values were not reported.
- The EDA correlation matrix and categorical frequency tables were truncated.
- Cross-validation and train-versus-test results were not reported.

---

## Executive Summary

- **Delivery time is predictable from the available features, but only with a non-linear model.** Gradient Boosting reached a test R² of 0.864 (RMSE 4.65 h, MAE 3.70 h). A linear baseline reached R² = 0.135 (RMSE 11.74 h). This is a single hold-out result, so the true out-of-sample performance may differ.
- **The model's typical error is about 3.7 hours.** That is roughly 9% of the mean delivery time (39.66 h). The average error is useful for setting expectations, but it does not describe the worst cases, which matter most for customer commitments.
- **No strong linear driver is visible in the marginal analysis, and the reporting does not say which feature is responsible.** The correlation results cannot be mapped cleanly to distance, weight, or item count.
- **Depot and weekday are reported as having no group differences, but this is not yet verified.** The raw test outputs are missing, so these results should not drive decisions until confirmed.
- **Delivery time is right-skewed (skew 1.20, mean 39.66 h vs. median 36.65 h).** Long-delivery cases (up to 90.6 h) deserve separate attention, and a log-transformed target may improve linear modeling.

**Decision supported:** A non-linear model can be used as a basis for delivery-time estimates, with a stated average error of about ±3.7 h. Before it is used for customer commitments, cross-validation, residual analysis of the long tail, and confirmation of the categorical findings should be completed.

---

## Dataset Overview

| Attribute | Value |
|---|---|
| Source | `/workspaces/agents/evals/data/shipments.csv` |
| Size | 1,000 rows × 6 columns |
| Target | `delivery_hours` (continuous, regression) |
| Numeric predictors | `parcel_weight_kg`, `distance_km`, `items` (3 used in the statistical tests, 4 numeric columns including the target) |
| Categorical predictors | `depot`, `weekday` |
| Missing values | 0 across all columns |
| Duplicate rows | 0 |

**Target summary (verified):**

| Statistic | Value |
|---|---|
| Mean | 39.66 h |
| Median | 36.65 h |
| Range | 15.70 – 90.60 h |
| Skew | 1.20 |

The data are complete and clean. The main structural feature is the right-skewed target.

---

## Analysis Methodology

### Strategic Approach

The analysis followed a three-stage sequence:

1. **Exploratory analysis** came first to check distributions, outliers, category frequencies, and numeric correlations before any modeling. With 1,000 complete rows, this stage was low-cost and necessary to confirm the target's shape.
2. **Statistical testing** came second to check whether the marginal relationships were real: correlation tests for numeric predictors, and ANOVA and Kruskal-Wallis tests for the categorical factors. The Kruskal-Wallis test was included because the target is skewed.
3. **Predictive modeling** came last. A linear baseline was compared with tree-based ensembles, with the target excluded from the predictor set. Models were evaluated on a hold-out test set, which is appropriate for a 1,000-row dataset.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory (EDA) | 2 |
| Statistical | 2 |
| Machine Learning | 2 |
| **Total** | **6 of 6 (100%)** |

Total execution time was 39.6 seconds. All tasks completed without errors, but completion does not mean every output was fully reported (see Data Reliability Note).

---

## Key Findings

### Exploratory Analysis

**Target distribution (verified)**
- `delivery_hours` has a mean of 39.66 h and a median of 36.65 h. The mean sits about 3 h above the median.
- The skew of 1.20 indicates a long upper tail. The maximum of 90.6 h is about 2.3 times the median.
- The minimum is 15.70 h, so the distribution is bounded below and stretches upward.

**Outliers (verified)**

| Feature | IQR Outliers | Share of Rows |
|---|---|---|
| `parcel_weight_kg` | 44 | 4.40% |
| `distance_km` | 0 | 0.00% |
| `items` | 0 | 0.00% |

Weight has a heavier tail than the other numeric features. Zero IQR outliers for `items` is expected for a discrete variable with a narrow range, so IQR-based detection is not very informative there.

**Categorical features and correlation matrix**
- The frequency tables for `depot` and `weekday` were truncated in the output, so category counts and balance cannot be reported.
- The numeric correlation matrix was also truncated. The only pairwise value available is distance vs. weight, r = −0.0167 (see Statistical Evidence).

### Statistical Evidence

**Note:** No p-values, test statistics, or effect sizes were reported for any test. The significance statements below are as reported in the synthesis and have not been independently verified.

**Test 1: Pearson correlation tests (Holm-adjusted)**

- **Purpose:** Test whether each numeric predictor has a linear association with `delivery_hours` (H0: ρ = 0).
- **Reported outcome:** Mixed. The synthesis reports two pairs as significant and three as not significant after Holm correction. The mapping to specific predictors is unresolved.
- **Verified coefficient:** distance_km vs. parcel_weight_kg, r = −0.0167. This is a predictor-predictor pair, not a test against `delivery_hours`, so it does not answer H1 directly.
- **My check:** For n = 1,000, the critical |r| at α = 0.05 is about 0.062. An r of −0.017 is far below that, so distance and weight are essentially uncorrelated (approximate two-sided p ≈ 0.60, computed from the t-statistic). This is consistent with the reported "fail to reject."
- **Plain English:** Distance and weight do not move together. The results for the delivery-time correlations cannot be interpreted until the output is corrected.

**Test 2: ANOVA of delivery_hours by depot and by weekday**

- **Purpose:** Test whether mean delivery time differs across depot and weekday levels.
- **Reported outcome:** Fail to reject H0 for both factors (group means equal).
- **Verification status:** The raw output is empty. Test statistics and p-values are unavailable.
- **Plain English:** The synthesis reports no average difference in delivery time by depot or weekday. This is unverified.

**Test 3: Kruskal-Wallis test of delivery_hours by depot and by weekday**

- **Purpose:** Test whether the full delivery-time distribution differs across levels. This is preferred over ANOVA here because of the skew.
- **Reported outcome:** Fail to reject H0 for both factors (identical distributions).
- **Verification status:** Unverified, same as above.
- **Plain English:** If confirmed, neither depot nor weekday shifts delivery times on its own. The synthesis also suggests these factors could matter through interactions with distance or weight, which was not tested.

**Test 4: Model comparison on the hold-out set (H6)**

- **Purpose:** Test whether non-linear models predict delivery time better than a linear baseline.
- **Result:** Supported. Gradient Boosting R² = 0.864 vs. linear R² = 0.135.
- **Effect size (computed):** RMSE fell from 11.74 h to 4.65 h, a 60.4% reduction. The model's RMSE is 11.7% of the mean delivery time, vs. 29.6% for the linear baseline.
- **Plain English:** The non-linear model explains about 86% of test-set variance, versus about 14% for the linear model. This is the strongest validated result, though it rests on one hold-out split.

**Hypothesis summary**

| Hypothesis | Test | Status | Evidence Quality |
|---|---|---|---|
| H1: Numeric predictors have linear correlation with delivery_hours | Pearson, Holm-adjusted | Mixed; unresolved | Low: no p-values, mapping unclear |
| H2–H3: delivery_hours differs by depot | ANOVA / Kruskal-Wallis | Fail to reject (reported) | Low: raw output missing |
| H4–H5: delivery_hours differs by weekday | ANOVA / Kruskal-Wallis | Fail to reject (reported) | Low: raw output missing |
| H6: Non-linear models outperform linear | Hold-out comparison | Supported | Moderate: single split, no CV |

### Predictive Models

**Setup:** Target `delivery_hours`. Predictors `parcel_weight_kg`, `distance_km`, `items`, `depot`, and `weekday`. The target was excluded from the predictor set.

**Models tested:** A linear baseline and tree-based ensembles, with Gradient Boosting as the best performer.

**Performance (hold-out test set)**

| Model | R² | RMSE (h) | MAE (h) |
|---|---|---|---|
| Linear baseline | 0.135 | 11.74 | Not reported |
| Gradient Boosting | 0.864 | 4.65 | 3.70 |

Minor reporting discrepancies exist (RMSE 4.65 vs. 4.66, MAE 3.70 vs. 3.71, R² 0.863 vs. 0.864). The differences are immaterial.

**Metric notes:** Accuracy, precision, and recall do not apply to a continuous target. The relevant metrics are R², RMSE, and MAE.

**Interpretive context (computed)**
- MAE of 3.7 h is about 9.3% of the mean delivery time.
- The hold-out test SD is 12.65 h. The model reduces unexplained spread from about 12.65 h to about 4.7 h.

**Feature importance:** Permutation importance was described as the method, but no values were reported. **The ranking of parcel_weight_kg, distance_km, items, depot, and weekday cannot be stated from these outputs.** The null categorical tests suggest depot and weekday have little marginal effect, but this is inference, not measurement.

**Predictive insights**
- The gap between linear and tree-based performance indicates that delivery time depends on something a linear specification misses. Candidates include interactions, thresholds, or the skewed target shape. These have not been tested.
- The model is useful for estimating typical delivery times. Its average error is acceptable for planning but may be too coarse for tight service-level commitments.

---

## Synthesis

**Consistent patterns**
- **Weak marginal signal, strong joint signal.** Individual features show little linear association with delivery time, yet the combined non-linear model explains most of the variance. Delivery time appears to depend on how the numeric features combine, not on any one of them alone.
- **Skew matters.** The right-skewed target (skew 1.20) fits poorly with a linear model on the raw scale, which may partly explain the low linear R². A log-scale model is a plausible next step.
- **Categorical factors look inactive on their own.** Depot and weekday show no reported marginal differences. Whether they matter conditionally is untested.

**Validated hypotheses**
- H6 (non-linear models outperform linear) is the only result with supporting numbers. It is supported by hold-out performance, but a single split with no cross-validation limits the confidence.

**Not validated**
- H1 through H5 cannot be confirmed from the outputs. The correlation attributions are unresolved, and the categorical test results are unverified.

---

## Conclusions

**What we can say with confidence**
1. Delivery time is not well explained by a linear model of these features (R² = 0.135 on the hold-out set).
2. A Gradient Boosting model explains about 86% of hold-out variance (R² = 0.864) with an average error of about 3.7 h (MAE).
3. The target is right-skewed, with a long tail up to 90.6 h.
4. The data are complete, with no missing values or duplicates.
5. About 4.4% of parcels (44 rows) are weight outliers.

**What we cannot yet say**
1. Which features drive delivery time, and in what order.
2. Whether depot or weekday matter, either alone or through interactions.
3. Whether the model performs consistently across the dataset, particularly for long deliveries and heavy parcels.
4. How stable the 0.864 R² is across different train/test splits.

---

## Limitations & Caveats

**Data quality**
- The dataset is complete and clean, but only 1,000 rows. Performance estimates for a five-feature ensemble may vary meaningfully with the split.
- The EDA categorical and correlation outputs were truncated.
- IQR-based outlier detection is not informative for `items`, which is discrete with a narrow range.

**Statistical assumptions**
- Pearson correlation assumes linearity and approximately normal variables. With a skew of 1.20, Spearman correlation would be more appropriate.
- ANOVA assumes normal residuals and equal variances. The Kruskal-Wallis result is more trustworthy under skew, but it was not verified.
- It is not stated whether Holm correction was applied across the full family of tests (correlations and group tests) or only the correlations.

**Failed or incomplete analyses**
- No failed tasks, but several outputs are incomplete: correlation attribution, categorical test statistics, and feature importances.

**Missing information**
- p-values, test statistics, and effect sizes for all tests
- Feature importance values
- Cross-validation scores and variance
- Train-versus-test performance (overfitting check)
- Linear baseline MAE
- Residual diagnostics for any model
- Hyperparameters
- Interaction tests

**Reporting inconsistencies**
- The synthesis labels the RMSE change as "+60.4%." It is a 60.4% **reduction**.
- Some synthesis claims go beyond the evidence. For example, "interactions or threshold effects" is a hypothesis, and "a log-additive process" is speculation. Neither has been tested.

---

## Recommendations

### Immediate Actions

1. **Use the non-linear model for planning estimates, not commitments.** A typical error of about 3.7 h supports internal planning and capacity forecasting. Do not set customer-facing delivery promises from it until the long tail is checked.
2. **Re-run the statistical tests and capture full outputs.** Report p-values, test statistics, and effect sizes (r or Spearman ρ for correlations, η² or ε² for group tests). Correct the correlation attributions and the RMSE label.
3. **Validate the model before deployment.** Run k-fold cross-validation, report the spread of R², RMSE, and MAE, and compare train and test performance to check for overfitting.
4. **Check the long tail.** Examine residuals for deliveries above roughly 60 h and for heavy parcels (the 44 weight outliers). If errors concentrate there, the model should not be used to quote times for those cases.

### Future Analysis

**Questions to investigate**
1. **Feature importance:** Report permutation importance for all five predictors with confidence intervals.
2. **Source of non-linearity:** Test interactions (distance × weight, distance × depot) and whether a log-transformed target improves the linear model.
3. **Conditional effects of depot and weekday:** Test these factors inside the model rather than in isolation.
4. **Heavy parcels:** Compare delivery-time distributions for the 44 weight outliers against the rest.
5. **Segment errors:** Break down residuals by depot, weekday, distance band, and weight band.
6. **Stability:** Bootstrap or repeat the train/test split to produce confidence intervals on R², RMSE, and MAE.
7. **Rank-based correlation:** Run Spearman correlations to check whether the weak linear picture holds under skew.
8. **Business impact:** Estimate the share of deliveries whose actual time falls outside a ±3.7 h window, and the operational cost of those misses.

**Data to collect**
- **Timestamps** for dispatch, pickup, and delivery, to decompose delivery time into stages.
- **Route or zone identifiers**, to capture geographic effects beyond distance.
- **Carrier, vehicle, or service-level type**, which may explain much of the unexplained variance.
- **Traffic and weather conditions** on the delivery date.
- **Delivery-attempt data** (failed attempts, reschedules), which likely drive the long upper tail.
- **Larger sample sizes or multiple periods**, to test model stability over time.