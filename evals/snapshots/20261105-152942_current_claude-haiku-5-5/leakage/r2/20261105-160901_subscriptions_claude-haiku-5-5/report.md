# Churn Analysis of a 1,000-Customer Dataset: Predicting `churned`

## Summary

- **Leakage flag is the dominant signal.** `refund_issued` alone separates churners from non-churners almost perfectly: churn is 1.6% when it is 0 and 95.9% when it is 1 (Cramer's V = 0.946). Whether refunds are recorded after churn is not established by the data, so this column is treated as a probable leakage column and is excluded from the other results below.
- **Without `refund_issued`, the models add little beyond the majority baseline.** Test accuracy is 0.605 for logistic regression and 0.620 for a random forest, against 0.635 for always predicting "not churned." Logistic regression has the higher test ROC AUC (0.612, against 0.563 for the forest).
- **Usage and tenure carry the legitimate signal.** Churned customers have lower `usage_hours` and shorter `tenure_months` than retained customers, with small-to-moderate effects. Both remain significant after adjustment for plan in a multivariable logistic regression (usage OR 0.947 per hour; tenure OR 0.976 per month).
- **The basic plan churns more than the other two plans.** Basic churn is 42.8%, against 29.3% for plus and 29.8% for pro. The plus and pro rates do not differ significantly. The basic-plan excess persists after adjusting for usage and tenure (plus OR 0.552, pro OR 0.612, both versus basic).

## Data

- **Size:** 1,000 rows and 5 columns.
- **Target:** `churned` (binary). Class 0 (retained) is 63.7% and class 1 (churned) is 36.3%.
- **Features:** `usage_hours` and `tenure_months` (numeric), `refund_issued` (numeric, binary in practice), and `plan` (categorical).
- **Missing values:** none in any column, so missingness cannot relate to other columns.
- **Dates and identifiers:** the dataset has no date/time columns and no ID or free-text columns.
- **Profile warning:** `refund_issued` alone predicts `churned` with accuracy 0.975, flagged as possible target leakage.

## Findings

### Overall churn and rates by group

Churn is 36.3% across the 1,000 rows (eda_1).

| Plan | Churn rate | n |
|---|---|---|
| basic | 42.8% | 512 |
| plus | 29.3% | 297 |
| pro | 29.8% | 191 |

![Churn rate by plan level](tasks/eda_1/charts/churn_rate_by_plan.png)

Churned customers have lower usage and shorter tenure:

| Variable | Retained: mean / median | Churned: mean / median |
|---|---|---|
| usage_hours | 21.8 / 20.5 | 17.3 / 16.2 |
| tenure_months | 39.1 / 41.0 | 29.8 / 26.0 |

Churn by usage_hours quartile bin falls from 46.6% (1.9 to 12.5 hours, n=253) to 41.1% (12.5 to 18.9, n=248), 36.1% (18.9 to 25.5, n=249) and 21.2% (25.5 to 67.7, n=250).

Churn by tenure_months quartile bin falls from 49.8% (0.999 to 18.0 months, n=257) to 41.5% (18.0 to 36.0, n=246), 29.1% (36.0 to 53.0, n=258) and 24.3% (53.0 to 71.0, n=239).

### refund_issued (analysed separately; probable leakage)

- Churn is 1.6% for `refund_issued` = 0 (n=632) and 95.9% for `refund_issued` = 1 (n=368). The chi-square test gives χ² = 895.2 (df 1), p < 0.001, Cramer's V = 0.946.
- 97.2% of churned rows have `refund_issued` = 1.
- The profile's single-column accuracy of 0.975 was reproduced in ml_2 (rule: predict churned = refund_issued, 1,000 rows).
- This is an association only. The data does not show whether refunds were recorded before or after churn. It is consistent with a refund recorded at or after cancellation, but the timing cannot be established from this dataset.

![Churn rate by refund_issued](tasks/eda_1/charts/churn_rate_by_refund_issued.png)

![Churn rate by refund_issued: share of rows with churned = 1 for refund_issued 0 and 1](tasks/ml_2/charts/refund_churn_rate.png)

### Statistical tests of association and difference

- **plan vs churned:** χ² = 19.03 (df 2), p = 0.00007, Cramer's V = 0.138 (small effect).
- **Pairwise plan comparisons (chi-square, Holm-corrected):**
  - basic vs plus: 42.8% vs 29.3%, Holm p = 0.0004 (significant).
  - basic vs pro: 42.8% vs 29.8%, Holm p = 0.0036 (significant).
  - plus vs pro: 29.3% vs 29.8%, Holm p = 0.90 (not significant).
- **usage_hours vs churned:** churned mean 17.30 against retained 21.77 (difference −4.47; Welch 95% CI −5.64 to −3.30). Mann-Whitney p = 7×10⁻¹¹; rank-biserial −0.248 (signed, churned minus retained), a small-to-moderate effect. Normality was not formally checked, so the rank-based test is the primary result.
- **tenure_months vs churned:** churned mean 29.84 against retained 39.12 (difference −9.27; Welch 95% CI −11.80 to −6.75). Mann-Whitney p = 3×10⁻¹²; rank-biserial −0.265 (signed), a small-to-moderate effect.

![Distributions of usage_hours and tenure_months for retained versus churned customers (boxplots; median and interquartile range shown)](tasks/stat_1/charts/numeric_by_churn.png)

![Churn rate by plan: share of customers who churned, per plan level](tasks/stat_1/charts/churn_rate_by_plan.png)

### Interactions (stat_2; partial)

**Plan × usage_hours:** no interaction was detected (LR χ² = 2.90, p = 0.235). This is no detected interaction at this sample size, not evidence that plan does not moderate the usage effect.

**Plan × tenure_months:** no interaction was detected (LR χ² = 1.40, p = 0.496). The same caveat applies.

Within-plan odds ratios (per unit):

| Plan | Usage OR per hour (95% CI, n) | Tenure OR per month (95% CI, n) |
|---|---|---|
| basic | 0.954 (0.935–0.974, 512) | 0.979 (0.970–0.988, 512) |
| plus | 0.957 (0.931–0.984, 297) | 0.970 (0.957–0.983, 297) |
| pro | 0.920 (0.882–0.959, 191) | 0.980 (0.964–0.995, 191) |

Plan versus basic, within median halves (odds ratios with 95% CI):

| Half | Plus vs basic | Pro vs basic |
|---|---|---|
| usage_hours, low (n=501) | 0.583 (0.386–0.881) | 0.658 (0.404–1.073) |
| usage_hours, high (n=499) | 0.517 (0.325–0.824) | 0.500 (0.292–0.857) |
| tenure_months, low (n=503) | 0.629 (0.420–0.941) | 0.602 (0.366–0.991) |
| tenure_months, high (n=497) | 0.435 (0.264–0.718) | 0.578 (0.342–0.979) |

Within the basic plan, churn by usage_hours quartile is 50.8%, 48.5%, 43.5% and 26.5% (lowest to highest usage). Within the basic plan, churn by tenure_months quartile is 54.9%, 47.1%, 37.2% and 29.1% (shortest to longest tenure).

![Churn rate by plan within usage_hours quartile bins](tasks/stat_2/charts/plan_by_usage_churn_rate.png)

**Breakdown decision.** Neither plan pair is treated as a moderated effect, because neither interaction test is significant. The stratified estimates above are reported for transparency. All plan-versus-basic odds ratios in both halves point the same way (below 1). Their sizes differ somewhat between halves: pro versus basic is 0.658 in the low-usage half and 0.500 in the high-usage half, and plus versus basic is 0.629 in the low-tenure half and 0.435 in the high-tenure half. The confidence intervals overlap widely, and the non-significant tests do not rule out these differences.

**Refund × tenure_months (unresolved).** The interaction test (LR χ² = 0.42, p = 0.519) is unreliable because of near-complete separation. Within `refund_issued` = 0, the per-month OR is 0.992 (95% CI 0.961–1.023, n=632). Within `refund_issued` = 1, it is 0.978 (95% CI 0.953–1.004, n=368); this model converged. Churn by refund and tenure quartile ranges from 1.1% to 2.3% when refund is 0, and from 93.2% to 97.7% when refund is 1. This reflects separation rather than moderation. Refund odds ratios within tenure halves (about 1,710 and 1,139) are likewise a separation artifact and are not read as moderation. This pair is not concluded either way.

### Adjusted multivariable model (stat_3)

Logistic regression of `churned` on plan, usage_hours and tenure_months, with `refund_issued` excluded (n=1,000; converged; VIFs between 1.00 and 1.12):

| Term | Adjusted OR | 95% CI | p |
|---|---|---|---|
| plus vs basic | 0.552 | 0.401–0.761 | 0.0003 |
| pro vs basic | 0.612 | 0.420–0.890 | 0.010 |
| usage_hours (per hour) | 0.947 | 0.933–0.962 | <0.001 |
| tenure_months (per month) | 0.976 | 0.969–0.983 | <0.001 |

After adjustment, the basic-plan churn excess persists, and usage and tenure are each significantly associated with lower churn. These effects exclude `refund_issued` by design and are conditional on that choice.

![Adjusted odds ratios with 95% CIs from logistic regression of churned; plan reference is basic](tasks/stat_3/charts/adjusted_or_churn.png)

### Predictive models without refund_issued (ml_1; ml_2 reproduction)

Setup: plan, usage_hours and tenure_months as features; stratified 80/20 split (800 train, 200 test; seed 42). Test churn rate is 36.5%, so the 63.7% majority baseline is a fair comparison.

| Model | Train accuracy | Test accuracy | Test ROC AUC | Test F1 (class 1) |
|---|---|---|---|---|
| Always-0 baseline | — | 0.635 | — | — |
| Logistic regression | 0.695 | 0.605 | 0.612 | 0.336 |
| Random forest (300 trees, min leaf 5) | 0.794 | 0.620 | 0.563 | 0.406 |

- Neither model beats the trivial baseline on test accuracy.
- Logistic regression is preferred on ROC AUC. Its train accuracy (0.695) and test accuracy (0.605) are closer together than the forest's (0.794 and 0.620), which indicates less overfitting. The forest has the higher class-1 F1 but ranks churners worse.
- usage_hours and tenure_months carry nearly all the importance. Standardized logistic coefficients are 0.634 and 0.529, against at most 0.133 for plan dummies. Forest importances are 0.511 and 0.430, against at most 0.025 for plan dummies.
- ml_2 retrained both models on the same partitions and reproduced these results.

![Test-set accuracy of the always-0 baseline, logistic regression and random forest for churned, using plan, usage_hours and tenure_months](tasks/ml_1/charts/churn_model_comparison_accuracy.png)

### Predictive models with refund_issued (ml_2)

Adding `refund_issued` on the same partitions gives:

| Model | Test accuracy | Test ROC AUC | Test F1 (class 1) |
|---|---|---|---|
| Logistic regression | 0.605 → 0.980 | 0.612 → 0.990 | 0.336 → 0.973 |
| Random forest | 0.620 → 0.980 | 0.563 → 0.976 | 0.406 → 0.973 |

These gains come from the leakage column. They are not evidence of predictive value until the timing of refunds relative to churn is confirmed, and the leakage recommendation is to exclude the column from the final model.

## Limitations

- **Leakage is unconfirmed.** `refund_issued` is the strongest predictor by a wide margin, but the data cannot show whether refunds were recorded before or after churn. Reverse causation (churned customers receive refunds) is also not ruled out. The stat_3 adjusted effects and the ml_1 models exclude this column, and their conclusions are conditional on that choice.
- **Refund × tenure interaction is unresolved.** Near-complete separation makes the joint model unreliable (stat_2). The lead's objection stands: it needs a penalized model such as Firth regression, or confirmation of leakage, before any conclusion.
- **Plan interactions are not established either way.** No interaction was detected, but at this sample size that is not evidence of no moderation. The stratified half-sample odds ratios differ in size (see the breakdown decision above), and the confidence intervals are wide.
- **stat_2 review issue (addressed).** The review asked for the full within-level estimates and a breakdown decision. The values now appear in the tables above. The decision and its basis are stated under Findings.
- **Model results rest on one split.** The ml_1 and ml_2 test sets have 200 rows, and differences of a few hundredths in accuracy or AUC are within what a single split can show. The random forest overfits (train–test gap 0.17).
- **Normality was not checked.** The numeric comparisons rely on rank-based tests as the primary result.
- **Non-significance is not absence.** The plus-versus-pro comparison and the interaction tests are non-significant at this sample size.
- **Only one dataset and one split were analysed.** The dataset has no date or time columns, so timing and temporal ordering cannot be examined.
- **No task failed.** stat_2 is marked partial, for the refund pair and the reasons above.

## Open questions

- Were refunds recorded after churn? This needs the source system's refund and cancellation timestamps.
- Does the refund effect hold after adjusting for plan, usage and tenure (a model that includes refund_issued alongside those terms, with penalized estimation for the separation)?
- Does the basic-plan excess hold once the plan × usage and plan × tenure interactions are modelled jointly, rather than tested pair by pair?
- Do the usage and tenure effects differ by plan level, and are they monotonic?
- Would engineered features (for example, usage per tenure month) or a threshold-tuned classifier beat the majority baseline on accuracy without `refund_issued`?
- Would a more constrained or cross-validated random forest reduce the train–test gap and improve test ROC AUC?