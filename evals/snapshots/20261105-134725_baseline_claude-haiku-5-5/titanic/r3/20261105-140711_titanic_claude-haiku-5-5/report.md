# Data Analysis Report: Titanic Survival

## Executive Summary

- **Sex is the strongest predictor of survival.** Women survived at 74.2% (233 of 314) and men at 18.9% (109 of 577), a gap of 55.3 percentage points. The chi-square test is highly significant (p = 1.197e-58), and the association is large (φ ≈ 0.54, derived from the reported table).
- **Passenger class is the second major signal.** First-class passengers survived at 62.96% versus 24.24% in third class (chi-square p = 4.549e-23). Class is also strongly tied to age and fare, so part of its effect may run through those variables.
- **A simple linear model is sufficient for the current goal.** Logistic regression achieved the best test ROC-AUC (0.8495). The random forest overfit (train–test accuracy gap of 0.1084) and did not outperform it. Model selection should favor the logistic regression, with its limits stated clearly.
- **Missing data needs deliberate handling.** Age is missing for 19.9% of passengers, and survival differs by missingness, so the data are likely not missing completely at random. The recommended approach is group-wise median imputation (Pclass × Sex) with an `Age_missing` indicator, rather than dropping rows, which would discard about one-fifth of the data.
- **Several decisions remain open.** Accuracy, precision, recall, and F1 were not reported, Cabin and Embarked handling is undocumented, and the family-size and Sex × Pclass effects were not tested. These gaps should be closed before the model is used to support operational decisions.

## Dataset Overview

- **Source:** `/workspaces/agents/evals/data/titanic.csv`
- **Size:** 891 passengers × 12 columns, with no duplicate rows or duplicate PassengerIds
- **Target:** `Survived` (binary; 1 = survived, 0 = died). Overall survival was 38.38% (342 survivors) and non-survival was 61.62% (549).
- **Features:** 7 numeric and 5 categorical, including Pclass, Sex, Age, SibSp, Parch, Fare, Cabin, and Embarked
- **Missingness:** Cabin 77.1% (687 rows), Age 19.9% (177 rows), Embarked 0.2% (2 rows)
- **Outliers:** 11 Age values fall outside the 1.5 × IQR fences

## Analysis Methodology

### Strategic Approach

The analysis followed a three-stage sequence:

1. **Exploratory analysis first**, to understand missingness, distributions, and bivariate patterns. Handling decisions for missing data had to be made before any modeling.
2. **Statistical testing second**, to confirm which group differences are significant and to guide feature selection. Chi-square tests were used for categorical associations and t-tests and ANOVA for continuous variables.
3. **Predictive modeling last**, using a train/test split and cross-validation. The 891-row sample is adequate for this. Feature importances were used to check whether the statistical findings held up.

Class imbalance (about 38/62) was judged mild enough that no resampling was needed.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory Data Analysis | 2 |
| Statistical Analysis | 1 |
| Machine Learning | 3 |
| **Total** | **6 of 6 (100% success, 0 failed)** |

Total execution time was 58.1 seconds.

## Key Findings

### Exploratory Analysis

**Overall outcome**
- 38.38% of passengers survived.

**Sex**
- Female survival: 74.2% (233 of 314)
- Male survival: 18.9% (109 of 577)
- Among survivors, women outnumber men about 2.1 to 1 (233 vs. 109). Among non-survivors, men outnumber women about 5.8 to 1 (468 vs. 81).

**Passenger class**
- First-class survival: 62.96%
- Third-class survival: 24.24%
- Second-class figures were not reported in the outputs.

**Age**
- 177 values (19.87%) are missing.
- Survival differs between passengers with and without a recorded age. The direction and size of this difference were described but not quantified.
- Age has 11 IQR outliers, so median-based methods are preferable to mean-based imputation.

**Fare**
- Fare is strongly associated with survival and tracks passenger class closely. Its distribution was reviewed but its detailed summary statistics were not reported.

**Family size**
- Solo travellers and very large families survived less often than intermediate-sized groups. This was observed descriptively and was not quantified.

**Missing-value decisions**

| Column | Missing | Decision | Status |
|---|---|---|---|
| Age | 19.9% | Median imputation by Pclass × Sex, plus `Age_missing` indicator. Do not drop rows or use the global mean. | Decided and justified |
| Cabin | 77.1% | Possible drop "if appropriate" | Final decision not reported |
| Embarked | 0.2% (2 rows) | Not reported | Not documented |

### Statistical Evidence

