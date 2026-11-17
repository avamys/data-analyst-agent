import json

from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict

from agent.run_store import LLMCallRecorder, RunStore
from agent.states import TaskResult


def test_recorder_captures_calls_made_inside_graph_nodes(tmp_path):
    # Nodes call llm.invoke() without passing config, like the agents do;
    # the recorder must still see those calls through the graph's callbacks
    llm = GenericFakeChatModel(messages=iter([AIMessage(content="hello back")]))

    class State(TypedDict):
        answer: str

    def ask(state):
        return {"answer": llm.invoke([HumanMessage(content="hello")]).content}

    graph = StateGraph(State)
    graph.add_node("ask", ask)
    graph.add_edge(START, "ask")
    graph.add_edge("ask", END)

    recorder = LLMCallRecorder(tmp_path / "llm_calls.jsonl")
    graph.compile().invoke({"answer": ""}, config={"callbacks": [recorder]})

    [record] = [json.loads(line) for line in (tmp_path / "llm_calls.jsonl").open()]
    assert record["node"] == "ask"
    assert record["prompt"] == [{"role": "human", "content": "hello"}]
    assert record["response"] == "hello back"
    assert recorder.calls == 1


def test_recorder_logs_tool_calls_and_reasoning_tokens(tmp_path):
    # Structured output over function calling (OpenRouter) has no text content
    call = {"name": "Review", "args": {"verdict": "accept"}, "id": "c1"}
    llm = GenericFakeChatModel(
        messages=iter(
            [
                AIMessage(
                    content="",
                    tool_calls=[call],
                    usage_metadata={
                        "input_tokens": 10,
                        "output_tokens": 30,
                        "total_tokens": 40,
                        "output_token_details": {"reasoning": 25},
                    },
                )
            ]
        )
    )
    recorder = LLMCallRecorder(tmp_path / "llm_calls.jsonl")
    llm.invoke([HumanMessage(content="review")], config={"callbacks": [recorder]})

    [record] = [json.loads(line) for line in (tmp_path / "llm_calls.jsonl").open()]
    assert record["response"][0]["args"] == {"verdict": "accept"}
    assert record["reasoning_tokens"] == 25


def test_write_tasks_writes_every_attempt(tmp_path):
    store = RunStore(tmp_path, "titanic", "qwen3.5:9b")
    assert store.path.name.endswith("_titanic_qwen3.5-9b")

    result = TaskResult(
        task_id="eda_1",
        specialist="eda",
        description="d",
        attempts=[
            {"attempt": 1, "code": "boom()", "output": "NameError('boom')"},
            {"attempt": 2, "code": "print(1)", "output": "1\n"},
        ],
    )
    store.write_tasks([result])

    task_dir = store.path / "tasks" / "eda_1"
    assert (task_dir / "attempt_1.py").read_text() == "boom()"
    assert (task_dir / "attempt_2_output.txt").read_text() == "1\n"
    assert json.loads((task_dir / "result.json").read_text())["task_id"] == "eda_1"


def test_eval_metadata_comes_from_the_runners_environment(monkeypatch):
    from agent.tracing import eval_metadata

    for var in ("EVAL_CASE", "EVAL_REPEAT", "EVAL_VERSION"):
        monkeypatch.delenv(var, raising=False)
    assert eval_metadata() == {}
    monkeypatch.setenv("EVAL_CASE", "leakage")
    monkeypatch.setenv("EVAL_REPEAT", "3")
    assert eval_metadata() == {"case": "leakage", "repeat": "3"}


def _record_one(tmp_path, message):
    llm = GenericFakeChatModel(messages=iter([message]))
    recorder = LLMCallRecorder(tmp_path / "llm_calls.jsonl")
    llm.invoke([HumanMessage(content="hi")], config={"callbacks": [recorder]})
    [record] = [json.loads(line) for line in (tmp_path / "llm_calls.jsonl").open()]
    return recorder, record


def test_recorder_splits_an_ollama_call_into_load_prompt_and_generation(tmp_path):
    # As ChatOllama returns them: nanoseconds, and "length" at num_predict
    meta = {
        "done_reason": "length",
        "load_duration": 2_000_000_000,
        "prompt_eval_count": 3000,
        "prompt_eval_duration": 10_000_000_000,
        "eval_count": 120,
        "eval_duration": 12_000_000_000,
    }
    usage = {"input_tokens": 3000, "output_tokens": 120, "total_tokens": 3120}
    recorder, record = _record_one(
        tmp_path,
        AIMessage(content="cut", response_metadata=meta, usage_metadata=usage),
    )
    assert record["stop_reason"] == "length"
    assert (record["load_seconds"], record["prompt_seconds"]) == (2.0, 10.0)
    assert record["generation_seconds"] == 12.0
    assert (record["prompt_tok_s"], record["generation_tok_s"]) == (300.0, 10.0)
    assert recorder.cut_off == 1 and recorder.empty == 0
    assert recorder.ollama == {
        "load_seconds": 2.0,
        "prompt_seconds": 10.0,
        "generation_seconds": 12.0,
        "generation_tokens": 120,
    }


def test_recorder_counts_an_anthropic_reply_with_only_thinking_as_cut_off_and_empty(
    tmp_path,
):
    # The P3.5 failure: the writer spent its whole cap thinking
    message = AIMessage(
        content=[{"type": "thinking", "thinking": "...", "signature": "s"}],
        response_metadata={"stop_reason": "max_tokens"},
    )
    recorder, record = _record_one(tmp_path, message)
    assert record["stop_reason"] == "max_tokens" and record["empty"] is True
    assert "load_seconds" not in record
    assert (recorder.cut_off, recorder.empty, recorder.ollama) == (1, 1, {})


def test_recorder_leaves_out_what_the_provider_does_not_return(tmp_path):
    recorder, record = _record_one(tmp_path, AIMessage(content="fine"))
    assert "stop_reason" not in record and "empty" not in record
    assert (recorder.cut_off, recorder.empty) == (0, 0)


def test_ollama_snapshot_gives_the_share_of_each_model_on_the_gpu(monkeypatch):
    from agent import run_store

    class Response:
        def json(self):
            return {
                "models": [
                    {
                        "name": "qwen3.5:9b",
                        "size": 6_000_000_000,
                        "size_vram": 1_500_000_000,
                        "context_length": 16384,
                    }
                ]
            }

    monkeypatch.setattr(run_store.httpx, "get", lambda *a, **k: Response())
    assert run_store.ollama_snapshot("http://ollama") == [
        {
            "model": "qwen3.5:9b",
            "size_gb": 6.0,
            "vram_gb": 1.5,
            "on_gpu": 0.25,
            "context_length": 16384,
        }
    ]

    def unreachable(*a, **k):
        raise run_store.httpx.ConnectError("refused")

    monkeypatch.setattr(run_store.httpx, "get", unreachable)
    assert run_store.ollama_snapshot("http://ollama") is None
