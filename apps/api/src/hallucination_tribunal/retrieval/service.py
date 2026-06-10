"""Retrieval service with vector and hybrid search."""

from rank_bm25 import BM25Okapi

from hallucination_tribunal.core.config import get_settings
from hallucination_tribunal.core.db import get_database
from hallucination_tribunal.core.logging import get_logger
from hallucination_tribunal.core.providers.chroma_store import get_vector_store
from hallucination_tribunal.core.providers.local_embedding import get_embedding_provider
from hallucination_tribunal.models.domain import Chunk, RetrievedSource

logger = get_logger(__name__)


def reciprocal_rank_fusion(
    ranked_lists: list[list[str]],
    k: int = 60,
) -> list[tuple[str, float]]:
    scores: dict[str, float] = {}
    for ranked in ranked_lists:
        for rank, item_id in enumerate(ranked):
            scores[item_id] = scores.get(item_id, 0.0) + 1.0 / (k + rank + 1)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


class RetrievalService:
    def __init__(self):
        self.db = get_database()
        self.settings = get_settings()
        self.vector_store = get_vector_store()
        self.embedder = get_embedding_provider()

    async def retrieve(
        self,
        question: str,
        top_k: int | None = None,
        document_ids: list[str] | None = None,
    ) -> list[RetrievedSource]:
        top_k = top_k or self.settings.top_k_default
        mode = self.settings.retrieval_mode

        if mode == "hybrid":
            return await self._hybrid_retrieve(question, top_k, document_ids)
        return await self._vector_retrieve(question, top_k, document_ids)

    async def _vector_retrieve(
        self,
        question: str,
        top_k: int,
        document_ids: list[str] | None,
    ) -> list[RetrievedSource]:
        query_embedding = self.embedder.embed_query(question)
        results = self.vector_store.query(
            query_embedding, top_k=top_k, document_ids=document_ids
        )
        return await self._build_sources(results)

    async def _hybrid_retrieve(
        self,
        question: str,
        top_k: int,
        document_ids: list[str] | None,
    ) -> list[RetrievedSource]:
        vector_results = await self._vector_retrieve(
            question, top_k * 2, document_ids
        )
        vector_ranked = [s.chunk_id for s in vector_results]

        chunks = await self.db.get_all_chunks(document_ids)
        if not chunks:
            return vector_results[:top_k]

        bm25_ranked = self._bm25_search(question, chunks, top_k * 2)
        fused = reciprocal_rank_fusion([vector_ranked, bm25_ranked])
        fused_ids = [item_id for item_id, _ in fused[:top_k]]

        chunk_map = {c.chunk_id: c for c in chunks}
        doc_map = {
            d.document_id: d
            for d in await self.db.list_documents()
        }
        vector_score_map = {s.chunk_id: s.similarity_score for s in vector_results}

        sources: list[RetrievedSource] = []
        for chunk_id in fused_ids:
            chunk = chunk_map.get(chunk_id)
            if not chunk:
                continue
            doc = doc_map.get(chunk.document_id)
            sources.append(
                RetrievedSource(
                    chunk_id=chunk.chunk_id,
                    document_id=chunk.document_id,
                    filename=doc.filename if doc else "unknown",
                    page_number=chunk.source_page,
                    section_title=chunk.source_section,
                    text=chunk.text,
                    similarity_score=vector_score_map.get(chunk_id, 0.5),
                )
            )
        return sources

    def _bm25_search(
        self, question: str, chunks: list[Chunk], top_k: int
    ) -> list[str]:
        if not chunks:
            return []
        corpus = [c.text.split() for c in chunks]
        bm25 = BM25Okapi(corpus)
        scores = bm25.get_scores(question.split())
        ranked_indices = sorted(
            range(len(scores)), key=lambda i: scores[i], reverse=True
        )[:top_k]
        return [chunks[i].chunk_id for i in ranked_indices]

    async def _build_sources(
        self, results: list[tuple[str, float, dict]]
    ) -> list[RetrievedSource]:
        sources: list[RetrievedSource] = []
        docs = {d.document_id: d for d in await self.db.list_documents()}

        for chunk_id, score, metadata in results:
            chunks = await self.db.get_all_chunks()
            chunk_map = {c.chunk_id: c for c in chunks}
            chunk = chunk_map.get(chunk_id)
            if not chunk:
                continue
            doc = docs.get(chunk.document_id)
            sources.append(
                RetrievedSource(
                    chunk_id=chunk_id,
                    document_id=chunk.document_id,
                    filename=doc.filename if doc else metadata.get("filename", "unknown"),
                    page_number=chunk.source_page,
                    section_title=chunk.source_section,
                    text=chunk.text,
                    similarity_score=score,
                )
            )
        return sources
