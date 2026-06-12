# Legacy: Vercel All-in-One Deploy

This repository previously supported deploying the Next.js UI and FastAPI API together on Vercel using **Vercel Services** (`experimentalServices` in `vercel.json`) with the API mounted at `/server/*`.

That path is **deprecated** because:

- Vercel serverless functions cannot reach private Render/Ollama hosts
- `/tmp` storage is ephemeral on serverless
- Tribunal runs can exceed serverless timeouts

## Current production model

- **UI**: Vercel with `NEXT_PUBLIC_BACKEND_URL` pointing at Render
- **API**: Render Docker service (see [deployment.md](deployment.md))

## Local development

Run the API locally or on Render and set `NEXT_PUBLIC_BACKEND_URL` in the web app. Do not rely on same-origin `/server` routing.
