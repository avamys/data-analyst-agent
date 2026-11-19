# Price Prediction from Size, Age and Rating: Distribution, Associations, Interactions and Models (600 Properties)

## Summary

- **Size is the only strong driver of price.** Size's Spearman correlation with price is 0.887 (95% CI 0.869 to 0.903). Median price rises from 90,850 in the lowest size quintile to 474,000 in the highest. Rating shows no significant association with price (Kruskal-Wallis p = 0.513, epsilon-squared effectively zero).
- **Age has a weak negative association with price.** Its Spearman rho is -0.157 (95% CI -0.234 to -0.078, p = 0.00011, n = 600). The age effect shows no detectable dependence on size or rating jointly (joint interaction test p = 0.708).
- **The best model has limited skill.** Linear regression on the three raw features reaches test R2 0.189, against 0.000 for the mean baseline. The random forest overfits (train R2 0.865, test R2 0.017, five-fold CV R2 averaging -0.037).
- **Three high-price test rows account for most of the test error.** The 19 rows above the upper fence of 749,662.5 are unevenly split between train (16) and test (3). The three above-fence test rows account for 91.0% of linear regression's test squared error. With the 19 rows removed from train and test, linear regression reaches test R2 0.806.

## Data

- 600 rows and 4 columns: `size_sqm`, `age_years` and `rating` as numeric features, and `price` as the continuous regression target.
- No categorical, date/time, id or free-text columns. All three features were used directly. Rating is a 1 to 5 level and was analysed as numeric in the correlation and model work.
- No missing values in any column.
- Price is heavy-tailed: mean 289,164, median 217,450, skew 6.44, range 44,100 to 4,130,400. The log10 scale has skew 0.35.
- The fixed 80/20 split used for modelling has 480 training rows and 120 test rows (random_state 42, no overlap).

## Findings

### Price distribution and outliers

Price is strongly right-skewed. Its quartiles are 119,225 (Q1), 217,450 (median) and 371,400 (Q3). The 5th and 95th percentiles are 70,465 and 628,625.

Using the 1.5 IQR rule (IQR 252,175), the upper fence is 749,662.5 and the lower fence is -259,037.5. This flags 19 outliers, 3.17% of rows. All 19 lie above the upper fence, and the smallest is 766,900. None fall below the lower fence.

On a log10 scale, skew falls from 6.44 to 0.35. Log price is much less skewed than raw price but not perfectly symmetric.

![Distribution of price on raw and log10 scales](tasks/eda_1/charts/price_histograms.png)

### Price by size, age and rating

**Size.** Price rises steeply across size quintiles. Mean and median price are:

| Size quintile | Mean | Median |
|---|---|---|
| Q1 | 102,376 | 90,850 |
| Q2 | 154,503 | 137,950 |
| Q3 | 249,433 | 215,900 |
| Q4 | 391,283 | 327,150 |
| Q5 | 548,226 | 474,000 |

Size's Spearman correlation with price is 0.887 (95% CI 0.869 to 0.903, p = 5.8e-203, n = 600). Its Pearson correlation is 0.498.

Dropping the 19 outliers (n = 581) gives a size Spearman of 0.917 (p = 2.7e-233). The Pearson correlation of size with log(price) is 0.844 (p = 5.1e-164). The size result therefore does not depend on the outliers.

![Scatter of price against size_sqm](tasks/eda_1/charts/price_vs_size.png)

**Age.** Age has little relation to price. Its Pearson correlation with price is -0.077 and its Spearman correlation is -0.157 (95% CI -0.234 to -0.078, p = 0.00011, n = 600). The lowest age quintile has mean 329,558 and median 240,150. The highest age quintile has mean 253,106 and median 202,000. The middle quintiles do not follow a consistent order.

After dropping the 19 outliers (n = 581), the age Spearman is -0.159 (p = 0.00012). The Pearson correlation of age with log(price) is -0.147 (p = 0.0003). The age association is not driven by the outliers.

