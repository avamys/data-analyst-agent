# Local vs hosted: qwen3.5:9b next to Claude Haiku 5.5 (P6.3)

One run of the agent on a local model, on the `titanic` eval case, next to Claude Haiku 5.5's six titanic runs from Phase 3. All runs use the default `local` preset (1 revision, 2 follow-ups). Findings, false claims and caveats are scored by the LLM judge (Claude Sonnet 5.5, rubric `983aca5d02a5`, [calibrated](calibration/README.md)); the rest by the deterministic graders.

- **Local:** qwen3.5:9b through Ollama, 32k context, on a laptop GPU with 4 GB. The model takes 7.4 GB, so 3.8 GB (52%) runs on the GPU and the rest on the CPU. Agent code `2728719`, one run. [Results](../../evals/results/20261119-125318_current_qwen3.5-9b.jsonl).
- **Hosted:** Claude Haiku 5.5. P3.5 dev suite (`v0.3.0-phase3`, [results](../../evals/results/20261113-181103_current_claude-haiku-5-5.jsonl)) and the `v0.3.1` dev check ([results](../../evals/results/20261117-171234_current_claude-haiku-5-5.jsonl)), 3 titanic runs each.

## Summary

| | qwen3.5:9b, local (1 run) | Haiku, P3.5 (3 runs) | Haiku, `v0.3.1` (3 runs) |
|---|---|---|---|
| Finished | yes | 3 of 3 | 3 of 3 |
| **Findings** | **79%** (5 of 7, 1 half) | 100% | 100% |
| False claims | 0 | 0 | 0 |
| Caveats | 50% | 100% | 100% |
| Tasks done | 8 (2 follow-ups) | 7 | 7 |
| Revisions | 7 | 5–6 | 5–6 |
| Unresolved review objections | 5 | 1–3 | 1–2 |
| Numbers not traced to a fact | 9 (4 of them wrong) | 0–4 | 0–5 |
| LLM calls | 99 | | 48–54 |
| Tokens in / out | 410k / 82k | | 371–446k / 96–102k |
| **Minutes** | **199** | 8–10 | 7–9 |
| Cost | $0 (the judge: $0.02) | $0.08–0.11 | $0.09–0.10 |

- **It finishes and makes no false claim, but finds less.** The report has the class gradient, higher fares among survivors, lower survival with a missing cabin or age, and models beating the majority class. It misses precision, recall or F1 (accuracy only), and gives survival by sex only within each class, never the overall 74% vs 19% (`partly`). It discusses the missing cabins without treating them as a limitation (`partly`).
- **The number check matters more locally.** Haiku mostly follows the rule to write only recorded numbers. qwen wrote 9 numbers that match no fact, and the check listed all 9 under Limitations. Checked against the data:
  - 5 are right: the χ² and Cramér's V for class, sex and port, which the code printed but didn't record, and one difference between two facts.
  - 4 are wrong:
    - survival of third-class women, 50.4% (actual 50.0%);
    - survival of third-class men, 13.6% (actual 13.5%);
    - the mean fare of women who died, $16.28 (actual $23.02);
    - a difference computed from that fare, $25.66 (actual $28.92).

  The judge doesn't count these as false claims: its rubric covers the case's traps, not every number. Without the check, nothing in the report would mark them.
- **More of the work is left open.** 5 objections were still open when revisions ran out, against 1–3 for Haiku. The report's Limitations also mention implementation detail the reader can't use ("the recorded dictionary keys included non-existent values").
- **It takes 25× as long.** Haiku makes half as many calls with about the same tokens in total.

## Where the time went

From the run's timings (P4.1): 199 minutes in total.

| Step | Minutes | Share |
|---|---|---|
| Plan | 2.7 | 1% |
| Tasks (8 tasks, 7 revisions) | 157.4 | 79% |
| Reviews | 24.8 | 12% |
| Report | 13.7 | 7% |

The Ollama timings for the same run:
- **Generating tokens: 185 of 199 minutes (93%)**, at 7.4 tokens a second.
- Reading prompts: 6.3 minutes (3%), at about 1,080 tokens a second.
- Loading the model: 25 seconds.

The model writes about as much as Haiku does (82k tokens), so the time is the speed of generation. With half the model on the CPU, a larger GPU is what would change it, not the prompts.

## The earlier attempt

The first local run (P4.2, 2026-11-17, 16k context) failed after 126 minutes, with 2 tasks done. A statistics prompt of about 13,200 tokens didn't fit the 12,288 left for it. The agent stopped with `ContextOverflowError` rather than let Ollama cut the prompt silently. A replay picked the 32k context used here, with the same speed. This run hit no context limit: its largest prompt was 13,738 tokens, and no call was cut off or came back empty.

## What this shows, and what it doesn't

- On this hardware, the agent runs end to end on a 9B local model with nothing leaving the machine. It finds most of what Haiku finds and makes none of the false claims the case tests for, in about 3 hours instead of 9 minutes.
- The local model's weaknesses are in what the checks catch: numbers not recorded, objections left open. The check outside the model did its job: every wrong number in the report is flagged in it.
- One run on one case. It gives no spread, and titanic is a dataset both models likely know. Local runs are an option for data that can't leave the machine; the agent was developed and measured on Claude.
