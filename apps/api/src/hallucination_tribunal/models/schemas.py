"""API request/response schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from hallucination_tribunal.models.domain import (
    Claim,
    DocumentStatus,
    JudgeVerdict,
    ProsecutorObjection,
    RetrievedSource,
    Verdict,
    WitnessAnswer,
)


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "0.1.0"


class DocumentResponse(BaseModel):
    document_id: str
    filename: str
    file_type: str
    chunk_count: int
    status: DocumentStatus
    error_message: str | None = None
    created_at: datetime
    updated_at: datetime


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]


class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    status: str
    chunk_count: int


class SampleDocumentResponse(BaseModel):
    sample_id: str
    title: str
    category: str
    source: str
    url: str
    description: str
    good_for: str = ""
    filename: str
    already_imported: bool = False


class SampleDocumentListResponse(BaseModel):
    samples: list[SampleDocumentResponse]
    categories: list[str]


class CorpusOverviewResponse(BaseModel):
    documents: list[DocumentResponse]
    samples: list[SampleDocumentResponse]
    categories: list[str]


class SampleDocumentImportRequest(BaseModel):
    sample_ids: list[str] = Field(min_length=1)


class SampleDocumentImportResult(BaseModel):
    sample_id: str
    document_id: str | None = None
    filename: str | None = None
    status: str
    chunk_count: int = 0
    message: str | None = None


class SampleDocumentImportResponse(BaseModel):
    imported: list[SampleDocumentImportResult]
    skipped: list[SampleDocumentImportResult]
    errors: list[SampleDocumentImportResult]


class TribunalAskRequest(BaseModel):
    question: str = Field(min_length=1)
    document_ids: list[str] | None = None
    top_k: int = Field(default=6, ge=1, le=20)


class TribunalAskResponse(BaseModel):
    tribunal_result_id: str
    question: str
    final_answer: str
    overall_verdict: Verdict | str
    reliability_score: float | str
    retrieved_sources: list[RetrievedSource]
    witness_answer: WitnessAnswer
    claims: list[Claim]
    prosecutor_objections: list[ProsecutorObjection]
    judge_verdict: list[JudgeVerdict]
    created_at: datetime


class EvaluationCaseResult(BaseModel):
    case_id: str
    question: str
    retrieval_hit: bool
    citation_accuracy: float
    unsupported_claim_count: int
    contradicted_claim_count: int
    reliability_score: float | str
    expected_verdict_behavior: str
    passed: bool


class EvaluationRunResponse(BaseModel):
    run_id: str
    started_at: datetime
    completed_at: datetime
    aggregate_metrics: dict[str, Any]
    case_results: list[EvaluationCaseResult]


class EvaluationRunsListResponse(BaseModel):
    runs: list[EvaluationRunResponse]


class ErrorResponse(BaseModel):
    detail: str
    code: str
