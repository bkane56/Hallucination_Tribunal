# Hallucination Tribunal API

FastAPI backend for document ingestion, hybrid retrieval, and the tribunal pipeline.

## Run locally

```bash
cd apps/api
uv sync --extra dev
uv run uvicorn hallucination_tribunal.main:app --reload --port 8000
```

Compatibility alias (same app):

```bash
uv run uvicorn src.main:app --reload --port 8000
```

## Tests

```bash
uv run pytest --cov=hallucination_tribunal --cov-report=term-missing
```

## Optional extras

```bash
uv sync --extra openai --extra local-embeddings
```

- `openai` — hosted LLM and embedding providers
- `local-embeddings` — sentence-transformers (falls back to hash embeddings when unavailable)