**Rating.** Rating levels have fairly even counts: 109, 112, 118, 127 and 134 for levels 1 to 5. Mean and median price by level are:

| Rating | n | Mean | Median |
|---|---|---|---|
| 1 | 109 | 286,769 | 237,100 |
| 2 | 112 | 250,008 | 184,150 |
| 3 | 118 | 291,622 | 204,600 |
| 4 | 127 | 253,302 | 217,200 |
| 5 | 134 | 355,663 | 227,200 |

Price shows no consistent monotone pattern with rating. Rating's Spearman correlation with price is 0.034 and its Pearson correlation is 0.066.

### Significance and effect sizes

**Rating.** The Kruskal-Wallis test finds no significant difference in price across the five rating levels (H = 3.28, df 4, p = 0.513, n = 600). Epsilon-squared is -0.001, so rating explains essentially none of the price variation.

Mean price has 95% t intervals and median price has bootstrap intervals:

| Rating | Mean (95% CI) | Median (95% CI) |
|---|---|---|
| 1 | 286,769 (237,220 to 336,317) | 237,100 (187,400 to 267,900) |
| 2 | 250,008 (217,866 to 282,150) | 184,150 (157,300 to 243,150) |
| 3 | 291,622 (228,240 to 355,004) | 204,600 (181,700 to 256,250) |
| 4 | 253,302 (222,528 to 284,076) | 217,200 (168,700 to 250,100) |
| 5 | 355,663 (270,984 to 440,343) | 227,200 (193,950 to 264,150) |

The rating 5 mean is higher than the other levels' means, but its median is not higher, and the intervals overlap. No significant difference is shown.

![Mean and median price with 95% confidence intervals for each rating level](tasks/stat_1/charts/rating_price_ci.png)

**Size and age.** Size's Spearman correlation with price is 0.887 (95% CI 0.869 to 0.903). Age's Spearman correlation is -0.157 (95% CI -0.234 to -0.078), a weak negative association.

### Does age's effect depend on size or rating?

- **Age × size.** The interaction is not significant. Its coefficient is 0.0000089 per sqm-year (95% CI -0.0000284 to 0.0000461, p = 0.64).
- **Age × rating.** The single-coefficient interaction is not significant. Its coefficient is 0.000428 per rating point (95% CI -0.000864 to 0.001721, p = 0.52).
- **Joint test.** Both interaction terms together give F(2, 594) = 0.346, p = 0.708. The age effect on log(price) does not depend on size or rating jointly.
- **Tertile slopes (descriptive only).** Slopes of log(price) on age are -0.00631 (low size, 95% CI -0.00989 to -0.00273, n 201), -0.00525 (mid size, -0.00884 to -0.00166, n 199) and -0.00569 (high size, -0.00913 to -0.00224, n 200). These agree with the non-significant interaction and are not the basis for the conclusion.
- **Rating omnibus test.** The categorical age × rating-level interaction, adjusted for size and age × size, is not significant (F(4, 588) = 1.35, p = 0.249).
- **Rating 4 contrast (post hoc).** The extra age slope for rating 4 is 0.00473 (95% CI 0.00035 to 0.00910, p = 0.034). It was chosen after viewing the slopes and is not corrected for five rating levels. The omnibus test does not confirm it, so it is a hypothesis, not an established difference.
- **Within-rating slopes.** All five rating-level slopes of log(price) on age are negative: rating 1 -0.00927 (95% CI -0.01747 to -0.00108), rating 2 -0.00823 (-0.01588 to -0.00058), rating 3 -0.00607 (-0.01408 to 0.00194), rating 4 -0.00143 (-0.00855 to 0.00569) and rating 5 -0.00886 (-0.01710 to -0.00061). The rating 3 and rating 4 intervals include zero. All intervals overlap heavily, and the omnibus test shows no established difference in age slope across ratings.
- **Main age coefficient.** The age coefficient in the interaction model is -0.00882 (95% CI -0.01483 to -0.00281, p = 0.004). It is the slope at size 0 and rating 0, outside the data range, so it is not an average age effect. The unadjusted age Spearman (-0.157) is the more direct summary.

