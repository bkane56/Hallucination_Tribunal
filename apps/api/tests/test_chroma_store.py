from unittest.mock import MagicMock, patch

from hallucination_tribunal.core.config import get_settings
from hallucination_tribunal.core.providers.chroma_store import (
    get_vector_store,
    reset_vector_store,
)


def test_serverless_uses_ephemeral_chroma_client(monkeypatch):
    monkeypatch.setenv("VERCEL", "1")
    get_settings.cache_clear()
    reset_vector_store()

    with patch("hallucination_tribunal.core.providers.chroma_store.chromadb") as mock_chromadb:
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_collection.count.return_value = 0
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_chromadb.EphemeralClient.return_value = mock_client

        store = get_vector_store()

        mock_chromadb.EphemeralClient.assert_called_once()
        mock_chromadb.PersistentClient.assert_not_called()
        assert store.count() == 0

    reset_vector_store()
    get_settings.cache_clear()


def test_local_uses_persistent_chroma_client(monkeypatch, tmp_path):
    monkeypatch.delenv("VERCEL", raising=False)
    monkeypatch.setenv("CHROMA_PERSIST_DIRECTORY", str(tmp_path / "chroma"))
    get_settings.cache_clear()
    reset_vector_store()

    with patch("hallucination_tribunal.core.providers.chroma_store.chromadb") as mock_chromadb:
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_collection.count.return_value = 0
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_chromadb.PersistentClient.return_value = mock_client

        get_vector_store()

        mock_chromadb.PersistentClient.assert_called_once()
        mock_chromadb.EphemeralClient.assert_not_called()

    reset_vector_store()
    get_settings.cache_clear()
