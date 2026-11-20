"""report.html: the run's report as one self-contained file

The report's Markdown rendered (raw HTML in it is escaped: the text comes from a
model), its charts embedded as base64, a header with the run's facts and
grades, the questions asked after the report with their answers
(questions.md), and an appendix with each task's status, open objection and
script, so a finding's numbers can be traced to the code that printed them.
Opens offline, anywhere, and prints.
"""

import base64
import html
import json
import mimetypes
import re
from pathlib import Path

from markdown_it import MarkdownIt

from agent.costs import run_model
from agent.run_grades import QUESTION_TASK, run_grades

MARKDOWN = MarkdownIt("commonmark", {"html": False}).enable("table")
IMAGE_SRC = re.compile(r'<img src="([^"]+)"')

CSS = """
:root { --fg: #1d1d1f; --muted: #6b6b70; --line: #d9d9de; --soft: #f4f4f6;
  --warn: #8a4b00; --warn-bg: #fff4e0; --bad: #a1131b; --bad-bg: #fdecec; }
@media (prefers-color-scheme: dark) {
  :root { --fg: #e8e8ea; --muted: #a0a0a8; --line: #3a3a40; --soft: #232327;
    --warn: #ffc069; --warn-bg: #3a2a10; --bad: #ff8a8a; --bad-bg: #3a1618; }
  body { background: #161618; } img { background: #fff; } }
body { color: var(--fg); font: 16px/1.55 system-ui, -apple-system, sans-serif;
  max-width: 52rem; margin: 2rem auto; padding: 0 1rem; }
h1 { font-size: 1.7rem; line-height: 1.25; } h2 { margin-top: 2.2rem; }
h1, h2, h3 { line-height: 1.25; }
img { max-width: 100%; height: auto; display: block; margin: 1rem 0; }
table { border-collapse: collapse; margin: 1rem 0; display: block;
  overflow-x: auto; font-size: 0.92rem; }
th, td { border: 1px solid var(--line); padding: 0.3rem 0.6rem; text-align: left; }
th { background: var(--soft); }
code { background: var(--soft); padding: 0.1rem 0.25rem; border-radius: 3px; }
pre { background: var(--soft); padding: 0.8rem; overflow-x: auto; font-size: 0.82rem; }
pre code { background: none; padding: 0; }
.run { border: 1px solid var(--line); border-radius: 6px; padding: 0.8rem 1rem;
  font-size: 0.92rem; color: var(--muted); }
.run dl { display: grid; grid-template-columns: max-content 1fr; gap: 0.2rem 1rem;
  margin: 0; }
.run dt { font-weight: 600; } .run dd { margin: 0; color: var(--fg); }
.note { border-radius: 6px; padding: 0.6rem 1rem; margin: 0.8rem 0; }
.warn { color: var(--warn); background: var(--warn-bg); }
.bad { color: var(--bad); background: var(--bad-bg); }
details { margin: 0.5rem 0 1rem; } summary { cursor: pointer; color: var(--muted); }
.task { border-top: 1px solid var(--line); padding-top: 0.6rem; }
@media print { details { display: none; } body { margin: 0; } }
"""


def render_html(run_dir: Path, with_questions: bool = True) -> str:
    """The page for a run directory, finished or failed. The app shows the
    questions apart from it (render_questions), below the report."""
    meta = _json(run_dir / "run_meta.json")
    grades = meta.get("grades") or run_grades(run_dir)  # older runs: no cost
    report_file = run_dir / "report.md"
    if report_file.exists():
        body = _embed_images(MARKDOWN.render(report_file.read_text()), run_dir)
    else:
        error = meta.get("error") or "the run stopped before writing its report"
        body = (
            f'<h1>No report</h1><p class="note bad">The run ended '
            f"<b>{html.escape(str(meta.get('status')))}</b>: {html.escape(error)}</p>"
        )
    title = re.search(r"<h1>(.*?)</h1>", body)
    title = re.sub(r"<[^>]+>", "", title[1]) if title else "Analysis report"
    questions = _questions(run_dir, meta) if with_questions else ""
    return _page(
        title,
        f"{_header(run_dir, meta, grades)}\n{body}\n{questions}\n"
        f"{_plan_review(meta)}\n{_appendix(run_dir)}",
    )


def _plan_review(meta: dict) -> str:
    """The conversation with the lead about the plan, before it ran"""
    if "plan_chat" not in meta:  # a run without plan approval
        return ""
    lines = [
        f"<p><b>{'You' if m['role'] == 'human' else 'Lead'}:</b> "
        f"{html.escape(m['text'])}</p>"
        for m in meta["plan_chat"]
    ]
    if not meta.get("plan_approved"):
        outcome = "The plan was never approved, so no task ran."
    elif lines:
        outcome = "The plan was approved after this conversation with the lead:"
    else:
        outcome = "The plan was approved as the lead first wrote it."
    return f"<h2>Plan review</h2><p>{outcome}</p>" + "".join(lines)


def render_questions(run_dir: Path) -> str | None:
    """The questions and answers alone, as a page; None when none was asked"""
    meta = _json(run_dir / "run_meta.json")
    body = _questions(run_dir, meta)
    return _page("Questions", body) if body else None


def _page(title: str, body: str) -> str:
    return (
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>{title}</title><style>{CSS}</style></head><body>\n"
        f"{body}\n</body></html>\n"
    )


def write_html(run_dir: Path) -> Path:
    path = run_dir / "report.html"
    path.write_text(render_html(run_dir))
    return path


