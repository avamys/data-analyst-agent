# Stay Rating Analysis of the 900-Stay Dataset

## Summary

- **Rating 99 is a separate code, not a score, and it is concentrated in agency bookings.** Of 900 stays, 125 (13.9%) carry code 99, against ratings 3 to 10. Agency stays have a 99 share of 32.2%, against 5.0% for direct and 7.1% for website. The sentinel-for-missing reading is a hypothesis that the data do not confirm. The 125 rows were excluded from rating analysis.
- **On the 775 rated stays, booking channel, room type and nightly rate are each significantly associated with rating class** (booking_channel chi-square p = 1.5e-8, room_type p = 2.1e-7, nightly rate Kruskal-Wallis p = 9.5e-9; all significant after Holm correction). Nights, guests and lead time show no association. Agency stays have the lowest mean rating (6.21).
- **No channel × room_type interaction was detected.** The OLS test gave p = 0.60, the log-linear test p = 0.69 and the ordinal likelihood-ratio test p = 0.48. These nulls are weak evidence because several interaction cells are small.
- **Neither predictive model beats the majority-class baseline.** Test accuracy was 0.1097 for logistic regression and 0.2323 for the random forest, against 0.2774 for always predicting rating 7. Macro-F1 was 0.1069 and 0.1315. The only feature with a consistent, though uncertain, importance signal was booking channel.
- **The association findings and the model findings point in different directions.** The tests find significant associations, but the models do not show predictive value from them. This is reported as found and not resolved.

## Data

- **Size:** 900 rows × 7 columns.
- **Target:** `stay_rating`, multiclass. Values are 3 to 10 plus a separate code 99. The class shares are 7: 23.9%, 8: 16.9%, 6: 16.6%, 99: 13.9%, 5: 12.8%, 9: 9.2%, 10: 3.7%, 4: 2.1%, 3: 1.0%. The profile header states "7" target classes, but nine values are listed (see Limitations).
- **Features:** numeric `nights`, `guests`, `lead_time_days`, `nightly_rate_eur`; categorical `booking_channel`, `room_type`. There are no date or time features and no ids or free-text fields.
- **Missing values:** none. There are 0 empty cells, and 0 empty or placeholder strings in `booking_channel` and `room_type`.
- **Numeric ranges:** nights 1 to 10 (median 6); guests 1 to 4 (median 2); lead time 1 to 183 days (median 34); nightly rate 65.19 to 280.5 EUR (median 113.9).

## Findings

### 1. Distribution of stay_rating and the code 99

Counts are 3: 9, 4: 19, 5: 115, 6: 149, 7: 215, 8: 152, 9: 83, 10: 33 and 99: 125. The most common real rating is 7, at 23.9%.

![Number of stays per stay_rating value; 99 is an isolated code above the 3-10 scale](tasks/eda_1/charts/stay_rating_counts.png)

- Code 99 lies outside the 3-10 scale. Its nightly rate mean is 127.72 EUR and its median is 114.58 EUR, within the range of the 3-10 ratings. Its nights median is 5 and its lead-time median is 35 days. These profiles are close to those of the other ratings, so they do not show whether 99 carries ordinal signal.
- Treating 99 as a sentinel for unrated or unknown stays is a hypothesis, not an established result.
- The decision taken was to treat 99 as missing for rating analysis. The 125 rows are kept with a flag, and the rating field is set to missing for them.

### 2. Missingness

The dataset has no empty cells and no placeholder text values. Missingness exists only in the sense that code 99 marks 125 stays that were excluded from the rated analyses.

### 3. Associations with stay_rating (rated stays, n = 775)

Tests use the 775 rated stays. Holm correction covers six tests.

**booking_channel.** Chi-square = 65.06, df = 14, p = 1.5e-8, Cramér's V = 0.205 (small to moderate), Holm-adjusted p = 7.5e-8. Mean rating by channel:

