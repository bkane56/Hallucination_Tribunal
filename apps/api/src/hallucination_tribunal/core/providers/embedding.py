"""Embedding provider abstraction."""

from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of texts."""

    @abstractmethod
    def embed_query(self, query: str) -> list[float]:
        """Embed a single query."""

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Embedding vector dimension."""
