"""
Configuration file for the AI-Powered Talent Scouting Agent.
"""
from typing import Optional
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # LLM provider settings
    LLM_PROVIDER: str = "gemini"
    GEMINI_API_KEY: Optional[str] = None

    # Model settings
    MODEL_NAME: str = "gemini-3-flash"
    EMBEDDING_BACKEND: str = "hash"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # Application settings
    DEBUG: bool = False
    DATABASE_URL: str = "sqlite:///./talent_scout.db"
    
    # Vector store settings
    VECTOR_STORE_PATH: str = "./data/vector_store.faiss"
    
    class Config:
        env_file = ".env"
        
    @classmethod
    def settings_customise_sources(cls, settings_cls, init_settings, env_settings, dotenv_settings, file_secret_settings):
        # Ignore system environment variables, only use .env file and init settings
        return dotenv_settings, init_settings


settings = Settings()
