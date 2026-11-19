# Data Analysis Report: Survey

## Executive Summary

- **The data shows no reliable relationship between any feature and the outcome.** Every univariate test (Welch t-tests, ANOVA/Kruskal-Wallis, with adjustment) failed to reject the null hypothesis at p ≥ 0.05. Neither model found a usable signal.
- **Both predictive models perform worse than chance on the test set.** Logistic regression reached a test ROC AUC of 0.391 and gradient boosting 0.454. An AUC below 0.5 means the ranking is worse than random, which usually points to a pipeline error rather than weak signal.
- **Model F1 scores are below a trivial baseline.** With a 41.1% positive rate (329 of 800), always predicting "positive" yields an F1 of about 0.58. Logistic regression (0.122) and gradient boosting (0.316) both fall short of that.
- **The reported "drivers" should not be acted on.** group_g4 (coefficient −0.356) and feat_3 (top gradient-boosting importance) have no statistical support, and both models fit noise.
- **Decision for stakeholders: do not deploy a predictive model or make feature-based decisions yet.** The first step is an audit of the pipeline (outcome coding, group encoding, split integrity, and preprocessing leakage). The results in this report are provisional.

## Dataset Overview

| Attribute | Value |
|---|---|
| Source | `/workspaces/agents/evals/data/survey.csv` |
| Rows × columns | 800 × 7 |
| Target variable | `outcome` (binary: 0 / 1) |
| Numeric features | 5 (feat_1 to feat_5, float64) |
| Categorical feature | 1 (`group`, object) |
| Missing values | None reported in the available outputs |

**Target distribution:** 471 negatives (58.9%) and 329 positives (41.1%). This is moderately imbalanced, not severely.

**Group distribution:**

| Group | n | % of total |
|---|---|---|
| g1 | 182 | 22.8% |
| g2 | 206 | 25.8% |
| g3 | 200 | 25.0% |
| g4 | 212 | 26.5% |
| **Total** | **800** | **100%** |

**Note on schema:** The source documentation describes "6 numeric features" and "g1, g2, g3." The actual file contains 5 numeric features and 4 group levels (g1–g4). The counts above reflect the data as reported in the group-level outputs, which sum to 800. The schema description should be corrected.

## Analysis Methodology

### Strategic Approach

Three strategies were applied in priority order:

1. **Exploratory analysis first.** With 800 rows and a mix of numeric and categorical variables, the goal was to check distributions, scales, outliers, group frequencies, and inter-feature correlations before any modeling.
2. **Statistical testing second.** Univariate tests (Welch t-tests for numeric features against the outcome, chi-square for group against outcome, ANOVA or Kruskal-Wallis for feature differences across groups) were used to test whether any feature–outcome or group–outcome relationship exists before a model is fit.
3. **Predictive modeling last.** Logistic regression and gradient boosting were trained on a stratified train/test split, with feature importance assessed. Results were interpreted in light of the earlier findings.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory (EDA) | 2 |
| Statistical | 2 |
| Machine Learning | 2 |
| **Total** | **6 of 6 (100%)** |

Total execution time was 34.9 seconds. All tasks reported completion, but several task outputs were truncated or incomplete (see Limitations). "Completed" describes task execution, not the completeness of the reported results.

## Key Findings

### Exploratory Analysis

**Data quality**
- No missing values were reported. The missing-value output was truncated after feat_2 in one task, and feat_3 was reported with zero missing values in another. Full completeness across all seven columns is therefore inferred rather than confirmed for every column.
- Outlier counts were requested but not reported.

**Outcome distribution**
- Positive class: 329 of 800 (41.1%). Negative class: 471 (58.9%).
- This imbalance is moderate. It is large enough to affect F1 and accuracy interpretation, so these metrics must be read against the baseline (see Predictive Models).

**Group distribution**
- Group sizes are fairly balanced: g1 is the smallest at 22.8%, while g4 is the largest at 26.5%. The spread between the largest and smallest group is 3.7 percentage points, so no group dominates the sample.

**Feature distributions**
- Shapiro-Wilk minimum p-value for feat_1 across groups was 0.104, so normality was not rejected for feat_1 in any group. Levene's test for feat_1 gave p = 0.587, indicating no evidence of unequal variances across groups. Feat_1 therefore meets the assumptions for parametric tests.
- Distributions, means, standard deviations, and skewness for feat_2 through feat_5 were not reported.

**Correlations**
- The correlation matrix was requested but not reported. Inter-feature redundancy and multicollinearity are unknown.

### Statistical Evidence

**Feature-outcome tests (Welch t-tests, feat_1 to feat_5)**

| Purpose | Test statistic | p-value | Significance (α = 0.05) | Effect size |
|---|---|---|---|---|
| Does each numeric feature differ between outcome classes? | Not reported | ≥ 0.05 for all five features | Not significant | Not reported |

Only threshold statements were reported ("fail to reject, p ≥ 0.05"). The actual p-values, t-statistics, mean differences, and confidence intervals are not available.

