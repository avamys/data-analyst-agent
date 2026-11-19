# Price Determinants and Predictability: Analysis of 600 Listings (Target: price)

## Summary

- **Size is the dominant association with price.** Spearman rho is 0.887 (95% CI 0.869 to 0.903, Holm-adjusted p about 2e-202). Mean price rises from 106167 in the smallest size quartile to 532703 in the largest.
- **Age has a small, independent negative association with log10 price.** The bivariate Spearman rho is -0.157 (p about 0.0001). After controlling for size and rating, the OLS coefficient is -0.00280 per year (95% CI -0.00359 to -0.00200, p = 1.0e-11). The bivariate mean and median patterns across age quartiles disagree, so the effect is uncertain.
- **Rating shows no detectable association with price.** Spearman rho is 0.034 (95% CI -0.046 to 0.114, p = 0.403), and the Kruskal-Wallis test across the five rating levels gives p = 0.513.
- **Size and age do not measurably interact.** The size-by-age interaction in log(price) is 9.99e-06 (p = 0.597). The low- and high-age slopes are both about 0.012 per sqm and their intervals overlap.
- **Predictive power from these three features is limited.** On the 120-listing test set, linear regression reaches R² 0.189 and MAE 102395, against 165645 for a mean-of-target baseline. The random forest is worse on test (R² 0.066) and overfits.

## Data

- 600 rows and 4 columns: the target `price` and three numeric features, `size_sqm`, `age_years` and `rating`.
- No categorical, date/time, identifier or free-text features.
- No missing values in any column (0 for all four), so missingness was confirmed as zero and not analysed.
- Price is strongly right-skewed. Mean 289164, median 217450, standard deviation 322321, skew 6.44, range 44100 to 4130400. On the log10 scale the skew is 0.35, so log10 price is close to symmetric.

## Findings

### Distribution of price

Price is strongly right-skewed. Mean price (289164) exceeds median price (217450), and the skew is 6.44. On the log10 scale the skew is 0.35, close to symmetric. The log10 mean is 5.334 and the log10 standard deviation is 0.315.

![Distribution of price: linear and log10 scale](tasks/eda_1/charts/price_hist.png)

By rating level, the mean exceeds the median at every level:

| Rating | Count | Mean | Median |
|---|---|---|---|
| 1 | 109 | 286769 | 237100 |
| 2 | 112 | 250008 | 184150 |
| 3 | 118 | 291622 | 204600 |
| 4 | 127 | 253302 | 217200 |
| 5 | 134 | 355663 | 227200 |

The gap is largest in absolute terms at rating 5 (355663 vs 227200) and at rating 3 (291622 vs 204600). These are descriptive differences. The rating tests below find no reliable association.

### Size and price

Size has a strong, monotone positive association with price. Spearman rho is 0.887 (95% CI 0.869 to 0.903, p about 6e-203, Holm-adjusted p about 2e-202). Mean and median price both rise across all four size quartiles:

| Size quartile (sqm) | Count | Mean | Median |
|---|---|---|---|
| 30.1 to 72.9 | 150 | 106167 | 94650 |
| 72.9 to 121.1 | 150 | 202297 | 160200 |
| 121.1 to 163.0 | 150 | 315489 | 265000 |
| 163.0 to 199.7 | 150 | 532703 | 452900 |

### Age and price

The bivariate association between age and price is weak and negative, and its quartile pattern is mixed.

- Spearman rho between age and price is -0.157 (95% CI -0.234 to -0.078, p about 0.00011, Holm-adjusted p about 0.00022). This is significant after Holm correction across the three overall tests. It is small, and it is not adjusted for size or rating.
- By age quartile, means fall from the first to the third quartile (317557, 309303, 251963) and then rise in the fourth (277834). Medians rise between the first two quartiles (237600, 263650) and then fall (187800, 205000). The two summaries therefore disagree, and the bivariate age effect is uncertain.

| Age quartile (years) | Count | Mean | Median |
|---|---|---|---|
| 0.1 to 16.9 | 150 | 317557 | 237600 |
| 16.9 to 30.1 | 150 | 309303 | 263650 |
| 30.1 to 43.9 | 150 | 251963 | 187800 |
| 43.9 to 59.8 | 150 | 277834 | 205000 |

The bivariate Spearman rho does not adjust for other features. The regression coefficient below does. The two results measure different things, and they are not directly comparable.

### Rating and price

Rating shows no monotone association with price.

- Spearman rho between rating and price is 0.034 (95% CI -0.046 to 0.114), p = 0.403, Holm-adjusted p = 0.403. This is not significant.
- The Kruskal-Wallis test across the five rating levels gives H = 3.28, p = 0.513. The epsilon-squared is -0.001. This value is a small-sample artifact, and the effect is effectively zero.

Within each rating level, Spearman correlations of price with size and age are as follows (n is the count at that level):

| Rating (n) | Size rho | Size p_holm | Size significant after Holm | Age rho | Age p | Age p_holm | Age significant after Holm |
|---|---|---|---|---|---|---|---|
| 1 (109) | 0.891 | 1.0e-37 | Yes | -0.214 | 0.025 | 0.101 | No |
| 2 (112) | 0.901 | 1.1e-40 | Yes | -0.211 | 0.025 | 0.101 | No |
| 3 (118) | 0.857 | 1.8e-34 | Yes | -0.123 | 0.183 | 0.366 | No |
| 4 (127) | 0.903 | 1.4e-46 | Yes | -0.032 | 0.719 | 0.719 | No |
| 5 (134) | 0.875 | 1.5e-42 | Yes | -0.217 | 0.012 | 0.058 | No |

