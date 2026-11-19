# Passenger Dataset: Analysis of the Survived Target

## Summary

- **Sex is the strongest association with survival.** 74.2% of female passengers survived against 18.9% of male passengers (chi-square 263.05, p = 3.7e-59, Cramér's V = 0.543).
- **Sex and Pclass interact.** The likelihood-ratio test gives chi-square 28.79 on 2 df (p = 5.6e-7). Survival falls steeply with class for women (96.8%, 92.1%, 50.0%) and much less for men (36.9%, 15.7%, 13.5%).
- **Embarked and Fare effects weaken after adjustment.** The Embarked C vs S odds ratio falls from 2.44 to 1.81 after adjusting for Pclass and Sex, and remains significant (p = 0.009). The Fare effect is not statistically supported after the same adjustment (OR per 10 units 1.02, 95% CI 0.98 to 1.06).
- **Predictive power is clearly above the majority-class baseline.** Logistic regression reaches 78.0% test accuracy and ROC AUC 0.839, against 61.4% accuracy for the majority-class baseline. A random forest reaches AUC 0.842, which is not clearly better than logistic regression.
- **Missingness is linked to class and survival.** Age-missing and Cabin-missing rows survive less often and are concentrated in lower classes. Within-class evidence is mixed for Age and rests mainly on Pclass 1 for Cabin.

## Data

- **Size:** 891 rows, 12 columns.
- **Target:** Survived (binary). 61.6% of passengers are 0 (549) and 38.4% are 1 (342).
- **Missing values:** Cabin 77.1% (687 rows), Age 19.9% (177 rows), Embarked 0.2% (2 rows). All other columns are complete.
- **Excluded as features:** PassengerId, Ticket, Cabin and Name. Cabin was used only as a missingness indicator. No title was extracted from Name.
- **Numeric features:** Pclass, Age, SibSp, Parch, Fare. **Categorical features:** Sex, Embarked. No date or time features.

## Findings

### Distribution of the target and single-feature survival rates

Overall, 38.4% of passengers survived.

- **Sex:** female 74.2% (n = 314); male 18.9% (n = 577).
- **Pclass:** class 1 63.0% (n = 216); class 2 47.3% (n = 184); class 3 24.2% (n = 491).
- **Sex within Pclass:** females 96.8%, 92.1% and 50.0% in classes 1, 2 and 3. Males 36.9%, 15.7% and 13.5%.

![Survival rate by Sex and Pclass](tasks/eda_1/charts/survival_rate_sex_pclass.png)

- **Embarked:** C 55.4% (n = 168); Q 39.0% (n = 77); S 33.7% (n = 644). The two passengers with missing Embarked both survived (n = 2), which is too few to test.
- **SibSp:** 0 siblings/spouses 34.5% (n = 608); 1 at 53.6% (n = 209); 2 at 46.4% (n = 28). Groups of 3 or more have 5 to 18 passengers each, with rates from 0% to 25%.
- **Parch:** 0 parents/children 34.4% (n = 678); 1 at 55.1% (n = 118); 2 at 50.0% (n = 80). Groups of 3 or more have 1 to 5 passengers each.
- **Age quartiles** (edges 0.42, 20.12, 28, 38, 80): Q1 45.8% (n = 179), Q2 36.1% (n = 183), Q3 43.4% (n = 175), Q4 37.3% (n = 177). Missing Age (n = 177) has the lowest rate, 29.4%.
- **Fare quartiles** (edges 0, 7.91, 14.45, 31, 512.33) rise monotonically: Q1 19.7% (n = 223), Q2 30.4% (n = 224), Q3 45.5% (n = 222), Q4 58.1% (n = 222).

### Statistical tests and effect sizes

Seven omnibus tests (three chi-square, four Mann-Whitney) were corrected with Holm. Sex, Pclass, Embarked, Fare, Parch and SibSp remain significant at 0.05 after correction. Age does not (Holm p = 0.16).

- **Sex:** chi-square 263.05 (df 1, n = 891), p = 3.7e-59, Cramér's V = 0.543 (large). Female minus male survival is 55.3 points (95% Wald CI 49.5 to 61.1).
- **Pclass:** chi-square 102.89 (df 2), p = 4.5e-23, Cramér's V = 0.340. Class 1 vs class 3 differs by 38.7 points (95% CI 31.3 to 46.2). Class 2 vs class 3 differs by 23.0 points (95% CI 14.9 to 31.2).
- **Embarked:** chi-square 26.49 (df 2, n = 889), p = 1.8e-6, Cramér's V = 0.173 (small). C vs S differs by 21.7 points (95% CI 13.3 to 30.0). Q vs S differs by 5.3 points (95% CI -6.2 to 16.8), which is not distinguishable from zero.
- **Fare:** Mann-Whitney p = 4.6e-22, rank-biserial r = 0.384 (medium). Median fare is 26.0 for survivors and 10.5 for non-survivors.
- **Parch:** Mann-Whitney p = 3.7e-5, rank-biserial r = 0.122 (small). Both medians are 0.
- **SibSp:** Mann-Whitney p = 0.008 (Holm p = 0.016), rank-biserial r = 0.086 (small). Both medians are 0.
- **Age:** Mann-Whitney p = 0.16, rank-biserial r = -0.062 (negligible). Both medians are 28.

The Fare, Parch and SibSp results are unadjusted for Sex and Pclass. The rate-difference confidence intervals are unadjusted Wald intervals and were not part of the Holm family.

![Survival rate by Pclass and Sex (share survived)](tasks/stat_1/charts/stat1_rate_by_sex_pclass.png)

### Sex × Pclass interaction and Age × Sex

**Sex × Pclass.** The likelihood-ratio test for the interaction gives chi-square 28.79 on 2 df, p = 5.6e-7. The full logit (Female × Pclass) coefficients for the interaction terms are:

| Term | Coefficient | p-value | Odds ratio |
|---|---|---|---|
| Female:Pclass 2 | 0.185 | 0.816 | 1.203 |
| Female:Pclass 3 | -2.096 | 0.0014 | 0.123 |

The reference is Pclass 1 and male passengers. The class 3 penalty is steeper for women: the odds ratio of class 3 vs class 1 is 0.033 for females and 0.268 for males. For class 2 vs class 1 the odds ratios are close, 0.385 for females and 0.320 for males. The difference is concentrated in class 3.

![Survival rate by Sex and Pclass](tasks/stat_2/charts/sex_pclass_survival_rate.png)

**Age × Sex.** This analysis covers only the 714 passengers with known Age; 177 rows with missing Age were excluded. eda_2 found Age missingness to be systematic and tied to class and fare, so this result may not generalise to the full sample.

- Unadjusted: Female × Age coefficient 0.041 (odds ratio 1.042 per year), p = 0.0024. LR chi-square 9.55, p = 0.0020.
- Adjusted for Pclass: coefficient 0.050 (odds ratio 1.051 per year), p = 0.00074. LR chi-square 11.90, p = 0.00056.

The female-versus-male survival gap in odds widens with age, and class does not explain this association. Fare, Embarked and family size were not controlled for. The main effect of Age was not significant (Mann-Whitney p = 0.16), so this is an interaction with Sex, not an independent Age effect.

### Missingness and survival

- **Age:** rows with missing Age survived at 29.4% (n = 177), against 40.6% when Age is present (n = 714). Missing-Age rows are 76.8% Pclass 3 (vs 49.7%), 29.9% female (vs 36.6%), with median fare 8.05 (vs 15.74).
- **Cabin:** rows with missing Cabin survived at 30.0% (n = 687), against 66.7% when Cabin is present (n = 204). Pclass 1 is 5.8% of Cabin-missing rows and 86.3% of Cabin-present rows. Median fare is 10.50 vs 55.22.
- **Embarked:** the two missing rows are both female, Pclass 1, survived, and paid a fare of 80. Two rows are too few to test.

![Survival rate (%) for rows with Age, Cabin or Embarked missing versus present](tasks/eda_2/charts/missingness_survival_rate.png)

**Within Pclass × Sex cells (eda_3).**

- **Age:** the count-weighted missing-minus-present gap across the six cells is -0.9 points, against an overall gap of about -11 points. Individual cell gaps range from -15.8 (class 1 male, 21 missing vs 101 present) to +13.4 (class 3 female, 42 missing vs 102 present). Cells rest on 2 to 94 missing rows, and no significance test was run. The gap is not established as persisting within cells.
- **Cabin:** the weighted gap is -14.5 points, against an overall gap of about -37 points. This depends heavily on class 2 and 3 cells where the present side has only 6 to 10 rows. The most reliable within-class evidence is class 1: female +3.7 points (13 missing vs 81 present), male -18.8 points (27 vs 95). The class 1 female gap is near zero, so the gap is not uniform across cells.

![Survival rate (%) within each Pclass x Sex cell for Age and Cabin missing vs present](tasks/eda_3/charts/within_cell_survival_rates.png)

### Adjusted effects of Embarked and Fare

Both adjusted models are logistic regressions controlling for Pclass and Sex. Holm correction covers the two adjusted tests.

- **Embarked C vs S:** adjusted OR 1.81 (95% CI 1.16 to 2.83), p = 0.009, Holm p = 0.018. The unadjusted OR was 2.44 (95% CI 1.73 to 3.45). The association is attenuated by about one third on the log-odds scale but remains significant.
- **Fare, per 10 units:** adjusted OR 1.02 (95% CI 0.98 to 1.06), p = 0.39. The unadjusted OR was 1.16 (95% CI 1.11 to 1.21), p = 1.6e-11. The interval is compatible with small effects in either direction. Fare is strongly correlated with Pclass, so the adjusted estimate is imprecise. The drop from 1.16 to 1.02 is consistent with class and sex accounting for the fare association, but this is an inference from the change in the estimate, not a tested mechanism.

The unadjusted Fare result (Mann-Whitney, p = 4.6e-22) and the adjusted Fare result (p = 0.39) disagree in significance. Both are reported as they stand: the first does not control for Pclass or Sex, and the second does.

### Predictive modelling

Models were fitted on a stratified 75/25 split (668 training rows, 223 test rows) with 12 features (see the feature set below).

- **Majority-class baseline:** 61.4% test accuracy, but F1 0.0 and ROC AUC 0.5, since it never predicts survival.
- **Logistic regression:** 78.0% test accuracy, precision 0.728, recall 0.686, F1 0.707, ROC AUC 0.839. Training accuracy is 80.7%.
- **Random forest** (500 trees, min_samples_leaf = 2): 79.4% test accuracy, precision 0.786, recall 0.640, F1 0.705, ROC AUC 0.842. Training accuracy is 91.6%, a gap of about 12 points on test, so its test scores are optimistic.

The random forest was chosen as the better model on test AUC. Its 5-fold cross-validated ROC AUC on the training set is 0.860 (SD 0.013), higher than its test AUC of 0.842. The two estimates do not agree closely. The model comparison is not clearly in favour of the random forest, since the AUC gap is 0.842 vs 0.839 and F1 is essentially equal.

**Feature set used.** The 12 features were Pclass; Sex (one-hot, two columns); Age (median-imputed with 28.0, plus an Age_missing indicator); SibSp; Parch; Fare; and Embarked (one-hot, including a Missing level). Name, Ticket, Cabin and PassengerId were excluded (ml_1_split: n_features = 12, age_median = 28.0).

**Feature importance.**

- *Random forest, permutation importance* (drop in test ROC AUC): Sex_male 0.072 (SD 0.017), Sex_female 0.049 (SD 0.014), Pclass 0.043 (SD 0.011), Age 0.030 (SD 0.011), Fare 0.026 (SD 0.014). The SDs overlap heavily, so the ordering among Sex_female, Pclass and Age is within the noise of a 223-row test set. Sex is split into two columns, so its combined effect is understated.
- *Logistic regression, absolute standardized coefficient:* Pclass 0.928, Sex (male 0.627, female 0.627), Age 0.541, SibSp 0.262, Age_missing 0.227.

The two methods are not directly comparable. Both rank Sex and Pclass among the top features, but no exact order should be read from either.

![Permutation importance (mean drop in test ROC AUC) of the random forest, by feature](tasks/ml_1/charts/ml_1_perm_importance.png)

## Limitations

- **Missing data.** Cabin is 77.1% missing and was used only as an indicator. Age is 19.9% missing; the median-imputed model treats it through a single value (28.0) plus an indicator. Embarked has two missing rows, which were not tested.
- **Systematic missingness.** eda_2 found Age and Cabin missingness systematic and tied to class and fare. Within-cell checks (eda_3) did not establish a consistent Age gap, and the Cabin within-class evidence rests on class 1 cells.
- **Unstable cells.** Several Pclass × Sex cells for Cabin have only 6 to 10 present-side rows. Small SibSp and Parch groups (for example 5 to 18 rows for SibSp of 3 or more) give unstable rates.
- **Multiple testing and intervals.** Holm correction covered the seven omnibus tests. The rate-difference confidence intervals are unadjusted Wald intervals.
- **Unadjusted results.** The Fare, Parch and SibSp Mann-Whitney results and the Embarked and Fare chi-square results do not control for Pclass or Sex.
- **Adjustment scope.** The Fare adjusted estimate is imprecise because Fare and Pclass are strongly correlated. Fare, Embarked and family size were not controlled in the Age × Sex analysis.
- **Model evaluation.** The test set has 223 rows. The random forest test scores are optimistic (training accuracy 91.6%). The model was chosen on test AUC, and the permutation importance uses the same test set, so both are optimistically biased. The cross-validated AUC (0.860) and test AUC (0.842) disagree.
- **Importance methods.** Permutation and coefficient rankings are different methods and are not comparable. The Sex one-hot split understates Sex's combined effect.
- **Unresolved review issues.**
  - *Age × Sex (stat_2):* the result covers only 714 passengers with known Age, and Age missingness is systematic and tied to class and fare, so it may not generalise to the full sample. The interaction terms are reported above, as requested.
  - *Feature set (ml_1):* the feature set is stated above, as requested, with the exclusions. The model comparison, importance ranking and interpretation of these features are limited by the caveats in the Predictive modelling section.
- **Failed tasks.** None. All seven analysis tasks were completed.

## Open questions

- Does the Embarked C effect hold when cabin or deck information is added? Does the adjusted C vs S association persist once Fare is also controlled?
- Does the fare effect vanish within each Pclass stratum, or is there a fare × class interaction?
- Does the Female × Age interaction hold after controlling for Fare and Embarked?
- Is the steeper class 3 penalty for women explained by Embarked or Fare?
- Does the lower survival of Age-missing passengers persist within each class and sex group after adjusting for Fare? Is the Age-missing pattern driven by Fare within Pclass 3?
- Does the Cabin-missing gap within class 1 male (-18.8 points) hold after adjusting for Fare?
- Does the deck letter from Cabin add survival signal beyond Pclass, Sex and Fare?
- Can the title from Name predict missing Age, and does it add signal beyond Sex and Pclass?
- Do family-size variables (SibSp plus Parch, or as a combined term) add signal beyond each alone, or change the Sex and Pclass effects?
- Would repeated cross-validation on the training set give a more reliable model comparison than a single test split?