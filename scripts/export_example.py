"""Copy what a reader needs from a run directory into examples/<name>/

    uv run python scripts/export_example.py <run dir> examples/<name>

Kept: report.md, questions.md, run_meta.json (without local paths or trace
links), the page (report.html, rendered here: the run itself is not changed)
and, per task, its script, result.json (findings, facts, reviews) and charts,
at the same paths as in the run, so report.md's charts show on GitHub. Left
out: every LLM call, the state after each step, logs and the objects tasks
published.
"""

import argparse
import json
import shutil
from pathlib import Path

from agent.html_report import render_html

# Where it ran, not what it found; trace links lead to a private LangSmith workspace
LEFT_OUT = ("command", "dataset_path", "trace_url")


def export(run_dir: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    for name in ("report.md", "questions.md"):
        if (run_dir / name).exists():
            shutil.copy2(run_dir / name, dest / name)
    meta = json.loads((run_dir / "run_meta.json").read_text())
    meta = {k: v for k, v in meta.items() if k not in LEFT_OUT}
    meta.get("settings", {}).pop("runs_directory", None)
    for question in meta.get("questions", []):
        question.pop("trace_url", None)
    (dest / "run_meta.json").write_text(json.dumps(meta, indent=2))
    for result in sorted(run_dir.glob("tasks/*/result.json")):
        task, out = result.parent, dest / "tasks" / result.parent.name
        out.mkdir(parents=True)
        for name in ("analysis.py", "result.json"):
            if (task / name).exists():
                shutil.copy2(task / name, out / name)
        if (task / "charts").is_dir():
            shutil.copytree(task / "charts", out / "charts")
    (dest / "report.html").write_text(render_html(run_dir))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("dest", type=Path)
    args = parser.parse_args()
    export(args.run_dir, args.dest)
    print(args.dest)
