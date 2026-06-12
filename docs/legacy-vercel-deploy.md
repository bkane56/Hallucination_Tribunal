# Legacy: Vercel All-in-One Deploy

This repository previously deployed the FastAPI API on Vercel alongside the Next.js UI using **Vercel Services** with the API mounted at `/server/*`. That **API-on-Vercel** path is deprecated.

## Current Vercel UI deploy

Production UI still uses Vercel **Services** framework when the project is configured that way in the Vercel dashboard. Root [`vercel.json`](../vercel.json) declares a **web-only** service:

- `entrypoint`: `apps/web` (Next.js)
- No API service — the Render API handles LLM/RAG via `NEXT_PUBLIC_BACKEND_URL`

To migrate off Services framework entirely, set Vercel **Root Directory** to `apps/web`, **Framework** to Next.js, and remove `vercel.json` from the repo root.

## Why the old all-in-one path was removed

- Vercel cannot reach private Ollama hosts
- Serverless `/tmp` storage is ephemeral
- Tribunal runs can hit serverless timeouts

For local experimentation, run the API separately and set `NEXT_PUBLIC_BACKEND_URL`.
