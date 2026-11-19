import pytest

from agent import context
from agent.config import settings
from agent.context import ContextOverflowError, check_prompt
from agent.core.specialists import format_facts


@pytest.fixture(autouse=True)
def fresh_counts(monkeypatch):
    monkeypatch.setattr(context, "cuts", context.Counter())
    monkeypatch.setattr(context, "warnings", [])


@pytest.fixture
def ollama(monkeypatch):
    # 1,000 tokens left for the prompt
    monkeypatch.setattr(settings, "model_provider", "ollama")
    monkeypatch.setattr(settings, "llm_num_ctx", 1500)
    monkeypatch.setattr(settings, "llm_max_tokens", 500)


def test_a_prompt_that_cant_fit_stops_the_call(ollama):
    with pytest.raises(ContextOverflowError, match="LLM_NUM_CTX"):
        check_prompt("x" * 5000, "reporter")  # at least 1,111 tokens


def test_a_prompt_that_may_not_fit_is_flagged(ollama):
    check_prompt("x" * 2000, "reporter")  # 444 to 741 tokens: fits
    assert context.warnings == []
    check_prompt("x" * 4000, "reporter")  # 889 to 1,481 tokens: may not fit
    assert len(context.warnings) == 1


def test_hosted_providers_are_not_checked(ollama, monkeypatch):
    # They reject oversized prompts with an error instead of cutting them
    monkeypatch.setattr(settings, "model_provider", "anthropic")
    check_prompt("x" * 100_000, "reporter")
    assert context.warnings == []


def test_prompt_caps_count_their_cuts():
    facts = {
        "long": {"value": "x" * 500, "desc": "d"},
        "short": {"value": 1, "desc": "d"},
    }
    format_facts(facts)
    assert context.cuts == {"fact value": 1}
