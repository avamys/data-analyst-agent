"""Centralized LLM management with caching and configuration"""

import logging
from typing import Any

from anthropic import transform_schema
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel

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

    # Settings fields per agent type, read at call time so presets and CLI flags
    # apply
    AGENT_CONFIGS = {
        "lead": {
            "model": "analyst_model",
            "temperature": "lead_temperature",
            "effort": "lead_effort",
        },
        "eda": {
            "model": "coder_model",
            "temperature": "eda_temperature",
            "effort": "specialist_effort",
        },
        "statistical": {
            "model": "coder_model",
            "temperature": "statistical_temperature",
            "effort": "specialist_effort",
        },
        "ml": {
            "model": "coder_model",
            "temperature": "ml_temperature",
            "effort": "specialist_effort",
        },
        "reporter": {
            "model": "reporter_model",
            "temperature": "reporter_temperature",
            "effort": "lead_effort",
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
            agent_type: Type of agent (lead, eda, etc.)
            model_name: Override default model
            temperature: Override default temperature
            force_new: Don't use cache, create new instance

        Returns:
            Configured LLM instance

        Example:
            >>> llm = LLMManager.get_llm("lead")
            >>> llm = LLMManager.get_llm("eda", temperature=0.1)
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
            **{"temperature": temperature, **cls._provider_kwargs(agent_type)},
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
            model_name or getattr(settings, config["model"]) or settings.model,
            temperature
            if temperature is not None
            else getattr(settings, config["temperature"]),
        )

    @classmethod
    def effort(cls, agent_type: str) -> str | None:
        """Claude's effort for an agent type; None: the model's default"""
        if settings.model_provider != "anthropic":
            return None
        return getattr(settings, cls.AGENT_CONFIGS[agent_type]["effort"])

    @staticmethod
    def with_structured_output(
        llm, schema: type[BaseModel], include_raw=False, effort: str | None = None
    ):
        """Make llm return schema objects, the way the active provider supports"""
        if settings.model_provider != "anthropic":
            # Many OpenRouter free models take tools but not response_format
            method = (
                "function_calling"
                if settings.model_provider == "openrouter"
                else "json_schema"
            )
            return llm.with_structured_output(
                schema, method=method, include_raw=include_raw
            )
        # JSON outputs: schema-valid by construction (forced tool calls let Haiku
        # drop required fields) and accepted by models that reject forced tools
        parser = PydanticOutputParser(pydantic_object=schema)
        llm = llm.bind(
            output_config={
                "format": {"type": "json_schema", "schema": transform_schema(schema)},
                **({"effort": effort} if effort else {}),
            }
        )
        if not include_raw:
            return llm | parser
        return llm | RunnableLambda(
            lambda raw: {
                "raw": raw,
                "parsed": parser.invoke(raw),
                "parsing_error": None,
            }
        )

    @staticmethod
    def _provider_kwargs(agent_type: str = "") -> dict[str, Any]:
        """Provider-specific options passed to init_chat_model"""
        if settings.model_provider == "openrouter":
            if settings.openrouter_api_key is None:
                raise ValueError("OPENROUTER_API_KEY is not set (see .env.example)")
            # OpenRouter speaks the OpenAI API; reasoning is its own request field
            return {
                "model_provider": "openai",
                "base_url": settings.openrouter_base_url,
                "api_key": settings.openrouter_api_key,
                "extra_body": {"reasoning": {"enabled": settings.openrouter_reasoning}},
                "max_tokens": settings.llm_max_tokens,
                "timeout": settings.llm_timeout_s,
            }
        if settings.model_provider == "anthropic":
            if settings.anthropic_api_key is None:
                raise ValueError("ANTHROPIC_API_KEY is not set (see .env.example)")
            return {
                "model_provider": "anthropic",
                "api_key": settings.anthropic_api_key,
                # Current Claude models reject sampling parameters
                "temperature": None,
                "max_tokens": settings.anthropic_report_max_tokens
                if agent_type == "reporter"
                else settings.anthropic_max_tokens,
                "timeout": settings.llm_timeout_s,
            }
        return {
            "model_provider": "ollama",
            "base_url": settings.ollama_base_url,
            "reasoning": settings.llm_reasoning,
            "num_ctx": settings.llm_num_ctx,
            "num_predict": settings.llm_max_tokens,
            "num_gpu": settings.llm_num_gpu,  # None = Ollama default
            "client_kwargs": {"timeout": settings.llm_timeout_s},
        }

    @classmethod
    def clear_cache(cls):
        """Clear LLM cache (useful for testing)"""
        cls._llm_cache.clear()
        logger.info("LLM cache cleared")
