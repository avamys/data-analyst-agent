# Data Analysis Report: Customer Churn

## Executive Summary

- **Churn affects nearly one in three customers.** Of 800 customers, 250 (31.25%) churned. A model that predicted "retained" for everyone would be 68.75% accurate, so accuracy is not a useful measure of performance here.
- **Contract type is the one confirmed churn driver.** Month-to-month customers churn at 37.3% (186 of 498), compared with 21.2% (64 of 302) for annual contracts. The association is statistically significant (χ² ≈ 22.8, df = 1, p < 0.001), and monthly customers have about 2.2 times the odds of churning (95% CI 1.6–3.1).
- **Monthly fee is the leading predictive feature, but its effect is not yet verified.** It has the highest random forest importance (0.70), but the formal test comparing fees between churned and retained customers did not come through in the analysis output.
- **Current models offer only modest predictive power.** The best model (logistic regression, ROC-AUC 0.714) can rank customers by churn risk. At its recall-oriented setting, roughly half of flagged customers would be true churners, so retention outreach would include many false positives.
- **Region does not predict churn.** The chi-square test found no significant association, so region should not drive retention targeting.

**Decisions supported now:** Prioritize month-to-month customers for retention review, and use the model as a risk-ranking aid in a controlled pilot with a holdout group. **Decisions to defer:** Final threshold selection, cost-benefit commitments, and any claim that support calls or monthly fee cause churn until the missing results are recovered.

---

## Dataset Overview

| Attribute | Detail |
|---|---|
| Source | `/workspaces/agents/evals/data/customers.csv` |
| Records | 800 customers |
| Columns | 5 (2 numeric, 3 categorical, including the target) |
| Numeric features | `monthly_fee` (float), `support_calls` (integer) |
| Categorical features | `contract`, `region` |
| Target | `churned_flag` (`yes` = churned, `no` = retained) |
| Class balance | 250 churned (31.25%), 550 retained (68.75%) |
| Missing values | None in the four predictor columns checked |

The target is stored as text (`yes`/`no`) and was recoded to 1/0 for modeling. The target was excluded from the predictors.

---

## Analysis Methodology

### Strategic Approach

The analysis followed three stages, in order:

1. **Exploratory analysis** to check data quality, the churn rate and class imbalance, and category frequencies before any modeling.
2. **Statistical testing** to identify which features are associated with churn and to guide feature selection. Chi-square tests were used for categorical features. Welch t-tests or Mann-Whitney U tests were planned for the numeric features, depending on distributional checks.
3. **Predictive modeling** to estimate how well churn can be predicted. The plan used stratified splits, class weighting, and metrics suited to imbalanced data (ROC-AUC, precision, recall, F1) rather than accuracy.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory (EDA) | 2 |
| Statistical | 2 |
| Machine Learning | 2 |
| **Total** | **6 of 6 (100% success rate)** |

The plan estimated about 12 tasks (3–4 exploratory, 3–4 statistical, 4–5 predictive). Six tasks were executed, so coverage is about half of what was planned. Total execution time was 40.1 seconds. Several task outputs were truncated, which limits the findings below.

---

## Key Findings

### Exploratory Analysis

**Target distribution.** Churn is moderately imbalanced: 250 churned and 550 retained, a 31.25% churn rate. This justifies stratified splitting and rules out accuracy as the main metric.

**Data quality.** The four predictor columns had zero missing values. The check did not report on `churned_flag`, so its completeness is confirmed only by the row counts in the churn tabulation (250 + 550 = 800).

**Contract distribution and churn by contract:**

| Contract | Customers | Churned | Retained | Churn Rate |
|---|---|---|---|---|
| Annual | 302 | 64 | 238 | **21.2%** |
| Monthly | 498 | 186 | 312 | **37.3%** |
| **Total** | **800** | **250** | **550** | **31.25%** |

Monthly contracts make up 62% of the customer base and account for 74% of all churners (186 of 250). Monthly customers churn at about 1.8 times the rate of annual customers.

**Not reported:** Summary statistics (mean, median, spread, outliers) for `monthly_fee` and `support_calls`, and category counts for `region`. The distribution of `support_calls` and `monthly_fee` therefore cannot be described here.

### Statistical Evidence

**Test 1: Chi-square test of independence, contract vs. churn**

- **Purpose:** Test whether churn status depends on contract type.
- **Hypotheses:** H0: churn and contract are independent. H1: they are associated.
- **Result:** Reject H0 at α = 0.05.
- **Test statistic and p-value:** The specialist reported the rejection but did not print the statistic. Recomputing from the reported contingency table gives **χ² ≈ 22.8, df = 1, p ≈ 2×10⁻⁶** (p < 0.001). With Yates' continuity correction, χ² ≈ 22.1, which gives the same conclusion.
- **Effect size (derived from the reported table):** φ = Cramér's V ≈ **0.17**. This is a small-to-moderate association. It is statistically strong, but the effect explains only a small share of the variation in churn.
- **Odds ratio (derived):** The odds of churn for monthly contracts are **2.2 times** those for annual contracts (95% CI 1.6–3.1).
- **Plain-English interpretation:** Contract type is linked to churn in a way that is very unlikely to be chance. Month-to-month customers churn more often. Contract type alone does not explain most churn, however.

