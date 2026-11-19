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
clean = load("eda_1/clean_frame")
print(clean.shape)
print([repr(c) for c in clean.columns])
print(clean.dtypes.value_counts())
miss = clean.isna().sum()
print(miss[miss > 0])
print(clean['Status'].value_counts())
print(clean['Country'].nunique())

# %%
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

d = clean.copy()
y = d['Life expectancy']
X = d.drop(columns=['Life expectancy', 'Country'])
num_cols = [c for c in X.columns if c != 'Status']
pre = ColumnTransformer([
    ('num', SimpleImputer(strategy='median'), num_cols),
    ('cat', OneHotEncoder(handle_unknown='ignore'), ['Status'])
])
pipe = Pipeline([
    ('pre', pre),
    ('model', RandomForestRegressor(n_estimators=300, random_state=42, n_jobs=-1))
])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipe.fit(X_train, y_train)
res = record_model('ml1_rf', pipe, X_train, y_train, X_test, y_test, 'Random forest predicting Life expectancy from numeric features and Status (one-hot), Country dropped, median imputation, 80/20 split seed 42')
print(res)

# %%
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_absolute_error, r2_score
base_pred = np.full(len(y_test), y_train.mean())
base_mae = mean_absolute_error(y_test, base_pred)
base_rmse = float(np.sqrt(np.mean((y_test - base_pred) ** 2)))
base_r2 = r2_score(y_test, base_pred)
pi = permutation_importance(pipe, X_test, y_test, n_repeats=5, random_state=42, n_jobs=-1, scoring='r2')
imp = pd.DataFrame({'mean': pi.importances_mean, 'sd': pi.importances_std}, index=X_test.columns).sort_values('mean', ascending=False).head(10)
print(imp)
print(base_mae, base_rmse, base_r2)
record_fact('ml1_mean_baseline', {'test_mae': float(base_mae), 'test_rmse': base_rmse, 'test_r2': float(base_r2), 'train_mean': float(y_train.mean())}, 'Mean-prediction baseline on the 586-row test set')
record_fact('ml1_permutation_top10', {k: {'mean': round(float(v['mean']), 4), 'sd': round(float(v['sd']), 4)} for k, v in imp.to_dict('index').items()}, 'Top 10 features by permutation importance (drop in test R2), random forest, 5 repeats')

# %%
print(imp.round(4).to_string())
print(pd.Series({k: round(float(v['mean']), 4) for k, v in imp.to_dict('index').items()}).to_string())

# %%
ranked = [{'rank': i + 1, 'feature': k, 'mean': round(float(v['mean']), 4), 'sd': round(float(v['sd']), 4)} for i, (k, v) in enumerate(imp.to_dict('index').items())]
for r in ranked:
    print(r)
record_fact('ml1_top10_ranked', ranked, 'Top 10 permutation importance in rank order: mean and SD of drop in test R2, random forest, 5 repeats, 586-row test set')
print(record_fact is not None)
