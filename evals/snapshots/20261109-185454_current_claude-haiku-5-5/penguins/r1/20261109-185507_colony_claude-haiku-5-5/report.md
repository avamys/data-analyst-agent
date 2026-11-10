# Penguin Body Mass (body_mass_g): Distribution, Group Differences, Correlates and Predictive Performance

## Summary

- **Species is the dominant driver of body mass.** Species explains most of the variation (Kruskal-Wallis H=217.6, p=5.6e-48; H-based eta-squared 0.636). Gentoo averages 5076.0 g, versus 3733.1 g for Chinstrap and 3700.7 g for Adelie. Adelie and Chinstrap do not differ significantly (Holm p=0.49).
- **Sex has a large effect that persists within species.** Males are 683 g heavier than females overall (95% Welch CI 526 to 841 g, Cohen d=0.94). The difference is significant within each species, but its size varies: +675 g in Adelie, +412 g in Chinstrap and +805 g in Gentoo. The species x sex interaction is significant (F=8.76, p=0.00020).
- **Flipper length is the strongest numeric correlate, and much of its association is between species.** Overall Pearson r is 0.871, falling to a partial r of 0.585 after controlling for species. Within species, flipper length, bill length and bill depth remain positively and significantly correlated with mass. Year is not associated with mass, overall or within species.
- **The bill_depth_mm sign reverses between the overall and within-species analyses.** Overall r is -0.472. Within each species it is positive (Adelie 0.576, Chinstrap 0.604, Gentoo 0.719), and the partial r controlling for species is +0.622.
- **Gradient boosting and linear regression both beat the mean-only baseline by a wide margin on one 69-row test split.** Test MAE is 684.2 g for the baseline, 239.8 g for linear regression and 222.0 g for gradient boosting. The gap between the two models is not established by this single split. Species and flipper length are the top two features in both models.

## Data

- **Size:** 344 rows × 8 columns.
- **Target:** body_mass_g (regression).
- **Features:** numeric: bill_length_mm, bill_depth_mm, flipper_length_mm, year. Categorical: species, island, sex. No date/time features and no identifier or free-text columns.
- **Missing values:**
  - bill_length_mm, bill_depth_mm, flipper_length_mm and body_mass_g: 0.6% each (2 rows each).
  - sex: 3.2% (11 rows).
  - species, island and year: none.
- **Analysis bases:** body_mass_g analyses use n=342. Analyses involving sex use n=333 (rows with recorded sex and mass). Model results use a single stratified 80/20 split (273 train, 69 test).

## Findings

### Distribution of body mass and missingness

**Overall distribution.** body_mass_g (n=342) has a mean of 4201.8 g, median 4050 g, SD 802.0 g and range 2700 to 6300 g, with mild right skew (0.47). No values fall beyond the 3-SD rule or the 1.5×IQR fences (1750 to 6550 g).

![body_mass_g histogram and boxplot per species (counts of penguins)](tasks/eda_1/charts/bm_species_hist_box.png)

**By species.** Gentoo is much heavier than the other two species:

| Species | n | Mean (g) | Median (g) | SD (g) |
|---|---|---|---|---|
| Gentoo | 123 | 5076.0 | 5000 | 504.1 |
| Chinstrap | 68 | 3733.1 | 3700 | 384.3 |
| Adelie | 151 | 3700.7 | 3700 | 458.6 |

Within-species SDs (384 to 504 g) are narrower than the overall SD. Within-species skews are 0.29 (Adelie), 0.25 (Chinstrap) and 0.07 (Gentoo), smaller than the overall 0.47. Mixing species with different means probably contributes to the overall skew, but this was not formally decomposed.

**By island and species composition.** Island composition does not mirror species. Biscoe holds 123 Gentoo and 44 Adelie, Dream holds 68 Chinstrap and 56 Adelie, and Torgersen holds 51 Adelie. Within Adelie, mean mass is 3709.7 g on Biscoe, 3688.4 g on Dream and 3706.4 g on Torgersen. The higher Biscoe mean (4716.0 g, median 4775, n=167) therefore reflects Gentoo composition rather than the island itself. See the island section below for the test.

**By sex.** Males average 4545.7 g (median 4300, n=168) and females 3862.3 g (median 3650, n=165). Nine penguins with missing sex average 4005.6 g.

**By year.** Means are 4124.5 g (2007, n=109), 4266.7 g (2008, n=114) and 4210.3 g (2009, n=119). Medians are 3900, 4200 and 4000 g. The year effect is tested in the statistics section.

