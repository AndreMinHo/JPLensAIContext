"""Configuration management for JPLensAIContext"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # 🔑 REQUIRED: AI Provider Configuration
    ai_provider: str = "openai"  # "openai" or "claude"

    # 🔑 REQUIRED: API Keys (depending on provider)
    openai_api_key: Optional[str] = None
    claude_api_key: Optional[str] = None

    # 🌐 JPLensContext API Configuration (sensible defaults)
    jplens_api_url: str = "http://localhost:8000"
    jplens_api_timeout: int = 30

    # 🤖 AI Model Configuration (optimized defaults)
    openai_model: str = "gpt-4"
    openai_max_tokens: int = 1000
    openai_temperature: float = 0.3

    claude_model: str = "claude-3-sonnet-20240229"
    claude_max_tokens: int = 1000
    claude_temperature: float = 0.3

    # ⚙️ Service Configuration (development-friendly defaults)
    debug: bool = True
    log_level: str = "INFO"

    # 🖥️ Server Configuration (local development defaults)
    host: str = "127.0.0.1"
    port: int = 8001

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()