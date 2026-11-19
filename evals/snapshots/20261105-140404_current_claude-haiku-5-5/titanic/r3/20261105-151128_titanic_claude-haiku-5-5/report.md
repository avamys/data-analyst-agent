# Titanic Dataset: What Drove Survival

## Summary

- **Sex was the strongest association with survival.** Women survived at 74.2% (314 passengers) and men at 18.9% (577), against an overall rate of 38.4%. The odds ratio is 12.35 (95% CI 8.90 to 17.14), and Cramér's V is 0.543.
- **Survival fell with passenger class and rose with fare.** Survival was 63.0% in Pclass 1, 47.3% in Pclass 2 and 24.2% in Pclass 3. Fare was higher for survivors (median 26.0 vs 10.5). After adjusting for Sex, Pclass and Age, the Fare association disappeared (OR 1.00 per 10 units, p = 0.99). Embarkation at Cherbourg stayed significant after adjustment (OR 1.78, p = 0.016).
- **Sex interacts with both Pclass and Age.** Women's survival fell from 96.8% in Pclass 1 to 50.0% in Pclass 3, while men's fell from 36.9% to 13.5% (LR χ² = 33.86, df 2, p = 4.4e-8). A separate Sex × Age interaction was also significant (p = 0.00056), though it uses the 714 passengers with recorded Age.
- **Logistic regression beat the majority-class baseline on the held-out test set.** Its test accuracy was 0.8212 against a baseline of 0.6145, with ROC AUC 0.8445. The random forest scored slightly lower on test (accuracy 0.8045, AUC 0.8385) and overfit (train accuracy 0.9129). Sex was the most important feature in both models.
- **Missingness:** Cabin-missing passengers had lower survival, and this held after adjusting for Pclass and Sex (OR 0.52, p = 0.020). The estimate weakened in the Age-present subsample (p = 0.061). Age-missingness was not significantly associated with survival after adjustment (OR 0.87, p = 0.548).

## Data

- **Size:** 891 rows × 12 columns.
- **Target:** `Survived`, binary. 38.4% survived (1) and 61.6% did not (0).
- **Features used:** Pclass, Age, SibSp, Parch, Fare (numeric); Sex, Embarked (categorical). There are no date or time features.
- **Not used as features:** PassengerId, Ticket, Cabin and Name. Cabin was used only in the missingness analysis.
- **Missing values:** Age 19.9% (177 rows), Cabin 77.1% (687 rows), Embarked 0.2% (2 rows).

## Findings

### 1. Group survival rates (EDA)

- **Sex:** female 74.2% (314 passengers), male 18.9% (577), overall 38.4%.
- **Pclass:** 1st 63.0% (216), 2nd 47.3% (184), 3rd 24.2% (491).
- **Fare quartiles:** Q1 (0 to 7.9) 19.7% (223); Q2 (7.92 to 14.45) 30.4% (224); Q3 (14.46 to 31.0) 45.5% (222); Q4 (31.28 to 512.33) 58.1% (222).
- **Embarked:** Cherbourg (C) 55.4% (168), Queenstown (Q) 39.0% (77), Southampton (S) 33.7% (644). The 2 passengers with missing Embarked both survived.
- **Age bins:** under 16 at 59.0% (83); 16–32 at 36.2% (345); 32–48 at 40.1% (197); 48+ at 41.6% (89); missing Age at 29.4% (177).

![Survival rate by Sex and by Pclass, with overall rate 38.4% (dashed)](tasks/eda_1/charts/survival_rate_by_sex_pclass.png)

### 2. Significance tests and effect sizes

