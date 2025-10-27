"""Graph construction for iterative analyst-coder-reporter workflow"""
from langgraph.graph import StateGraph, END, START
from agent.states import AgentState
from agent.nodes.analyst import analyst_node
from agent.nodes.coder import coder_node
from agent.nodes.reporter import reporter_node
from agent.graph.routing import (
    route_analyst_decision,
    route_coder_result,
    retry_node,
)


def build_graph() -> StateGraph:
    """
    Build the iterative analysis workflow graph:
    
    Flow:
    START → Analyst → (decision) → Coder → (check) → Analyst → ... → Reporter → END
    
    The analyst acts as supervisor, deciding when to:
    - ASK_CODER: Send a new task to coder (continues loop)
    - FINISH: Complete analysis and move to reporter
    
    The coder has retry logic for self-debugging on errors.
    """
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("analyst", analyst_node)
    graph.add_node("coder", coder_node)
    graph.add_node("reporter", reporter_node)
    graph.add_node("retry", retry_node)

    # Start with analyst
    graph.add_edge(START, "analyst")

    # Analyst decides: ASK_CODER or FINISH
    graph.add_conditional_edges(
        "analyst",
        route_analyst_decision,
        {
            "coder": "coder",
            "reporter": "reporter"
        }
    )

    # After coder executes, check for errors
    graph.add_conditional_edges(
        "coder",
        route_coder_result,
        {
            "retry": "retry",  # Retry on error
            "analyst": "analyst"  # Success -> back to analyst
        }
    )
    
    # Retry logic
    graph.add_edge("retry", "coder")
    
    # Reporter is terminal
    graph.add_edge("reporter", END)
    
    return graph.compile()
