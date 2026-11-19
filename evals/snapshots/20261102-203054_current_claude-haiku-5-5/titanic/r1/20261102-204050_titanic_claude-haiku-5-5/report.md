# Titanic Passenger Survival: Which Passenger Attributes Predicted Survival (Target: Survived)

## Summary

- **Sex was the strongest predictor.** Females survived at 74.2% (n=314) versus 18.9% for males (n=577). The chi-square test gave χ² = 263.05, df = 1, p = 3.7e-59, Cramér's V = 0.543. The female-minus-male difference is 55.3 percentage points (95% Wald CI 49.5 to 61.1).
- **Survival fell with passenger class, and the Sex effect varies by class.** Survival was 63.0% in Pclass 1, 47.3% in Pclass 2 and 24.2% in Pclass 3 (χ² = 102.89, df = 2, p = 4.5e-23, V = 0.340). The Sex × Pclass interaction was significant (LR χ² = 28.79, df = 2, p = 5.6e-7). Pclass 3 females survived at 50.0%, while Pclass 1 and 2 females survived at 96.8% and 92.1%.
- **Predictive models beat the majority-class baseline.** The baseline test accuracy was 61.5%. Logistic regression reached 80.5% test accuracy (ROC AUC 0.843, F1 0.724), and a random forest reached 79.3% (ROC AUC 0.839, F1 0.709). Permutation importance ranked Sex_male first, then Pclass and Age.
- **Missing Cabin is associated with lower survival, but the link is not fully explained by class and fare.** Survival was 30.0% without a recorded Cabin and 66.7% with one. The association remained significant after adjusting for Pclass and Fare (OR 0.351, p = 0.00013). The Cabin × Pclass interaction was not significant (p = 0.379).
- **Age did not differ significantly between survivors and non-survivors** (Mann-Whitney p = 0.16, negligible effect), whereas Fare did (p = 4.6e-22, medium effect).

## Data

- **Size:** 891 rows × 12 columns.
- **Target:** Survived is binary. 342 passengers survived (38.4%) and 549 did not (61.6%).
- **Features analysed:** Pclass, Age, SibSp, Parch and Fare (numeric); Sex and Embarked (categorical). Family size was derived as SibSp + Parch. PassengerId, Ticket, Cabin and Name were not used as features as they stand.
- **Missing values:**
  - Age: 177 of 891 (19.9%).
  - Cabin: 687 of 891 (77.1%).
  - Embarked: 2 of 891 (0.2%).
  - All other columns are complete.

## Findings

### 1. Survival rates by group

**Sex.** Females survived at 74.2% (n=314) and males at 18.9% (n=577). Mean Age was 27.9 for females and 30.7 for males. Mean Fare was 44.5 for females and 25.5 for males.

**Passenger class.** Survival was 63.0% in Pclass 1 (n=216), 47.3% in Pclass 2 (n=184) and 24.2% in Pclass 3 (n=491). Mean Fare rose from 13.7 in Pclass 3 to 84.2 in Pclass 1. Mean Age rose from 25.1 in Pclass 3 to 38.2 in Pclass 1.

**Sex within class.** The counts below come from the Sex × Pclass table.

| Sex | Pclass 1 | Pclass 2 | Pclass 3 |
|---|---|---|---|
| Female | 96.8% (91 of 94) | 92.1% (70 of 76) | 50.0% (72 of 144) |
| Male | 36.9% (45 of 122) | 15.7% (17 of 108) | 13.5% (47 of 347) |

![Survival rate by Sex and Pclass: proportion of passengers who survived, per sex and passenger class](tasks/eda_1/charts/survival_rate_by_sex_pclass.png)

**Embarkation.** The analysis excludes the 2 passengers with missing Embarked.
- C (Cherbourg, n=168): survival 55.4%, mean Fare 60.0.
- Q (Queenstown, n=77): survival 39.0%, mean Fare 13.3.
- S (Southampton, n=644): survival 33.7%, mean Fare 27.1.
- Mean Age ranged narrowly from 28.1 to 30.8 across the three ports.

**Family size (SibSp + Parch).** The relationship is non-monotone.

