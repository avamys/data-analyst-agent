# Data Analysis Report: Students

## Executive Summary

- **Pre-score is the clearest signal in the data.** Pre-score has a moderate, statistically significant negative association with score gain (Pearson r = −0.462, p = 5.2×10⁻⁵⁴, R² = 0.213). Students who start higher tend to gain less, which is consistent with a ceiling effect or regression to the mean.
- **The available features predict score gain only weakly.** The best model, linear regression, explains about 18% of test-set variance (R² = 0.184) and reduces RMSE by roughly 10% relative to a mean-only baseline (9.58 vs. 10.62). Most of the variation in score gain is not explained by these six features.
- **Linear regression should be the default model.** The random forest performed worse on held-out data (R² = 0.042) and showed a large train–test gap, indicating overfitting. The linear form was not rejected on linearity or curvature tests, so added flexibility does not appear to be needed.
- **We cannot yet say which levers matter most.** Permutation-importance rankings were computed but not reported by name, and the statistical tests for extra sessions and attendance are not clearly attributed. Intervention decisions based on these behavioral variables are not yet supported.
- **Several inputs need verification before this report is used for decisions.** The random forest's train–test gap is reported as both 0.125 and 0.851, and the EDA and statistical outputs are truncated. Section 7 lists these issues.

## 1. Dataset Overview

| Attribute | Value |
|---|---|
| Source | `/workspaces/agents/evals/data/students.csv` |
| Rows × columns | 1,000 × 6 |
| Target variable | `score_gain` (continuous, regression) |
| Features | 6 numeric (`pre_score`, `extra_sessions`, `attendance_pct`, `age`, `class_size`); 0 categorical |
| Missing values | None reported for the columns shown; see Limitations |

The target has a mean of −0.003 and a standard deviation of 11.48. A mean this close to zero is unusual for a score-gain variable and may reflect how the target was constructed (for example, centered or differenced). This should be confirmed before the scale is interpreted.

## 2. Analysis Methodology

### 2.1 Strategic Approach

Three strategies were applied in priority order:

1. **Exploratory analysis** came first to check data quality, distributions, and candidate relationships. With 1,000 complete rows and no categorical or temporal features, the focus was on distributions, outliers, and feature–target correlations.
2. **Statistical testing** came second to determine which relationships are significant and whether linear-model assumptions hold, so that only validated relationships carried into modeling.
3. **Predictive modeling** came last. A continuous target with 1,000 rows supports a train/test split and cross-validation, so regression models and feature importance could be compared against the statistical findings.

### 2.2 Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory (EDA) | 2 |
| Statistical | 1 |
| Machine Learning | 3 |
| **Total** | **6 of 6 (100%)** |

No tasks failed. Total execution time was 67.9 seconds. Completion status does not guarantee that every output was fully reported, and several outputs were truncated (see Section 7).

## 3. Key Findings

### 3.1 Exploratory Analysis

**Data quality.** The dataset is complete for the columns displayed in the quality check, which reported zero missing values for `pre_score` and `extra_sessions`. No rows were dropped during analysis preparation (1,000 of 1,000 retained).

**Feature types.** Four features are float64 (`pre_score`, `attendance_pct`, `score_gain`) and three are integers (`extra_sessions`, `age`, `class_size`). No encoding was needed.

**Candidate relationships.**
- **Pre-score vs. score gain:** Strong enough to be the primary driver in the statistical tests (r = −0.462, R² = 0.213; see Section 3.2).
- **Feature independence:** The correlation analysis reported "acceptable independence among features," suggesting that multicollinearity is not a major concern for coefficient interpretation. The specific correlation values and variance inflation factors were not reported.

**Distributions and outliers.** The EDA output was truncated after dtypes. Skewness, outlier counts, and distribution shape for the target and features are **not available** in the supplied material, so these findings cannot be reported with numbers.

**Sample illustration.** The first rows show the negative pre-score pattern: a student with a pre-score of 70.2 has a score gain of −4.9, while a student with 33.2 has a gain of 14.1. Five rows are not enough to support a conclusion and are shown only for illustration.

### 3.2 Statistical Evidence

