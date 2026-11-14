# Survival on the Titanic: Associations, Interactions and Predictive Performance (891 passengers, target: Survived)

## Summary

- **Sex is the strongest association with survival.** Females survived at 74.2% (n=314) and males at 18.9% (n=577), a difference of 55.3 percentage points (95% CI 49.5 to 61.1). The chi-square test gives p = 3.7e-59, Cramér's V = 0.543.
- **Survival also varies with class, fare and port, and these associations are significant.** Survival is 63.0% in Pclass 1, 47.3% in Pclass 2 and 24.2% in Pclass 3. Port C shows 55.4% and Port S 33.7%. Fare differs significantly between survivors and non-survivors. Age does not differ significantly after Bonferroni correction.
- **The Sex effect depends on class and on age.** Females survive at high rates in classes 1 and 2 (96.8% and 92.1%). Male survival is 36.9%, 15.7% and 13.5% across classes 1 to 3. The Sex x Pclass and Sex x Age interactions are both significant by likelihood-ratio test.
- **Port C stays associated with survival after adjusting for Pclass and Fare** (adjusted OR 1.68, 95% CI 1.14 to 2.46, p = 0.008). The predictive models, however, give Embarked almost no permutation importance.
- **Both models beat the majority-class baseline (61.4% test accuracy).** Logistic regression reaches 77.1% and random forest 79.8%, with ROC AUC of 0.841 and 0.826. Sex and Pclass carry most of the predictive signal in the permutation results. The accuracy gap between the two models (79.8% vs 77.1%) rests on a single split and should not be read as a reliable difference.

## Data

- **Size:** 891 rows × 12 columns.
- **Target:** Survived, binary. 342 passengers survived (38.4%); 61.6% did not.
- **Features used:** Sex, Pclass, Age, Fare, SibSp, Parch and Embarked as predictors. Numeric features are Pclass, Age, SibSp, Parch and Fare. Categorical features are Sex and Embarked. The dataset has no date or time features.
- **Excluded as direct features:** PassengerId, Ticket, Cabin and Name, which are identifiers or free text. Cabin was analysed only for its missingness.
- **Missing values:** Cabin 77.1% (687 rows), Age 19.9% (177 rows), Embarked 0.2% (2 rows).

## Findings

### Overall survival and group rates

The overall survival rate is 38.4% (342 of 891).

**Sex.** Females survived at 74.2% (n=314) and males at 18.9% (n=577).

**Pclass.** Survival was 63.0% in class 1 (n=216), 47.3% in class 2 (n=184) and 24.2% in class 3 (n=491).

**Embarked.** Port C had 55.4% (n=168), Port Q 39.0% (n=77) and Port S 33.7% (n=644). The two passengers with missing Embarked both survived (n=2), but a rate based on two passengers is not reliable.

**SibSp.** Survival was 34.5% for 0 siblings/spouses (n=608), 53.6% for 1 (n=209), 46.4% for 2 (n=28), 25.0% for 3 (n=16), 16.7% for 4 (n=18), and 0.0% for 5 (n=5) and 8 (n=7). Passengers with one or two siblings/spouses survived more often than those travelling alone. Groups of 4 and above survived less often. The groups of 5 and 8 rest on very few passengers.

**Parch.** Survival was 34.4% for 0 parents/children (n=678), 55.1% for 1 (n=118), 50.0% for 2 (n=80), 60.0% for 3 (n=5), 0.0% for 4 (n=4), 20.0% for 5 (n=5) and 0.0% for 6 (n=1). Small families of one or two survived more often than passengers travelling alone. Groups of 3 to 6 are too small for their rates to be reliable.

![Survival rate (share of passengers who survived) by Sex, Pclass, Embarked, SibSp and Parch](tasks/eda_1/charts/survival_rate_by_group.png)

