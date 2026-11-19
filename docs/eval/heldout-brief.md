# Brief: the held-out eval cases (P3.2b)

Phase 3's fixes are developed on the 12 dev cases in `evals/cases/`. The held-out cases test whether those fixes work on data nobody tuned them on. To make that hold, the person who writes the fixes (Claude) must not see the held-out cases until P3.5, and no agent runs on them before then.

## Keeping them blind
 
- Everything goes in `evals/heldout/`. It's gitignored, so the files stay out of commits, diffs and `git grep`.
- Don't paste case contents, names or numbers into a session with Claude. Close the files before you chat: the editor tells Claude which file is open, and sends any text you select.
- Don't run the agent on them, not even once to see whether a case is too easy. Choosing cases by how the current agent does on them biases the test as much as tuning the agent does.
- Run your checks in your own terminal, not by asking Claude.

## What to write

3–4 cases, each a synthetic dataset with planted answers. Cover:

1. **Confounding, in a different shape from penguins.** There, a categorical group reverses a pooled slope. Pick another mechanism or structure. The plan mentions "a group mix that changes over time"; you're free to pick something else, since Claude wrote that example.
2. **An effect whose direction is the finding**, in data where a model's importance ranking is the easy answer. The bar run missed directions when it reported only importances.
3. **An older trap in a new form:** leakage, pure noise, disguised missing values, outliers, a small sample or a non-linear effect. Use a mechanism different from the dev cases'. The dev case files (`evals/cases/`) and their tests (`tests/test_eval_cases.py`) show what's already covered.
4. *(Optional)* Anything you'd expect a careful analyst to catch and a hasty one to miss.

**Rules for a fair case:**
- **No famous datasets.** Generate the data yourself, so the model can't know the answers from training.
- **Neutral names.** The agent sees the file name and the column names: `pure_noise.csv` once gave an answer away. The file name should share no word with the case name. Use neutral case names too (e.g. `h1`…`h4`), since results files list them.
- **Effects strong enough to recover with a plain test at your seed**, and a trap that actually catches a naive analysis (e.g. the pooled slope really does have the wrong sign). Your tests check both.
- **Sizes like the dev cases:** 60–2,000 rows, 4–10 columns, one target (binary, numeric or a string label).

## Files

```
evals/heldout/
  generators.py        # GENERATORS = {"name": function(seed) -> DataFrame}
  cases/<name>.yaml    # one per case
  test_cases.py        # checks the expected answers against the data
```

**`generators.py`** follows [evals/generators.py](../../evals/generators.py): a seeded `numpy.random.default_rng(seed)`, a DataFrame out, values rounded to a few decimals. You may import helpers from it (`from evals.generators import _logistic`). Generator names must not clash with the dev ones.

**`cases/<name>.yaml`** follows [evals/cases/leakage.yaml](../../evals/cases/leakage.yaml):

| Field | What it is | Who reads it |
|---|---|---|
| `description` | The trap and the answers, for people | nobody else |
| `file` | Neutral CSV name, e.g. `orders.csv` | the agent (path) |
| `target` | Target column | the agent (`--target`) |
| `data` | `{generator: <name>, seed: <int>}` | the harness |
| `facts` | `{name, value, near: [keywords]}`: an exact value the report should state | deterministic grader: the value, rounded as written (or ×100 as a percentage), on a line with one of the keywords, case-insensitive |
| `must_find` | One checkable sentence per finding, with its direction (and rough size where it matters) | the judge (Sonnet 5.5): yes / partly / no |
| `must_not_claim` | The tempting wrong conclusion, stated as the report would put it | the judge: does the report say it? |
| `caveats` | `{name: [keywords]}`: a limitation the report should mention | the judge |

Each `must_find` item should be one claim. Write two items unless both halves are needed. 3–5 findings and 1–2 forbidden claims per case are enough.

**`test_cases.py`** works like [tests/test_eval_cases.py](../../tests/test_eval_cases.py). Call your generators directly, not `dataset()`, so no CSV is written to `evals/data/`. For each case, check that:
- every fact's `value` equals what you compute from the data;
- every planted effect is recoverable (a plain test, p well below 0.05), with the stated direction;
- the trap is real: the naive analysis gives the wrong answer;
- the case loads: `load_case("<name>")` from `evals.cases`, and `all_cases("heldout")` lists it.

Run them with `uv run pytest evals/heldout -q`. The main test suite doesn't collect them, so CI and Claude's test runs never print their names.

## When you're done

Commit to the cases with one hash. It covers every file and doesn't reveal any names:

```bash
tar --sort=name --mtime=@0 --owner=0 --group=0 --numeric-owner \
    --exclude=__pycache__ -cf - -C evals heldout | sha256sum | tee evals/heldout.sha256
```

Then tell Claude the hash file is in. It gets committed. From then on, don't change the cases. If you find a bug in one before P3.5, fix it, record a new hash, and note why in the commit.

## At P3.5

1. The Phase 3 agent is tagged. Nothing changes after this point.
2. You re-run the `tar … | sha256sum` line and check that it matches `evals/heldout.sha256`.
3. The cases go into git: remove the `evals/heldout/` line from `.gitignore`.
4. Two agents run on them, 3 repeats each:
   - the baseline (`--version baseline`);
   - the Phase 3 agent.

   Runs use `evals run --suite heldout`; then judge and report as usual. *About $1.90.* (The P3.2 agent, `71d5304`, was dropped on 2026-11-12 to stay within the $10 API budget.)
5. The held-out results are reported next to the dev ones. Changes made after seeing them are reported separately.
