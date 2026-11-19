# Data Analysis Report: Students

## Executive Summary

- **Student baseline scores are the strongest signal for score gains, and the relationship is negative.** Prior score correlates with score gain at r = -0.46 (95% CI [-0.51, -0.41], p < 0.001, Holm-adjusted p = 2.6e-53). Students who start higher tend to gain less. This may reflect a ceiling effect or regression to the mean, but it may also be partly mechanical if score gain is calculated from the prior score.
- **The features explain only a modest share of score gains.** The best model, linear regression, reaches test R² = 0.184 and reduces RMSE by about 10% relative to predicting the mean (9.58 vs. a test SD of 10.63). About 82% of variance in score gains is unexplained by these five variables.
- **Attendance is a second candidate driver, but its effect is not yet quantified.** `attendance_pct` is significant in the OLS model after Holm correction, but the coefficient, direction, and confidence interval were not in the available output. Attendance also appears to be related to prior score, so its independent contribution is uncertain.
- **Extra sessions, class size, and age show no reliable linear effect.** Each is non-significant in the OLS model. Their small permutation-importance values (RMSE increases of 0.0161 and 0.0200, about 0.2% of test RMSE each) do not justify resource decisions based on them.
- **Linear models outperform tree ensembles.** This suggests the relationships are approximately linear and additive. A simple, interpretable model is the right starting point for stakeholder use, provided its limited accuracy is communicated clearly.

## Dataset Overview

| Attribute | Detail |
|---|---|
| Source | `/workspaces/agents/evals/data/students.csv` |
| Size | 1,000 rows × 6 columns |
| Target variable | `score_gain` (continuous, regression) |
| Predictors | `pre_score`, `extra_sessions`, `attendance_pct`, `age`, `class_size` (5 numeric predictors) |
| Data types | 4 float64 (`pre_score`, `attendance_pct`, `score_gain`) and 2 int64 (`extra_sessions`, `age`, `class_size`); see note below |
| Missing values | 0 across all columns |
| Duplicate rows | 0 (0.00%) |
| Non-numeric entries | 0 |

**Note on column types:** The data has six columns: five predictors and the target. The original request referred to "six features," so this report treats `score_gain` as the target and the other five columns as predictors. Data types for `age` and `class_size` are integer; the EDA output listed `extra_sessions` and `age` as int64, and `class_size` as int64.

## Analysis Methodology

### Strategic Approach

Three strategies were applied in priority order:

1. **Exploratory analysis** came first to check data quality, distributions, outliers, and correlations before any modelling. The dataset is clean (no missing values or duplicates), so the EDA focused on distributions, pairwise relationships, and multicollinearity.
2. **Statistical analysis** came second to test whether each feature's association with `score_gain` is statistically meaningful. Because the target is continuous and there are no groups, the tests were correlation tests (Pearson and Spearman) and an OLS regression, not t-tests or ANOVA.
3. **Predictive modelling** came last to measure how much of `score_gain` the features can predict out of sample, and which features matter most. This stage used a linear baseline and tree ensembles on a train/test split.

Predictive work was informed by the earlier stages, so the modelling tested the relationships the statistics had already flagged.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory data analysis | 2 |
| Statistical analysis | 2 |
| Machine learning | 2 |
| **Total** | **6 of 6 (100% success, 0 failures)** |

Total execution time was 97.3 seconds. The task outputs were partly truncated, so some planned results are missing from this report (see Limitations).

## Key Findings

### Exploratory Analysis

**Data quality is high.** The dataset has no missing values, no duplicate rows, and no non-numeric entries in any column. This removes the need for imputation or cleaning before analysis.

**Correlation structure:**
- `pre_score` has the strongest linear association with `score_gain` (r = -0.46, r² = 0.213). This means prior score alone accounts for about 21% of the variance in score gains.
- The EDA flagged a dependence between `attendance_pct` and `pre_score`. This is the main multicollinearity concern, and it makes separating their individual effects harder.
- Pearson and Spearman tests both rejected the null hypothesis of no association for at least one feature, but the EDA and statistical outputs do not give a complete feature-by-feature table of correlation coefficients.

**Distributions and outliers:** The EDA was requested to report skewness, summary statistics, and IQR and z-score outlier counts for each variable. These results were not included in the available output, so this report cannot state distributional shape or the number of outliers. The EDA did flag outliers and non-linearity as present, but without magnitudes or affected row counts.

### Statistical Evidence

**Test 1: Pearson correlation, `pre_score` vs. `score_gain`**

| Metric | Value |
|---|---|
| Sample size | n = 1,000 |
| Correlation (r) | -0.4619 |
| P-value (raw) | 5.2 × 10⁻⁵⁴ |
| P-value (Holm-adjusted, 5 comparisons) | 2.6 × 10⁻⁵³ |
| 95% CI (Fisher z) | [-0.509, -0.412] |
| Effect size (r²) | 0.213 (21.3% of shared variance) |
| Significance | Significant at α = 0.05 (very strong) |

