# Price Drivers in a 600-Property Sample: Size, Age and Rating Against Price

## Summary

- **Size is the dominant association with price.** Spearman rho with price is 0.887 (95% CI 0.869 to 0.903). On the held-out test split, linear regression on size, age and rating reaches R² 0.234 against -0.006 for a mean baseline. Size accounts for most of that gain (permutation importance 0.436 in test R²).
- **Rating shows no detectable effect on price.** The Kruskal-Wallis test across rating levels gives p=0.51 (epsilon-squared 0.005). After adjusting for size and age, the joint test on log(price) gives p=0.13.
- **Age has a small negative association that survives adjustment on the log scale.** Holding size and rating constant, log(price) falls by 0.64% per year (95% CI -0.82% to -0.46%). On the raw price scale, the oldest-versus-newest tercile difference is not significant (p=0.10).
- **Size effects do not differ detectably by age or rating.** Joint interaction tests are non-significant on both log(price) and price (age p=0.53 on log scale; rating p=0.35 on log scale).
- **Model residuals are heavy-tailed, and the tail is not explained.** The 10 largest residuals carry about 48% of residual sum of squares. Quadratic, cubic and high-rating tests did not explain the tail.

## Data

- 600 rows, 4 columns.
- Target: `price` (continuous regression target).
- Numeric features: `size_sqm`, `age_years`, `rating`. Rating is an integer score with five levels (1 to 5), treated as ordinal groups.
- No categorical, date/time, identifier or free-text features.
- Missing values: none in any column (0 each for price, size_sqm, age_years and rating).
- Modelling split: 80/20, seed 42, stratified by rating, giving 480 training and 120 test rows.

## Findings

### Price distribution and descriptive patterns

Price is strongly right-skewed. The mean is 289,164 and the median is 217,450 (skew 6.44). Quartiles are 119,225 and 371,400. The IQR rule flags 19 of 600 properties as high outliers (above 749,662), and none as low outliers.

![Distribution of property price: linear and log10 histograms (counts of properties)](tasks/eda_1/charts/price_distribution.png)

Size shows the strongest descriptive pattern. Mean price rises from 106,167 in the smallest size quartile to 532,703 in the largest. The share of high-price properties (above the overall Q3 of 371,400) rises from 1.3% to 76.7%. The Pearson correlation of size with price is 0.498.

Age shows a weaker pattern. The mean is not monotone across age quartiles: 317,557 (Q1, youngest), 309,303 (Q2), 251,963 (Q3) and 277,834 (Q4). The share of high-price properties falls from 34.7% in the youngest quartile to 15.3% in the oldest. The Pearson correlation of age with price is -0.077.

![Mean property price by size_sqm and age_years quartile](tasks/eda_1/charts/price_by_size_age_quartile.png)

Average and median price vary across rating levels without a monotone pattern. Mean price by rating is 286,769 (rating 1), 250,008 (2), 291,622 (3), 253,302 (4) and 355,663 (5). Medians are 237,100, 184,150, 204,600, 217,200 and 227,200. Rating 5 has the highest share above Q3 (29.9%) and rating 4 the lowest (21.3%). The Pearson correlation of rating with price is 0.066.

### Modelling dataset

The split gives 480 training and 120 test rows. Mean price is 284,050 in training and 309,620 in test, an observed gap of 25,570 (about 9% of the training mean). The cause of this gap was not tested. Stratification by rating holds: the largest gap between train and test shares for a rating level is 0.005.

### Rating and price

- **Unadjusted, across rating levels:** Kruskal-Wallis H=3.28 (4 df), p=0.51, epsilon-squared 0.005 (negligible). The result is identical on log(price) because the log transform preserves ranks.
- **Unadjusted, one-way ANOVA on log(price):** F=1.24, p=0.29.
- **Adjusted for size and age (categorical rating, OLS on log(price)):** joint F(4, 593)=1.79, p=0.13, partial eta-squared 0.012 (small).
- **Adjusted contrasts vs rating 1 (log scale):**

