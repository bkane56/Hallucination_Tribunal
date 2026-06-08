from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from src.models import (
    Claim,
    JudgeVerdict,
    TribunalAskRequest,
    Verdict,
    WitnessAnswer,
)


def test_tribunal_ask_request_requires_question() -> None:
    with pytest.raises(ValidationError):
        TribunalAskRequest(question="")


def test_tribunal_ask_request_top_k_bounds() -> None:
    with pytest.raises(ValidationError):
        TribunalAskRequest(question="test", top_k=0)


def test_judge_verdict_confidence_bounds() -> None:
    with pytest.raises(ValidationError):
        JudgeVerdict(
            claim_id="c1",
            verdict=Verdict.SUPPORTED,
            confidence=1.5,
            explanation="test",
        )


def test_witness_answer_defaults() -> None:
    answer = WitnessAnswer(answer_text="Grounded response.")
    assert answer.citations == []
    assert answer.uncertainty_notes is None


def test_claim_model() -> None:
    claim = Claim(claim_id="c1", claim_text="External APIs require approval.")
    assert claim.claim_type.value == "factual"


def test_tribunal_result_round_trip() -> None:
    from src.models import OverallVerdict, TribunalResult

    result = TribunalResult(
        tribunal_result_id="t1",
        question="Are external LLMs allowed?",
        final_answer="Approval is required.",
        overall_verdict=OverallVerdict.REVISED,
        reliability_score=0.6,
        witness_answer=WitnessAnswer(answer_text="Maybe."),
        created_at=datetime.now(UTC),
    )
    payload = result.model_dump()
    assert payload["overall_verdict"] == "Revised"
