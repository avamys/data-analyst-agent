# Data Analysis Report: Lakeside Hotel Stays

**Scope note:** Several specialist outputs were truncated or missing. The EDA distributions, Kruskal-Wallis and ANOVA results, numeric correlations, and most model metrics were not returned. This report states only what the outputs support. Figures marked *(recomputed)* were calculated from the contingency table printed in the chi-square output. They are not specialist outputs.

---

## Executive Summary

- **Booking channel is strongly associated with stay rating, and direct bookings rate higher.** Among rated stays, direct bookings average 7.17 versus 6.21 for agency bookings, a gap of about one point on the 3–10 scale. The association is significant after Holm correction (adjusted p = 1.08e-26), and it holds up when the unrated records are excluded (recomputed Cramér's V ≈ 0.31, a moderate effect).
- **Agency bookings have a much higher share of unrated or sentinel records.** Of agency bookings, 32.2% carry the value 99 in stay_rating, compared with 5.0% of direct bookings. Part of the channel "effect" may therefore reflect a data-capture difference rather than guest satisfaction. This must be verified before any business decision relies on it.
- **Room type is also associated with rating,** with adjusted p = 7.39e-07. Its effect size and direction were not reported, so it cannot yet guide decisions.
- **The current models cannot reliably predict ratings.** The best model (random forest) shows severe overfitting, with a train–test macro-F1 gap of 0.79. Rare ratings (3 and 4) receive 0% test recall. Predictive use is not recommended until the analysis is rerun with cross-validation.
- **The rating target needs a data-quality audit first.** The value 99 appears as a rating category, which is outside the apparent 3–10 scale. It is likely a placeholder for "not rated," and it affects the class-imbalance picture, the chi-square tests, and any model trained on this column.

---

## Dataset Overview

| Attribute | Value |
|---|---|
| Source | `lakeside_hotel_stays.csv` |
| Rows × columns | 900 × 7 |
| Target | `stay_rating` (treated as a categorical class label) |
| Categorical features | `booking_channel`, `room_type` |
| Numeric features | `nights`, `guests`, `lead_time_days`, `nightly_rate_eur` |
| Missing values | None reported in any column |

Although `stay_rating` is an integer, it is an ordinal class label rather than a continuous measure. The analysis therefore treats it as categorical, and the nonparametric tests are appropriate for it.

Example record: a website booking for a standard room, 9 nights, 1 guest, booked 63 days ahead, at €84.36/night, rated 8.

---

## Analysis Methodology

### Strategic Approach

The analysis followed a three-stage sequence:

1. **Exploratory analysis first.** Class counts, frequency tables, and distributions were examined before any modeling, because the target is imbalanced and some categories are sparse.
2. **Statistical testing second.** Chi-square tests were used for categorical associations, with Holm correction for multiple comparisons. Kruskal-Wallis or ANOVA and numeric correlation tests were planned for the continuous features.
3. **Predictive modeling last.** Stratified splits, class-weighted models, and permutation importance were used, because the multiclass target is imbalanced and the 900-row sample limits the reliability of rare-class estimates.

### Execution

| Specialist | Tasks | Status |
|---|---|---|
| Exploratory (EDA) | 2 | Completed (outputs partially returned) |
| Statistical | 2 | Completed (outputs partially returned) |
| Machine learning | 2 | Completed (outputs partially returned) |
| **Total** | **6** | **6 completed, 0 failed (100%)** |

Total execution time was 52.8 seconds. All tasks reported completion, but the returned output is incomplete for several of them.

---

## Key Findings

### Exploratory Analysis

**Data quality**
- No missing values were found in any column.
- The `stay_rating` column contains a category coded **99**. The printed contingency table shows 103 records with this value, which is 17.5% of the table's 590 rows. Ratings otherwise run from 3 to 10. The value 99 is most likely a "not rated" placeholder, not a real score.

**Class distribution of `stay_rating`** *(from the printed table, which covers 590 of 900 rows)*

| Rating | Count | % of rated stays (n = 487) |
|---|---|---|
| 3 | 9 | 1.8% |
| 4 | 12 | 2.5% |
| 5 | 78 | 16.0% |
| 6 | 105 | 21.6% |
| 7 | 131 | 26.9% |
| 8 | 83 | 17.0% |
| 9 | 49 | 10.1% |
| 10 | 20 | 4.1% |
| 99 (unrated?) | 103 | n/a |

- Ratings 3 and 4 together make up 4.3% of rated stays. Ratings 6 and 7 together make up 48.5%.
- Class 3 (9 records) is the rarest class shown, and class 4 (12 records) is second. This explains the earlier conflicting reports: class 3 is the most severe case, and class 4 is also rare.

**Channel-level pattern** *(from the printed table, recomputed)*

| Booking channel | Records in table | Unrated (99) | Rated | Mean rating (rated) | Median (rated) | Modal rating (rated) | Ratings ≥ 7 |
|---|---|---|---|---|---|---|---|
| Agency | 270 | 87 (32.2%) | 183 | 6.21 | 6 | 6 (27.9%) | 41.0% |
| Direct | 320 | 16 (5.0%) | 304 | 7.17 | 7 | 7 (28.0%) | 68.4% |

The printed table has only two channels, but the first data row is a website booking. The 310 rows not shown likely belong to the website channel. This needs confirmation.

**Not reported:** distributions, outlier counts, and frequency tables for `nights`, `guests`, `lead_time_days`, and `nightly_rate_eur`; the room-type frequency table; and the correlation matrix.

### Statistical Evidence

**1. Chi-square test of independence: booking_channel × stay_rating**
- **Purpose:** Test whether rating distribution depends on booking channel.
- **Result:** Null hypothesis rejected. Holm-adjusted p = 1.08e-26 (α = 0.05).
- **Effect size (recomputed from the printed table, n = 590):** χ² ≈ 120.5, df = 8, Cramér's V ≈ 0.45. This is a large association.
- **Sensitivity check, rated stays only (n = 487):** χ² ≈ 47.8, df = 7, Cramér's V ≈ 0.31. This is a moderate association, and it remains significant.
- **Interpretation:** Channel and rating are clearly linked. The association is weaker once unrated records are removed, but it does not disappear. Direct bookings are concentrated in higher ratings.

**2. Chi-square test of independence: room_type × stay_rating**
- **Purpose:** Test whether rating distribution depends on room type.
- **Result:** Null hypothesis rejected. Holm-adjusted p = 7.39e-07 (α = 0.05).
- **Effect size:** Not reported, so the strength of the association is unknown.
- **Interpretation:** There is evidence of an association, but it is smaller in statistical terms than the channel effect and cannot be quantified yet.

**3. Normality check (Shapiro-Wilk on residuals from group means)**
- **Result:** W = 0.6855 for residuals by booking channel. The p-value was not reported.
- **Interpretation:** W well below 1 indicates a strong departure from normality. This is expected for a discrete ordinal rating, and it supports the use of nonparametric tests for rating comparisons.

**Not reported:** Kruskal-Wallis or ANOVA results for rating across channels and room types; correlation coefficients and significance tests for the numeric features; and the raw (unadjusted) p-values.

**Multiple-comparison note:** Holm correction was documented for the two chi-square tests only. Any other tests run in the same analysis are not documented, so their error rates cannot be assessed.

### Predictive Models

**Models tested**
- Logistic regression with balanced class weights
- Random forest

**Performance**
- **Best model by test macro-F1:** Random forest. The exact macro-F1 values were not returned.
- **Overfitting:** The random forest's train–test macro-F1 gap is 0.79. This is far too large to treat the test score as a reliable estimate of performance on new data.
- **Rare-class recall:** Class 3 has 0.00% test recall for the models evaluated. With about 2 class-3 examples in an 80/20 split, this estimate is very imprecise, but it does show the models are not capturing the class. Class 4 had the lowest average recall across models.
- **Not reported:** Overall accuracy, balanced accuracy, per-class precision and F1, and confusion matrices.

**Feature importance**
- **Booking channel** has the largest permutation importance, with a macro-F1 drop of 0.0545 when shuffled. This is the most reliable importance measure in the output.
- Permutation importances for `room_type`, `nights`, `guests`, `lead_time_days`, and `nightly_rate_eur` were not reported.
- Impurity-based importances were computed but are biased toward continuous and high-cardinality features. They should not be used for business interpretation.

**Predictive insights**
- Booking channel is the most useful predictor in the current models, which is consistent with the chi-square results.
- The current models are not fit for operational use. Their apparent test performance is unreliable because of overfitting, and their predictions for rare ratings are essentially absent.

---

## Synthesis

**Validated and consistent patterns**
1. **Booking channel is associated with rating.** This is supported by the chi-square test (adjusted p = 1.08e-26), by the recomputed effect sizes (V ≈ 0.45 on all rows, ≈ 0.31 on rated rows), by the rating gap (7.17 vs 6.21), and by its top ranking in permutation importance. This is the most consistent finding in the analysis.
2. **Room type is associated with rating,** with adjusted p = 7.39e-07. The effect size is unknown, and the signal is less established than the channel effect.
3. **Rare ratings are a structural limitation.** Ratings 3 and 4 make up only 4.3% of rated stays. The same sparsity that makes the chi-square expected counts unreliable also explains the zero recall for these classes.

**An important reconciliation**
- The 99 category is the most important unresolved issue. Agency bookings have 32.2% 99-coded records, against 5.0% for direct bookings. Some or all of the channel association may come from this difference in missing or unrated records, not from differences in guest satisfaction. The rated-only sensitivity check suggests a real association remains, but the size of that remaining effect cannot be confirmed until the coding is clarified.

**Limitations in the synthesis**
- Overfitting and model selection are linked. The best model by test macro-F1 is also the most overfit, so the test-set comparison may favor a model that memorized noise.
- Numeric relationships (nights, guests, lead time, nightly rate) were not assessed, so the report cannot say whether they relate to rating.

---

## Conclusions

**What we can say with reasonable confidence**
- Booking channel and stay rating are associated. Direct bookings are concentrated in higher ratings (41.0% of agency rated stays score 7 or higher, against 68.4% of direct), and the association holds after excluding unrated records.
- Room type is also associated with rating, though its strength is unknown.
- Ratings 3 and 4 are rare (4.3% of rated stays combined), and the current models do not predict them.
- The random forest as currently evaluated overfits heavily and should not be deployed.

**What we cannot yet conclude**
- Whether the channel effect reflects guest satisfaction or differences in how ratings are recorded.
- The size and direction of the room-type effect.
- Whether nights, guests, lead time, or nightly rate relate to rating.
- How accurately any model can predict ratings on new data.

---

## Limitations & Caveats

**Data quality issues**
- **Sentinel value 99 in `stay_rating`.** This value appears in 103 records (17.5% of the printed table) and is probably a "not rated" code. Its presence is unexplained, and it is concentrated in agency bookings (32.2% vs 5.0%).
- **Contradictory missing-value reports.** The data-quality check reports zero missing values, but the 99 code functions as a missing-value placeholder. "No missing values" therefore does not mean that every rating is valid.
- **Incomplete contingency table.** The printed table covers 590 of 900 rows and shows only two channels, although the sample includes website bookings.
- **Malformed fragments in the outputs.** Some extracted lines are truncated (e.g., "notable deviation):"), so some findings may be incomplete.

**Statistical limitations**
- **Chi-square assumptions.** Expected cell counts for ratings 3 and 4 are below 5, and the 99 category distorts the test. Fisher's exact test or collapsed categories would be more appropriate for sparse cells.
- **Effect sizes missing for room type.** Only the adjusted p-value was reported.
- **Multiple testing.** Holm correction was documented for two tests only. Other tests run in the same analysis are not documented.
- **Small rare-class samples.** Class 3 has roughly 9 observations, so its recall estimate (0% on about 2 test cases) is statistically uninformative. It only shows that the model is not capturing the class.

**Modeling limitations**
- **Test-set model selection.** The best model appears to have been chosen on the test set. Model selection should use cross-validation within the training data, with the test set reserved for a single final evaluation.
- **Overfitting.** The 0.79 train–test macro-F1 gap means the reported test metrics for the random forest may be optimistic.
- **Missing metrics.** Exact macro-F1 values, accuracy, balanced accuracy, per-class precision and F1, and confusion matrices were not returned.

**Failed or missing analyses**
- No analyses failed outright, but the following were not returned: full EDA distributions and outlier checks; Kruskal-Wallis or ANOVA for ratings; numeric correlation matrix and tests; room-type frequency table; effect sizes for room type; and full model metrics.

---

## Recommendations

### Immediate Actions

1. **Audit the 99 code before any further analysis.** Confirm with the data owner what 99 means, whether it marks unrated stays, and why it is concentrated in agency bookings. Until this is resolved, avoid making channel-based pricing, marketing, or partner decisions on the current rating data.
2. **Hold off on deploying the current model.** The random forest's 0.79 overfitting gap and 0% rare-class recall make it unsuitable for operational use.
3. **Confirm the full channel and rating breakdown** using all 900 rows, including the website channel, so the channel comparison is complete.
4. **Treat the booking-channel finding as a priority for investigation,** not as a settled conclusion. If the rated-only association holds on the full data, it is the strongest candidate for a business decision (for example, examining agency-channel guest experience).

### Future Analysis

**Questions to answer**
1. What is the direction and size of the room-type effect, and what is its Cramér's V?
2. Do `nights`, `guests`, `lead_time_days`, or `nightly_rate_eur` relate to rating? Run Kruskal-Wallis (for categorical groups) and Spearman correlations with Holm or FDR correction.
3. Is the random forest's apparent advantage over logistic regression real? Compare the two using repeated stratified cross-validation with confidence intervals.
4. Would regularizing the random forest (shallower trees, larger `min_samples_leaf`) close the overfitting gap without losing performance?
5. Can ratings 3 and 4 be predicted at all? Test whether collapsing them into a "low rating" class, or using class weighting or SMOTE (applied inside the cross-validation folds), improves recall.
6. Do booking channel and room type interact in their effect on rating?
7. Why are ratings 3 and 4 rare? Is this a real customer pattern, a survey-design effect, or a labeling artifact?

**Analysis practices to adopt**
- Use nested or stratified cross-validation for model selection. Reserve the test set for one final evaluation.
- Report macro-F1, balanced accuracy, per-class recall, and confusion matrices alongside accuracy.
- Report an effect size (Cramér's V, rank-biserial, or epsilon-squared) for every significance test.
- Document the multiple-comparison correction for every family of tests, not just the chi-square tests.

**Data to collect**
- **A clear definition of rating and of the unrated state.** Replace the 99 placeholder with a null value and record the reason for non-response separately.
- **More records for ratings 3 and 4.** Even modest increases would make rare-class modeling more reliable.
- **Guest-level and stay-level detail on satisfaction drivers,** such as complaint records, check-in issues, and room-specific feedback, to explain rating differences.
- **Channel attribution data** (for example, the agency's identity and commission terms), to determine whether agency bookings differ in rating or in rating capture.