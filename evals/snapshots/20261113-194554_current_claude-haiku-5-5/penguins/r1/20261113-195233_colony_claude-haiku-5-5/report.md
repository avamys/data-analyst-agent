# Penguin Body Mass (body_mass_g): Species, Sex, Island and Year Effects, with Predictive Models

## Summary

- **Species is the dominant factor.** Gentoo penguins average 5076.0 g, against 3700.7 g for Adelie and 3733.1 g for Chinstrap. Species explains a large share of variance (Kruskal-Wallis eta squared 0.67, p=5.6e-48). Adelie and Chinstrap do not differ significantly (Holm p=0.49).
- **Sex matters, but its size depends on species.** Males average 4545.7 g and females 3862.3 g (Welch difference 683.4 g). The within-species gap is smaller in Chinstrap (411.8 g) than in Adelie (674.7 g) and Gentoo (805.1 g). The species-by-sex interaction is significant (p=0.0002) but adds little explained variance (R-squared 0.847 to 0.855).
- **Island and year show no effect once species is considered.** The unadjusted Biscoe excess (1003.1 g over Dream and 1009.6 g over Torgersen) is confounded with the Gentoo share. Within Adelie, the only species present on all three islands, island is negligible (p=0.968). Year is not significant (p=0.28).
- **A linear model predicts mass well against a mean-only baseline.** On a 69-penguin test set it achieves MAE 255.2 g and R-squared 0.827, against 624.0 g and -0.002 for the baseline. Species is the most important feature, and year adds essentially nothing.

## Data

- **Size:** 344 rows × 8 columns. The analysis used 342 penguins with a recorded body mass.
- **Target:** body_mass_g (regression).
- **Numeric features:** bill_length_mm, bill_depth_mm, flipper_length_mm, year.
- **Categorical features:** species, island, sex.
- **Date/time and identifier features:** none.
- **Missing values:**
  - sex: 3.2% (11 of 344 rows).
  - bill_length_mm, bill_depth_mm, flipper_length_mm and body_mass_g: 0.6% each (2 of 344 rows). These are the same two rows, which lack all four measurements.
  - species, island and year: none.

## Findings

### 1. Body mass distribution and per-group means

Over the 342 penguins with a recorded mass, body_mass_g has a mean of 4201.8 g, a median of 4050 g, an SD of 801.95 g and a range of 2700 to 6300 g.

Per-species means show that Gentoo is much heavier than the other two species:

| Species | n | Mean (g) | Median (g) |
|---|---|---|---|
| Adelie | 151 | 3700.7 | 3700 |
| Chinstrap | 68 | 3733.1 | 3700 |
| Gentoo | 123 | 5076.0 | 5000 |

![Boxplot of body_mass_g per species](tasks/eda_1/charts/mass_by_species.png)

Per-island and per-year means are below. Both are unadjusted; see Section 4 for the island comparison within species.

| Island | n | Mean (g) | Median (g) |
|---|---|---|---|
| Biscoe | 167 | 4716.0 | 4775 |
| Dream | 124 | 3712.9 | 3687.5 |
| Torgersen | 51 | 3706.4 | 3700 |

| Year | n | Mean (g) | Median (g) |
|---|---|---|---|
| 2007 | 109 | 4124.5 | 3900 |
| 2008 | 114 | 4266.7 | 4200 |
| 2009 | 119 | 4210.3 | 4000 |

Sex means are: female 3862.3 g (n=165, median 3650 g), male 4545.7 g (n=168, median 4300 g), and missing sex 4005.6 g (n=9, median 4100 g).

### 2. Significance tests and effect sizes

**Species.** The Kruskal-Wallis test is highly significant (H=217.6, p=5.6e-48, eta squared 0.67). Pairwise Mann-Whitney tests with Holm adjustment give the following. Differences are first minus second, and the intervals are unadjusted Welch 95% CIs.

- Adelie minus Gentoo: -1375.4 g (95% CI -1491.2 to -1259.5), Holm p=8.9e-42. Gentoo is heavier.
- Chinstrap minus Gentoo: -1342.9 g (95% CI -1471.4 to -1214.4), Holm p=3.3e-28. Gentoo is heavier.
- Adelie minus Chinstrap: -32.4 g (95% CI -150.4 to 85.5), Holm p=0.49. No significant difference.

No omnibus confidence interval was computed for species.

**Island.** The Kruskal-Wallis test is significant (H=130.1, p=5.7e-29, eta squared 0.39). This is unadjusted for species.

