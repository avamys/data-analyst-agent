# Churn Analysis of 800 Customers: Predicting the churned_flag Target

## Summary

- **Contract, monthly fee and support calls are associated with churn; region is not.** Monthly contracts churned at 37.3% versus 21.2% for annual (chi-square p = 1.8e-6, Holm-adjusted p = 3.5e-6). Monthly fee and support calls also differ significantly between churned and retained customers after Holm adjustment. Region is not significant (Holm-adjusted p = 0.448).
- **The effects are modest.** Cramér's V for contract is 0.17, the rank-biserial for monthly fee is 0.27 and for support calls is 0.21.
- **No feature significantly changes the effect of another.** The joint test of all three interaction blocks gives p = 0.93.
- **The monthly fee association persists within each contract type.** Churn rises with fee quartile within both monthly and annual contracts.
- **Logistic regression beats a majority-class baseline, but predictive power is modest.** Test-set ROC AUC is 0.712 against 0.500, and repeated cross-validation gives a mean AUC of 0.699. Logistic regression catches about a third of churners at its default threshold (recall 0.32 on the test split, 0.285 under cross-validation). Gradient boosting has lower AUC under cross-validation.

## Data

- **Size:** 800 rows, 5 columns.
- **Target:** `churned_flag`, binary. 31.2% yes (250 customers) and 68.8% no (550). The target is imbalanced.
- **Features:** numeric `monthly_fee` and `support_calls`; categorical `contract` and `region`. There are no date/time features and no identifiers or free-text fields.
- **Missing values:** none in any column, and no rows with missing values in either the churned or retained group.

## Findings

### Churn rates by group

Overall churn is 31.25% (250 of 800).

- **Contract:** monthly contracts churned at 37.3% (n = 498). Annual contracts churned at 21.2% (n = 302).

  ![Churn rate by contract level (left) and by number of support calls (right); each bar is the share of customers in that group who churned.](tasks/eda_1/charts/churn_rate_contract_support_calls.png)

- **Region:** churn ranged from 27.5% in south (n = 200) to 34.5% in west (n = 194). East was 30.2% (n = 215) and north 33.0% (n = 191).

- **monthly_fee quartiles** (200 customers each): Q1 17.5%, Q2 28.5%, Q3 34.5%, Q4 44.5%.

- **support_calls:** churn rose with the number of calls. It was 22.6% at 0 calls (n = 164), 26.4% at 1 (n = 284), 34.5% at 2 (n = 206), 39.2% at 3 (n = 97) and 50% at 4 (n = 36). Calls of 5, 6 and 7 have 11, 1 and 1 customers, with churn of 90.9%, 0% and 100%. Quartile bins collapse to three groups because of tied values: 25.0% for 0–1 calls (n = 448), 34.5% for 2 (n = 206) and 45.9% for 3–7 (n = 146).

### Statistical tests and effect sizes

Holm adjustment applies across the four tests.

- **Contract:** chi-square = 22.84, df = 1, p = 1.8e-6 (Holm-adjusted p = 3.5e-6), Cramér's V = 0.17 (small to moderate). The difference in churn, monthly minus annual, is 16.2 percentage points (Wald 95% CI 9.9 to 22.4 pp).

  ![Churn rate (%) by contract (left) and region (right); each bar is the share of customers in that group who churned.](tasks/stat_1/charts/stat1_churn_rate_contract_region.png)

- **Region:** chi-square = 2.66, df = 3, p = 0.448 (Holm-adjusted p = 0.448), Cramér's V = 0.058 (negligible). The findings read the 27.5% to 34.5% spread as consistent with sampling noise. No power analysis was run.

- **monthly_fee:** Mann-Whitney p = 4.4e-10 (Holm-adjusted p = 1.8e-9), rank-biserial = 0.27 (small to moderate). Mean fee is 79.9 for churned and 66.1 for retained customers.

- **support_calls:** Mann-Whitney p = 8.5e-7 (Holm-adjusted p = 2.6e-6), rank-biserial = 0.21 (small). Mean calls are 1.84 for churned and 1.34 for retained customers.

Holm adjustment leaves contract, monthly_fee and support_calls significant and region non-significant. Among the numeric features, monthly_fee has the larger rank-biserial.