| Family size | n | Survival | Mean Age | Mean Fare |
|---|---|---|---|---|
| 0 (alone) | 537 | 30.4% | 32.22 | 21.24 |
| 1 | 161 | 55.3% | 31.39 | 49.89 |
| 2 | 102 | 57.8% | 26.04 | 39.69 |
| 3 | 29 | 72.4% | 18.27 | 54.86 |
| 4 | 15 | 20.0% | 20.82 | 58.09 |
| 5 | 22 | 13.6% | 18.41 | 73.72 |
| 6 | 12 | 33.3% | 15.17 | 29.37 |
| 7 | 6 | 0.0% | 15.67 | 46.90 |
| 10 | 7 | 0.0% | no Age recorded | 69.55 |

Survival is 0 to 33% for sizes 4 and above, where each group has 22 or fewer passengers. Mean Age falls with family size overall, but not strictly monotonically: size 4 (20.82) is above size 3 (18.27).

### 2. Significance tests and effect sizes

**Categorical associations with Survived** (chi-square tests):

| Variable | χ² | df | p | Cramér's V |
|---|---|---|---|---|
| Sex | 263.05 | 1 | 3.7e-59 | 0.543 (large) |
| Pclass | 102.89 | 2 | 4.5e-23 | 0.340 (medium to large) |
| Embarked | 26.49 | 2 | 1.8e-6 | 0.173 (small) |
| Family size | 80.67 | 8 | 3.6e-14 | 0.301 |

- **Embarked** is significant but weak. The 2 passengers with missing Embarked are excluded.
- **Family size** is significant, but 27.8% of cells have expected counts below 5 (minimum expected count 2.30). The p-value is therefore approximate, and the "medium" label for V = 0.301 should not be taken as firm. With sizes 4 and above pooled into one group, the test gives χ² = 77.59, df = 4, p = 5.6e-16, V = 0.295. The association therefore persists after pooling, though the pooled test uses only 891 passengers in five groups.

![Survival rate by family size: proportion of passengers who survived, per family size](tasks/stat_1/charts/stat1_survival_by_family_size.png)

**Continuous variables, survivors versus non-survivors** (Mann-Whitney tests):
- **Age:** p = 0.16, rank-biserial = -0.062 (negligible). Both medians are 28.0.
- **Fare:** p = 4.6e-22, rank-biserial = 0.384 (medium). Median Fare is 26.0 for survivors and 10.5 for non-survivors.

**Survival rate differences** (Wald 95% CIs):
- Female minus male: 55.3 percentage points [49.5, 61.1].
- Pclass 1 minus Pclass 3: 38.7 percentage points [31.3, 46.2].

### 3. Sex × Pclass interaction

The Sex × Pclass interaction is significant: the likelihood-ratio test comparing the interaction logit with the additive logit gives χ² = 28.79, df = 2, p = 5.6e-7.

![Survival rate (proportion survived) for each Sex x Pclass cell; counts: female 94/76/144 and male 122/108/347 in Pclass 1/2/3](tasks/stat_2/charts/stat2_rate_by_sex_pclass.png)

In the interaction logit with female Pclass 1 as reference:
- The female Pclass 1 baseline odds are 30.3.
- The male odds ratio is 0.019 in Pclass 1, about 0.016 in Pclass 2, and about 0.157 in Pclass 3. The sex gap is therefore much narrower in Pclass 3.
- Among females, the odds ratio is 0.385 for Pclass 2 versus Pclass 1 and 0.033 for Pclass 3 versus Pclass 1.
- Among males, the class penalty is much smaller than among females, whose survival is already low.

These odds ratios are point estimates; confidence intervals were not reported. Some cells are small.

### 4. Missingness in Age, Cabin and Embarked

**Counts.** Age is missing for 177 passengers (19.9%), Cabin for 687 (77.1%) and Embarked for 2 (0.2%). No other column has missing values.

**Embarked.** The two passengers with missing Embarked are PassengerId 62 and 830. Both are female Pclass 1 survivors, with Fare 80 and Cabin B28. Two rows are too few to test whether Embarked missingness relates to Survived, Pclass, Sex or Fare.

**Age.** Passengers without a recorded Age survived at 29.4%, versus 40.6% for those with an Age.

| Group | n | Share Pclass 1 | Share Pclass 3 | Share female | Mean Fare |
|---|---|---|---|---|---|
| Age recorded | 714 | 26.1% | 49.7% | 36.6% | 34.69 |
| Age missing | 177 | 17.0% | 76.8% | 29.9% | 22.16 |

