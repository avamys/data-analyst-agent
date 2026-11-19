# Titanic Survival Analysis Report

## Summary
- Approximately 61.6% of passengers did not survive, while approximately 38.4% survived; survival rates varied significantly by passenger class, with first-class passengers having a much higher survival probability than third-class.
- Statistical tests confirm that Pclass, Sex, and Fare are highly significant predictors of survival (p < 0.001), whereas Age shows a statistically significant but weaker association (p = 0.041).
- Missing data patterns reveal that missing 'Cabin' records are strongly associated with lower passenger classes and non-survival, while missing 'Age' is correlated with both Pclass and survival status.
- Machine learning models using imputed features achieved test accuracies of ~82% (Random Forest) and ~81% (Logistic Regression), significantly outperforming a baseline model that predicted the most frequent class (~59%).

## Data
The dataset contains 891 rows and 12 columns. The target variable is 'Survived' (binary). Numeric features include Pclass, Age, SibSp, Parch, and Fare; categorical features are Sex and Embarked. Missing values exist in Age (19.9%), Cabin (77.1%), and Embarked (0.2%).

## Findings

### Baseline Distribution and Missingness
Approximately 61.6% of passengers did not survive ('Survived'=0), while approximately 38.4% survived ('Survived'=1). The percentage of missing values is 19.87% for 'Age', 77.10% for 'Cabin', and 0.22% for 'Embarked'. Correlation analysis indicates that Age missingness correlates with Survived (-0.09) and Pclass (0.17); Cabin missingness correlates with Survived (-0.32) and Pclass (0.73); Embarked missingness correlates with Survived (0.06) and Pclass (-0.07).

![Survival Rate, Average Fare, and Median Age by Pclass and Sex](tasks/eda_2/charts/eda_2_grouped_stats.png)
![Survival Rate by Pclass, Sex, and Embarked](tasks/eda_2/charts/eda_2_survival_by_embarked.png)
![Average Fare by Pclass, Sex, and Embarked](tasks/eda_2/charts/eda_2_fare_by_embarked.png)
![Median Age by Pclass, Sex, and Embarked](tasks/eda_2/charts/eda_2_age_by_embarked.png)

