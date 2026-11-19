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
d['age_missing'] = d['Age'].isna()
d['cabin_missing'] = d['Cabin'].isna()
rows = []
groups = [('All', d)] + [(f'Pclass={p}', d[d['Pclass']==p]) for p in [1,2,3]] + [(f'Sex={s}', d[d['Sex']==s]) for s in ['male','female']]
for gname, g in groups:
    for var in ['age_missing','cabin_missing']:
        for flag in [True, False]:
            sub = g[g[var]==flag]
            n = len(sub)
            rate = float(sub['Survived'].mean()) if n>0 else None
            rows.append({'group':gname,'var':var,'missing':flag,'n':n,'surv':rate})
res = pd.DataFrame(rows)
print(res.to_string())
record_fact('eda4_survival_table', res.to_dict(orient='records'), 'Survival rate and n by group, Age/Cabin missing vs present, overall, by Pclass and by Sex')

# %%
from scipy import stats
rows2=[]
for gname, g in groups:
    for var in ['age_missing','cabin_missing']:
        ct=pd.crosstab(g[var], g['Survived'])
        if ct.shape==(2,2):
            p=float(stats.fisher_exact(ct.values)[1])
        else:
            p=None
        rows2.append({'group':gname,'var':var,'p_fisher':p})
pt=pd.DataFrame(rows2)
print(pt.to_string())
record_fact('eda4_fisher_p', pt.to_dict(orient='records'), 'Fisher exact p-values for survival by missingness within each group')
fig,ax=plt.subplots(figsize=(8,4))
sub=res[res['group'].str.startswith('Pclass')|res['group'].str.startswith('Sex')]
labels=[g+' '+('missing' if m else 'present') for g,m in zip(sub['group'],sub['missing'])]
ax.bar(range(len(sub)),sub['surv'])
ax.set_xticks(range(len(sub)))
ax.set_xticklabels(labels,rotation=90,fontsize=6)
ax.set_ylabel('Survival rate (proportion surviving)')
ax.set_title('Survival rate by Age/Cabin missingness within Pclass and Sex')
fig.tight_layout()
save_chart(fig,'eda4_within_group_survival','Survival rate within Pclass and Sex by Age-missing and Cabin-missing status')

# %%
tab = pd.DataFrame(res)
tab['surv']=tab['surv'].round(3)
print(tab.to_string())

# %%
print(pt.to_string())
print(pt[pt['var']=='age_missing'].to_string())

# %%
brief = res[res['group']!='All'].copy()
brief['surv'] = brief['surv'].astype(float).round(3)
print(brief.to_string())
record_fact('eda4_brief_table', brief.to_dict(orient='records'), 'Brief table: survival rate and n by Pclass and Sex for Age-missing and Cabin-missing vs present')

# %%
print(pt.to_string()); print(pt[pt['var']=='age_missing'].to_string()); print(pt[pt['var']=='cabin_missing'].to_string())
