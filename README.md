# The Hallucination Tribunal

A portfolio RAG application that answers questions from a controlled document corpus and subjects each answer to adversarial review: **Witness → Prosecutor → Judge**. Built to demonstrate retrieval-augmented generation, multi-agent orchestration, and claim-level verification in a local-first stack.

## What It Demonstrates

- Hybrid retrieval (vector + BM25) with structured, citeable answers
- Multi-agent tribunal pipeline with per-claim verdicts
- Document ingestion (PDF, MD, TXT, DOCX, HTML) and evaluation dashboard
- Privacy-conscious defaults (Ollama + ChromaDB; OpenAI optional)

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, TypeScript, Tailwind CSS |
| Backend | Python 3.12, FastAPI, Pydantic |
| Vector DB | ChromaDB |
| Embeddings | sentence-transformers (local) |
| LLM | Ollama (default), OpenAI (optional) |
| Tooling | yarn (frontend), uv (backend) |

## Sample Data

The demo ships with ready-to-use corpus content so reviewers can try the tribunal without uploading files.

**Curated AI governance library (17 documents)** — Import from the Corpus page. Each entry is a structured summary of a public standard or policy template (NIST AI RMF, GovAI Coalition resources, university GenAI policies, public-sector guidance) with source URLs and governance use cases. Catalog lives in `apps/api/src/hallucination_tribunal/documents/sample_catalog.py`.

**Seed documents (`data/seed/`)** — Mix of realistic internal policies (AI usage, data privacy, incident response, engineering standards) and a fictional *Dragon Sanctuary Care Guide* included to surface unsupported claims and test the prosecutor/judge pipeline.

## Quick Start

### Prerequisites

- Node.js 20+, Python 3.12+
- [uv](https://docs.astral.sh/uv/), [yarn](https://yarnpkg.com/)
- [Ollama](https://ollama.com/) with a chat model (default: `llama3.1:8b`)

### Environment

```bash
cp .env.example .env
```

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

Production deploys **web + API together on Vercel** via [Vercel Services](https://vercel.com/docs/services). Configure your existing Ollama host in `OLLAMA_BASE_URL`.

See [docs/deployment.md](docs/deployment.md) for step-by-step instructions.

```bash
# Deploy everything to Vercel
./scripts/deploy.sh vercel

# Local multi-service dev
./scripts/deploy.sh dev
```

Optional Docker stack for local API + Ollama (not used for Vercel production):

```bash
./scripts/deploy.sh api
```

### Docker

```bash
docker compose up --build
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

## License

MIT
