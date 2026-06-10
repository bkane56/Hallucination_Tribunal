"""Local sentence-transformers embedding provider."""

from functools import lru_cache

from hallucination_tribunal.core.config import get_settings
from hallucination_tribunal.core.providers.embedding import EmbeddingProvider


class LocalEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model_name: str | None = None):
        settings = get_settings()
        self.model_name = model_name or settings.local_embedding_model
        self._model = None
        self._dimension: int | None = None

    @property
    def model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_name)
            self._dimension = self._model.get_sentence_embedding_dimension()
        return self._model

    @property
    def dimension(self) -> int:
        if self._dimension is None:
            _ = self.model
        return self._dimension or 384

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return [emb.tolist() for emb in embeddings]

    def embed_query(self, query: str) -> list[float]:
        return self.embed_texts([query])[0]


class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self):
        settings = get_settings()
        self.model = settings.openai_embedding_model
        self._dimension = 1536

    @property
    def dimension(self) -> int:
        return self._dimension

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        from openai import OpenAI

        settings = get_settings()
        client = OpenAI(api_key=settings.openai_api_key)
        response = client.embeddings.create(input=texts, model=self.model)
        return [item.embedding for item in response.data]

    def embed_query(self, query: str) -> list[float]:
        return self.embed_texts([query])[0]


@lru_cache
def get_embedding_provider() -> EmbeddingProvider:
    settings = get_settings()
    if settings.embedding_provider == "ollama":
        from hallucination_tribunal.core.providers.ollama_embedding import (
            OllamaEmbeddingProvider,
        )

        return OllamaEmbeddingProvider()
    if settings.embedding_provider == "openai":
        return OpenAIEmbeddingProvider()
    try:
        import sentence_transformers  # noqa: F401

        return LocalEmbeddingProvider()
    except Exception:
        from hallucination_tribunal.core.providers.simple_embedding import (
            SimpleEmbeddingProvider,
        )

        return SimpleEmbeddingProvider()
