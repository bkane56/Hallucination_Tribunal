import importlib.util
from unittest.mock import MagicMock, patch

from hallucination_tribunal.core.config import get_settings
from hallucination_tribunal.core.providers.local_embedding import (
    OpenAIEmbeddingProvider,
    get_embedding_provider,
)
from hallucination_tribunal.core.providers.ollama_embedding import OllamaEmbeddingProvider
from hallucination_tribunal.core.providers.simple_embedding import SimpleEmbeddingProvider


def test_ollama_embedding_provider_selected(monkeypatch):
    monkeypatch.setenv("EMBEDDING_PROVIDER", "ollama")
    get_settings.cache_clear()
    get_embedding_provider.cache_clear()

    provider = get_embedding_provider()
    assert isinstance(provider, OllamaEmbeddingProvider)


@patch("hallucination_tribunal.core.providers.ollama_embedding.httpx.Client")
def test_ollama_embedding_provider_calls_embed_api(mock_client_cls, monkeypatch):
    monkeypatch.setenv("EMBEDDING_PROVIDER", "ollama")
    monkeypatch.setenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
    get_settings.cache_clear()
    get_embedding_provider.cache_clear()

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"embeddings": [[0.1, 0.2, 0.3]]}
    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.post.return_value = mock_response
    mock_client_cls.return_value = mock_client

    provider = get_embedding_provider()
    vectors = provider.embed_texts(["policy section one"])

    assert vectors == [[0.1, 0.2, 0.3]]
    mock_client.post.assert_called_once()
    payload = mock_client.post.call_args.kwargs["json"]
    assert payload["model"] == "nomic-embed-text"
    assert payload["input"] == ["policy section one"]


@patch("hallucination_tribunal.core.providers.ollama_embedding.httpx.Client")
def test_ollama_embedding_provider_batches_large_inputs(mock_client_cls, monkeypatch):
    monkeypatch.setenv("EMBEDDING_PROVIDER", "ollama")
    monkeypatch.setenv("EMBEDDING_BATCH_SIZE", "2")
    get_settings.cache_clear()
    get_embedding_provider.cache_clear()

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = [
        {"embeddings": [[0.1], [0.2]]},
        {"embeddings": [[0.3]]},
    ]
    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.post.return_value = mock_response
    mock_client_cls.return_value = mock_client

    provider = get_embedding_provider()
    vectors = provider.embed_texts(["one", "two", "three"])

    assert vectors == [[0.1], [0.2], [0.3]]
    assert mock_client.post.call_count == 2
    first_batch = mock_client.post.call_args_list[0].kwargs["json"]["input"]
    second_batch = mock_client.post.call_args_list[1].kwargs["json"]["input"]
    assert first_batch == ["one", "two"]
    assert second_batch == ["three"]


def test_openai_embedding_provider_selected(monkeypatch):
    monkeypatch.setenv("EMBEDDING_PROVIDER", "openai")
    get_settings.cache_clear()
    get_embedding_provider.cache_clear()

    provider = get_embedding_provider()
    assert isinstance(provider, OpenAIEmbeddingProvider)


def test_openai_package_available_for_openai_embedding_provider():
    assert importlib.util.find_spec("openai") is not None


def test_local_embedding_provider_selected_by_default(monkeypatch):
    monkeypatch.setenv("EMBEDDING_PROVIDER", "local")
    get_settings.cache_clear()
    get_embedding_provider.cache_clear()

    provider = get_embedding_provider()
    assert isinstance(provider, SimpleEmbeddingProvider)
