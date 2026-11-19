# Stay Rating Analysis: 900-Row Stays Dataset, Target stay_rating

## Summary

- **Code 99 is probably a sentinel, not a rating, but this is not settled.** It makes up 13.9% of rows (125 of 900), and 69.6% of those rows are agency bookings. The cause of this agency concentration was not established.
- **On valid ratings (3 to 10, n = 775), booking_channel and room_type are significantly associated with stay_rating, and nightly_rate_eur is significantly associated too.** The effects are booking_channel V = 0.20 (moderate), room_type V = 0.19 (small to moderate) and nightly_rate_eur epsilon-squared = 0.06 (small). nights, guests and lead_time_days show no detectable association.
- **Agency has the lowest mean valid rating (6.21), against 7.17 for direct and 7.13 for website.** Agency is also the channel where 87 of its 270 rows were excluded as code 99, so this comparison rests on a non-random valid subset.
- **Neither the channel by room_type interaction nor the nights by nightly_rate_eur interaction is detectable.** Both were tested and neither is worth reporting as effect modification.
- **Models do not clearly beat the majority-class baseline.** Logistic regression reaches 0.276 test accuracy against a baseline of 0.240. Gradient-boosted trees match the baseline accuracy. All models used the full target including code 99, so their results are not clean measures of rating prediction.

## Data

- **Size:** 900 rows × 7 columns.
- **Target:** stay_rating, multiclass with 9 observed values: 3, 4, 5, 6, 7, 8, 9, 10 and 99. Shares: 7 at 23.9%, 8 at 16.9%, 6 at 16.6%, 99 at 13.9%, 5 at 12.8%, 9 at 9.2%, 10 at 3.7%, 4 at 2.1%, 3 at 1.0%. The target is imbalanced.
- **Features:** numeric: nights, guests, lead_time_days, nightly_rate_eur. Categorical: booking_channel, room_type.
- **Excluded columns:** none. There are no date or time features and no ids or free-text fields.
- **Missing values:** none. No cells are empty.

## Findings

### The value 99 (eda_1, stat_3)

- Code 99 has 125 of 900 rows (13.89%). Valid ratings 3 to 10 hold 775 of 900 rows, with 7 as the mode.
- Because 99 lies outside the 3 to 10 scale used by all other values, the analysis treats it as a likely sentinel for not-rated or missing stays. This is a working assumption, not a confirmed fact.
- Descriptive differences between 99 rows and other rows are small. Nights have a median of 5 for 99 rows and 6 for other rows. Guests have a median of 3 and 2 respectively. Lead time means are 40.53 and 39.65. Nightly rate means are 127.72 and 126.72. No significance test was run on these gaps.
- Booking channel is concentrated among 99 rows. Agency makes up 69.6% of 99 rows against 23.6% of other rows. Direct is 12.8% against 39.2%, and website is 17.6% against 37.2%. Room type shares are nearly identical: standard 49.6% against 49.7%, suite 14.4% against 15.7%, superior 36.0% against 34.6%.
- Within each channel, the share of rows coded 99 is 32.2% for agency (87 of 270), 7.1% for website (22 of 310) and 5.0% for direct (16 of 320).
- A Pearson chi-square test of independence on the booking_channel by (99 or not) table gives chi-square = 109.0, df = 2, p = 2.2e-24. Cramér's V is 0.348 on this table. Pearson residuals for the 99 cell are +8.08 for agency, −4.27 for direct and −3.21 for website. The excess of 99 rows sits in agency bookings. The cause is not established.

![Count of rows for each stay_rating value; 99 shown in grey](tasks/eda_1/charts/target_distribution.png)

### Rating rates by booking_channel and room_type (eda_2)

Figures are among valid rows (3 to 10).

| Booking channel | Valid rows | Mean rating | Share at 8 | Share at 9 | Share at 10 |
|---|---|---|---|---|---|
| Agency | 183 (of 270) | 6.21 | 10.9% | 3.8% | 1.1% |
| Direct | 304 (of 320) | 7.17 | 20.7% | 13.8% | 5.9% |
| Website | 288 (of 310) | 7.13 | 24.0% | 11.8% | 4.5% |

- Agency's 87 excluded rows are 69.6% of the 125 rows coded 99. The agency comparison therefore rests on a non-random valid subset.

| Room type | Valid rows | Mean rating | Share at 8 | Share at 9 | Share at 10 |
|---|---|---|---|---|---|
| Suite | 122 (of 140) | 7.71 | 27.1% | 18.9% | 9.8% |
| Superior | 268 (of 313) | 7.06 | 21.3% | 11.9% | 4.5% |
| Standard | 385 (of 447) | 6.60 | 16.1% | 7.3% | 2.3% |

