# The Hallucination Tribunal

RAG-powered AI application that answers questions from a controlled document corpus, then subjects each answer to an adversarial review by Witness, Prosecutor, and Judge agents.

## Monorepo layout

```text
apps/
  api/    FastAPI backend (uv)
  web/    Next.js frontend (yarn)
data/     Local uploads, Chroma vectors, eval datasets
docs/     Architecture and design documentation
```

## Prerequisites

- [uv](https://docs.astral.sh/uv/) for the Python backend
- [yarn](https://yarnpkg.com/) for the Next.js frontend
- Optional: [Ollama](https://ollama.com/) for local LLM inference (Phase 4+)

## Quick start

1. Copy environment variables:

```bash
cp .env.example .env
```

2. Start the API:

```bash
cd apps/api
uv sync --extra dev
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

3. Start the web app (separate terminal):

```bash
cd apps/web
yarn install
yarn dev
```

4. Open [http://localhost:3000](http://localhost:3000). The home page reports API health from `GET /health`.

## Docker

```bash
docker compose up --build
```

## Implementation status

| Phase | Status |
|-------|--------|
| 0 — Monorepo scaffold | Complete |
| 1 — Backend foundation | Complete |
| 2 — Document ingestion | Planned |
| 3 — Retrieval | Planned |
| 4 — Tribunal pipeline | Planned |
| 5 — Frontend pages | Planned |
| 6 — Evaluation | Planned |
| 7 — Testing (≥90% coverage) | Planned |
| 8 — Docs and Docker polish | Planned |

See `the_hallucination_tribunal_requirements.md` for full specifications.
