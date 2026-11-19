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
clean = df.copy()
clean.columns = [c.strip() for c in clean.columns]
clean = clean.dropna(subset=['Life expectancy'])
publish('clean_frame', clean)
le = clean['Life expectancy']
q = le.quantile([0.25, 0.5, 0.75])
print('rows', len(clean))
print('overall mean', round(le.mean(),3), 'median', round(le.median(),3), 'sd', round(le.std(),3), 'q1', q.loc[0.25], 'q3', q.loc[0.75], 'min', le.min(), 'max', le.max())
print(clean.groupby('Status')['Life expectancy'].agg(['count','mean','median','std']).round(3))
print(clean[clean['Year'].between(2000,2015)].groupby('Year')['Life expectancy'].agg(['count','mean','median']).round(3))
print(clean['Status'].value_counts())

# %%
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
le_all = clean['Life expectancy']
for ax, s in zip(axes[:2], ['Developed', 'Developing']):
    ax.hist(clean.loc[clean['Status'] == s, 'Life expectancy'], bins=30)
    ax.set_title(f'Life expectancy histogram, {s} countries (counts of rows)')
    ax.set_xlabel('Life expectancy (years)')
    ax.set_ylabel('Count of rows')
data = [clean.loc[clean['Status'] == s, 'Life expectancy'].values for s in ['Developed', 'Developing']]
axes[2].boxplot(data, labels=['Developed', 'Developing'])
axes[2].set_title('Life expectancy box plot by Status (years)')
axes[2].set_xlabel('Status')
axes[2].set_ylabel('Life expectancy (years)')
plt.tight_layout()
save_chart(fig, 'le_dist_by_status', 'Life expectancy distribution by Status: histograms (counts of rows) and box plots (years)')

q1, q3 = float(le_all.quantile(0.25)), float(le_all.quantile(0.75))
iqr = q3 - q1
lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
record_fact('le_overall', {'count': int(le_all.count()), 'mean': float(le_all.mean()), 'median': float(le_all.median()), 'sd': float(le_all.std()), 'q1': q1, 'q3': q3, 'min': float(le_all.min()), 'max': float(le_all.max())}, 'Overall Life expectancy summary, years')
record_fact('le_outliers_overall', {'lower_fence': lo, 'upper_fence': hi, 'n_low': int((le_all < lo).sum()), 'n_high': int((le_all > hi).sum())}, 'IQR outlier counts for Life expectancy overall')
for s in ['Developed', 'Developing']:
    g = clean.loc[clean['Status'] == s, 'Life expectancy']
    gq1, gq3 = float(g.quantile(0.25)), float(g.quantile(0.75))
    gi = gq3 - gq1
    record_fact('le_by_status_' + s.lower(), {'count': int(g.count()), 'mean': float(g.mean()), 'median': float(g.median()), 'sd': float(g.std()), 'q1': gq1, 'q3': gq3, 'lower_fence': gq1 - 1.5 * gi, 'upper_fence': gq3 + 1.5 * gi, 'n_low_outliers': int((g < gq1 - 1.5 * gi).sum()), 'n_high_outliers': int((g > gq3 + 1.5 * gi).sum())}, f'Life expectancy summary and IQR outliers for Status {s}')
yr = clean[clean['Year'].between(2000, 2015)].groupby('Year')['Life expectancy'].agg(['count', 'mean', 'median'])
record_fact('le_mean_by_year', {str(int(k)): float(v) for k, v in yr['mean'].items()}, 'Mean Life expectancy per Year 2000-2015, years')
record_fact('le_median_by_year', {str(int(k)): float(v) for k, v in yr['median'].items()}, 'Median Life expectancy per Year 2000-2015, years')
record_fact('rows_by_year_and_status', {'rows_per_year': int(yr['count'].iloc[0]), 'rows_developed': int((clean['Status'] == 'Developed').sum()), 'rows_developing': int((clean['Status'] == 'Developing').sum())}, 'Row counts per Year and per Status')
print('overall fences', round(lo, 2), round(hi, 2), 'n_low', int((le_all < lo).sum()), 'n_high', int((le_all > hi).sum()))
for s in ['Developed', 'Developing']:
    g = clean.loc[clean['Status'] == s, 'Life expectancy']
    gq1, gq3 = float(g.quantile(0.25)), float(g.quantile(0.75))
    gi = gq3 - gq1
    print(s, 'fences', round(gq1 - 1.5 * gi, 2), round(gq3 + 1.5 * gi, 2), 'low', int((g < gq1 - 1.5 * gi).sum()), 'high', int((g > gq3 + 1.5 * gi).sum()))

# %%
yrs = clean[clean['Year'].between(2000, 2015)].groupby('Year')['Life expectancy'].agg(['count', 'mean', 'median']).round(3)
print(yrs.to_string())
all_183 = bool((yrs['count'] == 183).all())
counts_by_year = {str(int(k)): int(v) for k, v in yrs['count'].items()}
record_fact('rows_per_year_all', {'counts_by_year': counts_by_year, 'all_183': all_183, 'min_count': int(yrs['count'].min()), 'max_count': int(yrs['count'].max())}, 'Row counts per Year 2000-2015 checked for every year')
print('all_183', all_183, 'min', int(yrs['count'].min()), 'max', int(yrs['count'].max()))

# %%
yr_full = clean[clean['Year'].between(2000, 2015)].groupby('Year')['Life expectancy'].agg(['count', 'mean', 'median'])
per_year = {str(int(y)): {'count': int(r['count']), 'mean': round(float(r['mean']), 3), 'median': round(float(r['median']), 3)} for y, r in yr_full.iterrows()}
record_fact('le_year_table', per_year, 'Row count, mean and median Life expectancy for each Year 2000-2015, years')
print(yr_full.round(3).to_string())

# %%
ys = clean[clean['Year'].between(2000, 2015)].groupby(['Year', 'Status'])['Life expectancy'].agg(['count', 'mean', 'median']).round(3); tbl = {f"{int(y)}_{s}": {'count': int(r['count']), 'mean': float(r['mean']), 'median': float(r['median'])} for (y, s), r in ys.iterrows()}; record_fact('le_year_status_table', tbl, 'Row count, mean and median Life expectancy for each Year 2000-2015 and each Status, years'); print(ys.to_string())