| Test | Purpose | Statistic | p-value | Significance (α = 0.05) | Effect Size | Interpretation |
|---|---|---|---|---|---|---|
| Chi-square: Sex × Survived | Association between sex and survival | χ² ≈ 263 (derived) | 1.197e-58 | Significant | φ ≈ 0.54 (derived) | Very strong association |
| Chi-square: Pclass × Survived | Association between class and survival | Not reported | 4.549e-23 | Significant | Not reported | Strong association |
| t-test: Age by survival | Mean age difference between survivors and non-survivors | Not reported | 0.04119 | Significant, marginal | Not reported | Weak practical difference |
| t-test: Fare by survival | Mean fare difference between survivors and non-survivors | Not reported | 2.699e-11 | Significant | Not reported | Strong association, confounded with class |
| ANOVA: Age by Pclass | Mean age difference across classes | Not reported | 7.488e-24 | Significant | Not reported | Age differs substantially by class |

**Effect size for Sex (derived by the report author).** The statistical output did not include Cramér's V. I computed it from the reported 2 × 2 table. The chi-square statistic is about 263, and for a 2 × 2 table Cramér's V equals φ ≈ 0.54, a large effect. The crude odds ratio for female vs. male survival is (233 × 468) / (81 × 109) ≈ 12.4, and the relative risk is 0.742 / 0.189 ≈ 3.9.

**Plain-English interpretation**
- Sex and survival are clearly linked, with women surviving at roughly four times the rate of men.
- Class is also clearly linked to survival, but its effect size was not reported.
- The Age result is statistically significant at 0.05 but borderline. Practically, its association with survival is small.
- The Fare result is strong, but Fare is largely a proxy for class, so it should not be read as an independent effect.
- Age also differs by class, which means class, age, and fare carry overlapping information.

### Predictive Models

**Models tested**
- Logistic regression (baseline)
- Random forest

**Performance**

| Model | Test ROC-AUC | Other Metrics | Notes |
|---|---|---|---|
| Logistic regression | 0.8495 | Not reported | Best test performance |
| Random forest | Not reported | Not reported | Train–test accuracy gap of 0.1084, indicating overfitting |

- The test set is roughly 180 rows (20% holdout). At an AUC near 0.85, the standard error is about 0.03, so the 95% interval is roughly ±0.06. The gap between the two models should be read against that uncertainty.
- Cross-validation was run but its fold-level results were not reported.
- Accuracy, precision, recall, and F1 were requested but not reported, so threshold-dependent performance cannot be stated.

**Feature importance**
- **Logistic regression:** Sex has the largest standardized coefficient (1.234).
- **Random forest:** Sex is the top impurity-based feature (importance 0.315). Permutation importance also ranks Sex first for test ROC-AUC, though the values were not reported.
- **Pclass, Fare, Age, and family size:** Their importances were not reported, so their predictive contributions are unconfirmed.

**Correction to the source interpretation.** The synthesis describes the Sex coefficient as a 1-SD effect that multiplies odds by 3.43, and suggests reading this as "being female multiplies the odds of survival by roughly 3.4." This is not supported by the data. The crude odds ratio from the contingency table is about 12.4, and a standardized coefficient of 1.234 on a binary variable with SD ≈ 0.48 corresponds to a raw odds ratio closer to 13. The adjusted odds ratio (controlling for class, age, and fare) will be smaller than the crude value, but the "3.4" figure should not be used. The correct adjusted odds ratio should be read directly from the unstandardized model coefficients.

**Predictive insights**
- Sex and class carry most of the predictive signal, consistent across the statistical tests, group rates, and both models.
- A parsimonious logistic model generalizes better than the random forest on this sample.
- The random forest's importance rankings should be treated cautiously because the model itself is less reliable.

## Synthesis

**Validated, consistent findings**
- **Sex is the dominant predictor.** It appears in the chi-square test, the survival rates, the logistic coefficients, and the random forest importances.
- **Class is the second consistent signal.** It is significant in the chi-square test and is associated with age composition and fare.
- **Simpler models generalize better.** The logistic regression outperformed the overfitting random forest.

**Findings with partial support**
- **Age has a weak direct association with survival** (p = 0.041). Its incremental predictive value was not measured.
- **Family size is non-linear.** Both solo travellers and very large families did worse. This suggests a categorical encoding rather than a linear term, but the effect was not formally tested.
- **Missingness carries signal.** Survival differs by Age missingness, but no formal test was reported.

**Likely but untested relationships**
- **Sex × Pclass interaction.** Female survival appears high across classes while male survival is low, especially in third class. This is the most plausible source of variance that main-effects models miss.
- **Fare effect after adjusting for class.** Fare may add little once class is included.

**Data-handling implications**
- Class, age, and fare are correlated, so modeling them together risks multicollinearity. No variance inflation factors were reported.

## Conclusions

