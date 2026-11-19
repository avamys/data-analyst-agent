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
d.columns = [c.strip() for c in d.columns]
print(d.dtypes.to_string())
miss = d.isna().sum()
pct = (miss / len(d) * 100).round(2)
print(pd.DataFrame({'missing': miss, 'pct': pct}).to_string())
print(d['Status'].value_counts(dropna=False).to_string())
print(d['Year'].min(), d['Year'].max(), d['Year'].nunique())

# %%
import scipy.stats as st
cols = ['Hepatitis B', 'Population', 'GDP', 'Alcohol', 'Total expenditure']
le = d['Life expectancy']
m = d[cols].isna()
bs = (m.groupby(d['Status']).mean() * 100).round(2)
by = (m.groupby(d['Year']).mean() * 100).round(1)
print(bs.to_string())
print(by.to_string())
res = {}
for c in cols:
    ok = le.notna()
    a = le[ok & d[c].isna()]
    b = le[ok & d[c].notna()]
    t = st.ttest_ind(a, b, equal_var=False)
    res[c] = {'n_missing_with_le': int(len(a)), 'mean_le_missing': round(float(a.mean()), 2), 'mean_le_present': round(float(b.mean()), 2), 't': round(float(t.statistic), 3), 'p': float(t.pvalue)}
print(pd.DataFrame(res).T.to_string())
record_fact('eda3_missing_pct', {c: float(pct[c]) for c in d.columns}, 'Percent missing per column, all 22 columns')
record_fact('eda3_missing_by_status', bs.to_dict(), 'Percent missing for focus columns per Status group')
record_fact('eda3_missing_by_year', by.rename(index=str).to_dict(), 'Percent missing for focus columns per Year')
record_fact('eda3_le_by_missing', res, 'Mean Life expectancy for rows with vs without each focus value, Welch t-test')

# %%
import scipy.stats as st
d15 = d[d['Year'] < 2015]
res15 = {}
for c in ['Alcohol', 'Total expenditure']:
    miss_all = d[c].isna()
    share2015 = float((miss_all & (d['Year'] == 2015)).sum() / miss_all.sum() * 100)
    ok = d15['Life expectancy'].notna()
    a = d15.loc[ok & d15[c].isna(), 'Life expectancy']
    b = d15.loc[ok & d15[c].notna(), 'Life expectancy']
    t = st.ttest_ind(a, b, equal_var=False)
    res15[c] = {'share_missing_in_2015_pct': round(share2015, 2), 'n_missing_pre2015_with_le': int(len(a)), 'mean_le_missing_pre2015': round(float(a.mean()), 2), 'mean_le_present_pre2015': round(float(b.mean()), 2), 't': round(float(t.statistic), 3), 'p': float(t.pvalue)}
print(pd.DataFrame(res15).T.to_string())
record_fact('eda3_le_by_missing_excl_2015', res15, 'Alcohol and Total expenditure Life expectancy comparison excluding 2015, Welch t-test')
fig, ax = plt.subplots(figsize=(8, 4))
for c in cols:
    ax.plot(by.index, by[c], marker='o', label=c)
ax.set_title('Percent of rows missing per Year, focus columns')
ax.set_xlabel('Year')
ax.set_ylabel('Rows missing (%)')
ax.legend(fontsize=8)
plt.tight_layout()
save_chart(fig, 'eda3_missing_by_year', 'Percent of rows missing per Year for Hepatitis B, Population, GDP, Alcohol and Total expenditure')

# %%
le = d['Life expectancy']
ok = le.notna()
te = d['Total expenditure']
pres = ok & te.notna()
pre = d['Year'] < 2015
v = {'te_present_mean_all': round(float(le[pres].mean()), 2), 'te_present_n': int(pres.sum()), 'te_missing_mean_all': round(float(le[ok & te.isna()].mean()), 2), 'te_missing_n': int((ok & te.isna()).sum()), 'te_present_mean_pre2015': round(float(le[pres & pre].mean()), 2), 'full_le_mean': round(float(le[ok].mean()), 2), 'te_nonmissing_rows': int(te.notna().sum())}
print(v)
record_fact('eda3_te_check', v, 'Total expenditure present-row Life expectancy mean check, all rows and pre-2015, with full-sample mean')
print(bs.to_string())
print(by[['Population', 'GDP', 'Total expenditure', 'Alcohol']].to_string())
print(pd.DataFrame(res).T.to_string())
print(te.describe().round(3).to_string())

# %%
import statsmodels.formula.api as smf
le = d['Life expectancy']
ok = le.notna()
te = d['Total expenditure']
pres = ok & te.notna()
y15 = d['Year'] == 2015
n_pre_pres = int((pres & ~y15).sum())
n_15_pres = int((pres & y15).sum())
ver = {'te_present_2015_n': n_15_pres, 'te_present_2015_mean': round(float(le[pres & y15].mean()), 2) if n_15_pres > 0 else None, 'te_present_pre2015_n': n_pre_pres, 'te_present_pre2015_mean': round(float(le[pres & ~y15].mean()), 2), 'te_present_all_n': int(pres.sum()), 'te_present_all_mean': round(float(le[pres].mean()), 2), 'te_missing_2015_with_le_n': int((ok & te.isna() & y15).sum())}
print(ver)
record_fact('eda3_te_verify', ver, 'Total expenditure present-row Life expectancy means split by 2015 and pre-2015, with counts')
dd = d[ok].copy()
dd['hepB_miss'] = dd['Hepatitis B'].isna().astype(int)
m = smf.ols('Q("Life expectancy") ~ hepB_miss + C(Status) + Year', data=dd).fit()
reg = {'hepB_miss_coef': round(float(m.params['hepB_miss']), 3), 'hepB_miss_p': float(m.pvalues['hepB_miss']), 'hepB_miss_ci_low': round(float(m.conf_int().loc['hepB_miss', 0]), 3), 'hepB_miss_ci_high': round(float(m.conf_int().loc['hepB_miss', 1]), 3), 'n': int(m.nobs), 'r2': round(float(m.rsquared), 3)}
print(reg)
record_fact('eda3_hepB_adjusted', reg, 'OLS of Life expectancy on Hepatitis B missing indicator, controlling for Status and Year')

# %%
print(pd.DataFrame(res).T.to_string())
print(bs.to_string())
print(by[['Population', 'GDP', 'Total expenditure', 'Alcohol']].to_string())

# %%
expected = {'Population': 22.2, 'GDP': 15.2, 'Total expenditure': 7.7, 'Income composition of resources': 5.7, 'Schooling': 5.5, 'Polio': 0.6, 'Diphtheria': 0.6, 'BMI': 1.2, 'thinness 1-19 years': 1.2, 'thinness 5-9 years': 1.2}
for c, v in expected.items():
    print(repr(c), pct.get(c), v)
print(pct[pct > 0].sort_values(ascending=False).to_string())
print(int((pct == 0).sum()), 'columns with 0 percent missing')
print(list(pct.index))
