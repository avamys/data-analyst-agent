# Titanic Survival: Which Passenger Attributes Predict the Survived Outcome?

## Summary

- **Sex and passenger class are the strongest associations with survival, and they interact.** Females survived at 74.2% against 18.9% for males. The Sex x Pclass interaction is significant (LR = 28.79 on 2 df, p = 5.6e-7). Female class 3 survival is 50.0%, far below the female class 1 (96.8%) and class 2 (92.1%) rates.
- **Models beat the majority-class baseline.** On the 179-row test split, logistic regression reached accuracy 0.8212 (baseline 0.6145) and ROC AUC 0.8448. The random forest reached accuracy 0.8156 and AUC 0.8293 but overfit. Sex is the dominant feature in both models.
- **Embarked is significant in the crude test but weaker after adjustment.** The adjusted likelihood-ratio test gives p = 0.023. Only the Cherbourg contrast is individually significant (adjusted OR 1.78, 95% CI 1.14 to 2.80). The joint effect has not been attributed to a port.
- **Missing Cabin is linked to lower survival after adjusting for Pclass and Sex (OR 0.40, p = 0.005). Missing Age is not (OR 0.95, p = 0.82).**
- **The is_alone effect depends on sex and on the covariates included.** For males, the Pclass-adjusted OR is 0.59 (CI 0.37 to 0.94). With Age, Fare and Embarked added, it is 0.78 (CI 0.47 to 1.30). The female estimate includes 1 in every model.

## Data

- **Size:** 891 rows × 12 columns.
- **Target:** Survived, a binary outcome. 342 passengers (38.4%) survived and 61.6% did not.
- **Features used:** Pclass, Age, SibSp, Parch, Fare, Sex, Embarked, and the derived family_size (SibSp + Parch + 1) and is_alone (family_size = 1).
- **Not used as features:** PassengerId, Ticket and Name, which are identifiers or free text. Cabin is used only as a missingness flag.
- **Missing values:** Cabin 77.1% (687 rows), Age 19.9% (177 rows), Embarked 0.2% (2 rows). All other columns are complete.
- **Date/time features:** none.

## Findings

### Overall and single-factor survival

- **Sex** is the strongest split. Females survived at 74.2% (n=314) and males at 18.9% (n=577). Chi-square is 263.1, p < 0.001, Cramér's V = 0.54, and the result holds after Holm correction. Males survived 55.3 percentage points less often (95% CI -61.1 to -49.5). Mean Fare is 44.5 for females and 25.5 for males.

  ![Survival rate by Sex and by Passenger class](tasks/eda_1/charts/survival_rate_by_sex_pclass.png)

- **Pclass** shows a steady decline. Survival is 63.0% in class 1 (n=216), 47.3% in class 2 (n=184) and 24.2% in class 3 (n=491). Chi-square is 102.9, p < 0.001, V = 0.34, significant after Holm correction. Class 1 exceeds class 3 by 38.7 points (95% CI 31.3 to 46.2).

- **Fare** is higher among survivors (Mann-Whitney p < 0.001, rank-biserial 0.38, significant after Holm correction). Survival by Fare quartile rises from 19.7% (Q1, mean Fare 7.0) to 30.4% (Q2), 45.5% (Q3) and 58.1% (Q4, mean Fare 88.7).

- **Family size** differs between survivors and non-survivors (Mann-Whitney p = 8e-7, rank-biserial 0.17, a small effect, significant after Holm correction).

- **is_alone** is associated with survival (chi-square 36.9, p < 0.001, V = 0.20, significant after Holm correction). This is a crude association and is not adjusted for Sex or Pclass.

- **Age** does not differ significantly between survivors and non-survivors (Mann-Whitney p = 0.16, rank-biserial -0.06, not significant after Holm correction). By bin, survival is 59.0% for passengers under 16 (n=83), 36.2% for ages 16–32 (n=345), 40.1% for 32–48 (n=197), 41.6% for 48+ (n=89), and 29.4% for missing Age (n=177).

- **Embarked:** Cherbourg has the highest crude survival (55.4%, n=168), followed by Queenstown (39.0%, n=77) and Southampton (33.7%, n=644). Chi-square is 26.5, p = 2e-6, V = 0.17, significant after Holm correction. Mean Fare is highest at Cherbourg (60.0), so the port difference may partly reflect class and fare mix (see the Embarked section below).

