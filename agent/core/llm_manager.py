"""Centralized LLM management with caching and configuration"""

from langchain.chat_models import init_chat_model
from agent.config import settings
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class LLMManager:
    """
    Centralized LLM management

    Responsibilities:
    - Cache LLM instances to avoid re-initialization
    - Provide per-agent default configurations
    - Allow runtime overrides
    """

    _llm_cache: Dict[str, Any] = {}

    # Default configurations for each agent type
    AGENT_CONFIGS = {
        "orchestrator": {
            "model": settings.analyst_model,
            "temperature": 0.3,
        },
        "planner": {
            "model": settings.analyst_model,
            "temperature": 0.2,
        },
        "eda_specialist": {
            "model": settings.coder_model,
            "temperature": 0.3,
        },
        "statistical_specialist": {
            "model": settings.coder_model,
            "temperature": 0.2,
        },
        "ml_specialist": {
            "model": settings.coder_model,
            "temperature": 0.1,
        },
        "synthesizer": {
            "model": settings.analyst_model,
            "temperature": 0.3,
        },
        "reporter": {
            "model": settings.reporter_model,
            "temperature": settings.reporter_temperature,
        },
    }

    @classmethod
    def get_llm(
        cls,
        agent_type: str,
        model_name: Optional[str] = None,
        temperature: Optional[float] = None,
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
        # Get config defaults
        config = cls.AGENT_CONFIGS.get(agent_type, {})
        model_name = model_name or config.get("model", settings.analyst_model)
        temperature = (
            temperature if temperature is not None else config.get("temperature", 0.3)
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
            base_url=settings.ollama_base_url
            if settings.model_provider == "ollama"
            else None,
            temperature=temperature,
        )

        # Cache it
        cls._llm_cache[cache_key] = llm

        return llm

    @classmethod
    def clear_cache(cls):
        """Clear LLM cache (useful for testing)"""
        cls._llm_cache.clear()
        logger.info("LLM cache cleared")

    @classmethod
    def get_cache_info(cls) -> Dict[str, int]:
        """Get cache statistics"""
        return {
            "cached_llms": len(cls._llm_cache),
            "cache_keys": list(cls._llm_cache.keys()),
        }
