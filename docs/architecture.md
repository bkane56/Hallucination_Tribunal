# Architecture

See the system diagram in the Architecture page of the web app.

## Components

- **apps/web** — Next.js frontend with courtroom-themed UI
- **apps/api** — FastAPI backend with tribunal orchestration
- **data/uploads** — Original uploaded files
- **data/chroma** — ChromaDB persistence
- **data/evals** — Evaluation test cases
- **data/seed** — Demo policy documents

## Production deployment

```text
Browser
   └── Vercel (Next.js) ──HTTPS──► Render (FastAPI, /app/data disk)
                                        └── HTTPS ──► OpenAI (LLM + embeddings)
```

- UI calls the Render API via `NEXT_PUBLIC_BACKEND_URL` (cross-origin; CORS on API).
- API uses OpenAI for chat and embeddings by default (`LLM_PROVIDER=openai`, `EMBEDDING_PROVIDER=openai`).
- SQLite, ChromaDB, and uploads persist on Render disk at `/app/data`.
- Optional self-hosted path: set providers to `ollama` and point `OLLAMA_BASE_URL` at a private Ollama service.

## Data Flow

1. Documents are extracted, chunked, embedded, and stored in ChromaDB + SQLite
2. Questions trigger hybrid retrieval
3. Tribunal pipeline runs five LLM stages with structured outputs
4. Results persist to SQLite for replay and evaluation
