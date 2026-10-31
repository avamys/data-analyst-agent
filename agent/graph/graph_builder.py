"""Graph builder for hierarchical multi-agent analysis workflow"""

from langgraph.graph import StateGraph, END, START
import logging
from agent.states import HierarchicalState
from agent.nodes.orchestrator import orchestrator_node
from agent.nodes.planner import planner_node
from agent.nodes.execution_manager import execution_manager_node
from agent.nodes.synthesizer import synthesizer_node
from agent.nodes.reporter import hierarchical_reporter_node


logger = logging.getLogger(__name__)


def build_hierarchical_graph() -> StateGraph:
    """
    Build the hierarchical multi-agent analysis workflow graph

    Flow:
    START → Orchestrator → Planner → Execution Manager → Synthesizer → Reporter → END

    Layers:
    1. Orchestrator: Analyzes dataset, decides strategies
    2. Planner: Decomposes strategies into tasks
    3. Execution Manager: Routes tasks to specialists, manages execution
    4. Synthesizer: Combines findings from all specialists
    5. Reporter: Generates comprehensive final report
    """
    graph = StateGraph(HierarchicalState)

    # Add nodes for each layer
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("planner", planner_node)
    graph.add_node("execution_manager", execution_manager_node)
    graph.add_node("synthesizer", synthesizer_node)
    graph.add_node("reporter", hierarchical_reporter_node)

    # Linear flow through layers
    graph.add_edge(START, "orchestrator")
    graph.add_edge("orchestrator", "planner")
    graph.add_edge("planner", "execution_manager")
    graph.add_edge("execution_manager", "synthesizer")
    graph.add_edge("synthesizer", "reporter")
    graph.add_edge("reporter", END)

    logger.info("Hierarchical graph built successfully")

    return graph.compile()
