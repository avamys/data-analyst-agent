# Data Analysis Report: Daily Sales

## Executive Summary

- **Promotions are associated with a large, robust sales lift.** Promo days average 298.4 units versus 266.3 on non-promo days, a difference of +32.1 units (+12.1%). The effect is significant under Welch's t-test (t = 7.79, p < 0.05) and the Mann-Whitney U test, with a large standardized effect (Cohen's d ≈ 0.81). The estimated 95% CI is roughly +24 to +40 units. Because promotion assignment was not randomized, this is an association and not yet a proven causal effect.
- **Temperature shows no detectable relationship with sales.** Pearson and Spearman correlations are non-significant under naive, autocorrelation-adjusted, and permutation-based tests (all p > 0.6). Temperature should not be used as a sales driver in planning based on this data.
- **The current forecasting model is not ready for operational use.** On the held-out test period, it beats a naive lag-1 forecast on RMSE (29.06 vs. 33.05, about 12% better), but its R² is −0.217, meaning it predicts worse than simply using the test-period mean.
- **Performance is unstable across time.** Cross-validated R² averages 0.27, but held-out R² is −0.22. The reported mean-baseline RMSE also implies a level shift of roughly 57 units between training and test data. This must be diagnosed before any forecast or trend claim is trusted.
- **Decisions supported now:** Use the promo lift as a directional planning estimate and validate it with a controlled test (for example, a randomized holdout of promotions). Do not deploy the forecaster for inventory or staffing decisions. Investigate the test-period shift first.

## Dataset Overview

| Attribute | Value |
|---|---|
| Source | `/workspaces/agents/evals/data/daily_sales.csv` |
| Rows × columns | 730 × 4 |
| Date range | 2023-01-01 to 2024-12-30 |
| Target variable | `sales` (continuous, regression) |
| Numeric features | `temperature` (float), `promo` (binary integer, 0/1), `sales` |
| Categorical features | `date` (stored as string; parsed to derive temporal features) |
| Missing values | None in any column |
| Promo distribution | 626 non-promo days (85.8%), 104 promo days (14.2%) |

The date range runs from 2023-01-01 to 2024-12-30, which spans exactly 730 calendar days. This is consistent with a complete daily series with no gaps or duplicates, although the EDA output did not explicitly confirm this.

The dataset is small and covers two years of daily observations. This is enough for a chronological train/test split and time-series cross-validation, but not enough to estimate seasonal effects with high precision, since each season appears only twice.

## Analysis Methodology

### Strategic Approach

Analysis proceeded in three stages, in priority order:

1. **Exploratory analysis (first):** Confirm data integrity, parse dates, examine distributions and promo frequencies, and check the time structure. Random splits can leak temporal information in daily series, so date handling had to be correct before modeling.
2. **Statistical testing (second):** Test whether promotions shift sales, using parametric and nonparametric tests with effect sizes. Quantify the temperature–sales relationship while accounting for autocorrelation, since daily observations are not independent.
3. **Predictive modeling (last):** Build regression models with a chronological split and time-series cross-validation, using only lagged information to avoid look-ahead leakage. Feature importance was used to see whether promo and temperature matter in a predictive setting.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory data analysis | 2 |
| Statistical analysis | 2 |
| Machine learning | 2 |
| **Total** | **6 of 6 (100% success, 0 failures)** |

Total execution time was 50.5 seconds.

## Key Findings

### Exploratory Analysis

**Data integrity**
- The dataset has 730 rows and 4 columns with no missing values in any field.
- The date column is stored as text and was parsed into datetime for temporal analysis.
- The date range is consistent with 730 contiguous days.

**Sales distribution**
- Non-promo days (n = 626): mean 266.3, median 266.4, SD 39.7.
- Promo days (n = 104): mean 298.4, median 295.4, SD 38.8.
- The two groups have nearly identical spread, and the median and mean are close within each group, which indicates no strong skew in either.
- Shapiro-Wilk on non-promo days gave W = 0.991 (p = 0.001). With n = 626, even small departures from normality are detectable. The magnitude is small (skew 0.08, excess kurtosis −0.59), so the normality violation is practically minor.
- Promo days: W = 0.990 (p = 0.67), consistent with normality.

