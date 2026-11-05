# Data Analysis Report: Daily_Sales

## Executive Summary

- **Promotions are the one validated driver of daily sales.** Promo days average **298.4** sales versus **266.3** on non-promo days, a lift of about **+32 units (+12%)**. This is statistically significant (p ≈ 2e-12), and both parametric and non-parametric tests agree. The lift is observational, so it should not yet be treated as causal.
- **Temperature has no detectable linear relationship with sales** (r = 0.016, p = 0.67). Temperature should not be used as a sales-planning lever on the basis of this data, though non-linear effects remain untested.
- **Day of week is the strongest predictor of daily variation**, and a persistent upward trend shapes the level of sales over the two-year window. Together, these make calendar structure and trend the main forecastable components.
- **Predictive performance is unreliable at present.** The primary Random Forest overfits badly (train R² = 0.94, test R² = −0.11) and does not beat a simple persistence baseline by a meaningful margin (MAE 23.1 vs. 26.3). A linear model with a trend term performed much better (RMSE 15.6, R² = 0.65), but this result comes from a single split and has not been replicated.
- **Decision implication:** Promotion planning can use the observed lift as a working estimate. Forecasting should not be deployed until the model results are reconciled and validated with time-series cross-validation.

---

## Dataset Overview

| Attribute | Value |
|---|---|
| Source | `/workspaces/agents/evals/data/daily_sales.csv` |
| Rows × columns | 730 × 4 |
| Target | `sales` (continuous, regression) |
| Features | `temperature` (numeric), `promo` (binary, numeric-coded), `date` (parsed to datetime; used as a time index) |
| Date range | 2023-01-01 to 2024-12-30 (730 consecutive days; 2024-12-31 absent) |
| Missing values | None (0 in `sales` and `promo`; 0 unparseable dates) |
| Promo days | 104 (14.2%) vs. 626 non-promo (85.8%) |

The dataset is a complete daily series covering two years. Its key structural features are the promotion flag, which is imbalanced, and a time index that carries both weekly structure and a trend.

---

## Analysis Methodology

### Strategic Approach

Analysis followed a sequenced strategy: **exploratory → statistical → predictive**.

- **Exploratory first:** To inspect distributions, outliers, promo frequency, and time structure (continuity, trend, seasonality) before any modeling. The date column was parsed from text to datetime so that temporal features could be engineered and a time-respecting split could be used.
- **Statistical second:** To test whether the apparent relationships (temperature–sales, promo–sales) are significant, using correlation tests and two-group comparisons with robustness checks.
- **Predictive last:** Because sales is continuous and 730 rows is adequate for a train/test split, regression models were trained with a time-based split. Scalers and encoders were fit only on training data. Models included a Random Forest, a Ridge regression with a trend term, and naive baselines (mean and persistence).

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory Data Analysis | 2 |
| Statistical Testing | 2 |
| Machine Learning | 2 |
| **Total** | **6 of 6 (100% success, 0 failures)** |

Total execution time was 21.5 seconds.

---

## Key Findings

### Exploratory Analysis

**Sales distribution.** Sales are close to symmetric. Within-group skewness is minimal (0.08 for non-promo, 0.12 for promo). Shapiro–Wilk tests flag departures from normality (W = 0.993, p = 0.002 overall), but at n = 730 these tests are sensitive to trivial deviations, and the W statistic itself indicates a near-normal shape.

**Promo frequency.** Promotions are infrequent: 104 of 730 days (14.2%). This is enough to estimate a group difference with reasonable precision, but it limits the stability of any promo interaction analysis.

**Group descriptives by promo flag:**

| Group | n | Mean | Median | SD | Skew |
|---|---|---|---|---|---|
| No promo (0) | 626 | 266.3 | 266.4 | 39.7 | 0.08 |
| Promo (1) | 104 | 298.4 | 295.4 | 38.8 | 0.12 |

