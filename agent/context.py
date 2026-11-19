"""Context monitoring: prompts too long for the model, and what our caps cut

Ollama cuts a prompt that doesn't fit its context window without an error, so a
long prompt would silently lose its end (the P1.3 report was cut off this way).
Hosted providers reject such prompts instead, so only Ollama is checked. Without
the model's tokenizer the size is estimated from characters: qwen3.5 averaged
2.7-4.5 characters per token across 270 recorded calls.

The prompt caps in Settings (cell output, fact values, review script, planning
description) are counted when they cut something, so a run shows what its
agents didn't see. Both go into run_meta.json.
"""

import logging
from collections import Counter

from agent.config import settings

logger = logging.getLogger(__name__)

# Characters per token of qwen3.5 prompts: lowest and highest observed
MIN_CHARS_PER_TOKEN = 2.7
MAX_CHARS_PER_TOKEN = 4.5

# Per process, i.e. per run: read by run.py into run_meta.json
cuts: Counter[str] = Counter()
warnings: list[str] = []


class ContextOverflowError(RuntimeError):
    """The prompt can't fit the model's context window"""


def record_cut(where: str) -> None:
    """Count one cut made by a prompt cap"""
    cuts[where] += 1


def check_prompt(prompt: str, agent_type: str) -> None:
    """Stop on a prompt that can't fit the context; flag one that may not"""
    if settings.model_provider != "ollama":
        return
    budget = settings.llm_num_ctx - settings.llm_max_tokens  # the output needs room
    fewest = len(prompt) / MAX_CHARS_PER_TOKEN
    most = len(prompt) / MIN_CHARS_PER_TOKEN
    if fewest > budget:
        raise ContextOverflowError(
            f"{agent_type} prompt of {len(prompt):,} characters (at least "
            f"{fewest:,.0f} tokens) can't fit the {budget:,} tokens left for it in "
            f"llm_num_ctx={settings.llm_num_ctx:,}; Ollama would cut it silently. "
            "Raise LLM_NUM_CTX."
        )
    if most > budget:
        warning = (
            f"{agent_type} prompt of {len(prompt):,} characters (up to "
            f"{most:,.0f} tokens) may exceed the {budget:,} tokens left for it"
        )
        logger.warning(warning)
        warnings.append(warning)