**Variance**
- Levene's test (median-centered): W = 0.64, p = 0.42. The two groups have comparable variability, which supports the standard t-test assumptions.

**Promo balance**
- Promo days make up 14.2% of observations (104 of 730). This is a minority class but is large enough for reliable two-group comparison.

**Temperature**
- The first rows show winter values (−3.4°C to 5.4°C), consistent with a January start date.
- Full temperature distribution statistics (mean, SD, skewness, outlier counts) were not included in the EDA output and are therefore not reported here.

**Temporal structure**
- No long-run drift was reported by the EDA. However, the predictive results (see below) indicate a possible level shift in the test period, which the EDA did not check directly. The "no drift" conclusion should be treated as provisional.

### Statistical Evidence

#### Test 1: Promo effect on mean sales (Welch's two-sample t-test)
- **Purpose:** Determine whether mean sales differ between promo and non-promo days, without assuming equal variances.
- **Result:** t = 7.79, df = 141.3, p < 0.05. **Reject H0.**
- **Effect size:** Raw difference +32.1 units (+12.1% over the non-promo mean). Pooled SD ≈ 39.6, so Cohen's d ≈ 0.81, a large effect.
- **Confidence interval:** Approximately +24 to +40 units (derived from the summary statistics; confirm against the raw test output).
- **Interpretation:** Promo days sell about 32 more units on average, and the difference is far larger than day-to-day noise.

#### Test 2: Promo effect on sales distribution (Mann-Whitney U)
- **Purpose:** Confirm the promo effect without relying on normality, given the Shapiro-Wilk result for non-promo days.
- **Result:** Significant at p < 0.05. **Reject H0.** (Reported in the synthesis; the raw output is not included in the detailed findings.)
- **Interpretation:** The promo effect holds for the sales distribution as a whole, not only for the mean.

#### Test 3: Equal variance assumption (Levene's test)
- **Result:** W = 0.64, p = 0.42. No evidence of unequal variances.
- **Interpretation:** The standard assumptions for the t-test are reasonable.

#### Test 4: Temperature–sales correlation (Pearson and Spearman)
Results below are from the synthesis; the detailed naive-correlation output was truncated before the coefficient values.

| Test | Method | p-value | Conclusion |
|---|---|---|---|
| Pearson, naive | Assumes independent observations | 0.671 | Not significant |
| Spearman, naive | Assumes independent observations | 0.781 | Not significant |
| Pearson, autocorrelation-adjusted | Accounts for serial dependence | 0.819 | Not significant |
| Spearman, autocorrelation-adjusted | Accounts for serial dependence | 0.881 | Not significant |
| Circular-shift permutation | Preserves time structure in null distribution | 0.960 | Not significant |

- **Interpretation:** Temperature is not linearly or monotonically related to sales, and this holds under methods that account for the time structure. The naive p-values were the least conservative, and the adjusted tests were consistent with them, so the conclusion does not depend on the choice of test.
- **Coefficient magnitudes:** Not reported, so the size of any relationship can only be bounded as "not detectable at this sample size."

### Predictive Models

Results below are from the synthesis report. The detailed model outputs (hyperparameters, fold-level scores, full importance tables) were not included in the materials provided.

**Model types and validation**
- Model families used: lag- and rolling-window regression models (specific algorithms not named in the materials), plus a naive lag-1 baseline and a mean baseline.
- Validation: chronological train/test split and TimeSeriesSplit cross-validation. Lag features were built only from past observations.
- Note on metrics: This is a regression task, so classification metrics (accuracy, precision, recall) do not apply. Regression metrics are reported below.

**Performance**

| Model / Baseline | Test RMSE | Test R² | Notes |
|---|---|---|---|
| Best model | 29.06 | −0.217 | Worse than predicting the test mean |
| Naive lag-1 | 33.05 | — | Persistence forecast |
| Mean baseline | 62.72 | — | Implausibly high; see Contradictions |
| Best model, time-series CV | — | 0.269 (mean) | Fold-level variation not reported |

- The best model improves on naive persistence by about 12% on RMSE, which is a real but modest gain.
- The negative test R² means the model's errors on the test period are larger than the test-period variance. The model captures some short-term structure but does not generalize reliably to the held-out period.

