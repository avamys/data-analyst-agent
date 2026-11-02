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
