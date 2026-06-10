"""Application configuration from environment variables."""

import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _env_files() -> tuple[str, ...]:
    """Load .env from monorepo root first, then cwd."""
    api_root = Path(__file__).resolve().parents[3]
    monorepo_root = Path(__file__).resolve().parents[5]
    if (monorepo_root / "data").exists():
        return (str(monorepo_root / ".env"), str(api_root / ".env"), ".env")
    return (str(api_root / ".env"), ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_env_files(),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "development"
    frontend_url: str = "http://localhost:3000"
    backend_url: str = "http://localhost:8000"
    cors_allowed_origins: str = ""
    api_root_path: str = ""
    storage_root: str = ""

    llm_provider: Literal["ollama", "openai"] = "ollama"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"
    ollama_embedding_model: str = "nomic-embed-text"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    embedding_provider: Literal["local", "ollama", "openai"] = "local"
    local_embedding_model: str = "all-MiniLM-L6-v2"
    openai_embedding_model: str = "text-embedding-3-small"

    vector_db_provider: Literal["chromadb"] = "chromadb"
    chroma_persist_directory: str = "./data/chroma"
    sqlite_database_path: str = "./data/tribunal.db"

    max_upload_size_mb: int = 25
    chunk_size: int = 900
    chunk_overlap: int = 150
    top_k_default: int = 6
    retrieval_mode: Literal["vector", "hybrid"] = "hybrid"

    log_level: str = "info"
    upload_directory: str = Field(default="./data/uploads")
    seed_directory: str = Field(default="./data/seed")
    evals_directory: str = Field(default="./data/evals")

    @model_validator(mode="after")
    def apply_platform_defaults(self) -> "Settings":
        if os.getenv("VERCEL") and not self.storage_root.strip():
            self.storage_root = "/tmp/hallucination-tribunal"
        if os.getenv("VERCEL") and not self.api_root_path.strip():
            self.api_root_path = os.getenv("API_ROOT_PATH", "/server")
        return self

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024

    @property
    def cors_origins(self) -> list[str]:
        origins = {self.frontend_url.strip(), "http://localhost:3000"}
        if self.cors_allowed_origins.strip():
            origins.update(
                origin.strip()
                for origin in self.cors_allowed_origins.split(",")
                if origin.strip()
            )
        return sorted(origins)

    @property
    def project_root(self) -> Path:
        candidate = Path(__file__).resolve().parents[5]
        if (candidate / "data").exists():
            return candidate
        return Path(__file__).resolve().parents[3]

    def resolve_path(self, path: str) -> Path:
        p = Path(path)
        if p.is_absolute():
            return p
        if self.storage_root.strip():
            root = Path(self.storage_root)
            if path.startswith("./data/"):
                remainder = path.removeprefix("./data/").lstrip("/")
                return root / remainder if remainder else root
            if path == "./data":
                return root
        return self.project_root / path

    def ensure_data_directories(self) -> list[Path]:
        paths = [
            self.resolve_path(self.chroma_persist_directory),
            self.resolve_path(self.upload_directory),
            self.resolve_path(self.seed_directory),
            self.resolve_path(self.evals_directory),
        ]
        for path in paths:
            path.mkdir(parents=True, exist_ok=True)
        return paths


@lru_cache
def get_settings() -> Settings:
    return Settings()
