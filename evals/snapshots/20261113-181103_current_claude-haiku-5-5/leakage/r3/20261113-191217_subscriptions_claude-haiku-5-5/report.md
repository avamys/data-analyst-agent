# Churn Analysis of 1,000 Customers: Drivers and Predictability of `churned` (36.3% Positive)

## Summary

- **refund_issued dominates the data.** Customers with refund_issued=1 churned at 95.9% (n=368), versus 1.6% for refund_issued=0 (n=632). Cramér's V is 0.946. The dataset profile flags possible target leakage, and the models show the same dependence (see Findings).
- **Without refund_issued, the signal is weak in the single split and moderate in repeated CV.** The 80/20 split gives logistic regression a test ROC AUC of 0.612, with accuracy 0.605 below the 0.635 majority baseline. Repeated stratified CV gives a mean ROC AUC of 0.694 and accuracy of 0.674. These two estimates disagree, and both are reported.
- **Plan, usage_hours and tenure_months are associated with churn on their own, but the plan effect does not survive adjustment.** Plan is significant (chi-square p = 7.4e-05, Cramér's V = 0.138, a small effect). Churned customers have lower usage_hours and tenure_months, with small-to-medium rank-biserial effects. After adjusting for refund_issued and tenure quartile, the basic-plan odds ratio is 1.485 (95% CI 0.66 to 3.32, p = 0.33).
- **No plan interaction was detected.** Plan does not significantly change how usage_hours or tenure_months relate to churn, with or without refund_issued in the models. Non-significance does not rule out interactions, since power is limited.

## Data

- **Size:** 1,000 rows × 5 columns.
- **Target:** `churned` (binary). Class 0: 63.7%; class 1: 36.3%.
- **Features:** numeric `usage_hours`, `tenure_months`, `refund_issued`; categorical `plan`. No date/time features and no identifier or free-text columns.
- **Missing values:** none. Missing-value counts are 0 for every column (usage_hours, tenure_months, plan, refund_issued, churned), so no rows were dropped or imputed.
- **Leakage warning:** the profile flags refund_issued as a possible leak, since it alone predicts churned at 0.975.

## Findings

### Churn by plan

Churn is highest for basic-plan customers (42.8%, n=512). Plus (29.3%, n=297) and pro (29.8%, n=191) are similar to each other.

The overall plan association is significant: chi-square = 19.03, df = 2, p = 7.4e-05, Cramér's V = 0.138 (bootstrap 95% CI 0.081 to 0.197), a small effect.

![Churn rate by plan level](tasks/eda_1/charts/churn_rate_by_plan.png)

A basic-versus-other comparison gives chi-square = 19.01 (1 df, p = 1.3e-05), with churn of 42.8% for basic and 29.5% for plus and pro combined. This is a different test from the 2-df plan test above.

After adjustment, the basic-plan gap is not detectable (see *Adjusted plan effect* below).

### Churn by refund_issued

- refund_issued=0: 1.6% churn (n=632, 10 churners).
- refund_issued=1: 95.9% churn (n=368).
- Association: chi-square = 895.2, df = 1, p = 1.1e-196, Cramér's V = 0.946 (95% CI 0.925 to 0.966). The stat_1 analysis describes this as very large and consistent with target leakage.

![Churn rate by refund_issued value](tasks/eda_1/charts/churn_rate_by_refund_issued.png)

This is descriptive. Whether refund_issued is leakage or a real driver is not established by these findings.

### Churn by usage_hours and tenure_months

- **usage_hours quartiles:** churn falls steadily from 46.6% in Q1 (n=253) through 41.1% in Q2 (n=248) and 36.1% in Q3 (n=249) to 21.2% in Q4 (n=250).
- **tenure_months quartiles:** churn falls steadily from 49.8% in Q1 (n=257) through 41.5% in Q2 (n=246) and 29.1% in Q3 (n=258) to 24.3% in Q4 (n=239).

Mean and median values:

| Feature | Churned = 0 mean (median) | Churned = 1 mean (median) |
|---|---|---|
| usage_hours | 21.8 (20.5) | 17.3 (16.2) |
| tenure_months | 39.1 (41.0) | 29.8 (26.0) |
| refund_issued | 0.02 (0.0) | 0.97 (1.0) |

Churned customers have lower usage_hours and lower tenure_months. Churned customers have higher refund_issued (mean 0.97 vs 0.02).

### Effect sizes and significance tests

- **usage_hours:** Mann-Whitney U = 86990.5, p = 7.1e-11, rank-biserial r = -0.248 (95% CI -0.320 to -0.178), a small-to-medium effect. Churned customers have lower usage (n = 363 churned, 637 retained).
- **tenure_months:** Mann-Whitney U = 84982.5, p = 3.0e-12, rank-biserial r = -0.265 (95% CI -0.337 to -0.199), a small-to-medium effect. Churned customers have lower tenure.

![Effect sizes with bootstrap 95% CIs for churn: Cramér's V for plan and refund_issued; rank-biserial for usage_hours and tenure_months (negative = churned customers lower)](tasks/stat_1/charts/stat1_effect_sizes.png)

**Leakage check within refund_issued=0** (only 10 churners among 632):

- plan: chi-square p = 0.97, V = 0.010.
- usage_hours: rank-biserial r = -0.094 (95% CI -0.441 to 0.254), p = 0.61.
- tenure_months: rank-biserial r = -0.082 (95% CI -0.446 to 0.274), p = 0.66.

These tests have very low power. They show no detectable association, but they do not prove there is none. The overall associations appear to be carried by refund_issued.

### Plan interactions

No plan × usage_hours or plan × tenure_months interaction was detected in logistic models without refund_issued:

- Joint test: chi-square = 3.58, 4 df, p = 0.47.
- Usage: chi-square = 2.90, 2 df, p = 0.23.
- Tenure: chi-square = 1.40, 2 df, p = 0.50.

Adding refund_issued to both the restricted and full models does not change this:

- Joint: chi-square = 1.84, 4 df, p = 0.77.
- Usage: chi-square = 0.97, 2 df, p = 0.62.
- Tenure: chi-square = 0.43, 2 df, p = 0.81.

In the model with refund_issued, its coefficient is 7.54 (p < 0.001), so it dominates the fit.

Within usage terciles, churn falls with usage for every plan:

| Plan | Low usage | Mid usage | High usage |
|---|---|---|---|
| basic | 51.2% | 45.5% | 31.1% |
| plus | 36.6% | 30.2% | 20.2% |
| pro | 49.1% | 29.0% | 15.9% |

Within tenure terciles, churn falls with tenure for every plan:

| Plan | Short tenure | Medium tenure | Long tenure |
|---|---|---|---|
| basic | 53.2% | 41.2% | 32.1% |
| plus | 44.8% | 26.0% | 15.6% |
| pro | 42.6% | 26.2% | 21.7% |

Basic has the highest churn in all six usage and tenure bins. The formal tests do not show that the slopes differ across plans.

The pro-versus-plus gaps at low and high usage (49.1% vs 36.6%; 15.9% vs 20.2%) rest on 53 to 112 customers per cell (low pro 53, low plus 112, high pro 69, high plus 99). They are not tested separately.

![Churn rate (share churned) by plan within usage_hours and tenure_months terciles](tasks/stat_2/charts/stat2_churn_rates_by_plan.png)

### Adjusted plan effect

After controlling for refund_issued and tenure quartile:

- **Basic vs plus/pro (logistic):** OR = 1.485 (95% CI 0.66 to 3.32), LR p = 0.33. This is compatible with a substantial basic-plan effect as well as none.
- **Cochran-Mantel-Haenszel across 8 refund_issued × tenure-quartile strata:** OR = 1.50 (95% CI 0.66 to 3.37), p = 0.33.
- **Three plan levels (logistic, ref = basic):** LR chi-square = 1.82, df = 2, p = 0.40. OR plus vs basic = 0.86; OR pro vs basic = 0.48. Both have wide uncertainty.

Stratum sizes range from 25 to 103 customers. In refund_issued=0 strata, basic churn ranges from 0.0% to 3.1% and other-plan churn from 0.0% to 2.6%. In refund_issued=1 strata, basic churn ranges from 93.9% to 100% and other-plan churn from 91.5% to 98.0%.

![Churn rate by plan within refund_issued groups (pooled over tenure quartiles)](tasks/stat_3/charts/churn_by_plan_within_refund.png)

### Predictive performance with all features

On the single 200-customer test set:

| Model | Test ROC AUC | Test F1 | Test accuracy |
|---|---|---|---|
| Logistic regression | 0.990 | 0.973 | 0.980 |
| Gradient boosting | 0.976 | 0.951 | 0.965 |
| Majority class | 0.5 | 0.0 | 0.635 |

The report treats differences of a few hundredths as not meaningful, because the test set gives no interval estimates. The logistic regression and gradient boosting ROC AUCs (0.990 and 0.976) are therefore not distinguished here.

![Test F1 and ROC AUC for majority, logistic regression and gradient boosting, with all features and without refund_issued](tasks/ml_1/charts/ml1_model_scores.png)

### Predictive performance without refund_issued

Removing refund_issued lowers performance sharply:

| Model | Test ROC AUC (all → no refund) | Test F1 (all → no refund) |
|---|---|---|
| Logistic regression | 0.990 → 0.612 | 0.973 → 0.336 |
| Gradient boosting | 0.976 → 0.531 | 0.951 → 0.318 |

**Logistic regression without refund_issued** (80/20 stratified split, random_state 42):

- Test ROC AUC 0.612, accuracy 0.605 (below the 0.635 baseline), F1 0.336.
- Top coefficients: usage_hours 0.634, tenure_months 0.529, plan_plus 0.133, plan_basic 0.131, plan_pro 0.013.

**Gradient boosting without refund_issued** overfits: train accuracy 0.796 vs test accuracy 0.570. Its test ROC AUC of 0.531 is close to chance.

**Repeated stratified CV without refund_issued** (5 folds × 10 repeats, random_state 42), logistic regression:

- ROC AUC mean 0.694 (SD 0.033, range 0.596 to 0.751). Every fold is above 0.5.
- Accuracy mean 0.674 (SD 0.027) vs 0.637 (SD 0.002) for the majority baseline.
- F1 mean 0.441 (SD 0.047) vs 0 for the majority baseline.

The single split (ROC AUC 0.612, accuracy below baseline) and the CV (ROC AUC 0.694, accuracy above baseline) disagree. The split is lower than the CV mean, so the report treats the single split as a pessimistic draw. The disagreement is not resolved here.

![Box plot of ROC AUC per fold across 50 repeated stratified CV folds, logistic regression vs majority baseline, without refund_issued](tasks/ml_3/charts/ml3_cv_roc_auc.png)

### Feature importance without refund_issued

The no-refund model does not beat the majority baseline on the single split, so these importances describe a weak model.

The two methods rank features differently:

- **Logistic coefficients:** usage_hours first, then tenure_months, plan_plus, plan_basic, plan_pro.
- **Permutation importance (drop in test ROC AUC, 50 repeats):** tenure_months first (mean 0.066, SD 0.022), usage_hours second (mean 0.026, SD 0.032). Shuffling usage_hours alone lowers AUC by 0.024 (SD 0.027), with an SD larger than the mean.
- **Plan dummies:** individual permutation drops are small (plan_basic 0.019, plan_plus 0.005, plan_pro 0.002). Shuffled jointly, they lower AUC by 0.024 (SD 0.011), similar to usage_hours alone.

The ranking depends on the method, so neither ordering is treated as settled.

## Limitations

- **Leakage.** refund_issued alone predicts churned at 0.975, and the profile flags it as a possible leak. No timing or documentation establishes whether the refund precedes or follows churn. Every model comparison with and without refund_issued depends on this. The model results cannot show whether refund_issued is leakage or a legitimate driver.
- **Low churn among refund_issued=0 customers.** Only 10 of 632 churned. Tests within this group (plan, usage_hours, tenure_months, and the stratified and adjusted estimates) have very low power, so absence of effect is not proof of absence.
- **Single test set.** The all-feature and no-refund model scores come from a single 200-customer test set with no interval estimates. Differences of a few hundredths are not meaningful.
- **Disagreement on the no-refund signal.** The single split and repeated CV give different estimates (ROC AUC 0.612 vs 0.694; accuracy below vs above baseline). The 50 CV folds reuse the same 1,000 rows, so they are not independent. The fold SD is not a confidence interval, and "consistently above chance" holds only across resamples of this dataset.
- **Adjusted estimates are imprecise.** The refund_issued=1 strata are near 100% churn and give almost no basic-vs-other contrast. The adjusted and stratified odds ratios have wide intervals.
- **Plan-level subgroup comparisons are untested.** The pro-vs-plus gaps within usage terciles rest on 53 to 112 customers per cell and were not tested separately.
- **Linearity not checked.** The usage and tenure effects were modelled without checking linearity on the logit scale.
- **Unresolved review issues (the lead's objections still stand):**
  1. *eda_1 missing-value counts.* The per-column counts were required but not recorded as a fact in eda_1. They are recorded in stat_1 (usage_hours 0, tenure_months 0, plan 0, refund_issued 0, churned 0) and cited in the Data section above. The objection affects the Data section.
  2. *eda_1 averages sentence.* "Churned customers have lower feature averages" was incorrect for refund_issued. It is reworded in the Findings section: usage_hours and tenure_months are lower for churned customers, and refund_issued is higher (0.97 vs 0.02). The objection affects the feature-average finding.
  3. *stat_2 cell-size range.* The pro-vs-plus cell sizes were stated as 53 to 99. The correct range is 53 to 112 (low pro 53, low plus 112, high pro 69, high plus 99), as given in the counts. The corrected range is used in the Findings section.
- **Failed tasks.** None reported.

## Open questions

- Is refund_issued a leak, meaning it is recorded after churn occurs, or a causal driver? Answering this needs the data-generating process and documentation, and a timing check on when refunds were issued.
- Is the basic-plan churn gap still present after controlling for refund_issued and tenure? The adjusted analysis is imprecise and does not settle it.
- Is the crude basic-plan gap explained by plan differences in refund_issued rates or tenure distribution? A composition or mediation check would show the mechanism.
- Do the usage_hours and tenure_months signals without refund_issued hold under repeated or stratified CV, given that the single split and CV disagree?
- Do a spline on usage_hours and tenure_months, or a regularized gradient boosting model, raise the no-refund ROC AUC above 0.612 on the split, or above 0.694 under repeated CV? Do they change the feature ranking?
- Are the pro-versus-plus differences at low and high usage real? A formal pairwise plan contrast within usage terciles, adjusted for refund_issued, would answer this.
- Does the plan effect differ by refund_issued or tenure, given the sparse strata with near-100% churn? Is there enough churn among refund_issued=0 customers (10 churners) to test plan × usage and plan × tenure interactions? If not, a power analysis or a different design is needed.
- Are the usage and tenure effects linear on the logit scale? A spline or binned-logit check would test this.