import pytest
from conftest import ScriptedLLM
from test_lead import _brief, _plan, accept
from test_specialist import finish, run_cell

from agent.core.llm_manager import LLMManager
from agent.graph import build_hierarchical_graph
from agent.nodes.report import add_to_limitations

# small_df has 40 rows; the task records that, a fact named after its group,
# and one stale fact it doesn't cite
TASK = [
    run_cell(
        "record_fact('rows', len(df), 'Rows')\n"
        "record_fact('rate_(7.91, 14.454]', 0.3, 'Rate in a fare band')\n"
        "record_fact('stale', 123.4, 'From a failed attempt')\n"
        "fig, ax = plt.subplots(); ax.plot([0, 1])\n"
        "save_chart(fig, 'trend', 'A trend')"
    ),
    finish("rows", "rate_(7.91, 14.454]"),
    accept(),
]
CHART = "![A trend](tasks/eda_1/charts/trend.png)"


@pytest.fixture
def write(monkeypatch, tmp_path, small_csv):
    """Run the graph with one task; `drafts` are the writer's replies"""

    def _write(*drafts):
        llm = ScriptedLLM([_plan(_brief("eda_1")), *TASK, *drafts])
        monkeypatch.setattr(LLMManager, "get_llm", lambda **_: llm)
        state = build_hierarchical_graph().invoke(
            {"dataset_info": "", "dataset_path": small_csv, "run_dir": str(tmp_path)},
            config={"recursion_limit": 100},
        )
        return state, llm.prompts[4:]  # the writer's prompts

    return _write


def test_writer_sees_cited_facts_and_charts_only(write):
    state, [prompt] = write(f"# Report\n\nThe data has 40 rows.\n\n{CHART}")
    assert "eda_1.rows = 40" in prompt
    assert "stale" not in prompt
    assert CHART in prompt
    assert state["report"].endswith(CHART)  # the image exists, so it stays
    assert state["unverified_numbers"] == []


def test_numbers_in_cited_fact_names_count(write):
    state, prompts = write("Fares from 7.91 to 14.45 survive at 30%.")
    assert len(prompts) == 1
    assert state["unverified_numbers"] == []


def test_a_number_matching_no_fact_goes_back_once(write):
    state, [first, second] = write(
        "## Findings\n\nThe data has 41 rows.", "## Findings\n\nThe data has 40 rows."
    )
    assert "YOUR DRAFT" not in first
    assert '41 in: "The data has 41 rows."' in second
    assert state["report"] == "## Findings\n\nThe data has 40 rows."


def test_numbers_still_unmatched_are_listed_under_limitations(write):
    draft = "## Findings\n\nThe data has 41 rows.\n\n## Limitations\n\nFew.\n\n## Open questions\n\nNone."
    state, prompts = write(draft, draft)
    assert len(prompts) == 2
    assert state["unverified_numbers"] == ["41"]
    limitations = state["report"].split("## Limitations")[1].split("## Open")[0]
    assert '- 41 in: "The data has 41 rows."' in limitations


def test_images_whose_file_is_missing_are_removed(write):
    state, _ = write(f"See:\n{CHART}\n![Made up](tasks/eda_1/charts/nope.png)\nEnd.")
    assert state["report"] == f"See:\n{CHART}\nEnd."


def test_limitations_section_is_added_when_missing():
    report = add_to_limitations("## Findings\n\nx", [("41", "line")])
    assert report.endswith(
        '## Limitations\n\n**Numbers not traced to a recorded fact.** The automatic check found no recorded value for these numbers:\n- 41 in: "line"'
    )
