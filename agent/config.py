from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Read overrides from .env (e.g. ANALYST_MODEL=...); unrelated keys and
    # empty values are ignored
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_ignore_empty=True
    )

    # Where models run: local Ollama, or hosted OpenRouter / Anthropic. Each provider
    # keeps its own model, so switching is one setting (MODEL_PROVIDER or --provider).
    model_provider: Literal["ollama", "openrouter", "anthropic"] = "ollama"

    # Ollama configuration
    ollama_base_url: str = "http://host.docker.internal:11434"
    ollama_model: str = "qwen3.5:9b"

    # OpenRouter configuration. Free (":free") models have a daily request cap;
    # scripts/llm_smoke.py shows what is left.
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_api_key: SecretStr | None = None
    openrouter_model: str = "nvidia/nemotron-3-ultra-550b-a55b:free"
    openrouter_reasoning: bool = True

    # Anthropic configuration (thinking is on by default on current Claude models)
    anthropic_api_key: SecretStr | None = None
    anthropic_model: str = "claude-haiku-5-5"

    # Per-role model overrides; empty = the provider's model above
    analyst_model: str | None = None
    coder_model: str | None = None
    reporter_model: str | None = None

    @property
    def model(self) -> str:
        """The active provider's model"""
        return {
            "ollama": self.ollama_model,
            "openrouter": self.openrouter_model,
            "anthropic": self.anthropic_model,
        }[self.model_provider]

    # Generation limits. Thinking mode and the 4k default context make local
    # Ollama runs hang or silently truncate prompts, so both are set explicitly.
    llm_reasoning: bool = False  # Ollama only; OpenRouter uses openrouter_reasoning
    llm_num_ctx: int = 16384  # 8k cut off reports once task reports got complete
    llm_max_tokens: int = 4096
    llm_timeout_s: int = 900
    # Layers to put on the GPU; None lets Ollama decide. Ollama's estimate can be
    # very conservative on small GPUs, so this is a per-machine setting for .env.
    llm_num_gpu: int | None = None

    # Temperature settings
    reporter_temperature: float = 0.3

    # Workflow control
    max_specialist_steps: int = 5  # LLM steps per task (each runs a cell or finishes)
    max_cell_output_chars: int = 3000  # Output of a cell shown to the specialist
    max_tasks: int = 6  # Upper bound on planned tasks (keeps local runs tractable)
    max_follow_ups: int = 2  # Tasks the lead may add during reviews
    max_revisions: int = 1  # Times the lead may send one task back
    code_timeout_s: int = 300  # Per run of a task script

    # Paths
    runs_directory: str = "runs"  # One subdirectory per run (see agent/run_store.py)

    # Logging
    log_level: str = "INFO"


settings = Settings()
