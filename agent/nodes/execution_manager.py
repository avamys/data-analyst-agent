"""Execution Manager - Builds and runs dynamic specialist subgraph"""

import logging
from collections.abc import Callable

from langgraph.graph import END, START, StateGraph

from agent.core.specialists import get_specialist
from agent.states import AnalysisPlan, HierarchicalState, SubTask

logger = logging.getLogger(__name__)


def create_specialist_node(task: SubTask) -> Callable:
    """
    Factory function that creates a node function for a specific task

    Each task gets its own dedicated node function that:
    - Executes the task using the appropriate specialist
    - Updates state with the result
    - Logs execution details

    Args:
        task: The SubTask this node will execute

    Returns:
        Node function that takes and returns HierarchicalState
    """

    def specialist_node_fn(state: HierarchicalState) -> HierarchicalState:
        logger.info(f"\n{'=' * 60}")
        logger.info(f"Executing Task: {task.id}")
        logger.info(f"Type: {task.specialist}")
        logger.info(f"Description: {task.description}")
        if task.dependencies:
            logger.info(f"Dependencies: {task.dependencies}")
        logger.info(f"{'=' * 60}\n")

        # Get appropriate specialist
        specialist = get_specialist(task.specialist, max_retries=2)

        # Execute task
        result = specialist.execute(task, state)

        # Update state
        state.completed_tasks.append(result)

        # Log result
        if result.success:
            logger.info(f"✓ Task {task.id} completed successfully")
            if result.insights:
                logger.info(f"  Insights: {len(result.insights)} found")
        else:
            logger.error(f"✗ Task {task.id} failed: {result.error}")
            state.failed_tasks.append(result)

        # Progress update
        completed = len(state.completed_tasks)
        total = len(state.analysis_plan.tasks)
        logger.info(f"Progress: {completed}/{total} tasks completed\n")

        return state

    # Set a readable name for debugging
    specialist_node_fn.__name__ = f"specialist_node_{task.id}"

    return specialist_node_fn


def build_specialist_subgraph(execution_plan: AnalysisPlan):
    """
    Build a dynamic subgraph where each task is a node

    Creates a graph structure where:
    - Each task becomes a dedicated node
    - Tasks execute sequentially following the execution_order
    - Dependencies are implicitly satisfied by the order
    - All task executions are visible as graph nodes

    Sequential execution ensures only one LLM runs at a time
    (important for local LLM deployments)

    Args:
        execution_plan: AnalysisPlan with tasks and execution order

    Returns:
        Compiled LangGraph that can be invoked
    """
    logger.info("Building dynamic specialist subgraph...")

    subgraph = StateGraph(HierarchicalState)

    # Add a node for each task
    for task in execution_plan.tasks:
        subgraph.add_node(task.id, create_specialist_node(task))
        logger.info(f"  Added node: {task.id} ({task.specialist})")

    # Use planner's execution order for sequential chaining
    execution_order = execution_plan.execution_order

    logger.info(f"\nSequential execution order ({len(execution_order)} tasks):")
    logger.info(f"  {' → '.join(execution_order)}")

    # Create sequential chain
    for i, task_id in enumerate(execution_order):
        if i == 0:
            # First task connects from START
            subgraph.add_edge(START, task_id)
        else:
            # Each task waits for previous to complete
            subgraph.add_edge(execution_order[i - 1], task_id)

    # Last task connects to END
    if execution_order:
        subgraph.add_edge(execution_order[-1], END)
    else:
        # No tasks - connect START directly to END
        logger.warning("No tasks in execution plan!")
        subgraph.add_edge(START, END)

    logger.info("Subgraph compiled successfully\n")

    return subgraph.compile()


def execution_manager_node(state: HierarchicalState) -> HierarchicalState:
    """
    Execution Manager - Builds and runs dynamic specialist subgraph

    This node:
    1. Takes the execution plan from the planner
    2. Builds a dynamic subgraph where each task is a node
    3. Runs the subgraph (sequential execution)
    4. Returns the updated state with all task results

    All specialist executions are visible as proper graph nodes!

    Args:
        state: Current hierarchical state with execution plan

    Returns:
        Updated state with completed tasks
    """
    if not state.analysis_plan or not state.analysis_plan.tasks:
        logger.warning("No execution plan found! Skipping specialist execution.")
        return state

    logger.info("=" * 80)
    logger.info("EXECUTION PHASE - DYNAMIC SUBGRAPH")
    logger.info("=" * 80)
    logger.info(f"Total tasks to execute: {len(state.analysis_plan.tasks)}")
    logger.info("")

    # Build dynamic subgraph based on execution plan
    specialist_subgraph = build_specialist_subgraph(state.analysis_plan)

    # Execute the subgraph
    logger.info("Starting specialist subgraph execution...\n")
    result_state = specialist_subgraph.invoke(state)

    # LangGraph may return a dict instead of state object
    if isinstance(result_state, dict):
        # Update our state with the dict values
        for key, value in result_state.items():
            if hasattr(state, key):
                setattr(state, key, value)
        result_state = state

    # Summary
    successful = sum(1 for r in result_state.completed_tasks if r.success)
    failed = len(result_state.completed_tasks) - successful

    logger.info("\n" + "=" * 80)
    logger.info("EXECUTION SUMMARY")
    logger.info(f"Total Tasks: {len(state.analysis_plan.tasks)}")
    logger.info(f"Completed: {len(result_state.completed_tasks)}")
    logger.info(f"Failed: {failed}")
    logger.info(
        f"Success Rate: {successful}/{len(result_state.completed_tasks) if result_state.completed_tasks else 0}"
    )
    logger.info("=" * 80 + "\n")

    return result_state
