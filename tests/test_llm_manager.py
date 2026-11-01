import pytest

from agent.config import settings
from agent.core.llm_manager import LLMManager


@pytest.mark.parametrize(
    ("agent_type", "temperature"),
    [("eda", 0.3), ("statistical", 0.2), ("ml", 0.1)],
)
def test_specialists_get_their_own_config(agent_type, temperature):
    # B1: specialist agent types used to miss their config and fall back to defaults
    assert LLMManager.resolve_config(agent_type) == (settings.coder_model, temperature)


def test_overrides_win():
    assert LLMManager.resolve_config("lead", model_name="m", temperature=0.9) == (
        "m",
        0.9,
    )


def test_unknown_agent_type_raises():
    with pytest.raises(ValueError, match="Unknown agent type"):
        LLMManager.resolve_config("eda_specialist")
