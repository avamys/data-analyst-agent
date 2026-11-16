# Repeat Visit Analysis: Drivers and Predictability of `repeat_visit` in a 2,000-Row Dataset

## Summary

- **Tier is the dominant association with repeat visits.** Repeat rates are 89.6% for gold (n=720), 38.8% for silver (n=400) and 6.7% for bronze (n=880). The tier association is significant (chi-square 1113.7, df 2, Cramér's V 0.746), and tier accounts for almost all of the model's predictive lift.
- **Quarter is a second, weaker association, and it is confounded with tier mix.** The overall repeat rate rises from 22.0% in quarter 1 to 59.2% in quarter 8. Gold's share of rows grows across quarters, and when re-weighted to overall tier shares the rate falls from 45% to 36%.
- **age, distance_km and staff_on_shift show no significant association with repeat_visit.** Their tests are non-significant after Benjamini-Hochberg (BH) adjustment, and their permutation importances in the best model are near zero.
- **Tier does not significantly change the effects of distance_km, age or quarter.** The interaction tests are all non-significant. Within-tier quarter trends are descriptively negative, but the tests do not show that they differ by tier.
- **Logistic regression reached test ROC AUC 0.925 against 0.5 for the majority-class baseline** (accuracy 0.8575 against 0.57). Gradient boosting had higher accuracy (0.8725) and F1 but lower ROC AUC (0.903). Model selection used the test set, so these scores are slightly optimistic.

## Data

- **Size:** 2,000 rows × 6 columns: five features and the target.
- **Target:** `repeat_visit`, binary. Class 0 is 57.0% and class 1 is 43.0% (859 of 2,000 rows are 1).
- **Features:** numeric `quarter`, `age`, `distance_km`, `staff_on_shift`; categorical `tier`. There are no date/time features and no ids or free-text fields.
- **Missing values:** none. No values are missing in any of the six columns, and no row has a missing value (0 of 2,000). Missingness therefore cannot be related to the target or other columns.
- **Ranges:** age 18 to 85; distance_km 0.2 to 76.9 km (median 10.0, mean 11.94, so the distribution is right-skewed); staff_on_shift 3 to 12; quarter 1 to 8. No sentinel codes or non-positive values appear.
- **Quarter coding:** `quarter` takes values 1 to 8, with exactly 250 rows each. It is not confirmed whether this is a calendar quarter or a two-year index, so its meaning should be checked before use.

## Findings

### Overall distribution and univariate rates

The target is moderately imbalanced: 859 of 2,000 rows (43.0%) have `repeat_visit`=1. Repeat rates by group, from the exploratory pass:

- **Tier:** bronze 6.7%, silver 38.8%, gold 89.6%. Gold rows almost always repeat and bronze rows rarely do.
- **Quarter:** 22.0%, 33.2%, 38.0%, 42.8%, 42.4%, 51.6%, 54.4%, 59.2% for quarters 1 to 8. The rise has one small dip at quarter 5 (42.4%) relative to quarter 4 (42.8%).
- **staff_on_shift:** rates range from 39.3% (staff 7 and 11) to 48.3% (staff 9), with no monotone trend. Group sizes range from 184 to 219.
- **Age quartiles:** 43.7%, 38.8%, 44.5%, 44.4% for Q1 to Q4 (n=551, 469, 530, 450). No strong gap.
- **distance_km quartiles:** 42.7%, 44.1%, 44.2% for Q1 to Q3 and 40.8% for Q4 (n=500). The gap is small.

Charts:

![Share of repeat_visit=1 per tier level](tasks/eda_1/charts/rate_by_tier.png)

![Share of repeat_visit=1 per distance_km quartile band](tasks/eda_1/charts/rate_by_distance_band.png)

### Significance and effect sizes

| Feature | Test | Statistic | p | BH-adjusted p | Effect |
|---|---|---|---|---|---|
| tier | chi-square (df 2) | 1113.7 | 1.5e-242 | 7.3e-242 | Cramér's V 0.746 |
| quarter | chi-square (df 7) | 105.0 | 1.0e-19 | 2.5e-19 | Cramér's V 0.229 |
| staff_on_shift | chi-square | 9.40 | 0.401 | 0.628 | Cramér's V 0.069 |
| age | Mann-Whitney | 496257 | 0.628 | 0.628 | rank-biserial 0.013 |
| distance_km | Mann-Whitney | 482160 | 0.537 | 0.628 | rank-biserial −0.016 |

- **Tier:** gold minus bronze rate difference is 82.9 percentage points (95% CI 80.1 to 85.7).
- **Quarter:** quarter 8 minus quarter 1 rate difference is 37.2 percentage points (95% CI 29.2 to 45.2).
- **staff_on_shift:** the largest pairwise gap, staff 9 minus staff 7, is 9.0 points (95% CI −0.5 to 18.5). This pair was chosen post hoc as the most extreme, and the test does not correct for comparisons across all staff pairs. It is not significant.
- **Age:** mean difference (repeat=1 minus repeat=0) is 0.18 years (95% CI −0.87 to 1.23).
- **distance_km:** mean difference (repeat=1 minus repeat=0) is −0.41 km (95% CI −1.16 to 0.33).

Chart:

![Rate of repeat_visit=1 per tier level](tasks/stat_1/charts/stat1_rate_by_tier.png)

### Tier and distance_km, and tier and age interactions

- **Likelihood-ratio test:** adding tier × distance_km and tier × age to the main-effects model does not improve fit (LR chi-square 3.11, df 4, p 0.54). Tier does not significantly change the effect of distance_km or age on repeat_visit.
- **Interaction coefficients** (log-odds, bronze as reference):
  - gold × distance_km: −0.010 (SE 0.021, p 0.62)
  - silver × distance_km: 0.016 (SE 0.020, p 0.43)
  - gold × age: −0.013 (SE 0.015, p 0.39)
  - silver × age: −0.012 (SE 0.014, p 0.40)
- **Age terciles by tier** (young, mid, old):
  - bronze: 5.7%, 6.9%, 7.7%, rising monotonically
  - gold: 90.0%, 87.6%, 91.1%, non-monotone
  - silver: 40.4%, 34.6%, 41.5%, non-monotone
- **Distance terciles by tier** (near, mid, far; n per cell 132 to 311):

| Tier | Near | Mid | Far |
|---|---|---|---|
| Bronze | 6.8% | 6.9% | 6.4% |
| Gold | 89.3% | 90.4% | 88.9% |
| Silver | 33.3% | 38.9% | 43.8% |

  The tier gap dominates any distance pattern. Within silver, the repeat rate rises from 33.3% in the near band to 43.8% in the far band. This descriptive pattern is not significant: the silver × distance_km interaction is 0.016 log-odds per km (p 0.43), and the age interactions are about −0.012 to −0.013 log-odds per year.

Chart:

![Rate of repeat_visit=1 per tier within distance_km tertile bands](tasks/stat_2/charts/stat2_rate_by_tier_distance.png)

### Quarter, tier mix and within-tier trends

- **Tier mix shifts across quarters.** Gold rises from 8% of rows in quarter 1 (n=20) to 32% in quarter 4 (n=80) and 64% in quarter 8 (n=160). Bronze falls from 72% (n=180) to 48% (n=120) in quarters 1 to 4 and to 16% (n=40) in quarter 8. Silver is a constant 20% (n=50 per quarter).
- **Confounding.** The raw quarter rise (22.0% in quarter 1 to 59.2% in quarter 8) is confounded with tier mix. Re-weighting to overall tier shares gives 45% in quarter 1 and 36% in quarter 8, a decline.
- **Per-tier repeat rates by quarter (Q1 to Q8):**
  - Gold: 90%, 95%, 98%, 94%, 88%, 91%, 88%, 84%. Gold group sizes are small in early quarters (n=20 to 80 in Q1 to Q4).
  - Silver: 46%, 58%, 50%, 46%, 28%, 34%, 22%, 26% (n=50 per quarter).
  - Bronze: 7.8%, 10.0%, 7.9%, 7.5%, 4.0%, 3.8%, 3.3%, 0.0% (n=180 down to 40).
- **Within-tier Spearman correlations with quarter:**
  - bronze: ρ −0.086, p 0.011 (n=880)
  - gold: ρ −0.117, p 0.0016 (n=720)
  - silver: ρ −0.216, p 0.000013 (n=400)

  Within every tier the quarter trend is flat or negative, so the overall quarter rise does not persist within tiers.

Chart:

![Left: tier share of rows per quarter. Right: repeat_visit rate per quarter within each tier.](tasks/eda_3/charts/tier_mix_and_repeat_by_quarter.png)

### Tier × quarter interaction

- Adding tier × quarter to the main-effects logit (controlling for age, distance_km and staff_on_shift) gives LR chi-square 0.024 (df 2, p 0.988). There is no evidence of a tier difference in the quarter slope.
- Interaction coefficients (log-odds per quarter, bronze as reference): gold × quarter −0.012 (SE 0.102, p 0.90); silver × quarter 0.0005 (SE 0.087).
- The standard errors are large relative to the coefficients, so the interaction intervals remain wide. A moderate tier difference in the quarter slope cannot be ruled out.
- The linear-in-quarter logit is a rough fit. Gold is near 90% and bronze near 0%, so the logit is close to saturated for these tiers and the slopes are poorly identified at the extremes. The non-significant result is no evidence of a difference, not proof that the slopes are equal.

Chart:

![Rate of repeat_visit=1 per quarter, for each tier](tasks/stat_3/charts/stat3_rate_by_tier_quarter.png)

### Predictive models

- **Setup:** single stratified 80/20 split, seed 42, 400 test rows, shared by all models.
- **Logistic regression (best on test ROC AUC):** accuracy 0.8575, ROC AUC 0.925, F1 0.830.
- **Gradient boosting:** accuracy 0.8725, ROC AUC 0.903, F1 0.852. It scored higher on accuracy and F1 but lower on ROC AUC. The two findings disagree on which model is better, and the report does not resolve this.
- **Majority-class baseline:** accuracy 0.57, ROC AUC 0.5, F1 0.0. The 0.57 accuracy equals the majority-class share of the test set (class 0), so the baseline is a correct reference.
- **Lift over baseline (logistic regression):** test accuracy rises from 0.57 to 0.8575, and ROC AUC rises from 0.5 to 0.925.
- **Selection caveat:** the best model was selected by test-set ROC AUC, so the reported test scores are slightly optimistic.
- **Permutation importance (drop in test ROC AUC, logistic regression, 10 repeats):**
  - tier: 0.458 (sd 0.021)
  - quarter: 0.020 (sd 0.005)
  - age: −0.0005 (sd 0.0002)
  - distance_km: −0.0005 (sd 0.0005)
  - staff_on_shift: +0.0002 (sd 0.0013)

  The three non-tier, non-quarter features are near zero, within the noise of the repeats. Almost all of the model's lift comes from tier, with a small contribution from quarter.

Chart:

![Permutation importance of the five features for the best model on the test set, measured as the mean drop in ROC AUC](tasks/ml_1/charts/ml1_permutation_importance.png)

## Limitations

- **Data coverage:** none of the six columns has missing values, but quarter's meaning (calendar quarter or two-year index) is unconfirmed. The distance_km distribution is right-skewed (max 76.9 km), and the effect of its tail on any model was not assessed.
- **Small cells:** gold has only 20 rows in quarter 1 and 40 in quarter 2. Silver per quarter has n=50, and bronze falls to n=40 in quarter 8. Per-quarter rates for these cells are imprecise, and the bronze drop to 0.0% in quarter 8 rests on 0 of 40 rows.
- **Model selection on the test set:** logistic regression was chosen by test ROC AUC, and reported test scores are therefore slightly optimistic. The model comparison uses a single split, not repeated cross-validation.
- **Model disagreement:** logistic regression leads on ROC AUC and gradient boosting on accuracy and F1. Both results are reported without resolution.
- **No multiple-comparison correction for staff pairs:** the staff 9 vs 7 contrast was chosen post hoc and is not corrected across all staff pairs.
- **Linear logit limits:** the tier × quarter test relies on a linear quarter term, and gold and bronze are near the rate extremes, so the slopes are poorly identified. The interaction standard errors leave moderate tier differences open.
- **Descriptive versus inferential within-tier trends:** the within-tier Spearman results (for example silver ρ −0.216) are descriptive correlations. The interaction tests find no evidence that these trends differ by tier.
- **Inconsistency in stat_3's question text:** it states that the gold share rises "from 20 of 200 rows in quarter 1 to 160 of 200 in quarter 8." The eda_3 counts show 250 rows per quarter, with gold at 20 in quarter 1 and 160 in quarter 8. This report uses the eda_3 counts.
- **Unresolved review issue on stat_2 (lead objection still stands):** the stat_2 review required silver's distance-band rates and a check of silver's interaction coefficients and age-tercile rates. Silver's distance-band rates are now quoted above (33.3%, 38.9%, 43.8%). The silver interaction coefficients (0.016, SE 0.020, p 0.43 for distance; −0.012, SE 0.014, p 0.40 for age) and the silver age-tercile rates (40.4%, 34.6%, 41.5%) match the recorded values. The conclusion that the interactions are not significant is retained. The affected findings are the tier × distance_km and tier × age interaction results, and the silver distance pattern, which is descriptive only.
- **No failed tasks** were recorded.

## Open questions

- Is the quarter trend confounded with tier mix, and does the quarter effect survive controlling for tier? The re-weighting suggests a decline, but no adjusted model was fitted to estimate the quarter effect controlling for tier.
- Is the tier effect an interaction with quarter, as the stat_1 follow-up suggests? The stat_3 test found no tier × quarter interaction, so the question is not settled in the positive direction.
- Why does the bronze repeat rate fall to near zero after quarter 4 (0.0% to 4.0% in quarters 5 to 8), and is this a data-collection change or a real effect?
- Is the silver decline from about 50% in quarter 3 to 22% to 34% in quarters 5 to 8 real, or is it driven by sampling noise at n=50 per quarter?
- Does the gold drift from about 95% to 84% reflect small group sizes or a real decline?
- Would a model with quarter as categorical, or a tier-specific nonlinear quarter term, fit better where gold is near 90% and bronze near 0%?
- Would a model using only tier and quarter match the full five-feature model, which would show that age, distance_km and staff_on_shift add nothing? The permutation results suggest this, but the test was not run.
- Would repeated cross-validation give a less optimistic model comparison than a single test split?
- Does the staff_on_shift result hold after a multiple-comparison correction across all staff pairs?
- Is quarter associated with age, distance_km or staff_on_shift, which could partly explain the tier-quarter pattern?
- Is `quarter` a calendar quarter (1 to 4) or a two-year index (1 to 8), and should it be treated as numeric or categorical?