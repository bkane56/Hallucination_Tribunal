# Privacy and Security

## Defaults

- Documents stored on the API host (`data/uploads` locally, `/app/data/uploads` on Render)
- Vectors stored in ChromaDB on the same host
- LLM and embeddings via **OpenAI** when `LLM_PROVIDER=openai` and `EMBEDDING_PROVIDER=openai`
- No API keys in frontend

## Production (Render + Vercel)

- Document chunks are sent to OpenAI when `EMBEDDING_PROVIDER=openai`
- Tribunal prompts are sent to OpenAI when `LLM_PROVIDER=openai`
- The Vercel UI never talks to OpenAI directly — only to the Render API over HTTPS
- Set `OPENAI_API_KEY` only on the Render API service

## Self-hosted providers

Use `ollama` or `local` providers to keep document text and inference on your infrastructure:

- **ollama**: document chunks and tribunal prompts go to your Ollama host
- **local**: embeddings run via sentence-transformers on the API host (requires optional `local-embeddings` install)

See [docs/deployment.md](deployment.md) for Ollama setup.

## Upload Security

- File type validation (PDF, MD, TXT, DOCX, HTML only)
- Size limit via `MAX_UPLOAD_SIZE_MB`
- Secrets never logged

## UI

Privacy banner displayed on every page.
