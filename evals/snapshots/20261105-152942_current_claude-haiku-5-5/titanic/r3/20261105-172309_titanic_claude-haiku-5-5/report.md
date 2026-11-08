# Titanic Survival Analysis: Who Survived (Target: Survived)

## Summary

- **Sex and class are the strongest unadjusted associations with survival.** Females survived at 74.2% versus 18.9% for males (chi-square p = 3.7e-59, Cramér's V = 0.543). Survival fell from 63.0% in class 1 to 24.2% in class 3.
- **Sex and class interact, and the interaction holds after adjustment.** Females in classes 1 and 2 survived at 96.8% and 92.1%, but females in class 3 at 50.0%. The Sex x Pclass interaction was significant unadjusted (p = 5.6e-7) and after adjusting for Age, log Fare and Embarked (p = 5.0e-8, on 712 complete cases).
- **After adjusting for Pclass and Sex, Fare and Embarked lose significance, while class 3 and family size remain.** The Fare association (unadjusted p = 2.1e-16) is not significant after adjustment (likelihood-ratio p = 0.173). The joint Embarked test falls to p = 0.069. Class 3 (OR 0.202) and family size (OR 0.850 per person, p = 0.012) remain significant.
- **The best predictive model is logistic regression on the full feature set, with test accuracy 0.855 against a majority-class baseline of 0.615.** This model includes a Title feature derived from Name, which the brief excluded. The brief-compliant feature set gives 0.805 for logistic regression and 0.827 for random forest. Both beat the baseline.
- **Missingness is not random.** Cabin is missing for 77.1% of rows and is strongly tied to class and to survival. Its association with survival remains after adjusting for Pclass and Sex (adjusted OR 0.396). Age missingness is tied to class, and its association with survival is not significant after adjustment (adjusted OR 0.87, p = 0.55).

## Data

- **Size:** 891 rows, 12 columns.
- **Target:** Survived (binary). 0: 61.6%; 1: 38.4% (342 survived, 549 did not).
- **Features used:** Pclass, Sex, Age, SibSp, Parch, Fare, Embarked (numeric and categorical). Family size (SibSp + Parch) was derived. PassengerId, Ticket, Cabin and Name were not used as features. Title was derived from Name in the ML task only.
- **Missing values:**
  - Cabin: 687 of 891 (77.1%)
  - Age: 177 (19.9%)
  - Embarked: 2 (0.2%)
  - All other columns are complete.
- **Data premise mismatch:** The task premise described three rows with missing Embarked. The data has two.
- **No date or time features.**

## Findings

### Overall survival and group rates

Overall, 38.4% of passengers survived.

- **Sex:** Females survived at 74.2% (n = 314); males at 18.9% (n = 577).
- **Pclass:** Class 1 at 63.0% (n = 216), class 2 at 47.3% (n = 184), class 3 at 24.2% (n = 491).
- **Sex and Pclass together:** Females in classes 1 and 2 survived at 96.8% and 92.1%, and females in class 3 at 50.0%. Males fell from 36.9% in class 1 to 15.7% in class 2 and 13.5% in class 3.

![Survival rate by Sex and Pclass](tasks/eda_1/charts/survival_rate_by_sex_pclass.png)

- **Embarked:** Cherbourg (C) had the highest survival at 55.4% (n = 168), then Queenstown (Q) at 39.0% (n = 77) and Southampton (S) at 33.7% (n = 644). The two passengers with missing Embarked both survived.
- **Age bins:** Children aged 0 to 12 survived at 58.0% (n = 69), 13 to 18 at 42.9% (n = 70), 19 to 35 at 38.3% (n = 358), 36 to 60 at 40.0% (n = 195), and 60+ at 22.7% (n = 22). Survival does not fall monotonically with age. The child group has the highest rate among the bins, and the oldest group the lowest. The 177 passengers with missing Age are excluded from these bins.
- **Fare quartiles:** Q1 (Fare 0.00 to 7.90) survived at 19.7% (n = 223); Q2 (7.93 to 14.45) at 30.4% (n = 224); Q3 (14.46 to 31.00) at 45.5% (n = 222); Q4 (31.28 to 512.33) at 58.1% (n = 222).
- **Mean values:** Survivors had a mean Fare of 48.4 against 22.1 for non-survivors, and a mean Age of 28.3 against 30.6 (Age means exclude missing values).

### Significance tests and effect sizes

Seven tests were run, with a Bonferroni-adjusted alpha of 0.0071.

| Factor | Test | Result | Effect size |
|---|---|---|---|
| Sex | Chi-square | χ² = 263.1, df 1, p = 3.7e-59 | V = 0.543 (large) |
| Pclass | Chi-square | χ² = 102.9, df 2, p = 4.5e-23 | V = 0.340 |
| Embarked (n = 889) | Chi-square | χ² = 26.5, df 2, p = 1.8e-6 | V = 0.173 |
| Family group | Chi-square | χ² = 74.5, df 2, p = 6.5e-17 | V = 0.289 |
| Fare | Mann-Whitney | U = 129,951.5, p = 4.6e-22 | rank-biserial −0.384 |
| Family size (numeric) | Mann-Whitney | U = 110,099, p = 8.0e-7 | rank-biserial −0.173 |
| Age (n = 714) | Mann-Whitney | U = 57,682, p = 0.16 | rank-biserial 0.062 (negligible) |

Significant after Bonferroni: Sex, Pclass, family group, Fare, family size and Embarked. Age is not significant.

Key contrasts:

- **Female vs male:** difference 55.3 percentage points (95% CI 49.5 to 61.1); odds ratio 12.35 (95% CI 8.90 to 17.14).
- **Class 1 vs class 3:** difference 38.7 points (95% CI 31.3 to 46.2); odds ratio 5.31 (95% CI 3.76 to 7.50).
- **Class 2 vs class 3:** difference 23.0 points (95% CI 14.9 to 31.2); odds ratio 2.80 (95% CI 1.96 to 4.00).

Family size: the grouped test (alone, 1 to 3, 4+) and the numeric test both give significant results. The Embarked and Fare associations are unadjusted.

![Survival rate (share surviving) by Pclass and Sex](tasks/stat_1/charts/stat1_rate_by_sex_pclass.png)

### Sex x Pclass interaction

- In the logistic regression, the Sex x Pclass interaction is significant: LR χ² = 28.79, df 2, p = 5.6e-7. This means the Pclass gap differs by sex under the logistic model. It is not a general statement about effect size.
- Within females, class 2 vs class 1 has OR 0.385 (95% CI 0.093 to 1.592), not significant. Class 3 vs class 1 has OR 0.033 (95% CI 0.010 to 0.109).
- Within males, class 2 vs class 1 has OR 0.320 (95% CI 0.169 to 0.603). Class 3 vs class 1 has OR 0.268 (95% CI 0.166 to 0.433).
- The two computations of the within-sex female class 2 p-value disagree. The Wald-based figure is 0.19, and the Fisher exact figure is 0.30. For males, the Wald p-value for class 2 is 0.00043 and the Fisher p-value is 0.00033. Both are reported, and the choice of test is not resolved here.

![Survival rate by passenger class, separately for females and males](tasks/stat_2/charts/stat2_rate_by_sex_pclass.png)

- **Family size and Sex:** Family size does not significantly change the effect of Sex once Pclass is controlled (LR χ² = 5.58, df 2, p = 0.061). The female-by-small-family term is nominally significant (p = 0.018), but the joint test is not, so this is weak evidence only.

### Adjusted associations (logistic regression, n = 889)

Reference categories: class 1, male, Embarked C.

- **Pclass:** class 2 vs 1, OR 0.591 (95% CI 0.340 to 1.028), p = 0.062. Class 3 vs 1, OR 0.202 (95% CI 0.119 to 0.344), p < 0.001. The Pclass likelihood-ratio test gives p = 8.1e-10.
- **Sex:** female vs male, OR 15.32 (95% CI 10.39 to 22.58), p < 0.001.
- **Embarked:** the joint likelihood-ratio test gives LR = 5.34, df 2, p = 0.069, down from p = 2.4e-6 unadjusted. Adjusted OR for Q vs C is 0.811 (95% CI 0.392 to 1.678, p = 0.57). Adjusted OR for S vs C is 0.596 (95% CI 0.378 to 0.939, p = 0.026). S is nominally significant alone, but the joint test is not significant at 0.05.
- **Fare:** adjusted OR 1.003 per unit (95% CI 0.998 to 1.008). The likelihood-ratio test gives LR = 1.86, df 1, p = 0.173. The unadjusted Fare association was p = 2.1e-16. The Fare-Pclass correlation is −0.548, with a VIF of 1.75 for Fare. All VIFs are below 5.
- **Family size:** adjusted OR 0.850 per person (95% CI 0.748 to 0.965), p = 0.012. The likelihood-ratio test gives LR = 6.80, df 1, p = 0.009. The unadjusted linear logit for family size gives OR 1.023 per person, p = 0.59. The adjusted and unadjusted estimates point in opposite directions. The unadjusted grouped chi-square and numeric Mann-Whitney tests are significant. These tests answer different questions from the linear logit, and the data here do not explain the discrepancy. Whether the family-size effect is non-linear is not established. It is an open question.

![Adjusted odds ratios with 95% CI; reference: class 1, male, Embarked C, Fare per unit, FamilySize per person](tasks/stat_4/charts/stat4_adjusted_or.png)

### Sex x Pclass interaction after adjusting for Age, log Fare and Embarked

- The interaction remains significant: LR χ² = 33.64, df 2, p = 5.0e-8, on 712 complete cases. The unadjusted interaction on 891 rows was LR χ² = 28.79, p = 5.6e-7.
- The adjusted estimates are:
  - Females, class 2 vs 1: OR 0.331 (95% CI 0.073 to 1.508), p = 0.15, not significant.
  - Females, class 3 vs 1: OR 0.015 (95% CI 0.004 to 0.061), p < 0.001. The unadjusted OR was 0.033.
  - Males, class 2 vs 1: OR 0.164 (95% CI 0.072 to 0.370), p < 0.001. The unadjusted OR was 0.320.
  - Males, class 3 vs 1: OR 0.131 (95% CI 0.059 to 0.289), p < 0.001. The unadjusted OR was 0.268.
- The male penalties are stronger after adjustment. However, the adjusted model uses 712 rows (177 missing Age and 2 missing Embarked, with no overlap) and the unadjusted model uses 891. The change cannot be attributed to adjustment alone, because no unadjusted model has been refit on the same 712 rows.

### Child advantage within Sex x Pclass strata (partial, exploratory)

Each stratum compares children aged 0 to 12 with older passengers. Six strata were defined post hoc, with 1 to 25 children per stratum.

- **Male class 2:** all 9 children survived, against 6.7% of 90 older males. The difference is 93.3 points (Newcombe 95% CI 62.6 to 96.9). Holm-adjusted p is below 0.0001, so it remains significant after adjustment across the six strata.
- **Male class 3:** 36.0% of 25 children survived, against 12.7% of 228 older males. The difference is 23.3 points (Newcombe 95% CI 6.8 to 43.1). Fisher OR 3.86, Fisher p = 0.0052, Holm p = 0.026. It remains significant after adjustment.
- **Male class 1:** all 3 children survived, against 37.8% of 98 older males. The difference is 62.2 points (Newcombe 95% CI 5.2 to 71.2). Fisher p = 0.059 and Holm p = 0.18. Not significant after adjustment. The estimate is unreliable with three children.
- **Female class 1:** 0 of 1 child survived, against 97.6% of 84 older females. This is a nominal negative difference (Newcombe 95% CI −99.3 to −18.1). Fisher p = 0.035 and Holm p = 0.14. Not significant after adjustment. The Wald interval reported for this stratum is invalid and is not used.
- **Female class 2:** 100% of 8 children survived, against 90.9% of 66 older females. Difference 9.1 points (Newcombe 95% CI −23.7 to 18.4). Not significant.
- **Female class 3:** 47.8% of 23 children, against 45.6% of 79 older females. Difference 2.3 points (Newcombe 95% CI −19.3 to 24.2). Not significant.

The overall Age test is not significant (p = 0.16). The stratified results are consistent with that overall null being an average over stratum-level patterns. No interaction test was run, so this does not establish that the child effect varies by stratum.

### Age missingness and survival

- Age-missing rows survived at 29.4% (n = 177), against 40.6% for Age-present rows (n = 714).
- Unadjusted chi-square: eda_2 reported χ² = 7.11, p = 0.008. stat_6 recomputed the test without continuity correction and reported χ² = 7.57, p = 0.006. The two values differ and the cause is not verified. Both are reported.
- Age missingness is strongly related to Pclass (χ² = 46.1, p = 1e-10). Among Age-missing rows, 76.8% are class 3, 16.9% class 1 and 6.2% class 2. Of these rows, 70.1% are male.
- **Adjusted for Pclass and Sex:** OR 0.87 (95% CI 0.56 to 1.36), p = 0.55. The association is not significant after adjustment. The interval is wide and includes meaningful effects in both directions. No decomposition of the crude gap was run.

### Cabin missingness and survival

- Cabin-missing rows survived at 30.0% (n = 687), against 66.7% for Cabin-present rows (n = 204). The unadjusted chi-square gives χ² = 87.9, p = 6.7e-21.
- Cabin missingness is strongly tied to Pclass (χ² = 557.3, p = 1e-121). It cannot be treated as missing completely at random.
- **Unadjusted logistic OR:** 0.214 (95% CI 0.153 to 0.299), p = 1.4e-19.
- **Adjusted for Pclass and Sex:** OR 0.396 (95% CI 0.211 to 0.744), p = 0.0039, n = 891. Adjustment moves the OR toward 1, but the association remains. This is an association after controlling for Pclass and Sex. It is not evidence of a causal effect of Cabin recording on survival.

![Survival rate for rows with Age or Cabin present vs missing](tasks/eda_2/charts/eda2_survival_by_missingness.png)

The two Embarked-missing rows (PassengerId 62 and 830) are both class 1, female, paid Fare 80.0, have Cabin B28, and both survived.

### Predictive models

The test split is stratified 80/20 (712 train, 179 test), with seed 42. The majority-class baseline accuracy is 0.615.

**Headline models (full feature set, including the derived Title feature from Name):**

| Model | Test accuracy | ROC AUC | F1 | Train accuracy |
|---|---|---|---|---|
| Logistic regression | 0.855 | 0.884 | 0.803 | 0.830 |
| Random forest | 0.827 | 0.837 | 0.770 | 0.983 |

**Brief-compliant models (no derived features: no FamilySize, IsAlone or Title):**

| Model | Test accuracy | ROC AUC | F1 | Train accuracy |
|---|---|---|---|---|
| Logistic regression | 0.805 | 0.843 | 0.724 | 0.806 |
| Random forest | 0.827 | 0.836 | 0.760 | 0.982 |

- The brief asked for the feature set without derived features. **The brief-compliant answer is the brief-only set.** The full-model numbers include Title and are reported as additional context. Dropping derived features costs logistic regression about 0.05 accuracy and leaves random forest accuracy unchanged.
- Both random forests overfit. The brief-only forest has train accuracy 0.982 and test accuracy 0.827. The gap is about 0.15.
- **Feature importance (within each model only):** Age ranks 2nd in the random forest in both feature sets (0.208 full, 0.245 brief). In logistic regression, Age ranks 6th in the full model (coefficient 0.338) and 4th in the brief-only model (0.503). Sex ranks near the top in both logistic regressions (0.579 full, 0.639 brief). Pclass ranks first in both logistic regressions (0.852 full, 0.930 brief) but 6th in the full random forest (0.076). In the full random forest, Fare (0.237) and Age (0.208) lead.
- **Embarked ranks:** In the full logistic regression, the Embarked dummies rank 13th (Q), 14th (S) and 16th (C) of 17. In the full random forest, Embarked_S ranks 12th, Embarked_C 13th and Embarked_Q 16th. This was checked against the complete rank record and matches. In the brief-only logistic regression, Embarked_S and Embarked_Q rank 6th and 7th of 10, above Fare (8th). Their rank depends on which features are included.
- Logistic regression coefficients and random forest importances are not directly comparable. Compare orders within each model.
- SibSp, Parch and FamilySize are collinear by construction, so their individual coefficients should not be read alone.

![Test accuracy, F1 and ROC AUC of logistic regression and random forest for predicting Survived, with majority-class accuracy as dashed line](tasks/ml_1/charts/ml_1_model_comparison.png)

## Limitations

- **Data:** Cabin is 77.1% missing, Age is 19.9% missing, and Embarked is missing for two rows (the premise of three was wrong). Missingness in Age and Cabin is tied to class and, for Cabin, to survival.
- **Causation:** All findings are associations. None establishes a causal effect, and none is claimed here.
- **Adjusted models use fewer rows:** The Sex x Pclass adjusted model and the Age-missingness model use different samples from the unadjusted ones (712 rows against 891). The unadjusted model has not been refit on the 712 rows, so changes in estimates cannot be attributed to adjustment alone.
- **Inconsistent values across tasks:** Two figures for the Age-missingness chi-square differ (7.11 and 7.57). Within-sex female class 2 p-values differ between Wald (0.19) and Fisher (0.30) methods. Both are reported, and the discrepancies are not resolved.
- **Family size non-linearity (review issue, resolved by removing a claim):** The stat_4 finding stated that the grouped chi-square and Mann-Whitney tests capture a non-linear pattern. The data do not show this. The only supported statement is that the linear logit is not significant unadjusted, while the grouped chi-square and Mann-Whitney tests are significant. These tests answer different questions, and the discrepancy is not explained here. Non-linearity is an open question.
- **Stratified child analysis (stat_3, partial):** Strata were defined post hoc. Child counts are very small (1 to 25 per stratum). No interaction test was run. The female class 1 Wald interval is invalid and is not used. Only male class 2 and male class 3 remain significant after Holm adjustment, and these results are exploratory.
- **Predictive models (review issue, unresolved):** The headline models include the Title feature derived from Name, which the brief said to drop. The brief-compliant answer is the brief-only set, as stated above. The Age ranking in the full logistic regression was corrected to 6th. The remaining review issues cannot be resolved because the task cannot be redone. These are:
  - No ablation with Fare removed, and no Fare-Pclass test beyond the correlation.
  - No ablation with Title removed.
  - No repeated cross-validation, so the scores on 179 test rows have no confidence intervals.
  - No random forest tuning (depth or minimum leaf size), so overfitting is not addressed.
- **Adjustment limits:** The adjusted Embarked and Fare results are from models that also contain Pclass and Sex. Adjustment for Pclass and Sex does not decompose the crude Age-missingness gap.

## Open questions

- Does Fare add predictive power beyond Pclass? Would an ablation with Fare removed, and the Fare-Pclass correlation reported in detail, show this?
- Does the Title feature drive most of the gain of the full models over the brief-only models?
- How stable are the test scores? Would repeated stratified cross-validation give confidence intervals?
- Would tuning the random forest (depth, minimum leaf size) reduce overfitting and close the gap with logistic regression?
- Why do females in class 3 survive at 50.0%, far below the other female groups? Does this hold within each class?
- Does the child advantage hold within each Sex and Pclass group in a formal model? Does a child-by-stratum interaction test support it?
- Does family presence (SibSp + Parch) explain the male class 2 and male class 3 child advantage?
- Is the family-size effect non-linear (alone vs small vs large families) after adjusting for Sex and Pclass?
- Do the Embarked differences reflect the port-by-class mix? Would testing Embarked within each Pclass show this?
- Should the 177 missing Age values be imputed, and do results hold under multiple imputation or an Age-imputed model?
- Does the Cabin-missingness association differ by Pclass or Sex (interaction terms)? Can Cabin deck or presence be used as a predictive feature?
- Does the Age-missingness association differ by stratum, or does the crude-to-adjusted change decompose into Pclass and Sex contributions?
- How should the two Embarked-missing rows be filled?