### Sex and Pclass, jointly

Survival by Sex x Pclass cell (survived/n):

| Cell | Survival | Count |
|---|---|---|
| Female, class 1 | 96.8% | 91/94 |
| Female, class 2 | 92.1% | 70/76 |
| Female, class 3 | 50.0% | 72/144 |
| Male, class 1 | 36.9% | 45/122 |
| Male, class 2 | 15.7% | 17/108 |
| Male, class 3 | 13.5% | 47/347 |

- The female-minus-male gap is 59.9 points in class 1, 76.4 points in class 2 and 36.5 points in class 3. It is largest in class 2 and is not a steady decline across classes.
- The Pclass gap is larger among females (46.8 points, class 1 vs class 3) than among males (23.3 points).
- The male class effect is mostly between class 1 and the other two classes. Male class 2 (15.7%) and class 3 (13.5%) are both low.
- Males are 577 of the 891 passengers and hold 109 of the 342 survivors. Most low-survival passengers are male, especially in class 3.
- The Sex x Pclass interaction is significant (LR = 28.79, 2 df, p = 5.6e-7).
- The Sex and class effects are not yet adjusted for Age, Fare or Embarked. Whether female class 3 survival is explained by Fare, Embarked or age mix is open.

![Survival rate for each Sex x Pclass cell (rates, not counts)](tasks/eda_3/charts/survival_rate_by_sex_pclass_cells.png)

![Survival rate (proportion of passengers who survived) by Sex and by Passenger class](tasks/stat_1/charts/stat1_survival_rate_sex_pclass.png)

![Survival rate by Sex within each passenger class](tasks/stat_2/charts/stat2_sex_pclass_rates.png)

### Embarked

- The crude association is significant (chi-square 26.5, p = 2e-6, Holm-adjusted p = 4e-6).
- After adjusting for Pclass, Sex and Fare (n=889, complete cases), the joint likelihood-ratio test is still significant but weaker: chi-square 7.52 on 2 df, p = 0.023. The crude result was chi-square 26.5, p = 2e-6, so part of the crude difference reflects class, sex and fare mix.
- Adjusted odds ratios against Southampton:
  - **Cherbourg:** OR 1.78 (95% CI 1.14 to 2.80, p = 0.012). Individually significant at 0.05.
  - **Queenstown:** OR 1.57 (95% CI 0.85 to 2.92, p = 0.15). Not significant.
- The joint test was not broken down by contrast. The results do not establish that Cherbourg drives the joint effect.

### Missingness

- **Age missing (n=177):** survival is 29.4%, against 40.6% for recorded Age (n=714). Crude chi-square is 7.11, p = 0.008. Missing Age is strongly tied to class: 76.8% of the missing-Age group is class 3, against 49.7% of the recorded group. Sex is not significantly related (p = 0.12).
- **Age missing, adjusted (stat_5):** after adjusting for Pclass and Sex, the association is not significant (OR 0.95, coefficient -0.05, p = 0.82). The age-only model gives OR 0.87 (p = 0.55). The standardised gap is -2.0 points against a raw gap of -11.2 points. No interval or test was computed on this gap, so the residual difference is not quantified beyond its point estimate.
- **Cabin missing (n=687):** survival is 30.0%, against 66.7% for recorded Cabin (n=204). The missing group is 69.7% class 3 and 5.8% class 1. Pclass, Sex and Survived are all significantly related to cabin missingness.
- **Cabin missing, adjusted (stat_5):** the penalty persists after adjusting for Pclass and Sex. The cabin-only model gives OR 0.40 (coefficient -0.93, p = 0.004). With both indicators, OR 0.40 (p = 0.005). The standardised gap is -14.8 points against a raw gap of -36.7 points, so about 40% of the raw gap remains.
- **Stratum-level rates (stat_5):** the cabin-missing gap is visible in several strata. For example, male class 2 is 66.7% with a recorded Cabin (n=6) against 12.7% without (n=102). These cells are small (see Limitations).

![Survival rate within Pclass x Sex strata, Age recorded vs Age missing](tasks/stat_5/charts/stat5_age_missing_strata.png)

![Survival rate within Pclass x Sex strata, Cabin recorded vs Cabin missing](tasks/stat_5/charts/stat5_cabin_missing_strata.png)

