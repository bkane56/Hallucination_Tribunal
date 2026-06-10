#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

usage() {
  cat <<'EOF'
Hallucination Tribunal deploy helpers

Usage:
  ./scripts/deploy.sh vercel         Deploy web + API to Vercel (production)
  ./scripts/deploy.sh vercel:preview Deploy a Vercel preview
  ./scripts/deploy.sh dev            Run web + API locally via Vercel Services
  ./scripts/deploy.sh api              Docker API stack (local only, optional)
  ./scripts/deploy.sh api:check        Build the API Docker image only

Prerequisites:
  - Vercel CLI (`npm i -g vercel`) and `vercel login`
  - Project framework set to "Services" in Vercel (see docs/deployment.md)
  - Environment variables from .env.vercel.example
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
