# Score Prediction from Six Numeric Features: 60-Row Regression Analysis

## Summary

- **feat_1 is the only feature with a significant linear association with score.** The OLS slope is 4.74 score units per unit of feat_1 (95% CI 1.97 to 7.50, p = 0.001, Holm-adjusted p = 0.007). Pearson r is 0.41 (95% CI 0.18 to 0.60). The other five features show no significant association after adjustment.
- **feat_3 and feat_6 have weak negative associations that are not significant.** feat_3 has a slope of -2.71 (95% CI -5.57 to 0.15, Holm p = 0.31). feat_6 has a slope of -1.69 (95% CI -4.34 to 0.97, Holm p = 0.83). The data cannot rule out meaningful negative effects for feat_3, but they do not establish one.
- **No feature pair interacts significantly.** Of the seven interaction terms tested, the smallest raw p-value is 0.14, and all Holm-adjusted p-values are at least 0.985. The sample is too small to detect moderate interactions.
- **Prediction gains are not established at n = 60.** Linear regression and random forest on all six features do not beat a mean-only baseline in 5-fold CV. A feat_1-only linear model does beat the baseline (CV R-squared 0.098 vs -0.105), but feature selection was not repeated inside the folds, so this gain is optimistically biased.

## Data

- **Size:** 60 rows, 7 columns.
- **Target:** score (numeric, regression).
- **Features:** six numeric features (feat_1 to feat_6). There are no categorical, date/time, identifier, or free-text columns.
- **Missing values:** none in any column (0 of 60 rows per column). No rows were dropped.
- **Duplicates:** 0 fully duplicated rows.
- **Constant features:** none. Unique-value counts range from 50 to 56 for every feature except feat_1, which has 51.

## Findings

### Score distribution and feature overview

Score is roughly symmetric and close to normal in shape: mean 48.95, median 48.75, SD 11.22, min 25.3, max 75.6, skew -0.15, excess kurtosis -0.22 (n = 60). This read rests on skew and kurtosis only. No formal normality test was run.

![Histogram of score, counts of rows per bin (60 rows)](tasks/eda_1/charts/score_histogram.png)

Correlations of each feature with score (Pearson r; Spearman rho in parentheses):

| Feature | Pearson r (p) | Spearman rho (p) |
|---|---|---|
| feat_1 | 0.41 (0.001) | 0.47 (0.0001) |
| feat_2 | 0.02 (0.88) | 0.06 (0.64) |
| feat_3 | -0.24 (0.063) | -0.21 (0.116) |
| feat_4 | -0.09 (0.51) | -0.08 (0.57) |
| feat_5 | 0.08 (0.56) | 0.07 (0.60) |
| feat_6 | -0.16 (0.209) | -0.20 (0.119) |

feat_2, feat_4 and feat_5 show essentially no linear or monotonic relation with score (all p > 0.5).

![Scatter plot of each numeric feature against score, one point per row (60 rows)](tasks/eda_1/charts/feature_vs_score_scatter.png)

**Feature-to-feature correlation.** No pair of features exceeds |r| = 0.7, so no multicollinearity flag is raised. The largest absolute off-diagonal Pearson correlation is feat_2 with feat_5 at r = -0.185. feat_1 with feat_5 (r = -0.184) is not the largest pair; it is nearly tied with feat_2-feat_5 but falls just below it. The full 6×6 matrix is recorded in the analysis. Other pairs include feat_1-feat_6 at r = -0.15 and feat_4-feat_6 at r = 0.18.

### Linear associations with score (stat_1)

**feat_1 (significant).**
- OLS slope 4.74 (95% CI 1.97 to 7.50, p = 0.001, Holm-adjusted p = 0.007).
- Pearson r = 0.41 (95% CI 0.18 to 0.60).
- The feat_1 SD is 0.97, so a one-SD increase is associated with about +4.61 score units (95% CI +1.92 to +7.30). This is roughly 0.41 of the score SD of 11.2.
- The effect remains significant after Holm adjustment across the six tests.

**feat_3 (not significant after adjustment).**
- OLS slope -2.71 (95% CI -5.57 to 0.15, p = 0.063, Holm-adjusted p = 0.31).
- Pearson r = -0.24 (95% CI -0.47 to 0.01).
- The interval includes effects as large as about -5.6, so a meaningful negative effect is not ruled out, but neither is its absence.

**feat_6 (not significant).**
- OLS slope -1.69 (95% CI -4.34 to 0.97, p = 0.209, Holm-adjusted p = 0.835).
- Pearson r = -0.16 (95% CI -0.40 to 0.09).

