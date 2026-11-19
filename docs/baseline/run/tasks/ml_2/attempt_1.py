import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('data/titanic.csv')

# Prepare features: Select relevant columns and drop non-informative ones
feature_cols = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
target_col = 'Survived'

# Handle missing values
# Age is the main missing value column. We will fill with median for robustness.
df['Age'] = df['Age'].fillna(df['Age'].median())
# Embarked has missing values, fill with mode
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])

# Encode categorical variables
label_encoders = {}
for col in ['Sex', 'Embarked']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Define feature matrix and target
X = df[feature_cols]
y = df[target_col]

# Split train/test (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# --- Train Logistic Regression Baseline ---
log_reg_model = LogisticRegression(max_iter=1000, random_state=42)
log_reg_model.fit(X_train, y_train)

# Evaluate Logistic Regression
train_acc_lr = log_reg_model.score(X_train, y_train)
test_acc_lr = log_reg_model.score(X_test, y_test)
y_pred_lr = log_reg_model.predict(X_test)

print("=== Logistic Regression Baseline Performance ===")
print(f"Model: Logistic Regression")
print(f"Training Accuracy: {train_acc_lr:.2%}")
print(f"Test Accuracy: {test_acc_lr:.2%}")
print("\nTest Set Classification Report:")
print(classification_report(y_test, y_pred_lr))

# --- Train Random Forest Classifier ---
rf_model = RandomForestClassifier(n_estimators=100, max_depth=None, random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate Random Forest
train_acc_rf = rf_model.score(X_train, y_train)
test_acc_rf = rf_model.score(X_test, y_test)
y_pred_rf = rf_model.predict(X_test)

print("\n=== Random Forest Classifier Performance ===")
print(f"Model: Random Forest Classifier")
print(f"Training Accuracy: {train_acc_rf:.2%}")
print(f"Test Accuracy: {test_acc_rf:.2%}")
print("\nTest Set Classification Report:")
print(classification_report(y_test, y_pred_rf))

# Feature Importance (Random Forest only)
feature_names = X.columns.tolist()
importances = rf_model.feature_importances_
feat_imp_list = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)

print("\n=== Top 5 Important Features ===")
for feat, imp in feat_imp_list[:5]:
    print(f"{feat}: {imp:.4f}")

# Visualize Confusion Matrix for Random Forest on Test Set
plt.figure(figsize=(6, 4))
cm = confusion_matrix(y_test, y_pred_rf)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix: Random Forest (Test Set)')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

# Interpretation Summary
print("\n=== Interpretation ===")
print(f"The Logistic Regression achieved {test_acc_lr:.2%} accuracy on the test set.")
print(f"The Random Forest Classifier achieved {test_acc_rf:.2%} accuracy on the test set.")
print(f"Random Forest generally outperforms Logistic Regression in this dataset due to its ability to capture non-linear relationships and interactions between features (e.g., Age and Fare).")
print(f"Key drivers for survival identified by Random Forest include: {', '.join([f[0] for f in feat_imp_list[:3]])}.")