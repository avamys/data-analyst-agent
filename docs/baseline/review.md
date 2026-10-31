# Baseline review: how the agent behaves today

Reference run: [run/](run/) (`20261031-204254_titanic_qwen3.5-9b`, commit `03d2f98`, tag `v0.1.0-baseline`). Claim-by-claim check of the report: [annotations.md](annotations.md).

## The run

| Step | Time | LLM calls | What it produced |
|---|---|---|---|
| Orchestrator | 51 s | 1 | Strategies: exploratory → statistical → predictive; asked for 15 tasks |
| Planner | 67 s | 1 | 6 tasks (capped): 2 EDA, 1 statistical, 3 ML |
| Execution | 16 min | 9 | 6 / 6 tasks succeeded; `ml_2` needed 2 attempts, `ml_3` needed 3 |
| Synthesizer | 3 min | 1 | 1,641-token summary |
| Reporter | 4 min | 1 | 2,138-token report |
| **Total** | **25 min** | **13** | 14k input / 13k output tokens |

## What works

1. **Planning is sensible.** The strategy fits a binary-target dataset, task dependencies are logical, and the plan passed validation.
2. **Analysis code is mostly correct.** Both EDA tasks and the chi-square task ran on the first attempt, and every number they printed matches the data.
3. **Retries recover.** Both failing tasks succeeded on a later attempt.
4. **No invented numbers.** Every specific number in the report traces to code output. The legacy report (llama3.1:8b) got the headline survival rate backwards; this one doesn't.
5. **The report reads well.** It's well structured and in the right register.
6. **The run is observable.** This review was done entirely from the run directory.

## What's wrong, ranked by impact

### 1. Results don't reach the writer (root cause of most report errors)
- **Synthesizer:** it sees only the first **5 lines** of each task's output ([synthesizer.py](../../agent/nodes/synthesizer.py), `_summarize_results`).
- **Reporter:** it gets 15 lines per task, then the whole findings section is cut at **3,000 characters** ([reporter.py](../../agent/nodes/reporter.py)). In this run the cut fell in the middle of the first ML task's title, so the reporter saw no ML output at all.
- **Consequences:**
  - The feature ranking in the report is guessed, and wrong (Fare, the top feature, is missing).
  - Embarked's χ² appears as "N/A".
  - The precision/recall section admits the numbers "were truncated".
  - The strongest findings, survival 74% (women) vs 19% (men) and 63/47/24% by class, are absent.

### 2. Code is written blind, so "interpretations" are guesses
- **Pre-written interpretations:** the specialist prompts ask for "interpretation in print statements". The model writes those sentences before the code has run.
  - `ml_1` prints "top features are typically Sex and Pclass" right below output ranking Fare first.
  - `eda_2` prints "If survival rates differ significantly, Cabin presence is a strong predictor".
- **Insights scraped from those guesses:** the regex `InsightExtractor` then pulls "insights" out of these sentences ("good generalization on unseen data", "if the missingness is random or informative"), and they go to the synthesizer as findings.
- **No one ever reads the actual output** to draw conclusions. The synthesizer and reporter get it only truncated.

### 3. Tasks don't share anything
Each task is a separate script with a fresh Python REPL. It reloads the CSV and redoes all preprocessing.
- **Three RF fits:** the planner split ML into prepare → train → evaluate, so the Random Forest was fit three times, with different preprocessing and different splits (110/69 vs 105/74 test rows). That gave three different accuracies (81.0%, 82.7%, 82.1%).
- **Tasks drift from their descriptions:** `ml_1` ("prepare features and split") trained and evaluated a model instead, and `ml_3` ("compare models") evaluated only one.
- **Dependencies carry little:** a task only gets the first 500 characters of the output of the tasks it depends on.

### 4. Nobody checks the results
Nothing questions the numbers.
- **Overfitting:** a 98% train vs 82% test gap is called "healthy" and "strong generalization".
- **Contradictions:** line 84 of the report contradicts line 73.
- **No sanity checks:** none for overfitting, leakage, imbalance, or contradictions between tasks.

