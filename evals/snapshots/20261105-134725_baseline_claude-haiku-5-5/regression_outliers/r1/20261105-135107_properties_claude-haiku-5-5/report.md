# Data Analysis Report: Property Price Modeling

## Executive Summary

- **Log-transform the price target.** Raw price is heavily right-skewed (skewness 6.44; mean 289,164 vs. median 217,450). After a log transform, skewness falls to 0.35, close to symmetric. Any model should be trained and evaluated on log price.
- **Size is the dominant predictor.** `size_sqm` ranks first on RF impurity importance, RF permutation importance (test set), and the largest standardized Ridge coefficient. The price effect per square meter has not been quantified in the available output.
- **The best model explains about 63% of log-price variance.** Ridge regression on log price reached test R² = 0.627 using only three features. Roughly 37% of variation is unexplained, which points to omitted variables such as location, condition, or amenities.
- **Predictions are too imprecise for point valuation but may suit ranking.** The Random Forest's MAPE is about 22.8%, though its basis (raw or back-transformed) is unconfirmed. Use the model for screening or relative ranking, not for precise individual pricing, until residuals and outliers are audited.
- **Linear and tree models perform about equally.** Ridge (0.627) and Random Forest (0.598) differ by 0.03 R² on log price, which is likely within sampling noise on a test set of this size. The simpler linear model is the practical default.

---

## Dataset Overview

| Attribute | Value |
|---|---|
| Source | `/workspaces/agents/evals/data/properties.csv` |
| Rows × columns | 600 × 4 |
| Target variable | `price` (continuous; regression) |
| Features | `size_sqm` (float), `age_years` (float), `rating` (integer-coded) |
| Categorical features | None |
| Missing values | None reported for any column |

The price range extends to roughly 1.6M, against a mean near 289K. The minimum price, the full distribution of the features, and the rating range were not included in the available output.

---

## Analysis Methodology

### Strategic Approach

The analysis followed a three-stage sequence, with each stage informing the next:

1. **Exploratory analysis (first):** Check distributions, correlations, and outliers before modeling. The price range and skew needed to be understood before choosing a model form.
2. **Statistical testing (second):** Test which relationships are significant and whether a log transform is justified. This step determines the target scale and checks whether the predictors are independent.
3. **Predictive modeling (third):** With 600 rows, a train/test split is feasible. Models were compared and feature importance was assessed, informed by the earlier findings.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory data analysis | 2 |
| Statistical analysis | 2 |
| Machine learning | 2 |
| **Total** | **6 of 6 (100% success, 0 failed)** |

Total execution time was 31.7 seconds.

**Note on output quality:** Several specialist outputs were truncated, duplicated, or unlabeled. The findings below are limited to results that are directly supported by the reported numbers. Gaps are flagged explicitly.

---

## Key Findings

### Exploratory Analysis

**Price distribution**
- Mean price is 289,164 and median is 217,450. The mean sits about 33% above the median, a signature of a long right tail.
- Raw price skewness is 6.44, which is far from symmetric.
- Prices extend to about 1.6M, several times the median.
- After log transformation, skewness is 0.35, which is near-symmetric. This supports modeling on the log scale.

**Feature relationships**
- `size_sqm` and `age_years` are uncorrelated: r = −0.0006 (Pearson), with r² ≈ 0.0000. The Spearman correlation is also negligible (ρ = −0.0039).
- The reported correlation tests did not include price, so the strength of size, age, or rating relationships with price is unknown from the available output.

**Outliers and distribution shape**
- Outlier counts, bounds, and treatment were not reported.
- Distribution statistics for `size_sqm`, `age_years`, and `rating` were not included in the output.

**Data completeness**
- No missing values were reported for any column, so the 600 rows appear usable in full.

### Statistical Evidence

