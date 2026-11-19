# Titanic Survival Analysis: Drivers of Survival in the Titanic Passenger Data (Target: Survived)

## Summary

- **Sex was the strongest marginal association with survival.** 74.2% of 314 females survived against 18.9% of 577 males (chi-square = 263.05, p < 0.001, Cramér's V = 0.543). Passenger class, fare and embarkation port were also significantly associated with survival, though the port effect is weak.
- **The Sex effect differs by passenger class.** The interaction is significant (likelihood-ratio test, LR = 24.08 on 1 df, p < 0.001). Female survival is 96.8%, 92.1% and 50.0% in Pclasses 1, 2 and 3, against male survival of 36.9%, 15.7% and 13.5%.
- **A logistic regression beats the majority-class baseline clearly.** On the 223-row test split, the majority-class accuracy is 0.614 and logistic regression reaches 0.830 accuracy with ROC AUC 0.877. A random forest reaches 0.825 accuracy and ROC AUC 0.851, and overfits (training accuracy 0.909). The strongest logistic regression coefficients are Pclass, Sex and the Master title.
- **Some associations are partly explained by other variables, and some are not.** Embarked survival differences shrink but persist after standardizing for Pclass. The Cabin-missing survival gap of 37 points persists within every Pclass and Sex stratum, at 19 to 37 points. Cabin missingness is itself linked to class composition.

## Data

- **Size:** 891 rows, 12 columns.
- **Target:** Survived, binary. 549 passengers died (61.6%) and 342 survived (38.4%), so the classes are moderately imbalanced.
- **Features used:** Pclass, Age, SibSp, Parch, Fare (numeric); Sex, Embarked (categorical). The models also used a derived FamilySize and title indicators (Master, Miss, Mr, Mrs, Rare).
- **Excluded as features:** PassengerId, Ticket, Cabin and Name, as identifiers or free text. Cabin was used only in the missingness analysis.
- **Missing values:** Cabin 77.1% (687 rows), Age 19.9% (177 rows), Embarked 0.2% (2 rows).
- **Dates/time:** none.

## Findings

### Overall survival and single-feature patterns

Survival rates by group, from the exploratory analysis:

- **Sex:** 74.2% of 314 females survived, against 18.9% of 577 males.
- **Passenger class:** 63.0% in Pclass 1 (n=216), 47.3% in Pclass 2 (n=184), 24.2% in Pclass 3 (n=491).
- **Embarked:** 55.4% for port C (n=168), 39.0% for Q (n=77), 33.7% for S (n=644).
- **Fare quartiles:** 19.7% (up to 7.91, n=223), 30.4% (7.91 to 14.454, n=224), 45.5% (14.454 to 31.0, n=222), 58.1% (31.0 to 512.329, n=222). The rate rises across all four quartiles.
- **Age quartiles:** 45.8% (0.419 to 20.125, n=179), 36.1% (20.125 to 28.0, n=183), 43.4% (28.0 to 38.0, n=175), 37.3% (38.0 to 80.0, n=177). The pattern is non-monotone: the 20 to 28 bin is lowest. This is descriptive only. No effect-size comparison with Sex or Pclass was run, so the relative strength of Age is not established.

Mean fare was 84.15 in Pclass 1, 20.66 in Pclass 2 and 13.68 in Pclass 3. Mean fare was 44.48 for women and 25.52 for men.

![Survival rate (share of passengers who survived) by Sex (left) and by Passenger class (right)](tasks/eda_1/charts/survival_rate_sex_pclass.png)

Tests of each feature against Survived. All associations are unadjusted and tested one feature at a time. Sex, Pclass, Fare and Embarked are correlated with each other, so their individual effects are not independent.

- **Sex:** chi-square = 263.05, p < 0.001, Cramér's V = 0.543. Female minus male survival difference is 0.553 (95% CI 0.495 to 0.611).
- **Pclass:** chi-square = 102.89, p < 0.001, Cramér's V = 0.340. Class 1 minus class 3 difference is 0.387 (95% CI 0.313 to 0.462).
- **Fare:** Mann-Whitney p < 0.001, rank-biserial r = 0.384. Passengers paying above 14.454 survived 26.0 points more often than those paying 14.454 or less (95% CI 0.198 to 0.321). Median fare was 26.0 for survivors and 10.5 for those who died.
- **Embarked:** chi-square = 26.49 on n = 889, p < 0.001, Cramér's V = 0.173 (weak). The pairwise port C minus port S difference is 0.217 (95% CI 0.133 to 0.300).
- **FamilySize:** Mann-Whitney p < 0.001, rank-biserial r = 0.173 (small). Passengers travelling with family survived 20.2 points more often than those alone (95% CI 0.137 to 0.267). Median family size was 2 for survivors and 1 for those who died.
- **Age:** at the 28-year median split, no significant difference (Mann-Whitney p = 0.160, rank-biserial r = -0.062, n = 714). The over-28 minus 28-and-under difference is -0.005 (95% CI -0.077 to 0.067).

The age result and the quartile pattern above are different analyses and do not fully agree. The quartile pattern shows variation across bins, while the single median split shows no significant difference. Neither establishes the size or direction of an Age effect alone.

![Difference in survival rate between the main groups of each feature, with 95% Wald confidence intervals. Positive values mean the first group survived more often.](tasks/stat_1/charts/stat1_rate_differences.png)

### Sex by Pclass interaction

The effect of Sex differs by class. The likelihood-ratio test of the full logit against the additive model gives LR = 24.08 on 1 df, p < 0.001. The Wald p-value for the female:Pclass term is 2.2e-05 (coefficient -1.36 on the log-odds scale).

Survival by Sex and Pclass cell:

| Cell | Survived / n | Rate |
|---|---|---|
| Female, Pclass 1 | 91 / 94 | 96.8% |
| Female, Pclass 2 | 70 / 76 | 92.1% |
| Female, Pclass 3 | 72 / 144 | 50.0% |
| Male, Pclass 1 | 45 / 122 | 36.9% |
| Male, Pclass 2 | 17 / 108 | 15.7% |
| Male, Pclass 3 | 47 / 347 | 13.5% |

The female-minus-male gap is 59.9 points in Pclass 1, 76.4 points in Pclass 2 and 36.5 points in Pclass 3. It is widest in Pclass 2 and narrowest in Pclass 3.

![Survival rate by Sex within each Pclass](tasks/stat_2/charts/survival_rate_sex_pclass_interaction.png)

### Embarkation port and composition

Port composition differs. Port C passengers are 50.6% Pclass 1 and 43.5% female. Port S passengers are 19.7% Pclass 1 and 31.5% female. Port Q passengers are 93.5% Pclass 3 and 46.8% female.

- **Standardized to the overall Pclass mix,** survival is 48.6% for C, 46.6% for Q and 34.1% for S. The gap shrinks but does not disappear. The standardization weights are the Pclass shares of each port's passengers, not the overall Pclass mix.
- **Within each class,** C has higher survival than S in every class: Pclass 1 69.4% vs 58.3%, Pclass 2 52.9% vs 46.3%, Pclass 3 37.9% vs 19.0%.
- **Port Q** has an adjusted rate above its raw 39.0%. Its Pclass 1 (n=2) and Pclass 2 (n=3) cells are too small to interpret. Within Pclass 3, Q survives at 37.5% (n=72) against S at 19.0% (n=353).

![Survival rate by Embarked port within each Passenger class (share survived)](tasks/eda_3/charts/embarked_survival_within_pclass.png)

### Age and composition

Pclass mix changes across the Age quartile bins. Pclass 1 share is 11.7% in the youngest bin, rising to 16.9%, 27.4% and 48.6% in the oldest. Pclass 3 share falls from 68.7% to 28.8%. Female share is 43.0% in the youngest bin and between 33.9% and 34.9% in the other three.

Survival within each Pclass by Age bin:

- **Pclass 1:** 81.0%, 74.2%, 75.0%, 53.5%.
- **Pclass 2:** 74.3%, 40.4%, 43.1%, 40.0%.
- **Pclass 3:** 31.7%, 22.9%, 23.7%, 7.8%.

Cell counts for the Pclass 2 youngest and 20 to 28 bins were not reported. The Pclass 2 values should be treated as small until counts are given. The 20 to 28 dip is much smaller in Pclass 1 than in Pclass 2, and it is not absent there.

Survival within each Sex by Age bin:

- **Males:** 28.4%, 15.8%, 21.9%, 17.1%.
- **Females:** 68.8%, 74.6%, 83.6%, 76.7%.

The dip in the 20 to 28 bin holds for males. Female survival rises across the first three bins. The Age pattern is therefore not the same within each Sex. The finding cannot establish that Sex composition does not explain the Age pattern.

### Missingness

- **Age:** passengers with Age missing survived at 29.4% (n=177), against 40.6% for those with Age present (n=714). No test is reported.
- **Cabin:** passengers with Cabin missing survived at 30.0% (n=687), against 66.7% for those with Cabin present (n=204).

![Survival rate for passengers with Cabin missing vs present](tasks/eda_2/charts/cabin_missing_survival.png)

Cabin missingness tracks class. 86.3% of Cabin-present passengers are Pclass 1 (176 of 204). 69.7% of Cabin-missing passengers are Pclass 3 (479 of 687), and 5.8% are Pclass 1 (40 of 687). Cabin missingness also differs by Sex: 31.6% of Cabin-missing passengers are female, against 47.5% of Cabin-present passengers.

Cabin-missing survival compared with Cabin-present survival, within each stratum (unadjusted):

- **Pclass 1:** 47.5% (n=40) vs 66.5% (n=176).
- **Pclass 2:** 44.0% (n=168) vs 81.3% (n=16). The Cabin-present group is small.
- **Pclass 3:** 23.6% (n=479) vs 50.0% (n=12). The Cabin-present group is small.
- **Female:** 65.4% (n=217) vs 93.8% (n=97).
- **Male:** 13.6% (n=470) vs 42.1% (n=107).

All five within-stratum gaps are negative, between -19 and -37 points. The gap is therefore present in every stratum. Pclass 1 (-19 points) is the only stratum where it is clearly smaller than the marginal 37 points. These within-stratum figures are unadjusted, and the Pclass 2 and 3 Cabin-present estimates rest on very few passengers. The size of the composition effect can only be bounded, not measured precisely.

Only two passengers lack Embarked: IDs 62 and 830. Both are Pclass 1 females who survived, with Fare 80.0. Passenger 62 has Cabin B28, and passenger 830 also has Cabin B28.

![Survival rate for Cabin present vs missing within each Pclass and within each Sex (rates, unadjusted within-stratum)](tasks/eda_4/charts/eda4_strata_survival.png)

### Predictive models

Evaluation used a stratified 75/25 split: 668 training rows and 223 test rows. Age median (29.0) and Embarked mode (S) were fitted on training rows only.

| Model | Test accuracy | ROC AUC | F1 | Train accuracy |
|---|---|---|---|---|
| Majority-class baseline | 0.614 | – | – | – |
| Logistic regression | 0.830 | 0.877 | 0.774 | 0.829 |
| Random forest | 0.825 | 0.851 | 0.752 | 0.909 |

Logistic regression ranks passengers slightly better on this split. With 223 test rows, the two models should be treated as roughly comparable.

Refitting the imputation on the full dataset before splitting gave a random forest test accuracy of 0.834, ROC AUC 0.854 and F1 0.764. Logistic regression gave 0.830, 0.877 and 0.774. The earlier full-data figures may be slightly optimistic.

Feature importance:

- **Logistic regression** (standardized coefficients, absolute value): Pclass 0.874, Sex 0.627 for each level, Title_Master 0.509, Age 0.377, SibSp 0.305, FamilySize 0.242, Fare 0.178. Title_Master is associated with children, but its coefficient does not show that it carries age information beyond the Age variable.
- **Random forest** (impurity importance, training-only fit): Fare 0.187, Age 0.144, Title_Mr 0.137, Sex_male 0.128, Sex_female 0.107, Pclass 0.087. These are separate values and do not show that Sex and title together account for most of the signal.

The chart below comes from the full-data random forest fit, not the training-only fit whose values are quoted above. Its values differ slightly (for example, Fare 0.186 and Pclass 0.088).

![Random forest impurity-based feature importance on the training fit, top 10 features](tasks/ml_1/charts/ml1_rf_importance.png)

## Limitations

- **Marginal tests only.** The feature tests in the Findings are unadjusted and one at a time. Sex, Pclass, Fare and Embarked are correlated, so their individual effects are not independent.
- **Embarked and Age effects are not adjusted jointly.** A logistic model with Pclass, Sex, Embarked and Age together was proposed but not fitted. Those effects are only partly separated by the stratified and standardized figures above.
- **Small cells.** Port Q's Pclass 1 and 2 cells (n=2 and n=3), the Pclass 2 Age bins with unreported counts, and the Pclass 2 and 3 Cabin-present groups (n=16 and n=12) are too small for firm conclusions.
- **Age findings do not agree.** The quartile pattern and the non-significant median split are separate analyses and are reported as such. The team did not establish a strong or clear Age effect.
- **Age-by-Sex claim not established (unresolved review issue).** The 20 to 28 dip holds for males only. Female survival rises across the first three bins. The claim that Sex composition does not explain the Age pattern is not supported.
- **Pclass 1 Age pattern (unresolved review issue).** Pclass 1 survival falls from 81.0% to 74.2% in the 20 to 28 bin. The dip is much smaller in Pclass 1 than in Pclass 2, not absent.
- **Standardization weights (unresolved review issue).** The weights used for the Embarked standardization are the Pclass shares of each port's passengers, not the overall Pclass mix.
- **Age-bin Pclass and Sex percentages (unresolved review issue).** The percentages in the Age-bin composition finding could not be verified against the source facts.
- **Random forest importance source (unresolved review issue).** The importance values quoted above come from the training-only fit. The chart comes from the full-data fit, which gives slightly different values. The two should not be combined.
- **Overfitting.** The random forest has training accuracy 0.909 and test accuracy 0.825. Logistic regression shows almost no gap. Tuning was not run.
- **Small test set.** The 223-row test split means differences of a few points between models are not reliable.
- **Missingness tests.** No test is reported for the Age-missing survival gap (29.4% vs 40.6%). The Cabin-missing gaps are descriptive and unadjusted.
- **Imputation.** Full-data imputation may slightly inflate scores. Training-only imputation is used for the primary results.
- **Failed tasks.** None reported.

**Numbers not traced to a recorded fact.** The automatic check found no recorded value for these numbers:
- 86.3% in: "Cabin missingness tracks class. 86.3% of Cabin-present passengers are Pclass 1 (176 of 204). 69.7% of Cabin-missing passengers are Pclass 3 (479 of 687), and 5."
- 69.7% in: "Cabin missingness tracks class. 86.3% of Cabin-present passengers are Pclass 1 (176 of 204). 69.7% of Cabin-missing passengers are Pclass 3 (479 of 687), and 5."
- 5.8% in: "Cabin missingness tracks class. 86.3% of Cabin-present passengers are Pclass 1 (176 of 204). 69.7% of Cabin-missing passengers are Pclass 3 (479 of 687), and 5."
- 31.6% in: "Cabin missingness tracks class. 86.3% of Cabin-present passengers are Pclass 1 (176 of 204). 69.7% of Cabin-missing passengers are Pclass 3 (479 of 687), and 5."

## Open questions

- Does the Sex effect hold within each passenger class once the variables are modelled jointly? The interaction results show that the gap differs by class, but they do not answer this.
- Is the low survival in the 20 to 28 Age bin explained by Sex or Pclass composition? The Sex-specific pattern and the Pclass 2 pattern do not give a clear answer.
- Does the Embarked C advantage survive joint adjustment for Pclass, Sex, Age and fare?
- Why does port Q keep an advantage in Pclass 3 (37.5% vs 19.0% for S)? Fare, cabin and ticket information were not analysed.
- Does the Cabin-missing survival gap remain after adjusting for Pclass, Sex and Age together? Is it driven by fare or ticket group rather than class?
- Does Cabin deck letter carry survival information beyond the missing-versus-present split?
- Do the Fare and Age effects in the models hold after removing the title features, since titles partly encode Sex and Age?
- Is the logistic regression advantage in ROC AUC stable under repeated stratified cross-validation?
- Does the random forest improve with tuning (depth or minimum samples per leaf) to reduce its train-test gap?
- Is the low survival of Pclass 2 males (15.7%) the main reason the Pclass 2 Sex gap is the widest?