**Test 1: Pearson correlation, pre_score vs. score_gain**
- **Purpose:** Test H₀: ρ = 0 (no linear correlation)
- **Result:** r = −0.4619, p = 5.2 × 10⁻⁵⁴
- **95% CI for r (Fisher z):** [−0.509, −0.412]
- **Effect size:** R² = 0.213 (about 21% of variance shared)
- **Decision:** Reject H₀ at any conventional significance level
- **Interpretation:** Pre-score has a moderate, reliable negative linear association with score gain. Higher starting scores are associated with smaller gains. The confidence interval excludes zero by a wide margin, so the direction is clear. The magnitude is moderate, not large.

**Test 2: Spearman rank correlation.** Initiated, but its result was truncated in the output and is not reported here.

**Test 3: Slope test, pre_score → score_gain**
- **Purpose:** Test H₀: slope = 0
- **Decision:** Reject H₀
- **Limitation:** The test statistic and p-value are not reported in the supplied material.

**Tests 4–5: Model-form checks**
- **Linearity (H₀: linear form adequate):** Not rejected. No evidence of nonlinearity was found in the simple linear fit.
- **Curvature (H₀: no curvature):** Not rejected. This is consistent with the linearity result.

**Slopes for extra_sessions and attendance_pct.** The statistical log lists several "REJECT" outcomes without clearly attributing each to a predictor. Significance for `extra_sessions` and `attendance_pct` should be treated as **unconfirmed** until the per-predictor results are checked.

**Not tested.** `age` and `class_size` were not tested for statistical significance.

**Not verified.** Residual normality and heteroscedasticity were not reported. Because of this, p-values and confidence intervals for regression coefficients should be treated with caution.

### 3.3 Predictive Models

**Models tested:** Linear regression and random forest regression, compared against a mean-predictor baseline on a held-out test set.

| Model | Test R² | Test RMSE | RMSE / Target SD | Train–Test R² Gap |
|---|---|---|---|---|
| Linear regression | 0.184 | 9.576 | 0.901 | Not reported |
| Random forest | 0.042 | 10.376 | 0.976 | 0.851 or 0.125 (conflicting) |
| Mean baseline | 0.000 | 10.621 | 1.000 | N/A |

**Metric notes:**
- This is a regression task, so classification metrics (accuracy, precision, recall) do not apply.
- MAE was said to be computed, but its value is not included in the supplied material.
- Cross-validation was set up, but scores were not reported.

**Performance interpretation:**
- Linear regression reduces RMSE by about 9.8% relative to the baseline (9.576 vs. 10.621). This is a real improvement, but a modest one.
- The random forest barely improves on the baseline (RMSE 10.376) and shows a large train–test gap, which indicates that it memorizes noise in the training data.
- Hyperparameter tuning was recommended (larger `min_samples_leaf`, lower `max_depth`), but the tuned values and their effect on test performance are not reported.

**Feature importance.** Permutation importance was computed, but the feature names and scores are **not included** in the supplied material. We therefore cannot say which inputs drive predicted score gains. This is the most important gap for actionability.

**Predictive insight.** About 82% of the variance in score gain (1 − R² = 0.816) is unexplained by these features. Any individual prediction carries substantial uncertainty.

## 4. Synthesis

**Validated across analyses:**

1. **Pre-score is linked to score gain, and the link is negative.** The correlation test, the slope test, and the linear model all point the same way. A plausible explanation is that students with lower starting scores have more room to improve. This is a hypothesis to test rather than a settled conclusion, because the direction and magnitude of the slope were not reported in detail.

2. **The relationships are approximately linear.** The linearity and curvature tests were not rejected, and the linear model outperforms the flexible random forest on held-out data. Together these suggest additive, linear structure without strong nonlinearities that a flexible model could exploit. Interactions were not tested.

3. **The signal is weak overall.** Both models explain little variance (R² = 0.184 and 0.042), and the linear model's RMSE is 90% of the target's standard deviation. The residual error is large relative to the outcome's spread.

4. **Overfitting in the random forest is consistent with a noisy target.** A flexible model that learns training-set noise will generalize poorly when the signal is this weak.

**Not validated:** Residual normality, per-predictor effect sizes for behavioral variables, feature importance rankings, and the significance of `age` and `class_size`.

## 5. Conclusions

**What we can say with confidence:**
- Pre-score has a moderate, statistically significant negative association with score gain (r = −0.46, R² = 0.21).
- Linear regression is the better of the two tested models for this dataset and outperforms the mean baseline by about 10% on RMSE.
- The features explain only a small share of variation in score gain. Predictions should be treated as rough estimates.
- The relationships do not show evidence of nonlinearity, so a simple linear model is an appropriate starting point.

