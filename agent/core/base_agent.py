"""Base agent class - generic and reusable"""
from typing import Optional, Any
from langchain_core.messages import HumanMessage
from agent.core.llm_manager import LLMManager
from agent.states import HierarchicalState
import logging


class BaseAgent:
    """
    Generic base agent that can be used directly or subclassed
    
    Key Design Principles:
    - Simple: Can be instantiated directly for simple use cases
    - Extensible: Can be subclassed for complex business logic
    - Configurable: Supports structured output, custom models, etc.
    
    Usage:
        # Direct use (simple cases)
        agent = BaseAgent(agent_type="synthesizer")
        result = agent.invoke(prompt)
        
        # Subclass (complex logic)
        class OrchestratorAgent(BaseAgent):
            def execute(self, state):
                # Custom business logic
                pass
    """
    
    def __init__(
        self,
        agent_type: str,
        model_name: Optional[str] = None,
        temperature: Optional[float] = None,
        use_structured_output: bool = False,
        output_schema: Optional[Any] = None,
    ):
        """
        Initialize agent
        
        Args:
            agent_type: Identifier for this agent (used for LLM config)
            model_name: Override default model
            temperature: Override default temperature
            use_structured_output: Whether to use structured output
            output_schema: Pydantic model for structured output
        """
        self.agent_type = agent_type
        self.logger = logging.getLogger(f"agent.{agent_type}")
        
        # Get LLM from centralized manager (cached)
        self.llm = LLMManager.get_llm(
            agent_type=agent_type,
            model_name=model_name,
            temperature=temperature,
        )
        
        # Support structured output
        if use_structured_output and output_schema:
            self.llm = self.llm.with_structured_output(output_schema)
            self.logger.debug(f"Configured structured output with schema: {output_schema.__name__}")
    
    def invoke(self, prompt: str, **kwargs) -> Any:
        """
        Invoke LLM with prompt
        
        Args:
            prompt: The prompt to send to LLM
            **kwargs: Additional arguments for LLM invocation
        
        Returns:
            Response from LLM (string or structured object)
        """
        self.logger.debug(f"Invoking {self.agent_type} with prompt length: {len(prompt)}")
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)], **kwargs)
            self.logger.debug(f"Received response from {self.agent_type}")
            return response
        except Exception as e:
            self.logger.error(f"Error invoking {self.agent_type}: {e}", exc_info=True)
            raise
    
    def execute(self, state: HierarchicalState) -> HierarchicalState:
        """
        Execute agent logic
        
        Override this method in subclasses for custom business logic.
        For simple cases, you can use the agent directly without subclassing.
        
        Args:
            state: Current hierarchical state
        
        Returns:
            Updated state
        
        Raises:
            NotImplementedError: If not overridden in subclass
        """
        raise NotImplementedError(
            f"Agent {self.agent_type} must implement execute() method or be used directly with invoke()"
        )
