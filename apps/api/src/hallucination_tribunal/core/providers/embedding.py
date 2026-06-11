"""Embedding provider abstraction."""

from abc import ABC, abstractmethod
from collections.abc import Iterator


def iter_text_batches(texts: list[str], batch_size: int) -> Iterator[list[str]]:
    """Yield fixed-size batches of texts for embedding APIs."""
    size = max(1, batch_size)
    for start in range(0, len(texts), size):
        yield texts[start : start + size]


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