![Boxplots of body_mass_g (grams) by species, sex and year; penguins with missing sex excluded from the sex panel](tasks/stat_1/charts/stat1_bodymass_by_factor.png)

**Missingness.** Missing values occur only in the four numeric columns and sex. Sex is missing for 11 rows (3.2%). Those 11 rows are the same rows that lack any of bill_length_mm, bill_depth_mm, flipper_length_mm or sex.

- Sex missingness by species: Adelie 3.95%, Gentoo 4.03%, Chinstrap 0.0%.
- Sex missingness by island: Torgersen 9.62%, Biscoe 2.98%, Dream 0.81%. The Torgersen share rests on very few rows.

![Percent of rows with sex missing, grouped by island (all species)](tasks/eda_2/charts/sex_missing_by_island.png)

Incomplete rows have a mean mass of 4005.6 g (n=9 with recorded mass), against 4207.1 g for complete rows (n=333). Incomplete rows are compositionally different: they are 54.5% Adelie and 45.5% Gentoo, with no Chinstrap, against 43.8%, 35.7% and 20.4% among complete rows. Incomplete rows by year: 7 of 110 in 2007 (6.4%), 1 of 114 in 2008 (0.9%) and 3 of 120 in 2009 (2.5%). No significance test was run for any missingness pattern, so these are descriptive only.

### Statistical tests and effect sizes

**Species.** The omnibus tests are Kruskal-Wallis H=217.6 (p=5.6e-48) and ANOVA F=343.6 (p=2.9e-82), with H-based eta-squared 0.636 (n=342). Pairwise Mann-Whitney tests with Holm correction:

| Comparison | Mean difference (g) | Cohen d | Holm p | Significant |
|---|---|---|---|---|
| Gentoo vs Adelie | -1375 | -2.87 | 8.9e-42 | Yes |
| Gentoo vs Chinstrap | -1343 | -2.89 | 3.3e-28 | Yes |
| Adelie vs Chinstrap | -32 | -0.07 | 0.49 | No |

**Island.** The omnibus tests are Kruskal-Wallis H=130.1 (p=5.7e-29) and ANOVA F=110.0 (p=1.5e-37), with H-based eta-squared 0.378. This effect is largely confounded with species composition, since all Gentoo penguins are on Biscoe.

**Sex.** Males are heavier than females by 683 g (95% Welch CI 526 to 841 g; Welch p=4.8e-16; Mann-Whitney p=1.8e-15; Cohen d=0.94; H-based eta-squared 0.188, n=333).

Within each species, the male-female difference is significant:

| Species | Male minus female (g) | Cohen d | Mann-Whitney p | n (male/female) |
|---|---|---|---|---|
| Adelie | 675 | 2.17 | 3.1e-20 | 73/73 |
| Chinstrap | 412 | 1.26 | 5.3e-06 | 34/34 |
| Gentoo | 805 | 2.70 | 2.2e-19 | 61/58 |

**Year.** No significant effect: Kruskal-Wallis H=2.55 (p=0.28), ANOVA F=0.88 (p=0.41), eta-squared 0.002. The 2007 vs 2008 gap of 142 g has Holm-corrected p=0.31. The 2007 vs 2009 and 2008 vs 2009 comparisons are also not significant (Holm p=0.87 for both).

### Numeric correlates of body mass

**Overall (n=342).**

| Feature | Pearson r (95% CI) | Pearson p | Spearman rho | Spearman p |
|---|---|---|---|---|
| flipper_length_mm | 0.871 (0.843 to 0.895) | 4.4e-107 | 0.840 | 2.8e-92 |
| bill_length_mm | 0.595 (0.522 to 0.660) | 3.8e-34 | 0.584 | 1.3e-32 |
| bill_depth_mm | -0.472 (-0.550 to -0.385) | 2.3e-20 | -0.432 | 5.2e-17 |
| year | 0.042 (-0.064 to 0.148) | 0.44 | 0.041 | 0.46 |

**Within species.**

| Species (n) | bill_length_mm r | bill_depth_mm r | flipper_length_mm r | year r |
|---|---|---|---|---|
| Adelie (151) | 0.549 | 0.576 | 0.468 | -0.029 (p=0.72) |
| Chinstrap (68) | 0.514 | 0.604 | 0.642 | 0.037 (p=0.77) |
| Gentoo (123) | 0.669 | 0.719 | 0.703 | 0.061 (p=0.50) |