![Slope of log(price) on age_years with 95% CI, within size_sqm tertiles and within each rating level](tasks/stat_2/charts/age_slopes_forest.png)

### Rating and size together

Rating is nearly independent of size. Its Spearman correlation with size is 0.028, and mean rating by size quintile ranges from 2.97 (Q5) to 3.38 (Q4).

Within size quintiles, the rating-price Spearman correlations are mixed in sign: Q1 -0.136, Q2 0.151, Q3 -0.028, Q4 -0.025 and Q5 0.129. Cells contain about 14 to 37 rows, so most are too small for firm conclusions. The Q1 mean gap across ratings is driven by a few high values. Trimming the top and bottom 10% of each cell shifts the Q1 rating 3 mean from 142,043 to 98,179. The Q1 medians rise only from 85,400 (rating 1) to 97,150 (rating 3).

This analysis is partial. A firm test of rating after adjusting for size was not completed (see Limitations).

![Median price by size quintile for each rating level](tasks/eda_2/charts/rating_by_size_median.png)

### Model comparison (fixed 80/20 split)

Test-set results, with the mean baseline as reference:

| Model | Test RMSE | Test MAE | Test R2 |
|---|---|---|---|
| Mean baseline | 303,756 | 165,645 | 0.000 |
| Linear regression (raw price) | 273,535 | 102,395 | 0.189 |
| Random forest (raw price) | 301,080 | 108,882 | 0.017 |
| Random forest (log10 target) | 280,833 | 91,297 | 0.145 |

- **Linear regression** has the best test R2 and RMSE among raw-price models. Its train R2 is 0.270.
- **Random forest** overfits. Its train R2 is 0.865 against test R2 0.017. Its five-fold CV R2 on the training set averages -0.037 (sd 0.133), with folds from -0.205 to 0.179. Predictive skill from these three features is weak and unstable.
- **Log-target random forest** has the lowest MAE of the models tried (91,297), but its R2 (0.145) is below linear regression's. The log target helps MAE more than R2.

![Test-set R2 for mean baseline, linear regression and random forest predicting price](tasks/ml_1/charts/ml_1_model_r2.png)

### Feature importance

The random forest is not the best model on test, so its importances describe a model with almost no test skill.

- **Permutation importance (test set, random forest, 30 repeats).** Size's mean drop in test R2 when shuffled is 0.397 (sd 0.108), the only real positive signal. Age (mean -0.086, sd 0.043) and rating (mean -0.097, sd 0.038) have negative importance. Shuffling them does not reduce test R2.
- **Standardised linear coefficients (change in price per 1 SD).** Size is 165,767, rating 18,620 and age -20,511. The earlier ranking by unstandardised coefficients is withdrawn because those coefficients are in different units.
- **Agreement.** Permutation importance and standardised coefficients give the same order (size, then age, then rating). Only size's importance is a real positive signal, so the agreement on age and rating is not evidence of their importance.
- **Partial dependence (training data of an overfit forest).** Predicted price rises with size from 81,757 at 38.6 sqm to 535,871 at 190.7 sqm. It falls with age from 331,839 at 4.4 years to 269,138 at 56.5 years. These curves may not reflect test behaviour.

![Left: permutation importance of each feature for the random forest on the test set. Right: partial dependence of predicted price on size_sqm and age_years.](tasks/ml_2/charts/ml_2_importance_and_pdp.png)

### Effect of the high-price outliers on model results

Sixteen of the 19 above-fence rows are in training and 3 are in the 120-row test set. The three test rows account for 91.0% of linear regression's test squared error and 78.7% of the random forest's.

