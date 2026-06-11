from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from hallucination_tribunal.core.config import get_settings
from hallucination_tribunal.core.providers.ollama_llm import OllamaLLMProvider, get_llm_provider


@pytest.mark.asyncio
@patch("hallucination_tribunal.core.providers.ollama_llm.httpx.AsyncClient")
async def test_ollama_llm_keeps_model_loaded_between_calls(mock_client_cls, monkeypatch):
    monkeypatch.setenv("OLLAMA_KEEP_ALIVE", "10m")
    monkeypatch.setenv("OLLAMA_LLM_TIMEOUT", "180")
    get_settings.cache_clear()
    get_llm_provider.cache_clear()

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": {"content": '{"ok": true}'}}
    mock_client = MagicMock()
    mock_client.is_closed = False
    mock_client.post = AsyncMock(return_value=mock_response)
    mock_client_cls.return_value = mock_client

    provider = OllamaLLMProvider()
    await provider.generate("system", "first", json_mode=True)
    await provider.generate("system", "second", json_mode=True)

    assert mock_client.post.await_count == 2
    first_payload = mock_client.post.await_args_list[0].kwargs["json"]
    assert first_payload["keep_alive"] == "10m"
    mock_client_cls.assert_called_once()