| Rating | Difference in log(price) | 95% CI | Ratio | p |
|---|---|---|---|---|
| 2 | -0.028 | -0.127 to 0.071 | 0.972 | 0.58 |
| 3 | +0.036 | -0.062 to 0.133 | 1.037 | 0.47 |
| 4 | -0.056 | -0.152 to 0.039 | 0.945 | 0.25 |
| 5 | +0.051 | -0.043 to 0.146 | 1.053 | 0.29 |

All confidence intervals include zero. Their widths (about ±0.10 on the log scale) still allow effects of roughly 10% in either direction.

![Price distribution by rating level; whiskers hidden outliers](tasks/stat_1/charts/price_by_rating_box.png)

![Adjusted differences in log(price) by rating level vs reference rating, controlling size_sqm and age_years, with 95% CIs](tasks/stat_3/charts/rating_adjusted_forest.png)

- **Rating form:** a linear rating term versus categorical rating gives F=2.20 on 3 df, p=0.087. The linear form is not clearly rejected at 0.05, but the result is borderline. The linear slope is +0.008 per rating point (p=0.46), so there is no evidence of a linear trend either.

### Age and price

- **Raw scale, oldest versus newest age tercile (stat_1 assignment, 202 newest and 200 oldest):** the mean is 261,927 for the oldest and 311,930 for the newest, a difference of -50,003. The Welch 95% CI is -109,870 to +9,864 (p=0.10). This is not significant.
- **Log scale, same comparison:** the geometric-mean ratio is 0.788 (log difference -0.238, 95% CI on the log difference -0.377 to -0.099; p<0.001). This estimates a geometric-mean ratio, which is a different quantity from the arithmetic mean difference. The two scales therefore disagree in significance.
- **Joint adjusted model (OLS on log(price), with size_sqm, age_years and rating; n=600; R²=0.734):** the age coefficient is -0.0064 per year (95% CI -0.0080 to -0.0047, p<0.001), about -0.64% in price per year (95% CI -0.82% to -0.46%). The unadjusted log-scale slope is -0.0065 per year (p<0.001), so adjustment barely changes it. With rating as categories, the age coefficient is -0.0065 (p<0.001).
- **Robustness:** HC3 robust standard errors give -0.00644 (95% CI -0.00825 to -0.00462, p<0.001). Median (quantile 0.5) regression gives -0.00648 (95% CI -0.00795 to -0.00502).
- **Spearman with price:** rho = -0.157 (95% CI -0.234 to -0.078, p=0.0001), a weak negative association.

The raw-scale non-significance may reflect high-price properties in the newest tercile. This is a hypothesis the tests do not establish.

### Size effects and interactions

- **Within age terciles, the OLS slope of price on size_sqm** is about 3,158 per sqm (young), 3,395 (middle) and 3,143 (old). Mean price rises across size terciles in every age tercile (cell counts 61 to 72).

![Price against size_sqm split by age tercile (left) and fitted size slope by rating level (right)](tasks/eda_3/charts/eda3_price_vs_size.png)

- **Size-by-age interaction, log(price):** joint F=0.636, p=0.530. Middle vs young coefficient 0.00084 per sqm (p=0.26); old vs young 0.00050 per sqm (p=0.50). On price: joint F=0.204, p=0.816.
- **Continuous size-by-age interaction:** not significant on log(price) (p=0.595) or price (p=0.717).
- **Size-by-rating interaction:** joint F=1.106, p=0.353 on log(price); joint F=1.918, p=0.106 on price. No significant slope difference across ratings at 5%.
- **Per-rating price slopes per sqm:** 3,222 (rating 1, 95% CI 2,395 to 4,049), 2,642 (2, 2,254 to 3,030), 3,088 (3, 1,983 to 4,193), 2,633 (4, 2,201 to 3,064) and 4,343 (5, 2,761 to 5,925). The overlapping intervals agree with the non-significant joint tests.

