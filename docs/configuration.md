# Configuration Reference

Environment variables for the Hallucination Tribunal monorepo. Copy [`.env.example`](../.env.example) for local development.

## API (`apps/api`)

| Variable | Default | Local | Render | Description |
|---|---|---|---|---|
| `APP_ENV` | `development` | yes | yes | `development` or `production` |
| `FRONTEND_URL` | `http://localhost:3000` | yes | yes | Primary UI origin for CORS |
| `CORS_ALLOWED_ORIGINS` | (empty) | optional | yes | Comma-separated extra allowed origins |
| `API_ROOT_PATH` | (empty) | optional | no | ASGI root path (legacy Vercel mount) |
| `STORAGE_ROOT` | (empty) | optional | no | Writable root on serverless hosts |
| `LLM_PROVIDER` | `openai` | yes | yes | `openai` or `ollama` |
| `EMBEDDING_PROVIDER` | `openai` | yes | yes | `openai`, `ollama`, or `local` |
| `OPENAI_API_KEY` | (required when OpenAI) | yes | yes | OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o-mini` | yes | yes | Chat model |
| `OPENAI_EMBEDDING_MODEL` | `text-embedding-3-small` | yes | yes | Embedding model |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | optional | optional | Ollama host (use `http://ollama:11434` in Docker Compose) |
| `OLLAMA_MODEL` | `llama3.1:8b` | optional | optional | Ollama chat model |
| `OLLAMA_EMBEDDING_MODEL` | `nomic-embed-text` | optional | optional | Ollama embedding model |
| `LOCAL_EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | optional | no | sentence-transformers model |
| `VECTOR_DB_PROVIDER` | `chromadb` | yes | yes | Vector store backend |
| `CHROMA_PERSIST_DIRECTORY` | `./data/chroma` | yes | `/app/data/chroma` | Chroma persistence path |
| `SQLITE_DATABASE_PATH` | `./data/tribunal.db` | yes | `/app/data/tribunal.db` | SQLite path |
| `UPLOAD_DIRECTORY` | `./data/uploads` | yes | `/app/data/uploads` | Uploaded files |
| `SEED_DIRECTORY` | `./data/seed` | yes | `/app/data/seed` | Seed documents directory |
| `EVALS_DIRECTORY` | `./data/evals` | yes | `/app/data/evals` | Evaluation test cases |
| `MAX_UPLOAD_SIZE_MB` | `25` | yes | optional | Upload size limit |
| `CHUNK_SIZE` | `900` | yes | optional | Chunk character size |
| `CHUNK_OVERLAP` | `150` | yes | optional | Chunk overlap |
| `TOP_K_DEFAULT` | `6` | yes | optional | Default retrieval top-k |
| `RETRIEVAL_MODE` | `hybrid` | yes | yes | `vector` or `hybrid` |
| `EMBEDDING_BATCH_SIZE` | `16` | yes | optional | Embedding batch size |
| `OLLAMA_EMBEDDING_TIMEOUT` | `90` | optional | optional | Ollama embed timeout (seconds) |
| `OLLAMA_LLM_TIMEOUT` | `180` | optional | optional | Ollama LLM timeout (seconds) |
| `OLLAMA_KEEP_ALIVE` | `10m` | optional | optional | Ollama keep-alive |
| `LOG_LEVEL` | `info` | yes | yes | Logging level |

Render production template: [`.env.render.example`](../.env.render.example). Deploy guide: [deployment.md](deployment.md).

## Web (`apps/web`)

| Variable | Default | Local | Vercel | Description |
|---|---|---|---|---|
| `NEXT_PUBLIC_BACKEND_URL` | `http://localhost:8000` | yes | yes | Render API public URL |
| `NEXT_PUBLIC_API_ROUTE_PREFIX` | (empty) | optional | no | Legacy same-origin API prefix |

Vercel template: [`.env.vercel.example`](../.env.vercel.example).

## Tests

Run backend tests from `apps/api`:

```bash
cd apps/api && uv run pytest
```

Running pytest from the repository root creates a stray `.pytest_cache/` at the root.
