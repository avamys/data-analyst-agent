# Data Analysis Report: Customers

## Executive Summary

- **Contract type is significantly associated with churn** (chi-square p = 1.47×10⁻⁶). Contract terms are a business lever, so this is the most directly actionable finding. The churn rate for each contract level is not in the analysis outputs, so the size of the gap is still unknown. Pulling those rates is the first step.
- **Monthly fee and support calls both differ strongly between churned and retained customers** (fee: Mann-Whitney p = 4.4×10⁻¹⁰; support calls: Mann-Whitney p = 8.5×10⁻⁷). The direction and magnitude of these differences were not reported, so the findings can flag where to look but cannot yet size the effect or define an intervention threshold.
- **Region has no detectable relationship with churn** (chi-square p = 0.448). Geographic targeting of retention campaigns is not supported by this data.
- **A predictive model can rank customers by churn risk, but only moderately.** Logistic regression (class-weighted) reaches test ROC-AUC ≈ 0.71 and PR-AUC 0.530, against a 0.312 baseline (about 1.7× lift). It is useful for prioritizing outreach, but its precision at any threshold is too low to act on without cost-based tuning.
- **Churn affects roughly 31% of customers (250 of 800).** The imbalance is moderate and was handled by class weighting. The dataset is small, so the test-set estimates are imprecise.

---

## Dataset Overview

| Attribute | Value |
|---|---|
| Source | `/workspaces/agents/evals/data/customers.csv` |
| Records | 800 |
| Columns | 5 (2 numeric, 3 categorical) |
| Target | `churned_flag` (binary: "yes" / "no") |
| Numeric features | `monthly_fee` (float), `support_calls` (integer) |
| Categorical features | `contract`, `region`, `churned_flag` (target) |
| Missing values | 0 |
| Duplicate rows | 3 (not yet addressed) |
| Class balance | Retained 550 (68.8%), Churned 250 (31.2%) |
| Imbalance ratio | 2.2 : 1 |

---

## Analysis Methodology

### Strategic Approach

The analysis followed a three-stage sequence, with each stage building on the one before it:

1. **Exploratory analysis first.** With a small dataset, the distributions, category counts, and group-level churn rates needed to be understood before any modeling. This stage also checked for skew, outliers, and duplicates.
2. **Statistical testing second.** Chi-square tests were used for the categorical features, and Welch t-tests and Mann-Whitney U tests for the numeric features, comparing churned and retained customers. Because support calls are right-skewed, the nonparametric results were given priority for that variable.
3. **Predictive modeling last.** Logistic regression and gradient boosting were trained with class weighting and evaluated with cross-validation and a held-out test set. The evaluation focused on ROC-AUC, PR-AUC, and minority-class (churn) recall, not accuracy, because accuracy is misleading when 69% of customers are retained.

### Execution

| Specialist | Tasks Completed |
|---|---|
| Exploratory Data Analysis | 2 |
| Statistical Analysis | 2 |
| Machine Learning | 2 |
| **Total** | **6 of 6 (100% success, 0 failures)** |

Total execution time was 110.9 seconds.

---

## Key Findings

### Exploratory Analysis

**Data quality**
- The dataset is complete, with no missing values across 800 rows.
- Three duplicate rows were detected and not yet removed.

**Numeric distributions**

| Feature | Mean | Median | Skew | Interpretation |
|---|---|---|---|---|
| `monthly_fee` | 70.44 | 71.20 | −0.02 | Nearly symmetric; mean and median are close |
| `support_calls` | 1.50 | 1.00 | 0.80 | Right-skewed; most customers have 0–2 calls, with a long upper tail |

- Monthly fee needs no transformation.
- Support calls are skewed, which is why nonparametric tests are preferred for that variable. IQR outlier counts were referenced but not reported, so the extent of the upper tail is not quantified.

**Target distribution**
- Overall churn rate: **31.25%** (250 of 800 customers).
- Class imbalance is moderate (2.2 : 1). Class weighting was sufficient and resampling was not required.

**Categorical breakdowns**
- Churn rates by contract level and by region were requested, but the outputs do not include them. The contingency table for the chi-square test is also empty in the statistical output. These are the most actionable descriptive numbers and should be the first addition to the report.

**Correlations**
- A correlation matrix among the numeric features was computed, but the results were not reported. Collinearity between fee and support calls therefore cannot be assessed.

