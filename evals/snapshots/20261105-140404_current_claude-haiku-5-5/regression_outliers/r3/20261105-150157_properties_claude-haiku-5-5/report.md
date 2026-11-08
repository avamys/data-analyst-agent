# Price Drivers and Predictability in a 600-Property Dataset (Target: price)

## Summary

- **Price is strongly right-skewed.** The mean is 289,164 and the median is 217,450, with skew 6.44 on the linear scale and 0.35 on the log10 scale. Six properties sit above the 99th percentile (1,591,094), and 19 lie outside the 1.5 IQR upper fence (749,662.5). Twelve of the 19 have a price per square metre at least 5 times their same-rating, similar-size peers, which the analysis labels as likely error suspects. The 5× cutoff is a heuristic.
- **Size is the dominant association with price.** Spearman rho is 0.887. In the log-price multiple regression, each additional square metre is associated with about +1.24% price (95% CI +1.18% to +1.30%). The estimate stays between +1.21% and +1.24% across four specifications, including ones that remove or cap the flagged rows.
- **Age has a small negative association.** In the multiple regression, each additional year is associated with about −0.64% price (95% CI −0.82% to −0.46%). Age alone explains about 2% of the variance in log price (R² = 0.02).
- **Rating shows no detectable association.** The Kruskal-Wallis test gives p = 0.51, and the multiple-regression estimate is +0.81% per point (95% CI −1.31% to +2.97%, p = 0.457). Neither the size × age nor the size × rating interaction is significant.
- **Predictive power is modest.** On a 120-row test split, linear regression reduces MAE from 165,645 (mean baseline) to 102,395, but its test R² is only 0.189. The random forest overfits (train R² 0.865, test R² 0.017).

## Data

- 600 rows and 4 columns: one target (`price`) and three numeric features (`size_sqm`, `age_years`, `rating`).
- No categorical, date/time, identifier or free-text columns.
- No missing values in any column, so no rows were dropped and missingness was not analysed further.

## Findings

### Price distribution and skew

Price is strongly right-skewed. Mean 289,164, median 217,450, standard deviation 322,321, range 44,100 to 4,130,400, skew 6.44. On the log10 scale the skew falls to 0.35.

![Distribution of price: linear and log10 scale, counts of properties](tasks/eda_1/charts/price_hist.png)

### Binned averages

Price rises steeply with size. Mean and median price by size quartile:

| size_sqm quartile | Mean | Median | n |
|---|---|---|---|
| Q1 | 106,167 | 94,650 | 150 |
| Q2 | 202,297 | 160,200 | 150 |
| Q3 | 315,489 | 265,000 | 150 |
| Q4 | 532,703 | 452,900 | 150 |

Price against age is not monotone:

| age_years quartile | Mean | Median | n |
|---|---|---|---|
| Q1 | 317,557 | 237,600 | 150 |
| Q2 | 309,303 | 263,650 | 150 |
| Q3 | 251,963 | 187,800 | 150 |
| Q4 | 277,834 | 205,000 | 150 |

Price is highest in the youngest quartile and lowest in Q3, with Q4 slightly above Q3.

By rating, the mean is highest at rating 5 (355,663, n = 134), but medians stay within 184,150 to 237,100 and do not rise steadily with rating. Mean and median by rating: rating 1 286,769 / 237,100 (n = 109); rating 2 250,008 / 184,150 (n = 112); rating 3 291,622 / 204,600 (n = 118); rating 4 253,302 / 217,200 (n = 127); rating 5 355,663 / 227,200 (n = 134).

![Mean and median price by quartile of size_sqm and age_years, and by rating value](tasks/eda_1/charts/price_by_groups.png)

**Disagreement:** The raw age-quartile pattern is non-monotone, but the rank and regression results below describe a negative association with age. The raw rating-5 mean is the highest group mean, but the rating tests below find no association. These are reported as they stand and not reconciled.

### Univariate associations with price

