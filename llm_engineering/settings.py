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


    """

    ## Qdrant settings...
    
    USE_QDRANT_CLOUD: bool = False
    QDRANT_DATABASE_HOST: str = "localhost"
    QDRANT_DATABASE_PORT: int = 6333
    QDRANT_CLOUD_URL: str = ""
    QDRANT_APIKEY: str = ""

    # MongoDB settings - using full URI format 
    DATABASE_HOST: str = "mongodb://localhost:27017"  # Full MongoDB URI
    DATABASE_NAME: str = "digital_twin"               # my Database name

    # Application settings
    APP_NAME: str = "Digital Twin LLM"
    DEBUG: bool = True
    
    #  EMBEDDING SETTINGS:
    TEXT_EMBEDDING_MODEL_ID: str = "sentence-transformers/all-MiniLM-L6-v2"
    RAG_MODEL_DEVICE: str = "cpu"  # can use CUDA if I have GPU in the future
    RERANKING_CROSS_ENCODER_MODEL_ID: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"

    class Config:
        """Pydantic configuration."""
        env_file = ".env"  # Load from .env file
        case_sensitive = False


# Create global settings instance
settings = Settings()

# Log the configuration (helpful for debugging)
if settings.DEBUG:
    print(f"MongoDB Config: {settings.DATABASE_HOST} -> {settings.DATABASE_NAME}")
