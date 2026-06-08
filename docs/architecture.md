# Architecture

## Overview

The Hallucination Tribunal is a monorepo with a FastAPI backend and Next.js frontend. Answers flow through a three-agent adversarial review pipeline (Witness → Prosecutor → Judge) over a controlled document corpus.

## Backend layers (Phase 1)

```text
apps/api/src/
  api/           HTTP routes and error handlers
  core/          Settings, logging, paths, dependencies
  models/        Pydantic schemas (documents, retrieval, tribunal)
  providers/     LLM, embedding, and vector-store abstractions
  documents/     Ingestion (Phase 2)
  retrieval/     Search (Phase 3)
  tribunal/      Agent pipeline and scoring (Phase 4)
  evaluations/   Quality metrics (Phase 6)
```

## Provider abstraction

Runtime providers are selected from environment configuration:

| Provider | Options | Implementation phase |
|----------|---------|----------------------|
| LLM | `ollama`, `openai` | Phase 4 |
| Embeddings | `local`, `openai` | Phase 2 |
| Vector DB | `chromadb` | Phase 2 |

In `APP_ENV=test`, stub providers are used automatically for unit tests.

## Data directories

Resolved relative to the monorepo root when `data/` exists locally, or relative to the API working directory in Docker:

- `data/uploads` — original uploaded files
- `data/chroma` — vector index persistence
- `data/seed` — seed evaluation documents
- `data/evals` — evaluation run results

## Health endpoints

- `GET /health` — liveness
- `GET /health/ready` — data directory readiness and configured providers

## Reliability scoring

Claim-level verdicts map to weights (Supported=1.0, Partially Supported=0.6, Not Enough Evidence=0.4, Unsupported/Contradicted=0.0). The overall reliability score is the mean across claims.

See `the_hallucination_tribunal_requirements.md` for the full target design.
