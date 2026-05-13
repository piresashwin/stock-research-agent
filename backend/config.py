import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Stock Deep Research Agent API"
    database_url: str = "sqlite:///./research_agent.db"
    openai_base_url: str = "http://localhost:1234/v1"
    openai_api_key: str = "lm-studio"
    model_name: str = "default"  # LM Studio uses loaded model automatically if not restricted
    headless_browser: bool = True
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
