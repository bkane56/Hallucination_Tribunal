"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from hallucination_tribunal import __version__
from hallucination_tribunal.api.routes import router
from hallucination_tribunal.core.config import get_settings
from hallucination_tribunal.core.db import get_database
from hallucination_tribunal.core.logging import configure_logging
from hallucination_tribunal.evaluations.service import seed_eval_cases


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    settings = get_settings()
    settings.ensure_data_directories()
    seed_eval_cases(settings.resolve_path(settings.evals_directory))
    db = get_database()
    await db.initialize()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="The Hallucination Tribunal API",
        version=__version__,
        lifespan=lifespan,
        root_path=settings.api_root_path,
    )
    cors_kwargs: dict = {
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
        "allow_origins": settings.cors_origins,
    }
    app.add_middleware(CORSMiddleware, **cors_kwargs)
    app.include_router(router)
    return app


app = create_app()