- Mean nightly_rate_eur rises across adjacent rating classes, from 95.77 at rating 3 to 152.24 at rating 10.
- Mean lead_time_days falls from 43.95 at rating 4 to 33.82 at rating 10.
- Mean nights (5.44 to 5.94) and mean guests (2.22 to 2.58) show no clear trend across classes.
- These are descriptive means and shares. No significance test was run in this task.

![Percent of each booking_channel group in each valid stay_rating class (3-10); 99 excluded](tasks/eda_2/charts/eda2_rating_share_by_booking_channel.png)

![Percent of each room_type group in each valid stay_rating class (3-10); 99 excluded](tasks/eda_2/charts/eda2_rating_share_by_room_type.png)

### Feature associations with stay_rating (stat_1, stat_4)

Tests use valid ratings (3 to 10, n = 775). Holm adjustment covers the six tests jointly.

| Feature | Test | Statistic | Holm-adjusted p | Effect (95% bootstrap CI) |
|---|---|---|---|---|
| booking_channel | Chi-square, 14 df | 65.1 | 7.5e-8 | Cramér's V 0.205 (0.181 to 0.268), moderate |
| room_type | Chi-square, 14 df | 58.5 | 8.5e-7 | Cramér's V 0.194 (0.164 to 0.258), small to moderate |
| nightly_rate_eur | Kruskal-Wallis H = 50.9, 7 df | 50.9 | 5.7e-8 | Epsilon-squared 0.057 (0.035 to 0.101), small |
| nights | Kruskal-Wallis H = 1.4, 7 df | 1.4 | 1.0 | Epsilon-squared −0.007 (−0.006 to 0.015) |
| guests | Kruskal-Wallis H = 2.3, 7 df | 2.3 | 1.0 | Epsilon-squared −0.006 (−0.006 to 0.020) |
| lead_time_days | Kruskal-Wallis H = 6.0, 7 df | 6.0 | 1.0 | Epsilon-squared −0.001 (−0.005 to 0.025) |

- The booking_channel and room_type chi-square tests show a raw p of 1.5e-8 and 2.1e-7 respectively. The raw expected counts for ratings 3 and 4 are small, so these p-values are approximate.
- Robustness checks (stat_4), with ratings 3 and 4 merged and with a permutation test:
  - booking_channel: merged chi-square = 61.0 on 12 df, V = 0.198 (CI 0.171 to 0.256). Permutation p at most 0.0005.
  - room_type: merged chi-square = 57.8 on 12 df, V = 0.193 (CI 0.162 to 0.256). Permutation p at most 0.0005.
  - Both conclusions hold after merging and under permutation.
- Using all 900 rows, with code 99 kept as its own category:
  - booking_channel: chi-square = 165.9 on 16 df, V = 0.304 (CI 0.276 to 0.357). Merged: V = 0.300.
  - room_type: chi-square = 59.1 on 16 df, V = 0.181 (CI 0.160 to 0.243). Merged: V = 0.180.
  - Both remain significant with permutation p at most 0.0005.
- The all-rows and valid-row effects differ, most clearly for booking_channel (about 0.20 on valid rows, 0.30 on all rows). The cause of the difference is not established. Valid ratings exclude 87 agency rows, a non-random exclusion that may affect the valid-row effect. The all-rows and valid-row effects should therefore be read as bounds, not as a corrected estimate.
- Bootstrap intervals for the valid-row booking_channel effect differ slightly between the two tasks: 0.181 to 0.268 in stat_1 and 0.177 to 0.265 in stat_4.
- Kruskal-Wallis effects for nightly_rate_eur are 0.050 on all rows (CI 0.031 to 0.092) and 0.057 on valid rows.

