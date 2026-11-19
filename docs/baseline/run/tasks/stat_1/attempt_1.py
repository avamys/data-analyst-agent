import pandas as pd
from scipy import stats
import numpy as np

# Load dataset
df = pd.read_csv('data/titanic.csv')

print("=== Chi-Square Tests for Categorical Features vs Survival ===\n")

# 1. Test: Sex vs Survived
contingency_sex = pd.crosstab(df['Sex'], df['Survived'])
chi2_sex, p_value_sex, dof_sex, expected_sex = stats.chi2_contingency(contingency_sex, correction=False)

print("=== Chi-Square Test: Sex vs Survival ===")
print(f"Test Statistic (χ²): {chi2_sex:.2f}")
print(f"P-value: {p_value_sex:.4f}")
print(f"Degrees of Freedom: {dof_sex}")
# Calculate Cramér's V for effect size
n = df.shape[0]
effect_size_sex = np.sqrt(chi2_sex / (n * (min(contingency_sex.shape) - 1)))
print(f"Effect Size (Cramér's V): {effect_size_sex:.3f}")

if p_value_sex < 0.05:
    print("Conclusion: Significant association between Sex and Survival (p < 0.05)")
else:
    print("Conclusion: No significant association found")

print("-" * 60)

# 2. Test: Pclass vs Survived
contingency_pclass = pd.crosstab(df['Pclass'], df['Survived'])
chi2_pclass, p_value_pclass, dof_pclass, expected_pclass = stats.chi2_contingency(contingency_pclass, correction=False)

print("=== Chi-Square Test: Pclass vs Survival ===")
print(f"Test Statistic (χ²): {chi2_pclass:.2f}")
print(f"P-value: {p_value_pclass:.4f}")
print(f"Degrees of Freedom: {dof_pclass}")
# Calculate Cramér's V for effect size
effect_size_pclass = np.sqrt(chi2_pclass / (n * (min(contingency_pclass.shape) - 1)))
print(f"Effect Size (Cramér's V): {effect_size_pclass:.3f}")

if p_value_pclass < 0.05:
    print("Conclusion: Significant association between Pclass and Survival (p < 0.05)")
else:
    print("Conclusion: No significant association found")

print("-" * 60)

# 3. Test: Embarked vs Survived (handling missing values in 'Embarked')
df_embarked_clean = df.dropna(subset=['Embarked'])
contingency_embarked = pd.crosstab(df_embarked_clean['Embarked'], df_embarked_clean['Survived'])
chi2_embarked, p_value_embarked, dof_embarked, expected_embarked = stats.chi2_contingency(contingency_embarked, correction=False)

print("=== Chi-Square Test: Embarked vs Survival (excluding missing values) ===")
print(f"Test Statistic (χ²): {chi2_embarked:.2f}")
print(f"P-value: {p_value_embarked:.4f}")
print(f"Degrees of Freedom: {dof_embarked}")
# Calculate Cramér's V for effect size
n_embarked = df_embarked_clean.shape[0]
effect_size_embarked = np.sqrt(chi2_embarked / (n_embarked * (min(contingency_embarked.shape) - 1)))
print(f"Effect Size (Cramér's V): {effect_size_embarked:.3f}")

if p_value_embarked < 0.05:
    print("Conclusion: Significant association between Embarked port and Survival (p < 0.05)")
else:
    print("Conclusion: No significant association found")