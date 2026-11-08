# Titanic Passenger Survival (Target: Survived): Analysis Report

## Summary

- **Sex is the strongest association with survival.** Female passengers survived at 74.2% (n=314) versus 18.9% for males (n=577). The female odds ratio is 12.4 (95% CI 8.9 to 17.1; chi-square = 263.1, p = 3.7e-59, Cramér's V = 0.54).
- **Passenger class is the second strongest.** Survival is 63.0% in Pclass 1, 47.3% in Pclass 2 and 24.2% in Pclass 3. The class 1 vs class 3 odds ratio is 5.3 (95% CI 3.8 to 7.5).
- **Sex and Pclass interact.** The female advantage in odds is much smaller in third class. The interaction holds after adjusting for Age, Fare and Embarked (LR chi-square = 33.7, df 2, p = 4.8e-8), though the adjusted class 2 estimate is very imprecise.
- **Embarkation port is weakly associated with survival, and part of that association is explained by Pclass and Fare.** The C vs S odds ratio falls from 2.44 unadjusted to 1.68 (95% CI 1.14 to 2.46) after adjustment, so a residual association remains.
- **Models beat the majority-class baseline.** The baseline test accuracy is 0.614. Logistic regression reaches 0.785 accuracy and 0.840 ROC AUC. The random forest reaches 0.794 accuracy but overfits (train accuracy 0.918).

## Data

- **Size:** 891 rows, 12 columns.
- **Target:** Survived, a binary variable. 61.6% of passengers did not survive (class 0) and 38.4% survived (class 1).
- **Features used:** Sex, Pclass, Age, Fare, SibSp, Parch and Embarked. Cabin was used only as a missingness indicator. PassengerId, Name and Ticket were not used as features.
- **Missing values:** Age 19.9% (177 rows), Cabin 77.1% (687 rows), Embarked 0.2% (2 rows).

## Findings

### Overall survival and distributions

- Overall, 38.4% of the 891 passengers survived.
- Survivors had higher mean fares (48.4 vs 22.1) and were slightly younger on average (mean Age 28.3 vs 30.6). They had slightly fewer siblings/spouses aboard (mean SibSp 0.47 vs 0.55) and more parents/children aboard (mean Parch 0.47 vs 0.33).

### Sex

- Female passengers survived at 74.2% (n=314) and male passengers at 18.9% (n=577).
- Chi-square = 263.1 (df 1, p = 3.7e-59), Cramér's V = 0.54, n = 891.
- The female odds of survival are 12.4 times the male odds (95% CI 8.9 to 17.1). The female-male survival rate difference is 55.3 percentage points (95% CI 49.5 to 61.1).

![Survival rate by Sex with 95% CI in the text](tasks/stat_1/charts/stat1_survival_by_sex.png)

### Passenger class

- Survival rates: Pclass 1 at 63.0% (n=216), Pclass 2 at 47.3% (n=184), Pclass 3 at 24.2% (n=491).
- Chi-square = 102.9 (df 2, p = 4.5e-23), Cramér's V = 0.34.
- The class 1 odds of survival are 5.3 times the class 3 odds (95% CI 3.8 to 7.5).

### Embarked

- Survival rates: C 55.4% (n=168), Q 39.0% (n=77), S 33.7% (n=644). The two passengers with missing Embarked both survived, which is too few to interpret.
- Chi-square = 26.5 (df 2, p = 1.8e-6, n = 889), Cramér's V = 0.17. The association is weak.
- The C vs S odds ratio is 2.44 (95% CI 1.73 to 3.45). The survival rate difference is 21.7 percentage points (95% CI 13.3 to 30.0).
- Embarked is likely confounded with Pclass and Fare. The adjusted result is given under "Embarked after adjustment" below.

### Age

- Survival by Age bin: child (under 12) 57.4% (n=68), teen (12 to 17) 48.9% (n=45), adult (18 to 59) 38.6% (n=575), senior (60+) 26.9% (n=26). The 177 passengers with missing Age are excluded.

![Survival rate by Age bin; passengers with missing Age excluded](tasks/eda_1/charts/survival_by_age_bin.png)

- The Age results disagree between tests, and no firm conclusion can be drawn:
  - Mann-Whitney p = 0.16 (n = 290 survived, 424 died), rank-biserial r = +0.06, Cohen's d = -0.16.
  - Mean age difference (survived minus died) is -2.3 years (bootstrap 95% CI -4.5 to -0.1), which excludes zero.
  - Median age difference is 0.0 years (95% CI -3.0 to 2.0), which includes zero.
  - Welch t-test p = 0.04.
- The rank test does not reject, while the mean-based bootstrap and Welch test do.
- The Age-bin conclusions were not tested for sensitivity to imputing the 177 missing values.

### Fare

- Survival rises across Fare quartiles: Q1 (up to 7.91) 19.7% (n=223), Q2 (7.91 to 14.45) 30.4% (n=224), Q3 (14.45 to 31.00) 45.5% (n=222), Q4 (above 31.00) 58.1% (n=222).
- Mann-Whitney p = 4.6e-22 (n = 342 survived, 549 died). Rank-biserial r = -0.38. The sign is negative under the stated convention (r = 1 - 2U/(n1 n2)) because survivors have higher fares. Cohen's d = +0.55.
- Mean fare difference (survived minus died) is 26.3 (bootstrap 95% CI 19.0 to 33.8). Median difference is 15.5 (95% CI 12.1 to 17.1). Median fare is 26.0 for survivors and 10.5 for those who died. Welch t-test p = 2.7e-11.
- Fare was not tested for independence from Pclass in this analysis (see the adjusted results below).

### Sex x Pclass interaction

- The likelihood-ratio test of the Sex x Pclass interaction in a logistic regression (log-odds scale) gives chi-square = 28.8, df 2, p = 5.6e-7. This model includes Sex and Pclass only.
- The female vs male odds ratios within each class (Haldane 0.5 correction, Wald 95% CI) are unadjusted:
  - Class 1: 44.5 (14.4 to 137.6)
  - Class 2: 56.7 (21.9 to 147.0)
  - Class 3: 6.3 (4.0 to 9.9)
- The female-vs-male log odds ratios are 3.80 in class 1, 4.04 in class 2 and 1.84 in class 3.
- The ratio of odds ratios is 0.14 for class 3 vs class 1 and 1.27 for class 2 vs class 1. These are ratios of odds ratios, not effect sizes on the log-odds scale. Classes 1 and 2 have similar Sex effects, and class 3 has a much smaller one.
- The Pclass effect (class 1 vs class 3) is larger for women than for men on both scales:
  - Survival rate gap: 46.8 percentage points for women (96.8% vs 50.0%) and 23.3 points for men (36.9% vs 13.5%).
  - Odds ratio: 26.1 (95% CI 8.6 to 79.8) for women and 3.7 (95% CI 2.3 to 6.0) for men.
- Female minus male survival rate differences by class (Wald 95% CI, unadjusted): class 1 59.9 points (50.7 to 69.2), class 2 76.4 points (67.2 to 85.5), class 3 36.5 points (27.5 to 45.4).

Cell counts and survival by Sex and Pclass:

| Sex | Pclass | n | Survived | Survival rate |
|---|---|---|---|---|
| Female | 1 | 94 | 91 | 96.8% |
| Female | 2 | 76 | 70 | 92.1% |
| Female | 3 | 144 | 72 | 50.0% |
| Male | 1 | 122 | 45 | 36.9% |
| Male | 2 | 108 | 17 | 15.7% |
| Male | 3 | 347 | 47 | 13.5% |

- The within-class estimates rest on small cells: 94 women in class 1 with 3 deaths, and 76 women in class 2 with 6 deaths. They use a Haldane correction, and the interaction contrast has no separate confidence interval.

![Survival rate (%) by Pclass, split by Sex](tasks/stat_2/charts/stat2_survival_sex_pclass.png)

- **Adjusted results.** With Age, Fare and Embarked in the model, the interaction remains significant: LR chi-square = 33.7, df 2, p = 4.8e-8. This uses 712 complete cases; 179 were excluded (177 with missing Age and 2 with missing Embarked). The missing-Age passengers were excluded, not imputed.
- Adjusted female vs male odds ratios: class 1 35.5 (10.2 to 123.2, n=184), class 2 138.7 (38.1 to 505.5, n=173), class 3 4.5 (2.6 to 7.9, n=355). The female advantage in odds is still much smaller in third class, though the class 2 estimate is very imprecise.
- The adjusted class 2 odds ratio (138.7) is well above the unadjusted one (56.7), and the adjusted class 3 odds ratio (4.5) is below the unadjusted one (6.3). These estimates come from different samples and models and were not reconciled.

### Embarked after adjustment

- After adjusting for Pclass and Fare (with a Q dummy in the model), C vs S remains associated with survival: adjusted OR = 1.68 (95% CI 1.14 to 2.46, p = 0.008). The unadjusted OR on the same C/S rows is 2.44. The finding reports this as a reduction of about 31% on the odds-ratio scale.
- Part of the port effect is explained by Pclass and Fare, but a residual association remains.
- The 2 rows with missing Embarked were dropped (complete-case analysis), so the model uses n = 889. Fare had no missing values among the remaining rows.

### Missingness

- Missing counts: Age 177 of 891 (19.9%), Cabin 687 (77.1%), Embarked 2 (0.2%).
- **Cabin.** Passengers with a recorded Cabin survived at 66.7% (n=204) versus 30.0% without (n=687). Chi-square = 87.9, p = 6.7e-21. Cabin missingness is strongly associated with Pclass (chi-square = 557.3, p = 9.6e-122), so this gap is probably partly confounded by class and should not be read as a strong independent marker of survival.
- **Age.** Survival is 29.4% without Age (n=177) versus 40.6% with Age (n=714), chi-square p = 0.0077. Age missingness depends on class: 13.9% in Pclass 1, 6.0% in Pclass 2 and 27.7% in Pclass 3 (chi-square p = 9.9e-11). By Sex it is 16.9% for women and 21.5% for men, which is not significant (p = 0.119). The survival gap for missing Age is probably partly confounded by class too.

![Rate of missing Age by passenger class](tasks/eda_2/charts/age_missing_by_pclass.png)

- Embarked missingness (2 rows) is too small to test.

### Predictive models

- Majority-class baseline test accuracy: 0.614 (223-passenger stratified test set; 668 training rows).

| Model | Train accuracy | Test accuracy | Test ROC AUC | Test F1 | Test precision | Test recall |
|---|---|---|---|---|---|---|
| Logistic regression (standardized) | 0.810 | 0.785 | 0.840 | 0.711 | 0.738 | 0.686 |
| Random forest (500 trees, min leaf 2) | 0.918 | 0.794 | 0.835 | 0.716 | 0.763 | 0.674 |

- Both models beat the baseline. The random forest's accuracy and F1 edge (1 to 2 percent points) is within the noise of a 223-row test set. The random forest overfits, with a train-test gap of about 0.12. The logistic regression gap is smaller (0.810 vs 0.785).
- **Preferred model.** Logistic regression is the model judged best. It has the higher ROC AUC (0.840 vs 0.835) and the smaller train-test gap. The AUC difference is small, and no test of the difference was reported.
- **Feature ranking, logistic regression** (absolute standardized coefficients, from the fitted model):
  1. Sex, 1.252
  2. Pclass, 0.929
  3. Age, 0.536
  4. SibSp, 0.262
  5. Age_missing, 0.227
  6. Embarked_S, 0.188
  7. Embarked_Q, 0.140
  8. Fare, 0.122
  9. Parch, 0.055
- **Random forest importances, for comparison:** Sex 0.333, Fare 0.245, Age 0.189, Pclass 0.105, SibSp 0.044, Parch 0.038, Embarked_S 0.024, Age_missing 0.013, Embarked_Q 0.009.
- Sex and Pclass rank high in both models, and Age is important in both. Fare ranks second in the random forest but eighth in logistic regression, and its contribution depends on the model. The Age_missing indicator has a sizeable logistic regression coefficient.
- Preprocessing: Age was median-imputed, with an Age_missing indicator added. Embarked missing values were filled with S, and Embarked was one-hot encoded (Q and S against C). Sex was binary (female = 1). PassengerId, Name, Ticket and Cabin were excluded from the features. The split was stratified 75/25 on Survived.

![Test-set accuracy, ROC AUC and F1 for logistic regression and random forest, with the majority-class baseline accuracy as a dashed line](tasks/ml_1/charts/ml1_model_comparison.png)

## Limitations

- **Observational data.** All associations are descriptive. The findings do not establish causes.
- **Confounding.** Pclass, Fare and Embarked are correlated. The unadjusted Embarked, Fare and missingness results are not adjusted for each other. The Cabin and Age missingness gaps are probably partly confounded by class, and this was not tested after adjustment.
- **Age results disagree.** The Mann-Whitney test does not reject, while the Welch test (p = 0.04) and the mean-difference bootstrap CI (excluding zero) do. The median-difference CI includes zero. No firm conclusion about Age is drawn.
- **Age imputation.** Age-bin results and the interaction test in the adjusted model exclude the 177 missing-Age passengers, while the machine learning models median-impute them. The sensitivity of results to imputation was not tested.
- **Small cells and corrections.** The within-class odds ratios for women in classes 1 and 2 rest on small cells and use a Haldane correction. The adjusted class 2 estimate (138.7, CI 38 to 506) is very imprecise.
- **Unresolved review issue, Sex x Pclass interaction (stat_2).** The lead's objection stands in part:
  - The within-class odds ratios and rate differences are unadjusted for Fare, Embarked and Age.
  - The interaction test of 28.8 (p = 5.6e-7) comes from a model with Sex and Pclass only.
  - The adjusted results in the same section come from a different sample (712 complete cases), so they are not directly comparable with the unadjusted estimates.
  - The requested fixes are applied in this report: a complete cell table is included, the 0.14 and 1.27 values are labelled as ratios of odds ratios, and the log odds ratios are described as such.
- **Unresolved review issue, model ranking (ml_1).** The feature ranking is given from the logistic regression fit, and the model choice rests on a small AUC difference. The ranking was not checked for stability across resamples or test splits.
- **Embarked and missing values.** Embarked missing values were filled with S in the machine learning models, but dropped in the regression. Two passengers with missing Embarked both survived, too few to interpret.
- **Model overfitting.** The random forest's train-test gap (0.918 vs 0.794) was not addressed by tuning or cross-validation.
- **Failed tasks.** None were recorded. All tasks in this analysis were completed and accepted.

## Open questions

- Does the Embarked C vs S association hold within each Pclass (Embarked x Pclass interaction)?
- How much of the Embarked effect is explained by the Pclass-Fare correlation, using a model with Fare only versus Pclass only?
- Are the Age-bin results and the Sex x Pclass interaction robust to multiple imputation of the 177 missing Age values?
- Do exact tests or bootstrap confidence intervals for the small female cells confirm the within-class odds ratios?
- Is the female class 3 survival rate (50.0%) explained by Fare or Embarked, which are correlated with class?
- Does Fare keep its predictive value after adjusting for Pclass, and is there a non-linear Fare effect? This could explain the gap between its high random forest importance and its small logistic regression coefficient.
- Do family-size features (SibSp + Parch), or Cabin- and Ticket-derived features, add predictive signal beyond Sex, Pclass and Fare?
- Does the Cabin missingness gap remain after controlling for Pclass and Sex? Is Cabin missingness related to shared ticket groups or deck letters?
- Can the two passengers with missing Embarked be assigned a port from Ticket or Fare?
- Does tuning the random forest's depth or leaf size, or using cross-validation, reduce its train-test gap?