*Plain English:* Students with higher prior scores tend to show smaller score gains. The effect is medium in size and very unlikely to be a chance result. The confidence interval excludes zero by a wide margin.

**Test 2: OLS regression, all five predictors**

| Predictor | Holm-adjusted significance | Result |
|---|---|---|
| `pre_score` | p < 0.05 | Significant. Strongest and most consistent finding. |
| `attendance_pct` | p < 0.05 | Significant. Coefficient, direction, and CI not reported. |
| `extra_sessions` | p ≥ 0.05 | Not significant. No reliable linear effect detected. |
| `age` | p ≥ 0.05 | Not significant. |
| `class_size` | p ≥ 0.05 | Not significant. |

*Plain English:* Two of five predictors show a statistically reliable linear association with score gains after correcting for multiple comparisons. The other three do not. A non-significant result here means the data do not show an effect, not that the effect is zero. Small or non-linear effects can go undetected at this sample size.

**Residual diagnostics:** Assumption checks (normality, homoscedasticity, linearity) and influence diagnostics (Cook's distance, leverage) were requested but not reported. The OLS p-values should be treated as provisional until these checks are available.

**Effect sizes for the OLS coefficients were not reported.** Only the r² for `pre_score` is available.

### Predictive Models

**Models tested:** Linear regression (baseline), random forest, and gradient boosting, evaluated on a held-out test set.

**Performance (test set):**

| Model | R² | RMSE | Result |
|---|---|---|---|
| Linear regression | 0.184 | 9.58 | Best performer |
| Random forest | Not reported | Not reported | Underperformed linear regression |
| Gradient boosting | Not reported | Not reported | Underperformed linear regression |

*Interpretation:* The model explains roughly 18% of score-gain variance. Its RMSE of 9.58 compares with a test-set target SD of 10.63. That is about a 10% reduction in prediction error relative to predicting the average gain for every student. This is a real but modest improvement, and it is not enough for individual-level decisions.

*Metrics note:* This is a regression task, so accuracy, precision, and recall do not apply. The relevant metrics are R² and RMSE, which are reported above.

**Feature importance (permutation, test set):**

| Feature | Reported importance | Consistency with OLS |
|---|---|---|
| `pre_score` | Ranked most influential | Significant in OLS. Consistent across methods. |
| `attendance_pct` | Not reported | Significant in OLS. Permutation result missing. |
| `class_size` | RMSE increase of 0.0200 (about 0.2% of test RMSE) | Not significant in OLS. Conflicting. |
| `extra_sessions` | RMSE increase of 0.0161 (about 0.2% of test RMSE) | Not significant in OLS. Conflicting. |
| `age` | Not reported | Not significant in OLS. |

The importance rankings contain conflicts (see Limitations). The one result that holds across methods is `pre_score`. Its permutation ranking is consistent with its OLS significance.

**Predictive insights:**
- Features explain about one-fifth of score-gain variation. Most of what drives gains is outside this dataset.
- The linear model's advantage over tree models suggests there is little non-linear structure for trees to exploit at this sample size. More complex models are not a route to better accuracy here.
- Train-test R² gaps (a check for overfitting) were not reported.

## Synthesis

**Validated across analyses:**
- **Prior score is associated with smaller score gains.** This is supported by the Pearson test (r = -0.46, p < 0.001), the OLS coefficient (significant after Holm correction), and its top permutation-importance ranking. It is the most robust finding in this report.
- **Attendance is associated with score gains.** It is supported by the OLS result alone, so the evidence is weaker and less cross-validated than for prior score.
- **Extra sessions, class size, and age show no reliable linear effect.** Their OLS results are non-significant. The permutation results for `extra_sessions` and `class_size` are tiny and conflict with the OLS findings, so they do not overturn the null result.

**Consistent patterns:**
- The relationships appear linear and additive, based on linear regression outperforming tree ensembles.
- The features as a set have limited predictive power (R² = 0.18).

**Relationship between attendance and prior score:** The EDA found these two variables are dependent. Attendance may affect gains partly through prior score, or both may reflect a shared factor such as engagement or baseline ability. Separating their effects requires a model that includes both and tests their interaction, or a formal mediation analysis.

## Conclusions

**What we can say with confidence:**
1. Prior score is the strongest measured predictor of score gains, and the relationship is negative. Students who start higher gain less on average.
2. Attendance is significantly associated with score gains after multiple-comparison correction, but its magnitude and direction are not yet established.
3. Extra sessions, class size, and age show no reliable linear association with score gains in this dataset.
4. The five available features explain about 18% of score-gain variance. Accurate prediction of individual gains will require other information.
5. Linear models are sufficient for this data. More complex models did not improve performance.

**What we cannot yet conclude:**
- The size and direction of the attendance effect.
- Whether extra sessions, class size, or age matter in non-linear or interaction forms.
- Which features drive the unexplained 82% of variance.
- Whether the results hold without outliers, or whether residual assumptions are met.

## Limitations & Caveats

**Data quality:** The dataset is clean (no missing values, duplicates, or non-numeric entries). However, outlier counts and magnitudes were flagged but not reported, so their influence on OLS estimates is unknown.

**Statistical limitations:**
- **Mechanical correlation risk.** If `score_gain` is calculated as post-score minus `pre_score`, the negative correlation with `pre_score` is partly built into the data. This must be checked before interpreting the result as a causal or behavioral pattern.
- **Multicollinearity.** Variance inflation factors were not reported. The `attendance_pct`–`pre_score` dependence means their individual coefficients may be unstable.
- **Residual diagnostics missing.** Normality, homoscedasticity, linearity, and influential-point checks were requested but not reported.
- **Effect sizes and confidence intervals missing** for OLS coefficients and for most correlations. Only the `pre_score` Pearson CI is available.
- **Correlation reporting is incomplete.** Pearson and Spearman results were given as generic "reject H0" lines without feature-level mapping, except for `pre_score`.

**Conflicting results:**
- **`class_size` and `extra_sessions`** are non-significant in OLS but appear in the permutation rankings. The reported percentage shares (for example, about 55% of permutation signal for `class_size`) appear to have been computed over only a subset of features, which makes them unreliable as rankings. Their RMSE increases are negligible (0.0200 and 0.0161 against a test RMSE of 9.58).
- **Conflicting "most influential" claims:** One result names `pre_score` as most influential, and another assigns the largest share to `class_size`. Both cannot be correct under the same metric. This is most likely a reporting error.
- **Minor R² inconsistency:** RMSE/SD implies R² ≈ 0.188, versus the reported 0.184. This is small and may come from rounding or degrees-of-freedom conventions, but it should be checked.

**Predictive limitations:**
- Random forest and gradient boosting test metrics were not reported.
- Hyperparameters, scaling, cross-validation folds, and random seeds were not documented, so the model comparison cannot be reproduced exactly.
- Train-test gaps were not reported, so overfitting in the tree models cannot be assessed.

**Scope note:** The EDA and statistical outputs were partly truncated. Some planned analyses (distributional statistics, full correlation matrix, OLS coefficients) are missing from the available results.

**Failed analyses:** None failed outright. Six of six tasks completed, but several outputs were incomplete.

## Recommendations

### Immediate Actions

1. **Use prior score as the primary segmentation variable, with caution.** Students with lower starting scores have larger average gains in this data. Before acting on this, confirm how `score_gain` is defined. If it is post minus pre, reframe the finding in those terms and do not treat it as evidence that low-scoring students respond better to intervention.
2. **Do not reallocate resources based on extra sessions, class size, or age.** The data show no reliable linear effect for these. Any decision should wait for non-linear or interaction analysis.
3. **Treat attendance as a promising lead, not an established lever.** Before investing in attendance programs, obtain the coefficient, its confidence interval, and the direction of the effect, and check whether the effect holds after controlling for prior score.
4. **Use the linear model only for directional planning, not for individual predictions.** With R² = 0.18, it can indicate broad tendencies across groups but cannot reliably forecast any single student's gain.
5. **Correct and re-issue the feature-importance summary.** Remove the conflicting percentage shares and report one consistent ranking with its denominator stated.

### Future Analysis

**Analyses to complete (priority order):**
1. Full OLS output: coefficients, standard errors, confidence intervals, and VIFs.
2. Residual diagnostics and influence statistics (Cook's distance, leverage), with a robust regression sensitivity check for outliers.
3. Confirm how `score_gain` is calculated, and test the `pre_score` relationship accordingly.
4. Partial effect or mediation analysis for `attendance_pct` and `pre_score`.
5. Interaction terms, for example `extra_sessions × pre_score`, to test whether extra sessions help low-scoring students more.
6. Spline or binned analysis for `class_size` and `age` to check for non-linear effects.
7. Ridge or lasso regression to test whether regularization stabilizes coefficients under collinearity.
8. Report tree-model test metrics, train-test gaps, and full hyperparameter and CV settings.
9. Bootstrap confidence intervals for R² and feature importance.

**Data to collect:**
- **Class or teacher identifiers**, to allow multilevel modelling. This would separate class-level from student-level variation, which matters given the unexplained `class_size` signal.
- **Socioeconomic and home-environment indicators**, which may explain part of the unexplained 82% of variance.
- **Motivation or engagement measures**, to help clarify whether attendance works directly or as a proxy for engagement.
- **Session content and timing for extra sessions**, to test whether the intervention has any effect at all before concluding it is ineffective.
- **Pre- and post-assessment dates and measurement details**, to check the score-gain calculation and any ceiling effects.