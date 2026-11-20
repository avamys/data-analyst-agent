"""Streamlit app: upload a CSV, watch the analysis, read its report, ask about it.

    uv run --group ui streamlit run app/streamlit_app.py

Each analysis runs as its own process (`analyst run`), so a crash can't take
the page down and per-run counters stay per run (agent/context.py); the page
only reads the files the run writes. Past runs open the same way. A question
about a finished run runs as `analyst ask`, recorded in that run. With plan
review on, the run waits after its plan; the page writes the human's replies to
the run's stdin.
"""

import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from agent.config import settings
from agent.html_report import render_html, render_questions
from app.runs import (
    list_runs,
    plan_chat,
    read_events,
    stage,
    task_rows,
    waiting_plan,
)

ROOT = Path(__file__).resolve().parent.parent
PROVIDERS = {
    "anthropic": "anthropic_model",
    "openrouter": "openrouter_model",
    "ollama": "ollama_model",
}
STATE_ICONS = {
    "waiting": "·",
    "running": "▶",
    "revising": "↻",
    "in review": "…",
    "sent back": "↺",
    "accepted": "✓",
    "failed": "✗",
}


def main():
    st.set_page_config(page_title="Data analyst agent", layout="wide")
    runs_root = Path(
        st.sidebar.text_input("Runs folder", settings.runs_directory)
    ).expanduser()
    page = st.sidebar.radio("Page", ["New analysis", "Past runs"])
    if page == "New analysis":
        new_analysis(runs_root)
    else:
        past_runs(runs_root)


def new_analysis(runs_root: Path):
    st.title("Analyse a CSV")
    launched = st.session_state.get("launched")
    if launched:
        if launched.get("done"):
            show_run(launched["done"])
        elif shown := _waiting(launched):
            plan_review(launched, shown)
        else:
            watch(launched)
        if st.button("Start another analysis"):
            del st.session_state["launched"]
            st.rerun()
        return

    upload = st.file_uploader("CSV file", type="csv")
    samples = sorted((ROOT / "data").glob("*.csv")) if (ROOT / "data").exists() else []
    sample = None
    if upload is None and samples:
        sample = st.selectbox(
            "…or a dataset from data/", [None, *samples], format_func=_name
        )
    if upload is None and sample is None:
        st.caption(
            "Prompts and samples of the data go to the chosen model provider, and "
            "to LangSmith when tracing is on. Ollama keeps everything on this "
            "machine."
        )
        return

    df = pd.read_csv(upload if upload is not None else sample, nrows=1000)
    st.dataframe(df.head(), hide_index=True)
    target = st.selectbox("Target column", ["(detect)", *df.columns])
    provider = st.selectbox("Provider", list(PROVIDERS))
    model = st.text_input("Model", getattr(settings, PROVIDERS[provider]))
    if provider == "ollama":
        st.warning("A local run takes hours on a small GPU (Claude: ~10-20 minutes).")
    review = st.checkbox(
        "Review the plan before it runs",
        value=True,
        help="The lead shows its plan and waits. Ask about it, or tell it what to "
        "add, change or remove; nothing runs until you approve.",
    )

    if st.button("Start the analysis", type="primary"):
        if upload is not None:
            csv = runs_root / "uploads" / upload.name
            csv.parent.mkdir(parents=True, exist_ok=True)
            csv.write_bytes(upload.getvalue())
        else:
            csv = sample
        st.session_state["launched"] = launch(
            csv,
            None if target == "(detect)" else target,
            provider,
            model,
            runs_root,
            approve_plan=review,
        )
        st.rerun()


def launch(
    csv: Path,
    target,
    provider: str,
    model: str,
    runs_root: Path,
    approve_plan: bool = False,
) -> dict:
    """Start `analyst run` in its own process; its console output goes to a log.
    With approve_plan, the page keeps the run's stdin to answer its plan."""
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log = runs_root / "uploads" / f"{stamp}_{csv.stem}.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, "-m", "agent.cli", "run", str(csv.resolve())]
    command += ["--provider", provider, "--model", model, "--out", str(runs_root)]
    if provider != "ollama":  # more revisions and follow-ups than the local default
        command += ["--preset", "hosted"]
    if target:
        command += ["--target", target]
    if approve_plan:
        command += ["--approve-plan"]
    with log.open("w") as out:
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            stdout=out,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE if approve_plan else None,
            text=True,
        )
    return {"process": process, "log": log, "started": time.time()}


def _waiting(launched: dict) -> dict | None:
    """The plan the run waits on, if it's alive and waiting for a reply"""
    run_dir = _run_dir(launched)
    if run_dir is None or launched["process"].poll() is not None:
        return None
    return waiting_plan(read_events(run_dir), launched.get("answered", 0))


def plan_review(launched: dict, shown: dict):
    """The plan the run waits on, the conversation about it, and the replies.
    Outside the refreshing fragment, so a refresh can't clear a message."""
    st.subheader("The plan, waiting for your approval")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "task": t["id"],
                    "specialist": t["specialist"],
                    "question": t["question"],
                    "after": ", ".join(t["depends_on"]),
                }
                for t in shown["tasks"]
            ]
        ),
        hide_index=True,
    )
    for role, text in plan_chat(read_events(_run_dir(launched))):
        st.chat_message("user" if role == "human" else "assistant").write(text)
    if st.button("Approve and run", type="primary"):
        _reply(launched, "approve")
    if text := st.chat_input("Ask about the plan, or tell the lead what to change"):
        _reply(launched, text)
    st.caption(
        "The lead does what you ask: tasks you add aren't held to the plan's usual "
        "limit, and it drops only the tasks you name."
    )


