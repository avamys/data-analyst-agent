# Titanic Passenger Survival: Analysis of the Survived Target (891 Passengers)

## Summary

- **Sex is the strongest association with survival.** 74.2% of females survived versus 18.9% of males (chi-square 260.8, p = 1.2e-58, Cramer's V = 0.54). The gap is 55.3 percentage points (95% CI 49.5 to 61.1).
- **Passenger class and sex interact.** Survival falls with class (63.0%, 47.3% and 24.2% for classes 1, 2 and 3), but the drop is much steeper for women (Sex x Pclass likelihood-ratio chi-square 28.8, df 2, p = 5.6e-7). Female class 3 survival is 50.0%, against 96.8% for female class 1.
- **Embarked is significant only in unadjusted tests.** Its association with survival is significant (p = 1.8e-6), but not after adjusting for Sex, Pclass, Age and Fare (likelihood-ratio p = 0.142).
- **Predictive models beat the baseline but are tied with each other.** The majority-class baseline scores 61.5% test accuracy. Logistic regression scores 80.4% (ROC AUC 0.844) and random forest 81.6% (ROC AUC 0.836). The difference between them is within sampling noise on 179 test passengers. Sex and Pclass are the top two features in both models.
- **Missing Cabin is associated with lower survival, but the association is confounded.** Survival was 30.0% with Cabin missing versus 66.7% with Cabin present. Cabin missingness is concentrated in class 3 and low fares, and no adjusted test of missingness was run.

## Data

- **Size:** 891 rows, 12 columns.
- **Target:** Survived (binary). 342 passengers survived (38.4%) and 549 did not (61.6%), so the target is moderately imbalanced.
- **Features used:** Pclass, Age, SibSp, Parch, Fare (numeric); Sex and Embarked (categorical). Name, Ticket, Cabin and PassengerId were not used as raw features.
- **Missing values:** Age 177 (19.9%), Cabin 687 (77.1%), Embarked 2 (0.2%). No date or time features.

## Findings

### Survival rates by group

- **Overall:** 342 of 891 passengers survived (38.4%).
- **Sex:** Females survived at 74.2% (n = 314) and males at 18.9% (n = 577).
- **Pclass:** Survival was 63.0% in class 1 (n = 216), 47.3% in class 2 (n = 184) and 24.2% in class 3 (n = 491).
- **Sex within Pclass:** Females in classes 1 and 2 survived at 96.8% and 92.1%. Males in class 1 survived at 36.9%, and class 3 males at 13.5%.
- **Embarked:** C 55.4% (n = 168), Q 39.0% (n = 77), S 33.7% (n = 644).
- **SibSp:** 0 siblings/spouses: 34.5% (n = 608); 1: 53.6% (n = 209); 2: 46.4% (n = 28). Groups of 3 or more fell to 25% or lower on small counts (3: 25.0%, n = 16; 4: 16.7%, n = 18; 5: 0.0%, n = 5; 8: 0.0%, n = 7).
- **Parch:** 0 parents/children: 34.4% (n = 678); 1: 55.1% (n = 118); 2: 50.0% (n = 80). Groups of 3 or more are too small to be reliable (3: 60.0%, n = 5; 4: 0.0%, n = 4; 5: 20.0%, n = 5; 6: 0.0%, n = 1).
- **Age and Fare by survival:** Mean age was 28.3 years for survivors and 30.6 for non-survivors. Both groups had a median age of 28. Median fare was 26.0 for survivors and 10.5 for non-survivors (means 48.4 and 22.1).

![Survival rate by Sex and Pclass (fraction of passengers who survived)](tasks/eda_1/charts/survival_rate_by_sex_pclass.png)

### Significance tests and effect sizes

- **Sex:** Chi-square 260.8 (df 1, p = 1.2e-58, n = 889), Cramer's V = 0.54. The female-minus-male difference is 55.3 percentage points (95% CI 49.5 to 61.1, Wald), Cohen's h = 1.18. It passes the Bonferroni threshold (0.01 for five tests).
- **Pclass:** Chi-square 101.0 (df 2, p = 1.2e-22, n = 889), Cramer's V = 0.34. Class 1 minus class 3 is 38.4 percentage points (95% CI 30.9 to 45.9). This class 1 rate is 62.6% on the 889-passenger base used for the test. The 63.0% in the descriptive results uses all 891 passengers. The two differ only because the two passengers with missing Embarked were dropped. The Pclass result passes the Bonferroni threshold.
- **Embarked:** Chi-square 26.5 (df 2, p = 1.8e-6, n = 889), Cramer's V = 0.17 (small to moderate). C minus S is 21.7 percentage points (95% CI 13.3 to 30.0). This is unadjusted and is not adjusted for Pclass or Fare. It passes the Bonferroni threshold, but Pclass and Embarked were not adjusted for each other here (see the adjusted model below).
- **Fare:** Mann-Whitney p = 4.6e-22, rank-biserial r = 0.38, with survivors tending to have higher fares. It passes the Bonferroni threshold.
- **Age:** Mann-Whitney p = 0.16, rank-biserial r = -0.06. This is negligible and does not pass the Bonferroni threshold.

![Survival rate by Pclass and Sex](tasks/stat_1/charts/stat_survival_sex_pclass.png)

### Sex x Pclass and Age x Sex interactions

- **Sex x Pclass:** Survival counts (survived/n) were female class 1 91/94 (96.8%), female class 2 70/76 (92.1%), female class 3 72/144 (50.0%), male class 1 45/122 (36.9%), male class 2 17/108 (15.7%) and male class 3 47/347 (13.5%). The female-minus-male gap is about 60 points in class 1, 76 in class 2 and 37 in class 3. The joint likelihood-ratio test of the interaction gives LR chi-square 28.8 (df 2, p = 5.6e-7). Sex changes the effect of Pclass.
- **Age x Sex, unadjusted:** In a logit with a female x Age term on 714 passengers with Age (Age-only model), the interaction coefficient is 0.041 per year (Wald p = 0.0024). This model is unadjusted for Pclass and Fare, so the result is provisional.
- **Age x Sex, adjusted:** Under an additive model (female x Age + class + Fare, n = 714), the female:Age coefficient is 0.050 per year (p = 0.00076). This model omits the Sex x Pclass term, so the Age x Sex result is not established under full adjustment.
- **Direction correction:** The adjusted female:Age coefficient is positive. The age slope on survival is therefore less negative for women than for men, which reverses the earlier wording that it is "steeper for women." Predicted survival for class 1 at mean fare, from the additive model, is nearly flat across age for women and falls steeply for men:

| Age | Male | Female |
|---|---|---|
| 10 | 0.802 | 0.955 |
| 20 | 0.695 | 0.952 |
| 30 | 0.562 | 0.949 |
| 40 | 0.420 | 0.945 |
| 50 | 0.290 | 0.941 |
| 60 | 0.187 | 0.937 |

These predictions apply only to class 1 at mean fare.

![Survival rate by Sex within each Pclass; counts in stat2_sex_pclass_table](tasks/stat_2/charts/stat2_sex_pclass_rates.png)

### Adjusted model: Embarked, Sex, Pclass, Age and Fare

Logistic regression on 712 complete rows (reference: male, Embarked S):

| Term | Odds ratio | 95% CI | p |
|---|---|---|---|
| Female (vs male) | 12.44 | 8.25 to 18.75 | < 0.001 |
| Pclass (per step) | 0.295 | 0.216 to 0.404 | < 0.001 |
| Embarked C (vs S) | 1.62 | 0.96 to 2.74 | 0.069 |
| Embarked Q (vs S) | 0.72 | 0.26 to 1.99 | 0.522 |
| Age (per year) | 0.964 | 0.950 to 0.979 | < 0.001 |
| Fare (per unit) | 1.000 | 0.995 to 1.004 | 0.907 |

- **Embarked overall:** Likelihood-ratio chi-square 3.90 (df 2, p = 0.142). It is not significant after adjustment.
- **C vs S:** The unadjusted 21.7-point difference does not hold at 0.05 after adjustment. In a sensitivity model that adds Sex x Pclass, the C vs S OR is 1.79 (95% CI 1.05 to 3.05, p = 0.032), but the overall Embarked likelihood-ratio test is chi-square 4.73 (p = 0.094). The sensitivity result for C is weak and exploratory, and the overall Embarked association is still not significant.
- **Sex x Pclass in the sensitivity model:** The interaction OR is 0.22 (95% CI 0.11 to 0.44, p < 0.001), so the class gradient is steeper for women. The main-effect ORs for Sex and Pclass are averages across the other variable's levels, so they should be read as conditional on each other. The female OR of 512 in the interaction model extrapolates to Pclass 0 and is not interpretable.
- **Fare:** Not significant once Sex, Pclass, Embarked and Age are in the model.

### Missingness in Age, Cabin and Embarked

- **Age:** Survival was 29.4% with Age missing (n = 177) and 40.6% with Age present (n = 714). Chi-square 7.57 (p = 0.006), Cramer's V = 0.09, a small association. The Age-missing group is 76.8% class 3, with median fare 8.05 versus 15.74 for the rest. The unadjusted gap does not show an independent effect of missingness.
- **Cabin:** Survival was 30.0% with Cabin missing (n = 687) and 66.7% with Cabin present (n = 204). Chi-square 89.5 (p < 0.001), Cramer's V = 0.32, a moderate association. The Cabin-missing group is 69.7% class 3, with median fare 10.5 versus 55.22. Within classes the gap persists: class 1 66.5% present vs 47.5% missing; class 2 81.3% vs 44.0%; class 3 50.0% vs 23.6% (only 12 passengers with Cabin present in class 3). These gaps are unadjusted and confounded, so they do not establish an independent effect.
- **Sex mix:** Sex is similar across missingness groups (Age-missing 70.1% male; Cabin-missing 68.4% male).
- **Embarked:** Two rows are missing, passengers 62 and 830. Both are female, class 1, fare 80.0, cabin B28, and share ticket 113572. Two rows are too few to analyse.

![Survival rate for rows with Age or Cabin missing versus present](tasks/eda_2/charts/survival_by_missingness.png)

### Predictive models

- **Setup:** A single stratified 80/20 split (seed 42; 712 training, 179 test). Age was median-imputed and Sex one-hot encoded. Embarked was one-hot encoded with an extra Embarked_Missing category. Name, Ticket, Cabin and PassengerId were excluded.
- **Test results:**

| Model | Accuracy | F1 | ROC AUC | Precision | Recall |
|---|---|---|---|---|---|
| Majority-class baseline | 61.5% | n/a | n/a | n/a | n/a |
| Logistic regression | 80.4% | 0.724 | 0.844 | 0.793 | 0.667 |
| Random forest | 81.6% | 0.732 | 0.836 | 0.833 | 0.652 |

- **Comparison:** Both models beat the baseline. With 179 test passengers the two models are treated as tied, and neither is claimed better on accuracy. The random forest overfits: training accuracy is 91.4% against 81.6% on test.
- **Feature importance (permutation, mean drop in test ROC AUC over 30 repeats, Sex indicators permuted jointly):**
  - Logistic regression: Sex 0.221, Pclass 0.097, Age 0.026, SibSp 0.018, Embarked_C 0.003, Fare 0.003, Embarked_Missing 0.000; Embarked_S, Parch and Embarked_Q are at or below zero.
  - Random forest: Sex 0.220, Pclass 0.037, Fare 0.029, Age 0.023, SibSp 0.008; Embarked indicators and Parch are near zero, and Embarked_Missing is 0.000.
- **Embarked_Missing:** It has a coefficient of 0.176 on the standardised scale in logistic regression, but its permutation importance is 0.000, so it adds no predictive value.
- **Fare:** Its importance is higher in the random forest than in logistic regression. The reason has not been tested.

![Test-set accuracy, F1 and ROC AUC for the majority-class baseline, logistic regression and random forest; baseline F1 and AUC not applicable](tasks/ml_1/charts/ml1_model_comparison.png)

## Limitations

- **Unresolved review issue, feature ranking (ml_1):** The lead's objection stands. The ranking claim in the task output is corrected above. Sex and Pclass are the top two features in both models. Age is third for logistic regression but fourth for the random forest, where Fare (0.029) ranks above Age (0.023). The claim that Fare carries signal mainly through nonlinear interactions with class is removed. No interaction was tested, and the random forest's impurity-based Fare ranking is a different measure from the permutation importance. Only the higher importance of Fare in the random forest is stated.
- **Embarked_Missing and encoding (ml_1):** This is a deviation from plain one-hot encoding, kept so no passengers are dropped. Its importance is 0.000 and the category rests on two passengers.
- **Median Age imputation (ml_1):** Median imputation was applied to the 177 missing ages. Its effect on predictions for those passengers was not assessed.
- **Single split (ml_1):** The model comparison uses one split of 179 test passengers. Differences between models are within sampling noise.
- **Age x Sex result is provisional (stat_2, stat_4):** The unadjusted result omits Pclass and Fare. The adjusted result omits the Sex x Pclass term, which is significant. Both analyses exclude the 177 passengers with missing Age, and robustness to them was not tested.
- **Adjusted Embarked result (stat_3):** Embarked is not significant overall after adjustment. The C-port contrast is significant only in a sensitivity model, and the overall test there is not significant. Pclass was entered as a single linear term, and linearity was not checked, although the class-by-sex pattern suggests the linear per-step odds ratio may misrepresent the gradient. Pclass was not entered as categorical dummies.
- **Missingness analyses are unadjusted (eda_2):** The Age and Cabin gaps are confounded with Pclass and Fare. No adjusted model of missingness was fitted. The within-class Cabin comparison for class 3 rests on 12 passengers with Cabin present.
- **Small groups (eda_1):** SibSp and Parch groups of 3 or more are too small to interpret. They were not pooled.
- **Sample base:** Tests use 889 passengers (two with missing Embarked dropped). Descriptive rates use 891, so some figures differ slightly (for example, class 1 at 62.6% and 63.0%).
- **Scope:** All results are associations in this sample. No causal interpretation is supported.
- **Failed tasks:** None. All five analysis tasks (eda_1, stat_1, stat_2, ml_1, eda_2) and stat_3 and stat_4 are complete.

## Open questions

- Does the Sex x Pclass interaction in class 3 reflect Embarked or Fare, which correlate with class? The adjusted model includes both, but the within-class-3 question was not analysed directly.
- Does the Age x Sex interaction hold when Sex x Pclass is included, and within classes 2 and 3?
- Are the Age x Sex and Sex x Pclass results robust to the 177 passengers with missing Age (for example, via multiple imputation)?
- Does a nonlinear Fare term change the interaction results?
- Does Pclass as categorical dummies (2 vs 1, 3 vs 1) change the Sex and Embarked results?
- Is the C-port association explained by the correlation of class and fare with port? The adjusted C result is not significant at 0.05, but the reason was not tested.
- Does the Age effect differ between children and adults?
- Should SibSp and Parch be pooled, and does a family-size feature improve prediction?
- Would title extracted from Name, or a Cabin-present flag or deck letter, improve prediction beyond Pclass and Sex?
- Does the Fare effect in the random forest reflect class or ticket group membership rather than price?
- Is median Age imputation biasing predictions for passengers with missing age? Should Age be imputed by title or class group, given that missing Age is concentrated in class 3?
- Is Cabin missingness associated with survival after adjusting for Pclass, Fare and Sex? Is Age missingness associated with survival after controlling for Pclass and Sex?
- Does Embarked_Missing carry any real signal, or is it only two passengers?