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
print(d[['Survived','Pclass','Sex','Age','SibSp','Parch','Fare','Embarked']].dtypes)
print(d[['Survived','Pclass','Sex','Age','SibSp','Parch','Fare','Embarked']].isna().sum())
print(d['Survived'].value_counts())
print(d['Embarked'].value_counts(dropna=False))

# %%
from scipy import stats
from statsmodels.stats.multitest import multipletests
d = df.copy()
d['Survived'] = d['Survived'].astype(int)
res = {}
def cramers_v(tab):
    chi2, p, dof, _ = stats.chi2_contingency(tab, correction=False)
    n = tab.values.sum()
    k = min(tab.shape) - 1
    return chi2, p, dof, np.sqrt(chi2 / (n * k))
def wilson(k, n, z=1.96):
    p = k / n
    den = 1 + z**2 / n
    c = (p + z**2 / (2*n)) / den
    h = z * np.sqrt(p*(1-p)/n + z**2/(4*n**2)) / den
    return c - h, c + h
cat_feats = ['Sex', 'Pclass', 'Embarked', 'SibSp', 'Parch']
for f in cat_feats:
    sub = d.dropna(subset=[f])
    tab = pd.crosstab(sub[f], sub['Survived'])
    chi2, p, dof, v = cramers_v(tab)
    rates = sub.groupby(f)['Survived'].agg(['mean', 'count'])
    rate_d = {str(k): {'rate': round(float(r['mean']), 4), 'n': int(r['count'])} for k, r in rates.iterrows()}
    res[f] = {'test': 'chi2', 'stat': float(chi2), 'p': float(p), 'dof': int(dof), 'effect': float(v), 'effect_name': 'cramers_v', 'rates': rate_d}
for f in ['Age', 'Fare']:
    sub = d.dropna(subset=[f])
    a = sub.loc[sub['Survived'] == 1, f]
    b = sub.loc[sub['Survived'] == 0, f]
    u, p = stats.mannwhitneyu(a, b, alternative='two-sided')
    rbc = 2 * u / (len(a) * len(b)) - 1
    # bootstrap CI for rank-biserial
    rng = np.random.default_rng(0)
    bs = []
    av, bv = a.values, b.values
    for _ in range(1000):
        aa = rng.choice(av, len(av)); bb = rng.choice(bv, len(bv))
        uu = stats.mannwhitneyu(aa, bb, alternative='two-sided').statistic
        bs.append(2 * uu / (len(aa) * len(bb)) - 1)
    lo, hi = np.percentile(bs, [2.5, 97.5])
    res[f] = {'test': 'mannwhitney', 'stat': float(u), 'p': float(p), 'effect': float(rbc), 'effect_name': 'rank_biserial', 'ci': [float(lo), float(hi)], 'n': int(len(sub)), 'median_survived': float(a.median()), 'median_died': float(b.median())}
ps = [res[f]['p'] for f in res]
reject, padj, _, _ = multipletests(ps, method='holm')
for f, pa, rj in zip(res, padj, reject):
    res[f]['p_holm'] = float(pa)
    res[f]['significant_holm'] = bool(rj)
    print(f, round(res[f]['p'], 6), round(pa, 6), rj, round(res[f]['effect'], 3))
for f in cat_feats:
    print(f, res[f]['rates'])
for f in ['Age','Fare']:
    print(f, {k: res[f][k] for k in ['effect','ci','median_survived','median_died','n']})
    record_fact(f'stat1_{f.lower()}_test', res[f], f'Mann-Whitney test for {f} vs Survived with rank-biserial effect, bootstrap 95% CI, Holm-adjusted p across 7 features')
for f in cat_feats:
    record_fact(f'stat1_{f.lower()}_test', res[f], f'Chi-square test for {f} vs Survived with Cramers V, group survival rates, Holm-adjusted p across 7 features')

# %%
rng = np.random.default_rng(1)
ci_out = {}
for f in cat_feats:
    sub = d.dropna(subset=[f])[[f, 'Survived']].reset_index(drop=True)
    vs = []
    for _ in range(1000):
        s = sub.iloc[rng.integers(0, len(sub), len(sub))]
        tab = pd.crosstab(s[f], s['Survived'])
        if tab.shape[0] < 2 or tab.shape[1] < 2:
            continue
        vs.append(cramers_v(tab)[3])
    lo, hi = np.percentile(vs, [2.5, 97.5])
    ci_out[f] = [float(lo), float(hi)]
    record_fact(f'stat1_{f.lower()}_cramers_v_ci', {'effect': res[f]['effect'], 'ci': [float(lo), float(hi)]}, f'Bootstrap 95% CI for Cramers V of {f} vs Survived')
    print(f, round(res[f]['effect'], 3), round(lo, 3), round(hi, 3))