def _embed_images(body: str, run_dir: Path) -> str:
    """Charts as data URIs; an image outside the run directory is dropped"""
    root = run_dir.resolve()

    def embed(m: re.Match) -> str:
        path = (run_dir / html.unescape(m[1])).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            return '<img src=""'
        data = base64.b64encode(path.read_bytes()).decode()
        kind = mimetypes.guess_type(path.name)[0] or "image/png"
        return f'<img src="data:{kind};base64,{data}"'

    return IMAGE_SRC.sub(embed, body)


def _header(run_dir: Path, meta: dict, grades: dict) -> str:
    profile = _json(run_dir / "state" / "01_profile.json").get("dataset_profile", {})
    calls = run_dir / "llm_calls.jsonl"
    model = run_model(calls) if calls.exists() else None
    minutes = f"{meta['seconds'] / 60:.1f}" if meta.get("seconds") else "?"
    cost = grades.get("cost_usd")
    rows = {
        "Dataset": f"{meta.get('dataset') or _dataset(run_dir, meta, model)}"
        + (f" ({profile['n_rows']:,} rows)" if profile.get("n_rows") else ""),
        "Target": profile.get("target_column") or "none",
        "Model": model or "?",
        "Run": f"{meta.get('started', '?').replace('T', ' ')}, {minutes} min"
        + (f", ${cost:.3f}" if cost is not None else ""),
        "Tasks": f"{grades.get('tasks_completed') or 0} done, "
        f"{grades.get('tasks_failed') or 0} failed; "
        f"{grades.get('revisions') or 0} sent back for revision",
    }
    if asked := meta.get("questions"):
        answered = sum(1 for q in asked if q.get("status") == "ok")
        costs = [(q.get("grades") or {}).get("cost_usd") for q in asked]
        rows["Questions"] = f"{answered} answered" + (
            f", {len(asked) - answered} not" if answered < len(asked) else ""
        )
        if None not in costs:
            rows["Questions"] += f", ${sum(costs):.3f}"
    dl = "".join(
        f"<dt>{name}</dt><dd>{html.escape(str(value))}</dd>"
        for name, value in rows.items()
    )
    notes = []
    if grades.get("tasks_failed"):
        notes.append(("bad", f"{grades['tasks_failed']} task(s) failed: see below."))
    if unverified := meta.get("unverified_numbers"):
        listed = ", ".join(str(n) for n in unverified)
        notes.append(
            (
                "warn",
                f"{len(unverified)} number(s) not traced to a recorded fact: {listed}. "
                "They are listed under Limitations.",
            )
        )
    if grades.get("unresolved_objections"):
        notes.append(
            (
                "warn",
                f"The lead's last review of {grades['unresolved_objections']} "
                "task(s) asked for changes that weren't made: see the tasks below.",
            )
        )
    shown = "".join(
        f'<p class="note {kind}">{html.escape(text)}</p>' for kind, text in notes
    )
    return f'<section class="run"><dl>{dl}</dl></section>{shown}'


def _dataset(run_dir: Path, meta: dict, model: str | None) -> str:
    """For runs older than meta["dataset"]: the CSV in the command, else the
    run directory's name, <YYYYmmdd-HHMMSS>_<dataset>_<model>"""
    csv = next((a for a in meta.get("command", []) if a.endswith(".csv")), None)
    if csv:
        return Path(csv).stem
    name = run_dir.name[16:]
    safe = re.sub(r"[^\w.-]", "-", model or "")
    return name.removesuffix(f"_{safe}") if safe else name


def _questions(run_dir: Path, meta: dict) -> str:
    """The answers (questions.md), and the questions that got none"""
    path = run_dir / "questions.md"
    body = (
        _embed_images(MARKDOWN.render(path.read_text()), run_dir)
        if path.exists()
        else ""
    )
    for q in meta.get("questions") or []:
        if q.get("status") not in ("ok", "running"):
            body += (
                f'<p class="note bad">Q{q["number"]}. {html.escape(q["question"])}: '
                f"no answer ({html.escape(q.get('error') or q['status'])})</p>"
            )
    return body


def _appendix(run_dir: Path) -> str:
    """Per task: status, revisions, the lead's open objection, its script"""
    tasks = []
    results = sorted(
        run_dir.glob("tasks/*/result.json"),  # a question's tasks after the run's
        key=lambda p: (bool(QUESTION_TASK.match(p.parent.name)), p.parent.name),
    )
    for path in results:
        r = _json(path)
        report = r.get("report") or {}
        status = report.get("status") or "failed"
        if not r.get("success", True):
            status = "failed"
        reviews = r.get("reviews") or []
        line = (
            f"<b>{html.escape(r['task_id'])}</b> ({html.escape(r['specialist'])}, "
            f"{status}, {r.get('revisions', 0)} revision(s)): "
            f"{html.escape(r.get('description', ''))}"
        )
        parts = [f"<p>{line}</p>"]
        if r.get("error"):
            parts.append(f'<p class="note bad">{html.escape(r["error"])}</p>')
        if reviews and reviews[-1]["verdict"] == "revise":
            parts.append(
                '<p class="note warn">Open objection: '
                f"{html.escape(reviews[-1].get('feedback') or '')}</p>"
            )
        script = path.parent / "analysis.py"
        code = script.read_text() if script.exists() else r.get("code", "")
        if code:
            parts.append(
                f"<details><summary>Script ({code.count(chr(10)) + 1} lines)"
                f"</summary><pre><code>{html.escape(code)}</code></pre></details>"
            )
        tasks.append(f'<div class="task">{"".join(parts)}</div>')
    if not tasks:
        return ""
    return (
        "<h2>Appendix: tasks and their code</h2>"
        "<p>The numbers in the report and the answers were checked against the "
        "facts these scripts recorded when they ran; any that matched none are "
        "listed under Limitations or at the end of the answer. Tasks named q1_, "
        "q2_… ran for a question.</p>" + "".join(tasks)
    )


def _json(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() else {}
