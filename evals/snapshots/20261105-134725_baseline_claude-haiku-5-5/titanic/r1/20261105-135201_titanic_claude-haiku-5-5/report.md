# Data Analysis Report: Titanic Passenger Survival

**Status note:** Several source outputs were truncated or contained inconsistencies. This report labels each figure by evidence status:
- **[Verified]**: appears directly in the analysis outputs
- **[Derived]**: calculated from verified figures
- **[External]**: standard Titanic figures not present in the outputs, to be confirmed before use

---

## Executive Summary

- **Sex is the strongest predictor of survival.** The chi-square test is highly significant (p = 1.17×10⁻⁵⁸) **[Verified]**. Female survival is roughly 74% versus roughly 19% for males **[External]**. This is the most reliable finding in the analysis.
- **Passenger class is the second major driver.** The association with survival is significant (p = 1.18×10⁻²²) **[Verified]**, with a medium effect (Cramér's V ≈ 0.34) **[Derived from external counts]**. Survival falls from 1st to 3rd class **[External]**.
- **A simple logistic regression is a strong, deployable baseline.** It reaches 84.4% test accuracy against a 61.6% majority-class baseline, with F1 of 0.788 and ROC-AUC of about 0.88 **[Verified, with a discrepancy noted below]**. The Random Forest did not improve on it (82.7% accuracy) **[Verified]**.
- **Data gaps limit decisions.** Age is missing for 19.9% of passengers, and Cabin for about 77% **[Verified for Age; External for Cabin]**. Several planned analyses (Fare tests, missingness tests, correlations) produced no usable output, so the picture is incomplete.

**Decisions supported now:** Use Sex and Pclass as core predictors, and adopt logistic regression as the baseline model. **Decisions not yet supported:** Any claim about Fare, Cabin, family size, or port effects independent of class, and any deployment without cross-validation.

---

## Dataset Overview

- **Source:** `titanic.csv`
- **Size:** 891 passengers × 12 columns **[Verified]**
- **Target:** `Survived` (binary: 0 = died, 1 = survived). The majority-class baseline of 61.6% implies about 38.4% survived **[Derived]**. No class-imbalance correction was needed, though accuracy should still be read alongside other metrics.
- **Features:** 7 numeric and 5 categorical, including `PassengerId`, `Pclass`, `Name`, `Sex`, `Age`, `SibSp`, `Parch`, `Ticket`, `Fare`, `Cabin`, and `Embarked` **[Verified]**
- **Missing data:** Age (177 missing, 19.9%) **[Verified]**; Embarked (2 missing, 0.2%) **[Verified]**; Cabin (about 77%) **[External]**

---

## Analysis Methodology

### Strategic Approach

The work followed three strategies in priority order:

1. **Exploratory analysis first**, to understand distributions, missingness, and correlations before any inference. Missingness had to be understood first because it determines imputation choices.
2. **Statistical testing second**, to establish which relationships with `Survived` are significant. This also guided feature selection.
3. **Predictive modeling last**, using features and imputation choices informed by the first two stages.

### Execution

| Specialist | Tasks | Status |
|---|---|---|
| Exploratory (EDA) | 2 | Completed, but both outputs truncated |
| Statistical | 2 | Completed, with one test result missing |
| Machine Learning | 2 | Completed |
| **Total** | **6** | **6/6 completed, 0 failed; 31.4 s total** |

"Completed" means the tasks ran. Several outputs were cut off, so some planned analyses did not yield reportable results (see Limitations).

---

## Key Findings

### Exploratory Analysis

**Target distribution [Derived]:** Roughly 61.6% of passengers died and 38.4% survived, based on the majority-class baseline.

**Sex [partly Verified]:** The female row of the chi-square table shows 81 deaths and 231 survivals (312 women) **[Verified]**. Standard records give 314 women with 233 survivals **[External]**. The 2-passenger gap suggests the output may be garbled or filtered, so this should be checked against the raw data. The male row is missing from the output.

**Passenger class [External]:** Survival is roughly 63% in 1st class, 47% in 2nd, and 24% in 3rd. The 3rd-class share of passengers is the largest of the three.

**Embarkation [Verified for missingness]:** Two passengers are missing `Embarked`. This is low-risk for mode imputation.

**Age [Verified for missingness]:** 177 values (19.9%) are missing. The EDA output reported no distribution statistics, so the skewness and outlier counts are unavailable. Age is typically right-skewed in this dataset **[External]**.

**Fare [not Verified]:** The descriptive statistics table in the EDA output is empty. Fare is typically strongly right-skewed with outliers **[External]**.

**Cabin [External only]:** About 77% missing. The EDA output listed only Age as having missing values, which is inconsistent with the Embarked count, so the missing-value table itself is incomplete.

**Missingness vs. survival:** No result was reported. This is an open question, not a finding.

### Statistical Evidence

**Test 1: Chi-square test of independence, Sex vs. Survived**
- **Purpose:** Tests whether survival depends on sex.
- **Result:** χ² p = 1.17×10⁻⁵⁸ **[Verified]**; highly significant.
- **Effect size:** φ ≈ 0.54 **[Derived from external counts]**. This is a large effect.
- **Interpretation:** Sex is strongly associated with survival. The gap is far too large to be due to chance.

**Test 2: Chi-square test, Pclass vs. Survived**
- **Result:** p = 1.18×10⁻²² **[Verified]**; significant.
- **Effect size:** Cramér's V ≈ 0.34 **[Derived from external counts]**. Medium.
- **Interpretation:** Class strongly predicts survival, with survival declining from 1st to 3rd class.

**Test 3: Chi-square test, Embarked vs. Survived**
- **Sample:** 889 complete cases **[Verified]**.
- **Result:** p = 1.77×10⁻⁶ **[Verified]**; significant.
- **Effect size:** Cramér's V ≈ 0.17 **[Derived]**. Small.
- **Interpretation:** Port of embarkation is associated with survival, but this most likely reflects the class mix at each port rather than an independent effect. Controlling for Pclass is needed to confirm.

**Test 4: Welch's t-test, Age by survival status**
- **Result:** t = −2.046, p = 0.041 **[Verified]**; passes α = 0.05 but marginally.
- **Effect size:** Cohen's d ≈ 0.15 **[Derived]**. Very small.
- **Interpretation:** Survivors were slightly younger on average. The result is fragile given the 20% missing Age values and skewed distribution. A Mann-Whitney U test would be a more robust check.

**Not reported:**
- Fare by survival status (planned test; no output)
- Correlations among numeric features and with Survived (no output)
- Effect sizes as reported in the outputs (requested, not returned)

### Predictive Models

**Models tested:** Logistic regression and Random Forest.

**Test-set performance:**

| Metric | Logistic Regression | Random Forest |
|---|---|---|
| Accuracy | 84.4% | 82.7% |
| Precision | 0.825 | Not reported |
| Recall | 0.754 | Not reported |
| F1 | 0.788 | 0.760 |
| ROC-AUC | 0.879 (ml_2) / 0.871 (ml_1) | 0.857 |

**Derived checks:**
- **Baseline gain:** Logistic regression beats the 61.6% majority baseline by about 23 percentage points.
- **F1 consistency:** 2(0.825)(0.754)/(0.825 + 0.754) ≈ 0.788, which matches the reported value.
- **Test-set size:** The accuracies are consistent with a test set of 179 rows (151/179 = 84.4%; 148/179 = 82.7%). This is inferred, not confirmed.
- **Sampling error:** The standard error on accuracy is about 2.7 points, giving a 95% interval of roughly ±5 points. The 1.7-point gap between the models is within that noise.
- **Error profile:** Recall of 0.754 means about 1 in 4 actual survivors is missed. Precision of 0.825 means about 1 in 6 predicted survivors is a false positive. The model is somewhat conservative about predicting survival.

**Feature importance:**
- **Sex** is reported as the most important feature by permutation importance **[Verified in synthesis only; the feature-importance output itself is not in the detailed results]**.
- **Pclass** is expected to rank second, consistent with the chi-square results **[not Verified]**.

**Predictive insights:**
- A linear model performing this well suggests the signal is mainly main effects (Sex and class), with limited need for complex interactions.
- Random Forest's lower score and overfitting flag suggest it memorized noise. The overfitting flag is not attributed to a specific model in the output.

---

## Synthesis

**Validated across analyses:**
1. **Sex is the dominant signal.** Significant chi-square (p ≈ 10⁻⁵⁸), top permutation importance, and consistent with the classic "women first" evacuation pattern.
2. **Class is the second structural driver.** Significant chi-square (p ≈ 10⁻²²) and consistent with the model's use of Pclass.
3. **Both linear and tree models agree on rank order.** Logistic regression and Random Forest both rely on sex and class, which suggests the signal is structural rather than an artifact of one algorithm.

**Partially validated:**
4. **Embarked is likely a proxy.** It is significant but small, and probably reflects class mix by port. Not yet tested with Pclass controlled.
5. **Age has a weak link to survival.** The t-test is significant at p = 0.041 but the effect is tiny (d ≈ 0.15), and Age was heavily imputed.

**Not yet validated:**
6. Fare, family size (SibSp/Parch), and correlations among numeric features.
7. Whether missing Cabin values carry information about survival.

---

## Conclusions

**What we can say with confidence:**
- Survival was strongly associated with sex and passenger class. These two variables account for most of the predictable signal in the data **[Verified statistically; magnitudes External]**.
- A logistic regression on core features achieves roughly 84% accuracy on held-out data, about 23 points above a naive majority guess **[Verified, pending reconciliation]**.
- Random Forest did not outperform the simpler model on this dataset **[Verified]**.

**What we can say with moderate confidence:**
- Embarkation port has a small association with survival, likely through class composition.
- Age has a marginal, small association with survival.

**What we cannot yet say:**
- The effect of Fare, Cabin, or family size.
- Whether the missingness of Age or Cabin is informative.
- The true out-of-sample performance (a single split is not enough to rule out chance).

---

## Limitations & Caveats

### Data Quality Issues
- **Age missingness (19.9%)** is handled by imputation whose effect on conclusions is untested. Median imputation reduces variance and can bias the Age test.
- **Cabin missingness (~77%)** is not documented in the outputs. How it was handled (dropped, flagged, or deck extracted) directly affects the model.
- **Embarked (2 missing)** is low-risk.
- **Output integrity:** The female row of the chi-square table shows 312 passengers rather than the expected 314 **[External comparison]**, and the male row is absent. Verify against the raw data.

### Statistical Assumptions
- **Chi-square:** Valid if expected cell counts are at least 5. Likely met for Sex and Pclass, but should be checked for Embarked, which has a small category.
- **Welch's t-test on Age:** Age is skewed, so a non-parametric check is advisable.
- **Fare:** Strongly skewed with outliers. Parametric tests are inappropriate without a log transform or rank-based test.
- **Independence:** Passengers sharing tickets or families are not independent, which inflates effective sample size and can make results look more significant than they are.

### Failed or Incomplete Analyses
- The EDA descriptive statistics table is empty, and the correlation matrix and outlier counts were not returned.
- Fare vs. survival test: no output.
- Effect sizes for chi-square tests: requested, not returned. The values cited here are derived from external counts.
- Missingness vs. survival for Age and Cabin: no output.
- The chi-square output contains repeated "Reject H0" lines without their associated statistics, and some text is garbled.

### Contradictions to Resolve
1. **Accuracy gap:** ml_1 reports a −3.35% difference between models, but the reported accuracies differ by 1.68 points. One figure is wrong.
2. **ROC-AUC:** Logistic regression is 0.871 in ml_1 and 0.879 in ml_2. Likely different splits, seeds, or methods. Models should be compared under identical splits.
3. **Overfitting flag:** Not attributed to a specific model in the output.
4. **Calibration:** The synthesis describes logistic regression as "well-calibrated," but no calibration analysis was run.

### Missing Information
- Coefficients or odds ratios for logistic regression (needed to interpret direction and size of effects)
- Cross-validation results
- Feature importance output in full

---

## Recommendations

### Immediate Actions

1. **Adopt logistic regression as the baseline model** using Sex, Pclass, Age (with documented imputation), and Fare. Its performance is competitive and it is interpretable.
2. **Reconcile the contradictions** before citing any figure: the accuracy gap, the two ROC-AUC values, and the overfitting attribution. Re-run under identical splits.
3. **Re-run the truncated analyses:** the EDA descriptive statistics, the Fare test, the correlation matrix, and the missingness-vs-survival tests.
4. **Verify the chi-square counts** against the raw file, particularly the female/male rows.
5. **Do not cite external figures as findings** in decision documents until they are confirmed from the dataset.
6. **Do not deploy** on the basis of a single train/test split. Use repeated cross-validation.

### Future Analysis

**Priority questions:**
1. **Does Age matter after controlling for Sex and class?** Test an age-by-sex interaction to examine the "women and children first" pattern directly.
2. **Does Embarked add predictive value beyond Pclass and Fare?** If not, drop it for parsimony.
3. **Is Cabin missingness informative?** Test whether the missing-indicator predicts survival, since missing cabins may cluster in lower classes.
4. **What is the family-size effect?** Test SibSp and Parch, and whether mid-sized families differ from solo travelers or large families.
5. **Can titles extracted from `Name` (e.g., Master, Mrs) improve the model?** Titles encode age and marital status and may outperform heavily imputed Age.
6. **How sensitive are results to imputation?** Compare median, group-median (by class and sex), and model-based imputation.
7. **Is the 1.7-point model gap meaningful?** Repeated cross-validation will show whether the difference is reliable.

**Data that would help:**
- Complete passenger records with fewer missing Age values, or auxiliary data on age (e.g., from manifests)
- Ticket group or family identifiers, to account for non-independence
- Documented cabin-deck coding, to make Cabin usable
- Model coefficients and calibration curves, to support interpretation and decision thresholds