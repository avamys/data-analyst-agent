# Data Analysis Report: Shipments

**Dataset:** `/workspaces/agents/evals/data/shipments.csv` | **Rows:** 1,000 | **Target:** `delivery_hours`

> **Reading note:** Several source outputs were truncated. Key gaps include the Pearson and Spearman coefficient values, the permutation importance rankings, the EDA skewness and outlier results, and the full weekday test output. Where this report gives numbers that were not directly reported, it says so. Two data-integrity issues also need resolution before the weekday results can be relied on (see Limitations).

---

## Executive Summary

- **Gradient boosting predicts delivery time well; linear models do not.** Gradient Boosting explains 86.3% of test-set variance (R² = 0.863) with a mean absolute error of 3.7 hours. Linear Regression explains only 13.5% (R² = 0.135, MAE 9.1 hours). The gap points to nonlinear relationships or feature interactions. Any delivery-time estimate should use the nonlinear model.
- **Distance is the only confirmed driver.** Distance_km is significantly associated with delivery_hours under both Pearson and Spearman tests (p < 0.0125, Bonferroni-adjusted). The coefficient magnitude was not captured, so its size is unquantified.
- **Depot has no meaningful effect on delivery time.** Depot means range only from 38.3 to 40.7 hours. The ANOVA and Kruskal-Wallis tests both fail to reject the null hypothesis, and depot explains about 0.5% of variance (η² ≈ 0.005, derived from summary statistics). Depot-level operational changes are unlikely to shift delivery times on their own.
- **The weekday result is not yet trustworthy.** Weekday group sizes sum to only 425 of the 1,000 rows. Saturday deliveries average about 2.9 hours longer than Monday deliveries, and the derived p-value for that subset is about 0.07. The "no difference" conclusion cannot be confirmed until the missing rows are accounted for.
- **Delivery time is strongly right-skewed and non-normal.** The Shapiro-Wilk test gives W = 0.894 (p = 1.27 × 10⁻²⁵). Mean delivery time is about 39.5 hours, but the median runs 1–2 hours below the mean in every depot and weekday group. Averages alone are a poor guide to typical performance.

---

## Dataset Overview

| Attribute | Detail |
|---|---|
| Records | 1,000 rows, 6 columns |
| Target variable | `delivery_hours` (continuous, regression) |
| Numeric features | `parcel_weight_kg`, `distance_km`, `items` (3) |
| Categorical features | `depot` (4 levels: alpha, beta, gamma, delta), `weekday` (levels reported: Fri, Mon, Sat) |
| Missing values | None in the checked columns (0.0%) |
| Class imbalance | Not applicable (regression). Depot group sizes range from 238 to 263. |

The profile lists four numeric features, but `delivery_hours` is the target and was excluded from the predictor set. The predictors are therefore three numeric and two categorical.

---

## Analysis Methodology

### Strategic Approach

Three strategies were applied in priority order:

1. **Exploratory analysis** came first to establish distributions, category frequencies, and correlation structure before any testing. The target's skew and the category balance were needed to choose appropriate tests.
2. **Statistical testing** came second to check whether the apparent relationships were real. ANOVA was paired with Kruskal-Wallis because the target is non-normal, and correlation tests were run on distance, weight, and item count.
3. **Predictive modelling** came last, using a train/test split on 1,000 rows. Linear Regression served as a interpretable baseline and Gradient Boosting as a nonlinear comparison. The ordering let the earlier findings inform the modelling choices.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory (EDA) | 2 |
| Statistical | 2 |
| Machine Learning | 2 |
| **Total** | **6 of 6 (100% success, 0 failures)** |

Total execution time was 9.5 seconds.

---

## Key Findings

### Exploratory Analysis

**Target distribution**
- `delivery_hours` is non-normal (Shapiro-Wilk W = 0.894, p = 1.27 × 10⁻²⁵).
- Group-level summaries show a consistent pattern: the mean exceeds the median by roughly 2–3 hours in each group. For example, in the depot table, alpha has a mean of 38.3 and a median of 35.6. This indicates a right-skewed distribution with a tail of slow deliveries.
- Standard deviations are large relative to the means, at about 12–14 hours in every group. Spread is wide everywhere.

