"""Smoke tests: the package imports, prompts render and the graph compiles without an LLM"""

from agent.core.template_manager import prompt_templates
from agent.data_loader import generate_dataset_info, load_dataset
from agent.graph import build_hierarchical_graph
from agent.profiling import auto_profile_dataset


def test_graph_compiles():
    graph = build_hierarchical_graph()
    assert {
        "profile",
        "plan",
        "run_task",
        "review",
        "synthesizer",
        "reporter",
    } <= set(graph.get_graph().nodes)


def test_all_templates_parse():
    templates = prompt_templates.list_templates()
    assert templates
    for name in templates:
        prompt_templates.env.get_template(name)  # raises TemplateSyntaxError


def test_dataset_info_and_profile(small_csv):
    df = load_dataset(small_csv)
    info = generate_dataset_info(df, small_csv)
    assert "Columns: age, fare, sex, port, target" in info

    profile = auto_profile_dataset(df, small_csv)
    assert (profile.n_rows, profile.n_cols) == (40, 5)
    assert profile.target_column == "target"
    assert profile.target_type == "binary"
    assert profile.missing_percentages == {"age": 12.5}


def test_templates_contain_no_dataset_specific_text():
    # The baseline copied dataset-specific examples into every analysis
    words = ["titanic", "survived", "survival", "pclass", "sibsp", "parch", "embarked"]
    for name in prompt_templates.list_templates():
        source = prompt_templates.env.loader.get_source(prompt_templates.env, name)[0]
        found = [w for w in words if w in source.lower()]
        assert not found, f"{name} mentions {found}"
