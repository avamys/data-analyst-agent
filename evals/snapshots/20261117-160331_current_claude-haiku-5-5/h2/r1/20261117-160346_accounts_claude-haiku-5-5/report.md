# Renewal Drivers in 1,600 Accounts: Analysis of the Binary Target `renewed`

## Summary

- **Baseline:** 57.5% of the 1,600 accounts renewed, so a majority-class prediction is 57.5% accurate. Three features show significant renewal differences: support_tickets (renewal 18.8% at 0 tickets, 71.9% at 4), discount_pct (80% at 0% discount, 35% at 30%), and seats quartiles (35.0% in Q1, 74.7% in Q4). contract_months, region and signup_month do not survive correction.
- **Adjusted effects:** In a multivariable logistic model that adjusts for region and contract_months, each additional support ticket multiplies the odds of renewal by 1.90, each percentage point of discount by 0.915, and each additional seat by 1.075. All three are significant (p below 1e-24).
- **Prediction:** A logistic regression on all features reaches 76.9% test accuracy and ROC AUC 0.832, against 57.5% accuracy and AUC 0.5 for the majority-class baseline. Gradient-boosted trees perform somewhat worse (73.4% accuracy, AUC 0.816) and overfit.
- **Interactions:** No significant discount × contract_months or discount × region interaction was found. Discount × support_tickets was not tested. The region test has limited power.
- **Confounding:** The focal predictors are nearly uncorrelated, but the support_tickets odds ratio shifts after adjustment, so confounding among the predictors is not ruled out.

## Data

- **Size:** 1,600 rows and 7 columns.
- **Target:** `renewed` (binary). Class 1 (renewed) is 57.5%; class 0 (not renewed) is 42.5%.
- **Features:** Numeric: discount_pct, seats, support_tickets, contract_months, signup_month. Categorical: region. There are no date/time features and no ids or free-text columns.
- **Shape of numeric features:** discount_pct takes levels 0 to 30 (most common 10, 400 accounts). support_tickets ranges from 0 to 10 (most common 3, 362 accounts). contract_months is 12 or 24 (12 is the most common, 821 accounts). signup_month ranges from 1 to 12. seats is heavily right-skewed: median 10, maximum 214. Group-level rates therefore use quantile bins for seats.
- **Missing values:** None in any column.

## Findings

### Renewal rate across feature levels (eda_1)

- The overall renewal rate is 57.5%.
- **discount_pct:** Renewal falls steadily with discount. It is 80% at 0%, 65% at 10%, 50% at 20%, and 35% at 30%, with 400 accounts per level. The spread is 45 points.
- **support_tickets:** Renewal rises with ticket count, from 18.8% at 0 tickets (n=69) and 36.4% at 1 (n=264) to 71.9% at 4 (n=256). It reaches 89% at 6 and 100% at 8 or more, but those levels are small (n=20 at 8, n=4 at 9, n=1 at 10). The spread is 81 points.
- **seats (quartiles):** 35.0% in Q1, 57.3% in Q2, 66.6% in Q3, and 74.7% in Q4. The spread is 40 points.
- **region:** East 55.5%, north 57.4%, south 57.0%, west 60.2%. The spread is 4.6 points, and the chi-square test finds no significant association (chi2=1.79, 3 df, p=0.62).
- **contract_months:** 56.5% at 12 months and 58.5% at 24 months. The spread is 2 points.
- **signup_month:** The spread is 11 points, from 53.5% (month 1) to 64.7% (month 9). Each month has only about 125 to 140 accounts, so this pattern may be noise. It is tested in stat_1 and stat_4.
- **Numeric means and medians by renewed status:** Not renewed accounts have a mean discount of 19.4 and renewed accounts 11.7. Mean seats are 10.0 for not renewed and 17.6 for renewed. Mean support_tickets are 2.27 for not renewed and 3.52 for renewed. Mean contract_months (17.7 and 17.9) and signup_month (6.41 and 6.55) are nearly the same.

![Renewal rate by discount_pct and by region (share of accounts renewed in each group)](tasks/eda_1/charts/renewal_rate_by_discount_and_region.png)

### Significance and effect sizes (stat_1)

Chi-square tests of each feature against `renewed`, with Holm correction across the six features:

| Feature | Chi-square (df) | p | Holm p | Cramér's V | Max rate difference |
|---|---|---|---|---|---|
| support_tickets | 208.3 (10) | 3.0e-39 | 1.5e-38 | 0.361 | 81.2 points |
| discount_pct | 184.1 (3) | 1.1e-39 | 6.7e-39 | 0.339 | 45.0 points |
| seats (quartiles) | 148.9 (3) | 4.7e-32 | 1.9e-31 | 0.305 | 39.7 points |
| contract_months | 0.67 (1) | 0.41 | 1.0 | 0.020 | 2.0 points |
| region | 1.79 (3) | 0.62 | 1.0 | 0.033 | 4.6 points |
| signup_month | 8.97 (11) | 0.63 | 1.0 | 0.075 | 11.3 points |