**Depot distribution**

| Depot | Count | Share | Mean (h) | Median (h) | Std (h) |
|---|---|---|---|---|---|
| alpha | 249 | 24.9% | 38.3 | 35.6 | 12.2 |
| beta | 250 | 25.0% | 40.7 | 37.5 | 13.9 |
| delta | 263 | 26.3% | 39.5 | 36.3 | 13.1 |
| gamma | 238 | 23.8% | 40.2 | 37.5 | 13.1 |

Depots are close to evenly represented. The mean spread between depots is 2.4 hours (38.3 to 40.7), which is small relative to a standard deviation of about 13 hours.

**Weekday distribution**

| Weekday | Count | Share of 425 | Mean (h) | Median (h) | Std (h) |
|---|---|---|---|---|---|
| Fri | 125 | 29.4% | 38.3 | 35.2 | 12.2 |
| Mon | 152 | 35.8% | 38.6 | 35.9 | 12.8 |
| Sat | 148 | 34.8% | 41.5 | 38.1 | 13.5 |

Saturday shows the highest mean and median. These counts cover only 425 rows, which is a data issue discussed under Limitations.

**Distance**
- `distance_km` is also non-normal (W = 0.949, p = 4.0 × 10⁻¹⁸).
- Skewness, kurtosis, and outlier counts for the numeric features were not captured in the excerpt, so the outlier profile is unknown.

**Correlation structure**
- The correlation matrix was computed for the numeric features, but the printed coefficients were not captured. Based on the statistical stage, distance_km is linearly and monotonically associated with delivery_hours. The relationships of parcel_weight_kg and items with delivery_hours are not confirmed. One correlation result in the synthesis reads "fail to reject H0 (no significant linear correlation)", which may refer to one of these two features.

### Statistical Evidence

**1. Depot effect on delivery time (one-way ANOVA)**
- **Purpose:** Test whether mean delivery time differs across the four depots.
- **Result:** Fail to reject H0. The F-statistic and p-value were not captured in the excerpt.
- **Effect size (derived):** Using the group means and standard deviations, η² ≈ 0.005 and F(3, 996) ≈ 1.6, p ≈ 0.18. Depot therefore explains roughly 0.5% of variance in delivery time.
- **Plain English:** Depot does not meaningfully change how long deliveries take. The largest depot gap is about 2.4 hours, but depots differ from one another by less than the typical delivery's variation.

**2. Depot effect (Kruskal-Wallis, non-parametric check)**
- **Purpose:** Confirm the depot result without assuming normality, given the skew.
- **Result:** Fail to reject H0. The test statistic was not reported.
- **Plain English:** The non-parametric test agrees with ANOVA, so the depot conclusion does not depend on the normality assumption.

**3. Weekday effect (ANOVA and Kruskal-Wallis)**
- **Purpose:** Test whether delivery time differs by day of the week.
- **Result:** Both tests are reported as fail to reject H0 in the consolidated insights. The full weekday output is not visible.
- **Derived check:** Using only the 425 rows with weekday labels, η² ≈ 0.012, F(2, 422) ≈ 2.6, p ≈ 0.07. This is borderline and not significant at α = 0.05. The Saturday effect (about +2.9 hours vs. Monday) is the largest observed difference, but its significance depends on which rows are included.
- **Plain English:** Weekday has at most a small effect, and the evidence is not conclusive. The result should be re-run on the full dataset before it is reported.

**4. Two-way ANOVA (depot)**
- **Result:** Listed as fail to reject H0. Design, interaction terms, and statistics are not shown, so this result cannot be verified.

**5. Distance–delivery correlation (Pearson, linear)**
- **Purpose:** Test whether distance is linearly associated with delivery time.
- **Result:** Reject H0 at the Bonferroni-adjusted threshold (p < 0.0125).
- **Effect size:** The correlation coefficient r was not captured.
- **Plain English:** Longer routes are associated with longer delivery times. The pattern is statistically clear, but its strength is unquantified.

