# Titanic Survival (Target: Survived): Final Report

## Summary

- **Sex and passenger class are the strongest unadjusted associations with survival.** Females survived at 74.2% against 18.9% for males. Survival fell with class: 63.0% in Pclass 1, 47.3% in Pclass 2 and 24.2% in Pclass 3. Sex has the largest effect size (Cramér's V 0.543).
- **After joint adjustment, Sex and class remain significant, but Fare does not.** In the adjusted model, the female vs male odds ratio is 14.24 and the Pclass 2 and 3 odds ratios (vs Pclass 1) are 0.318 and 0.096. The Fare odds ratio is 1.0017 per unit (p = 0.505). Age and FamilySize remain significant, and Embarked does not.
- **The effect of Sex depends on class, but two analyses disagree on the size of that dependence.** Both find a significant Sex × Pclass interaction (LR chi² 28.79 in stat_2; 31.81 in stat_4). The within-class female vs male odds ratios differ between them and are not reconciled.
- **The raw SibSp and Parch advantages are not established after stratifying on Sex and Pclass.** The Mantel-Haenszel odds ratios are 0.811 (CI 0.541 to 1.216) for SibSp and 0.652 (CI 0.401 to 1.06) for Parch. Whether Sex and Pclass composition explains the raw gaps was not tested.
- **Both predictive models beat the majority-class baseline of 61.5% on the test split.** Random forest reaches 82.7% accuracy (a gain of about 21 points) and logistic regression 80.4% (a gain of about 19 points). The random forest is clearly overfit (training accuracy 0.983), so its test scores are optimistic.

## Data

- **Size:** 891 rows × 12 columns.
- **Target:** Survived, binary. 342 passengers survived (38.4%) and 549 died (61.6%).
- **Features used:** Numeric: Pclass, Age, SibSp, Parch, Fare. Categorical: Sex, Embarked. No date or time features.
- **Not used as features as they are:** PassengerId, Ticket, Cabin and Name (identifiers or free text).
- **Missing values:**
  - Cabin: 687 rows (77.1%)
  - Age: 177 rows (19.9%)
  - Embarked: 2 rows (0.2%)
  - The other columns have no missing values.

## Findings

### Descriptive survival rates (eda_1)

Rates below are unadjusted. Each group's survival rate is the group mean of Survived.

- **Sex:** Females survived at 74.2% (n=314) and males at 18.9% (n=577).

  ![Survival rate by Sex (red line: overall rate)](tasks/eda_1/charts/survival_rate_by_sex.png)

- **Pclass:** Pclass 1 survived at 63.0% (n=216), Pclass 2 at 47.3% (n=184) and Pclass 3 at 24.2% (n=491). Fare and Pclass are correlated, so these rates overlap with the Fare effect.

  ![Survival rate by Pclass (red line: overall rate)](tasks/eda_1/charts/survival_rate_by_pclass.png)

- **Fare quartile:** Survival rose with fare. Q1 (mean fare 7.03) survived at 19.7% (n=223), Q2 (mean fare 10.39) at 30.4% (n=224), Q3 (mean fare 23.03) at 45.5% (n=222) and Q4 (mean fare 88.68) at 58.1% (n=222).

  ![Survival rate by FareQuartile (red line: overall rate)](tasks/eda_1/charts/survival_rate_by_farequartile.png)

- **Embarked:** Cherbourg (C) survived at 55.4% (n=168), Queenstown (Q) at 39.0% (n=77) and Southampton (S) at 33.7% (n=644). The 2 passengers with missing Embarked are excluded.

  ![Survival rate by Embarked (red line: overall rate)](tasks/eda_1/charts/survival_rate_by_embarked.png)

- **Age bin:** Children under 16 survived at 59.0% (n=83). Ages 16–32 were lowest at 36.2% (n=345), ages 32–48 at 40.1% (n=197) and ages 48+ at 41.6% (n=89). The 177 passengers with missing Age are excluded.

  ![Survival rate by AgeBin (red line: overall rate)](tasks/eda_1/charts/survival_rate_by_agebin.png)

- **SibSp:** SibSp 0 survived at 34.5% (n=608) and SibSp 1 at 53.6% (n=209). SibSp 2 was 46.4% (n=28), SibSp 3 25.0% (n=16), SibSp 4 16.7% (n=18), SibSp 5 0.0% (n=5) and SibSp 8 0.0% (n=7). The SibSp 5 and SibSp 8 groups are too small for firm conclusions.
- **Parch:** Parch 0 survived at 34.4% (n=678) and Parch 1 at 55.1% (n=118). Parch 2 was 50.0% (n=80), Parch 3 60.0% (n=5), Parch 4 0.0% (n=4), Parch 5 20.0% (n=5) and Parch 6 0.0% (n=1). Groups of 3 or more are too small for firm conclusions.

### Missingness (eda_2)

- **Age missingness** is associated with lower survival. Rows with Age missing survived at 29.4% (n=177), against 40.6% for rows with Age present (n=714).
  - Among Age-missing rows, 76.8% are Pclass 3 (136), 16.9% Pclass 1 (30) and 6.2% Pclass 2 (11). There are 124 males and 53 females.
  - Within Pclass 1, Age-missing rows survived at 46.7% (n=30) against 65.6% for Age-present rows (n=186).
  - Within Pclass 2, Age-missing rows survived at 36.4% (n=11) against 48.0% (n=173).
  - Within Pclass 3, Age-missing rows survived at 25.0% (n=136) against 23.9% (n=355), so there is no visible gap in that class.

  ![Survival rate for rows with Age missing versus present](tasks/eda_2/charts/survival_by_age_missing.png)

- **Cabin missingness** tracks class. Cabin is missing for 18.5% of Pclass 1 rows, 91.3% of Pclass 2 rows and 97.6% of Pclass 3 rows. Rows with Cabin missing survived at 30.0% (n=687), against 66.7% for rows with Cabin present (n=204). Because Cabin missingness is so closely tied to class, this association is largely confounded with Pclass.
- **Embarked missingness:** The two rows are passengers 62 and 830, both Pclass 1 with a Fare of 80.0.

### Marginal association tests (stat_1)

All tests are unadjusted marginal associations. Holm adjustment was applied across the six features.

- **Sex:** chi² 263.05 (df 1), p = 3.7e-59, Cramér's V 0.543. Female vs male OR 12.35 (95% CI 8.90 to 17.14). Holm-adjusted p ≈ 2.2e-58.
- **Pclass:** chi² 102.89 (df 2), p = 4.5e-23, Cramér's V 0.340. OR Pclass 1 vs 3 is 5.31 (95% CI 3.76 to 7.50). OR Pclass 2 vs 3 is 2.80 (95% CI 1.96 to 4.00).
- **Fare:** Mann-Whitney p = 4.6e-22, rank-biserial −0.384, Cohen's d 0.547 (n=891). Survivors paid higher fares. Fare is correlated with Pclass, so this effect cannot be separated from class here.
- **FamilySize** (clipped at 5 for the test): chi² 77.59 (df 4), p = 5.6e-16, Cramér's V 0.295.
- **Embarked:** chi² 26.49 (df 2), p = 1.8e-6, Holm-adjusted p = 3.5e-6, Cramér's V 0.173. It overlaps with Pclass and Fare.
- **Age:** Mann-Whitney p = 0.160, rank-biserial 0.062, Cohen's d −0.157 (n=714). Not significant.

Ranking by effect size: Sex (V 0.543), Fare (|rank-biserial| 0.384), Pclass (V 0.340), FamilySize (V 0.295), Embarked (V 0.173), Age (|rank-biserial| 0.062). Cramér's V and rank-biserial are on different scales, so the ranking across them is approximate. The ranking should not be read as independent contributions.

![Effect size of each feature on survival (Cramer V for categorical, absolute rank-biserial for Fare and Age). All values are unadjusted marginal associations; Fare and Pclass are correlated and not separable here.](tasks/stat_1/charts/stat1_effect_sizes_v2.png)

*The earlier chart stat1_effect_sizes is superseded and is not used here.*

### Sex × Pclass interaction (stat_2)

- **Survival by Sex and Pclass:**
  - Female: 96.8% in Pclass 1 (91/94), 92.1% in Pclass 2 (70/76), 50.0% in Pclass 3 (72/144).
  - Male: 36.9% in Pclass 1 (45/122), 15.7% in Pclass 2 (17/108), 13.5% in Pclass 3 (47/347).

  ![Survival rate by Sex and Pclass (n per cell in the facts)](tasks/stat_2/charts/stat2_rates.png)

- **Interaction test:** Adding Sex × Pclass to the additive logit model improves fit (LR chi² 28.79, df 2, p = 5.6e-7; AIC 834.9 additive vs 810.1 with interaction). The female × Pclass 3 coefficient is −2.10 (p = 0.0014) and the female × Pclass 2 coefficient is 0.18 (p = 0.82). The interaction comes mainly from Pclass 3, where the female advantage is smaller.
- **Female vs male OR by class:** Pclass 1: 51.9 (95% CI 15.5 to 173.6). Pclass 2: 62.5 (95% CI 23.4 to 166.6). Pclass 3: 6.4 (95% CI 4.1 to 10.0). The Pclass 1 and 2 estimates are inflated by near-ceiling female survival and have wide intervals, so the Pclass 3 value is the more stable comparison.
- **Sex × Age (known-age subset, n=714):** Adding female × Age, with Age main effect and Pclass in the model, gives LR chi² 11.90, p = 0.00056. The coefficient is +0.050 per year of age on the log-odds scale (p = 0.00074), so the female advantage grows with age. The term is statistically detectable. The 177 passengers with missing Age are excluded, so the result may not generalise to the full sample. This is an association, not a causal estimate.

### Sex × Pclass interaction in the adjusted model (stat_4)

This model is the joint adjusted model (see the next section). Its interaction result **disagrees** with stat_2:

- LR chi² 31.81 (df 2, p = 1.2e-7).
- Within-class female vs male ORs: 37.4 in Pclass 1, 86.4 in Pclass 2 and 4.85 in Pclass 3.

The stat_2 and stat_4 values were recorded under different specifications. The lead has not reconciled them, so both are reported here. Neither is the single correct figure.

### Family size: SibSp and Parch adjusted for Sex and Pclass (stat_3)

Mantel-Haenszel pooled ORs were computed within the six Sex × Pclass strata. Composition shares of the SibSp and Parch groups were not computed (see Limitations).

- **SibSp 1 vs 0:** MH OR 0.811 (95% CI 0.541 to 1.216), p = 0.29. The raw advantage (53.6% vs 34.5%) is not established after adjustment. The adjusted estimate points slightly below 1 and its CI spans 1.

  Within-stratum survival, SibSp 0 vs SibSp 1 (n in parentheses):

  | Stratum | SibSp 0 | SibSp 1 |
  |---|---|---|
  | Female, Pclass 1 | 98.0% (49) | 95.0% (40) |
  | Female, Pclass 2 | 93.2% (44) | 89.3% (28) |
  | Female, Pclass 3 | 59.3% (81) | 44.7% (38) |
  | Male, Pclass 1 | 32.9% (88) | 48.4% (31) |
  | Male, Pclass 2 | 11.8% (76) | 25.9% (27) |
  | Male, Pclass 3 | 13.0% (270) | 22.2% (45) |

  The within-stratum differences have mixed signs. Several gaps rest on SibSp 1 counts of 27 to 38, so they are imprecise.

- **Parch 1 vs 0:** MH OR 0.652 (95% CI 0.401 to 1.06), p = 0.066. The raw advantage (55.1% vs 34.4%) is not established after adjustment, and the adjusted estimate points the other way from the raw comparison.

  Within-stratum survival, Parch 0 vs Parch 1 (n in parentheses):

  | Stratum | Parch 0 | Parch 1 |
  |---|---|---|
  | Female, Pclass 1 | 98.4% (64) | 100.0% (17) |
  | Female, Pclass 2 | 88.9% (45) | 94.4% (18) |
  | Female, Pclass 3 | 58.8% (85) | 48.0% (25) |
  | Male, Pclass 1 | 36.4% (99) | 28.6% (14) |
  | Male, Pclass 2 | 9.0% (89) | 50.0% (14) |
  | Male, Pclass 3 | 12.2% (296) | 26.7% (30) |

  The largest gap (male Pclass 2, +41.0 points) rests on only 14 passengers in the Parch 1 group. The female Pclass 1 stratum has n=17 in the Parch 1 group and is too small for firm conclusions.

![Survival rate within Sex x Pclass strata for SibSp 0 vs 1 and Parch 0 vs 1 (rates, not counts)](tasks/stat_3/charts/family_survival_strata.png)

### Joint adjusted model (stat_4)

The logistic model adjusts for Sex, Pclass, Age, Fare, Embarked and FamilySize on 712 complete cases. The 179 dropped rows are 177 with missing Age and 2 with missing Embarked. The model has no Sex × Pclass term unless stated.

| Term | Adjusted OR | 95% CI | p |
|---|---|---|---|
| Female vs male | 14.24 | 9.23 to 21.99 | < 0.001 |
| Age (per year) | 0.959 | 0.944 to 0.975 | < 0.001 |
| Fare (per unit) | 1.0017 | 0.9966 to 1.0069 | 0.505 |
| Fare (per 10 units) | 1.018 | 0.967 to 1.071 | — |
| FamilySize (continuous) | 0.809 | 0.695 to 0.942 | 0.006 |
| Embarked Q vs C | 0.430 | 0.134 to 1.388 | 0.158 |
| Embarked S vs C | 0.654 | 0.382 to 1.117 | 0.120 |
| Pclass 2 vs 1 | 0.318 | 0.168 to 0.604 | 0.0005 |
| Pclass 3 vs 1 | 0.096 | 0.049 to 0.187 | < 0.001 |

- **Sex:** The OR of 14.24 is slightly above the unadjusted 12.35. It assumes a common Sex effect across classes, which the interaction result above contradicts. The single OR should not be read as a uniform effect.
- **Pclass:** The class effect remains significant after adjustment. The ORs are relative to Pclass 1.
- **Fare:** Not significant after adjustment. The unadjusted Fare association (stat_1) does not survive joint adjustment. Fare correlates with Pclass (r = −0.549 on 891 rows). VIFs are 1.76 for Fare and 2.81 for Pclass 3, below the usual threshold of 5. The VIFs are consistent with class carrying much of the Fare association, but this is an interpretation, not a tested result. The model does not separate the two effects.
- **Age:** Significant after adjustment (OR 0.959 per year), although not significant unadjusted (p = 0.160 in stat_1).
- **FamilySize:** Significant with a continuous term (OR 0.809 per member). The test is not directly comparable to the categorical unadjusted test in stat_1.
- **Embarked:** Not significant after adjustment. The estimates are imprecise, and the result does not show that the unadjusted association is explained by class and fare.

### Predictive models (ml_1)

Models were fitted on a stratified 80/20 split (712 training, 179 test). The test-split majority-class baseline accuracy is 61.5%. This differs from the 61.6% overall class share, and the 61.5% is the figure for comparing with the test-split models.

| Model | Test accuracy | ROC AUC | F1 | Precision | Recall | Training accuracy |
|---|---|---|---|---|---|---|
| Random forest | 82.7% | 0.833 | 0.763 | 0.807 | 0.725 | 0.983 |
| Logistic regression | 80.4% | 0.850 | 0.729 | 0.783 | 0.681 | 0.802 |

- Against the 61.5% baseline, random forest accuracy is a gain of about 21 points and logistic regression a gain of about 19 points.
- The two models are close and neither clearly dominates. The forest has higher accuracy and F1; logistic regression has higher ROC AUC. The 2-point accuracy gap is about 4 passengers on 179, which is within noise.
- **The random forest is overfit.** Its training accuracy is 0.983 against 0.827 on test, so its test scores are optimistic.

**Feature importance.** The two methods disagree.

- Random forest impurity importances (training split of the overfit model): Fare 0.253, Age 0.238, Sex male 0.142, Sex female 0.141, Pclass 0.084, FamilySize 0.046. These importances favour continuous features and are not reliable evidence that Fare and Age matter most. They disagree with the logistic ranking on Fare.
- Logistic coefficients (standardised; within this additive model): Sex male −1.29, Sex female +1.26, Pclass −0.89, Age −0.49, Embarked S −0.34, Embarked Q +0.34, IsAlone −0.31, SibSp −0.29, FamilySize −0.22, Fare +0.086.

![Random forest feature importance on the training split](tasks/ml_1/charts/ml1_rf_importance.png)

The logistic ranking is an association within this model, not a driver ranking. The additive model omits the Sex × Pclass interaction (stat_2: LR chi² 28.79, 2 df, p = 5.6e-7), so the Sex and Pclass coefficients describe an additive fit that is misspecified for the class 3 female contrast. The Age coefficient is conditional on the other features, was fitted with median imputation for the 19.9% of rows with missing Age, and contrasts with the non-significant marginal Age result in stat_1 (Mann-Whitney p = 0.160).

## Limitations

- **Missing data.** Age is missing for 19.9% of rows and Cabin for 77.1%. Age-missing passengers survived less often and are concentrated in Pclass 3. Cabin is not used as a feature in any model. The adjusted models (stat_4) use complete cases only (712 of 891), and the dropped rows may not be representative. The ML models use median imputation for Age. The subset results in stat_2 cover known-age passengers only.
- **Unadjusted and marginal associations.** The stat_1 tests and effect sizes are unadjusted. Fare, Pclass and Embarked overlap, and the effect sizes are on different scales, so the ranking is approximate.
- **Small groups.** SibSp of 5 or more, Parch of 3 or more, and several Sex × Pclass × family strata have small counts. Their rates are not reliable.
- **Sex × Pclass disagreement (not resolved).** stat_2 reports within-class female vs male ORs of 51.9, 62.5 and 6.4, with LR chi² 28.79. stat_4 reports 37.4, 86.4 and 4.85, with LR chi² 31.81. The two were recorded under different specifications, and the discrepancy has not been reconciled.
- **Reference-category mismatch in stat_4 (not resolved).** The stat_4 Pclass ORs are relative to Pclass 1, while the unadjusted ORs in stat_1 are relative to Pclass 3. The adjusted-versus-unadjusted comparison cannot be read as showing that adjustment strengthened the class gradient, so no such claim is made here.
- **Unresolved review issue, stat_2 (Age × Sex).** The lead's objection still stands. The female × Age term is statistically detectable (LR chi² 11.90, p = 0.00056; coefficient p = 0.00074) with a positive coefficient of 0.050 per year. The lead also asked for a statement of its material size across the age range. No multiplicative figure is given in this report, because none is a recorded fact. The result applies only to the 714 known-age passengers and is an association only.
- **Unresolved review issue, stat_3 (family size).**
  - Composition shares of Sex and Pclass for the SibSp = 1 and Parch = 1 groups were not computed for either variable. The part of the brief asking whether the gaps persist or are explained by composition is unanswered.
  - The SibSp adjusted estimate is not established, and composition was not tested. The report does not imply that the raw advantage simply disappears.
  - All six strata are shown for each variable, including Parch female Pclass 1 (n=64 at 98.4% vs n=17 at 100%).
- **Unresolved review issue, ml_1 (logistic ranking).** The objection still stands and is stated in the findings: the logistic coefficients omit the Sex × Pclass interaction, the Age coefficient is conditional and uses median imputation, and the coefficient ranking is an association within this model, not a driver ranking.
- **Model evaluation.** The random forest is overfit. Test scores come from a single split, and the model comparison has no confidence intervals. Permutation importance and repeated cross-validation were not run.
- **Failed tasks.** None are recorded.

**Numbers not traced to a recorded fact.** The automatic check found no recorded value for these numbers:
- 21 in: "- **Both predictive models beat the majority-class baseline of 61.5% on the test split.** Random forest reaches 82.7% accuracy (a gain of about 21 points) and l"
- 21 in: "- Against the 61.5% baseline, random forest accuracy is a gain of about 21 points and logistic regression a gain of about 19 points."

## Open questions

- Do the stat_2 and stat_4 Sex × Pclass results agree once their specifications are checked? What are the correct within-class female vs male odds ratios?
- Is the female advantage in Pclass 3 explained by Fare, Embarked or family size, which are correlated with class? Does the Sex × Pclass interaction hold in a model that includes Fare and FamilySize?
- Does the Age × Sex interaction hold within each Pclass, or is it driven by Pclass 3? Does it hold when the 177 age-missing passengers are included, through imputation or a missing-indicator model?
- Does imputing the 177 missing ages change the Age and Embarked estimates? Does it change the Age-based survival patterns reported in eda_1?
- Is the Age effect present within Sex or Pclass strata, and does it differ between them?
- Is the Cherbourg survival advantage explained by the higher Pclass and Fare share among Cherbourg passengers?
- Is the Fare effect independent of Pclass when Fare is modelled within class strata?
- Do the Sex and Pclass composition shares of the SibSp = 1 and Parch = 1 groups account for the raw gaps? Does the male Pclass 2 Parch gap (50% vs 9%, n=14 vs 89) hold in a larger sample or a logistic model with Sex × Pclass × family-size terms?
- Are the Fare and Age importances in the random forest real? A permutation importance on the test split would test this.
- What are the confidence intervals for the accuracy and AUC gaps between the two models, and for the forest's overfit estimate? Repeated stratified cross-validation would answer this.
- Does the Cabin deck letter, derived from Cabin where present, add information without leaking the class effect?