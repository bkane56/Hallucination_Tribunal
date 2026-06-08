from datetime import datetime

from pydantic import BaseModel, Field

from src.models.common import Citation
from src.models.enums import ClaimType, ObjectionType, OverallVerdict, Verdict
from src.models.retrieval import RetrievedSource


class WitnessAnswer(BaseModel):
    answer_text: str
    citations: list[Citation] = Field(default_factory=list)
    uncertainty_notes: str | None = None


class Claim(BaseModel):
    claim_id: str
    claim_text: str
    claim_type: ClaimType = ClaimType.FACTUAL
    cited_sources: list[str] = Field(default_factory=list)
    extracted_from_sentence: str | None = None


class ProsecutorObjection(BaseModel):
    objection_id: str
    claim_id: str
    objection_type: ObjectionType
    explanation: str
    missing_evidence: str | None = None
    contradicted_by_sources: list[str] = Field(default_factory=list)


class JudgeVerdict(BaseModel):
    claim_id: str
    verdict: Verdict
    confidence: float = Field(ge=0.0, le=1.0)
    explanation: str
    supporting_sources: list[str] = Field(default_factory=list)
    recommended_revision: str | None = None


class TribunalAskRequest(BaseModel):
    question: str = Field(min_length=1)
    document_ids: list[str] | None = None
    top_k: int = Field(default=6, ge=1, le=20)


class TribunalAskResponse(BaseModel):
    question: str
    final_answer: str
    overall_verdict: OverallVerdict
    reliability_score: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Null when no factual claims were extracted.",
    )
    retrieved_sources: list[RetrievedSource] = Field(default_factory=list)
    witness_answer: WitnessAnswer
    claims: list[Claim] = Field(default_factory=list)
    prosecutor_objections: list[ProsecutorObjection] = Field(default_factory=list)
    judge_verdicts: list[JudgeVerdict] = Field(default_factory=list)


class TribunalResult(BaseModel):
    tribunal_result_id: str
    question: str
    final_answer: str
    overall_verdict: OverallVerdict
    reliability_score: float | None = None
    retrieved_sources: list[RetrievedSource] = Field(default_factory=list)
    witness_answer: WitnessAnswer
    claims: list[Claim] = Field(default_factory=list)
    prosecutor_objections: list[ProsecutorObjection] = Field(default_factory=list)
    judge_verdicts: list[JudgeVerdict] = Field(default_factory=list)
    created_at: datetime
