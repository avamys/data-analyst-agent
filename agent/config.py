"""Every setting that changes how a run behaves, in one place

Precedence, lowest first: the defaults below < the preset (PRESET or --preset)
< .env and environment variables (e.g. MAX_FOLLOW_UPS=4) < command-line flags.
run_meta.json records the resolved values of every run.
"""

from typing import Literal

from pydantic import PrivateAttr, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# Named sets of values; a preset replaces defaults, never explicit settings
PRESETS: dict[str, dict] = {
    # The defaults: sized for qwen3.5 on a 4 GB GPU, ~1-2 h per run
    "local": {},
    # Hosted models: ~2x the time and cost of the defaults (Haiku 5.5, 2026-11-02:
    # 18.7 min, $0.18), and no review objection left unresolved
    "hosted": {"max_follow_ups": 5, "max_revisions": 2},
}


class Settings(BaseSettings):
    # Unrelated keys in .env and empty values are ignored
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_ignore_empty=True
    )

    preset: Literal["local", "hosted"] = "local"

    # --- Provider and models ---
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

    # --- Generation ---
    # Thinking mode and the 4k default context make local Ollama runs hang or
    # silently truncate prompts, so both are set explicitly.
    llm_reasoning: bool = False  # Ollama only; OpenRouter uses openrouter_reasoning
    llm_num_ctx: int = 16384  # 8k cut off reports once task reports got complete
    llm_max_tokens: int = 4096
    # Thinking counts against the cap, and an unused cap costs nothing
    anthropic_max_tokens: int = 16000
    llm_timeout_s: int = 900
    # Layers to put on the GPU; None lets Ollama decide. Ollama's estimate can be
    # very conservative on small GPUs, so this is a per-machine setting for .env.
    llm_num_gpu: int | None = None
    # Extra attempts after a parse failure or a crashed Ollama runner
    llm_retries: int = 1

    # Temperature per role (not sent to current Claude models, which reject it)
    lead_temperature: float = 0.2
    eda_temperature: float = 0.3
    statistical_temperature: float = 0.2
    ml_temperature: float = 0.1
    reporter_temperature: float = 0.3

    # --- Budgets: how much work a run does ---
    max_tasks: int = 6  # Upper bound on planned tasks
    max_follow_ups: int = 2  # Tasks the lead may add during reviews, per run
    max_revisions: int = 1  # Times the lead may send one task back
    max_specialist_steps: int = 5  # LLM steps per attempt (run a cell or finish)
    max_report_rewrites: int = 1  # Times numbers matching no fact go back to the writer
    code_timeout_s: int = 300  # Per run of a task script

    # --- What agents see: caps on prompt content ---
    max_cell_output_chars: int = 3000  # Latest cell output shown to the specialist
    prompt_fact_chars: int = 200  # Fact value shown in prompts (model scores: whole)
    review_script_chars: int = 8000  # End of a task's script the lead reviews
    plan_description_chars: int = 1000  # Dataset description the lead plans from

    # --- Sanity checks shown to the lead during review ---
    overfit_gap: float = 0.1  # Train score above test score by more than this
    near_perfect_score: float = 0.99  # Test score suspicious at or above this
    baseline_margin: float = 0.02  # Accuracy within this of the baseline adds nothing

    # --- Profiling ---
    # A column is a leakage suspect when on its own it removes this share of the
    # errors of always predicting the most frequent class, or (regression) when its
    # |correlation| with the target reaches it
    leakage_score: float = 0.9
    imbalance_ratio: float = 2.0  # Largest / smallest class above this: imbalanced

    # --- Number check of the report ---
    number_check_max_label: int = 10  # Plain integers up to this aren't checked
    number_check_conventions: list[float] = [0.05]  # Conventions, not results

    # --- Eval judge (evals/judge.py); called through the Anthropic API whatever
    # the agent's provider, with anthropic_api_key ---
    judge_model: str = "claude-sonnet-5-5"

    # --- Paths and logging ---
    runs_directory: str = "runs"  # One subdirectory per run (see agent/run_store.py)
    log_level: str = "INFO"

    # Fields set explicitly (arguments, environment, .env): presets leave them
    _explicit: set[str] = PrivateAttr(default_factory=set)

    def model_post_init(self, context) -> None:
        self._explicit = set(self.model_fields_set) - {"preset"}
        self.use_preset(self.preset)

    def use_preset(self, name: str) -> None:
        """Switch to a preset: its values replace defaults, not explicit settings"""
        self.preset = name
        for key in {key for values in PRESETS.values() for key in values}:
            if key not in self._explicit:
                default = type(self).model_fields[key].default
                setattr(self, key, PRESETS[name].get(key, default))


settings = Settings()
