"""Analyst Agent - Supervisor that forms hypotheses and directs the investigation"""
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
import logging
from agent.states import AgentState, AnalystDecision, ConversationTurn
from agent.config import settings


logger = logging.getLogger(__name__)


analyst_llm = init_chat_model(
    settings.analyst_model,
    model_provider="ollama",
    base_url=settings.ollama_base_url,
    temperature=settings.analyst_temperature,
)
analyst_structured = analyst_llm.with_structured_output(AnalystDecision)


def analyst_node(state: AgentState) -> AgentState:
    """
    Analyst acts as supervisor:
    - Forms hypotheses based on dataset info and previous results
    - Interprets coder's outputs
    - Decides next action: ASK_CODER (with new task) or FINISH
    """
    dataset_info = state.dataset_info
    conversation_history = state.conversation_history
    insights_collected = state.insights_collected
    iteration_count = state.iteration_count
    code_output = state.code_output
    
    # Build context from previous iterations
    history_context = ""
    if conversation_history:
        history_context = "PREVIOUS INVESTIGATION STEPS:\n"
        for turn in conversation_history:
            history_context += f"\n{turn.iteration}. Hypothesis: {turn.hypothesis}\n"
            history_context += f"   Task: {turn.code_task}\n"
            history_context += f"   Result: {turn.code_result[:200]}...\n"
            history_context += f"   Interpretation: {turn.interpretation}\n"
    
    insights_context = ""
    if insights_collected:
        insights_context = f"\nKEY INSIGHTS FOUND SO FAR:\n" + "\n".join([f"- {insight}" for insight in insights_collected])
    
    if iteration_count == 0:
        prompt = f"""You are a senior data analyst supervising an investigation.

DATASET INFO:
{dataset_info}

This is your first look at the data. Your task:
1. Form an initial hypothesis about something interesting to investigate
2. Define a specific code task for the coder agent to execute
3. Decide: ASK_CODER to start investigation

Be specific and focused. Start with exploratory questions like:
- "What are the key patterns in the data?"
- "Are there any correlations between X and Y?"
- "How does X vary across different groups?"

IMPORTANT: Focus on STATISTICAL and NUMERICAL analysis during investigation.
- Request: counts, percentages, correlations, statistical tests, group comparisons
- AVOID requesting: charts, plots, visualizations, graphs during investigation
- Reason: You cannot see images. Numerical results are much more useful for interpretation.
- Visualizations can be created later in the final report.

Decision format:
- decision: "ASK_CODER" 
- reasoning: Why this hypothesis is worth investigating
- hypothesis: Your current hypothesis
- code_task: Specific task for coder (e.g., "Calculate correlation between Age and Survived, print statistics")
"""
    else:
        prompt = f"""You are a senior data analyst supervising an investigation.

DATASET INFO:
{dataset_info}

{history_context}

{insights_context}

LATEST CODER OUTPUT:
{code_output[:1000]}

Based on the latest results and previous investigation:
1. Interpret what the coder's output reveals
2. Decide if you want to:
   - ASK_CODER: Investigate a new hypothesis or dig deeper into current findings
   - FINISH: You have enough insights to write a comprehensive report

Guidelines:
- If results are interesting, form a follow-up hypothesis
- If you've investigated {settings.max_iterations - 1}+ different angles, consider FINISH
- Each new task should build on previous findings
- Be specific about what code to run next

IMPORTANT: Focus on STATISTICAL and NUMERICAL analysis during investigation.
- Request: counts, percentages, correlations, statistical tests, group comparisons, summary tables
- AVOID requesting: charts, plots, visualizations, graphs during investigation
- Reason: You cannot see images. Numerical results are much more useful for interpretation.
- Visualizations will be created later in the final report.

Decision format:
- decision: "ASK_CODER" or "FINISH"
- reasoning: Why you're making this decision
- hypothesis: New hypothesis to investigate (if ASK_CODER)
- code_task: Specific task for coder (if ASK_CODER)
"""
    
    decision = analyst_structured.invoke([HumanMessage(content=prompt)])
    
    # Force FINISH if max iterations reached
    if iteration_count >= settings.max_iterations - 1:
        logger.warning(f"Max iterations ({settings.max_iterations}) will be reached. Forcing FINISH.")
        from agent.states import AnalystDecision
        decision = AnalystDecision(
            decision="FINISH",
            reasoning=f"Maximum iterations reached. {decision.reasoning if decision else 'Wrapping up analysis.'}",
            hypothesis=None,
            code_task=None
        )
    
    logger.info(f"Analyst Decision (Iteration {iteration_count + 1}):")
    logger.info(f"  Decision: {decision.decision}")
    logger.info(f"  Reasoning: {decision.reasoning}")
    if decision.hypothesis:
        logger.info(f"  Hypothesis: {decision.hypothesis}")
    if decision.code_task:
        logger.info(f"  Code Task: {decision.code_task}")
    
    # Update state
    state.current_decision = decision
    state.iteration_count += 1
    
    # If asking coder, prepare the task
    if decision.decision == "ASK_CODER":
        state.code_task = decision.code_task or ""
        
        # If we have a previous iteration, save it to history
        if code_output and iteration_count > 0:
            # Interpret the previous result
            interpretation = _interpret_result(decision.reasoning, code_output[:500])
            
            prev_turn = ConversationTurn(
                iteration=iteration_count,
                hypothesis=conversation_history[-1].hypothesis if conversation_history else "Initial exploration",
                code_task=state.code_task,
                code_result=code_output[:500],
                interpretation=interpretation
            )
            state.conversation_history.append(prev_turn)
            
            # Extract key insight
            if "insight" in interpretation.lower() or "found" in interpretation.lower():
                state.insights_collected.append(interpretation[:200])
    
    return state


def _interpret_result(reasoning: str, code_output: str) -> str:
    """Extract interpretation from reasoning and output"""
    # Simple extraction - in production could use another LLM call
    if "correlation" in code_output.lower():
        return f"Correlation analysis: {reasoning}"
    elif "distribution" in code_output.lower():
        return f"Distribution analysis: {reasoning}"
    else:
        return reasoning[:200]