- **Sex:** χ² = 263.05 (1 df), p = 3.7e-59, Cramér's V = 0.543.
- **Pclass:** χ² = 102.89 (2 df), p = 4.5e-23, Cramér's V = 0.340.
- **Embarked:** χ² = 29.67 (3 df), p = 1.6e-6, Cramér's V = 0.183. The 2 missing-Embarked passengers form their own group in this test.
- **Female vs male:** OR 12.35 (95% CI 8.90 to 17.14). Risk difference 0.553 (95% CI 0.495 to 0.611), i.e. 55 percentage points higher survival for women.
- **First vs third class:** OR 5.31 (95% CI 3.76 to 7.50).
- **Fare:** Mann-Whitney p = 4.6e-22, with medians of 26.0 (survivors) and 10.5 (died). Welch t = 6.84, p = 2.7e-11, Cohen's d = 0.505. Mean fare was 48.40 for survivors and 22.12 for those who died (95% CI for the difference 18.75 to 33.81).
- **Age:** The two tests disagree. Welch t = −2.05, p = 0.041, Cohen's d = −0.157, with mean age 28.34 (survivors) vs 30.63 (died). The 95% CI for the difference is −4.47 to −0.10 years. The Mann-Whitney test gives p = 0.16, with medians of 28.0 in both groups. The evidence for an age difference is weak and depends on the test used.

The Sex gap holds within each class. Survival for women was 96.8% in Pclass 1, 92.1% in Pclass 2 and 50.0% in Pclass 3. For men it was 36.9%, 15.7% and 13.5%.

![Survival rate by passenger class and sex](tasks/stat_1/charts/stat1_survival_pclass_sex.png)

### 3. Interactions: Sex × Pclass and Sex × Age

**Sex × Pclass.** Survival by Sex and Pclass, with counts from all 891 rows (survivors / n):

| Pclass | Women | Men |
|---|---|---|
| 1 | 96.8% (91 / 94) | 36.9% (45 / 122) |
| 2 | 92.1% (70 / 76) | 15.7% (17 / 108) |
| 3 | 50.0% (72 / 144) | 13.5% (47 / 347) |

- In a logistic regression controlling for Age (n = 714 complete cases), the Sex × Pclass interaction gives LR χ² = 33.86, df 2, p = 4.4e-8.
- The female × Pclass 3 term is −2.19 (p = 0.001). The female × Pclass 2 term is 0.67 (p = 0.41, not significant).
- The female main effect is 3.64 log-odds in Pclass 1. The female advantage over men therefore shrinks to about 1.4 log-odds in Pclass 3.
- The class gradient is steeper for women than for men.
- The result rests mainly on the third-class contrast, since the Pclass 2 term is not significant.

![Survival rate by Pclass for each Sex](tasks/stat_2/charts/stat2_rates_pclass_sex.png)

**Sex × Age.** On complete cases (n = 714), the LR χ² is 11.90 (df 1, p = 0.00056), and the interaction coefficient is +0.050 per year (p = 0.00074). The age-related decline is weaker for women than for men.

- For men, the Age slope from the logit model (adjusted for Pclass) is −0.057 log-odds per year (95% CI −0.077 to −0.037, p = 1.6e-8).
- The female slope is not reported as a separate test. It equals the men's slope plus the interaction term, and no test is given for it. The claim of almost no Age effect for women is therefore weaker than the men's result.
- These estimates exclude the 177 passengers with missing Age.

### 4. Adjusted associations for Fare and Embarked

- **Fare:** the crude OR per 10 currency units is 1.16 (95% CI 1.11 to 1.22, p < 0.001). After adjusting for Sex, Pclass and Age (main effects only), it is 1.00 (95% CI 0.96 to 1.04, p = 0.99). This holds in both the full model (n = 891) and the refit without the 2 missing-Embarked passengers (n = 889). The result is limited to this additive specification and does not rule out interactions. Because the Sex × Pclass and Sex × Age interactions are significant, Fare's effect could differ by group.
- **Embarked C:** the crude OR versus S is 2.44 (p = 4.1e-7). In the refit (n = 889), the adjusted OR is 1.78 (95% CI 1.11 to 2.83, p = 0.016). The full model with the separated missing-Embarked indicator gives the same 1.78. The refit is the cleaner specification.
- **Embarked Q:** the crude OR versus S is 1.26 (p = 0.36, not significant). In the refit, the adjusted OR is 1.99 (95% CI 1.02 to 3.87, p = 0.043). This is borderline, rests on a small number of Q passengers, and should be treated cautiously.
- **Other covariates in the refit (n = 889):** female OR 12.93 (95% CI 8.92 to 18.75); Pclass 2 vs 1 OR 0.38 (95% CI 0.21 to 0.67, p = 0.0008); Pclass 3 vs 1 OR 0.10 (95% CI 0.06 to 0.18, p < 0.001); Age OR 0.967 per year (95% CI 0.953 to 0.982, p < 0.001); missing-Age indicator OR 0.72 (95% CI 0.45 to 1.18, p = 0.19).

