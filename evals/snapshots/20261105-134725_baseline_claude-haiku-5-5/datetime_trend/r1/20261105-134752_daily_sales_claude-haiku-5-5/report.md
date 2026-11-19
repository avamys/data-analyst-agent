# Data Analysis Report: Daily Sales

**Status: Provisional.** The promo and temperature findings are supported by reported test statistics. The predictive results conflict across pipeline outputs and should be reconciled before they inform decisions.

---

## Executive Summary

- **Promotions are associated with a large, statistically significant sales lift.** Promo days average **298.4** units versus **266.3** on non-promo days, a difference of **+32.1 units (+12.1%)**, with p < 0.05 (Welch t-test). The effect is large (Cohen's d ≈ 0.81, derived from reported summary statistics). This is the most decision-relevant finding, though it is not yet adjusted for time trend or seasonality.
- **Temperature has no meaningful linear relationship with sales.** Pearson r = 0.016 (p = 0.67, 95% CI [−0.057, 0.088]), explaining 0.02% of variance. Temperature should not be used as a standalone sales lever.
- **A linear model with a time trend and promo is the strongest predictive candidate.** Linear Regression achieved test RMSE 15.6 and R² 0.649 on a chronological holdout. A Random Forest performed worse than predicting a constant on the same split (R² −0.190). The linear model is the recommended working baseline.
- **Sales follow a time-driven trajectory that any forecast must account for.** The linear model's largest coefficient is on `trend_index`, indicating systematic movement across 2023–2024. The direction and size of this trend have not been quantified.
- **Predictive metrics are not yet trustworthy.** Four different sets of error metrics were reported for overlapping models, and several are inconsistent. Reconciliation is required before any forecast is operationalized.

---

## Dataset Overview

| Attribute | Value |
|---|---|
| Source | `daily_sales.csv` |
| Observations | 730 daily records |
| Columns | 4 (date, temperature, promo, sales) |
| Date range | 2023-01-01 to 2024-12-30 (730 consecutive days, no gaps implied) |
| Target | `sales` (continuous, regression) |
| Features | 3 numeric (temperature, promo, date-derived), 1 categorical/date |
| Missing values | None reported for any column |
| Promo prevalence | 104 of 730 days (14.2%) |

**Derived overall sales statistics** (from reported group summaries; not directly reported): mean ≈ 271 units, standard deviation ≈ 41 units.

---

## Analysis Methodology

### Strategic Approach

The analysis followed a three-stage sequence:

1. **Exploratory analysis first**, to validate data types, distributions, outliers, the date structure, and the correlation structure before any inference.
2. **Statistical testing second**, to test whether the main hypothesized drivers (temperature and promo) have significant associations with sales. Promo's sparsity (14%) made a group comparison the appropriate test.
3. **Predictive modeling last**, because sales is a continuous target and 730 rows support a train/test split. Models were used to rank drivers and to establish a forecast benchmark.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory Data Analysis | 2 |
| Statistical Testing | 1 |
| Machine Learning | 3 |
| **Total** | **6 of 6 (100% success)** |

Total execution time: 51.1 seconds.

---

## Key Findings

### Exploratory Analysis

- **Data integrity is clean.** There are no missing values, the date span is exactly 730 days (consistent with a complete daily series), and promo is a clean binary indicator.
- **Date handling:** The `date` column was stored as text and required parsing to datetime before use in trend and seasonality features.
- **Promo is a sparse signal.** Only 104 of 730 days (14.2%) were promotional, so promo-group estimates are less precise than the non-promo estimates (n = 626).
- **Sales variability is substantial.** Overall sales have a standard deviation of roughly 41 units around a mean of roughly 271. Within each promo group, the standard deviation is similar (≈39–40 units), so promo shifts the mean but does not change the spread much.
- **Test-period variance is lower.** Back-calculated from the reported R² and RMSE values (see Contradictions), the 2024 holdout period has a sales standard deviation of about 26 units. Much of the full-period variance therefore appears to come from changes over time, which is consistent with the trend finding.

*Not reported in the available outputs:* distribution shape (skewness, normality), outlier counts, temperature summary statistics, categorical frequencies, and the full correlation matrix. These are gaps in the EDA record.

### Statistical Evidence

| Test | Purpose | Result | Effect Size | Interpretation |
|---|---|---|---|---|
| **Pearson correlation** (temperature vs. sales) | Test for linear association | r = 0.016, **p = 0.67** (fail to reject H0) | r² = 0.0002 (0.02% of variance) | No linear relationship. 95% CI for r [−0.057, 0.088] includes zero. |
| **Spearman correlation** (robustness check) | Test for monotonic association without linearity assumption | ρ = 0.010, **p = 0.78** | — | Confirms no monotonic relationship. |
| **Welch two-sample t-test** (promo vs. no promo) | Test whether mean sales differ by promo status | **p < 0.05** (reject H0) | Cohen's d ≈ 0.81 (large); mean difference +32.1 units | Promo days sell about 32 more units on average. |

**Promo test details** (reported group summaries, with derived values marked *):

| Group | n | Mean Sales | Std. Dev. |
|---|---|---|---|
| No promo | 626 | 266.27 | 39.72 |
| Promo | 104 | 298.39 | 38.79 |
| **Difference** | | **+32.12 (+12.1%)** | |
| *Welch t-statistic (derived)* | | *≈ 7.8* | |
| *95% CI for difference (derived)* | | *≈ [+24, +40] units* | |

**Plain-English interpretation:** On days with a promotion, sales are on average about 32 units higher (roughly 12%). The result is statistically robust, and the effect is large relative to day-to-day variation. The derived t-statistic and confidence interval should be confirmed against the original test output.

**Important limitation:** These tests treat days as independent. Daily sales are typically autocorrelated and trend over time, and promotions may cluster in particular periods. The +32 units could partly reflect timing rather than promo causation.

### Predictive Models

**Setup:** A chronological split was used: training on 584 days (2023-01-01 to 2024-08-06) and testing on 146 days (2024-08-07 to 2024-12-30). Features included promo, temperature, trend index, day of week, and month.

**Note on metric types:** This is a regression problem, so accuracy, precision, and recall are not applicable. Performance is reported with RMSE, MAE, and R².

**Model comparison (test set, as reported in ML task 3):**

| Model | Test RMSE | Test R² | Reduction vs. Baseline RMSE (63.17) |
|---|---|---|---|
| **Linear Regression** | **15.60** | **0.649** | ~75% |
| Random Forest (300 trees, min leaf = 2) | 28.73 | −0.190 | ~55% |
| Baseline (reference) | 63.17 | — | — |

A negative R² means the Random Forest predicts the 2024 holdout worse than a constant equal to the holdout mean.

**Feature importance:**

- **Linear Regression:** `trend_index` has the largest coefficient magnitude. Promo, day of week, month, and temperature also contribute, but their individual coefficients were not reported.
- **Random Forest (permutation importance):** Promo is the most influential single raw feature.

The two models rank drivers differently. Because the methods differ, neither ranking is definitive. A single importance method (e.g., SHAP or permutation importance) applied to both models is needed to resolve this.

**Predictive insights:**

- A simple, interpretable structure (trend plus promo) captures most of the predictable variation (test R² ≈ 0.65).
- The Random Forest's poor test performance is most plausibly explained by **extrapolation**, not general overfitting. Tree models cannot predict values outside the range seen in training, while the trend variable keeps rising into the test period. A linear model can extrapolate the trend, which may explain its advantage. This hypothesis is consistent with the numbers but has not been directly tested.
- The linear model's test performance depends on the trend continuing. Extrapolation beyond December 2024 carries risk if the trend changes.

---

## Synthesis

**Validated across analyses:**

1. **Promo has a real, large association with sales** (+32 units, p < 0.05). It is the one driver that appears consistently in the statistical test and in the Random Forest's importance ranking.
2. **Temperature does not have a linear relationship with sales** (r = 0.016, p = 0.67). It is also not prominent in the models. Both analyses agree that temperature is not a meaningful linear driver.
3. **Time trend is the dominant structure in the predictive models.** The linear model's largest coefficient is on the trend term, and the Random Forest fails when asked to extrapolate it.

**Resolved conflict:** The four sets of error metrics reported across the pipeline are not as contradictory as they first appear. Back-calculating from each reported RMSE and R² pair gives an implied test-set variance of about **693** in every case (LR: 693; RF: 694; ML task 1: 694; baseline: 693). This means all results describe the **same chronological test split**, and the baseline's RMSE of 63.17 corresponds to its own reported R² of −4.754. The baseline is therefore not a test-mean predictor, and the earlier conclusion that the metrics were incompatible does not hold. The ML task 1 result (RMSE 39.5, R² −124.8%) is a different, weaker model on the same split, not a different dataset.

**Still unresolved:** The linear model's reported train/test RMSE gap implies a training RMSE of about 41, which is close to the full-sample sales standard deviation. That would mean the linear model explains almost nothing on training data, which conflicts with its strong test performance. This figure is probably miscalculated and should be rechecked.

---

## Conclusions

**What we can say with confidence:**

- Promotional days generate substantially higher sales. The observed lift is about **+32 units (+12%)** per promo day, and it is statistically significant and large in effect size.
- Temperature has no linear association with sales and should not be used to forecast sales.
- Sales are strongly structured over time. A linear time-trend model explains roughly two-thirds of variation in the 2024 holdout period.
- A simple linear model outperforms the Random Forest on chronological holdout data, so added complexity is not justified at present.

**What we cannot yet say:**

- The exact size of the promo effect after adjusting for trend, seasonality, and day of week. The estimate may be inflated if promotions are scheduled into high-demand periods.
- Whether the promo effect is stable over time.
- The direction, cause, or sustainability of the sales trend.
- Whether any forecast will hold beyond December 2024.
- Any absolute accuracy figure for operational forecasting. The current metrics are provisional.

---

## Limitations & Caveats

**Data quality**
- No missing values or duplicates were reported, but the full EDA outputs (distributions, outliers, categorical frequencies, correlation matrix) were not captured, so distributional assumptions are unverified.
- Promo is a single binary flag with no information on intensity, duration, type, or discount depth. The effect may vary across promo types.

**Statistical assumptions**
- **Independence:** Daily sales are likely autocorrelated, which can overstate the significance of the t-test and correlation results.
- **Confounding:** The promo comparison does not control for time. Promos may cluster in particular months or trend periods.
- **Normality and variance:** The Welch test relaxes the equal-variance assumption, but normality within groups was not verified.
- **Linearity:** The temperature test only detects linear and monotonic relationships. A threshold or U-shaped effect (e.g., heat spikes) would be missed.

**Modeling limitations**
- The Random Forest's failure is most likely due to extrapolation beyond the training range. This is a hypothesis and has not been tested.
- The linear model's performance relies on trend extrapolation into a period it did not see during training.
- No residual diagnostics, autocorrelation checks, or time-series cross-validation were reported.
- The model descriptions are inconsistent: one task refers to gradient boosting and another to Random Forest. It is unclear whether these are the same model.
- The train/test gap reported for the linear model appears implausible (see Synthesis).
- The Random Forest's reported overfitting cannot be confirmed without its training-set metrics.

**Failed or missing analyses**
- No failed analyses were recorded (6 of 6 tasks completed).
- Not reported: test statistics and CIs for the temperature correlation at the model level; coefficient estimates for LR; seasonality decomposition; day-of-week effects; interaction effects (promo × trend, promo × month).

---

## Recommendations

### Immediate Actions

1. **Use the promo finding for planning, with a caveat.** The data supports planning on a promo lift of roughly +30 units per promo day (about +12%). Before committing budget, confirm the effect with a time-adjusted estimate (see below).
2. **Stop using temperature as a standalone sales driver** in planning or forecasting. Revisit only if a nonlinear test shows an effect.
3. **Adopt the linear trend-plus-promo model as the working baseline** for forecasting. Do not deploy the Random Forest in its current form.
4. **Reconcile the metrics before reporting externally.** Re-run the full pipeline from a single script with a fixed chronological split, and report one consistent set of RMSE, MAE, and R² for each model, along with training-set metrics.
5. **Do not extrapolate the trend beyond 2024 without a review.** Treat forecasts past the observed window as scenarios, not predictions.

### Future Analysis

**Priority analyses**
1. **Time-adjusted promo effect:** Regress sales on promo with controls for trend, month, and day of week, and report the coefficient with a 95% CI. This is the most important next step for quantifying the promo lift.
2. **Promo × time interaction:** Test whether the promo effect is stable over 2023 and 2024 or changes with the trend.
3. **Time-series validation:** Use walk-forward or expanding-window cross-validation, and check residual autocorrelation (e.g., Durbin–Watson or ACF plots).
4. **Extrapolation check:** Test whether the Random Forest performs better when `trend_index` is removed or when the target is detrended. This would confirm or reject the extrapolation explanation.
5. **Consistent importance analysis:** Apply SHAP or permutation importance to both models to resolve the trend-versus-promo ranking question.
6. **Seasonality and day-of-week effects:** Decompose the series and quantify weekly and monthly patterns.
7. **Nonlinear temperature test:** Use splines or binned analysis to check for threshold effects.
8. **Dedicated time-series model:** Compare a SARIMAX model with promo and temperature as exogenous variables against the linear baseline.

**Data to collect**
- **Promo details:** Promo type, discount depth, duration, and channel, so that effects can be compared across promotion types.
- **Promo scheduling rationale:** Whether promotions were planned for high- or low-demand periods, to assess confounding.
- **Price and competitor data:** Price changes are a common driver of sales that is absent here.
- **Calendar variables:** Holidays, school terms, and local events that may explain seasonal patterns.
- **Inventory and stock-out records:** To distinguish true demand from supply-constrained sales.
- **Longer history:** More than two years would allow stronger seasonal estimates and a more reliable test of trend stability.