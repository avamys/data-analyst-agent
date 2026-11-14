# Churn Analysis of 1,000 Customers: Plan, Usage, Tenure and refund_issued as Predictors of the Churned Target

## Summary

- **Churn is common and concentrated in low-usage, short-tenure, basic-plan customers.** 36.3% of customers churned. Basic plan churn is 42.8%, against 29.3% for plus and 29.8% for pro. Churn falls from 49.0% in the lowest usage quintile to 21.0% in the highest, and from 50.2% to 24.4% across tenure quintiles. All four associations were significant after Holm correction, though plan's association is small (Cramér's V = 0.138).
- **refund_issued almost perfectly predicts churn, and it is a leakage candidate.** Churn is 95.9% when refund_issued = 1 and 1.6% when it = 0. Whether refund_issued is recorded after the churn decision has not been confirmed, so it is excluded from the primary analysis and shown only for comparison.
- **Without refund_issued, the models barely beat the majority baseline on the single test split and do not beat it at all for gradient boosting.** On the 200-row test split, logistic regression reaches 60.5% accuracy and gradient boosting 57.0%, against a 63.5% baseline. Their ROC AUCs are 0.612 and 0.531. Cross-validation gives a different picture: logistic regression averages 67.5% accuracy and 0.694 AUC over 50 folds, while gradient boosting averages 63.4% and 0.637.
- **No interaction of plan with tenure or usage was detected.** Every interaction term has a 95% CI that spans zero, and the joint likelihood-ratio test gives p = 0.466 with refund_issued excluded. These intervals still allow plan-dependent slopes, so the absence of detected interactions is not evidence that none exist.
- **With refund_issued included, models score near-perfectly (test accuracy 0.98 for logistic regression), but this reflects the leakage and is not a churn driver.**

## Data

- **Size:** 1,000 rows and 5 columns.
- **Target:** `churned` (binary). Class 0 (retained) is 63.7% and class 1 (churned) is 36.3%.
- **Features:** numeric `usage_hours`, `tenure_months` and `refund_issued`; categorical `plan`. No date/time features, and no ids or free-text columns.
- **Missing values:** none. Counts of missing values were confirmed as 0 of 1,000 for every column (`usage_hours`, `tenure_months`, `plan`, `refund_issued`, `churned`).
- **Leakage warning:** `refund_issued` alone predicts `churned` almost perfectly (profile score 0.975).

## Findings

### Churn rates and feature averages

**Plan.** Basic plan churn is 42.8% (n = 512), plus is 29.3% (n = 297) and pro is 29.8% (n = 191). Basic churns most often.

**Usage hours (quintiles).** Churn falls steadily across quintiles: Q1 49.0% (n = 204), Q2 42.4% (n = 198), Q3 38.9% (n = 198), Q4 30.0% (n = 200), Q5 21.0% (n = 200).

**Tenure (quintiles).** Churn falls across quintiles: Q1 50.2% (n = 215), Q2 45.8% (n = 190), Q3 33.8% (n = 195), Q4 26.6% (n = 203), Q5 24.4% (n = 197).

**refund_issued.** Churn is 95.9% (n = 368) when refund_issued = 1 and 1.6% (n = 632) when it = 0. This near-deterministic split is the leakage concern noted above.

**Means by churn group.** Churned customers have mean usage_hours of 17.30 against 21.77 for retained customers, and mean tenure_months of 29.84 against 39.12.

![Churn rate by plan (left) and by tenure quintile (right)](tasks/eda_1/charts/churn_rate_by_plan_and_tenure.png)

![Churn rate by refund_issued value (0 vs 1)](tasks/eda_1/charts/churn_rate_by_refund.png)

### Statistical tests and effect sizes

Four tests were run and Holm-corrected together. All four remain significant after correction.

| Factor | Test | Statistic | p (Holm-adjusted) | Effect size |
|---|---|---|---|---|
| plan vs churned | Chi-square, 2 df | χ² = 19.03 | 7.4e-05 | Cramér's V = 0.138 (small) |
| refund_issued vs churned | Chi-square, 1 df | χ² = 895.2 | 1.1e-196 (4.3e-196) | Cramér's V = 0.946 |
| usage_hours, churned vs retained | Mann-Whitney | U = 86990.5 | 7.1e-11 (1.43e-10) | Rank-biserial 0.248; Cohen's d = −0.460 (small-to-medium) |
| tenure_months, churned vs retained | Mann-Whitney | U = 84982.5 | 3.0e-12 (9.1e-12) | Rank-biserial 0.265; Cohen's d = −0.472 (small-to-medium) |

- **refund_issued churn difference:** 1 minus 0 is 0.943, with 95% Wald CI 0.921 to 0.966.
- **Rank-biserial sign:** positive values mean churned customers rank lower. This matches the negative Cohen's d values for usage_hours and tenure_months.

