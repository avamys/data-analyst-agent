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
cols = list(df.columns)
print(cols)
print(df['Status'].value_counts(dropna=False))
print(df[[c for c in cols if c.strip() in ['Life expectancy','Schooling','Adult Mortality']]].isna().sum())
print(df.dtypes.value_counts())

# %%
import statsmodels.formula.api as smf
d = df.rename(columns=lambda c: c.strip())
d = d[['Life expectancy','Adult Mortality','Schooling','Status']].dropna().copy()
d['Status'] = d['Status'].astype(str)
d['Status'] = pd.Categorical(d['Status'], categories=['Developing','Developed'])
d = d.rename(columns={'Life expectancy':'LE','Adult Mortality':'AM'})
print(len(d))
m = smf.ols('LE ~ Schooling * C(Status) + AM * C(Status)', data=d).fit()
ci = m.conf_int()
out = pd.DataFrame({'coef': m.params, 'ci_low': ci[0], 'ci_high': ci[1], 'p': m.pvalues})
print(out.round(4))
print('R2', round(m.rsquared,4), 'n', int(m.nobs))
record_fact('ols_coefs', {k: float(v) for k, v in m.params.items()}, 'OLS coefficients of LE on Schooling, Adult Mortality, Status (Developed vs Developing reference) and interactions')
record_fact('ols_ci', {k: [float(ci.loc[k,0]), float(ci.loc[k,1])] for k in m.params.index}, '95% CIs of OLS coefficients')
record_fact('ols_pvalues', {k: float(v) for k, v in m.pvalues.items()}, 'p-values of OLS coefficients')
record_fact('ols_r2', {'r2': float(m.rsquared), 'n': int(m.nobs)}, 'OLS model fit: R squared and sample size')
# interaction joint test
names = [k for k in m.params.index if ':' in k]
wald = m.wald_test(' , '.join(f'{k} = 0' for k in names), scalar=True)
record_fact('interaction_joint_test', {'f': float(wald.statistic), 'p': float(wald.pvalue), 'terms': names}, 'Joint Wald F test that all Status interaction terms are zero')
print('joint interaction F', float(wald.statistic), float(wald.pvalue))
# within-group slopes
for s in ['Developing','Developed']:
    g = d[d['Status']==s]
    mg = smf.ols('LE ~ Schooling + AM', data=g).fit()
    gci = mg.conf_int()
    print(s, len(g), mg.params.round(4).to_dict(), mg.pvalues.round(4).to_dict())
    record_fact('slopes_'+s.lower(), {'n': int(len(g)), 'schooling_slope': float(mg.params['Schooling']), 'schooling_ci': [float(gci.loc['Schooling',0]), float(gci.loc['Schooling',1])], 'schooling_p': float(mg.pvalues['Schooling']), 'adult_mortality_slope': float(mg.params['AM']), 'adult_mortality_ci': [float(gci.loc['AM',0]), float(gci.loc['AM',1])], 'adult_mortality_p': float(mg.pvalues['AM'])}, f'Within-group OLS slopes of LE on Schooling and Adult Mortality for {s} countries')

# %%
fig, ax = plt.subplots(figsize=(7, 4.5))
for s, colr in [('Developing', 'tab:blue'), ('Developed', 'tab:orange')]:
    g = d[d['Status'] == s]
    ax.scatter(g['Schooling'], g['LE'], s=8, alpha=0.4, color=colr, label=f'{s} (n={len(g)})')
    b = np.polyfit(g['Schooling'], g['LE'], 1)
    xs = np.linspace(g['Schooling'].min(), g['Schooling'].max(), 50)
    ax.plot(xs, b[0] * xs + b[1], color=colr, lw=2)
ax.set_xlabel('Schooling (years of schooling per country-year)')
ax.set_ylabel('Life expectancy (years)')
ax.set_title('Life expectancy vs Schooling by country Status: points are country-years, lines are within-group linear fits')
ax.legend()
save_chart(fig, 'le_vs_schooling_by_status', 'Life expectancy against Schooling for Developing and Developed countries, with a separate linear fit for each Status group')
plt.close(fig)

# %%
terms = ['Schooling:C(Status)[T.Developed]', 'AM:C(Status)[T.Developed]']
rows = {k: {'coef': float(m.params[k]), 'ci': [float(ci.loc[k, 0]), float(ci.loc[k, 1])], 'p': float(m.pvalues[k])} for k in terms}
record_fact('interaction_terms_detail', rows, 'Coefficient, 95% CI and p-value of the Schooling x Developed and Adult Mortality x Developed interaction terms')
print(rows)