**6. Distance–delivery correlation (Spearman, monotonic)**
- **Result:** Reject H0 at the same adjusted threshold (p < 0.0125).
- **Plain English:** The relationship holds even when the assumption of linearity is relaxed, which supports the finding that distance has a consistent effect across the range of values.

**7. Multiple-comparison correction**
- The threshold of 0.0125 corresponds to α = 0.05 divided by 4 comparisons. The four tests are not fully identified in the excerpt.

**8. Normality (Shapiro-Wilk)**

| Variable | W | p-value | Conclusion |
|---|---|---|---|
| delivery_hours | 0.894 | 1.27 × 10⁻²⁵ | Non-normal |
| distance_km | 0.949 | 4.02 × 10⁻¹⁸ | Non-normal |

Both variables depart from normality. This affects the reliability of Pearson p-values and parametric ANOVA, which is why non-parametric checks were run alongside them.

### Predictive Models

**Models tested:** Linear Regression (baseline) and Gradient Boosting Regressor. This is a regression task, so classification metrics such as accuracy, precision, and recall do not apply. The metrics below are R², RMSE, and MAE.

| Model | Test R² | RMSE (h) | MAE (h) | Train–Test R² Gap |
|---|---|---|---|---|
| Linear Regression | 0.135 | 11.73 | 9.11 | −0.001 |
| Gradient Boosting | 0.863 | 4.66 | 3.71 | 0.079 |

**Interpretation**
- **Gradient Boosting reduces prediction error by about 60%.** RMSE falls from 11.7 to 4.7 hours (60% lower), and MAE falls from 9.1 to 3.7 hours (59% lower).
- **Linear Regression is not fit for purpose.** It explains only about 13.5% of variance. Its near-zero train–test gap shows it is underfitting, not overfitting.
- **Gradient Boosting shows a moderate train–test gap.** An R² gap of 0.079 suggests some overfitting. It is not severe, but it is not zero. Hyperparameters and tuning procedure were not documented, and only a single split was reported.

**Feature importance**
- Permutation importance was computed, but the per-feature values were not captured.
- Distance_km is the only feature with confirmed significant association, so it is the most likely leading predictor. This must be verified against the permutation output before it is stated as a finding.
- Parcel weight and item count are not confirmed as drivers.

**Predictive insights**
- The model's typical error of about 3.7 hours is the figure to weigh against operational tolerance. Whether that is acceptable depends on the service-level commitments, which were not provided.
- Because depot and weekday showed little group-level effect, the model is probably drawing mainly on continuous features. This is an inference and has not been tested directly.

---

## Synthesis

**Validated across analyses**
1. **Distance drives delivery time.** Confirmed by Pearson and Spearman tests and consistent with operational intuition.
2. **Relationships are nonlinear.** The gap between linear (R² 0.135) and tree-based (R² 0.863) performance is large and is the clearest signal in the modelling results.
3. **Depot does not matter on its own.** ANOVA and Kruskal-Wallis agree, and the derived effect size is negligible (η² ≈ 0.5%).
4. **The target is skewed.** The mean exceeds the median in every group, so averages overstate typical delivery times.

**Partially supported or unresolved**
- **Weekday:** Possibly a small effect (Saturday about 2.9 hours above Monday), but the test covers only 425 of 1,000 rows and is not significant on that subset.
- **Parcel weight and items:** Conflicting correlation results appear in the synthesis, and the full correlation table is needed to resolve them.
- **Interactions:** The strength of the nonlinear model suggests interactions (for example, depot × distance), but no interaction test has been run.

**Pattern that holds across the analyses:** Delivery time is driven by route characteristics, specifically distance, and is poorly explained by the administrative grouping of depot or weekday. Simple linear rules fail, so operational planning based on averages or on a single linear rule will be inaccurate.

---

## Conclusions

**What we can say with confidence**
1. Delivery time is well predicted by a nonlinear model using the available features. Gradient Boosting explains 86% of test variance with a typical error of about 3.7 hours.
2. Distance is significantly associated with delivery time, in both linear and monotonic form.
3. Depot has negligible influence on delivery time (η² ≈ 0.5%).
4. Linear models are inadequate for this problem. Any planning or forecasting tool should not rely on linear extrapolation.