fig, axes = plt.subplots(1, 3, figsize=(12, 4))
for ax, f in zip(axes, ['Sex', 'Pclass', 'Embarked']):
    r = d.dropna(subset=[f]).groupby(f)['Survived'].agg(['mean', 'count'])
    ax.bar(r.index.astype(str), r['mean'], color='steelblue')
    ax.axhline(d['Survived'].mean(), ls='--', color='red')
    ax.set_title(f'Survival rate by {f} (share surviving)')
    ax.set_xlabel(f)
    ax.set_ylabel('Survival rate (share surviving)')
    ax.set_ylim(0, 1)
    for i, (m, n) in enumerate(zip(r['mean'], r['count'])):
        ax.text(i, m + 0.02, f'n={n}', ha='center')
plt.tight_layout()
save_chart(fig, 'stat1_survival_rates_categorical', 'Survival rate (share surviving) by Sex, Pclass and Embarked; dashed red line = overall base rate 38.4%')

# %%
from scipy.stats import chi2_contingency
d2 = df.copy(); d2['Survived'] = d2['Survived'].astype(int)
q = pd.qcut(d2['Fare'], 4, labels=['Q1 (lowest)', 'Q2', 'Q3', 'Q4 (highest)'])
fq = d2.groupby(q, observed=True)['Survived'].agg(['mean', 'count'])
fare_rates = {str(k): {'rate': round(float(r['mean']), 4), 'n': int(r['count'])} for k, r in fq.iterrows()}
record_fact('stat1_fare_quartile_rates', fare_rates, 'Descriptive survival rate and n by Fare quartile (pd.qcut); descriptive only, not produced by the Mann-Whitney test')
print(fare_rates)
ages = d2.dropna(subset=['Age']).copy()
ages['ab'] = pd.cut(ages['Age'], bins=[-1, 12, 18, 35, 60, 200], labels=['0-12', '13-18', '19-35', '36-60', '61+'])
ar = ages.groupby('ab', observed=True)['Survived'].agg(['mean', 'count'])
age_rates = {str(k): {'rate': round(float(r['mean']), 4), 'n': int(r['count'])} for k, r in ar.iterrows()}
record_fact('stat1_age_bin_rates', age_rates, 'Descriptive survival rate and n by Age band, passengers with Age recorded; Age-missing excluded from bins and from the Mann-Whitney test')
print(age_rates)
record_fact('stat1_age_missing_count', int(d2['Age'].isna().sum()), 'Passengers with missing Age, excluded from the Mann-Whitney test and the Age bands')
for f in ['SibSp', 'Parch']:
    tab = pd.crosstab(d2[f], d2['Survived'])
    _, _, _, exp = chi2_contingency(tab, correction=False)
    record_fact(f'stat1_{f.lower()}_expected_check', {'cells': int(exp.size), 'cells_below_5': int((exp < 5).sum()), 'min_expected': round(float(exp.min()), 3)}, f'Expected-count check for chi-square of {f} vs Survived (cells with expected count below 5)')
    print(f, int(exp.size), int((exp < 5).sum()), round(float(exp.min()), 3))
collapse = {'SibSp': d2['SibSp'].clip(upper=2), 'Parch': d2['Parch'].clip(upper=2)}
for f in ['SibSp', 'Parch']:
    tab = pd.crosstab(collapse[f], d2['Survived'])
    chi2, p, dof, exp = chi2_contingency(tab, correction=False)
    n = tab.values.sum(); v = np.sqrt(chi2 / (n * (min(tab.shape) - 1)))
    rates = d2.groupby(collapse[f])['Survived'].agg(['mean', 'count'])
    rd = {str(k): {'rate': round(float(r['mean']), 4), 'n': int(r['count'])} for k, r in rates.iterrows()}
    record_fact(f'stat1_{f.lower()}_collapsed_test', {'levels': '0, 1, 2+', 'chi2': float(chi2), 'p': float(p), 'dof': int(dof), 'cramers_v': float(v), 'min_expected': round(float(exp.min()), 3), 'cells_below_5': int((exp < 5).sum()), 'rates': rd}, f'Chi-square of {f} with sparse levels collapsed to 0, 1, 2+; sensitivity check, not Holm-adjusted')
    print(f, round(chi2, 2), p, round(v, 3), round(float(exp.min()), 2), rd)
