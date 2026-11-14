# Churn Analysis of churned_flag in an 800-Customer Dataset

## Summary

- **Contract is the clearest categorical association with churn.** Monthly contracts churn at 37.3% versus 21.2% for annual contracts (chi-square 22.84, df 1, p = 1.8e-6, Cramér's V = 0.169). The association survives Holm correction and remains after adjustment for monthly_fee, support_calls and region (adjusted OR 2.39, 95% CI 1.68 to 3.38).
- **Higher monthly_fee and more support_calls are both significantly associated with churn**, and both survive Holm correction. Churn rises from 17.5% in the lowest fee quartile to 44.5% in the highest, and from 22.6% at 0 support calls to 39.2% at 3. Adjusted, each unit of fee has OR 1.018 and each additional call has OR 1.46.
- **Region shows no detectable association** with churn (chi-square 2.66, df 3, p = 0.448, Cramér's V = 0.058). It adds no signal in the adjusted model or in either predictive model.
- **Logistic regression beats both the majority-class baseline and random forest on ROC AUC** in repeated 5×5 stratified CV on all 800 rows (mean 0.698 vs 0.607 for random forest; baseline 0.5). Its accuracy gain over the baseline is small (0.719 vs 0.6875), and churn-class F1 is low (0.382).
- **No interaction is established.** The contract × monthly_fee interaction is inconclusive, the contract × support_calls and contract × region interactions are null, and the feature order among the top predictors is not stable across models and folds.

## Data

- 800 rows, 5 columns: target `churned_flag` (binary); numeric features `monthly_fee` and `support_calls`; categorical features `contract` and `region`. There are no date/time features and no id or free-text fields.
- Target classes: no 68.8%, yes 31.2%. The imbalance matters for the accuracy comparisons below. The exact overall churn rate is 31.25% (250 of 800), which rounds to 31.3%; the dataset profile reports 31.2%.
- Missing values: none. The missingness check found zero missing values in all columns.

## Findings

### Churn distribution and descriptive rates

Overall churn is 31.25% (250 of 800). Churn rates by group:

- **Contract:** monthly 37.3% (n=498); annual 21.2% (n=302).
- **Region:** east 30.2% (n=215), north 33.0% (n=191), south 27.5% (n=200), west 34.5% (n=194).
- **Monthly_fee quartile:** Q1 17.5%, Q2 28.5%, Q3 34.5%, Q4 44.5% (n=200 each).
- **Support_calls:** 0 calls 22.6% (n=164); 1 call 26.4% (n=284); 2 calls 34.5% (n=206); 3 calls 39.2% (n=97); 4 calls 50.0% (n=36). Counts above 4 are very small: 5 calls 90.9% (n=11), 6 calls 0% (n=1), 7 calls 100% (n=1).

Churned customers have higher monthly_fee (mean 79.9, median 82.9) than retained customers (mean 66.1, median 63.3), and more support_calls (mean 1.84, median 2) than retained customers (mean 1.34, median 1).

![Churn rate by contract type (left) and by support_calls value (right)](tasks/eda_1/charts/churn_by_contract_support_calls.png)

### Significance tests and effect sizes

**Contract.** Chi-square 22.84 (df 1), p = 1.8e-6, Cramér's V = 0.169. Monthly churn is 37.3% (95% Wilson CI 33.2% to 41.7%) and annual churn is 21.2% (95% CI 17.0% to 26.1%). Holm-adjusted p = 3.5e-6.

**Region.** Chi-square 2.66 (df 3), p = 0.448, Cramér's V = 0.058. Per-group rates with 95% Wilson CIs:

- east 30.2% (24.5% to 36.7%)
- north 33.0% (26.7% to 39.9%)
- south 27.5% (21.8% to 34.1%)
- west 34.5% (28.2% to 41.5%)

The intervals overlap widely. Region does not survive Holm correction (adjusted p = 0.448).

**Monthly_fee.** Mann-Whitney p = 4.4e-10, rank-biserial 0.275. The mean difference (churned minus retained) is 13.8, with a bootstrap 95% CI of 9.8 to 18.0. Holm-adjusted p = 1.8e-9. Among the two numeric features, monthly_fee has the larger rank-biserial effect.

**Support_calls.** Mann-Whitney p = 8.5e-7, rank-biserial 0.209. The mean difference is 0.50 calls, with a bootstrap 95% CI of 0.32 to 0.69. Holm-adjusted p = 2.6e-6.

Across the four tests, contract, monthly_fee and support_calls remain significant after Holm correction; region does not. These are unadjusted tests of one feature at a time. The rank-biserial and Cramér's V values are different effect-size measures and are not directly comparable.

![Churn rate with 95% Wilson CI by contract and by region](tasks/stat_1/charts/stat1_churn_rates_by_contract_region.png)

### Interactions

**Contract × high monthly_fee: inconclusive.** Using a single median split on fee, churn is 48.2% for monthly contracts with high fee (n=251) versus 26.3% with low fee (n=247). For annual contracts it is 24.8% with high fee (n=149) versus 17.6% with low fee (n=153). The interaction test gives LR 2.46 (df 1), p = 0.117. The interaction coefficient is 0.55 on the logit scale, 95% CI −0.14 to 1.23 (odds ratio 0.87 to 3.43). The data cannot rule out a slight negative or a large positive interaction, so this is inconclusive, not absent.

**Contract × support_calls (2+ vs 0–1): null.** LR 0.03 (df 1), p = 0.863; coefficient −0.05, p = 0.881. Monthly churn is 30.6% at 0–1 calls (n=284) and 46.3% at 2+ calls (n=214). Annual churn is 15.2% at 0–1 calls (n=164) and 28.3% at 2+ calls (n=138).

**Contract × region: null.** LR 0.68 (df 3), p = 0.877. The joint test of all contract interaction terms (fee, calls and region) gives LR 3.16 (df 5), p = 0.675.

![Churn rate by contract and monthly fee (low/high split at median)](tasks/stat_2/charts/churn_by_contract_fee.png)

### Adjusted association (all four features together)

A logistic regression of churned_flag on contract, monthly_fee, support_calls and region (n = 800, pseudo R² = 0.099, LLR p = 6.2e-19) gives these adjusted odds ratios:

- **Monthly vs annual contract:** OR 2.39 (95% CI 1.68 to 3.38), Wald p = 1.0e-6.
- **Monthly_fee, per unit:** OR 1.018 (95% CI 1.012 to 1.024), p = 1.1e-9.
- **Support_calls, per additional call:** OR 1.46 (95% CI 1.28 to 1.67), p = 2.9e-8.
- **Region, vs east:** north OR 1.12 (95% CI 0.72 to 1.75, p = 0.61); south OR 0.77 (95% CI 0.49 to 1.21, p = 0.25); west OR 1.08 (95% CI 0.69 to 1.68, p = 0.73).

The contract association persists after adjustment. Region shows no adjusted effect, consistent with the unadjusted test.

### Predictive models versus the majority-class baseline

**Single 160-row stratified test split** (50 churners, 110 non-churners):

- Majority-class baseline: accuracy 0.6875, ROC AUC 0.5.
- Logistic regression: train accuracy 0.7281, test accuracy 0.7188, ROC AUC 0.7122, churn-class precision 0.5926, recall 0.32, F1 0.4156.
- Random forest: train accuracy 1.0, test accuracy 0.6312 (below baseline), ROC AUC 0.6259, F1 0.404. It fits the training set perfectly and overfits.

![Permutation importance of the four features on the 160-row test set, by model](tasks/ml_1/charts/ml1_permutation_importance.png)

**Repeated stratified 5×5 CV on all 800 rows** (25 folds):

| Model | ROC AUC mean (sd) | Accuracy mean (sd) | Churn F1 mean (sd) |
|---|---|---|---|
| Logistic regression (scaled features) | 0.698 (0.036) | 0.719 (0.020) | 0.382 (0.059) |
| Random forest | 0.607 (0.029) | 0.644 (0.027) | 0.397 (0.047) |
| Majority class | 0.5 (0.0) | 0.6875 (0.0) | 0.0 |

Both models exceed the baseline ROC AUC of 0.5. Logistic regression's accuracy gain over the baseline is small. Random forest's mean train ROC AUC is 1.0 against a mean test ROC AUC of 0.607, a gap of 0.393, so it overfits strongly. Churn-class F1 is low for both models.

![Mean test ROC AUC of logistic regression and random forest vs majority baseline (0.5), 5x5 stratified CV on 800 rows](tasks/ml_2/charts/ml2_model_roc_auc.png)

### Feature importance

Two importance analyses disagree on contract, and both are reported.

**Single test split (ml_1).**
- Logistic regression, permutation importance (mean drop in test ROC AUC): monthly_fee 0.091 (sd 0.026), support_calls 0.070 (sd 0.028), contract 0.026 (sd 0.028), region 0.006 (sd 0.005). Contract is within one sd of zero.
- Random forest: support_calls 0.072 (sd 0.036), monthly_fee 0.055 (sd 0.037), contract 0.044 (sd 0.028), region −0.015 (sd 0.035).
- Logistic regression coefficients rank contract (magnitude about 0.477) as largest. This conflicts with the permutation ranking. The numeric features were unscaled in this model, so coefficient magnitudes are not comparable across features.

**Repeated CV on 800 rows, scaled features (ml_2).**
- Logistic regression mean permutation importance: monthly_fee 0.084 (sd 0.022), support_calls 0.062 (sd 0.024), contract 0.054 (sd 0.015), region 0.000 (sd 0.007). The ranking is monthly_fee > support_calls > contract > region.
- Monthly_fee exceeds support_calls in 72% of folds and exceeds contract in 92%. Support_calls exceeds contract in only 56%, so the middle pair is not reliably ordered. Contract exceeds region in 100% of folds.
- Random forest ranking is support_calls > monthly_fee > contract > region, but it is unstable. Support_calls exceeds monthly_fee in 60% of folds, and monthly_fee exceeds contract in 44%. Contract exceeds region in 100% of folds. Region's mean importance is −0.007 (sd 0.026) and is positive in 44% of folds.

**Reconciling the two.** The single-split analysis (ml_1) finds contract's importance indistinguishable from noise, while the CV analysis (ml_2) finds contract above region in every fold. Both agree that region carries no reliable signal and that monthly_fee and support_calls are useful. Neither establishes the order of monthly_fee and support_calls, and contract's position relative to the top two features is not stable.

## Limitations

- **Small sample and small test set.** The dataset has 800 rows. The single test split used for ml_1 has 160 rows with 50 churners, so its performance and importance figures are noisy and provisional. The CV results in ml_2 are more stable but still show wide spread (sd values above).
- **Region groups are small.** Each region has about 200 customers, so the per-region CIs are wide (for example, west spans 28.2% to 41.5%).
- **Fee interaction is underpowered.** The contract × fee interaction is inconclusive. The interval for its coefficient spans a slight negative to a large positive interaction. The fee split is a single median split, not a continuous term.
- **Support_calls above 4 is sparse.** Rates at 5 calls (n=11), 6 calls (n=1) and 7 calls (n=1) rest on very small counts and should not be read as patterns.
- **Associations, not causes.** All findings are associations in a single observational dataset. The unadjusted tests examine one feature at a time. Only the adjusted logistic model in stat_3 controls for the other features, and it does not test interactions.
- **Model comparisons are limited.** The logistic regression and random forest were not tuned. The random forest was not regularised. Churn-class F1 is low for both models, and the accuracy gain over the majority baseline is small given the 31/69 class split.
- **Coefficient ranking not comparable.** The ml_1 logistic regression used unscaled numeric features, so its coefficient ranking is not comparable across features.
- **Overall churn rate rounding.** The exact rate is 31.25%. The dataset profile reports 31.2%, and this report gives 31.3% as the rounded value of the exact rate.
- **No failed tasks.** All analysis tasks (eda_1, stat_1, stat_2, stat_3, ml_1, ml_2) completed.

## Open questions

- Is the monthly-fee association stronger within monthly contracts with a larger sample or a continuous fee term? The current interaction test is inconclusive.
- Do support_calls thresholds other than 2+ show different effects by contract? Only the 2+ threshold was tested.
- Do the monthly-contract and support_calls effects hold within contract type, given that monthly contracts may carry higher fees? The interaction tests do not fully answer this.
- Does a non-linear term or interaction for monthly_fee and support_calls change the logistic regression ranking? The order of monthly_fee and support_calls remains unresolved.
- Would a tuned, more regularised random forest close the train/test gap and beat logistic regression?
- Is region's lack of signal real, or an artefact of one-hot encoding with few levels?
- Does a nonlinear model (beyond the tested logistic and random forest) change the feature ordering?