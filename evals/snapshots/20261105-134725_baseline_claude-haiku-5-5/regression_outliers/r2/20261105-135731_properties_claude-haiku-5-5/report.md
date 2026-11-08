# Data Analysis Report: Properties

## Executive Summary

- **Property size is the only feature that carries meaningful predictive signal.** Permutation importance assigns 95.5% of the Random Forest's importance to `size_sqm`. Shuffling size raises test RMSE by about 70,500, while shuffling age or rating raises it by only about 2,900 and 500.
- **The available features explain only a small share of price variation.** The best model, linear regression, reaches a held-out R² of 0.189, meaning it explains about 19% of price variance. Predictions are typically off by about 102,000 (test MAE). The model is useful as a rough size-based estimate, not for individual property valuations.
- **Important price drivers appear to be missing from the dataset.** With only four columns, the data cannot capture location, property type, condition, or amenities. Collecting these variables is the highest-value next step, ahead of further modeling.
- **Price is likely right-skewed, and a few high-value properties probably drive most of the error.** The test RMSE is about 2.7 times the MAE (273,535 vs. 102,395), which indicates that large residuals dominate the squared-error loss. Skewness was not directly measured, so this is an inference.
- **Simple models outperformed the tree-based ensemble.** Linear regression beat the untuned Random Forest by about 22,100 in test RMSE (273,535 vs. 295,646). The relationship appears approximately linear and additive, and added complexity did not help.

**Decisions supported by this analysis:** Use the model only for rough, size-based screening. Do not use it for individual valuations or pricing decisions. Prioritize data collection for location and property-quality variables. Test a log-price model before any further modeling investment.

---

## Dataset Overview

| Attribute | Value |
|---|---|
| Source | `/workspaces/agents/evals/data/properties.csv` |
| Observations | 600 rows |
| Columns | 4 (all numeric) |
| Target variable | `price` (continuous; regression task) |
| Features | `size_sqm` (float), `age_years` (float), `rating` (integer) |
| Missing values | 0 in all columns (0.0%) |

The target `price` reportedly ranges up to about 1.6 million, with a mean near 289,000. These figures come from the analysis brief and were not reproduced in the detailed EDA output.

---

## Analysis Methodology

### Strategic Approach

Three analysis strategies were applied in priority order:

1. **Exploratory analysis (first).** With 600 rows, four numeric columns, no missing values, and a regression target, the distribution of price and the presence of outliers had to be understood before modeling. The brief flagged the gap between the mean and the maximum as a possible sign of skew.
2. **Statistical analysis (second).** This stage tested the relationships among size, age, and rating, and checked for nonlinearity and heteroscedasticity to inform model choice.
3. **Predictive modeling (third).** A train/test split of the 600 rows supported a linear regression baseline and a tree-based ensemble, with permutation feature importance to quantify each feature's contribution.

### Execution

| Specialist | Tasks Completed | Status |
|---|---|---|
| Exploratory Data Analysis | 2 | Completed |
| Statistical | 1 | Completed |
| Machine Learning | 3 | Completed |
| **Total** | **6** | **100% success (0 failures)** |

Total execution time was 17.5 seconds.

---

## Key Findings

### Exploratory Analysis

**Data integrity**
- The dataset has 600 rows and 4 columns, with no missing values in any column. The data types are float64 for `size_sqm`, `age_years`, and `price`, and int64 for `rating`.
- The first rows show plausible values. For example, a 121.5 m² property rated 5 with age 33.7 years sells for 145,700, and an 88.4 m² property rated 5 with age 0.6 years sells for 225,500.

**Distribution of the target**
- The brief reports a price maximum of about 1.6M against a mean of about 289K, a ratio of roughly 5.5 to 1. This pattern suggests a long right tail, but the EDA output did not include skewness, quartiles, or an outlier count, so the magnitude of the skew is unmeasured.

**Limitations of the EDA output**
- The EDA output did not include the price distribution summary, skewness, outlier counts, or the correlation matrix between features and price. These are the most important exploratory results, and they are missing from the record. The conclusions in this report about the target's distribution rely on indirect evidence.

### Statistical Evidence

The statistical analysis tested relationships among the features. It did not test any relationship involving price.

**Test 1: Pearson correlation, size vs. age**
- **Purpose:** Test whether size and age have a linear association.
- **Result:** r = −0.0006, R² = 0.0000
- **P-value:** 0.988 (α = 0.05)
- **95% CI (Fisher z):** [−0.081, +0.079]
- **Decision:** Fail to reject H₀
- **Effect size:** Negligible
- **Interpretation:** Size and age are not linearly related in this sample. Because the confidence interval is narrow, the test could detect any correlation larger than about ±0.08. The data rule out any substantial linear link.

