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
print(d.dtypes)
print(d['plan'].value_counts())
print(d['refund_issued'].value_counts())
print(d[['usage_hours','tenure_months','churned']].describe().round(3))
print(pd.crosstab(d['plan'], d['refund_issued']))

# %%
import statsmodels.formula.api as smf
d = df.copy()
d['tenure_c'] = (d['tenure_months'] - d['tenure_months'].mean())/d['tenure_months'].std()
d['usage_c'] = (d['usage_hours'] - d['usage_hours'].mean())/d['usage_hours'].std()
d['plan'] = pd.Categorical(d['plan'], categories=['basic','plus','pro'])
f = 'churned ~ C(plan) * tenure_c + C(plan) * usage_c + refund_issued * tenure_c'
m = smf.logit(f, data=d).fit(disp=0)
ci = m.conf_int()
tab = pd.DataFrame({'coef': m.params, 'p': m.pvalues, 'lo': ci[0], 'hi': ci[1]}).round(4)
print(tab)
inter = [k for k in tab.index if ':' in k]
print(tab.loc[inter])
record_fact('stat2_interaction_terms', {k: {'coef': float(tab.loc[k,'coef']), 'p': float(tab.loc[k,'p']), 'ci_low': float(tab.loc[k,'lo']), 'ci_high': float(tab.loc[k,'hi'])} for k in inter}, 'Logit interaction coefficients (standardized tenure/usage; basic plan and refund=0 as reference), with p-values and 95% CIs')
d['tenure_bin'] = pd.qcut(d['tenure_months'], 4, labels=['T1','T2','T3','T4'])
rates = d.pivot_table(index='tenure_bin', columns='plan', values='churned', aggfunc='mean', observed=False).round(3)
ns = d.pivot_table(index='tenure_bin', columns='plan', values='churned', aggfunc='size', observed=False)
print(rates)
print(ns)
record_fact('stat2_churn_by_plan_tenure_bin', {str(k): {str(c): float(rates.loc[k,c]) for c in rates.columns} for k in rates.index}, 'Churn rate by plan within tenure quartile bins')
fig, ax = plt.subplots(figsize=(7,4))
for p in rates.columns:
    ax.plot(rates.index.astype(str), rates[p], marker='o', label=p)
ax.set_title('Churn rate by plan within tenure quartiles')
ax.set_xlabel('Tenure quartile (T1 lowest to T4 highest)')
ax.set_ylabel('Churn rate (share churned)')
ax.legend(title='plan')
save_chart(fig, 'stat2_churn_by_plan_tenure', 'Churn rate by plan within tenure quartiles')

# %%
r = d.groupby('refund_issued')['churned'].agg(['mean','size'])
print(r)
record_fact('stat2_churn_by_refund', {str(k): {'churn_rate': float(r.loc[k,'mean']), 'n': int(r.loc[k,'size'])} for k in r.index}, 'Churn rate and n by refund_issued, recomputed in this task')
record_fact('stat2_overall_churn_rate', {'rate': float(df['churned'].mean()), 'n': int(len(df))}, 'Overall churn rate and n, recomputed in this task')

# %%
import statsmodels.formula.api as smf
d = df.copy()
d['tenure_c'] = (d['tenure_months'] - d['tenure_months'].mean())/d['tenure_months'].std()
d['usage_c'] = (d['usage_hours'] - d['usage_hours'].mean())/d['usage_hours'].std()
d['plan'] = pd.Categorical(d['plan'], categories=['basic','plus','pro'])
m = smf.logit('churned ~ C(plan)*tenure_c + C(plan)*usage_c + refund_issued*tenure_c', data=d).fit(disp=0)
ci = m.conf_int()
tab = pd.DataFrame({'coef': m.params, 'p': m.pvalues, 'lo': ci[0], 'hi': ci[1]}).round(4)
inter = [k for k in tab.index if ':' in k]
print(tab.loc[inter].to_string())
record_fact('stat2_interaction_terms_full', {k: {'coef': float(tab.loc[k,'coef']), 'p': float(tab.loc[k,'p']), 'ci_low': float(tab.loc[k,'lo']), 'ci_high': float(tab.loc[k,'hi'])} for k in inter}, 'All interaction terms from the logit with plan x tenure_c, plan x usage_c, refund_issued x tenure_c (standardized; basic plan and refund=0 reference), with p-values and 95% CIs')
d['tenure_bin'] = pd.qcut(d['tenure_months'], 4, labels=['T1','T2','T3','T4'])
rates = d.pivot_table(index='tenure_bin', columns='plan', values='churned', aggfunc='mean', observed=False).round(3)
ns = d.pivot_table(index='tenure_bin', columns='plan', values='churned', aggfunc='size', observed=False)
print(rates.to_string())
print(ns.to_string())
record_fact('stat2_churn_by_plan_tenure_bin_full', {str(k): {str(c): {'rate': float(rates.loc[k,c]), 'n': int(ns.loc[k,c])} for c in rates.columns} for k in rates.index}, 'Churn rate and n by plan within tenure quartiles, all four tiers including pro')
