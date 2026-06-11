#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

usage() {
  cat <<'EOF'
Hallucination Tribunal deploy helpers

Production (split deploy):
  - API: Render Web Service (render.yaml, .env.render.example)
  - UI:  Vercel (.env.vercel.example → NEXT_PUBLIC_BACKEND_URL)

Usage:
  ./scripts/deploy.sh vercel         Deploy Next.js UI to Vercel (production)
  ./scripts/deploy.sh vercel:preview Deploy a Vercel preview
  ./scripts/deploy.sh dev            Run web locally via Vercel (API: uvicorn or Render)
  ./scripts/deploy.sh api            Local Docker API + Ollama (not production)
  ./scripts/deploy.sh api:check      Build the API Docker image only

Render API:
  Connect repo in Render dashboard or apply render.yaml Blueprint.
  Root Directory: apps/api (or dockerContext in render.yaml).
  See docs/deployment.md

Prerequisites:
  - Vercel CLI (`npm i -g vercel`) and `vercel login`
  - Environment variables from .env.vercel.example (UI) and .env.render.example (API)
EOF
}

deploy_vercel() {
  if ! command -v vercel >/dev/null 2>&1; then
    echo "Install the Vercel CLI: npm i -g vercel" >&2
    exit 1
  fi
  if [[ "${1:-}" == "preview" ]]; then
    vercel
  else
    vercel --prod
  fi
}

dev_vercel() {
  if ! command -v vercel >/dev/null 2>&1; then
    echo "Install the Vercel CLI: npm i -g vercel" >&2
    exit 1
  fi
  vercel dev -L
}

deploy_api_local() {
  docker compose -f docker-compose.prod.yml up --build -d
  echo "API: http://localhost:${API_PORT:-8000}"
  echo "Ollama: http://localhost:11434 (internal to compose network)"
}

build_api_image() {
  docker build -t hallucination-tribunal-api apps/api
}

case "${1:-}" in
  vercel) deploy_vercel prod ;;
  vercel:preview) deploy_vercel preview ;;
  dev) dev_vercel ;;
  web) deploy_vercel prod ;;
  web:preview) deploy_vercel preview ;;
  api) deploy_api_local ;;
  api:check) build_api_image ;;
  -h|--help|help|"") usage ;;
  *)
    echo "Unknown command: ${1}" >&2
    usage
    exit 1
    ;;
esac
