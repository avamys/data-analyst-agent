# Repeat Visit Analysis: Predictors of repeat_visit in a 2,000-Row Dataset

## Summary

- **Tier is by far the strongest association.** Repeat-visit rates are 6.7% for bronze, 38.8% for silver and 89.6% for gold (chi-square = 1113.7, Cramér's V = 0.746). Tier also dominates the predictive models.
- **Quarter is the only numeric feature significantly associated with repeat_visit after Holm correction** (Mann-Whitney Holm-adjusted p = 4.9e-23). Its marginal association is positive, but its standardized logistic coefficient conditional on tier is negative (−0.42). These two results disagree, and this report does not resolve the disagreement.
- **Age, distance_km and staff_on_shift show no significant association** after Holm correction. Their predictive contributions are small.
- **Both models beat the majority-class baseline** (accuracy 0.57, ROC AUC 0.50) on a single 400-row test split. Logistic regression reaches ROC AUC 0.925 and log loss 0.345. The random forest reaches ROC AUC 0.901 and log loss 0.382. A tier-only logistic model reaches ROC AUC 0.903 and log loss 0.358, so the extra features add only a small gain on that split.
- **No tier interaction with distance_km or age was significant** (joint LR test p = 0.540).

## Data

- **Size:** 2,000 rows × 6 columns.
- **Target:** repeat_visit (binary). Class 0 is 57.0% and class 1 is 43.0%.
- **Features:** quarter, age, distance_km and staff_on_shift (numeric), and tier (categorical). The data has no date/time features and no id or free-text columns.
- **Missing values:** none in any column.

## Findings

### Overall rate and descriptive rates by group

The overall positive rate of repeat_visit is 0.4295 (about 43%). The profile confirms 0 missing values in every column.

**Tier** is the strongest separator:
- Bronze: 6.7% (n = 880)
- Silver: 38.8% (n = 400)
- Gold: 89.6% (n = 720)

**Quarter** rates rise from 22.0% at level 1 to 59.2% at level 8, with one dip. Level 4 is 42.8% and level 5 is 42.4%. Each level has n = 250. These are descriptive differences.

**Age** quintile bins range from 39.9% to 45.5%. **Distance_km** quintile bins range from 40.5% to 46.3%. **Staff_on_shift** bins are 46.4% (3–5, n = 578), 41.4% (6–8, n = 609) and 41.7% (9–12, n = 813). None of these differences is tested at this stage.

Charts:

![Share of rows with repeat_visit = 1 (rate) within each group of tier, quarter, age, distance_km and staff_on_shift; red line is overall rate 0.43](tasks/eda_1/charts/eda1_rate_by_feature.png)

![Repeat visit rate by tier level: share of rows with repeat_visit = 1 in each tier group; red dashed line is overall rate 0.43](tasks/eda_1/charts/eda1_rate_tier.png)

![Repeat visit rate by quarter level: share of rows with repeat_visit = 1 in each quarter group; red dashed line is overall rate 0.43](tasks/eda_1/charts/eda1_rate_quarter.png)

![Repeat visit rate by age quintile bin: share of rows with repeat_visit = 1 in each age_bin group; red dashed line is overall rate 0.43](tasks/eda_1/charts/eda1_rate_age.png)

![Repeat visit rate by distance_km quintile bin: share of rows with repeat_visit = 1 in each distance_bin group; red dashed line is overall rate 0.43](tasks/eda_1/charts/eda1_rate_distance.png)

![Repeat visit rate by staff_on_shift bin: share of rows with repeat_visit = 1 in each staff_bin group; red dashed line is overall rate 0.43](tasks/eda_1/charts/eda1_rate_staff.png)

### Tier: association and pairwise differences

Tier is strongly associated with repeat_visit: chi-square = 1113.7 (df = 2, p ≈ 1.5e-242), Cramér's V = 0.746, n = 2,000.

Pairwise differences in rate (Wald 95% CIs, unadjusted two-proportion z-tests):
- Silver vs bronze: +0.320 (95% CI 0.270 to 0.371)
- Gold vs bronze: +0.829 (95% CI 0.801 to 0.857)
- Gold vs silver: +0.508 (95% CI 0.456 to 0.561)

All three p-values are below 0.001. They are unadjusted for multiplicity.

![Repeat visit rate by tier with overall rate line](tasks/stat_1/charts/stat1_tier_rate.png)

### Numeric features: tests and effect sizes

Tests compare each numeric feature between repeat_visit = 1 and repeat_visit = 0. Holm step-down correction was applied separately to the four Mann-Whitney tests and to the four point-biserial tests.

| Feature | Mean difference (Welch 95% CI) | Mann-Whitney p | Holm (MW) | Point-biserial r | Holm (PB) |
|---|---|---|---|---|---|
| quarter | 1.04 (0.84 to 1.23) | 1.2e-23 | 4.9e-23 | 0.224 | 1.4e-23 |
| age | 0.18 (−0.87 to 1.23) | 0.63 | 1.00 | 0.007 | 0.74 |
| distance_km | −0.41 (−1.16 to 0.34) | 0.54 | 1.00 | −0.024 | 0.57 |
| staff_on_shift | −0.25 (−0.50 to 0.004) | 0.056 | 0.17 | −0.043 | 0.16 |

- **Quarter** is significant after correction under both tests.
- **Age** is not significant. Its CI includes effects of about one year in either direction, so small effects are not excluded.
- **Distance_km** is not significant. Its CI includes small effects, so no association is detected at this sample size.
- **Staff_on_shift** is not significant after correction. Its CI is close to zero and does not rule out a small effect.

Ranking by effect size: tier (Cramér's V 0.746) > quarter (r 0.224) > staff_on_shift (|r| 0.043) > distance_km (|r| 0.024) > age (|r| 0.007). Cramér's V and point-biserial r are on different scales, so the ranking across tier and numeric features is indicative only.

### Tier interactions with distance_km and age

- **Tier × distance_km:** LR chi-square = 2.14 (df = 2, p = 0.343).
- **Tier × age:** LR chi-square = 0.91 (df = 2, p = 0.633).
- **Both jointly:** LR chi-square = 3.11 (df = 4, p = 0.540). No interaction is worth reporting.

Rates within median halves of each feature, by tier (low vs high):
- Distance_km: bronze 6.5% vs 6.9%; silver 35.5% vs 42.0%; gold 89.0% vs 90.2%.
- Age: bronze 5.3% vs 8.2%; silver 38.3% vs 39.3%; gold 88.9% vs 90.3%.

The tier gradient (bronze < silver < gold) holds in every half. Within-tier two-proportion tests (unadjusted, 6 tests) are not significant at 0.05. The closest is bronze age (difference +0.029, p = 0.089). In the adjusted logistic model with standardized predictors, the bronze distance_km slope is −0.005 log-odds per SD (p = 0.972) and the bronze age slope is 0.156 per SD (p = 0.247).

![Repeat visit rate by tier within low and high halves of distance_km and age](tasks/stat_2/charts/stat2_rates_by_half.png)

### Quarter and tier mix (descriptive)

Tier mix changes across quarters. Bronze falls from 180 of 250 rows at quarter 1 to 40 of 250 at quarter 8, and gold rises from 20 to 160. Silver is fixed at 50 per quarter.

Within tier:
- **Gold** stays high, about 0.84 to 0.98 across quarters.
- **Bronze** stays low, about 0.00 to 0.10.
- **Silver** declines from 0.46, 0.58 and 0.50 in quarters 1 to 3 to 0.22 and 0.26 in quarters 7 and 8. Its descriptive linear slope is −0.046 per quarter level.

The quarter trend therefore partly persists within silver. This result does not establish how much of the quarter association is explained by tier. The silver decline is not tested for significance, and the gold quarter 1 (n = 20) and bronze quarter 8 (n = 40) cells are too small for firm interpretation.

![Repeat visit rate by quarter level, drawn separately for each tier; the trend is shown within tier](tasks/eda_2/charts/eda2_rate_quarter_by_tier.png)

### Predictive modelling

**Setup:** A stratified 80/20 split with random_state = 42 gives 1,600 training rows and 400 test rows. The positive rate is 0.4295 overall, 0.4294 in training and 0.43 in test. The feature table has quarter, age, distance_km and staff_on_shift as numeric, plus tier one-hot encoded (tier_bronze, tier_gold, tier_silver).

**Scores on the 400-row test split:**

| Model | Accuracy | ROC AUC | Log loss |
|---|---|---|---|
| Majority-class baseline | 0.57 | 0.50 | 15.50* |
| Logistic regression (regularized, ml_2) | 0.8575 | 0.9247 | 0.3452 |
| Random forest (ml_2) | 0.8625 | 0.9006 | 0.3817 |
| Tier-only logistic (ml_3) | 0.86 | 0.9035 | 0.3580 |
| Full logistic refit, unregularized (ml_3) | 0.8575 | 0.9246 | 0.3456 |

*The baseline's log loss comes from constant 0/1 probabilities on the test split and is not a meaningful reference.

- Logistic regression has the lower log loss of the two ml_2 models (0.345 vs 0.382). The random forest has slightly higher accuracy (0.8625 vs 0.8575).
- The tier-only logistic is slightly lower in accuracy than the random forest, but higher in ROC AUC and lower in log loss.
- The regularized ml_2 logistic and the ml_3 full refit give ROC AUC 0.9247 and 0.9246 and log loss 0.3452 and 0.3456. The ml_3 finding notes that the two fits are not identical because the ml_2 model was regularized. Both sets of values are reported as they stand.
- Full minus tier-only: accuracy −0.0025 (one row of 400), ROC AUC +0.021, log loss −0.012. The extra features add small gains in ranking and calibration on this split, and accuracy shows no gain.
- In the full refit, unstandardized absolute coefficients are tier_gold 2.67, tier_bronze 2.47, tier_silver 0.19, quarter 0.18, staff_on_shift 0.03, distance_km 0.003 and age 0.002. This ranks coefficient size and is not a significance test.

![Test-set accuracy of the majority baseline, logistic regression and random forest](tasks/ml_2/charts/ml2_model_accuracy.png)

**Feature importance:**
- **Random forest permutation drops in test ROC AUC:** tier_gold 0.173 (sd 0.022) and tier_bronze 0.084 (sd 0.013). Quarter (−0.001, sd 0.004), age (−0.003, sd 0.003), distance_km (−0.005, sd 0.004), staff_on_shift (−0.007, sd 0.003) and tier_silver (−0.002, sd 0.004) are small.
- **Staff_on_shift:** its drop of 0.007 is under 0.01 ROC AUC in absolute terms. It is larger than its own permutation sd (0.003), so the earlier description of it as "within about one sd" is withdrawn.
- **Regularized logistic standardized coefficients:** tier_gold +1.33, tier_bronze −1.23, quarter −0.42, staff_on_shift −0.07, tier_silver −0.06, distance_km −0.02 and age −0.02. All three tier dummies are included, so these are not contrasts against silver.

![Permutation importance of each feature for the random forest on the test split](tasks/ml_2/charts/ml2_permutation_importance.png)

**Quarter in the models (disagreement):** Marginally, quarter is positively associated with repeat_visit (stat_1). Conditional on tier, its standardized logistic coefficient is −0.42 in the regularized ml_2 model, and its standardized coefficient in the ml_3 refit is also −0.42. The unstandardized coefficient in the ml_3 refit is +0.175. The sign therefore differs between the marginal association and the conditional model. These findings are reported as they stand and are not resolved here. Whether tier and quarter are confounded was not tested in these findings; eda_2 shows only that tier mix changes across quarters.

## Limitations

- **Quarter finding is unresolved.** The lead's review asked that the quarter result state only the conditional coefficient (−0.42, opposite in sign to the marginal association) and that confounding with tier be described as untested and dependent on eda_2. The Findings section follows this. The sign disagreement between the marginal and conditional results remains open. It affects the Summary and the quarter rows of the Findings.
- **Staff_on_shift wording is corrected.** The earlier claim that its permutation drop was within one standard deviation is withdrawn, because its drop (−0.007) is larger than its own sd (0.003). The drop is described only as small in absolute terms.
- **Tier permutation values were checked against the full fact.** The ml_2 fact gives drops in test ROC AUC of 0.1732 for tier_gold (sd 0.0216) and 0.0845 for tier_bronze (sd 0.0133). The ml_3 restatement gives these as negative values. The ml_2 fact is the source reported here.
- **Multiplicity:** The tier pairwise comparisons are unadjusted. The within-tier half tests (6 unadjusted tests) and the interaction tests are not multiplicity-adjusted. The bronze age result (p = 0.089) is not significant.
- **Small cells:** The gold quarter 1 (n = 20) and bronze quarter 8 (n = 40) rates are unstable. The silver quarter decline has not been tested for significance.
- **Single split:** All model results come from one 400-row test split. No cross-validation was run, so the model differences (for example, logistic vs random forest log loss, and the small full-vs-tier gains) are not shown to hold on other splits.
- **Model fits differ:** The regularized ml_2 logistic and the unregularized ml_3 refit give slightly different scores.
- **Task status:** ml_3 is marked partial. Its tier-only vs full comparison is reported on one split only.
- **Association only:** The analyses measure associations and predictive performance. They do not establish causes.

## Open questions

- Does the tier effect hold after adjusting for quarter, given that tier mix shifts across quarters?
- Is the quarter association independent of tier once tier is adjusted for? Why does its sign differ between the marginal association and the conditional logistic coefficient, and does the sign change when tier is controlled for?
- Is the quarter trend linear, or driven by a few levels (including the dip at level 5)?
- Is the within-silver decline across quarters statistically significant, given n = 50 per quarter?
- Are the gold quarter 1 and bronze quarter 8 estimates stable enough to interpret, for example with confidence intervals?
- Are the small age, distance_km and staff_on_shift differences significant after controlling for tier and quarter (for example, with a pooled logistic model)?
- Is the bronze age difference (0.053 vs 0.082) a real small effect or noise?
- Does a tier-only model match the full model's accuracy, ROC AUC and log loss across repeated cross-validation, rather than on one split?
- Does the logistic log loss advantage over the random forest hold under repeated cross-validation?