# RAG Design

## Chunking

- Recursive character splitting with configurable `CHUNK_SIZE` and `CHUNK_OVERLAP`
- Metadata preserved: document_id, filename, page, section

## Embeddings

- Default: `all-MiniLM-L6-v2` via sentence-transformers
- Swappable via `EMBEDDING_PROVIDER=openai`

## Retrieval

- **Vector**: ChromaDB cosine similarity
- **Hybrid**: Reciprocal rank fusion of vector + BM25 keyword scores
- Metadata filtering by document_id

## Grounding

All agent prompts enforce context-only answers with explicit uncertainty behavior.