**feat_2, feat_4, feat_5 (no significant association).**
- Slopes: feat_2 0.23 (95% CI -2.78 to 3.25, p = 0.88); feat_4 -0.98 (95% CI -3.92 to 1.95, p = 0.51); feat_5 1.30 (95% CI -3.12 to 5.72, p = 0.56).
- All Holm-adjusted p-values are 1.0, and all confidence intervals span zero.

### Interactions (stat_2)

Seven pairwise interaction terms were tested: feat_1 crossed with each other feature, plus feat_3 × feat_6 and feat_2 × feat_5. The pairs were chosen by design (feat_1 crossed with all others, feat_3 and feat_6 as the two marginal negative features, and feat_2 × feat_5 as the largest absolute feature correlation). Other pairs, such as feat_2 × feat_3 and feat_4 × feat_5, were not tested.

- No interaction is significant. The two closest are feat_2 × feat_5 (coefficient 3.51, 95% CI -1.21 to 8.23, p = 0.14, Holm 0.985) and feat_1 × feat_3 (coefficient -2.33, 95% CI -5.62 to 0.96, p = 0.16, Holm 0.985).
- The other five are feat_1 × feat_2 (-0.89, p = 0.70), feat_1 × feat_4 (-0.70, p = 0.72), feat_1 × feat_5 (2.35, p = 0.30), feat_1 × feat_6 (-0.17, p = 0.90) and feat_3 × feat_6 (-0.50, p = 0.70). All have Holm-adjusted p = 1.0.
- **Power:** at 80% power and alpha 0.05 (two-sided), the minimum detectable interaction coefficient is 3.6 to 6.6 score units per unit of product (mean 5.2). Residual SD is 10.07. Smaller interactions cannot be ruled out, so the null result is not evidence of no interaction.
- **Model fit:** the interaction model (six features and seven products, 14 parameters) has R-squared 0.37 and adjusted R-squared 0.19. The products are uncentered, so main-effect coefficients are unstable.

### feat_3 after controlling for feat_1 (stat_3)

- Controlling for feat_1, the feat_3 slope is -2.53 (95% CI -5.16 to 0.10, p = 0.059). The simple slope was -2.71, a 6.6% reduction in magnitude. Adding feat_1 does not explain away the feat_3 association, and the association remains non-significant.
- The two-feature model (feat_1 and feat_3) has R-squared 0.220. feat_1 keeps its positive effect. Adding all six features raises R-squared only to 0.273.
- In the full six-feature model, the feat_3 slope is -2.81 (95% CI -5.47 to -0.15, p = 0.039). This reaches nominal significance only when the other non-significant features are included. The evidence for a feat_3 effect beyond feat_1 is weak and fragile.

### Predictive models (ml_1)

All models were evaluated with 5-fold shuffled CV (seed 0) on the clean 60-row table.

| Model | CV R-squared (fold SD) | CV MAE (fold SD) |
|---|---|---|
| Mean-only baseline | -0.105 (0.078) | 8.82 (0.93) |
| Linear regression, all six features | -0.126 (0.378) | 9.00 (1.14) |
| Random forest, all six features | -0.151 (0.416) | 8.93 (1.44) |

![Per-fold cross-validated R-squared for the mean-predicting baseline, linear regression and random forest on the same 5 folds; black bar is the fold mean](tasks/ml_1/charts/ml1_model_cv_r2.png)

- Neither all-feature model beats the baseline. Their CV R-squared values are lower, their MAEs are higher, and the differences are inside the fold SD.
- The in-sample OLS slope on feat_1 is significant (slope 4.74, p = 0.001, R-squared 0.169 on all 60 rows). This does not translate into a CV gain for the all-feature models.
- Because the mean baseline has no importances by construction, permutation importances are reported for the two other models. The mean drop in R-squared when each feature is permuted, with fold SD in parentheses:

| Feature | Linear regression | Random forest |
|---|---|---|
| feat_1 | 0.430 (0.275) | 0.266 (0.228) |
| feat_2 | -0.002 (0.012) | -0.059 (0.129) |
| feat_3 | 0.088 (0.151) | -0.003 (0.082) |
| feat_4 | -0.084 (0.174) | -0.035 (0.065) |
| feat_5 | -0.028 (0.260) | -0.058 (0.099) |
| feat_6 | 0.043 (0.055) | 0.005 (0.063) |

feat_1 has the largest mean importance in both models. Because neither model beats the baseline, the other importances are unreliable.

### feature-only and regularized models (ml_2)

