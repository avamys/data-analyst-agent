"""Run progress as events, one JSON line each in progress.jsonl, and printed

Specialists emit their own steps (task started, each cell run) through the
graph's custom stream, from whichever thread runs the task. The rest comes from
the graph's node updates: the plan, a task finished, the lead's verdict, the
report. The CLI writes every event to the run directory and prints a line for
it; the app (P5.5) reads the file.
"""

import json
import time
from pathlib import Path

from langgraph.config import get_stream_writer


def emit(event: str, **fields) -> None:
    """Send a progress event from inside the graph; a no-op outside it (tests)"""
    try:
        writer = get_stream_writer()
    except RuntimeError:
        return
    writer({"event": event, **fields})


def _result_of_review(update: dict):
    """The task a review step decided on: sent back, or the last one done"""
    if update.get("under_review") is not None:
        return update["under_review"]
    for key in ("completed_tasks", "failed_tasks"):
        if update.get(key):
            return update[key][-1]
    return None


def _count(n: int, noun: str) -> str:
    return f"{n} {noun}" + ("" if n == 1 else "s")


def _minutes(seconds: float) -> str:
    return f"{int(seconds // 60)}m{int(seconds % 60):02d}s"


def _grades_line(grades: dict) -> str:
    """The run's grades in one line, e.g. "5 tasks done, 1 failed · $0.081" """
    if grades.get("tasks_completed") is None:
        return ""
    parts = [f"{_count(grades['tasks_completed'], 'task')} done"]
    if grades.get("tasks_failed"):
        parts[0] += f", {grades['tasks_failed']} failed"
    if grades.get("unverified_numbers"):
        parts.append(
            f"{_count(grades['unverified_numbers'], 'number')} not traced to a fact"
        )
    if grades.get("unresolved_objections"):
        parts.append(f"{_count(grades['unresolved_objections'], 'open objection')}")
    if grades.get("cost_usd") is not None:
        parts.append(f"${grades['cost_usd']:.3f}")
    return "\n  " + " · ".join(parts)


class Progress:
    """Writes events to progress.jsonl and prints one line per event"""

    def __init__(self, path: Path, echo: bool = True):
        self.path = path
        self.echo = echo
        self.start = time.time()
        self.known: set[str] = set()  # Brief ids, to spot follow-ups
        self.started: dict[str, float] = {}  # Task id -> when its work began

    def event(self, event: dict) -> None:
        event = {"time": round(time.time() - self.start, 1), **event}
        with self.path.open("a") as f:
            f.write(json.dumps(event) + "\n")
        if self.echo and (line := self.describe(event)):
            print(line, flush=True)

    def update(self, node: str, update) -> None:
        """Events for a node's output"""
        if not isinstance(update, dict):
            return
        if node == "plan":
            briefs = update.get("backlog", [])
            self.known |= {b.id for b in briefs}
            self.event(
                {
                    "event": "plan",
                    "tasks": [
                        {"id": b.id, "specialist": b.specialist, "question": b.question}
                        for b in briefs
                    ],
                }
            )
        elif node == "run_task" and update.get("under_review") is not None:
            result = update["under_review"]
            report = result.report
            self.event(
                {
                    "event": "task_finished",
                    "task": result.task_id,
                    "status": report.status if report else "failed",
                    "findings": len(report.findings) if report else 0,
                    "cells": len(result.attempts),
                    "error": result.error,
                }
            )
        elif node == "review" and (result := _result_of_review(update)):
            new = [b for b in update.get("backlog", []) if b.id not in self.known]
            self.known |= {b.id for b in new}
            # A task stopped by the context window isn't reviewed (lead.py)
            review = (
                result.reviews[-1]
                if result.reviews and "overflow" not in result.metadata
                else None
            )
            sent_back = update.get("under_review") is not None
            self.event(
                {
                    "event": "reviewed",
                    "task": result.task_id,
                    "verdict": review.verdict if review else None,
                    "outcome": "revise"
                    if sent_back
                    else ("completed" if result.success else "failed"),
                    "feedback": review.feedback if review and sent_back else None,
                    "follow_ups": [
                        {"id": b.id, "specialist": b.specialist, "question": b.question}
                        for b in new
                    ],
                }
            )
        elif node == "report":
            self.event(
                {
                    "event": "report",
                    "unverified": len(update.get("unverified_numbers") or []),
                }
            )

    def describe(self, event: dict) -> str | None:
        """The console line for an event"""
        kind = event["event"]
        if kind == "plan":
            ids = ", ".join(t["id"] for t in event["tasks"])
            return f"Plan: {_count(len(event['tasks']), 'task')} ({ids})"
        if kind == "task_started":
            self.started[event["task"]] = event["time"]
            if event.get("revision"):
                return f"→ {event['task']} revision {event['revision']}"
            return f"→ {event['task']}: {event['question']}"
        if kind == "step":
            outcome = f"error: {event['error']}" if event.get("error") else "ok"
            return f"  {event['task']} step {event['step']}: cell {outcome}"
        if kind == "task_finished":
            took = event["time"] - self.started.get(event["task"], event["time"])
            return (
                f"  {event['task']} finished ({event['status']}): "
                f"{_count(event['findings'], 'finding')}, "
                f"{_count(event['cells'], 'cell')} run, {_minutes(took)}"
            )
        if kind == "reviewed":
            task = event["task"]
            if event["outcome"] == "revise":
                line = f"↺ {task} sent back: {event['feedback'] or ''}".rstrip()
                line = line if len(line) <= 100 else line[:99] + "…"
            elif event["outcome"] == "completed":
                line = f"✓ {task} accepted" + (
                    "" if event["verdict"] == "accept" else " with an open objection"
                )
            else:
                line = f"✗ {task} failed"
            if event["follow_ups"]:
                line += "\n+ follow-ups: " + ", ".join(
                    f"{t['id']} ({t['question']})" for t in event["follow_ups"]
                )
            return line
        if kind == "report":
            unverified = event["unverified"]
            return "Report written" + (
                f" ({_count(unverified, 'number')} not traced to a fact)"
                if unverified
                else ""
            )
        if kind == "run_done":
            took = _minutes(event["seconds"])
            if event["status"] == "ok":
                line = f"Done in {took}: {event['report'] or 'no report'}"
            else:
                line = f"Run {event['status']} after {took}: {event.get('error') or ''}"
            return line + _grades_line(event.get("grades") or {})
        return None
