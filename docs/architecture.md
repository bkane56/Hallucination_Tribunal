# Architecture

See the system diagram in the Architecture page of the web app.

## Components

- **apps/web** — Next.js frontend with courtroom-themed UI
- **apps/api** — FastAPI backend with tribunal orchestration
- **data/uploads** — Original uploaded files
- **data/chroma** — ChromaDB persistence
- **data/evals** — Evaluation test cases
- **data/seed** — Demo policy documents

## Data Flow

1. Documents are extracted, chunked, embedded, and stored in ChromaDB + SQLite
2. Questions trigger hybrid retrieval
3. Tribunal pipeline runs five LLM stages with structured outputs
4. Results persist to SQLite for replay and evaluation