**Feature importance (as reported)**
- `is_weekend` ranks first.
- Lag and rolling-window features dominate overall importance, which indicates that recent sales history and day-of-week cycles are the main predictive signals.
- Promo and temperature were described as contributing "meaningfully," but no importance values were reported for either. This claim cannot be verified (see Contradictions).

**Predictive insights**
- Short-term persistence and weekly rhythm are the most useful predictive signals.
- The model does not reliably forecast beyond the training regime, so its forecasts should be treated as a baseline, not a production forecaster.

## Synthesis

### Validated Hypotheses

| # | Hypothesis | Test | Result | Status |
|---|---|---|---|---|
| H1 | Promo changes mean sales | Welch t-test | t = 7.79, p < 0.05 | **Supported** |
| H2 | Promo shifts the sales distribution | Mann-Whitney U | p < 0.05 | **Supported** |
| H3 | Promo and non-promo variances differ | Levene's test | p = 0.42 | Not supported; equal-variance assumption reasonable |
| H4 | Temperature linearly predicts sales | Pearson (naive) | p = 0.671 | Not supported |
| H5 | Temperature monotonically predicts sales | Spearman (naive) | p = 0.781 | Not supported |
| H6 | Temperature effect survives autocorrelation adjustment | Adjusted Pearson / Spearman | p = 0.819 / 0.881 | Not supported |
| H7 | Temperature effect exceeds chance under time-structure null | Circular-shift permutation | p = 0.960 | Not supported |

### Consistent Patterns

1. **Promo is the clearest sales driver in the data.** It is significant under parametric and nonparametric tests and has a large effect size. This is the most robust finding.
2. **Temperature has no detectable bivariate relationship with sales.** Four independent tests agree.
3. **Recent history and weekly cycles carry predictive signal.** Lag features and `is_weekend` rank highest in the model.
4. **Predictive skill is modest and unstable.** Gains over naive persistence are small, and cross-validated and held-out performance disagree sharply.

### Cross-Cutting Insight

Sales appear to follow a combination of recent level, weekly rhythm, and promotional lift. Temperature plays no clear role in the bivariate analysis. The unresolved question is whether the test period differs structurally from earlier data, since that would affect both the promo estimate and the forecasts.

## Conclusions

**What we can say with confidence**

1. Promo days sell substantially more than non-promo days. The average difference is about +32 units (+12%), with a 95% CI of roughly +24 to +40 units, and this result holds under both parametric and nonparametric tests.
2. Temperature does not meaningfully predict daily sales in this dataset. This conclusion holds across naive, autocorrelation-adjusted, and permutation-based tests.
3. The data is structurally clean: 730 rows, no missing values, a contiguous two-year daily series, and no promo class-balance problem for the comparison.
4. The current forecasting model is not reliable enough for operational decisions. Its test R² is negative.

**What we cannot yet conclude**

1. Whether the promo effect is causal. Promotions were not randomly assigned, and they may be targeted at particular days or periods.
2. Whether the promo effect is stable over time. The test period appears to differ from training data.
3. Whether temperature matters in a nonlinear or interaction-based way. The model's claim that temperature contributes "meaningfully" conflicts with the bivariate null result and is unverified.
4. Whether the sales series has a stable level. The mean-baseline results suggest a shift that the EDA did not detect.

## Limitations & Caveats

### Data Quality Issues
- **Incomplete EDA outputs:** Full distribution statistics (skewness, outlier counts, temperature summary) and explicit duplicate and gap checks were not reported. The "no missing values" result is verified, but the other integrity checks are not.
- **Missing test statistics:** The exact t-test confidence interval, Shapiro-Wilk results for the full sample, and the Mann-Whitney raw output were not included in the detailed findings. Figures marked as derived should be confirmed.
- **Missing correlation coefficients:** Pearson and Spearman r values and their CIs were not reported, so the magnitude of any temperature relationship cannot be bounded.

