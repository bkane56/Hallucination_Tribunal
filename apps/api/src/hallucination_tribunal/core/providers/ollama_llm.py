"""Ollama LLM provider."""

import json
from functools import lru_cache
from typing import Any

import httpx

from hallucination_tribunal.core.config import get_settings
from hallucination_tribunal.core.providers.llm import LLMProvider


class OllamaLLMProvider(LLMProvider):
    def __init__(self):
        settings = get_settings()
        self.base_url = settings.ollama_base_url.rstrip("/")
        self.model = settings.ollama_model
        self.timeout = settings.ollama_llm_timeout
        self.keep_alive = settings.ollama_keep_alive
        self._client: httpx.AsyncClient | None = None

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        json_mode: bool = False,
    ) -> str:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "keep_alive": self.keep_alive,
        }
        if json_mode:
            payload["format"] = "json"

        client = self._get_client()
        response = await client.post(f"{self.base_url}/api/chat", json=payload)
        if response.status_code == 404:
            detail = response.text.strip() or "model not found"
            raise RuntimeError(
                f"Ollama model '{self.model}' is not available ({detail}). "
                f"Run `ollama list` and set OLLAMA_MODEL to an installed model, "
                f"or pull it with `ollama pull {self.model}`."
            )
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]

    async def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        schema: dict[str, Any],
    ) -> dict[str, Any]:
        enhanced_system = (
            f"{system_prompt}\n\nRespond with valid JSON matching this schema:\n"
            f"{json.dumps(schema, indent=2)}"
        )
        raw = await self.generate(enhanced_system, user_prompt, json_mode=True)
        return json.loads(raw)


class OpenAILLMProvider(LLMProvider):
    def __init__(self):
        settings = get_settings()
        self.model = settings.openai_model
        self.api_key = settings.openai_api_key

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        json_mode: bool = False,
    ) -> str:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=self.api_key)
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        response = await client.chat.completions.create(**kwargs)
        return response.choices[0].message.content or ""

    async def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        schema: dict[str, Any],
    ) -> dict[str, Any]:
        raw = await self.generate(system_prompt, user_prompt, json_mode=True)
        return json.loads(raw)


@lru_cache
def get_llm_provider() -> LLMProvider:
    settings = get_settings()
    if settings.llm_provider == "openai":
        return OpenAILLMProvider()
    return OllamaLLMProvider()
