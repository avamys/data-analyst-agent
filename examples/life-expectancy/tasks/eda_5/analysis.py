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
le = d['Life expectancy']
low = d[le < 44.2][['Country','Year','Status','Life expectancy','Adult Mortality','HIV/AIDS']]
print(len(low))
print(low.sort_values('Life expectancy').to_string())
print(low['Status'].value_counts())
print(low['Year'].value_counts().sort_index())
print(low['Country'].value_counts())
print(d['Status'].value_counts())
print(d['Country'].nunique())

# %%
rows = low.sort_values('Life expectancy')[['Country','Year','Status','Life expectancy']].values.tolist()
record_fact('eda5_low_rows', rows, 'Rows below 44.2 years: country, year, status, life expectancy')
record_fact('eda5_low_by_status', {str(k): int(v) for k, v in low['Status'].value_counts().items()}, 'Count of rows below 44.2 years by Status')
record_fact('eda5_low_by_year', {str(k): int(v) for k, v in low['Year'].value_counts().sort_index().items()}, 'Count of rows below 44.2 years by Year')
record_fact('eda5_low_by_country', {str(k): int(v) for k, v in low['Country'].value_counts().items()}, 'Count of rows below 44.2 years by Country; total rows 2938, countries 193')
fig, ax = plt.subplots(figsize=(7, 4))
low['Country'].value_counts().plot.bar(ax=ax)
ax.set_title('Rows with Life expectancy below 44.2 years, by country (count of rows)')
ax.set_xlabel('Country')
ax.set_ylabel('Rows (count)')
save_chart(fig, 'eda5_low_by_country', 'Count of rows with Life expectancy below 44.2 years, by country')
plt.close(fig)

# %%
sl = low[low['Country']=='Sierra Leone'].sort_values('Year')[['Year','Life expectancy']]
print(sl.to_string())
record_fact('eda5_sierra_leone_rows', sl.values.tolist(), 'Sierra Leone rows below 44.2 years: year, life expectancy')
record_fact('eda5_status_base_rate', {'developing_rows': 2416, 'total_rows': 2928, 'share': 2416/2928}, 'Developing share of rows in eda_1 overall summary (accepted counts)')
print(2416/2928)

# %%
counts = d['Year'].value_counts().sort_index()
record_fact('eda5_rows_per_year', {str(int(k)): int(v) for k, v in counts.items()}, 'Row counts per Year in df (basis for year finding: each year has equal rows)')
print(counts.min(), counts.max(), len(counts))