### Statistical Assumptions and Limitations
- **Independence:** Daily sales are serially dependent. The naive t-test and correlation p-values assume independence, which may overstate significance. The promo test should be re-checked with a time-aware method, such as a regression with autocorrelation-robust errors, before the result is used in a formal decision.
- **Non-normality:** Non-promo sales show a statistically significant departure from normality, but the departure is small in magnitude. The Mann-Whitney result addresses this.
- **Observational design:** The promo effect is confounded with any factors that drive promotion scheduling. If promotions cluster on weekends, in certain seasons, or during higher-demand periods, the estimate may overstate the true lift.
- **Small effective sample for seasonality:** Two years of data provide only two observations of each season, which limits seasonal inference.

### Metric Consistency Concern
The reported test metrics are internally inconsistent in a way that needs checking:
- Test RMSE 29.06 with R² = −0.217 implies a test-period variance of about 694 (SD ≈ 26).
- A mean-baseline RMSE of 62.72 can only be reached with that variance if the training mean differs from the test mean by about 57 units.
- Sales means across the rest of the data sit between roughly 266 and 298, so a 57-unit offset would be a large level shift. The EDA did not detect this.
- Either the test period contains a genuine level shift, or one of the baseline definitions differs from what the report assumes. Both possibilities must be resolved before relying on the predictive results.

### Failed or Incomplete Analyses
- No analysis failed outright (6 of 6 tasks completed).
- Several analyses were incomplete in their reported outputs: fold-level CV results, feature-importance values for promo and temperature, model hyperparameters, and residual diagnostics.

### Missing Information
- Promotion assignment process (how and why promotions were scheduled)
- Adjusted regression of sales on promo, weekend, and temperature together
- Promo × weekend and promo × temperature interaction tests
- Change-point or structural-break analysis
- Test-period versus training-period summary statistics

## Recommendations

### Immediate Actions

1. **Use the promo lift as a directional planning estimate, not a precise forecast.** A planning assumption of roughly +30 units (about +12%) on promo days is supported by the data. Treat it as an association until causal evidence is available.
2. **Validate the promo effect experimentally.** Randomize promotions across comparable days or stores for a defined period, and compare outcomes against a control. This directly tests causality and would clarify whether the lift is stable.
3. **Do not deploy the current forecasting model** for inventory, staffing, or revenue planning. Its test R² is negative, so it adds no reliable value over the test-period mean.
4. **Do not use temperature as a sales driver** in planning or pricing decisions based on this dataset. Revisit only if new data or a nonlinear analysis shows a relationship.
5. **Verify the baseline calculations** before reporting any model performance. Confirm how the mean baseline and R² are computed, and whether the test period has a level shift.

### Future Analysis

**Immediate analytical follow-ups (short term)**
1. Re-run the EDA with full outputs: distribution statistics, outlier counts, explicit duplicate and gap checks, and temperature summaries.
2. Run a change-point analysis on the sales series to identify any level shift and its timing.
3. Fit an adjusted regression of sales on `promo`, `is_weekend`, and `temperature` together, with autocorrelation-robust standard errors.
4. Test promo × weekend and promo × temperature interactions to see whether the promo effect varies by context.
5. Check whether promotions cluster on particular weekdays, months, or temperature ranges. Clustering would confound the promo estimate.

**Modeling follow-ups (medium term)**
6. Try models with explicit trend and seasonality handling, such as SARIMAX or gradient boosting with calendar features (day of week, month, holiday indicators). Compare them against the persistence baseline.
7. Report fold-level CV results and residual diagnostics, and check whether errors are concentrated in particular periods.
8. Evaluate forecasts with a rolling-origin backtest over multiple windows, rather than a single test split, to assess stability.

**Data to collect**
- **Promotion details:** Start and end dates, discount depth, channel, and the rule or reason for each promotion. This is needed to separate promo effects from scheduling effects.
- **Randomized or quasi-experimental promotion data:** Holdout groups or staggered rollouts would provide causal estimates.
- **Additional drivers:** Price changes, competitor activity, marketing spend, inventory availability, store or channel identifiers, and public holidays.
- **Weather detail:** If temperature is retained as a candidate driver, collect precipitation and humidity as well, since temperature alone may be a weak proxy.
- **Longer history:** More than two years would allow stronger seasonal estimates and better evaluation of structural change.