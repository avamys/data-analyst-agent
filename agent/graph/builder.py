"""Graph construction"""
from langgraph.graph import StateGraph, END, START
from agent.states import AgentState
from agent.nodes.analyst import analyst_node
from agent.nodes.coder import coder_node
from agent.nodes.critic import critic_node
from agent.graph.routing import (
    check_code_success,
    check_critic_verdict,
    retry_node,
    revise_node,
    finish_node
)

def build_graph() -> StateGraph:
    """Build and compile the agent workflow graph"""
    graph = StateGraph(AgentState)

    graph.add_node("analyst", analyst_node)
    graph.add_node("coder", coder_node)
    graph.add_node("critic", critic_node)
    # graph.add_node("debug", debugger_node)
    graph.add_node("retry", retry_node)
    graph.add_node("revise", revise_node)
    graph.add_node("finish", finish_node)

    graph.add_edge(START, "analyst")
    graph.add_edge("analyst", "coder")

    graph.add_conditional_edges(
        "coder",
        check_code_success,
        {
            "retry": "retry",
            "finish": "finish",
            "critic": "critic"
        }
    )

    graph.add_conditional_edges(
        "critic",
        check_critic_verdict,
        {
            "revise": "revise",
            "finish": "finish"
        }
    )
    
    graph.add_edge("retry", "coder")
    # graph.add_edge("debug", "coder")
    graph.add_edge("revise", "coder")
    graph.add_edge("finish", END)
    
    return graph.compile()