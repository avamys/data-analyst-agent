from langchain_core.runnables import RunnableLambda
from ollama import ResponseError

from agent.core.base_agent import BaseAgent
from agent.core.llm_manager import LLMManager


def test_retries_once_when_the_model_runner_crashes(monkeypatch):
    # Ollama answers 500 when its runner crashes and restarts it on the next call
    calls = []

    def flaky(messages):
        calls.append(messages)
        if len(calls) == 1:
            raise ResponseError("model runner has unexpectedly stopped", 500)
        return "ok"

    monkeypatch.setattr(LLMManager, "get_llm", lambda **_: RunnableLambda(flaky))
    assert BaseAgent(agent_type="reporter").invoke("hi") == "ok"
    assert len(calls) == 2
