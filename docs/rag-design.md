# RAG Design

## Chunking

- Recursive character splitting with configurable `CHUNK_SIZE` and `CHUNK_OVERLAP`
- Token estimates via `tiktoken` when available
- Metadata preserved: document_id, filename, page, section

## Embeddings

Upload and retrieval use embeddings only (no LLM). Document text is chunked and vectorized for search.

- **openai** (default): `text-embedding-3-small` via OpenAI API — requires `OPENAI_API_KEY`; document chunks are sent to OpenAI
- **local**: `all-MiniLM-L6-v2` via sentence-transformers — runs on the API host; requires optional `local-embeddings` extra
- **ollama**: embedding model on your Ollama host (e.g. `nomic-embed-text`)

## Retrieval

- **Vector**: ChromaDB cosine similarity
- **Hybrid**: Reciprocal rank fusion of vector + BM25 keyword scores
- Metadata filtering by document_id

## Grounding

All agent prompts enforce context-only answers with explicit uncertainty behavior.