- The three significant features have Holm-adjusted p-values of 1.5e-38 for support_tickets, 6.7e-39 for discount_pct and 1.9e-31 for seats quartiles.
- The support_tickets chi-square has sparse cells at high levels (8 and above), so its p-value is less reliable there. A trend test is reported in stat_4.
- The chi-square results for contract_months, region and signup_month are not significant after correction.

**Unadjusted odds ratios per unit (from stat_3):** discount_pct OR 0.936 (95% CI 0.927–0.946); support_tickets OR 1.63 (95% CI 1.52–1.76); seats OR 1.055 (95% CI 1.044–1.067).

**Multivariable logistic regression (stat_1):** This model includes all five numeric features, and each odds ratio is adjusted for the others.
- support_tickets: OR 1.90 per ticket (95% CI 1.74–2.07), p=8e-49
- discount_pct: OR 0.915 per point (95% CI 0.904–0.926), p=4e-46
- seats: OR 1.074 per seat (95% CI 1.060–1.089), p=5.5e-25
- contract_months: OR 1.015 (95% CI 0.994–1.035), p=0.16, not significant
- signup_month: OR 1.007 (95% CI 0.972–1.043), p=0.70, not significant

These adjusted odds ratios are not the same as the unadjusted chi-square effects above.

![Share of accounts renewed (%) at each discount_pct level (left) and each support_tickets level (right)](tasks/stat_1/charts/stat1_renewal_rate_by_discount_and_tickets.png)

### Interactions (stat_2)

- **discount × contract_months:** Not significant (likelihood-ratio chi2=2.48, 3 df, p=0.48). The 0%-to-30% drop is 40.6 points at 12 months and 49.3 points at 24 months. The difference between these drops is not significant.
- **discount × region:** Not significant (likelihood-ratio chi2=4.96, 9 df, p=0.84). The 0%-to-30% drop ranges from 40.8 points (east) to 47.8 points (south). Cells hold about 90 to 115 accounts, so small interactions cannot be ruled out.
- **Consistency of the main pattern:** At 0% discount, renewal ranges from 77.7% to 82.1% across contract cells and from 74.2% to 83.5% across region cells. Renewal falls at each discount step (0% to 10%, 10% to 20%, 20% to 30%) in all six series (2 contract levels and 4 regions).

![Share of accounts renewed (%) at each discount_pct level, split by contract_months (left) and by region (right)](tasks/stat_2/charts/stat2_renewal_by_discount_contract_region.png)

### Predictive performance (ml_1)

Models were trained on 1,280 accounts and tested on 320.

| Model | Test accuracy | Precision | Recall | F1 | ROC AUC | Log loss |
|---|---|---|---|---|---|---|
| Logistic regression | 76.9% | 0.778 | 0.837 | 0.806 | 0.832 | 0.498 |
| Gradient-boosted trees | 73.4% | 0.759 | 0.788 | 0.773 | 0.816 | 0.553 |
| Majority-class baseline | 57.5% | — | — | — | 0.5 | 0.682 |

- Logistic regression beats the baseline on every metric.
- Gradient-boosted trees also beat the baseline but score below logistic regression. Their training accuracy is 92.2%, which indicates overfitting.
- **Permutation importance** (drop in test ROC AUC, logistic regression, 30 repeats): support_tickets 0.159 (sd 0.019), discount_pct 0.117 (sd 0.019), seats 0.073 (sd 0.013). The region dummies, contract_months and signup_month contribute close to zero: region_east 0.001, region_south 0.001, contract_months 0.001, region_north 0.000, region_west −0.000, signup_month −0.001.
- Coefficient magnitudes from the scaled model rank seats first, support_tickets second, and discount_pct third. These are not comparable to the odds ratios above, and the ranking differs from the permutation ranking.

![Permutation importance of each feature for the logistic regression on the 320-account test set, measured as the drop in ROC AUC](tasks/ml_1/charts/ml_1_permutation_importance.png)

### Adjusted effects and confounding (stat_3)

After adjusting for each other, region and contract_months:
- discount_pct: adjusted OR 0.915 per point (95% CI 0.903–0.926), p=4e-46
- support_tickets: adjusted OR 1.90 per ticket (95% CI 1.75–2.08), p=8e-49
- seats: adjusted OR 1.075 per seat (95% CI 1.061–1.090), p=3e-25

