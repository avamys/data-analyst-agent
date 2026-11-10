# Penguin Dataset: Body Mass (body_mass_g) Analysis Report

## Summary

- **Species drives most of the body-mass variation.** Gentoo penguins average 5076 g, while Adelie (3700.7 g) and Chinstrap (3733.1 g) are close to each other. Species alone gives a Kruskal-Wallis H of 217.6 (p=5.6e-48). In the random forest, shuffling the species columns together lowers test R² by 0.745.
- **Sex matters, but its size depends on species.** Males are heavier than females overall (Mann-Whitney r=0.44). The species × sex interaction is significant (F=10.55, p=3.6e-5). Holding flipper length fixed within species, the male-female gap is 599 g in Adelie, 194 g in Chinstrap and 598 g in Gentoo.
- **Body mass is well predicted relative to a mean baseline.** On a single 69-row test set, the random forest reaches RMSE 285.1 g and R² 0.876, and linear regression reaches RMSE 289.9 g and R² 0.872. The mean baseline RMSE is 809.5 g. The difference between the two models is within noise.
- **Island and year differences are not separated from species.** Biscoe's higher mean coincides with its Gentoo share (73.8%). Excluding Gentoo, the island means lie between 3706 and 3713 g. Year is not significantly related to body mass (Kruskal-Wallis p=0.279).
- **Missingness is small, with one suggestive pattern.** Only 11 rows (3.2%) lack sex. Sex missingness is associated with island (permutation p=0.0093, Holm-adjusted p=0.028). This rests on 11 rows and small expected counts, so it is suggestive only.

## Data

- **Size:** 344 rows × 8 columns.
- **Target:** body_mass_g (regression). Overall mean 4201.8 g, median 4050 g, SD 801.95 g, range 2700 to 6300 g, across 342 non-missing rows.
- **Numeric features:** bill_length_mm, bill_depth_mm, flipper_length_mm, year.
- **Categorical features:** species, island, sex.
- **Date/time features and identifier or free-text columns:** none.
- **Missing values:**
  - body_mass_g, bill_length_mm, bill_depth_mm and flipper_length_mm: 2 rows each (0.58%).
  - sex: 11 rows (3.2%).
  - species, island and year: none.

## Findings

### Body mass distribution and group differences

Species, island and sex were each tested against body mass with Kruskal-Wallis tests. These are one-factor tests that are not adjusted for each other.

- **Species:** Gentoo mean 5076 g (median 5000, n=123). Adelie mean 3700.7 g (median 3700, n=151). Chinstrap mean 3733.1 g (median 3700, n=68). Kruskal-Wallis H=217.6, df=2, p=5.6e-48, epsilon²=0.636. Gentoo is heavier than Adelie (r=0.82) and Chinstrap (r=0.80). Adelie and Chinstrap do not differ (Holm p=0.49, r=0.05).

  ![Box plot of body_mass_g by species (missing body mass excluded)](tasks/eda_1/charts/body_mass_by_species_box.png)

- **Island:** Biscoe mean 4716 g (median 4775, n=167). Dream mean 3712.9 g (median 3687.5, n=124). Torgersen mean 3706.4 g (median 3700, n=51). Kruskal-Wallis H=130.1, df=2, p=5.7e-29, epsilon²=0.378. Biscoe differs from Dream (r=0.61) and from Torgersen (r=0.52). Dream and Torgersen do not differ (Holm p=0.81, r=0.02).
  - Island and species are confounded: Biscoe holds 124 Gentoo and 44 Adelie rows, Dream holds 56 Adelie and 68 Chinstrap rows, and Torgersen holds 52 Adelie rows only. The island effect therefore cannot be read as independent of species.
  - Descriptive split by species within island: on Biscoe, Gentoo rows average 5076.0 g (n=123) and non-Gentoo rows average 3709.7 g (n=44). Non-Gentoo means are 3712.9 g on Dream (n=124) and 3706.4 g on Torgersen (n=51). Excluding Gentoo, the three islands' means lie within about 7 g of one another (3706 to 3713 g). These are descriptive values and are not adjusted for sex.

- **Sex:** Male mean 4545.7 g (median 4300, n=168). Female mean 3862.3 g (median 3650, n=165). Rows with missing sex but observed mass: mean 4005.6 g (n=9). Kruskal-Wallis H=63.3, df=1, p=1.8e-15, epsilon²=0.188 (n=333). Mann-Whitney r=0.44.

