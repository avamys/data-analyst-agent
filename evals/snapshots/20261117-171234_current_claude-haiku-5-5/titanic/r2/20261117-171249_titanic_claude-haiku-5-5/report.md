# Titanic Passenger Survival: Final Report on the Survived Target

## Summary

- **Sex was the strongest split.** Females survived at 74.2% (n=314) against 18.9% for males (n=577). In a logistic regression adjusted for Pclass, female odds of survival were 14.06 times male odds (95% CI 9.81 to 20.16).
- **Pclass and Fare were also significantly associated with survival.** Survival fell from 63.0% in Pclass 1 to 24.2% in Pclass 3. Each step up in class multiplied the adjusted odds of survival by 0.38. Fare rose across quartiles from 19.7% to 58.1%. Fare is correlated with Pclass, so its association may partly reflect class; this has not been adjusted for.
- **The Sex effect depends on class.** The Sex × Pclass interaction is significant (LR = 24.08, p = 9.3e-07). The interaction is concentrated in third class: women's survival is 50.0% there, against 92% to 97% in classes 1 and 2.
- **Both predictive models beat the majority-class baseline.** The baseline accuracy is 61.45%. Logistic regression reaches 80.45% accuracy and ROC AUC 0.844. Random forest reaches 81.56% accuracy and ROC AUC 0.832, but it is overfitted (train accuracy 0.983). The two models are roughly equivalent on the 179-row test set.
- **Age was not significantly associated with survival after correction.** Missing Age (177 rows) was imputed with medians, so all Age-based results depend on those imputed values.

## Data

- **Size:** 891 rows × 12 columns.
- **Target:** Survived (binary). 61.6% of passengers are class 0 (did not survive) and 38.4% are class 1 (survived). The survivor count is 342.
- **Features used:** Pclass, Age, SibSp, Parch, Fare (numeric); Sex, Embarked (categorical). PassengerId, Ticket, Cabin and Name were not used as features as they stand. FamilySize was derived for the models.
- **Missing values:**
  - Cabin: 77.1% (687 of 891)
  - Age: 19.9% (177 of 891)
  - Embarked: 0.2% (2 of 891)
- **No date or time features.**

## Findings

### Overall survival and descriptive rates

The overall survival rate is 38.38% (342 of 891).

**By Sex:** Females survived at 74.2% (n=314) and males at 18.9% (n=577).

**By Pclass:** Survival was 63.0% in class 1 (n=216), 47.3% in class 2 (n=184) and 24.2% in class 3 (n=491).

**By Embarked:** Survival was 55.4% for C (n=168), 39.0% for Q (n=77) and 33.9% for S (n=646). The 2 missing Embarked values were filled with S, so the S count includes them. Embarked is associated with Pclass and Fare (see the Embarked subsection).

![Survival rate (fraction of passengers who survived) by Sex, Pclass and Embarked](tasks/eda_1/charts/survival_rate_by_group.png)

**By age bin:** Survival was 59.2% under 13 (n=71), 33.4% for ages 13–30 (n=485), 42.8% for ages 31–50 (n=271) and 34.4% over 50 (n=64). The 177 missing Age values were imputed with the median of their Pclass and Sex group before these rates were computed. The under-13 group is small, and its rate rests partly on imputed ages, so the apparent child advantage is tentative.

**By Fare quartile:** Survival rose steadily: 19.7% (Q1, n=223), 30.4% (Q2, n=224), 45.5% (Q3, n=222) and 58.1% (Q4, n=222).

**Mean Age and Fare by survival:** Survivors had a mean Age of 28.11 and non-survivors 29.74. Survivors had a mean Fare of 48.40 and non-survivors 22.12. The Age means depend on the median-imputed values.

### Statistical tests and effect sizes

Holm correction was applied across five tests: Sex, Pclass and Embarked (chi-square), and Age and Fare (Mann-Whitney).

