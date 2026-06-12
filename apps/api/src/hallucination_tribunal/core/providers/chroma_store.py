"""ChromaDB vector store for local/Docker deployments."""

from typing import Any

import chromadb
from chromadb.config import Settings as ChromaSettings

from hallucination_tribunal.core.config import get_settings
from hallucination_tribunal.core.logging import get_logger
from hallucination_tribunal.core.providers.memory_vector_store import InMemoryVectorStore
from hallucination_tribunal.core.providers.vector_store import VectorStore
from hallucination_tribunal.models.domain import Chunk

COLLECTION_NAME = "tribunal_chunks"
logger = get_logger(__name__)


class ChromaVectorStore(VectorStore):
    def __init__(self):
        settings = get_settings()
        persist_dir = str(settings.resolve_path(settings.chroma_persist_directory))
        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )

    def count(self) -> int:
        return self.collection.count()

    def upsert_chunks(
        self,
        chunks: list[Chunk],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]],
    ) -> None:
        if not chunks:
            return
        ids = [c.chunk_id for c in chunks]
        documents = [c.text for c in chunks]
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

    def delete_by_document_id(self, document_id: str) -> None:
        try:
            self.collection.delete(where={"document_id": document_id})
        except Exception as exc:
            logger.warning("chroma_delete_failed", document_id=document_id, error=str(exc))

    def query(
        self,
        query_embedding: list[float],
        top_k: int = 6,
        document_ids: list[str] | None = None,
    ) -> list[tuple[str, float, dict[str, Any]]]:
        where: dict[str, Any] | None = None
        if document_ids:
            if len(document_ids) == 1:
                where = {"document_id": document_ids[0]}
            else:
                where = {"document_id": {"$in": document_ids}}

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where,
            include=["metadatas", "distances"],
        )

        output: list[tuple[str, float, dict[str, Any]]] = []
        if not results["ids"] or not results["ids"][0]:
            return output

        for chunk_id, distance, metadata in zip(
            results["ids"][0],
            results["distances"][0] or [],
            results["metadatas"][0] or [],
        ):
            similarity = 1.0 - (distance or 0.0)
            output.append((chunk_id, similarity, metadata or {}))
        return output

    def clear(self) -> None:
        try:
            self.client.delete_collection(COLLECTION_NAME)
        except Exception as exc:
            logger.warning("chroma_clear_failed", error=str(exc))
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )


_vector_store: VectorStore | None = None


def get_vector_store() -> VectorStore:
    global _vector_store
    if _vector_store is None:
        settings = get_settings()
        if settings.is_serverless:
            _vector_store = InMemoryVectorStore()
        else:
            _vector_store = ChromaVectorStore()
    return _vector_store


def reset_vector_store() -> None:
    global _vector_store
    _vector_store = None
