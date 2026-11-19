# Data Analysis Report: Daily Sales

## Executive Summary

- **Promotions are associated with higher sales, but the effect is modest.** Promo has the strongest linear correlation with sales (r = 0.273, p = 5.82e-14), explaining about 7.5% of daily sales variance (r² ≈ 0.075). Promo-on and promo-off periods differ significantly (p = 2.06e-12), though the group means and effect size were not reported.
- **Temperature has no detectable linear relationship with sales** (r = 0.016, p = 0.671). It should not be used as a sales driver on this evidence, though a nonlinear or conditional effect has not been ruled out.
- **Neither predictive model is usable for forecasting.** On the held-out period, the random forest achieved R² = −1.23 and the baseline achieved R² = −4.75. Both perform worse than predicting the test-period mean, so the current feature set does not forecast sales.
- **The likely cause of the forecast failure is non-stationarity.** The EDA reports a long-run trend and weekly seasonality, but their magnitudes are unquantified. Until these are modelled, forecasts and promo-lift estimates should be treated with caution.
- **Decision guidance:** Promotions can be treated as a real but small associated driver of sales. Do not use the current models for budgeting or forecasting, and do not claim promo causes the lift until the time structure is controlled for.

## Dataset Overview

| Attribute | Value |
|---|---|
| Source | `/workspaces/agents/evals/data/daily_sales.csv` |
| Rows × columns | 730 × 4 |
| Columns | `date`, `temperature`, `promo`, `sales` |
| Target variable | `sales` (continuous, regression) |
| Feature types | 2 numeric (`temperature`, `sales` excluded as target: `temperature` numeric), `promo` (binary, treated as categorical) |
| Date coverage | Starts 2023-01-01; 730 rows is consistent with two years of consecutive days, but continuity was not explicitly confirmed |
| Missing values | 0 |
| Duplicate rows | 0 |
| Promo distribution | 626 non-promo days (85.8%), 104 promo days (14.2%) |

The promo class is imbalanced: only 104 promotional days, so promo-on estimates rest on a small group.

## Analysis Methodology

### Strategic Approach

The analysis followed three stages in priority order:

1. **Exploratory analysis** to establish distributions, outliers, correlations, and the time structure of the date column. Dates were to be parsed into temporal features and checked for daily continuity.
2. **Statistical testing** to verify whether observed relationships are significant. This included Pearson correlations, Spearman rank correlations, and group comparisons of promo-on versus promo-off sales (t-test or ANOVA).
3. **Predictive modelling** using a time-aware train/test split, with a baseline for comparison. A random split was deliberately avoided because the data is sequential.

### Execution

| Specialist | Tasks Completed | Status |
|---|---|---|
| Exploratory (EDA) | 2 | Completed |
| Statistical | 2 | Completed |
| Machine Learning | 2 | Completed |
| **Total** | **6** | **100% success, 0 failures** |

Total execution time was 28.6 seconds.

**Note on output completeness:** All six tasks completed, but several requested outputs were not returned. These include skewness, outlier counts, Spearman and confidence-interval values, group means, effect sizes, MAE/RMSE, and feature importances. Where these are absent, this report says so rather than estimating them.

## Key Findings

### Exploratory Analysis

**Sales distribution**
- Mean sales: **270.84**; median: **270.25**; standard deviation: **41.13**
- Range: **178.3 to 391.8**
- Interquartile range: approximately **239.4 to 300.5**
- Mean and median are nearly equal, which suggests a roughly symmetric distribution. Skewness was flagged but not quantified, so this should be confirmed before finalising any transformation decision.

**Data quality**
- All 730 rows are complete, with no missing or duplicate records.

**Correlations with sales**
- **Promo:** r = 0.273, the strongest linear correlate of sales
- **Temperature:** r = 0.016, effectively zero
- Promo explains roughly 7.5% of sales variance; temperature explains about 0.02%

