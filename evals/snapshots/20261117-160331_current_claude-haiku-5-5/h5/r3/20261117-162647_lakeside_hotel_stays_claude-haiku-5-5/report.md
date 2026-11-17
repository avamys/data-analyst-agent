# stay_rating in a 900-Stay Hotel Dataset: Distribution, Associations and Predictability

## Summary

- **Code 99 is a large class and is probably not a rating.** It covers 125 rows (13.9%), and its value lies outside the 3–10 scale. Its share is highly uneven by booking channel: 32.2% of agency rows, against 5.0% of direct and 7.1% of website rows. Agency accounts for 69.6% of all code-99 rows.
- **With code 99 excluded, booking_channel and room_type are each significantly associated with stay_rating, with small-to-moderate effects** (Cramér's V 0.205 and 0.194). Agency has the lowest mean (6.21 vs 7.13 for website and 7.17 for direct), and suites have the highest (7.70). These results depend on excluding code 99, and including it as a category strengthens the booking_channel association (V 0.304).
- **No channel interaction was detected** with room_type, nightly rate or nights, under either an OLS-based test or an ordinal proportional-odds model. The sample is small, so this does not rule out small interactions.
- **Models add little over the majority-class baseline.** Logistic regression reaches 0.2889 test accuracy against 0.2389 for the baseline. The random forest reaches a higher macro-F1 (0.1534 or 0.1556, depending on the run) but lower accuracy (0.2). All results rest on a single 180-row test split and are not reliable.
- **Nightly rate is the clearest numeric association** (Spearman rho 0.245, weak), and lead time is marginally significant and negligible (rho −0.076). Nights and guests show no detectable association.

## Data

- **Size:** 900 rows × 7 columns.
- **Target:** stay_rating, with 9 distinct values, including code 99. The profile header says "7 classes" but lists nine values; this report uses the nine listed values.
- **Class shares (all 900 rows):** 7: 23.9%; 8: 16.9%; 6: 16.6%; 99: 13.9%; 5: 12.8%; 9: 9.2%; 10: 3.7%; 4: 2.1%; 3: 1.0%. The target is imbalanced.
- **Features:** numeric (nights, guests, lead_time_days, nightly_rate_eur); categorical (booking_channel, room_type). There are no date/time features and no identifier or free-text columns.
- **Missing values:** none in any column. The value 99 appears in stay_rating (125 rows) and in lead_time_days (2 rows). Lead time ranges from 1 to 183 days, so those 2 rows are treated as plausible values. No other numeric column contains a sentinel value.

## Findings

### Distribution of stay_rating and code 99

Among the 775 rows with a scale value, rating 7 is the most common (215 rows, 23.9% of all rows). Code 99 lies 89 points above the next value (10), and it is most likely a non-score code for an unknown or missing rating. This is an interpretation from the value alone; the data does not confirm it.

The 125 code-99 rows differ little from other rows on the numeric columns: mean nights 5.34 vs 5.61, guests 2.53 vs 2.45, lead time 40.5 vs 39.7 days, and nightly rate EUR 127.7 vs 126.7.

Code 99 is concentrated in agency bookings: 32.2% of agency rows (87 of 270), against 5.0% of direct rows (16 of 320) and 7.1% of website rows (22 of 310). The bootstrap 95% CI for the agency rate is 26.7% to 37.8%. Whether agency uses a separate rating or placeholder process is a hypothesis that these data do not test.

![Within-channel share of stays in each stay_rating class, including code 99](tasks/eda_1/charts/rating_dist_by_channel.png)

### Associations with stay_rating (code 99 excluded, n = 775)

**booking_channel.** The chi-square test is significant: χ² = 65.05, dof = 14, p = 1.5e-8, Cramér's V = 0.205 (bootstrap 95% CI 0.182 to 0.264, from stat_1; the stat_3 recomputation gives 0.179 to 0.266). This is a small-to-moderate association, conditional on excluding code 99.

Mean stay_rating by channel (code 99 excluded):
- Agency: 6.21 (95% CI 6.01 to 6.41, n = 183)
- Direct: 7.17 (7.01 to 7.34, n = 304)
- Website: 7.13 (6.96 to 7.29, n = 288)

Agency sits about 1 point below the other two channels, whose CIs overlap. This gap may partly reflect which rows were excluded (see Treatment of code 99 below).

**room_type.** The chi-square test is significant: χ² = 58.52, dof = 14, p = 2.1e-7, V = 0.194 (bootstrap 95% CI 0.167 to 0.256), similar in size to booking_channel.

Mean stay_rating by room_type (code 99 excluded), rising with room category:
- Standard: 6.59 (95% CI 6.45 to 6.74, n = 385)
- Superior: 7.06 (6.88 to 7.23, n = 268)
- Suite: 7.70 (7.46 to 7.95, n = 122)

The three CIs do not overlap.

![Mean stay_rating per booking_channel and room_type level, code 99 excluded, with 95% CI](tasks/stat_1/charts/stat1_group_means.png)

**Numeric features (Spearman, code 99 excluded):**
- nightly_rate_eur: rho = 0.245 (95% CI 0.177 to 0.310), p = 4.9e-12. Higher-priced stays tend to receive higher ratings; the effect is weak.
- lead_time_days: rho = −0.076 (95% CI −0.146 to −0.006), p = 0.033. This is only marginally significant and negligible.
- nights: rho = 0.008 (95% CI −0.062 to 0.079), p = 0.81.
- guests: rho = 0.004 (95% CI −0.066 to 0.075), p = 0.90.

### Treatment of code 99

Results depend on how code 99 is handled:

- **booking_channel with code 99 as a category (n = 900):** χ² = 165.9, dof = 16, p = 5.4e-27, V = 0.304 (bootstrap 95% CI 0.277 to 0.355). The association is stronger than with code 99 excluded (V = 0.205). This likely reflects the concentration of code 99 in agency rows; that explanation is a hypothesis and is not tested here.
- **room_type with code 99 as a category (n = 900):** χ² = 59.1, dof = 16, p = 7.4e-7, V = 0.181 (bootstrap 95% CI 0.160 to 0.244). The effect barely changes from the excluded version (V = 0.194).
- **Agency mean with code 99 as a category:** 36.1 (t-based 95% CI 30.9 to 41.3) against 12.7 for the other channels, a gap of +23.4. This is driven by treating 99 as a numeric-looking value and should not be read as a rating effect.
- **Agency mean with code 99 excluded:** 6.21 (95% CI 6.01 to 6.41) against 7.15 for the other channels, a gap of −0.94. This gap is conditional on excluding code 99 and is not established as a rating effect.

![Rate of stay_rating code 99 per booking_channel, all 900 rows, bootstrap 95% CI](tasks/stat_3/charts/stat3_share99_by_channel.png)

### Interactions

With code 99 excluded (n = 775), the tests found no detectable interaction:

- **OLS / Gaussian likelihood-ratio tests** (treating stay_rating as continuous, not ordinal):
  - Channel × room_type: LR χ² = 2.68 on 4 df, p = 0.61 (nested F p = 0.62).
  - Channel × nightly_rate_eur: LR = 1.35 on 2 df, p = 0.51.
  - Channel × nights: LR = 0.78 on 2 df, p = 0.68.
- **Proportional-odds (ordinal) models:**
  - Channel × room_type: LR χ² = 3.46 on 4 df, p = 0.48.
  - Channel × nightly_rate_eur: LR χ² = 1.87 on 2 df, p = 0.39.
  - A rough check of proportional odds on base predictors (multinomial vs PO, LR = 25.54 on 30 df, p = 0.70) does not reject the assumption. This check does not cover the interaction terms.

The ordinal and OLS results agree. Within every channel, the room_type ordering is standard < superior < suite, and agency sits below direct and website in every room type (OLS cell means, e.g., agency standard 5.78, n = 82; agency suite 6.88, n = 25). The within-channel nightly-rate slopes per EUR are agency 0.0086 (95% CI 0.0039 to 0.0134), direct 0.0068 (0.0033 to 0.0103) and website 0.0100 (0.0065 to 0.0136); the CIs overlap heavily.

These null results are not evidence of no interaction. The agency suite cell is small (n = 25), and power is limited.

![Mean stay_rating by room_type within each booking_channel, code 99 excluded (n = 775)](tasks/stat_2/charts/stat2_roomtype_by_channel.png)

### Predictive models

All models predict the nine target values, including code 99, on a shared stratified split (720 training rows, 180 test rows).

| Model | Test accuracy | Test macro-F1 | Notes |
|---|---|---|---|
| Majority class (predicts 7) | 0.2389 | 0.0429 | Recall 1.0 for class 7, 0.0 for all others |
| Logistic regression (ml_1) | 0.2889 | 0.1273 | Recall 0.558 (7), 0.367 (8), 0.68 (99); 0.0 for ratings 3, 4, 5, 6, 9, 10 |
| Random forest (ml_1) | 0.2 | 0.1534 | Train accuracy 1.0; recall 0.372 (7), 0.24 (99) |
| Random forest, re-fit (ml_2) | 0.2 | 0.1556 | Train accuracy 1.0; recall 0.33 (7), 0.28 (99), 0.0 for ratings 3 and 10 |

Logistic regression has the highest accuracy and the random forest the highest macro-F1. The ml_1 and ml_2 random forest figures differ (macro-F1 0.1534 vs 0.1556; code-99 recall 0.24 vs 0.28). The likely cause is a different random state or fit configuration; this is not confirmed. The ml_1 figures are cited for ml_1, and the ml_2 figures describe only the re-fit.

![Test-set accuracy and macro-F1 of the majority baseline, logistic regression and random forest predicting stay_rating (180 test rows)](tasks/ml_1/charts/ml1_model_scores.png)

### Feature importance

- **Logistic regression (ml_1), absolute coefficients:** the largest are booking_channel_agency (0.667), booking_channel_direct (0.398), nightly_rate_eur (0.362), booking_channel_website (0.337) and room_type_suite (0.325). The agency weight is tied to the concentration of code 99 in agency rows.
- **Random forest impurity importance (ml_1 and ml_2):** nightly_rate_eur (0.304 / 0.308), lead_time_days (0.286 / 0.284), nights (0.193 / 0.195) and guests (0.112 / 0.112). Categorical features have small impurity importances (each at or below 0.027).
- **Random forest permutation importance (ml_2, drop in test macro-F1 over 30 shuffles):** nightly_rate_eur 0.0253 (sd 0.0221), guests 0.0221 (sd 0.0139), booking_channel 0.0193 (sd 0.0272), nights 0.0017 (sd 0.0222), room_type −0.0017 (sd 0.0285), lead_time_days −0.0012 (sd 0.0208). Only guests is reasonably separated from zero. The impurity and permutation measures conflict for lead_time_days; the permutation result is the one to trust for test performance, and lead time should not be called important.

![Mean drop in test macro-F1 when each original feature is shuffled](tasks/ml_2/charts/ml2_perm_importance.png)

## Limitations

- **Code 99 is probably a non-score code.** This is inferred from its value only. Its concentration in agency rows (32.2% vs 5.0% and 7.1%) may partly explain the agency gap and the booking_channel results, and this has not been tested.
- **Associations and means are conditional on excluding code 99.** This is the main analysis, but the sensitivity check with code 99 treated as missing has not been run. Including code 99 as a category changes the booking_channel effect size (V 0.205 to 0.304) and the agency gap (−0.94 to +23.4).
- **Chi-square p-values are approximate.** With code 99 excluded, the minimum expected cell count is 2.13 for booking_channel and 1.42 for room_type, and 4 of 24 cells in each table have expected counts below 5. The bootstrap intervals do not rely on this assumption.
- **Cramér's V interval for booking_channel differs by task.** stat_1 reports 0.182 to 0.264; stat_3 reports 0.179 to 0.266. The point estimate is identical (0.205). This report cites the stat_3 interval for that task and the stat_1 interval for the earlier one.
- **Interaction tests have limited power.** Small cells (e.g., agency suite, n = 25) mean small interactions cannot be ruled out. The OLS tests treat stay_rating as continuous; the ordinal check covers the interaction terms but its proportional-odds check is limited to base predictors.
- **Model results rest on one 180-row test split** with no uncertainty estimate. Margins over the baseline are small and should not be read as reliable. Both models were trained with code 99 as a target class.
- **Overfitting.** The random forest has train accuracy 1.0 against test accuracy 0.2, so its impurity importances describe an overfit model.
- **Unresolved review issues.** The ml_1 and ml_2 random forest results disagree and were not reconciled; the cause is not confirmed. The ml_2 task is marked partial, and its permutation importances rest on 30 shuffles of one test split, so the ranking is not reliable.
- **Not tested:** the missingness and sentinel check beyond the value-level inspection, the agency placeholder hypothesis, and the sensitivity analysis treating code 99 as missing.

## Open questions

- Why are agency bookings over-represented among code-99 rows, and does the agency channel use a separate rating or placeholder process? This would need data beyond the current set.
- Would treating code 99 as missing, or removing it from the target, change the booking_channel and room_type rankings and the models' accuracy on ratings 3 to 10?
- Are the 2 rows with lead_time_days equal to 99 real values, or a coincidence with the rating code?
- Does the nightly_rate effect hold within room_type, given that suites are priced higher?
- Would repeated cross-validation or bootstrap intervals show whether the models' gains over the baseline, and the permutation importances (especially guests and nightly_rate_eur), are reliably above zero?
- Would class weighting or a regularised random forest reduce overfitting and raise recall on the rare rating classes?
- What is the minimum detectable channel × room_type interaction given the small agency suite cell?
- Would a full multinomial model with channel interaction terms confirm the proportional-odds results?
- Would fixing the random state and reporting the spread across seeds explain the gap between the ml_1 and ml_2 random forest figures?