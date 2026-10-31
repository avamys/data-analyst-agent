# Data Analysis Report: Titanic Passenger Survival Prediction

## Executive Summary
*   **Demographics Dictate Survival:** Gender is the single strongest predictor of survival, with a statistically significant association ($\chi^2 = 263.05$, $p < 0.0001$). Socioeconomic status (Passenger Class) and embarkation port are also critical determinants.
*   **Robust Predictive Performance:** Machine learning models achieve approximately **81–82% accuracy** on unseen test data, indicating strong generalization capabilities despite the small dataset size.
*   **Data Quality Challenges:** The 'Cabin' feature is highly sparse (77.10% missing), rendering standard imputation invalid. Strategic handling via binary flags ('HasCabin') or categorical imputation ('Unknown') is required to preserve information without bias.
*   **Model Comparison:** While Random Forest achieves slightly higher accuracy (~82%), Logistic Regression performs competitively (~80.5%), suggesting that the underlying relationships between features and survival are largely linear or monotonic, though tree-based models better capture non-linear interactions like "Child + Female."

## Dataset Overview
*   **Source:** `data/titanic.csv`
*   **Dimensions:** 891 rows × 12 columns.
*   **Target Variable:** `Survived` (Binary: 0 = No, 1 = Yes).
*   **Feature Composition:** 7 numeric features (Age, Fare, etc.) and 5 categorical features (Sex, Pclass, Embarked, Cabin, Ticket).
*   **Baseline Reality:** The overall survival rate for the population was **38.38%** (342 survivors out of 891 passengers).

## Analysis Methodology

### Strategic Approach
The analysis followed a sequential priority order to ensure robustness:
1.  **Exploratory Strategy:** First, we mapped data structure, identified missing value patterns (specifically in 'Age' and 'Cabin'), and visualized distributions to understand baseline correlations.
2.  **Statistical Strategy:** Second, we applied Chi-Square tests to validate relationships between categorical features (Sex, Pclass, Embarked) and the target, ensuring findings were statistically significant before modeling.
3.  **Predictive Strategy:** Finally, we engineered cleaned features and built classification models (Random Forest, Logistic Regression) to quantify predictive power and handle non-linear interactions.

### Execution Summary
*   **Total Tasks Executed:** 6
*   **Success Rate:** 100% (0 failures).
*   **Specialist Breakdown:**
    *   *Exploratory Data Analysis (EDA):* 2 tasks completed.
    *   *Statistical Testing:* 1 task completed.
    *   *Machine Learning:* 3 tasks completed.
*   **Total Execution Time:** 9.0 seconds.

## Key Findings

### Exploratory Analysis
*   **Target Distribution:** The dataset is imbalanced, with **61.62%** of passengers not surviving (549 cases) versus **38.38%** surviving (342 cases).
*   **Missing Value Patterns:**
    *   **Age:** Contains 177 missing values (**19.87%**). The distribution is relatively symmetric (Mean: 29.70, Median: 28.00), suggesting median imputation is appropriate.
    *   **Cabin:** Extremely sparse with **687 missing values (77.10%)**. Only 147 unique cabin values exist among the non-missing entries. This suggests a confounding variable where lower-class passengers likely lacked assigned cabins.
*   **Data Sparsity Implication:** The high sparsity in 'Cabin' indicates that "No Cabin" is not just missing data but potentially an informative feature correlated with socioeconomic class.

### Statistical Evidence
Hypothesis tests confirmed significant associations between key demographic factors and survival:

