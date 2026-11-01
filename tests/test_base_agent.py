import pytest
from langchain_core.exceptions import OutputParserException
from langchain_core.runnables import RunnableLambda
from ollama import ResponseError

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