**Test 2: Chi-square test of independence, region vs. churn**

- **Result:** Fail to reject H0 at α = 0.05.
- **Test statistic, p-value, and effect size:** Not reported in the available output.
- **Plain-English interpretation:** There is no evidence that churn differs by region. Region is not a useful targeting variable on this evidence.

**Test 3: Numeric features vs. churn (`monthly_fee`, `support_calls`)**

- **Purpose:** Compare churned and retained customers on each numeric feature using a Welch t-test or Mann-Whitney U test, chosen after distributional checks.
- **Result:** Not available. The output was truncated before the test statistics, p-values, and direction of effect were reported.
- **Implication:** The relationships of `monthly_fee` and `support_calls` with churn are **unverified** at the hypothesis-test level. Conclusions about them rely on model results only.

### Predictive Models

**Setup:** The target was `churned_flag` (1 = churned). Predictors were `monthly_fee` and `support_calls` (scaled), and `contract` and `region` (one-hot encoded). Models were evaluated on a held-out test set.

**Models tested:** Logistic regression (LR) and random forest (RF), each unweighted and class-balanced.

**Test-set performance:**

| Model | Class Weighting | ROC-AUC | Recall | F1 | Implied Precision* |
|---|---|---|---|---|---|
| Logistic regression | None | **0.714** (best) | Not reported | Not reported | Not reported |
| Logistic regression | Balanced | 0.713 | **0.700** | **0.603** | ≈ 0.53 |
| Random forest | None | 0.685 | Not reported | Not reported | Not reported |
| Random forest | Balanced | 0.686 | 0.600 | 0.540 | ≈ 0.49 |

*Derived from the reported F1 and recall using F1 = 2PR / (P + R).

**Interpretation:**

- **Discrimination:** An ROC-AUC of 0.71 means that, given one churner and one retained customer chosen at random, the model ranks the churner higher about 71% of the time. This is useful but modest. Random guessing scores 0.50.
- **Class weighting:** Balancing did not change ROC-AUC meaningfully (LR 0.714 → 0.713; RF 0.685 → 0.686). It did shift the operating point toward catching more churners. The balanced LR reaches 70% recall, but without the unweighted recall it is not possible to quantify the trade-off precisely.
- **Precision trade-off:** At these settings, about half of flagged customers would be true churners. A retention campaign would therefore reach many customers who would have stayed.
- **Model choice:** Logistic regression is preferred on ROC-AUC. The advantage over the random forest (0.714 vs. 0.685) is modest, and no confidence intervals were reported, so it may not be statistically meaningful at this sample size.

**Feature importance:**

| Feature | Importance (RF) | Direction | Notes |
|---|---|---|---|
| `monthly_fee` | **0.705** | Not reported | Largest contributor by a wide margin |
| `contract` | Not reported | Monthly → higher churn (from Test 1) | Confirmed by the chi-square test |
| `support_calls` | Not reported | Not reported | Included in the models; effect unknown |
| `region` | Not reported | None detected | Not associated with churn |

The importance of `monthly_fee` (0.70) suggests it carries most of the predictive information the random forest uses. Because importance measures predictive contribution rather than causal effect, and the direction of the effect is unknown, this result should be read as a signal worth verifying, not a finding about price sensitivity.

---

## Synthesis

**Validated relationships:**

- **Contract type and churn** are associated (χ² ≈ 22.8, p < 0.001). This is the only formally tested, confirmed relationship.

**Consistent patterns across analyses:**

- **Billing structure looks central.** Contract type is significantly associated with churn, and monthly fee is the top model feature. Both point toward billing structure and price as the main levers, though the two have not been tested together.
- **Region is a non-factor.** It is not associated with churn, and no model result suggests otherwise.
- **Linear models are at least as good as tree models.** Logistic regression outperforms the random forest, which suggests the relationships are largely additive. The random forest may be overfitting.

**Unresolved:**

- The direction and significance of `monthly_fee` and `support_calls` effects.
- Whether high fees matter specifically for month-to-month customers (an interaction effect, not yet tested).

---

## Conclusions

**What we can say with confidence:**

1. Churn is 31.25% in this sample, with 250 churners among 800 customers.
2. Month-to-month customers churn at 37.3% versus 21.2% for annual customers. The difference is statistically significant and practically meaningful (odds ratio ≈ 2.2).
3. Region is not associated with churn.
4. The best available model ranks customers by churn risk better than chance (ROC-AUC 0.71), but its predictions are imprecise.

