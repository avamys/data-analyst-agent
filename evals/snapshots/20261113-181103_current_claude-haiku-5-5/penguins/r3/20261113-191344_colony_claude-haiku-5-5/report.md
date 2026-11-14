# Penguin Body Mass (body_mass_g): Distribution, Group Differences, Interactions and Prediction

## Summary

- **Species is the strongest group difference.** Gentoo penguins average 5076.0 g, against 3700.7 g for Adelie and 3733.1 g for Chinstrap (Kruskal-Wallis H = 217.6, p = 5.6e-48, eta-squared from H = 0.64). Adelie and Chinstrap do not differ after Holm adjustment (p = 0.485).
- **Sex matters within every species, but the size of the gap varies.** Males are heavier than females overall by 683.4 g (Cohen's d = 0.94). The species × sex interaction is significant (F = 8.71, p = 0.0002). The male-minus-female gap is 411.8 g in Chinstrap and 805.1 g in Gentoo.
- **Species and flipper length carry almost all the predictive signal.** On a 69-row test set, linear regression reduces test MAE from 624.0 g (mean baseline) to 265.7 g (test R² 0.812). Gradient boosting reaches 280.0 g (test R² 0.789). Island and year contribute almost nothing.
- **Island differences are largely explained by species mix.** Within Adelie, island has no detectable effect once sex is controlled (p = 0.94). Island effects cannot be estimated within Chinstrap or Gentoo, because each sits on a single island.
- **Missing values are rare.** Sex is missing for 3.2% of penguins, and the missingness clusters on Torgersen (9.6%). That pattern is post-hoc and needs confirmation. The 0.6% gaps in the measurement columns show no pattern.

## Data

- **Size:** 344 rows × 8 columns. The analysis sample is 342 penguins with body_mass_g present.
- **Target:** body_mass_g (regression).
- **Features:** bill_length_mm, bill_depth_mm, flipper_length_mm and year (numeric); species, island and sex (categorical). There are no date/time features and no identifier or free-text columns.
- **Missing values:**
  - bill_length_mm, bill_depth_mm, flipper_length_mm and body_mass_g: 2 penguins each (0.6%). The same 2 rows lack all three measurements and body mass.
  - sex: 11 penguins (3.2%).
  - species, island and year: none.

## Findings

### Overall distribution and per-group summaries

Across the 342 penguins with body mass present, mean body mass is 4201.8 g, median 4050 g, SD 801.95 g, with a minimum of 2700 g and a maximum of 6300 g. The distribution is mildly right-skewed (skew 0.47, mean above median). No values fall beyond 1.5 IQR from the quartiles.

![Distribution of body_mass_g across all penguins](tasks/eda_1/charts/bm_hist.png)

Per-group count, mean and median body mass:

| Variable | Level | n | Mean (g) | Median (g) |
|---|---|---|---|---|
| species | Adelie | 151 | 3700.7 | 3700 |
| species | Chinstrap | 68 | 3733.1 | 3700 |
| species | Gentoo | 123 | 5076.0 | 5000 |
| island | Biscoe | 167 | 4716.0 | 4775 |
| island | Dream | 124 | 3712.9 | 3687.5 |
| island | Torgersen | 51 | 3706.4 | 3700 |
| sex | female | 165 | 3862.3 | 3650 |
| sex | male | 168 | 4545.7 | 4300 |
| year | 2007 | 109 | 4124.5 | 3900 |
| year | 2008 | 114 | 4266.7 | 4200 |
| year | 2009 | 119 | 4210.3 | 4000 |

![body_mass_g by species: median, quartiles and outliers](tasks/eda_1/charts/bm_box_species.png)

- **Species:** Gentoo is much heavier than the other two species. Adelie and Chinstrap are nearly identical.
- **Island:** Biscoe has the highest mean (4716.0 g). All 123 Gentoo penguins are on Biscoe. Within Adelie, the island means are close: Biscoe 3709.7 g (n=44), Dream 3688.4 g (n=56), Torgersen 3706.4 g (n=51). Dream and Torgersen are similar overall.
- **Sex:** Males average 4545.7 g and females 3862.3 g. The female median (3650 g) sits well below the female mean, which points to a right-skewed female distribution. The 9 penguins with body mass present but sex missing have mean 4005.6 g and median 4100 g. They are excluded from the sex comparison.
- **Year:** Mean body mass is stable across 2007, 2008 and 2009. Year shows no clear trend.

### Significance and effect sizes

**Species.** Kruskal-Wallis H = 217.6, p = 5.6e-48, eta-squared from H = 0.64. Group means with 95% CIs:

- Adelie 3700.7 g (3626.9 to 3774.4), n=151
- Chinstrap 3733.1 g (3640.1 to 3826.1), n=68
- Gentoo 5076.0 g (4986.0 to 5166.0), n=123

Pairwise Mann-Whitney tests with Holm adjustment:

- Gentoo vs Adelie: p = 3e-42 raw, 8.9e-42 adjusted.
- Gentoo vs Chinstrap: p = 1.7e-28 raw, 3.3e-28 adjusted.
- Adelie vs Chinstrap: p = 0.485 raw and adjusted.

**Sex.** Welch t = 8.55, p = 4.8e-16. Male mean 4545.7 g (95% CI 4425.7 to 4665.7, n=168); female mean 3862.3 g (95% CI 3759.9 to 3964.7, n=165). The mean difference is 683.4 g (95% CI 526.2 to 840.6), with Cohen's d = 0.94. This comparison is unadjusted across species and may partly reflect species mix. The within-species result is reported under Species × sex below.

**Island.** Kruskal-Wallis H = 130.1, p = 5.7e-29, eta-squared from H = 0.38. Group means with 95% CIs:

- Biscoe 4716.0 g (4596.4 to 4835.6), n=167
- Dream 3712.9 g (3638.8 to 3787.0), n=124
- Torgersen 3706.4 g (3581.2 to 3831.6), n=51

The Biscoe difference largely reflects species mix, since all Gentoo penguins are on Biscoe.

**Year.** Kruskal-Wallis H = 2.55, p = 0.279, eta-squared from H = 0.002. Group means with 95% CIs:

- 2007: 4124.5 g (3974.1 to 4275.0), n=109
- 2008: 4266.7 g (4120.2 to 4413.2), n=114
- 2009: 4210.3 g (4060.9 to 4359.7), n=119

The year effect is not significant.

![Mean body_mass_g with 95% confidence intervals by species, island and sex](tasks/stat_1/charts/stat1_group_means_ci.png)

**Correlations with body mass (all 342 penguins, pooled across species):**

- flipper_length_mm: r = 0.871 (95% CI 0.843 to 0.895), p = 4.4e-107.
- bill_length_mm: r = 0.595 (95% CI 0.522 to 0.660), p = 3.8e-34.
- bill_depth_mm: r = -0.472 (95% CI -0.550 to -0.385), p = 2.3e-20.

### Species × sex interaction and island within species

**Interaction.** Adding species × sex to the additive model (species, sex and island) gives F = 8.71, p = 0.0002 (n=333). The male-minus-female gap therefore differs by species.

Male-minus-female gap within each species (Welch 95% CI; Cohen's d):

- Adelie: 674.7 g (573.0 to 776.3); d = 2.17.
- Chinstrap: 411.8 g (253.7 to 569.8); d = 1.26.
- Gentoo: 805.1 g (697.1 to 913.1); d = 2.70.

The sex gap is large in every species and smallest in Chinstrap.

![Mean body mass (g) for each species within sex, with 95% t confidence intervals (complete cases, n=333)](tasks/stat_2/charts/sex_species_means.png)

Within-cell means with 95% t CIs (complete cases):

- Adelie: female 3368.8 g (n=73, 3306.0 to 3431.7); male 4043.5 g (n=73, 3962.6 to 4124.4).
- Chinstrap: female 3527.2 g (n=34, 3427.6 to 3626.8); male 3939.0 g (n=34, 3812.6 to 4065.3).
- Gentoo: female 4679.7 g (n=58, 4605.7 to 4753.8); male 5484.8 g (n=61, 5404.6 to 5565.0).

**Species × island.** This interaction cannot be tested. Only five species-island cells are observed: Gentoo appears only on Biscoe, and Chinstrap only on Dream. The additive model already fits every observed cell.

**Island within Adelie.** Adelie is the only species present on all three islands. Adjusting for sex, island has no detectable effect within Adelie (F = 0.058, df 2 and 142, p = 0.94). Island effects within Chinstrap and Gentoo cannot be estimated, because each species sits on one island.

### Within-species correlations

All nine within-species correlations with body mass are positive, with p < 0.001 in every case.

- **Adelie** (n=151): bill_length r = 0.549 (95% CI 0.427 to 0.651); bill_depth r = 0.576 (0.459 to 0.674); flipper_length r = 0.468 (0.333 to 0.584).
- **Chinstrap** (n=68): bill_length r = 0.514 (0.314 to 0.670); bill_depth r = 0.604 (0.428 to 0.737); flipper_length r = 0.642 (0.476 to 0.763).
- **Gentoo** (n=123): bill_length r = 0.669 (0.558 to 0.757); bill_depth r = 0.719 (0.621 to 0.795); flipper_length r = 0.703 (0.600 to 0.782).

For flipper length, the pooled correlation (r = 0.871) is stronger than every within-species value (0.468 to 0.703). For bill length, the pooled value (0.595) is above the within-species values for Adelie (0.549) and Chinstrap (0.514), and below Gentoo (0.669). No decomposition of the pooled correlation into within- and between-species parts was computed, so the species contribution is not quantified.

The pooled bill_depth correlation is negative (r = -0.472), but within each species it is positive (Adelie 0.576, Chinstrap 0.604, Gentoo 0.719). The pooled negative sign is consistent with species-level differences rather than a within-species association.

### Predictive power

The analysis used an 80/20 split with seed 42: 273 training and 69 test rows. Sex was recoded as a separate "missing" category. Missing numeric values were imputed with the training median.

| Model | Test MAE (g) | Test RMSE (g) | Test R² | Train R² |
|---|---|---|---|---|
| Mean baseline | 624.0 | 751.7 | — | — |
| Linear regression | 265.7 | 325.7 | 0.812 | 0.884 |
| Gradient boosting | 280.0 | 345.2 | 0.789 | 0.958 |

Gradient boosting overfits more than linear regression (train R² 0.958 against 0.884) and does slightly worse on the test set.

**Permutation importance, linear model (test MAE increase when shuffled, g):** species 342.3, flipper_length_mm 99.1, sex 76.4, bill_depth_mm 43.6, bill_length_mm 22.3, year 1.3, island -0.5.

**Permutation importance, gradient boosting (test MAE increase when shuffled, g):** flipper_length_mm 201.7, species 199.1, sex 85.9, bill_depth_mm 19.0, island 7.5, year 3.1, bill_length_mm -0.6.

![Left: test MAE of the mean baseline, linear regression and gradient boosting for body_mass_g. Right: permutation importance per feature on the test set for both models.](tasks/ml_1/charts/ml1_model_importance.png)

Species is first for the linear model. For gradient boosting, flipper length (201.7 g) and species (199.1 g) are effectively tied, and the report's source calls that near-tie within noise on 69 test rows. Species and flipper length are strongly correlated with each other and with body mass, so their importances share credit and should not be read as independent effects. Year and island contribute almost nothing in either model.

**Grouped permutation importance (50 repeats, seed 42).** Species dummies were shuffled together, and bill and flipper measures were shuffled together.

- Linear model: species 353.0 g; bill_length, bill_depth and flipper_length together 133.3 g; flipper_length alone 105.3 g; sex 73.2 g; island -0.5 g; year 1.0 g. Species remains first.
- Gradient boosting: flipper_length alone 206.6 g; species 200.3 g; bill and flipper measures together 175.4 g; sex 80.3 g; island 7.5 g; year 2.9 g. Flipper length is marginally ahead of species. No interval was computed, so this report does not claim the ordering is noise.

![Grouped permutation importance (increase in test MAE, g) for linear regression and gradient boosting; species dummies and bill/flipper measures are each shuffled together](tasks/ml_2/charts/ml2_grouped_importance.png)

The two models disagree on how much species matters. Species importance is 353.0 g for the linear model and 200.3 g for gradient boosting. The two models also order species and flipper length differently: species first for linear, flipper length first for gradient boosting. The cause of this gap was not tested.

**Refit without species.** The linear model without species dummies gives test MAE 266.7 g and test R² 0.800, against 265.7 g and 0.812 for the full model. A plausible explanation is that island, sex, year and the bill and flipper measures carry overlapping information about species. The refit is consistent with this, but no test of shared information was run.

### Missing values

- **sex:** missing for 11 of 344 penguins (3.2%). By island: Torgersen 9.6% (5 of 52), Biscoe 3.0% (5 of 168), Dream 0.8% (1 of 124). Torgersen against the other islands: Fisher exact OR 5.07, p = 0.0148. This was a post-hoc subgroup comparison among about a dozen tests, so the association is suggestive and needs confirmation in new data. The sex-by-island chi-square (p = 0.0099) is approximate because several expected counts are below 5.

![Percent of penguins with sex missing, by island (n per island in the table)](tasks/eda_2/charts/sex_missing_by_island.png)

- **sex by species and year:** by species, 4.0% Adelie, 0.0% Chinstrap, 4.0% Gentoo (chi-square p = 0.25, approximate). By year, 6.4% in 2007, 0.9% in 2008, 2.5% in 2009 (chi-square p = 0.057, approximate and borderline). Neither association is significant.
- **sex missingness and body mass:** the 9 penguins with sex missing have mean body mass 4005.6 g, against 4207.1 g for the 333 with sex present. The difference is not significant (Welch p = 0.41, Mann-Whitney p = 0.54, d = -0.25). With 9 penguins the test has little power.
- **bill measures and body_mass_g:** each is missing for 2 penguins, and the same 2 rows lack all of them. Missing rates by species, island and year range from 0% to 1.9%. These rates are too small to show a pattern, and the chi-square tests are approximate. Missingness in these columns was not tested against body mass, because no row has a bill measurement missing with body mass present.
- **body_mass_g missingness:** not tested against body mass itself, because the 2 affected rows have no body mass. Its rates by species, island and year (0% to 1.9%) are too small to show a pattern.

## Limitations

- **Small test set.** All prediction results come from one 69-row test split with seed 42. Model rankings were not checked under repeated cross-validation. The gradient boosting near-tie between flipper length and species (201.7 g against 199.1 g) is within the noise that a 69-row set can produce.
- **Gradient boosting was not tuned.** Its gap with the linear model is therefore not established as a property of the method.
- **Two species-importance estimates differ.** The single-feature permutation result (342.3 g, linear) and the grouped result (353.0 g, linear) use different shuffling schemes. The gradient boosting species importance also differs between the two schemes (199.1 g and 200.3 g). The gap between the models (353.0 g against 200.3 g) was not explained.
- **Coefficient magnitudes are not comparable across reports.** The ml_1 and ml_2 linear-model reports list different coefficient magnitudes for the same features (for example, bill_depth_mm). They are not used in this report, and the reason for the difference was not established.
- **Sex missingness and Torgersen.** The clustering of missing sex on Torgersen is post-hoc and needs replication. The sex-by-island chi-square is approximate.
- **Sex-missing rows.** Their 9 penguins with body mass present were excluded from the sex comparison. The sex-gap estimates could be affected by how these rows are handled; this was not tested.
- **Skew and robustness.** The female median sits well below the female mean, indicating skew. Whether a log or robust model changes the sex-gap or interaction results was not tested.
- **Confounding and mediation.** The sex-gap and interaction results are unadjusted for bill and flipper measures, which may mediate the sex effect. Associations are not causal.
- **Island within species.** Island effects within Chinstrap and Gentoo cannot be estimated. The species × island interaction is not estimable.
- **Pooled versus within-species correlations.** The species share of the pooled correlations was not decomposed.
- **Approximate tests.** Several chi-square tests on missingness have expected counts below 5, and several were run among about a dozen tests without multiplicity adjustment.
- **Open review issue (stat_1).** The review asked for 95% CIs for the year group means, and the original year finding stated only that the intervals overlap. The CIs are now quoted above from the stat_1 record. The review issue itself remains open, and the lead's objection to the stat_1 task as written still stands.
- **Failed tasks.** None. All five analysis tasks (eda_1, eda_2, stat_1, stat_2, stat_3) and both ML tasks (ml_1, ml_2) completed.

## Open questions

- Does the sex difference hold within each species after adjusting for bill and flipper measures, which may mediate it?
- Does the female right-skew distort the sex-gap estimates, and would a log or robust model change the species × sex interaction?
- Is the Torgersen concentration of missing sex a recording issue for that island, and does it replicate in a new sample?
- Does imputing sex from island or species change the sex-gap estimate?
- Are the model rankings (species versus flipper length, and the near-tie in gradient boosting) stable under repeated cross-validation?
- Would tuning gradient boosting (depth, learning rate, regularisation) close its gap with the linear model?
- Does a direct test of shared information, such as regressing flipper length on species and the other features, explain why removing species costs little accuracy?
- How much of the pooled bill_length and flipper_length correlations is between-species versus within-species?