"""Application configuration management."""

import os
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    APP_NAME: str = "FloatChat API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:8080",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:8080"
        ],
        env="CORS_ORIGINS"
    )
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = Field(env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-4o-mini", env="OPENAI_MODEL")
    
    # MongoDB Configuration
    MONGODB_URI: str = Field(env="MONGODB_URI")
    DB_NAME: str = Field(default="argo_data", env="DB_NAME")
    COLLECTION_NAME: str = Field(default="profiles", env="COLLECTION_NAME")

    # FastAPI Configuration
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    
    # Logging Configuration
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()