# Listing Price Analysis: Predicting Price (Target) from size_sqm, age_years and rating

## Summary

- **Size is the only strong predictor.** Size_sqm has a Spearman correlation with price of 0.887 (95% bootstrap CI 0.857 to 0.911). Age_years has a weak negative association (rho = -0.157), and rating shows no detectable association (rho = 0.034, p = 0.40).
- **Linear regression beats the mean baseline but explains little variance.** On the 120-listing test set, test RMSE is 273,535 against 303,756 for the baseline, and test R2 is 0.189. Size_sqm is by far the most important feature in permutation importance (drop in test R2 of 0.474).
- **Six listings above the 99th percentile look suspect.** Each is priced between 1,927,100 and 4,130,400, while its size_sqm, age_years and rating are in the range of the other listings. A log-price model fit on the other 594 listings predicts them at about 7.0 to 11.2 times lower than their actual prices. The evidence does not show they are genuine, and they remain unverified.
- **No significant size-by-age interaction.** The size-price correlation is strong in both age halves (rho 0.883 and 0.907), and the difference between them is not significant.
- **No significant rating 5 vs rating 1 difference.** This holds on the raw mean, on log price and on the 10% trimmed mean, both with and without the six suspect listings.

## Data

- **Size:** 600 rows × 4 columns.
- **Target:** price, a continuous variable. It is strongly right-skewed (skewness 6.44 raw, 0.35 after log transform), with mean 289,164, median 217,450 and maximum 4,130,400.
- **Features:** three numeric features (size_sqm, age_years, rating). There are no categorical, date/time, id or free-text features.
- **Missing values:** none.

## Findings

### Price distribution and outliers

- Price is strongly right-skewed. The mean (289,164) sits well above the median (217,450). Quartiles are 119,225 (Q1) and 371,400 (Q3), with std 322,321. The range runs from 44,100 to 4,130,400.
- Six listings (1% of 600) lie above the 99th percentile of 1,591,094. The maximum is far beyond this threshold.
- Log price is close to symmetric (skewness 0.35), compared with 6.44 for raw price.

![Price and log-price distributions: counts of listings per bin](tasks/eda_1/charts/price_histograms.png)

### Price by rating, and by binned size and age

- **Size:** Mean and median price rise across the four size quartile bins (150 listings each).
  - Mean: 106,167 (Q1), 202,297 (Q2), 315,489 (Q3), 532,703 (Q4).
  - Median: 94,650, 160,200, 265,000, 452,900.
- **Age:** The pattern is not monotonic.
  - Mean: 317,557 (Q1), 309,303 (Q2), 251,963 (Q3), 277,834 (Q4).
  - Median: 237,600, 263,650, 187,800, 205,000.
- **Rating:** The pattern is not monotonic.
  - Mean: 286,769 (1), 250,008 (2), 291,622 (3), 253,302 (4), 355,663 (5), with counts of 109, 112, 118, 127 and 134.
  - Median: 237,100, 184,150, 204,600, 217,200 (4), 227,200 (5). Rating 5 has the highest mean, but its median is close to the others.

![Mean price per rating value, bars show the mean of all listings with that rating](tasks/eda_2/charts/eda2_mean_price_by_rating.png)

![Scatter of price against size_sqm for all 600 listings](tasks/eda_2/charts/eda2_price_vs_size_scatter.png)

### Association tests and effect sizes

- **Size_sqm:** Spearman rho = 0.887 (95% bootstrap CI 0.857 to 0.911, p = 5.8e-203).
- **Age_years:** Spearman rho = -0.157 (95% bootstrap CI -0.233 to -0.083, p = 0.00011).
- **Rating:** Spearman rho = 0.034 (95% bootstrap CI -0.047 to 0.115, p = 0.40).
- **Rating groups:** Kruskal-Wallis H = 3.28 with 4 df, p = 0.51. Epsilon-squared = 0.0055, a negligible effect.
- **Rating 5 vs rating 1 (raw mean):** The difference is 68,895 (355,663 vs 286,769). The Welch 95% CI runs from -28,836 to 166,626 and includes zero. This comparison was not rerun on log price or a trimmed mean at this stage.
- **Per-group means with 95% CIs:** rating 1, 286,769 (237,774 to 335,763); rating 2, 250,008 (218,216 to 281,800); rating 3, 291,622 (228,894 to 354,350); rating 4, 253,302 (222,823 to 283,781); rating 5, 355,663 (271,753 to 439,574).