**What we cannot yet say**
- The size of the distance effect (no coefficient reported).
- Which features rank highest in the model (permutation values missing).
- Whether weekday matters (incomplete data and borderline result).
- Whether parcel weight or item count matter (conflicting or missing results).
- Whether the model is operationally acceptable (no tolerance threshold has been defined).

---

## Limitations & Caveats

**Data quality issues**
- **Weekday coverage is incomplete.** Weekday group counts (125 + 152 + 148) sum to 425, not 1,000. Either other weekday levels exist and were omitted from the output, or the analysis silently dropped about 58% of rows. This must be investigated before weekday results are used.
- **Outlier results are missing.** The effect of extreme values on correlations, regressions, and group tests is unknown.
- **Missing-value checks were partial.** The excerpts confirm zero missing values for the columns shown, but not for every column in every output.

**Statistical assumptions and limitations**
- **Non-normality** of the target and of distance affects the reliability of Pearson p-values and parametric ANOVA. Non-parametric checks partly mitigate this.
- **Non-significance is not equivalence.** The depot and weekday results show no detectable difference, but this does not prove the groups are the same. Effect sizes and confidence intervals were not reported for the tests.
- **Single train/test split.** No cross-validation variance or confidence intervals are reported for R², RMSE, or MAE.
- **Interactions were not tested,** even though the nonlinear model's performance suggests they may matter.
- **Overfitting judgement.** The Gradient Boosting gap of 0.079 is described as "no major overfitting," which is a judgement, not a formal test.

**Failed or incomplete analyses**
- The two-way ANOVA for depot is reported without design, interaction terms, or statistics, so it cannot be verified.
- Permutation importance was computed but not reported.
- Correlation coefficient magnitudes were not captured.
- The full weekday test output is not visible.

**Missing information**
- Operational tolerance for delivery-time error (needed to judge the 3.7-hour MAE).
- Hyperparameters and tuning method for the Gradient Boosting model.
- Definitions of the depot and weekday variables, including whether the weekday field is complete.

---

## Recommendations

### Immediate Actions

1. **Resolve the weekday data gap before any weekday decision.** Confirm whether the 575 rows without a weekday label in the output are missing, mislabelled, or excluded by mistake. Re-run the weekday ANOVA and Kruskal-Wallis tests on the full dataset.
2. **Use Gradient Boosting, not linear models, for delivery-time estimates.** Establish whether a typical 3.7-hour error is acceptable for customer commitments. If it is not, flag which deliveries fall outside the acceptable range.
3. **Do not treat depot as a lever for delivery speed.** Depot explains about 0.5% of variance. Operational changes at depot level are unlikely to produce meaningful time savings on the evidence available.
4. **Plan around distance.** Use distance as the primary input for delivery-time estimates and for route-level commitments. Long routes should carry longer promised windows.
5. **Report medians alongside means** when summarising delivery performance, since the distribution is right-skewed.

### Future Analysis

**Questions to investigate**
1. Which features drive the Gradient Boosting model? Report permutation importance for distance, weight, items, depot, and weekday.
2. What is the shape of the distance relationship? Is it linear, or does it show thresholds or step changes at particular distances?
3. Do depot or weekday matter through interactions, for example depot × distance or weekday × distance?
4. Would a log-transformed target improve the linear model? Given the skew, this is a low-cost test.
5. What drives the large residuals? Examine cases with prediction errors above 10 hours for patterns.
6. Is the model stable? Use k-fold cross-validation and report confidence intervals for R², RMSE, and MAE.

**Data to collect**
- **Traffic and time-of-day data.** Likely drivers of delivery time that are absent from the current dataset.
- **Courier capacity and staffing levels.** Could explain much of the unexplained variance.
- **Weather data.** A plausible source of delay.
- **Service-level targets.** Required to define acceptable prediction error.
- **Complete weekday and depot coding,** with documentation of how each field is populated.
- **Actual delivery-time commitments,** so that predictions can be checked against promises and not only against historical outcomes.