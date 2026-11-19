# Data Analysis Report: Properties

## Executive Summary

- **Property size is the most reliable price driver.** Size_sqm shows a moderate linear correlation with price (Pearson r = 0.498, 95% CI [0.435, 0.556], p < 0.001) and a strong monotonic association (Spearman ρ = 0.887, p < 0.001). It is also the top-ranked feature in the permutation importance analysis.
- **The three available features explain only a small share of price variation.** The best held-out R² is about 0.19, so roughly 81% of price variance is unexplained. Typical prediction errors (RMSE ≈ 273K) are close to the average price (289K). The model is useful for directional guidance, not for valuing individual properties.
- **Price is heavily right-skewed, and a log transform is warranted.** Skewness falls from about 6.4 to 0.35 after a log transform. Model performance differences between approaches are small, however, so the transform is a modeling convenience rather than a source of major accuracy gains.
- **Age and rating effects remain unresolved.** The statistical outputs for age contradict each other, and rating results are not reported with usable statistics. No decision should rely on either variable until these are rerun.
- **The analysis pipeline has internal inconsistencies that must be fixed before the results are used for decisions.** Reported test R² values differ across runs (0.159 vs. 0.189), the maximum price is described two different ways, and the correlation results point to a nonlinear relationship while the models suggest linearity.

**Decisions supported now:** Use size as the primary input for rough price tiers or comparisons. Do not use the current model for individual price estimates. Prioritize data collection on location, condition, and other missing drivers before investing in more complex models.

## Dataset Overview

| Attribute | Value |
|---|---|
| Source | `/workspaces/agents/evals/data/properties.csv` |
| Rows × columns | 600 × 4 |
| Target variable | `price` (continuous, regression) |
| Features | `size_sqm` (float), `age_years` (float), `rating` (integer score) |
| Feature types | 3 numeric features; no categorical features |
| Missing values | None (0% in all columns) |
| Duplicates | None reported |

## Analysis Methodology

### Strategic Approach

The analysis followed three strategies in this order:

1. **Exploratory analysis** came first to characterize distributions, outliers, and pairwise relationships. Price is right-skewed with extreme high values, which determined how later tests and models were specified.
2. **Statistical analysis** came second to formally test whether size and age correlate with price and whether price differs across rating levels. Rating was treated as ordinal because it is an integer score.
3. **Predictive modeling** came last. With 600 rows, a train/test split and cross-validation are feasible, and the models quantify how much of price the features can explain.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory data analysis (EDA) | 2 |
| Statistical | 1 |
| Machine learning | 3 |
| **Total** | **6 of 6 (100% success, 0 failed)** |

Total execution time was 93.2 seconds.

## Key Findings

### Exploratory Analysis

**Price distribution**
- Price is strongly right-skewed. Skewness is 6.44 on the raw scale and 0.35 after a log transform. (The statistical stage reported 6.42; this small discrepancy should be reconciled.)
- The average price is about 289K. The maximum is described inconsistently: as about 1.6M (roughly 5.5× the mean) in the EDA brief, and as 14.3× the mean (about 4.1M) in the EDA output. These cannot both be correct, so the maximum must be verified against the raw file.

**Size and price**
- Size shows the strongest association with price of the three features.
- The gap between the Pearson (0.498) and Spearman (0.887) coefficients is large. This indicates that the relationship is strongly monotonic but not well captured by a straight line on the raw scale, and/or that a small number of high-price observations are influencing the Pearson estimate.

**Age and rating**
- No distributional summaries, outlier counts, or correlation coefficients for `age_years` or `rating` appear in the outputs provided.

**Multicollinearity**
- A correlation matrix among features was requested, but feature-to-feature coefficients are not reported, so multicollinearity cannot be assessed.

### Statistical Evidence

| Test | Purpose | Statistic | p-value | Effect size | Result |
|---|---|---|---|---|---|
| Pearson correlation: size vs. price | Test linear association | r = 0.498 | 7.4 × 10⁻³⁹ | r = 0.498, 95% CI [0.435, 0.556] | Significant (reject H₀) |
| Spearman correlation: size vs. price | Test monotonic association, robust to skew | ρ = 0.887 | 5.8 × 10⁻²⁰³ | ρ = 0.887 (CI not reported) | Significant (reject H₀) |
| Age vs. price correlation | Test linear association | Not clearly reported | Not clearly reported | Not reported | **Unresolved** (conflicting entries) |
| Rating vs. price (Kruskal-Wallis / Spearman) | Test group differences across ordinal ratings | Not reported | Not clearly reported | Not reported | **Unresolved** |

**Plain-English interpretation**

