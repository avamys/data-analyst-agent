# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from agent.execution.runtime import (
    df,
    load,
    publish,
    record_fact,
    record_model,
    save_chart,
)

# %%
from sklearn.model_selection import train_test_split

d = df.copy()
age_median_by_group = d.groupby(['Pclass', 'Sex'])['Age'].transform('median')
d['Age'] = d['Age'].fillna(age_median_by_group).fillna(d['Age'].median())
d['Embarked'] = d['Embarked'].fillna(d['Embarked'].mode()[0])
X = pd.get_dummies(d[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']], columns=['Sex', 'Embarked'], drop_first=False, dtype=int)
y = d['Survived'].astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
publish('train_test', (X_train, X_test, y_train, y_test))
print(X.shape)
print(list(X.columns))
print(y.value_counts().to_dict())
print(X_train.shape, X_test.shape)
print(X.isna().sum().sum())

# %%
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

mu = X_train.mean()
sd = X_train.std()
Xs_train = (X_train - mu) / sd
Xs_test = (X_test - mu) / sd

dummy = DummyClassifier(strategy='most_frequent').fit(X_train, y_train)
r0 = record_model('ml1_majority_baseline', dummy, X_train, y_train, X_test, y_test, 'Majority-class baseline on the shared stratified split')

lr = LogisticRegression(max_iter=1000).fit(Xs_train, y_train)
r1 = record_model('ml1_logistic_regression', lr, Xs_train, y_train, Xs_test, y_test, 'Logistic regression on standardized features, shared split')

rf = RandomForestClassifier(n_estimators=300, random_state=42).fit(X_train, y_train)
r2 = record_model('ml1_random_forest', rf, X_train, y_train, X_test, y_test, 'Random forest, 300 trees, shared split')

print(r0)
print(r1)
print(r2)
print(dict(zip(X.columns, lr.coef_[0].round(3))))
print(dict(zip(X.columns, rf.feature_importances_.round(3))))

# %%
fig, ax = plt.subplots(figsize=(7, 4))
names = ['Majority baseline', 'Logistic regression', 'Random forest']
acc = [r0['test_accuracy'], r1['test_accuracy'], r2['test_accuracy']]
auc = [r0['test_roc_auc'], r1['test_roc_auc'], r2['test_roc_auc']]
x = np.arange(3)
ax.bar(x - 0.2, acc, 0.4, label='Test accuracy')
ax.bar(x + 0.2, auc, 0.4, label='Test ROC AUC')
ax.set_xticks(x)
ax.set_xticklabels(names)
ax.set_ylabel('Score on test set (0 to 1)')
ax.set_ylim(0, 1)
ax.set_title('Test accuracy and ROC AUC by model, shared stratified split')
ax.legend()
save_chart(fig, 'ml1_model_comparison', 'Test accuracy and test ROC AUC for the majority-class baseline, logistic regression and random forest on the same split (n_test=223)')
record_fact('ml1_model_scores', {'baseline_test_accuracy': acc[0], 'logreg_test_accuracy': acc[1], 'rf_test_accuracy': acc[2], 'baseline_test_roc_auc': auc[0], 'logreg_test_roc_auc': auc[1], 'rf_test_roc_auc': auc[2]}, 'Test accuracy and ROC AUC for the three models on the shared split')
print(acc, auc)
