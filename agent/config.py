from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    ollama_base_url: str = "http://host.docker.internal:11434"
    analyst_model: str = "llama3.1:8b"
    coder_model: str = "llama3.1:8b"
    analyst_temperature: float = 0.4
    coder_temperature: float = 0.2
    
    max_code_retries: int = 3
    max_revisions: int = 2

    data_directory: str = "data"
    output_directory: str = "output"
    log_level: str = "INFO"

settings = Settings()
