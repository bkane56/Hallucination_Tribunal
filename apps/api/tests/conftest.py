import pytest
from httpx import ASGITransport, AsyncClient

from hallucination_tribunal.core.config import get_settings
from hallucination_tribunal.core.db import reset_database
from hallucination_tribunal.core.providers.local_embedding import get_embedding_provider
from hallucination_tribunal.main import app


@pytest.fixture(autouse=True)
def reset_state(tmp_path, monkeypatch):
    get_settings.cache_clear()
    get_embedding_provider.cache_clear()
    reset_database()
    db_path = tmp_path / "test.db"
    upload_dir = tmp_path / "uploads"
    chroma_dir = tmp_path / "chroma"
    upload_dir.mkdir()
    chroma_dir.mkdir()
    monkeypatch.setenv("SQLITE_DATABASE_PATH", str(db_path))
    monkeypatch.setenv("UPLOAD_DIRECTORY", str(upload_dir))
    monkeypatch.setenv("CHROMA_PERSIST_DIRECTORY", str(chroma_dir))
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("EMBEDDING_PROVIDER", "local")
    get_settings.cache_clear()
    get_embedding_provider.cache_clear()
    reset_database()
    yield
    get_settings.cache_clear()
    get_embedding_provider.cache_clear()
    reset_database()


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