| Feature | Test Statistic ($\chi^2$) | P-Value | Effect Size (Cramér's V) | Interpretation |
| :--- | :--- | :--- | :--- | :--- |
| **Sex** | 263.05 | $< 0.0001$ | 0.543 | **Highly Significant.** Gender is the primary determinant of survival. |
| **Pclass** | 102.89 | $< 0.0001$ | 0.340 | **Significant.** Higher socioeconomic class (lower Pclass number) strongly correlates with survival. |
| **Embarked**| N/A | $< 0.05$ | N/A | **Significant.** Port of embarkation influences survival, likely interacting with ticket class and gender. |

### Predictive Models
We evaluated two primary models to determine the best approach for prediction:

*   **Random Forest Classifier:**
    *   **Training Accuracy:** ~98% (Indicates model captures complex patterns).
    *   **Test Accuracy:** **~81.0% - 82.1%** (Strong generalization).
    *   **Insight:** Handles non-linear interactions well (e.g., the specific combination of being a child and female).
*   **Logistic Regression:**
    *   **Training Accuracy:** ~80.2%.
    *   **Test Accuracy:** **~80.45%**.
    *   **Insight:** Performs nearly as well as Random Forest, suggesting the relationship between features and survival is largely linear or monotonic.

**Feature Importance (Inferred):** Based on statistical tests and model behavior, the hierarchy of importance is:
1.  **Sex** (Highest impact).
2.  **Pclass** (Strong secondary impact).
3.  **Embarked** (Significant tertiary impact).
4.  **Age** (High importance when imputed/flagged).

## Synthesis
Combining EDA, statistical testing, and modeling reveals a clear picture of the Titanic disaster dynamics:
*   **Socio-Demographic Stratification:** Survival was not random; it followed a strict hierarchy based on gender and class. The "lifeboat priority" pattern is evident in the data, where intersections like *Female + 1st Class* yield the highest survival probabilities.
*   **Geographic Influence:** The significance of the 'Embarked' variable implies that passengers boarding from different ports (Cherbourg vs. Southampton) had distinct survival rates, potentially due to ticket pricing tiers or proximity to the sinking location relative to embarkation points.
*   **Model Generalization:** The gap between training accuracy (~98%) and test accuracy (~82%) in the Random Forest model is healthy. It indicates the model is learning genuine patterns rather than just memorizing noise, unlike models that collapse from high training to low test scores.

## Conclusions
We can confidently conclude that:
1.  **Gender was the primary factor:** The statistical evidence ($\chi^2 = 263.05$) leaves no doubt that sex was the dominant predictor of survival.
2.  **Class matters significantly:** Socioeconomic status provided a substantial survival advantage, independent of gender to some extent.
3.  **Predictive viability is high:** A model can reliably predict individual survival outcomes with ~81% accuracy, which is robust for this dataset size.
4.  **Data cleaning is critical:** The 'Cabin' column cannot be treated as standard missing data; it must be engineered (e.g., via a `HasCabin` flag) to avoid introducing bias regarding passenger class.

## Limitations & Caveats
*   **Missingness Mechanism Uncertainty:** The analysis notes uncertainty regarding whether missing values in 'Age' and 'Cabin' are Missing At Random (MAR) or Missing Not At Random (MNAR). If MNAR, current imputation strategies may be biased.
*   **Training/Test Discrepancy:** While acceptable, the large gap between training and test accuracy warrants caution when deploying models on significantly larger or different populations.
*   **Incomplete Classification Metrics:** Specific metrics like Precision, Recall, and F1-Score were noted as areas for deeper investigation in the task list but detailed numbers were truncated in the initial synthesis; these are crucial for evaluating false negatives (saving lives).
*   **Small Sample Size:** With only 891 rows, the model's variance is higher than it would be on modern large-scale datasets.

## Recommendations

### Immediate Actions
*   **Feature Engineering for 'Cabin':** Do not drop the 'Cabin' column entirely. Instead, create a binary feature `HasCabin` (Yes/No) and impute missing values with 'Unknown'. This preserves the information that lower-class passengers often lacked cabins.
*   **Imputation Strategy:** For 'Age', use **Median Imputation** (28.00) rather than Mean to minimize skew from outliers, as the distribution is relatively symmetric.
*   **Model Selection:** Both Random Forest and Logistic Regression are viable. If interpretability is a priority, Logistic Regression is preferred; if capturing complex interactions (like child/female synergy) is key, use Random Forest.

### Future Analysis
*   **Interaction Effects:** Investigate specific interaction terms between 'Age' and 'Sex' (e.g., comparing survival rates of young children vs. adult males within the same class).
*   **Threshold Optimization:** Current metrics focus on accuracy. Future work should optimize the decision threshold to minimize False Negatives, prioritizing the "saving lives" objective over pure accuracy.
*   **Feature Engineering:** Explore combining 'Embarked' and 'Fare' to see if they reveal stronger patterns than 'Embarked' alone (e.g., distinguishing between first-class tickets bought at Southampton vs. Cherbourg).
*   **Missingness Investigation:** Conduct deeper analysis to determine if the missingness in 'Cabin' is informative (MNAR) and adjust imputation strategies accordingly.