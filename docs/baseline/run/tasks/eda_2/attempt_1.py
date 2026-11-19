import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('data/titanic.csv')

print("=== Missing Value Analysis for 'Age' and 'Cabin' ===")
print(f"Total Rows: {len(df)}")
print("-" * 50)

# Age Column Analysis
age_missing_count = df['Age'].isna().sum()
age_missing_pct = (age_missing_count / len(df)) * 100
age_min = df['Age'].min()
age_max = df['Age'].max()
age_mean = df['Age'].mean()
age_median = df['Age'].median()

print(f"Column: Age")
print(f"Missing Count: {age_missing_count}")
print(f"Missing Percentage: {age_missing_pct:.2f}%")
print(f"Range (Min-Max): [{age_min}, {age_max}]")
print(f"Mean: {age_mean:.2f} | Median: {age_median:.2f}")
print(f"Interpretation: Age has {age_missing_count} missing values ({age_missing_pct:.2f}%). "
      f"The median ({age_median:.2f}) is closer to the mean ({age_mean:.2f}), suggesting a relatively symmetric distribution. "
      f"Imputation strategy: Median imputation is preferred over Mean to minimize skew from outliers.")
print("-" * 50)

# Cabin Column Analysis
cabin_missing_count = df['Cabin'].isna().sum()
cabin_missing_pct = (cabin_missing_count / len(df)) * 100
cabin_non_null_unique = df['Cabin'][~df['Cabin'].isna()].nunique()

print(f"Column: Cabin")
print(f"Missing Count: {cabin_missing_count}")
print(f"Missing Percentage: {cabin_missing_pct:.2f}%")
print(f"Unique Non-Missing Values: {cabin_non_null_unique}")
print(f"Interpretation: Cabin has {cabin_missing_count} missing values ({cabin_missing_pct:.2f}%). "
      f"This indicates that a large portion of passengers did not have a recorded cabin number. "
      f"Imputation strategy: Since the data is highly sparse and categorical, simple mean/median imputation is invalid. "
      f"Strategies include: 1) Drop rows if critical, 2) Impute with 'Unknown', or 3) Create a binary flag (HasCabin).")
print("-" * 50)

# Cross-tabulation: Missingness vs Survival for Age
age_missing_survived = df[df['Age'].isna()][['Survived']].value_counts().sort_index()
age_present_survived = df[~df['Age'].isna()][['Survived']].value_counts().sort_index()

print("=== Cross-Tabulation: Missingness vs Survival ===")
print(f"Passengers with missing Age - Survived: {age_missing_survived.get(1, 0)}, Not Survived: {age_missing_survived.get(0, 0)}")
print(f"Passengers with known Age - Survived: {age_present_survived.get(1, 0)}, Not Survived: {age_present_survived.get(0, 0)}")
print("Interpretation: Comparing survival rates between missing and non-missing Age groups can reveal if the missingness is random or informative.")

# Cross-tabulation: Cabin Presence vs Survival
cabin_has_survived = df[df['Cabin'].notna()][['Survived']].value_counts().sort_index()
cabin_missing_survived = df[df['Cabin'].isna()][['Survived']].value_counts().sort_index()

print("=== Cross-Tabulation: Cabin Presence vs Survival ===")
total_cabin = len(df[df['Cabin'].notna()])
total_no_cabin = len(df[df['Cabin'].isna()])
if total_cabin > 0:
    survival_rate_with_cabin = (cabin_has_survived.get(1, 0) / total_cabin) * 100
else:
    survival_rate_with_cabin = 0
if total_no_cabin > 0:
    survival_rate_without_cabin = (cabin_missing_survived.get(1, 0) / total_no_cabin) * 100
else:
    survival_rate_without_cabin = 0

print(f"Survival Rate with Cabin: {survival_rate_with_cabin:.2f}%")
print(f"Survival Rate without Cabin: {survival_rate_without_cabin:.2f}%")
print("Interpretation: If survival rates differ significantly, 'Cabin' presence is a strong predictor and should be encoded as a binary feature before imputation.")

# Summary Statistics for Age by Sex (to inform stratified imputation)
age_stats_by_sex = df.groupby('Sex')['Age'].agg(['mean', 'median', 'count']).round(2)
print("=== Age Statistics by Sex ===")
print(age_stats_by_sex)
print("Interpretation: If imputing, consider calculating the median separately for each Sex group to preserve demographic differences.")