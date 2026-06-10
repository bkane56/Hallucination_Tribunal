from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from hallucination_tribunal.models.domain import Chunk
from hallucination_tribunal.retrieval.service import RetrievalService


@pytest.mark.asyncio
@patch("hallucination_tribunal.retrieval.service.get_embedding_provider")
@patch("hallucination_tribunal.retrieval.service.get_vector_store")
@patch("hallucination_tribunal.retrieval.service.get_database")
async def test_vector_retrieve(mock_db, mock_vector, mock_embed):
    mock_embed.return_value.embed_query.return_value = [0.1, 0.2, 0.3]
    mock_vector.return_value.query.return_value = [
        ("chunk-1", 0.88, {"filename": "policy.md", "document_id": "d1"})
    ]

    db = MagicMock()
    db.get_all_chunks = AsyncMock(
        return_value=[
            Chunk(
                chunk_id="chunk-1",
                document_id="d1",
                chunk_index=0,
                text="Approval required.",
            )
        ]
    )
    db.list_documents = AsyncMock(
        return_value=[MagicMock(document_id="d1", filename="policy.md")]
    )
    mock_db.return_value = db

    service = RetrievalService()
    service.settings.retrieval_mode = "vector"
    sources = await service.retrieve("approval required", top_k=3)

    assert len(sources) == 1
    assert sources[0].filename == "policy.md"
