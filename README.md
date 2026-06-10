# The Hallucination Tribunal

A portfolio-quality RAG application that answers questions from a controlled document corpus and subjects each answer to an adversarial review process: Witness → Prosecutor → Judge.

## Features

- Document upload and indexing (PDF, MD, TXT, DOCX, HTML)
- Hybrid retrieval (vector + BM25)
- Three-agent tribunal pipeline with claim-level verification
- Claim Docket UI with sortable verdict table
- Evaluation dashboard with automated test cases
- Local-first privacy (Ollama + ChromaDB)

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, TypeScript, Tailwind CSS |
| Backend | Python 3.12, FastAPI, Pydantic |
| Vector DB | ChromaDB |
| Embeddings | sentence-transformers (local) |
| LLM | Ollama (default), OpenAI (optional) |
| Package managers | yarn (frontend), uv (backend) |

## Local Setup

### Prerequisites

- Node.js 20+
- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- [yarn](https://yarnpkg.com/)
- [Ollama](https://ollama.com/) with a chat model installed (default: `llama3.1:8b`; run `ollama list` to verify)

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

### Docker

```bash
docker compose up --build
```

## Usage

1. Upload seed documents from `data/seed/` via the Corpus page
2. Ask a question on the Tribunal page
3. Review Witness Answer, Prosecutor Objections, Claim Docket, and Final Ruling
4. Run evaluations from the Evaluation Dashboard

## Tests

```bash
# Backend
cd apps/api && uv run pytest --cov=hallucination_tribunal --cov-report=term-missing

# Frontend
cd apps/web && yarn test:coverage

# End-to-end (Playwright; starts Next.js dev server automatically)
cd apps/web && yarn playwright install chromium && yarn test:e2e
```

## Known Limitations

- Verdict quality depends on LLM adherence to structured prompts
- Complex PDF layouts may lose structure
- Reranking not included in MVP
- Evaluation metrics are heuristic

## License

MIT
