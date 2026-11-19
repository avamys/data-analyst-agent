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
print(d.shape)
print(d.dtypes.to_string())
missing = d.isna().sum()
print(missing.to_string())
print(d['churned'].value_counts(dropna=False).to_string())
print(d['plan'].value_counts(dropna=False).to_string())
print(d['refund_issued'].value_counts(dropna=False).to_string())
print(d[['usage_hours','tenure_months']].describe().round(2).to_string())
record_fact('missing_per_column', {c: int(v) for c, v in missing.items()}, 'Count of missing values per column')
record_fact('n_rows', int(d.shape[0]), 'Number of rows in dataset')

# %%
d = df.copy()
d['usage_bin'] = pd.qcut(d['usage_hours'], 5, labels=['Q1','Q2','Q3','Q4','Q5'], duplicates='drop')
d['tenure_bin'] = pd.qcut(d['tenure_months'], 5, labels=['Q1','Q2','Q3','Q4','Q5'], duplicates='drop')
publish('binned_frame', d)

overall = float(d['churned'].mean())
record_fact('overall_churn_rate', {'rate': overall, 'n': int(len(d))}, 'Overall churn rate and n')

def rate_table(col):
    t = d.groupby(col, observed=True)['churned'].agg(['mean','count']).rename(columns={'mean':'churn_rate','count':'n'})
    return t

plan_t = rate_table('plan')
usage_t = rate_table('usage_bin')
tenure_t = rate_table('tenure_bin')
refund_t = rate_table('refund_issued')
for name, t in [('plan', plan_t), ('usage_bin', usage_t), ('tenure_bin', tenure_t), ('refund_issued', refund_t)]:
    print(name)
    print(t.round(3).to_string())
    record_fact(f'churn_by_{name}', {str(k): {'churn_rate': round(float(v['churn_rate']),4), 'n': int(v['n'])} for k, v in t.iterrows()}, f'Churn rate and n by {name}')

means = d.groupby('churned')[['usage_hours','tenure_months']].mean().round(3)
print(means.to_string())
record_fact('mean_by_churn', {str(k): {'usage_hours': float(v['usage_hours']), 'tenure_months': float(v['tenure_months'])} for k, v in means.iterrows()}, 'Mean usage_hours and tenure_months per churned group')

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].bar(plan_t.index.astype(str), plan_t['churn_rate'])
axes[0].set_title('Churn rate by plan (share of customers churned)')
axes[0].set_xlabel('Plan')
axes[0].set_ylabel('Churn rate')
axes[1].bar(tenure_t.index.astype(str), tenure_t['churn_rate'])
axes[1].set_title('Churn rate by tenure quintile (share churned)')
axes[1].set_xlabel('Tenure months quintile')
axes[1].set_ylabel('Churn rate')
fig.tight_layout()
save_chart(fig, 'churn_rate_by_plan_and_tenure', 'Churn rate by plan (left) and by tenure quintile (right)')

fig2, ax2 = plt.subplots(figsize=(6,4))
ax2.bar(refund_t.index.astype(str), refund_t['churn_rate'])
ax2.set_title('Churn rate by refund_issued (0 vs 1)')
ax2.set_xlabel('refund_issued')
ax2.set_ylabel('Churn rate')
fig2.tight_layout()
save_chart(fig2, 'churn_rate_by_refund', 'Churn rate by refund_issued value (0 vs 1)')
