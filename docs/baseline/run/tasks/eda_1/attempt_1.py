import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('data/titanic.csv')

# --- 1. Descriptive Statistics and Summaries ---
print("=== Target Variable Analysis ===")
print(f"Total Passengers: {len(df)}")
print(f"Target Column: 'Survived' (0=No, 1=Yes)")
print("-" * 30)

# Basic counts and percentages
survived_count = df['Survived'].sum()
total_count = len(df)
survival_rate = survived_count / total_count
not_survived_count = total_count - survived_count

print(f"Survived Count: {survived_count}")
print(f"Not Survived Count: {not_survived_count}")
print(f"Overall Survival Rate: {survival_rate:.2%}")

# --- 2. Distribution Analysis (Counts and Ranges) ---
print("\n=== Detailed Distribution ===")
print("Value Counts:")
print(df['Survived'].value_counts().sort_index())

print("\nPercentage Distribution:")
for val in sorted(df['Survived'].unique()):
    pct = df['Survived'].value_counts()[val] / total_count * 100
    print(f"Survived={val}: {pct:.2f}%")

# --- 3. Data Quality Checks (Missing Values) ---
print("\n=== Data Quality Check: Missing Values ===")
missing_stats = df.isnull().sum()
missing_pct = missing_stats[missing_stats > 0] / total_count * 100
for col, count in missing_stats.items():
    if count > 0:
        print(f"Column '{col}': {count} missing values ({count/total_count*100:.2f}%)")

# --- 4. Cross-tabulations and Group Comparisons (Numerical Focus) ---
print("\n=== Group Comparisons by Sex ===")
grouped = df.groupby('Sex')['Survived'].agg(['count', 'sum', 'mean'])
grouped.columns = ['Count', 'Survived_Count', 'Survival_Rate']
for sex in grouped.index:
    rate = grouped.loc[sex, 'Survival_Rate']
    print(f"Sex: {sex} | Survival Rate: {rate:.2%}")

print("\n=== Group Comparisons by Passenger Class (Pclass) ===")
pclass_stats = df.groupby('Pclass')['Survived'].agg(['count', 'mean'])
pclass_stats.columns = ['Count', 'Survival_Rate']
for pclass in sorted(pclass_stats.index):
    rate = pclass_stats.loc[pclass, 'Survival_Rate']
    print(f"Pclass: {pclass} | Survival Rate: {rate:.2%}")

print("\n=== Group Comparisons by Embarked Port ===")
embarked_stats = df.groupby('Embarked')['Survived'].agg(['count', 'mean'])
embarked_stats.columns = ['Count', 'Survival_Rate']
for port in sorted(embarked_stats.index):
    rate = embarked_stats.loc[port, 'Survival_Rate']
    print(f"Embarked: {port} | Survival Rate: {rate:.2%}")

# --- 5. Numerical Summary Statistics for Survived Variable ---
print("\n=== Numerical Summary Statistics (Survived) ===")
print(df['Survived'].describe())

# Check for outliers in Fare based on survival status (Contextual check)
print("\n=== Contextual Outlier Check: Fare by Survival Status ===")
fare_survived = df[df['Survived'] == 1]['Fare'].describe()
fare_not_survived = df[df['Survived'] == 0]['Fare'].describe()

print("Fare Statistics for Survivors (Survived=1):")
for stat in fare_survived.index:
    print(f"  {stat}: {fare_survived[stat]:.2f}")

print("\nFare Statistics for Non-Survivors (Survived=0):")
for stat in fare_not_survived.index:
    print(f"  {stat}: {fare_not_survived[stat]:.2f}")