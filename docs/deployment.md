# Deployment Guide

Production uses a **split deploy**: FastAPI on **Render**, Next.js UI on **Vercel**, Ollama on the private Render service **consultationAI**.

| Service | Host | URL |
|---|---|---|
| Web UI | Vercel | `https://your-app.vercel.app` |
| API | Render (Docker) | `https://your-api.onrender.com` |
| LLM + embeddings | Render private service | `http://consultationAI:11434` (internal only) |

```text
Browser → your-app.vercel.app (Next.js)
              │
              └── HTTPS → your-api.onrender.com (FastAPI)
                            │
                            └── HTTP → consultationAI:11434 (Ollama)
```

---

## Prerequisites

- GitHub repo connected to Render and Vercel
- Private Ollama service `consultationAI` in the **same Render region** as the API
- Models on Ollama: `llama3.2:1b` (chat), `nomic-embed-text` (embeddings)
- [Vercel CLI](https://vercel.com/docs/cli) for UI deploys (optional)

---

## Step 1 — Deploy API on Render

### Option A: Blueprint (`render.yaml`)

1. In Render → **New** → **Blueprint** → connect `Hallucination_Tribunal`.
2. Set `FRONTEND_URL` and `CORS_ALLOWED_ORIGINS` to your Vercel URL when prompted.
3. Confirm disk mount at `/app/data` (1 GB).

### Option B: Manual Web Service

| Setting | Value |
|---|---|
| **Root Directory** | `apps/api` |
| **Dockerfile Path** | `Dockerfile` |
| **Health check** | `/health` |
| **Disk mount** | `/app/data` (1 GB+) |
| **Region** | Same as `consultationAI` |

Copy environment variables from [`.env.render.example`](../.env.render.example).

**Important:** `OLLAMA_BASE_URL=http://consultationAI:11434` only works from Render services on the private network—not from Vercel or your laptop.

### Smoke test

```bash
curl https://your-api.onrender.com/health
curl https://your-api.onrender.com/health/ready
```

`/health/ready` reports `ollama_reachable` when the API can reach `consultationAI`.

---

## Step 2 — Deploy UI on Vercel

1. Import the repo at [vercel.com/new](https://vercel.com/new).
2. **Root Directory** = repository root.
3. Add environment variable:

| Variable | Value |
|---|---|
| `NEXT_PUBLIC_BACKEND_URL` | `https://your-api.onrender.com` (no trailing slash) |

Copy from [`.env.vercel.example`](../.env.vercel.example).

**Do not set** `NEXT_PUBLIC_API_ROUTE_PREFIX`, `API_ROOT_PATH`, or `OLLAMA_*` on Vercel.

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
# Backend
cd apps/api && uv sync --extra dev && uv run uvicorn hallucination_tribunal.main:app --reload --port 8000
# Frontend
cd apps/web && yarn install && yarn dev
```

Local Ollama: `OLLAMA_BASE_URL=http://localhost:11434`

### Local Docker (API + Ollama)

```bash
./scripts/deploy.sh api
```

See [`docker-compose.prod.yml`](../docker-compose.prod.yml).

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Render build: `COPY src` not found | Set **Root Directory** to `apps/api` or use `dockerContext` in `render.yaml` |
| Render crash: `IndexError` in `config.py` | Fixed: monorepo path detection walks parents safely in Docker |
| `ollama_reachable: false` on `/health/ready` | API not in same region/network as `consultationAI`; check hostname casing |
| CORS errors in browser | Set `FRONTEND_URL` and `CORS_ALLOWED_ORIGINS` on Render API |
| UI calls `localhost:8000` in prod | Set `NEXT_PUBLIC_BACKEND_URL` on Vercel, redeploy |
| Free tier cold start ~50s | First request after idle wakes the Render instance |
| Uploads vanish on Render | Attach disk at `/app/data` and set data path env vars |

---

## Legacy: Vercel all-in-one (serverless API)

The repo previously deployed web + API together via Vercel Services (`/server/*`). That path is deprecated for production because:

- Vercel cannot reach private `consultationAI`
- Serverless `/tmp` storage is ephemeral
- Tribunal runs can hit serverless timeouts

For local experimentation with `vercel dev`, run the API separately (`uvicorn` or Render) and set `NEXT_PUBLIC_BACKEND_URL`.

---

## Release checklist

- [ ] Render API **Root Directory** = `apps/api`, disk at `/app/data`
- [ ] Render env: `OLLAMA_BASE_URL=http://consultationAI:11434`, models, data paths, CORS
- [ ] `GET /health` and `/health/ready` return 200 with `ollama_reachable: true`
- [ ] Vercel `NEXT_PUBLIC_BACKEND_URL` = Render public URL
- [ ] Corpus import + tribunal question works end-to-end
