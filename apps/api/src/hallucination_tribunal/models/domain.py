"""Domain models for The Hallucination Tribunal."""

from datetime import datetime
from enum import Enum
from typing import Annotated, Any
from uuid import uuid4

from pydantic import BaseModel, BeforeValidator, Field

from hallucination_tribunal.models.coercion import LlmStrList, coerce_null_to_list


class DocumentStatus(str, Enum):
    PENDING = "pending"
    INDEXED = "indexed"
    ERROR = "error"


class Verdict(str, Enum):
    SUPPORTED = "Supported"
    PARTIALLY_SUPPORTED = "Partially Supported"
    UNSUPPORTED = "Unsupported"
    CONTRADICTED = "Contradicted"
    NOT_ENOUGH_EVIDENCE = "Not Enough Evidence"


VERDICT_SCORES: dict[Verdict, float] = {
    Verdict.SUPPORTED: 1.0,
    Verdict.PARTIALLY_SUPPORTED: 0.6,
    Verdict.NOT_ENOUGH_EVIDENCE: 0.4,
    Verdict.UNSUPPORTED: 0.0,
    Verdict.CONTRADICTED: 0.0,
}


class Document(BaseModel):
    document_id: str = Field(default_factory=lambda: str(uuid4()))
    filename: str
    file_type: str
    original_path: str
    text_hash: str = ""
    chunk_count: int = 0
    status: DocumentStatus = DocumentStatus.PENDING
    error_message: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Chunk(BaseModel):
    chunk_id: str = Field(default_factory=lambda: str(uuid4()))
    document_id: str
    chunk_index: int
    text: str
    token_count: int = 0
    embedding_id: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)
    source_page: int | None = None
    source_section: str | None = None


class RetrievedSource(BaseModel):
    chunk_id: str
    document_id: str
    filename: str
    page_number: int | None = None
    section_title: str | None = None
    text: str
    similarity_score: float


class Citation(BaseModel):
    document_name: str
    page_number: int | None = None
    section_title: str | None = None
    chunk_id: str | None = None


class WitnessAnswer(BaseModel):
    answer_text: str
    citations: Annotated[list[Citation], BeforeValidator(coerce_null_to_list)] = Field(
        default_factory=list
    )
    uncertainty_notes: str | None = None


class Claim(BaseModel):
    claim_id: str = Field(default_factory=lambda: str(uuid4()))
    claim_text: str
    claim_type: str = "factual"
    cited_sources: LlmStrList = Field(default_factory=list)
    extracted_from_sentence: str = ""


class ProsecutorObjection(BaseModel):
    objection_id: str = Field(default_factory=lambda: str(uuid4()))
    claim_id: str
    objection_type: str
    explanation: str
    missing_evidence: str | None = None
    contradicted_by_sources: LlmStrList = Field(default_factory=list)


class JudgeVerdict(BaseModel):
    claim_id: str
    verdict: Verdict
    confidence: float = Field(ge=0.0, le=1.0)
    explanation: str
    supporting_sources: LlmStrList = Field(default_factory=list)
    recommended_revision: str | None = None


class TribunalResult(BaseModel):
    tribunal_result_id: str = Field(default_factory=lambda: str(uuid4()))
    question: str
    final_answer: str
    overall_verdict: Verdict | str
    reliability_score: float | str
    retrieved_sources: list[RetrievedSource] = Field(default_factory=list)
    witness_answer: WitnessAnswer
    claims: list[Claim] = Field(default_factory=list)
    prosecutor_objections: list[ProsecutorObjection] = Field(default_factory=list)
    judge_verdicts: list[JudgeVerdict] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
