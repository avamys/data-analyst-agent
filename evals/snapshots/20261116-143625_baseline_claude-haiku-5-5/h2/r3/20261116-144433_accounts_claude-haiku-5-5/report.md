# Data Analysis Report: Accounts

## Executive Summary

- **Renewal is predictable from account attributes.** The best model (Random Forest) reached a test ROC-AUC of about 0.835 and accuracy of about 77%, versus a 57.5% majority-class baseline. That is roughly 19 percentage points above the naive approach.
- **Discount level is the strongest and most actionable signal.** Renewing accounts averaged 11.7% discount versus 19.4% for non-renewing accounts, a gap of 7.7 points (Welch t = -14.50, p = 1.1e-44, Cohen's d ≈ -0.73). The association is very strong, but the data cannot show whether discounts cause lower renewal or are targeted at accounts already at risk.
- **Region is not a reliable driver.** Renewal rates range only from 55.5% (east) to 60.2% (west), and a chi-square test finds no evidence of association (fail to reject independence). Region nonetheless appears among the top predictive features, so its role is unresolved.
- **Model choice is a judgment call.** Logistic Regression and Random Forest reached nearly identical accuracy (0.7656 to 0.7688). Random Forest has the higher AUC, but the Logistic Regression AUC is not reported, so the gap cannot yet be confirmed as material.
- **Decision readiness: moderate.** The discount relationship and the predictive signal are sound enough to support risk scoring and targeted outreach. They are not yet sufficient to change discount policy, which requires a controlled experiment.

## Dataset Overview

- **Source:** `/workspaces/agents/evals/data/accounts.csv`
- **Size:** 1,600 rows × 7 columns
- **Target variable:** `renewed` (binary; 1 = renewed, 0 = not renewed)
- **Features:**
  - Six numeric: `discount_pct`, `seats`, `support_tickets`, `contract_months`, `signup_month`, and the target-adjacent numeric fields listed above
  - One categorical: `region` (four levels: east, north, south, west)
- **Class balance:** 920 renewed (57.5%) and 680 not renewed (42.5%). This is moderately balanced and does not require resampling.
- **Data quality:** The missing-value check reported zero missing values for the columns it displayed. The remaining columns were truncated in the output, but no missing data was flagged for the dataset as a whole.

## Analysis Methodology

### Strategic Approach

Three analysis strategies were applied in priority order:

1. **Exploratory:** Examine distributions, outliers, correlations, and category balance before testing or modeling. This establishes data quality and reveals sparse levels that could destabilize later results.
2. **Statistical:** Test candidate relationships with `renewed` using a chi-square test (region) and Welch t-tests or point-biserial correlations (numeric features), with Holm correction across each family of four tests and α = 0.05.
3. **Predictive:** Train and compare classifiers (Logistic Regression and Random Forest) on a train/test split, then use permutation importance to check whether the statistically identified signals also carry predictive weight.

This order was chosen so that modeling would build on validated relationships, and so that predictive importances could be cross-checked against statistical evidence.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory (EDA) | 2 |
| Statistical | 2 |
| Machine Learning | 2 |
| **Total** | **6 of 6 (100%)** |

Total execution time was 32.9 seconds. No tasks failed. Several specialist outputs were truncated, so some results reported below are incomplete (see Limitations).

## Key Findings

### Exploratory Analysis

**Target distribution**
- 920 of 1,600 accounts renewed (57.5%); 680 did not (42.5%).
- A model that always predicts "renew" would be correct 57.5% of the time. This is the accuracy baseline for all models.

**Region distribution and renewal by region**

| Region | Accounts | Renewed | Not Renewed | Renewal Rate |
|---|---|---|---|---|
| East | 389 | 216 | 173 | 55.5% |
| North | 406 | 233 | 173 | 57.4% |
| South | 416 | 237 | 179 | 57.0% |
| West | 389 | 234 | 155 | 60.2% |
| **Total** | **1,600** | **920** | **680** | **57.5%** |

- All four regions are well populated (389 to 416 accounts each), so no region is sparse.
- The spread in renewal rates across regions is 4.6 percentage points (east to west), a modest difference.

**Other exploratory findings**
- Outlier analysis and pairwise correlation results were requested but were truncated in the output. Multicollinearity among numeric features (for example, seats and contract length) therefore remains unassessed.

### Statistical Evidence

**Test 1: Chi-square test of independence (region vs. renewed)**
- **Purpose:** Determine whether renewal rates differ across regions.
- **Result:** Fail to reject the null hypothesis of independence. The reported test statistic and p-value were truncated.
- **Verification:** Recomputing the chi-square statistic from the observed counts above gives χ² ≈ 1.79 with 3 degrees of freedom, p ≈ 0.62, and Cramér's V ≈ 0.03. These values are our recalculation, not specialist output, but they agree with the reported conclusion.
- **Plain English:** Region does not meaningfully change the chance of renewal. The regional differences seen in the table are consistent with random variation.

**Test 2: Welch's t-test (discount_pct by renewed)**
- **Purpose:** Determine whether average discount differs between renewing and non-renewing accounts.
- **Result:**

| Group | n | Mean discount_pct |
|---|---|---|
| Renewed = 1 | 920 | 11.74% |
| Renewed = 0 | 680 | 19.41% |
| **Difference** | | **−7.67 points** |

- **Test statistic:** t = −14.50
- **P-value:** 1.08 × 10⁻⁴⁴. This remains far below α = 0.05 even after Holm correction across the four-test family.
- **Effect size:** Cohen's d ≈ −0.73, derived from the t statistic and group sizes (pooled standard deviation was not reported). This is a large effect by conventional standards.
- **Plain English:** Accounts that renewed received, on average, discounts about 40% smaller than accounts that did not renew. This is the strongest and most reliable statistical relationship in the analysis.

**Tests 3 to 5: seats, support_tickets, contract_months**
- Welch t-tests or point-biserial correlations were run for these features, but their statistics, p-values, and effect sizes were truncated. **These relationships are unverified at the statistical level.** They are supported only by their appearance in the predictive importance rankings (seats and support_tickets), and contract_months does not appear there at all.

**Multiple-comparison control**
- Holm correction was applied within the four-test family. Conclusions about discount_pct are unaffected by this correction.

### Predictive Models

**Models tested:** Logistic Regression and Random Forest, trained on a single stratified train/test split.

**Performance**

| Metric | Result | Interpretation |
|---|---|---|
| Test accuracy | 0.7656 to 0.7688 | About 19 points above the 57.5% baseline |
| ROC-AUC (Random Forest) | ≈ 0.835 (reported as 0.8352 and 0.8355) | Good discrimination between renewers and non-renewers |
| ROC-AUC (Logistic Regression) | Not reported | Cannot quantify the model gap |
| Precision, recall, F1 | Not reported | Cannot assess error trade-offs |
| Train-test gap | Not reported | Overfitting risk cannot be quantified |

- Accuracy is effectively tied between models. The 0.003 difference is well within the noise of a single split.
- The two AUC values for Random Forest differ slightly (0.8352 vs. 0.8355), most likely from rounding or run-to-run variation.

**Feature importance (permutation, consensus across both models)**
1. `discount_pct`: strongest and most actionable. Consistent with the t-test.
2. `seats`
3. `support_tickets`
4. `region`: a top predictor despite the null chi-square result (see Synthesis)

`contract_months` did not appear in the consensus importance list. Its absence is unexplained.

**Predictive insights**
- The features collectively carry real signal. Discount level stands out in both the statistical and predictive analyses.
- Permutation importance shows relevance but not direction. The per-feature coefficient signs were not reported, so we cannot say whether more seats or more support tickets increase renewal.

## Synthesis

**Validated across methods**
- **Discount level is associated with non-renewal.** The t-test establishes a large, highly significant group difference (7.7 points, d ≈ −0.73), and discount_pct ranks as the top predictive feature in both models. This is the most robust finding in the analysis.
- **The features carry predictive signal.** Random Forest's AUC of about 0.835 is well above chance, and it is consistent across the reported outputs.
- **Seats and support tickets have predictive relevance.** They appear in both models' consensus importances, but their statistical tests were not reported, so effect size and direction are unconfirmed.

**Conflicting or unresolved signals**
- **Region:** The chi-square test shows no marginal association with renewal, yet region ranks among the consensus predictive features. The most plausible explanations are:
  - *An interaction effect:* Region matters only in combination with other features (for example, discount or seats).
  - *An encoding or model artifact:* One-hot encoding of a four-level variable can inflate permutation importance, particularly if the model splits on it in combination with correlated features.
  
  Either way, region should not be treated as a standalone driver.
- **Contract length:** It was tested statistically but dropped out of the predictive importance ranking. This could mean a true null effect, or that its signal is absorbed by correlated features such as seats. It is unresolved.

**Patterns with business meaning**
- Accounts with lower discounts are more likely to renew. Because discounts are a business lever, this pattern requires careful interpretation (see Conclusions).
- Renewal rates are fairly uniform across regions, which suggests that regional retention strategies may not be a priority based on these data.

## Conclusions

**What we can say with confidence**
1. Renewal is meaningfully predictable from the available account attributes. The best model achieves about 77% accuracy and AUC ≈ 0.835, compared with a 57.5% baseline.
2. Accounts that renewed had substantially lower average discounts (11.7% vs. 19.4%). This difference is large and statistically robust.
3. Region does not have a meaningful marginal association with renewal (renewal rates 55.5% to 60.2%, no significant chi-square result).

**What we cannot yet say**
- Whether discounts cause lower renewal, or whether they are offered preferentially to at-risk accounts. The observed direction is consistent with either explanation.
- The direction and size of effects for seats, support tickets, and contract length.
- Whether Random Forest's AUC advantage over Logistic Regression is real or within noise.
- Model performance at any specific decision threshold (precision and recall were not reported).

## Limitations & Caveats

**Data quality**
- Several specialist outputs were truncated, including chi-square statistics, the seats, support_tickets, and contract_months test results, outlier analysis, pairwise correlations, and the region cross-tabulation's expected counts.
- The missing-value output was also cut off after the first two columns.

**Statistical assumptions**
- The chi-square test assumes expected cell counts of at least 5. With 389 to 416 accounts per region and roughly 40% or more in each renewal cell, this assumption is almost certainly met, but it was not explicitly verified.
- Welch's t-test is robust to unequal variances but assumes reasonably well-behaved distributions. Outliers in discount_pct were not reported.
- Cohen's d was derived from the t statistic rather than computed from the pooled standard deviation. It is an approximation.

**Modeling limitations**
- A single train/test split was apparently used. Without cross-validation, the variance of the accuracy and AUC estimates is unknown.
- Whether `signup_month` was included as a feature is not stated. If it was used in a random split, cohort effects may have leaked between train and test sets.
- Permutation importance can be misleading when features are correlated.
- No calibration analysis or threshold tuning was reported.

**Interpretation limits**
- All findings are associational. The discount relationship may reflect selection (discounts given to at-risk accounts) rather than a causal effect.

**Failed analyses**
- No tasks failed. Several outputs were incomplete, as noted above.

**Missing information**
- Chi-square statistic and p-value (reported only as a conclusion)
- Test results for seats, support_tickets, and contract_months
- Logistic Regression ROC-AUC
- Precision, recall, F1, and confusion matrices
- Per-feature coefficient signs and odds ratios
- Train-test gap and cross-validated estimates

## Recommendations

### Immediate Actions

1. **Do not change discount policy on the basis of these data alone.** The discount–renewal association is strong, but without evidence of causality, reducing discounts could harm retention if discounts are currently being used to save at-risk accounts.
2. **Deploy a risk-scoring model for prioritization.** The model's ~77% accuracy and AUC ≈ 0.835 are sufficient to rank accounts by renewal risk for outreach, provided that the outputs are used to prioritize human review rather than to make automated decisions.
3. **Use Logistic Regression as the default for explanation and deployment** unless cross-validation shows that Random Forest's AUC advantage is stable. Logistic Regression coefficients are easier to explain to stakeholders and audit.
4. **Do not use region as a standalone targeting criterion.** Regional renewal differences are small and not statistically significant.
5. **Report the missing metrics before any go-live decision.** Precision, recall, and the confusion matrix are required to choose a threshold that balances unnecessary retention offers against missed at-risk accounts.

### Future Analysis

**Priority analyses**
1. **Controlled discount experiment:** Randomly assign discount levels, or hold out a random subset from discount changes, to estimate the causal effect of discounts on renewal. This is the most important next step for any discount policy decision.
2. **Logistic regression coefficients and odds ratios** with confidence intervals for discount, seats, support_tickets, and contract_months, to establish direction and magnitude.
3. **Cross-validated model comparison** (repeated stratified k-fold) to test whether the Random Forest AUC advantage is stable.
4. **Interaction tests**, particularly region × discount and region × seats, to explain why region predicts conditionally but not marginally.
5. **Multicollinearity check** (variance inflation factors) for seats and contract_months.
6. **Cohort analysis of `signup_month`** using a time-based train/test split, to check for temporal drift.
7. **Threshold and cost analysis** to select an operating point based on the relative cost of a false retention offer versus a missed at-risk account.

**Data that would strengthen future analysis**
- **Discount history and rationale:** When and why discounts were offered, to separate policy effects from targeting.
- **Churn reasons or cancellation notes**, to validate the risk signal.
- **Account revenue or lifetime value**, to convert model performance into expected financial impact.
- **Usage and engagement metrics** (logins, feature adoption, and recent support contact) to capture behavior beyond static account attributes.
- **Region definitions with account counts at finer granularity**, to test whether the regional signal is an artifact of coarse grouping.
- **A larger sample or repeated observations per account over time**, to support time-aware modeling and more precise estimates of small effects.