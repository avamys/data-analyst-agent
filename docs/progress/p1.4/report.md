# Data Analysis Report: Titanic Passenger Survival

## Executive Summary

*   **Gender is the Dominant Predictor:** Female passengers had a survival rate of **74.2%**, compared to only **18.9%** for males. This represents a massive disparity in life chances based on gender alone (Cramer's V = 0.541).
*   **Wealth and Class are Critical Determinants:** Higher fare prices ($48.40 vs $22.12 mean) and First-Class status strongly correlate with survival. The model identifies socioeconomic status as the primary proxy for access to lifeboats.
*   **Geographic Segregation Matters:** Passengers embarking from Cherbourg showed a distinct survival advantage (**55.36%**) compared to those from Southampton (**33.70%**), suggesting demographic differences in boarding groups.
*   **Predictive Power:** A Logistic Regression model utilizing these features achieved an **81.0%** test accuracy, significantly outperforming the trivial majority-class baseline of **58.7%**.
*   **Age Paradox:** Contrary to historical narratives emphasizing child protection, age alone was not a statistically significant predictor ($p=0.058$) in this dataset, suggesting that location (class/gender) outweighed individual age in determining survival probability.

---

## Dataset Overview

*   **Dataset Name:** Titanic Passenger Survival
*   **Size:** 891 rows × 12 columns
*   **Target Variable:** `Survived` (Binary: 0 = No, 1 = Yes)
*   **Key Features:**
    *   **Numeric (5):** Age, SibSp (siblings/spouses aboard), Parch (parents/children aboard), Fare, Embarked.
    *   **Categorical (2):** Sex, Pclass (Passenger Class).
    *   **Text/Missing Data:** Name, Ticket, Cabin (used for analysis but excluded from final modeling due to high missingness).

---

## Analysis Methodology

### Approach
The analysis followed a rigorous, multi-stage pipeline designed to move from foundational understanding to predictive modeling:
1.  **Foundational Understanding:** Quantified missingness patterns and target distribution to inform data cleaning strategies.
2.  **Exploratory Data Analysis (EDA):** Quantified group differences in survival rates and calculated average metrics for key numeric features.
3.  **Statistical Analysis:** Performed hypothesis testing (t-tests, Chi-square) to validate observed differences and calculate effect sizes.
4.  **Feature Engineering:** Handled missing values systematically and encoded categorical variables for modeling.
5.  **Predictive Modeling:** Built a Logistic Regression model to quantify predictive power and feature importance.

### Execution Summary
*   **Total Tasks Executed:** 6
*   **Success Rate:** 100% (6 Completed, 0 Failed)
*   **Specialist Breakdown:**
    *   EDA Specialist: 3 tasks (Missingness, Numeric Relationships, Cabin Analysis)
    *   Statistical Specialist: 1 task (Hypothesis Testing & Effect Sizes)
    *   Machine Learning Specialist: 2 tasks (Feature Prep & Model Training)

---

## Key Findings

### Exploratory Analysis

**1. Missing Value Patterns:**
*   **Age:** 19.87% missing (177 passengers).
*   **Cabin:** 77.10% missing (687 passengers). This is not random; it is heavily correlated with lower passenger class (97.56% missing in 3rd Class vs 18.52% in 1st Class).
*   **Embarked:** Only 0.22% missing (2 passengers).

**2. Target Distribution & Survival Rates:**
*   Overall survival rate: **38.38%** (342 survivors out of 891).
*   **By Sex:** Female (74.20%) vs Male (18.89%).
*   **By Class:** 1st Class (62.96%) > 2nd Class (47.28%) > 3rd Class (24.24%).
*   **By Embarkation Port:** Cherbourg (55.36%) > Queenstown (38.96%) > Southampton (33.70%).

**3. Numeric Feature Relationships:**
*   Survivors had a higher mean fare ($48.40) compared to non-survivors ($22.12).
*   The mean age of survivors (28.34 years) was slightly lower than non-survivors (30.63 years), though the difference is marginal.

### Statistical Evidence

| Feature | Test Type | P-Value | Effect Size | Interpretation |
| :--- | :--- | :--- | :--- | :--- |
| **Sex** | Chi-Square | $1.20 \times 10^{-58}$ | Cramer's V = 0.541 | **Highly Significant.** Large effect size; gender is the strongest predictor. |
| **Pclass** | Chi-Square | $4.55 \times 10^{-23}$ | Cramer's V = 0.340 | **Highly Significant.** Large effect size; class structure drives outcomes. |
| **Fare** | T-Test | $2.70 \times 10^{-11}$ | Cohen's d = 0.505 | **Highly Significant.** Medium effect size; wealth correlates strongly with survival. |
| **Embarked**| Chi-Square | $1.77 \times 10^{-6}$ | Cramer's V = 0.173 | **Significant.** Medium effect size; departure port impacts probability. |
| **Age** | T-Test | 0.0583 | Cohen's d = -0.132 | **Borderline/Insignificant.** Small effect size; age alone is a weak predictor. |

### Predictive Models

*   **Model Type:** Logistic Regression with One-Hot Encoding.
*   **Performance Metrics (Test Set):**
    *   **Accuracy:** 81.0%
    *   **Precision:** 78.6%
    *   **Recall:** 74.3%
    *   **F1-Score:** 76.4%
    *   **ROC-AUC:** 0.882
*   **Baseline Comparison:** The model significantly outperforms a trivial baseline (predicting "No Survival" for everyone) which yields only 58.7% accuracy.
*   **Feature Importance Ranking** (based on absolute coefficients):
    1.  **Sex_male** (Dominant driver)
    2.  **Pclass** (Strong driver)
    3.  **Embarked_S**
    4.  **SibSp** (Family size)
    5.  **Embarked_Q**
    6.  **Parch** (Parents/Children count)
    7.  **Age** (Weak driver)
    8.  **Fare** (Surprisingly weak in the final model, likely due to multicollinearity with Pclass).

---

## Synthesis

Combining EDA, statistical testing, and modeling reveals a clear narrative of **socioeconomic stratification**. The data suggests that "wealth" was the primary proxy for access to lifeboats or priority boarding.

*   **Validated Hypotheses:**
    *   **Gender Bias:** The "Women and Children First" protocol is statistically robust in this dataset, though the data shows that many women (and children) did not survive, while some men survived.
    *   **Class Structure:** Social class was a decisive factor. The correlation between high fare/high class and survival is so strong that it suppresses the apparent weight of Fare in the logistic regression model (multicollinearity).
    *   **The "Unknown" Penalty:** Missing Cabin data acts as a systematic indicator of lower socioeconomic status, limiting its utility without imputation strategies.

*   **Contradictions & Limitations:**
    *   **Age Paradox:** While children survived at high rates, the mean age difference between survivors and non-survivors was not statistically significant ($p=0.058$). This suggests that while children were prioritized, they were a small subset; the bulk of survivors were adults who happened to be in safe locations defined by class and gender.
    *   **Fare vs. Coefficient:** Despite statistical significance in EDA, Fare has a low coefficient in the final model. This is explained by multicollinearity: Pclass captures the variance that Fare also explains.

---

## Conclusions

We can confidently state that survival on the Titanic was not a matter of chance but a function of **social hierarchy**.
1.  **Gender** was the single most critical factor.
2.  **Class (Pclass)** served as the primary determinant of location and resources.
3.  **Fare** acted as a reliable proxy for class, though redundant when Pclass is known.
4.  **Age** played a secondary role, insufficient to overcome the constraints imposed by gender and class.

The predictive model confirms that these structural factors are robust enough to predict outcomes with high accuracy (81%), validating the historical understanding of the disaster's dynamics.

---

## Limitations & Caveats

*   **Data Quality Bias:** The `Cabin` column has 77% missingness, heavily biased toward lower classes. This limits analysis of deck-level survival or specific cabin locations.
*   **Age Significance:** The lack of statistical significance for Age ($p=0.058$) is a limitation of the dataset size and composition; it does not necessarily mean age didn't matter in reality, but that this specific sample lacked the power to detect the effect without interaction terms.
*   **Multicollinearity:** The model attributes most predictive power to Pclass rather than Fare, potentially underestimating the independent value of ticket price if class information were unavailable.

---

## Recommendations

### Immediate Actions
*   **Prioritize Demographics:** Any future analysis or policy simulation regarding emergency evacuation should treat gender and class as primary stratification variables.
*   **Feature Selection:** For modeling purposes, prioritize `Sex` and `Pclass`. While `Fare` is significant, it adds little incremental value if `Pclass` is already included in the model.
*   **Handle Missingness:** Treat missing `Cabin` values as a proxy for low socioeconomic status rather than attempting to impute specific deck numbers without external data.

### Future Analysis
*   **Interaction Effects:** Investigate interaction terms, specifically `Sex * Pclass`. For example, were female passengers in 3rd class treated differently regarding boat access compared to males in 1st class?
*   **Title Engineering:** Extract titles from the `Name` column (e.g., "Mr", "Mrs", "Master") to refine predictions for children and women without relying solely on the binary `Sex` flag.
*   **Deck-Level Analysis:** If possible, impute `Cabin` data using deck information to analyze survival based on proximity to lifeboats, which could provide deeper insight into evacuation logistics.