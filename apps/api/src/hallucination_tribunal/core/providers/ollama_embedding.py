"""Ollama embedding provider — keeps document text on your Ollama host."""

import httpx

from hallucination_tribunal.core.config import get_settings
from hallucination_tribunal.core.providers.embedding import EmbeddingProvider


class OllamaEmbeddingProvider(EmbeddingProvider):
    def __init__(self):
        settings = get_settings()
        self.base_url = settings.ollama_base_url.rstrip("/")
        self.model = settings.ollama_embedding_model
        self._dimension: int | None = None

    @property
    def dimension(self) -> int:
        if self._dimension is None:
            self.embed_query("dimension probe")
        return self._dimension or 768

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        with httpx.Client(timeout=120.0) as client:
            response = client.post(
                f"{self.base_url}/api/embed",
                json={"model": self.model, "input": texts},
            )
            if response.status_code == 404:
                detail = response.text.strip() or "model not found"
                raise RuntimeError(
                    f"Ollama embedding model '{self.model}' is not available ({detail}). "
                    f"Run `ollama pull {self.model}` and set OLLAMA_EMBEDDING_MODEL."
                )
            response.raise_for_status()
            embeddings = response.json()["embeddings"]

        if embeddings and self._dimension is None:
            self._dimension = len(embeddings[0])
        return embeddings

    def embed_query(self, query: str) -> list[float]:
        return self.embed_texts([query])[0]
