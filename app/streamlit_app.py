"""Streamlit app: upload a CSV, watch the analysis, read its report.

    uv run --group ui streamlit run app/streamlit_app.py

Each analysis runs as its own process (`analyst run`), so a crash can't take
the page down and per-run counters stay per run (agent/context.py); the page
only reads the files the run writes. Past runs open the same way.
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
from agent.html_report import render_html
from app.runs import list_runs, read_events, task_rows

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
        st.warning("A local run takes hours on a small GPU (Claude: ~10 minutes).")

    if st.button("Start the analysis", type="primary"):
        if upload is not None:
            csv = runs_root / "uploads" / upload.name
            csv.parent.mkdir(parents=True, exist_ok=True)
            csv.write_bytes(upload.getvalue())
        else:
            csv = sample
        st.session_state["launched"] = launch(
            csv, None if target == "(detect)" else target, provider, model, runs_root
        )
        st.rerun()


def launch(csv: Path, target, provider: str, model: str, runs_root: Path) -> dict:
    """Start `analyst run` in its own process; its console output goes to a log"""
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log = runs_root / "uploads" / f"{stamp}_{csv.stem}.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, "-m", "agent.cli", "run", str(csv.resolve())]
    command += ["--provider", provider, "--model", model, "--out", str(runs_root)]
    if target:
        command += ["--target", target]
    with log.open("w") as out:
        process = subprocess.Popen(
            command, cwd=ROOT, stdout=out, stderr=subprocess.STDOUT
        )
    return {"process": process, "log": log, "started": time.time()}


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
    if finished:  # died before it could record its end
        st.error("The run stopped. Its console output:")
        st.code(launched["log"].read_text()[-3000:] or "(empty)")
        return
    minutes = (time.time() - launched["started"]) / 60
    st.info(f"Running for {minutes:.0f} min… {run_dir or ''}")
    rows = task_rows(events)
    if not rows:
        st.write("Profiling the data and planning the analysis…")
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
    """A finished run: its grades, trace link, report and a download"""
    page = render_html(run_dir)
    meta = json.loads((run_dir / "run_meta.json").read_text())
    if meta.get("trace_url"):
        st.link_button("LangSmith trace", meta["trace_url"])
    st.download_button(
        "Download report.html", page, file_name=f"{run_dir.name}.html", mime="text/html"
    )
    components.html(page, height=1100, scrolling=True)


def _name(path: Path | None) -> str:
    return "—" if path is None else path.name


if __name__ == "__main__":  # also how Streamlit runs it
    main()
