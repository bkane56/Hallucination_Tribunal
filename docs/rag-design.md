# RAG Design

## Chunking

- Recursive character splitting with configurable `CHUNK_SIZE` and `CHUNK_OVERLAP`
- Metadata preserved: document_id, filename, page, section

## Embeddings

Upload and retrieval use embeddings only (no LLM). Document text is chunked and vectorized for search.

- **local** (default for local dev): `all-MiniLM-L6-v2` via sentence-transformers — runs on your machine
- **ollama** (recommended for Render production): embedding model on `consultationAI` (e.g. `nomic-embed-text`)
- **openai** (opt-in): `text-embedding-3-small` via OpenAI API — requires `OPENAI_API_KEY`; document chunks are sent to OpenAI

## Retrieval

- **Vector**: ChromaDB cosine similarity
- **Hybrid**: Reciprocal rank fusion of vector + BM25 keyword scores
- Metadata filtering by document_id

## Grounding

All agent prompts enforce context-only answers with explicit uncertainty behavior.
