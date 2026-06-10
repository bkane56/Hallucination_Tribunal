"""Simple hash-based embedding fallback when sentence-transformers is unavailable."""

import hashlib
import math
import struct

from hallucination_tribunal.core.providers.embedding import EmbeddingProvider


class SimpleEmbeddingProvider(EmbeddingProvider):
    """Deterministic lightweight embeddings for local dev and CI."""

    def __init__(self, dimension: int = 384):
        self._dimension = dimension

    @property
    def dimension(self) -> int:
        return self._dimension

    def _embed_one(self, text: str) -> list[float]:
        vector = [0.0] * self._dimension
        tokens = text.lower().split()
        for token in tokens:
            digest = hashlib.sha256(token.encode()).digest()
            for i in range(0, min(len(digest), self._dimension), 4):
                value = struct.unpack(">I", digest[i : i + 4])[0]
                idx = value % self._dimension
                vector[idx] += (value % 1000) / 1000.0
        if not tokens:
            vector[0] = 1.0
        norm = math.sqrt(sum(v * v for v in vector)) or 1.0
        return [v / norm for v in vector]

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_one(text) for text in texts]

    def embed_query(self, query: str) -> list[float]:
        return self._embed_one(query)
