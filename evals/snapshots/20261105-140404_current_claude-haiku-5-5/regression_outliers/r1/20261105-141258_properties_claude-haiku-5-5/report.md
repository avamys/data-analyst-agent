# Price Prediction from Size, Age and Rating: Analysis of a 600-Row Dataset (Target: price)

## Summary

- **Size is the one clearly associated feature.** Size_sqm correlates with price at Pearson r = 0.498 (95% CI 0.435 to 0.556) and Spearman rho = 0.887. The association holds in every specification tested.
- **Rating shows no significant association with price** on any test. Kruskal-Wallis p = 0.513, and the rating ordering changes with the location measure used.
- **Predictive models do not clearly beat the mean baseline.** On the 120-row test set, linear regression has test RMSE 273,535 against a baseline of 303,756, with test R² 0.189. Gradient boosting has RMSE 342,792 and test R² −0.274, and it overfits.
- **Price is strongly right-skewed** (mean 289,164, median 217,450, skewness 6.44), with 19 rows (3.2%) outside the 1.5×IQR fences. Those rows affect the mean-based comparisons.
- **Age has a small negative association with price that depends on the specification.** It is significant on Spearman rho and on log price, but not on the raw-price Pearson correlation.

## Data

- **Size:** 600 rows × 4 columns.
- **Target:** price (continuous regression target). Observed range 44,100 to 4,130,400.
- **Features:** three numeric features, size_sqm, age_years and rating. There are no categorical, date/time, identifier or free-text features.
- **Missing values:** none in any column.
- **Rating levels:** five, with 109 to 134 rows per level.

## Findings

### Price distribution and outliers

Price is strongly right-skewed. The mean is 289,164, the median is 217,450, the standard deviation is 322,321, and the skewness is 6.44. The minimum is 44,100 and the maximum is 4,130,400. Nineteen rows (3.2%) lie outside the 1.5×IQR fences (below −259,038 or above 749,663), and the maximum is far above the upper fence, so the mean is pulled up by the tail.

![Distribution of price: count of rows, linear and log10 scale](tasks/eda_1/charts/price_hist.png)

### Rating and price

Rating shows no significant association with price, and the ordering depends on how the location is measured.

| Rating | Count | Mean | Median | 5% trimmed mean | 10% trimmed mean |
|---|---|---|---|---|---|
| 1 | 109 | 286,769 | 237,100 | 255,266 | 249,845 |
| 2 | 112 | 250,008 | 184,150 | 236,001 | 227,178 |
| 3 | 118 | 291,622 | 204,600 | 252,987 | 242,028 |
| 4 | 127 | 253,302 | 217,200 | 237,287 | 229,883 |
| 5 | 134 | 355,663 | 227,200 | 278,440 | 266,563 |

- **Significance tests:** Pearson r = 0.066 (p = 0.104); Spearman rho = 0.034 (p = 0.403). Kruskal-Wallis H = 3.28 with 4 df (p = 0.513), with epsilon squared of −0.001, i.e. no measurable effect. One-way ANOVA on raw price gives F = 2.25 (p = 0.062, eta squared 0.015). On log price it gives F = 1.24 (p = 0.293, eta squared 0.008).
- **Ordering by measure:** The mean ranks ratings 5 > 3 > 1 > 4 > 2. Both trimmed means rank 5 > 1 > 3 > 4 > 2. The median and the median of log10(price) rank 1 > 5 > 4 > 3 > 2.
- **Log-price medians:** The median of log10(price) is 5.375 for rating 1 and 5.356 for rating 5 (rounded). The gap is about 0.02 log10 units, as stated in the review of this task. An earlier wording of a 0.01 gap is withdrawn; see Limitations.
- **Lowest rating:** Rating 2 is lowest under every location measure.
- **Disagreement:** Rating 5 has the highest mean and trimmed means, while rating 1 has the highest median and median log10. These findings disagree on the top position, and the analysis does not resolve which measure is right.

![Median price for each rating level](tasks/stat_1/charts/median_price_by_rating.png)

