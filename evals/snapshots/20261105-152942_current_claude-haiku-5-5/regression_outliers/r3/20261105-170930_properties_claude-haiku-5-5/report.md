# Price Analysis of a 600-Row Dataset (Target: price)

## Summary

- **Size is the only feature with a clear, significant link to price.** Spearman is 0.887 (bootstrap 95% CI 0.859 to 0.911). The geometric Q4/Q1 size-quartile price ratio is 4.94 (95% CI 4.53 to 5.38). On the log scale, the slope is about +1.24% price per m².
- **Size's relation to price is convex on the raw scale but not on the log scale.** The raw-price quadratic is significant on all 600 rows (p = 0.0013) and remains strongly significant with the top 6 price rows excluded (p = 1.8e-12). On log(price), curvature is not supported (p = 0.631).
- **Age has a modest negative association.** It is significant on the log scale (p = 0.00029) and in rank correlation (p = 0.00011), but not on the raw linear scale (p = 0.061). Rating shows no significant association with price, before or after adjustment.
- **Prediction is weak.** The best model, linear regression, reduces held-out RMSE from 323,395 (mean baseline) to 282,184, but its test R² is only 0.234. Gradient boosting overfits and does not beat the baseline.

## Data

- 600 rows and 4 columns: one numeric target (price) and three numeric features (size_sqm, age_years, rating).
- No categorical, date/time, identifier or free-text columns.
- No missing values in any column (0 of 600 for size_sqm, age_years, rating and price). Missingness was therefore confirmed as absent and not modelled.

## Findings

### Price distribution

- Price is strongly right-skewed. Mean is 289,164, median 217,450, standard deviation 322,321, minimum 44,100 and maximum 4,130,400. Skew is 6.44 and raw kurtosis 59.5.
- The top 1% of rows (6 of 600) hold about 9.7% of total price.
- A log transform reduces skew to 0.35 and kurtosis to 0.32.

![Histogram of price](tasks/eda_1/charts/price_histogram.png)

### Feature associations (significance and effect size)

**Size (size_sqm)**
- Spearman is 0.887 (bootstrap 95% CI 0.859 to 0.911, p = 5.8e-203).
- Raw-price Pearson is 0.498 (95% CI 0.435 to 0.556, p = 7.4e-39). The raw OLS slope is 3,228.7 per m² (95% CI 2,776.7 to 3,680.7).
- On log(price), Pearson is 0.844 (95% CI 0.819 to 0.866, p = 5.1e-164). The slope is 0.01232 log-price units per m² (95% CI 0.01169 to 0.01295), about +1.24% price per m².
- Mean price rises across size quartiles: 106,167 (Q1), 202,297 (Q2), 315,489 (Q3), 532,703 (Q4). Median price is 94,650, 160,200, 265,000 and 452,900.
- Q4 minus Q1 mean difference is 426,535 (bootstrap 95% CI 362,809 to 503,312). The geometric Q4/Q1 ratio is 4.94 (95% CI 4.53 to 5.38).

![Price against size_sqm with each dot one row](tasks/stat_1/charts/size_price_scatter.png)

![Scatter of price against size_sqm and age_years](tasks/eda_1/charts/price_scatter.png)

**Age (age_years)**
- Spearman is -0.157 (bootstrap 95% CI -0.230 to -0.080, p = 0.00011).
- Log-scale Pearson is -0.147 (95% CI -0.225 to -0.068, p = 0.00029). The log slope is -0.00647 per year (95% CI -0.00996 to -0.00299), about -0.64% price per year.
- Raw-scale Pearson is -0.077 (95% CI -0.156 to 0.003, p = 0.061). The raw OLS slope is -1,496 per year (95% CI -3,058.9 to 66.9, p = 0.061).
- Age quartile mean prices are 317,557, 309,303, 251,963 and 277,834. The pattern is not monotone: the mean dips at Q3 and partly recovers at Q4. The Q4 minus Q1 mean difference is -39,723 (bootstrap 95% CI -112,497 to 43,655, which includes zero). The geometric Q4/Q1 ratio is 0.81 (95% CI 0.69 to 0.96).
- The stat_1 conclusion is that the age effect should be reported as a modest effect, not a robust one, because its significance depends on the scale and test chosen.

