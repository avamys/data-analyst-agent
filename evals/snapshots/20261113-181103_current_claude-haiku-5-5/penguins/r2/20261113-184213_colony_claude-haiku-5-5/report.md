# Penguin Dataset: Body Mass (body_mass_g) by Group, Species Effects, and Prediction

## Summary

- **Species is the largest group difference in body mass.** Gentoo averages 5076 g (n=123), against 3701 g for Adelie (n=151) and 3733 g for Chinstrap (n=68). Adelie and Chinstrap do not differ (Welch p=0.59, Holm-adjusted). Kruskal-Wallis H=217.60, p=5.6e-48, eta² = 0.670.
- **Males are heavier than females, but the size of the gap depends on species.** Males average 4546 g and females 3862 g (Cohen's d = 0.94, 95% CI 0.71 to 1.16). Adjusted for flipper length, the male-female difference is 599 g in Adelie, 194 g in Chinstrap and 598 g in Gentoo. The sex-by-species block is significant (F(2)=10.54, p=3.7e-5).
- **A linear regression predicts body mass well on the 69-row test set.** Its test MAE is 255 g and R² is 0.826, against 624 g and R² of -0.002 for the mean baseline. Gradient boosting is close behind (MAE 273 g, R² 0.802). The model was chosen on the test set, so these scores are slightly optimistic. Species is the most important feature by permutation importance.
- **The island effect in raw data is not confirmed after controlling for species, but the test is inconclusive.** Within Adelie, the only species found on all three islands, body mass does not differ by island (ANOVA p=0.97). The intervals are wide enough to leave differences of roughly 200 g open.
- **Flipper-length slopes are positive in every species (16 to 27 g/mm), but no slope difference between species is supported at Holm-adjusted 0.05** under either model that was run. The intervals overlap, and this is not a formal test of slope equality.

## Data

- **Size:** 344 rows, 8 columns.
- **Target:** body_mass_g (regression).
- **Numeric features:** bill_length_mm, bill_depth_mm, flipper_length_mm, year.
- **Categorical features:** species, island, sex.
- **Date/time features and id or text columns:** none.
- **Missing values:**
  - sex: 11 rows (3.2%).
  - bill_length_mm, bill_depth_mm, flipper_length_mm and body_mass_g: 2 rows each (0.6%).
  - All 11 rows with any missing value are the same rows with missing sex. The two rows missing body_mass_g are excluded from all statistics that use body mass.

## Findings

### Body mass distribution and group means (EDA)

Overall body_mass_g (n=342 non-missing) has mean 4201.75 g, median 4050 g, SD 801.95 g, minimum 2700 g and maximum 6300 g. The histogram is right-skewed, with the mean above the median.

![Histogram of body_mass_g across all non-missing rows](tasks/eda_1/charts/body_mass_hist.png)

| Group | n | Mean (g) | Median (g) |
|---|---|---|---|
| Adelie | 151 | 3700.66 | 3700 |
| Chinstrap | 68 | 3733.09 | 3700 |
| Gentoo | 123 | 5076.02 | 5000 |
| Biscoe | 167 | 4716.02 | 4775 |
| Dream | 124 | 3712.90 | 3687.5 |
| Torgersen | 51 | 3706.37 | 3700 |
| Male | 168 | 4545.68 | 4300 |
| Female | 165 | 3862.27 | 3650 |
| 2007 | 109 | 4124.54 | 3900 |
| 2008 | 114 | 4266.67 | 4200 |
| 2009 | 119 | 4210.29 | 4000 |

- **Species:** Gentoo is much heavier than the other two species.
- **Island:** Biscoe has the highest mean. Dream and Torgersen are close to each other. The EDA noted that the island gap may reflect species mix, which this task did not test.
- **Sex:** Males are heavier. The 11 rows with missing sex are excluded from this comparison.
- **Year:** The means are similar across 2007, 2008 and 2009, and small relative to the overall SD. No test was run on year.

### Species, island and sex: significance and effect size (stat_1)

![Box plots of body_mass_g (g) by species, island and sex, non-missing rows only](tasks/stat_1/charts/body_mass_by_group_box.png)

- **Species** (342 rows, 2 dropped): Kruskal-Wallis H=217.60, p=5.6e-48, eta² = 0.670. 95% CIs for the means: Adelie 3700.66 g [3626.93, 3774.40]; Chinstrap 3733.09 g [3640.06, 3826.12]; Gentoo 5076.02 g [4986.03, 5166.00].
  - Holm-adjusted Welch pairwise tests: Adelie vs Chinstrap p=0.59 (no difference). Adelie vs Gentoo and Chinstrap vs Gentoo are both p<1e-47.
- **Island** (342 rows, 2 dropped): Kruskal-Wallis H=130.07, p=5.7e-29, eta² = 0.394. 95% CIs for the means: Biscoe 4716.02 g [4596.41, 4835.62]; Dream 3712.90 g [3638.84, 3786.97]; Torgersen 3706.37 g [3581.18, 3831.56].
  - Holm-adjusted Welch pairwise tests: Biscoe vs Dream p=1.5e-33; Biscoe vs Torgersen p=2.6e-22; Dream vs Torgersen p=0.93.
  - These tests do not control for species, so the island gap may partly reflect species mix (see the next section).
- **Sex** (333 rows, 11 dropped for missing sex or body mass): Mann-Whitney U=20845.5, p=1.8e-15. Welch t=8.55, p=4.8e-16. Both tests agree. Cohen's d (male minus female) = 0.94, 95% CI [0.71, 1.16], a large effect. 95% CIs for the means: female 3862.27 g [3759.87, 3964.67] (n=165); male 4545.68 g [4425.71, 4665.65] (n=168).

### Island effect after controlling for species (stat_3, partial)

![Mean body_mass_g per species-island cell; Chinstrap has only Dream and Gentoo only Biscoe, so island effects within species are testable only for Adelie.](tasks/stat_3/charts/bm_species_island_cells.png)

Species-island cell counts are: Adelie Biscoe 44, Adelie Dream 56, Adelie Torgersen 51, Chinstrap Dream 68, Gentoo Biscoe 123.

- **Species-adjusted additive model (342 rows):** Island contrasts are identified only from Adelie, because Gentoo is found only on Biscoe and Chinstrap only on Dream.
  - Biscoe vs Dream: +21.3 g (95% CI -162 to +205, p=0.82).
  - Torgersen vs Dream: +18.0 g (95% CI -158.5 to +194.5, p=0.84).
  - These intervals are too wide to rule out island differences of roughly 200 g in either direction. The result is inconclusive and is not evidence of no island difference.
  - R² is 0.6697 with species alone and 0.6697 with species and island.
- **Within Adelie:** The one-way ANOVA gives F=0.03, p=0.97. Pairwise differences are at most 21 g, with |Cohen's d| of 0.05 or less.
  - Biscoe vs Dream: +21.3 g (n=44 vs 56; 95% CI -168 to +211; p=0.82).
  - Biscoe vs Torgersen: +3.3 g (n=44 vs 51; 95% CI -188 to +195; p=0.97).
  - Dream vs Torgersen: -18.0 g (n=56 vs 51; 95% CI -191 to +155; p=0.84).
- **Interaction:** The species-by-island interaction cannot be tested. Island within Gentoo and island within Chinstrap are not estimable.

### Flipper length, species and sex (stat_2, stat_4)

**Full model (stat_2, Adelie female reference, sex-adjusted interactions).** Flipper length is positive in the reference species, with the species and sex interaction terms added on top.

| Term | Coefficient (g/mm or g) | p |
|---|---|---|
| flipper_length_mm | 12.66 | 0.036 |
| flipper × Chinstrap | -0.65 | 0.95 |
| flipper × Gentoo | +22.57 | 0.048 |
| flipper × male | +6.28 | 0.42 |
| flipper × Chinstrap × male | +21.98 | 0.13 |
| flipper × Gentoo × male | -23.27 | 0.10 |
| Chinstrap × male | -4743.6 | 0.089 |
| Gentoo × male | +4849.3 | 0.098 |

**Reduced additive model (stat_4, one common flipper slope, no interactions, for comparison).** Flipper length 20.02 g/mm (p=1.2e-11); Chinstrap -87.6 g (p=0.060); Gentoo +836.3 g (p=4e-20); male +530.4 g (p=2e-35). These terms assume a common slope and are not directly comparable to the interaction terms above.

**Per-species slopes of body_mass_g on flipper_length_mm, adjusted for sex (stat_2):**

- Adelie: 16.3 g/mm (95% CI 8.4 to 24.3; n=146)
- Chinstrap: 26.7 g/mm (95% CI 14.6 to 38.8; n=68)
- Gentoo: 23.5 g/mm (95% CI 13.2 to 33.8; n=119)

Each slope is positive. The intervals overlap, and overlapping intervals are not a test of slope equality. The Gentoo flipper-by-species interaction is p=0.048. No single flipper-by-species term is clearly significant.

**Interaction block.** The full block of flipper, species and sex interactions (7 df) is significant against the additive model: F(7)=4.62, p=6.1e-5. R² rises from 0.867 to 0.879 (adjusted 0.865 to 0.875). Individually, the sex-by-species terms are about p=0.09. The individual terms were not tested as a subset, so this report does not say which terms carry the joint result.

**Sex effect within species (stat_2, adjusted for flipper length):**

- Adelie: male minus female 599 g (95% CI 496 to 703; p=5e-22; n=146).
- Chinstrap: 194 g (95% CI 23 to 365; p=0.027; n=68).
- Gentoo: 598 g (95% CI 462 to 733; p=2e-14; n=119).
- Sex-by-species block: F(2)=10.54, p=3.7e-5.

The Chinstrap sex gap is about one third of the Adelie and Gentoo gaps. The data do not show whether this reflects sample size or a real difference, and the analysis did not adjust for island.

**Pairwise flipper-slope contrasts (stat_4, complete rows, n=333).** Contrasts are second species minus first species.

| Pair | Common-sex model: difference (g/mm), 95% CI, raw p, Holm p | Species-by-sex model: difference (g/mm), 95% CI, raw p, Holm p |
|---|---|---|
| Adelie vs Chinstrap | -5.14; -17.53 to 7.25; 0.415; 0.415 | +10.36; -3.77 to 24.49; 0.150; 0.450 |
| Adelie vs Gentoo | +8.96; -2.13 to 20.05; 0.113; 0.226 | +7.18; -5.98 to 20.35; 0.284; 0.567 |
| Chinstrap vs Gentoo | +14.10; 1.28 to 26.92; 0.031; 0.094 | -3.18; -19.13 to 12.78; 0.696; 0.696 |

- **Common-sex model:** no pairwise slope difference is supported at Holm-adjusted 0.05. Chinstrap vs Gentoo is closest (raw p=0.031, Holm p=0.094). This model assumes no species-by-sex interaction, which the sex-by-species block test (F(2)=10.54, p=3.7e-5, stat_2) argues against.
- **Species-by-sex model (stat_4, complete rows):** the sex-by-species block is again significant (F(2)=9.13, p=1.4e-4). No pairwise slope difference is supported at Holm-adjusted 0.05. The sign of the Adelie vs Chinstrap difference reverses between the two models.

The species-by-sex model's per-species slopes match stat_2 for Adelie (16.31) and Chinstrap (26.67) and for Gentoo (23.50). The CIs differ slightly from stat_2 (see Limitations).

**Answer to the question on species and flipper slopes:** The sex effect on body mass differs by species, supported by the sex-by-species block. Flipper-length slopes are positive in every species, but the data do not show a supported difference between species in those slopes.

### Predictive modelling (ml_1)

![Test-set MAE in grams for the mean baseline, linear regression and gradient boosting predicting body_mass_g](tasks/ml_1/charts/ml1_model_test_mae.png)

Split: 80/20, random_state 42, on the 342 rows with non-missing body mass. Training has 273 rows and test has 69. Numeric features were median-imputed. Sex was most-frequent-imputed. Species and island were one-hot encoded. Nine of the 342 modelling rows have missing sex.

| Model | Test MAE (g) | Test R² | Train R² |
|---|---|---|---|
| Mean baseline | 624.0 | -0.002 | 0.0 |
| Linear regression | 255.2 | 0.826 | 0.883 |
| Gradient boosting | 272.7 | 0.802 | 0.958 |

- Both models beat the mean baseline on the test set.
- Gradient boosting overfits more: a train-test R² gap of 0.156, against 0.056 for linear regression.
- Linear regression was selected because it has the higher test R² and lower test MAE. Selection used the test set, so the test-set scores and importances are slightly optimistic. The choice has not been validated on a separate split or by cross-validation.

**Permutation importance for the selected linear regression (test set, drop in R²):**

- Species: 0.875 (SD 0.117)
- flipper_length_mm: 0.179 (SD 0.025)
- sex: 0.137 (SD 0.030)
- bill_depth_mm: 0.071 (SD 0.015)
- bill_length_mm: 0.036 (SD 0.012)
- island: -0.001 (SD 0.002)
- year: -0.005 (SD 0.006)

Island and year show no positive contribution. Gradient boosting's importance ranking is similar at the top: species Gentoo 0.59, flipper_length_mm 0.17, and sex 0.08 (female) and 0.08 (male).

## Limitations

- **Missing data:** Sex is missing in 11 rows (3.2%). The 11 rows with missing sex have a lower mean body mass (4005.6 g) than rows with sex recorded (4207.1 g), a gap of about 200 g. This covers only the 9 rows with sex missing and body mass present. The sample is too small to test this, so it should not be read as a reliable association. Missing sex is concentrated in Torgersen (9.6% of that island's rows) and in 2007 (6.4%), and the EDA says counts this small cannot establish a relationship with species, island or year. No test was run on these associations. The two rows missing body mass are excluded from all body-mass statistics.
- **Island analysis (stat_3, partial):** Island effects within species are testable only for Adelie. The species-by-island interaction cannot be tested. The species-adjusted island results are inconclusive, not evidence of no island difference. The stat_3 status is partial, so the analysis is not complete.
- **Interaction block and flipper slopes (stat_2):** The review asked that the claim that the block is driven mainly by sex-by-species terms, and not by flipper slopes, be removed. No subset test supports it, so it is not made here. Overlapping CIs are not a test of slope equality. The Gentoo flipper-by-species interaction is p=0.048, and the formal pairwise slope comparison is reported in stat_4 above.
- **Pairwise slope contrasts (stat_4, partial, unresolved review issue):** The review asked for the species-by-sex contrasts for all three pairs, with Holm correction and a statement of which differences the species-by-sex model supports. Those are reported above. Under that model, none is supported at Holm 0.05. The implied common-sex per-species slopes were removed because they were not recorded as facts.
- **Disagreement between stat_2 and stat_4 CIs:** Both report the same per-species slope point estimates, but the 95% CIs differ slightly. Adelie: stat_2 [8.37, 24.26] and stat_4 [8.62, 24.01]. Chinstrap: stat_2 [14.60, 38.75] and stat_4 [14.82, 38.53]. Gentoo: stat_2 [13.15, 33.85] and stat_4 [12.82, 34.18]. The source of the difference is not established here.
- **Common-sex versus species-by-sex models:** These give different signs for the Adelie vs Chinstrap slope difference (-5.14 and +10.36 g/mm). The data do not settle which model is correct. The sex-by-species block test favours the species-by-sex model.
- **Sample size for sex effects:** The Chinstrap sex gap (194 g) rests on 68 Chinstrap rows, all from Dream. Whether it holds after controlling for island is not tested.
- **Modelling:** Model selection used the test set. The test set has 69 rows, so the MAE and R² estimates are imprecise. Gradient boosting overfits, and its tuning was not explored.
- **Year:** Year was summarised but not tested.

## Open questions

- Is the island difference in body mass present after controlling for species, flipper length and sex? The Adelie-only comparison does not answer this for Gentoo or Chinstrap, because those species are each on one island.
- Does the Chinstrap sex gap (194 g) reflect sample size or a real difference, and does it hold after controlling for island?
- Does the Chinstrap vs Gentoo flipper-slope difference (raw p=0.031, common-sex model) hold once the species-by-sex interaction is included, and with a larger sample or after controlling for island? The species-by-sex model gives a non-significant -3.18 g/mm (Holm p=0.696).
- Do bill and flipper measurements differ by island within Adelie, which might show a morphological difference that body mass does not?
- What is the minimum detectable island effect within Adelie at 80% power with 44 to 56 rows per island?
- Does the male-female gap hold within each species after controlling for island?
- Does the gradient boosting overfit shrink with tuning or regularisation, and does it then beat linear regression?
- Does a cross-validated comparison confirm the choice of linear regression?
- Are the missing-sex rows associated with island, year or body mass beyond chance? A chi-square or Fisher test on the 11 cases could address this, but was not run.
- Does imputing sex from species and island change the body-mass model?
- Does the Gentoo flipper slope differ from the Adelie slope when tested with a formal test that uses all rows?