![Mean, 5% and 10% trimmed mean, and median of price per rating value, with counts 109 to 134 per rating](tasks/eda_2/charts/eda2_robust_price_by_rating.png)

### Size and price

Size is strongly associated with price.

- **Full data:** Pearson r = 0.498 (95% CI 0.435 to 0.556, p = 7.4e-39). Spearman rho = 0.887 (95% CI 0.869 to 0.903, p = 5.8e-203). The large Spearman value compared with Pearson is consistent with a monotone relation distorted by the high-price tail.
- **Excluding the 19 outliers:** Pearson r = 0.867 (95% CI 0.846 to 0.886, n = 581). Spearman rho = 0.917 (95% CI 0.903 to 0.929, n = 581). Excluding outliers truncates the outcome, so these coefficients are biased.
- **Log price:** Pearson r = 0.844 (95% CI 0.819 to 0.866, n = 600). Spearman is unchanged at 0.887 because ranks are invariant to the log transform.
- **Quartile means:** Mean price rises from 106,167 (smallest size quartile) to 202,297, 315,489 and 532,703 (largest). Medians are 94,650, 160,200, 265,000 and 452,900. Each quartile has 150 rows.
- **Linear slope:** On the 480 training rows, price rises by about 3,344 per square metre (95% CI 2,840 to 3,848, p ≈ 2e-33).

### Age and price

The age association is small and negative, and its significance depends on the specification.

- **Spearman:** rho = −0.157 (95% CI −0.234 to −0.078, p = 0.00011) on the full data. Excluding outliers gives rho = −0.159 (p = 0.00012).
- **Pearson, raw price:** r = −0.077 (95% CI −0.156 to 0.003, p = 0.061). Not significant at alpha 0.05.
- **Pearson, log price:** r = −0.147 (95% CI −0.225 to −0.068, p = 0.0003). Significant.
- **Pearson, excluding outliers:** r = −0.173 (95% CI −0.251 to −0.093, p = 2.7e-5, n = 581). This is biased by outcome truncation and is a secondary check only.
- **Quartile means:** Mean price is 317,557, 309,303, 251,963 and 277,834 from the youngest to oldest quartile. The pattern is not monotone. Medians are 237,600, 263,650, 187,800 and 205,000.

The findings disagree on whether the raw-price Pearson result is significant. Log price supports a significant negative association, while raw price does not. The analysis does not resolve this.

### Size-by-age and size-by-rating interactions

No interaction was detected.

- **Within-group slopes of log price on size_sqm (per sqm):**
  - Age young: 0.01192 (95% CI 0.01093 to 0.01292, r = 0.858, n = 202).
  - Age mid: 0.01270 (95% CI 0.01162 to 0.01378, r = 0.856, n = 198).
  - Age old: 0.01239 (95% CI 0.01129 to 0.01349, r = 0.845, n = 200).
  - Rating low (1–2): 0.01213 (95% CI 0.01121 to 0.01306, r = 0.868, n = 221).
  - Rating high (3–5): 0.01242 (95% CI 0.01158 to 0.01326, r = 0.832, n = 379).
  - All five slopes are positive and significant (p < 0.001).
- **Interaction tests on log price:** Size × age (continuous) has p = 0.604, and adding it raises R² only from 0.7344 to 0.7345. Size × rating (high vs low) has p = 0.487.
- **Interaction tests on raw price:** Size × age has p = 0.694, and size × rating has p = 0.278.

![Within-group size slope on log price with 95% CI, by age tertile and rating group](tasks/stat_2/charts/stat2_slopes.png)

### Predictive models

Both models were evaluated on a single 120-row test split (seed 42, 480 training rows). Neither clearly beats the mean baseline.

| Model | Test RMSE | Test MAE | Test R² | Train R² |
|---|---|---|---|---|
| Mean baseline (training mean 290,012) | 303,756 | 165,645 | — | — |
| Linear regression | 273,535 | 102,395 | 0.189 | 0.270 |
| Gradient boosting | 342,792 | 122,790 | −0.274 | 0.922 |

