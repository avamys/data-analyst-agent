# Titanic Survival: Analysis Report on the Survived Target

## Summary

- **Sex is the strongest association with survival.** Female passengers survived at 74.2% (n=314) against 18.9% for males (n=577), a difference of 55.3 percentage points (Wald 95% CI 49.5 to 61.1; Cramér's V 0.543). These are unadjusted rates.
- **Passenger class and fare are also strongly associated, and they overlap with sex.** Pclass 1 survival was 63.0% and Pclass 3 was 24.2%. Fare is significantly associated with survival (Mann-Whitney p=4.6e-22, rank-biserial 0.384). Neither effect is adjusted for the others.
- **Sex and class interact.** The Sex x Pclass interaction is significant (LR chi2=28.79, 2 df, p=5.6e-7). Among females, survival was 96.8% in Pclass 1 and 50.0% in Pclass 3. Among males, it was 36.9% in Pclass 1 and 13.5% in Pclass 3. The interaction survives joint adjustment for Sex x Age and Fare (p=5.3e-6).
- **The predictive models beat the majority-class baseline.** The baseline is 61.5% on the test set. Logistic regression reached 82.1% test accuracy and a ROC AUC of 0.841. The random forest reached 81.0% and 0.841. The difference between them is within sampling noise.
- **The Age association is unresolved.** With imputed Age, the Mann-Whitney p is 0.25. With observed Age only, the rank test gives p=0.16 with a negligible effect, but the mean-difference CI (-4.47 to -0.09 years) excludes zero. Whether this survives multiplicity correction depends on how the test family is defined.

## Data

- **Size:** 891 rows × 12 columns.
- **Target:** `Survived` is binary. 549 passengers died (61.6%, coded 0) and 342 survived (38.4%, coded 1).
- **Features used:** Pclass, Sex, Age, SibSp, Parch, Fare and Embarked. FamilySize was derived for the tests. PassengerId, Ticket, Cabin and Name were not used directly as features. The profile lists no date or time features.
- **Missing values:**
  - Cabin: 687 of 891 (77.1%).
  - Age: 177 (19.9%). These were median-imputed by Pclass and Sex for the analyses that use all rows.
  - Embarked: 2 (0.2%). These were filled with the mode, S.
  - All other columns are complete.

## Findings

### Unadjusted survival rates by group

- **Sex:** female 74.2% (n=314), male 18.9% (n=577).
- **Pclass:** Pclass 1 63.0% (n=216), Pclass 2 47.3% (n=184), Pclass 3 24.2% (n=491).

![Survival rate (%) by Sex and Pclass](tasks/eda_1/charts/survival_by_sex_pclass.png)

- **Embarked:** Cherbourg (C) 55.4% (n=168), Queenstown (Q) 39.0% (n=77), Southampton (S) 33.9% (n=646). These rates are unadjusted.
- **Fare quartile:** Q1 19.7% (n=223), Q2 30.4% (n=224), Q3 45.5% (n=222), Q4 58.1% (n=222). Survival rises with fare quartile. This is unadjusted and overlaps with class.
- **Age bins, with imputed Age included:** 0–12 58.0% (n=69), 13–30 33.7% (n=487), 31–60 42.5% (n=313), 60+ 22.7% (n=22).
  - With observed Age only, 13–30 is 37.1% (n=340) and 31–60 is 42.0% (n=283).
  - The 0–12 and 60+ bins contain no imputed rows, so their rates are the same in both versions.
  - The 60+ bin is small.
- **Fare and Age by survival:**
  - Fare mean is 48.40 for survivors and 22.12 for non-survivors. Medians are 26.0 and 10.5.
  - Age mean (imputed) is 28.11 for survivors and 29.74 for non-survivors. Medians are 27 and 25.
  - With observed Age only, means are 28.34 and 30.63, and medians are both 28.

### Association tests and effect sizes

Tests are two-sided. Holm-adjusted p-values are across the 8 primary tests (3 chi-square, 5 Mann-Whitney).

- **Sex:** chi2=263.05 (1 df), p=3.7e-59, Cramér's V 0.543 (large). The female–male difference is 55.3 points (CI 49.5 to 61.1).
- **Pclass:** chi2=102.89 (2 df), p=4.5e-23, V 0.340 (medium). The Pclass 1 – Pclass 3 difference is 38.7 points (CI 31.3 to 46.2).
- **Embarked:** chi2=25.96 (2 df), p=2.3e-6, V 0.171 (small). Embarked was filled with S for 2 rows before this test.
- **Fare:** Mann-Whitney p=4.6e-22 (Holm 2.7e-21), rank-biserial 0.384 (medium). The mean difference (survived minus died) is 26.28 (Welch CI 18.73 to 33.83).
- **Parch:** Mann-Whitney p=3.7e-5 (Holm 0.00011), rank-biserial 0.122 (small). The mean difference is 0.14 (CI 0.03 to 0.24).
- **FamilySize:** Mann-Whitney p=8.0e-7 (Holm 4.0e-6), rank-biserial 0.173 (small). Medians are 2 for survivors and 1 for non-survivors. The mean difference is 0.06 (CI -0.14 to 0.25), which includes zero.
- **SibSp:** Mann-Whitney p=0.008 (Holm 0.016), rank-biserial 0.086 (negligible). The mean difference is -0.08 (CI -0.21 to 0.05), which includes zero.
- **Age (imputed):** Mann-Whitney p=0.25 (Holm 0.25), rank-biserial -0.046. The mean difference is -1.6 years (CI -3.5 to 0.2).

All three of Sex, Pclass and Embarked remain significant after Holm correction. Sex, Pclass, Embarked, Fare, Parch and FamilySize also remain significant after correction, and SibSp is significant but negligible in effect size. Sex, Pclass and Fare overlap, so none of these associations is an independent effect.

![Effect sizes by feature for association with Survived](tasks/stat_1/charts/stat1_effect_sizes.png)

**Age:** The result is inconclusive, not a confirmed null. Observed-only Age (290 survived, 424 died) gives a Mann-Whitney p=0.16 with rank-biserial -0.062, which is negligible. The mean difference is -2.28 years (Welch CI -4.47 to -0.09, p=0.041). A bootstrap percentile CI is -4.45 to -0.11. The 10% trimmed-mean difference is -1.58 years (survived 28.18, died 29.76). Medians are 28.0 in both groups. The trimmed result was not tested for outliers, so outliers are not established as the cause.

### Sex x Pclass and Sex x Age interactions

- **Sex x Pclass:** LR chi2=28.79 (2 df), p=5.6e-7.
- **Survival by sex and class (survivors/n, rate):**

| Sex | Pclass 1 | Pclass 2 | Pclass 3 |
|---|---|---|---|
| Female | 91/94 (96.8%) | 70/76 (92.1%) | 72/144 (50.0%) |
| Male | 45/122 (36.9%) | 17/108 (15.7%) | 47/347 (13.5%) |

- **Class gap within sex:** the Pclass 1 – Pclass 3 gap is 46.8 points among females and 23.3 points among males.
- **Source of the interaction:** in the logit with female x Pclass terms (reference female Pclass 1), female x Pclass 3 has coefficient -2.096 (p=0.0014). Female x Pclass 2 has coefficient 0.185 (p=0.82).

![Survival rate (%) by Pclass for female and male passengers](tasks/stat_2/charts/sex_pclass_rates.png)

- **Sex x Age (unadjusted):** on the 714 passengers with observed Age, LR chi2=9.55 (1 df), p=0.002. The female x Age coefficient is 0.041 (p=0.0024). This model is not adjusted for Pclass or Fare, and it excludes the 177 rows with missing Age.
- **Joint model (observed-Age rows, n=714):** the joint logit includes Sex x Pclass, Sex x Age and Fare.
  - Sex x Pclass: LR chi2=24.28 (2 df), p=5.3e-6. It survives adjustment.
  - Sex x Age: LR chi2=2.35 (1 df), p=0.126. It is no longer significant. The finding notes that the drop is consistent with class composition and fare, but does not establish the cause.
  - In the joint model (reference female Pclass 1), male x Pclass 3 has coefficient 1.715 (p=0.022). This p-value is uncorrected for the other coefficients. Male x Pclass 2 has coefficient -0.915 (p=0.273). Male x Age has coefficient -0.0267 (p=0.12). Fare has coefficient -0.00043 (p=0.86).

### Embarked after adjustment

- **Unadjusted:** LR=25.36 (2 df), p=3.1e-6.
- **Adjusted for Pclass and Fare:** LR=16.75 (2 df), p=0.00023. Part of the port association is shared with class and fare.
- **Adjusted for Pclass only:** LR=18.51 (2 df), p=9.5e-5.
- **Adjusted odds ratios (logit with Embarked, Pclass and Fare; reference Cherbourg):**
  - Southampton: OR 0.55 (95% CI 0.37 to 0.81, p=0.0026).
  - Queenstown: OR 1.28 (95% CI 0.70 to 2.34, p=0.41).
- The adjusted port effect is driven by Southampton versus Cherbourg. Queenstown does not differ from Cherbourg after adjustment.

### Missingness and its relation to survival

- **Cabin:** survival was 30.0% when Cabin is missing (n=687) and 66.7% when present (n=204), chi-square p=6.7e-21.
  - Cabin missingness is strongly tied to class: 479 of 687 missing-Cabin passengers are Pclass 3, against 12 of 204 with Cabin present (p=9.6e-122).
  - Of the 687 Cabin-missing passengers, 217 are female. Of the 204 with Cabin present, 97 are female (chi-square p=4.0e-5).
  - Cabin missingness is also associated with Embarked (p=7.5e-12). This test is unreliable because the two missing Embarked rows form a category with expected counts far below 5.
- **Cabin within class (Fisher p; Wald CI for the difference, missing minus present):**
  - Pclass 1: 47.5% (n=40) vs 66.5% (n=176); difference -0.19 (CI -0.36 to -0.02); p=0.030.
  - Pclass 2: 44.0% (n=168) vs 81.2% (n=16); difference -0.37 (CI -0.58 to -0.17); p=0.007.
  - Pclass 3: 23.6% (n=479) vs 50.0% (n=12); difference -0.26 (CI -0.55 to 0.02); p=0.080. This is not significant and rests on 12 Cabin-present passengers.
- **Cabin adjusted odds ratios:** the crude OR is 0.214 (95% CI 0.153 to 0.299). After adjustment for Pclass, Sex and Age missingness, it is 0.400 (95% CI 0.212 to 0.754, p=0.0046). The adjusted model assumes one common OR across classes.

![Survival rate (share survived) by Cabin present vs missing, within each Pclass](tasks/stat_6/charts/stat6_cabin_within_class.png)

![Survival rate (%) for passengers with Cabin present vs missing](tasks/eda_2/charts/eda2_cabin_missing_survival.png)

- **Age missingness (unadjusted):** survival was 29.4% when Age is missing (n=177) and 40.6% when present (n=714), chi-square p=0.008. Age missingness is related to Pclass (p=9.9e-11) but not to Sex (p=0.12).
- **Age-missing within class (Fisher p):**
  - Pclass 1: 46.7% (n=30) vs 65.6% (n=186); p=0.065.
  - Pclass 2: 36.4% (n=11) vs 48.0% (n=173); p=0.54.
  - Pclass 3: 25.0% (n=136) vs 23.9% (n=355); p=0.82.
- **Age-missing adjusted odds ratios:** the crude OR is 0.608 (95% CI 0.426 to 0.869, p=0.006). Adjusted for Pclass, Sex and Cabin missingness, it is 0.948 (95% CI 0.605 to 1.486, p=0.82). This is compatible with confounding by class and sex, but the analysis does not establish that.
- **Recording:** the finding states that Cabin missingness may reflect recording differences rather than survival. This was not tested.

### Predictive models

Split: stratified 80/20 on Survived, seed 42 (712 training rows, 179 test rows). Baseline is the majority class, 61.5% on the test set and 61.6% overall.

| Model | Test accuracy | Precision | Recall | F1 | ROC AUC |
|---|---|---|---|---|---|
| Logistic regression (standardized, 12 features) | 82.1% | 0.814 | 0.696 | 0.750 | 0.841 |
| Random forest (500 trees, 12 features) | 81.0% | 0.787 | 0.696 | 0.739 | 0.841 |

- The logistic regression 5-fold stratified CV on the training set gives accuracy 80.1% (sd 2.8 points), ROC AUC 0.854 and F1 0.730.
- The random forest reaches 98.3% training accuracy, so it overfits.
- The 1.1-point test-accuracy gap is two rows of 179. The choice of logistic regression was made on test-set results, so the held-out score is not an unbiased estimate.

**Permutation importance (logistic regression, test set, mean accuracy drop over 30 repeats):**

- Sex: 7.2 points (sd 2.0). The Sex_male and Sex_female columns are exact complements, so they have identical importance. Sex should be read as one feature.
- Age: 4.5 points (sd 1.9).
- SibSp: 4.2 points (sd 1.1).
- Pclass_1: 3.7 points (sd 0.9).
- Pclass_3: 3.1 points (sd 1.2).
- Parch: 1.1 points (sd 0.4).
- Fare: 0.6 points (sd 0.5).
- Pclass_2: 0.5 points (sd 0.5).
- Embarked_S: 0.5 points (sd 0.6). Embarked_Q: 0.3 points (sd 0.5). Embarked_C: 0.2 points (sd 0.3).

![Permutation importance of each feature for the logistic regression, measured as mean drop in test accuracy when shuffled](tasks/ml_1/charts/ml1_perm_importance.png)

The Age importance is computed on partly imputed values.

**Impurity importance (random forest):** Fare has the highest single value (0.255), followed by Age (0.247), Sex_male (0.142) and Sex_female (0.138). Fare is above each Sex column individually, but the two Sex columns together exceed Fare. The two importance methods disagree on Fare and Sex, so neither ranking is reliable.

### Does Fare add signal beyond Sex and Pclass?

Models use Pclass and Sex only, with or without Fare, on the same split (this is a different feature set from the 12-feature models above, so their scores are not directly comparable).

- **Accuracy:** 77.7% with and without Fare.
- **ROC AUC:** 0.822 without Fare, 0.820 with Fare (-0.002).
- **F1:** 0.692 without Fare, 0.697 with Fare (+0.005).
- **Fare permutation importance** (logistic regression with Fare): 0.3 points (sd 0.4).
- **Random forest on Pclass, Sex and Fare (impurity):** Fare 0.550, Sex_male 0.348, Pclass_3 0.087, Pclass_2 0.015. This forest was not scored for accuracy or AUC.
- Fare and Pclass are correlated (Spearman rho -0.688 on all 891 rows). The finding offers this as a possible explanation for the impurity–permutation disagreement, but it was not tested.

![Test accuracy, ROC AUC and F1 of logistic regression with and without Fare on the same stratified split](tasks/ml_2/charts/ml2_fare_comparison.png)

The chart's y-axis starts at 0.6, not 0, so the visual gaps look larger than the actual differences.

## Limitations

- **Age imputation:** 177 rows (19.9%) have Age median-imputed by Pclass and Sex. All Age-based results that use all rows depend on this. The imputed Age test shows no association (p=0.25), while the observed-only results are unresolved.
- **Embarked imputation:** the 2 missing Embarked rows were filled with S in all analyses that use Embarked. The Cabin–Embarked chi-square test is unreliable for this reason.
- **Overlapping unadjusted associations:** the Sex, Pclass, Fare and Embarked associations are unadjusted and overlap. Adjusted results (stat_4, stat_5, stat_6) are limited to the models they used.
- **Small cells:** Pclass 2 Age-missing (n=11), Pclass 2 Cabin-present (n=16), Pclass 3 Cabin-present (n=12) and the 60+ Age bin (n=22). The Pclass 3 Cabin-present Wald interval is unreliable, and the 60+ rate is not stable.
- **Observed-only Age subset:** the joint Sex x Pclass / Sex x Age model uses 714 rows. Age missingness is related to Pclass, so results may not generalize to the full sample.
- **Cabin:** 77.1% missing. Cabin missingness may reflect recording differences; this was not tested. The Cabin-missing adjusted OR assumes a common effect across classes, and no Pclass x Cabin-missing interaction was tested.
- **Model selection:** the logistic regression was chosen on test-set results, and the accuracy gap to the random forest is within noise. The ml_2 models use a different feature set from ml_1 and were scored on one split only.
- **Multiplicity and the Age test family:**
  - In the 8-test family, the observed-only Welch test replaces the imputed Mann-Whitney test in the Age slot, so the test types differ across slots. Under this family, its Holm-adjusted p is 0.041, which is significant at 0.05.
  - If the imputed-Age Mann-Whitney test is kept as a ninth test, the Holm-adjusted p for the observed-only Welch test is 0.082, which is not significant.
  - The Age result therefore depends on how the family is defined.
- **Pclass 3 p-value in the joint model:** the male x Pclass 3 p-value (0.022) is uncorrected for the other coefficients.

**Unresolved review issues (stated against the affected findings):**

- **Age association (stat_1, stat_3):** the Age result is unresolved, not a confirmed null. The rank test is reported as non-significant (p=0.16) with a negligible rank-biserial. The rank-based and median comparisons are likewise non-significant, not established as null.
- **Impurity importance (ml_1):** the statement that impurity importance places Fare above Sex is incorrect when Sex is read as one feature. Fare is above each Sex column, but the two Sex columns combined exceed Fare. The combined value is not given here because it is a sum that no finding reports.
- **Permutation importance (ml_1):** Fare is not "near the bottom" of the ranking. Its value (0.6 points) is above Pclass_2, Embarked_S, Embarked_Q and Embarked_C. The equal Sex_male and Sex_female values reflect the symmetric, complementary encoding of the two columns, not a separate finding about shuffling.
- **Verification of Fare, Pclass_2 and Embarked importances (ml_1):** the review flagged these as unverifiable from the visible facts. The values reported above are taken from the ml1_perm_importance record.
- **Test-set bias in model selection (ml_1):** the choice of logistic regression was made on test-set results.

**Failed tasks:** none. All eight tasks (eda_1, stat_1 to stat_6, eda_2, ml_1, ml_2) are complete.

## Open questions

- Does the observed-only Age gap (-2.28 years) hold after adjusting for Sex and Pclass in a multivariable model?
- Is the observed-only Age gap driven by a few older or very young passengers? Winsorised mean, Yuen test, or a cut-off comparison were not run.
- Does the observed-only Age association hold within passenger class and sex?
- Does the Sex x Age slope hold when Age is imputed for the 177 missing rows?
- Is the 60+ Age-bin rate (22.7%, n=22) reliable given its size?
- Does Fare add signal within Pclass strata, or after a log transform of its skew? Do repeated splits or repeated CV give a stable accuracy, AUC and F1 difference with and without Fare?
- Does the random forest's Fare dominance persist when it is scored for accuracy and AUC on the same test set? Does removing Pclass change the gap between impurity and permutation importance?
- Do FamilySize or IsAlone add predictive signal beyond Sex, Pclass and Fare? Does FamilySize or Parch add signal beyond the 12-feature set?
- Does repeated or nested cross-validation change the logistic regression versus random forest comparison?
- Is the Pclass 3 female effect driven by a specific subgroup, such as Embarked or FamilySize?
- Does the Embarked association hold within Pclass, and is the Cherbourg class mix the explanation? The adjusted analysis shows the port effect persists after adjusting for Pclass and Fare, but it does not show whether the Cherbourg class mix explains the unadjusted difference.
- Should Pclass x Cabin-missing and Pclass x Age-missing interaction terms be tested in the logit?
- Is Cabin recording systematically different (fare, embarkation port, ticket class) between Cabin-present and Cabin-missing passengers within class?
- Are the two missing Embarked rows correct in the source data?
- Is there a fixed multiplicity family for the Age tests (8-slot substitution or 9-test inclusive)?