**What we can say with moderate confidence:**

5. Monthly fee is the strongest predictor among the features tested, based on random forest importance. Its direction and statistical significance are not yet confirmed.
6. Important churn drivers appear to be missing from the dataset. An AUC near 0.71 suggests that factors such as tenure, usage, satisfaction, or payment history may matter.

**What we cannot yet say:**

- Whether support calls increase or decrease churn risk.
- Whether the random forest has useful nonlinear structure or is simply overfitting.
- The expected business value of any retention campaign, since no decision threshold has been tied to costs.
- Whether any of these relationships are causal.

---

## Limitations & Caveats

**Data quality and coverage**

- No missing values were found in the predictor columns, but the check did not cover `churned_flag`.
- The output for the numeric-feature distributions and the region category counts was not available, so the data's distributional characteristics are only partly documented.

**Statistical assumptions and limitations**

- The choice between a Welch t-test and a Mann-Whitney U test depended on distributional checks that were not reported, so the test selection cannot be verified.
- Chi-square tests assume adequate expected cell counts (commonly at least 5). The contract table meets this easily. The region table was not checked, and this matters if region has many sparse categories.
- No correction for multiple comparisons was applied. With only a few tests, the impact is small, but it should be noted.
- All results are associational. Nothing here shows that monthly fee or contract type causes churn.

**Modeling limitations**

- **Overfitting:** A train/test accuracy gap of 25.31% was reported, but the model it applies to is not stated. If it applies to the random forest, its test results are likely optimistic. Treat all test metrics as provisional until this is resolved.
- **Small test set:** With a 20% holdout, about 50 churners fall in the test set (not ~40, as estimated in the synthesis). Metric estimates for ROC-AUC, recall, and F1 are therefore noisy, and no confidence intervals were reported.
- **No cross-validation results** were reported, although folds were requested.
- **Missing metrics:** Recall and F1 for the unweighted models, confusion matrices, and PR-AUC were not reported. PR-AUC is the more informative metric for an imbalanced target and should be added.
- **Model selection ambiguity:** Logistic regression (unweighted) is preferred for ranking, but the reported recall and F1 values come from the balanced version. A single operating model needs to be chosen explicitly.

**Failed or incomplete analyses**

- Numeric-feature hypothesis tests (monthly fee and support calls vs. churn): output truncated.
- Chi-square statistic and effect size for region: not reported.
- Cramér's V for contract: not reported (the value in this report is derived from the reported table).
- Full feature importances and coefficient signs: not reported.
- Interaction tests (for example, contract × monthly fee): not performed.
- Only 6 of approximately 12 planned tasks were executed.

---

## Recommendations

### Immediate Actions

1. **Target month-to-month customers in retention efforts.** This segment accounts for 74% of churners and churns at 37%. Prioritize it for outreach or for contract-conversion offers, such as incentives to move to annual terms. Pilot this with a holdout group so the effect can be measured.

2. **Use the logistic regression model as a risk-ranking tool, not a final decision rule.** It can rank customers by churn risk, but roughly half of flagged customers would not churn. Before any campaign, set the decision threshold by comparing outreach costs with the revenue lost to churn.

3. **Deprioritize region** as a targeting variable on current evidence.

4. **Do not finalize business recommendations on monthly fee or support calls yet.** Recover the truncated outputs first, specifically the stat_2 results, the coefficient signs, and the full feature importances.

5. **Resolve the overfitting question** by reporting train and test metrics for each model separately, and confirm which model the 25.31% gap applies to.

### Future Analysis

**Priority analyses:**

- Recover and report the Welch t-test or Mann-Whitney U results for `monthly_fee` and `support_calls`, with effect sizes and direction.
- Report the chi-square statistic and Cramér's V for region, along with the churn rate by region and expected cell counts.
- Run stratified k-fold cross-validation and report mean and spread of ROC-AUC, PR-AUC, precision, recall, and F1. Include confidence intervals.
- Test the monthly fee × contract interaction to see whether high fees drive churn specifically in month-to-month contracts.
- Tune or regularize the random forest (depth limits, minimum leaf size) to check whether it can match or beat logistic regression once overfitting is controlled.
- Choose a decision threshold based on expected value, using explicit retention-offer costs and customer lifetime value.

**Data to collect:**

- **Tenure** (months as a customer): often one of the strongest churn predictors.
- **Usage or engagement metrics**, such as logins, product usage, or service volume.
- **Satisfaction data**, such as survey scores, complaint categories, or the reasons behind support calls.
- **Payment history**, including late payments, billing disputes, and price changes.
- **Plan details**, such as product tier and discounts, to separate the effect of price level from the effect of contract type.
- **Churn timing and outcome reason**, so the analysis can distinguish early-life churn from later churn and understand stated reasons.
- **Larger sample size** or additional periods of data, so that test-set metrics are more stable and results can be validated out of sample.