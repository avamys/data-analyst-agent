# Promo Is Associated with Higher Daily Sales; Temperature Shows No Detectable Association: Sales Analysis (730 Days, 2023–2024)

## Summary

- **Promo days sell more.** Mean sales are 298.39 on promo days (n = 104) versus 266.27 on non-promo days (n = 626), a difference of 32.12 units (95% CI 23.97 to 40.27; Welch t = 7.79, p < 0.001; Cohen's d = 0.81). The promo coefficient stays at 31.96 (95% CI 27.19 to 36.72) after adjusting for a time trend and temperature.
- **Temperature is not significantly associated with sales.** Pearson r = 0.016 (p = 0.671) and Spearman rho = 0.010 (p = 0.781). After adjusting for promo and time, the temperature coefficient is -0.046 (p = 0.71).
- **Whether the promo effect changes with temperature is unresolved.** The interaction tests are not significant (linear interaction p = 0.41; cubic-polynomial p = 0.741; quartile bands p = 0.414), but the confidence intervals are wide, so a meaningful change is neither confirmed nor ruled out.
- **Sales rise over the period.** Quarterly mean sales climb from 223.16 (2023Q1) to 321.05 (2024Q4), and the time coefficient is 0.153 units per day after adjustment. Promo share does not differ significantly across quarters (chi-square p = 0.35).
- **Predictive power is low.** The best model, linear regression on temperature and promo, reduces test RMSE from 38.78 (mean baseline) to 36.72 and reaches test R² of 0.069. The random forest does not beat the baseline (test RMSE 40.31).

## Data

- 730 daily rows and 4 columns: `date`, `temperature`, `promo`, `sales`.
- Target: `sales` (continuous, regression).
- Features used in modelling: `temperature` and `promo`, both numeric. There are no categorical features.
- `date` is an identifier-like text field, so it was excluded from model features. It was parsed and used only for the time analyses. All 730 values parsed, with 730 unique dates and no duplicates, spanning 2023-01-01 to 2024-12-30.
- Missing values: none in any column.

## Findings

### Sales distribution

Daily sales are close to symmetric: mean 270.84, median 270.25, standard deviation 41.13, skew 0.10 (n = 730).

![Distribution of daily sales across 730 days](tasks/eda_1/charts/sales_hist.png)

### Promo and sales

- Descriptively, promo days have higher sales: promo = 1 (n = 104) has mean 298.39 and median 295.40; promo = 0 (n = 626) has mean 266.27 and median 266.40.
- The difference is statistically significant. Welch t = 7.79 (df 141.3), p < 0.001. The mean difference is 32.12 units (95% CI 23.97 to 40.27). Cohen's d is 0.81 (approximate 95% CI 0.60 to 1.02), a large effect.
- Promo's Pearson correlation with sales is 0.273.

### Temperature and sales

- By temperature quartile band, sales means are 269.61 (Q1, n = 184), 273.74 (Q2, n = 183), 266.61 (Q3, n = 181) and 273.38 (Q4, n = 182). Medians are 267.90, 272.40, 265.30 and 276.25. The quartile cut points are -4.0, 6.4, 12.4, 18.1 and 28.1. These band differences were described but not tested for significance.

![Mean and median daily sales per temperature quartile](tasks/eda_1/charts/sales_by_temp_band.png)

- Temperature is not significantly associated with sales: Pearson r = 0.016 (95% CI -0.057 to 0.088, p = 0.671) and Spearman rho = 0.010 (95% CI -0.062 to 0.083, p = 0.781), n = 730 in both.
- After adjusting for promo and a time index, the temperature coefficient is -0.046 (p = 0.71).

### Does the promo effect vary with temperature?

**Linear interaction (n = 730).** The temperature-by-promo coefficient is 0.49 sales units per degree (95% CI -0.68 to 1.67, p = 0.41). This test is inconclusive rather than a finding of no change: the interval is wide, so the data cannot rule out a meaningful change in how much promo helps as temperature changes.

**Promo effect within temperature terciles** (cut points 8.2 and 16.4 degrees). The promo effect is positive and significant in each band:

| Band | Promo effect (units) | 95% CI | n promo / non-promo | p |
|---|---|---|---|---|
| Cold (below 8.2) | +26.67 | 13.44 to 39.89 | 37 / 207 | < 0.001 |
| Mild (8.2 to 16.4) | +35.80 | 19.55 to 52.05 | 32 / 212 | < 0.001 |
| Warm (above 16.4) | +34.44 | 20.45 to 48.44 | 35 / 207 | < 0.001 |

The band estimates range from 26.67 to 35.80, but their intervals overlap widely.

![Promo effect on sales within temperature terciles, mean difference with 95% CI](tasks/stat_2/charts/promo_effect_by_band.png)

**Cubic polynomial in standardized temperature** (terms x, x², x³ interacted with promo; not a knotted spline). The joint F-test gives F = 0.42, p = 0.741. The promo:x coefficient is 2.20 (95% CI -13.43 to 17.82). The model implies a promo effect of 25.73 units at the 10th temperature percentile (2.7 degrees; 95% CI 10.85 to 40.61) and 34.12 at the 90th percentile (21.11 degrees; 95% CI 18.79 to 49.45). The point estimates differ, but the interaction test does not establish that the difference is real.

**Quartile bands.** The promo effect is positive in every quartile:

| Band | Promo effect (units) | 95% CI | n promo / non-promo | p |
|---|---|---|---|---|
| Q1 | +21.94 | 5.45 to 38.43 | 28 / 156 | 0.009 |
| Q2 | +40.56 | 23.96 to 57.16 | 31 / 152 | < 0.001 |
| Q3 | +29.44 | 10.88 to 48.00 | 19 / 162 | 0.002 |
| Q4 | +34.00 | 19.01 to 49.00 | 26 / 156 | < 0.001 |

The joint promo-by-quartile interaction test gives F = 0.95, p = 0.414.

![Promo effect on sales within temperature quartile bands, mean difference with 95% CI](tasks/stat_3/charts/promo_effect_by_quartile_band.png)

**Verdict.** The tercile, cubic and quartile analyses all fail to find a significant interaction, and none rules out a change. The data do not settle whether the promo effect varies with temperature.

### Time trend and promo

- Sales rise over the period. Quarterly means are 223.16 (2023Q1, n = 90), 233.84 (2023Q2), 249.12 (2023Q3), 266.14 (2023Q4), 277.28 (2024Q1), 288.70 (2024Q2), 306.80 (2024Q3) and 321.05 (2024Q4, n = 91). Quarterly medians rise from 221.3 to 317.8, and each quarter is higher than the one before.
- Monthly means in 2024 exceed those in 2023 for all 12 calendar months (for example, January 219.66 in 2023 versus 275.71 in 2024; December 262.69 versus 324.43).

![Mean and median daily sales per calendar quarter, 2023-2024](tasks/eda_2/charts/sales_by_quarter.png)

- After adjusting for promo and temperature, sales rise by 0.153 units per day (p = 7.1e-175).
- With only two years of data, a seasonal (month-of-year) pattern cannot be separated from the upward level shift. The monthly pattern is best read as trend.
- Adjusting for the time index barely changes the promo estimate. The promo coefficient is 31.96 (95% CI 27.19 to 36.72, p = 1.2e-35, n = 730), against the uncontrolled difference of 32.12.

### Promo share over time

- Promo share does not differ significantly between years: 13.97% of 2023 days and 14.52% of 2024 days (chi-square = 0.045, p = 0.83). A non-significant result does not establish that the shares are equal.
- Promo share by calendar quarter ranges from 6.6% (2024Q2) to 19.8% (2024Q1): 2023Q1 13.3%, 2023Q2 12.1%, 2023Q3 14.1%, 2023Q4 16.3%, 2024Q1 19.8%, 2024Q2 6.6%, 2024Q3 15.2%, 2024Q4 16.5%.
- Across the eight quarters, promo share does not differ significantly: chi-square = 7.82, dof = 7, p = 0.35.

![Percent of days flagged promo in each calendar quarter, 2023-2024](tasks/stat_4/charts/promo_share_by_quarter.png)

- Adding quarter dummies to the model (sales ~ promo + temperature + time index) gives a promo coefficient of 32.10 (95% CI 27.27 to 36.94, p = 4.7e-35), essentially unchanged from 31.96 without them. The quarterly variation in promo share does not appear to confound the promo estimate.

![Percent of days flagged promo in each calendar quarter, 2023-2024 (stat 5)](tasks/stat_5/charts/promo_share_by_quarter_stat5.png)

### Predictive models

Evaluation uses an 80/20 split (584 training rows, 146 test rows, random_state 42), with temperature and promo as features.

| Model | Test RMSE (sales units) | Test R² |
|---|---|---|
| Mean-of-train baseline | 38.78 | -0.038 |
| Linear regression | 36.72 | 0.069 |
| Random forest | 40.31 | -0.12 |

- The linear model has a lower test RMSE than the baseline (36.72 against 38.78). Its R² of 0.069 means it explains about 7% of test variance, which the analysis describes as a modest improvement.
- The random forest does not beat the baseline. Its train R² is 0.32 against test R² of -0.12, which indicates overfitting.
- On the linear model, permutation importance shows that shuffling promo raises test RMSE by 2.60 on average (sd 0.80). Shuffling temperature raises it by 0.035 (sd 0.048), within noise.
- The random forest's built-in importance ranks temperature first (0.84) and promo second (0.16). This disagrees with the permutation result on the linear model. The two measures were not reconciled.

![Test RMSE in sales units (lower is better) of the mean baseline, linear regression and random forest on the 146-row test split](tasks/ml_2/charts/ml_2_test_rmse.png)

## Limitations

- **Sample and period.** The data cover two years (2023-01-01 to 2024-12-30) and 730 days. Seasonality cannot be separated from the trend with this span.
- **Promo subgroups are small.** Promo days number 104 of 730. The tercile and quartile subgroups contain 19 to 37 promo days each, which widens their intervals.
- **Interaction tests are underpowered.** The interaction tests are inconclusive (see Findings). They do not rule out a meaningful change in the promo effect across temperature.
- **Cubic polynomial, not a spline.** The temperature-by-promo model in stat_3 uses a cubic polynomial in standardized temperature. It is not a knotted spline, and the result depends on that functional form.
- **Task status.** The stat_3 task is marked partial. Its spline and quartile analyses are reported above, but the sensitivity of the promo effect to cut points or to a knotted spline with different degrees of freedom was not tested.
- **Unrun tests.** Temperature-band differences in sales (the ANOVA or Kruskal-Wallis test) were raised by eda_1 and stat_1 but not run. The band differences are reported descriptively only.
- **Model scope.** The predictive models use only temperature and promo. Date-derived features were not added to any model. The random forest overfits and does not beat the baseline.
- **Disagreeing importance measures.** The random forest's built-in importance (temperature first) disagrees with permutation importance on the linear model (promo first). The analysis reports both and does not resolve the disagreement.
- **Chi-square assumptions.** The expected cell counts for the quarterly promo-share test were not checked, so the reliability of the chi-square approximation is unconfirmed.

## Open questions

- Does the promo effect differ between 2023 and 2024 (promo × year interaction)?
- Does a linear time trend or a level shift better describe the rise in sales?
- Is the promo effect sensitive to the choice of tercile or quartile cut points, or to a true knotted spline with different degrees of freedom?
- Do the temperature-band differences in sales (Q1 to Q4) reach statistical significance under an ANOVA or Kruskal-Wallis test with effect sizes?
- Do sales vary by day of week or other short-cycle patterns? No weekly-pattern test was run.
- Are the expected counts per quarter large enough for the chi-square approximation to be reliable?
- Why does the random forest's built-in importance rank temperature first while permutation importance on the linear model shows temperature contributing almost nothing?
- Does adding date-derived features (trend or seasonality) improve test RMSE over the temperature-and-promo linear model? Does a temperature-by-promo interaction or spline improve it?