"""Base agent class - generic and reusable"""

import logging
from typing import Any

from langchain_core.exceptions import OutputParserException
from langchain_core.messages import HumanMessage
from ollama import ResponseError
from pydantic import ValidationError

from agent.config import settings
from agent.context import check_prompt
from agent.core.llm_manager import LLMManager
from agent.states import HierarchicalState


class BaseAgent:
    """
    Generic base agent that can be used directly or subclassed

    Key Design Principles:
    - Simple: Can be instantiated directly for simple use cases
    - Extensible: Can be subclassed for complex business logic
    - Configurable: Supports structured output, custom models, etc.

    Usage:
        # Direct use (simple cases)
        agent = BaseAgent(agent_type="reporter")
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
        model_name: str | None = None,
        temperature: float | None = None,
        use_structured_output: bool = False,
        output_schema: Any | None = None,
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
            self.llm = LLMManager.with_structured_output(self.llm, output_schema)
            self.logger.debug(
                f"Configured structured output with schema: {output_schema.__name__}"
            )

        # A crashed Ollama runner (HTTP 500, or a stream that ends with no data,
        # a ValueError) is restarted on the next request, and a malformed
        # structured response often parses on a second try
        self.llm = self.llm.with_retry(
            retry_if_exception_type=(
                ResponseError,
                OutputParserException,
                ValidationError,
                ValueError,
            ),
            stop_after_attempt=1 + settings.llm_retries,
        )

    def invoke(self, prompt: str, **kwargs) -> Any:
        """
        Invoke LLM with prompt

        Args:
            prompt: The prompt to send to LLM
            **kwargs: Additional arguments for LLM invocation

        Returns:
            Response from LLM (string or structured object)
        """
        self.logger.debug(
            f"Invoking {self.agent_type} with prompt length: {len(prompt)}"
        )

        try:
            check_prompt(prompt, self.agent_type)
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