| Hypothesis | Test | Result | Decision |
|---|---|---|---|
| H₀: r(size_sqm, age_years) = 0 | Pearson correlation (two-sided) | r = −0.0006, r² = 0.0000, p = 0.9881, 95% CI [−0.081, 0.079] | **Fail to reject.** Effect size is negligible. Holm-adjusted p = 1.0. |
| H₀: size_sqm and age_years are monotonically unrelated | Spearman correlation | ρ = −0.0039, p = 0.9236 | **Fail to reject.** Negligible effect. |
| H₀: raw price is symmetric | Skewness and normality test (name not specified in output) | Skewness = 6.44 | **Reject.** Log transform warranted. |
| H₀: log(price) is symmetric | Skewness and normality test | Skewness = 0.35 | **Supported.** Near-symmetric. |
| H₀: size_sqm has no predictive contribution | RF permutation importance; Ridge standardized coefficient | Largest importance on both measures | **Reject qualitatively.** No p-values or CIs reported. |
| H₀: nonlinear model outperforms linear model | Test R² comparison | Raw scale: LR 0.189 vs. RF 0.066. Log scale: Ridge 0.627 vs. RF 0.598 | **Fail to reject** on log scale. Linear is at least as good. |

**Plain-English interpretation**
- **Size and age are independent.** Knowing a property's size tells you nothing about its age, so their effects on price can be interpreted separately without multicollinearity concerns.
- **Price is multiplicative and right-skewed.** Modeling log price is the appropriate choice. Without it, a few expensive properties would dominate the fit.
- **Simple models are sufficient for now.** There is no statistical evidence that a tree-based model captures structure a linear model misses.

**Caveats on the statistical evidence**
- The claim that size correlates with price is **not statistically validated** in the available output. The model importances imply it, but the correlation test with price is missing.
- Several "REJECT H₀" entries in the statistical output are unlabeled and cannot be traced to a specific test, statistic, or p-value. They are not cited as validated here.
- No confidence intervals are available for model metrics or feature importances.

### Predictive Models

**Models tested**
- Linear Regression (raw price)
- Random Forest (raw price)
- Ridge Regression (log price)
- Random Forest (log price)

**Performance**

| Model | Target Scale | Test R² | Other Metrics |
|---|---|---|---|
| Linear Regression | Raw price | 0.189 | Not reported |
| Random Forest | Raw price | 0.066 | Not reported |
| **Ridge Regression** | **Log price** | **0.627** | Not reported |
| Random Forest | Log price | 0.598 | MAPE ≈ 22.8% |

**Metric note:** Accuracy, precision, and recall are classification metrics and do not apply to this regression task. The appropriate metrics are R², RMSE/MAE (in price units), and MAPE. RMSE and MAE were not reported, so the typical error in currency terms cannot be stated.

**Interpretation of results**
- The R² values are not directly comparable across scales. The jump from 0.189 (raw) to 0.627 (log) reflects the better fit to the multiplicative price structure, and it should not be read as a like-for-like improvement. The raw-scale comparison (0.189 vs. 0.066) is also not a fair test of the models' relative quality.
- The best available model, Ridge on log price, explains about 63% of log-price variance on the test set.
- The Random Forest's MAPE of about 23% indicates that a typical prediction misses the actual price by roughly one-quarter. This is practically meaningful for property valuation. Whether MAPE was computed on raw or back-transformed predictions is unconfirmed.

**Feature importance**

| Rank | Feature | Evidence |
|---|---|---|
| 1 | `size_sqm` | Top-ranked by RF impurity importance, RF permutation importance (test set), and largest standardized Ridge coefficient |
| 2 | `age_years` | Importance values not reported; ranking unknown |
| 3 | `rating` | Importance values not reported; ranking unknown |

Size is the most consistent signal across methods. The effect size (price change per additional square meter) has not been reported, so the magnitude of the effect is unknown.

**Predictive insights**
- Three features are enough to explain a majority of log-price variance, which suggests size, age, and rating capture a meaningful share of value.
- The remaining ~37% of variance likely reflects omitted factors such as location, property type, or condition. None of these are in the dataset.
- The model is better suited to relative ranking than to precise point estimates.

---

## Synthesis

**Validated, consistent patterns**
1. **Log-scale modeling is necessary.** Skewness drops from 6.44 to 0.35, and R² on the log scale is far stronger than on the raw scale.
2. **Size dominates prediction.** It is the top feature across all three importance methods that were reported.
3. **Size and age are independent.** This holds under both Pearson and Spearman tests.
4. **Linear and tree models are roughly equivalent** on log price (0.627 vs. 0.598). The linear model is preferred for interpretability.

