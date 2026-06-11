# Privacy and Security

## Defaults

- Documents stored on the API host (`data/uploads` locally, `/app/data/uploads` on Render)
- Vectors stored in ChromaDB on the same host
- LLM inference via Ollama on the private Render service `consultationAI`
- No API keys in frontend

## Production (Render + Vercel)

- Document text for embeddings is sent to `consultationAI` when `EMBEDDING_PROVIDER=ollama`
- Chat/tribunal prompts are sent to the same private Ollama host when `LLM_PROVIDER=ollama`
- The Vercel UI never talks to Ollama directly—only to the Render API over HTTPS

## Hosted Providers

OpenAI requires explicit `LLM_PROVIDER=openai` and `OPENAI_API_KEY` in environment variables.

Document uploads do not use an LLM. They are chunked and embedded for vector search only.

Documents are not sent to hosted embedding APIs unless `EMBEDDING_PROVIDER=openai`. Use `local` or `ollama` to keep proprietary text on your infrastructure.

## Upload Security

- File type validation (PDF, MD, TXT, DOCX, HTML only)
- Size limit via `MAX_UPLOAD_SIZE_MB`
- Secrets never logged

## UI

Privacy banner displayed on every page.