- **Linear regression** has lower RMSE and MAE than the baseline. The margin rests on a 120-row test set, so it is not established as a clear margin.
- **Gradient boosting** has higher RMSE than the baseline and a train R² of 0.922 against a test R² of −0.274, which indicates overfitting on the 480 training rows.
- **Permutation importance (linear model, increase in test RMSE):** size_sqm 70,636 (sd 11,423); age_years 2,866 (sd 1,798); rating 484 (sd 2,144), which is indistinguishable from zero.
- **Gradient boosting importances:** size_sqm 0.578, age_years 0.380, rating 0.042.
- **Linear coefficients:** These are on unscaled features and are not a ranking of importance. Rating has the largest absolute coefficient (13,363), but its permutation importance is near zero.

The weak RMSE fit is partly consistent with the right-skewed, outlier-heavy price. The effect of the outliers on the comparison is untested. These results do not show that size, age and rating explain little of price in general.

![Test RMSE of the mean baseline, linear regression and gradient boosting on the 120 test rows](tasks/ml_2/charts/ml2_model_rmse.png)

## Limitations

- **Outliers:** The 19 high-price rows (3.2%) were kept in most analyses. The only outlier-excluded results (stat_3) truncate the outcome and are biased. Log-price results are the more defensible robustness check. Whether these rows are data errors or genuine listings is unknown.
- **Unresolved review issue (eda_2), affecting the rating findings:**
  - The earlier statement that rating 1 exceeds rating 5 on median log10(price) by 0.01 log10 units (about 3%) is incorrect. The reviewer states the gap is about 0.02 log10 units. The corrected values are 5.375 for rating 1 and 5.356 for rating 5.
  - The claim that all groups are large enough for the trimmed means and medians to be stable is withdrawn, because no stability check was run. The report states only that counts are 109 to 134 per rating.
  - The eda_2 rating ordering is therefore reported without a stability assessment.
- **Test set size:** Model comparisons use a single 120-row test split. Margins over the baseline are not established as clear.
- **Model features:** The models use only size_sqm, age_years and rating. Test R² is low, and the analysis does not test whether additional predictors would help.
- **Interaction tests:** They use log price with age as a continuous term, and the 19 outliers were not excluded.
- **Spearman intervals:** All Spearman confidence intervals are Fisher-z approximations, not exact intervals.
- **Age specification dependence:** The age association is significant on Spearman and log price but not on raw-price Pearson. The findings disagree and are reported as such.
- **Associations only:** All results are associations. No causal interpretation is supported.
- **Failed tasks:** None. All seven tasks were accepted as complete.

**Numbers not traced to a recorded fact.** The automatic check found no recorded value for these numbers:
- 0.02 in: "- **Log-price medians:** The median of log10(price) is 5.375 for rating 1 and 5.356 for rating 5 (rounded). The gap is about 0.02 log10 units, as stated in the "
- 0.02 in: "- The earlier statement that rating 1 exceeds rating 5 on median log10(price) by 0.01 log10 units (about 3%) is incorrect. The reviewer states the gap is about "

## Open questions

- Does size explain the rating differences once size is controlled, and does age remain negatively associated with price after controlling for size (partial correlation or multiple regression)?
- Is the gap between rating 1 and rating 5 distinguishable from zero under a bootstrap of trimmed means and medians?
- Do the high-priced rows concentrated in rating 5 come from a few listings, and are the 19 high-price outliers data errors or genuine luxury listings?
- Does the size slope differ by age on raw price after excluding the outliers?
- Would a log-price target, evaluation that excludes or down-weights the largest prices, or cross-validation rather than a single split change the comparison with the mean baseline?
- Would a regularised or tuned gradient boosting model avoid the overfitting observed?
- Would more predictors or more rows be needed to explain price well?
- How do bootstrap or exact rank-based intervals compare with the Fisher-z approximations used for the Spearman intervals?