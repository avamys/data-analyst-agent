# Data Analysis Report: Shipments

*Dataset: `/workspaces/agents/evals/data/shipments.csv`. Analysis scope: exploratory, statistical, and predictive. Several specialist outputs were truncated, so some results below are reported without their full statistics. Values marked **(derived)** were calculated from reported figures, not taken directly from the output.*

---

## Executive Summary

- **Parcel weight and distance drive delivery time.** Both are significantly associated with `delivery_hours`. Distance alone shows a moderate positive correlation (r ≈ 0.31, derived, p < 0.001). Weight carries 82.8% of the Random Forest's feature importance, though that figure should be validated (see Limitations).
- **A nonlinear model predicts delivery time well.** A Random Forest explains **86.3%** of variance on held-out data (R²), with an RMSE of **4.67 hours** and an MAE of **3.64 hours**. This is about 9% of the mean delivery time (39.66 h). A linear model explains only 13.5%, so the relationship is clearly not linear.
- **Depot and weekday do not meaningfully explain delivery time.** Depot group means fall within a 2.4-hour range (38.3 to 40.7 h). The depot test was not significant, and its effect size is negligible (η² ≈ 0.005, derived). The weekday test also failed to reject the null, though its statistics were not reported.
- **Model performance is stable, with moderate overfitting.** Cross-validated R² varies by only ±0.026 across folds, so the result does not depend on a lucky split. The gap between training and test error suggests moderate overfitting, not severe.

**Decision relevance:** The model can support delivery-time estimates and capacity planning based primarily on parcel weight and distance. Depot and weekday assignments should not be treated as the main levers for reducing delivery time, based on current evidence.

---

## Dataset Overview

| Attribute | Value |
|---|---|
| Records | 1,000 |
| Columns | 6 |
| Target | `delivery_hours` (continuous; regression) |
| Numeric columns | `parcel_weight_kg`, `distance_km`, `items`, `delivery_hours` (4, including the target) |
| Categorical columns | `depot` (4 levels: alpha, beta, delta, gamma), `weekday` (7 levels: Mon–Sun) |
| Predictors | 5 (3 numeric, 2 categorical), after excluding the target |
| Missing values | None reported for the columns checked; "usable rows: 1000" |

**Target summary:** `delivery_hours` has a mean of 39.66 h, SD of 13.10 h, and median of 36.65 h. The mean exceeds the median by about 3 hours, which suggests a right-skewed distribution with a tail of slow deliveries. Skewness and outlier counts were not reported.

---

## Analysis Methodology

### Strategic Approach

The analysis followed a deliberate sequence:

1. **Exploratory analysis** to understand distributions, missingness, correlations, and category sizes before any modeling.
2. **Statistical testing** to confirm which relationships are real: group tests (ANOVA or Kruskal-Wallis) for depot and weekday, and correlation tests for the numeric features.
3. **Predictive modeling** to quantify how well the variables predict delivery time and which drive predictions. A linear baseline and a Random Forest were compared.

Because `delivery_hours` is both listed as the target and as a numeric column, it was excluded from the predictors to avoid target leakage.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory (EDA) | 2 |
| Statistical | 2 |
| Machine Learning | 2 |
| **Total** | **6 of 6 (100% success)** |

Total execution time was 48.9 seconds.

---

## Key Findings

### Exploratory Analysis

- **Data quality is clean.** No missing values were found in the columns checked (`parcel_weight_kg`, `distance_km`). The dataset has 1,000 usable rows.
- **Depot groups are balanced.** Group sizes are alpha 249, beta 250, delta 263, and gamma 238. Each is roughly 24–26% of the data, so no depot dominates or is underrepresented.
- **Group-level delivery times are similar.** Mean delivery time by depot:

| Depot | n | Mean (h) | Median (h) | SD (h) | 95% CI for mean (h) |
|---|---|---|---|---|---|
| alpha | 249 | 38.28 | 35.60 | 12.25 | 36.75–39.81 |
| beta | 250 | 40.71 | 37.45 | 13.93 | 38.98–42.45 |
| delta | 263 | 39.46 | 36.30 | 13.06 | 37.87–41.05 |
| gamma | 238 | 40.21 | 37.50 | 13.07 | 38.54–41.88 |

- **Spread is consistent across depots.** Standard deviations range from 12.2 to 13.9 h. Medians are consistently about 2–3 h below the means, which is consistent with the right skew in the overall target.
- **Target distribution:** Mean 39.66 h, median 36.65 h, SD 13.10 h. The long right tail is the main source of extreme delivery times.
- **Weekday counts:** Seven levels (Mon through Sun). Per-day counts were not reported.
- **Distributions of weight, distance, and items:** Summary statistics and outlier counts for these variables were not captured in the truncated output.

