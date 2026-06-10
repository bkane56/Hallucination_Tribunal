"""In-memory vector store for serverless runtimes (no Chroma/SQLite file locks)."""

from typing import Any

import numpy as np

from hallucination_tribunal.core.providers.vector_store import VectorStore
from hallucination_tribunal.models.domain import Chunk


class InMemoryVectorStore(VectorStore):
    def __init__(self):
        self._ids: list[str] = []
        self._embeddings: np.ndarray | None = None
        self._metadatas: list[dict[str, Any]] = []
        self._id_to_index: dict[str, int] = {}

    def count(self) -> int:
        return len(self._ids)

    def upsert_chunks(
        self,
        chunks: list[Chunk],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]],
    ) -> None:
        if not chunks:
            return

        for chunk, embedding, metadata in zip(chunks, embeddings, metadatas):
            vector = np.asarray(embedding, dtype=np.float32)
            index = self._id_to_index.get(chunk.chunk_id)
            if index is None:
                index = len(self._ids)
                self._id_to_index[chunk.chunk_id] = index
                self._ids.append(chunk.chunk_id)
                self._metadatas.append(metadata)
                if self._embeddings is None:
                    self._embeddings = vector.reshape(1, -1)
                else:
                    self._embeddings = np.vstack([self._embeddings, vector.reshape(1, -1)])
            else:
                self._embeddings[index] = vector
                self._metadatas[index] = metadata

    def delete_by_document_id(self, document_id: str) -> None:
        keep_indices = [
            i
            for i, metadata in enumerate(self._metadatas)
            if metadata.get("document_id") != document_id
        ]
        if len(keep_indices) == len(self._ids):
            return

        self._ids = [self._ids[i] for i in keep_indices]
        self._metadatas = [self._metadatas[i] for i in keep_indices]
        if self._embeddings is not None and keep_indices:
            self._embeddings = self._embeddings[keep_indices]
        else:
            self._embeddings = None
        self._id_to_index = {chunk_id: idx for idx, chunk_id in enumerate(self._ids)}

    def query(
        self,
        query_embedding: list[float],
        top_k: int = 6,
        document_ids: list[str] | None = None,
    ) -> list[tuple[str, float, dict[str, Any]]]:
        if self._embeddings is None or not self._ids:
            return []

        query = np.asarray(query_embedding, dtype=np.float32)
        query_norm = np.linalg.norm(query) or 1.0
        query = query / query_norm

        matrix_norms = np.linalg.norm(self._embeddings, axis=1)
        matrix_norms = np.where(matrix_norms == 0, 1.0, matrix_norms)
        similarities = (self._embeddings / matrix_norms[:, None]) @ query

        allowed = set(document_ids) if document_ids else None
        ranked: list[tuple[str, float, dict[str, Any]]] = []
        for index, chunk_id in enumerate(self._ids):
            metadata = self._metadatas[index]
            if allowed is not None and metadata.get("document_id") not in allowed:
                continue
            ranked.append((chunk_id, float(similarities[index]), metadata))

        ranked.sort(key=lambda item: item[1], reverse=True)
        return ranked[:top_k]

    def clear(self) -> None:
        self._ids = []
        self._embeddings = None
        self._metadatas = []
        self._id_to_index = {}
