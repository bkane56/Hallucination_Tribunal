from functools import lru_cache

from src.core.config import Settings, get_settings
from src.providers.factory import (
    create_embedding_provider,
    create_llm_provider,
    create_vector_store,
)
from src.providers.protocols import EmbeddingProvider, LLMProvider, VectorStore


def get_app_settings() -> Settings:
    return get_settings()


@lru_cache
def _llm_provider() -> LLMProvider:
    return create_llm_provider(get_settings())


@lru_cache
def _embedding_provider() -> EmbeddingProvider:
    return create_embedding_provider(get_settings())


@lru_cache
def _vector_store() -> VectorStore:
    return create_vector_store(get_settings())


def get_llm_provider() -> LLMProvider:
    return _llm_provider()


def get_embedding_provider() -> EmbeddingProvider:
    return _embedding_provider()


def get_vector_store() -> VectorStore:
    return _vector_store()


def reset_provider_cache() -> None:
    """Clear cached providers. Used in tests when settings change."""
    _llm_provider.cache_clear()
    _embedding_provider.cache_clear()
    _vector_store.cache_clear()
