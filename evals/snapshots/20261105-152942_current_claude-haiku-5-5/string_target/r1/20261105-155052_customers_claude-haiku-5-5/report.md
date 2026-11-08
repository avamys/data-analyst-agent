# Churn Analysis of 800 Customers: Drivers of the Binary churned_flag Target

## Summary

- **Contract type is strongly associated with churn, and the association holds after adjustment.** Monthly contracts churn at 37.3% (186 of 498) versus 21.2% for annual (64 of 302), a significant difference (chi-square(1) = 22.84, p = 1.76e-06, Cramér's V = 0.169). In a multivariable logistic regression that also includes monthly_fee and support_calls, the adjusted odds ratio for monthly contract is 2.36 (95% CI 1.67 to 3.34).
- **monthly_fee and support_calls are significantly associated with churn, and both gradients rise steadily.** Churn rises from 17.5% in the lowest monthly_fee quartile to 44.5% in the highest, and from 22.6% at 0 support calls to 45.9% at 3 or more. Region is not significant (chi-square(3) = 2.66, p = 0.448, Cramér's V = 0.058).
- **No significant contract interaction was detected, but the test has limited power.** The likelihood-ratio test of contract × support_calls and contract × monthly_fee gives p = 0.871. The descriptive gap between contract levels widens with support calls, but this is not a reliable interaction.
- **Predictive gain over the majority baseline (68.8% accuracy) is modest.** On the 160-row test split, logistic regression reaches 0.725 accuracy and 0.712 ROC AUC, and the random forest falls below baseline (0.631). Under 5-fold CV on all 800 rows, logistic regression reaches 0.721 accuracy and 0.695 ROC AUC, and the regularized forest reaches 0.698 accuracy, within fold noise of the baseline.
- **Feature importance is consistent on monthly_fee and region, but not on contract versus support_calls.** monthly_fee ranks first in every importance measure reported. Region ranks last in permutation importance. Whether impurity under-credits contract relative to permutation remains untested, and the two analysis runs that address it (ml_4 and ml_5) do not reproduce each other.

## Data

- **Size:** 800 rows × 5 columns.
- **Target:** churned_flag (binary). 550 "no" (68.75%) and 250 "yes" (31.25%). The classes are imbalanced, so the majority-class baseline of 68.8% accuracy is the reference for model results.
- **Features:** monthly_fee and support_calls (numeric); contract and region (categorical). There are no date/time features, and no ids or free-text columns.
- **Missing values:** none in any column (total = 0).

## Findings

### Churn rates by feature (eda_1)

- **Contract:** Monthly contracts churn at 37.3% (186 of 498) and annual contracts at 21.2% (64 of 302).

  ![Churn rate by contract type](tasks/eda_1/charts/churn_rate_by_contract.png)

- **Region:** Churn varies only modestly: west 34.5% (67 of 194), north 33.0% (63 of 191), east 30.2% (65 of 215), south 27.5% (55 of 200).

  ![Churn rate by region](tasks/eda_1/charts/churn_rate_by_region.png)

- **monthly_fee quartile:** Q1 17.5% (35 of 200), Q2 28.5% (57 of 200), Q3 34.5% (69 of 200), Q4 44.5% (89 of 200). Churn rises steadily across quartiles.
- **support_calls:** 22.6% at 0 calls (164 customers), 26.4% at 1 (284), 34.5% at 2 (206), and 45.9% at 3 or more (67 of 146). Counts above 4 calls are very small (11 at 5, 1 at 6, 1 at 7), so the individual rates at those levels are unstable.

### Significance tests and effect sizes (stat_1)

- **Contract:** Significant. chi-square(1) = 22.84, p = 1.76e-06, Cramér's V = 0.169 (small to moderate).
- **Region:** Not significant. chi-square(3) = 2.66, p = 0.448, Cramér's V = 0.058 (negligible).
- **monthly_fee (churners vs non-churners):** Significant. Means 79.94 vs 66.12; medians 82.92 vs 63.35; Mann-Whitney U = 87649.5, p = 4.4e-10, rank-biserial r = 0.275 (small to moderate).
- **support_calls (churners vs non-churners):** Significant. Means 1.84 vs 1.34; medians 2 vs 1; Mann-Whitney U = 83116.5, p = 8.5e-07, rank-biserial r = 0.209 (small).
- **Contract churn difference:** Monthly minus annual is 16.2 percentage points, Wald 95% CI 9.9 to 22.4 points.
- **Wilson 95% CIs by contract:** monthly 33.2% to 41.7%; annual 17.0% to 26.1%. The intervals do not overlap.
- **Multiple-comparison correction:** Across the four tests, Holm-Bonferroni adjusted p-values are 1.8e-09 for monthly_fee, 2.6e-06 for support_calls, and 3.5e-06 for contract. All three remain significant at 0.05. Region does not (adjusted p = 0.448).
- **Contract chi-square, two computations:** The Yates-corrected chi-square on all 800 rows is 22.10 (p = 2.6e-06), and the uncorrected Pearson chi-square is 22.84 (p = 1.76e-06). Both have 1 df. The two values come from different computations and are not one result. The uncorrected value is the one used in the test above.
- **Region chi-square:** Uncorrected, 3 df, chi-square = 2.66, p = 0.448, Cramér's V = 0.058.

### Contract × support_calls and contract × monthly_fee interactions (stat_2)

- **Interaction test:** The likelihood-ratio test of both interaction terms gives chi-square(2) = 0.277, p = 0.871. No significant interaction was detected. The test has limited power for these terms, so this does not show that the effects are equal across contracts.
- **Main-effects logit (no interactions):** Annual contract coefficient −0.858 (p = 1.2e-06, lower churn odds than monthly). support_calls +0.377 per call, centered (p = 0.0176 as reported in the findings; the coefficient CI is 0.243 to 0.511). monthly_fee +0.018 per unit, centered. The interaction model gives nearly the same values (annual −0.834, support_calls 0.395, monthly_fee 0.018).
- **Individual interaction terms:** contract × support_calls = −0.054 (p = 0.713); contract × monthly_fee = −0.0025 (p = 0.694). Their direction is not reliably established.
- **Churn by support_calls within each contract (n in brackets):**
  - 0 calls: annual 17.2% (58), monthly 25.5% (106)
  - 1 call: annual 14.2% (106), monthly 33.7% (178)
  - 2 calls: annual 25.0% (80), monthly 40.5% (126)
  - 3 or more calls: annual 32.8% (58), monthly 54.5% (88)

  Monthly churn is higher than annual at every call count. The findings describe the monthly-minus-annual gap as about 8 points at 0 calls, 20 at 1, 16 at 2, and 22 at 3 or more. This widening is descriptive only, because the interaction test is non-significant and the cells are modest in size.

  ![Churn rate by support_calls within monthly and annual contracts](tasks/stat_2/charts/stat2_churn_by_calls_contract.png)

- **Sparse high-call counts:** Customers with 5 or more calls (11 at 5, 1 at 6, 1 at 7) are pooled into the 3-or-more group, which holds 146 customers.

### Adjusted contract effect (stat_3)

- **Contract:** Adjusted for monthly_fee and support_calls in one logistic regression, monthly contract remains significant. Adjusted OR 2.36 (95% CI 1.67 to 3.34), p = 1.19e-06. The unadjusted OR is 2.22, so the effect is slightly larger after adjustment.
- **monthly_fee:** Adjusted OR 1.018 per unit of fee (95% CI 1.012 to 1.024), p = 1.01e-09.
- **support_calls:** Adjusted OR 1.458 per additional call (95% CI 1.275 to 1.668), p = 3.50e-08.
- **Collinearity:** VIFs are 2.24 for monthly contract, 2.99 for monthly_fee, and 2.19 for support_calls, all below the usual threshold of 5. The point-biserial correlation between monthly contract and monthly_fee is r = 0.024 (p = 0.49).

### monthly_fee gradient by contract (stat_4)

- **Churn by fee quartile, monthly vs annual (n in brackets):**
  - Q1: monthly 23.7% (118), annual 8.5% (82); gap 15.2 points
  - Q2: monthly 28.7% (129), annual 28.2% (71); gap 0.5 points
  - Q3: monthly 43.5% (124), annual 19.7% (76); gap 23.8 points
  - Q4: monthly 52.8% (127), annual 30.1% (73); gap 22.6 points

  The gap is not monotone, since Q2 is near zero. This is descriptive, based on 71 to 129 customers per cell.

  ![Churn rate by monthly_fee quartile within monthly and annual contracts](tasks/stat_4/charts/stat4_churn_by_fee_quartile.png)

- **Fee-only interaction:** The contract × monthly_fee term in the fee-only logit has coefficient −0.0021 and p = 0.730. The fee gradient is not shown to differ between contracts.
- **Source of the other p-value:** The p = 0.6935 quoted in stat_2 comes from a model that also includes support_calls. It was cited in stat_4, not refit there, and is not the fee-only test.

### Predictive models

**Split and baseline (ml_1):** A stratified 80/20 split with seed 42 gives 640 training rows and 160 test rows. Churn is 31.25% in both sets (200 of 640 and 50 of 160). The scaler and one-hot encoder were fitted on training rows only (0 test rows used in fitting). The eight features are monthly_fee and support_calls (standardized), contract_annual, contract_monthly, and region_east, region_north, region_south, region_west. Only the four source columns were used, so there is no target leakage. Majority-class accuracy is 0.688 in both sets.

**Test split, 160 rows with 50 churners (ml_2):**

| Model | Accuracy | ROC AUC | Precision | Recall | F1 |
|---|---|---|---|---|---|
| Majority baseline | 0.688 | 0.500 | 0.000 | 0.000 | 0.000 |
| Logistic regression | 0.725 | 0.712 | 0.615 | 0.320 | 0.421 |
| Random forest | 0.631 | 0.627 | 0.408 | 0.400 | 0.404 |

  ![Test-set accuracy, ROC AUC, precision, recall and F1 on the 160-row split](tasks/ml_2/charts/ml2_model_comparison.png)

- Logistic regression is about 6 rows above the baseline on accuracy. The findings describe it as not clearly better, because its recall of 0.320 means it misses most churners, and the gap is untested for significance with 50 positives.
- The random forest does not beat the baseline on accuracy. Its training accuracy is 1.0, which the findings read as overfitting.

**5-fold stratified CV on all 800 rows (ml_3):**

| Model | Accuracy | ROC AUC | Precision | Recall | F1 |
|---|---|---|---|---|---|
| Majority baseline | 0.688 (sd 0) | 0.500 | 0 | 0 | 0 |
| Logistic regression | 0.721 (sd 0.028) | 0.695 (sd 0.030) | 0.613 (sd 0.083) | 0.280 (sd 0.079) | 0.382 (sd 0.087) |
| Regularized random forest | 0.698 (sd 0.012) | 0.671 (sd 0.035) | 0.594 (sd 0.117) | 0.096 (sd 0.036) | 0.164 (sd 0.056) |

- The logistic regression accuracy and AUC lead over the forest (0.023 and 0.024) are within fold SDs, so they are not clearly separated from fold noise. The recall and F1 gaps are clearly larger than fold noise. Precision does not separate the models.
- Logistic regression is 3.3 accuracy points above the baseline, with gain only partly outside fold noise. The regularized forest is 1.0 point above the baseline, within fold noise, so it does not clearly beat the baseline on accuracy. Its recall of 0.096 means it rarely predicts churn.

  ![Mean 5-fold CV accuracy, ROC AUC and F1 for baseline, logistic regression and regularized random forest; error bars show fold SD](tasks/ml_3/charts/ml3_cv_model_comparison.png)

### Feature importance

**Test-split importance (ml_2):**
- Random forest impurity importance: monthly_fee 0.771, support_calls 0.145, contract_monthly 0.020, contract_annual 0.019, region levels 0.011 or less each.
- Logistic coefficients (scaled features): monthly_fee 0.497, support_calls 0.452, contract_monthly 0.476, contract_annual −0.477, region_south −0.187, region_west 0.110, region_east 0.048, region_north 0.029.
- Random forest permutation importance (drop in ROC AUC): support_calls 0.070 (sd 0.036) and monthly_fee 0.052 (sd 0.038) are largest; contract_monthly 0.028 and contract_annual 0.025; all region levels are between −0.025 and 0.012.
- ml_2 also records an untested hypothesis that impurity importance under-credits contract in an overfit forest. It is not verified in ml_2.

**Cross-validated permutation importance (ml_3, ROC AUC drop, 5 folds):**
- Regularized forest: monthly_fee 0.078 (sd 0.031), contract 0.070 (sd 0.022), support_calls 0.041 (sd 0.008), region −0.008 (sd 0.013).
- Logistic regression: monthly_fee 0.086 (sd 0.028), support_calls 0.062 (sd 0.014), contract 0.057 (sd 0.014), region −0.0004 (sd 0.004).
- Contract is positive in every fold for both models. Its forest value varies by about a third of its mean (sd/mean 0.32), against about a quarter for logistic regression (0.24).
- The ml_2 and ml_3 rankings differ. ml_2 had support_calls first on test-split permutation, while under CV monthly_fee leads in both models.

**Impurity versus permutation, same folds (ml_4, status partial):**

| Feature | Impurity, training folds (sum to 1) | Permutation, held-out folds (AUC drop) |
|---|---|---|
| monthly_fee | 0.497 (sd 0.027) | 0.077 (sd 0.032) |
| support_calls | 0.234 (sd 0.004) | 0.036 (sd 0.011) |
| contract | 0.177 (sd 0.026) | 0.059 (sd 0.036) |
| region | 0.092 (sd 0.014) | −0.009 (sd 0.005) |

- monthly_fee ranks first on both measures.
- Contract ranks third by impurity and second by permutation. The impurity ordering of contract and support_calls is well beyond fold SDs. The permutation ordering is within fold noise, because contract permutation runs from 0.001 on fold 0 to 0.092 on fold 1.
- The two measures use different data (training vs held-out folds) and different scales, so the rank shift cannot be read as impurity under-crediting contract. The study does not answer this question (see Limitations).

**Impurity versus permutation, ml_5 run (status partial):**

| Feature | Impurity, training folds | Permutation, held-out folds (AUC drop) |
|---|---|---|
| monthly_fee | 0.586 (sd 0.013) | 0.066 (sd 0.027) |
| support_calls | 0.231 (sd 0.016) | 0.052 (sd 0.016) |
| contract | 0.099 (sd 0.009) | 0.054 (sd 0.023) |
| region | 0.084 (sd 0.008) | −0.006 (sd 0.017) |

- monthly_fee ranks first on both measures. Contract ranks third by impurity, and nominally second by permutation, but its permutation value (0.054) and support_calls (0.052) differ by 0.002, well within fold SDs. Contract's permutation on fold 1 is 0.013, against about 0.06 on the other folds.
- The region permutation value is negative on average, so region adds no held-out AUC in this run. Its impurity credit reflects in-sample fit.

## Limitations

**Data**
- The dataset has 800 rows and only 250 churners. The test split has only 50 churners, so the test-split model comparisons are noisy.
- The support_calls counts at 5 or more are very small (11 at 5, 1 at 6, 1 at 7), and individual rates at those levels are unstable.
- Region's effect is negligible on every measure used.

**Caveats stated in the findings**
- The contract × support_calls and contract × monthly_fee interaction tests have limited power. A non-significant result does not show that the effects are equal across contracts.
- The descriptive widening of the contract gap with support calls, and the non-monotone monthly_fee gap by quartile, are not reliable findings. Cell sizes are modest.
- The logistic regression advantage over the baseline on test-split accuracy is not tested for significance.
- Test-split permutation and impurity results come from an overfit random forest (training accuracy 1.0). The ml_2 impurity values are not comparable to the regularized-forest CV values.
- The Yates and uncorrected contract chi-square values differ (22.10 and 22.84). Both are reported, and neither should be read as one result.
- The permutation measure is ROC AUC, not accuracy. The findings make no accuracy-based importance claims.
- All findings are associations. No causal claims are supported.

**Unresolved review issues (lead's objections still stand)**
1. **The brief's question is not answered.** Whether impurity under-credits contract relative to permutation in the same model remains untested. Impurity is computed on training folds and permutation on held-out folds, and the two measures are on different scales. The ml_5 run was designed to match the brief, but its permutation ordering of contract and support_calls is not stable, so it does not settle the question. Affected findings: ml_2 hypothesis, ml_4 table, ml_5 table.
2. **ml_4 does not reproduce ml_3 on what is claimed to be the same folds.** The ml_4 contract permutation is 0.059 (sd 0.036) against ml_3's relayed 0.070 (sd 0.022), and support_calls is 0.036 (sd 0.011) against 0.041 (sd 0.008). The source of this difference is unknown until the ml_3 records are checked. The ml_3 values quoted in this report are the lead's relayed figures and are not verified.
3. **ml_5 does not reconcile with ml_4 under nominally identical settings.** Impurity contract is 0.099 (sd 0.009) in ml_5 against 0.177 (sd 0.026) in ml_4, and monthly_fee is 0.586 against 0.497. The permutation values also differ. The cause is unknown.
4. **ml_5 does not reconcile with ml_3 for any of the four features on permutation.** Monthly_fee is 0.066 (sd 0.027) in ml_5 against 0.078 (sd 0.031) relayed from ml_3, and contract is 0.054 (sd 0.023) against 0.070 (sd 0.022). Region is close in mean but not in SD. The cause is unknown.
5. **The ml_3 settings are not confirmed to match ml_4 or ml_5.** The ml_5 settings are documented, but it is not established that they match ml_3 or ml_4.

**Failed tasks:** None reported. ml_4 and ml_5 have status partial, and their gaps are listed above.

## Open questions

- Is the monthly-contract effect still present after adjusting for monthly_fee and support_calls in a larger sample? (Partly answered by stat_3 on this sample; the larger-sample question is open.)
- Are the monthly_fee and support_calls gradients driven by contract type (confounding)? stat_3 reports low collinearity, but the question is not fully answered.
- Is the support_calls gradient steeper for monthly contracts in a larger sample, with the interaction tested at adequate power?
- Is the support_calls effect robust once the sparse counts at 5 or more calls are grouped? (They were pooled into 3 or more; no robustness test was run.)
- Do the small regional differences hold up with a significance test? (Answered: not significant, p = 0.448.)
- Does the monthly-minus-annual gap by fee quartile remain stable in a larger sample, with the contract × monthly_fee interaction tested at adequate power?
- Would cross-validation or a tuned, more regularized random forest change the conclusion that the forest does not beat the baseline on accuracy? (Partly addressed by ml_3 with one regularized configuration; tuning was not tested.)
- Would a tuned forest close the recall and F1 gap to logistic regression?
- Do the logistic-regression vs baseline and vs forest accuracy and AUC differences hold with repeated CV or a larger sample, given fold SDs of about 0.03?
- Does permutation importance under CV support or reject the untested hypothesis that impurity importance under-credits contract? (Not answered; see Limitations.)
- Why is contract permutation importance near zero on fold 0 and fold 1 in some runs but high on other folds, for example through an interaction with monthly_fee?
- Is the contract vs support_calls permutation ordering stable across several CV seeds?
- Is impurity credit to contract inflated when compared with out-of-fold permutation on the same training-fold data?
- What is the source of the ml_3, ml_4 and ml_5 mismatches? This requires checking the ml_3 records for fold seed, random-forest random_state, permutation repeats and feature set.