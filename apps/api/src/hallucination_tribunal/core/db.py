"""SQLite database layer."""

import asyncio
import json
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, AsyncIterator

import aiosqlite

from hallucination_tribunal.core.config import Settings, get_settings
from hallucination_tribunal.models.domain import (
    Chunk,
    Document,
    DocumentStatus,
    TribunalResult,
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (
    document_id TEXT PRIMARY KEY,
    filename TEXT NOT NULL,
    file_type TEXT NOT NULL,
    original_path TEXT NOT NULL,
    text_hash TEXT,
    chunk_count INTEGER DEFAULT 0,
    status TEXT NOT NULL,
    error_message TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS chunks (
    chunk_id TEXT PRIMARY KEY,
    document_id TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    text TEXT NOT NULL,
    token_count INTEGER DEFAULT 0,
    embedding_id TEXT,
    source_page INTEGER,
    source_section TEXT,
    metadata TEXT,
    FOREIGN KEY (document_id) REFERENCES documents(document_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tribunal_results (
    tribunal_result_id TEXT PRIMARY KEY,
    question TEXT NOT NULL,
    final_answer TEXT NOT NULL,
    overall_verdict TEXT NOT NULL,
    reliability_score TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS evaluation_runs (
    run_id TEXT PRIMARY KEY,
    started_at TEXT NOT NULL,
    completed_at TEXT NOT NULL,
    aggregate_metrics TEXT NOT NULL,
    case_results TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_chunks_document_id ON chunks(document_id);
"""


class Database:
    _init_lock = asyncio.Lock()

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()
        self.db_path = self.settings.resolve_path(self.settings.sqlite_database_path)
        self._initialized = False

    @classmethod
    async def _configure_connection(cls, conn: aiosqlite.Connection) -> None:
        await conn.execute("PRAGMA journal_mode=WAL")
        await conn.execute("PRAGMA busy_timeout=30000")

    async def initialize(self) -> None:
        async with self._init_lock:
            if self._initialized:
                return
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            async with aiosqlite.connect(self.db_path, timeout=30) as conn:
                await self._configure_connection(conn)
                await conn.executescript(SCHEMA)
                await conn.commit()
            self._initialized = True

    @asynccontextmanager
    async def session(self) -> AsyncIterator[aiosqlite.Connection]:
        if not self._initialized:
            await self.initialize()
        conn = await aiosqlite.connect(self.db_path, timeout=30)
        conn.row_factory = aiosqlite.Row
        await self._configure_connection(conn)
        try:
            yield conn
            await conn.commit()
        finally:
            await conn.close()

    async def create_document(self, doc: Document) -> Document:
        async with self.session() as conn:
            await conn.execute(
                """
                INSERT INTO documents (
                    document_id, filename, file_type, original_path, text_hash,
                    chunk_count, status, error_message, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    doc.document_id,
                    doc.filename,
                    doc.file_type,
                    doc.original_path,
                    doc.text_hash,
                    doc.chunk_count,
                    doc.status.value,
                    doc.error_message,
                    doc.created_at.isoformat(),
                    doc.updated_at.isoformat(),
                ),
            )
        return doc

    async def update_document(self, doc: Document) -> Document:
        doc.updated_at = datetime.utcnow()
        async with self.session() as conn:
            await conn.execute(
                """
                UPDATE documents SET
                    chunk_count = ?, status = ?, error_message = ?,
                    text_hash = ?, updated_at = ?
                WHERE document_id = ?
                """,
                (
                    doc.chunk_count,
                    doc.status.value,
                    doc.error_message,
                    doc.text_hash,
                    doc.updated_at.isoformat(),
                    doc.document_id,
                ),
            )
        return doc

    async def get_document(self, document_id: str) -> Document | None:
        async with self.session() as conn:
            cursor = await conn.execute(
                "SELECT * FROM documents WHERE document_id = ?",
                (document_id,),
            )
            row = await cursor.fetchone()
        if not row:
            return None
        return self._row_to_document(row)

    async def list_documents(self) -> list[Document]:
        async with self.session() as conn:
            cursor = await conn.execute(
                "SELECT * FROM documents ORDER BY created_at DESC"
            )
            rows = await cursor.fetchall()
        return [self._row_to_document(row) for row in rows]

    async def delete_document(self, document_id: str) -> bool:
        async with self.session() as conn:
            await conn.execute(
                "DELETE FROM chunks WHERE document_id = ?", (document_id,)
            )
            cursor = await conn.execute(
                "DELETE FROM documents WHERE document_id = ?",
                (document_id,),
            )
            return cursor.rowcount > 0

    async def save_chunks(self, chunks: list[Chunk]) -> None:
        async with self.session() as conn:
            for chunk in chunks:
                await conn.execute(
                    """
                    INSERT INTO chunks (
                        chunk_id, document_id, chunk_index, text, token_count,
                        embedding_id, source_page, source_section, metadata
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        chunk.chunk_id,
                        chunk.document_id,
                        chunk.chunk_index,
                        chunk.text,
                        chunk.token_count,
                        chunk.embedding_id,
                        chunk.source_page,
                        chunk.source_section,
                        json.dumps(chunk.metadata),
                    ),
                )

    async def delete_chunks_for_document(self, document_id: str) -> None:
        async with self.session() as conn:
            await conn.execute(
                "DELETE FROM chunks WHERE document_id = ?", (document_id,)
            )

    async def get_chunks_for_document(self, document_id: str) -> list[Chunk]:
        async with self.session() as conn:
            cursor = await conn.execute(
                "SELECT * FROM chunks WHERE document_id = ? ORDER BY chunk_index",
                (document_id,),
            )
            rows = await cursor.fetchall()
        return [self._row_to_chunk(row) for row in rows]

    async def get_all_chunks(
        self, document_ids: list[str] | None = None
    ) -> list[Chunk]:
        async with self.session() as conn:
            if document_ids:
                placeholders = ",".join("?" * len(document_ids))
                cursor = await conn.execute(
                    f"SELECT * FROM chunks WHERE document_id IN ({placeholders})",
                    document_ids,
                )
            else:
                cursor = await conn.execute("SELECT * FROM chunks")
            rows = await cursor.fetchall()
        return [self._row_to_chunk(row) for row in rows]

    async def save_tribunal_result(self, result: TribunalResult) -> TribunalResult:
        async with self.session() as conn:
            await conn.execute(
                """
                INSERT INTO tribunal_results (
                    tribunal_result_id, question, final_answer, overall_verdict,
                    reliability_score, payload, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    result.tribunal_result_id,
                    result.question,
                    result.final_answer,
                    str(result.overall_verdict),
                    str(result.reliability_score),
                    result.model_dump_json(),
                    result.created_at.isoformat(),
                ),
            )
        return result

    async def get_tribunal_result(self, tribunal_result_id: str) -> TribunalResult | None:
        async with self.session() as conn:
            cursor = await conn.execute(
                "SELECT payload FROM tribunal_results WHERE tribunal_result_id = ?",
                (tribunal_result_id,),
            )
            row = await cursor.fetchone()
        if not row:
            return None
        return TribunalResult.model_validate_json(row["payload"])

    async def save_evaluation_run(
        self,
        run_id: str,
        started_at: datetime,
        completed_at: datetime,
        aggregate_metrics: dict[str, Any],
        case_results: list[dict[str, Any]],
    ) -> None:
        async with self.session() as conn:
            await conn.execute(
                """
                INSERT INTO evaluation_runs (
                    run_id, started_at, completed_at, aggregate_metrics, case_results
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    run_id,
                    started_at.isoformat(),
                    completed_at.isoformat(),
                    json.dumps(aggregate_metrics),
                    json.dumps(case_results),
                ),
            )

    async def list_evaluation_runs(self) -> list[dict[str, Any]]:
        async with self.session() as conn:
            cursor = await conn.execute(
                "SELECT * FROM evaluation_runs ORDER BY started_at DESC"
            )
            rows = await cursor.fetchall()
        return [
            {
                "run_id": row["run_id"],
                "started_at": row["started_at"],
                "completed_at": row["completed_at"],
                "aggregate_metrics": json.loads(row["aggregate_metrics"]),
                "case_results": json.loads(row["case_results"]),
            }
            for row in rows
        ]

    async def get_evaluation_run(self, run_id: str) -> dict[str, Any] | None:
        async with self.session() as conn:
            cursor = await conn.execute(
                "SELECT * FROM evaluation_runs WHERE run_id = ?",
                (run_id,),
            )
            row = await cursor.fetchone()
        if not row:
            return None
        return {
            "run_id": row["run_id"],
            "started_at": row["started_at"],
            "completed_at": row["completed_at"],
            "aggregate_metrics": json.loads(row["aggregate_metrics"]),
            "case_results": json.loads(row["case_results"]),
        }

    @staticmethod
    def _row_to_document(row: aiosqlite.Row) -> Document:
        return Document(
            document_id=row["document_id"],
            filename=row["filename"],
            file_type=row["file_type"],
            original_path=row["original_path"],
            text_hash=row["text_hash"] or "",
            chunk_count=row["chunk_count"],
            status=DocumentStatus(row["status"]),
            error_message=row["error_message"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    @staticmethod
    def _row_to_chunk(row: aiosqlite.Row) -> Chunk:
        metadata = json.loads(row["metadata"]) if row["metadata"] else {}
        return Chunk(
            chunk_id=row["chunk_id"],
            document_id=row["document_id"],
            chunk_index=row["chunk_index"],
            text=row["text"],
            token_count=row["token_count"],
            embedding_id=row["embedding_id"] or "",
            source_page=row["source_page"],
            source_section=row["source_section"],
            metadata=metadata,
        )


_db: Database | None = None


def get_database() -> Database:
    global _db
    if _db is None:
        _db = Database()
    return _db


def reset_database() -> None:
    global _db
    _db = None
