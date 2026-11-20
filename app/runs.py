"""What the app reads from run directories: the runs under a folder, a run's
progress events (agent/progress.py) and the state of each task so far. For a
question after the report, the events from its "question" event on."""

import json
from pathlib import Path


def read_events(run_dir: Path) -> list[dict]:
    """progress.jsonl so far; a line still being written is skipped"""
    path = run_dir / "progress.jsonl"
    if not path.exists():
        return []
    events = []
    for line in path.read_text().splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            break
    return events


def task_rows(events: list[dict]) -> list[dict]:
    """One row per task, in plan order, then follow-ups as they're added"""
    tasks: dict[str, dict] = {}

    def add(brief: dict, follow_up=False):
        tasks.setdefault(
            brief["id"],
            {
                "task": brief["id"],
                "specialist": brief["specialist"],
                "question": brief["question"],
                "state": "waiting",
                "cells": 0,
                "errors": 0,
                "findings": None,
                "revisions": 0,
                "follow-up": follow_up,
            },
        )

    for e in events:
        kind = e["event"]
        if kind in ("plan", "asked"):
            for brief in e["tasks"]:
                add(brief)
        elif kind == "plan_revised":  # before any task ran: the new list
            tasks.clear()
            for brief in e["tasks"]:
                add(brief)
        elif kind == "task_started" and e["task"] in tasks:
            row = tasks[e["task"]]
            row["state"] = "revising" if e.get("revision") else "running"
            row["revisions"] = e.get("revision") or 0
        elif kind == "step" and e["task"] in tasks:
            tasks[e["task"]]["cells"] += 1
            tasks[e["task"]]["errors"] += bool(e.get("error"))
        elif kind == "task_finished" and e["task"] in tasks:
            row = tasks[e["task"]]
            row["state"] = "in review"
            row["findings"] = e["findings"]
        elif kind == "reviewed" and e["task"] in tasks:
            tasks[e["task"]]["state"] = {
                "revise": "sent back",
                "completed": "accepted",
                "failed": "failed",
            }[e["outcome"]]
            for brief in e.get("follow_ups", []):
                add(brief, follow_up=True)
    return list(tasks.values())


def waiting_plan(events: list[dict], answered: int = 0) -> dict | None:
    """The plan the run shows while it waits for the human, if it does: its
    last plan_waiting, when more have come than the `answered` ones"""
    shown = [e for e in events if e["event"] == "plan_waiting"]
    return shown[-1] if len(shown) > answered else None


def plan_chat(events: list[dict]) -> list[tuple[str, str]]:
    """The conversation about the plan so far, as (role, text)"""
    chat = []
    for e in events:
        if e["event"] == "plan_message":
            chat.append(("human", e["text"]))
        elif e["event"] == "plan_revised":
            chat.append(("lead", e["reply"]))
    return chat


def stage(events: list[dict]) -> str | None:
    """What the run or question is doing when no task is: before the plan, and
    after the last review while the lead writes the report or the answer"""
    kinds = {e["event"] for e in events}
    if events and events[-1]["event"] == "plan_message":
        return "The lead is reading your message…"
    if events and events[-1]["event"] == "plan_approved":
        return "Plan approved. Starting the tasks…"
    rows = task_rows(events)
    if "question" in kinds:
        if "asked" not in kinds:
            return "The lead is reading the question and the recorded facts…"
        if not rows:
            return "The recorded facts answer it. The lead is writing the answer…"
        if all(r["state"] in ("accepted", "failed") for r in rows):
            return "All tasks are done. The lead is writing the answer…"
        return None
    if not rows:
        return "Profiling the data and planning the analysis…"
    if all(r["state"] in ("accepted", "failed") for r in rows):
        return "All tasks are done. The lead is writing the report…"
    return None


def list_runs(root: Path) -> list[dict]:
    """Run directories under root (at any depth), newest first"""
    runs = []
    for meta_file in root.rglob("run_meta.json"):
        run_dir = meta_file.parent
        if run_dir.is_symlink() or any(p.is_symlink() for p in run_dir.parents):
            continue  # runs/latest points at a run listed already
        try:
            meta = json.loads(meta_file.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        cost = (meta.get("grades") or {}).get("cost_usd")
        runs.append(
            {
                "run_dir": run_dir,
                "name": run_dir.name,
                "status": meta.get("status"),
                "started": meta.get("started", ""),
                "minutes": round(meta["seconds"] / 60, 1)
                if meta.get("seconds")
                else None,
                "cost": cost,
                "report": (run_dir / "report.md").exists(),
            }
        )
    return sorted(runs, key=lambda r: r["started"], reverse=True)
