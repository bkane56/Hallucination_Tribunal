# Deployment Guide

Production uses a **split deploy**: FastAPI on **Render**, Next.js UI on **Vercel**, with **OpenAI** for LLM and embeddings by default.

| Service | Host | URL |
|---|---|---|
| Web UI | Vercel | `https://your-app.vercel.app` |
| API | Render (Docker) | `https://your-api.onrender.com` |
| LLM + embeddings | OpenAI API | Configured via `OPENAI_API_KEY` on Render |

```text
Browser → your-app.vercel.app (Next.js)
              │
              └── HTTPS → your-api.onrender.com (FastAPI)
                            │
                            └── HTTPS → api.openai.com (LLM + embeddings)
```

---

## Prerequisites

- GitHub repo connected to Render and Vercel
- [OpenAI API key](https://platform.openai.com/api-keys) for production LLM and embeddings
- [Vercel CLI](https://vercel.com/docs/cli) for UI deploys (optional)

---

## Step 1 — Deploy API on Render

### Option A: Blueprint (`render.yaml`)

1. In Render → **New** → **Blueprint** → connect `Hallucination_Tribunal`.
2. Set `OPENAI_API_KEY`, `FRONTEND_URL`, and `CORS_ALLOWED_ORIGINS` when prompted.
3. Confirm disk mount at `/app/data` (1 GB).

### Option B: Manual Web Service

| Setting | Value |
|---|---|
| **Root Directory** | `apps/api` |
| **Dockerfile Path** | `Dockerfile` |
| **Health check** | `/health` |
| **Disk mount** | `/app/data` (1 GB+) |

Copy environment variables from [`.env.render.example`](../.env.render.example).

### Smoke test

```bash
curl https://your-api.onrender.com/health
curl https://your-api.onrender.com/health/ready
```

`/health/ready` reports provider configuration and directory readiness. When using Ollama, it also reports `ollama_reachable`.

---

## Step 2 — Deploy UI on Vercel

1. Import the repo at [vercel.com/new](https://vercel.com/new).
2. **Root Directory** = repository root.
3. Add environment variable:

| Variable | Value |
|---|---|
| `NEXT_PUBLIC_BACKEND_URL` | `https://your-api.onrender.com` (no trailing slash) |

Copy from [`.env.vercel.example`](../.env.vercel.example).

**Do not set** `OLLAMA_*` or `OPENAI_*` on Vercel — those belong on the Render API only.

```bash
vercel login
vercel link
./scripts/deploy.sh vercel
```

---

## Step 3 — End-to-end test

1. Open your Vercel URL
2. **Corpus** → import sample documents
3. **Tribunal** → ask a question
4. Confirm Witness → Prosecutor → Judge completes

---

## Local development

```bash
cp .env.example .env
# Set OPENAI_API_KEY in .env
# Backend
cd apps/api && uv sync --extra dev && uv run uvicorn hallucination_tribunal.main:app --reload --port 8000
# Frontend
cd apps/web && yarn install && yarn dev
```

### Local Docker (API + web)

```bash
docker compose up --build
```

### Local Docker with Ollama (optional)

```bash
# Set LLM_PROVIDER=ollama and EMBEDDING_PROVIDER=ollama in .env
docker compose --profile ollama up --build
```

The API service uses `OLLAMA_BASE_URL=http://ollama:11434` inside Docker Compose so it can reach the Ollama container.

For a self-hosted API + Ollama stack without the web container:

```bash
./scripts/deploy.sh api
```

See [`docker-compose.prod.yml`](../docker-compose.prod.yml).

---

## Self-hosted / private LLM (Ollama)

To keep document text and inference off hosted APIs, set on the Render API (or local `.env`):

```bash
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama
OLLAMA_BASE_URL=http://consultationAI:11434   # Render private service hostname
OLLAMA_MODEL=llama3.2:1b
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
```

On Render, run a private Ollama service in the **same region** as the API and point `OLLAMA_BASE_URL` at its internal hostname. See [docs/privacy-and-security.md](privacy-and-security.md) for data-flow implications.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Render build: `COPY src` not found | Set **Root Directory** to `apps/api` or use `dockerContext` in `render.yaml` |
| `OPENAI_API_KEY is required` on startup | Set `OPENAI_API_KEY` on Render when `LLM_PROVIDER` or `EMBEDDING_PROVIDER` is `openai` |
| `ollama_reachable: false` on `/health/ready` | Only applies when a provider is `ollama`; check hostname and network |
| CORS errors in browser | Set `FRONTEND_URL` and `CORS_ALLOWED_ORIGINS` on Render API |
| UI calls `localhost:8000` in prod | Set `NEXT_PUBLIC_BACKEND_URL` on Vercel, redeploy |
| Evaluations fail: no test cases | Bundled cases seed on startup; confirm `/app/data/evals` on Render disk |
| Free tier cold start ~50s | First request after idle wakes the Render instance |
| Uploads vanish on Render | Attach disk at `/app/data` and set data path env vars |

---

## Legacy: Vercel all-in-one (serverless API)

The repo previously deployed web + API together via Vercel Services (`/server/*`). That path is deprecated. See [docs/legacy-vercel-deploy.md](legacy-vercel-deploy.md).

For local experimentation, run the API separately and set `NEXT_PUBLIC_BACKEND_URL`.

---

## Release checklist

- [ ] Render API **Root Directory** = `apps/api`, disk at `/app/data`
- [ ] Render env: `OPENAI_API_KEY`, `LLM_PROVIDER=openai`, `EMBEDDING_PROVIDER=openai`, CORS origins
- [ ] `GET /health` and `/health/ready` return 200
- [ ] Vercel `NEXT_PUBLIC_BACKEND_URL` = Render public URL
- [ ] Corpus import + tribunal question works end-to-end