Within species, bill_length_mm, bill_depth_mm and flipper_length_mm correlations are positive and significant in all nine tests. Year is not significant in any species. The overall flipper_length_mm r (0.871) is higher than every within-species value (0.468 to 0.703). The report does not test why, but pooling species with different masses probably inflates the overall value.

**Partial correlations controlling for species (n=342).**

| Feature | Partial r (95% CI) | p |
|---|---|---|
| bill_depth_mm | 0.622 (0.552 to 0.683) | 8.1e-38 |
| bill_length_mm | 0.585 (0.511 to 0.651) | 1.2e-32 |
| flipper_length_mm | 0.585 (0.510 to 0.651) | 1.4e-32 |
| year | 0.017 (-0.090 to 0.123) | 0.76 |

The bill_depth_mm sign reverses after controlling for species, which matches the positive within-species correlations. Flipper length's partial r (0.585) is well below its overall r (0.871), so species accounts for much of its overall association. Bill length barely changes (0.595 overall, 0.585 partial).

**Spearman confidence intervals (approximate, Fisher z, SE sqrt(1.06/(n-3))).** Overall: bill_length_mm 0.584 (0.507 to 0.651), bill_depth_mm -0.432 (-0.517 to -0.339), flipper_length_mm 0.840 (0.805 to 0.869), year 0.041 (-0.069 to 0.149). Within species, bill_depth_mm only: Adelie 0.596 (0.478 to 0.692), Chinstrap 0.579 (0.389 to 0.722), Gentoo 0.755 (0.665 to 0.824).

![Left: body_mass_g against flipper_length_mm by species with OLS line per species. Right: male minus female mean body_mass_g within each species with 95% Welch CI.](tasks/stat_3/charts/stat3_sex_and_slope_by_species.png)

### Interactions: species with sex and with flipper length

- **Species x sex:** nested OLS F=8.76 (df 2, 327), p=0.00020 (n=333). The sex difference differs by species (see the table in the statistics section and Welch CIs below).
- **Species x flipper length:** nested OLS F=5.35 (df 2, 327), p=0.0052 (n=333). The flipper slope differs by species.

Male-female differences with 95% Welch CIs: Adelie +675 g (573 to 776, Welch p=6.4e-26), Chinstrap +412 g (254 to 570, Welch p=2.3e-06), Gentoo +805 g (697 to 913, Welch p=1.9e-28). All three are significant.

Flipper-length slopes (g per mm) within each species:

| Species | Slope (g/mm) | 95% CI | r | n |
|---|---|---|---|---|
| Adelie | 32.7 | 22.4 to 42.9 | 0.46 | 146 |
| Chinstrap | 34.6 | 24.4 to 44.7 | 0.64 | 68 |
| Gentoo | 54.2 | 44.4 to 64.0 | 0.71 | 119 |

Slopes are positive in every species, and Gentoo's is steepest. The Adelie and Gentoo n values here (146 and 119) differ from the correlation analysis (151 and 123); the report does not reconcile these counts.

### Predictive models

On one stratified 80/20 split (seed 42; 273 train, 69 test rows):

| Model | Test MAE (g) | Test RMSE (g) | Test R² |
|---|---|---|---|
| Mean-only baseline | 684.2 | 809.5 | -0.002 |
| Linear regression | 239.8 | 291.0 | 0.871 |
| Gradient boosting | 222.0 | 270.7 | 0.888 |

Both models cut baseline MAE by about two-thirds. Gradient boosting has the lower test MAE. This is a single 69-row test split with no interval, so that difference is not established as a real one. Gradient boosting's training R² is 0.950 against a test R² of 0.888, a larger gap than linear regression's (0.866 vs 0.871).

**Gradient boosting permutation importance** (mean increase in test MAE over 30 shuffles): species 275.3 g, flipper_length_mm 157.3 g, sex 50.6 g, bill_depth_mm 47.4 g, bill_length_mm 31.5 g, island 14.3 g, year 8.9 g.

**Linear regression permutation importance** (same procedure): species 320.5 g, flipper_length_mm 149.1 g, bill_depth_mm 57.1 g, sex 40.1 g, bill_length_mm 21.3 g, year 5.3 g. Island is -4.5 g, meaning shuffling it slightly lowered test MAE. This is noise, not evidence that island contributes nothing.

The two models agree on the top two features (species, flipper_length_mm). They disagree on the third: sex for gradient boosting (50.6 g) and bill_depth_mm for linear regression (57.1 g). Ranks below the top two are not reliably ordered, since each importance comes from one 69-row test set with no spread reported.

