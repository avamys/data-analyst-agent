# Data Analysis Report: Properties

## Executive Summary

- **The three available features explain only a small share of price variation.** The best model, Ridge regression, reaches R² = 0.189 on held-out data, so size, age, and rating account for roughly 19% of price variance. Typical absolute errors are about 102,000 (MAE), and the RMSE of 273,506 indicates that a minority of large errors dominates.
- **Size is the leading price driver, but its effect is not quantified.** size_sqm ranks first by permutation importance. The direction and magnitude of its effect (for example, price change per square meter) were not reported.
- **Price is non-normal and right-skewed, so a transformation should be tested.** Normality and skewness tests rejected the null hypothesis. The before/after log-transform comparison that would confirm the fix is missing from the outputs.
- **size_sqm and age_years are statistically independent.** The Pearson correlation was r = -0.0006 (p = 0.988), which means the two features do not share information and their effects can be interpreted separately.
- **The model is not ready for individual property valuation.** Its errors are too large for pricing single properties. It can support rough, directional analysis only until missing features (most likely location) are added and the log-transform and residual checks are completed.

## Dataset Overview

| Attribute | Value |
|---|---|
| Source | `/workspaces/agents/evals/data/properties.csv` |
| Rows × columns | 600 × 4 |
| Target variable | `price` (continuous, regression) |
| Features | `size_sqm` (float), `age_years` (float), `rating` (integer) |
| Categorical features | None |
| Missing values | 0 in all four columns |
| Price range | Tens of thousands to over 1.5 million (per the analysis brief) |

The dataset is small but usable for regression. It is clean: no missing values were found in any column. Exact summary statistics for price (mean, median, standard deviation, skewness, kurtosis) were not included in the outputs.

## Analysis Methodology

### Strategic Approach

Three strategies were applied in this order:

1. **Exploratory analysis** came first to establish data quality, distributions, correlations, and outliers before any modeling.
2. **Statistical analysis** followed to test whether the relationships seen in exploration were significant. It also covered whether price was skewed enough to justify a log transform.
3. **Predictive modeling** came last. A clear target and 600 rows allowed a train/test split and cross-validated regression, with feature importance used to rank drivers.

This sequence is sound. The statistical tests used a Bonferroni correction for six pairwise comparisons (α = 0.05 / 6 ≈ 0.0083), which controls false positives across the family of tests.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory Data Analysis | 2 |
| Statistical Analysis | 2 |
| Machine Learning | 2 |
| **Total** | **6 of 6 (100%)** |

Total execution time was 60.5 seconds. All six tasks completed. However, several task outputs were truncated, so "completed" does not mean every planned result was reported (see Limitations).

## Key Findings

### Exploratory Analysis

**What the outputs establish:**
- **Structure:** 600 rows, 4 columns. Dtypes are float64 for `size_sqm`, `age_years`, and `price`, and int64 for `rating`.
- **Data quality:** Zero missing values in every column (0.0%). This is a strength and removes the need for imputation.

**What was requested but not reported:**
- Price distribution: mean, median, standard deviation, skewness, and kurtosis
- Outlier counts and thresholds for any variable
- Distribution summaries for `size_sqm`, `age_years`, and `rating`
- The full correlation matrix, including price

Because these outputs are absent, the report cannot give specific percentages for price concentration, tail behavior, or outlier share. The price range (tens of thousands to over 1.5 million) indicates a wide spread, and the statistical results below suggest a right-skewed distribution with a long upper tail, but the magnitude of that skew is not documented.

### Statistical Evidence

#### Test 1: Pearson correlation, size_sqm vs. age_years

- **Purpose:** Test whether a linear relationship exists between size and age.
- **Result:** r = -0.0006
- **P-value:** 0.988 (Bonferroni-adjusted: 1.000)
- **95% confidence interval:** [-0.081, 0.079]
- **Effect size:** r² = 0.0000 (0.0% shared variance); negligible
- **Conclusion:** Fail to reject H0. No significant linear correlation.
- **Plain English:** Knowing a property's size tells us nothing about its age, and vice versa. The confidence interval includes zero and is narrow, so this is a precise null result rather than a lack of power.

#### Test 2: Spearman rank correlation, size_sqm vs. age_years

- **Purpose:** Test for a monotonic (not necessarily linear) relationship.
- **Result:** Fail to reject H0 after Bonferroni correction (per the insight summary).
- **Specific rho, p-value, and CI:** Not reported in the output.
- **Plain English:** No monotonic relationship between size and age was detected. This agrees with the Pearson result.

#### Additional Correlation Tests