**Rating**
- Rating has five levels. Kruskal-Wallis gives H = 3.28, p = 0.513, identical on raw and log price.
- Eta-squared (H-based) is -0.0012, with bootstrap 95% CI -0.0050 to 0.0237. The raw value is negative and is floored at 0. The effect is negligible.
- Pearson is 0.066 and Spearman 0.034 (p = 0.403).
- No pairwise Mann-Whitney comparison is significant after Holm correction (all Holm p = 1.0).
- Mean price by level is 286,769 (1), 250,008 (2), 291,622 (3), 253,302 (4) and 355,663 (5). Median price is 237,100, 184,150, 204,600, 217,200 and 227,200. Neither mean nor median is monotone in rating.

### Size-price curvature (convexity)

- Earlier, convexity was inferred from the gap between Spearman (0.887) and Pearson (0.498) and was not tested directly. This section reports the direct tests.
- **Raw price, all 600 rows:** the quadratic coefficient is 42,644 (SE 13,191, p = 0.0013, 95% CI 16,737 to 68,552). The quadratic beats linear (F = 10.45, p = 0.0013). R² rises from 0.248 to 0.261, and AIC falls from 16,755.0 to 16,746.6. The B-spline beats linear (F = 2.93, p = 0.020, R² 0.262) but has no better AIC than the quadratic (16,751.3).
- **Raw price, top 6 rows excluded (n = 594):** the quadratic coefficient is 40,208 (95% CI 29,250 to 51,167, p < 0.00001). The quadratic beats linear (F = 51.9, p < 0.00001). R² rises from 0.567 to 0.602, and AIC falls from 15,599.9 to 15,551.8. The B-spline beats linear (F = 15.5, p < 0.00001; R² 0.608; AIC 15,548.2).
- Excluding the top 6 rows raises the size Pearson from 0.498 to 0.753 but barely changes Spearman (0.887 to 0.892). The top rows therefore inflate the Pearson-Spearman gap, but the curvature itself does not depend on them.
- **Robust check:** a Huber regression on the 594 rows gives a raw-scale quadratic coefficient of 14.63 per m² (SE 1.27, p = 6.7e-31, 95% CI 12.15 to 17.11). The OLS quadratic on the same rows is 16.27 per m² (SE 2.26, p = 1.8e-12). The 40,208 figure above is the same term on a standardised size scale, so the two sets of numbers differ only in scale.
- **Log price:** the curvature term is not significant (coefficient -0.00890, SE 0.0185, p = 0.631, 95% CI -0.0452 to 0.0274). The quadratic does not beat linear (F = 0.232, p = 0.631), and R² is 0.7125 (linear) and 0.7126 (quadratic). The log-scale spline does not beat linear (F = 0.490, p = 0.743), and its AIC (577.8) is worse than linear (571.8).
- **Interpretation as stated in the findings:** the gap is consistent with a multiplicative (log-linear) relation on the raw scale. The raw convexity is the shape that such a relation takes on the raw scale, not a separate curvature in log space. The raw-scale OLS p-values were not checked with heteroscedasticity-robust standard errors.

![Linear and quadratic fits of size_sqm on raw price (left) and log(price) (right)](tasks/stat_3/charts/stat3_linear_vs_quadratic_fit.png)

### Interactions with age

- **Age × size (log price):** coefficient 0.00001, p = 0.597, 95% CI -0.000027 to 0.000047. On the raw scale, p = 0.708.
- **Age slopes within size halves (median split at 121.1 m²):** low size -0.67% per year (p = 0.0003, n = 300); high size -0.74% per year (p = 0.00001, n = 300).
- **Age × rating (log price):** coefficient 0.00074, p = 0.555, 95% CI -0.0017 to 0.0032. On the raw scale, p = 0.397.
- **Age slopes within each rating level (log price):** level 1 -0.93% (p = 0.027), level 2 -0.82% (p = 0.035), level 3 -0.61% (p = 0.136), level 4 -0.14% (p = 0.693), level 5 -0.89% (p = 0.035). The slopes overlap within their confidence intervals, and the interaction test is not significant.