| Channel | Mean rating | 95% CI | n |
|---|---|---|---|
| Agency | 6.21 | 6.01 to 6.41 | 183 |
| Direct | 7.17 | 7.01 to 7.34 | 304 |
| Website | 7.13 | 6.97 to 7.29 | 288 |

Because agency stays hold most of the excluded 99 codes, these channel effects are conditional on that exclusion (see Limitations).

**room_type.** Chi-square = 58.52, df = 14, p = 2.1e-7, Cramér's V = 0.194, Holm-adjusted p = 8.5e-7. Mean rating by room type:

| Room type | Mean rating | 95% CI | n |
|---|---|---|---|
| Standard | 6.60 | 6.45 to 6.74 | 385 |
| Suite | 7.71 | 7.47 to 7.94 | 122 |
| Superior | 7.06 | 6.89 to 7.23 | 268 |

Collapsing sparse rating classes into 3-5, 6, 7, 8 and 9-10 leaves no expected count below 5. The collapsed chi-square is 58.87 (df = 8, p = 7.8e-10) for channel and 54.32 (df = 8, p = 6.0e-9) for room type. A permutation test on the full classes (2,000 shuffles) gave p = 0.0005, the floor of that test. The full-class chi-square p-values are therefore approximate, but the conclusions do not change.

**nightly_rate_eur.** Kruskal-Wallis H = 50.92, p = 9.5e-9, Holm-adjusted p = 5.7e-8, epsilon-squared = 0.057 (small to moderate). The mean rate rises from 95.77 EUR at rating 3 to 152.24 EUR at rating 10, with intermediate values of 102.36 (4), 113.9 (5), 120.06 (6), 124.46 (7), 137.88 (8) and 140.67 (9).

![Mean nightly rate per stay_rating class on rated stays, with 95% CI; rate rises with rating](tasks/stat_1/charts/stat1_nightly_rate_by_rating.png)

**nights, guests, lead_time_days.** No association. Kruskal-Wallis p = 0.99 (nights, H = 1.40), p = 0.94 (guests, H = 2.25) and p = 0.54 (lead time, H = 6.02). Holm-adjusted p = 1.0 for each. Epsilon-squared values are -0.007, -0.006 and -0.001, which indicates no detectable effect.

Per-class means and confidence intervals for nights, guests and lead time are in the task record. Per-class rating intervals have zero width, because the class mean equals the class value, so they carry no information.

### 4. Interactions between booking_channel and room_type

**Omnibus tests.** The OLS F-test of the channel × room type interaction gives F = 0.68 (df = 4), p = 0.60. The log-linear three-way test on collapsed rating classes gives G² = 12.77 (df = 16), p = 0.69. Seven of 45 three-way cells have expected counts below 5; the smallest has n = 2 (agency/standard, rating 9-10). Agency/suite has n = 25. These nulls are absence of evidence under limited power, not proof of no interaction.

**Ordinal model.** The likelihood-ratio test of the four interaction terms gives chi-square = 3.46, df = 4, p = 0.48. Individual interaction coefficients (log-odds, from the interaction model that also includes the rate covariate) are:

- direct × suite: -0.37 (SE 0.49, p = 0.45)
- direct × superior: -0.32 (SE 0.37, p = 0.39)
- website × suite: 0.32 (SE 0.50, p = 0.52)
- website × superior: -0.20 (SE 0.37, p = 0.58)

Approximate 95% intervals run from about -1.3 to +0.6, so moderate interactions are not excluded.

**Cell means (rated stays, n in brackets):**

| Channel | Standard | Suite | Superior |
|---|---|---|---|
| Agency | 5.78 (82) | 6.88 (25) | 6.45 (76) |
| Direct | 6.88 (156) | 7.76 (51) | 7.33 (97) |
| Website | 6.74 (147) | 8.09 (46) | 7.26 (95) |

Suite is highest and standard lowest within every channel. This pattern fits additive main effects, but additivity was not tested directly.

