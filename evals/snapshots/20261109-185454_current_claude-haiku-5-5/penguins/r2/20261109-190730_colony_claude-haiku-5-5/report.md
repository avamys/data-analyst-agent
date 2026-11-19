# Body Mass (body_mass_g) in 344 Penguins: Species and Sex Drive Mass, Island and Year Do Not, and Sex Missingness Is Only a Tentative Lead

## Summary

- **Species is the dominant factor.** Gentoo penguins average 5076 g, against 3700.7 g for Adelie and 3733.1 g for Chinstrap. Species explains the most variation (eta² = 0.67). Adelie and Chinstrap do not differ (Holm p = 0.59).
- **The sex effect is real but depends on species.** Males average 683 g heavier overall (95% CI 526 to 841 g). The male-female gap differs by species (interaction p = 0.0002), ranging from 412 g in Chinstrap to 805 g in Gentoo, with all three CIs excluding zero.
- **A linear model predicts mass well, a random forest less so.** On a single 75/25 split, linear regression reaches test MAE 253 g (R² 0.82) against 633 g for a mean baseline. The random forest reaches 277 g (R² 0.79) and overfits. The linear model was selected on the test set, so its score is optimistic.
- **Island and year add little.** Unadjusted for species, Biscoe is 1003 g above Dream and 1010 g above Torgersen. Within Adelie, the only species found on all three islands, island has no detectable effect (p = 0.97). Year shows no detectable effect (p = 0.41).
- **Missingness is sparse and mostly untestable.** Sex is missing for 11 rows (3.2%). Its link to island (exact p = 0.018) is a tentative lead on 11 rows. Links to species and year are not supported. Missing body_mass_g (2 rows) cannot be meaningfully tested.

## Data

- **Size:** 344 rows × 8 columns.
- **Target:** body_mass_g (regression). The analysis uses 342 rows with non-missing mass.
- **Features:** numeric (bill_length_mm, bill_depth_mm, flipper_length_mm, year); categorical (species, island, sex). No date/time features, IDs or free-text fields.
- **Missing values:** sex 11 rows (3.2%). Each of body_mass_g, bill_length_mm, bill_depth_mm and flipper_length_mm has 2 rows (0.6%). Species, island and year have none.
- **Clean table:** dropping the 2 rows missing body_mass_g leaves 342 rows, of which 9 still lack sex.

## Findings

### Distribution and group means (descriptive)

- Overall body_mass_g (n = 342): mean 4201.75 g, median 4050 g, SD 801.95 g, range 2700 to 6300 g.
- **By species:** Gentoo 5076.0 g (n = 123), Chinstrap 3733.1 g (n = 68), Adelie 3700.7 g (n = 151). Medians are 5000 g for Gentoo and 3700 g for both Adelie and Chinstrap.

![Box plot of body_mass_g in grams for each species (missing values excluded)](tasks/eda_1/charts/bm_box_by_species.png)

- **By island:** Biscoe 4716.0 g (n = 167), Dream 3712.9 g (n = 124), Torgersen 3706.4 g (n = 51). These are not adjusted for species.
- **By sex:** male 4545.7 g (n = 168), female 3862.3 g (n = 165).
- **By year:** 2007 4124.5 g (n = 109), 2008 4266.7 g (n = 114), 2009 4210.3 g (n = 119).

### Significance and effect sizes

Omnibus tests were Holm-corrected across the four factors.

| Factor | Test results | Holm-adjusted omnibus p | eta² |
|---|---|---|---|
| Species | ANOVA F = 343.6, p = 2.9e-82; Kruskal-Wallis H = 217.6, p = 5.6e-48 | 1.2e-81 | 0.67 (large) |
| Island | ANOVA F = 110.0, p = 1.5e-37; Kruskal-Wallis H = 130.1, p = 5.7e-29 | 4.5e-37 | 0.39 (large) |
| Sex | Mann-Whitney p = 1.8e-15 | 9.6e-16 | 0.18 |
| Year | ANOVA F = 0.88, p = 0.41; Kruskal-Wallis p = 0.28 | 0.41 | 0.005 (negligible) |

