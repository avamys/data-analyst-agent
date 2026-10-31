from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Read overrides from .env (e.g. ANALYST_MODEL=...); unrelated keys and
    # empty values are ignored
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_ignore_empty=True
    )

    # Ollama configuration
    ollama_base_url: str = "http://host.docker.internal:11434"

    # Model configuration
    analyst_model: str = "qwen3.5:9b"
    coder_model: str = "qwen3.5:9b"
    reporter_model: str = "qwen3.5:9b"

    # Generation limits (Ollama). Thinking mode and the 4k default context make
    # local runs hang or silently truncate prompts, so both are set explicitly.
    llm_reasoning: bool = False
    llm_num_ctx: int = 8192
    llm_max_tokens: int = 4096
    llm_timeout_s: int = 900
    # Layers to put on the GPU; None lets Ollama decide. Ollama's estimate can be
    # very conservative on small GPUs, so this is a per-machine setting for .env.
    llm_num_gpu: int | None = None

    model_provider: Literal["ollama", "openai"] = "ollama"
    openai_api_key: str | None = None

    # Temperature settings
    reporter_temperature: float = 0.3

    # Workflow control
    max_code_retries: int = 2  # Retries per task after a failed execution
    max_tasks: int = 6  # Upper bound on planned tasks (keeps local runs tractable)

    # Paths
    runs_directory: str = "runs"  # One subdirectory per run (see agent/run_store.py)

    # Logging
    log_level: str = "INFO"


settings = Settings()