**Age and fare by survival.** Survivors had mean age 28.3 and median 28.0. Non-survivors had mean 30.6 and median 28.0. Survivors had mean fare 48.4 and median 26.0. Non-survivors had mean fare 22.1 and median 10.5. The fare mean is pulled up by a long right tail, so the medians give the clearer contrast.

### Significance and effect sizes

Each test below was run on the full sample unless stated otherwise.

- **Sex:** chi-square = 263.05, df = 1, p = 3.7e-59, Cramér's V = 0.543. Difference 55.3 points (95% CI 49.5 to 61.1).
- **Pclass:** chi-square = 102.89, df = 2, p = 4.5e-23, Cramér's V = 0.340. Class 1 versus class 3 difference 38.7 points (95% CI 31.3 to 46.2).
- **Embarked (n = 889 with known port):** chi-square = 26.49, df = 2, p = 1.8e-6, Cramér's V = 0.173. Port C versus S difference 21.7 points (95% CI 13.3 to 30.0). The finding notes this may partly reflect the Pclass mix.
- **SibSp:** chi-square = 37.27, df = 6, p = 1.6e-6, Cramér's V = 0.205.
- **Parch:** chi-square = 27.93, df = 6, p = 9.7e-5, Cramér's V = 0.177. The SibSp and Parch chi-square approximations are less reliable because small-group cells are sparse.
- **Fare:** Mann-Whitney p = 4.6e-22, rank-biserial r = 0.384. Survivors tend to have higher fares.
- **Age:** Mann-Whitney p = 0.160, rank-biserial r = -0.062, a negligible effect.

Under a Bonferroni correction across seven tests (adjusted alpha = 0.0071), Sex, Pclass, Embarked, SibSp, Parch and Fare are significant. Age is not.

![Survival rate (%) of passengers by Sex, Pclass and Embarked](tasks/stat_1/charts/stat1_survival_rate_by_group.png)

### Interaction of Sex with Pclass and with Age

**Sex x Pclass.** The interaction is significant by likelihood-ratio test (chi2 = 28.79, df = 2, p = 5.6e-7). AIC falls from 834.9 without the interaction to 810.1 with it. Survival by Sex and Pclass cell:

| Cell | n | Survived | Rate |
|---|---|---|---|
| Female, class 1 | 94 | 91 | 96.8% |
| Female, class 2 | 76 | 70 | 92.1% |
| Female, class 3 | 144 | 72 | 50.0% |
| Male, class 1 | 122 | 45 | 36.9% |
| Male, class 2 | 108 | 17 | 15.7% |
| Male, class 3 | 347 | 47 | 13.5% |

Female survival is high in classes 1 and 2 and falls to 50.0% in class 3. Male survival is lower in every class. The narrative comparing how steeply each sex's survival falls across classes is subject to an unresolved review issue (see Limitations).

![Survival rate (%) by Pclass for female and male passengers](tasks/stat_2/charts/stat2_rate_by_sex_pclass.png)

**Sex x Age.** In the complete-case sample (n = 714), the Sex x Age interaction is significant by likelihood-ratio test (chi2 = 11.90, df = 1, p = 5.6e-4). The male age slope is -0.057 log-odds per year and the female slope is -0.007. The male-minus-female log-odds gap is -2.16 at age 20 and -4.15 at age 60, so the sex gap widens with age.

### Embarked after adjustment for Pclass and Fare

- **Port C versus S, adjusted:** OR 1.68 (95% CI 1.14 to 2.46), p = 0.008, n = 889 with 340 survivors. The unadjusted OR is 2.44 (95% CI 1.73 to 3.45), p = 4e-7. The Port C log-odds coefficient fell from 0.89 to 0.52 after adjustment. Part of the unadjusted Port C advantage reflects class mix and fare, but a significant effect remains.
- **Port Q versus S, unadjusted:** OR 1.26 (95% CI 0.77 to 2.04), p = 0.36.
- **Port Q versus S, adjusted:** OR 2.10 (95% CI 1.26 to 3.50), p = 0.004. The unadjusted and adjusted results point in different directions. The finding attributes this reversal to Port Q passengers being concentrated in class 3 (72 of 77). Port Q has only 2 passengers in class 1 and 3 in class 2, so its adjusted estimate is driven almost entirely by class 3 and has a wide CI.