**Pairwise differences (Welch 95% CIs):**
- **Species:**
  - Gentoo minus Adelie: 1375 g (95% CI 1260 to 1491 g; Holm p = 2.3e-64).
  - Gentoo minus Chinstrap: 1343 g (95% CI 1214 to 1471 g; Holm p = 6.8e-48).
  - Adelie minus Chinstrap: −32 g (95% CI −150 to 86 g; Holm p = 0.59, not significant).
- **Island:**
  - Biscoe minus Dream: 1003 g (95% CI 863 to 1143 g; Holm p = 1.5e-33).
  - Biscoe minus Torgersen: 1010 g (95% CI 838 to 1181 g; Holm p = 2.6e-22).
  - Dream minus Torgersen: 7 g (95% CI −138 to 151 g; Holm p = 0.93, not significant).
- **Sex (male minus female):** 683 g (95% CI 526 to 841 g; Welch t-test p = 4.8e-16; Cohen's d = 0.94). This is pooled across species.

These results describe marginal differences. Species and island overlap, since Biscoe is mostly Gentoo, and sex is not tested within species here.

### Sex effect by species (interaction)

- Adding sex-by-species to the additive model (island included) gives F = 8.71, p = 0.0002 (df 2, 325). **The sex effect depends on species.**
- Male minus female within each species (OLS, 95% CI):
  - Adelie: 675 g (573 to 776 g; n = 73 male, 73 female).
  - Chinstrap: 412 g (254 to 570 g; n = 34 male, 34 female).
  - Gentoo: 805 g (697 to 913 g; n = 61 male, 58 female).
- The gap is positive and its CI excludes zero in all three species.
- Within Adelie, the sex-by-island interaction is not significant (F = 0.13, p = 0.88; df 2, 140). The sex effect does not vary detectably by island.

![Mean body_mass_g difference between male and female within each species, with 95% confidence intervals](tasks/stat_2/charts/sex_gap_by_species.png)

### Species-by-island interaction (not estimable)

- Chinstrap appears only on Dream and Gentoo only on Biscoe. The full species-by-island model is rank-deficient (rank 8 of 12 columns), and its F-test returned infinity with no valid p-value.
- On the five observed species-island cells, the species-by-island term has 0 degrees of freedom. It cannot be tested.
- Within Adelie, island has no detectable effect on mass: F = 0.032, p = 0.97 (df 2, 148, n = 151). This is the only estimable within-species island contrast.
- **Conclusion:** whether the species effect depends on island cannot be answered from these data.

### Prediction

Setup: fixed 75/25 split (random_state 42), 256 training and 86 test rows, 13 features. Missing sex is coded as its own category (5 in the test set). Numeric columns are median-imputed, fitted on training data.

| Model | Test MAE (g) | Test RMSE (g) | Test R² | Train R² |
|---|---|---|---|---|
| Mean baseline | 632.8 | 755.9 | −0.02 | 0.00 |
| Linear regression | 253.0 | 316.4 | 0.82 | 0.88 |
| Random forest | 276.7 | 343.7 | 0.79 | 0.98 |

- Both models clearly beat the mean baseline.
- The random forest overfits: a train-test R² gap of 0.19, against 0.06 for linear regression.
- Linear regression was chosen because it has the lower test MAE and higher test R². This choice was made on the test set, so the selected model's score is optimistic and not independently validated.

**Feature importance** (increase in test MAE when a feature is shuffled; mean of 20 repeats):
- **Species** is the strongest driver in both models. Grouped shuffling of the three species columns raises MAE by 358 g (linear regression) and 256 g (random forest).
- **Flipper length** is second in both. Single-column shuffling raises MAE by 95 g (linear regression) and 121 g (random forest).
- **Sex** ranks third in the random forest (sex_male 41 g, sex_female 31 g). In linear regression, bill_depth_mm (37 g) and bill_length_mm (27 g) rank above sex (sex_male 25 g, sex_female 17 g). The two models therefore disagree on whether bill measurements or sex carry more information. Grouped results show the same disagreement: sex 84 g versus bill_depth 35 g and bill_length 28 g in linear regression, against sex 106 g versus bill_depth 10 g and bill_length 5 g in the random forest.
- **Island and year** add essentially nothing. Grouped island shuffling changes MAE by −0.11 g (linear regression) and 2.86 g (random forest). Year changes it by 3.24 g and 1.76 g.
- **Missing sex** has no detectable signal: −1.12 g (linear regression) and −0.05 g (random forest). Its linear coefficient is 18.9 g, based on 4 training rows.

![Single-column permutation importance of each one-hot or numeric column for the best model predicting body_mass_g on the test set; species is split across three indicators](tasks/ml_1/charts/ml1_permutation_importance_v2.png)

### Missingness

**Sex missing (11 rows)**

| Factor | Counts (present/missing) | Missing rate | Exact p (Freeman-Halton) | Asymptotic p |
|---|---|---|---|---|
| Species | Adelie 146/6, Chinstrap 68/0, Gentoo 119/5 | Adelie 3.9%, Chinstrap 0%, Gentoo 4.0% | 0.26 | 0.25 |
| Island | Biscoe 163/5, Dream 123/1, Torgersen 47/5 | Biscoe 3.0%, Dream 0.8%, Torgersen 9.6% | 0.018 | 0.0099 |
| Year | 2007 103/7, 2008 113/1, 2009 117/3 | 2007 6.4%, 2008 0.9%, 2009 2.5% | 0.061 | 0.057 |

- All tables have expected counts below 5, so the exact p-values are the basis for conclusions.
- The island association (exact p = 0.018) rests on 11 missing rows, 5 of them on Torgersen. It is a tentative lead, not an established association.
- Species and year associations are not supported.
- The 9 rows with missing sex have a mean body_mass_g of 4005.6 g, against 4207.1 g for rows with sex recorded. This gap was not tested for significance.

**Missing body_mass_g (2 rows)**
- Missingness shows no association with species (exact p = 1.0), island (exact p = 0.41) or year (exact p = 0.77).
- With 2 missing rows, these tests have almost no power and are not meaningful.

## Limitations

- **Unresolved review issue (affects the stat_1 sex finding and the Summary).** The sex η² (0.18) is computed with total sum of squares over all non-missing body_mass_g rows, while the 9 rows with missing sex are excluded from the group sums. The sex η² is therefore slightly understated. The Gentoo-minus-Adelie line carries no Cohen's d, and no pairwise Cohen's d values are reported here.
- **Confounding.** Species and island overlap strongly (Biscoe is mostly Gentoo). The island differences are unadjusted for species. The sex difference is pooled across species, and the within-species gaps differ.
- **Interactions not fully answered.** The species-by-island interaction has no valid p-value (stat_2 and stat_4 both show it is not estimable on these data). The direct test of whether the male-female gap differs between Chinstrap and Gentoo was not run. These two species never share an island.
- **Missingness.** The sex-by-island association is based on 11 missing rows and is tentative. The sex-missing and body_mass-missing comparisons are underpowered. The lower mass of the 9 rows with missing sex was not tested.
- **Prediction.** Results come from a single split with 86 test rows. The linear regression model was selected on the test set, so its test scores are optimistic. The random forest was not tuned, and its train-test gap is large. Feature rankings disagree between the two models on bill measurements versus sex. The sex_missing coefficient rests on 4 training rows.
- **Failed or partial tasks.** stat_2 and stat_4 are marked partial. The species-by-island interaction could not be tested with a p-value. No task failed outright.

## Open questions

- Does the male-female body mass gap differ between Chinstrap and Gentoo? This comparison was proposed but not run, because the two species do not share an island.
- Does the Torgersen excess of missing sex (5 of 52 rows) reflect data collection, and does it bias the sex comparison? A Torgersen-versus-rest 2×2 Fisher exact test was proposed but not run.
- Are the 9 rows with missing sex lighter than expected given their species and island? If so, missingness would not be random. This was not tested.
- Is the island effect explained by species composition? Within Adelie, island shows no effect, but the full question was not tested with a valid model.
- Would species-specific models or species-by-sex interaction terms improve prediction beyond the additive linear model?
- Would a tuned or regularised random forest, selected by cross-validation rather than on the test set, reduce the 0.19 train-test gap?
- Do bill measurements and sex carry different information? The two models rank them differently, and this was not resolved.