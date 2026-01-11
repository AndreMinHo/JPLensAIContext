"""Configuration management for JPLensAIContext"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # 🔑 REQUIRED: AI Provider & Model Configuration
    ai_provider: str = "openai"  # "openai" or "claude"
    ai_model: Optional[str] = None  # Specific model to use (recommended to specify)

    # 🔑 REQUIRED: API Keys (depending on provider)
    openai_api_key: Optional[str] = None
    claude_api_key: Optional[str] = None

    # 🌐 JPLensContext API Configuration (sensible defaults)
    jplens_api_url: str = "http://localhost:8000"
    jplens_api_timeout: int = 30

    # 🤖 AI Model Configuration (defaults if ai_model not specified)
    openai_model: str = "gpt-3.5-turbo"  # Default OpenAI model
    openai_max_tokens: int = 1000
    openai_temperature: float = 0.3

    claude_model: str = "claude-3-haiku-20240307"  # Default Claude model
    claude_max_tokens: int = 1000
    claude_temperature: float = 0.3

    # ⚙️ Service Configuration (development-friendly defaults)
    debug: bool = True
    log_level: str = "INFO"

    # 🖥️ Server Configuration (local development defaults)
    host: str = "localhost"
    port: int = int(os.getenv("PORT", 8001))  # Railway provides PORT env var

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
