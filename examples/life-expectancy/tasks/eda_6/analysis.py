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
cols = {c.strip(): c for c in df.columns}
lе = cols['Life expectancy']
am = cols['Adult Mortality']
st = cols['Status']
co = cols['Country']
print(df[st].value_counts(dropna=False))
print(df[[lе, am]].isna().sum())
print(df[am].describe())
print(df[co].nunique())

# %%
d=df[[co,st,lе,am]].dropna().copy()
d.columns=['c','s','le','am']
edges=[1.0,74.0,144.0,228.0,723.0]
d['band']=pd.cut(d['am'],bins=edges,include_lowest=True,labels=['b1','b2','b3','b4'])
res={}
for s in ['Developed','Developing']:
    g=d[d['s']==s]
    tab=g.groupby('band',observed=False)['le'].agg(['count','mean','median']).round(3)
    print(s)
    print(tab)
    top=g[g['band']=='b2']['c'].value_counts().head(10)
    print(top)
    res[s]={'edges':edges,'band_count':[int(x) for x in tab['count'].tolist()],'band_mean':[float(x) for x in tab['mean'].tolist()],'band_median':[float(x) for x in tab['median'].tolist()],'band2_top_countries':{str(k):int(v) for k,v in top.items()}}
    record_fact(s.lower()+'_am_bands',res[s],'Per-band n, mean and median Life expectancy by Adult Mortality band (fixed edges 1,74,144,228,723) within '+s+', plus top countries by row count in band b2 (74 to 144)')

# %%
import matplotlib.pyplot as plt
res2={}
fig,axes=plt.subplots(1,2,figsize=(10,4),sharey=True)
for ax,s in zip(axes,['Developed','Developing']):
    g=d[d['s']==s].copy()
    q=g['am'].quantile([0,.25,.5,.75,1]).tolist()
    g['qb']=pd.cut(g['am'],bins=q,include_lowest=True,labels=['q1','q2','q3','q4'])
    tab=g.groupby('qb',observed=False)['le'].agg(['count','mean','median']).round(3)
    top=g[g['qb']=='q2']['c'].value_counts().head(10)
    print(s); print(tab); print(top)
    res2[s]={'edges':[round(x,2) for x in q],'n':[int(x) for x in tab['count']],'mean':[float(x) for x in tab['mean']],'median':[float(x) for x in tab['median']],'q2_top':{str(k):int(v) for k,v in top.items()}}
    record_fact(s.lower()+'_am_quartile_bands',res2[s],'Quartile band edges, n, mean and median Life expectancy by Adult Mortality quartile band within '+s+'; q2 top countries by row count')
    ax.bar(tab.index.astype(str),tab['mean'])
    ax.set_title(s+': mean Life expectancy by Adult Mortality quartile band')
    ax.set_xlabel('Adult Mortality quartile band (q1 lowest to q4 highest)')
    ax.set_ylabel('Mean Life expectancy (years)')
plt.tight_layout()
save_chart(fig,'am_quartile_bands_by_status','Mean Life expectancy (years) per Adult Mortality quartile band, separately for Developed and Developing countries')

# %%
for s in ['Developed','Developing']: g=d[(d['s']==s)&(d['band']=='b2')]; vc=g['c'].value_counts(); print(s,len(g),g['c'].nunique()); print(vc.head(10)); record_fact(s.lower()+'_am_b2_countries',{'rows':int(len(g)),'countries':int(g['c'].nunique()),'top10':{str(k):int(v) for k,v in vc.head(10).items()}},'Countries with most rows in fixed Adult Mortality band 74 to 144 within '+s)