### Statistical Evidence

| Hypothesis | Test | Result | Effect Size | Interpretation |
|---|---|---|---|---|
| `distance_km` is linearly associated with `delivery_hours` | Pearson correlation | **Significant** (t = 10.46, df = 998, p < 0.001) | r ≈ 0.31 **(derived)**; r² ≈ 0.10 | Longer distances are associated with longer delivery times. Distance explains about 10% of the variance on its own. |
| `parcel_weight_kg` is linearly associated with `delivery_hours` | Pearson correlation | **Significant** (p < 0.05; exact p and r not reported) | Not reported | Heavier parcels are associated with longer delivery times. Strength is unquantified. |
| `distance_km` and `parcel_weight_kg` each contribute beyond the other | Partial/adjusted test (method not stated) | **Both significant** (p < 0.05) | Not reported | Each variable carries information the other does not. Method should be confirmed. |
| `items` is linearly associated with `delivery_hours` | Pearson correlation | **Not significant** (p ≥ 0.05) | Not reported | No meaningful linear link. Items may still matter through interactions (untested). |
| Delivery time differs across depots | One-way ANOVA or Kruskal-Wallis | **Fail to reject H₀** | η² ≈ 0.005 **(derived)** | Depot explains roughly 0.5% of delivery-time variance. Depot is not a meaningful driver. |
| Delivery time differs across weekdays | One-way ANOVA or Kruskal-Wallis | **Fail to reject H₀** | Not reported | No evidence of a weekday effect. Test statistics were not captured. |

**How the depot result was derived:** Using the reported group means and sizes, the between-group sum of squares is about 833 and the total is about 171,400. This gives η² ≈ 0.005 and an approximate F(3, 996) ≈ 1.6, with p ≈ 0.18. These are approximations, but they are consistent with the reported non-significance.

**Plain-English interpretation:**
- Parcel weight and distance are real signals. Their effects are measurable, but the linear correlation with distance is only moderate.
- Depot and weekday do not explain delivery time. The depot result is strong evidence of a negligible effect, not just a failure to detect one.
- Items shows no linear relationship, which is a notable result given its apparent operational relevance.

**Multiple testing:** Roughly 10 or more tests were run, and no correction for multiple comparisons is reported. The marginal results are most at risk of false positives. The strong results (distance, depot) are unlikely to be affected.

### Predictive Models

**Models tested:**
1. Linear regression (baseline)
2. Random Forest regressor

**Performance on held-out test data:**

| Model | R² | RMSE (h) | MAE (h) |
|---|---|---|---|
| Linear regression | 0.135 | 11.74 | Not reported |
| Random Forest | **0.863** | **4.67** | **3.64** |

*Classification metrics (accuracy, precision, recall) do not apply to this continuous regression target.*

**Interpreting the errors:**
- The Random Forest's MAE of 3.64 h is about **9%** of the mean delivery time (39.66 h). Its RMSE of 4.67 h is about **12%** of the mean.
- The linear model's RMSE of 11.74 h is roughly 2.5 times larger, indicating that the linear model misses most of the structure.
- A typical prediction is within about 3.6 hours of the actual delivery time. Large errors are possible in the long right tail, which RMSE penalizes most heavily.

**Model stability:**
- Cross-validated R² has a standard deviation of 0.026 across folds, indicating consistent performance.
- The train–test R² gap for the Random Forest is about 0.10 (training R² ≈ 0.96, derived).
- The train–test RMSE difference of 2.17 h suggests training RMSE is about 2.5 h against 4.67 h on test (derived). This indicates **moderate overfitting**. It does not invalidate the model, but it means test performance is somewhat optimistic relative to training fit.

**Feature importance:**
- `parcel_weight_kg`: **82.8%** of total Random Forest importance.
- `distance_km`, `items`, `depot`, `weekday`: individual importance values were not captured. The remaining 17.2% is distributed among them.

**Predictive insights:**
- The gap between linear (R² 0.14) and forest (R² 0.86) performance indicates **nonlinear or interaction effects** drive most of the predictable variation. Weight and/or distance likely affect delivery time through thresholds, curves, or combinations, not simple proportional increases.
- Because depot and weekday add little, the model's predictive power comes from parcel characteristics.
- About 14% of variance remains unexplained. Factors not in this dataset (route conditions, carrier, traffic, time of dispatch) may account for part of it.

---

## Synthesis

Combining the three analyses produces a consistent picture:

**Validated across analyses:**
- **Parcel weight and distance are the primary drivers of delivery time.** Both are significant in bivariate tests, both retain significance after adjustment, and weight dominates the model's importance ranking.
- **Depot and weekday do not explain delivery time.** The depot effect is negligible (η² ≈ 0.005), and the weekday test showed no effect.
- **Items has no detectable linear relationship** with delivery time, though it may interact with weight.
- **The relationship is nonlinear.** The gap between linear and forest performance is large and reproducible.

