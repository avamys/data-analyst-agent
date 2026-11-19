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
import statsmodels.formula.api as smf

d = df.copy()
d.columns = [c.strip().replace(' ', '_').replace('-', '_') for c in d.columns]
print(d.columns.tolist())
print(d['Status'].value_counts(dropna=False))
print('Countries:', d['Country'].nunique())
print(d[['Life_expectancy','Schooling','Adult_Mortality']].isna().sum())
print(d[['Life_expectancy','Schooling','Adult_Mortality']].dtypes)

# %%
res = {}
for y in ['Life_expectancy','Schooling','Adult_Mortality']:
    sub = d[['Country','Status',y]].dropna().copy()
    sub['dev'] = (sub['Status']=='Developed').astype(int)
    m = smf.ols(f'{y} ~ dev', data=sub).fit(cov_type='cluster', cov_kwds={'groups': pd.factorize(sub['Country'])[0]})
    ci = m.conf_int().loc['dev']
    res[y] = {'coef': float(m.params['dev']), 'ci_low': float(ci[0]), 'ci_high': float(ci[1]), 'p': float(m.pvalues['dev']), 'n_rows': int(len(sub)), 'n_clusters': int(sub['Country'].nunique())}
    print(y, res[y])
    record_fact(f'stat4_cluster_{y.lower()}', res[y], f'Cluster-robust (Country) OLS Developed vs Developing coefficient for {y}: coef, 95% CI, p, rows, clusters')

# %%
naive = {'life_expectancy': {'diff': 12.09, 'ci_low': 11.59, 'ci_high': 12.58, 'n_developed': 512, 'n_developing': 2416}, 'schooling': {'diff': 4.63, 'ci_low': 4.42, 'ci_high': 4.83, 'n_developed': 464, 'n_developing': 2311}, 'adult_mortality': {'diff': -103.15, 'ci_low': -109.73, 'ci_high': -96.57, 'n_developed': 512, 'n_developing': 2416}}
for k, v in naive.items():
    record_fact(f'stat1_{k}', v, f'Naive Welch 95% CI for Developed minus Developing {k} from stat_1')
cluster = {'life_expectancy': (10.322965660539639, 13.8498070008842), 'schooling': (3.8835050449614505, 5.3689317640031575), 'adult_mortality': (-121.7696966435683, -84.52560033490857)}
ratios = {}
for k in naive:
    cw = cluster[k][1] - cluster[k][0]
    nw = naive[k]['ci_high'] - naive[k]['ci_low']
    ratios[k] = {'cluster_width': cw, 'naive_width': nw, 'ratio': cw / nw}
    print(k, ratios[k])
record_fact('stat4_width_ratios', ratios, 'Cluster-robust CI width divided by naive stat_1 CI width, per outcome')