**Group comparisons (ANOVA or Kruskal-Wallis, with post-hoc correction)**

| Purpose | Test | p-value | Significance | Effect size |
|---|---|---|---|---|
| Do numeric features differ across groups? (feat_1 to feat_5) | ANOVA / Kruskal-Wallis, adjusted | Adjusted p ≥ 0.05 for all five | Not significant | Not reported |

The correction method (e.g., Bonferroni, Holm, Benjamini-Hochberg) was not named. The Kruskal-Wallis results were referenced but not shown.

**Group–outcome association (chi-square)**

| Purpose | Test statistic | df | p-value | Effect size |
|---|---|---|---|---|
| Is outcome associated with group? | Not reported | Not reported | Reported as "fail to reject" | Not reported (Cramér's V not computed) |

The chi-square statistic, degrees of freedom, and p-value are missing. The "fail to reject" conclusion cannot be verified and should be treated as unconfirmed.

**Plain-English interpretation:** None of the tests found evidence that any numeric feature or any group is associated with the outcome at conventional thresholds. Because the reported results lack effect sizes and confidence intervals, we cannot say whether the absence of significance reflects a true null effect or insufficient power. With 800 observations, the study has reasonable power to detect moderate effects, but small effects could still be missed.

### Predictive Models

**Models tested**
1. Logistic regression (with group encoded and numeric features scaled)
2. Gradient boosting classifier

A random forest was requested in one task but was not trained.

**Performance on the held-out test set**

| Model | Test ROC AUC | Test F1 | Train ROC AUC (implied*) | Train–test AUC gap |
|---|---|---|---|---|
| Logistic regression | 0.391 | 0.122 | ≈ 0.586 | 0.195 |
| Gradient boosting | 0.454 | 0.316 | ≈ 0.967 | 0.513 |

*Implied train AUC = test AUC + reported gap. It was not reported directly.

**Metrics not reported:** accuracy, precision, recall, confusion matrices, and calibration. These were requested but are absent, so the performance picture is incomplete.

**Interpretation**
- **Discrimination:** Both AUCs are below 0.5. An AUC of 0.5 corresponds to random ranking, so both models rank cases worse than random. The most common cause is an inverted outcome encoding or misaligned predictions, which must be checked before any conclusion.
- **F1 in context:** The F1 for an always-positive classifier at this 41.1% base rate is about 0.58. Both models score below that, so neither improves on a trivial strategy. The gradient-boosting F1 (0.316) is higher than logistic regression's (0.122), but this reflects threshold choice, not better discrimination, since its AUC is lower.
- **Overfitting:** Gradient boosting shows a train–test AUC gap of 0.513 (implied training AUC ≈ 0.97), versus 0.195 for logistic regression. The model has memorized the training data without generalizing.

**Feature importance**

| Model | Top feature | Measure | Reported value | Reliability |
|---|---|---|---|---|
| Logistic regression | group_g4 | Coefficient | −0.356 | Low. Not supported by group tests; model fails the AUC check. |
| Gradient boosting | feat_3 | Impurity importance | Not reported | Low. Impurity importance favors continuous features and is unreliable for a model below chance. |

The negative coefficient for group_g4 suggests lower odds of the positive outcome relative to the reference group. However, this is uncorroborated and the reference category is unverified (see Limitations).

**Predictive insight:** Nothing can be predicted reliably from these features with the current pipeline. The importance rankings should be treated as artifacts of fitting noise.

## Synthesis

**Validated hypotheses**

| Hypothesis | Evidence | Status |
|---|---|---|
| Numeric features differ between outcome classes | Welch t-tests, all p ≥ 0.05 | Not supported |
| Outcome varies across groups | Chi-square, reported without statistics | Not supported (incomplete) |
| Numeric features differ across groups | ANOVA / Kruskal-Wallis, adjusted p ≥ 0.05 | Not supported |
| Features linearly predict outcome | Logistic regression, test AUC 0.391 | Not supported (sub-chance) |
| Features non-linearly predict outcome | Gradient boosting, test AUC 0.454 | Not supported (sub-chance) |

No hypothesis was confirmed.

**Consistent patterns**
- Univariate tests, group comparisons, and multivariate models all indicate no detectable signal. This consistency is meaningful. It suggests either that the features carry little outcome information or that the pipeline is masking any signal that exists.
- The sub-chance AUCs are the key anomaly. Random noise would typically produce AUCs near 0.5, not clearly below it, so this pattern points toward a systematic problem.

**Inconsistencies to resolve**
- **Group levels:** Group outputs show four levels (g1–g4), while some documentation references three (g1–g3).
- **Feature count:** The documentation references six numeric features, but the file contains five.
- **Robust predictors:** One task describes the features as "robust predictors." This conflicts with the sub-chance AUCs and should be disregarded.
- **Interaction claim:** One task suggests that disagreement between the two models indicates interaction effects. Both models failed, so this disagreement does not support an interaction hypothesis. No interaction terms were tested.

## Conclusions

**What we can say with confidence**
1. The dataset is clean on available checks: no missing values were reported, groups are balanced (22.8% to 26.5%), and the outcome is moderately imbalanced (41.1% positive).
2. feat_1 meets the normality and equal-variance assumptions for parametric testing across groups.
3. No feature, and no group, shows a statistically significant association with the outcome in the reported tests.
4. Neither the logistic regression nor the gradient-boosting model produces usable predictions. Both perform below chance on the test set and below a trivial baseline on F1.
5. The gradient-boosting model overfits severely, and the current model setup should not be used for prediction.

**What we cannot yet conclude**
- Whether any feature is a real driver of the outcome. The importance rankings are unvalidated.
- Whether group_g4 has a real association with the outcome.
- Whether the features have no predictive value. The sub-chance AUCs suggest the pipeline may be at fault, so the question remains open.
- The direction and size of any effects, since effect sizes and confidence intervals were not reported.

## Limitations & Caveats

**Data quality issues**
- Missing-value output was truncated in at least one task. Full completeness is not confirmed for all columns.
- Outlier analysis was requested but not reported.
- The schema documentation (6 numeric features, groups g1–g3) conflicts with the data (5 numeric features, groups g1–g4).

**Statistical assumptions and limitations**
- Normality and equal-variance checks were reported only for feat_1. The assumptions for feat_2 through feat_5 are unverified.
- The multiple-comparison correction method was not named.
- Effect sizes (Cohen's d, η², Cramér's V) and confidence intervals were not reported. Non-significance cannot be interpreted as absence of effect without them.
- Power was not assessed. Small effects could go undetected.

**Failed or incomplete analyses**
- Both models score below chance (AUC < 0.5). The most likely causes, which must be checked, are:
  - Outcome coding reversed or misaligned with predicted probabilities.
  - Preprocessing (scaling or encoding) fit on the full dataset before splitting, or row misalignment after the split.
  - Distribution shift between training and test partitions, or memorization of identifiers.
- The chi-square test was reported without its statistic, degrees of freedom, or p-value.
- Kruskal-Wallis results were referenced but not shown.
- Accuracy, precision, recall, and confusion matrices were requested but not reported.
- The random forest was requested but not trained.

**Missing information**
- Correlation matrix and multicollinearity diagnostics (VIF)
- Descriptive statistics (mean, SD, skewness) for feat_2 to feat_5
- Outlier counts
- Cross-validated performance (a single split at n = 800 is unstable)
- Regularization settings
- Reference category used for the group variable in the logistic regression

## Recommendations

### Immediate Actions

1. **Do not deploy or act on either model.** Both perform below chance and below a trivial baseline.
2. **Audit the modeling pipeline before any further analysis:**
   - Verify outcome encoding (confirm which class is coded 1 and that predicted probabilities correspond to that class).
   - Confirm group levels (g1–g4) and the reference category used in the model.
   - Verify that the train/test split is stratified and that no rows are misaligned.
   - Confirm that scalers and encoders are fit on training data only.
   - Fix a random seed and rerun to check reproducibility.
3. **Correct the data documentation:** 5 numeric features, 4 group levels, outcome prevalence 41.1%.
4. **Stop using the "robust predictors" and "driver" labels** for feat_3 and group_g4 until they are validated.

### Future Analysis

**Re-run the analyses with complete outputs:**
- Full descriptive statistics, outlier counts, and correlation matrix for all five numeric features.
- Test statistics, exact p-values, effect sizes, and 95% confidence intervals for every test.
- Chi-square group × outcome with statistic, df, p-value, and Cramér's V.
- Named multiple-comparison correction.

**Rebuild the predictive models:**
- Stratified k-fold cross-validation (e.g., 5 or 10 folds) to replace the single split.
- Regularized logistic regression, a random forest, and gradient boosting with early stopping and hyperparameter search.
- Report accuracy, precision, recall, F1, ROC AUC, PR AUC (more informative under imbalance), a confusion matrix, and calibration.
- Compare every model against the trivial baselines: majority-class accuracy (58.9%) and always-positive F1 (≈ 0.58).

**Validate feature importance:**
- Use permutation importance on a validated model, with confidence intervals.
- Test group × feature interactions to check whether effects differ across groups.

**Additional questions to investigate:**
- Is there any signal once the pipeline is correct?
- Do feature effects vary by group?
- Is the outcome associated with group after proper testing and effect-size reporting?

**Data that would help:**
- A data dictionary specifying feature definitions, units, the group variable's meaning, and the outcome definition.
- Confirmation of the survey instrument's sampling design (e.g., whether the groups are strata, clusters, or self-selected), since this affects valid inference.
- Additional candidate predictors, if the survey can capture them, since the current five numeric features show little signal.
- Timestamps or identifiers to verify the train/test split and detect leakage.