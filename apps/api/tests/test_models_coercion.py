import pytest

from hallucination_tribunal.models.domain import (
    Claim,
    JudgeVerdict,
    ProsecutorObjection,
    Verdict,
)


def test_prosecutor_objection_coerces_null_contradicted_sources():
    objection = ProsecutorObjection.model_validate(
        {
            "claim_id": "claim-1",
            "objection_type": "unsupported",
            "explanation": "No evidence.",
            "contradicted_by_sources": None,
        }
    )
    assert objection.contradicted_by_sources == []


def test_claim_coerces_null_cited_sources():
    claim = Claim.model_validate(
        {
            "claim_text": "Example claim.",
            "cited_sources": None,
        }
    )
    assert claim.cited_sources == []


def test_claim_coerces_json_string_cited_sources():
    claim = Claim.model_validate(
        {
            "claim_text": "Example claim.",
            "cited_sources": "[]",
        }
    )
    assert claim.cited_sources == []


def test_claim_coerces_json_string_array_cited_sources():
    claim = Claim.model_validate(
        {
            "claim_text": "Example claim.",
            "cited_sources": '["policy.md"]',
        }
    )
    assert claim.cited_sources == ["policy.md"]


def test_judge_verdict_coerces_null_supporting_sources():
    verdict = JudgeVerdict.model_validate(
        {
            "claim_id": "claim-1",
            "verdict": Verdict.SUPPORTED,
            "confidence": 0.9,
            "explanation": "Supported.",
            "supporting_sources": None,
        }
    )
    assert verdict.supporting_sources == []


def test_coerce_verdict_from_string():
    from hallucination_tribunal.models.coercion import coerce_verdict

    assert coerce_verdict("Supported") == Verdict.SUPPORTED
    assert coerce_verdict("unknown-value") == "unknown-value"


def test_coerce_reliability_score():
    from hallucination_tribunal.models.coercion import coerce_reliability_score

    assert coerce_reliability_score("Not Applicable") == "Not Applicable"
    assert coerce_reliability_score("0.75") == 0.75
