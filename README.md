# The Hallucination Tribunal

A portfolio RAG application that answers questions from a controlled document corpus and subjects each answer to adversarial review: **Witness → Prosecutor → Judge**. Built to demonstrate retrieval-augmented generation, multi-agent orchestration, and claim-level verification.

## What It Demonstrates

- Hybrid retrieval (vector + BM25) with structured, citeable answers
- Multi-agent tribunal pipeline with per-claim verdicts
- Document ingestion (PDF, MD, TXT, DOCX, HTML) and evaluation dashboard
- OpenAI for LLM and embeddings by default; [Ollama](https://ollama.com/) or local embeddings available as self-hosted alternatives

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, TypeScript, Tailwind CSS |
| Backend | Python 3.12, FastAPI, Pydantic |
| Vector DB | ChromaDB |
| Embeddings | OpenAI (`text-embedding-3-small`); optional local or Ollama |
| LLM | OpenAI (`gpt-4o-mini`); optional Ollama |
| Tooling | yarn (frontend), uv (backend) |

## Sample Data

The demo ships with ready-to-use corpus content so reviewers can try the tribunal without uploading files.

**Curated AI governance library (17 documents)** — Import from the Corpus page. Each entry is a structured summary of a public standard or policy template (NIST AI RMF, GovAI Coalition resources, university GenAI policies, public-sector guidance) with source URLs and governance use cases. Catalog lives in `apps/api/src/hallucination_tribunal/documents/sample_catalog.py`.

**Seed documents (`data/seed/`)** — Mix of realistic internal policies (AI usage, data privacy, incident response, engineering standards) and a fictional *Dragon Sanctuary Care Guide* included to surface unsupported claims and test the prosecutor/judge pipeline.

## Quick Start

### Prerequisites

- Node.js 20+, Python 3.12+
- [uv](https://docs.astral.sh/uv/), [yarn](https://yarnpkg.com/)
- An [OpenAI API key](https://platform.openai.com/api-keys)

### Environment

```bash
cp .env.example .env
# Edit .env and set OPENAI_API_KEY
```

Required variables for the default setup:

```bash
LLM_PROVIDER=openai
EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=your-key-here
```

If you previously indexed documents with local or Ollama embeddings, re-embed after switching providers:

```bash
curl -X POST http://localhost:8000/documents/rebuild-index
```

See [docs/privacy-and-security.md](docs/privacy-and-security.md) for what data is sent to hosted providers.

### Using Ollama instead (optional)

To keep document text and LLM inference on your machine, set in `.env`:

```bash
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama   # or local
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

Install [Ollama](https://ollama.com/) and pull your models. For Docker with Ollama: `docker compose --profile ollama up --build`.

### Backend

```bash
cd apps/api
uv sync --extra dev
uv run uvicorn hallucination_tribunal.main:app --reload --port 8000
```

### Frontend

```bash
cd apps/web
yarn install
yarn dev
```

Open http://localhost:3000

## Deployment

Production can use **Render for the API** and **Vercel for the UI** (see [docs/deployment.md](docs/deployment.md) for the Ollama-on-Render layout). Local development in this repo defaults to **OpenAI** for both LLM and embeddings.

| Component | Host |
|---|---|
| UI | Vercel (`NEXT_PUBLIC_BACKEND_URL` → Render API) |
| API | Render Docker (`render.yaml`, `.env.render.example`) |
| LLM (Render example) | Private Ollama on Render |

```bash
# Deploy UI to Vercel
./scripts/deploy.sh vercel

# Local Docker API + web (OpenAI via .env)
docker compose up --build

# Local Docker with Ollama (optional profile)
docker compose --profile ollama up --build
```

## Try the Demo

1. On **Corpus**, import sample governance documents or upload files from `data/seed/`
2. On **Tribunal**, ask a policy question (e.g. *What are our rules for external LLM APIs?*)
3. Review Witness answer, Prosecutor objections, Claim Docket, and Final Ruling
4. Run automated evaluations from the Evaluation Dashboard

## Tests

```bash
# Backend
cd apps/api && uv run pytest --cov=hallucination_tribunal --cov-report=term-missing

# Frontend
cd apps/web && yarn test:coverage

# End-to-end (Playwright)
cd apps/web && yarn playwright install chromium && yarn test:e2e
```

## Known Limitations

- Verdict quality depends on LLM adherence to structured prompts
- Complex PDF layouts may lose structure
- Reranking not included in MVP
- Evaluation metrics are heuristic
- OpenAI usage sends document chunks and tribunal prompts to OpenAI's API

## License

MIT
