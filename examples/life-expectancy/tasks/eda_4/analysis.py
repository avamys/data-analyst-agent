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
LE_COL=[c for c in df.columns if c.strip()=="Life expectancy"][0]
d=df[["Year","Status",LE_COL]].copy()
d.columns=["Year","Status","LE"]
d["Status"]=d["Status"].astype(str).str.strip()
d["Year"]=d["Year"].astype(int)
d=d[(d.Year>=2000)&(d.Year<=2015)]
def q1(s): return s.quantile(0.25)
def q3(s): return s.quantile(0.75)
aggf=dict(count="count",mean="mean",median="median",sd="std",q1=q1,q3=q3)
gs=d.groupby(["Year","Status"])["LE"].agg(**aggf).round(3)
print(gs.unstack("Status").to_string())
ys=d.groupby("Year")["LE"].agg(**aggf).round(3)
print(ys.to_string())
gap=(gs.xs("Developed",level="Status")["mean"]-gs.xs("Developing",level="Status")["mean"]).round(3)
print(gap.to_string())
tbl={}
for (y,s),r in gs.iterrows():
    tbl[f"{y}_{s}"]={k:float(v) for k,v in r.items()}
record_fact("eda4_le_year_status_stats",tbl,"Count, mean, median, SD, Q1, Q3 of Life expectancy by Year and Status, 2000-2015, years")
yt={str(y):{k:float(v) for k,v in r.items()} for y,r in ys.iterrows()}
record_fact("eda4_le_year_stats",yt,"Count, mean, median, SD, Q1, Q3 of Life expectancy by Year, all Status, 2000-2015, years")
record_fact("eda4_gap_by_year",{str(y):float(v) for y,v in gap.items()},"Developed minus Developing mean Life expectancy by Year, years")

# %%
dev=gs.xs('Developed',level='Status')
dng=gs.xs('Developing',level='Status')
rise_dev=float(dev.loc[2015,'mean']-dev.loc[2000,'mean'])
rise_dng=float(dng.loc[2015,'mean']-dng.loc[2000,'mean'])
g0=float(gap.loc[2000]); g1=float(gap.loc[2015])
record_fact('eda4_rise_by_status',{'developed_mean_rise':round(rise_dev,3),'developing_mean_rise':round(rise_dng,3),'gap_2000':g0,'gap_2015':g1,'gap_change':round(g1-g0,3)},'Change in mean Life expectancy 2000 to 2015 by Status and change in Developed-Developing mean gap, years')
fig,ax=plt.subplots(figsize=(8,4.5))
ax.plot(dev.index,dev['mean'],marker='o',label='Developed')
ax.plot(dng.index,dng['mean'],marker='o',label='Developing')
ax.set_title('Mean Life expectancy by Year and Status, 2000-2015')
ax.set_xlabel('Year')
ax.set_ylabel('Mean Life expectancy (years)')
ax.legend()
ax.grid(alpha=0.3)
save_chart(fig,'eda4_mean_le_by_status','Mean Life expectancy by Year for Developed and Developing countries, 2000-2015 (years)')
print(round(rise_dev,3),round(rise_dng,3),g0,g1)

# %%
mm=(ys['mean']-ys['median']).round(3)
print(mm.to_string())
record_fact('eda4_mean_median_gap_by_year',{str(y):float(v) for y,v in mm.items()},'Mean minus median Life expectancy by Year, all Status, 2000-2015, years')
cnt=gs['count'].unstack('Status')
print(cnt.iloc[[0,-1]].to_string())
record_fact('eda4_rows_by_year_status',{str(y):{s:float(cnt.loc[y,s]) for s in cnt.columns} for y in cnt.index},'Row counts by Year and Status, 2000-2015')
