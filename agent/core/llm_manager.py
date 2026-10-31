"""Centralized LLM management with caching and configuration"""

import logging
from typing import Any

from langchain.chat_models import init_chat_model

from agent.config import settings

logger = logging.getLogger(__name__)


class LLMManager:
    """
    Centralized LLM management

    Responsibilities:
    - Cache LLM instances to avoid re-initialization
    - Provide per-agent default configurations
    - Allow runtime overrides
    """

    _llm_cache: dict[str, Any] = {}

    # Default configuration per agent type; "model" names the settings field
    AGENT_CONFIGS = {
        "orchestrator": {
            "model": "analyst_model",
            "temperature": 0.3,
        },
        "planner": {
            "model": "analyst_model",
            "temperature": 0.2,
        },
        "eda": {
            "model": "coder_model",
            "temperature": 0.3,
        },
        "statistical": {
            "model": "coder_model",
            "temperature": 0.2,
        },
        "ml": {
            "model": "coder_model",
            "temperature": 0.1,
        },
        "synthesizer": {
            "model": "analyst_model",
            "temperature": 0.3,
        },
        "reporter": {
            "model": "reporter_model",
            "temperature": settings.reporter_temperature,
        },
    }

    @classmethod
    def get_llm(
        cls,
        agent_type: str,
        model_name: str | None = None,
        temperature: float | None = None,
        force_new: bool = False,
    ):
        """
        Get or create LLM for agent type

        Args:
            agent_type: Type of agent (orchestrator, planner, etc.)
            model_name: Override default model
            temperature: Override default temperature
            force_new: Don't use cache, create new instance

        Returns:
            Configured LLM instance

        Example:
            >>> llm = LLMManager.get_llm("orchestrator")
            >>> llm = LLMManager.get_llm("planner", temperature=0.1)
        """
        model_name, temperature = cls.resolve_config(
            agent_type, model_name, temperature
        )

        # Create cache key
        cache_key = f"{agent_type}:{model_name}:{temperature}"

        # Return cached if available
        if not force_new and cache_key in cls._llm_cache:
            logger.debug(f"Using cached LLM for {cache_key}")
            return cls._llm_cache[cache_key]

        # Create new LLM
        logger.info(
            f"Initializing LLM for {agent_type}: {model_name} (temp={temperature})"
        )

        llm = init_chat_model(
            model_name,
            model_provider=settings.model_provider,
            temperature=temperature,
            **cls._provider_kwargs(),
        )

        # Cache it
        cls._llm_cache[cache_key] = llm

        return llm

    @classmethod
    def resolve_config(
        cls,
        agent_type: str,
        model_name: str | None = None,
        temperature: float | None = None,
    ) -> tuple[str, float]:
        """Return (model, temperature) for an agent type, applying overrides"""
        if agent_type not in cls.AGENT_CONFIGS:
            raise ValueError(
                f"Unknown agent type: {agent_type!r}. "
                f"Known: {', '.join(cls.AGENT_CONFIGS)}"
            )
        config = cls.AGENT_CONFIGS[agent_type]
        return (
            model_name or getattr(settings, config["model"]),
            temperature if temperature is not None else config["temperature"],
        )

    @staticmethod
    def _provider_kwargs() -> dict[str, Any]:
        """Provider-specific options passed to init_chat_model"""
        if settings.model_provider == "ollama":
            return {
                "base_url": settings.ollama_base_url,
                "reasoning": settings.llm_reasoning,
                "num_ctx": settings.llm_num_ctx,
                "num_predict": settings.llm_max_tokens,
                "num_gpu": settings.llm_num_gpu,  # None = Ollama default
                "client_kwargs": {"timeout": settings.llm_timeout_s},
            }
        return {
            "max_tokens": settings.llm_max_tokens,
            "timeout": settings.llm_timeout_s,
        }

    @classmethod
    def clear_cache(cls):
        """Clear LLM cache (useful for testing)"""
        cls._llm_cache.clear()
        logger.info("LLM cache cleared")