- **size_sqm:** Spearman rho = 0.887 (95% CI 0.869 to 0.903, p = 5.8e-203, n = 600). Log-price OLS slope gives +1.24% per m² (95% CI +1.18% to +1.30%), R² = 0.71.
- **age_years:** Spearman rho = −0.157 (95% CI −0.234 to −0.078, p = 0.00011, n = 600). Log-price OLS gives −0.65% per year (95% CI −0.99% to −0.30%, p = 0.0003), R² = 0.02.
- **rating:** Spearman rho = 0.034 (95% CI −0.046 to 0.114, p = 0.40). Kruskal-Wallis across the five rating levels gives H = 3.28 (df 4), p = 0.51, epsilon-squared = 0.0055, a negligible effect. Log-price OLS gives +2.23% per point (95% CI −1.9% to +6.5%, p = 0.29, R² = 0.002). This single-feature estimate is not supported once size and age are controlled (see below).

### Interactions

- **Size × age:** The interaction coefficient is 0.0000102 per m² per year (95% CI −0.000027 to 0.000047, p = 0.59). The point shift in the size slope across one age SD (16.5 years) is about 1.4% of the baseline slope. The CI allows shifts from about −3.6% to +6.3%, so moderate moderation is not ruled out, but none is detected.
- **Size × rating:** The interaction coefficient is 0.000241 per m² per rating point (95% CI −0.000193 to 0.000676, p = 0.28). The point shift across one rating SD (1.42 points) is about 2.8% of the baseline slope. The CI allows shifts from about −2.2% to +7.8%. No interaction is detected.
- The interaction model has R² = 0.735 (n = 600), almost all of it from size.

### Joint (multiple) regression of log(price) and sensitivity checks

Main model, all 600 rows including the 19 flagged rows:

- Size: +1.24% per m² (95% CI +1.18% to +1.30%)
- Age: −0.64% per year (95% CI −0.82% to −0.46%)
- Rating: +0.81% per point (95% CI −1.31% to +2.97%, p = 0.457)
- R² = 0.734 (adjusted 0.733)

Sensitivity checks:

| Specification | Size per m² (95% CI) | Age per year (95% CI) | Rating per point (95% CI) |
|---|---|---|---|
| Price capped at IQR fence, n = 600 | +1.21% (+1.16 to +1.26) | −0.65% (−0.80 to −0.50) | +0.26% (−1.48 to +2.03) |
| Excluding 12 highest-ratio rows, n = 588 | +1.23% (+1.19 to +1.28) | −0.65% (−0.77 to −0.53) | −0.40% (−1.82 to +1.03) |
| Excluding 11 rows with ratio ≥ 5, n = 589 | +1.23% (+1.19 to +1.28) | −0.66% (−0.78 to −0.53) | −0.28% (−1.74 to +1.21) |

Rating is null in every specification. Its sign changes between specifications, but its CI always includes zero. The sensitivity analysis reports that the size coefficient moves by about 0.03 points across these specifications. Size and age are uncorrelated (Pearson r = −0.0006), so their joint estimates are not affected by collinearity between them.

### Flagged high-price properties

- **Peer comparison:** All 19 flagged properties have a price per m² above 1.5 times the median of same-rating peers within 20 m². Ratios range from 1.60 to 10.72, with median 5.52. Peer groups contain 15 to 37 properties.
- **Top 1% (six properties):** Their ratios range from 5.05 to 10.72. Their prices range from 1,927,100 to 4,130,400, at percentile ranks 0.990 to 0.998.
- **Classification:** 12 properties have ratios of at least 5 and are labelled suspect. Seven have ratios from 1.60 to 3.11 and are labelled ambiguous (idx 4, 277, 94, 433, 230, 498, 111).
- **Context:** The unflagged data have median price 210,500, median size 120.4 m², median age 30.3 years, median rating 3 and median price per m² 1,978.9.
- **Reported recommendation:** Treat the 12 suspect rows as likely errors until checked against source records, and do not treat the six top-1% properties as genuine luxury listings by default. For the seven ambiguous rows, the analysis suggests keeping them or capping them, and confirming idx 4 and idx 498 first because they have the smallest peer groups (16 and 15).

