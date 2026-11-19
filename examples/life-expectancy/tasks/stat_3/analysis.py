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
print(df.columns.tolist())
print(df['Status'].value_counts(dropna=False))
cols=['Life expectancy ','Schooling','Income composition of resources','HIV/AIDS']
c=[x for x in df.columns if x.strip() in ['Life expectancy','Schooling','Income composition of resources','HIV/AIDS','Status']]
print(c)
print(df[c].isna().sum())
print(df.groupby(df['Status'].str.strip())[c[:4]].count())

# %%
import scipy.stats as st
d=df.copy()
d.columns=[c.strip() for c in d.columns]
d['Status']=d['Status'].str.strip()
drv=['Schooling','Income composition of resources','HIV/AIDS']
def block(sub):
    res={}
    for v in drv:
        s=sub[['Life expectancy',v]].dropna()
        r,_=st.pearsonr(s[v],s['Life expectancy'])
        rho,_=st.spearmanr(s[v],s['Life expectancy'])
        res[v]=(len(s),r,rho)
    return res
groups={'pooled':d,'Developed':d[d.Status=='Developed'],'Developing':d[d.Status=='Developing']}
R={g:block(s) for g,s in groups.items()}
for g in R:
    for v in drv:
        n,r,rho=R[g][v]
        print(g,v,n,round(r,3),round(rho,3))
        key=(g+'_'+v).replace(' ','_').replace('/','_')+'_corr'
        record_fact(key,{'n':int(n),'pearson_r':float(r),'spearman_rho':float(rho)},'Correlation of '+v+' with Life expectancy, group '+g)
for v in drv:
    n1,r1,_=R['Developed'][v]
    n2,r2,_=R['Developing'][v]
    zs=(np.arctanh(r1)-np.arctanh(r2))/np.sqrt(1/(n1-3)+1/(n2-3))
    p=2*(1-st.norm.cdf(abs(zs)))
    print('fisher',v,round(zs,3),p)
    key=('fisher_dev_vs_ing_'+v).replace(' ','_').replace('/','_')
    record_fact(key,{'z':float(zs),'p_value':float(p)},'Fisher z test of Pearson r, Developed vs Developing, for '+v)
def boot(v,B=1000,seed=0):
    s=d[['Status','Life expectancy',v]].dropna()
    rng=np.random.default_rng(seed)
    x0=s[v].values; y0=s['Life expectancy'].values; g0=s.Status.values
    rp0=np.corrcoef(x0,y0)[0,1]
    out={}
    for g in ['Developed','Developing']:
        m=g0==g
        out[g]=[rp0-np.corrcoef(x0[m],y0[m])[0,1],[]]
    for _ in range(B):
        idx=rng.integers(0,len(s),len(s))
        x=x0[idx]; y=y0[idx]; gg=g0[idx]
        rp=np.corrcoef(x,y)[0,1]
        for g in out:
            m=gg==g
            out[g][1].append(rp-np.corrcoef(x[m],y[m])[0,1])
    return {g:(out[g][0],np.percentile(out[g][1],[2.5,97.5]).tolist()) for g in out}
for v in drv:
    bres=boot(v)
    for g in bres:
        est,ci=bres[g]
        print('boot',v,g,round(est,3),[round(c,3) for c in ci])
        key=('boot_pooled_minus_within_'+g+'_'+v).replace(' ','_').replace('/','_')
        record_fact(key,{'diff_pearson_pooled_minus_within':float(est),'ci_low':float(ci[0]),'ci_high':float(ci[1])},'Bootstrap difference of pooled minus within-'+g+' Pearson r for '+v)

# %%
import scipy.stats as st
print(d.loc[d.Status=='Developed','HIV/AIDS'].describe())
print('unique Developed HIV/AIDS values:', d.loc[d.Status=='Developed','HIV/AIDS'].nunique())
hv=d.loc[d.Status=='Developed',['Life expectancy','HIV/AIDS']].dropna()
record_fact('developed_hiv_unique_values',{'n':int(len(hv)),'n_unique':int(hv['HIV/AIDS'].nunique()),'min':float(hv['HIV/AIDS'].min()),'max':float(hv['HIV/AIDS'].max())},'HIV/AIDS values among Developed rows with Life expectancy present')
def fl(x):
    return None if (x is None or np.isnan(x)) else float(x)
def boot_s(v,B=500,seed=1):
    s=d[['Status','Life expectancy',v]].dropna()
    x0=s[v].values; y0=s['Life expectancy'].values; g0=s.Status.values
    rho0=st.spearmanr(x0,y0)[0]
    gs=['Developed','Developing']
    out={}
    for g in gs:
        m=g0==g
        out[g]=[rho0-st.spearmanr(x0[m],y0[m])[0],[]] if len(set(x0[m]))>1 else [np.nan,[]]
    rng=np.random.default_rng(seed)
    for _ in range(B):
        idx=rng.integers(0,len(s),len(s))
        x=x0[idx]; y=y0[idx]; gg=g0[idx]
        rp=st.spearmanr(x,y)[0]
        for g in gs:
            m=gg==g
            if len(set(x[m]))>1 and len(set(y[m]))>1:
                out[g][1].append(rp-st.spearmanr(x[m],y[m])[0])
    res={}
    for g in gs:
        arr=out[g][1]
        ci=np.percentile(arr,[2.5,97.5]).tolist() if len(arr)>0 else [np.nan,np.nan]
        res[g]=(out[g][0],ci,len(arr))
    return res
for v in ['Schooling','Income composition of resources','HIV/AIDS']:
    res=boot_s(v)
    for g in res:
        est,ci,nb=res[g]
        print('spearman boot',v,g,est,ci,nb)
        key=('boot_spearman_pooled_minus_within_'+g+'_'+v).replace(' ','_').replace('/','_')
        record_fact(key,{'diff_spearman_pooled_minus_within':fl(est),'ci_low':fl(ci[0]),'ci_high':fl(ci[1]),'n_valid_resamples':int(nb)},'Bootstrap difference of pooled minus within-'+g+' Spearman rho for '+v+' (500 resamples; resamples with constant group input skipped)')

# %%
fig,ax=plt.subplots(figsize=(9,5))
x=np.arange(len(drv)); w=0.25
for i,g in enumerate(['pooled','Developed','Developing']):
    vals=[float(R[g][v][1]) for v in drv]
    ax.bar(x+(i-1)*w, vals, w, label=g)
ax.set_xticks(x)
ax.set_xticklabels(['Schooling','Income composition\nof resources','HIV/AIDS'])
ax.set_ylabel('Pearson r with Life expectancy (correlation coefficient)')
ax.set_title('Pearson r with Life expectancy: pooled rows vs Developed rows vs Developing rows')
ax.axhline(0,color='grey',lw=0.8)
ax.legend(title='Rows used')
save_chart(fig,'within_group_pearson','Pearson correlation of each driver with Life expectancy, pooled and within each Status group. The Developed HIV/AIDS bar is absent because HIV/AIDS is constant (0.1) among Developed rows, so r is undefined.')
plt.close(fig)
