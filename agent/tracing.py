"""LangSmith tracing helpers. Tracing is enabled through env vars (see .env.example)."""

import logging
from uuid import UUID

from langchain_core.tracers.langchain import wait_for_all_tracers
from langsmith import Client
from langsmith import utils as ls_utils

logger = logging.getLogger(__name__)


def tracing_enabled() -> bool:
    return bool(ls_utils.tracing_is_enabled())


def trace_url(run_id: UUID) -> str | None:
    """Flush pending traces and return the LangSmith URL of a root run"""
    if not tracing_enabled():
        return None
    try:
        wait_for_all_tracers()
        client = Client()
        return client.get_run_url(run=client.read_run(run_id))
    except Exception as e:
        logger.warning(f"Could not resolve LangSmith trace URL: {e}")
        return None