Variance is similar across groups (Levene's test W = 0.64, p = 0.42), so the groups can be compared on a shared-variance basis.

**Temporal structure.**
- **Weekly seasonality:** Clear weekday patterns are visible, and the autocorrelation structure is consistent with a 7-day cycle.
- **Annual pattern:** A high autocorrelation at lag 365 was observed. With only two years of data, this rests on roughly one full cycle and should be treated as suggestive, not established.
- **Trend:** The predictive results (see below) imply a sustained upward movement in sales across the window.

**Temperature.** Temperature is approximately normal, with a range that includes sub-zero values (e.g., −3.4 on 2023-01-03). It shows no visible relationship with sales in the exploratory summaries.

### Statistical Evidence

| Test | Purpose | Statistic | p-value | Significance (α = 0.05) | Effect size / CI |
|---|---|---|---|---|---|
| Pearson correlation: temperature vs. sales | Test linear association | r = 0.016 | 0.67 | Not significant | 95% CI [−0.057, 0.088] |
| Spearman correlation: temperature vs. sales | Rank-based association | — | 0.78 | Not significant | Not reported |
| Pearson correlation: promo vs. sales | Test linear association | r ≈ 0.25 (back-calculated) | 2.06e-12 | Significant | Not reported directly |
| Welch t-test: sales by promo | Compare group means | Mean difference +32.1 | Reported < 0.05 | Significant | See derived values below |
| Mann–Whitney U: sales by promo | Compare distributions (robustness) | — | Reported < 0.05 | Significant | Not reported |

**Plain-English interpretation:**

- **Temperature and sales: no relationship.** The correlation is 0.016, which explains effectively zero variance (r² ≈ 0.0003). The confidence interval includes zero and is narrow, so a meaningful linear effect is ruled out. Non-linear effects (such as a heat threshold) were not tested.

- **Promo and sales: a real, moderate association.** Promo days sell about **32 units more per day (+12%)** than non-promo days. Using the reported descriptives, I estimate Cohen's d ≈ 0.8 (a large effect in standardized terms) and a point-biserial r ≈ 0.27, consistent with the p-value. An approximate 95% CI for the mean difference is **[24, 40] units**. These are my calculations from the reported group statistics and should be confirmed against the reported test output.

- **Robustness:** Both the Welch t-test (mean comparison) and Mann–Whitney U (distribution comparison) reject equality. Because the group distributions are nearly symmetric, the two tests agree for the expected reason, which strengthens confidence in the finding.

- **Caveat on p-values:** Daily sales are autocorrelated and the series is trending. The standard tests assume independent observations, so their p-values are likely overstated. The promo effect is probably real in direction, but its significance level should be confirmed with autocorrelation-robust inference (see Limitations).

### Predictive Models

**Models tested:**
- Random Forest regressor (two runs, ml_1 and ml_2, with different reported specifications)
- Ridge regression with a trend term (reported in ml_1 only)
- Naive baselines: mean and persistence

**Evaluation metrics on the held-out test period:**

| Model | RMSE | MAE | R² | Notes |
|---|---|---|---|---|
| Ridge with trend | **15.59** | not reported | **0.650** | Best performer; single split only |
| Random Forest (ml_1) | 26.25 | not reported | ≈ 0.006 | 58% RMSE reduction vs. mean baseline |
| Random Forest (ml_2) | 27.69 | 23.12 | −0.106 | Train R² = 0.941 (heavy overfitting) |
| Persistence baseline | not reported | 26.32 | not reported | RF MAE is ~12% lower |
| Mean baseline | 63.17 | ~57.5 (implied) | −4.754 | Naive benchmark |

*Note on metrics: This is a regression task, so accuracy, precision, and recall do not apply. RMSE, MAE, and R² are the relevant measures. Values marked "implied" were back-calculated from other reported figures.*

**Feature importance:**
- **day_of_week** is the most influential feature by permutation importance. Weekday effects are the main variation the Random Forest captures.
- **trend_index** is the only feature capturing growth over time. Its importance was not reported, but it is central to the Ridge model's advantage.
- **promo** and **temperature** importances were not reported. This is a gap, since promo is the strongest statistically validated driver.

**Predictive insights:**
- **The test period sits well above the training distribution.** Working back from the mean baseline's reported R² (−4.75) and RMSE (63.2), the test-period mean is roughly 57 units away from the training mean. Tree models cannot extrapolate beyond the range seen in training, which likely explains their poor test performance. A linear trend model can extrapolate and does not share this limitation.
- **The Random Forest's test-period R² is near zero for both runs**, meaning it predicts no better than the test-period average once that average is known. Its advantage over the mean baseline comes mainly from avoiding the level shift.
- **Model reconciliation:** The two Random Forest R² values are internally consistent (both imply a test variance of about 693, or SD ≈ 26.3). The real discrepancy is the RMSE difference (26.25 vs. 27.69), which points to different specifications or splits.

---

## Synthesis

**Validated findings (consistent across analyses):**

| # | Finding | Evidence | Confidence |
|---|---|---|---|
| 1 | Promo days have higher sales (+32 units, +12%) | Correlation p ≈ 2e-12; Welch and Mann–Whitney both significant | **High** on direction; moderate on magnitude (observational, autocorrelation not yet adjusted) |
| 2 | Temperature has no linear relationship with sales | r = 0.016, p = 0.67 (Pearson); p = 0.78 (Spearman) | **High** for linear effects |
| 3 | Weekly cycle is the dominant short-term pattern | EDA autocorrelation; RF permutation importance ranks day_of_week first | **Moderate** (descriptive, not formally tested) |
| 4 | Sales trend upward over the window | Ridge advantage; test-period level shift | **Moderate** (single split, no formal trend test) |
| 5 | Annual seasonality | High ACF at lag 365 | **Low** (only ~2 cycles) |

**Where the analyses interact:**
- **Trend and weekday structure** jointly appear to drive predictive performance. Models that handle trend extrapolation outperform those that do not.
- **Promo and calendar structure may be confounded.** If promotions cluster on particular weekdays or periods, part of the promo lift reflects timing rather than the promotion itself. This has not been tested.
- **Temperature does not appear to confound the promo effect**, since it has no association with sales in any analysis.

**Unexplored interactions:** Promo × day of week and promo × trend are plausible but untested.

---

## Conclusions

**What we can say with confidence:**
1. Promotions are associated with substantially higher daily sales: about 32 units, or 12%, above non-promo days. The direction of this effect is robust across tests.
2. Temperature is not a linear driver of sales in this dataset.
3. Sales follow a weekly cycle, and the level of sales changes over the two-year window.

**What we can say with moderate confidence:**
4. The promo lift is large enough to matter for planning, but its precise size depends on adjustment for trend and weekday, which has not been done.
5. A trend-aware linear model is likely a better forecasting starting point than a tree-based model on this data, but this has not been confirmed.

**What we cannot yet say:**
6. Whether the promo effect is causal, or whether it varies by weekday or over time.
7. Whether an annual seasonal pattern exists.
8. Which Random Forest specification is correct, or whether Ridge's advantage holds across multiple time windows.
9. How accurately the model will forecast beyond a single held-out window.

---

## Limitations & Caveats

**Data quality**
- The series is complete over 730 consecutive days. The final day (2024-12-31) is absent from the range, which should be confirmed as intentional.
- Promo days are scarce (104 observations), which limits precision for interaction analysis and for any seasonal breakdown of the promo effect.
- Two years of data supports at most two annual cycles, which is insufficient for a reliable yearly seasonality estimate.

**Statistical assumptions**
- **Independence:** Daily sales are autocorrelated. The t-test, Mann–Whitney, and correlation p-values assume independence, so they are likely overstated.
- **Stationarity:** The series trends upward. Correlation and group tests on non-stationary data can produce spurious significance. The promo finding should be re-checked after detrending.
- **Skew reporting conflict:** The statistical analysis justified the Mann–Whitney test by skew, but the reported group skewness (0.08 and 0.12) is negligible and the EDA describes the distribution as roughly symmetric. The Mann–Whitney result is still valid as a robustness check, but the stated rationale should be corrected.
- **Test reporting inconsistency:** The Pearson output reports p = 0.67 for temperature, while the summary cites p = 0.78 (presumably the Spearman result). The stated primary method was Spearman, but the printed output was Pearson. Both results agree on the conclusion.

**Missing information**
- Exact p-values and confidence intervals for the Welch and Mann–Whitney tests, and the promo mean-difference CI as reported by the test itself.
- Cohen's d and point-biserial r as reported (the values here are derived).
- Ridge MAE, and RMSE/MAE for the naive baselines in full.
- Train/test split definition (cutoff date and sizes).
- Feature importance for trend_index, promo, and temperature.
- Hyperparameters, residual diagnostics, and multicollinearity checks.

**Modeling limitations**
- All performance figures come from a single time split. There is no time-series cross-validation.
- The two Random Forest runs report different RMSE values (26.25 and 27.69) under different, undocumented specifications.
- The Ridge result (R² = 0.65) comes from one run and has not been replicated. The gap between Ridge and Random Forest is large enough to warrant verification.
- The Random Forest cannot extrapolate beyond the training range, so its test performance is structurally limited if the level keeps shifting.

**Failed analyses:** None. All six tasks completed successfully.

---

## Recommendations

### Immediate Actions

1. **Use the promo lift as a working planning estimate, with appropriate caveats.** Promo days averaged about 32 units (12%) more in sales. Use this to set expectations for promotional campaigns, but present it as an observational association until it is confirmed.
2. **Do not deploy the Random Forest for forecasting.** Its test R² is near zero and it overfits heavily. Stop using it as the production candidate until the discrepancy between ml_1 and ml_2 is resolved.
3. **Stop treating temperature as a sales driver** for planning purposes, based on current evidence.
4. **Reconcile the model results before any forecast is communicated.** Confirm the train/test split, rerun the Ridge model with time-series cross-validation, and report MAE alongside RMSE and R².
5. **Correct the reporting gaps.** Document the exact test p-values, confidence intervals, and skewness figures, and fix the Pearson/Spearman labeling.

### Future Analysis

**Priority analyses**
- **Promo effect, adjusted:** Estimate the promo effect with a regression that includes trend and day-of-week terms, using HAC/Newey–West standard errors to account for autocorrelation. This is the most important next step.
- **Promo timing:** Check whether promotions are scheduled on specific weekdays or periods. If so, quantify how much of the lift is confounded with calendar structure.
- **Interactions:** Test promo × day of week and promo × trend. Also check whether the promo effect persists into adjacent days (carryover) or decays.
- **Stationarity and trend:** Run formal ADF/KPSS tests and quantify the trend. Repeat the promo analysis on detrended data.
- **Model validation:** Use expanding-window time-series cross-validation. Report MAE, RMSE, and R² for every model, including Ridge, persistence, and the mean baseline.
- **Forecast horizon:** Measure how accuracy degrades over multi-day and multi-week horizons.
- **Non-linear temperature effects:** Test for heat or cold thresholds, using splines or binned temperature, since a linear null does not rule out threshold effects.

**Data to collect**
- **Price and promotion details:** Promotion depth (discount level), duration, and channel. The current binary flag cannot distinguish a small promotion from a large one.
- **Holiday and event calendars:** To test for annual and holiday-driven patterns, which two years of data cannot establish.
- **Longer history:** At least three to four years would allow a credible estimate of yearly seasonality.
- **Trend drivers:** Customer counts, pricing changes, store or channel changes, and marketing spend, to explain the upward trend.
- **Lagged and rolling features:** Previous-day and rolling-average sales, to test whether they improve forecasts beyond calendar and trend features.