**Test 2: Spearman rank correlation, size vs. age**
- **Purpose:** Test for a monotonic, possibly nonlinear, association.
- **Result:** ρ = −0.0039
- **Decision:** Fail to reject H₀ (no monotonic association)
- **Interpretation:** The rank-based result agrees with the Pearson test. There is no evidence of a curved or monotonic pattern between size and age.

**Test 3: Size vs. rating (linear and monotonic)**
- **Purpose:** Test whether property size is associated with rating.
- **Decision:** Fail to reject H₀ for both the linear and monotonic tests (α = 0.05)
- **Caveat:** Test statistics and p-values were not reported for these tests, so effect sizes cannot be stated.

**Summary of statistical results**

| Relationship | Test | Decision (α = 0.05) | Effect size |
|---|---|---|---|
| Size vs. age | Pearson | Fail to reject H₀ (p = 0.988) | r = −0.0006 |
| Size vs. age | Spearman | Fail to reject H₀ | ρ = −0.0039 |
| Size vs. rating | Linear and monotonic | Fail to reject H₀ | Not reported |

**Not tested or not reported**
- Correlation of size, age, or rating with price (the central question)
- Nonlinearity of the price relationship (e.g., RESET or polynomial comparison)
- Heteroscedasticity (e.g., Breusch-Pagan or White test)
- Age vs. rating
- Normality of residuals

### Predictive Models

**Models tested**
- **Linear regression:** Baseline model; best by test RMSE.
- **Random Forest regressor:** Untuned tree-based ensemble.

Because this is a regression task, classification metrics such as accuracy, precision, and recall do not apply. Performance is reported with RMSE, MAE, and R².

**Held-out test performance (single train/test split)**

| Model | RMSE | MAE | R² |
|---|---|---|---|
| Linear Regression | 273,535 | 102,395 | 0.189 |
| Random Forest | 295,646 | 107,135 | 0.053 |

**Interpreting the metrics**
- **R²:** The linear model explains about 19% of price variance. The Random Forest explains about 5%.
- **RMSE vs. MAE:** RMSE is about 2.7 times MAE for the linear model. The gap indicates that a minority of large errors inflates the squared error.
- **Baseline context:** Back-calculating from R² and RMSE gives a test-set price standard deviation of about 304,000. The linear model therefore reduces error only modestly relative to predicting the average price for every property.

**Feature importance (Random Forest, permutation importance on the test set)**

| Feature | Share of importance | RMSE increase when shuffled |
|---|---|---|
| `size_sqm` | 95.5% | +70,509 |
| `age_years` | 3.9% | +2,857 |
| `rating` | 0.7% | +484 |

The shares are consistent with the raw RMSE increases. Rating's contribution is close to the noise level for a single split.

**Predictive insights**
- Size carries nearly all of the usable signal in this dataset.
- Age and rating add very little. Whether they affect price cannot be determined here, because their correlation with price was not tested.
- The Random Forest did not generalize as well as the linear model. The brief reports an overfitting flag, but the train-versus-test values that would confirm it were not included in the output.

---

## Synthesis

Combining the analyses produces a consistent picture, with some limits on what can be confirmed.

**Validated or well-supported findings**

| Finding | Evidence | Status |
|---|---|---|
| Size is the dominant predictor | 95.5% of permutation importance; +70,509 RMSE when shuffled | Supported (model-based, not a formal test) |
| Features explain a modest share of price variance | Test R² = 0.189 (linear), 0.053 (Random Forest) | Supported |
| Relationship appears approximately linear | Linear model beats Random Forest by 22,111 RMSE | Supported indirectly; no formal nonlinearity test |
| Size is unrelated to age | r = −0.0006, p = 0.988; ρ = −0.0039 | Supported (no association) |
| Size is unrelated to rating | Failed to reject H₀ (statistic not reported) | Supported in direction; effect size unknown |

**Cross-cutting interpretation**
- Because size is independent of age and rating, the features carry separate information. The weak model performance is therefore not caused by redundant predictors. The low R² more likely reflects missing variables.
- Age and rating appear to have little independent predictive value in this sample. The stronger interpretation, that they have no effect on price, cannot be made without testing their correlation with price directly.

**Not validated**
- Heteroscedasticity and residual normality
- Significance of any correlation with price
- The size-to-price effect size (for example, the price increase per additional square meter)
- Whether the Random Forest actually overfits (train metrics were not reported)

---

## Conclusions

**What we can say with confidence**
1. **Size is the main driver of price in this dataset.** Among the three features available, size is the only one with a meaningful predictive contribution.
2. **The current feature set is insufficient for reliable valuation.** The best model explains about 19% of price variance and typically misses by about 102,000.
3. **Simple linear models perform better than the untuned Random Forest here.** Added complexity did not improve test performance.
4. **Size, age, and rating are essentially independent of each other.** Multicollinearity is not a concern for this feature set.

