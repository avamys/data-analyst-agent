import pytest
from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import RunnableSequence
from pydantic import SecretStr

from agent.config import settings
from agent.core.base_agent import BaseAgent
from agent.core.llm_manager import LLMManager
from agent.states import Review, SpecialistStep


@pytest.mark.parametrize(
    ("agent_type", "temperature"),
    [("eda", 0.3), ("statistical", 0.2), ("ml", 0.1)],
)
def test_specialists_get_their_own_config(agent_type, temperature):
    # B1: specialist agent types used to miss their config and fall back to defaults
    assert LLMManager.resolve_config(agent_type) == (settings.model, temperature)


def test_overrides_win():
    assert LLMManager.resolve_config("lead", model_name="m", temperature=0.9) == (
        "m",
        0.9,
    )


def test_unknown_agent_type_raises():
    with pytest.raises(ValueError, match="Unknown agent type"):
        LLMManager.resolve_config("eda_specialist")


@pytest.fixture
def openrouter(monkeypatch):
    monkeypatch.setattr(settings, "model_provider", "openrouter")
    monkeypatch.setattr(settings, "openrouter_api_key", SecretStr("sk-test"))
    monkeypatch.setattr(settings, "openrouter_model", "vendor/model:free")


def test_switching_provider_switches_model(monkeypatch, openrouter):
    monkeypatch.setattr(settings, "ollama_model", "local:9b")
    assert LLMManager.resolve_config("lead")[0] == "vendor/model:free"
    monkeypatch.setattr(settings, "model_provider", "ollama")
    assert LLMManager.resolve_config("lead")[0] == "local:9b"


def test_role_override_beats_provider_model(monkeypatch, openrouter):
    monkeypatch.setattr(settings, "coder_model", "vendor/coder")
    assert LLMManager.resolve_config("ml")[0] == "vendor/coder"
    assert LLMManager.resolve_config("lead")[0] == "vendor/model:free"


def test_openrouter_uses_openai_api_with_reasoning(openrouter):
    kwargs = LLMManager._provider_kwargs()
    assert kwargs["model_provider"] == "openai"
    assert kwargs["base_url"] == "https://openrouter.ai/api/v1"
    assert kwargs["extra_body"] == {"reasoning": {"enabled": True}}
    assert "num_ctx" not in kwargs  # Ollama-only options stay out


def test_openrouter_without_key_fails_early(monkeypatch, openrouter):
    monkeypatch.setattr(settings, "openrouter_api_key", None)
    with pytest.raises(ValueError, match="OPENROUTER_API_KEY"):
        LLMManager._provider_kwargs()


def test_openrouter_llm_builds_without_network(openrouter):
    LLMManager.clear_cache()
    llm = LLMManager.get_llm("lead")
    assert llm.model_name == "vendor/model:free"
    assert llm.openai_api_base == "https://openrouter.ai/api/v1"
    LLMManager.clear_cache()


def test_anthropic_sends_no_temperature(monkeypatch):
    # Current Claude models reject sampling parameters with a 400
    monkeypatch.setattr(settings, "model_provider", "anthropic")
    monkeypatch.setattr(settings, "anthropic_api_key", SecretStr("sk-ant-test"))
    assert LLMManager.resolve_config("ml")[0] == "claude-haiku-5-5"
    LLMManager.clear_cache()
    llm = LLMManager.get_llm("ml")
    assert llm.temperature is None
    assert "temperature" not in llm._get_request_payload("hi")
    LLMManager.clear_cache()


def test_anthropic_without_key_fails_early(monkeypatch):
    monkeypatch.setattr(settings, "model_provider", "anthropic")
    monkeypatch.setattr(settings, "anthropic_api_key", None)
    with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
        LLMManager._provider_kwargs()


def _payload(agent) -> dict:
    """The request an agent would send, with the kwargs bound anywhere in its chain"""
    runnable, kwargs = agent.llm, {}
    while not isinstance(runnable, BaseChatModel):
        if isinstance(runnable, RunnableSequence):  # model | parser
            runnable = runnable.first
        else:  # bindings, the retry wrapper
            kwargs |= runnable.kwargs
            runnable = runnable.bound
    return runnable._get_request_payload("hi", **kwargs)


def test_anthropic_effort_is_set_per_role(monkeypatch):
    monkeypatch.setattr(settings, "model_provider", "anthropic")
    monkeypatch.setattr(settings, "anthropic_api_key", SecretStr("sk-ant-test"))
    monkeypatch.setattr(settings, "specialist_effort", "low")
    monkeypatch.setattr(settings, "lead_effort", "high")
    LLMManager.clear_cache()
    step = BaseAgent("eda", use_structured_output=True, output_schema=SpecialistStep)
    assert _payload(step)["output_config"]["effort"] == "low"
    assert _payload(step)["output_config"]["format"]["type"] == "json_schema"
    review = BaseAgent("lead", use_structured_output=True, output_schema=Review)
    assert _payload(review)["output_config"]["effort"] == "high"
    assert _payload(BaseAgent("reporter"))["output_config"] == {"effort": "high"}
    monkeypatch.setattr(settings, "lead_effort", None)  # the model's default
    assert "output_config" not in _payload(BaseAgent("reporter"))
    LLMManager.clear_cache()
