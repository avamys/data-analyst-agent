# Penguin Body Mass (body_mass_g): Species, Sex, Island and Predictive Performance

## Summary

- **Species and sex are the two strongest associations with body mass.** Species has the largest effect (two-way ANOVA eta-squared 0.464; Kruskal-Wallis p=8.8e-47). Gentoo's Tukey mean difference from Adelie is 1386 g (95% CI 1252 to 1520). Males are heavier than females by 683.4 g (Welch 95% CI 526.2 to 840.6, p=4.8e-16, Cohen's d=0.94).
- **The crude island difference is associated with species mix.** Biscoe has the highest mean (4716.0 g), and Gentoo occurs only on Biscoe. In the additive two-way model, island shows no effect (F=0.059, p=0.94), but that adjustment is not fully identified. Within Adelie, the only species found on all three islands, island means range from 3701.4 g to 3709.7 g (Kruskal-Wallis p=0.96).
- **The sex difference holds within every species, but its size varies.** Within-species male-female gaps are 674.7 g (Adelie), 411.8 g (Chinstrap) and 805.1 g (Gentoo). All are significant (Welch p<0.001 for Adelie and Gentoo, p=2.3e-6 for Chinstrap). The species-by-sex interaction is significant (F=8.71, p=0.0002).
- **Linear regression beats the mean baseline on one fixed split.** It reaches test MAE 239.7 g and R² 0.839, against 632.8 g and R² -0.02 for the mean baseline. The random forest reaches test MAE 263.1 g and R² 0.807, with train R² 0.982. Only this single split was evaluated.
- **Missing sex is the only substantive missingness.** It affects 11 of 344 rows (3.2%) and shows no clear link to species, island or year. The 9 of these rows with body mass recorded average 4005.6 g, against 4207.1 g for the 333 rows with sex recorded. This group is too small for firm conclusions.

## Data

- **Size:** 344 rows × 8 columns.
- **Target:** body_mass_g (regression).
- **Numeric features:** bill_length_mm, bill_depth_mm, flipper_length_mm, year.
- **Categorical features:** species, island, sex.
- **Date/time features:** none. **Identifier or free-text columns:** none.
- **Missing values:** bill_length_mm, bill_depth_mm, flipper_length_mm and body_mass_g are each missing for 2 rows (0.6%). Sex is missing for 11 rows (3.2%). Eleven rows have at least one missing value.

## Findings

### Overall distribution and group means

Across the 342 rows with body_mass_g recorded, mean body mass is 4201.8 g, median 4050 g, SD 801.95 g, and range 2700 to 6300 g.

![Distribution of body_mass_g across all penguins (30 bins, about 120 g each)](tasks/eda_1/charts/body_mass_histogram.png)

*The histogram uses 30 bins of about 120 g each. An earlier title said "per 100 g bin"; that was wrong and has been replaced. A duplicate chart, body_mass_histogram_v2, carries the same content and is not reproduced here.*

**By species** (sex-missing rows excluded from these group means):
- Gentoo: mean 5076.0 g, median 5000 g, n=123.
- Chinstrap: mean 3733.1 g, median 3700 g, n=68.
- Adelie: mean 3700.7 g, median 3700 g, n=151.

Adelie and Chinstrap are nearly identical. Gentoo is about 1386 g heavier than Adelie (Tukey, from the species tests below).

![body_mass_g by species](tasks/eda_1/charts/body_mass_boxplot_by_species.png)

**By island** (sex-missing rows excluded):
- Biscoe: mean 4716.0 g, median 4775 g, n=167.
- Dream: mean 3712.9 g, median 3687.5 g, n=124.
- Torgersen: mean 3706.4 g, median 3700 g, n=51.

Biscoe's higher mean is associated with its species mix: 123 of its 167 penguins are Gentoo, and Gentoo occurs only on Biscoe. Within-species island means were not computed in the descriptive task; they are reported under the species-mix findings below.

**By sex** (sex-missing rows excluded): females have mean 3862.3 g (median 3650 g, n=165); males have mean 4545.7 g (median 4300 g, n=168).

