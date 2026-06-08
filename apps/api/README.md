# Hallucination Tribunal API

FastAPI backend for document ingestion, retrieval, and the Witness → Prosecutor → Judge tribunal pipeline.

## Development

```bash
uv sync --extra dev
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Tests

```bash
uv run pytest
```