![Mean stay_rating per booking_channel x room_type on rated stays, with 95% CI from the per-cell standard error](tasks/stat_2/charts/stat2_rating_mean_by_channel_room.png)

**Within-channel room-type association.** Website chi-square = 37.7 (df = 8, p = 1e-5); direct chi-square = 15.99 (df = 8, p = 0.043); agency chi-square = 19.09 (df = 8, p = 0.014), with 26.7% of expected counts below 5. The source text calls the agency stratum "weaker and unreliable". Its chi-square (19.09) is larger than the direct one (15.99), so the "weaker" label rests on the sparsity caveat, not on the statistic. The differences in strength across channels were not tested as an interaction.

**Ordinal main effects with the rate covariate.** Without the rate covariate, the main effects (log-odds, agency and standard as reference) are: direct 1.26, website 1.22, suite 1.41 and superior 0.67. With the rate covariate they are: direct 1.26, website 1.22, suite 1.26 and superior 0.62. The rate covariate is 0.13 per 100 EUR (SE 0.39, p = 0.74). The suite effect shrinks from 1.41 to 1.26 and its SE rises from 0.19 to 0.49. The source reads this as overlap between the rate and the suite cell, which the data do not separate.

### 5. Share of code 99 by channel

Agency stays carry 99 at 32.2% (87 of 270). Non-agency stays carry 99 at 6.0%. Direct is 5.0% (16 of 320) and website is 7.1% (22 of 310). Room-type shares of 99 are standard 13.9%, suite 12.9% and superior 14.4%.

![Share of stays with stay_rating 99 per booking_channel; agency is the only grouping available (no agency id or date field)](tasks/eda_2/charts/eda2_share99_by_channel.png)

The dataset has no agency identifier and no date field. The share of 99 therefore cannot be broken down by individual agency or over time, and the task remains partial.

### 6. Predictive models

**Setup.** The models use the 775 rated stays. A stratified 80/20 split with seed 42 gives 620 training rows and 155 test rows. The feature matrix has 10 columns: three channel dummies, three room-type dummies and four numeric features. Numeric features are unscaled in the matrix, and logistic regression was standardised inside its fit. The majority-class baseline (always predicting rating 7) gets 43 of 155 test rows right, which is 27.74%.

**Scores (test set, n = 155):**

| Model | Test accuracy | Macro-F1 | Train accuracy |
|---|---|---|---|
| Majority baseline (rating 7) | 0.2774 | n/a | n/a |
| Logistic regression (balanced weights) | 0.1097 | 0.1069 | 0.1597 |
| Random forest (500 trees, balanced weights) | 0.2323 | 0.1315 | 1.0 |

Neither model beats the baseline on accuracy. The random forest's training accuracy of 1.0 indicates heavy overfitting.

**Per-class recall.** Logistic regression: rating 3 = 1.0 (on about 2 test rows), rating 4 = 0.0, rating 5 = 0.0435, rating 6 = 0.0667, rating 7 = 0.0698, rating 8 = 0.0667, rating 9 = 0.25, rating 10 = 0.4286. Random forest: rating 3 = 0.0, rating 4 = 0.0, rating 5 = 0.1304, rating 6 = 0.2, rating 7 = 0.4651, rating 8 = 0.1667, rating 9 = 0.125, rating 10 = 0.0.

![Left: test accuracy of each model against the majority-class baseline. Right: per-class test recall by stay_rating for logistic regression and random forest.](tasks/ml_2/charts/ml2_model_comparison.png)

**Grouped permutation importance (drop in test macro-F1).**

- booking_channel: logistic regression 0.0228 (sd 0.0159); random forest 0.0210 (sd 0.0156). Ranked first by both models.
- room_type: logistic regression -0.0051 (sd 0.0175); random forest 0.0073 (sd 0.0125).
- nightly_rate_eur: logistic regression -0.0175 (sd 0.0193); random forest 0.0075 (sd 0.0166).
- Lead time, nights and guests: all within noise, and mostly negative or near zero.

