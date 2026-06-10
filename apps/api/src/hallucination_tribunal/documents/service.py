"""Document ingestion and management service."""

import hashlib
import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from hallucination_tribunal.core.config import get_settings
from hallucination_tribunal.core.db import Database, get_database
from hallucination_tribunal.core.logging import get_logger
from hallucination_tribunal.core.providers.chroma_store import get_vector_store
from hallucination_tribunal.core.providers.local_embedding import get_embedding_provider
from hallucination_tribunal.documents.chunker import chunk_segments
from hallucination_tribunal.documents.extractors import TextExtractor
from hallucination_tribunal.documents.sample_catalog import (
    SampleDocument,
    get_sample_document,
    list_sample_documents,
)
from hallucination_tribunal.models.domain import Document, DocumentStatus

logger = get_logger(__name__)

ALLOWED_EXTENSIONS = {"pdf", "md", "txt", "docx", "html"}


class DocumentService:
    def __init__(self, db: Database | None = None):
        self.db = db or get_database()
        self.settings = get_settings()
        self.upload_dir = self.settings.resolve_path(self.settings.upload_directory)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def _get_file_type(self, filename: str) -> str:
        ext = Path(filename).suffix.lstrip(".").lower()
        if ext == "markdown":
            ext = "md"
        return ext

    def list_sample_documents(self) -> list[SampleDocument]:
        return list_sample_documents()

    async def find_document_by_filename(self, filename: str) -> Document | None:
        for doc in await self.db.list_documents():
            if doc.filename == filename:
                return doc
        return None

    async def import_sample_document(self, sample_id: str) -> tuple[Document, bool]:
        sample = get_sample_document(sample_id)
        if not sample:
            raise ValueError(f"Unknown sample document: {sample_id}")

        existing = await self.find_document_by_filename(sample.filename)
        if existing:
            return existing, True

        content = sample.render_markdown().encode("utf-8")
        return await self._ingest_bytes(
            filename=sample.filename,
            file_type="md",
            content=content,
        ), False

    async def import_sample_documents(self, sample_ids: list[str]) -> dict[str, object]:
        imported: list[dict[str, object]] = []
        skipped: list[dict[str, object]] = []
        errors: list[dict[str, str]] = []

        for sample_id in sample_ids:
            try:
                doc, already_present = await self.import_sample_document(sample_id)
                if already_present:
                    skipped.append({"sample_id": sample_id, "document": doc})
                else:
                    imported.append({"sample_id": sample_id, "document": doc})
            except ValueError as exc:
                errors.append({"sample_id": sample_id, "error": str(exc)})
            except Exception as exc:
                logger.error("sample_import_failed", sample_id=sample_id, error=str(exc))
                errors.append({"sample_id": sample_id, "error": str(exc)})

        return {
            "imported": imported,
            "skipped": skipped,
            "errors": errors,
        }

    async def _ingest_bytes(
        self,
        *,
        filename: str,
        file_type: str,
        content: bytes,
    ) -> Document:
        if file_type not in ALLOWED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {file_type}")
        if len(content) > self.settings.max_upload_bytes:
            raise ValueError(
                f"File exceeds maximum size of {self.settings.max_upload_size_mb}MB"
            )

        document_id = str(uuid4())
        safe_filename = f"{document_id}_{Path(filename).name}"
        file_path = self.upload_dir / safe_filename
        file_path.write_bytes(content)

        text_hash = hashlib.sha256(content).hexdigest()
        doc = Document(
            document_id=document_id,
            filename=filename,
            file_type=file_type,
            original_path=str(file_path),
            text_hash=text_hash,
            status=DocumentStatus.PENDING,
        )
        await self.db.create_document(doc)

        try:
            await self._index_document(doc, file_path)
        except Exception as exc:
            logger.error("ingestion_failed", document_id=document_id, error=str(exc))
            doc.status = DocumentStatus.ERROR
            doc.error_message = str(exc)
            await self.db.update_document(doc)
            raise

        return doc

    async def upload_document(self, file: UploadFile) -> Document:
        file_type = self._get_file_type(file.filename or "unknown")
        if file_type not in ALLOWED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {file_type}")

        content = await file.read()
        return await self._ingest_bytes(
            filename=file.filename or "upload",
            file_type=file_type,
            content=content,
        )

    async def _index_document(self, doc: Document, file_path: Path) -> None:
        segments = TextExtractor.extract(file_path, doc.file_type)
        if not segments:
            raise ValueError("Document contains no extractable text")

        chunks = chunk_segments(segments, doc.document_id)
        if not chunks:
            raise ValueError("Document produced no chunks after splitting")

        embedder = get_embedding_provider()
        vector_store = get_vector_store()
        texts = [c.text for c in chunks]
        embeddings = embedder.embed_texts(texts)

        metadatas = []
        for chunk in chunks:
            chunk.embedding_id = chunk.chunk_id
            metadatas.append(
                {
                    "document_id": doc.document_id,
                    "filename": doc.filename,
                    "chunk_index": chunk.chunk_index,
                    "source_page": chunk.source_page or -1,
                    "source_section": chunk.source_section or "",
                }
            )

        vector_store.upsert_chunks(chunks, embeddings, metadatas)
        await self.db.save_chunks(chunks)

        doc.chunk_count = len(chunks)
        doc.status = DocumentStatus.INDEXED
        doc.error_message = None
        await self.db.update_document(doc)
        logger.info(
            "document_indexed",
            document_id=doc.document_id,
            chunk_count=len(chunks),
        )

    async def list_documents(self) -> list[Document]:
        return await self.db.list_documents()

    async def get_document(self, document_id: str) -> Document | None:
        return await self.db.get_document(document_id)

    async def delete_document(self, document_id: str) -> bool:
        doc = await self.db.get_document(document_id)
        if not doc:
            return False

        get_vector_store().delete_by_document_id(document_id)
        await self.db.delete_document(document_id)

        file_path = Path(doc.original_path)
        if file_path.exists():
            file_path.unlink()
        return True

    async def rebuild_index(self) -> dict[str, int]:
        docs = await self.db.list_documents()
        vector_store = get_vector_store()
        vector_store.clear()

        rebuilt = 0
        for doc in docs:
            if doc.status != DocumentStatus.INDEXED:
                continue
            await self.db.delete_chunks_for_document(doc.document_id)
            file_path = Path(doc.original_path)
            if not file_path.exists():
                doc.status = DocumentStatus.ERROR
                doc.error_message = "Original file missing"
                await self.db.update_document(doc)
                continue
            try:
                await self._index_document(doc, file_path)
                rebuilt += 1
            except Exception as exc:
                doc.status = DocumentStatus.ERROR
                doc.error_message = str(exc)
                await self.db.update_document(doc)

        return {"rebuilt_count": rebuilt, "total_documents": len(docs)}
