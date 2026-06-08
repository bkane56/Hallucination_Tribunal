from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: Literal["development", "production", "test"] = "development"
    frontend_url: str = "http://localhost:3000"
    backend_url: str = "http://localhost:8000"

    llm_provider: Literal["ollama", "openai"] = "ollama"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1"

    embedding_provider: Literal["local", "openai"] = "local"
    local_embedding_model: str = "all-MiniLM-L6-v2"
    openai_api_key: str = ""
    openai_embedding_model: str = "text-embedding-3-small"

    vector_db_provider: Literal["chromadb"] = "chromadb"
    chroma_persist_directory: str = "./data/chroma"
    uploads_directory: str = "./data/uploads"
    seed_directory: str = "./data/seed"
    evals_directory: str = "./data/evals"

    max_upload_size_mb: int = Field(default=25, ge=1, le=100)
    chunk_size: int = Field(default=900, ge=100)
    chunk_overlap: int = Field(default=150, ge=0)

    log_level: Literal["debug", "info", "warning", "error"] = "info"

    @property
    def app_version(self) -> str:
        return "0.1.0"


@lru_cache
def get_settings() -> Settings:
    return Settings()
