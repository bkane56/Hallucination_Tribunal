# Deployment Guide (Vercel)

Deploy the **Next.js UI and FastAPI API together on Vercel** using [Vercel Services](https://vercel.com/docs/services). Point the API at your existing Ollama endpoint via `OLLAMA_BASE_URL`.

| Service | Route | Runtime |
|---|---|---|
| Web UI | `/` | Next.js |
| API | `/server/*` | Python / FastAPI |

```text
Browser → your-app.vercel.app
            ├── /              Next.js UI
            └── /server/*      FastAPI (documents, tribunal, evaluations)
                      │
                      └── HTTP → OLLAMA_BASE_URL (your Ollama host)
```

> **Note:** Vercel runs the API as serverless functions, not as a Docker container. Ollama itself must be reachable at a **public URL** you configure in `OLLAMA_BASE_URL` — that can be a tunnel to your local machine, a VPS, or any host running Ollama. Vercel functions call it over HTTP; they do not run the Ollama binary.

---

## Prerequisites

- GitHub repo connected to Vercel
- [Vercel CLI](https://vercel.com/docs/cli): `npm i -g vercel`
- **Services** enabled on your Vercel team (required for multi-service projects)
- A reachable Ollama URL with `llama3.1:8b` (or your chosen model) available
- OpenAI API key (recommended on Vercel for embeddings — avoids bundling torch/sentence-transformers)

---

## Step 1 — Create the Vercel project

1. Go to [vercel.com/new](https://vercel.com/new) and import `Hallucination_Tribunal`.
2. Set **Root Directory** to the **repository root** (not `apps/web`).
3. Set **Framework Preset** to **Services** (required when `experimentalServices` is in `vercel.json`).
4. Deploy once to confirm the project links correctly.

The repo root [`vercel.json`](../vercel.json) defines both services:

```json
{
  "experimentalServices": {
    "web": { "entrypoint": "apps/web", "routePrefix": "/" },
    "api": { "entrypoint": "apps/api/src/hallucination_tribunal/main.py", "routePrefix": "/server" }
  }
}
```

---

## Step 2 — Environment variables

In **Vercel → Project → Settings → Environment Variables**, add:

### Web (Next.js)

| Variable | Value |
|---|---|
| `NEXT_PUBLIC_API_ROUTE_PREFIX` | `/server` |

Do **not** set `NEXT_PUBLIC_BACKEND_URL` unless you want a separate API host. Leaving it unset makes the UI call same-origin `/server/*` routes.

### API + shared

| Variable | Value |
|---|---|
| `APP_ENV` | `production` |
| `API_ROOT_PATH` | `/server` |
| `FRONTEND_URL` | `https://your-app.vercel.app` |
| `LLM_PROVIDER` | `ollama` |
| `OLLAMA_BASE_URL` | Your Ollama URL, e.g. `https://ollama.example.com` |
| `OLLAMA_MODEL` | `llama3.1:8b` |
| `EMBEDDING_PROVIDER` | `openai` |
| `OPENAI_API_KEY` | Your OpenAI key |
| `OPENAI_EMBEDDING_MODEL` | `text-embedding-3-small` |

Copy the full template from [`.env.vercel.example`](../.env.vercel.example).

Data paths (`/tmp/hallucination-tribunal/*`) are configured automatically when `VERCEL` is detected. Uploads and the vector index are **ephemeral** on serverless — fine for demos; use Docker locally or add external storage for durable production data.

---

## Step 3 — Deploy

```bash
vercel login
vercel link          # once, from repo root
./scripts/deploy.sh vercel
```

Preview deploys:

```bash
./scripts/deploy.sh vercel:preview
```

Local multi-service dev (web + API together):

```bash
./scripts/deploy.sh dev
# equivalent: vercel dev -L
```

---

## Step 4 — Smoke test

```bash
curl https://your-app.vercel.app/server/health
```

Then in the browser:

1. Open your Vercel URL
2. **Corpus** → import sample documents
3. **Tribunal** → ask a question
4. Confirm the Witness → Prosecutor → Judge pipeline completes

---

## Ollama connectivity

Your Ollama host must accept requests from Vercel's serverless network:

- Set `OLLAMA_ORIGINS` or reverse-proxy auth if needed
- Use HTTPS for public endpoints
- Ensure the model is pulled: `ollama pull llama3.1:8b`

If Ollama runs on your laptop, expose it with [Tailscale Funnel](https://tailscale.com/kb/1242/tailscale-funnel) or [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/) and set `OLLAMA_BASE_URL` to that URL.

---

## Limits to know

| Topic | Vercel behavior |
|---|---|
| Tribunal timeout | Up to 300s on Pro (`maxDuration` in `vercel.json`) |
| Bundle size | Python function max ~500 MB — use OpenAI embeddings, not local sentence-transformers |
| Persistence | `/tmp` storage resets between cold starts — demo/portfolio use |
| Ollama | External HTTP endpoint only — not run inside Vercel functions |

---

## Optional: local Docker stack

If you prefer running API + Ollama in Docker locally (not on Vercel):

```bash
./scripts/deploy.sh api
```

See [`docker-compose.prod.yml`](../docker-compose.prod.yml).

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| 404 on `/server/health` | Confirm Framework Preset is **Services** and root `vercel.json` is deployed |
| UI calls `localhost:8000` in prod | Set `NEXT_PUBLIC_API_ROUTE_PREFIX=/server`, redeploy web |
| Ollama model not found | Pull model on Ollama host; verify `OLLAMA_MODEL` matches `ollama list` |
| Build exceeds size limit | Use `EMBEDDING_PROVIDER=openai`; do not install `[local-embeddings]` |
| CORS errors | Same-origin `/server` routes should not need CORS; check `FRONTEND_URL` if using split deploy |
| Uploads vanish | Expected on serverless `/tmp` — use Docker locally for persistent data |

---

## Release checklist

- [ ] Vercel project root = repo root, Framework = **Services**
- [ ] `NEXT_PUBLIC_API_ROUTE_PREFIX=/server`
- [ ] `OLLAMA_BASE_URL` reachable from the public internet
- [ ] `OPENAI_API_KEY` set (embeddings)
- [ ] `GET /server/health` returns 200
- [ ] Sample import + tribunal question works end-to-end
