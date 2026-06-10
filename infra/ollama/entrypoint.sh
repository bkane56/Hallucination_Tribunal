#!/bin/sh
set -eu

ollama serve &
pid="$!"

until ollama list >/dev/null 2>&1; do
  sleep 1
done

if [ -n "${OLLAMA_MODEL:-}" ]; then
  echo "Ensuring Ollama model is available: ${OLLAMA_MODEL}"
  ollama pull "${OLLAMA_MODEL}"
fi

wait "${pid}"
