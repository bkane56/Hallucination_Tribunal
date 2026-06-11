"""Ollama embedding provider — keeps document text on your Ollama host."""

import httpx

from hallucination_tribunal.core.config import get_settings
from hallucination_tribunal.core.logging import get_logger
from hallucination_tribunal.core.providers.embedding import EmbeddingProvider, iter_text_batches

logger = get_logger(__name__)


class OllamaEmbeddingProvider(EmbeddingProvider):
    def __init__(self):
        settings = get_settings()
        self.base_url = settings.ollama_base_url.rstrip("/")
        self.model = settings.ollama_embedding_model
        self.batch_size = settings.embedding_batch_size
        self.timeout = settings.ollama_embedding_timeout
        self._dimension: int | None = None

    @property
    def dimension(self) -> int:
        if self._dimension is None:
            self.embed_query("dimension probe")
        return self._dimension or 768

    def _embed_batch(self, client: httpx.Client, texts: list[str]) -> list[list[float]]:
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
        return response.json()["embeddings"]

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        batches = list(iter_text_batches(texts, self.batch_size))
        all_embeddings: list[list[float]] = []

        with httpx.Client(timeout=self.timeout) as client:
            for index, batch in enumerate(batches, start=1):
                logger.info(
                    "ollama_embed_batch",
                    batch=index,
                    batch_count=len(batches),
                    texts_in_batch=len(batch),
                )
                batch_embeddings = self._embed_batch(client, batch)
                all_embeddings.extend(batch_embeddings)

        if all_embeddings and self._dimension is None:
            self._dimension = len(all_embeddings[0])
        return all_embeddings

    def embed_query(self, query: str) -> list[float]:
        return self.embed_texts([query])[0]