- **Year:** Means by year are 4124.5 g (2007), 4266.7 g (2008) and 4210.3 g (2009). Medians are 3900, 4200 and 4000 g. Kruskal-Wallis H=2.55, df=2, p=0.279, epsilon²=0.0016 (n=342). Pairwise Mann-Whitney tests with Holm correction are all non-significant (Holm p≥0.31, r≤0.11). These year values are not adjusted for species or island.

### Pooled numeric correlations with body mass

These correlations are pooled across species and unadjusted.

- flipper_length_mm: Spearman ρ=0.84 (95% CI 0.81 to 0.87); Pearson r=0.87.
- bill_length_mm: Spearman ρ=0.58 (95% CI 0.51 to 0.65); Pearson r=0.60.
- bill_depth_mm: Spearman ρ=−0.43 (95% CI −0.51 to −0.34); Pearson r=−0.47.

Because species differs strongly in both body mass and bill depth, these pooled values mix between-species and within-species association. The negative bill-depth correlation may be driven by species composition. This has not been checked within species.

  ![Flipper length against body mass, one point per penguin, colored by species](tasks/stat_1/charts/flipper_vs_mass.png)

### Missingness

- **Measurement columns:** bill_length_mm, bill_depth_mm, flipper_length_mm and body_mass_g are each missing in the same 2 rows (0.58%): an Adelie on Torgersen in 2007 and a Gentoo on Biscoe in 2009. Group rates rest on 2 rows each and are not informative about any pattern.
- **Sex missingness by species:** Adelie 3.95%, Chinstrap 0%, Gentoo 4.03%. Chi-square p=0.25, which is unreliable given the small expected counts. Permutation p=0.256.
- **Sex missingness by island:** Biscoe 2.98%, Dream 0.81%, Torgersen 9.62%. Chi-square p=0.0099. Permutation p=0.0093 (20000 shuffles). Holm-adjusted p=0.028. Minimum expected count is 1.66.
- **Sex missingness by year:** 2007 6.36%, 2008 0.88%, 2009 2.5%. Chi-square p=0.057. Permutation p=0.052. Holm-adjusted p=0.103, so it does not survive correction.
- **Body mass and missing sex:** among rows with observed mass, the 9 rows with missing sex average 4005.6 g against 4207.1 g for the rest. The difference is −201.5 g (Welch p=0.41, Mann-Whitney p=0.54). Nine rows give little power.
- **Body mass and missing measurements:** the 2 rows missing bill or flipper measurements have no observed body mass, so no comparison is possible.

  ![Percent of rows with missing sex, by island](tasks/eda_2/charts/sex_missing_by_island.png)

### Species, island and sex interactions

Analysis sample: 333 complete rows on species, sex, flipper_length_mm and body_mass_g. The 11 excluded rows are the 11 rows with missing sex. The 2 rows missing flipper_length_mm or body_mass_g are among these 11, so the exclusions overlap and the total excluded is 11 (344 minus 333), not 11 plus 2.

- **Species × sex:** adding the interaction to the additive model (species, sex, common flipper slope) gives F=10.55, df=2, p=3.6e-5. Raw cell means, unadjusted for flipper length:

  | Species | Female mean (g), n | Male mean (g), n |
  |---|---|---|
  | Adelie | 3368.8, n=73 | 4043.5, n=73 |
  | Chinstrap | 3527.2, n=34 | 3939.0, n=34 |
  | Gentoo | 4679.7, n=58 | 5484.8, n=61 |

  ![Mean body mass (g) for each species-by-sex cell](tasks/stat_2/charts/cell_means_species_sex.png)

- **Flipper slopes within species, adjusted for sex:**
  - Adelie 16.3 g/mm (95% CI 8.4 to 24.3).
  - Chinstrap 26.7 g/mm (95% CI 14.6 to 38.8).
  - Gentoo 23.5 g/mm (95% CI 13.2 to 33.8).

  These intervals overlap. The unadjusted within-species slopes (Adelie 32.7, Chinstrap 34.6, Gentoo 54.2 g/mm) are pooled over sex and are not the within-sex flipper effect.
- **Male-female gap holding flipper length fixed:** Adelie 599 g (p=5e-22), Chinstrap 194 g (p=0.027), Gentoo 598 g (p=2e-14). The Chinstrap gap is much smaller than the other two, but its sample is n=68.
- **Species × flipper slope:** adding it to the model that already includes species × sex gives F=1.25, df=2, p=0.29. Species does not significantly change the slope. The per-species slopes are descriptive, and this omnibus test is the inferential comparison.

### Predictive models

