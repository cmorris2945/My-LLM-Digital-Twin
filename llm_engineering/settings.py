"""
Application Settings

Central configuration for the LLM Engineering application.
Loads settings from environment variables or uses defaults.
"""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    To override defaults, set environment variables or create .env file:
    DATABASE_HOST=mongodb://localhost:27017
    DATABASE_NAME=digital_twin
    """
    
    # MongoDB settings - using full URI format like the book
    DATABASE_HOST: str = "mongodb://localhost:27017"  # Full MongoDB URI
    DATABASE_NAME: str = "digital_twin"               # Database name
    
    # Application settings
    APP_NAME: str = "Digital Twin LLM"
    DEBUG: bool = True
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"  # Load from .env file if exists
        case_sensitive = False


# Create global settings instance
settings = Settings()

# Log the configuration (helpful for debugging)
if settings.DEBUG:
    print(f"MongoDB Config: {settings.DATABASE_HOST} -> {settings.DATABASE_NAME}")
