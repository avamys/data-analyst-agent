"""Graph builder for the lead/specialist analysis workflow"""

import logging

from langgraph.graph import END, START, StateGraph

from agent.nodes.lead import (
    next_step,
    plan_node,
    profile_node,
    review_node,
    run_task_node,
)
from agent.nodes.report import write_report_node
from agent.states import HierarchicalState

logger = logging.getLogger(__name__)


def build_hierarchical_graph() -> StateGraph:
    """
    Build the analysis workflow graph

    Flow:
    START → profile → plan → run_task ⇄ review → report → END

    - profile: deterministic dataset profile (no LLM)
    - plan: the lead writes a backlog of briefs
    - run_task: a specialist works the next brief, or the one sent back
    - review: the lead accepts it or sends it back, and may add follow-ups;
      the loop ends when nothing is sent back and the backlog is empty
    - report: the lead writes the report from the accepted results; numbers
      that match no recorded value go back once, then are listed as such
    """
    graph = StateGraph(HierarchicalState)

    graph.add_node("profile", profile_node)
    graph.add_node("plan", plan_node)
    graph.add_node("run_task", run_task_node)
    graph.add_node("review", review_node)
    graph.add_node("report", write_report_node)

    routes = {"run_task": "run_task", "report": "report"}
    graph.add_edge(START, "profile")
    graph.add_edge("profile", "plan")
    graph.add_conditional_edges("plan", next_step, routes)
    graph.add_edge("run_task", "review")
    graph.add_conditional_edges("review", next_step, routes)
    graph.add_edge("report", END)

    logger.info("Hierarchical graph built successfully")

    return graph.compile()