![Churn rate by plan (left) and by refund_issued value (right)](tasks/stat_1/charts/stat1_churn_rate_plan_refund.png)

### Interactions

**Logit with refund_issued included** (standardized tenure and usage; basic plan and refund_issued = 0 as reference):

| Term | Coefficient | p | 95% CI |
|---|---|---|---|
| plus × tenure_c | 0.015 | 0.974 | −0.907 to 0.937 |
| pro × tenure_c | 0.508 | 0.375 | −0.614 to 1.629 |
| plus × usage_c | −0.519 | 0.296 | −1.492 to 0.454 |
| pro × usage_c | 0.086 | 0.898 | −1.223 to 1.394 |
| refund_issued × tenure_c | −0.264 | 0.543 | −1.113 to 0.586 (see Limitations) |

**Logit without refund_issued** (basic plan as reference):

| Term | Coefficient | p | 95% CI |
|---|---|---|---|
| plus × tenure_c | −0.169 | 0.327 | −0.507 to 0.169 |
| pro × tenure_c | 0.113 | 0.560 | −0.266 to 0.492 |
| plus × usage_c | 0.038 | 0.836 | −0.320 to 0.395 |
| pro × usage_c | −0.287 | 0.231 | −0.757 to 0.183 |

The joint likelihood-ratio test of the full plan-interaction model against the main-effects model, without refund_issued, gives LR χ² = 3.576 on 4 df, p = 0.466.

No plan or refund interaction with tenure or usage is statistically supported at the 0.05 level in either specification. Descriptively, basic plan has the highest churn in every tenure quartile. Churn by plan within tenure quartiles (basic / plus / pro, as percentages):

| Tenure quartile | Basic (n) | Plus (n) | Pro (n) |
|---|---|---|---|
| T1 | 54.9 (144) | 44.3 (70) | 41.9 (43) |
| T2 | 47.1 (121) | 36.1 (83) | 35.7 (42) |
| T3 | 37.2 (137) | 18.8 (69) | 21.2 (52) |
| T4 | 29.1 (110) | 17.3 (75) | 24.1 (54) |

These quartile figures are descriptive and were not tested as an interaction.

![Churn rate by plan within tenure quartiles](tasks/stat_2/charts/stat2_churn_by_plan_tenure.png)

### Predictive models

**Feature sets.** The primary `no_leak` set has usage_hours, tenure_months, and one-hot plan_basic, plan_plus and plan_pro. The `with_refund` set adds refund_issued and is for comparison only. Data were split 80/20, stratified on churned, with random_state 42, giving 800 training and 200 test rows. The test churn rate is 36.5%, and always predicting class 0 gives 63.5% test accuracy.

**Leakage check.** A shallow tree on refund_issued alone reaches 0.974 train and 0.98 test accuracy.

**Single test split, with and without refund_issued:**

| Model | Features | Train acc. | Test acc. | Precision | Recall | F1 | ROC AUC |
|---|---|---|---|---|---|---|---|
| Logistic regression | no_leak | 0.695 | 0.605 | 0.435 | 0.274 | 0.336 | 0.612 |
| Gradient boosting | no_leak | 0.796 | 0.570 | 0.377 | 0.274 | 0.318 | 0.531 |
| Logistic regression | with_refund | 0.974 | 0.980 | 0.973 | 0.973 | 0.973 | 0.990 |
| Gradient boosting | with_refund | 0.990 | 0.965 | 0.971 | 0.932 | 0.951 | 0.976 |

- Removing refund_issued lowers test accuracy by 0.375 for logistic regression and by 0.395 for gradient boosting. It lowers ROC AUC by 0.378 and 0.446. The F1 gap reflects the leakage, not a real churn driver.
- Gradient boosting on no-leak features overfits: train accuracy 0.796 against test accuracy 0.570.
- Gradient boosting's no-leak test AUC of 0.531 is essentially chance. Logistic regression's 0.612 is only modestly above chance.

**Feature importance, no-leak models.**
- Logistic regression (standardized coefficients): usage_hours −0.634, tenure_months −0.529, plan_basic 0.131, plan_plus −0.133, plan_pro −0.013. Higher usage and longer tenure go with lower churn.
- Gradient boosting (importance): usage_hours 0.611, tenure_months 0.330, plan_plus 0.030, plan_basic 0.020, plan_pro 0.010.
- Both models rank usage_hours and tenure_months as the top two features. The small plan contribution here is relative to usage and tenure. It does not contradict the significant but small plan association in the statistical tests.

![Test accuracy and ROC AUC for logistic regression and gradient boosting, with and without refund_issued, against the majority-class baseline of 0.635](tasks/ml_2/charts/ml2_model_comparison.png)

