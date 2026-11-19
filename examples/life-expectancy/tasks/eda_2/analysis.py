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
cols = {'LE':'Life expectancy ','AM':'Adult Mortality','SCH':'Schooling','BMI':' BMI ','ICR':'Income composition of resources','HIV':' HIV/AIDS','GDP':'GDP'}
print([repr(c) for c in df.columns])
print(df.dtypes.value_counts())
for k,c in cols.items():
    print(k, repr(c), c in df.columns, int(df[c].isna().sum()) if c in df.columns else None)
print(df.shape)

# %%
from scipy import stats
LE = 'Life expectancy '
drivers = [('am','Adult Mortality','Adult Mortality'),('sch','Schooling','Schooling'),('bmi','BMI',' BMI '),('icr','Income composition of resources','Income composition of resources'),('hiv','HIV/AIDS',' HIV/AIDS'),('gdp','GDP','GDP')]
for key, label, c in drivers:
    sub = df[[LE, c]].dropna()
    qs = sub[c].quantile([0, .25, .5, .75, 1.0]).values
    band = pd.qcut(sub[c], 4, labels=False, duplicates='drop')
    g = sub.groupby(band)[LE].agg(['count','mean','median'])
    edges = [float(x) for x in qs]
    r = stats.pearsonr(sub[c], sub[LE])[0]
    rho = stats.spearmanr(sub[c], sub[LE])[0]
    record_fact(f'{key}_quartiles', {'n': int(len(sub)), 'edges': edges, 'band_count': [int(x) for x in g['count']], 'band_mean': [round(float(x),3) for x in g['mean']], 'band_median': [float(x) for x in g['median']], 'pearson_r': float(r), 'spearman_rho': float(rho)}, f'{label}: quartile band edges, Life expectancy mean and median per band, Pearson and Spearman with Life expectancy')
    print(label, len(sub), [round(x,2) for x in qs])
    print(g.round(2))
    print('pearson', round(r,3), 'spearman', round(rho,3))
    fig, ax = plt.subplots(figsize=(6,4))
    ax.scatter(sub[c], sub[LE], s=6, alpha=0.4)
    ax.set_title(f'Life expectancy vs {label}, rows with both values')
    ax.set_xlabel(label)
    ax.set_ylabel('Life expectancy (years)')
    save_chart(fig, f'scatter_{key}', f'Scatter of Life expectancy (years) against {label}, one point per row')
    plt.close(fig)

# %%
import matplotlib.pyplot as plt
LE = 'Life expectancy '
drivers = [('am','Adult Mortality','Adult Mortality'),('sch','Schooling','Schooling'),('bmi','BMI',' BMI '),('icr','Income composition of resources','Income composition of resources'),('hiv','HIV/AIDS',' HIV/AIDS'),('gdp','GDP','GDP')]
for key, label, c in drivers:
    sub = df[[LE, c]].dropna()
    fig, ax = plt.subplots(figsize=(6,4))
    ax.scatter(sub[c], sub[LE], s=6, alpha=0.4)
    ax.set_title(f'Life expectancy vs {label}, rows with both values')
    ax.set_xlabel(label)
    ax.set_ylabel('Life expectancy (years)')
    save_chart(fig, f'scatter_{key}', f'Scatter of Life expectancy (years) against {label}, plotting only rows with both Life expectancy and {label} present, one point per row')
    plt.close(fig)
