from datetime import datetime

from pydantic import BaseModel, Field

from src.models.enums import DocumentStatus, FileType


class Document(BaseModel):
    document_id: str
    filename: str
    file_type: FileType
    original_path: str
    text_hash: str
    chunk_count: int = 0
    status: DocumentStatus = DocumentStatus.PENDING
    created_at: datetime
    updated_at: datetime


class Chunk(BaseModel):
    chunk_id: str
    document_id: str
    chunk_index: int
    text: str
    token_count: int
    embedding_id: str | None = None
    metadata: dict[str, str] = Field(default_factory=dict)
    source_page: int | None = None
    source_section: str | None = None


class DocumentSummary(BaseModel):
    document_id: str
    filename: str
    file_type: FileType
    chunk_count: int
    status: DocumentStatus
    created_at: datetime


class DocumentListResponse(BaseModel):
    documents: list[DocumentSummary]


class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    status: DocumentStatus
    chunk_count: int
