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
print(d.columns.tolist())
print(d['Status'].value_counts(dropna=False))
print(d[['Life expectancy','Schooling','Adult Mortality']].isna().sum())
print(d[['Life expectancy','Schooling','Adult Mortality']].describe().round(2))

# %%
from scipy import stats
d['Status'] = d['Status'].str.strip()
res = {}
for var in ['Life expectancy', 'Schooling', 'Adult Mortality']:
    s = d[[var, 'Status']].dropna()
    a = s.loc[s.Status == 'Developed', var]
    b = s.loc[s.Status == 'Developing', var]
    na, nb = len(a), len(b)
    ma, mb = a.mean(), b.mean()
    sa, sb = a.std(ddof=1), b.std(ddof=1)
    se_a, se_b = sa/np.sqrt(na), sb/np.sqrt(nb)
    tcrit_a = stats.t.ppf(0.975, na-1)
    tcrit_b = stats.t.ppf(0.975, nb-1)
    ci_a = (ma - tcrit_a*se_a, ma + tcrit_a*se_a)
    ci_b = (mb - tcrit_b*se_b, mb + tcrit_b*se_b)
    welch = stats.ttest_ind(a, b, equal_var=False)
    mw = stats.mannwhitneyu(a, b, alternative='two-sided')
    sp = np.sqrt(((na-1)*sa**2 + (nb-1)*sb**2)/(na+nb-2))
    d_val = (ma - mb)/sp
    se_d = np.sqrt((na+nb)/(na*nb) + d_val**2/(2*(na+nb)))
    d_ci = (d_val - 1.96*se_d, d_val + 1.96*se_d)
    diff = ma - mb
    se_diff = np.sqrt(se_a**2 + se_b**2)
    dfw = (se_a**2 + se_b**2)**2 / (se_a**4/(na-1) + se_b**4/(nb-1))
    tc = stats.t.ppf(0.975, dfw)
    diff_ci = (diff - tc*se_diff, diff + tc*se_diff)
    out = {'n_developed': na, 'n_developing': nb, 'mean_developed': ma, 'mean_developing': mb, 'ci_developed': list(ci_a), 'ci_developing': list(ci_b), 'mean_diff_dev_minus_ing': diff, 'diff_ci': list(diff_ci), 'welch_t': float(welch.statistic), 'welch_p': float(welch.pvalue), 'mannwhitney_p': float(mw.pvalue), 'cohens_d': d_val, 'cohens_d_ci': list(d_ci)}
    res[var] = out
    print(var, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in out.items() if not isinstance(v, list)})
    print('  CI dev', np.round(ci_a, 3), 'CI ing', np.round(ci_b, 3), 'diff CI', np.round(diff_ci, 3), 'd CI', np.round(d_ci, 3))
    record_fact('stat1_' + var.replace(' ', '_').lower(), out, 'Developed vs Developing comparison for ' + var + ': group means, 95% CIs, Welch t, Mann-Whitney p, Cohen d with CI')

# %%
fig, ax = plt.subplots(figsize=(7, 4))
g_dev = d.loc[d.Status == 'Developed', 'Life expectancy'].dropna()
g_ing = d.loc[d.Status == 'Developing', 'Life expectancy'].dropna()
ax.boxplot([g_dev, g_ing])
ax.set_xticks([1, 2])
ax.set_xticklabels(['Developed (n=%d)' % len(g_dev), 'Developing (n=%d)' % len(g_ing)])
ax.set_ylabel('Life expectancy (years)')
ax.set_xlabel('Status of country (rows per group in brackets)')
ax.set_title('Life expectancy (years) by Status: Developed vs Developing countries')
fig.tight_layout()
save_chart(fig, 'stat1_le_box_by_status', 'Box plot of Life expectancy in years for Developed and Developing country rows')
plt.close(fig)
print(len(g_dev), len(g_ing))

# %%
for var, o in res.items():
    print(var, 'welch_t', round(o['welch_t'], 3), 'welch_p', o['welch_p'], 'mw_p', o['mannwhitney_p'], 'd', round(o['cohens_d'], 3), 'd_ci', np.round(o['cohens_d_ci'], 3), 'diff', round(o['mean_diff_dev_minus_ing'], 3), 'diff_ci', np.round(o['diff_ci'], 3))
