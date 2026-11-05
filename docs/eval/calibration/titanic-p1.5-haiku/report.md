# Titanic Survival Analysis: Drivers of Survived (891 Passengers)

## Summary

- **Sex is the strongest association with survival.** 74.2% of women survived against 18.9% of men (chi-square 263.05, Cramér's V = 0.543). Men had odds of survival 0.081 times those of women (95% CI 0.058 to 0.112).
- **Class and sex interact.** The Sex×Pclass interaction is significant (LR chi-square 28.79 on 2 df, p = 5.6e-7). The female-vs-male odds ratio is 51.9 in class 1, 62.5 in class 2 and 6.38 in class 3. The class 1 and 2 estimates are imprecise because the male cells are small. The interaction remains significant after adjusting for Age, Fare and Embarked.
- **Fare adds no independent survival information once Pclass and Sex are controlled for** (LR p = 0.40). Pclass accounts for about 85% of the crude Fare effect, by a coefficient-reduction measure. Fare's crude association with survival is strong, though: 19.7% in the lowest Fare quartile against 58.1% in the highest.
- **The predictive models beat the majority-class baseline.** The majority-class test accuracy is 61.4%. Logistic regression reaches 78.5% and random forest 78.9% on a 223-passenger test split, with ROC AUC of 0.840 and 0.836. Sex is the most important feature in both models.

## Data

- **Size:** 891 rows × 12 columns.
- **Target:** `Survived` (binary). 38.4% survived (342 passengers) and 61.6% did not.
- **Features used:** Pclass, Age, SibSp, Parch, Fare (numeric); Sex, Embarked (categorical). No date or time features.
- **Excluded as features:** PassengerId, Ticket, Cabin, Name (identifiers or free text).
- **Missing values:** Age 177 of 891 (19.9%), Cabin 687 (77.1%), Embarked 2 (0.2%).

## Findings

### Survival rates by group

- **Sex:** 74.2% of female passengers (314) survived, against 18.9% of male passengers (577).
- **Pclass:** survival falls with class. It is 63.0% in class 1 (216 passengers), 47.3% in class 2 (184) and 24.2% in class 3 (491).
- **Embarked:** 55.4% at C (168 passengers), 39.0% at Q (77) and 33.7% at S (644). The two passengers with no Embarked value both survived.
- **Age (quartile bins):** 45.8% (0.4 to 20 years, n = 179), 36.1% (20 to 28, n = 183), 43.4% (28 to 38, n = 175) and 37.3% (38 to 80, n = 177). The pattern is not monotonic. Passengers with missing Age (n = 177) survived at 29.4%.
- **Fare (quartiles):** 19.7% (up to 7.91, n = 223), 30.4% (7.91 to 14.45, n = 224), 45.5% (14.45 to 31.0, n = 222) and 58.1% (above 31.0, n = 222).
- **Survivors vs non-survivors:** mean Fare is 48.4 for survivors against 22.1 for non-survivors. Mean Age is 28.3 against 30.6, mean SibSp 0.47 against 0.55, and mean Parch 0.47 against 0.33. The analysis describes the groups as differing mainly in Fare.

![Survival rate by Sex and Pclass (share of passengers who survived)](tasks/eda_1/charts/survival_rate_sex_pclass.png)

### Significance and effect sizes

- **Sex:** chi-square 263.05, p = 3.7e-59, Cramér's V = 0.543. The odds ratio for male vs female survival is 0.081 (95% CI 0.058 to 0.112).
- **Pclass:** chi-square 102.89, p = 4.5e-23, Cramér's V = 0.340. Odds ratios against the other classes are 3.87 for class 1 (95% CI 2.81 to 5.34), 1.59 for class 2 (95% CI 1.15 to 2.21) and 0.254 for class 3 (95% CI 0.191 to 0.338).
- **Embarked:** on the 889 passengers with a known port, chi-square 26.49 (df = 2), p = 1.8e-6, Cramér's V = 0.173. The analysis describes this as weak to moderate. The two passengers with no port were excluded rather than kept as a category, because a category with 2 passengers has expected counts below 5, which makes the chi-square test invalid. The minimum expected count in the 889-passenger table is 29.4. Excluding them does not change the conclusion, and the ordering C > Q > S holds. This result supersedes an earlier three-category test that included the invalid Missing category.
- **Fare:** Mann-Whitney p = 4.6e-22, Welch t-test p = 2.7e-11. The mean difference (survived minus not) is 26.28 (95% CI 18.73 to 33.83). Median Fare is 26.0 for survivors and 10.5 for non-survivors.
- **Age:** the result depends on the test. The Mann-Whitney p-value is 0.16 (not significant), but the Welch t-test p-value is 0.041. The mean difference (survived minus not) is −2.28 years (95% CI −4.47 to −0.09), so survivors are slightly younger on average. The two tests disagree, and this report does not resolve the disagreement. The effect is small and should be read cautiously.

![Left: survival rate by Pclass and Sex (share who survived). Right: Fare distribution for non-survivors and survivors.](tasks/stat_1/charts/stat1_survival_sex_pclass_fare.png)

### Sex × Pclass and Sex × Age interactions

- **Cell rates:** female class 1 91 of 94 (96.8%); female class 2 70 of 76 (92.1%); female class 3 72 of 144 (50.0%); male class 1 45 of 122 (36.9%); male class 2 17 of 108 (15.7%); male class 3 47 of 347 (13.5%). Male survival is lower than female survival in every class, and the gap is widest in classes 1 and 2.
- **Sex × Pclass:** the interaction is significant (LR chi-square 28.79 on 2 df, p = 5.6e-7). Female-vs-male odds ratios are 51.9 in class 1 (95% CI 15.5 to 173.6), 62.5 in class 2 (95% CI 23.4 to 166.6) and 6.38 in class 3 (95% CI 4.08 to 10.0). The class 1 and 2 male cells contain only 45 and 17 survivors, so the magnitudes in those classes are imprecise. Their direction and significance are clear.
- **Sex × Pclass after adjustment:** on 712 passengers with complete Age, Fare and Embarked, the interaction is LR chi-square 33.70 on 2 df, p = 4.8e-8. On the same 712 passengers without covariates it is LR 29.93 on 2 df, so adjustment does not weaken it. Adjusted female-vs-male odds ratios are 36.2 in class 1 (95% CI 10.4 to 125.5), 76.0 in class 2 (95% CI 27.2 to 212.3) and 4.21 in class 3 (95% CI 2.46 to 7.22). The female advantage stays far larger in classes 1 and 2 than in class 3.
- **Sex × Age:** significant but weak. On 714 passengers with known Age, the LR chi-square is 9.55 on 1 df (p = 0.002). The per-year odds ratio for Age is 1.020 for women and 0.979 for men, and the interaction odds ratio is 0.960 (95% CI 0.935 to 0.986). Older women were slightly more likely to survive and older men slightly less likely, but each per-year effect is small.
- **Sex × Age after adjusting for Pclass:** LR chi-square 11.90 on 1 df, p = 0.00056, on 714 passengers. This model did not adjust for Fare or Embarked, so its robustness to those variables is untested.

![Survival rate by Pclass and Sex: share of passengers who survived in each of the six cells](tasks/stat_2/charts/stat2_survival_rate_sex_pclass.png)

### Fare after controlling for Pclass and Sex

- **Fare adds no significant information:** adding log(Fare+1) to the Pclass + Sex logistic model gives a likelihood-ratio statistic of 0.715 (p = 0.40).
- **Adjusted Fare effect:** the odds ratio is 1.10 per log unit of Fare (95% CI 0.88 to 1.39), and 1.015 per 10-unit increase in Fare (95% CI 0.975 to 1.056). Both intervals include 1.
- **Fare and Pclass are correlated:** Pearson r = −0.55 for Fare and −0.66 for log(Fare+1), so higher-fare passengers are mostly in higher classes.
- **Pclass accounts for most of the crude Fare effect:** the log-Fare coefficient falls from 0.642 (Sex + Fare model) to 0.099 once Pclass is added, so about 85% of the effect is accounted for by Pclass. This is a coefficient-reduction measure, not a variance decomposition.

### Missing values and survival

- **Age missingness and survival:** rows with missing Age survived at 29.4%, against 40.6% for rows with Age present (chi-square p = 0.0077).
- **Age missingness and Pclass:** 76.8% of rows with missing Age are class 3 (49.7% for present Age), and 16.9% are class 1 (26.1% for present Age). Chi-square p = 9.9e-11.
- **Age missingness and other variables:** not related to Sex (chi-square p = 0.119), but related to Fare (Mann-Whitney p = 2.7e-08).
- **Cabin missingness and survival:** rows with missing Cabin survived at 30.0%, against 66.7% for rows with Cabin present (chi-square p = 6.7e-21).
- **Cabin missingness and Pclass:** 69.7% of rows with missing Cabin are class 3, against 5.9% of rows with Cabin present. 86.3% of rows with Cabin present are class 1, against 5.8% of rows with Cabin missing (chi-square p = 9.6e-122).
- **Embarked missingness:** the two rows with no port have a median Fare of 80.0, against 14.45 for rows with a port (Mann-Whitney p = 0.042). Both are class 1 females, and both survived. This is weak evidence from two rows.

![Survival rate for rows with missing vs present Age (left) and Cabin (right)](tasks/eda_2/charts/missingness_vs_survival.png)

### Predictive modelling

- **Setup:** the train/test split was stratified on Survived, with a 25% test size and random_state 42 (668 training and 223 test rows). The feature table excludes PassengerId, Name, Ticket and Cabin. Age is median-imputed with an Age_missing flag, and Embarked is one-hot encoded.
- **Scores on the test split:**
  - Majority-class baseline: 61.4% accuracy.
  - Logistic regression: 78.5% accuracy, precision 0.738, recall 0.686, F1 0.711, ROC AUC 0.840. Training accuracy is 81.0%.
  - Random forest: 78.9% accuracy, precision 0.753, recall 0.674, F1 0.712, ROC AUC 0.836. Training accuracy is 92.1%.
- **Model choice:** the two models perform almost identically on the test split. The random forest overfits more (92.1% training against 78.9% test). The simpler logistic regression is as good a choice for this table.
- **Sex is the most important feature in both models.** It has the largest standardized logistic coefficient (1.25) and the largest random forest impurity importance (0.33). Permutation importance drops test ROC AUC by 0.224 when Sex is shuffled.
- **Pclass and Age come next.** Pclass has the second-largest logistic coefficient (0.93) and a permutation drop of 0.044. Age has a coefficient of 0.54 and a permutation drop of 0.032.
- **Fare's importance depends on the measure.** Its logistic coefficient is 0.12 and its permutation drop is 0.027, but its random forest impurity importance is 0.24. The analysis did not test why.
- **SibSp, Embarked and Age_missing are not negligible under logistic regression.** Their standardized coefficients are 0.262 (SibSp), 0.227 (Age_missing) and 0.169 (Embarked_Q), all above Fare's 0.122. Under permutation importance they contribute little (ROC AUC drops of 0.0042 for SibSp and 0.0012 for Age_missing), and their random forest impurity importance is also small (0.0136 for Age_missing). The two measures therefore disagree on these features, and this report does not resolve the disagreement.

![Test-split accuracy, F1 and ROC AUC for logistic regression and random forest predicting Survived, against the majority-class accuracy baseline (61.4%)](tasks/ml_1/charts/ml1_model_scores.png)

## Limitations

- **Unresolved review issue: logistic coefficients for SibSp, Age_missing and Embarked are unchecked for collinearity.** The lead's objection stands. These features are not negligible under logistic regression, but the model has not been refit without them to check whether their coefficients reflect signal or collinearity. This affects the ml_1 findings on SibSp, Embarked and Age_missing, and the logistic feature ranking that depends on them.
- **Data leakage in preprocessing:** the Age median and the Embarked mode were computed on the full dataset before the train/test split. The test-split scores are therefore slightly optimistic.
- **Single split:** model performance was measured on one 25% test split. Cross-validation was not run, so the stability of the baseline advantage is unknown.
- **Small male cells:** the class 1 and class 2 male cells have 45 and 17 survivors. The female-vs-male odds ratios for those classes have very wide confidence intervals (for example, 15.5 to 173.6 in class 1). Their magnitudes are imprecise. Firth-penalised or exact estimates were not computed.
- **Age test disagreement:** the Mann-Whitney and Welch tests disagree on the Age difference (p = 0.16 against p = 0.041). The effect is small in either case.
- **Sex × Age adjustment is incomplete:** the adjusted model (LR 11.90) adjusts only for Pclass. Its robustness to Fare and Embarked was not tested.
- **Embarked exclusions:** the two passengers with no port are excluded from the Embarked test. The Embarked-missingness Fare result rests on two rows.
- **Fare mediation measure:** the 85% figure is a coefficient-reduction measure, not a variance decomposition.
- **Observational data:** the findings are associations. They do not establish causes.
- **Failed tasks:** none reported.

**Numbers not traced to a recorded fact.** The automatic check found no recorded value for these numbers:
- 7.91 in: "- **Fare (quartiles):** 19.7% (up to 7.91, n = 223), 30.4% (7.91 to 14.45, n = 224), 45.5% (14.45 to 31.0, n = 222) and 58.1% (above 31.0, n = 222)."
- 31.0 in: "- **Fare (quartiles):** 19.7% (up to 7.91, n = 223), 30.4% (7.91 to 14.45, n = 224), 45.5% (14.45 to 31.0, n = 222) and 58.1% (above 31.0, n = 222)."

## Open questions

- Do Firth-penalised or exact estimates give more stable female-vs-male odds ratios in class 1 and class 2, given the small male cells?
- Does the Sex × Age interaction remain significant after also adjusting for Fare and Embarked, in the 712-passenger complete-case sample?
- Within third class, what explains the gap between female (50.0%) and male (13.5%) survival after adjustment?
- Does the Fare effect differ within each class, and is the Fare–survival relationship non-linear on the log scale? Does a spline or binned Fare change the conclusion?
- Does Cabin carry survival information beyond Pclass and Fare, through its deck letter or as a known-Cabin indicator?
- Does imputing Age by Pclass and Sex, or deriving a title from Name, change the survival signal or improve prediction beyond Sex, Pclass and Age?
- Does a family-size feature (SibSp plus Parch) or a ticket-group feature add predictive signal, given that Fare is mostly redundant with Pclass?
- Do the SibSp and Age_missing logistic coefficients reflect real signal or collinearity, as checked by refitting without them?
- Does the model's advantage over the baseline hold across cross-validation folds?
- Does Ticket sharing or family size explain the Fare and Pclass pattern of missing Cabin?