![Permutation importance of each raw input column for the gradient boosting model predicting body_mass_g: increase in test MAE in grams when that column is shuffled (sign corrected).](tasks/ml_1/charts/ml1_perm_importance_gbr_fixed.png)

### Island after species composition

Within Adelie, the only species present on all three islands, mean mass is 3709.7 g on Biscoe (median 3750, n=44), 3688.4 g on Dream (median 3575, n=56) and 3706.4 g on Torgersen (median 3700, n=51). A one-way ANOVA gives F=0.032, p=0.968. The Biscoe excess is consistent with Gentoo's presence on Biscoe. Gentoo (mean 5076.0 g, median 5000, n=123) appears only on Biscoe, and Chinstrap (mean 3733.1 g, n=68) only on Dream. Neither can be compared across islands, so an island effect on Gentoo or Chinstrap mass cannot be ruled out.

![Mean body_mass_g per species, grouped by island](tasks/eda_3/charts/bm_species_island_means_eda3.png)

## Limitations

- **Unresolved review issue: Spearman confidence intervals.** The brief requires 95% CIs for Spearman rho for every numeric feature, overall and within each species. Only partly addressed:
  - stat_4 gives approximate Fisher-z CIs for overall rho for all four numeric features, and within species for bill_depth_mm only.
  - Within-species Spearman CIs for bill_length_mm, flipper_length_mm and year are still missing. The within-species Spearman results for those features are reported without intervals (stat_2).
  - The stat_4 CIs use an approximate SE, sqrt(1.06/(n-3)).
- **No multiple-comparison correction in stat_2.** The 16 Pearson and 16 Spearman tests were reported unadjusted. All non-year p-values are far below the Bonferroni-corrected threshold for 16 tests. The Pearson year p-values (0.44 to 0.77) are far above it.
- **Confounding by species and island.** Island effects are largely species composition (Gentoo only on Biscoe, Chinstrap only on Dream). Overall correlations are inflated or reversed by pooling species; the bill_depth_mm sign reversal is the clearest case.
- **Missingness not tested.** The island, species and year patterns in missing sex were tabulated only. No Fisher or chi-square test was run. With 11 affected rows, these are hypotheses. The 9 penguins with missing sex have mean mass 4005.6 g, but that rests on 9 rows and no test was run.
- **Skew decomposition not formally done.** The claim that mixing species contributes to the overall skew is not tested.
- **Model results rest on one split.** The 69-row test set has no interval, no repeated splits and no cross-validation. Permutation importances have no spread. The gradient boosting versus linear regression gap is not established.
- **Count inconsistencies across tasks.** Within-species n values for flipper slopes (stat_3: 146 and 119) differ from those in the correlation analysis (stat_2: 151 and 123). Year counts also differ between eda_1 (n=342) and eda_2 (n=344 basis). These were reported as produced and not reconciled.
- **Sex-test p-values differ by method.** Within-species sex differences have Mann-Whitney p-values in stat_1 and Welch p-values in stat_3. Both are reported as produced.
- **Failed tasks:** none. All eight accepted tasks are complete.

**Numbers not traced to a recorded fact.** The automatic check found no recorded value for these numbers:
- 2.5% in: "Incomplete rows have a mean mass of 4005.6 g (n=9 with recorded mass), against 4207.1 g for complete rows (n=333). Incomplete rows are compositionally different"

## Open questions

- Does sex still explain body mass after adjusting for species and flipper length together? stat_3 raised this but did not test it.
- Does the species x sex interaction hold after adjusting for flipper length and island together?
- Is the Gentoo flipper slope robust to including sex as a covariate?
- Do partial Spearman correlations (controlling for species) match the partial Pearson results, given possible outliers or nonlinearity? Do the species-by-feature slopes differ, which would undermine the common-slope assumption behind partial correlations?
- Does the species x flipper length interaction explain why gradient boosting outperforms linear regression on test MAE?
- Do the feature rankings and the model gap hold across repeated splits or cross-validation, giving intervals?
- Is island redundant once species is known? Linear regression's near-zero island importance is not a finding of no contribution.
- Is the 2007 to 2008 year difference significant within species?
- Is sex missingness associated with island, species or year under a formal test? Does the Torgersen concentration reflect a collection or recording issue?
- What drives the nine penguins with missing sex, and does their body mass match the other groups?
- Is the island effect on Gentoo and Chinstrap mass testable, given that each species occurs on only one island?