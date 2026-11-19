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
print(df.dtypes)
print(df.head(3))
print(df['plan'].value_counts(dropna=False))
print(df['churned'].value_counts(normalize=True).round(4))
print(df['refund_issued'].value_counts(dropna=False).head(10))
print(df.isna().sum())

# %%
from sklearn.model_selection import train_test_split
X_base = pd.concat([df[['usage_hours', 'tenure_months']], pd.get_dummies(df['plan'], prefix='plan', dtype=int)], axis=1)
X_no = X_base.copy()
X_with = X_base.assign(refund_issued=df['refund_issued'].astype(int))
y = df['churned'].astype(int)
idx = np.arange(len(df))
tr_idx, te_idx = train_test_split(idx, test_size=0.2, stratify=y, random_state=42)
X_train_no_leak = X_no.iloc[tr_idx]
X_test_no_leak = X_no.iloc[te_idx]
X_train_with_refund = X_with.iloc[tr_idx]
X_test_with_refund = X_with.iloc[te_idx]
y_train = y.iloc[tr_idx]
y_test = y.iloc[te_idx]
baseline_acc = float((y_test == 0).mean())
split_data = {'X_train_no_leak': X_train_no_leak, 'X_test_no_leak': X_test_no_leak, 'X_train_with_refund': X_train_with_refund, 'X_test_with_refund': X_test_with_refund, 'y_train': y_train, 'y_test': y_test, 'feature_names': {'no_leak': list(X_no.columns), 'with_refund': list(X_with.columns)}}
publish('split_data', split_data)
record_fact('split_sizes', {'n_train': len(tr_idx), 'n_test': len(te_idx), 'test_size': 0.2, 'random_state': 42}, 'Stratified 80/20 split sizes')
record_fact('split_class_rates', {'train_churn_rate': float(y_train.mean()), 'test_churn_rate': float(y_test.mean())}, 'Churn rate in each split')
record_fact('baseline_always_0_test_accuracy', {'test_accuracy': baseline_acc}, 'Test accuracy of always predicting class 0')
record_fact('feature_sets', {'no_leak_features': list(X_no.columns), 'with_refund_features': list(X_with.columns)}, 'Feature sets; with_refund is comparison only')
print(X_no.shape, X_with.shape, len(tr_idx), len(te_idx))
print(round(baseline_acc, 4), round(float(y_train.mean()), 4), round(float(y_test.mean()), 4))

# %%
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
c = DecisionTreeClassifier(max_depth=3, random_state=42).fit(X_train_with_refund[['refund_issued']], y_train)
tr = accuracy_score(y_train, c.predict(X_train_with_refund[['refund_issued']]))
te = accuracy_score(y_test, c.predict(X_test_with_refund[['refund_issued']]))
record_fact('refund_only_leak_check', {'train_accuracy': float(tr), 'test_accuracy': float(te)}, 'Leakage check: shallow tree on refund_issued alone')
print(round(tr, 3), round(te, 3))