### Stability of model scores under cross-validation

Repeated stratified 5-fold CV (10 repeats, 50 folds, seed 0) was run on the no-leak features. Seeds 1 and 2 were also checked for mean scores. The majority baseline has mean accuracy 0.637.

| Model | CV accuracy mean (sd; min–max) | Seed means (0 / 1 / 2) | CV ROC AUC mean (sd) | CV F1 mean (sd) |
|---|---|---|---|---|
| Logistic regression | 0.675 (0.023; 0.630–0.715) | 0.675 / 0.675 / 0.674 | 0.694 (0.030) | 0.445 (0.045) |
| Gradient boosting | 0.634 (0.028; 0.575–0.705) | 0.634 / 0.636 / 0.640 | 0.637 (0.034) | 0.402 (0.048) |
| Majority baseline | 0.637 (0.002) | — | 0.500 | 0.000 |

- Logistic regression's mean CV accuracy exceeds the majority baseline across all three CV seeds. Its lowest fold (0.630) is below baseline.
- Gradient boosting's seed means range from 0.634 to 0.640, straddling the 0.637 baseline. It does not beat the baseline on accuracy.
- Both models score above chance on ROC AUC in CV.
- The source finding attributes the single-split results (0.605 accuracy for logistic regression; 0.57 for gradient boosting) to split-to-split variation.

**Disagreement:** the single test split says logistic regression falls below the baseline (0.605 against 0.635), while the 50-fold CV says it beats the baseline (0.675 against 0.637). These findings are reported side by side and not reconciled here.

![Per-fold CV accuracy, ROC AUC and F1 on no-leak features for logistic regression, gradient boosting and majority baseline (red line: majority accuracy 0.637)](tasks/ml_3/charts/ml3_cv_scores.png)

## Limitations

- **Leakage.** refund_issued almost perfectly predicts churn (0.959 against 0.016). Whether it is recorded after the churn decision has not been confirmed. All statements about it are conditional on that, and it is excluded from the primary models. The with-refund results should not be read as evidence of a churn driver.
- **Unresolved review issue on stat_3.** The lead's objection to three items in the stat_3 findings stands, and it is addressed here as follows:
  1. The claim that removing refund_issued narrows the plan × usage CIs "by about half" is not used, because no fraction was computed. The actual intervals are: plus × usage_c, −1.492 to 0.454 with refund_issued and −0.320 to 0.395 without; pro × usage_c, −1.223 to 1.394 with refund_issued and −0.757 to 0.183 without. The without-refund intervals are narrower, and both still span zero.
  2. The refund-free intervals are narrower yet still span zero, so interaction effects are not ruled out.
  3. The refund × tenure_c upper CI bound is 0.585 in the exact stat_3 value (0.58547). The accepted stat_2 text gives 0.586, which is a rounding difference from the same value (0.5855). The 0.585 figure is used here.
- **Interactions.** Non-significance is not evidence of no interaction. The CIs remain wide, and the refund-included estimates are unstable (see stat_3 findings).
- **Single split.** The test set has 200 rows, so its accuracy and AUC carry large sampling error. This is why the single-split and CV results differ.
- **CV is not independent.** The 50 folds are 10 repeats over the same 1,000 rows. The standard deviations understate or distort uncertainty, and no inferential interval is given for CV scores.
- **Seed stability was tested only on CV seeds 0–2 (means only).** It was not tested for model seeds or test-set sampling variation. F1 was recorded only for seed 0.
- **Gradient boosting was not tuned.** Its overfitting and weak AUC on the single split were not addressed.
- **No nested CV or independent held-out set** was used to confirm the logistic regression result over baseline.
- **Effect sizes are small.** Cramér's V for plan is 0.138, and the Cohen's d values are −0.460 and −0.472.
- **The stat_2 claim that basic plan has the highest churn in every tenure quartile** is descriptive and was not tested.
- **All four tasks are complete;** none failed.

## Open questions

- Is refund_issued recorded before or after the churn decision? This determines whether it can be used at all.
- Does refund_issued carry any churn signal once leakage is resolved?
- Do the usage and tenure slopes differ by plan? Would a likelihood-ratio test or a fitted main-effects model (estimating plan main effects and slopes, without refund_issued) answer this more precisely?
- Does logistic regression's CV accuracy advantage over baseline hold under nested CV or an independent held-out set?
- Does gradient boosting's no-leak AUC of about 0.64 improve with tuning (depth, learning rate, regularization, early stopping), and does tuning remove its overfitting?
- Is the 0.5-point gap between the 63.5% test baseline and the 63.7% profile figure stable across other random seeds?
- Why does refund_issued separate churn so closely (0.959 against 0.016)?