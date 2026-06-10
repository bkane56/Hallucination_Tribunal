FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml .
RUN uv pip install --system -e ".[dev]" || uv pip install --system .

COPY src ./src

ENV PYTHONPATH=/app/src
EXPOSE 8000

CMD ["uvicorn", "hallucination_tribunal.main:app", "--host", "0.0.0.0", "--port", "8000"]