- Biscoe minus Dream: 1003.1 g (95% CI 862.9 to 1143.3), Holm-adjusted Mann-Whitney p=6.9e-25.
- Biscoe minus Torgersen: 1009.6 g (95% CI 837.9 to 1181.4), p=2.8e-14.
- Dream minus Torgersen: 6.5 g (95% CI -137.9 to 151.0), p=0.81.

**Sex.** The difference is significant (Mann-Whitney p=1.8e-15, Cohen d=0.94). Males minus females is 683.4 g (95% CI 526.2 to 840.6). The 9 rows with missing sex are excluded. This comparison is not adjusted for species.

**Year.** The Kruskal-Wallis test is not significant (H=2.55, p=0.28, eta squared 0.005). Pairwise differences are all non-significant after Holm correction:

- 2007 minus 2008: -142.1 g (95% CI -351.0 to 66.7), p=0.31.
- 2007 minus 2009: -85.8 g (95% CI -296.6 to 125.1), p=0.87.
- 2008 minus 2009: 56.4 g (95% CI -151.7 to 264.5), p=0.87.

### 3. Does species moderate the sex effect?

Yes, the sex gap differs by species. Within-species Welch differences (male minus female):

| Species | Difference (g) | 95% CI (g) | p | Males / females |
|---|---|---|---|---|
| Adelie | 674.7 | 573.0 to 776.3 | 6.4e-26 | 73 / 73 |
| Chinstrap | 411.8 | 253.7 to 569.8 | 2.3e-6 | 34 / 34 |
| Gentoo | 805.1 | 697.1 to 913.1 | 1.9e-28 | 61 / 58 |

![Mean body_mass_g for female and male penguins within each species](tasks/stat_2/charts/sex_gap_by_species.png)

Gentoo and Adelie have overlapping intervals, so their gaps are not clearly different. Chinstrap is clearly smaller than the other two only in the sense that its interval does not overlap them; this is not a formal pairwise test.

The two-way OLS model shows a significant species-by-sex interaction (F=8.76, df 2 and 327, p=0.0002). Adding it raises R-squared only from 0.847 to 0.855. The omnibus test does not identify which species pairs differ. The analysis recommends quoting the sex gap per species (roughly 412 to 805 g) rather than the pooled 683 g.

The per-species gaps are unadjusted for island, and their p-values are not multiplicity-adjusted.

### 4. Island within species

Chinstrap appears only on Dream and Gentoo only on Biscoe, so neither species contributes a within-species island contrast. Adelie is the only species on all three islands.

Within Adelie, body mass does not differ by island:

| Adelie island | n | Mean (g) | Median (g) |
|---|---|---|---|
| Biscoe | 44 | 3709.7 | 3750 |
| Dream | 56 | 3688.4 | 3575 |
| Torgersen | 51 | 3706.4 | 3700 |

One-way ANOVA gives F=0.032, p=0.968. Kruskal-Wallis gives p=0.920, with eta squared 0.0004.

The species-adjusted additive OLS gives Dream minus Biscoe of -21.3 g (p=0.820) and Torgersen minus Biscoe of -3.3 g (p=0.973). The overall island term has p=0.969. The Dream estimate equals the Adelie Biscoe-versus-Dream difference (Welch t=0.22, p=0.824).

These adjusted estimates rest on the additive assumption of no species-by-island interaction, which cannot be tested for Chinstrap or Gentoo. The Biscoe excess should not be read as a clean island effect.

### 5. Correlations with bill and flipper measures

Pooled correlations with body_mass_g:

- flipper_length_mm: r=0.871 (p=4.4e-107).
- bill_length_mm: r=0.595 (p=3.8e-34).
- bill_depth_mm: r=-0.472 (p=2.3e-20).

These pooled correlations may partly reflect species size differences. Within each species, the picture differs.

| Species | n | Flipper r | Bill length r | Bill depth r |
|---|---|---|---|---|
| Adelie | 151 | 0.468 | 0.549 | 0.576 |
| Chinstrap | 68 | 0.642 | 0.514 | 0.605 |
| Gentoo | 123 | 0.703 | 0.669 | 0.719 |

![Scatter of body mass against flipper length, coloured by species](tasks/eda_3/charts/eda3_mass_vs_flipper_by_species.png)

