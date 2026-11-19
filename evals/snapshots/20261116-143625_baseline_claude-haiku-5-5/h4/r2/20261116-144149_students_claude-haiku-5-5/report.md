# Data Analysis Report: Students

## Executive Summary

- **Prior score is the strongest and most reliable signal of score gain.** Students with higher pre-scores tend to gain less (Pearson r = −0.46, 95% CI [−0.51, −0.41], R² = 0.21, p ≈ 5×10⁻⁵⁴). It is also the top-ranked feature by permutation importance.
- **Attendance is a second, independent predictor.** It remains significant (p < 0.05) after adjusting for the other predictors in the multivariable model. The effect direction and size still need confirmation from the full coefficient table.
- **Extra sessions and age show no detectable association with score gain** after adjusting for other factors (p ≥ 0.05). Adding sessions alone is unlikely to raise gains based on this data, though a null result at n = 1,000 does not rule out a small effect.
- **Predictability is modest.** The best model, linear regression, explains about 18% of variance on held-out data (test R² = 0.184). Roughly 80% of the variation in score gain comes from factors not captured in this dataset. Predictions are useful for population-level planning but not for individual decisions.
- **A linear model performs better than gradient boosting** (test R² 0.184 vs. 0.054; boosting RMSE about 7.5% higher). The relationships appear largely linear, so added model complexity is not warranted at present.

---

## Dataset Overview

| Attribute | Value |
|---|---|
| Source | `/workspaces/agents/evals/data/students.csv` |
| Size | 1,000 rows × 6 columns |
| Target variable | `score_gain` (continuous; regression task) |
| Predictors | `pre_score`, `extra_sessions`, `attendance_pct`, `age`, `class_size` (all numeric) |
| Categorical features | None |
| Missing values | None reported in the checks that completed |

The dataset is a clean, complete, all-numeric table. Its observational design means that associations reported here are not causal estimates.

---

## Analysis Methodology

### Strategic Approach

Three strategies were applied in priority order:

1. **Exploratory analysis** came first to establish distributions, correlations, and outliers. With a small, clean, all-numeric dataset, this step is quick and reveals structure before any testing.
2. **Statistical analysis** followed to test whether each feature is associated with the target. Pearson tests with multiple-comparison correction were used for univariate relationships, and OLS regression for adjusted, multivariable associations.
3. **Predictive modeling** came last. With 1,000 rows, an 80/20 train/test split and cross-validation were feasible. A linear regression baseline was compared against gradient boosting, with permutation importance used for interpretation.

This ordering moved from understanding, to validating relationships, to testing predictive performance, with each step informed by the one before it.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory (EDA) | 2 |
| Statistical | 2 |
| Machine Learning | 2 |
| **Total** | **6 of 6 (100% success, 0 failures)** |

Total execution time was 33.6 seconds.

---

## Key Findings

### Exploratory Analysis

**Data quality**
- The dataset has 1,000 rows and 6 columns with no missing values in the checks reported.
- All columns are numeric: `pre_score` and `attendance_pct` are floating-point, while `extra_sessions`, `age`, and `class_size` are integers. `score_gain` is floating-point.

**Sample records** (first rows, for orientation):

| pre_score | extra_sessions | attendance_pct | age | class_size | score_gain |
|---|---|---|---|---|---|
| 70.2 | 0 | 94.1 | 16 | 32 | −4.9 |
| 52.7 | 0 | 92.6 | 17 | 20 | 1.0 |
| 33.2 | 1 | 82.0 | 17 | 23 | 14.1 |
| 69.1 | 0 | 83.4 | 15 | 22 | 2.7 |

The sample rows show that `score_gain` can be negative, and that the highest pre-score in the sample (70.2) corresponds to a loss, while the lowest (33.2) corresponds to the largest gain. This pattern is consistent with the statistical result below.

**Distributional and structural notes**
- The EDA flagged **strong asymmetry** in at least one variable, but the variable and skewness values were not reported.
- The EDA flagged **possible nonlinearity or outlier influence**, but no specific variable or test was named.
- The EDA flagged **serious collinearity** among predictors, but the specific pairs and VIF values were not reported. This is a gap that matters for interpreting the regression coefficients (see Limitations).

Specific summary statistics (means, standard deviations, ranges, skewness, and outlier counts) were not included in the outputs provided, so they cannot be reported here.

### Statistical Evidence

**Test 1: Pearson correlation tests, features vs. `score_gain`**

- **Purpose:** Test whether each feature has a linear association with `score_gain`.
- **Number of tests:** 5, with Bonferroni, Holm, and Benjamini-Hochberg (BH-FDR) correction.

| Feature | r | R² | 95% CI for r | Raw p | Adjusted p (BH) | Result |
|---|---|---|---|---|---|---|
| `pre_score` | −0.462 | 0.213 | [−0.509, −0.412] | 5.2 × 10⁻⁵⁴ | 2.6 × 10⁻⁵³ | **Significant; survives correction** |
| Other four features | Not reported individually | Not reported | Not reported | Not reported | Not reported | Three tests rejected H₀ and two did not, but the features are not labeled |

