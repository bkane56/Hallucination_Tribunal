from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import health
from src.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="The Hallucination Tribunal API",
    description="RAG-powered adversarial answer review pipeline",
    version=settings.app_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "The Hallucination Tribunal API"}