![Age slope on log(price) within size halves and each rating level](tasks/stat_2/charts/age_slopes_by_group.png)

### Adjusted effects (multiple regression on log price)

- **Age, adjusted for size:** coefficient -0.00645 per year (95% CI -0.00827 to -0.00463, p = 8.9e-12). Unadjusted, the coefficient is -0.00647. Adding size changes the age estimate by about 0.35%.
- **Age, adjusted for size and rating:** coefficient -0.00644 per year (95% CI -0.00826 to -0.00462, p = 1.0e-11).
- The age-size correlation was not computed, so confounding of the age effect by size was not formally ruled out.
- Model R² rises from 0.022 (age alone) to 0.734 (with size). Size accounts for nearly all explained variance.
- **Rating, adjusted for size and age:** numeric coefficient 0.0080 per level (95% CI -0.013 to 0.029, p = 0.457). Dropping rating changes R² by 0.00025. Treated as categorical (levels vs level 1), the joint F-test gives F = 1.79, p = 0.130. A non-significant test does not establish that no effect exists.
- **Size, adjusted:** coefficient 0.01231 per m² (95% CI 0.01171 to 0.01292, p = 1.2e-170).

### Influence of the top 1% of prices

Excluding the top 6 price rows (eda_2):

- **Size quartiles:** the ordering holds. Q4 mean falls from 532,703 to 475,088 (about 11%). Q1 is unchanged. Medians barely move (Q4 from 452,900 to 448,300).
- **Age quartiles:** the Q3 dip holds and is deeper. Mean price falls from Q2 to Q3 by 287,987 to 224,590 in the excluded sample, against 309,303 to 251,963 in the full sample. The Q4 mean is 237,115 in the excluded sample, against 277,834 in the full sample.
- **Rating:** the non-monotone pattern holds, and level 1 still has the highest median (234,150 excluding the top rows, against 237,100 in the full sample). Level 5's mean falls from 355,663 to 278,622, only slightly above level 1 (271,581). The earlier claim that level 5 has the highest mean is not supported after exclusion.
- **Correlations:** size Pearson rises from 0.498 to 0.753. Size Spearman moves from 0.887 to 0.892. Age Pearson becomes -0.174 (from -0.077), and age Spearman -0.164 (from -0.157). Rating Pearson falls from 0.066 to 0.015.

![Mean price by size quartile, age quartile and rating level, full sample vs excluding the top 6 price rows](tasks/eda_2/charts/eda2_group_means.png)

The age slope has not been re-estimated in a regression with these rows excluded (see Limitations).

### Predictive modelling

Evaluation used an 80/20 split (480 training, 120 test) with seed 42.

| Model | Test RMSE | Test MAE | Test R² | 5-fold CV RMSE (train) |
|---|---|---|---|---|
| Mean baseline | 323,395 | 173,453 | -0.006 | n/a |
| Linear regression | 282,184 | 111,189 | 0.234 | 261,589 (sd 97,318) |
| Gradient boosting | 337,117 | 123,861 | -0.094 | 301,404 (sd 98,368) |

- Linear regression is about 12.7% lower in test RMSE than the baseline. Its train R² is 0.26. The CV standard deviation shows the gain is consistent but noisy.
- Gradient boosting is worse than the baseline on test data. Its train R² is 0.905, which indicates overfitting.
- Linear regression was selected by lower CV RMSE and saved as best_model.pkl.

![Predicted versus actual price on the 20 percent test set for the best model](tasks/ml_1/charts/ml1_pred_vs_actual.png)

### Feature importance and direction (linear regression)

