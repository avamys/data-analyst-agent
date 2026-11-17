# Data Analysis Report: Lakeside Hotel Stays

**Scope note:** This report reflects only the outputs that were actually returned. Several results referenced in the synthesis (p-values, Cramér's V, the correlation matrix, class counts, feature importances, and per-model metrics) do not appear in the raw specialist outputs. Where a figure comes only from the synthesis, this report labels it as *reported in synthesis, not verified*. Where a figure is missing, the report says so and does not estimate it.

---

## Executive Summary

- **The available features do not predict hotel stay rating.** The best model reached 22.22% test accuracy, below the 23.89% majority-class baseline. Accuracy is not the right yardstick for an imbalanced multiclass target, but the balanced metrics also show weak performance, so the conclusion holds.
- **No statistically supported link was found between booking channel or room type and stay rating.** The chi-square results were reported as non-significant, but the p-values and effect sizes were not included in the outputs, so the strength of this null cannot be quantified.
- **The data is clean and structurally ready.** All 900 rows and all 7 columns have zero missing values, which means the data-quality problems lie in what the data measures, not in completeness.
- **Do not deploy a rating-prediction model or use these features to target booking-channel or room-type decisions.** Doing so would rely on signal that the evidence does not show.
- **The most valuable next step is better data, not more modeling.** Guest-experience variables (reviews, service incidents, amenities, stay-specific factors) are the most likely source of rating variation. Before further modeling, the team should also confirm the class distribution and fix the reporting gaps noted below.

---

## Dataset Overview

| Attribute | Value |
|---|---|
| Source file | `lakeside_hotel_stays.csv` |
| Rows × columns | 900 × 7 |
| Target variable | `stay_rating` (integer, treated as multiclass) |
| Categorical features | `booking_channel`, `room_type` (2) |
| Numeric features | `nights`, `guests`, `lead_time_days`, `nightly_rate_eur` (4) |
| Missing values | 0 in all 7 columns (verified) |

The EDA profile describes "5 numeric features." This count includes the target, `stay_rating`, which is stored as an integer. The true feature count is 4 numeric plus 2 categorical. The modeling used the correct count.

---

## Analysis Methodology

### Strategic Approach

The analysis used three strategies in priority order:

1. **Exploratory analysis first.** The goal was to establish the target's class distribution, the shape of the numeric features, and how categorical levels are distributed. This step decides how the later steps should be run. For example, imbalance affects the choice of metrics, and skew affects the choice of tests.
2. **Statistical testing second.** Chi-square tests were planned for the categorical features, and ANOVA or Kruskal-Wallis tests for the numeric features, to check whether any feature differs across rating classes.
3. **Predictive modeling last.** The plan called for stratified splitting, class weighting, and macro-averaged metrics, with feature importances cross-checked against the statistical results.

The sequence was chosen so that modeling would be informed by the diagnostic and statistical findings rather than run blindly.

### Execution

| Specialist | Tasks completed |
|---|---|
| Exploratory data analysis | 3 |
| Statistical analysis | 1 |
| Machine learning | 2 |
| **Total** | **6 of 6 (100% completion, 0 failures)** |

Total execution time was 124.0 seconds.

Completion counts measure whether tasks ran, not whether their outputs are complete. Several planned outputs are missing, as detailed below.

---

## Key Findings

### Exploratory Analysis

**Data integrity**
- Zero missing values in all seven columns. Each column is typed as expected (two text categoricals, four numeric features, one integer target).

**Numeric feature distributions (verified from output)**

| Feature | Mean | Median | Skewness | Shape |
|---|---|---|---|---|
| `nights` | 5.57 | 6.00 | 0.00 | Symmetric |
| `guests` | 2.46 | 2.00 | 0.04 | Symmetric |
| `lead_time_days` | 39.77 | 34.00 | 1.34 | Right-skewed |
| `nightly_rate_eur` | 126.86 | 113.86 | 1.32 | Right-skewed |

- **Booking lead time and nightly rate are right-skewed.** Their means sit above their medians by 5.77 days and €13.00, respectively. A small number of long-lead or high-rate bookings pull the averages up. Median values are a more representative summary for these two features.
- **Nights and guests are symmetric.** Their means and medians nearly coincide, so no transformation is needed for them.
- The EDA output notes an "outlier- or nonlinearity-driven association," but it gives no statistic or direction. This observation cannot be interpreted and should be treated as unverified.

**Not reported**
- Class counts for `stay_rating`. The output does not show how many ratings fall in each class, so the imbalance cannot be quantified. The synthesis describes the majority class as roughly 24% of observations (consistent with the 23.89% baseline) and flags ratings 3, 4, and 10 as rare, but these are not verified counts.
- The correlation matrix among the numeric features. The requested matrix was not included, so relationships among `nights`, `guests`, `lead_time_days`, and `nightly_rate_eur` are unknown.
- Frequency counts and cross-tabulations for `booking_channel` and `room_type`, and Cramér's V effect sizes for them.

### Statistical Evidence

The statistical task was planned to cover the following tests, but its raw output contains only the missing-value check and no test results.

| Test | Purpose | Test statistic | p-value | Effect size | Status |
|---|---|---|---|---|---|
| Chi-square: `booking_channel` vs. `stay_rating` | Is channel associated with rating? | Not reported | Not reported | Not reported (Cramér's V not computed) | Reported as "fail to reject H0" in synthesis; not verified |
| Chi-square: `room_type` vs. `stay_rating` | Is room type associated with rating? | Not reported | Not reported | Not reported | Reported as "fail to reject H0" in synthesis; not verified |
| ANOVA / Kruskal-Wallis: numeric features vs. `stay_rating` | Do numeric features differ across rating classes? | Not reported | Not reported | Not reported | Reported as "fail to reject H0" for all features in synthesis; not verified |
| Multiple-comparison correction | Control false positives across tests | — | — | — | Mentioned in synthesis; method and adjusted thresholds not shown |

**Plain-English interpretation (conditional on the synthesis being accurate):**
- If the chi-square results are correct, booking channel and room type show no detectable association with stay rating. Neither is a useful basis for predicting rating, and neither should be used to justify rating-based decisions about those channels or room types.
- A "fail to reject" result does not prove that no association exists. With 900 rows and a rating scale that spreads observations across about ten classes, many cells are likely small. Small cells reduce the power of chi-square tests, so a real but modest association could go undetected.
- The chi-square test assumes adequate expected cell counts (generally at least 5). Sparse rating classes probably violate this assumption, so these results should be treated as provisional until exact tests or collapsed categories are used.
- The synthesis counts five "fail to reject" results, but the planned tests (two chi-square plus four numeric tests, if the four numeric features were each tested) would total six. One result may be missing from the report.

**Whether class imbalance distorts group comparisons** was part of the statistical plan, but no output addresses it.

### Predictive Models

**Model types tested:** class-weighted logistic regression and class-weighted random forest. The model outputs were not shown directly. The figures below come from the synthesis.

**Performance (reported in synthesis; not verified against raw output)**

| Model | Test accuracy | Macro-F1 | Balanced accuracy | Notes |
|---|---|---|---|---|
| Majority-class baseline | 23.89% | — | — | Reference point |
| Logistic regression | ~22% | 0.106 | 0.241 | Macro-F1 near chance level |
| Random forest | 22.22% (best model, per synthesis) | 0.173 (or 0.168) | 0.165 (or 0.177) | Severe overfitting |

Several values conflict across sections:
- Random forest macro-F1 is cited as both 0.173 and 0.168.
- Random forest balanced accuracy is cited as both 0.165 and 0.177. The synthesis suggests the 0.177 may come from a different model or split, but this is unclear.

**Overfitting.** The random forest's training-to-test gap is reported as +0.74 in accuracy and +0.80 in macro-F1. This means the forest memorizes its training data and generalizes poorly. Cross-validated macro-F1 (0.152) is reported to be consistent with the test figure, which suggests the performance level is stable, though low.

**Interpreting the metrics**
- Test accuracy (about 22%) is below the 23.89% majority baseline. A model that always predicts the most common rating would score higher, so the models add no accuracy value.
- Macro-F1 is the more informative metric here because it weights every rating class equally. Values near 0.10 would be expected from random guessing across about ten classes, so the logistic regression's 0.106 is essentially at chance. The random forest's 0.17 is higher but still low.
- Balanced accuracy complicates this reading. The logistic regression's 0.241 is well above the 0.10 chance level that would apply with ten equally likely classes. This conflicts with the "at chance" interpretation. The true chance level depends on the actual number of classes and their frequencies, which are not reported. This discrepancy should be resolved before either model is judged.

**Feature importances:** Not reported. The planned cross-check against the statistical results could not be completed. Because the random forest overfits, any impurity-based importances it produced would largely reflect noise and should not be relied on.

**Predictive insight:** The current features do not predict stay rating in a way that is useful for decisions.

---

## Synthesis

**Consistent null pattern.** Categorical tests (reported as chi-square), numeric tests (reported as ANOVA or Kruskal-Wallis), and predictive models (logistic regression and random forest) all point to weak or absent signal. This consistency across methods is the strongest cross-cutting finding, though the statistical half of it could not be checked against raw output.

**Validated hypotheses**

| Hypothesis | Evidence | Status |
|---|---|---|
| Booking channel is associated with rating | Chi-square, reported non-significant | Not supported (p-value not reported) |
| Room type is associated with rating | Chi-square, reported non-significant | Not supported (p-value not reported) |
| Numeric features differ across rating classes | ANOVA / Kruskal-Wallis, reported non-significant | Not supported (p-values not reported) |
| Features predict rating better than baseline | Test accuracy 22.22% vs. baseline 23.89% | Not supported |

No hypothesis was validated as a significant relationship.

**Model trade-off.** The random forest has higher macro-F1 but lower balanced accuracy than the logistic regression. This suggests the two models handle rare ratings differently, and neither handles them well. Because the discrepancy may partly reflect the conflicting values noted above, it should not be used to choose a model.

**Skew and nonlinearity.** The right skew in lead time and nightly rate could hide relationships from linear tests, and the EDA's "nonlinearity-driven association" note may point to this. It remains speculative because no statistic supports it.

---

## Conclusions

**What we can say with confidence**
1. The dataset is complete. All 900 rows and 7 columns have zero missing values.
2. Nights and guests are roughly symmetric. Lead time and nightly rate are right-skewed, with means 5.77 days and €13.00 above their medians.
3. The available features do not predict stay rating better than the majority-class baseline. Test accuracy was 22.22% against 23.89%.
4. The random forest overfits heavily, so its performance estimates are optimistic and its importances are unreliable.

**What we can say with moderate confidence**
5. Booking channel and room type show no detectable association with stay rating. This rests on synthesis-reported chi-square results with no p-values or effect sizes shown.
6. Numeric features show no detectable difference across rating classes. This is also synthesis-reported.

**What we cannot yet say**
- How strong the null results are, since no p-values or effect sizes are available.
- How severe the class imbalance is, since class counts were not reported.
- Whether any feature matters for specific rating levels (3, 4, or 10).
- Whether nonlinear or interaction effects exist.
- Whether the omitted correlation structure or feature importances would change the picture.

**Bottom line:** The current data does not support a rating-prediction model or rating-based business decisions. The evidence points to missing drivers outside these seven columns, not to a problem that a better algorithm will solve.

---

## Limitations & Caveats

**Data quality and reporting**
- **Conflicting values:** Random forest macro-F1 (0.173 vs. 0.168) and balanced accuracy (0.165 vs. 0.177) appear in different sections. The final report should use one verified value for each.
- **Dataset profile error:** The profile lists 5 numeric features. The correct count is 4 numeric features plus 2 categorical.
- **Missing outputs:** Class counts, p-values, test statistics, Cramér's V, the correlation matrix, cross-tabulations, confusion matrices, and feature importances are not in the raw outputs.
- **Unclear insight:** The "outlier- or nonlinearity-driven association" note has no accompanying statistic and cannot be interpreted.

**Statistical assumptions**
- **Chi-square tests** assume adequate expected cell counts (at least 5 per cell). Sparse rating classes probably violate this, so the chi-square results may be unreliable. Exact tests or collapsed categories are needed.
- **ANOVA** assumes approximately normal residuals and equal variances. The right-skewed features violate these assumptions, so Kruskal-Wallis is the more appropriate test. The output does not confirm which test was run.
- **Ordinal treatment:** Ratings appear to be ordered (the example value is 8, and the synthesis describes a range of about ten classes), but they were modeled as unordered classes. Ordinal methods would use the ordering and could detect signal that nominal methods miss.
- **Multiple comparisons:** A correction was mentioned but not shown, so the adjusted thresholds are unknown.

**Modeling limitations**
- **Overfitting:** The random forest was not tuned for depth, leaf size, or tree count, and no nested cross-validation was reported.
- **Sample size:** With 900 rows spread across about ten classes, some rating levels likely have very few observations. This limits both statistical power and the stability of per-class estimates.
- **Preprocessing:** The requirement that preprocessing be fit on training data only is described, but its correct application is not confirmed.

**Failed or incomplete analyses**
- No analysis failed outright (6 of 6 tasks completed), but several planned outputs are absent, including the feature-importance cross-check, the imbalance effect on group comparisons, and the Cramér's V effect sizes.

**Missing information**
- Booking dates (for time-based validation), guest or review data, and stay-specific operational data.

---

## Recommendations

### Immediate Actions

1. **Do not deploy a stay-rating prediction model.** The current features do not beat the majority-class baseline.
2. **Do not use booking channel or room type to predict or explain ratings,** based on the current evidence.
3. **Verify the reported numbers before circulating the results.** Resolve the conflicting macro-F1 and balanced-accuracy values, correct the feature count, and confirm the test count (five versus six "fail to reject" results).
4. **Report class counts for `stay_rating`.** This is the single most important missing number, since it determines the chance level for every metric and the reliability of per-class results.
5. **Add p-values, test statistics, and Cramér's V to the statistical results,** so that the strength of the null findings can be judged.

### Future Analysis

**Analytical questions**
1. Do ordinal models (such as ordinal logistic regression) or Spearman correlations reveal an ordered relationship that the nominal analysis missed?
2. Do rare ratings (3, 4, and 10) account for the failures, or do the models fail across all classes?
3. Do interactions matter, for example room type by nightly rate, or booking channel by lead time?
4. Does a regularized or shallower model generalize better, and does any real signal survive once overfitting is controlled?
5. Are the results stable under nested cross-validation and permutation-based feature importance on held-out data?
6. Is the sample large enough to detect small effects? A power analysis would show the minimum detectable effect size at 900 rows.
7. Do ratings drift over time? A time-based split, if booking dates are available, would test this.

**Data to collect**

Because the existing features show no detectable signal, new data is the priority. Useful additions include:
- **Guest experience measures:** service incidents, complaints, check-in and check-out experience, and cleanliness.
- **Stay-specific factors:** room condition, amenities used, and whether the stay met expectations.
- **Booking-context variables:** season, day of week, purpose of stay (leisure or business), and loyalty status.
- **Booking dates** to support time-based validation.
- **Rating metadata:** how ratings are collected, the scale definition, and whether the scale is ordered.

Collecting these variables is more likely to produce usable predictions than further modeling on the current seven columns.