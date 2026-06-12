FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

COPY pyproject.toml README.md ./
COPY src ./src

# Production (Render) defaults to OpenAI embeddings — skip torch/sentence-transformers (~2GB+).
# Set INSTALL_LOCAL_EMBEDDINGS=1 for local Docker stacks that use EMBEDDING_PROVIDER=local.
ARG INSTALL_LOCAL_EMBEDDINGS=0
RUN if [ "$INSTALL_LOCAL_EMBEDDINGS" = "1" ]; then \
      uv pip install --system torch --index-url https://download.pytorch.org/whl/cpu \
      && uv pip install --system -e ".[local-embeddings]"; \
    else \
      uv pip install --system -e .; \
    fi

ENV PYTHONPATH=/app/src
ENV APP_ENV=production

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "hallucination_tribunal.main:app", "--host", "0.0.0.0", "--port", "8000"]
