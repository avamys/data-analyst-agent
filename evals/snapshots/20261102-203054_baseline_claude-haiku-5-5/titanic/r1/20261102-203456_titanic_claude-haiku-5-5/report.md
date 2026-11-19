# Data Analysis Report: Titanic Passenger Survival

## Executive Summary

- **Sex is the dominant predictor of survival.** Women survived at 74.2% (233 of 314) versus 18.9% for men (109 of 577). The association is highly significant (χ² p = 1.2×10⁻⁵⁸, Cramér's V ≈ 0.54), and the adjusted odds ratio for female is 3.91.
- **Survival is predictable well above chance.** A logistic regression reaches 80.5% test accuracy and ROC-AUC 0.843, about 19 points above the 61.6% majority-class baseline. Cross-validated accuracy is 80.2% ± 1.4%, so the result is stable.
- **Passenger class and embarkation port are also associated with survival,** but more weakly. Pclass is significant (p ≈ 4.5×10⁻²³) and Embarked is significant (p ≈ 1.8×10⁻⁶). The Pclass effect size is about V ≈ 0.34 and Embarked about V ≈ 0.17, though these values are not verified in the output.
- **The model can rank passengers by survival likelihood, but it is not yet validated for probability estimates or model selection.** Calibration was not assessed, and the random forest comparison was not reported. Decisions that depend on exact probabilities should wait for these checks.

## Dataset Overview

- **Source:** `/workspaces/agents/evals/data/titanic.csv`
- **Size:** 891 passengers × 12 columns
- **Target variable:** `Survived` (binary; 1 = survived, 0 = did not survive)
- **Overall survival:** 38.4% (342 survived, 549 did not)
- **Features:** 7 numeric and 5 categorical, including identifiers and free text (`PassengerId`, `Name`, `Ticket`, `Cabin`)
- **Missing data:** Age is missing for 177 rows (19.9%). Cabin is missing for about 77% of rows. Embarked is missing for about 0.2% (2 rows).

## Analysis Methodology

### Strategic Approach

The analysis proceeded in three stages:

1. **Exploratory analysis first.** Distributions, missingness, and category frequencies were examined before any testing. This was necessary because the data mixes numeric and categorical features and has substantial missingness in Age and Cabin.
2. **Statistical testing second.** Chi-square tests were applied to categorical features against survival, and Age and Fare were to be compared across survival groups. These tests confirm which relationships are real before modeling.
3. **Predictive modeling last.** A binary target and 891 rows support a train/test split and cross-validation. Because the dataset is small, feature importance and model comparisons were interpreted cautiously.

Identifiers and free-text fields were excluded or deferred to avoid leakage and noise. `PassengerId` was removed. `Cabin` was dropped because of its high missingness. `Name` and `Ticket` were not used.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory (EDA) | 2 |
| Statistical | 2 |
| Machine Learning | 2 |
| **Total** | **6 of 6 (100% success)** |

Total execution time was 48.7 seconds. All tasks reported completion, but several outputs were truncated (see Limitations).

## Key Findings

### Exploratory Analysis

- **Target distribution:** 38.4% survived and 61.6% did not. This is a moderate imbalance. It is not severe, but accuracy alone is a weak measure, so AUC should be reported alongside it.
- **Sex:** 314 passengers were female (35.2%) and 577 male (64.8%). Female passengers had a survival rate of 74.2% (95% Wilson CI: 69.1%–78.7%), roughly four times the male rate of 18.9%.
- **Missingness:**
  - Age: 177 missing (19.9%). Age was imputed for modeling.
  - Embarked: about 0.2% missing. Imputation has negligible effect.
  - Cabin: about 77% missing. Dropped from modeling.
- **Not available:** The output does not include the Age and Fare distributions, outlier counts, the numeric correlation matrix, or any test of whether missingness is related to survival. These gaps are discussed below.

### Statistical Evidence

The Bonferroni-adjusted significance threshold for three tests is α = 0.0167.

| Hypothesis | Test | Result | Significance (α = 0.0167) | Effect Size |
|---|---|---|---|---|
| Survival depends on Sex | χ² test of independence | p = 1.2×10⁻⁵⁸ | Significant | Cramér's V ≈ 0.54 |
| Survival depends on Pclass | χ² test of independence | p ≈ 4.5×10⁻²³ | Significant | V ≈ 0.34 (unverified) |
| Survival depends on Embarked | χ² test of independence | p ≈ 1.8×10⁻⁶ | Significant | V ≈ 0.17 (unverified) |
| Female sex increases survival odds | Logistic regression coefficient | OR = 3.91 | Supported | Adjusted odds ratio |

**Plain-English interpretation:**

- **Sex:** This is the strongest and most reliable finding. The 2×2 contingency table is complete in the output, so the effect size of V ≈ 0.54 can be checked directly from the counts. The crude odds ratio is about 12.4. After adjusting for other features, the odds ratio falls to 3.91, which indicates that part of the crude gap is explained by other variables, most likely class and age.
- **Pclass and Embarked:** The output does not label these p-values. They were assigned by order and by known Titanic results. Their effect sizes are back-calculated from published Titanic χ² values rather than from this output, so they should be treated as provisional until confirmed against the raw results.
- **Age and Fare:** The group comparisons and numeric correlations with `Survived` were not reported. No conclusion can be drawn about these variables from the statistical evidence.

### Predictive Models

**Model types tested**

- **Logistic regression (baseline):** Trained on Sex, Pclass, Embarked, Age, SibSp, Parch, and Fare, with Age imputed and categoricals encoded. PassengerId, Name, Ticket, and Cabin were excluded.
- **Random forest:** Intended as a comparison model. Results were not reported.

**Performance (logistic regression)**

| Metric | Value | Notes |
|---|---|---|
| Test accuracy | 80.45% | 144 of 179 correct |
| Training accuracy | 81.04% | Gap of 0.6 points, no sign of overfitting |
| Cross-validated accuracy | 80.20% ± 1.42% | Preferred estimate given the small hold-out set |
| ROC-AUC (test) | 0.843 | Good discrimination |
| Majority-class baseline | 61.6% | Always predicting "did not survive" |
| Precision, recall, F1 | Not reported | Needed for a complete classification picture |

The hold-out set has 179 rows, so the standard error of test accuracy is about ±3 percentage points. The CV estimate is more reliable.

**Feature importance**

- **Sex (female):** The strongest driver, with an adjusted odds ratio of 3.91. This is the only feature importance that can be stated with confidence.
- **Other features:** Rankings were not available because the random forest importances were not reported. Impurity-based importances tend to favor continuous variables such as Age and Fare, so they should be interpreted with care even when reported.

**Predictive insights**

- The model separates survivors from non-survivors well (AUC 0.84), and the cross-validated accuracy closely matches the hold-out accuracy.
- Performance is driven primarily by Sex, with class and port adding information.
- No model can yet be declared superior, since the random forest comparison is missing.

## Synthesis

The strongest cross-cutting result is that **Sex is the dominant factor in survival**, and two independent analyses support it. The χ² test shows a large, highly significant association (V ≈ 0.54), and the logistic regression assigns it the largest effect (adjusted OR = 3.91). This matches the well-documented pattern from the disaster, in which women and children were prioritized for lifeboats and first-class passengers had better access to them.

**Validated:**
- Sex is strongly associated with survival (validated by χ² test and logistic regression).
- A logistic regression on these features predicts survival with about 80% accuracy and AUC 0.84, with stable cross-validation.

**Provisionally supported (pending verification):**
- Pclass and Embarked are associated with survival. Their p-values are significant, but their labels and effect sizes need confirmation.

**Not yet supported:**
- Any claim about Age or Fare, which were not tested in the output.
- Any claim that random forest outperforms or underperforms logistic regression.
- Any interaction effects (such as Sex × Pclass).

There were no contradictions between the statistical and machine learning results.

## Conclusions

**What we can say with confidence:**

1. **Sex was the single strongest determinant of survival.** Women survived at 74.2% versus 18.9% for men.
2. **Passenger features predict survival reasonably well.** A simple logistic model achieves about 80% accuracy and AUC 0.84, and this performance holds under cross-validation.
3. **Overall survival was 38.4%,** so any model should be judged against the 61.6% baseline and assessed with AUC as well as accuracy.

**What we can say with moderate confidence:**

4. Passenger class and port of embarkation are associated with survival. The direction and rough size are consistent with the historical record, but the exact figures need confirmation.

**What we cannot yet say:**

5. Whether Age and Fare differ by survival status.
6. Whether a random forest or another model would perform better.
7. How well calibrated the predicted probabilities are.
8. Whether the associations of Pclass and Embarked hold after adjusting for each other and for Sex.

## Limitations & Caveats

**Data quality issues**
- Age is missing for 19.9% of passengers. The imputation method is not specified, and imputation may bias the Age coefficient toward the median.
- Cabin is missing for about 77% of passengers and was dropped entirely. Any information it holds, such as deck location, is lost. Whether missingness itself relates to survival was not tested.
- Name was not used. Titles (Mr, Mrs, Master) could carry information about age and social status that the model does not capture.

**Statistical assumptions and validity**
- The χ² test assumes expected cell counts of at least 5. This is likely met for Sex and Pclass, but should be checked for Embarked, which has small groups.
- The Pclass and Embarked results are not labeled in the output, so their attribution relies on order and external reference values.
- The class balance is moderate (38/62), not absent as assumed in the strategy. Accuracy should be read alongside AUC and ideally precision and recall.
- The hold-out set (n = 179) is small. Differences of 1–2 points between models are not reliable.
- Permutation importance on this sample size is unstable.
- All findings are associational. They describe the 1912 passenger manifest and do not establish causation.

**Failed or incomplete analyses**
- No tasks failed, but the following outputs were truncated or missing:
  - Age and Fare comparisons across survival groups
  - Numeric correlations with `Survived`
  - EDA outlier and correlation matrix results
  - Missingness-versus-survival analysis
  - Cabin and Name/Ticket profiling
  - Random forest results and the RF-versus-baseline comparison
- Confidence intervals for model accuracy and AUC were not reported.
- Calibration was not assessed.

**Missing information**
- Precision, recall, and F1 for the classifier.
- Effect sizes for Pclass and Embarked computed directly from the output.
- Interaction tests.

## Recommendations

### Immediate Actions

1. **Use the logistic regression for ranking, not for precise probability estimates.** An AUC of 0.84 and a CV accuracy of about 80% support ranking passengers by survival likelihood in analytical settings. Calibration has not been checked, so do not use the predicted probabilities as calibrated risk scores yet.
2. **Treat Sex as the core explanatory variable in any reporting.** It is the most robust and interpretable finding, with strong evidence from two methods.
3. **Re-run or retrieve the truncated outputs before drawing conclusions about Age, Fare, or model choice.** Priority items are the Age/Fare tests, the random forest comparison, and the missing Pclass and Embarked labels.
4. **Report AUC and accuracy together, against the 61.6% baseline.** Accuracy alone overstates performance on an imbalanced outcome.
5. **Do not deploy a model for individual decisions yet.** The sample is small, the comparison is incomplete, and calibration is unknown.

### Future Analysis

**Priority analyses**
- Complete the Age and Fare group comparisons with confidence intervals and effect sizes (Mann-Whitney or t-test, as appropriate for the distributions).
- Compare the random forest with the logistic regression using repeated or nested cross-validation, reporting AUC, precision, recall, and F1.
- Test the Sex × Pclass interaction. The "women and children first" pattern suggests it may be present, and a main-effects model would miss it.
- Confirm whether Embarked's association persists after adjusting for Pclass.
- Assess calibration with a reliability curve and Brier score.

**Feature engineering**
- Extract titles from `Name` and test whether they add predictive value beyond Sex.
- Test whether Cabin missingness, or deck derived from Cabin, predicts survival.
- Run a sensitivity analysis with alternative Age imputations (median by Sex and Pclass, or model-based) to check robustness.
- Consider family-size features (SibSp + Parch + 1) and ticket-group features.

**Data to collect or add**
- Age for the 177 passengers with missing values, or a verified source for them.
- Cabin or deck information from original passenger records.
- Larger or more recent datasets to reduce the variance of hold-out estimates.
- Outcome data from comparable events, to test whether the patterns generalize beyond this single disaster.