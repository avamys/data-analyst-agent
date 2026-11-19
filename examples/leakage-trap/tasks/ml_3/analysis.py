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
from sklearn.model_selection import RepeatedStratifiedKFold
d = df.copy()
print(d.shape)
print(d.dtypes.to_string())
print(d['churned'].value_counts().to_string())
X_nl = pd.get_dummies(d[['usage_hours','tenure_months','plan']], columns=['plan'], drop_first=False, dtype=float)
y = d['churned'].astype(int).values
print(X_nl.columns.tolist())
print(X_nl.isna().sum().sum(), len(y))

# %%
from sklearn.model_selection import RepeatedStratifiedKFold, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.dummy import DummyClassifier

scoring = {'accuracy': 'accuracy', 'roc_auc': 'roc_auc', 'f1': 'f1'}
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=0)
models = {
    'logreg': make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    'gbt': GradientBoostingClassifier(random_state=0),
    'majority': DummyClassifier(strategy='most_frequent'),
}
res = {}
for k, m in models.items():
    r = cross_validate(m, X_nl.values, y, cv=cv, scoring=scoring)
    res[k] = {s: r['test_' + s] for s in scoring}
    summ = {s: {'mean': float(np.mean(v)), 'sd': float(np.std(v, ddof=1)), 'min': float(np.min(v)), 'max': float(np.max(v))} for s, v in res[k].items()}
    record_fact(f'ml3_cv_{k}', summ, f'Repeated stratified 5-fold x10 CV summary for {k} on no-leak features: mean, sd, min, max of accuracy, roc_auc, f1')
    print(k, {s: (round(v['mean'], 4), round(v['sd'], 4)) for s, v in summ.items()})

fig, axes = plt.subplots(1, 3, figsize=(12, 4))
for ax, s in zip(axes, ['accuracy', 'roc_auc', 'f1']):
    ax.boxplot([res[k][s] for k in models], labels=list(models))
    ax.set_title(f'CV {s} per fold (50 folds), no-leak features')
    ax.set_ylabel(f'{s} score')
axes[0].axhline(0.637, color='r', ls='--')
plt.tight_layout()
save_chart(fig, 'ml3_cv_scores', 'Per-fold CV accuracy, ROC AUC and F1 on no-leak features for logistic regression, gradient boosting and majority baseline (red line: majority accuracy 0.637)')

# %%
record_fact('ml2_logreg_no_leak', {'train_accuracy': 0.695, 'test_accuracy': 0.605, 'baseline_accuracy': 0.635, 'test_roc_auc': 0.612, 'test_f1': 0.3361}, 'Single 800/200 split result for logistic regression on no-leak features, copied from ml_2 for comparison with repeated CV'); record_fact('ml2_gbt_no_leak', {'train_accuracy': 0.7963, 'test_accuracy': 0.57, 'baseline_accuracy': 0.635, 'test_roc_auc': 0.5305, 'test_f1': 0.3175}, 'Single 800/200 split result for gradient boosting on no-leak features, copied from ml_2 for comparison with repeated CV'); print({k: (round(float(np.mean(res[k]['f1'])),4), round(float(np.std(res[k]['f1'], ddof=1)),4)) for k in ['logreg','gbt']})

# %%
from sklearn.model_selection import RepeatedStratifiedKFold, cross_validate
seed_out = {}
for seed in [1, 2]:
    cvs = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=seed)
    seed_out[str(seed)] = {}
    for k, m in models.items():
        r = cross_validate(m, X_nl.values, y, cv=cvs, scoring=scoring)
        seed_out[str(seed)][k] = {s: float(np.mean(r['test_' + s])) for s in ['accuracy', 'roc_auc']}
record_fact('ml3_seed_stability', seed_out, 'Mean CV accuracy and roc_auc per model for CV seeds 1 and 2 (10 repeats of 5 folds each), to compare with seed 0')
print(seed_out)
