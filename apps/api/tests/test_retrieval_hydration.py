from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from hallucination_tribunal.core.config import get_settings
from hallucination_tribunal.models.domain import Chunk, Document, DocumentStatus
from hallucination_tribunal.retrieval.service import RetrievalService


@pytest.mark.asyncio
async def test_serverless_hydrates_empty_vector_index(monkeypatch):
    monkeypatch.setenv("VERCEL", "1")
    get_settings.cache_clear()

    chunk = Chunk(
        chunk_id="chunk-1",
        document_id="doc-1",
        chunk_index=0,
        text="Approval required for all purchases.",
    )
    doc = Document(
        document_id="doc-1",
        filename="policy.md",
        file_type="md",
        original_path="/tmp/policy.md",
        status=DocumentStatus.INDEXED,
    )

    mock_vector = MagicMock()
    mock_vector.count.side_effect = [0, 1]
    mock_vector.query.return_value = [
        ("chunk-1", 0.9, {"filename": "policy.md", "document_id": "doc-1"})
    ]

    mock_embed = MagicMock()
    mock_embed.embed_query.return_value = [0.1, 0.2]
    mock_embed.embed_texts.return_value = [[0.1, 0.2]]

    mock_db = MagicMock()
    mock_db.get_all_chunks = AsyncMock(return_value=[chunk])
    mock_db.get_chunks_by_ids = AsyncMock(return_value=[chunk])
    mock_db.list_documents = AsyncMock(return_value=[doc])

    with (
        patch(
            "hallucination_tribunal.retrieval.service.get_vector_store",
            return_value=mock_vector,
        ),
        patch(
            "hallucination_tribunal.retrieval.service.get_embedding_provider",
            return_value=mock_embed,
        ),
        patch(
            "hallucination_tribunal.retrieval.service.get_database",
            return_value=mock_db,
        ),
    ):
        service = RetrievalService()
        service.settings.retrieval_mode = "vector"
        sources = await service.retrieve("approval required", top_k=3)

    mock_embed.embed_texts.assert_called_once()
    mock_vector.upsert_chunks.assert_called_once()
    assert len(sources) == 1
    assert sources[0].chunk_id == "chunk-1"

    get_settings.cache_clear()