![Effect sizes of each feature on stay_rating with 95% bootstrap CIs; booking_channel and room_type use Cramér's V, numeric features use epsilon-squared](tasks/stat_1/charts/assoc_effect_sizes.png)

### Interactions (stat_2)

- **booking_channel × room_type:** R² increment 0.003, F(4, 766) = 0.68, parametric p = 0.60, permutation p = 0.67. The bootstrap 95% CI for the increment is 0.001 to 0.020. The F and permutation tests find no interaction, but the CI lower bound excludes zero, so an increment up to about 0.02 R² cannot be ruled out.
- **nights × nightly_rate_eur:** R² increment 0.001, F(1, 771) = 0.96, parametric p = 0.33, permutation p = 0.37. Standardized interaction coefficient −0.051. Bootstrap CI for the increment 0.000003 to 0.009. An increment up to about 0.01 R² cannot be ruled out.
- Both interaction tests treat rating as numeric and do not use an ordinal model.
- Cell rates by booking_channel and room_type (25 to 156 rows per cell) vary in level, but the interaction test finds no reliable change in slope.

![Share of each stay_rating class within each booking_channel x room_type cell (valid ratings 3 to 10); cell sizes range from 25 to 156 rows.](tasks/stat_2/charts/interaction_class_rates_bc_rt.png)

### Predictive models (ml_1)

- Setup: one stratified 75/25 split, random_state 42, with 675 training rows and 225 test rows. The full target was used, including code 99 as its own class. Valid-only refits were not run.
- Majority-class baseline (predicts 7): accuracy 0.240, macro F1 0.043.
- Logistic regression: train accuracy 0.310, test accuracy 0.276, test macro F1 0.121, against the baseline accuracy of 0.240 and baseline macro F1 of 0.043. The gain comes from one split and has no interval, so it is suggestive, not established.
  - Largest absolute coefficients: booking_channel_agency 0.648, booking_channel_direct 0.379, nightly_rate_eur 0.376, booking_channel_website 0.347, room_type_suite 0.335, room_type_standard 0.293. nights 0.127, lead_time_days 0.107, guests 0.059.
- Gradient-boosted trees: train accuracy 0.600, test accuracy 0.240 (equal to baseline), test macro F1 0.168. The model was chosen by test macro F1 on the same split used to report it, so its score is optimistic. The gap between train and test accuracy shows overfitting.
  - Impurity importance: nightly_rate_eur 0.476, lead_time_days 0.241, booking_channel_agency 0.130, nights 0.094, guests 0.029.
  - Permutation importance (drop in test macro F1, 20 repeats): booking_channel_agency has the largest mean drop, 0.042 (sd 0.013). Among numeric features, guests is first at 0.027 (sd 0.009), then nightly_rate_eur at 0.027 (sd 0.012), lead_time_days at 0.020 (sd 0.016) and nights at 0.017 (sd 0.017).
- **These results disagree with stat_1.** stat_1 finds no detectable association for guests, lead_time_days or nights on valid ratings. The model importances rank guests, lead_time_days and nights highly. The ml_1 finding states that this ranking is driven by the 99 class and the overfit model and should not be read as guests mattering. Both results are reported here as they stand.

![Test accuracy and macro F1 for the baseline and two models, full stay_rating target](tasks/ml_1/charts/ml1_model_scores.png)

![Permutation importance for the gradient-boosted model on the test split, full stay_rating target](tasks/ml_1/charts/ml1_permutation_importance.png)

## Limitations

- **Code 99 is assumed to be a sentinel.** This rests on it lying outside the 3 to 10 scale. Its agency concentration (69.6% of 99 rows) is not explained, and the cause is not established. Whether 99 rows should be dropped or imputed was not tested.
- **Agency valid rows are a non-random subset.** 87 agency rows are excluded from all valid-row analyses. The valid-row and all-rows effects differ, and their cause is not established, so both should be read as bounds rather than a corrected estimate.
- **Unresolved review issue (stat_1), which still stands:**
  - The valid-row figures should not be treated as a corrected effect size. Valid ratings exclude 87 agency rows, a non-random exclusion that may affect the valid-row effect. Read the all-rows and valid-row effects as bounds.
  - The all-rows and valid-row effects differ, and the cause is not established.
  - Chi-square expected counts for ratings 3 and 4 may be small, so the booking_channel and room_type chi-square p-values are approximate. stat_4 checked this with merged ratings and a permutation test, and the conclusions held. The raw p-values are still reported above, so the caveat applies to them.
- **The model results use the full target, including 99.** Their scores and importances may reflect the 99 class rather than the features. A valid-only refit was not run.
- **Model evaluation is weak.** There is one split, no confidence intervals, and no separate validation set. The gradient-boosted model was selected on its test score and overfits. Logistic regression's gain over baseline is small and unquantified by any interval.
- **Rating is treated as numeric in the interaction tests.** No ordinal model or trend test was run.
- **Descriptive gaps are untested.** The 99-versus-other comparisons and the class means in eda_1 and eda_2 have no significance tests.
- **No task failed.** All tasks are marked complete.

## Open questions

- Does the 99 share vary by agency identity or over time? This would test whether the missingness is non-random.
- After controlling for booking_channel, does the 99 flag depend on guests or nights? Is the flag associated with booking_channel after controlling for room_type and nightly_rate_eur?
- Do the room_type, booking_channel and nightly_rate_eur conclusions change when the model is fit on valid ratings 3 to 10 only?
- Does an ordinal model or trend test (for example Jonckheere-Terpstra) on valid ratings give the same conclusions for nightly_rate_eur and booking_channel?
- Does excluding the 87 agency rows drive the gap between valid-row and all-rows booking_channel effects? How does the agency share change across ratings 3 to 10?
- Does the agency gap persist after controlling for room_type?
- Do the interaction results change when the 87 agency rows are included under a coding that does not treat them as missing?
- Do the nightly_rate_eur and room_type rating differences overlap, given that suite has both the highest rate and the highest rating?
- Does the lead_time_days decline at the top ratings hold after adjusting for booking_channel?
- Does the 99 class itself predict well from booking_channel and nightly_rate_eur?
- Do the models' gains over baseline hold across repeated stratified splits or cross-validation? Does a tuned gradient-boosted model, scored once on a held-out test set, change the picture?