- **Size:** permutation on the test set lowers R² by a mean of 0.450 (sd 0.078, 30 repeats). Coefficient +3,294 per m².
- **Age:** mean R² drop 0.0135 (sd 0.0085, 30 repeats). Coefficient -1,181 per year.
- **Rating:** mean R² drop 0.0059 (sd 0.0064, 30 repeats). Coefficient +9,269 per rating point.
- The coefficients are on different feature scales and are not comparable as importance measures.
- The order by absolute correlation (size, age, rating) matches the permutation order, and each correlation's sign matches its coefficient. The age and rating permutation drops overlap within their standard deviations, so their relative order (second vs third) is not reliable.
- Rating's Spearman is 0.034 (p = 0.403), and the Kruskal-Wallis result shows no reliable association, so the data do not show that higher ratings raise price.
- Test residuals have Pearson correlations of -0.062 (size), -0.090 (age) and +0.055 (rating) with the features. Only linear correlations were tested, so nonlinear patterns are not ruled out.

![Test-set residuals of linear regression against each feature](tasks/ml_2/charts/ml2_residuals_vs_features.png)

## Limitations

- **Missing features:** the dataset records no location, condition or similar variables. The test R² of 0.234 means most variation in price is not explained by these features.
- **Age direction (unresolved review issue):** the raw-scale age effect is not significant (raw OLS slope -1,496 per year, p = 0.061). The negative association is significant only on the log scale and in rank correlation. It should be read as a modest effect, not a robust one.
- **Age and rating importance ranking (unresolved review issue):** the permutation drops for age (0.0135, sd 0.0085) and rating (0.0059, sd 0.0064) overlap within their standard deviations. Their relative order (second vs third) is not reliable, so the statement that the ranking agrees fully with the correlation ranking must be qualified accordingly.
- **Age robustness to top rows (unresolved review issue):** the age slope has not been re-estimated in a regression after excluding the top 6 price rows, and no robust regression was run on it. The eda_2 results show these rows shift several associations, so the age slope is not yet shown to be robust.
- **Heteroscedasticity:** OLS p-values for the raw-price quadratic (full and top-6-excluded samples) were not checked with heteroscedasticity-robust standard errors. The Huber check supports the curvature but is not a substitute for HC errors.
- **Confounding:** the correlation between age and size was not computed, so confounding of the age effect by size is not formally ruled out.
- **Convexity:** the convexity inference in eda_1 was not tested there. The direct tests are in stat_3 and stat_6, and their results are reported above.
- **Rating non-significance:** a non-significant rating test does not establish that rating has no effect.
- **Modelling scope:** the gradient boosting model was not tuned, and the findings do not assess whether a regularised or shallower model would perform better.
- **Sample size for outliers:** the top 1% comprises 6 rows, so the exclusion analyses rest on very few observations.

**Numbers not traced to a recorded fact.** The automatic check found no recorded value for these numbers:
- 1.24% in: "- **Size is the only feature with a clear, significant link to price.** Spearman is 0.887 (bootstrap 95% CI 0.859 to 0.911). The geometric Q4/Q1 size-quartile p"
- 1.24% in: "- On log(price), Pearson is 0.844 (95% CI 0.819 to 0.866, p = 5.1e-164). The slope is 0.01232 log-price units per m² (95% CI 0.01169 to 0.01295), about +1.24% p"

## Open questions

- Does a spline on size, or a log-price model, change the adjusted rating and age estimates? Size curvature is absent on the log scale, but adjusted rating and age were not re-estimated with a spline.
- Does the age effect survive adjustment for size in a robust or top-row-excluded regression on log price?
- Is the non-monotone age pattern (Q3 dip, partial Q4 recovery) explained by the size mix across age quartiles? This was not tested.
- Does rating interact with size once size and age are controlled for? The interaction was not tested in a model with size.
- Do the top 6 price rows form a distinct segment (for example, all in the largest size quartile) that should be modelled separately or excluded?
- Would location or condition features, which the dataset lacks, explain the weak overall predictive signal?
- Do standardised coefficients or confidence intervals confirm the size and direction of the age and rating effects in the predictive model?
- Does a shallower, regularised gradient boosting model, with early stopping, generalise better than the current overfit model?