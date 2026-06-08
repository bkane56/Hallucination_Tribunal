from src.core.config import Settings
from src.core.paths import ensure_data_directories, resolve_path


def test_resolve_path_uses_monorepo_data_directory() -> None:
    settings = Settings()
    resolved = resolve_path(settings, settings.uploads_directory)
    assert resolved.name == "uploads"
    assert resolved.parent.name == "data"


def test_ensure_data_directories_creates_paths(tmp_path, monkeypatch) -> None:
    settings = Settings(
        chroma_persist_directory=str(tmp_path / "chroma"),
        uploads_directory=str(tmp_path / "uploads"),
        seed_directory=str(tmp_path / "seed"),
        evals_directory=str(tmp_path / "evals"),
    )

    def fake_resolve(_settings: Settings, relative_path: str):
        return tmp_path / relative_path.split("/")[-1]

    monkeypatch.setattr("src.core.paths.resolve_path", fake_resolve)
    created = ensure_data_directories(settings)
    assert len(created) == 4
    for path in created:
        assert path.exists()
