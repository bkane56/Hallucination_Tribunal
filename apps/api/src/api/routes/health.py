from fastapi import APIRouter, Depends

from src.core.config import Settings, get_settings
from src.core.paths import ensure_data_directories, resolve_path

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check(settings: Settings = Depends(get_settings)) -> dict[str, str]:
    return {
        "status": "ok",
        "version": settings.app_version,
        "environment": settings.app_env,
    }


@router.get("/health/ready")
def readiness_check(settings: Settings = Depends(get_settings)) -> dict[str, object]:
    directories = ensure_data_directories(settings)
    return {
        "status": "ready",
        "version": settings.app_version,
        "environment": settings.app_env,
        "providers": {
            "llm": settings.llm_provider,
            "embedding": settings.embedding_provider,
            "vector_db": settings.vector_db_provider,
        },
        "data_directories": {
            "chroma": str(resolve_path(settings, settings.chroma_persist_directory)),
            "uploads": str(resolve_path(settings, settings.uploads_directory)),
            "seed": str(resolve_path(settings, settings.seed_directory)),
            "evals": str(resolve_path(settings, settings.evals_directory)),
        },
        "directories_ready": all(path.exists() for path in directories),
    }
