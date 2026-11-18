import json
import re

import pytest

from agent.cli import main
from agent.html_report import render_html, render_questions

# A 1×1 PNG
PIXEL = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
    "0000000d4944415478da63f8ffff3f0005fe02fea7d6a4b20000000049454e44ae426082"
)

REPORT = """# Survival report

| group | rate |
|---|---|
| women | 74.2% |

<script>alert(1)</script>

![Survival by sex](tasks/eda_1/charts/by_sex.png)
![Outside the run](../../secret.png)
"""


def _write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content if isinstance(content, str) else json.dumps(content))


@pytest.fixture
def run_dir(tmp_path):
    run = tmp_path / "runs" / "20261118-120000_small_claude-haiku-5-5"
    _write(
        run / "run_meta.json",
        {
            "status": "ok",
            "dataset": "small",
            "started": "2026-11-18T12:00:00",
            "seconds": 300,
            "unverified_numbers": ["1.1"],
            "grades": {"tasks_completed": 1, "tasks_failed": 1, "cost_usd": 0.0812},
        },
    )
    _write(run / "report.md", REPORT)
    _write(run / "tasks/eda_1/charts/by_sex.png", PIXEL)
    _write(tmp_path / "runs/secret.png", PIXEL)
    review = {"verdict": "revise", "feedback": "Add the CI."}
    _write(
        run / "tasks/eda_1/result.json",
        {
            "task_id": "eda_1",
            "specialist": "eda",
            "description": "How does survival vary by sex?",
            "success": True,
            "report": {"status": "complete"},
            "revisions": 1,
            "reviews": [review, review],
        },
    )
    _write(run / "tasks/eda_1/analysis.py", "record_fact('rate', 0.742, 'x')\n")
    _write(
        run / "tasks/ml_1/result.json",
        {
            "task_id": "ml_1",
            "specialist": "ml",
            "description": "Predict it",
            "success": False,
            "error": "Stopped: prompt can't fit",
            "report": None,
        },
    )
    return run


def test_the_page_is_self_contained(run_dir):
    page = render_html(run_dir)
    sources = re.findall(r'(?:src|href)="([^"]*)"', page)
    assert sources == [sources[0], ""]  # the chart, and the image outside the run
    assert sources[0].startswith("data:image/png;base64,")
    assert "<link" not in page and "<script" not in page  # model text is escaped
    assert "&lt;script&gt;" in page
    assert "<table>" in page and "<td>74.2%</td>" in page
    assert "<title>Survival report</title>" in page


def test_the_header_and_appendix_show_what_went_wrong(run_dir):
    page = render_html(run_dir)
    assert "small" in page and "5.0 min, $0.081" in page
    assert "1 task(s) failed" in page
    assert "1 number(s) not traced to a recorded fact: 1.1" in page
    assert "Open objection: Add the CI." in page
    assert "Stopped: prompt can&#x27;t fit" in page
    assert "record_fact(&#x27;rate&#x27;, 0.742" in page  # the script, escaped


def test_a_run_without_a_report_shows_its_failure(run_dir):
    (run_dir / "report.md").unlink()
    meta = json.loads((run_dir / "run_meta.json").read_text())
    meta.update(status="failed", error="ContextOverflowError('too long')")
    (run_dir / "run_meta.json").write_text(json.dumps(meta))
    page = render_html(run_dir)
    assert "<h1>No report</h1>" in page
    assert "ContextOverflowError" in page


def test_analyst_report_writes_the_page(run_dir, capsys):
    assert main(["report", str(run_dir)]) == 0
    assert capsys.readouterr().out.strip() == str(run_dir / "report.html")
    assert (run_dir / "report.html").read_text().startswith("<!doctype html>")


def test_questions_show_on_the_page_and_alone(run_dir):
    assert render_questions(run_dir) is None
    (run_dir / "questions.md").write_text(
        "## Questions after the report\n\n### Q1. Why?\n\n"
        "![By sex](tasks/eda_1/charts/by_sex.png)\n"
    )
    page = render_html(run_dir)
    assert page.index("<h3>Q1. Why?</h3>") < page.index("Appendix")
    assert "Q1. Why?" not in render_html(run_dir, with_questions=False)
    alone = render_questions(run_dir)
    assert "<h3>Q1. Why?</h3>" in alone and "data:image/png;base64," in alone