- **Plain-English interpretation:** Students with higher pre-scores tended to have smaller gains. A correlation of −0.46 is a moderate, clearly nonzero relationship. The pre-score alone accounts for about 21% of the variation in score gain.
- **Note on the unlabeled results:** The Pearson output reports three rejections and two non-rejections across the five features, but it does not identify which features fall into each group. The OLS results (below) agree with the Pearson result for pre-score, extra sessions, and age. Attendance's and class size's Pearson results cannot be confirmed from the outputs.

**Test 2: Multivariable OLS regression, `score_gain` on all six numeric features**

- **Purpose:** Estimate each feature's association with `score_gain` while holding the others constant.

| Result | Finding | Significance |
|---|---|---|
| Overall F-test | Rejects H₀ that all slopes are zero | p < 0.05 |
| `pre_score` | Significant | p < 0.05 |
| `attendance_pct` | Significant | p < 0.05 |
| `extra_sessions` | Not significant | p ≥ 0.05 |
| `age` | Not significant | p ≥ 0.05 |
| `class_size` | Not confirmed from outputs | Not reported |

- **Effect sizes:** Coefficients, standard errors, and confidence intervals were not included in the outputs. The direction and magnitude of the attendance effect are therefore unconfirmed.
- **Plain-English interpretation:** After accounting for the other predictors, prior score and attendance each carry information about score gain. Extra sessions and age do not.
- **Residual diagnostics** (normality, homoscedasticity) were requested but not reported.

**Hypothesis summary**

| Hypothesis | Evidence | Status |
|---|---|---|
| `pre_score` is linearly associated with `score_gain` | r = −0.46, p ≈ 5×10⁻⁵⁴; significant in OLS; survives BH-FDR | **Supported (negative direction)** |
| `attendance_pct` is associated with `score_gain` after adjustment | OLS p < 0.05 | **Supported (direction and size unconfirmed)** |
| `extra_sessions` is associated with `score_gain` | OLS p ≥ 0.05 | **Not supported** |
| `age` is associated with `score_gain` | OLS p ≥ 0.05 | **Not supported** |
| At least one predictor is associated with `score_gain` | OLS overall F-test, p < 0.05 | **Supported** |
| Nonlinear models outperform linear models | Test R²: GB 0.054 vs. LR 0.184 | **Not supported** |

### Predictive Models

**Models tested**

Both models were evaluated on an 80/20 train/test split (about 200 test rows) with cross-validation.

| Model | Test R² | Test RMSE vs. baseline | Role |
|---|---|---|---|
| Linear Regression | **0.184** | Baseline (selected on CV RMSE) | Selected model |
| Gradient Boosting | 0.054 | About 7.5% higher | Comparison |

**Metric applicability:** Because this is a regression task, classification metrics (accuracy, precision, recall, F1) do not apply. RMSE, MAE, and R² are the relevant measures. RMSE and MAE values, cross-validation means, and fold standard deviations were not included in the outputs, so only R² and the relative RMSE comparison are reported.

**Feature importance**
- **`pre_score`** ranked first by permutation importance. This result most likely came from the gradient boosting model rather than the selected linear model, so it should be treated as indicative.
- **`attendance_pct`** is the second significant predictor in OLS, but its rank in the importance results was not reported.
- **`extra_sessions`** and **`age`** contribute little.

**Predictive insights**
- The linear model explains **18.4%** of held-out variance. The in-sample Pearson R² for `pre_score` alone is 21.3%. These figures are not directly comparable (one is in-sample, the other out-of-sample), but they suggest that the other features add little predictive value beyond prior score. This should be checked directly.
- The better performance of the simpler model suggests the signal is largely linear and that added flexibility increases error on new data.
- The boosting model may have been under-tuned or overfit. Training-set R² was not reported, so the explanation cannot be confirmed.

---

## Synthesis

**Patterns that held across analyses**

1. **Prior score is the most robust driver.** It appears in the Pearson test (significant after correction), the OLS model (significant), and the importance ranking (first). Three independent lines of evidence point the same way.
2. **Attendance is a second, independent driver.** It is significant in the multivariable model, meaning it contributes beyond prior score.
3. **Extra sessions and age are not meaningful predictors.** Both are non-significant in OLS, and neither contributes to the predictive model.
4. **The relationships are predominantly linear.** The linear model beats boosting on held-out data, and no nonlinear interaction was found to add value.
5. **The overall signal is real but limited.** The OLS F-test is significant, but the explained variance is only about 18%.

**Tension to resolve**

Extra sessions and attendance are both engagement measures, yet only attendance is significant. One possible explanation is that extra sessions are assigned non-randomly, for example to lower-performing students, which would mask any true benefit. This is a hypothesis and has not been tested.

---

## Conclusions

**What we can say with reasonable confidence**

- Higher prior scores are associated with smaller score gains. The association is moderate (r ≈ −0.46) and highly statistically robust.
- Attendance is associated with score gain even after accounting for prior score and the other variables. The direction still needs confirmation from the coefficient table.
- Extra sessions and age do not show a detectable association with score gain in this dataset.
- A linear model is the appropriate baseline for this data. Gradient boosting did not improve prediction.
- Most of the variation in score gain is unexplained by these six variables.