**What we cannot yet conclude**
- The size-to-price effect size, and its statistical significance.
- Whether age and rating affect price in a way the models missed.
- Whether the price distribution is skewed in the way the brief suggests.
- Whether the Random Forest's gap is stable across different data splits.

**Bottom line:** The dataset supports a simple, approximate size-based estimate of price. It does not support individual property valuation or any conclusion about the drivers beyond size.

---

## Limitations & Caveats

**Data quality issues**
- The EDA output was incomplete. It did not include the price distribution, skewness, outlier counts, or the feature-price correlation matrix. Some statements about the target's distribution are inferred from summary figures rather than measured.
- The statistical output reported decisions for several tests but omitted test statistics and p-values for most of them.
- The brief's summary statistics (price mean near 289K, maximum near 1.6M) were not reproduced in the detailed output and should be verified against the source file.

**Statistical assumptions and limitations**
- **Linear regression assumptions** (homoscedastic, approximately normal residuals) are likely violated, given the suspected right skew and the RMSE-to-MAE gap. No diagnostic test was run to confirm this.
- **Single train/test split.** The reported R² and RMSE values come from one split of 600 rows. Their sampling variability is unknown, and the margin between the two models has not been validated.
- **Untuned Random Forest.** The tree-based comparison used default-style settings and may understate what a tuned ensemble could achieve, although the feature set's limits likely remain the binding constraint.

**Inconsistencies in the reported results**
- The feature importance was described as coming from the "best model," but by test RMSE the best model is linear regression. The importances reported are from the Random Forest. Linear coefficients were not reported, so it is unknown whether the linear model also assigns size dominant weight.
- The overfitting claim refers to gap values that were not included in the output.

**Failed or missing analyses**
- No direct test of the relationship between any feature and price.
- No nonlinearity test (e.g., RESET or polynomial comparison).
- No heteroscedasticity test on the linear residuals.
- No influence diagnostics (e.g., Cook's distance) for high-price observations.
- No cross-validated performance estimates or confidence intervals.
- No check on whether high-priced properties form a distinct segment.

---

## Recommendations

### Immediate Actions

1. **Restrict the current model's use.** Apply it only as a rough, size-based screening tool or benchmark. Do not use it for individual property valuations, pricing decisions, or any decision with significant financial consequences.
2. **Complete the missing EDA.** Report the price distribution (skewness, quartiles, outlier count) and the correlation of each feature with price, with p-values and confidence intervals. This is inexpensive and resolves the most important gaps.
3. **Verify the high-price observations.** Confirm that the values near 1.6M are genuine and not data-entry errors. Check whether they are a separate market segment. Errors in these few rows could distort both the model and the RMSE.
4. **Test a log-price model.** If price is right-skewed, a log transformation may reduce the influence of extreme values and improve residual behavior. Compare its RMSE and MAE with the current results, reported on the original price scale.
5. **Report linear coefficients** alongside the permutation importance so that feature contributions are reported consistently for the best-performing model.

### Future Analysis

**Modeling and statistical checks**
- Run repeated or k-fold cross-validation to estimate the variability of R², RMSE, and MAE, and to confirm the linear-versus-Random-Forest ranking.
- Test for nonlinearity (e.g., RESET test, or a comparison of polynomial size terms against a linear term) and for heteroscedasticity (Breusch-Pagan or White test).
- Examine residuals and influence (Cook's distance) for the high-price properties.
- Consider quantile regression or prediction intervals if decisions depend on the range of plausible prices rather than a point estimate.
- Tune a gradient boosting model before concluding that nonlinear methods offer no advantage.

**Questions to investigate**
- Is the relationship between size and price nonlinear at the extremes (for example, rising price per square meter for large units)?
- Do age and rating affect price once size is controlled for, or do they matter only within specific segments (such as older properties in particular areas)?
- Are high-priced properties a distinct segment that requires separate modeling?

### Data to Collect

The most important gap is a set of explanatory variables that the current dataset lacks. In priority order:

1. **Location:** Neighborhood, postal code, or coordinates, with distance to amenities or the city center. This is likely the largest single missing driver.
2. **Property type and layout:** House, apartment, or other type; number of bedrooms and bathrooms; floor level; presence of a garage or outdoor space.
3. **Condition and quality:** Renovation status, build quality, and energy rating.
4. **Amenities:** Parking, transit access, schools, and other local features.
5. **Transaction context:** Sale date (to control for market trends), listing versus sale price, and seller type.
6. **Data definitions:** Clear definitions of `rating` (source, scale, and whether it is assessed or reported), and the currency and date basis of `price`.

Collecting these variables would test whether the low explained variance reflects missing information, and would likely raise predictive performance more than any further change in model type.