**By year** (sex-missing rows excluded): means are similar across years, at 4124.5 g in 2007 (n=109), 4266.7 g in 2008 (n=114) and 4210.3 g in 2009 (n=119). Year shows no large shift.

**Pearson correlations with body_mass_g:** flipper_length_mm r=0.871; bill_length_mm r=0.595 (positive); bill_depth_mm r=-0.472 (negative).

### Missing data and missingness

- Sex is missing in 11 rows (3.2%). Each of the four measurement columns and body_mass_g is missing in 2 rows (0.58%).
- The 2 rows with missing measurements are a subset of the 11 rows with missing sex. Neither has a body_mass_g value, so they cannot be compared on body mass.
- Among the 11 sex-missing rows, 9 have body_mass_g. Their mean is 4005.6 g, against 4207.1 g for the 333 rows with sex recorded.
- Sex-missing composition: Adelie 6, Gentoo 5; Torgersen 5, Biscoe 5, Dream 1; 2007 7, 2009 3, 2008 1.
- Sex-missing rates: Adelie 3.95%, Gentoo 4.03%, Chinstrap 0%; Torgersen 9.6%, Biscoe 3.0%, Dream 0.8%; 2007 6.4%, 2008 0.9%, 2009 2.5%.
- In this sample, missingness in sex is not clearly tied to species, island, year or body mass. The Torgersen and 2007 rates are higher, but the flagged groups contain only 1 to 7 rows each, so these differences are not treated as real.

![Percent of rows missing per column](tasks/eda_2/charts/missing_pct_by_column.png)

### Species, island and sex: significance and effect sizes

The analysis sample is the 333 rows with body_mass_g and sex recorded. The 9 body-mass rows with missing sex are dropped. All tests in this section use this sample, not the 342 rows above.

