# Titanic Survival: Factors Associated with the Survived Target (891 Passengers)

## Summary

- **Sex and passenger class are the strongest associations with survival.** 74.2% of 314 females survived against 18.9% of 577 males (chi-square p = 3.7e-59, Cramér's V = 0.543; female odds 12.35 times male odds). Survival fell from 63.0% in class 1 to 24.2% in class 3. The Sex × Pclass interaction is significant (LR = 28.79, df 2, p = 5.6e-7): females in classes 1 and 2 survived at 96.8% and 92.1%, while males in classes 2 and 3 survived at 15.7% and 13.5%.
- **Family structure and fare are also significantly associated with survival, and the Embarked effect remains after adjusting for Pclass.** Travelling alone has odds ratio 0.43 against not travelling alone. Mean fare was 48.4 for survivors and 22.1 for those who died (Cohen's d = 0.505). Port C's advantage over S holds after adjusting for Pclass (odds ratio 1.92, Wald p = 0.0008), though this conclusion adjusts for Pclass only.
- **Models beat the majority-class baseline (61.5% test accuracy) but perform about equally.** Logistic regression reached 80.5% accuracy and ROC AUC 0.849; the default random forest reached 81.0% and 0.843. A tuned random forest reached the highest test accuracy (82.7%) but not the highest ROC AUC (0.844). Gradient boosting had the lowest ROC AUC (0.824). Test-set differences are within noise on 179 rows, and the model comparison has an unresolved feature-set issue (see Limitations).
- **The 22–25 Age bin pattern does not hold with observed Age only.** Age was missing for 177 rows (19.9%), and these passengers survived at 29.4% against 40.6% for observed-Age passengers. The 22–25 bin at 21.3% (all rows) is 37.1% with observed Age only. Among observed-Age passengers, the Age difference between survivors and non-survivors is not significant after Holm correction (adjusted p ≈ 0.082).

## Data

- **Size:** 891 rows × 12 columns.
- **Target:** `Survived` (binary). 38.4% positive (survived), 61.6% negative (died).
- **Features used:** Pclass, Age, SibSp, Parch, Fare (numeric); Sex, Embarked (categorical). Derived family variables (family_size, is_alone) were used in the models. PassengerId, Name, Ticket and Cabin were not used as raw features.
- **No date or time features.**
- **Missing values:**
  - Age: 177 of 891 rows (19.9%). Imputed with the median of Pclass and Sex before binning and modelling.
  - Cabin: 687 of 891 rows (77.1%). Not used except through missingness analysis.
  - Embarked: 2 rows (0.2%). Filled with the mode, S, before analysis.

## Findings

### 1. Survival rates by group

**Sex.** Females: 74.2% of 314 survived. Males: 18.9% of 577 survived. Overall: 38.4%.

![Survival rate by sex: percent of passengers surviving per group](tasks/eda_1/charts/surv_by_sex.png)

**Passenger class.** Class 1: 63.0% (n = 216). Class 2: 47.3% (n = 184). Class 3: 24.2% (n = 491).

![Survival rate by passenger class: percent of passengers surviving per group](tasks/eda_1/charts/surv_by_pclass.png)

**Embarkation port.** C: 55.4% (n = 168). Q: 39.0% (n = 77). S: 33.9% (n = 646). Two rows with missing Embarked were filled with S.

**Family structure.**
- SibSp: 34.5% with none (n = 608) against 53.6% with one (n = 209). Groups of 5 or 8 siblings/spouses (n = 12) all died.
- Parch: 34.4% with none (n = 678), 55.1% with one (n = 118), 50.0% with two (n = 80). Larger groups are small, with 1 to 5 passengers each.

**Fare quartiles.** 19.7% (fare up to 7.91, n = 223), 30.4% (7.91–14.45, n = 224), 45.5% (14.45–31.0, n = 222), 58.1% (above 31.0, n = 222). Fare is not affected by Age imputation.

![Survival rate by Fare quartile: percent of passengers surviving per group](tasks/eda_1/charts/surv_by_fare_quartile.png)

**Age.** Age bins using all rows (including imputed values) are not reliable and are not reported as a pattern. Using observed Age only (n = 714), survival by quartile is 45.8% (up to 20.1, n = 179), 36.1% (20.1–28.0, n = 183), 43.4% (28.0–38.0, n = 175) and 37.3% (38–80, n = 177). There is no strong monotone pattern. The observed-Age decile rates range from 28.4% to 58.4% with no consistent trend. See Section 5 for the imputation analysis.

### 2. Statistical tests and effect sizes

| Factor | Test | Result | Effect size |
|---|---|---|---|
| Sex | Chi-square (df 1) | χ² = 263.05, p = 3.7e-59 | Cramér's V = 0.543; OR female vs male = 12.35 (95% CI 8.90–17.14) |
| Pclass | Chi-square (df 2) | χ² = 102.89, p = 4.5e-23 | V = 0.340; OR class 1 vs 3 = 5.31 (3.76–7.50); class 2 vs 3 = 2.80 (1.97–4.00) |
| Embarked | Chi-square (df 2) | χ² = 25.96, p = 2.3e-6 | V = 0.171; OR C vs S = 2.42 (1.71–3.41); Q vs S = 1.25 (0.77–2.02), not distinguishable from no difference |
| SibSp (capped at 3) | Chi-square (df 3) | χ² = 35.43, p = 9.9e-8 | V = 0.199; OR one vs none = 2.19 (1.59–3.01) |
| Parch (capped at 3) | Chi-square (df 3) | χ² = 23.98, p = 2.5e-5 | V = 0.164; OR one vs none = 2.34 (1.58–3.48) |
| Alone | Chi-square (df 1) | χ² = 36.85, p = 1.3e-9 | V = 0.203; OR alone vs not alone = 0.43 (0.32–0.56) |
| Fare | Welch t = 6.84, p = 2.7e-11; Mann-Whitney p = 4.6e-22 | Means 48.4 (survived) vs 22.1 (died) | Cohen's d = 0.505 (medium); rank-biserial = 0.384 |
| Age (observed only) | Welch p = 0.041; Mann-Whitney p = 0.160 | Means 28.3 (survived, n = 290) vs 30.6 (died, n = 424) | Cohen's d = −0.157 (small) |

- **Multiple-testing correction.** Holm adjustment across the 10 tests (six chi-square, plus Welch and Mann-Whitney for Age and Fare) keeps all chi-square results and both Fare tests significant at 0.05. The Age tests do not survive correction (Welch adjusted p ≈ 0.082; Mann-Whitney adjusted p = 0.160).
- **Odds ratio chart.** Ratios above 1 mean higher survival odds than the reference group.

![Odds ratios of survival with 95% confidence intervals; ratios above 1 mean higher survival odds than the reference group](tasks/stat_1/charts/stat1_odds_ratios.png)

### 3. Interactions

**Sex × Pclass.** The interaction is significant (LR = 28.79, df 2, p = 5.6e-7). Survival by cell:

| Pclass | Female | Male |
|---|---|---|
| 1 | 96.8% (n = 94) | 36.9% (n = 122) |
| 2 | 92.1% (n = 76) | 15.7% (n = 108) |
| 3 | 50.0% (n = 144) | 13.5% (n = 347) |

- Odds ratios against the reference group (male, class 3): females in class 1 OR 193.6 (95% CI 58.9–636.8); females in class 2 OR 74.5 (30.6–181.1); females in class 3 OR 6.4 (4.1–10.0); males in class 1 OR 3.7 (2.3–6.0); males in class 2 OR 1.19 (0.65–2.18), which does not differ from class 3.
- The class gradient therefore differs by sex: among males, class 2 and class 3 are nearly equal.
- The very large female class 1 and 2 odds ratios rest on small cells. No exact or Firth-penalised model was fitted.

![Survival rate per Sex by Pclass cell](tasks/stat_2/charts/stat2_sex_pclass.png)

**Sex × Age band (child under 16 vs adult).** The interaction is significant on all rows (LR = 19.85, df 1, p = 8.4e-6) and on observed Age only (LR = 19.73, df 1, p = 8.9e-6).

| Cell | Survival | n |
|---|---|---|
| Female adults | 75.6% | 271 |
| Male adults | 16.4% | 537 |
| Female children | 65.1% | 43 |
| Male children | 52.5% | 40 |

- On observed Age only, female adults are 77.5% (n = 218) and male adults 17.4% (n = 413). Child counts are identical in both samples, so no imputed row is a child.
- Odds ratios against male adults: female adults 15.8 (11.1–22.7); female children 9.5 (4.9–18.6); male children 5.6 (2.9–10.9).
- Among children only, female vs male OR is 1.69 (95% CI 0.70–4.08), not distinguishable from no sex difference (n = 83 children: 43 female, 40 male).

### 4. Missingness and survival

- **Counts:** Age 177 (19.9%), Cabin 687 (77.1%), Embarked 2 (0.2%).
- **Age missing vs survival.** Survival is 29.4% when Age is missing (n = 177) against 40.6% when present (n = 714). Chi-square p = 0.0077; Welch t-test on Survived p = 0.0042.
- **Cabin missing vs survival.** Survival is 66.7% when Cabin is present (n = 204) against 30.0% when missing (n = 687). Chi-square p = 6.7e-21.

![Survival rate (percent surviving) for passengers with Age or Cabin recorded versus missing](tasks/eda_2/charts/missing_vs_survival.png)

- **Age missingness and class/sex.** Age missingness is strongly associated with Pclass (chi-square p = 9.9e-11) and not significantly associated with Sex (p = 0.119). Percent of Age missing by cell: class 1 female 9.6%; class 1 male 17.2%; class 2 female 2.6%; class 2 male 8.3%; class 3 female 29.2%; class 3 male 27.1%.
- **Confounding.** Both Age and Cabin missingness vary with Pclass and Sex, so the raw survival gaps by missingness are confounded with class and sex. They are not evidence of an independent effect of missingness on survival.
- **Embarked.** Missing for only 2 rows, too few to test or model.

### 5. Robustness of Age patterns to median imputation

- **The 22–25 bin.** With all rows, the bin shows 21.3% survival (n = 164). Of these, 94 have imputed Age and survive at 9.6%. The 70 with observed Age survive at 37.1%. The 37.1% sits within the observed-Age decile range (neighbours: 19–22 at 28.4%, n = 67; 25–28 at 39.3%, n = 61). The earlier 21.3% should not be cited as an Age pattern.

![Survival in the 22-25 Age bin split by observed vs median-imputed Age](tasks/eda_3/charts/eda3_bin_22_25_split.png)

- **All-rows quartiles.** Imputed rows fall in every all-rows quartile (42, 94, 20 and 21 imputed rows across the four bins, summing to 177). The shift in the quartile rates comes from the 94 imputed rows in the 21.5–26.0 bin, which has 24.9% survival. The nearest observed-Age quartile (20.1–28.0) has 36.1%. The all-rows quartile survival rates are 45.5% (0.4–21.5 bin) and 45.9% (26–36 bin), as recorded in the all-rows quartile table.
- **Imputed vs observed survival.** Imputed-Age rows survive at 29.4% against 40.6% for observed-Age rows (Section 4). Imputation places each row at the median of its Pclass and Sex group, so the low survival of imputed rows is not explained by this analysis. Whether it reflects their Pclass and Sex mix has not been tested.

### 6. Predictive models

**Setup.** Stratified 80/20 split, seed 42: 712 training rows, 179 test rows. Majority-class baseline test accuracy: 61.5%.

**Default models (ml_1).**

| Model | Train acc. | Test acc. | Test ROC AUC | Test F1 | Test precision | Test recall |
|---|---|---|---|---|---|---|
| Logistic regression (standardised) | 80.9% | 80.5% | 0.849 | 0.729 | 0.783 | 0.681 |
| Random forest (500 trees, min leaf 2) | 91.3% | 81.0% | 0.843 | 0.730 | 0.807 | 0.667 |

- The two models perform about equally. Test accuracy is 80.5% for logistic regression and 81.0% for the random forest; ROC AUC is 0.849 and 0.843. These differences are within noise on 179 rows and do not establish that one model is better.
- The random forest overfits (train 91.3% against test 81.0%). Logistic regression is stable.

**Feature importance, random forest.** Mean drop in test ROC AUC when one-hot groups are permuted jointly, averaged over 30 repeats:

- Sex 0.219; Age 0.032; Fare 0.031; Pclass 0.023; Embarked 0.011; family_size 0.010; SibSp 0.004; Parch 0.001; is_alone −0.003.

![Random forest permutation importance: mean drop in test ROC AUC per feature](tasks/ml_1/charts/ml1_rf_permutation_importance.png)

**Logistic regression standardised coefficients.** Pclass −0.97 (lower class, lower survival); Sex female +0.62; Age −0.56; SibSp −0.29; is_alone −0.28; family_size −0.22; Fare 0.08 (small once Pclass is in the model, although its random forest grouped importance is 0.031, so part of Fare's signal overlaps with Pclass). Parch −0.05; Embarked_C 0.03; Embarked_Q 0.11; Embarked_S −0.09.

- Family variables (family_size, SibSp, Parch, is_alone) are built from overlapping information. Their individual coefficients and importances are not separately interpretable. A joint family-group importance was not computed.
- Age in the models includes median-imputed values for 177 rows, so the Age importance and coefficient are not clean estimates of the Age effect.

**Gradient boosting and tuned forest (ml_2).** Same test split.

| Model | Train acc. | Test acc. | Test ROC AUC | Test F1 |
|---|---|---|---|---|
| Majority baseline | — | 61.5% | Not applicable | Not applicable |
| Logistic regression (carried over from ml_1) | 80.9% | 80.5% | 0.849 | 0.729 |
| Default random forest (carried over from ml_1) | 91.3% | 81.0% | 0.843 | 0.730 |
| Gradient boosting (default settings) | 90.9% | 80.5% | 0.824 | 0.720 |
| Tuned random forest | 87.6% | 82.7% | 0.844 | 0.744 |

- A constant predictor has no ranking, so ROC AUC and F1 are not applicable to the majority baseline.
- Tuned forest: grid search over max depth and minimum samples per leaf, using training data only, chose max depth none and minimum samples per leaf 5, with 5-fold CV ROC AUC of 0.875 on the training split. This is well above the tuned forest's test ROC AUC (0.844), and close to the default forest's test ROC AUC (0.843), so tuning did not improve held-out ranking.
- The tuned forest has the highest test accuracy (82.7% against 80.5% for logistic regression), but its ROC AUC is lower (0.844 vs 0.849) and its F1 is higher (0.744 vs 0.729). These differences are within noise on 179 rows. The tuned forest also overfits moderately (train 87.6%).
- Gradient boosting overfits strongly (train 90.9%, test 80.5%) and has the lowest test ROC AUC of the models compared.
- The ml_2 models are recorded as using 12 engineered columns (Pclass, Age, SibSp, Parch, Fare, family_size, is_alone, Sex_female, Sex_male, Embarked_C, Embarked_Q, Embarked_S). The printed column list was not recorded, so this is not confirmed (see Limitations).

![Test accuracy of majority baseline, logistic regression, default and tuned random forest, and gradient boosting on the shared 179-row test split](tasks/ml_2/charts/ml2_test_accuracy.png)

### 7. Embarked after adjusting for Pclass

- **Adjusted logit (Embarked, reference S, plus Pclass).** C vs S: coefficient 0.654, odds ratio 1.92, 95% CI on the log-odds scale 0.27 to 1.04, Wald p = 0.0008. Likelihood-ratio test for Embarked after adjusting for Pclass: χ² = 18.5, df 2, p = 0.0001.
- **Raw and adjusted rates.** Raw survival is 55.4% for C and 33.9% for S. Adjusted for Pclass and standardised to the full Pclass mix, the rates are 48.1% for C and 34.3% for S.
- **Port Q.** Adjusted survival is 52.2%, against 39.0% raw. This estimate rests on 77 Q passengers, 72 of them in class 3 (93.5%), and is model-dependent.
- **Disagreement with Section 2.** The unadjusted Q vs S comparison (odds ratio 1.25, CI 0.77–2.02) shows no distinguishable difference, while the Pclass-adjusted logit gives Q vs S odds ratio 2.32 (p = 0.0015). These two results disagree; the adjusted Q estimate depends on the model and on very few first-class and second-class Q passengers.
- **Within-class rates** (missing Embarked filled with S):
  - Class 1: C 69.4% (n = 85); S 58.9% (n = 129); Q n = 2 (50.0%, not interpretable).
  - Class 2: S 46.3% (n = 164); C 52.9% (n = 17); Q n = 3 (66.7%, not interpretable).
  - Class 3: C 37.9% (n = 66); Q 37.5% (n = 72); S 19.0% (n = 353).
- **Scope.** The port effect survives adjustment for Pclass only. It has not been checked against Sex or Age, which may also differ by port, so the adjusted C advantage should not be treated as a pure port effect.

![Percent surviving by Embarked (C, Q, S) within each passenger class; Q has only 2 passengers in class 1 and 3 in class 2, so those bars are unreliable](tasks/stat_3/charts/stat3_embarked_within_pclass.png)

## Limitations

- **Age imputation.** Age was median-imputed by Pclass and Sex for 177 rows (19.9%). Imputed rows survive less than observed-Age rows (29.4% vs 40.6%). Any all-rows Age bin, quartile or model coefficient therefore reflects the imputation as well as Age. Age is not significant among observed-Age passengers after Holm correction.
- **Cabin.** Cabin is 77.1% missing and was used only through its missingness. Its survival gap is confounded with Pclass and Sex. No Cabin-derived feature was built.
- **Embarked.** Two missing rows were filled with the mode (S). Port Q estimates rest on few first-class and second-class passengers (2 and 3, respectively).
- **Small cells.** Several odds ratios rest on small cells (for example, female class 1 OR 193.6, CI 58.9–636.8; child-by-sex cells of 40 to 43). No exact or Firth-penalised estimates were produced.
- **Adjustment scope.** Embarked was adjusted for Pclass only. The Sex × Pclass and Sex × Age interactions are analysed without adjusting for other factors, and Fare's association has not been tested after controlling for Pclass.
- **Associations, not causes.** All results are associations in this observational dataset.
- **Model evaluation.** The ml_1 and ml_2 comparisons use one stratified 80/20 split with 179 test rows. Differences between models of a few points are within noise. Repeated splits were not run; the only cross-validation was the training-data grid search for the tuned forest.
- **Unresolved review issue: ml_1 (permutation importance).** The standard deviation given for Embarked in the grouped permutation importance is not supported by any recorded fact, so it is not reported; only the mean (0.011) is given. The earlier statement that SibSp, Embarked and is_alone add almost nothing is too strong and is not made here: their coefficients are nonzero but shared with family_size, and no joint family-group importance was computed.
- **Unresolved review issue: ml_2 (feature set).** The exact column list the ml_2 models were trained on (the printed `list(X_train.columns)` output) was not recorded, so it cannot be confirmed that the carried-over ml_1 logistic regression and default random forest numbers were computed on the same feature set. The ml_2 comparison may therefore mix feature sets. The "not material" conclusion about the tuned forest's accuracy gain is tempered accordingly, and the claim that the earlier 10-feature list omitted Sex_male and Embarked_C is not stated. The majority-baseline ROC AUC and F1 are not applicable, as explained above.
- **Unresolved review issue: eda_3 (imputation explanation).** The all-rows quartile shift is attributed to the 94 imputed rows in the 21.5–26.0 bin, not to imputed rows in the middle quartiles. The 45.5% and 45.9% figures are stated only as all-rows quartile survival rates from the recorded quartile table.
- **Failed tasks.** None. All eight tasks (eda_1, stat_1, stat_2, eda_2, ml_1, ml_2, eda_3, stat_3) are recorded as complete.

## Open questions

- Does the Sex effect differ by passenger class after adjusting for other variables, and is the female class 1 and 2 odds ratio stable under an exact or Firth-penalised model?
- Is the child survival advantage among males (52.5% vs 16.4% or 17.4% for adult males, depending on sample) robust to the cutoff of 16?
- Does the Embarked effect hold after also adjusting for Sex and Age, since port C may differ in those too? Is the Q estimate stable?
- Is the low survival of imputed-Age rows (29.4% vs 40.6%) explained by their Pclass and Sex mix, or by the imputation itself? Does a model-based Age imputation (using Pclass, Sex, SibSp, Parch and Fare) change the Age pattern?
- Does the observed-Age survival pattern by Age hold after controlling for Sex and Pclass, for example with a logistic regression on observed rows only?
- Does Fare remain significant after controlling for Pclass?
- Does family_size add predictive value beyond SibSp, Parch and is_alone, tested by a joint family-group ablation?
- Does a cross-validated search over gradient boosting settings (learning rate, depth, subsampling) close the ROC AUC gap to logistic regression?
- Are the accuracy differences between the tuned forest and logistic regression stable across repeated stratified splits or cross-validation?
- Does adding an Age-missing indicator, or a family-group ablation, change which model ranks highest?