### Interactions

Each test compares a model with the interaction term to the main-effects logistic model.

- **Contract × support_calls:** LR chi2 = 0.245, df = 1, p = 0.62. The monthly-vs-annual slope coefficient is 0.073 log-odds (95% CI −0.215 to 0.360). The data are consistent with no detectable difference in slope. This does not show identical slopes.

  Churn by support_calls within contract:

  | Calls | Monthly | Annual |
  |---|---|---|
  | 0 | 25.5% (n = 106) | 17.2% (n = 58) |
  | 1 | 33.7% (n = 178) | 14.2% (n = 106) |
  | 2 | 40.5% (n = 126) | 25.0% (n = 80) |
  | 3+ | 54.5% (n = 88) | 32.8% (n = 58) |

  The annual dip at 1 call rests on a group of 106.

  ![Churn rate by support_calls level, separately for annual and monthly contracts](tasks/stat_2/charts/stat2_churn_support_by_contract.png)

- **Contract × monthly_fee:** LR chi2 = 0.108, df = 1, p = 0.74. The coefficient is 0.0021 log-odds per fee unit (95% CI −0.0103 to 0.0145).

- **Contract × region:** LR chi2 = 0.983, df = 3, p = 0.81. All three region interaction coefficients (each relative to east) have intervals that include zero. Churn by contract and region:

  | Region | Annual | Monthly |
  |---|---|---|
  | East | 18.8% | 37.7% |
  | North | 24.1% | 39.8% |
  | South | 16.9% | 33.3% |
  | West | 25.4% | 38.9% |

- **All interactions jointly:** LR chi2 = 1.34, df = 5, p = 0.93. The interaction terms add nothing to the main-effects model.

### The monthly_fee association within contract types

- **Monthly contracts (n = 498):** churn rises across fee quartiles: 23.7% (28/118) in Q1, 28.7% (37/129) in Q2, 43.5% (54/124) in Q3, 52.8% (67/127) in Q4. The logistic slope is 0.0179 per fee unit (p about 1e-7).
- **Annual contracts (n = 302):** churn also rises overall: 8.5% (7/82) in Q1, 28.2% (20/71) in Q2, 19.7% (15/76) in Q3, 30.1% (22/73) in Q4. The slope is 0.0157 per fee unit (p about 0.0025). The increase is less steady, with Q3 below Q2.
- **Reading:** the findings state that the fee effect remains within both contract types and is not explained by the higher share of monthly contracts. The slopes are similar (0.0179 and 0.0157), and both are significant within their own group. Quartiles use full-sample cut-offs.

  ![Share churned by monthly_fee quartile, separately for monthly and annual contracts](tasks/ml_2/charts/ml2_churn_by_fee_quartile_within_contract.png)

### Predictive performance on a single 160-row test split

Training used 640 rows and testing used 160 rows, about 50 of them yes.

| Model | Accuracy | Yes-class recall | Yes-class precision | ROC AUC |
|---|---|---|---|---|
| Majority-class baseline | 0.6875 | 0 | 0 (undefined, set to 0) | 0.500 |
| Logistic regression | 0.725 | 0.32 | 0.615 | 0.712 |
| Gradient boosting | 0.694 | 0.34 | 0.515 | 0.660 |

- Logistic regression beats the baseline on accuracy and AUC. The baseline never predicts yes.
- Gradient boosting's accuracy (0.694) is no better than the baseline's (0.6875). Its AUC is above chance. Its training accuracy is 0.819, against 0.694 on test. The findings read this gap as possible overfitting on 640 rows.
- The findings conclude that predictive power is modest and that the test estimates are imprecise.

![Test-set ROC AUC and recall of the churn (yes) class for the majority baseline, logistic regression and gradient boosting (160 test rows).](tasks/ml_1/charts/ml1_model_comparison.png)

**Feature ranking (single split).** The findings rank the features as follows:

- *Logistic regression* (absolute coefficients, on scaled one-hot features): monthly_fee 0.497, contract annual 0.477, contract monthly 0.476, support_calls 0.452. Region is at most 0.187 (south).
- *Gradient boosting* (importance): monthly_fee 0.708, support_calls 0.153, contract monthly 0.064, contract annual 0.040. Region is at most 0.016.