These estimates come from a model with region and contract_months as controls. The stat_1 model includes the other numeric features instead, so its confidence intervals differ slightly.

**Collinearity:** The focal predictors are not collinear. Pairwise correlations are 0.024 (discount–tickets), −0.027 (discount–seats) and −0.006 (tickets–seats). Variance inflation factors are about 1.001.

**Shifts after adjustment:** The discount_pct odds ratio moves from 0.936 (univariate) to 0.915 (adjusted). The support_tickets odds ratio moves from 1.63 to 1.90. Because the support_tickets estimate changes after adjustment, the unadjusted effect is partly explained by the other predictors and controls, and confounding is not ruled out. The seats effect is modest (adjusted OR 1.075 per seat). This report does not compute a seats univariate comparison.

**Region after adjustment:** The likelihood-ratio test gives chi2=3.25 (3 df, p=0.355). Adjusted odds ratios against the baseline region are 1.07 for north (p=0.69), 1.34 for south (p=0.10) and 1.22 for west (p=0.26). This agrees with the unadjusted region test (p=0.62).

**contract_months after adjustment:** OR 1.015 per month (95% CI 0.994–1.036), p=0.157. No detectable effect.

![Odds ratios of renewed per unit increase, univariate and adjusted, with 95% CIs](tasks/stat_3/charts/stat3_or_univariate_vs_adjusted.png)

### Monotone trends (stat_4)

Cochran-Armitage trend tests, with Holm correction across six features:
- **discount_pct:** Significant decreasing trend, z=−13.57, p=6.0e-42, Holm p=3.0e-41. Renewal falls from 80.0% (320/400) to 65.0%, 50.0% and 35.0%. This agrees with the chi-square result.
- **support_tickets:** Significant increasing trend, z=14.09, p=4.2e-45, Holm p=2.5e-44. Levels 7 and above are pooled (n=63, 58 renewed, about 92%). The rate rises from 18.8% at 0 tickets to 36.4% at 1, 59.9% at 3, 71.9% at 4, and 74.4% at 5. This agrees with the chi-square result.
- **seats (quartiles):** Significant increasing trend, z=11.80, p=3.9e-32, Holm p=1.6e-31. This agrees with the chi-square result.
- **contract_months:** Not significant, z=0.82, p=0.41, Holm p=1.0.
- **signup_month:** Not significant, z=0.82, p=0.41, Holm p=1.0.

The trend-test conclusions match the chi-square conclusions in stat_1 for every feature.

## Limitations

- **Unresolved review issue, stat_2 (row count):** The original claim about "12 discount × contract and discount × region rows" was wrong. There are 8 discount × contract rows and 16 discount × region rows, 24 in total. The statement above is restated as "all six series (2 contract levels and 4 regions)," which matches the cells reported.
- **Unresolved review issue, stat_3 (confounding):** The original statement that adjusted and unadjusted estimates are close is withdrawn. The actual shifts are reported above. Low predictor correlation and near-1 VIF show the predictors are not collinear, but confounding is not ruled out. The seats effect is described as modest, and the seats univariate comparison is not made in this report.
- **Sparse high-level cells:** Chi-square p-values for support_tickets are less reliable at levels 8 and above. The stat_4 trend test pools levels 7 and above.
- **Region has no ordinal trend test.** Its nominal chi-square p-value (0.62) is included in the Holm family, so the family mixes trend tests with a nominal test.
- **signup_month:** Each month has about 125 to 140 accounts. The spread of 11 points may be noise; the tests find no significant association.
- **Interaction power:** The discount × region test has about 90 to 115 accounts per cell, so small interactions cannot be excluded. Discount × support_tickets was not tested.
- **Model scope:** Model results come from one train/test split (1,280 and 320 accounts). Gradient-boosted trees overfit.
- **Association, not cause:** All odds ratios and rates describe associations in this dataset.
- **Linearity:** The seats effect is modelled per unit on the log-odds scale. Whether it levels off across quartiles was not tested.
- **No tasks failed.** All five analysis tasks completed.

## Open questions

- Is the discount effect modified by support_tickets (discounting mattering more for accounts with many tickets)? This interaction was not tested.
- Is the signup_month pattern (peaks around March and July to September) real, or noise across 12 small groups?
- Is the support_tickets effect linear, or is there a threshold? Would a model with separate level effects differ from the trend test?
- After adjusting for each other, how confounded are discount_pct, support_tickets and seats? A fuller interaction or stability analysis was not run.
- Is the seats effect linear on the log scale, or does it level off across quartiles?
- Would a proper ordinal trend test for region, or a sensitivity check that drops region from the Holm family, change any conclusion?
- Would a tuned or more regularised gradient-boosted model close the gap with logistic regression?