| Scenario | Baseline RMSE | Linear RMSE | RF RMSE | Linear R2 | RF R2 |
|---|---|---|---|---|---|
| All rows | 303,756 | 273,535 | 301,080 | 0.189 | 0.017 |
| Outliers removed from train and test (117 test rows) | 145,838 | 64,262 | 65,747 | 0.806 | 0.797 |
| Outliers removed from train only (120 test rows) | 305,929 | 274,303 | 273,379 | 0.184 | 0.190 |

- With all rows, linear regression has the lower test RMSE.
- With outliers removed from both sets, linear regression has the lower RMSE (64,262 vs 65,747) and higher R2 (0.806 vs 0.797). The random forest has the lower MAE (46,752 vs 50,347).
- With outliers removed from train only, the random forest has a marginally lower RMSE (273,379 vs 274,303). The report does not treat this difference as meaningful.

![Test RMSE of the mean baseline, linear regression and random forest with all rows, without the 19 upper-fence outliers in train and test, and without them in train only](tasks/ml_3/charts/ml_3_rmse_by_scenario.png)

## Limitations

- **Heavy-tailed target and small test set.** Price has a skew of 6.44. Nineteen rows lie above the upper fence, and only three of them fall in the 120-row test set. Test RMSE and R2 are therefore dominated by a few rows, and the model comparison is sensitive to the split.
- **Outlier-removed scores are not directly comparable.** The models with outliers removed were evaluated on a subset defined by the price distribution, so their scores are not directly comparable with the all-rows scores.
- **Random forest overfitting.** Train R2 is 0.865 against test R2 0.017. Shallower or regularised forests were not tested. The importances from this forest have limited meaning.
- **Rating analysis is incomplete (eda_2, status partial).** The rating-by-size analysis relies on small cells (about 14 to 37 rows). A firm test of rating after adjusting for size was not completed. The rating null result is therefore supported by the unadjusted tests and the near-zero rating-size correlation, not by an adjusted model.
- **Rating 4 contrast is a single post hoc comparison.** The rating 4 flat-slope result (extra slope 0.00473, p = 0.034) was chosen after viewing the slopes, is not corrected for multiple comparisons, and is not supported by the omnibus test (p = 0.249).
- **Interpretation of the age coefficient.** The main age coefficient in the interaction model refers to size 0 and rating 0, outside the data range.
- **Unresolved review issues.**
  - stat_1: the review asked for the 95% CI of the age Spearman correlation to be added beside rho -0.157. The interval (-0.234 to -0.078) is now reported there. The review remains formally unresolved, and the lead's objection stands for the age finding.
  - stat_2: the review asked for a correction to the description of the within-rating age slopes. The text now states that all five are negative, that the rating 3 and rating 4 intervals include zero, and that the intervals overlap heavily. The conclusion of no established difference in age slope across ratings is unchanged. The review remains formally unresolved, and the lead's objection stands for the rating-slope finding.
- **Failed or incomplete tasks.** eda_2 (rating confounding by size) is partial, as described above. No other task failed.
- **Other limits.** The three features are used in raw form in the predictive models. No nonlinear or size interaction term was fitted in those models. Results are for these 600 rows and these three features only.

## Open questions

- Does a model with size and rating jointly, or on log price, detect a small rating effect that the quintile cells are too small to show?
- Is the rating null result confounded by size once size is adjusted for explicitly (for example with size as a covariate or with size tertiles as strata)?
- Is the rating 4 flat age slope real, or a chance result of post hoc comparison? Does it replicate on new data or with a pre-specified contrast?
- Does age interact with size in its effect on price beyond the linear interaction tested?
- Is the high-price tail above 749,662.5 a distinct population that should be modelled separately, or handled with a log-price or quantile model? Is it concentrated in particular rating levels or the largest size quintile?
- Does a linear model on log10(price) with a size × age interaction beat the raw-price linear model on test?
- Would a shallower or regularised random forest generalise better, and would the model ranking change once the outliers are handled?
- Would a nonlinear term on size (for example a spline) or derived features explain more variance than the three raw features, especially in the non-outlier rows where linear regression reaches R2 0.806?