**Sex:** The association with survival is significant (chi-square = 263.05, df 1, p = 3.7e-59, Cramér's V = 0.543; Holm-adjusted p = 1.9e-58). In the logistic regression Survived ~ female + Pclass, female odds of survival were 14.06 times male odds (95% CI 9.81 to 20.16, p = 6.9e-47).

**Pclass:** The association is significant (chi-square = 102.89, df 2, p = 4.5e-23, Cramér's V = 0.340; Holm-adjusted p = 1.8e-22). In the logistic regression Survived ~ female + Pclass, each step in class (1 to 2 to 3) multiplied the odds of survival by 0.38 (95% CI 0.31 to 0.47, p = 1.3e-19).

**Embarked:** The association is significant but weak (chi-square = 25.96, df 2, p = 2.3e-6, Cramér's V = 0.171; Holm-adjusted p = 4.6e-6). Embarked was not adjusted for Pclass, so the association may reflect the class mix of the ports.

**Fare:** Survivors paid on average 26.28 more (mean 48.40 vs 22.12). The Welch 95% CI for the difference is 18.73 to 33.83 (Welch p = 2.7e-11). The Mann-Whitney test is significant (Holm-adjusted p = 1.4e-21). The rank-biserial correlation is 0.38 and Cohen's d is 0.55, with positive values meaning survivors paid more. Both magnitudes are in the medium range. Fare is correlated with Pclass, so this association may partly reflect class.

**Age:** The mean difference is −1.63 years (survivors younger; Welch 95% CI −3.46 to 0.21, Welch p = 0.082). The Holm-adjusted Mann-Whitney p is 0.25. The rank-biserial correlation is −0.046 and Cohen's d is −0.12, both negligible. The Age values include 177 median-imputed ages. Age is not significant after correction.

**Multiple comparisons:** After Holm correction, Sex, Pclass, Embarked and Fare remain significant at the 0.05 level. Age does not.

![Effect sizes: Cramér's V for Sex, Pclass, Embarked; rank-biserial for Age and Fare (positive = survivors higher)](tasks/stat_1/charts/stat_effect_sizes.png)

### Sex × Pclass interaction

**Survival by Sex and Pclass:**

| Group | Survived | Rate |
|---|---|---|
| Women, class 1 | 91 of 94 | 96.8% |
| Women, class 2 | 70 of 76 | 92.1% |
| Women, class 3 | 72 of 144 | 50.0% |
| Men, class 1 | 45 of 122 | 36.9% |
| Men, class 2 | 17 of 108 | 15.7% |
| Men, class 3 | 47 of 347 | 13.5% |

**Linear-slope model:** The interaction coefficient is −1.359 log-odds per class for women relative to men (p = 2.2e-05, 95% CI −1.99 to −0.73). The Pclass slope is −0.642 log-odds per class for men and about −2.00 for women. The interaction model fits better than the additive model (LR = 24.08, df 1, p = 9.3e-07; AIC 811.1 vs 833.2).

**Factor-coded model:** Coding Pclass as a factor, the interaction still holds (LR = 28.79, df 2, p = 5.6e-7; AIC 810.1 vs 834.9). The per-class odds ratios for women vs men are:
- Class 1: OR 51.9 (95% CI 15.5 to 173.6)
- Class 2: OR 62.5 (95% CI 23.4 to 166.6)
- Class 3: OR 6.4 (95% CI 4.1 to 10.0)

The class-2 interaction term is 0.185 (SE 0.79, p about 0.82), so women's advantage in class 2 does not differ from class 1. The class-3 interaction term is −2.10 (SE 0.66, p about 0.001). The factor-coded result therefore qualifies the linear-slope description: the interaction is a step at class 3 rather than a constant per-class slope.

![Survival rate (share of passengers who survived) by passenger class, plotted separately for women and men](tasks/stat_2/charts/sex_pclass_survival_rate.png)

### Embarked and its link to Pclass and Fare

Embarked is strongly associated with Pclass (chi-square 122.64, df 4, p about 1.5e-25). Of passengers at C, 50.6% were in class 1 (85 of 168). Of passengers at Q, 93.5% were in class 3 (72 of 77). Of passengers at S, 54.6% were in class 3 (353 of 646). The 2 missing Embarked values were filled with S.

Mean Fare by port is C 59.95, S 27.24 and Q 13.28. Within classes, C's mean is higher than S's in class 1 (104.72 vs 70.51) and class 2 (25.36 vs 20.33). In class 3, C's mean is lower (11.21 vs 14.64). Fare therefore explains part of the port gap, but not all of it.

Within each class, C's survival is still above S's:
- Class 1: 69.4% (n=85) vs 58.9% (n=129)
- Class 2: 52.9% (n=17) vs 46.3% (n=164)
- Class 3: 37.9% (n=66) vs 19.0% (n=353)

The port effect is therefore not only a class effect. The Q cells are very small (2, 3 and 72 passengers in classes 1, 2 and 3), so Q-based comparisons within class are unreliable.

![Survival rate (fraction survived) by Pclass, grouped by Embarked port; counts in recorded facts](tasks/eda_3/charts/survival_by_pclass_embarked.png)

### Missing values and survival

**Age:** Passengers with Age missing survived at 29.4% (n=177), against 40.6% for those with Age present (n=714). The chi-square p is 0.0077. This is an unadjusted association; it has not been checked against Pclass or Sex.

**Cabin:** Missingness depends strongly on Pclass. Cabin is missing for 18.5% of class 1 (n=216), 91.3% of class 2 (n=184) and 97.6% of class 3 (n=491); chi-square p is about 1e-121. Cabin is missing for 87.6% of non-survivors (n=549) and 60.2% of survivors (n=342), with chi-square p about 7e-21. This association likely reflects Pclass, since Cabin missingness is driven by class. It has not been adjusted for Pclass.

![Percent of passengers with missing Cabin, by Pclass](tasks/eda_2/charts/cabin_missing_by_pclass.png)

**Embarked:** The two rows with missing Embarked are PassengerId 62 and 830. Both were filled with S.

### Predictive models

The test set has 179 passengers, from an 80/20 stratified split of 712 training rows. Features were Pclass, Sex, Age, SibSp, Parch, Fare, Embarked and FamilySize.

| Model | Train accuracy | Test accuracy | Precision | Recall | F1 | ROC AUC |
|---|---|---|---|---|---|---|
| Majority-class baseline | 0.6166 | 0.6145 | 0.0 | 0.0 | 0.0 | 0.5 |
| Logistic regression | 0.8076 | 0.8045 | 0.7931 | 0.6667 | 0.7244 | 0.8437 |
| Random forest (300 trees) | 0.9831 | 0.8156 | 0.7903 | 0.7101 | 0.7481 | 0.8318 |

Both models beat the baseline on test accuracy. The random forest is overfitted: its train accuracy exceeds its test accuracy by 0.17, so its test scores are optimistic. Its accuracy edge over logistic regression (1.1 points) is within the noise of a 179-row test set. Random forest has higher F1, and logistic regression has higher ROC AUC.

![Test-set accuracy, F1 and ROC AUC of logistic regression and random forest predicting Survived](tasks/ml_1/charts/ml1_model_scores.png)

**Feature importance (permutation drop in test ROC AUC, 20 repeats):**
- Logistic regression: Pclass 0.0931, Sex_male 0.0459, Sex_female 0.0427, Age 0.0244, SibSp 0.0083, Fare 0.0035, FamilySize 0.0025, Embarked_C 0.0004.
- Random forest: Age 0.0514, Sex_male 0.0409, Fare 0.038, Sex_female 0.0308, Pclass 0.0286, Embarked_S 0.0001, Embarked_C −0.0017, FamilySize −0.0021.

Pclass, Sex and Age carry most of the signal. Fare ranks third for the random forest but is near zero for logistic regression, so its role should not be generalised across models. Parch contributes nothing (−0.0023 for random forest, 0.0001 for logistic regression). SibSp is small for logistic regression (0.0083) and negative for random forest (−0.0025). FamilySize and Embarked add little beyond Sex, Pclass and Age.

Age was imputed with the training median of 28.5 for 19.9% of rows (177 of 891). The imputed passengers carry no real age information, which may dilute the Age signal for them.

## Limitations

- **Imputed Age.** 177 Age values (19.9%) were imputed. The EDA used the median of Pclass and Sex groups; the models used the training median of 28.5. Results that use Age depend on these values: the age-bin rates, the mean Age by survival, the Age tests, and the model Age features. The child advantage under 13 is explicitly tentative because the group is small (n=71) and partly imputed.
- **Age null result not checked.** Whether the Age null result holds when imputed rows are excluded or flagged has not been tested.
- **Embarked imputation.** The 2 missing Embarked values were filled with S. The S counts include them.
- **Small Embarked cells.** Q has 2, 3 and 72 passengers in classes 1, 2 and 3. Within-class port comparisons for Q are not reliable.
- **Unadjusted associations.** The Embarked chi-square was not adjusted for Pclass. The Cabin association was not adjusted for Pclass. The Age-missingness association was not adjusted for Pclass or Sex. The Fare association was not adjusted for Pclass in a joint model.
- **Fare and Pclass correlation (unresolved review issue).** Fare is correlated with Pclass, so the Fare association may partly reflect class. The adjusted analysis that would settle this is in eda_3 or stat_2, but neither task fitted a model that adjusts for Fare and Pclass together. This issue stands.
- **Confidence intervals for Age and Fare effect sizes (unresolved review issue).** The review requires 95% confidence intervals for the rank-biserial and/or Cohen's d for Age and Fare. These are not reported here. The Welch CI for the mean difference is reported, but not for the effect sizes. This issue stands.
- **Magnitude of the Fare effect (unresolved review issue).** The rank-biserial correlation of 0.38 and Cohen's d of 0.55 are medium in magnitude. Fare should not be described as a strong effect.
- **Overfitted random forest (unresolved in ml_1).** The random forest's test scores are optimistic. Its accuracy advantage over logistic regression is not reliable on 179 test rows. The models were evaluated on a single 80/20 split.
- **Disagreement on Fare importance.** Fare ranks third for the random forest and is near zero for logistic regression. The findings disagree and this is reported as such, not resolved.
- **Age: two results that do not address the same question.** The EDA reports a tentative under-13 survival rate of 59.2% (n=71, partly imputed). The statistical test covers all ages and finds no significant Age association after correction (Holm-adjusted Mann-Whitney p 0.25). The child advantage was not tested separately, so these two results are not directly compared.
- **Association, not causation.** All results are associations in a single historical sample, with no causal analysis.
- **No failed tasks.** All seven tasks (eda_1, stat_1, ml_1, stat_2, eda_2, eda_3, stat_3) completed.

**Numbers not traced to a recorded fact.** The automatic check found no recorded value for these numbers:
- 0.001 in: "The class-2 interaction term is 0.185 (SE 0.79, p about 0.82), so women's advantage in class 2 does not differ from class 1. The class-3 interaction term is −2."
- 50.6% in: "Embarked is strongly associated with Pclass (chi-square 122.64, df 4, p about 1.5e-25). Of passengers at C, 50.6% were in class 1 (85 of 168). Of passengers at "
- 93.5% in: "Embarked is strongly associated with Pclass (chi-square 122.64, df 4, p about 1.5e-25). Of passengers at C, 50.6% were in class 1 (85 of 168). Of passengers at "
- 54.6% in: "Embarked is strongly associated with Pclass (chi-square 122.64, df 4, p about 1.5e-25). Of passengers at C, 50.6% were in class 1 (85 of 168). Of passengers at "
- 1.1 in: "Both models beat the baseline on test accuracy. The random forest is overfitted: its train accuracy exceeds its test accuracy by 0.17, so its test scores are op"

## Open questions

- Does the Sex effect hold within each Pclass once adjusted for Age, Fare, Embarked and FamilySize, or is the Sex × Pclass interaction driven by these correlated variables?
- Does the class-3 interaction survive adjustment for Age, Fare, Embarked and FamilySize?
- Is the Embarked effect explained by Pclass or Fare once they are adjusted for in a multivariable logistic regression? Does the C vs S gap hold after adjusting for both jointly?
- Why do third-class women survive at only 50%? Do Embarked, Cabin or Fare explain the drop?
- Is Cabin missingness still associated with Survived after controlling for Pclass?
- Is Age missingness associated with Pclass or Sex, and does that explain its lower survival rate?
- Is the child advantage robust when the 177 median-imputed Age rows are excluded or flagged?
- Is the Age null result robust when imputed rows are excluded or flagged?
- Does the title in Name (Mr, Mrs, Miss, Master) add signal beyond Sex and Age? Does the Sex × Pclass interaction hold when Sex is replaced by title?
- Would cross-validated or tuned models, such as gradient boosting or a regularised logistic regression, reduce the random forest overfitting and give a more reliable model comparison on a larger evaluation set?
- Is imputing Age with the training median hurting the models for passengers with missing Age?