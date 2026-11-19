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
miss = df[['Age','Cabin','Embarked']].isna().sum()
pct = (miss / len(df) * 100).round(2)
print(pd.DataFrame({'missing': miss, 'pct': pct}))
record_fact('missing_counts', {'Age': int(miss['Age']), 'Cabin': int(miss['Cabin']), 'Embarked': int(miss['Embarked'])}, 'Missing counts for Age, Cabin, Embarked')
record_fact('missing_pct', {'Age': float(pct['Age']), 'Cabin': float(pct['Cabin']), 'Embarked': float(pct['Embarked'])}, 'Missing percentages for Age, Cabin, Embarked')
print(df['Survived'].isna().sum(), df['Pclass'].isna().sum(), df['Sex'].isna().sum(), df['Fare'].isna().sum())

# %%
d = df.copy()
d['age_missing'] = d['Age'].isna()
d['cabin_missing'] = d['Cabin'].isna()
sr_age = d.groupby('age_missing')['Survived'].agg(['mean','count'])
sr_cab = d.groupby('cabin_missing')['Survived'].agg(['mean','count'])
print(sr_age)
print(sr_cab)
print(pd.crosstab(d['age_missing'], d['Pclass'], normalize='index').round(3))
print(pd.crosstab(d['age_missing'], d['Sex'], normalize='index').round(3))
print(d.loc[d['Embarked'].isna(), ['PassengerId','Pclass','Fare','Survived','Sex']])
record_fact('survival_by_age_missing', {'missing': float(sr_age.loc[True,'mean']), 'present': float(sr_age.loc[False,'mean']), 'n_missing': int(sr_age.loc[True,'count']), 'n_present': int(sr_age.loc[False,'count'])}, 'Survival rate for rows with Age missing vs present')
record_fact('survival_by_cabin_missing', {'missing': float(sr_cab.loc[True,'mean']), 'present': float(sr_cab.loc[False,'mean']), 'n_missing': int(sr_cab.loc[True,'count']), 'n_present': int(sr_cab.loc[False,'count'])}, 'Survival rate for rows with Cabin missing vs present')
pc_age = pd.crosstab(d['age_missing'], d['Pclass'], normalize='index')
sx_age = pd.crosstab(d['age_missing'], d['Sex'], normalize='index')
record_fact('age_missing_pclass_share', {'missing_pclass1': float(pc_age.loc[True,1]), 'missing_pclass2': float(pc_age.loc[True,2]), 'missing_pclass3': float(pc_age.loc[True,3]), 'complete_pclass1': float(pc_age.loc[False,1]), 'complete_pclass2': float(pc_age.loc[False,2]), 'complete_pclass3': float(pc_age.loc[False,3])}, 'Pclass share among Age-missing rows vs Age-complete rows')
record_fact('age_missing_sex_share', {'missing_female': float(sx_age.loc[True,'female']), 'missing_male': float(sx_age.loc[True,'male']), 'complete_female': float(sx_age.loc[False,'female']), 'complete_male': float(sx_age.loc[False,'male'])}, 'Sex share among Age-missing rows vs Age-complete rows')
eb = d[d['Embarked'].isna()]
record_fact('embarked_missing_rows', {'passenger_ids': [int(x) for x in eb['PassengerId']], 'fare': [float(x) for x in eb['Fare']], 'pclass': [int(x) for x in eb['Pclass']], 'survived': [int(x) for x in eb['Survived']]}, 'Rows with Embarked missing: Fare, Pclass, Survived')

# %%
fig, ax = plt.subplots(figsize=(7,4))
rates = [sr_age.loc[False,'mean'], sr_age.loc[True,'mean'], sr_cab.loc[False,'mean'], sr_cab.loc[True,'mean']]
labels = ['Age present','Age missing','Cabin present','Cabin missing']
ax.bar(labels, rates, color=['#4C72B0','#DD8452','#4C72B0','#DD8452'])
ax.set_title('Survival rate (share of passengers who survived) by Age and Cabin missingness')
ax.set_ylabel('Survival rate (proportion survived)')
for i,v in enumerate(rates):
    ax.text(i, v+0.01, f'{v:.2f}', ha='center')
save_chart(fig, 'survival_by_missingness', 'Survival rate for rows with Age or Cabin present vs missing')
plt.close(fig)
fare = d.groupby('age_missing')['Fare'].median()
record_fact('fare_median_by_age_missing', {'missing': float(fare.loc[True]), 'present': float(fare.loc[False])}, 'Median Fare for Age-missing vs Age-present rows')
print(fare)