The findings conclude that monthly_fee, contract and support_calls carry most of the signal. The three contract and fee terms are nearly tied in logistic regression.

### Predictive performance under cross-validation

Repeated stratified 5-fold CV on all 800 rows (3 repeats, 15 folds):

| Model | ROC AUC mean (sd) | Yes-class recall mean (sd) | Yes-class precision mean (sd) |
|---|---|---|---|
| Majority-class baseline | 0.500 (0.0) | 0 (0.0) | 0 (0.0) |
| Logistic regression | 0.699 (0.042) | 0.285 (0.064) | 0.613 (0.068) |
| Gradient boosting | 0.634 (0.047) | 0.244 (0.061) | 0.482 (0.094) |

- **AUC:** logistic regression keeps a mean AUC of about 0.70, consistent with the single-split value of 0.712. Gradient boosting's CV AUC is 0.634, above the baseline but below logistic regression. The mean per-fold difference (logistic minus GBM) is 0.065 (sd 0.042). Logistic regression is higher in 13 of 15 folds. The paired t-test gives p about 3e-5. The findings call this p-value optimistic, because folds from repeats are not independent.
- **Precision:** logistic regression precision under CV is 0.613 (sd 0.068). GBM precision is 0.482 (sd 0.094), lower and more variable.
- **Recall, logistic regression only:** CV recall is 0.285 (sd 0.064), against 0.32 on the single split. This is within one fold-level sd of the single-split value. The findings do not show that the single split is optimistic for logistic regression. The recall estimate is imprecise either way.

![Repeated 5-fold stratified CV (3 repeats, 15 folds): mean and SD of ROC AUC and yes-class recall for the majority baseline, logistic regression and gradient boosting](tasks/ml_3/charts/ml3_cv_model_comparison.png)

## Limitations

- **Unresolved review issue on gradient boosting recall.** The lead's objection stands. GBM's CV recall is 0.244 (sd 0.061), against 0.34 on the single split. That drop is larger than one fold sd, so the single-split GBM recall is judged optimistic. The single-split ordering, with GBM recall (0.34) above logistic regression (0.32), does not hold under CV, where logistic regression (0.285) is above GBM (0.244). Treat the single-split recall comparison in the modelling findings as unreliable.
- **Test-set size.** The single split has 160 rows, about 50 of them yes. Its estimates are imprecise, as the findings state.
- **CV p-values.** Folds from repeats are not independent, so the paired-test p-value for the AUC difference is optimistic.
- **Sparse tails.** Support_calls values of 5, 6 and 7 have 11, 1 and 1 customers. The 3+ and 4+ groups are small, and the annual dip at 1 call rests on 106 customers. The annual fee quartiles have about 70 to 80 customers each.
- **Power.** The region test and the interaction tests were not assessed for power. The findings say non-significance is consistent with noise, not that no difference exists. Moderate interactions could be missed.
- **Non-linearity and adjustment.** The findings did not test whether the support_calls gradient holds after adjusting for monthly_fee, or whether it is non-linear in the 3+ tail.
- **Scope of claims.** The analysis is associational. The findings do not establish causes or mechanisms.
- **Failed tasks.** None. All tasks reported complete.

## Open questions

- Does the contract effect hold within each monthly_fee quartile? The fee-quartile breakdown by contract (ml_2) addresses fee within contract, but not contract within fee quartiles.
- Is the support_calls effect stronger for monthly contracts than for annual ones? The interaction test was non-significant, so the question is not settled.
- What is the statistical power of the region test, and how large a region difference could it detect?
- Would rank-based binning of support_calls give a finer picture of the high-count tail?
- Does support_calls or region confound the fee-churn association within each contract type?
- Is the fee effect in annual contracts driven by a few high-fee customers, given the non-monotone Q2 to Q3 step?
- Would cross-validation give more stable estimates for other threshold or model settings?
- Would tuning the yes-class decision threshold raise recall without losing too much precision?
- Does gradient boosting improve with regularisation or fewer trees, given its train/test gap and its lower CV AUC?
- Does the support_calls gradient hold after adjusting for monthly_fee, and is it non-linear at the 3+ tail?