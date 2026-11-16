# Data Analysis Report: Visits

## Executive Summary

- **Customer tier and visit quarter are both significantly associated with repeat visits.** Chi-square tests for each returned p < 0.0001. Tier is the most consistent signal, ranking at the top in both predictive models.
- **A Logistic Regression model predicts repeat visits well on held-out data.** It achieved ROC-AUC 0.922, F1 0.846, and accuracy 87.0%. The majority-class baseline is 57.0% (the 43.0% repeat rate means always predicting "no repeat" is right 57.0% of the time), so the model adds about 30 percentage points of accuracy over that baseline.
- **Numeric features add less than categorical ones.** Only two of the five numeric group comparisons were significant at p < 0.05, and the feature names for these results are missing from the output.
- **Decision readiness: moderate.** The model can support ranking or segmenting customers by repeat-visit likelihood. It should not yet support causal claims about tier, quarter-specific interventions, or a deployment decision threshold until the tier direction, precision/recall, and effect sizes are confirmed.

## Dataset Overview

- **Source:** `/workspaces/agents/evals/data/visits.csv`
- **Size:** 2,000 rows × 6 columns, with no missing values in any column
- **Target:** `repeat_visit` (binary). Class counts are 1,141 non-repeat (57.05%) and 859 repeat (42.95%). This is a moderate imbalance, not a severe one.
- **Features:**
  - Numeric: `age`, `distance_km`, `staff_on_shift`
  - Integer-coded categorical: `quarter` (treated as categorical; it reaches at least level 7, so it is not a standard calendar quarter)
  - Categorical: `tier` (gold, silver, bronze observed)
- **Sample records:** Row 1 is quarter 6, gold tier, age 56, distance 12.0 km, staff on shift 12, repeat visit = 1. Row 2 is quarter 1, bronze tier, age 39, distance 9.1 km, staff on shift 3, repeat visit = 0.

## Analysis Methodology

### Strategic Approach

Analysis followed a sequence of exploratory, statistical, and predictive steps:

1. **Exploratory analysis** came first to check distributions, outliers, and the categorical distributions of tier and quarter before any modeling.
2. **Statistical testing** came second to confirm which features relate to `repeat_visit` before choosing model inputs. It used chi-square tests for categorical features and group comparisons for numeric ones.
3. **Predictive modeling** came last, using a train/test split with Logistic Regression and a tree ensemble. The earlier steps informed feature selection.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory (EDA) | 2 |
| Statistical | 2 |
| Machine Learning | 2 |
| **Total** | **6 of 6 (100% success, 0 failed)** |

Total execution time was 72.7 seconds. Note that the detailed ML task output was not included in the findings supplied for this report. Predictive results below are taken from the synthesized summary and should be verified against the raw model logs.

## Key Findings

### Exploratory Analysis

- **Target balance:** 859 of 2,000 customers (42.95%) made a repeat visit. The majority class is 57.05%.
- **Data completeness:** No missing values were detected across the six columns.
- **Outliers:** Both EDA tasks found no IQR outliers in the numeric features. Extreme values are unlikely to distort the models or the group comparisons.
- **Distributions by category:** The tier and quarter frequency tables were not included in the output, so category sizes and their repeat rates cannot be reported.
- **Numeric summaries:** Means, standard deviations, and ranges for `age`, `distance_km`, and `staff_on_shift` were not included in the supplied output, so they cannot be cited here.

### Statistical Evidence

**1. Chi-square test of independence: tier vs. repeat_visit**
- **Purpose:** Test whether repeat-visit rates differ across customer tiers.
- **Result:** p < 0.0001 (reported as 0.0000). **Significant.**
- **Effect size:** Not reported. Cramér's V can be computed once the contingency table is available.
- **Interpretation:** Repeat-visit behavior is not independent of tier. The contingency counts are missing from the output, so the direction and size of the difference are unknown.

**2. Chi-square test of independence: quarter vs. repeat_visit**
- **Purpose:** Test whether repeat-visit rates vary across quarter codes.
- **Result:** p < 0.0001. **Significant.**
- **Effect size:** Not reported.
- **Interpretation:** Repeat visits vary by quarter code. Because the codes go up to at least 7, the meaning of "quarter" needs confirmation (see Limitations).