- **Embarked missing (n=2):** no test of its relation to other columns or to survival has power. The two rows are both class 1 females with Fare 80, and both survived. This is descriptive only.

### Is_alone within sex

Two analyses disagree on the strength of the male is_alone effect. Both are reported here without resolving the difference.

- **Unadjusted:** among females, survival is 78.6% when alone (n=126) and 71.3% when not alone (n=188). Among males, it is 15.6% when alone (n=411) and 27.1% when not alone (n=166). The Sex x is_alone interaction is significant (LR = 9.88, 1 df, p = 0.0017). This is unadjusted for Pclass.
- **Adjusted for Pclass (stat_4):** the interaction remains (LR = 7.66, 1 df, p = 0.0056). For males, the crude OR is 0.50 (95% CI 0.32 to 0.77) and the Pclass-adjusted OR is 0.59 (95% CI 0.37 to 0.94). For females, the adjusted OR is 1.64 (95% CI 0.94 to 2.86), which includes 1.
- **Adjusted for Pclass, Age, Fare and Embarked (stat_6, 889 rows):** the interaction is LR = 4.28 on 1 df, p = 0.038. The male OR is 0.78 (95% CI 0.47 to 1.30), which includes 1. The female OR is 1.75 (95% CI 0.97 to 3.14), also including 1. At the same 889 rows, the Pclass-only male OR is 0.59 (0.37 to 0.94).
- **The stat_6 result is not directly comparable with stat_4.** It adds Age, Fare and Embarked, so the male effect is attenuated and no longer clear. The Pclass-only result (OR 0.59) is below the fully adjusted result (OR 0.78), and the two intervals overlap widely. Whether Fare or Age drives the change is open.

Stratum-specific survival, unadjusted (stat_4, stat_6):

- Females, alone vs not alone: class 1 97.1% (n=34) vs 96.8% (n=60); class 2 90.6% (n=32) vs 93.2% (n=44); class 3 61.7% (n=60) vs 41.7% (n=84).
- Males, alone vs not alone: class 1 33.3% (n=75) vs 42.6% (n=47); class 2 9.7% (n=72) vs 27.8% (n=36); class 3 12.1% (n=264) vs 18.1% (n=83).

Female survival is near ceiling in classes 1 and 2, which limits the is_alone contrast there. The class 3 cells carry most of the female information, and the wide female interval mainly reflects them.

Pooled over sexes (unadjusted for Sex): class 1 survival is 72.9% when not alone (n=107) and 53.2% when alone (n=109). Class 2 survival is 63.7% (n=80) and 34.6% (n=104). This pooled comparison cannot rule out sex confounding.

![Survival rate by Sex and is_alone within each Pclass (unadjusted cell rates)](tasks/stat_4/charts/stat4_alone_by_sex_pclass.png)

![Adjusted odds ratios for is_alone by Sex, with 95% CIs, from logistic models with and without Age, Fare and Embarked (n=889)](tasks/stat_6/charts/stat6_alone_or_forest.png)

### Predictive models (stratified 80/20 split, test n=179)

| Model | Accuracy | ROC AUC | F1 | Train accuracy |
|---|---|---|---|---|
| Majority-class baseline | 0.6145 | — | — | — |
| Logistic regression | 0.8212 | 0.8448 | 0.746 | 0.8034 |
| Random forest | 0.8156 | 0.8293 | 0.7481 | 0.9831 |

- Both models beat the baseline. Logistic regression ranks slightly higher on AUC, and the two are tied on F1.
- The random forest overfits (train 0.9831 against test 0.8156), so its test metrics are less reliable. Logistic regression shows no comparable gap.
- **Permutation importance (drop in test ROC AUC):**
  - Logistic regression: Sex 0.2120 (sd 0.0391), Pclass 0.0915 (sd 0.0188), Age 0.0270 (sd 0.0085). The other features are below 0.01.
  - Random forest: Sex 0.2022 (sd 0.0338), Age 0.0379 (sd 0.0114), Pclass 0.0278 (sd 0.0102), Fare 0.0226 (sd 0.0132).