![Per-rating OLS slope of price on size_sqm with 95% confidence intervals; the joint interaction test shows no significant slope difference across ratings](tasks/stat_4/charts/stat4_slope_by_rating.png)

The size-by-age and size-by-rating results are reported with both scales agreeing. The eda_3 slope differences were not tested in that task; the tests reported here are from stat_4.

### Predictive models

On the single 120-row test split:

| Model | RMSE | MAE | R² |
|---|---|---|---|
| Mean baseline | 323,395 | 173,453 | -0.006 |
| Linear regression | 282,184 | 111,189 | 0.234 |
| Random forest | 322,304 | 118,753 | 0.0005 |

- Linear regression has a lower test RMSE than the baseline (282,184 vs 323,395), against a test price SD of 323,734. This comes from one split with no interval or repeated-split check.
- The random forest does not improve on the baseline on the test split. Its training R² of 0.869 indicates overfitting to the 480 training rows.
- Linear regression permutation importance (drop in test R²): size_sqm 0.436 (SD 0.078), age_years 0.013 (SD 0.008), rating 0.006 (SD 0.006).
- Random forest permutation importance: size_sqm 0.317 (SD 0.083), age_years -0.038 (SD 0.045), rating -0.083 (SD 0.040). Negative values mean the feature does not help out of sample.
- The train-test mean gap of 25,570 accounts for about 0.6% of the mean baseline's test MSE. This share was computed only for the mean baseline, not for the other models.

![Test-set RMSE of the mean baseline, linear regression and random forest predicting price](tasks/ml_1/charts/ml1_rmse_by_model.png)

### Residual diagnostics and tails

- **Joint log(price) model residuals:** skew 2.81 and excess kurtosis 13.6 (Jarque-Bera p<0.001). After trimming the 1st and 99th percentiles, skew is 2.15. Breusch-Pagan p=0.61, Durbin-Watson 1.98, and the maximum Cook's distance is 0.078. There is no sign of heteroscedasticity, autocorrelation or a single dominant influential point.

![Histogram of residuals from the joint log(price) model on size_sqm, age_years and rating](tasks/stat_5/charts/stat5_resid_hist.png)

- **Tail concentration:** the 10 largest absolute residuals carry 48.5% of residual sum of squares. Their mean rating is 3.9, against 3.1 overall. Their mean size and age are close to the sample means. Quadratic size and age terms are not significant (F=1.09, p=0.34), and cubic terms add nothing (F=0.32, p=0.73). The age coefficient under a quadratic form is unstable (-0.0110, CI -0.0183 to -0.0037), and AIC worsens (530.2 vs 528.4), so it is not a better fit.
- **Categorical-rating model:** the 10 largest residuals carry 47.9% of residual sum of squares, with mean rating 3.6. Rating 5 is 4 of the 10 against 22.3% of the sample. This is descriptive only.

![Adjusted log(price) difference for rating 4-5 vs 1-3 across quantiles, with 95% CIs and OLS mean effect](tasks/stat_6/charts/stat6_high_rating_quantiles.png)

- **High-rating (4-5 vs 1-3) effect across quantiles of log(price), adjusted for size and age:** q0.10 -0.024 (95% CI -0.079 to 0.031, p=0.39), q0.50 -0.025 (95% CI -0.074 to 0.023, p=0.30), q0.75 -0.046 (95% CI -0.110 to 0.018, p=0.16), q0.90 -0.001 (95% CI -0.078 to 0.076, p=0.98). The OLS mean effect is also non-significant. Bootstrap tests show the quantile effects do not differ detectably from the OLS mean effect.
- **Quantile rating coefficients:** most intervals include zero. The one exception is rating 4 at q0.75 (-0.125, 95% CI -0.221 to -0.029). With 20 coefficients tested, this is not treated as established.
- **Residual skew after the high-rating adjustment:** 2.78 for all residuals and 2.15 after trimming.