**Cabin.** Passengers without a recorded Cabin survived at 30.0%, versus 66.7% for those with a Cabin.

| Group | n | Share Pclass 1 | Share Pclass 3 | Share female | Mean Fare |
|---|---|---|---|---|---|
| Cabin recorded | 204 | 86.3% | 5.9% | 47.6% | 76.14 |
| Cabin missing | 687 | 5.8% | 69.7% | 31.6% | 19.16 |

![Survival rate (share survived) for passengers with and without a recorded Age and with and without a recorded Cabin](tasks/eda_2/charts/survival_by_missingness.png)

These are unadjusted descriptive comparisons. The missing-value groups contain far more Pclass 3 passengers and have lower mean Fares, so the crude differences coincide with class and fare. No adjusted test was run for Age or Cabin missingness in this step. Adjusted results for Cabin are reported in sections 5 and 6.

### 5. Cabin missingness and survival, within Pclass and adjusted

**Within each Pclass** (Fisher exact tests, uncorrected):

| Pclass | Survival with Cabin (n) | Survival without Cabin (n) | Fisher p |
|---|---|---|---|
| 1 | 66.5% (176) | 47.5% (40) | 0.030 |
| 2 | 81.3% (16) | 44.0% (168) | 0.007 |
| 3 | 50.0% (12) | 23.6% (479) | 0.080 |

Survival was lower without a recorded Cabin in all three classes. The Pclass 3 Cabin-recorded group has only 12 passengers. The three stratum tests are not adjusted for multiple comparisons.

![Survival rate (share survived) with and without a recorded Cabin, within each Pclass; Pclass 1: 176 with Cabin, 40 without; Pclass 2: 16 with, 168 without; Pclass 3: 12 with, 479 without](tasks/stat_3/charts/cabin_survival_by_pclass.png)

**Logistic regression of survival on Cabin missingness:**
- Unadjusted: coefficient -1.54 (odds ratio 0.214; 95% CI for the coefficient -1.87 to -1.21; p = 1.4e-19).
- Adjusted for Pclass (categorical) and Fare: coefficient -1.05 (odds ratio 0.351; 95% CI -1.58 to -0.51; p = 0.00013).

The coefficient shrinks by about 32% after adjustment, and the association remains significant.

**Cabin × Pclass interaction** (stat_4, adjusted for Fare):
- The likelihood-ratio test gives χ² = 1.94, df = 2, p = 0.379 (n = 891). The data do not show that the Cabin-missing association differs across Pclass. A non-significant result does not show that the association is equal across classes, because the test has low power here.
- Within Pclass 1, the Cabin-missing coefficient is -0.74 (OR 0.48; 95% CI -1.46 to -0.03; p = 0.041).
- Within Pclass 2, the coefficient is -1.73 (OR 0.18; 95% CI -3.02 to -0.43; p = 0.009). It rests on only 16 Cabin-recorded passengers, so the interval is very wide.
- Within Pclass 3, the coefficient is -1.19 (OR 0.30; 95% CI -2.34 to -0.04; p = 0.043). It rests on 12 Cabin-recorded passengers and is imprecise.
- All three within-class estimates are negative and overlap widely.

**Disagreement between the two tests in Pclass 3.** The stratum Fisher test (section above) gives p = 0.080 and is not significant. The Pclass 3 logistic estimate from the interaction model (adjusted for Fare) gives p = 0.043 and is significant at 0.05. The two methods differ in adjustment, so these results disagree. This report does not resolve the disagreement.

### 6. Predictive models

**Setup.** Models used Pclass, Sex, Age, SibSp, Parch, Fare and Embarked, with a stratified 80/20 split (712 training rows, 179 test rows, random_state = 42). Two preprocessing choices affect the results (see Limitations): the two missing Embarked values were filled with 'S' before the split, and Age was imputed with the training-split median of 28.5.

| Model | Test accuracy | Train accuracy | Test ROC AUC | Test precision | Test recall | Test F1 |
|---|---|---|---|---|---|---|
| Majority-class baseline (predict 0) | 61.5% | – | – | – | – | – |
| Logistic regression | 80.5% | 80.6% | 0.843 | 0.793 | 0.667 | 0.724 |
| Random forest (500 trees, min_samples_leaf=2) | 79.3% | 91.6% | 0.839 | 0.776 | 0.652 | 0.709 |

