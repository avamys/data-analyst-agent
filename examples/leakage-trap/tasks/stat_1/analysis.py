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
print(d['churned'].value_counts())
print(d[['usage_hours','tenure_months']].describe().round(3))
print(pd.crosstab(d['refund_issued'], d['churned']))

# %%
from scipy import stats
from statsmodels.stats.multitest import multipletests

res = {}

# Chi-square for plan vs churned
ct_plan = pd.crosstab(d['plan'], d['churned'])
chi2_p, chi2_p_val, dof_p, _ = stats.chi2_contingency(ct_plan, correction=False)
n = ct_plan.values.sum()
v_plan = np.sqrt(chi2_p / (n * (min(ct_plan.shape) - 1)))
res['plan'] = {'chi2': float(chi2_p), 'dof': int(dof_p), 'p': float(chi2_p_val), 'cramers_v': float(v_plan)}

# Chi-square for refund_issued vs churned
ct_ref = pd.crosstab(d['refund_issued'], d['churned'])
chi2_r, p_r, dof_r, _ = stats.chi2_contingency(ct_ref, correction=False)
n_r = ct_ref.values.sum()
v_ref = np.sqrt(chi2_r / (n_r * (min(ct_ref.shape) - 1)))
res['refund_issued'] = {'chi2': float(chi2_r), 'dof': int(dof_r), 'p': float(p_r), 'cramers_v': float(v_ref)}

# Mann-Whitney for numeric vs churned, with rank-biserial and Cohen's d
for col in ['usage_hours', 'tenure_months']:
    a = d.loc[d['churned'] == 1, col]
    b = d.loc[d['churned'] == 0, col]
    u, p_u = stats.mannwhitneyu(a, b, alternative='two-sided')
    rbc = 1 - 2 * u / (len(a) * len(b))
    sp = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    dcoh = (a.mean() - b.mean()) / sp
    res[col] = {'U': float(u), 'p': float(p_u), 'rank_biserial': float(rbc), 'cohens_d': float(dcoh), 'mean_churned': float(a.mean()), 'mean_retained': float(b.mean())}

# 95% CI for churn rate difference by refund_issued (1 minus 0), Wald
g1 = d.loc[d['refund_issued'] == 1, 'churned']
g0 = d.loc[d['refund_issued'] == 0, 'churned']
p1, p0 = g1.mean(), g0.mean()
se = np.sqrt(p1 * (1 - p1) / len(g1) + p0 * (1 - p0) / len(g0))
diff = p1 - p0
ci = (diff - 1.96 * se, diff + 1.96 * se)
res['refund_ci'] = {'rate_refund1': float(p1), 'rate_refund0': float(p0), 'diff': float(diff), 'ci_low': float(ci[0]), 'ci_high': float(ci[1])}

# Holm correction across the four p-values
pvals = [res['plan']['p'], res['refund_issued']['p'], res['usage_hours']['p'], res['tenure_months']['p']]
rej, p_adj, _, _ = multipletests(pvals, method='holm')
names = ['plan', 'refund_issued', 'usage_hours', 'tenure_months']
for nm, pa, rj in zip(names, p_adj, rej):
    res[nm]['p_holm'] = float(pa)
    res[nm]['significant_after_holm'] = bool(rj)

for k, v in res.items():
    print(k, {kk: (round(vv, 6) if isinstance(vv, float) else vv) for kk, vv in v.items()})

record_fact('stat1_plan_chi2', res['plan'], 'Chi-square plan vs churned with Cramer V and Holm-adjusted p')
record_fact('stat1_refund_chi2', res['refund_issued'], 'Chi-square refund_issued vs churned with Cramer V and Holm-adjusted p')
record_fact('stat1_usage_mwu', res['usage_hours'], 'Mann-Whitney usage_hours churned vs retained with rank-biserial, Cohen d, Holm p')
record_fact('stat1_tenure_mwu', res['tenure_months'], 'Mann-Whitney tenure_months churned vs retained with rank-biserial, Cohen d, Holm p')
record_fact('stat1_refund_diff_ci', res['refund_ci'], 'Churn rate difference refund_issued=1 minus 0 with 95% Wald CI')

# %%
import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
r = d.groupby('plan')['churned'].mean()
axes[0].bar(r.index.astype(str), r.values, color='steelblue')
axes[0].set_title('Churn rate by plan (share of customers churned)')
axes[0].set_xlabel('plan')
axes[0].set_ylabel('churn rate (share churned)')
r2 = d.groupby('refund_issued')['churned'].mean()
axes[1].bar(['refund_issued=0', 'refund_issued=1'], r2.values, color='indianred')
axes[1].set_title('Churn rate by refund_issued value (share churned)')
axes[1].set_xlabel('refund_issued')
axes[1].set_ylabel('churn rate (share churned)')
fig.tight_layout()
save_chart(fig, 'stat1_churn_rate_plan_refund', 'Churn rate by plan (left) and by refund_issued value (right)')
plt.close(fig)

# %%
print('usage_hours p_holm:', repr(res['usage_hours']['p_holm']))
print('tenure_months p_holm:', repr(res['tenure_months']['p_holm']))
print('usage_hours p:', repr(res['usage_hours']['p']))
print('tenure_months p:', repr(res['tenure_months']['p']))