**Where the evidence is thinner:**
- The forest's weight importance (82.8%) may reflect a known bias of impurity-based importance, which favors continuous features. Permutation importance is needed to confirm it.
- Distance is significant in univariate tests, but its model importance is unknown. It may be correlated with weight or work mainly through interactions.
- The assignment of "not significant" to items is inferred from unlabeled output and should be verified.

---

## Conclusions

**What we can say with confidence:**
1. Parcel weight and distance are associated with delivery time. Longer distances show a moderate positive correlation (r ≈ 0.31).
2. Delivery time is predictable from these operational variables. The Random Forest explains about 86% of variance on held-out data, with a typical error of about 3.6 hours.
3. Depot and weekday assignments do not meaningfully change expected delivery time, based on the available data.
4. The relationship between inputs and delivery time is nonlinear, so simple linear rules of thumb will understate or misstate delivery times, particularly for heavy or distant parcels.

**What we cannot yet say:**
- The exact functional form of the weight and distance effects.
- Whether weight and distance interact.
- The true relative importance of each feature, independent of the impurity-based measure.
- Whether the model's error is uniform across depots, weekdays, or parcel sizes.
- The cause of the long right tail in delivery times.

---

## Limitations & Caveats

**Data quality and reporting**
- Several specialist outputs were truncated. Pearson r for weight, group-test statistics for weekday, and skewness and outlier counts are missing.
- Insight statements in the source are partly unlabeled or duplicated (for example, repeated "FAIL TO REJECT" lines), so some results could not be mapped to specific tests with full confidence.
- The column description lists four numeric features, but one is the target. The actual predictor set is three numeric and two categorical.

**Statistical assumptions**
- Pearson correlation assumes linearity and approximately normal residuals. The mean–median gap suggests right skew, which can distort Pearson results. Spearman correlation would be a safer check.
- It is not stated whether ANOVA or Kruskal-Wallis was used. Kruskal-Wallis is more appropriate under skew.
- No multiple-comparison correction was reported.

**Modeling limitations**
- The train/test split ratio, hyperparameters, and random seed are not reported, which limits reproducibility.
- Impurity-based importance may overstate the weight feature.
- The Random Forest shows moderate overfitting. Test performance may be modestly optimistic.
- No residual analysis was reported, so it is unknown whether errors grow with delivery time.

**Failed or missing analyses**
- No analyses failed outright, but the following were not performed or not reported: interaction tests (weight × distance, weight × items), permutation importance or SHAP, partial dependence plots, residual diagnostics, and a two-way model testing depot and weekday controlling for parcel mix.

---

## Recommendations

### Immediate Actions

1. **Use the model for delivery-time estimates, with error bands.** Present predictions as roughly ±4–5 hours (based on RMSE) rather than point estimates, and communicate the wider uncertainty for long or heavy shipments.
2. **Prioritize parcel weight and distance in operational planning.** Flag heavy and long-distance shipments for proactive scheduling or customer communication.
3. **Do not rely on depot or weekday reassignment to reduce delivery time** without further evidence. The current data does not support it as a lever.
4. **Validate the model on a more recent or independent sample** before relying on it for decisions. This addresses the overfitting risk and confirms stability over time.

### Future Analysis

**Priority analyses:**
1. **Permutation importance and SHAP values** on the test set, to confirm whether weight truly dominates and to rank distance and items.
2. **Interaction tests** (weight × distance, weight × items) to determine whether combined effects drive the nonlinearity.
3. **Partial dependence plots or a GAM** to reveal the functional form of the weight and distance effects.
4. **Target transformation** (for example, log of delivery hours) and comparison of linear model performance. This tests whether the linear baseline's weakness is due to skew.
5. **Residual analysis** by depot, weekday, and delivery-time quantile, to check for heteroscedasticity and differential accuracy.
6. **Complete statistical reporting:** test statistics, exact p-values, Spearman correlations, and multiple-comparison correction.
7. **Long-tail investigation:** identify which parcel profiles produce the slowest deliveries.

**Data to collect:**
- Route or zone identifiers, and road or traffic conditions
- Carrier or vehicle type, and service level (for example, express versus standard)
- Dispatch time and time of day, and actual versus scheduled delivery windows
- Delay reasons or exception codes
- Parcel dimensions (not just weight), which may explain part of the nonlinear weight effect
- Customer location details (urban versus rural), which may explain the long tail

Collecting these variables could explain some of the remaining 14% of unexplained variance and clarify why a small number of shipments take much longer than expected.