### 5. Missingness

- **Missing counts:** Age 177 of 891 (19.9%); Cabin 687 (77.1%); Embarked 2 (0.2%).
- **Age-missing vs survival:** 29.4% of rows with missing Age survived, against 40.6% of rows with Age present (χ² p = 0.0077). A Welch t-test on Survived gives p = 0.0042.
- **Cabin-missing vs survival:** 30.0% (687) survived, against 66.7% (204) with Cabin recorded (χ² p = 6.7e-21).
- **Embarked-missing vs survival:** both of the 2 passengers survived. The test is not significant (p = 0.286), and with n = 2 it is not informative.

![Survival rate for passengers with vs without a recorded Age (left) and Cabin (right); rate = share of passengers who survived](tasks/eda_2/charts/missingness_survival_rates.png)

- **Age-missingness by class:** 13.9% of Pclass 1 (216), 6.0% of Pclass 2 (184) and 27.7% of Pclass 3 (491). Pclass χ² p = 9.9e-11.
- **Age-missingness by sex:** 16.9% of women (314) and 21.5% of men (577). The sex difference is not significant (p = 0.119).
- **Other differences:** Age-missing and Age-present passengers also differ on Fare (Welch p = 6.5e-5) and Pclass (Welch p = 6.8e-8).

**Adjusted missingness associations** (logit of Survived on the missingness flags, Pclass and female; n = 891):

- **Age-missing:** OR 0.87 (95% CI 0.56 to 1.36), p = 0.548. Not significant.
- **Cabin-missing:** OR 0.52 (95% CI 0.30 to 0.90), p = 0.020. Significant at 5%, so Cabin-missing passengers had lower adjusted odds of survival.
- **Sensitivity, Age-present rows only (n = 714, no Age flag):** Cabin-missing OR 0.56 (95% CI 0.31 to 1.03), p = 0.061. The direction matches, but the estimate is less precise and not significant at 5%.

The crude Age-missing association (p = 0.0077) is not significant after adjustment for Pclass and Sex. Age-missingness differs significantly by Pclass (p = 9.9e-11), and the stat_4 reconciliation attributes the attenuation mainly to that difference. The stat_3 model, which median-imputed Age and used n = 889, gave an Age-missing OR of 0.72 (p = 0.19). That is a different coding and sample, but both analyses find no significant adjusted Age-missing effect.

### 6. Predictive models

- **Majority-class baseline:** always predicting "did not survive" gives test accuracy 0.6145. Survivors are 38.5% of the test set.
- **Setup:** stratified 80/20 split (random_state 42), with 712 training and 179 test rows and 10 features: Pclass, Sex_male, Age, Age_missing, SibSp, Parch, Fare, and Embarked dummies. PassengerId, Name, Ticket and Cabin are excluded.

| Model | Train acc. | Test acc. | Test F1 | Test ROC AUC |
|---|---|---|---|---|
| Logistic regression (standardized) | 0.8034 | 0.8212 | 0.7460 | 0.8445 |
| Random forest (500 trees, min_samples_leaf 2) | 0.9129 | 0.8045 | 0.7244 | 0.8385 |

- Both models beat the baseline. Logistic regression has precision 0.8246 and recall 0.6812 on the test set. The random forest has precision 0.7931 and recall 0.6667.
- Logistic regression is slightly better than the random forest on every test metric. The test accuracy gap is 0.0167 on 179 test rows.
- The random forest overfits (train-test accuracy gap of about 0.11). Logistic regression shows no such gap.

**Feature importance.** The two models use different measures, so the rankings should be compared by order only.

