"""In-memory provider stubs for tests and local scaffolding."""

from src.models.document import Chunk
from src.models.retrieval import RetrievedSource
from src.providers.protocols import EmbeddingProvider, LLMProvider, VectorStore


class StubLLMProvider:
    provider_name = "stub"

    async def complete(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        json_mode: bool = False,
    ) -> str:
        _ = (system_prompt, json_mode)
        return f"stub-response:{user_prompt[:32]}"


class StubEmbeddingProvider:
    provider_name = "stub"
    dimension = 4

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [[float(index), 0.0, 0.0, 1.0] for index, _ in enumerate(texts)]


class InMemoryVectorStore:
    provider_name = "in_memory"

    def __init__(self) -> None:
        self._chunks: dict[str, Chunk] = {}
        self._embeddings: dict[str, list[float]] = {}

    async def add_chunks(
        self,
        chunks: list[Chunk],
        embeddings: list[list[float]],
    ) -> None:
        for chunk, embedding in zip(chunks, embeddings, strict=True):
            self._chunks[chunk.chunk_id] = chunk
            self._embeddings[chunk.chunk_id] = embedding

    async def search(
        self,
        query_embedding: list[float],
        *,
        top_k: int,
        document_ids: list[str] | None = None,
    ) -> list[RetrievedSource]:
        _ = query_embedding
        results: list[RetrievedSource] = []
        for chunk in self._chunks.values():
            if document_ids and chunk.document_id not in document_ids:
                continue
            results.append(
                RetrievedSource(
                    chunk_id=chunk.chunk_id,
                    document_id=chunk.document_id,
                    filename=chunk.metadata.get("filename", "unknown"),
                    page_number=chunk.source_page,
                    section_title=chunk.source_section,
                    text=chunk.text,
                    similarity_score=0.5,
                )
            )
        return results[:top_k]

    async def delete_by_document_id(self, document_id: str) -> int:
        to_delete = [
            chunk_id
            for chunk_id, chunk in self._chunks.items()
            if chunk.document_id == document_id
        ]
        for chunk_id in to_delete:
            del self._chunks[chunk_id]
            del self._embeddings[chunk_id]
        return len(to_delete)

    async def count_chunks(self, document_id: str | None = None) -> int:
        if document_id is None:
            return len(self._chunks)
        return sum(
            1 for chunk in self._chunks.values() if chunk.document_id == document_id
        )
