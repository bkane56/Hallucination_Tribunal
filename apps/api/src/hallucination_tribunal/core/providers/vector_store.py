"""Vector store abstraction."""

from abc import ABC, abstractmethod
from typing import Any

from hallucination_tribunal.models.domain import Chunk


class VectorStore(ABC):
    @abstractmethod
    def upsert_chunks(
        self,
        chunks: list[Chunk],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]],
    ) -> None:
        """Insert or update chunks with embeddings."""

    @abstractmethod
    def delete_by_document_id(self, document_id: str) -> None:
        """Delete all chunks for a document."""

    @abstractmethod
    def query(
        self,
        query_embedding: list[float],
        top_k: int = 6,
        document_ids: list[str] | None = None,
    ) -> list[tuple[str, float, dict[str, Any]]]:
        """Return (chunk_id, score, metadata) tuples."""

    @abstractmethod
    def clear(self) -> None:
        """Clear all vectors."""