**Temporal structure**
- The EDA reports a long-run upward or shifting trend, day-to-day persistence (autocorrelation), and weekly seasonality. These findings matter for model validity but were not quantified.

### Statistical Evidence

| Hypothesis | Test | Statistic | p-value | α = 0.05 | Interpretation |
|---|---|---|---|---|---|
| Temperature is linearly associated with sales | Pearson correlation (df = 728) | t = 0.42, r = 0.016 | 0.671 | Fail to reject H₀ | No meaningful linear relationship |
| Promo is linearly associated with sales | Pearson correlation | r = 0.273 | 5.82e-14 | Reject H₀ | Significant positive association |
| Promo group means differ | t-test / ANOVA | Not reported | 2.06e-12 | Reject H₀ | Sales differ between promo-on and promo-off days |
| Other pairwise associations | Correlation tests | Not reported | 0.388; 0.781 | Fail to reject H₀ | No evidence of association for these pairs |

**Effect sizes and confidence intervals**
- Promo: r = 0.273 (R² ≈ 0.075). This is a small-to-moderate effect in practical terms.
- Temperature: r = 0.016 (R² = 0.0002). Negligible.
- Group-level effect sizes (Cohen's d or η²) and confidence intervals were not reported.

**Plain-English interpretation**
- Promotional days have higher sales than non-promotional days, on average. The association is statistically robust under the standard test, but its size in currency terms is unknown until group means are reported.
- Temperature has no detectable linear link with sales.
- Unidentified pairwise tests returned p-values of 0.388 and 0.781, and the output does not name the variables involved. These results should not be attributed to specific relationships.

**Caveat on p-values:** The correlation tests assume independent observations. Daily sales show persistence, which reduces the effective sample size. The reported p-values are therefore likely overstated, though the promo result is strong enough that it may survive a correction. This has not been verified.

### Predictive Models

**Models tested**
- Baseline model (reference for comparison)
- Random forest regressor
- Train/test split was time-aware, as intended

**Performance on the held-out test period**

| Model | R² | Interpretation |
|---|---|---|
| Baseline | −4.754 | Much worse than predicting the test mean |
| Random forest | −1.229 | Worse than predicting the test mean, but better than the baseline |

Because this is a regression task, accuracy, precision, and recall do not apply. The relevant metrics are R², MAE, and RMSE. MAE and RMSE were not reported, so error magnitude cannot be expressed in sales units.

**Feature importances:** Not available. The ML task did not return a ranking of temperature, promo, trend, day-of-week, and month.

**Predictive insights**
- Neither model generalises to the test period. Negative R² means the models add error relative to a constant prediction of the test mean.
- The most likely explanation is a shift in the level of sales between training and test periods. A trending series placed in a time-aware split will often fall outside the range the model learned from. Tree ensembles cannot extrapolate beyond their training range, which would explain the poor random forest result.
- A reported train/test RMSE gap described as "moderate" does not show that the model generalises. The negative test R² is the more reliable indicator, and it contradicts the generalisation claim.

## Synthesis

**Validated findings**
1. **Promo is associated with higher sales.** This is supported by the correlation (r = 0.273) and by the group-difference test (p = 2.06e-12). Both point the same way.
2. **Temperature is not linearly associated with sales** (r = 0.016, p = 0.671).
3. **Sales are approximately symmetric** (mean ≈ median), though skewness has not been confirmed numerically.

**Consistent patterns**
- Promo is the only variable with a demonstrated association with sales. This pattern holds across the correlation and group-comparison analyses.
- Temporal structure (trend, persistence, weekly seasonality) is reported by the EDA and is the most plausible reason the predictive models failed.

**Unresolved tensions**
- The ML output's generalisation claim conflicts with negative test R². The R² result should be treated as the operative finding.
- The promo association may partly reflect timing. If promotions cluster in particular periods (for example, high-trend phases or particular weekdays), the observed lift could be confounded with trend or seasonality. This has not been tested.
- Interactions (for example, promo × day-of-week or promo × trend) were not tested.

## Conclusions

**What we can say with confidence**
- Promotional days show higher sales than non-promotional days, and the association is statistically significant. The effect is modest, explaining roughly 7.5% of daily variance.
- Temperature does not have a detectable linear relationship with sales in this dataset.
- The current models cannot forecast daily sales on the held-out period. Both produce negative R².

**What we cannot yet say**
- The size of the promotional lift in currency terms, and whether it justifies promotional spend. Group means and confidence intervals are needed.
- Whether promotions cause the sales increase, as opposed to being associated with it because of timing.
- Which features drive sales once trend and seasonality are controlled, since feature importances were not returned.
- Whether temperature has a nonlinear or conditional effect (for example, extreme heat, or interaction with promo).

## Limitations & Caveats

**Data quality**
- The dataset is complete and has no duplicates, but it contains only four columns. No product, store, price, or competitor variables are available, which limits the explanatory scope.
- Daily continuity was intended to be checked but is not explicitly confirmed. Gaps would affect lag and trend features.
- The promo group is small (104 days), so promo-on estimates are less precise than the full-sample statistics suggest.

**Statistical assumptions**
- Correlation tests assume independent observations. Autocorrelation in sales violates this, so reported p-values are likely overstated.
- Normality and equal-variance checks were not reported. With n = 730 the t-test and ANOVA are reasonably robust to mild departures, but this has not been verified.
- Effect sizes and confidence intervals for group comparisons are missing.

**Failed or incomplete analyses**
- The predictive models failed on the held-out period (negative R²).
- Several requested outputs were not returned: skewness, outlier counts, Spearman results, group means, MAE/RMSE, and feature importances.
- Five "REJECT the null" outputs had no associated test names or statistics. They were not counted as independent evidence.
- The output does not identify which variable pair produced some of the p-values, so those results are not attributed in this report.

**Missing information**
- Group means and confidence intervals for promo versus non-promo sales
- Trend magnitude, seasonality amplitude, and stationarity tests (ADF/KPSS)
- Autocorrelation diagnostics
- Feature importances and error metrics (MAE, RMSE)
- Walk-forward or rolling-origin validation results

## Recommendations

### Immediate Actions

1. **Do not use the current models for forecasting or budgeting.** Both fail on the held-out period.
2. **Treat promotions as a real but modest associated driver.** Use them in planning as a factor to monitor, not as a proven lever. Before committing spend, estimate the promo lift in currency terms with a confidence interval.
3. **Deprioritise temperature as a sales driver** unless nonlinear or interaction effects are tested and shown to matter.
4. **Report the missing statistics.** Obtain group means, effect sizes, skewness, MAE/RMSE, and feature importances before the findings are used in a business decision.

### Future Analysis

**Modelling**
- Remove trend and weekly seasonality before modelling, or add lagged sales and time features. Compare against a seasonal naive baseline.
- Test SARIMAX or regression with ARIMA errors, using promo as an exogenous variable. These models handle non-stationarity more directly than tree ensembles.
- Use rolling-origin (walk-forward) validation to check whether performance is stable across periods.
- Test whether the promo effect is stable over time, and whether it varies with day of week.

**Statistical checks**
- Correct the correlation and group-test p-values for autocorrelation, for example with a Newey-West adjustment or block bootstrap.
- Test promo × day-of-week and promo × trend interactions.
- Test stationarity formally (ADF and KPSS) and quantify the trend.
- Check whether temperature has a threshold or nonlinear effect, for example using a spline or binned analysis.

**Data to collect**
- Confirmation of daily continuity and the exact date range.
- Promotion details: depth, duration, channel, and whether promotions were planned or reactive.
- Price, inventory, and competitor activity, which may explain the trend and level shifts.
- Holiday and calendar indicators, which would help with seasonality.
- Store or product identifiers, if the sales figures aggregate multiple units.