![Mean price per rating level; bars show the mean with a 95% CI (normal approximation)](tasks/stat_1/charts/stat1_mean_price_by_rating.png)

### Size-by-age interaction

- Age was split at its median (30.1) into two halves of 300 listings each.
- **Younger half:** Spearman rho = 0.883 (95% CI 0.830 to 0.921).
- **Older half:** Spearman rho = 0.907 (95% CI 0.876 to 0.930).
- **Difference in correlations:** Young minus old = -0.025. Fisher z = -1.53, p = 0.127. The approximate 95% CI runs from -0.278 to 0.036. This treats Spearman as Pearson on the Fisher scale, so it is approximate.
- **Price-scale OLS interaction (size × older half):** -15.6 per sqm (95% CI -920 to 889), p = 0.97. This estimate may be driven by a few large prices.
- **Rank-based interaction (ranked size and price):** 0.024 (95% CI -0.046 to 0.095), p = 0.50.
- Overall, no significant interaction was detected. Moderate differences in slope or correlation cannot be ruled out.

![Scatter of price against size_sqm, coloured by age_years half](tasks/stat_2/charts/stat2_size_price_by_age_half.png)

### Predictive performance and feature importance

- Models were evaluated on one train/test split (480 training listings, 120 test listings).
- **Mean baseline:** test RMSE 303,756, test MAE 165,645, test R2 -0.0002.
- **Linear regression:** test RMSE 273,535, test MAE 102,395, test R2 0.189 (train R2 0.270). It beats the baseline on RMSE and MAE, but explains a modest share of price variation.
- **Gradient boosting:** train R2 0.922 but test R2 -0.274, with test RMSE 342,792. It overfits and is worse than the baseline.
- Linear regression was selected as the best model by test R2, and its permutation importance on the test set (drop in test R2) is:
  - size_sqm: 0.474 (sd 0.085)
  - age_years: 0.017 (sd 0.011)
  - rating: 0.003 (sd 0.013), indistinguishable from zero
- The linear coefficient ranking puts rating first, but the features are on different scales, so this ranking is not comparable.

![Test RMSE of price by model; lower is better. Baseline predicts the training mean.](tasks/ml_1/charts/ml1_model_test_rmse.png)

### The six listings above the 99th percentile

- The six listings (threshold 1,591,094) are listed below as price; size_sqm; age_years; rating.
  - 523: 4,130,400; 185.8; 44.9; 5.0
  - 44: 3,485,400; 170.7; 27.9; 3.0
  - 24: 2,628,000; 159.1; 30.8; 5.0
  - 508: 2,451,700; 169.3; 57.7; 5.0
  - 198: 2,228,000; 139.3; 8.1; 5.0
  - 412: 1,927,100; 102.1; 33.5; 1.0
- A log-price model fit on the other 594 listings (R2 = 0.79, using size_sqm, age_years and rating) gives actual-to-predicted price ratios of 9.5 (523), 8.5 (44), 7.6 (24), 7.5 (508), 7.0 (198) and 11.2 (412).
- Price per sqm for the six ranges from 14,481 (508) to 22,230 (523). For the other 594 listings, the median is 1,986, the p99 is 8,079 and the maximum is 15,587. All six exceed the others' p99. Five exceed the others' maximum; 508 does not.
- **Verdict:** The six listings most likely reflect data errors (for example a unit, currency or entry error) or an unexplained premium segment. The evidence does not show they are genuine, and they should be verified against the source before being kept in modelling. The ratios are not a single clean factor, so a simple unit error is not proven.

