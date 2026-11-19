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
import statsmodels.formula.api as smf
from scipy import stats
d = df.copy()
d['tenure_c'] = (d['tenure_months'] - d['tenure_months'].mean()) / d['tenure_months'].std()
d['usage_c'] = (d['usage_hours'] - d['usage_hours'].mean()) / d['usage_hours'].std()
full = smf.logit('churned ~ C(plan) * tenure_c + C(plan) * usage_c', data=d).fit(disp=0)
main = smf.logit('churned ~ C(plan) + tenure_c + usage_c', data=d).fit(disp=0)
lr_stat = 2 * (full.llf - main.llf)
lr_df = full.df_model - main.df_model
lr_p = stats.chi2.sf(lr_stat, lr_df)
ci = full.conf_int()
terms = [k for k in full.params.index if ':' in k]
tab = {k: {'coef': float(full.params[k]), 'p': float(full.pvalues[k]), 'ci_low': float(ci.loc[k, 0]), 'ci_high': float(ci.loc[k, 1])} for k in terms}
for k, v in tab.items():
    print(k, {a: round(b, 4) for a, b in v.items()})
print('LR', round(lr_stat, 3), 'df', lr_df, 'p', round(lr_p, 4))
record_fact('stat3_interaction_terms', tab, 'Interaction logit coefficients (standardized tenure/usage, no refund_issued; basic plan reference) with p-values and 95% CIs')
record_fact('stat3_lr_test', {'lr_stat': float(lr_stat), 'df': float(lr_df), 'p': float(lr_p)}, 'LR test full interaction model vs main-effects model, no refund_issued')

# %%
ref_full = smf.logit('churned ~ C(plan) * tenure_c + C(plan) * usage_c + refund_issued * tenure_c', data=d).fit(disp=0)
ci_r = ref_full.conf_int()
ref_terms = [k for k in ref_full.params.index if ':' in k]
ref_tab = {k: {'coef': float(ref_full.params[k]), 'p': float(ref_full.pvalues[k]), 'ci_low': float(ci_r.loc[k, 0]), 'ci_high': float(ci_r.loc[k, 1])} for k in ref_terms}
record_fact('stat3_refund_included_interactions', ref_tab, 'Comparison: interaction logit coefficients with refund_issued x tenure_c included (standardized; basic plan and refund=0 reference)')
all_tab = {k: v for k, v in tab.items()}
record_fact('stat3_interaction_terms_all', all_tab, 'All plan x tenure_c and plan x usage_c interaction coefficients, no refund_issued, with p-values and 95% CIs')
for k, v in all_tab.items():
    print(k, {a: round(b, 3) for a, b in v.items()})
print('refund-included:')
for k, v in ref_tab.items():
    print(k, {a: round(b, 3) for a, b in v.items()})
