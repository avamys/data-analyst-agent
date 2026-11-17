import json

from scripts.run_cost import estimate_cost, openrouter_id, run_model, summarize_calls


def write_calls(path, calls):
    path.write_text("".join(json.dumps(c) + "\n" for c in calls))
    return path


def test_totals_per_node_and_overall(tmp_path):
    log = write_calls(
        tmp_path / "llm_calls.jsonl",
        [
            {
                "node": "plan",
                "model": "m",
                "input_tokens": 100,
                "output_tokens": 50,
                "reasoning_tokens": 20,
                "seconds": 2.0,
            },
            {
                "node": "run_task",
                "model": "m",
                "input_tokens": 300,
                "output_tokens": 70,
                "seconds": 3.0,
            },
            {
                "node": "run_task",
                "model": "m",
                "input_tokens": 400,
                "output_tokens": 80,
                "seconds": 4.0,
            },
            # A failed call has no token counts
            {"node": "review", "model": "m", "error": "boom", "seconds": 1.0},
        ],
    )
    nodes = summarize_calls(log)
    assert list(nodes) == ["plan", "run_task", "review", "total"]
    tokens = ("calls", "input", "output", "reasoning", "seconds")
    assert {k: nodes["run_task"][k] for k in tokens} == {
        "calls": 2,
        "input": 700,
        "output": 150,
        "reasoning": 0,
        "seconds": 7.0,
    }
    assert {k: nodes["total"][k] for k in tokens} == {
        "calls": 4,
        "input": 800,
        "output": 200,
        "reasoning": 20,
        "seconds": 10.0,
    }
    assert run_model(log) == "m"


def test_ollama_time_split_and_cut_off_calls_per_node(tmp_path):
    log = write_calls(
        tmp_path / "llm_calls.jsonl",
        [
            {
                "node": "report",
                "stop_reason": "length",
                "load_seconds": 20.0,
                "prompt_seconds": 300.0,
                "generation_seconds": 600.0,
            },
            {"node": "report", "stop_reason": "stop", "generation_seconds": 50.0},
            {"node": "plan", "stop_reason": "max_tokens", "empty": True},
        ],
    )
    nodes = summarize_calls(log)
    assert nodes["report"]["load_seconds"] == 20.0
    assert nodes["report"]["prompt_seconds"] == 300.0
    assert nodes["report"]["generation_seconds"] == 650.0
    assert (nodes["report"]["cut_off"], nodes["report"]["empty"]) == (1, 0)
    assert (nodes["total"]["cut_off"], nodes["total"]["empty"]) == (2, 1)


def test_cost_uses_per_token_prices():
    total = {"input": 1_000_000, "output": 200_000}
    # OpenRouter prices are strings, USD per token
    price = {"prompt": "0.0000006", "completion": "0.0000024"}
    assert estimate_cost(total, price) == 0.6 + 0.48


def test_anthropic_ids_map_to_openrouter_names():
    assert openrouter_id("claude-haiku-5-5") == "anthropic/claude-haiku-5.5"
    assert openrouter_id("claude-opus-5") == "anthropic/claude-opus-5"
    assert openrouter_id("qwen/qwen3.5-9b") == "qwen/qwen3.5-9b"
