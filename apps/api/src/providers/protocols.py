from typing import Protocol

from src.models.document import Chunk
from src.models.retrieval import RetrievedSource


class LLMProvider(Protocol):
    """Abstraction for text completion across Ollama, OpenAI, etc."""

    @property
    def provider_name(self) -> str: ...

    async def complete(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        json_mode: bool = False,
    ) -> str: ...


class EmbeddingProvider(Protocol):
    """Abstraction for embedding generation."""

    @property
    def provider_name(self) -> str: ...

    @property
    def dimension(self) -> int: ...

    async def embed_texts(self, texts: list[str]) -> list[list[float]]: ...


class VectorStore(Protocol):
    """Abstraction for vector persistence and search."""

    @property
    def provider_name(self) -> str: ...

    async def add_chunks(
        self,
        chunks: list[Chunk],
        embeddings: list[list[float]],
    ) -> None: ...

    async def search(
        self,
        query_embedding: list[float],
        *,
        top_k: int,
        document_ids: list[str] | None = None,
    ) -> list[RetrievedSource]: ...

    async def delete_by_document_id(self, document_id: str) -> int: ...

    async def count_chunks(self, document_id: str | None = None) -> int: ...
