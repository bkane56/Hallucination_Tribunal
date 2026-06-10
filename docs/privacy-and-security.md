# Privacy and Security

## Defaults

- Documents stored locally in `data/uploads`
- Vectors stored locally in ChromaDB
- LLM inference via Ollama (local)
- No API keys in frontend

## Hosted Providers

OpenAI requires explicit `LLM_PROVIDER=openai` and `OPENAI_API_KEY=sk-********` in `.env`.

Document uploads do not use an LLM. They are chunked and embedded for vector search only.

Documents are not sent to hosted embedding APIs unless `EMBEDDING_PROVIDER=openai`. Use `local` or `ollama` to keep proprietary text on your infrastructure.

## Upload Security

- File type validation (PDF, MD, TXT, DOCX, HTML only)
- Size limit via `MAX_UPLOAD_SIZE_MB`
- Secrets never logged

## UI

Privacy banner displayed on every page.