- **Flipper:** most of the pooled correlation reflects between-species differences. Within species the correlation is weaker, ranging from 0.468 (Adelie) to 0.703 (Gentoo).
- **Bill length:** the within-species correlations (0.514 to 0.669) are close to the pooled 0.595, so this relationship largely survives species adjustment.
- **Bill depth:** the pooled negative correlation is driven by between-species differences. Within each species the correlation is positive.

The flipper-correlation differences across species are descriptive only. No heterogeneity test was run, and the Chinstrap estimate is less precise because of its smaller sample.

### 6. Predictive models

Each model was evaluated on a 69-penguin test set, with 273 penguins used for training.

| Model | Test MAE (g) | Test R-squared | Train R-squared | Test RMSE (g) |
|---|---|---|---|---|
| Linear regression | 255.2 | 0.827 | 0.883 | 312.9 |
| Random forest | 277.6 | 0.790 | 0.982 | 344.2 |
| Mean-only baseline | 624.0 | -0.002 | 0.0 | 751.7 |

The linear regression is the best model. The random forest overfits strongly.

Permutation importance for the linear model, measured as the increase in test MAE when a feature is permuted:

| Feature | MAE increase (g) |
|---|---|
| Species | 355.6 |
| Flipper length | 103.5 |
| Sex | 83.2 |
| Bill depth | 48.3 |
| Bill length | 24.7 |
| Year | 1.8 |
| Island | -0.5 |

Island adds little once species is in the model. Single-feature permutation can understate island because island is correlated with species, so this conclusion is soft.

### 7. Missingness

- **Sex missingness** is 11 of 344 rows overall. By species: Adelie 3.95% (6 of 152), Chinstrap 0.00% (0 of 68), Gentoo 4.03% (5 of 124). By island: Torgersen 9.62% (5 rows), Biscoe 2.98% (5 of 168), Dream 0.81% (1 of 124). The Torgersen share rests on only 5 rows.
- **Mass of sex-missing rows:** among the 9 sex-missing rows with a recorded mass, the mean is 4005.6 g, against 4207.1 g for rows with sex present. This gap rests on 9 rows and is weak evidence. The other 2 sex-missing rows also lack mass.
- **Measurement missingness** affects 2 rows, the same rows for all four measurement columns. Adelie has 1 row (0.66%), Gentoo 1 row (0.81%) and Chinstrap none. By year: 2007 has 1 row (0.91%), 2009 has 1 row (0.83%) and 2008 none. bill_depth_mm is missing on exactly the same rows as the other measurement columns.

The pattern looks mostly random. The counts are too small for a reliable link between sex missingness and species or island.

## Limitations

- **Confounding of species and island.** Gentoo appears only on Biscoe and Chinstrap only on Dream. The island comparisons in Section 2 are unadjusted and confounded with species. The species-adjusted island estimates rely on the additive assumption and on Adelie alone.
- **Sex comparisons.** The pooled sex difference (683.4 g) is not adjusted for species. The per-species sex gaps are unadjusted for island, and their p-values are not multiplicity-adjusted. The Chinstrap gap rests on 34 penguins per sex.
- **Within-species correlations.** No heterogeneity test was run, so differences among species in the flipper correlation are descriptive only.
- **Missing data.** Sex missingness is 11 rows, and its link to species and island rests on 5 to 6 rows per group. The two rows missing all measurements cannot be compared on mass.
- **Models.** Model scores come from a single 69-penguin test split. The random forest overfits, and island importance from permutation is confounded with species.
- **Record labelling.** One record describing the species-adjusted island model names Torgersen as the reference level, while the reported coefficients are relative to Biscoe. The Biscoe-referenced values are used here, consistent with the Adelie Biscoe-versus-Dream comparison.
- **Review issues and failed tasks.** None were recorded as unresolved, and no task failed.

## Open questions

- Does the species effect hold after adjusting for sex in a two-way model?
- Does the sex effect hold after adjusting for island within species?
- Does the island effect hold within species after adjusting for sex? Can it be estimated within Gentoo or Chinstrap, which each occur on only one island?
- Is the flipper-mass slope different across species when tested formally with a species interaction?
- Do the within-species bill depth and flipper associations hold after adjusting for sex, given that sex differs within species?
- Is the Chinstrap sex gap sensitive to its small sample (34 per sex)?
- Is the sex-missingness pattern on Torgersen real, or chance with 5 rows missing there? Would imputing sex from species, island and mass change the sex effect?
- Do the 2 rows missing all measurements share any other feature that explains their gaps?