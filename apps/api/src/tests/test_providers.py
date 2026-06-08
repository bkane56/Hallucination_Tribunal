import pytest

from src.core.config import Settings
from src.core.exceptions import ProviderNotConfiguredError
from src.providers.factory import (
    create_embedding_provider,
    create_llm_provider,
    create_vector_store,
)
from src.providers.stubs import InMemoryVectorStore


@pytest.mark.asyncio
async def test_stub_llm_provider_in_test_env() -> None:
    settings = Settings(app_env="test")
    provider = create_llm_provider(settings)
    result = await provider.complete(system_prompt="sys", user_prompt="hello")
    assert result.startswith("stub-response:")


@pytest.mark.asyncio
async def test_in_memory_vector_store_round_trip() -> None:
    from src.models import Chunk, FileType

    store = InMemoryVectorStore()
    chunk = Chunk(
        chunk_id="chunk-1",
        document_id="doc-1",
        chunk_index=0,
        text="Approval is required for external LLM APIs.",
        token_count=10,
        metadata={"filename": "policy.md"},
        source_page=4,
    )
    await store.add_chunks([chunk], [[1.0, 0.0, 0.0, 1.0]])
    results = await store.search([1.0, 0.0, 0.0, 1.0], top_k=3)
    assert len(results) == 1
    assert results[0].filename == "policy.md"
    deleted = await store.delete_by_document_id("doc-1")
    assert deleted == 1
    assert await store.count_chunks() == 0


def test_development_llm_provider_not_configured() -> None:
    settings = Settings(app_env="development", llm_provider="ollama")
    with pytest.raises(ProviderNotConfiguredError) as exc_info:
        create_llm_provider(settings)
    assert "Phase 4" in exc_info.value.message


def test_development_embedding_provider_not_configured() -> None:
    settings = Settings(app_env="development", embedding_provider="local")
    with pytest.raises(ProviderNotConfiguredError):
        create_embedding_provider(settings)


def test_test_env_providers_available() -> None:
    settings = Settings(app_env="test")
    assert create_llm_provider(settings).provider_name == "stub"
    assert create_embedding_provider(settings).provider_name == "stub"
    assert create_vector_store(settings).provider_name == "in_memory"
