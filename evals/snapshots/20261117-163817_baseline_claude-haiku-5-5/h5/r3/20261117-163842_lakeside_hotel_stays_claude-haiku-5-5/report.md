# Data Analysis Report: Lakeside_Hotel_Stays

> **Data availability note:** The specialist outputs were truncated and several key results are missing. This report states only what the source outputs support. Where a number was not reported, the report says so and does not estimate it. Some figures are derived arithmetically from reported values, and the report labels these as derived.

---

## Executive Summary

- **The target is heavily concentrated and has a sparse tail.** Rating 7 is the most common class (215 of 900 rows, 23.9%). Rating 3 has only about 9 rows (1.0%). Ratings 4 and 3 together account for about 3% of stays, so any rating-level conclusion about them rests on very little data.
- **The Random Forest model overfits badly and should not be deployed as is.** The reported train/test macro-F1 gap is 0.789. If the gap is measured as training minus test, the test macro-F1 cannot exceed 0.211 (derived). Reported test performance is the only figure to trust, and that value is missing from the outputs.
- **At least one numeric predictor is associated with stay rating, but the outputs do not say which one.** One Kruskal-Wallis/ANOVA test rejected the null hypothesis, and three did not. Effect direction and magnitude are unknown.
- **Booking channel and room type may be associated with rating, but this is not confirmed.** The chi-square output contains only the phrase "a cell deviates from independence," with no p-values or Cramér's V.
- **The most important data question is whether class "99" is a real rating.** It sits among ratings 3–10 and may be a sentinel code for "not rated." Until this is resolved, the class count, the imbalance figures, and every model result are uncertain.

**Decisions supported now:** Pause deployment of the current model, verify the target coding, and re-run the statistical tests with the missing outputs recorded. Decisions about which factors drive ratings should wait until the tests are complete.

---

## Dataset Overview

| Attribute | Value |
|---|---|
| Source file | `/workspaces/agents/evals/data/lakeside_hotel_stays.csv` |
| Rows × columns | 900 × 7 |
| Target | `stay_rating` (multiclass, integer-coded) |
| Categorical features | `booking_channel`, `room_type` (2) |
| Numeric features | `nights`, `guests`, `lead_time_days`, `nightly_rate_eur` (4 numeric, plus `stay_rating`) |
| Missing values | 0 in all relevant columns |
| Observed rating levels | 3, 4, 5, 6, 7, 8, 9, 10, 99 (9 classes) |

*Note: the task description lists 5 numeric features. The data dictionary shows 4 numeric predictors plus the numeric target. This report uses the 4 predictors.*

---

## Analysis Methodology

### Strategic Approach

The analysis followed a three-stage sequence:

1. **Exploratory analysis first.** This covered target distribution, class imbalance, category frequencies, and numeric distributions. It was needed to check for sparse levels and skew before any testing.
2. **Statistical testing second.** Chi-square tests were planned for the two categorical predictors against rating. Kruskal-Wallis or ANOVA tests, with post-hoc comparisons and multiple-comparison correction, were planned for the four numeric predictors.
3. **Predictive modeling last.** Stratified splits, class weighting, and macro-F1 were chosen because of the imbalance. Accuracy was not used as the primary metric.

### Execution

| Specialist | Tasks | Status |
|---|---|---|
| Exploratory (EDA) | 2 | Completed, output truncated |
| Statistical | 2 | Completed, output truncated |
| Machine learning | 2 | Completed, metrics not reported |
| **Total** | **6** | **6 of 6 completed (100%), total runtime 128.4 s** |

"Completed" means the task finished. It does not mean every planned output was reported. Several planned outputs are missing (see Limitations).

---

## Key Findings

### Exploratory Analysis

**Target distribution**

Class sizes were reported for seven of the nine levels. Ratings 10 and 99 were cut off.

| Rating | Rows | Share of 900 |
|---|---|---|
| 3 | 9 | 1.0% |
| 4 | 19 | 2.1% |
| 5 | 115 | 12.8% |
| 6 | 149 | 16.6% |
| 7 | 215 | 23.9% |
| 8 | 152 | 16.9% |
| 9 | 83 | 9.2% |
| 10 and 99 | 158 combined (derived) | 17.6% combined |

- Rating 7 is the modal class. Its share (23.9%) is the accuracy a majority-class predictor would achieve. This is the baseline any model must beat.
- Ratings 3 and 4 together hold 28 rows (3.1%). Per-class metrics for these levels will be unstable.
- The EDA summary describes the imbalance as "notable" but gives no imbalance ratio. Using the reported counts, the ratio between the largest class (215) and the smallest (9) is about 24:1.
- The reported distribution is concentrated in the middle ratings (5–9 account for 82.4% of rows, derived).

**Categorical frequencies**

Counts for `booking_channel` and `room_type` were not reported in the available output. The sparsity check on these levels was therefore not completed.

**Numeric distributions and correlations**