**What we cannot yet say:**
- Which features most drive score gains. Feature importances are unreported.
- Whether extra sessions or attendance have a meaningful association with score gains. Their significance is unconfirmed.
- Whether any effect is causal. These variables are behavioral and may reflect motivation or prior ability.
- Whether the pre-score effect is a genuine learning effect or a regression-to-the-mean artifact.

## 6. Limitations & Caveats

### 6.1 Data Quality Issues
- **Truncated outputs.** The EDA output shows only dtypes and two of six missing-value rows. The statistical output does not show the Spearman result. Some conclusions depend on summaries that cannot be checked against the underlying numbers.
- **Target scale.** The target mean is −0.003 with SD 11.48. The construction of `score_gain` (centered, differenced, or otherwise transformed) must be confirmed before effect sizes are interpreted.
- **Unverified missing-value claim.** The synthesis states that no features had missing values, but the quality check shown covers only two columns.

### 6.2 Statistical Assumptions and Limitations
- **Residual normality** was not reported. This affects the validity of p-values and confidence intervals on coefficients.
- **Heteroscedasticity** was not checked. Score-gain variance may differ across pre-score levels.
- **Independence of observations** is assumed but not discussed. If students are clustered within classes (`class_size` is a feature), standard errors may be understated.
- **Causal inference** is not supported. All associations are observational.

### 6.3 Conflicting Findings
- **Random forest train–test gap:** Reported as 0.851 in one summary and 0.125 in another. A gap of 0.851 implies a training R² near 0.89, which would be a severe overfit. The 0.125 figure may come from a different model, split, or tuned version. This must be reconciled before reporting.
- **Test R² attribution:** One summary attributes R² = 0.184 generally, while another attributes it specifically to linear regression. The linear regression attribution is used here.
- **Feature-importance claims:** One summary says the analysis identifies "which inputs most drive predicted score gains," but no features are named.

### 6.4 Failed or Missing Analyses
- No tasks failed.
- Missing: test statistics and p-values for each predictor, standardized coefficients, named feature-importance rankings, residual diagnostics, results for `age` and `class_size`, cross-validation scores, MAE values, and tuned random forest hyperparameters.

## 7. Recommendations

### 7.1 Immediate Actions

1. **Adopt linear regression as the working model** for score-gain prediction, and treat its predictions as approximate. Use the mean baseline as the reference point for any reported improvement.
2. **Use pre-score as the primary stratification variable** when reviewing score gains. Consider reporting results by pre-score band, since the negative association is the strongest signal in the data.
3. **Do not make intervention decisions based on extra sessions or attendance yet.** Their statistical significance is unconfirmed, and the association may not be causal.
4. **Reconcile the random forest train–test gap** (0.851 vs. 0.125) and confirm which model produced each figure before any results are shared.
5. **Confirm how `score_gain` was constructed** so that effect sizes can be interpreted on the correct scale.
6. **Stop further random forest tuning** unless regularization is applied and documented. Its current performance does not justify additional complexity.

### 7.2 Future Analysis

**Questions to investigate:**
1. **Which features drive score gains?** Report permutation-importance rankings by feature name, along with standardized coefficients from the linear model.
2. **Is the pre-score effect a regression-to-the-mean artifact?** Model post-score directly, or control for pre-score, to separate genuine gains from mechanical ones.
3. **Do extra sessions and attendance have causal effects?** A quasi-experimental design or propensity-score analysis would be needed.
4. **Do age and class size matter?** Test both for significance, and model class-level clustering with a mixed-effects model if students are nested within classes.
5. **Are there interactions?** Test terms such as attendance × extra sessions.
6. **Is there unexplained structure in the target?** With R² near 0.18, additional variables may be needed.

**Diagnostics to complete:**
- Residual normality (for example, Q–Q plots and Shapiro–Wilk tests)
- Heteroscedasticity (Breusch–Pagan test)
- Influential points (Cook's distance)
- Cross-validation results for both models

**Data to collect:**
- **Prior course history and prior test scores**, to better separate learning from baseline ability
- **Teacher or instructor identifiers**, to account for teacher effects
- **Socioeconomic and home-environment indicators**, which may explain part of the unexplained variance
- **Intervention records with dates and dosage**, to support causal analysis of extra sessions
- **Post-score and the exact definition of score gain**, to clarify the target's construction and scale