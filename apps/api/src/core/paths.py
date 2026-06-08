from pathlib import Path

from src.core.config import Settings


def _api_root() -> Path:
    return Path(__file__).resolve().parents[2]


def resolve_path(settings: Settings, relative_path: str) -> Path:
    """Resolve configured paths for local monorepo and Docker layouts."""
    path = Path(relative_path)
    if path.is_absolute():
        return path

    api_root = _api_root()
    monorepo_root = api_root.parent.parent
    if (monorepo_root / "data").is_dir():
        return (monorepo_root / path).resolve()

    return (api_root / path).resolve()


def ensure_data_directories(settings: Settings) -> list[Path]:
    """Create required data directories if missing. Returns created paths."""
    directories = [
        resolve_path(settings, settings.chroma_persist_directory),
        resolve_path(settings, settings.uploads_directory),
        resolve_path(settings, settings.seed_directory),
        resolve_path(settings, settings.evals_directory),
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    return directories