- **Logistic regression (absolute standardized coefficient):** Sex_male 1.26, Pclass 0.92, Age 0.51, SibSp 0.26, Age_missing 0.18, followed by the Embarked dummies, Fare 0.09, Parch 0.09 and Embarked_C 0.05.
- **Random forest (impurity importance):** Sex_male 0.330, Fare 0.245, Age 0.185, Pclass 0.106, SibSp 0.044, Parch 0.035, and smaller values for the remaining features.
- **Random forest (permutation importance, drop in test ROC AUC, 30 repeats):** Sex_male 0.214, Pclass 0.043, Age 0.037, Fare 0.028, SibSp 0.008, Parch 0.005, and near zero for the Embarked dummies and Age_missing.

Sex_male ranks first in all three rankings. The two random forest measures disagree on Fare: impurity importance ranks it second, and permutation importance ranks it fourth. This disagreement is reported, not resolved.

![Test accuracy of logistic regression and random forest against always predicting did-not-survive](tasks/ml_2/charts/ml2_accuracy_vs_baseline.png)

## Limitations

- **Observational data:** all results are associations within this one dataset. The analysis makes no causal claims.
- **Missing Age:** 177 passengers (19.9%) lack Age. The Age tests and the Sex × Age interaction use only complete cases (n = 714). In the predictive models and the adjusted logit, Age was median-imputed, with a missing-Age flag.
- **Age test disagreement:** the Welch t-test (p = 0.041) and the Mann-Whitney test (p = 0.16) disagree on whether survivors and non-survivors differ in age. The Welch test excludes missing Age.
- **Embarked missingness:** only 2 passengers. Their indicator separated the data in the full adjusted model, so the refit without them (n = 889) is the reported specification.
- **Embarked Q:** the adjusted result (p = 0.043) is borderline and rests on a small number of Q passengers. The analysis advises a Firth or bootstrap check, which was not run.
- **Fare null result:** the adjusted Fare OR of 1.00 is for main effects only. It does not rule out Fare effects that vary by sex, class or age.
- **Female Age slope:** the female slope is not separately tested. The claim of almost no Age effect for women is weaker than the men's result.
- **Sex × Pclass result:** rests mainly on the third-class contrast. The Pclass 2 interaction term is not significant.
- **Cabin-missing result:** significant in the full model (p = 0.020) but not in the Age-present sample (p = 0.061). Its robustness is uncertain.
- **Random forest:** overfits (train 0.9129, test 0.8045). Its test scores are optimistic relative to generalization.
- **Imputation leak:** the Age median (28.0) and Embarked mode (S) were computed on the full dataset before the train/test split. This is acceptable for median and mode imputation but makes the test scores slightly optimistic.
- **Feature importance measures:** logistic coefficients and random forest importances are on different scales and should not be compared by magnitude.
- **Unresolved review issue (stat_2):** the lead asked that the survivor counts and totals for all six Sex × Pclass cells be stated, and that the female Age slope be flagged as not separately tested. The counts are given in Finding 3. The female slope test remains absent, so the claim about the Age effect for women is not separately supported.
- **Unresolved review issue (stat_4):** the lead asked that the reconciliation of the Age-missing association not describe Age-missingness as concentrated in males. The sex difference (16.9% vs 21.5%, p = 0.119) is not significant. The attenuation of the crude association is attributed to the significant Pclass difference in Age-missingness (p = 9.9e-11). The adjusted result (OR 0.87, p = 0.548, adjusted for Pclass and Sex) is kept as stated.
- **Failed tasks:** none. All analysis tasks are reported as complete.

## Open questions

- Does imputing Age by Pclass and Sex, rather than the global median, change the Age pattern or improve model accuracy?
- Does a multiple-imputation or sensitivity analysis confirm the Sex × Age interaction on all 891 passengers?
- Does Cabin missingness add predictive signal beyond Pclass and Sex in the models? Does its adjusted association hold after adding Fare or Embarked?
- Does Fare carry survival signal after controlling for Pclass, when Fare × Pclass and Fare × Sex interactions are tested?
- Does the Pclass × Sex interaction hold when Fare replaces Pclass, and with a different reference class?
- Do Sex effects differ by Embarked port?
- Is the Embarked Q association robust under Firth or bootstrap estimation?
- Does tuning the random forest (depth or min_samples_leaf) narrow its train-test gap without losing test accuracy?