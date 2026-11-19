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
d = d[d['Age'].notna()].copy()
d['child'] = np.where(d['Age'] <= 12, 'child 0-12', 'older')
overall = d.groupby('child')['Survived'].agg(['mean', 'count'])
print(overall)
print(len(d))
print(d.groupby(['Pclass', 'child'])['Survived'].agg(['mean', 'count']))
print(d.groupby(['Sex', 'child'])['Survived'].agg(['mean', 'count']))
print(d.groupby(['Sex', 'Pclass', 'child'])['Survived'].agg(['mean', 'count']))

# %%
t1=d.groupby(['Pclass','child'])['Survived'].agg(['mean','count']); t2=d.groupby(['Sex','child'])['Survived'].agg(['mean','count']); rec_pclass={f'{a}|{b}':{'rate':round(float(v[0]),3),'n':int(v[1])} for (a,b),v in zip(t1.index,t1.values)}; rec_sex={f'{a}|{b}':{'rate':round(float(v[0]),3),'n':int(v[1])} for (a,b),v in zip(t2.index,t2.values)}; record_fact('child_by_pclass',rec_pclass,'Survival rate and n for child 0-12 vs older, by Pclass (Age known, n=714)'); record_fact('child_by_sex',rec_sex,'Survival rate and n for child 0-12 vs older, by Sex (Age known, n=714)'); record_fact('child_overall',{'child_rate':round(float(overall.loc['child 0-12','mean']),4),'child_n':int(overall.loc['child 0-12','count']),'older_rate':round(float(overall.loc['older','mean']),4),'older_n':int(overall.loc['older','count']),'base_rate':0.3838},'Child 0-12 survival rate vs older passengers and the 38.4% base rate (Age known, n=714)'); cr=[t1.loc[(p,'child 0-12'),'mean'] for p in [1,2,3]]+[t2.loc[(s,'child 0-12'),'mean'] for s in ['female','male']]; orr=[t1.loc[(p,'older'),'mean'] for p in [1,2,3]]+[t2.loc[(s,'older'),'mean'] for s in ['female','male']]; x=np.arange(5); fig,ax=plt.subplots(figsize=(8,4)); ax.bar(x-0.2,cr,0.4,label='child 0-12'); ax.bar(x+0.2,orr,0.4,label='older passengers'); ax.axhline(0.3838,color='red',ls='--',label='base rate 38.4%'); ax.set_xticks(x); ax.set_xticklabels(['Pclass 1','Pclass 2','Pclass 3','Female','Male']); ax.set_ylabel('Survival rate (share surviving)'); ax.set_title('Survival rate of children 0-12 vs older passengers, by Pclass and Sex (Age known, n=714)'); ax.legend(); save_chart(fig,'eda3_child_survival_by_group','Survival rate of children 0-12 vs older passengers within each Pclass and each Sex; dashed red line = base rate 38.4%')

# %%
t1=d.groupby(['Pclass','child'])['Survived'].agg(['mean','count'])
t3=d.groupby(['Sex','Pclass','child'])['Survived'].agg(['mean','count'])
print(t1)
print(t3)
rec_sp={f'{a}|{b}|{c}':{'rate':round(float(v[0]),3),'n':int(v[1])} for (a,b,c),v in zip(t3.index,t3.values)}
record_fact('child_by_sex_pclass',rec_sp,'Survival rate and n for child 0-12 vs older, by Sex and Pclass (Age known, n=714)')
record_fact('child_by_pclass_full',{f'{a}|{b}':{'rate':round(float(v[0]),3),'n':int(v[1])} for (a,b),v in zip(t1.index,t1.values)},'Survival rate and n for child 0-12 vs older by Pclass, all levels (Age known, n=714)')
