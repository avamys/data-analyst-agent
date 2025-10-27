from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Ollama configuration
    ollama_base_url: str = "http://host.docker.internal:11434"
    
    # Model configuration
    analyst_model: str = "llama3.1:8b"
    coder_model: str = "llama3.1:8b"
    reporter_model: str = "llama3.1:8b"
    
    # Temperature settings
    analyst_temperature: float = 0.4
    coder_temperature: float = 0.2
    reporter_temperature: float = 0.3
    
    # Workflow control
    max_iterations: int = 10  # Max analyst-coder loops
    max_code_retries: int = 3  # Max retries per code execution

    # Paths
    data_directory: str = "data"
    output_directory: str = "output"
    
    # Logging
    log_level: str = "INFO"

settings = Settings()