**3. Group comparisons: numeric features vs. repeat_visit (t-tests / point-biserial correlation)**
- **Purpose:** Test whether numeric features differ between repeat and non-repeat customers.
- **Result:** Two results were significant at p < 0.05, and three were not (p ≥ 0.05).
- **Effect size:** Not reported.
- **Interpretation:** Only some numeric features relate to repeat visits. The feature names are missing from the output. There are only four numeric predictors (`age`, `distance_km`, `staff_on_shift`, and `quarter` if treated as numeric), yet five test results were reported. This mismatch needs to be resolved before any feature is named as significant.

**Summary of hypothesis results**

| Hypothesis | Test | Result | Status |
|---|---|---|---|
| Tier is associated with repeat visits | Chi-square | p < 0.0001 | Supported |
| Quarter is associated with repeat visits | Chi-square | p < 0.0001 | Supported |
| Some numeric features differ by repeat status | t-test / point-biserial | p < 0.05 (2 results) | Supported (features unnamed) |
| Other numeric features show no difference | t-test / point-biserial | p ≥ 0.05 (3 results) | Not rejected (features unnamed) |
| Numeric features contain outliers | IQR rule | None found | No outliers |

### Predictive Models

**Models tested:** Logistic Regression and a tree ensemble (Random Forest). The Logistic Regression was selected as the best model on the held-out test set.

| Metric | Logistic Regression | Tree Ensemble |
|---|---|---|
| ROC-AUC | 0.9218 | Not reported |
| F1 | 0.8462 | Not reported |
| Accuracy | 87.00% | Not reported |
| Precision | Not reported | Not reported |
| Recall | Not reported | Not reported |

**Baseline comparison:** A majority-class classifier scores 57.05% accuracy. The Logistic Regression's 87.00% is about 30 percentage points above that. ROC-AUC of 0.92 indicates strong ranking ability, well above the 0.5 expected from chance.

**Feature importances:**
- **Random Forest:** Tier (gold, bronze, silver) dominates.
- **Logistic Regression:** Tier (gold, bronze) and quarter 7 have the largest coefficients. Coefficient signs and magnitudes were not reported, so the direction of each effect is unknown.
- **Weak candidates:** Non-significant numeric features, including `age` (see Limitations for why this is unconfirmed).

**Predictive insights:**
- Categorical features (tier and quarter) carry most of the predictive signal.
- The tree ensemble's test metrics are missing, and its training output flagged possible overfitting. It cannot yet be compared fairly with the Logistic Regression.
- The model uses a single train/test split, so the reported metrics have no uncertainty estimate.

## Synthesis

**Consistent across methods:**
- **Tier is the most robust signal.** It is significant in the chi-square test and ranks at the top in both models. Two independent analyses agree.
- **Quarter matters, but its effect is specific to certain levels.** It is significant in the chi-square test and appears through quarter 7 in the Logistic Regression. The other quarter levels are not reported.
- **Categorical features outweigh numeric ones.** Numeric features show weaker group differences, and the model results point the same way.

**Conflicts and open questions:**
- **Secondary drivers differ by model.** The Random Forest emphasizes silver tier, while the Logistic Regression emphasizes quarter 7. Possible explanations include different importance methods (impurity versus coefficients) and the tree model capturing interactions that the linear model cannot.
- **Interactions have not been tested.** Whether tier effects vary by quarter is unknown.

## Conclusions

**What we can say with confidence:**
1. Tier and quarter are both significantly associated with repeat visits (p < 0.0001 each).
2. A Logistic Regression model using these features ranks customers well (ROC-AUC 0.92) and beats the majority-class baseline by about 30 percentage points of accuracy.
3. Numeric features are weaker predictors, and not all of them are significant.
4. The data contains no missing values and no IQR outliers, so the results are not driven by data errors.

**What we cannot yet say:**
- Which direction tier pushes repeat visits (gold versus bronze, for example)
- Which quarters drive repeat visits, or whether this reflects seasonality or a data artifact
- How large any effect is in practical terms
- Whether the tree ensemble outperforms the linear model
- Whether the model holds up over time or across different customer groups

## Limitations & Caveats

