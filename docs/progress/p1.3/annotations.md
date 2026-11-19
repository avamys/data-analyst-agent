# P1.3 reference run: claim-by-claim check

Report: [report.md](report.md) · run `20261101-121244_titanic_qwen3.5-9b` · commit `2eb8a56` · 6 tasks, 54 min, 38 LLM calls, 9 charts.
Method as in the [baseline annotations](../../baseline/annotations.md).

**Legend:** ✅ correct · ❌ wrong · ⚠️ unsupported (not computed in this run) · ➖ misleading or incomplete

## Summary

| | Baseline | P1.2 | P1.3 |
|---|---|---|---|
| ✅ Correct | 15 | 14 | 14 |
| ❌ Wrong | 7 | 4 | 3 |
| ⚠️ Unsupported | 6 | 7 | 7 |
| ➖ Misleading | 6 | 2 | 3 |
| Baseline findings still absent | 7 | 6 | 5 |
| Charts | 0 | 6 | 9 |

- **Better:**
  - **Two baseline findings are back:** survival by class (63/47/24%) and fare by outcome (48.40 vs 22.12).
  - **Column kinds work:** ml_1 dropped the ID and text columns (PassengerId, Name, Ticket, Cabin) instead of encoding them.
  - **The missingness analysis is thorough:** Age missing 23% vs 9% depending on Cabin.
- **Worse:**
  - **No model was trained.** `ml_1` again didn't publish its split, `ml_2` spent 5 steps on `load` errors and missing imports, and the report has no model metrics.
  - **The report is cut off mid-sentence:** prompt (6,262 tokens) + output (1,930) filled the 8,192-token context.
- **The two remaining wrong statistics come from findings that cite no facts.** `stat_1` recorded one fact (a text note) but reported six tests with numbers. The citation check only rejected unknown fact names, so a finding citing nothing passed. Its Age t-test claims survivors were *older* with p < 0.001; the data says younger, p = 0.04.

## Claims

| Line | Claim | Verdict | Truth / evidence |
|---|---|---|---|
| 4 | Survival 63% in 1st class vs 24% in 3rd | ✅ | `eda_2.eda_2_survival_rate_by_class` |
| 4 | Lifeboat access was "heavily stratified by ticket class" | ⚠️ | Interpretation beyond the data |
| 5 | Gender is the strongest single predictor, Cramér's V = 0.54 | ✅ | True (0.541), but not recorded as a fact |
| 5 | The gender advantage was "significantly diminished for women in lower classes" | ⚠️ | Not computed (true: 96.8% in 1st vs 50.0% in 3rd) |
| 6 | Fare: p < 0.001, Cohen's d = 0.55 | ✅ | Not recorded as a fact |
| 6 | Wealthier passengers had "safer deck locations or priority boarding" | ⚠️ | Speculation |
| 7 | Imputation reduced missing values to zero "while preserving demographic distributions" | ⚠️ | Zero missing is recorded; preservation was never checked |
| 8, 61 | Logistic Regression "is expected to achieve > 80%" | ⚠️ | No model was trained |
| 17 | 342 survivors (38.4%), 549 non-survivors | ✅ | |
| 28 | "Execution Time: 151.0 seconds" | ➖ | Code time only; the run took 54 minutes |
| 38 | Cabin 687 missing (77%): 479 in 3rd class, 515 at Southampton | ✅ | |
| 38 | Southampton passengers "had less recorded cabin information" | ➖ | Confounded: 72% of passengers boarded at Southampton, mostly in 3rd class |
| 39 | Age 177 missing; P(Age missing) is 23% when Cabin is missing vs 9% | ✅ | 0.230 vs 0.093 |
| 41–43 | Survival 63.0% / 47.3% / 24.2% by class | ✅ | |
| 45 | Mean fare 48.40 (survived) vs 22.12 (died); max 512.33 | ✅ | |
| 53 | Embarked: p < 0.001, V = 0.17 | ✅ | χ² p = 1.8 × 10⁻⁶, V = 0.173 |
| 54 | Age: survivors **older**, p < 0.001, d = 0.37 | ❌ | Survivors are younger: p = 0.039 (Student) / 0.041 (Welch), d = −0.16 |
| 55 | Parch: p = 0.013, d = 0.17 | ✅ | Welch p = 0.0134 |
| 57 | SibSp: p = 0.23, not significant | ✅ | Welch p = 0.233 |
| 62–69 | Feature importance hierarchy "derived from statistical analysis" | ⚠️ | No importances computed |
| 72 | 3rd-class women survived at 24% vs 96% for 1st-class women | ❌ | 3rd-class women: 50.0%; 24% is all of 3rd class. 96.8% is right but wasn't computed. |
| 74 | High fares "almost exclusively" in 1st class | ⚠️ | Not computed |
| 77 | Survival is "primarily a function of Class, followed closely by Gender" | ❌ | Contradicts the report's own effect sizes (Sex V = 0.54 vs Pclass 0.34) and its line 5 |
| 80 | 11 Age values outside the IQR fences | ✅ | |
| 81 | Fare is right-skewed; a log transform was suggested but not applied | ✅ | |
| 82 | The model comparison could not be completed | ✅ | Honest limitation |
| 83 | (report ends mid-sentence) | ➖ | The context window filled up |

## Fixes before P1.4

| Problem | Fix |
|---|---|
| Findings that cite no facts pass validation | Every finding must cite at least one recorded fact; otherwise the specialist gets feedback |
| A failed cell's replacement drops its other imports (`ml_2`: fixing `accuracy_score` lost `LogisticRegression`, and the other way round) | On failure, the observation says the next cell replaces the failed one *completely*: repeat its imports and setup |
| `seaborn` tried again despite the library list (`eda_3`, 2 steps) | Install it: two runs show the model reaches for it regardless |
| `save_chart("ml_1/x", …)` failed on the slash | Chart names are made filename-safe |
| Report cut off by the 8k context | `num_ctx` 16,384; on this machine `LLM_NUM_GPU=17` keeps the same GPU headroom (3.39 GB, ~12% slower). P1.5 removes the duplicate synthesis draft from the writer's prompt. |
| `ml_1` doesn't publish what `ml_2` needs | P1.4: briefs name the expected outputs |