The output reports a significant linear correlation that survives Bonferroni correction. The variable pair is not named, and no r, p-value, or CI is given. The analysis ran six pairwise tests, but only the size–age results are shown. **The price correlations, which matter most for this analysis, are therefore unverified.**

#### Test 3: Price normality and skewness

- **Purpose:** Determine whether price is skewed enough to justify a log transform.
- **Results:**
  - Two skewness tests rejected H0 (p < 0.05).
  - Three normality tests rejected H0 (p < 0.05).
- **Effect size:** Skewness values and kurtosis not reported.
- **Log-transform comparison:** Not reported. The recommended target representation could not be verified from the output.
- **Plain English:** Price departs significantly from a normal distribution and is skewed. Such skew commonly inflates RMSE and reduces fit on the raw scale, and it suggests modeling log(price). This is a well-supported hypothesis, but not yet a demonstrated improvement.

#### Summary of Statistical Results

| Hypothesis | Test | p-value | Decision | Confidence |
|---|---|---|---|---|
| size and age are linearly correlated | Pearson | 0.988 | Fail to reject H0 | High (precise null) |
| size and age are monotonically correlated | Spearman | Not reported | Fail to reject H0 | Moderate (no detail) |
| Price is skewed | Skewness test (×2) | < 0.05 | Reject H0 | High, magnitude unknown |
| Price is not normal | Normality test (×3) | < 0.05 | Reject H0 | High |
| A price pair is linearly correlated | Pearson | < 0.0083 (implied) | Reject H0 | Unverified (pair unnamed) |
| Log transform improves normality | Before/after | Not reported | Not tested | None |

### Predictive Models

**Task:** Predict `price` from `size_sqm`, `age_years`, and `rating`.

**Models tested:**
- **Ridge regression** (best held-out performer)
- **Random Forest** (tuned)

**Performance (Ridge, held-out test split):**

| Metric | Value | Interpretation |
|---|---|---|
| R² | 0.189 | Explains ~19% of price variance; ~81% unexplained |
| RMSE | 273,506 | Penalizes large errors heavily |
| MAE | 102,307 | Typical absolute error of about 102,000 |

The RMSE-to-MAE ratio is about 2.7. This means the errors are heavy-tailed: a small number of properties with very large errors (most likely high-priced ones) drive most of the RMSE. This is consistent with skewed price and suggests that a log-scale model may help.

*Note: Classification metrics (accuracy, precision, recall) do not apply to this regression task and were not computed.*

**Random Forest:**
- Train/test R² gap: 0.31, indicating overfitting.
- Test-set R² and error metrics were not reported.
- Per the synthesis, it did not outperform Ridge on test R².

**Feature importance:**
- **size_sqm** ranks first by permutation importance.
- The full ranking, importance magnitudes, and impurity-based rankings were not reported. The two importance methods reportedly disagree, but the disagreement is not quantified.

**Coefficients and directions:** Not reported. The effect of each feature on price (for example, change in price per additional square meter, or per additional year of age) is unknown.

**Predictive insights:**
- A linear model outperforming a more flexible forest suggests that the signal is largely linear and that additional complexity mainly fits noise.
- The three features leave most price variation unexplained. The missing ~81% likely reflects variables not in the dataset, such as location, property type, or condition.

## Synthesis

Combining the three analyses produces these cross-cutting conclusions:

**Validated (consistent across analyses):**
1. **Features are independent of each other.** size and age are uncorrelated (r = -0.0006), which supports reading their effects separately.
2. **Price is non-normal and skewed.** Both skewness and normality tests agree.
3. **Size is the dominant feature.** It leads permutation importance, which is consistent with economic intuition, though its effect size is undocumented.
4. **Model performance is limited by the feature set, not by model complexity.** Ridge beats the Random Forest, and the forest overfits.

**Linked but unproven:**
- **Skew and weak fit may be connected.** The high RMSE-to-MAE ratio is consistent with a right-skewed target dominating errors. A log transform could improve fit, but this has not been shown.

**Unresolved contradictions:**
- The source attributes the importance disagreement to "correlated features." Size and age are uncorrelated, so either rating is correlated with size or age (untested) or the cause lies elsewhere.
- The unnamed significant correlation may or may not involve price. If it does, it would be the most important relationship in the dataset, and it cannot be interpreted until identified.

## Conclusions

**What we can say with confidence:**
1. The dataset is clean, with no missing values.
2. Size, age, and rating together explain about 19% of price variance on held-out data. They are not sufficient for accurate individual property valuation.
3. Size and age are statistically independent.
4. Price is significantly non-normal and right-skewed.
5. Ridge regression generalizes better than the tuned Random Forest on this data.