**Points that require caution**
- The synthesis claims that size, age, and rating are mutually uncorrelated. Only the size–age pair was tested. The rating correlations are **not** reported and this claim is unverified for rating.
- The statement that linear models "outperform" random forests on raw price mixes scales and should not be cited. The valid comparison is on log price, where the gap is small.
- The apparent nonlinearity flag in one ML output is not supported by a finding. It should not be treated as evidence of interactions.

---

## Conclusions

**What we can say with confidence**
- Price is strongly right-skewed. Modeling log price is the correct approach.
- Size is the most important predictor among the three features.
- A regularized linear model on log price explains about 63% of test-set variance. This is a reasonable baseline.
- Size and age are not correlated in this dataset.
- A typical prediction error is about 23% (MAPE), which is too large for high-stakes individual pricing.

**What we cannot yet say**
- How much a square meter adds to price.
- Whether age and rating contribute meaningfully, or in which direction.
- Whether the ~1.6M properties are legitimate or data errors, and how they influence the fit.
- Whether the linear model holds across subgroups.
- How stable the model ranking is across different splits.

---

## Limitations & Caveats

**Data quality issues**
- The outlier analysis did not report counts, bounds, or treatment. The high-price tail (~1.6M) has not been verified.
- Minimum price, feature distributions, and the rating range are unreported.
- Several statistical results are unlabeled, which prevents verification.

**Statistical and methodological limitations**
- **Single train/test split with unstated size.** A 20% test set would contain about 120 rows. R² estimates on a sample this size carry wide confidence intervals, and a 0.03 difference between models is not interpretable without them.
- **No cross-validation or repeated splits.** Model rankings may not be stable.
- **No hyperparameter tuning reported** for Ridge or Random Forest. The forest may be over- or under-regularized.
- **No residual diagnostics** (heteroscedasticity, residual normality on the log scale, influential points).
- **MAPE basis unclear.** Log-scale MAPE would be misleading.
- **No confidence intervals** on any reported metric or coefficient.

**Failed or incomplete analyses**
- Price-related correlations (size–price, age–price, rating–price) were not reported. These are the most important missing results.
- The full correlation matrix, feature-importance values for age and rating, and the permutation-importance p-values are missing.
- The log-transform comparison was requested with normality tests, but only skewness values were reported.

**Missing information**
- Location, property type, and condition variables, which are likely drivers of the unexplained ~37% of variance.
- Currency units and the data collection period.

---

## Recommendations

### Immediate Actions

1. **Adopt log price as the modeling target** and report all metrics on both log and back-transformed raw scales.
2. **Use the Ridge model as the working baseline** (log-price R² = 0.627) given its interpretability and parity with the Random Forest.
3. **Restrict current use to ranking and screening.** Do not use the model for individual point valuations until the error profile is characterized.
4. **Audit the high-price tail.** Verify whether the ~1.6M properties are accurate records and whether they distort the fit.
5. **Recover the missing outputs:** price correlations with confidence intervals, age and rating coefficients, and the MAPE calculation basis.

### Future Analysis

**Modeling**
- Use k-fold cross-validation and report mean and spread of R², RMSE, and MAE.
- Report RMSE and MAE in currency units, so stakeholders can see typical error in dollars or euros.
- Tune Ridge and Random Forest, and test gradient boosting to assess nonlinear alternatives fairly.
- Test interaction terms (e.g., size × age) and spline or GAM specifications to check for nonlinear effects.
- Run residual diagnostics on the log-scale model and examine influential points.

**Statistics**
- Re-run all pairwise correlations including price, with r, p-values, and 95% confidence intervals.
- Quantify the size effect: the implied percentage price change per additional square meter, with a confidence interval.
- Check whether the size–price slope differs across rating tiers or age bands.

**Data collection**
- **Location** (postcode, neighborhood, or coordinates): likely the largest single source of unexplained variance.
- **Property type and condition**: structure type, renovation status, and number of rooms or bathrooms.
- **Amenities**: parking, outdoor space, proximity to transit.
- **Data dictionary**: definitions and scales for `rating` (range and source) and `age_years` (age at sale or at listing).
- **Measurement validation**: confirm how `size_sqm` is measured, since it is the top predictor.
- **Larger sample**: learning curves would show whether more data would change the linear-versus-tree ranking.

**Decision question to resolve before further investment:** Is the intended use ranking, screening, or point valuation? An acceptable error level for each differs substantially, and the current ~23% MAPE is adequate only for the first two.