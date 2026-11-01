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
    llm_num_ctx: int = 16384  # 8k cut off reports once task reports got complete
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
    max_specialist_steps: int = 5  # LLM steps per task (each runs a cell or finishes)
    max_cell_output_chars: int = 3000  # Output of a cell shown to the specialist
    max_tasks: int = 6  # Upper bound on planned tasks (keeps local runs tractable)
    code_timeout_s: int = 300  # Per run of a task script

    # Paths
    runs_directory: str = "runs"  # One subdirectory per run (see agent/run_store.py)

    # Logging
    log_level: str = "INFO"


settings = Settings()