**What we suspect but cannot yet confirm:**
- Size is the largest price driver.
- A log-transformed target would improve fit.
- Rating is related to size or age and affects the importance rankings.

**What we cannot conclude:**
- The direction or magnitude of any feature's effect on price.
- Whether rating matters at all.
- Which pair produced the unnamed significant correlation.
- Whether nonlinear or interaction effects exist.

## Limitations & Caveats

### Data Quality and Output Issues
- **Truncated EDA output.** Only the header, dtypes, and missingness check appeared. Price distribution statistics, outlier analysis, and the correlation matrix are missing.
- **Incomplete statistical output.** Spearman results, most pairwise correlations, skewness values, and the log-transform comparison were not reported.
- **Duplicated and merged insight lines.** Several conclusions appear more than once, suggesting that output was repeated or merged.
- **Unnamed significant result.** One reported rejection cannot be attributed to a variable pair.

### Statistical and Modeling Assumptions
- **Linearity and homoscedasticity.** Ridge assumes a linear relationship and constant error variance. Residual diagnostics were not reported. A skewed target likely violates homoscedasticity, so prediction intervals would be unreliable.
- **Ambiguous validation scheme.** One task describes a cross-validated baseline and another a held-out test split. It is unclear whether the reported Ridge metrics come from cross-validation, a single split, or both.
- **Target scale uncertainty.** The reported RMSE (273,506) is consistent with raw-price modeling. If a log-scale model were in use, that figure would be implausible, so the metrics are most likely on the raw scale. This should be confirmed.
- **Multiple testing.** Bonferroni correction was clearly applied to the correlation tests. It is not documented for the normality and skewness tests.
- **Sample size.** With n = 600, the correlation tests are well powered for moderate effects. Overfitting in the Random Forest suggests the sample is adequate for simple models but limited for complex ones.

### Failed or Incomplete Analyses
- No analyses failed outright, but the following were not completed or reported:
  - Log-transform before/after comparison
  - Random Forest test-set metrics
  - Ridge coefficients
  - Residual analysis
  - Interaction and nonlinearity tests
  - Price-specific correlations

### Missing Information
- Effect sizes and confidence intervals for most tests
- Price summary statistics and outlier counts
- Feature importance magnitudes
- Model coefficients and their directions
- Full correlation matrix

## Recommendations

### Immediate Actions

1. **Do not use the current model for individual property valuation.** A typical error of about 102,000 and an R² of 0.19 are insufficient for pricing decisions. Use it, if at all, only for rough, portfolio-level directional analysis, and report its uncertainty.
2. **Adopt a log-transformed target as the default for further modeling**, pending confirmation. The skewness and normality results support it, and the heavy-tailed errors suggest it will help. Compare before and after on the same split.
3. **Recover the missing outputs before drawing further conclusions.** Priority items are:
   - The full correlation matrix, including all price pairs, with r, p-values, and CIs
   - Price skewness and kurtosis values
   - The name of the significant correlation pair
   - The Ridge coefficients and the Random Forest test metrics
4. **Use Ridge coefficients (on the chosen scale) to report feature directions and magnitudes**, since these are needed for any business interpretation of size and age.
5. **Standardize the validation scheme.** Use one documented method (preferably k-fold cross-validation with a final held-out test set) and report it consistently.

### Future Analysis

**Analyses to run:**
- Log-transform comparison: normality, skewness, R², RMSE, and MAE on both scales
- Residual diagnostics: plots of residuals against fitted values, checks for heteroscedasticity, and identification of influential points
- Outlier influence analysis: determine whether a small set of high-priced properties accounts for most of the RMSE
- Rating analysis: test rating's correlation with price, size, and age, and its contribution to model fit
- Nonlinear and interaction models: splines for size and age, and size × age and size × rating interactions
- Regularized forest: retune the Random Forest (shallower trees, larger minimum leaf size) to reduce overfitting
- Gradient boosting or similar models, compared on the same split

**Data to collect:**
- **Location** (district, postcode, or coordinates). This is the most likely source of the unexplained ~81% of variance.
- **Property type** (apartment, house, etc.) and number of rooms or bedrooms
- **Condition or renovation status**
- **Transaction date**, to control for market timing
- **Documentation of rating's definition and scale**, so its effect can be interpreted
- **Additional observations** to strengthen the tails, where the high-price error is concentrated

Once these are in place, the model should be re-evaluated against the current baseline. Success criteria should be set in advance, for example a target R² and MAE on a held-out set, and the model should not be deployed for valuation until it meets them.