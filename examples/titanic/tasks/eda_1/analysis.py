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
base = d['Survived'].mean()
record_fact('base_rate', round(base,4), 'Overall survival rate across all passengers with Survived recorded')
rows = []
for col in ['Sex','Pclass','Embarked','SibSp','Parch']:
    g = d.groupby(col)['Survived'].agg(['mean','count'])
    for lvl, r in g.iterrows():
        rows.append({'feature': col, 'level': str(lvl), 'survival_rate': round(float(r['mean']),4), 'n': int(r['count'])})
tab = pd.DataFrame(rows)
print(tab.to_string())
record_fact('survival_by_categorical_table', rows, 'Survival rate and group size for each level of Sex, Pclass, Embarked, SibSp, Parch')
d['AgeBin'] = pd.cut(d['Age'], bins=[0,12,18,35,60,100], labels=['0-12','13-18','19-35','36-60','61+'])
d['FareQ'] = pd.qcut(d['Fare'], 4, labels=['Q1 (lowest)','Q2','Q3','Q4 (highest)'])
age_tab = d.groupby('AgeBin', observed=True).agg(survival_rate=('Survived','mean'), n=('Survived','count'), mean_fare=('Fare','mean'), mean_age=('Age','mean')).round(3)
fare_tab = d.groupby('FareQ', observed=True).agg(survival_rate=('Survived','mean'), n=('Survived','count'), mean_fare=('Fare','mean'), mean_age=('Age','mean')).round(3)
print(age_tab.to_string())
print(fare_tab.to_string())
record_fact('survival_by_age_bin', {str(k): {'survival_rate': round(float(v['survival_rate']),4), 'n': int(v['n']), 'mean_fare': round(float(v['mean_fare']),2), 'mean_age': round(float(v['mean_age']),2)} for k, v in age_tab.iterrows()}, 'Survival rate, group size, mean Fare and mean Age by binned Age')
record_fact('survival_by_fare_quartile', {str(k): {'survival_rate': round(float(v['survival_rate']),4), 'n': int(v['n']), 'mean_fare': round(float(v['mean_fare']),2), 'mean_age': round(float(v['mean_age']),2)} for k, v in fare_tab.iterrows()}, 'Survival rate, group size, mean Fare and mean Age by Fare quartile')
record_fact('missing_age_count', int(d['Age'].isna().sum()), 'Passengers with missing Age, excluded from Age bins')
fig, axes = plt.subplots(2,3,figsize=(15,8))
panels = [('Sex', d.groupby('Sex')['Survived'].mean()), ('Pclass', d.groupby('Pclass')['Survived'].mean()), ('Embarked', d.groupby('Embarked')['Survived'].mean()), ('Age bin (years)', age_tab['survival_rate']), ('Fare quartile', fare_tab['survival_rate'])]
for ax, (name, s) in zip(axes.flat, panels):
    s = s.copy(); s.index = s.index.astype(str)
    s.plot(kind='bar', ax=ax, color='steelblue', rot=0)
    ax.axhline(base, color='red', ls='--')
    ax.set_title('Survival rate by ' + name)
    ax.set_ylabel('Survival rate (share of group surviving)')
    ax.set_xlabel(name)
axes.flat[-1].axis('off')
plt.tight_layout()
save_chart(fig, 'eda1_survival_by_groups', 'Survival rate (share surviving) by Sex, Pclass, Embarked, binned Age and Fare quartile; dashed red line = overall base rate 38.4%')
