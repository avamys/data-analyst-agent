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
d = df.copy()
d.columns = [c.strip() for c in d.columns]
print(d.shape)
print(d['Country'].nunique(), 'countries')
print(d['Status'].value_counts().to_dict())
print(d['Country'].value_counts().describe().round(2).to_dict())
print(d.isna().sum()[d.isna().sum()>0].to_dict())

# %%
from sklearn.model_selection import GroupKFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
t = 'Life expectancy'
e = d.dropna(subset=[t]).reset_index(drop=True)
y = e[t]
g = e['Country']
num_cols = [c for c in e.columns if c not in ['Country', t, 'Status'] and pd.api.types.is_numeric_dtype(e[c])]
X = pd.get_dummies(e[num_cols + ['Status']], columns=['Status'], dtype=float)
rows = []
for k, (tr, te) in enumerate(GroupKFold(n_splits=5).split(X, y, g)):
    rf = make_pipeline(SimpleImputer(strategy='median'), RandomForestRegressor(n_estimators=300, random_state=42, n_jobs=-1))
    rf.fit(X.iloc[tr], y.iloc[tr])
    p = rf.predict(X.iloc[te])
    b = np.full(len(te), y.iloc[tr].mean())
    yt = y.iloc[te]
    overlap = len(set(g.iloc[tr]) & set(g.iloc[te]))
    rows.append({'fold': k, 'n_test_rows': len(te), 'n_test_countries': int(g.iloc[te].nunique()), 'n_train_countries': int(g.iloc[tr].nunique()), 'country_overlap': overlap, 'rf_r2': r2_score(yt, p), 'rf_mae': mean_absolute_error(yt, p), 'rf_rmse': np.sqrt(mean_squared_error(yt, p)), 'base_r2': r2_score(yt, b), 'base_mae': mean_absolute_error(yt, b), 'base_rmse': np.sqrt(mean_squared_error(yt, b))})
r = pd.DataFrame(rows)
print(r.round(3).to_string())
summ = {}
for c in ['rf_r2', 'rf_mae', 'rf_rmse', 'base_r2', 'base_mae', 'base_rmse']:
    summ[c] = {'mean': float(r[c].mean()), 'sd': float(r[c].std())}
summ['mean_test_countries'] = float(r['n_test_countries'].mean())
summ['total_country_overlap'] = int(r['country_overlap'].sum())
summ['relative_mae_reduction'] = float(1 - r['rf_mae'].mean() / r['base_mae'].mean())
summ['n_folds'] = int(len(r))
print(summ)
record_fact('q2_grouped_folds', r.round(4).to_dict(orient='records'), 'Per-fold RF and mean-baseline metrics, GroupKFold(5) by Country')
record_fact('q2_grouped_summary', summ, 'Mean and SD across country-held-out folds for RF and mean baseline; overlap count; relative MAE reduction vs ml_1 random split (test R2 0.967, MAE 1.05)')
fig, ax = plt.subplots(figsize=(8, 4.5))
xs = np.arange(len(r))
ax.bar(xs - 0.2, r['rf_mae'], 0.4, label='Random forest')
ax.bar(xs + 0.2, r['base_mae'], 0.4, label='Mean-prediction baseline')
ax.set_xticks(xs)
ax.set_xticklabels([f'Fold {i}' for i in r['fold']])
ax.set_xlabel('GroupKFold fold (held-out countries)')
ax.set_ylabel('Test MAE (years of life expectancy)')
ax.set_title('Test MAE per country-held-out fold: random forest vs mean baseline')
ax.legend()
save_chart(fig, 'q2_mae_by_fold', 'Test MAE per GroupKFold fold (countries held out): random forest vs mean-prediction baseline')

# %%
print(r.round(3).to_string())
print(summ)
ml1 = {'test_r2': 0.9671, 'test_mae': 1.0527, 'test_rmse': 1.6873, 'baseline_mae': 7.676658321262128, 'baseline_rmse': 9.308237114515464, 'baseline_r2': -0.0016633162021579828, 'n_test': 586}
ml1['relative_mae_reduction'] = float(1 - ml1['test_mae'] / ml1['baseline_mae'])
record_fact('q2_ml1_reference', ml1, 'ml_1 random 80/20 split reference: RF test R2 0.967, MAE 1.05, RMSE 1.69; mean baseline MAE 7.68, RMSE 9.31; relative MAE reduction')
print(ml1)
