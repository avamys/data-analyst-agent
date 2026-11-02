from typing import Literal

import pytest
from langchain_core.exceptions import OutputParserException
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda
from ollama import ResponseError
from pydantic import BaseModel

from agent.config import settings
from agent.core.base_agent import BaseAgent
from agent.core.llm_manager import LLMManager


@pytest.mark.parametrize(
    "error",
    [
        # Ollama answers 500 when its runner crashes and restarts it on the next call
        ResponseError("model runner has unexpectedly stopped", 500),
        # A malformed structured response is worth one more try
        OutputParserException("Invalid json output"),
    ],
)
def test_retries_once_on_transient_failures(monkeypatch, error):
    calls = []

    def flaky(messages):
        calls.append(messages)
        if len(calls) == 1:
            raise error
        return "ok"

    monkeypatch.setattr(LLMManager, "get_llm", lambda **_: RunnableLambda(flaky))
    assert BaseAgent(agent_type="reporter").invoke("hi") == "ok"
    assert len(calls) == 2


@pytest.mark.parametrize(
    ("provider", "method"),
    # OpenRouter's free models reject response_format, so they get a tool instead
    [("ollama", "json_schema"), ("openrouter", "function_calling")],
)
def test_structured_output_method_follows_provider(monkeypatch, provider, method):
    seen = {}

    class SpyLLM:
        def with_structured_output(self, schema, **kwargs):
            seen.update(kwargs)
            return RunnableLambda(lambda _: None)

    monkeypatch.setattr(settings, "model_provider", provider)
    monkeypatch.setattr(LLMManager, "get_llm", lambda **_: SpyLLM())
    BaseAgent(agent_type="lead", use_structured_output=True, output_schema=dict)
    assert seen == {"method": method, "include_raw": False}


def test_anthropic_uses_json_outputs(monkeypatch):
    # Forced tool calls let Haiku drop required fields; JSON outputs can't
    class Verdict(BaseModel):
        verdict: Literal["accept", "revise"]

    reply = AIMessage(
        content=[
            {"type": "thinking", "thinking": "", "signature": "s"},
            {"type": "text", "text": '{"verdict": "accept"}'},
        ]
    )
    monkeypatch.setattr(settings, "model_provider", "anthropic")
    chain = LLMManager.with_structured_output(
        GenericFakeChatModel(messages=iter([reply])), Verdict
    )
    fmt = chain.first.kwargs["output_config"]["format"]
    assert fmt["schema"]["additionalProperties"] is False
    assert fmt["schema"]["required"] == ["verdict"]
    assert chain.invoke("review") == Verdict(verdict="accept")