### 5. Prompts steer too hard, and toward Titanic
- **The ML example becomes the answer:** the ML prompt's example is a complete RF pipeline, and every ML task produced one regardless of what it was asked.
- **Titanic leaks into generic prompts:** the examples use "Survival Rate" and "Sex vs Survived", so the prompts won't transfer to other datasets.
- **The prompt forbids plots,** yet the report claims it "visualized distributions".
- **The environment isn't described.** The model doesn't know which libraries are installed.

### 6. Retries are spent on avoidable errors
- **Avoidable:** `import seaborn` (not installed), a syntax error from a stray trailing `.`, a hallucinated `scipy.stats.cramers_v` (in the earlier failed run).
- **Real:** a `KeyError` from dropping a column that wasn't there.
- **Cheap fixes:** listing the available libraries and a `compile()` check before running would have saved 3 of the 4 retries.
- **Repeated errors:** in the failed run, the ML task hit the *same* `LabelEncoder` error twice, so the error feedback doesn't always work.

### 7. The profile is sloppy
- **Target and IDs listed as features:** `PassengerId` and the target `Survived` itself are counted among the 7 numeric features.
- **Free-text columns treated as categories:** `Name` and `Ticket` (unique per row) are counted as categorical.
- **The report repeats it:** it inherits the miscount (annotation line 13).

### 8. Too many management hops, too little analysis
- **Writing costs as much as analysing:** 4 of 13 calls are orchestration or writing (orchestrator, planner, synthesizer, reporter). Synthesizer + reporter take 7 of the 25 minutes, and the synthesizer is only a lossy draft for the reporter.
- **Budget spent on fragments:** with a 6-task budget, 3 tasks went to fragments of one ML pipeline.
- **Gaps in coverage:**
  - only one statistical test family
  - no tests on the numeric features (Fare, Age)
  - no interactions (sex × class)

### Smaller
- "Total Execution Time: 9.0 seconds" is the code time only; the run took 25 minutes.
- "100% success rate" hides that 2 of 6 tasks needed retries.
- The χ² variant (with or without continuity correction) isn't stated.

## Proposed Phase 1: agent quality (for discussion)

**Goal:** everything the analysis computes reaches the report, every interpretation is based on actual results, and tasks build on each other.

| # | Change | Fixes |
|---|---|---|
| 1.1 | **Shared analysis session.** One Python process per run, so tasks build on each other's variables (`df`, cleaned data, train/test split, fitted models) like cells in a notebook. Runs in a subprocess with a timeout; success = no exception. | 3, part of 6; groundwork for the sandbox |
| 1.2 | **Structured findings instead of scraped stdout.** Code records results with a helper (`record_fact(name, value, desc)`). After a task runs, the specialist reads its *actual* output and writes findings. No interpretations in print statements; the regex extractor is removed. | 1, 2 |
| 1.3 | **One writer with the full fact table.** Merge synthesizer + reporter; the writer gets all recorded facts and findings, not truncated text. | 1, 8 |
| 1.4 | **Deterministic sanity checks** that add caveats: train/test gap, near-perfect feature–target correlation, class imbalance, many tests without correction. | 4 |
| 1.5 | **Generic, task-faithful prompts.** No Titanic examples, no full example pipelines. Describe the environment (libraries, session variables). Check `compile()` before running. | 5, 6 |
| 1.6 | **Profiler fixes.** Exclude the target, flag ID-like and free-text columns. | 7 |
| 1.7 | **Merge orchestrator + planner,** with a planner that knows the task budget and covers the basics (target, key groups, numeric tests, one model). | 8 |

**How to check it (until the eval harness exists):** re-run the reference run after each change and repeat the annotation. Target: 0 wrong, at most 2 unsupported, and every finding in "computed but missing" present in the report.

**Effect on the plan:** this pulls the core of the old Phase 2 (execution harness) and Phase 3 (grounded reporting) forward, ahead of the eval harness. The before/after story still works: `v0.1.0-baseline` is tagged, and the eval harness's report-level graders can score it later.