**What we cannot yet conclude**

- The size and direction of the attendance effect.
- Whether any of these associations are causal.
- Whether the negative pre-score relationship reflects genuine learning dynamics or partly reflects how `score_gain` is calculated (see Limitations).
- Whether class size matters once class-level clustering is considered.

---

## Limitations & Caveats

**Data quality issues**
- Several source outputs were truncated, including the full OLS coefficient table. Some insights in the synthesis were generic template text. Only specific reported results are used in this report.
- Outlier counts, skewness values, and the variables affected were not reported. Influential points could bias the coefficient estimates.
- The EDA's collinearity warning is unquantified. If `pre_score` and `attendance_pct` (or `extra_sessions`) are strongly correlated, individual coefficients would be unstable.

**Statistical assumptions and limitations**
- **Mathematical coupling:** If `score_gain` is computed as post-score minus pre-score, a negative correlation with `pre_score` is partly expected by construction. This is a serious interpretive issue and should be checked against how the variable was defined.
- **Regression to the mean:** High scorers have less room to gain, and measurement noise in `pre_score` would also produce a negative association. This could be the driver of the pre-score finding rather than a real effect of prior achievement.
- **Linearity:** Supported indirectly by the model comparison but not formally tested.
- **Residual assumptions:** Normality and homoscedasticity diagnostics were requested but not reported.
- **Independence:** `class_size` is a predictor, which suggests students are nested within classes. If so, standard errors may be underestimated without clustering adjustments.
- **Observational design:** These are associations, not causal effects. Students were not randomly assigned to attendance levels or extra sessions.

**Failed analyses**
- No tasks failed (6 of 6 completed). However, several outputs were incomplete, and the results listed under "Missing information" below were not produced.

**Missing information**
- Regression coefficients, standard errors, and confidence intervals for each predictor
- Labels identifying which features were significant in the five Pearson tests (other than `pre_score`)
- Residual plots, normality tests, and heteroscedasticity tests
- VIF values for all predictors
- RMSE and MAE values, cross-validation means and standard deviations
- Training vs. test error for both models (needed to evaluate the overfitting explanation for boosting)
- Permutation importance for the linear model
- Interaction tests (e.g., `pre_score` × `attendance_pct`)

---

## Recommendations

### Immediate Actions

1. **Do not treat extra sessions as a standalone lever for raising score gains.** The data show no detectable association. Hold any expansion of sessions until a controlled test is run.
2. **Use attendance as a monitoring and intervention priority,** since it is a significant, independent predictor. Confirm its direction and magnitude from the full coefficient table before setting targets.
3. **Account for prior score when evaluating students or programs.** Comparing raw gains across students with different starting points will be misleading. Gains should be assessed relative to baseline performance.
4. **Verify how `score_gain` is defined** before interpreting the pre-score result. If it is post minus pre, reframe the finding accordingly.
5. **Use the linear regression as the working model** for planning. Limit its use to group-level projections, given that it explains only about 18% of variance.

### Future Analysis

**Immediate analytical follow-ups**
- Obtain the full OLS coefficient table with standard errors and confidence intervals.
- Run residual diagnostics and check for influential points (e.g., Cook's distance).
- Compute VIFs and the full correlation matrix among predictors to quantify collinearity.
- Compare training and test R² for both models, and report RMSE and MAE with cross-validation spread.
- Test interaction terms, especially `pre_score` × `attendance_pct`.
- Test for nonlinear effects directly (e.g., splines or a threshold in attendance).
- Try regularized linear models (ridge or lasso) and a properly tuned boosting model to confirm that linearity is not under-modeled.

**Data to collect**
- **Class or teacher identifiers,** so that clustering can be modeled and class-level effects separated from student-level effects.
- **Session assignment records and how sessions were allocated,** to determine whether extra sessions were targeted at specific students.
- **Post-score and pre-score as separate variables** (not only their difference), to avoid mathematical coupling and to model the outcome more precisely.
- **Measures of motivation, prior-year grades, instructional method, and teacher quality,** which are plausible drivers of the unexplained ~80% of variance.
- **Attendance measured over time,** to test whether consistency matters more than the average level.

**Study designs to establish causality**
- A **randomized trial** assigning extra sessions to a random subset of students, with pre-specified outcome measures, would be the most direct test of whether sessions raise gains.
- A **quasi-experimental analysis** (e.g., difference-in-differences across classes or cohorts with and without attendance interventions) could estimate the effect of attendance changes.

---

**Bottom line:** Prior score and attendance are the most credible predictors of score gain in this dataset. Prior score shows a moderate, statistically robust negative association, and attendance contributes independently after adjustment. Extra sessions and age show no detectable effect. A linear model captures most of the learnable signal, but leaves about 80% of the variance unexplained. Before acting on these findings, the team should confirm the attendance coefficient, verify how `score_gain` is defined, and run a controlled test before investing in extra sessions.