Both models beat the baseline by about 18 to 19 points. Logistic regression scored slightly higher than the random forest on every test metric, a gap of about 2 test passengers. The random forest's training accuracy of 91.6% shows some overfitting. The baseline figure of 61.5% differs slightly from the 61.6% in the brief because of the exact split.

**Feature importance.**
- Logistic regression coefficients (standardized features, in absolute value) rank Sex_male (1.27), Pclass (0.93) and Age (0.51) first, followed by SibSp (0.26) and Embarked_S (0.17).
- Random forest permutation importance on the 179 test rows gives a mean accuracy drop of 0.178 for Sex_male (SD 0.024 over 30 repeats), 0.042 for Pclass (SD 0.016) and 0.026 for Age (SD 0.016). This agrees with the logistic regression ranking at the top.
- Fare has a mean permutation importance of 0.006 (SD 0.017). Parch, both Embarked dummies and SibSp are at or below zero. These small values are within noise on 179 test rows.
- The random forest's impurity-based importance ranks Fare second (0.249), while its permutation importance is 0.006. The rankings differ. A possible explanation, that Fare shares information with Pclass, was proposed but not tested.

![Permutation importance for random forest predicting Survived on the test set](tasks/ml_1/charts/ml1_permutation_importance.png)

## Limitations

- **Observational data.** All results describe associations. None establishes a causal effect of any attribute on survival.
- **Unresolved review issue (eda_1).** The lead's review asked that eda_1 add mean Fare by family size and note that the Age decline with family size is not strictly monotone. Both are now reflected in the Findings above. The review issue is recorded as unresolved, so the objection still stands.
- **Family-size tests are sparse.** 27.8% of cells have expected counts below 5, and sizes 4 and above have 6 to 22 passengers each. The chi-square p-value is approximate. The family-size survival pattern is non-monotone and may be driven by small groups.
- **Missingness is not adjusted in the descriptive step.** The eda_2 comparisons are unadjusted. Age missingness was not tested with any adjusted model. Only Cabin missingness was adjusted (section 5).
- **Small Cabin-recorded groups.** Only 16 Cabin-recorded passengers are in Pclass 2 and 12 in Pclass 3. The stratum estimates are imprecise. The stratum p-values are not corrected for multiple comparisons.
- **Conflicting Pclass 3 Cabin result.** The Fisher test (p = 0.080) and the interaction-model estimate (p = 0.043) disagree on significance in Pclass 3 (section 5).
- **Model preprocessing.** The two missing Embarked values were filled with 'S' before the train/test split, which affects the Embarked dummies. Age was imputed using the training-split median (28.5), not the full-data median.
- **Model evaluation.** The test set has 179 rows, so differences of about 2 passengers between models are small. No cross-validation was run. The permutation importance ranks small features within noise.
- **Embarked missingness.** Two rows are too few to test, so Embarked missingness was not analysed further.
- **Failed tasks.** None. All five analysis tasks (eda_1, eda_2, stat_1 to stat_4, ml_1) reported complete.

## Open questions

- Does the Sex effect hold after controlling for Pclass and Fare, for example in a logistic regression with interactions? The Sex × Pclass interaction is reported, but the Sex effect was not tested after adjusting for Fare.
- Why does Cherbourg have higher survival, and is this explained by its higher share of Pclass 1 passengers? This was not tested.
- Is the non-monotone family-size pattern real or driven by small groups? Would grouping sizes into alone, 1 to 3, and 4 or more be more stable? This grouping was suggested but not run.
- Is the Embarked survival gap explained by class composition?
- Can Age missingness (177 passengers) be imputed from the title in Name without biasing survival estimates? Would a Title feature improve accuracy?
- Do survival rates and Sex/Pclass distributions differ within the Age-missing and Cabin-missing groups when analysed separately?
- Does the Cabin-missing association hold after also adjusting for Sex, Age and Age missingness?
- Is the Cabin association explained by deck letter or by the number of cabins recorded, rather than by missingness itself?
- Does the Cabin × Pclass interaction become testable with a larger sample or a pooled comparison across Pclass 2 and 3?
- Does cross-validation confirm that logistic regression beats the random forest?
- Does Fare add predictive value once Pclass is controlled for? Is Fare correlated with Pclass?
- Does the Embarked fill with 'S', or the training-split Age median, change the ranking of the small-importance features?