**What we can say with confidence**
1. Sex is the strongest predictor of survival in this dataset. Women survived at 74.2% and men at 18.9%, a large and highly significant difference (χ² test p = 1.2e-58; φ ≈ 0.54).
2. Passenger class is strongly associated with survival (63.0% first class vs. 24.2% third class; p = 4.5e-23).
3. A logistic regression with main effects is a reasonable baseline, with test ROC-AUC of 0.85 (approximately ±0.06 at 95% confidence).
4. Random forest does not improve on the logistic baseline in its current form.
5. Age missingness is probably not random and should be handled with an indicator rather than by dropping rows.

**What we cannot yet conclude**
1. The independent effect of Fare, Age, or family size after adjusting for class and sex.
2. Whether the female advantage differs across classes (interaction).
3. Classification performance at any practical threshold.
4. The correct handling of Cabin and Embarked.
5. The exact magnitude of the adjusted sex effect.

## Limitations & Caveats

**Data quality issues**
- Age is 19.9% missing, and the missingness is informative.
- Cabin is 77.1% missing. Its handling decision was not reported, and its missingness was not tested against class or survival.
- Embarked is missing for 2 rows. No handling decision was reported.
- Age contains 11 IQR outliers.

**Statistical assumptions and limitations**
- The Age t-test is borderline (p = 0.041) and Age is likely right-skewed. A non-parametric check (Mann–Whitney U) was not run.
- Effect sizes were not reported for the t-tests, the ANOVA, or the Pclass chi-square test.
- The standardized coefficient for a binary predictor is not directly interpretable as a per-unit odds change, and the "3.4" odds figure in the source should not be used.
- Impurity-based random forest importance favors continuous and high-cardinality features. The fact that Sex still ranks first strengthens its finding, but impurity values should not be compared directly with coefficient magnitudes.
- Pclass, Fare, and Sex are correlated, and no collinearity diagnostics were reported.

**Modeling and evaluation limitations**
- Results come from a single stratified split (about 180 test rows), which gives wide uncertainty.
- Accuracy, precision, recall, F1, and calibration were not reported.
- The random forest overfitting was diagnosed but not resolved. No regularized or depth-limited model was reported.
- It is unclear whether the Pclass × Sex imputation medians were computed on the full dataset or only on the training split. If the former, test-set information leaked into preprocessing. This must be verified.

**Failed analyses**
- No task failed (6 of 6 completed). However, several requested outputs were not reported: model accuracy and related metrics, cross-validation results, Cabin and Embarked decisions, and family-size statistics.

**Missing information**
- Second-class survival rate and class-level counts
- Effect sizes for the t-tests, ANOVA, and Pclass chi-square
- Random forest test ROC-AUC
- Permutation importance values

## Recommendations

### Immediate Actions

1. **Adopt the logistic regression as the baseline model** and report it with its ROC-AUC and confidence interval. Do not deploy the random forest in its current form.
2. **Verify the imputation pipeline.** Confirm that Pclass × Sex medians are computed on training data only. Keep the `Age_missing` indicator.
3. **Document the Cabin and Embarked decisions.** Drop Cabin unless a deck or "has cabin" feature is justified by testing. Impute Embarked (2 rows) with the mode and record the choice.
4. **Report full classification metrics** (accuracy, precision, recall, F1, and confusion matrix) at a stated threshold, and choose that threshold based on the use case.
5. **Correct the odds-ratio interpretation** in all stakeholder materials. Report the adjusted odds ratio from the unstandardized model, not the "3.4" figure.
6. **Use the findings for stakeholder communication:** sex and class are the primary drivers of survival in this dataset, and this is well supported.

### Future Analysis

1. **Test the Sex × Pclass interaction** in the logistic model with a likelihood-ratio test.
2. **Quantify the family-size effect.** Create a categorical family-size variable (SibSp + Parch + 1), report survival by category, and test it with a chi-square test. Check whether it persists after adjusting for class and sex.
3. **Measure the incremental value of Age and Fare** with nested models or a change in ROC-AUC after adding each variable to a base model with Sex and Pclass.
4. **Test whether Age missingness is associated with survival** (chi-square) and examine what drives it (class, sex, ticket group).
5. **Evaluate title extraction** (Mr, Mrs, Miss, Master) for imputation and as a predictor.
6. **Tune or regularize the random forest** (depth limits, minimum leaf size) or use gradient boosting, and compare with cross-validated log-loss and ROC-AUC.
7. **Use repeated cross-validation** to produce confidence intervals for all model comparisons.
8. **Check calibration** of predicted probabilities before using them for ranking or risk scores.

### Data That Would Help

- Complete fare and cabin records, including deck location and proximity to lifeboats
- Verified ages for the 177 passengers currently missing them, or a documented reason for the gaps
- Ticket-level information for group and family relationships beyond SibSp and Parch
- Outcome data for passengers who were not in the dataset, to test generalization beyond this sample