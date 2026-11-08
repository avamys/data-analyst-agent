# Predicting a Binary Survey Outcome from Five Numeric Features and Group: 800 Rows, Target `outcome`

## Summary

- **No group or numeric-feature association survived correction.** The outcome rate by group ranged from 46.2% (g1) to 36.8% (g4), but the chi-square test gave p=0.289 (Cramér's V=0.068). No numeric feature passed Holm correction (smallest adjusted p=0.897, feat_3). All numeric effect sizes are tiny, and every confidence interval includes zero.
- **The feat_3 Q5 drop is nominal.** Q5 had a 33.1% outcome rate against 43.1% for Q1–Q4 pooled (z=-2.30, p=0.021). The quintile chi-square was not significant (p=0.223), the linear trend was not significant (p=0.133), and the Q5 result does not survive Bonferroni correction over five quintiles (p≈0.107).
- **No feature-by-group interaction was confirmed.** The strongest raw signal was feat_3 (LR p=0.029), which fell to a Holm-adjusted p of 0.147.
- **No model beats the majority-class baseline.** On the shared 80/20 split, logistic regression scored 0.550 and gradient boosting 0.531, against 0.5875 for always predicting class 0. Repeated 5-fold CV gave mean ROC AUC of 0.492 (logistic regression) and 0.479 (gradient boosting), against 0.5 for the baselines. Both models had higher log loss than a prior-only forecast.
- **The feature importance ranking is not reliable.** feat_3 ranks first on permutation importance, but the logistic regression behind that ranking has a test ROC AUC of 0.391, so it describes a model that does not beat chance.

## Data

- **Size:** 800 rows × 7 columns.
- **Target:** `outcome`, binary. 0: 58.9% (471 rows); 1: 41.1% (329 rows).
- **Features:** Five numeric features (feat_1 to feat_5) and one categorical feature, `group`. No date/time features, and no ids or free text.
- **Missing values:** None in any column.
- **Group levels:** The task framing lists g1–g3 as observed, but the EDA and tests report four levels, g1 to g4 (n=182, 206, 200, 212). The analysis below uses the four levels reported in the results.

## Findings

### Overall and group outcome rates

The outcome rate by group is shown below. The EDA found a gradient across group levels, but the test found it not significant. The gradient should not be read as an effect.

![Proportion of outcome=1 within each group level](tasks/eda_1/charts/outcome_rate_by_group.png)

- Outcome rate by group: g1 46.2% (n=182), g2 42.2% (n=206), g3 40.0% (n=200), g4 36.8% (n=212).
- Chi-square test of group vs outcome: χ²(3)=3.75, p=0.289, Cramér's V=0.068 (n=800). This is a negligible-to-small association. The group test was run separately and was not part of the Holm family for the numeric features.
- Adjusted group effect: The planned test of whether the group difference holds after adjusting for the features was not reported as a separate result. Group enters the logistic regression models only through the standardized coefficients reported under Feature importance below.

### Outcome rates by numeric feature quintile (EDA)

- **feat_1:** Q1 45.6%, Q2 37.5%, Q3 41.0%, Q4 37.1%, Q5 44.4% (n=160 each, Q3 n=161). No monotone trend.
- **feat_2:** Q1 38.1%, Q2 44.4%, Q3 41.6%, Q4 40.6%, Q5 40.9% (n=159–161). Flat, with no clear trend.
- **feat_3:** Q1 42.5%, Q2 42.2%, Q3 45.3%, Q4 42.5%, then Q5 33.1% (n=160 each, Q2 n=161, Q3 n=159). The clearest pattern in the EDA.
- **feat_4:** Q1 40.0%, Q2 42.5%, Q3 39.4%, Q4 45.6%, Q5 38.1% (n=160 each). No monotone trend.
- **feat_5:** Q1 38.8%, Q2 39.4%, Q3 39.4%, Q4 45.6%, Q5 42.5% (n=160 each). A mild upward tendency.

Feature means by outcome class (outcome=0 vs outcome=1):
- feat_1: 0.011 (SD 0.989) vs -0.002 (SD 1.067)
- feat_2: -0.006 (SD 1.029) vs 0.011 (SD 0.975)
- feat_3: 0.055 (SD 1.015) vs -0.027 (SD 0.967)
- feat_4: 0.062 (SD 1.005) vs 0.057 (SD 0.958)
- feat_5: 0.001 (SD 1.022) vs 0.092 (SD 0.994)

### Significance and effect sizes for numeric features

Each feature was compared between outcome classes with a Mann-Whitney test. Holm correction covered the five numeric features only.

| Feature | Raw p | Holm p | Rank-biserial | Cohen's d | Mean difference (95% CI) |
|---|---|---|---|---|---|
| feat_3 | 0.179 | 0.897 | -0.056 | -0.083 | -0.082 (-0.222 to 0.057) |
| feat_5 | 0.210 | 0.897 | 0.052 | 0.090 | 0.091 (-0.051 to 0.233) |
| feat_1 | 0.740 | 1.000 | -0.014 | -0.013 | -0.014 (-0.160 to 0.132) |
| feat_4 | 0.864 | 1.000 | 0.007 | -0.005 | -0.005 (-0.143 to 0.133) |
| feat_2 | 0.978 | 1.000 | 0.001 | 0.017 | 0.017 (-0.124 to 0.158) |

No numeric feature shows a significant outcome difference, and all confidence intervals include zero. The rank-biserial and Cohen's d measures differ, so the numeric effects are ranked only among themselves, not against the group Cramér's V.

### feat_3 quintiles: is the Q5 drop real?

![Outcome rate (%) by feat_3 quintile, n per quintile shown in the facts](tasks/stat_3/charts/feat3_quintile_outcome_rate.png)

- Outcome rate by quintile: Q1 42.5% (n=160), Q2 42.2% (n=161), Q3 45.3% (n=159), Q4 42.5% (n=160), Q5 33.1% (n=160). Events per quintile: 68, 68, 72, 68, 53.
- Quintile vs outcome chi-square: χ²(4)=5.70, p=0.223, Cramér's V=0.084.
- Cochran-Armitage linear trend over quintiles 1–5: z=-1.50, p=0.133.
- Deviation from linearity: χ²(3)=3.44, p=0.329. This does not establish linearity, because five bins have limited power to detect non-linear patterns.
- Q5 vs Q1–Q4 pooled: 33.1% (n=160) vs 43.1% (n=640), z=-2.30, p=0.021. This is nominal. Q5 was selected post hoc from five quintiles, and Bonferroni over five gives p≈0.107, which is not significant.

### Feature-by-group interaction

No feature-by-group interaction survives Holm correction across feat_1 to feat_5 (none significant at 0.05 after correction).

| Feature | LR statistic (3 df) | Raw p | Holm p |
|---|---|---|---|
| feat_3 | 8.99 | 0.029 | 0.147 |
| feat_2 | 6.29 | 0.098 | 0.394 |
| feat_5 | 3.48 | 0.323 | 0.968 |
| feat_1 | 0.95 | 0.813 | 1.000 |
| feat_4 | 1.30 | 0.729 | 1.000 |

- feat_3's nominal signal: the g2 contrast has coefficient -0.418 with raw Wald p=0.049. It does not survive correction, so it is not a confirmed group modification. The tests have limited power, so a non-significant result does not exclude a modest group modification.
- Descriptive per-unit odds ratios for feat_3 from the feat_3×group logit (g1 as reference): g1 1.02, g2 0.67, g3 0.90, g4 1.22. These are descriptive only and do not establish group-specific effects.

### Predictive models on the shared 80/20 split

The split was stratified, with random_state 42: 640 training rows and 160 test rows. It is saved as train_test_split.pkl for reuse. The test-set majority baseline is 0.5875 (the full-data rate is 58.9%).

![Test accuracy of each model against the majority-class baseline on the shared 80/20 split](tasks/ml_1/charts/ml1_accuracy_vs_baseline.png)

- **Logistic regression** (features plus one-hot group, scaled): test accuracy 0.550 (train 0.586), precision 0.313, recall 0.076, F1 0.122, ROC AUC 0.392, test log loss 0.709.
- **Gradient boosting** (same inputs): test accuracy 0.531 (train 0.836), precision 0.400, recall 0.273, F1 0.324, ROC AUC 0.466, test log loss 0.754.
- **Prior-only log loss** on the test set: 0.678.

On this split, neither model beats the majority baseline on accuracy. Gradient boosting overfits, with train accuracy 0.836 against test accuracy 0.531. Both models have higher log loss than the prior-only forecast.

### Cross-validated model estimates

Repeated stratified 5-fold CV (3 repeats, 15 folds):

| Model | Mean accuracy (SD) | Mean ROC AUC (SD) | Mean log loss (SD) | Folds beating majority accuracy |
|---|---|---|---|---|
| Logistic regression | 0.567 (0.018) | 0.492 (0.045) | 0.687 (0.012) | 1 of 15 (6.7%) |
| Gradient boosting | 0.535 (0.033) | 0.479 (0.039) | 0.750 (0.035) | 0 of 15 (0%) |
| Majority class | 0.589 (0.003) | 0.5 (0) | — | — |
| Prior only | — | — | 0.677 (0.001) | — |

- Both models average below the majority-class accuracy of 0.589.
- Both models' mean ROC AUC is at or slightly below 0.5. Gradient boosting's mean is about 2.1 naive standard errors below 0.5. The folds are correlated, so the naive standard error is optimistic, and this was not formally tested against chance.
- Logistic regression's log loss is 0.687 (SD 0.012) against 0.677 for the prior-only baseline. Gradient boosting's log loss is 0.750 (SD 0.035), which is clearly worse and more variable.

The conclusion is that neither model beats the majority-class or prior-only baselines consistently across folds. The single-split result is confirmed.

![CV accuracy of logistic regression and gradient boosting against the majority-class baseline](tasks/ml_3/charts/ml3_cv_accuracy.png)

### Feature importance

On the shared test split, the logistic regression permutation importance (ROC AUC drop, mean and SD over 30 repeats) was:

- feat_3: 0.022 (SD 0.007), the largest mean drop on this split.
- group_g3: 0.005 (SD 0.010)
- feat_2: 0.004 (SD 0.006)
- group_g2: 0.002 (SD 0.007)
- feat_4: -0.011 (SD 0.010)
- feat_1: -0.018 (SD 0.010)
- feat_5: -0.040 (SD 0.022)
- group_g4: -0.094 (SD 0.036)

Interpretation:

- The feat_3 lead is the largest value in this table, but it describes a logistic regression whose test ROC AUC is 0.391, below chance. The ranking is therefore not evidence of a reliable predictor. It is also not consistent with stat_1, where feat_3 has raw p=0.179 and Holm p=0.897.
- feat_2, group_g3 and group_g2 have positive mean drops smaller than their SDs, and feat_4 has a negative mean drop within about one SD. These are treated as within noise.
- feat_1 (mean drop -0.018, SD 0.010) does not meet the within-one-SD criterion, so it is not classified as within noise.
- feat_5 and group_g4 have negative mean drops beyond their SDs. On this split, permuting these features was associated with higher test AUC. This describes the model's behaviour on this split only; it is not evidence of a real effect.
- Signed standardized logistic regression coefficients: feat_5 +0.139, feat_2 +0.034, group_g4 -0.253, group_g3 -0.076, feat_1 -0.064, feat_4 -0.055, feat_3 -0.048, group_g2 -0.029. The coefficient ranking (group_g4 and feat_5 on top) disagrees with the permutation ranking (feat_3 on top). Both are reported as stated, and they are not resolved here.

## Limitations

- **Sample size:** 800 rows, with a 160-row test split. Single-split estimates, including the test AUC of 0.392 for logistic regression, are unstable.
- **Group levels:** The task framing lists g1–g3 as observed, while the results report g1–g4. This discrepancy is not resolved here.
- **Power:** Interaction tests and the five-bin quintile analysis have limited power. A non-significant result does not establish absence of an effect.
- **Multiple comparisons:** The feat_3 Q5 result and the feat_3 interaction are nominal and do not survive correction.
- **Model performance:** Both models are at or below the majority baseline, and at or below chance on AUC across CV. Gradient boosting overfits (train accuracy 0.836 vs test 0.531). Regularization was not tuned in the tasks reported.
- **Unresolved review issues, ml_2 (permutation importance and coefficients):**
  - (1) feat_1 is not within noise, so it is not listed with feat_2, feat_4, group_g2 and group_g3.
  - (2) The feat_3 lead is reported alongside the stat_1 result (raw p=0.179, Holm p=0.897) and the logistic regression test AUC of 0.391. The permutation ranking describes a model that does not beat chance and is not evidence of a reliable predictor.
  - (3) The phrase "most consistent result" is removed, because the ranking rests on one split and is unstable.
  - (4) The negative drops for feat_5 and group_g4 are described only as model behaviour on this split.
- **Failed tasks:** None reported.

**Numbers not traced to a recorded fact.** The automatic check found no recorded value for these numbers:
- 471 in: "- **Target:**  , binary. 0: 58.9% (471 rows); 1: 41.1% (329 rows)."

## Open questions

- Does the feat_3 Q5 pattern hold in a logistic regression with feat_3 as a continuous term and a Q5 indicator, adjusted for group and feat_1 to feat_5?
- Is the Q5 drop stable across other binnings (deciles or splines) or across bootstrap resamples?
- Does the feat_3 non-linear quintile pattern differ by group? A quintile-by-group interaction test was suggested but not run.
- Does the feat_3 by group interaction replicate in an independent sample, or add predictive value in a pooled or nested model?
- Do feature importance rankings and coefficient signs (feat_3 on top for permutation, group_g4 and feat_5 on top for coefficients) hold under cross-validation on the full data?
- Does permutation importance for gradient boosting, the best model from the earlier task, agree with the logistic regression ranking?
- Does gradient boosting with stronger regularization close its train-test gap and reach chance-level or better log loss under CV?
- Is there any feature subset or simple model that beats the prior-only log loss consistently across folds?
- Would repeated CV with more repeats, or nested resampling, give tighter estimates of the ROC AUC, which is at or below 0.5?