### Missingness

- **Cabin:** 687 of 891 rows (77.1%) are missing Cabin. Survival is 30.0% when Cabin is missing and 66.7% when present (p = 6.7e-21). Missing Cabin is tied to class: 69.7% of missing-Cabin rows are Pclass 3 and 5.8% are Pclass 1 (p = 9.6e-122). The sex distribution among missing-Cabin rows is 68.4% male and 31.6% female, and this association is significant (p = 4.0e-5). Mean fare is 19.16 when Cabin is missing and 76.14 when present (Welch p = 8.0e-22).
- **Age:** 177 rows (19.87%) are missing Age. Survival is 29.4% when Age is missing and 40.6% when present (p = 0.0077). Missing Age is strongly tied to class: 76.8% of missing-Age rows are Pclass 3 and 17.0% are Pclass 1 (p = 9.9e-11). It is not significantly related to Sex (p = 0.119). Mean fare is 22.16 when Age is missing and 34.69 when present (Welch p = 6.5e-5).
- **Embarked:** Only 2 rows are missing Embarked. Both survived, against 38.3% of other rows. With n = 2 this is not reliable (p = 0.29). The class association (p = 0.044) is also weak evidence at n = 2. The fare comparison (mean 80.0 versus 32.1) gives a p-value that is not trustworthy, because the two missing-Embarked rows share one fare and the test rests on one group's variance.

![Survival rate for rows with vs without a missing Age or Cabin value](tasks/eda_2/charts/survival_by_missingness.png)

**Missingness after adjustment for Pclass and Sex (logistic regression):**

- **Age missing:** unadjusted OR 0.61 (95% CI 0.43 to 0.87), p = 0.006. Adjusted for Pclass and Sex, OR 0.86 (95% CI 0.55 to 1.33), p = 0.50. The association is no longer significant after adjustment. The attenuation is consistent with class and sex accounting for the association, but this is not proven.
- **Cabin missing:** unadjusted OR 0.21 (95% CI 0.15 to 0.30), p < 0.001. Adjusted for Pclass and Sex, OR 0.52 (95% CI 0.30 to 0.90), p = 0.019. The association remains significant after adjustment.
- **Joint model (both missingness indicators with Pclass and Sex):** Cabin missing OR 0.52 (95% CI 0.30 to 0.90), p = 0.020. Age missing OR 0.87 (95% CI 0.56 to 1.36), p = 0.548.

### Predictive models

Models used median-imputed Age and one-hot Sex and Embarked, trained on 668 passengers and tested on a stratified 223-passenger test set.

| Model | Test accuracy | Precision | Recall | F1 | ROC AUC | Train accuracy |
|---|---|---|---|---|---|---|
| Majority-class baseline | 61.4% | – | – | – | – | – |
| Logistic regression | 77.1% | 0.711 | 0.686 | 0.698 | 0.841 | 81.1% |
| Random forest | 79.8% | 0.781 | 0.663 | 0.717 | 0.826 | 91.8% |

![Test accuracy of the majority-class baseline, logistic regression and random forest](tasks/ml_1/charts/ml1_model_accuracy.png)

Logistic regression ranks better on ROC AUC and the forest is slightly better on F1. The two models are close. The forest overfits: its training accuracy is 91.8% against 79.8% on the test set. Its test-accuracy gain over logistic regression (79.8% vs 77.1%) rests on one split and should not be read as a reliable difference between the models.

**Feature importance, which disagrees between methods:**