- **feat_1-only linear regression** has CV R-squared 0.098 (fold SD 0.113) and MAE 7.74 (fold SD 1.34). This is above the baseline on both metrics and is the only model in the analysis that beats the baseline.
- **Ridge regression on all six features** (alpha 1.0, standardized) has CV R-squared -0.116 (fold SD 0.371) and MAE 8.94 (fold SD 1.13). It does not beat the baseline. One fold has R-squared near -0.61.

![Mean 5-fold CV R-squared for the mean baseline, feat_1-only linear regression and ridge on all six features; error bars show fold sd](tasks/ml_2/charts/ml2_model_cv_r2.png)

The two sets of results differ because of the feature set. The feat_1-only model beats the baseline on the same folds, while the all-feature linear, ridge and random forest models do not. ml_1 did not test a feat_1-only model, so the results do not contradict each other. The feat_1-only gain is optimistically biased, because feat_1 was selected from correlations computed on all 60 rows and that selection was not repeated inside each fold. Five folds on 60 rows is also a small basis, so the result is suggestive rather than conclusive.

### Missing values (eda_2)

No values are missing in any of the seven columns (0 counts, 0.0%). There is therefore no missingness to relate to other columns or to score. There are no duplicate rows.

## Limitations

- **Sample size.** With 60 rows, estimates are imprecise and fragile. Several intervals span large effects, and the interaction tests are underpowered for moderate effects (minimum detectable coefficient about 3.6 to 6.6).
- **Multiple testing.** Six linear tests and seven interaction tests were run. Holm adjustment was applied, and only feat_1 survives it.
- **feat_3 and feat_6.** Their weak negative associations are not significant. feat_3 reaches nominal significance only in the full six-feature model (p = 0.039), which the analysis treats as fragile.
- **Linearity and robustness not checked.** The feat_1 relationship was assumed linear. No transformation, spline, outlier check or robust regression was run.
- **Normality not formally tested.** The "close to normal" description rests on skew and kurtosis only. No Shapiro-Wilk or similar test was run.
- **Selection bias in ml_2.** The feat_1-only CV gain uses a feature chosen on all 60 rows. Repeated CV with selection inside each fold was not run.
- **CV stability.** Fold SDs are large relative to the differences between models for the all-feature models, and five folds is a small basis.
- **Interaction coverage.** Only seven of the 15 possible pairs among the six features were tested. The chosen pairs were not exhaustive.
- **Unresolved review issue, feature-correlation claim (eda_1, also stated in stat_1, eda_2, ml_1).** The earlier eda_1 finding named feat_1-feat_5 as the largest feature correlation. That is incorrect. The largest absolute feature-to-feature Pearson correlation is feat_2-feat_5 at r = -0.185. feat_1-feat_5 (r = -0.184) is not the largest pair. This report uses the corrected pair. The claim that no pair exceeds |r| = 0.7 stands.
- **Unresolved review issue, permutation importances (ml_1).** The ml_1 importance section omitted feat_4, feat_5 and feat_6 for both models. Their values are now reported above from the recorded importance facts. Those values come from models that do not beat the baseline and should be read with the same caution as the other importances.
- **Disagreement across models.** ml_1 finds no CV gain over the baseline for models on all six features. ml_2 finds a CV gain for a feat_1-only model. The two results are reported as they stand. They differ by feature set, and the feat_1-only gain has the selection-bias caveat above.
- **Failed tasks.** None of the tasks reported failure.

## Open questions

- Does the feat_1 relationship hold on a larger sample, and is it linear, or does a transformation or spline fit better?
- Are the weak negative trends for feat_3 and feat_6 real, or noise at n = 60?
- Does feat_3 remain associated with score after controlling for feat_1 once collinearity (variance inflation factors) and outliers are checked? A robust or rank-based regression has not been run.
- Is the feat_1 effect robust to outliers, for example under a rank-based or robust regression?
- Do feat_2, feat_4 and feat_5 have non-monotonic or non-linear effects that correlation and linear models miss?
- Would a feat_1-only model still beat the baseline under repeated CV with different seeds and with feature selection repeated inside each fold?
- Do feat_2 through feat_6 add predictive value once feat_1 is included? Would tuned ridge or lasso on all features recover a gain over feat_1 alone?
- Do the interactions feat_2 × feat_5 and feat_1 × feat_3 become significant with centered features and a larger sample?
- Does the feat_1 slope differ across levels of feat_3 in a stratified or piecewise analysis?
- Is score normally distributed? A formal normality test has not been run.
- If future data contain missing values, does their occurrence depend on score or on the feature values?