- After Sex, the order differs by model. Age ranks second in the random forest, but its model importance is conditional on the other features and does not match its non-significant crude association.
- Fare's rank depends on the model: fourth in the random forest, near zero in logistic regression.
- Permutation means for SibSp, Parch, family_size, Embarked and age_missing are close to zero, and their signs vary across repeats. None is clearly distinguishable from zero on a 179-row test set.
- Random forest impurity importance (Fare 0.2537 first, then Age 0.2236) does not match the permutation ranking. The two measures are different and are not reconciled here.

![Permutation importance of each feature for the random forest, measured as the drop in test ROC AUC](tasks/ml_1/charts/ml1_perm_importance.png)

## Limitations

- **Observational data.** All results are associations. The tasks make no causal claims, and nothing here establishes mechanisms.
- **Small cells.** Several strata are very small: Age-missing cells of 2 to 9 rows in classes 1 and 2, and recorded-Cabin cells of 6 to 10 rows outside class 1. Within-stratum contrasts in those cells are unstable.
- **Missing data.** Cabin is 77.1% missing and was used only as a flag. Age is 19.9% missing. The adjusted Age results use median imputation with a missing indicator (stat_6). The adjusted Embarked and interaction results use complete cases (n=889).
- **Test set size.** Model scores come from a 179-row test set. Permutation importances for the small features are not distinguishable from zero.
- **Random forest overfitting.** Its test metrics are less reliable than logistic regression's.
- **Unconverged 891-row model (stat_6, partial).** The 891-row full model did not converge under Newton. Its interaction (LR 4.28, p = 0.038) and ORs are unverified. The 889-row result reproduces the same estimates by construction, because the two missing-Embarked rows are the only difference. It is not an independent check. The stat_6 task is partial.
- **Attenuation of the male is_alone effect is unexplained.** The male OR moves from 0.59 (Pclass only) to 0.78 (with Age, Fare and Embarked). Whether Fare or Age drives this is not established.
- **Unresolved review issue (stat_4).** The lead's objection still stands and affects the stat_4 findings on the female is_alone rates and the labelling of within-class rates:
  - The female paragraph must state that female survival in classes 1 and 2 is near ceiling (96.8% and 93.2%), which limits the is_alone contrast there. The wide female interval mainly reflects the class 3 cells. The claim that the imprecision is "not because female survival is uniformly high" must be removed. The stat_6 rewrite of this paragraph is used above.
  - Within-class male and female rates must be labelled as unadjusted stratum-specific rates, not "Pclass-adjusted survival". This report uses that labelling.
  - The pooled within-class comparison is unadjusted for Sex and cannot rule out sex confounding. This is stated above.
- **Embarked joint test not decomposed.** The Cherbourg contrast is significant, but the joint test (p = 0.023) has not been broken down by port. Attribution to Cherbourg is not established.
- **Age and survival.** Age is not significant crude (p = 0.16), yet it ranks second in both models' importance. These two results are reported as they stand and have not been reconciled.
- **Derived features.** family_size = SibSp + Parch + 1 and is_alone are not independent of SibSp and Parch. Their individual permutation importances understate the joint contribution of family structure.

## Open questions

- Does the Sex x Pclass pattern hold after adjusting for Age, Fare and Embarked, or is female class 3 survival (50.0%) explained by Fare, Embarked or age mix?
- Is the Sex x Pclass interaction with Age and Fare in the model still significant? This was not tested.
- Which port drives the joint Embarked effect? Does the Cherbourg advantage persist within each class? Does Embarked interact with Sex or Pclass?
- Does the male is_alone effect hold after adjustment for Age, Fare and Embarked when the 891-row model converges? Is the attenuation from 0.59 to 0.78 driven by Fare or by Age?
- Is the female class 3 is_alone pattern (61.7% alone vs 41.7% not alone) explained by Fare, Age or Embarked?
- Is the male is_alone effect concentrated in class 2, given the small male class 1 and class 2 cells?
- Do Age and Cabin missingness overlap, and does the Age effect change once Cabin is in the model?
- Does the cabin-missing penalty hold within class 2 and class 3 separately?
- Is the residual cabin-missing association a proxy for deck or location information that Pclass does not capture? The data do not contain this information.
- Would a grouped permutation of family_size, SibSp and Parch give a clearer estimate of family-structure value?
- Does Age have a non-linear effect (for example, children vs adults) that the whole-sample rank test misses?
- Can Age be imputed from Pclass, Sex and name titles without biasing the survival estimates?