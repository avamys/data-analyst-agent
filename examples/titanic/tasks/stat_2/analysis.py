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
d = df[['Survived','Pclass','Sex']].dropna().copy()
d['Pclass'] = d['Pclass'].astype(int)
d['female'] = (d['Sex'] == 'female').astype(int)
print(d['Sex'].value_counts().to_dict(), d['Pclass'].value_counts().sort_index().to_dict(), len(d))
g = d.groupby(['Pclass','Sex'])['Survived'].agg(['sum','count','mean'])
print(g.round(3))

# %%
import statsmodels.formula.api as smf
from scipy import stats
from statsmodels.stats.proportion import proportion_confint

full = smf.logit('Survived ~ C(Pclass) * C(Sex)', data=d).fit(disp=0)
red = smf.logit('Survived ~ C(Pclass) + C(Sex)', data=d).fit(disp=0)
lr = 2*(full.llf - red.llf)
df_lr = full.df_model - red.df_model
p_lr = stats.chi2.sf(lr, df_lr)
print(full.summary2().tables[1].round(4))
print('LR interaction', round(lr,3), df_lr, p_lr)

rows = {}
for c in [1,2,3]:
    s = d[d.Pclass==c]
    f = s[s.Sex=='female']; m = s[s.Sex=='male']
    rf, nf = f.Survived.mean(), len(f)
    rm, nm = m.Survived.mean(), len(m)
    diff = rf-rm
    se = np.sqrt(rf*(1-rf)/nf + rm*(1-rm)/nm)
    lo, hi = diff-1.96*se, diff+1.96*se
    rows[str(c)] = {'female_rate': round(rf,4), 'female_n': nf, 'male_rate': round(rm,4), 'male_n': nm, 'diff_female_minus_male': round(diff,4), 'ci': [round(lo,4), round(hi,4)]}
print(rows)

d2 = d.groupby(['Pclass','Sex'])['Survived'].agg(['sum','count']).reset_index()
record_fact('stat2_pclass_sex_rates', rows, 'Survival rate by Sex within each Pclass, with n, female-minus-male difference and Wald 95% CI')
record_fact('stat2_interaction_lr', {'lr_chi2': round(lr,4), 'dof': int(df_lr), 'p': p_lr}, 'Likelihood-ratio test of Pclass x Sex interaction in logistic regression')
record_fact('stat2_logit_interaction_coefs', {k: [round(v,4), round(full.pvalues[k],6)] for k,v in full.params.items()}, 'Logistic regression with Pclass*Sex interaction: coefficient and p-value per term')

fig, ax = plt.subplots(figsize=(7,4))
for sex, mk in [('female','o'),('male','s')]:
    sub = d.groupby(['Pclass','Sex'])['Survived'].mean().xs(sex, level='Sex')
    ax.plot(sub.index, sub.values, marker=mk, label=sex)
ax.set_xticks([1,2,3]); ax.set_xlabel('Pclass'); ax.set_ylabel('Survival rate (share surviving)'); ax.set_title('Survival rate by Pclass, separately for female and male passengers'); ax.legend(); ax.set_ylim(0,1)
save_chart(fig, 'stat2_survival_by_pclass_sex', 'Survival rate by Pclass for female and male passengers')
