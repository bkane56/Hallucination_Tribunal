import pytest

from hallucination_tribunal.core.db import Database
from hallucination_tribunal.models.domain import Document, DocumentStatus


@pytest.mark.asyncio
async def test_database_document_crud(tmp_path, monkeypatch):
    from hallucination_tribunal.core.config import get_settings

    get_settings.cache_clear()
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("SQLITE_DATABASE_PATH", str(db_path))

    db = Database()
    doc = Document(
        document_id="doc-1",
        filename="test.md",
        file_type="md",
        original_path=str(tmp_path / "test.md"),
        status=DocumentStatus.PENDING,
    )
    await db.create_document(doc)
    fetched = await db.get_document("doc-1")
    assert fetched is not None
    assert fetched.filename == "test.md"

    doc.status = DocumentStatus.INDEXED
    doc.chunk_count = 5
    await db.update_document(doc)
    updated = await db.get_document("doc-1")
    assert updated.status == DocumentStatus.INDEXED

    docs = await db.list_documents()
    assert len(docs) == 1

    deleted = await db.delete_document("doc-1")
    assert deleted is True
    assert await db.get_document("doc-1") is None