- **Size and price are clearly related.** Larger apartments tend to be more expensive. A Pearson r of 0.498 corresponds to an R² of about 0.25, meaning size alone accounts for roughly a quarter of the linear variation in price. The Spearman result is stronger, indicating that larger size reliably goes with higher price rank, even though the relationship is not a straight line on the raw scale.
- **Age's effect is unknown.** The output contains both "FAIL TO REJECT H₀ (p ≥ 0.05)" and "REJECT H₀ (age has no linear effect on price)." These are contradictory, and the output does not state which test each label belongs to. No coefficient, direction, or confidence interval is available.
- **Rating's effect is unknown.** Entries labeled "REJECT H₀ (p < 0.05)" appear in the output, but they are not attached to a named test, statistic, or group means, so they cannot be interpreted.

### Predictive Models

**Setup:** Target was log-transformed for modeling and reported on the original price scale. Features were size_sqm, age_years, and rating. Evaluation used an 80/20 train/test split plus cross-validation.

**Models tested and held-out performance**

| Model | Test R² | Test RMSE | Assessment |
|---|---|---|---|
| Dummy baseline (predict mean) | ≈ 0.00 | ≈ 289K | Reference |
| Linear regression | 0.189 | 273,535 | Interpretable baseline |
| Huber regression | 0.191 | 273,198 | Equivalent to linear regression (difference of 0.002 R², about 340 in RMSE) |
| Random forest | 0.120 | 284,930 | Weakest; likely overfitting |

Note: Regression models do not use accuracy, precision, or recall. The appropriate metrics are R², RMSE, and MAE. MAE was not reported.

**Stability**
- Cross-validated R² is 0.31 ± 0.20 across folds, which is well above the held-out test R² of 0.19. The fold-to-fold spread is large, so any single performance number is imprecise.
- The reported train–test R² gap is 0.34. The model whose train score this refers to is not identified.

**Feature importance**
- `size_sqm` is the most influential feature by permutation importance.
- Permutation importance values for `age_years` and `rating` are not reported, so their relative contributions cannot be ranked.

**Predictive insights**
- The features carry a modest, approximately linear signal. Adding model flexibility (random forest) did not help.
- The model can indicate that larger apartments generally cost more. It cannot reliably predict the price of a specific property, since typical errors are on the order of 270K.
- A simple size-only model was not run. Given that size alone explains about 25% of linear variance in price, it may perform about as well as the three-feature model. This should be tested.

## Synthesis

**Consistent patterns across analyses**
- **Size is the dominant, stable predictor.** It appears in the correlation analysis, the rank-based test, and the permutation importance results.
- **Price skew shapes everything.** The log transform normalizes the target, and the large residuals and outliers in the models are consistent with the skew.
- **The features explain only a limited share of price.** Held-out R² of about 0.19 is consistent across the linear and Huber models.

**Validated hypotheses**

| Hypothesis | Evidence | Status |
|---|---|---|
| Size is linearly associated with price | Pearson r = 0.498, CI [0.435, 0.556], p < 0.001 | **Supported** |
| Size and price are monotonically associated | Spearman ρ = 0.887, p < 0.001 | **Supported** |
| Price is right-skewed and a log transform helps | Skewness 6.44 → 0.35 | **Supported** (descriptive, no formal test) |
| Age has no linear effect on price | Conflicting statistical outputs | **Unresolved** |
| Price differs across rating levels | No usable test statistic reported | **Unresolved** |
| Relationship is nonlinear | Spearman ≫ Pearson suggests monotonic nonlinearity; but flexible models underperform | **Contradictory evidence** |

**Cross-cutting tensions**
- The correlation results suggest a monotonic but nonlinear relationship, yet the models favor linear fits. Either the nonlinearity is weak in the model-relevant range, or the random forest is overfitting. Partial dependence plots would help resolve this.
- The synthesis attributes the gap between Pearson and Spearman to outliers inflating Pearson. The gap could also reflect nonlinearity on the raw scale. The direction of the bias has not been verified.

## Conclusions

**What we can say with confidence**
1. Larger apartments are associated with higher prices. The association is statistically significant (r = 0.498, ρ = 0.887), and size is the most important feature among those tested.
2. Price is highly right-skewed. Analyses on the raw scale should be treated with caution, and log-scale modeling is appropriate.
3. Size, age, and rating together explain only about 19% of price variation on held-out data. Most of what drives price is not captured in this dataset.
4. The current predictive model is suitable for broad directional guidance, not for property-level valuation.