---

### Statistical Evidence

Four hypothesis tests were run. Bonferroni correction for four comparisons sets the significance threshold at 0.05 / 4 = **0.0125**. The results below are reported against both the 0.05 and the corrected threshold.

| Hypothesis | Test | Statistic p-value | Significant at 0.05? | Survives Bonferroni (0.0125)? | Decision |
|---|---|---|---|---|---|
| Churn is associated with contract type | Chi-square test of independence | **1.47 × 10⁻⁶** | Yes | Yes | Reject H₀ |
| Churn is associated with region | Chi-square test of independence | **0.448** | No | No | Fail to reject H₀ |
| Monthly fee differs by churn status | Welch t-test | **1.4 × 10⁻¹⁰** | Yes | Yes | Reject H₀ |
| Monthly fee differs by churn status | Mann-Whitney U | **4.4 × 10⁻¹⁰** | Yes | Yes | Reject H₀ |
| Support calls differ by churn status | Welch t-test | **3.6 × 10⁻⁷** | Yes | Yes | Reject H₀ |
| Support calls differ by churn status | Mann-Whitney U | **8.5 × 10⁻⁷** | Yes | Yes | Reject H₀ |

**Plain-English interpretation**

- **Contract type:** Churn rates are not the same across contract categories. The result is highly significant, but the magnitude is unknown.
- **Region:** The data does not show that churn differs by region. The non-significant result is a finding in its own right: region is unlikely to be a useful targeting variable. It does not prove that regions are identical, since the test has limited power at this sample size.
- **Monthly fee:** Churned and retained customers differ in monthly fee. Both parametric and nonparametric tests agree. The direction of the difference (whether churners pay more or less) is not reported in the outputs.
- **Support calls:** Churned and retained customers differ in support call volume. Because the variable is skewed, the Mann-Whitney result is more trustworthy than the Welch result. The direction is also not reported.

**Effect sizes and confidence intervals**

Effect sizes were not reported for any test. This is a material gap. With 800 observations, even trivial differences can reach p < 0.001, so the p-values alone do not establish practical importance.

| Test | Needed effect size | Status |
|---|---|---|
| Chi-square (contract, region) | Cramér's V | Not reported |
| Welch t-test / Mann-Whitney (fee) | Cohen's d or rank-biserial r | Not reported |
| Welch t-test / Mann-Whitney (support calls) | Cohen's d or rank-biserial r | Not reported |

The statistical output also mentions permutation tests, bootstrap confidence intervals, and an undersampling sensitivity analysis, but none of their results appear in the output. These should be treated as not yet completed.

**Assumption checks**
- Welch's t-test assumes approximately normal group means. This is reasonable for monthly fee but questionable for support calls, which supports the emphasis on Mann-Whitney.
- The chi-square test assumes expected cell counts of at least 5. This has not been verified, and it matters most if any contract category is small.

---

### Predictive Models

**Models tested**
- Logistic regression with class weighting (balanced)
- Gradient boosting with class weighting (balanced)

Evaluation used a train/test split (test set ≈ 160 rows, ≈ 50 churners) and 5-fold cross-validation.

**Performance summary**

| Metric | Logistic Regression | Gradient Boosting |
|---|---|---|
| Test ROC-AUC | **0.713** (0.711 in one summary) | 0.701 |
| Test PR-AUC | **0.530** (baseline 0.312) | Not reported |
| Train–test ROC-AUC gap | −0.007 | +0.066 |
| Recall at threshold 0.5 | 70.0% | Not reported |
| Precision at threshold 0.5 | 53.0% | Not reported |
| Churn recall at threshold 0.519 | 64.0% | Not reported |

**Model selection**
- Logistic regression was selected. Both 5-fold CV ROC-AUC and CV PR-AUC favored it, which makes the choice robust across two criteria.
- Gradient boosting showed a train–test gap of +0.066, indicating overfitting. Logistic regression's gap is near zero.

**Interpreting the metrics**
- A PR-AUC of 0.530 against a random-classifier baseline of 0.312 is about **1.7× lift**. That is useful for ranking, but it means many flagged customers will not churn.
- At the default 0.5 threshold, the model catches 70% of churners, but only 53% of flagged customers actually churn. Raising the threshold to 0.519 trades about 6 points of recall (70% → 64%) for higher precision. The right operating point depends on the relative cost of missing a churner versus offering retention incentives to a customer who would have stayed, and that cost has not been quantified.
- With roughly 50 churners in the test set, the ROC-AUC confidence interval is probably ±0.05 or wider. Differences of around 0.01 between the two models are not meaningful.