**Single-column importance (indicative only).** For the random forest, the agency column gives a drop of 0.0135 (sd 0.0098). For logistic regression it gives 0.0014 (sd 0.0103). No other single column shows a clear drop. The logistic regression coefficients are largest for nightly rate (x9), but its permutation drop is negative, so the coefficient does not show predictive value.

## Limitations

- **Code 99 and exclusion.** The sentinel-for-missing reading of 99 is a hypothesis and is not established. All rated analyses exclude the 125 code-99 stays, which are concentrated in agency bookings (32.2% of agency stays). The modelled set is therefore non-random, and the channel effects, the baseline and the model results may not transfer to the full dataset. The channel effects may partly reflect which stays were excluded.
- **Unresolved review issue on ml_2 (importance claims).** The lead's objection still stands. The random forest agency drop (0.0135, sd 0.0098) is roughly 1.4 sd from zero and should be read as suggestive, not clear, in the same way as the room-type results, which are at noise level. The grouped booking_channel drops (0.0228 and 0.0210, sd about 0.016) should be held to the same standard, or all grouped and single-column importances should be called uncertain. Single-column permutation of one-hot dummies breaks the group structure, so the per-column results are only indicative and the grouped results are the more reliable comparison. This affects the statements on booking-channel and room-type importance in section 6.
- **Association findings disagree with model findings.** The univariate tests (section 3) find significant associations with channel, room type and nightly rate. The models (section 6) do not beat the baseline, and nightly rate shows no permutation importance. Both sets of results are reported here, and this report does not resolve the disagreement.
- **Ordinal model.** The proportional-odds assumption was not checked for any model, so the single-coefficient reading per main effect may not hold across rating thresholds.
- **Power and sparse cells.** Several interaction cells are small (agency/suite n = 25; agency/standard at rating 9-10 n = 2). No formal power calculation was run, so the null interaction results cannot rule out moderate interactions. The permutation p-value of 0.0005 is the floor of that test.
- **Verification note on stat_3.** The source notes that the website interaction terms and the suite and superior standard errors were recorded in a prior report and should be checked against the full coefficient table, which was truncated in printed output. The values in this report are taken from the full coefficient table as recorded, and they have not been verified against a second source.
- **Inconsistent class count in the profile.** The profile header states 7 target classes, but nine values are listed (3 to 10 and 99). This report uses the nine listed values.
- **Incomplete eda_2.** The dataset has no agency identifier and no date field. The agency concentration of 99 cannot be tested by agency or over time, and whether a few agencies account for most 99 codes is unknown.
- **Small classes.** Ratings 3 and 4 have 9 and 19 rated stays. Per-class statistics for these classes are unstable, and the logistic-regression rating-3 recall of 1.0 rests on about 2 test rows.

## Open questions

- Does the agency share of 99 reflect unsubmitted ratings? Testing this needs an agency identifier and a field recording whether a rating was submitted. Neither is in the dataset.
- Does the agency share of 99 change over time or differ between agencies? Testing this needs a booking date and an agency identifier.
- Does the agency rating gap and the room-type pattern survive adjustment for the 99 flag or rated status?
- Do cross-validation estimates on all 775 rated stays give more stable scores than the 155-row test set, and does the weak signal persist?
- Do the importance results change when agency stays are removed?
- Can ordinal models or class-threshold tuning beat the majority baseline on accuracy while keeping recall for ratings 3, 4 and 10?
- Does a model that uses the agency channel or the 99 flag predict the 99 code well enough to matter for rating prediction?
- Is the agency stratum's room-type association weaker than the others once sparsity is addressed, and is the strength of room-type association different across channels? This was not tested as an interaction.
- Does the rate covariate overlap with the suite room type? This could be tested by fitting rate within room type or comparing models with and without a rate-by-suite term.
- Does the proportional-odds assumption hold? This could be checked with a partial-odds or per-threshold comparison.