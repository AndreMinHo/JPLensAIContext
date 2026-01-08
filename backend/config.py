"""Configuration management for JPLensAIContext"""

import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # JPLensContext API Configuration
    jplens_api_url: str = "http://localhost:8000"
    jplens_api_timeout: int = 30

    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    openai_max_tokens: int = 1000
    openai_temperature: float = 0.3

    # Service Configuration
    debug: bool = False
    log_level: str = "INFO"

    # Server Configuration
    host: str = "127.0.0.1"
    port: int = 8001

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()