![Price against size_sqm; the 19 IQR-flagged and 6 top-1% properties are shown in red on a log price axis](tasks/eda_2/charts/flagged_scatter.png)

### Predictive models

- **Split:** 80/20 with random_state = 42, giving 480 training and 120 test rows. Features: size_sqm, age_years, rating. Target: raw price. This is a single split.
- **Mean baseline (test):** MAE 165,645, RMSE 303,756, R² −0.0002.
- **Linear regression (test):** MAE 102,395, RMSE 273,535, R² 0.189.
- **Random forest (test):** MAE 108,882, RMSE 301,080, R² 0.017. Train R² is 0.865, so the model overfits. Its feature importances are size_sqm 0.640, age_years 0.302, rating 0.059.
- **Permutation importance for linear regression (drop in test R²):** size_sqm 0.474 (SD 0.085), age_years 0.017 (SD 0.011), rating 0.003 (SD 0.013).

![Test-set MAE, RMSE and R2 for the mean baseline, linear regression and random forest on the 120-row test split](tasks/ml_2/charts/ml2_model_comparison.png)

## Limitations

- **Outliers and errors:** Price is heavily skewed, and 19 flagged rows are high-price outliers. The analysis did not verify them against source records. Twelve are labelled likely errors and seven ambiguous, using a heuristic 5× cutoff. The peer groups for idx 4 and 498 are small (16 and 15), so their ratios are less stable.
- **Unresolved review issue (eda_2):** The recommendation for the six top-1% rows gives the price range as 1,587,700 to 4,130,400 and the rank range as 0.988 to 0.998. The correct range is 1,927,100 to 4,130,400 and ranks 0.990 to 0.998. The value 1,587,700 (rank 0.988) belongs to idx 4, which is not in the top 1% and is labelled ambiguous. The lead's objection stands and affects the eda_2 recommendation for the top-1% rows. The other eda_2 findings are supported as stated.
- **Sample of the statistical tests:** The univariate and interaction tests are on log price with all 600 rows as reported. The multiple-regression sensitivity analysis is the only place where flagged rows are excluded or capped.
- **Models:** The ML models use raw price and a single 120-row test split. The findings do not state whether the flagged rows were removed from the ML data. Linear regression explains about 19% of test variance, so predictions are imprecise. The ML findings do not include cross-validation or log-price model results.
- **Non-linearity:** No log-size, spline or robust-regression (for example Huber) fit has been run, so linearity of size and age is assumed in the reported slopes.
- **Interpretation:** All results are associations in observational data. The findings do not support causal statements.
- **Failed tasks:** None. All seven tasks are reported as complete.

## Open Questions

- Are the 12 suspect high-ratio properties data-entry errors (for example a missing decimal point or a currency mix-up) when checked against source records?
- Do the size and age effects hold after controlling for age and rating in a log-price regression on the cleaned data, and do they change when the 6 top-1% and 19 IQR-flagged rows are handled differently? The sensitivity checks partly answer this, but the cleaning choice for the ML models is not settled.
- Is the rating-5 mean premium (355,663) driven by a few high-price flagged properties? The regression results show rating has no detectable association, but the raw mean premium has not been decomposed.
- Are the seven ambiguous high-price rows (ratios 1.60 to 3.11) genuine, and do robust regression (for example Huber) estimates match the size and age slopes?
- Is the age effect non-linear once size is controlled, given the non-monotone age-quartile pattern?
- Is a log-size or spline term a better fit for size than a linear slope?
- Does a log-price model improve on raw-price linear regression on the test split?
- Would non-linear terms or interactions for size and age raise R² without the random forest's overfitting, and how stable are the coefficients across cross-validation folds?
- Does the low R² reflect outliers in price, and how do the model scores change when the flagged rows are excluded from the ML data?