- **Species:** Kruskal-Wallis H=212.09, p=8.8e-47. In the two-way ANOVA (body_mass_g ~ species × sex + island, Type II), species has F=315.3, p<0.001, eta-squared 0.464. Tukey pairwise differences: Gentoo minus Adelie 1386 g (95% CI 1252 to 1520); Gentoo minus Chinstrap 1359 g (95% CI 1194 to 1524); Chinstrap minus Adelie 27 g (95% CI -132 to 186), not significant.
- **Island (unadjusted):** Kruskal-Wallis H=124.35, p=9.9e-28. Tukey: Dream minus Biscoe -1000 g (95% CI -1178 to -823); Torgersen minus Biscoe -1011 g; Torgersen minus Dream -10 g (95% CI -265 to 244), not significant.
- **Island (adjusted):** In the additive two-way ANOVA, island has F=0.059, p=0.94, eta-squared 0.0001. Because Gentoo occurs only on Biscoe, this adjustment is not fully identified (see Limitations).
- **Sex:** Males are heavier by 683.4 g (Welch 95% CI 526.2 to 840.6; t=8.55, df=323.9, p=4.8e-16; Cohen's d=0.94). Mann-Whitney p=1.8e-15. In the two-way ANOVA, sex has F=385.3, p<0.001, eta-squared 0.284.
- **Species × sex interaction:** F=8.71, p=0.0002, eta-squared 0.013. The sex effect differs by species (see the next section).
- **Residual:** The residual eta-squared is 0.239. Species and sex account for most of the explained variation; island contributes essentially nothing once they are in the model.

![Boxplots of body_mass_g in grams by species, split by sex](tasks/stat_1/charts/body_mass_by_species_sex.png)

### Species mix and within-species effects

**Sex within each species** (male minus female, body_mass_g):

| Species | Female mean (n) | Male mean (n) | Difference | 95% CI | Cohen's d |
|---|---|---|---|---|---|
| Adelie | 3368.8 g (73) | 4043.5 g (73) | 674.7 g | 573.0 to 776.3 | 2.17 |
| Chinstrap | 3527.2 g (34) | 3939.0 g (34) | 411.8 g | 253.7 to 569.8 | 1.26 |
| Gentoo | 4679.7 g (58) | 5484.8 g (61) | 805.1 g | 697.1 to 913.1 | 2.70 |

All three are significant: Welch p=6.4e-26 (Adelie), 2.3e-6 (Chinstrap), 1.9e-28 (Gentoo). Mann-Whitney p is below 0.001 for Adelie and Gentoo and 5.3e-6 for Chinstrap. Medians point the same way: Adelie 4000 vs 3400, Chinstrap 3950 vs 3550, Gentoo 5500 vs 4700 (male vs female).

The overall sex coefficient is 683.4 g raw and 667.6 g after species adjustment (p=8.7e-56). The overall sex gap is therefore not explained by species composition.

Sex is balanced within species: Adelie 73 female and 73 male, Chinstrap 34 and 34, Gentoo 58 female and 61 male. Sex-missing rows are 6 Adelie and 5 Gentoo.

**Species-by-island means** (body_mass_g; the Adelie and Chinstrap figures below come from the all-body-mass-present basis, except where noted):
- Adelie | Biscoe: 3709.7 g (n=44). Adelie | Dream: 3688.4 g (n=56). Adelie | Torgersen: 3706.4 g (n=51).
- Chinstrap | Dream: 3733.1 g (n=68). Gentoo | Biscoe: 5076.0 g (n=123).

Adelie is flat across islands; the crude Biscoe advantage is associated with species mix.

**Island within Adelie** (sex-recorded sample): Biscoe 3709.7 g (median 3750, n=44), Dream 3701.4 g (median 3600, n=55), Torgersen 3708.5 g (median 3700, n=47). Kruskal-Wallis p=0.96; ANOVA p=0.995. Pairwise Welch: Biscoe minus Dream 8.3 g (p=0.93, d=0.02); Biscoe minus Torgersen 1.1 g (p=0.99, d=0.00). In an OLS with sex adjustment, the Dream and Torgersen coefficients versus Biscoe are -14.4 g (p=0.82) and +6.0 g (p=0.93), against a sex coefficient of 674.9 g (p=4.7e-26).

**Island after species adjustment** (OLS, Biscoe reference): Dream -8.3 g (p=0.93) and Torgersen -1.1 g (p=0.99), against a Gentoo coefficient of 1382.8 g (p=9.4e-47). This is a conditional null, not proof of zero island effect.

![body_mass_g distribution for females and males within Adelie, Chinstrap and Gentoo](tasks/stat_2/charts/sex_within_species_boxplot.png)

**Species composition and missingness:** The chart below shows counts per species and island on the body-mass-present basis. The all-rows counts differ by one row for Adelie Torgersen (52 in all rows, 51 in the chart) and Gentoo Biscoe (124 vs 123), because one penguin has missing body_mass_g.

![Counts of penguins per species, split by island](tasks/eda_3/charts/species_by_island_counts.png)

### Predictive models

Evaluation uses a fixed 75/25 split (256 train, 86 test; random_state=42) on the 342 rows with body_mass_g.

| Model | Test MAE (g) | Test R² | Train R² |
|---|---|---|---|
| Mean baseline | 632.8 | -0.02 | 0.0 |
| Linear regression | 239.7 | 0.839 | 0.882 |
| Random forest | 263.1 | 0.807 | 0.982 |

Both models clearly beat the mean baseline on this split. On this single fixed split, linear regression has the lower test MAE (239.7 vs 263.1 g) and the higher test R² (0.839 vs 0.807). No interval, repeated split or cross-validation was checked. The random forest's train R² (0.982) is well above its test R² (0.807), which the analysis describes as clear overfitting. Linear regression's train R² is 0.882.

**Linear regression permutation importance** (increase in test MAE, 30 repeats, original features, ranked by mean increase):

| Rank | Feature | MAE increase (g) | SD (g) |
|---|---|---|---|
| 1 | species | 378.1 | 43.5 |
| 2 | sex | 93.7 | 20.5 |
| 3 | flipper_length_mm | 91.0 | 14.4 |
| 4 | bill_depth_mm | 45.4 | 11.5 |
| 5 | bill_length_mm | 27.6 | 10.0 |
| 6 | year | 2.8 | 3.0 |
| 7 | island | -0.4 | 2.0 |

The accepted results list seven input features, which is the full set of original features (the eighth column is the target).

![Permutation importance (increase in test MAE, g) of each input feature for the linear regression predicting body_mass_g](tasks/ml_1/charts/ml_1_permutation_importance.png)

**Random forest impurity importance:** species 0.44; flipper_length_mm 0.31; sex (male and female indicator columns) about 0.075 each; bill_length_mm 0.044; bill_depth_mm 0.043; year 0.010; island indicators 0.002 to 0.003 each. The ranking agrees with linear regression: species first, then flipper length.

## Limitations

- **Missing sex:** 11 rows (3.2%) lack sex. The flagged groups contain 1 to 7 rows each, so the flagged-group differences in species, island and year are not tested. The 2 rows with missing measurements have no body_mass_g values and cannot be compared on body mass.
- **Analysis samples differ:** The descriptive section uses 342 rows with body_mass_g. The significance tests and within-species results use the 333 rows with body_mass_g and sex recorded. Some cell counts differ by one row between these bases (for example, Adelie Torgersen 51 vs 52).
- **Island effect not fully identified:** Gentoo occurs only on Biscoe, so the additive island adjustment rests on Adelie and Chinstrap comparisons. The within-Adelie null supports it, but no within-species island comparison is available for Chinstrap, which occurs only on Dream.
- **Small within-species samples:** Chinstrap has 34 penguins per sex. The smaller Chinstrap sex gap was not tested for sensitivity to this sample size.
- **Model evaluation:** Results come from one fixed split with random_state=42. No interval, repeated split or cross-validation was checked, and the random forest was not tuned. The overfitting was judged from the train-test gap only.
- **Sex-missing handling in the models:** The ML findings do not state how the 9 body-mass rows with missing sex were handled when sex is a feature.
- **Unresolved review issue, ml_1 (permutation importance and model claim):** The lead required the full permutation importance for all features, with mae_increase and SD for bill_depth_mm, bill_length_mm, year and island, and required the claim that linear regression is better to be qualified to this single fixed split with no interval or repeated split checked. The full table is given above and the claim is qualified. The review note refers to eight features, but the accepted results list seven, which is the full original feature set.
- **Unresolved review issue, eda_3 (Adelie gap and Gentoo statement):** The lead required the Adelie male-female gap to be corrected to 674.7 g (4043.5 minus 3368.8), and the sentence stating that the Gentoo sex gap was earlier reported as not visible to be removed. The corrected Adelie gap is used above, the unsupported sentence is omitted, and the Gentoo gap is stated only as 805.1 g.
- **Chart duplicate:** body_mass_histogram_v2 duplicates body_mass_histogram and is not separately embedded.
- **Failed tasks:** None. All six tasks (eda_1, eda_2, eda_3, stat_1, stat_2, ml_1) completed and were accepted, subject to the review issues above.

## Open questions

- Does the sex difference hold within each species after adjusting for flipper length and the bill measurements? Do the bill measurements differ by sex within species, and does flipper length absorb the sex effect?
- Does the species-by-sex interaction reflect a real difference in effect size across species, and is the smaller Chinstrap gap sensitive to its sample of 34 per sex?
- Is sex missingness associated with island or year? The planned chi-square or Fisher exact test was not run.
- Do the 2 rows missing all measurements have a recoverable species or island, and can they be imputed?
- Which penguin has missing body_mass_g on Torgersen, and does dropping it change the Adelie island comparison?
- Does the random forest's overfitting shrink with tuning or repeated cross-validation, and does the linear regression ranking hold across different splits?
- Does flipper length within species explain the remaining prediction error (MAE 239.7 g on the test split), and is the bill depth correlation still negative within species?
- Does sampling vary by year, and why are the 2007 to 2009 year means similar?