![Price against size_sqm; red points are the six listings above the p99 price threshold](tasks/eda_3/charts/eda3_top_scatter.png)

### Rating 5 vs rating 1: robustness checks

- **Log price, all listings:** The mean log difference (rating 5 minus rating 1) is 0.0976, a ratio of about 1.10. The Welch 95% CI is -0.096 to 0.291 (n = 109 for rating 1, 134 for rating 5). It includes zero.
- **10% trimmed mean, all listings:** The difference is 16,718 (266,563 for rating 5, 249,845 for rating 1). The bootstrap 95% CI is -31,839 to 69,858. It includes zero.
- **Sensitivity, six listings excluded (n = 108 for rating 1, 130 for rating 5):**
  - Log difference 0.0425, a ratio of about 1.04, 95% CI -0.135 to 0.220.
  - Trimmed mean difference 8,089 (255,047 for rating 5, 246,958 for rating 1), 95% CI -38,172 to 56,395.
- Neither CI excludes zero in either analysis. Both point estimates shrink toward zero when the six listings are excluded.
- The main results depend on the six listings being valid, which is unverified. The sensitivity estimates, which exclude them, are the safer reading. Listing 523 (rating 5, price 4,130,400) is one of the six and sits in the rating 5 group.

![Rating 5 minus rating 1 differences with 95% CIs: mean log price (left, log units) and 10% trimmed mean price (right, thousands)](tasks/stat_3/charts/stat3_rating_diff_ci.png)

## Limitations

- **Suspect prices.** Price is heavily right-skewed (skewness 6.44). Six listings above the p99 threshold are unverified and may be errors. Mean-based and squared-error results, including the price-scale regression and the raw-mean rating comparison, are sensitive to them.
- **Unresolved review issue (eda_3).** The size_sqm, age_years and rating values for listings 24, 198, 508 and 412 are not fully reported in the eda_3 findings, and the rest-of-data ranges for these three features are not stated. The claim that the six listings' features fall within the ranges of the other listings therefore cannot be fully checked.
- **Unresolved review issue (stat_3).** The main rating 5 vs rating 1 results depend on the six listings being valid, which is unverified. The sensitivity estimates, which exclude them, are the safer reading. eda_3 found that the evidence does not show the six listings are genuine.
- **Single split, small test set.** The test set has 120 listings. Model choice was made by test R2, so the test scores are slightly optimistic. No cross-validation was run.
- **Model scale.** The predictive models and the raw-mean rating comparison in stat_1 use raw price. The log-price and trimmed-mean checks are reported in stat_3 and the log-price model in eda_3 only.
- **Approximate tests.** The Fisher z comparison of Spearman correlations is approximate. The price-scale interaction estimate may be driven by extreme prices.
- **Power.** Group sizes of 108 to 134 may be too small to detect a 10% difference between ratings 1 and 5. This was raised but not tested.
- **Weak predictive gain.** Test R2 is 0.189, so most price variation is not explained by these three features.
- **Failed tasks.** None. All seven analysis tasks are marked complete.

## Open questions

- Are the six listings above the p99 threshold valid? Do the source records show currency, unit or keying errors?
- Is there a separate premium segment that explains the high price-per-sqm listings? Do those listings differ in other fields?
- Do the top 1% of listings cluster in rating 5, and does the rating 5 mean gap come from a few high-priced listings?
- Does the size_sqm association remain after controlling for age_years and rating in a multiple regression, with diagnostics?
- Does the rating 5 vs rating 1 gap persist after adjusting for size_sqm and age_years in a regression on log price?
- Does the size-by-age interaction hold on log price and when the extreme listings are removed?
- Is the relationship between size_sqm, age_years, rating and log price linear after the transform?
- Would a cross-validated comparison, or a regularised or scaled model, give more reliable test estimates than a single split?
- Is the study underpowered to detect a 10% price difference between ratings 1 and 5?