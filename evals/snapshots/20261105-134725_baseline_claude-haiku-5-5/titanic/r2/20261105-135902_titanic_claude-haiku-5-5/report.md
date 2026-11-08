# Data Analysis Report: Titanic Survival

**Data source:** `/workspaces/agents/evals/data/titanic.csv`
**Status:** Complete, with caveats (see Limitations & Caveats)

> **Note on figures:** Most values in this report come directly from the analysis outputs. A few come from the synthesis step as "reference values" that were not in the raw output (flagged as *[reference, unverified]*). Several model-level metrics appear only in the synthesis summary, and the outputs contain conflicting attributions for some of them. These are identified where they occur.

---

## Executive Summary

- **Sex is the dominant predictor of survival.** Survival was strongly associated with sex (χ² = 263.05, p ≈ 3.7 × 10⁻⁵⁹, Cramér's V = 0.543, a large effect). Sex was also the most important feature in the random forest (importance 0.174), more than any other single feature.
- **Passenger class and social-status proxies carry most of the remaining signal.** Pclass, Title, and Sex form the core predictive group. Pclass was significant in the chi-square screening, though its test statistic is not reported in the output.
- **A simple model performs well and is hard to beat.** The best model reached 79.89% test accuracy (143/179), about 18.4 percentage points above the 61.45% majority-class baseline. The 95% interval for that estimate is roughly 74–86%, so the result is solid but not precise.
- **Cabin information is informative mainly because it reflects class.** Passengers with a recorded cabin survived at 66.67%, versus 29.99% without. Cabin is 77.1% missing, and its apparent effect largely overlaps with the Pclass effect.
- **The findings are descriptive of the 1912 passenger population.** They are useful as a benchmark and for understanding the data, but they should not be used to make decisions about current individuals or events.

---

## Dataset Overview

| Attribute | Value |
|---|---|
| Rows | 891 |
| Columns | 12 |
| Target | `Survived` (binary: 0 = did not survive, 1 = survived) |
| Numeric features | 7 (PassengerId, Pclass, Age, SibSp, Parch, Fare, Survived as target) |
| Categorical features | 5 (Name, Sex, Ticket, Cabin, Embarked) |
| Class balance | Not severe; majority class (did not survive) is 61.45% in the test split |

**Key data characteristics:**
- **Age:** 177 missing (19.87%). Missingness is concentrated in Pclass 3, though the exact rate for that class is not legible in the output.
- **Cabin:** 687 missing (77.10%).
- **Embarked:** 2 missing (0.22%).
- **Fare:** Right-skewed (skewness 4.79), with 116 IQR outliers (13.02%). These are plausible high first-class fares and were retained.
- **Age IQR outliers:** 11 (1.54% of non-missing values).

---

## Analysis Methodology

### Strategic Approach

The analysis followed a three-stage sequence:

1. **Exploratory analysis first.** The dataset has substantial missingness in Age and Cabin, and its structure needed to be understood before any modeling. Missing-value patterns and distributions were examined first.
2. **Statistical testing second.** Chi-square tests (categorical features vs. survival) and t-tests (Age and Fare by survival status) were used to identify which features have evidence of association. A Bonferroni correction was applied across five tests (corrected α = 0.010).
3. **Predictive modeling last.** With a binary target and 891 rows, a stratified 80/20 train/test split was used. Feature selection was informed by the statistical screening. Because the classes are not severely imbalanced, accuracy was used as the primary metric, with AUC as a secondary metric.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory Data Analysis (EDA) | 2 |
| Statistical | 1 |
| Machine Learning | 3 |
| **Total** | **6 of 6 (100% success, 0 failed)** |

Total execution time: 54.3 seconds.

---

## Key Findings

### Exploratory Analysis

**Data structure and missingness**
- Age is missing for 177 passengers (19.87%). Imputation is therefore a material decision, and the Age test depends on it.
- Cabin is missing for 687 passengers (77.10%). Its missingness is structured, not random: it is associated with lower class. The missingness pattern itself carries information, which supports keeping a `HasCabin` indicator.
- Embarked is missing for only 2 passengers, so its imputation has negligible effect.

**Distributions and outliers**
- Fare is strongly right-skewed (skewness 4.79). It should be log-transformed or handled with robust methods before any linear modeling.
- 116 Fare values (13.02%) fall outside the IQR fences. These reflect genuine high-fare, first-class tickets, so they were kept.
- 11 Age values (1.54%) are IQR outliers, computed on non-missing values only.

**Survival by cabin status**

| Group | Passengers (approx.) | Survival rate |
|---|---|---|
| Cabin recorded | 204 | **66.67%** (136 survived) |
| Cabin missing | 687 | **29.99%** (206 survived) |

Both group counts reconcile with the total of 891 and with the 687 missing-cabin figure.

### Statistical Evidence

Five tests were run with a Bonferroni-corrected significance threshold of α = 0.010. The outputs report the following.

**Test 1: Pearson chi-square, Sex vs. Survived (fully reported)**

| Statistic | Value |
|---|---|
| χ² | 263.051 |
| Degrees of freedom | 1 |
| p-value | 3.71 × 10⁻⁵⁹ |
| Cramér's V | 0.543 (large effect) |
| Result | **Reject independence** (p far below 0.010) |

*Interpretation:* Survival differed sharply by sex. Sex alone explains a large share of the variation in survival outcomes. The Cramér's V of 0.543 is among the largest effect sizes typically seen in social data.

**Other tests (summarized from output)**

| # | Hypothesis | Test | Result at α = 0.010 | Effect size |
|---|---|---|---|---|
| H1 | Survival is independent of Sex | χ² | **Reject** | Cramér's V = 0.543 |
| H2 | Survival is independent of Pclass | χ² | **Reject** | Not reported in output |
| H3 | Survival is independent of Embarked | χ² | Reject (per summary) | Not reported; likely small |
| H4 | Mean Age is equal for survivors and non-survivors | t-test | **Reject** | Not reported; direction not stated |
| H5 | Mean Fare is equal for survivors and non-survivors | t-test | **Reject** | Not reported |

*Caveats on the table:* The output reports three χ² rejections and two t-test rejections, which is consistent with the five tests. However, only the Sex test's full statistics are shown. P-values for the other tests are not reported, so their relative strength cannot be ranked. The Fare t-test is also questionable given the skewness (see Limitations).

*[Reference, unverified]* Commonly cited values for this dataset are Cramér's V ≈ 0.34 for Pclass and survival rates of roughly 74% for women and 19% for men. These are not in the analysis output and should be verified against the raw results before citation.

**What is not yet established**
- The *direction* of the Age and Fare effects. The output says the means differ, but not whether survivors were younger or older, or paid more or less.
- Whether children (rather than Age as a continuous variable) had elevated survival. This was not tested directly.
- Whether the Sex effect differs by class (interaction).

### Predictive Models

**Setup:** Stratified 80/20 train/test split, with the test set containing 179 passengers. Imputation statistics were computed on training data only. Models included a logistic regression baseline and a random forest.

**Performance (held-out test set, n = 179)**

| Metric | Value | Notes |
|---|---|---|
| Test accuracy | **79.89%** (143/179) | Model not named in the output |
| Majority-class baseline | 61.45% (110/179) | Predict "did not survive" for everyone |
| Gain over baseline | +18.4 percentage points | |
| ROC AUC (best model) | **0.8723** | Logistic regression, per the ML summary |
| ROC AUC (second value) | 0.839 | Model not identified in the output |
| Random forest train–test accuracy gap | 8.6 points | Moderate overfitting |
| Precision, recall, F1, confusion matrix | Not reported | |

**Confidence in the test estimate:** The standard error for accuracy at n = 179 is about 3 points, giving an approximate 95% interval of **74–86%**. Differences of 1–2 points between models are within noise.

**Model comparison:** Logistic regression is reported as the best model by AUC (0.8723). Because the logistic regression matched or outperformed the random forest, the signal appears to be largely additive and low-dimensional (sex, class, title). A more complex model adds little and overfits modestly.

**Feature importance**

| Rank | Feature | Importance | Source |
|---|---|---|---|
| 1 | `Sex_female` | 0.174 (random forest impurity) | ML output |
| 2 | Title, Pclass, Sex (dominant group) | Not quantified | ML summary |
| 3 | Fare, Deck, HasCabin, IsAlone, Embarked | Secondary; not quantified | Bonferroni screen and ML summary |

Impurity-based importance favors continuous and high-cardinality features, so these rankings should be confirmed with permutation importance.

**Predictive insights**
- Most of the predictive signal is captured by a few variables: sex, class, and title. Title is a compressed signal that encodes sex and age (Master/Miss vs. Mr/Mrs), which is why it screens strongly.
- Engineered features (Title, Deck, HasCabin, IsAlone) passed the statistical screen alongside the raw variables, which suggests that feature engineering on Name and Cabin adds information.

---

## Synthesis

**Validated, consistent patterns**
1. **Sex is the strongest and most consistent signal** across statistical tests, feature importance, and the predictive model.
2. **Class-related variables carry the next layer of signal.** Pclass, Title, and Fare are linked to one another and to survival, so their effects overlap.
3. **Cabin's effect is largely a class effect.** Recorded cabins are concentrated in higher classes, so HasCabin primarily captures class and record-keeping, not an independent effect.
4. **Missingness is structured, not random.** Cabin and Age missingness are both associated with class. Keeping missingness indicators is justified.
5. **The signal is simple.** A low-complexity model performs as well as or better than a complex one.

**Cross-cutting relationships (hypotheses to test, not yet confirmed)**
- **Sex × Class interaction:** The "women first" pattern may be stronger in higher classes. Not tested.
- **Fare and Pclass collinearity:** Fare likely tracks class closely. This should be checked before both enter a linear model.
- **Hub-variable effect:** Pclass links to Cabin recording, Fare, Embarked port, and Age missingness, so its influence may appear in several features at once.

---

## Conclusions

**What we can say with confidence**
1. Survival in this dataset was strongly associated with sex. The association is large (Cramér's V = 0.543) and highly significant (p ≈ 4 × 10⁻⁵⁹).
2. Passenger class and title carry substantial additional predictive signal.
3. A simple model using sex, class, and title-related features achieves about 80% accuracy on held-out data (95% interval roughly 74–86%), well above the 61% majority baseline.
4. Recorded cabin status is associated with much higher survival (66.7% vs. 30.0%), but this association is largely explained by class.

**What we cannot yet say**
- The size and direction of the Age and Fare effects.
- Whether the sex effect varies by class.
- Whether children specifically had elevated survival.
- Which model produced the 79.89% accuracy and the 0.839 AUC.
- Precision, recall, and calibration of the classifier.

---

## Limitations & Caveats

**Data quality issues**
- **Age (19.87% missing):** The Age t-test depends on the imputation method. Results should be checked against alternative imputation (median, Title × Pclass group means).
- **Cabin (77.10% missing):** Cabin-derived features rest mainly on whether a cabin was recorded, which is closely tied to class.
- **Fare outliers and skew (4.79):** Real but extreme. The skew violates the normality assumption of the t-test.
- **Embarked (2 missing):** Negligible impact.

**Statistical assumptions and limitations**
- **t-tests on skewed Fare:** Assumption violated. A Mann-Whitney U test or log-transformed Fare is needed. The Fare t-test result should be treated as provisional.
- **Chi-square with small expected counts:** Some cells, particularly for Embarked and within small Pclass groups, may have expected counts below 5. Fisher's exact test should be used for those tables.
- **Multiple comparisons:** Bonferroni was applied to the five initial tests. Engineered-feature screens and model comparisons add further unadjusted comparisons.
- **Incomplete reporting:** Exact p-values and effect sizes for four of the five tests are not shown, so the strength of each result cannot be ranked.

**Methodological concerns**
- **Feature-selection leakage:** Statistical screening appears to have run on all 891 rows before the train/test split. The selected features were therefore partly chosen using test-set information, which inflates the reported test performance. Screening should be repeated within training folds.
- **Small test set:** 179 rows gives an accuracy standard error of about 3 points. Model differences smaller than that are not reliable.
- **Overfitting description:** The random forest's 8.6-point train–test gap is moderate, not severe.

**Inconsistencies in the outputs**
- **Model attribution:** The 79.89% accuracy and 0.839 AUC are not tied to a named model. The 0.8723 AUC is attributed to logistic regression. Until the outputs are reconciled, the logistic regression's advantage over the random forest should be treated as likely but unconfirmed.
- **Feature list mismatch:** Eight features passed the Bonferroni screen, including Title, Deck, HasCabin, and IsAlone. The statistical tests shown covered only Sex, Pclass, Embarked, Age, and Fare. The engineered-feature tests were either truncated or were run on a different basis.
- **Truncated or duplicated output:** Several summary lines are repeated or cut off, and the correlation matrix is incomplete. These fragments were not used as evidence.

**Failed analyses:** None. All six tasks completed successfully.

**Missing information**
- Exact p-values and effect sizes (Cramér's V, Cohen's d, or rank-biserial) for Pclass, Embarked, Age, and Fare tests
- Confusion matrix, precision, recall, F1, and calibration
- Confidence intervals for AUC
- Permutation importance and partial dependence or SHAP values
- Numeric correlation values
- Tests of the Sex × Pclass interaction
- Ticket and PassengerId were not evaluated

**Scope limitation:** This is historical data on 891 passengers from a single 1912 voyage. Findings describe that population and should not be generalized to other disasters, time periods, or decision contexts without further evidence.

---

## Recommendations

### Immediate Actions

1. **Use the sex–class–title model as a benchmark, not a decision tool.** It achieves about 80% accuracy, but the 95% interval is 74–86%, and the data describes a historical population.
2. **Correct the analysis pipeline before reporting results further:**
   - Rerun the statistical feature screen inside training folds only.
   - Apply a log transform or robust scaling to Fare, and use Mann-Whitney in place of the Fare t-test.
   - Use Fisher's exact test for sparse contingency tables.
3. **Reconcile the model attribution.** Confirm which model produced 79.89% accuracy and 0.839 AUC, and report precision, recall, F1, and a confusion matrix for each.
4. **Report the full statistics for every test.** Exact p-values and effect sizes should be included for all five hypotheses.
5. **Do not interpret the Cabin effect as independent of class.** Any stakeholder summary should state that the cabin-survival association is largely a class effect.

### Future Analysis

**Statistical questions**
1. **Does the sex effect differ by class?** Test the Sex × Pclass interaction in logistic regression or with stratified analysis.
2. **Is there an independent Cabin effect?** Fit a model with Pclass and HasCabin together and check whether HasCabin remains significant.
3. **Is there a child effect?** Compare survival for passengers under 10 or under 15 against adults, controlling for sex and class.
4. **Is the Age and Fare association robust?** Test under alternative imputation methods and use non-parametric tests. Report the direction of each effect.
5. **Is the logistic regression advantage real?** Use repeated stratified cross-validation with confidence intervals on the difference between models.

**Modeling questions**
6. **Which features survive rigorous selection?** Check whether Title, Deck, and IsAlone remain significant after selection is nested within cross-validation folds.
7. **Are Fare and Pclass separable?** Test whether Fare has signal after controlling for Pclass. If it does, the effect may reflect group travel or port of embarkation rather than wealth alone.
8. **Does ticket sharing add signal?** Shared tickets may indicate family or group travel, which could be a stronger social signal than IsAlone. Ticket has not yet been evaluated.

**Data to collect or improve (if this analysis is extended or reused)**
- **Complete cabin records,** or a documented reason for missingness, to separate record-keeping effects from class effects.
- **Complete age records,** with the imputation method documented.
- **Group or family identifiers,** beyond SibSp and Parch, to capture social-group travel more accurately.
- **Verified outcome and feature metadata** (data dictionary, collection dates, and source provenance) to support reproducibility.