**What we cannot yet conclude**
- Whether older properties are cheaper, and by how much.
- Whether higher-rated properties command higher prices.
- Whether the size–price relationship is linear, nonlinear, or both.
- Which model is genuinely best, since differences between linear and Huber regression fall within cross-validation noise.

## Limitations & Caveats

**Data quality issues**
- **Price maximum is inconsistent.** Reported as about 1.6M (≈5.5× mean) in one place and 14.3× the mean (≈4.1M) in another.
- **Outlier handling is undocumented.** The method (removal, capping, or winsorizing) and number of affected rows are not recorded.
- **Rating encoding is inconsistent.** It is treated as numeric in the ML pipeline and as ordinal in statistical tests.
- **Skewness values differ slightly** (6.44 vs. 6.42), likely from computation or rounding.

**Statistical limitations**
- Pearson correlation is sensitive to outliers and assumes linearity. Its gap from Spearman indicates these assumptions are not met on the raw scale.
- The Kruskal-Wallis assumption of similar group distribution shapes was not checked.
- Linear regression assumptions (homoscedasticity, normal residuals, independence) were not tested; residual plots are missing.
- No correction for multiple comparisons was applied across the size, age, and rating tests.
- Confidence intervals are missing for the Spearman coefficient and all model R² values.

**Modeling limitations**
- **Inconsistent test R².** The same problem yields 0.159 in one run and 0.189 in another, suggesting different splits, transforms, or evaluation scales. R² values may not be comparable if some were computed on the log scale and others on the original scale.
- **"Best" model label is overstated.** Huber's advantage over linear regression is within cross-validation noise (±0.20).
- **Overfitting diagnosis is unclear.** The train–test gap of 0.34 is not attributed to a specific model, and the cross-validated R² (0.31) is higher than the test R² (0.19), which needs explanation.
- Random forest hyperparameters were not reported, so its poor performance may reflect tuning rather than the data.

**Failed or incomplete analyses**
- No analyses failed outright (6 of 6 tasks completed), but several outputs are incomplete:
  - Full correlation matrix with coefficients and p-values
  - Age effect size and direction
  - Rating test statistic, p-value, and group medians
  - Permutation importance for `age_years` and `rating`
  - Residual diagnostics and influence analysis (e.g., Cook's distance)

**Missing information**
- Source, collection method, and date range of the data
- Currency and units for price
- Definition of "rating" and its scale
- Geographic location or any segment identifiers

## Recommendations

### Immediate Actions

1. **Verify the raw data.** Confirm the maximum price, check for data entry errors, and document how outliers were handled. Do this before any further reporting.
2. **Standardize the evaluation pipeline.** Use one train/test split, one evaluation scale (original price), and report R², RMSE, and MAE together with confidence intervals. Recompute the model comparison under this pipeline.
3. **Rerun the age and rating tests cleanly.** Report one test per variable, with the test statistic, p-value, effect size, and confidence interval. For age, report the coefficient per year with its CI.
4. **Use size as the primary pricing input for decision-making.** It is the only feature with consistent evidence. For directional planning, communicate that size explains roughly a quarter of price variation.
5. **Do not deploy the model for individual property valuations.** Typical errors (about 270K) are close to the average price.
6. **Compare a size-only model** against the three-feature model. If performance is similar, the simpler model is preferable.

### Future Analysis

**Questions to investigate**
- What is the effect of age on price after controlling for size? A partial regression or generalized additive model (GAM) would clarify whether the effect is negative, nonlinear, or null.
- Do rating levels differ in price, and is the relationship monotonic?
- Does price per square meter rise with size? Would a log–log model fit better?
- Are large residuals concentrated in high-priced properties or in specific segments? Would segment-specific models help?
- Does the log-transformed model introduce bias when converted back to the original scale? A smearing correction should be evaluated.
- Would interaction terms (e.g., size × age) or a price-per-square-meter target improve fit?
- Are the models stable across time periods or geographic subgroups?

**Analyses to add**
- Full Pearson and Spearman correlation matrix with p-values and CIs
- Partial dependence plots to test the nonlinearity question directly
- Repeated cross-validation to quantify model stability
- Residual diagnostics and influence analysis
- Hyperparameter tuning details for the random forest and Huber models

**Data to collect**
The model explains only about 19% of price variation, so the highest-value investment is in additional predictors:
- **Location** (neighborhood, district, or coordinates), which is likely the largest missing driver
- **Property condition and renovation status**
- **Floor level, number of rooms, and building type**
- **Amenities** (parking, elevator, outdoor space)
- **Transaction date**, to test for market-wide price trends
- **Clear definitions** for `rating` (scale and source) and `age_years` (age at sale or at listing)

Collecting these variables is likely to improve predictive accuracy far more than changes to model type.