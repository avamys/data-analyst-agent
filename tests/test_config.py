import pytest

from agent.config import PRESETS, Settings, settings
from agent.core.llm_manager import LLMManager
from agent.number_check import numbers_in


def make(**kwargs) -> Settings:
    return Settings(_env_file=None, **kwargs)  # a developer's .env must not leak in


def test_the_local_preset_is_the_defaults():
    s = make()
    assert s.preset == "local"
    assert (s.max_follow_ups, s.max_revisions) == (2, 1)


def test_a_preset_replaces_defaults():
    s = make(preset="hosted")
    assert s.max_follow_ups == PRESETS["hosted"]["max_follow_ups"]
    assert s.max_revisions == PRESETS["hosted"]["max_revisions"]


def test_explicit_values_beat_the_preset(monkeypatch):
    monkeypatch.setenv("MAX_FOLLOW_UPS", "4")
    s = make(preset="hosted", max_revisions=3)
    assert (s.max_follow_ups, s.max_revisions) == (4, 3)


def test_switching_preset_restores_defaults_but_keeps_explicit_values():
    s = make(preset="hosted", max_revisions=3)
    s.use_preset("local")
    assert (s.preset, s.max_follow_ups, s.max_revisions) == ("local", 2, 3)


def test_unknown_preset_is_rejected():
    with pytest.raises(ValueError):
        make(preset="fast")


def test_role_temperatures_are_read_when_used(monkeypatch):
    # They used to be read at import time, so overrides never reached them
    monkeypatch.setattr(settings, "ml_temperature", 0.7)
    assert LLMManager.resolve_config("ml")[1] == 0.7


def test_number_check_exemptions_come_from_settings(monkeypatch):
    assert [n for n, *_ in numbers_in("class 3 and 0.05")] == []
    monkeypatch.setattr(settings, "number_check_max_label", 2)
    monkeypatch.setattr(settings, "number_check_conventions", [])
    assert [n for n, *_ in numbers_in("class 3 and 0.05")] == ["3", "0.05"]