**Data quality and definitions**
- **Quarter coding is unclear.** Quarter is stored as an integer and reaches at least level 7. Standard calendar quarters run 1 to 4, so this may be a different coding scheme (for example, a period index or a mislabeled field). The meaning must be confirmed before quarter effects are interpreted.
- **Feature count mismatch.** The numeric group comparisons report five results, but only four numeric predictors exist. The feature names are missing, so it is unclear which features were significant.
- **Class balance was reported as unconfirmed in the synthesis, but it is available.** The counts are 1,141 and 859, a 57/43 split. This is moderate imbalance, and accuracy should be read against the 57.05% baseline.

**Statistical assumptions**
- **Expected cell counts for chi-square tests are not verified.** Quarter has several levels, and some tier-by-outcome or quarter-by-outcome cells may be sparse. Expected counts should be ≥5. Fisher's exact test or collapsed categories may be needed otherwise.
- **Effect sizes are missing.** With n = 2,000, very small effects can reach p < 0.0001, so statistical significance does not confirm practical importance.
- **Multiple comparisons are uncorrected.** The tier and quarter p-values are far below any reasonable threshold, so the conclusions are unlikely to change. The borderline numeric results (near p = 0.05) could be affected.
- **Independence of observations is unverified.** If customers appear more than once, the significance tests are inflated and the train/test split may leak information.
- **Tier may be a consequence rather than a cause.** If tier is assigned based on past behavior, the model is partly predicting its own inputs.

**Modeling limitations**
- Precision, recall, and the confusion matrix are missing, so the error types are unknown.
- A single train/test split gives no confidence interval for ROC-AUC or F1.
- The tree ensemble's test metrics are missing, and overfitting was flagged, so the model comparison is incomplete.
- Predicted probabilities have not been checked for calibration.
- The ML output that supports the model results was not included in the detailed findings for this report.

**Unverified claims**
- The synthesis states that age has near-zero correlation with the target. The correlation output was not included, so this is unverified.
- The synthesis suggests dropping weak features based on permutation importance. Permutation importance was not reported, so this recommendation is untested.

**Failed analyses:** None. All six tasks completed. Several outputs are truncated (for example, "a notable cell)"), so some detail was lost.

## Recommendations

### Immediate Actions

1. **Use the model for ranking and segmentation, not yet for hard decisions.** The ROC-AUC of 0.92 supports prioritizing customers by predicted repeat-visit likelihood. Set decision thresholds only after reviewing precision and recall for the business's cost of false positives versus false negatives.
2. **Report tier-level repeat rates to stakeholders.** Tier is the strongest and most consistent signal. Publishing observed repeat rates by tier (from the existing contingency table) gives an immediately usable view without relying on model internals.
3. **Confirm the meaning of the quarter field before acting on quarter effects.** Do not plan quarter-specific campaigns until the coding is verified.
4. **Do not treat numeric features as drivers yet.** Confirm which two numeric features are significant before using them in decisions.
5. **Verify the tree ensemble and Logistic Regression results.** Retrieve the full metric table and the raw ML logs to confirm that the reported numbers match the saved models.

### Future Analysis

**Analyses to run**
- Report the full contingency tables and observed repeat rates for tier and quarter, with Cramér's V for each chi-square test.
- Compute effect sizes (Cohen's d or point-biserial r) for each numeric group comparison, and name each feature.
- Report Logistic Regression coefficients with signs, magnitudes, and confidence intervals, to establish the direction of the tier effects.
- Report precision, recall, and the confusion matrix at the chosen threshold.
- Use k-fold cross-validation or repeated splits to estimate performance variance and a confidence interval for ROC-AUC.
- Test tier × quarter interactions.
- Check expected cell counts for each chi-square test and apply Fisher's exact test where needed.
- Run permutation importance before removing any feature.
- Check probability calibration.

**Validation**
- Use a temporal split (train on earlier periods, test on later ones) to test whether quarter and tier effects generalize.
- Confirm whether customers appear more than once, and if so, split by customer rather than by row.

**Data to collect**
- A data dictionary defining `quarter`, `tier`, and `distance_km` units, and explaining how tier is assigned.
- Timestamps for each visit, so seasonality and time trends can be modeled directly.
- Customer identifiers, so repeat behavior can be tracked and leakage can be ruled out.
- Outcome definitions: the time window used to define a "repeat visit."
- Business cost estimates for false positives and false negatives, to set the decision threshold.