**Feature importance**
- A feature importance ranking was requested, but none is included in the outputs.
- Based on the univariate tests, monthly fee, support calls, and contract type are the likely drivers, and region is unlikely to contribute. This is an inference, not a measured result. It should be confirmed with logistic regression coefficients (with standardized inputs) or permutation importance on the held-out set.

**Predictive insights**
- Churn is predictable to a moderate degree from the available variables.
- The fee and support-call signals are individually significant but do not combine into strong discrimination, which suggests churn is driven by many weaker, overlapping factors not captured in this dataset.

---

## Synthesis

**Validated, consistent findings**

| Finding | Evidence from Multiple Analyses |
|---|---|
| Contract type matters | Significant chi-square (p = 1.5×10⁻⁶); survives Bonferroni correction |
| Monthly fee differs by churn status | Significant under both parametric and nonparametric tests; survives correction |
| Support calls differ by churn status | Significant under both tests; Mann-Whitney preferred due to skew; survives correction |
| Region does not matter | Non-significant chi-square (p = 0.448); consistent with weak predictive contribution |

**Cross-cutting patterns**

1. **Pricing and service appear together.** Fee and support calls are the two strongest numeric signals. Together they suggest a plausible mechanism: price sensitivity combined with dissatisfaction. Whether they interact (for example, whether high-fee customers with frequent support contacts are the highest risk) has not been tested.

2. **Structural factors over geography.** Contract type is significant and region is not. Churn seems to follow account and customer characteristics rather than location.

3. **Significance does not equal predictive power.** The strongest univariate effects produce a model with only moderate discrimination (ROC-AUC ≈ 0.71). Retention targeting should not rely on any single variable.

4. **Model choice is stable.** The simpler logistic regression is favored by both cross-validation criteria and shows no sign of overfitting, so it is the defensible production candidate.

---

## Conclusions

**What we can say with confidence**

- Churn is not evenly distributed across the customer base. Contract type, monthly fee, and support call volume are each significantly associated with churn, and these associations survive correction for multiple comparisons.
- Region is not a meaningful churn signal in this data.
- About 31% of customers churn, and a class-weighted logistic regression ranks churn risk with moderate skill (ROC-AUC ≈ 0.71, PR-AUC about 1.7× baseline).
- Logistic regression is the more reliable model here, since gradient boosting overfits.

**What we cannot yet say**

- Which direction each relationship runs, and how large each effect is.
- Which contract type churns most, or by how much.
- How many churners each support call or fee increment corresponds to.
- Whether the model is precise enough to drive individual-level decisions at any threshold.
- Whether the results hold over time or across regions.

**Bottom line:** The data supports using contract type, fee, and support-call volume as the starting variables for a retention-risk score. It does not yet support specific pricing or service interventions, because effect sizes, directions, and cost trade-offs are missing.

---

## Limitations & Caveats

### Data Quality Issues
- **Duplicates:** Three duplicate rows remain. They should be removed or justified before modeling.
- **Outliers:** IQR outlier counts were referenced but not reported. Support calls may have high-value outliers that affect the Welch t-test.
- **Encoding:** The target is labeled "yes"/"no" in the statistical tests but "churned_flag" in the EDA. The encoding should be confirmed as consistent across pipelines.
- **Empty contingency table:** The contract × churn contingency table is blank in the statistical output, so the cell counts behind the chi-square test cannot be verified.

### Statistical Assumptions and Limitations
- **Multiple comparisons:** Four tests were run without an adjustment in the original outputs. The significant results survive Bonferroni correction, but the adjustment has been applied here, not in the source analysis.
- **Effect sizes missing:** Without them, practical importance cannot be judged from the p-values.
- **Expected cell counts:** The chi-square assumption (expected counts ≥ 5) has not been verified.
- **Class imbalance:** The tests do not account for imbalance directly. This does not invalidate them, but it reduces the power of group comparisons.