The EDA output for `nightly_rate_eur`, `nights`, `guests`, and `lead_time_days` was cut off before the skewness, outlier, and correlation results. No values are available for these checks.

**Data quality**

No missing values were found in any column. This was the only data quality check reported as complete.

---

### Statistical Evidence

#### Test 1: Chi-square tests of independence (booking_channel and room_type vs. stay_rating)

- **Purpose:** Test whether the distribution of ratings differs across booking channels and across room types.
- **Table size:** 3 × 9 (booking channels × rating classes), as reported for the booking-channel test. The room-type table size was not reported.
- **Result:** The output says only that "a cell deviates from independence." This phrase appears twice with identical wording, which suggests an extraction artifact.
- **p-values:** Not reported.
- **Effect size (Cramér's V):** Not reported.
- **Expected-count check:** Not reported. With 9 rating classes and some classes below 20 rows, many expected cell counts are likely below 5. The chi-square approximation may therefore be unreliable.

**Plain-English interpretation:** There is an indication that rating distribution is not identical across booking channels and possibly across room types. The strength of the association and which channels or room types are involved are unknown. This should not be treated as confirmed.

#### Test 2: Kruskal-Wallis / ANOVA (numeric predictors vs. stay_rating)

- **Purpose:** Test whether rating distributions differ across the four numeric predictors.
- **Test selection:** Kruskal-Wallis was the appropriate choice given likely skewness of nightly rates and sparse classes. The reported output did not confirm which test was run for each variable.
- **Results:**
  - 1 variable: reject H0 (rating distributions differ)
  - 3 variables: fail to reject H0
- **Variable labels:** Not reported. The rejected variable cannot be identified.
- **H-statistics, p-values, and epsilon-squared effect sizes:** Not reported.
- **Post-hoc tests and multiple-comparison correction:** Not reported.

**Plain-English interpretation:** At least one of nightly rate, nights, guests, or lead time is associated with stay rating. The data does not say which one, or in what direction.

#### Hypothesis summary

| Hypothesis | Test | Result | Status |
|---|---|---|---|
| booking_channel is associated with rating | Chi-square | "Deviates from independence"; p and V not reported | Unconfirmed |
| room_type is associated with rating | Chi-square | Same statement; p and V not reported | Unconfirmed |
| At least one numeric predictor is associated with rating | Kruskal-Wallis/ANOVA | Reject H0 (one variable) | Supported; variable unknown |
| The other numeric predictors show no rating difference | Kruskal-Wallis/ANOVA | Fail to reject H0 (three variables) | Not rejected; no p-values reported |

---

### Predictive Models

**Model types tested**

- Random Forest (selected as best on test macro-F1)
- Logistic regression (trained, results not reported)

Both models used class weighting to address the imbalance.

**Performance metrics**

| Metric | Random Forest | Logistic Regression |
|---|---|---|
| Train macro-F1 | Not reported directly | Not reported |
| Test macro-F1 | Not reported (selected as best) | Not reported |
| Train/test macro-F1 gap | 0.789 | Not reported |
| Accuracy | Not reported | Not reported |
| Per-class precision and recall | Not reported | Not reported |
| Confusion matrix | Not reported | Not reported |

**Derived bound on test performance:** If the gap is defined as training macro-F1 minus test macro-F1, then test macro-F1 = training macro-F1 − 0.789. Since macro-F1 cannot exceed 1.0, the Random Forest's test macro-F1 is at most 0.211. This is an upper bound only. The actual value is unknown.

**Baseline comparison (derived):** A predictor that always outputs the majority class (rating 7) has accuracy of 23.9%. Its macro-F1 would be approximately 0.04, because it would earn an F1 of about 0.39 on one class and 0 on the other eight, averaged over nine classes. Any model should be compared against this baseline, not against zero.

**Feature importance**

Permutation importance was the planned method, filtered by the significant statistical tests. No importance values were reported. No feature can be named as a driver of rating.

**Predictive insights**

- The Random Forest's training score is far higher than its test score. The training score should not be used to judge the model.
- The outputs do not show that the model beats the majority-class baseline on test data. This cannot be confirmed from the available results.
- The model selection used the test set, which means the reported test score is optimistically biased.

---

## Synthesis

**Validated and consistent patterns**

1. **The target is imbalanced and concentrated.** Ratings 5–9 hold 82.4% of rows, and rating 7 alone holds 23.9%. This is the one fact consistently supported across the outputs.
2. **At least one numeric predictor is associated with rating.** This is supported by one significant Kruskal-Wallis/ANOVA result, though the variable is unidentified.
3. **The Random Forest overfits.** The 0.789 gap is large and is the most actionable model-quality finding.

**Partially supported or unconfirmed**

- Booking channel and room type may be associated with rating, but no p-values or effect sizes are available.
- Random Forest may have some predictive signal beyond the majority class, but its test score is not reported.

**Cross-analysis consistency**

The variables flagged in the statistical tests overlap with the variables used by the ML pipeline. This makes the statistical and model results compatible in principle, but the feature importances needed to link them are missing.

---

## Conclusions

**What can be stated with confidence**

- The dataset is complete, with no missing values in the relevant columns.
- Stay ratings are concentrated in the middle of the scale. Rating 7 is the most common (23.9%), and ratings 5–9 together account for 82.4%.
- Ratings 3 and 4 are very rare (28 rows combined, 3.1%).
- At least one of the four numeric predictors is associated with rating distribution.
- The current Random Forest model overfits severely. Its test macro-F1 is at most 0.211 under the stated gap definition.

**What cannot yet be concluded**

- Which numeric predictor is associated with rating, and in what direction.
- Whether booking channel or room type is associated with rating, and how strongly.
- Whether any model beats the majority-class baseline on macro-F1.
- Which features drive ratings. The results are associations at most and do not establish causation.

---

## Limitations & Caveats

**Data quality issues**

- **Class "99" is ambiguous.** It may be a sentinel code for "not rated." If so, it is being treated as a valid rating class, which affects class counts, imbalance figures, and every downstream result.
- **Ratings are ordinal but were treated as nominal.** Chi-square tests and multiclass classification ignore the order of the scale. Ordinal methods may be more suitable.
- **Very small classes.** Rating 3 has about 9 rows, so its precision and recall are unstable, and macro-F1 is sensitive to it.

**Statistical assumptions**

- **Chi-square:** Expected counts are likely below 5 in many cells, so the asymptotic approximation may be invalid. Fisher's exact test or merged rating groups would be safer. The expected-count check was not reported.
- **ANOVA:** Normality and equal variance are unlikely, given skewed nightly rates and sparse classes. Kruskal-Wallis is the more appropriate test.
- **Multiple comparisons:** Pairwise post-hoc tests across nine classes inflate false-positive risk. Correction was planned but no corrected p-values were reported.
- **Interactions:** No interaction effects were tested.

**Methodological concerns**

- **Overfitting:** The 0.789 gap indicates hyperparameters were not constrained enough.
- **Test-set model selection:** Choosing the best model on test macro-F1 biases the reported performance upward.
- **Causal language:** Any reference to "drivers" of ratings should be read as association only.

**Failed or incomplete analyses**

The tasks finished, but the following outputs are missing or truncated:

- Chi-square p-values, Cramér's V, and expected-count tables
- Kruskal-Wallis/ANOVA statistics, variable labels, and post-hoc results
- Correlation matrix, skewness, and outlier summaries for the numeric predictors
- Category counts for `booking_channel` and `room_type`
- Class counts for ratings 10 and 99
- Test macro-F1, accuracy, per-class precision and recall, and confusion matrices
- Feature importance values
- Logistic regression results

**Missing information**

Most of the quantitative detail needed for stakeholder decisions is absent. The findings above are directional at best.

---

## Recommendations

### Immediate Actions

1. **Do not deploy the current Random Forest model.** Its training performance is inflated, and its test performance is unverified.
2. **Verify the target coding, especially class 99.** Confirm whether it is a valid rating, a "not rated" code, or missing data. Then decide whether to remove, recode, or model it separately.
3. **Re-run the chi-square tests with reporting.** Record p-values, Cramér's V, and expected-count checks. Use Fisher's exact test or merge sparse rating classes where needed.
4. **Re-run the Kruskal-Wallis tests with labeled variables.** Report H-statistics, p-values, corrected post-hoc comparisons, and epsilon-squared effect sizes.
5. **Establish the majority-class baseline explicitly.** Report that a model must exceed 23.9% accuracy and roughly 0.04 macro-F1 to add value.
6. **Frame all current findings as associations,** not drivers, in any stakeholder communication.

### Future Analysis

**Modeling**

- Tune the Random Forest (`min_samples_leaf`, `max_depth`, `n_estimators`) using cross-validation. Report training and CV scores together to show the gap narrowing.
- Select the final model on validation data or cross-validation only. Report test performance once.
- Report per-class precision, recall, and the confusion matrix, with particular attention to ratings 3 and 4.
- Evaluate an ordinal model (for example, ordinal logistic regression) as an alternative to nominal classification.
- Test interactions between nightly rate, stay length, and lead time with booking channel and room type.

**Statistical follow-up**

- Identify which numeric predictor drives the significant Kruskal-Wallis result, and its direction.
- Run level-by-level post-hoc comparisons for booking channel and room type to see which categories differ.

**Data to collect**

- **Clearer target coding.** Documentation for rating 99, and any other non-rating codes.
- **More observations in sparse ratings.** Ratings 3 and 4 have 28 rows combined. More data, or a deliberate pooling rule, is needed for reliable per-class estimates.
- **Guest-level and stay-level context.** Variables such as room features, stay purpose, and guest history could explain more of the rating variation than the current predictors do.
- **Rating collection details.** When and how ratings were collected, and the response rate, so that selection bias can be assessed.