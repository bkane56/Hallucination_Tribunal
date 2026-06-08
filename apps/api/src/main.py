from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.error_handlers import register_error_handlers
from src.api.routes import health
from src.core.config import get_settings
from src.core.logging import get_logger, setup_logging
from src.core.paths import ensure_data_directories

settings = get_settings()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    setup_logging(settings.log_level)
    directories = ensure_data_directories(settings)
    logger.info(
        "API starting env=%s data_dirs=%s",
        settings.app_env,
        [str(path) for path in directories],
    )
    yield
    logger.info("API shutdown")


app = FastAPI(
    title="The Hallucination Tribunal API",
    description="RAG-powered adversarial answer review pipeline",
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_error_handlers(app)
app.include_router(health.router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "The Hallucination Tribunal API"}