### Predictive Modeling Limitations
- **Small test set:** About 160 test rows and about 50 churners produce wide confidence intervals on ROC-AUC.
- **Unexplained distribution shift:** An adversarial validation AUC of 0.637 was reported as a "small shift in distributions" with no explanation. If accurate, train and test populations differ, and test metrics may be optimistic or pessimistic. This must be investigated.
- **Inconsistent reporting:** Logistic regression ROC-AUC appears as both 0.713 and 0.711. The source should be confirmed. The train–test gap is also slightly negative (−0.007), meaning test performance is marginally higher than training performance. This is uncommon and worth checking for data leakage or a split artifact.
- **Incomplete gradient boosting results:** Its PR-AUC, precision, and recall were not reported, so the two models are not compared on the same metrics.
- **Threshold not tuned to costs:** The 0.5 and 0.519 thresholds were not chosen against a business cost model.

### Failed or Incomplete Analyses
All six tasks completed successfully, but the following were requested or referenced without reported results:
- Permutation tests and bootstrap confidence intervals
- Undersampling sensitivity analysis
- Effect sizes and confidence intervals
- Feature importance ranking and model coefficients
- Correlation matrix results
- IQR outlier counts
- Churn rates by contract level and by region
- Probability calibration check

### Missing Information
- Tenure, usage, payment history, and demographics
- The cost of a retention offer relative to the value of a retained customer
- The time period covered by the data (needed for any temporal validation)

---

## Recommendations

### Immediate Actions

1. **Report churn rates by contract level and by region.** This is the most actionable information and requires only a groupby on existing data. It also completes the contingency table that is currently blank.

2. **Report direction and size of the fee and support-call effects.** Compute group means and medians, and effect sizes (rank-biserial r for both variables, Cramér's V for contract). Without these, the fee and support-call findings cannot be translated into interventions.

3. **Clean the data.** Remove or justify the three duplicate rows, confirm the target encoding, and report IQR outlier counts for both numeric features.

4. **Investigate the adversarial AUC of 0.637.** Determine whether train and test distributions differ, and whether that shift affects the reported model metrics. Also confirm the 0.711 vs. 0.713 discrepancy.

5. **Do not use region as a basis for geographic retention targeting.** The data does not support it.

6. **Set the decision threshold using business costs.** Estimate the cost of a missed churner and the cost of an unnecessary retention offer. Use these to select between the 0.5 and 0.519 operating points, or a different threshold entirely.

7. **Pilot a risk-based outreach program with a holdout group.** Use the logistic regression score to prioritize a subset of at-risk customers, and compare their churn to a randomly selected control group. This tests whether the model's ranking translates into retention gains, which the offline metrics cannot establish.

### Future Analysis

**Statistical questions**
- Do fee and support calls interact? Test a fee × support-call interaction term in the model.
- What is the shape of the relationship between support calls and churn? Check whether it plateaus or accelerates, for example with a binned churn-rate plot.
- Do the fee and contract effects hold within each region? Check for region-specific effects.
- Compute bootstrap confidence intervals for all key metrics, including ROC-AUC and PR-AUC.

**Modeling questions**
- Report feature importance using standardized logistic regression coefficients and permutation importance on the test set.
- Check probability calibration (calibration curve and Brier score) before using predicted probabilities for cost-based decisions.
- Run repeated stratified cross-validation to reduce the variance of the performance estimates.
- Complete the gradient boosting evaluation with PR-AUC, precision, and recall, so the two models are compared on the same metrics.
- Test whether adding interaction terms or nonlinear fee and support-call effects improves on the current model.

**Validation questions**
- Is performance stable over time? A temporal split (train on earlier customers, test on later) is the most realistic check for a churn model.

### Data to Collect

| Data | Why It Matters |
|---|---|
| **Tenure** (months as a customer) | Often the strongest churn predictor; likely to improve AUC beyond 0.71 |
| **Usage or engagement metrics** | Shows whether low activity precedes churn |
| **Payment history** (late payments, failed charges) | Financial friction is a common churn driver |
| **Support call reasons and resolution outcomes** | Tells whether unresolved issues, not just call volume, drive churn |
| **Price change history** | Distinguishes customers who churn after a fee increase from those who were always high-fee |
| **Churn date and observation window** | Enables time-based validation and survival analysis |
| **Customer segment or product tier** | Tests whether effects differ by customer type |
| **Retention offer costs and customer lifetime value** | Required to set a financially optimal threshold |

The highest-value addition is probably **tenure and engagement data**. The current features explain only part of churn, and the modest ROC-AUC suggests important drivers are missing from the dataset.