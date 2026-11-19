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
train_test = load("ml_1/split_data")
print(type(train_test))
if isinstance(train_test, dict):
    print(list(train_test.keys()))
    for k, v in train_test.items():
        print(k, getattr(v, 'shape', len(v) if hasattr(v, '__len__') else v))
else:
    for item in train_test:
        print(type(item), getattr(item, 'shape', None))

# %%
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score

Xtr_nl = train_test['X_train_no_leak']; Xte_nl = train_test['X_test_no_leak']
Xtr_wr = train_test['X_train_with_refund']; Xte_wr = train_test['X_test_with_refund']
ytr = train_test['y_train']; yte = train_test['y_test']
fn_nl = list(Xtr_nl.columns); fn_wr = list(Xtr_wr.columns)

res = {}
for tag, Xtr, Xte, fn in [('no_leak', Xtr_nl, Xte_nl, fn_nl), ('with_refund', Xtr_wr, Xte_wr, fn_wr)]:
    lr = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    gb = GradientBoostingClassifier(random_state=42)
    lr.fit(Xtr, ytr); gb.fit(Xtr, ytr)
    r_lr = record_model(f'ml2_logreg_{tag}', lr, Xtr, ytr, Xte, yte, f'Logistic regression ({tag})')
    r_gb = record_model(f'ml2_gbt_{tag}', gb, Xtr, ytr, Xte, yte, f'Gradient boosting ({tag})')
    res[tag] = {'logreg': r_lr, 'gbt': r_gb}
    print(tag, 'LR', r_lr)
    print(tag, 'GB', r_gb)

print('baseline test acc', accuracy_score(yte, np.zeros_like(yte)))
print(list(yte.value_counts().items()) if hasattr(yte,'value_counts') else np.unique(yte, return_counts=True))

# %%
lr_nl = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(Xtr_nl, ytr)
coefs = {f: round(float(c), 4) for f, c in zip(fn_nl, lr_nl[-1].coef_[0])}
record_fact('ml2_logreg_no_leak_signed_coefs', coefs, 'Standardized logistic regression coefficients for the no_leak model; sign gives direction of association with churn')
print(coefs)
d = {'logreg_acc_drop': round(res['with_refund']['logreg']['test_accuracy'] - res['no_leak']['logreg']['test_accuracy'], 4), 'logreg_auc_drop': round(res['with_refund']['logreg']['test_roc_auc'] - res['no_leak']['logreg']['test_roc_auc'], 4), 'gbt_acc_drop': round(res['with_refund']['gbt']['test_accuracy'] - res['no_leak']['gbt']['test_accuracy'], 4), 'gbt_auc_drop': round(res['with_refund']['gbt']['test_roc_auc'] - res['no_leak']['gbt']['test_roc_auc'], 4)}
record_fact('ml2_refund_score_drop', d, 'Test score drop when refund_issued is removed (with_refund minus no_leak), for both models')
print(d)
labels = ['LR no_leak', 'GBT no_leak', 'LR with_refund', 'GBT with_refund']
recs = [res['no_leak']['logreg'], res['no_leak']['gbt'], res['with_refund']['logreg'], res['with_refund']['gbt']]
acc = [r['test_accuracy'] for r in recs]
auc = [r['test_roc_auc'] for r in recs]
fig, ax = plt.subplots(figsize=(9, 5))
x = np.arange(4); w = 0.35
ax.bar(x - w/2, acc, w, label='Test accuracy')
ax.bar(x + w/2, auc, w, label='Test ROC AUC')
ax.axhline(0.635, color='gray', ls='--', label='Majority baseline accuracy (0.635)')
ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylim(0, 1.05)
ax.set_ylabel('Score on 200-row test set')
ax.set_title('Test accuracy and ROC AUC of churn classifiers vs majority baseline')
ax.legend()
save_chart(fig, 'ml2_model_comparison', 'Test accuracy and ROC AUC for logistic regression and gradient boosting, with and without refund_issued, against the majority-class baseline of 0.635')