- **Logistic regression, permutation importance (drop in test ROC AUC, 30 repeats):** Sex 0.2154 (sd 0.0321), Pclass 0.0842 (sd 0.0201), Age 0.028 (sd 0.0115), SibSp 0.019 (sd 0.0064), Fare 0.002 (sd 0.004), Parch 0.0018 (sd 0.001), Embarked -0.0004 (sd 0.0051).
- **Random forest, impurity-based importance:** Fare 0.2212, Sex male 0.2008, Age 0.1855, Sex female 0.1777, Pclass 0.1014, SibSp 0.0413, Parch 0.0361, Embarked S 0.0161, Embarked C 0.0128, Embarked Q 0.0072.

These two rankings disagree on Fare and Age. The forest's impurity importance puts Fare first and Age third, while permutation importance on the logistic regression puts Fare near zero and Age third. Both are reported as they stand. One untested hypothesis is that impurity-based importance may favour continuous features with many split points. This was not tested, and permutation importance on the forest itself would be needed to check it.

Embarked has essentially no permutation importance in the logistic regression. This does not match the inferential result above, where Port C remains associated with survival after adjustment. The two analyses answer different questions, and this report does not reconcile them.

## Limitations

- **Unresolved review issue, stat_2 finding 2.** The lead's objection stands. The finding still contains a retracted sentence about the class 1 to class 3 drop, which the lead asked to be removed. The required clean replacement statement has not been made in the accepted text. This report omits the retracted sentence and gives only the cell rates, which match the accepted data. The narrative on how steeply male and female survival fall across classes is affected and is not relied on here.
- **Small groups.** SibSp groups of 5 and 8 (n = 5 and 7), Parch groups of 3 to 6 (n = 1 to 5), and the two passengers missing Embarked are too small for reliable rates. The SibSp and Parch chi-square approximations are less reliable because of sparse cells.
- **Port Q adjusted estimate.** It rests on 77 passengers, mostly in class 3, and has a wide CI. Port C is the more reliable adjusted result.
- **Missing Embarked fare test.** The Welch p-value for the two missing-Embarked rows is not trustworthy, as stated above.
- **Age in models and interaction tests.** Logistic regression used median-imputed Age. The Sex x Age interaction used only complete-case rows (n = 714). Missing Age is non-random with respect to class and fare, so both treatments may bias the results. Imputation by Pclass and Title was not tested.
- **Adjustment limits.** Pclass enters the cabin and age missingness models as a single numeric term, and Sex as a single binary term. The adjustment may not fully capture class effects. This matters most for Cabin, since 69.7% of Cabin-missing rows are class 3, so the residual Cabin effect may be partly confounded by class.
- **Single split.** Model comparisons and the forest-versus-logistic difference come from one stratified split and one forest fit. Repeated cross-validation was not run.
- **Associational results.** All findings describe associations in this sample. The analyses do not establish causes.
- **Failed tasks.** None. All seven tasks completed.

## Open questions

- Does the Sex x Pclass interaction hold after adjusting for Fare and Embarked, and after adding family size (SibSp/Parch)?
- Is the Sex x Age interaction driven by a few age bands? A binned-age check was proposed but not run.
- Do the small-family survival gains (SibSp and Parch) persist once Sex and Pclass are controlled for, or are they driven by sex and class mix?
- How much of the Fare difference between survivors and non-survivors is explained by Pclass?
- Does Embarked add anything once Pclass and Fare are controlled for in the predictive model, given that the inferential and permutation results differ?
- Is there a Pclass x Embarked interaction, and does the Port C effect differ across classes? Does the Port Q adjusted effect hold within class 3 alone?
- Does the random forest's Fare and Age importance hold under permutation importance on the forest itself?
- Do the model comparison and the accuracy difference between the two models (79.8% vs 77.1%) hold across repeated cross-validation?
- Is Cabin missingness informative beyond class? Does the deck letter, where present, relate to survival and fare?
- Does Age imputation by Pclass and Title reduce bias from non-random Age missingness?
- Does the Cabin_missing association hold when Pclass is entered as categorical dummies rather than a linear term?
- Does the Age_missing association differ by Sex or Pclass?
- Do the two passengers missing Embarked share a ticket or cabin pattern?