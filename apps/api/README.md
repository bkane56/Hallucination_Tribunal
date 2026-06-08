# Hallucination Tribunal API

FastAPI backend for document ingestion, retrieval, and the Witness → Prosecutor → Judge tribunal pipeline.

## Phase 1 — Backend foundation

- Pydantic models for documents, retrieval, and tribunal results
- Structured logging and global error handling
- Provider protocols for LLM, embeddings, and vector storage
- Data directory bootstrap on startup
- `GET /health` and `GET /health/ready`

## Development

```bash
uv sync --extra dev
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Tests

```bash
uv run pytest
```
