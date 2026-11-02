# Data Analysis Report: Titanic

## Executive Summary

- **Sex is the dominant predictor of survival.** Women survived at 74.2% (233 of 314) compared with 18.9% for men (109 of 577). The association is large (Cramér's V = 0.543, Holm-adjusted p = 2.6e-58), and Sex is the single most important feature in the predictive model.
- **The effect of sex depends on passenger class.** Female survival falls from 96.8% in first class to 50.0% in third class, while male survival falls from 36.9% to 13.5%. The Sex × Pclass interaction is significant (LR χ² = 28.79, df = 2, p = 5.6e-7) and remains significant after adjusting for Age and Fare on 714 complete cases (LR χ² = 33.81, p = 4.6e-8). Third-class women are the clearest subgroup contrast in the data.
- **The predictive model is useful but not precise.** Logistic regression reaches 77.6% test accuracy and ROC AUC 0.841, against 61.4% for a majority-class baseline. Its train–test gap is small (0.03), so it is the more reliable of the two models tested.
- **Several apparent effects are weaker than they first look.** Age is borderline and not significant after family-level correction (Holm p = 0.082). The Embarked (port) effect is nominally significant after adjusting for class and sex but is fragile (family-level significance depends on the model chosen). SibSp results depend on how the variable is coded. Cabin and Age missingness are largely proxies for class and fare.
- **Data quality limits what can be concluded.** Cabin is missing for 77.1% of passengers and Age for 19.9%. Age was median-imputed before the split, and the adjusted analyses use only 714 complete cases. These limits should be resolved before any model is used for decisions.

## Dataset Overview

The dataset is the Titanic passenger manifest, with **891 passengers and 12 columns**. The target is **Survived** (binary; 1 = survived). Of the passengers, 549 (61.6%) did not survive and 342 (38.4%) did.

- **Numeric features (5):** Age, Fare, SibSp (siblings or spouses aboard), Parch (parents or children aboard), and Pclass (treated here as ordinal, with values 1 to 3).
- **Categorical features (2):** Sex and Embarked (port of embarkation: C, Q or S).
- **Excluded from modelling:** Name and Ticket, which were not used directly. Title extraction from Name was left out of scope.

**Missing values:**

| Column | Missing | Share |
|---|---|---|
| Cabin | 687 | 77.1% |
| Age | 177 | 19.9% |
| Embarked | 2 | 0.2% |

The data are observational. The results describe associations in one historical sample and do not establish why particular passengers survived.

## Analysis Methodology

### Approach

The analysis addressed seven questions, ordered by importance:

1. **Descriptive patterns (EDA):** the overall survival distribution, survival rates by group, and mean Age and Fare by survival status.
2. **Group differences (statistical):** which differences in survival are significant across Sex, Pclass, Embarked, Age, Fare, SibSp and Parch, and how large the effects are, with Holm correction across seven primary tests.
3. **Interactions (statistical):** whether Sex changes the effect of Pclass (and of Age), tested with likelihood-ratio (LR) tests on logistic models.
4. **Missingness (EDA):** where values are missing, and whether missingness in Age, Cabin and Embarked is related to survival, class, sex or fare.
5. **Predictive modelling (ML):** how well survival can be predicted, compared with a majority-class baseline, and which features matter most, using a stratified 75/25 train/test split.
6. **Adjusted Embarked effect (statistical):** whether the port association persists after adjusting for Pclass and Sex, with the two missing-Embarked passengers excluded.
7. **Robustness of the interaction (statistical):** whether the Sex × Pclass interaction survives joint adjustment for Age and Fare, given that Fare is correlated with class.

### Execution

| Specialist | Tasks | Status |
|---|---|---|
| Exploratory analysis (EDA) | 2 | 2 completed |
| Statistical | 4 | 4 completed |
| Machine learning | 1 | 1 completed |
| **Total** | **7** | **7 completed, 0 failed (100%)** |

Total execution time was 151.9 seconds. No analyses failed. Two tests have documented caveats (stat_3 was reported as partial in its status, and its Holm-adjusted results are approximate). Both are discussed under Limitations.

## Key Findings

### Exploratory Analysis

**Overall distribution.** The survival rate is 38.4% (342 of 891).

**Sex.** This is the strongest single split.
- Female: 74.2% survived (n = 314)
- Male: 18.9% survived (n = 577)

**Passenger class.** Survival falls steadily with class.
- Class 1: 63.0% (n = 216)
- Class 2: 47.3% (n = 184)
- Class 3: 24.2% (n = 491)

**Sex × class.** The class gradient is much steeper for women.

| Group | Class 1 | Class 2 | Class 3 | Gap (class 1 − class 3) |
|---|---|---|---|---|
| Female | 96.8% (n = 94) | 92.1% (n = 76) | 50.0% (n = 144) | 46.8 points |
| Male | 36.9% (n = 122) | 15.7% (n = 108) | 13.5% (n = 347) | 23.4 points |

**Embarkation.** Cherbourg (C) has the highest survival rate at 55.4% (n = 168), followed by Queenstown (Q) at 39.0% (n = 77) and Southampton (S) at 33.7% (n = 644). The two passengers with no port recorded both survived. Class mix may explain part of the port differences; this is tested later.

**Family size.**
- SibSp: 34.5% survival with no siblings or spouses (n = 608), 53.6% with one (n = 209), and 46.4% with two (n = 28). Rates fall to 25.0% with three (n = 16), 16.7% with four (n = 18), and 0% with five (n = 5) or eight (n = 7).
- Parch: 34.4% with no parents or children (n = 678), 55.1% with one (n = 118), and 50.0% with two (n = 80). Groups of three or more have 1 to 5 passengers each, so their rates are unreliable.

**Continuous features by survival status.**
- Age: survivors have mean 28.3 and median 28.0 (n = 290 non-missing). Non-survivors have mean 30.6 and median 28.0 (n = 424 non-missing). The interquartile ranges are 19 to 36 for survivors and 21 to 39 for non-survivors, so the difference is a modest shift across the distribution.
- Fare: survivors have mean £48.40 and median 26.0. Non-survivors have mean 22.12 and median 10.5. Both distributions are right-skewed, since the means sit well above the medians.

![Survival rate by sex and passenger class](survival_rate_by_sex_pclass)

### Statistical Evidence

Seven primary tests were run and Holm-corrected together. Categorical features used chi-square tests and numeric features used Welch t-tests, with Mann-Whitney tests as checks.

| Feature | Test | Result (raw p) | Holm-adjusted p | Effect size | Interpretation |
|---|---|---|---|---|---|
| Sex | Chi-square | χ² = 263.05, p = 3.7e-59 | 2.6e-58 | V = 0.543 (large) | Very strong association; women survived far more often |
| Pclass | Chi-square | χ² = 102.89, p = 4.5e-23 | 2.7e-22 | V = 0.340 (medium to large) | Strong gradient by class |
| Embarked (excl. 2 missing) | Chi-square, df = 2, n = 889 | χ² = 26.49, p = 1.8e-6 | 7.1e-6 | V = 0.173 (small) | Port association is real but small |
| Fare | Welch t-test | p = 2.7e-11 | 1.3e-10 | Mean difference +26.28 (95% CI 18.73 to 33.83); rank-biserial 0.384 | Survivors paid much more |
| Parch | Welch t-test | p = 0.013 | 0.040 | Mean difference +0.135 (95% CI 0.03 to 0.24); rank-biserial 0.122 (small) | Modest association; any parent or child: +16.8 points (chi-square p = 1.1e-5) |
| SibSp | Welch t-test | p = 0.233 | 0.233 | Mean difference −0.080 (95% CI −0.21 to 0.05); rank-biserial 0.086 (negligible) | Mean-based test not significant; any sibling or spouse: +12.1 points (p = 5.4e-4) |
| Age | Welch t-test | p = 0.041 | 0.082 | Mean difference −2.28 years (95% CI −4.47 to −0.09); rank-biserial −0.062 (negligible) | Borderline; not significant after correction |

**Plain-English reading.**
- Sex, class and fare are unambiguous. Their associations are large and survive correction by a wide margin.
- Embarkation is significant but small. Its unadjusted association could partly reflect class mix.
- Parch is significant after correction, but the effect is small.
- SibSp is not significant when measured as a mean. The result depends on coding: any-sibling-or-spouse versus none is significant, while the count-based test is not.
- Age is not significant at the family level. The Mann-Whitney test gives p = 0.160 and the effect is negligible, so no firm conclusion about Age can be drawn from its marginal effect.

**Sex × Pclass interaction (stat_2).** The effect of class differs by sex.
- LR test (unadjusted, all 891 rows): χ² = 28.79, df = 2, **p = 5.6e-7**. AIC falls from 834.9 to 810.1 when the interaction is added.
- The female-minus-male survival gap is 60 points in class 1, 76 points in class 2 and 36 points in class 3. The sex gap is largest in class 2 and smallest in class 3.

**Sex × Age interaction (stat_2, secondary).** On the 714 passengers with a recorded Age, the Sex × Age interaction gives LR χ² = 9.55, df = 1, **p = 0.002**. This indicates the Age slope differs between women and men. The result is based on complete cases only.

**Adjusted Sex × Pclass interaction (stat_4).** On the 714 complete cases, adding the interaction to a model that already includes Age and Fare gives LR χ² = 33.81, df = 2, **p = 4.6e-8**. AIC falls from 659.2 to 629.4. The interaction therefore remains significant after joint adjustment for Age and Fare.

- The adjusted and unadjusted LR statistics come from different samples (714 versus 891 rows), so the increase from 28.79 to 33.81 cannot be attributed to adjustment. A like-for-like comparison would require refitting the unadjusted model on the same 714 rows.
- Fare and Pclass are moderately correlated (r = −0.554). This is strong enough that the two carry overlapping information, but the interaction is not absorbed by Fare.

**Adjusted Embarked effect (stat_3).** Logistic regression on 889 passengers, with Embarked as the predictor and Pclass and Sex as covariates.

| Model | Embarked LR test | Adjusted OR, C vs S (95% CI) | Adjusted OR, Q vs S (95% CI) | Holm-adjusted p (approx.) |
|---|---|---|---|---|
| Additive (Pclass + Sex) | χ² = 7.96, df = 2, p = 0.019 | 1.81 (1.16 to 2.83) | 1.57 (0.84 to 2.91) | 0.056 (does not reach 0.05) |
| With Pclass × Sex interaction | χ² = 9.37, df = 2, p = 0.009 | 1.87 (1.19 to 2.93) | 1.73 (0.97 to 3.08) | 0.037 (reaches 0.05) |

Passengers embarking at Cherbourg have roughly 80% higher adjusted odds of survival than those embarking at Southampton. The Queenstown estimate is not significant. The Holm values are approximate, because the other six p-values in the family are unadjusted. Whether the port effect counts as significant depends on which model is chosen, so it should be treated as provisional.

**Missingness (eda_2).**
- **Cabin:** survival is 30.0% when Cabin is missing versus 66.7% when present (p = 6.7e-21). Cabin missingness is, however, almost entirely a function of class: 18.5% missing in class 1, 91.3% in class 2 and 97.6% in class 3 (p ≈ 1e-121). Median fare is 10.5 when Cabin is missing versus 55.2 when present.
- **Age:** survival is 29.4% when Age is missing versus 40.6% when present (p = 0.008). Missingness is related to class (13.9% in class 1, 6.0% in class 2, 27.7% in class 3; p ≈ 1e-10) and to fare (median 8.05 when missing versus 15.74 when present; p = 3e-8). It is not related to sex (p = 0.12).
- **Embarked:** both passengers with missing Embarked survived. With only two rows, the chi-square tests are unreliable (expected counts below 5). The nominal associations with class (p = 0.044) and fare (p = 0.042) should not be relied on.

### Predictive Models

**Setup.** Stratified 75/25 split, seed 42. Training n = 668; test n = 223. Features: Pclass, Sex (female indicator), Age (median-imputed), SibSp, Parch, Fare and Embarked (one-hot).

**Model types tested:**
- Majority-class baseline (always predicts "did not survive")
- Logistic regression
- Random forest (300 trees)

**Performance on the test set:**

| Model | Train accuracy | Test accuracy | Precision | Recall | F1 | ROC AUC |
|---|---|---|---|---|---|---|
| Majority-class baseline | — | 0.614 | — | 0.000 | 0.000 | 0.500 |
| Logistic regression | 0.808 | 0.776 | 0.720 | 0.686 | 0.702 | 0.841 |
| Random forest | 0.981 | 0.780 | 0.747 | 0.651 | 0.696 | 0.824 |

**Interpretation.**
- Both models clearly beat the baseline. The baseline is correct 61% of the time only because most passengers did not survive, and it never identifies a survivor.
- With 223 test rows, the 95% interval on accuracy is roughly ±5 percentage points. The two models' accuracies are statistically indistinguishable.
- The random forest overfits (train–test gap of 0.20), so its test metrics and impurity importances are optimistic. Logistic regression generalises more tightly (gap 0.03) and is the more reliable model.

**Feature importance.** Permutation importance is measured as the drop in test ROC AUC for the random forest, averaged over 30 repeats.

| Tier | Feature | Permutation importance (SD) | Note |
|---|---|---|---|
| Top | Sex (female) | 0.209 (0.028) | About four times the next feature |
| Second | Pclass | 0.054 (0.013) | Clearly above zero |
| Second | Age | 0.051 (0.017) | Clearly above zero |
| Second | Fare | 0.040 (0.015) | Clearly above zero |
| Near zero | Parch | 0.002 (0.009) | Positive but within noise |
| Near zero | Embarked (S) | 0.003 (0.006) | Positive but within noise |
| Near zero | SibSp | −0.001 (0.009) | Within noise |
| Near zero | Embarked (C) | −0.004 (0.005) | Within noise |
| Near zero | Embarked (Q) | −0.0002 (0.003) | Within noise |

The near-zero features should be read as "no detectable added predictive value beyond the other features in this sample," not as "no relationship with survival." Their standard deviations are as large as or larger than their estimates. Parch and Embarked (S) have small positive estimates, but these are indistinguishable from zero.

**Ranking conflict.** The random forest's impurity importance ranks Fare first (0.276), but impurity importance favours continuous features and is inflated by overfitting. The logistic regression coefficients (Sex 2.54, Pclass 1.10, Fare 0.003) are unscaled. Fare is measured in currency units, while the other inputs are binary or small counts, so these coefficients are not comparable across features. The low Fare coefficient does not show that Fare is unimportant. Standardised features are needed before the ranking can be settled.

**Predictive insights.**
- Knowing sex alone captures most of the predictable signal. The additional features contribute mainly through class and age.
- The models are good at identifying likely non-survivors and reasonably good at identifying survivors (recall about 0.65 to 0.69).
- Parch, SibSp and Embarked add little once sex, class, age and fare are known, even though some have significant marginal associations.

## Synthesis

**Validated, consistent patterns:**

1. **Sex is the strongest and most robust factor.** It is the largest association in the statistical tests, the top feature in the model, and the basis of the largest rate difference in the EDA.
2. **Class and sex interact.** The gradient by class is far steeper for women (46.8 points from class 1 to class 3) than for men (23.4 points). This interaction is significant unadjusted (p = 5.6e-7), with Age and Fare adjustment on complete cases (p = 4.6e-8), and in the model, where class and sex are both important.
3. **Class and fare are closely linked.** Fare is moderately correlated with class (r = −0.554), and both differ strongly by survival. The survival difference in fare is partly a class difference, and fare carries only a limited independent signal once class is controlled. This has not been settled, because fare coefficients were unscaled.
4. **Missingness is entangled with class and fare.** Cabin and Age missingness both rise with lower class and lower fare. Their apparent survival associations are therefore likely confounded.
5. **Family size has a modest, coding-dependent link.** Having any parent or child, or any sibling or spouse, is associated with higher survival (+16.8 and +12.1 points). Mean-based SibSp tests are not significant, and very large families (5 or more) are too small to interpret.
6. **Embarkation is a provisional port effect.** Cherbourg passengers survived more often, and the association persists after adjustment (OR about 1.8 to 1.9), though it is borderline at the family level.

**Contradictions and reconciliations:**
- **Parch:** significant in the statistical tests, but near zero in the model. The two methods answer different questions: marginal association versus added predictive value. This should be reported, not hidden.
- **Age:** borderline in the statistical tests (Holm p = 0.082), yet it has a second-tier permutation importance (0.051) in the model. A plausible reconciliation is that Age matters conditionally on sex (Sex × Age, p = 0.002), which a marginal test misses and a model can capture. This is a hypothesis, not a tested result. It also rests on median-imputed Age for about 20% of rows.
- **Embarked:** significant unadjusted and nominally significant after adjustment, but near zero in model importance and not significant at the family level in the additive model.

## Conclusions

**What we can say with confidence:**
- Survival in this sample was driven primarily by sex. Women survived at 74.2% and men at 18.9%.
- Class mattered strongly, and it mattered much more for women. Third-class women survived at 50%, compared with 96.8% for first-class women.
- A model using the seven listed features predicts survival with about 78% accuracy on held-out data. This clearly beats the 61% baseline, but accuracy does not differ detectably between logistic regression and random forest.
- Sex and passenger class are the two features that consistently carry predictive value.

**What we can say with moderate confidence:**
- The Sex × Pclass interaction is robust, persisting after adjustment for Age and Fare on complete cases.
- Passengers embarking at Cherbourg had higher adjusted survival odds than those from Southampton (OR about 1.8 to 1.9), though the result is provisional.
- Having family aboard (any parent or child, or any sibling or spouse) is associated with higher survival, by roughly 12 to 17 percentage points, though the effect is small.

**What we cannot yet say:**
- Whether Age has an independent effect. The marginal test is borderline and not significant after correction, and the model importance depends on imputation.
- Whether fare has any survival information beyond class.
- Whether Parch, SibSp or Embarked add predictive value once the other features are known. The model suggests they add little.
- Why any of these patterns occurred. All results are observational and do not support causal claims.

## Limitations & Caveats

**Data quality**
- **Missing Age (19.9%)** was imputed with the median (28.0). That median was computed on all 891 rows before the train/test split, so information from the test set leaked into training. The leakage is small because the median does not use the outcome, but it should be fixed. An Age_missing indicator was created but not used, so the models cannot see which ages were imputed. Age missingness is itself related to class, fare and survival.
- **Missing Cabin (77.1%)** was not used in any model, even though it shows the strongest raw association with survival. Its association is largely a proxy for class and fare.
- **Missing Embarked (2 rows)** were filled with S in the model and excluded from the statistical tests. Both passengers survived and both are in class 1. With two rows, no test involving them is reliable.
- **Small subgroups:** Parch of 3 or more and SibSp of 5 or more have between 1 and 16 passengers each, so their rates are unstable.

**Statistical assumptions and limits**
- **Multiple comparisons:** the Holm correction covers the seven primary tests. The interaction tests (stat_2 and stat_4) and the adjusted Embarked test (stat_3) are outside that family. The adjusted Embarked Holm values are approximate, because the other six p-values are unadjusted.
- **Sample mismatch in adjusted comparisons:** the unadjusted interaction uses 891 rows and the adjusted one uses 714 complete cases. The change in the LR statistic (28.79 to 33.81) cannot be attributed to adjustment. A fair comparison requires refitting the unadjusted model on the same 714 rows. AIC values are not comparable across the two samples.
- **Sex × Age coefficient:** the coefficient (−0.041) was not recorded by the analysis and is excluded from this report. Only the LR test (χ² = 9.55, df = 1, p = 0.002) is reported.
- **Embarked model specification:** the adjusted Embarked models were fitted on Pclass and Sex. Fare and Cabin were not adjusted for, so a wealth or cabin-location explanation for the Cherbourg effect has not been excluded.
- **Unscaled coefficients:** logistic coefficients are not comparable across features. No variance inflation factor was computed for the adjusted model.
- **Test-set size:** the 223-row test set gives unstable permutation importances. Importance also depends on feature correlation, and Fare, Pclass and Embarked overlap.
- **Overfitting:** the random forest's train–test gap (0.20) makes its impurity importances and test metrics optimistic.
- **Observational design:** all results are associations. None supports causal claims about why women or higher-class passengers survived.

**Failed analyses:** none. Every task completed. Stat_3 was marked partial in the execution record because its Holm-adjusted results are approximate, not because the test failed.

**Missing information:** the dataset does not include ticket-group size, crew status or cabin deck (only the raw Cabin string, which is mostly missing). Title, which could improve Age imputation, was not extracted.

## Recommendations

### Immediate Actions

1. **Use sex and class as the baseline for any survival-based analysis or model.** They are the most reliable predictors, and the interaction between them should be included rather than treated as two separate main effects.
2. **Do not treat Cabin or Age missingness as clean signals.** Both are tied to class and fare. Report these associations only after adjusting for class and fare.
3. **Fix the modelling pipeline before relying on the rankings:**
   - Compute the Age median on training data only.
   - Add the Age_missing indicator to the models.
   - Standardise numeric features before comparing coefficients.
4. **Report the logistic regression as the primary model.** Its train–test gap is small and its test performance is at least as good as the random forest's. Describe the random forest's importances as optimistic.
5. **Report the Embarked effect as provisional.** State that it is significant after adjustment in both models, but that family-level significance depends on the model chosen.
6. **Standardise the coding of family size before any decision that depends on it.** Any-relative indicators are more stable than counts for this sample.

### Future Analysis

**Priority questions:**
1. **Does fare carry survival information beyond class?** Fit a standardised logistic model with fare, class and sex, and check variance inflation factors. This would settle whether the fare effect is independent of class.
2. **Is the Embarked effect explained by fare or cabin?** Add fare and cabin deck (where recorded) to the adjusted model.
3. **Does the Sex × Pclass interaction hold on all 891 rows?** Use multiple imputation for Age, or impute by title or by class-and-sex group, then refit.
4. **Is the Age effect conditional on sex, and does it differ for children and adults?** Test this with the imputed sample and with an Age_missing indicator.
5. **Which family-size coding is best?** Compare any-relative indicators, counts, and merged buckets of three or more.
6. **How stable are the feature rankings?** Use repeated stratified cross-validation, standardised features and a tuned random forest. This would reduce the variance of the near-zero importances and show whether the second-tier ranking holds.
7. **Is the Cabin association independent of class?** Model Cabin as a recorded-versus-missing indicator or a deck-level feature, adjusted for class and fare.

**Data that would help:**
- Complete or validated Age data, or an external source for imputation
- Cabin deck and location, and ticket group size, to separate wealth, family and cabin-location effects
- Crew status and occupation, which would clarify the class gradient for non-passengers
- Titles extracted from Name, which would improve Age imputation and allow a check on family structure