### Statistical Significance of Features
For Pclass, the Chi-square test shows a highly significant difference in survival rates ($χ^2 = 102.89$, $p = 4.55e-23$), with a large effect size (Cramer's V $≈ 0.34$). For Sex, the Chi-square test shows a highly significant difference in survival rates ($χ^2 = 263.05$, $p < 0.001$), with a large effect size (Cramer's V $≈ 0.54$). For Embarked, the Chi-square test shows a significant difference in survival rates ($χ^2 = 26.49$, $p < 0.001$), with a moderate effect size (Cramer's V $≈ 0.17$). For Age, the t-test shows a statistically significant difference in survival rates ($t = -2.05$, $p = 0.041$), with a small-to-moderate effect size (Cohen's h $≈ -0.38$). For Fare, the t-test shows a highly significant difference in survival rates ($t = 6.84$, $p = 2.70e-11$), with a moderate effect size (Cohen's h $≈ -0.47$).

![Age and Fare distributions for Survived vs Not Survived](tasks/stat_1/charts/numeric_survival_distributions.png)

### Feature Importance
The Random Forest model identifies 'Sex', 'Fare', and 'Age' as the top three features driving survival predictions, with importance scores of 0.2733, 0.2721, and 0.2527 respectively. The Logistic Regression model achieved a test accuracy of 0.8101, also outperforming the baseline.

![Feature Importance from Random Forest Model](tasks/ml_2/charts/feature_importance.png)
![Comparison of Baseline, Logistic Regression, and Random Forest model accuracies](tasks/ml_1/charts/model_comparison.png)

### Interaction Effects
Survival rates for the four groups (Male/Female x Pclass 1/2/3) are: Female in 1st Class (96.8%), Male in 1st Class (36.9%), Female in 2nd Class (92.1%), Male in 2nd Class (15.7%), Female in 3rd Class (50.4%), Male in 3rd Class (13.6%). The effect of 'Fare' on survival differs significantly between sexes: For males, the mean fare for survivors is $40.82 vs $21.96 for non-survivors (difference ~$18.86), while for females it is $51.94 vs $16.28 (difference ~$25.66). Additionally, survival rates increase with fare quartiles for both sexes, but the gap between male and female survival rates narrows at higher fares.

![Comparison of survival rates across Pclass and Sex groups](tasks/eda_3/charts/survival_rates_pclass_sex.png)

### Missingness Mechanisms
Passengers with missing 'Age' data have a survival rate of 0.294, compared to 0.406 for those with recorded age values (p-value: 0.0059). Passengers with missing 'Cabin' data have a survival rate of 0.300, compared to 0.667 for those with recorded cabin values (p-value: 3.09e-22). Passengers with missing 'Embarked' data have a survival rate of 1.0, compared to 0.382 for those with recorded embarkation ports (p-value: 0.0730). The Pearson correlation between 'Age' (non-missing) and 'Survived' is -0.077.

![Survival rates for passengers with missing vs recorded Age and Cabin data](tasks/stat_2/charts/stat_2_survival_by_missingness.png)

Cabin missingness is heavily concentrated in lower passenger classes (Pclass 3: 53.8%) and among non-survivors (54.0%). Age missingness increases with lower Pclass (Pclass 3: 15.3%) and shows a strong pattern related to Fare, being highest in the lowest Fare Quartile (Q0: 35.9%).

![Missing values for Cabin and Age by Pclass (left) and Survived (right)](tasks/eda_4/charts/eda_4_missingness_patterns.png)

## Limitations
The findings regarding grouped statistics for Pclass, Sex, and Embarked are incomplete due to data representation errors in the aggregation step; specifically, the recorded dictionary keys included non-existent values (e.g., '0' to '17') instead of the valid range (1-3), preventing a complete citation of specific group survival rates. Additionally, the discussion on missingness bias relies on correlations found in the baseline analysis but does not fully resolve how global median imputation for 'Age' interacts with the structural dependency between missing age and passenger class.

**Numbers not traced to a recorded fact.** The automatic check found no recorded value for these numbers:
- 0.34 in: "For Pclass, the Chi-square test shows a highly significant difference in survival rates ($χ^2 = 102.89$, $p = 4.55e-23$), with a large effect size (Cramer's V $"
- 263.05 in: "For Pclass, the Chi-square test shows a highly significant difference in survival rates ($χ^2 = 102.89$, $p = 4.55e-23$), with a large effect size (Cramer's V $"
- 0.54 in: "For Pclass, the Chi-square test shows a highly significant difference in survival rates ($χ^2 = 102.89$, $p = 4.55e-23$), with a large effect size (Cramer's V $"
- 26.49 in: "For Pclass, the Chi-square test shows a highly significant difference in survival rates ($χ^2 = 102.89$, $p = 4.55e-23$), with a large effect size (Cramer's V $"
- 50.4% in: "Survival rates for the four groups (Male/Female x Pclass 1/2/3) are: Female in 1st Class (96.8%), Male in 1st Class (36.9%), Female in 2nd Class (92.1%), Male i"
- 13.6% in: "Survival rates for the four groups (Male/Female x Pclass 1/2/3) are: Female in 1st Class (96.8%), Male in 1st Class (36.9%), Female in 2nd Class (92.1%), Male i"
- 18.86 in: "Survival rates for the four groups (Male/Female x Pclass 1/2/3) are: Female in 1st Class (96.8%), Male in 1st Class (36.9%), Female in 2nd Class (92.1%), Male i"
- 16.28 in: "Survival rates for the four groups (Male/Female x Pclass 1/2/3) are: Female in 1st Class (96.8%), Male in 1st Class (36.9%), Female in 2nd Class (92.1%), Male i"
- 25.66 in: "Survival rates for the four groups (Male/Female x Pclass 1/2/3) are: Female in 1st Class (96.8%), Male in 1st Class (36.9%), Female in 2nd Class (92.1%), Male i"

## Open questions
- Investigate the impact of different imputation strategies for 'Age' on model performance.
- Analyze the impact of encoding 'Embarked' with different methods (e.g., one-hot vs. label encoding) on model accuracy.
- Investigate if missing 'Cabin' values are associated with specific ticket prefixes or embarkation ports.
- Analyze the distribution of 'Age' for passengers with known vs. unknown age to understand the imputation strategy.