def _reply(launched: dict, text: str):
    """One line to the run's stdin; the page then watches the run again"""
    launched["answered"] = launched.get("answered", 0) + 1
    try:
        launched["process"].stdin.write(" ".join(text.split()) + "\n")
        launched["process"].stdin.flush()
    except OSError:  # the run has stopped; watch shows its console output
        pass
    st.rerun()


def _run_dir(launched: dict) -> Path | None:
    """From the run's first console line, "Run directory: <path> (...)" """
    for line in launched["log"].read_text().splitlines():
        if line.startswith("Run directory: "):
            return ROOT / line.removeprefix("Run directory: ").rsplit(" (", 1)[0]
    return None


@st.fragment(run_every=3)
def watch(launched: dict):
    """Refreshes itself every few seconds until the run ends"""
    run_dir = _run_dir(launched)
    finished = launched["process"].poll() is not None
    events = read_events(run_dir) if run_dir else []
    if any(e["event"] == "run_done" for e in events):
        launched["done"] = run_dir
        st.rerun()  # the whole page, which then shows the report once
    if not finished and waiting_plan(events, launched.get("answered", 0)):
        st.rerun()  # the whole page, which then shows the plan to review
    if finished:  # died before it could record its end
        st.error("The run stopped. Its console output:")
        st.code(launched["log"].read_text()[-3000:] or "(empty)")
        return
    minutes = (time.time() - launched["started"]) / 60
    st.info(f"Running for {minutes:.0f} min… {run_dir or ''}")
    _progress(events)


def _progress(events: list[dict]):
    """What the lead is doing, and a row per task"""
    if now := stage(events):
        st.write(now)
    rows = task_rows(events)
    if not rows:
        return
    st.dataframe(
        pd.DataFrame(
            [
                {"": STATE_ICONS[r["state"]], **r, "follow-up": "yes" * r["follow-up"]}
                for r in rows
            ]
        ),
        hide_index=True,
    )


def past_runs(runs_root: Path):
    st.title("Past runs")
    runs = list_runs(runs_root) if runs_root.exists() else []
    if not runs:
        st.write(f"No runs under {runs_root}.")
        return
    labels = {
        r["run_dir"]: f"{r['name']} · {r['status']}"
        + (f" · {r['minutes']} min" if r["minutes"] else "")
        + (f" · ${r['cost']:.3f}" if r["cost"] is not None else "")
        for r in runs
    }
    run_dir = st.selectbox("Run", list(labels), format_func=labels.get)
    show_run(run_dir)


def show_run(run_dir: Path):
    """A finished run: its grades, trace link, report and a download, then the
    questions asked about it and a box to ask another"""
    meta = json.loads((run_dir / "run_meta.json").read_text())
    if meta.get("trace_url"):
        st.link_button("LangSmith trace", meta["trace_url"])
    st.download_button(
        "Download report.html",
        render_html(run_dir),  # with the questions
        file_name=f"{run_dir.name}.html",
        mime="text/html",
    )
    components.html(
        render_html(run_dir, with_questions=False), height=1100, scrolling=True
    )
    if answers := render_questions(run_dir):
        components.html(answers, height=600, scrolling=True)
    if meta.get("status") == "ok" and (run_dir / "report.md").exists():
        questions(run_dir)


def questions(run_dir: Path):
    """Ask about the run; one question at a time per run"""
    asking = st.session_state.setdefault("asking", {})
    current = asking.get(str(run_dir))
    if current and not current.get("ended"):
        watch_question(current)
        return
    if current:  # ended without answering: its console output, once
        del asking[str(run_dir)]
        st.error("The question stopped before it was answered. Its console output:")
        st.code(current["log"].read_text()[-3000:] or "(empty)")
    with st.form(f"ask {run_dir}", clear_on_submit=True):
        text = st.text_area(
            "Ask a question about this data",
            placeholder="Does the effect hold within each group?",
        )
        if st.form_submit_button("Ask") and text.strip():
            asking[str(run_dir)] = ask(run_dir, text.strip())
            st.rerun()
    st.caption(
        "The lead answers from the recorded facts, or first runs up to 2 new tasks "
        "(a few minutes). It uses the run's provider and model."
    )


def ask(run_dir: Path, text: str) -> dict:
    """Start `analyst ask` in its own process; its console output goes to a log"""
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log = run_dir / "questions" / f"{stamp}_console.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    offset = len(read_events(run_dir))  # this question's events come after
    command = [sys.executable, "-m", "agent.cli", "ask", str(run_dir.resolve()), text]
    with log.open("w") as out:
        process = subprocess.Popen(
            command, cwd=ROOT, stdout=out, stderr=subprocess.STDOUT
        )
    return {
        "process": process,
        "log": log,
        "run_dir": run_dir,
        "offset": offset,
        "started": time.time(),
    }


@st.fragment(run_every=3)
def watch_question(current: dict):
    """Refreshes itself every few seconds until the question ends"""
    events = read_events(current["run_dir"])[current["offset"] :]
    if any(e["event"] == "question_done" for e in events):
        del st.session_state["asking"][str(current["run_dir"])]
        st.rerun()  # the whole page, which then shows the answer
    if current["process"].poll() is not None:  # died before it could record its end
        current["ended"] = True
        st.rerun()
    minutes = (time.time() - current["started"]) / 60
    question = next((e for e in events if e["event"] == "question"), None)
    if question is None:
        st.info("Loading the run…")
        return
    st.info(
        f"Answering for {minutes:.0f} min… Q{question['number']}: {question['question']}"
    )
    _progress(events)


def _name(path: Path | None) -> str:
    return "—" if path is None else path.name


if __name__ == "__main__":  # also how Streamlit runs it
    main()