The tail source is not established. The tests do not favour any specific cause, and a formal rating non-linearity test in the tails was not run.

## Limitations

- **Single test split for model comparisons.** The linear regression gain (R² 0.234) is from one 120-row split with no interval or repeated-split check.
- **Rebuilt split in ml_1.** The saved eda_2 split object was not a 4-tuple, so ml_1 rebuilt the split using the eda_2 settings. Its training and test means (284,050 and 309,620) match eda_2.
- **Partial task.** eda_3 is marked partial. Its size-by-age and size-by-rating slope comparisons were not tested for significance there. Those tests appear in stat_4, which reports them with the conclusions above.
- **Age tercile assignment differs between tasks.** stat_1 assigns 202 observations to the newest tercile; stat_2 uses rank method 'first', giving 200. The newest-tercile mean is 311,930 in stat_1 and 313,379.5 in stat_2. The raw-scale difference is -50,003 (p=0.10) in stat_1 and -51,453 (p=0.093) in stat_2. The log-scale ratio is 0.788 in stat_1 and 0.785 in stat_2 (both p<0.001). The conclusions are unchanged. The headline numbers use the stat_1 assignment, and stat_2 is a sensitivity check.
- **Price skew values differ slightly.** eda_1 reports a price skew of 6.44 and stat_1 reports 6.42 for the same variable. The two values were not reconciled.
- **Correlation measures differ.** Pearson correlations (eda_1) and Spearman correlations (stat_1) are different statistics and are not directly comparable. The Spearman values are the ones used for association strength.
- **Residual non-normality.** Residual skew and kurtosis are high. OLS, HC3 and median regression give the same age estimate, so the age conclusion is not sensitive to this. The tails are not explained by the tests run.
- **Outliers.** 19 properties are IQR high outliers. The raw-scale age and mean comparisons are sensitive to them, and no trimmed or winsorised raw-scale analysis was run.
- **Train-test gap.** The 25,570 gap between training and test mean price is not explained.
- **Rating treatment.** Rating is treated as five groups or as a linear ordinal term. The rating-form test is borderline (p=0.087). Rating groups are small in the interaction tests, so those tests have limited power.
- **Limited power for rating.** The confidence intervals for rating contrasts are about ±0.10 on the log scale. Effects of around 10% cannot be ruled out.
- **Random forest.** Its test performance is at baseline level, and it overfits. No regularised or tuned variant was tested.
- No unresolved review issues were recorded in the accepted results.

## Open questions

- Does the rating effect hold after controlling for size, given the uneven rating group means? (Partly addressed: no significant adjusted effect was found, but a larger sample or pre-specified contrast was not tested.)
- Is the train-test mean gap of 25,570 driven by a few high-price outliers, and would a split stratified on price quartiles give more balanced means?
- Would modelling log(price) or removing outliers improve the predictive models?
- Would repeated cross-validation or bootstrap intervals show whether the linear regression R² gain of about 0.23 holds across splits?
- Would a regularised model or more data reduce the random forest's overfitting?
- Is the raw-scale age difference driven by a small set of high-price properties? Winsorised or trimmed means were not computed.
- Does the residual tail reflect a non-linear rating effect? A formal tail test of rating non-linearity has not been run.
- Are the tail rows (412, 523, 44, 24, 508, 198) high-price or data-entry outliers? Influence measures and a trimmed-sample age estimate were not computed.
- Does the age effect differ by size band or rating level (age-by-size or age-by-rating interactions)?
- Is the size-by-rating interaction significant with a single linear rating term or a larger sample?
- Is there a non-linear size effect (size-squared term) that captures heterogeneity better than separate slopes?
- Would a larger sample give enough power to detect a rating effect of the size shown in the confidence intervals?