All models use one 80/20 split stratified by species (random_state 42): 273 training rows and 69 test rows, with 13 features. The feature table one-hot encodes species, island and sex. Sex missingness is kept as its own sex_unknown column, so the 9 modelling rows with unknown sex remain. Imputation was fitted on training rows only, but it filled 0 values because the only missing numeric values were in the 2 rows already dropped.

| Model | Test RMSE (g) | Test MAE (g) | Test R² | Train R² |
|---|---|---|---|---|
| Mean baseline | 809.5 | 684.2 | −0.002 | 0.0 |
| Linear regression | 289.9 | 238.6 | 0.872 | 0.874 |
| Random forest (500 trees) | 285.1 | 232.0 | 0.876 | 0.979 |

- Both models cut baseline RMSE by about two thirds.
- The random forest's train R² of 0.979 against test R² of 0.876 shows overfitting relative to test. The difference between the two models on RMSE and R² is within noise on 69 rows, and no interval is given for it.
- Linear regression's largest absolute coefficients are species_Gentoo (684.6), species_Chinstrap (457.8), sex_male (278.4) and species_Adelie (226.7).

**Feature importance (random forest, test set, 30 repeats).** Grouped importance is the appropriate measure for multi-level features:

| Group | Mean drop in test R² | SD |
|---|---|---|
| Species | 0.745 | 0.109 |
| Sex (including sex_unknown) | 0.155 | 0.033 |
| flipper_length_mm | 0.100 | 0.027 |
| Island | 0.009 | 0.005 |
| Year | 0.006 | 0.007 |

Per-column importances are contrasts against a reference level, not whole features. species_Gentoo drops R² by 0.751 (SD 0.096), sex_male by 0.127 (SD 0.029), and island_Biscoe by 0.007 (SD 0.004). Among numeric features, flipper_length_mm drops R² by 0.101, bill_depth_mm by 0.039 and bill_length_mm by 0.014. Permutation importance for sex_unknown was not computed separately.

  ![Permutation importance of features for the random forest predicting body_mass_g on the test set. Bars show the mean drop in R2 when each feature is shuffled.](tasks/ml_2/charts/ml2_perm_importance.png)

## Limitations

- **Unresolved review issue (sample description, stat_2):** the 2 rows missing flipper_length_mm or body_mass_g are among the 11 rows with missing sex, so the exclusions overlap. The total excluded is 11 (344 minus 333 complete rows), not 11 plus 2. This correction affects the stated analysis sample in the stat_2 findings. The other stat_2 numbers stand as recorded.
- **Small samples for missingness:** sex missingness totals 11 rows. Expected counts are small (minimum 1.66 to 3.52). The chi-square p-values are unreliable, and the permutation p-values are approximate. The permutation test uses the chi-square statistic, not the Fisher-Freeman-Halton statistic. The island association is suggestive and should be confirmed with more data. The year association does not survive correction.
- **Measurement missingness:** each measurement-column rate rests on 2 rows, so no pattern can be inferred.
- **Confounding:** species, island and sex are unbalanced across one another. The island and year comparisons are unadjusted, and the pooled correlations mix within- and between-species association. The bill-depth result is not verified within species.
- **Sex-gap precision:** the Chinstrap adjusted gap (194 g) rests on n=68, and the sex-adjusted flipper slopes have overlapping intervals.
- **Model evaluation:** the test set has only 69 rows. Test R² and RMSE differences between the random forest and linear regression are within noise, and no repeated cross-validation was run. The random forest is overfitted, and no tuning was done. Per-column importance understates multi-level features, and sex_unknown's permutation importance was not computed separately.
- **Imputation:** the 11 missing sex values were not imputed, so the sex comparisons use the complete rows.
- **Failed tasks:** none. All tasks were marked complete.

## Open questions

- Do the species-specific sex differences hold when the 11 missing-sex values are imputed from species, island and body mass? Would imputation change the sex comparison?
- Is the Biscoe-Dream island difference explained by species composition once species and sex are controlled?
- Do the year differences persist once species composition is held fixed?
- Do the correlations of bill length, bill depth and flipper length with body mass hold within each species, with confidence intervals?
- Is the small Chinstrap male-female gap (194 g adjusted) a sample-size artefact (n=68) or a real species difference?
- Are the sex-missing rows on Torgersen different from other islands in species or year, which could confound the island association?
- Would Fisher-Freeman-Halton tests confirm the island and year associations with sex missingness?
- Would a model using only species, sex and flipper_length_mm perform as well as the full 13-feature model?
- Does tuning the random forest (depth, minimum leaf size) change the feature ranking?
- Would repeated cross-validation give confidence intervals for the RMSE and R² gap between linear regression and the random forest?