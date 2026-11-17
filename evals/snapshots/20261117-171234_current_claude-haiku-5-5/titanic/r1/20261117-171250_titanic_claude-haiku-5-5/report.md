# Survival on the Titanic Passenger Data: Predictors of Survived

## Summary

- **Sex is the strongest single predictor.** Female passengers survived at 74.2% (n=314) versus 18.9% for male passengers (n=577). The chi-square test gives p=3.7e-59, with Cramér's V=0.543 (95% bootstrap CI 0.485 to 0.600).
- **Pclass and Fare also differ significantly, and the Sex effect depends on class.** Survival falls from 63.0% in class 1 to 24.2% in class 3 (Cramér's V=0.340). Female survival in class 3 is 50.0%, against 96.8% in class 1 and 92.1% in class 2. The Pclass × Sex interaction is significant (LR chi2=28.79, dof 2, p=5.6e-7).
- **Age is not a significant overall predictor.** The Mann-Whitney test gives p=0.160. Children aged 0-12 survived at 58.0% (n=69), but this advantage is not consistent across classes and sexes (see the child findings below).
- **On one stratified split, logistic regression outperforms the majority-class baseline.** Test accuracy is 0.7982 against 0.6143, and test ROC AUC is 0.8417 against 0.5. The random forest scored lower (test accuracy 0.7623, AUC 0.8284). This is a single 223-row test split, so the advantage of logistic regression over the random forest is not established as general.

## Data

- **Size:** 891 rows × 12 columns.
- **Target:** Survived (binary). 61.6% of passengers are 0 (did not survive) and 38.4% are 1 (survived).
- **Features analysed:** Sex and Embarked (categorical); Pclass, Age, SibSp, Parch and Fare (numeric). PassengerId, Ticket, Cabin and Name were not used as features as they stand.
- **Missing values:**
  - Cabin: 77.1% of rows (687 of 891)
  - Age: 19.9% of rows (177 of 891)
  - Embarked: 0.2% of rows (2 of 891)
  - Survived, Pclass, Sex and Fare have no missing values.

## Findings

### Survival rates by group

Survival rates across Sex, Pclass, Embarked, SibSp, Parch, binned Age and Fare quartile were compared with the 38.4% base rate.

- **Sex:** female 74.2% (n=314); male 18.9% (n=577).
- **Pclass:** class 1 63.0% (n=216); class 2 47.3% (n=184); class 3 24.2% (n=491).
- **Embarked:** C 55.4% (n=168); Q 39.0% (n=77); S 33.7% (n=644). The two passengers with missing Embarked are excluded from these rows.
- **SibSp:** 0 at 34.5% (n=608); 1 at 53.6% (n=209); 2 at 46.4% (n=28); 3 at 25.0% (n=16); 4 at 16.7% (n=18); 5 at 0.0% (n=5); 8 at 0.0% (n=7). Groups of 3 or more are too small to read reliably, and the pattern is non-monotonic.
- **Parch:** 0 at 34.4% (n=678); 1 at 55.1% (n=118); 2 at 50.0% (n=80). Parch 3 to 6 each have 5 or fewer passengers and are not reliable.
- **Fare quartiles:** Q1 (lowest) 19.7% (n=223); Q2 30.4% (n=224); Q3 45.5% (n=222); Q4 (highest) 58.1% (n=222). The mean fare rises from 7.03 in Q1 to 88.68 in Q4.
- **Age bands:** 0-12 at 58.0% (n=69); 13-18 at 42.9% (n=70); 19-35 at 38.3% (n=358); 36-60 at 40.0% (n=195); 61+ at 22.7% (n=22). Age-missing passengers (n=177) are excluded from the bands. The 61+ group is small.

![Survival rate (share surviving) by Sex, Pclass, Embarked, binned Age and Fare quartile; dashed red line = overall base rate 38.4%](tasks/eda_1/charts/eda1_survival_by_groups.png)

### Statistical significance and effect sizes

Seven feature-level tests were run, with Holm correction across the seven. Chi-square tests use uncorrected Pearson statistics with Cramér's V. Mann-Whitney tests use rank-biserial effects. Each effect-size CI is a percentile bootstrap with 1000 resamples.

- **Sex:** chi2=263.05, p=3.7e-59 (Holm-significant); Cramér's V=0.543 (95% CI 0.485 to 0.600).
- **Pclass:** chi2=102.9, dof 2, p=4.5e-23 (Holm-significant); Cramér's V=0.340 (95% CI 0.281 to 0.403).
- **Embarked:** chi2=26.5, dof 2, p=1.8e-6 (Holm-significant); Cramér's V=0.173 (95% CI 0.106 to 0.244). The effect is small. The C-versus-S gap may reflect class and fare mix, which was not tested.
- **SibSp:** in the original 14-cell table, chi2=37.3, dof 6, p=1.6e-6 (Holm-significant); Cramér's V=0.205 (95% CI 0.158 to 0.269). Four of 14 cells have expected counts below 5 (minimum 1.92), so this p-value is indicative only. With levels collapsed to 0, 1, 2+ (no cell below 5), chi2=28.3, dof 2, p=7.3e-7, Cramér's V=0.178. This collapsed test is a sensitivity check, is not Holm-adjusted, and has no CI. Survival in the collapsed 2+ group is 27.0% (n=74).
- **Parch:** in the original 14-cell table, chi2=27.9, dof 6, p=9.7e-5 (Holm-significant); Cramér's V=0.177 (95% CI 0.131 to 0.249). Eight of 14 cells have expected counts below 5 (minimum 0.38), so this p-value is indicative only. With levels collapsed to 0, 1, 2+, chi2=21.1, dof 2, p=2.7e-5, Cramér's V=0.154. This is a sensitivity check, not Holm-adjusted, with no CI. Survival in the collapsed 2+ group is 46.3% (n=95).
- **Fare:** Mann-Whitney p=4.6e-22 (Holm-significant); rank-biserial=0.384 (95% CI 0.317 to 0.450), n=891. The median fare is 26.0 for survivors and 10.5 for non-survivors.
- **Age:** Mann-Whitney p=0.160 (not Holm-significant); rank-biserial=-0.062 (95% CI -0.148 to 0.028), on the 714 passengers with Age recorded.

The Fare quartile rates above are descriptive and were not produced by the Mann-Whitney test.

![Survival rate (share surviving) by Sex, Pclass and Embarked; dashed red line = overall base rate 38.4%](tasks/stat_1/charts/stat1_survival_rates_categorical.png)

### Sex and Pclass interaction

The effect of Sex differs across classes, and the Pclass effect differs by sex.

- **Female-minus-male survival gap:** 59.9 points in class 1 (95% Wald CI 50.7 to 69.2); 76.4 points in class 2 (CI 67.2 to 85.5); 36.5 points in class 3 (CI 27.5 to 45.4).
- **Rates by Pclass and Sex:** female class 1 96.8% (n=94), class 2 92.1% (n=76), class 3 50.0% (n=144); male class 1 36.9% (n=122), class 2 15.7% (n=108), class 3 13.5% (n=347).
- **Interaction test:** LR chi2=28.79, dof 2, p=5.6e-7. The class 3 interaction term is 2.10 on the log-odds scale (p=0.0014). The class 2 term is -0.19 (p=0.82), so the class 1 and class 2 gaps are not clearly different. The meaningful contrast is class 3 against classes 1 and 2.

![Survival rate by Pclass for female and male passengers](tasks/stat_2/charts/stat2_survival_by_pclass_sex.png)

### Missing values and survival

- **Missingness counts:** Cabin 687 (77.10%), Age 177 (19.87%), Embarked 2 (0.22%).
- **Age missing:** survival 29.4% (n=177) versus 40.6% (n=714) with Age present. A Fisher test on the overall gap gives p=0.006. Of Age-missing rows, 76.8% are Pclass 3, compared with 49.7% of Age-complete rows. Age-missing rows also have a lower median fare (8.05 versus 15.74).
- **Age missing, within strata (Fisher p):** Pclass 1 p=0.065 (missing 46.7% n=30 versus present 65.6% n=186); Pclass 2 p=0.543 (missing 36.4% n=11 versus present 48.0% n=173); Pclass 3 p=0.815 (missing 25.0% n=136 versus present 23.9% n=355); male p=0.069; female p=0.301. None is below 0.05.
- **Cabin missing:** survival 30.0% (n=687) versus 66.7% (n=204) with Cabin present. Fisher p=1.1e-20 overall. Within sex, male p=3.3e-10 (missing 13.6% n=470 versus present 42.1% n=107) and female p=1.2e-08 (missing 65.4% n=217 versus present 93.8% n=97).
- **Cabin missing, within Pclass (Fisher p):** Pclass 1 p=0.030 (missing 47.5% n=40 versus present 66.5% n=176); Pclass 2 p=0.007 (missing 44.0% n=168 versus present 81.3% n=16); Pclass 3 p=0.080 (missing 23.6% n=479 versus present 50.0% n=12).
- **Embarked missing:** two rows (PassengerId 62 and 830). Both are Pclass 1, both have Fare 80.0, and both survived. Their port cannot be inferred from the data. Survival was not analysed by Embarked for these rows.

The Age-missing overall gap is not significant within any single class or sex. The Cabin-missing gap is significant overall and within each sex. Within Pclass, it is significant in classes 1 and 2 but not in class 3. Whether class composition explains the overall Age-missing gap was not formally tested.

![Survival rate for rows with Age or Cabin present vs missing](tasks/eda_2/charts/survival_by_missingness.png)

![Survival rate within Pclass and Sex by Age-missing and Cabin-missing status](tasks/eda_4/charts/eda4_within_group_survival.png)

### Child survival advantage

- **Overall:** children aged 0-12 survived at 58.0% (n=69) versus 38.8% (n=645) for older passengers, among the 714 with Age recorded. This comparison does not adjust for class mix.
- **By Pclass:**
  - Class 1: children 75.0% (n=4) versus older 65.4% (n=182). The child group is too small to read.
  - Class 2: children 100% (n=17) versus older 42.3% (n=156).
  - Class 3: children 41.7% (n=48) versus older 21.2% (n=307).
- **By Sex:** male children 56.8% (n=37) versus older men 17.3% (n=416); female children 59.4% (n=32) versus older women 77.7% (n=229). The advantage is large among males and absent among females.
- **Sex within Pclass:**
  - Males: class 1 children 100% (n=3) versus older 37.8% (n=98); class 2 children 100% (n=9) versus older 6.7% (n=90); class 3 children 36.0% (n=25) versus older 12.7% (n=228).
  - Females: class 1 children 0.0% (n=1) versus older 97.6% (n=84); class 2 children 100% (n=8) versus older 90.9% (n=66); class 3 children 47.8% (n=23) versus older 45.6% (n=79).
- **Caveat:** 9 of the 17 class 2 children are male, and the class 2 child group is small. The male child advantage was not tested with a model that adjusts for Pclass.

![Survival rate of children 0-12 vs older passengers within each Pclass and each Sex; dashed red line = base rate 38.4%](tasks/eda_3/charts/eda3_child_survival_by_group.png)

### Predictive models

All three models used one stratified split (test_size 0.25, random_state 42; n_train 668, n_test 223). Age was imputed with the median of Pclass and Sex groups, then the overall Age median for any remaining gaps. Embarked was filled with its mode. Sex and Embarked were one-hot encoded. Name, Ticket, Cabin and PassengerId were excluded. Standardisation was applied only for logistic regression.

| Model | Train accuracy | Test accuracy | Test precision | Test recall | Test F1 | Test ROC AUC |
|---|---|---|---|---|---|---|
| Majority-class baseline | 0.6168 | 0.6143 | 0.0 | 0.0 | 0.0 | 0.5 |
| Logistic regression | 0.8099 | 0.7982 | 0.7531 | 0.7093 | 0.7305 | 0.8417 |
| Random forest (300 trees) | 0.982 | 0.7623 | 0.726 | 0.6163 | 0.6667 | 0.8284 |

- Logistic regression has the highest test accuracy and AUC on this split: test accuracy 0.7982 against 0.7623 for the random forest, and test ROC AUC 0.8417 against 0.8284. Both comparisons rest on one 223-row test set.
- The random forest's train accuracy of 0.982 against test accuracy 0.7623 indicates overfitting relative to its test score.
- **Feature importance differs by model:**
  - Logistic regression (absolute standardised coefficients): Pclass 1.0194; Sex_female and Sex_male 0.6286 each; Age 0.5991; SibSp 0.2763; Fare 0.1205; Embarked dummies 0.04 to 0.09; Parch 0.0323. Only magnitudes are recorded, not signs.
  - Random forest (impurity importance): Fare 0.2545; Age 0.2463; Sex_male 0.1542; Sex_female 0.1365; Pclass 0.0859; SibSp 0.0475; Parch 0.0396; Embarked dummies 0.0069 to 0.0158.
- The two models disagree on the leading feature: logistic regression ranks Pclass first, and the random forest ranks Fare first. The ranking therefore depends on the model.

![Test accuracy and test ROC AUC for the majority-class baseline, logistic regression and random forest on the same split (n_test=223)](tasks/ml_1/charts/ml1_model_comparison.png)

## Limitations

- **Unresolved review issue (eda_4):** the report does not give the full brief table. The lead's objection still stands and affects the within-Pclass and within-Sex missingness findings. Survival and n for Age missing versus present, and for Cabin missing versus present, are given above for all Pclass levels and both sexes from the stored tables. The lead has asked that every cell be checked against the exact n in eda4_survival_table and that small cells be flagged. The Pclass 2 Age-missing cell (n=11) and the Pclass 3 Cabin-present cell (n=12) are too small to read reliably, and their rates and p-values should not be interpreted.
- **eda_4 status is partial.** Its within-group analysis is incomplete, and the Age and Cabin tests within Pclass were not adjusted for each other or for Fare.
- **Missing values and tests:** Age-missing and Cabin-missing survival gaps were reported descriptively in eda_2 without significance tests. The eda_4 Fisher tests use the same comparisons and are the only significance results for these gaps. The overall Age-missing gap may reflect class composition; this was not formally tested. The Cabin-missing gap is also confounded with Pclass.
- **SibSp and Parch:** both chi-square tests have sparse cells. Their original p-values are indicative only. Collapsed sensitivity checks are not Holm-adjusted and have no CI.
- **Embarked:** the C-versus-S difference is a descriptive and significant association with a small effect size. Its relation to class and fare was not tested.
- **Small groups:** the child 0-12 Pclass 1 group (n=4), the female class 1 child group (n=1) and the male class 1 child group (n=3) are too small to support conclusions. The 61+ Age band has n=22, and the Parch 3 to 6 and SibSp 5 and 8 groups each have 5 or fewer passengers.
- **Age imputation:** models used Age imputed from Pclass and Sex medians. Imputation by title was not tested, so the effect of this choice on model results is unknown.
- **Model evaluation:** all model scores come from one 223-row test split. No repeated splits or cross-validation were run. The stated advantage of logistic regression over the random forest is therefore not established as general.
- **Multiple comparisons:** Holm correction was applied across the seven feature-level tests only. The effect-size CIs are bootstrap percentile intervals with 1000 resamples.
- **Causal claims:** none of the associations here were tested for causal effects.

## Open questions

- Do Sex and Pclass together explain the Fare and Embarked effects, or does Fare add information once class and sex are controlled?
- Does the Embarked difference (C above S) survive adjustment for class and fare?
- Is the SibSp 1 and Parch 1 advantage robust once class and sex are adjusted for? Are the SibSp and Parch associations real or an artefact of small groups?
- Does the child advantage hold within each class and sex after a model adjusts for Pclass, Sex and Age group?
- Why do older females survive at a higher rate than children of either sex in the same class? Is this a mix effect of Pclass within the female group?
- Is the class 2 child result (100%, n=17) reliable, or does it depend on a few families?
- Does the Sex × Pclass interaction hold after adjusting for Age, Fare, Embarked and family size? Is the female class 3 survival rate (50.0%) driven by Embarked or Fare mix within class 3?
- Do the rate-difference CIs hold up under a bootstrap or an exact method, given the small cells?
- Does Age imputation by Pclass and Sex, or by a title extracted from Name, change model results compared with dropping Age-missing rows?
- Do repeated stratified splits or cross-validation confirm that logistic regression beats the random forest?
- Is the Cabin deck predictive of survival once Pclass is controlled for? Is the Cabin-missing gap explained by Pclass and Fare, or does missing Cabin carry independent information?
- Does Age-missing carry independent information about survival after controlling for Pclass, Sex and Fare?
- Do the Age-missing and Cabin-missing survival gaps persist within each Pclass, and are they significant after adjustment?