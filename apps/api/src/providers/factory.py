from src.core.config import Settings
from src.core.exceptions import ProviderNotConfiguredError
from src.providers.protocols import EmbeddingProvider, LLMProvider, VectorStore
from src.providers.stubs import (
    InMemoryVectorStore,
    StubEmbeddingProvider,
    StubLLMProvider,
)


def create_llm_provider(settings: Settings) -> LLMProvider:
    if settings.app_env == "test":
        return StubLLMProvider()

    if settings.llm_provider == "ollama":
        raise ProviderNotConfiguredError(
            "Ollama LLM provider is configured but not yet implemented. "
            "See Phase 4 — Tribunal pipeline.",
            details={"provider": settings.llm_provider},
        )

    if settings.llm_provider == "openai":
        raise ProviderNotConfiguredError(
            "OpenAI LLM provider is configured but not yet implemented. "
            "See Phase 4 — Tribunal pipeline.",
            details={"provider": settings.llm_provider},
        )

    raise ProviderNotConfiguredError(
        f"Unknown LLM provider: {settings.llm_provider}",
        details={"provider": settings.llm_provider},
    )


def create_embedding_provider(settings: Settings) -> EmbeddingProvider:
    if settings.app_env == "test":
        return StubEmbeddingProvider()

    if settings.embedding_provider == "local":
        raise ProviderNotConfiguredError(
            "Local embedding provider is configured but not yet implemented. "
            "See Phase 2 — Document ingestion.",
            details={"provider": settings.embedding_provider},
        )

    if settings.embedding_provider == "openai":
        raise ProviderNotConfiguredError(
            "OpenAI embedding provider is configured but not yet implemented. "
            "See Phase 2 — Document ingestion.",
            details={"provider": settings.embedding_provider},
        )

    raise ProviderNotConfiguredError(
        f"Unknown embedding provider: {settings.embedding_provider}",
        details={"provider": settings.embedding_provider},
    )


def create_vector_store(settings: Settings) -> VectorStore:
    if settings.app_env == "test":
        return InMemoryVectorStore()

    if settings.vector_db_provider == "chromadb":
        raise ProviderNotConfiguredError(
            "ChromaDB vector store is configured but not yet implemented. "
            "See Phase 2 — Document ingestion.",
            details={"provider": settings.vector_db_provider},
        )

    raise ProviderNotConfiguredError(
        f"Unknown vector store provider: {settings.vector_db_provider}",
        details={"provider": settings.vector_db_provider},
    )