Size stays strongly associated with price at every rating level and survives Holm correction at all five. No age correlation survives Holm correction at any rating level. At rating 5 the age p_holm is 0.058, just above 0.05.

### Size-by-age interaction

The size-by-age interaction term in an OLS model of log(price) is 9.99e-06 (95% CI -2.71e-05 to 4.71e-05, p = 0.597). The data do not show that age changes the effect of size on log(price). The test did not detect a difference, which is not the same as showing that the slopes are equal.

Split into terciles of age, the slope of log(price) on size_sqm is:

- Low age tercile (age up to 21.3 years, n = 202): 0.01192 per sqm (95% CI 0.01093 to 0.01292).
- High age tercile (age above 38.3 years, n = 200): 0.01239 per sqm (95% CI 0.01129 to 0.01349).

The intervals overlap widely, and both slopes are about 0.012 per sqm.

![Slope of log(price) on size_sqm within low and high age terciles, with 95% CI](tasks/stat_2/charts/tercile_size_slopes.png)

### Age effect after adjustment for size and rating

In an OLS model of log10 price on size_sqm, age_years and rating (n = 600), the age coefficient is -0.00280 per year (95% CI -0.00359 to -0.00200, p = 1.0e-11). This corresponds to roughly a 0.6% lower price per additional year of age.

- Across the three tested terms, Holm correction keeps the age effect significant (Holm-adjusted p = 2.0e-11). The comparable values are 3.6e-170 for size_sqm and 0.457 for rating.
- Dropping age lowers R² from 0.734 to 0.713 (adjusted R² from 0.733 to 0.712). The nested F-test for age gives F = 48.21 on 1 numerator degree of freedom, p = 1.0e-11.

### Predictive models

The models were evaluated on a single fixed 80/20 split (480 training and 120 test listings, seed 42). The baseline predicts the training mean.

| Model | Test MAE | Test RMSE | Test R² | Train R² |
|---|---|---|---|---|
| Mean baseline | 165645 | 303756 | -0.0002 | n/a |
| Linear regression | 102395 | 273535 | 0.189 | 0.270 |
| Random forest (300 trees, min leaf 3) | 104230 | 293584 | 0.066 | 0.527 |

- Linear regression is the best model on the test set. Its MAE is 38% below the baseline and its RMSE is 10% below the baseline.
- The random forest is worse on test and overfits: its train R² is 0.527 against a test R² of 0.066.
- Size, age and rating explain only a small part of price. The best model reaches a test R² of 0.19.

![Test MAE of the mean baseline, linear regression and random forest](tasks/ml_1/charts/ml1_model_mae.png)

The feature importance results disagree on ranking:

- Linear regression permutation importance (drop in test R², 30 repeats) ranks size_sqm first (mean 0.474, sd 0.085), then age_years (0.017, sd 0.011), then rating (0.003, sd 0.013, within noise).
- The linear regression coefficient ranking (absolute value) places rating first (13363), then size_sqm (3315), then age_years (1230).
- The random forest importance ranks size_sqm first (0.792), age_years second (0.168) and rating third (0.040).

The coefficient ranking and the permutation ranking disagree on rating. This report does not resolve the disagreement.

## Limitations

- **Price distribution.** Price is strongly right-skewed (skew 6.44 on the linear scale), with a wide range (44100 to 4130400). Means exceed medians at every rating level. Whether a few high-price listings drive the means was not established.
- **Robustness of the age result.** Robust or HC standard errors and alternative transforms of price were not checked, so the age conclusion has not been tested against them.
- **Age effect is uncertain.** The bivariate mean and median age patterns disagree. The adjusted coefficient is significant, but the bivariate Spearman association is marginal and small.
- **Interaction not detected.** The size-by-age test found no evidence of interaction. This does not show that the slopes are equal.
- **Predictive performance is low.** A test R² of 0.19 for the best model means size, age and rating leave most price variation unexplained. The random forest overfits. All model results rest on one 120-listing test split.
- **Feature importance disagrees.** Coefficient-based and permutation-based rankings disagree on rating.
- **Unresolved review issues for stat_1 (status: partial).** The lead's objections to this task still stand, and they affect the following findings:
  - The within-rating Spearman results for ratings 2 to 5 were not verified in that task. The table above is taken from the recorded values, and the Holm survival statements rely on the recorded adjusted p-values.
  - The rating-price Spearman interval was recorded only partially in that task. The full recorded interval (-0.046 to 0.114) is given above.
  - The epsilon-squared of -0.001 is a small-sample artifact and is described as effectively zero, not as a negative effect size.
- **Task status.** stat_1 is partial. No tasks are recorded as failed.

## Open questions

- Does age's negative association with price hold after controlling for size and rating in a multiple regression on log10 price? The adjusted coefficient is significant, but the bivariate pattern remains mixed.
- Why do the mean and median age patterns disagree, and are a few high-price listings driving the age means?
- Why do the mean and median price differ at every rating level, and are a few high-price listings driving the means?
- Is the size-price relationship better modelled on a log scale? The log10 price distribution is close to symmetric, but the size model was not compared with a linear model.
- Do the age effects differ between small and large listings?
- Do robust or HC standard errors, or a different transform of price, change the age conclusion?
- Is the age effect non-linear (for example, log age or age bands), and does it interact with size?
- Does rating's effect change after controlling for size and age? Its bivariate and interaction results show no detectable effect.
- Why does the random forest overfit and underperform linear regression on this sample?