import json
from unittest.mock import AsyncMock, patch

import pytest

from hallucination_tribunal.models.domain import (
    Citation,
    Claim,
    JudgeVerdict,
    ProsecutorObjection,
    RetrievedSource,
    Verdict,
    WitnessAnswer,
)
from hallucination_tribunal.tribunal.agents import (
    extract_claims,
    generate_objections,
    generate_verdicts,
    generate_witness_answer,
    revise_final_answer,
)


@pytest.fixture
def sources():
    return [
        RetrievedSource(
            chunk_id="c1",
            document_id="d1",
            filename="ai_usage_policy.md",
            page_number=1,
            section_title="External LLM APIs",
            text="External LLM APIs require approval from the AI Governance Committee.",
            similarity_score=0.92,
        )
    ]


@pytest.mark.asyncio
async def test_witness_no_sources():
    result = await generate_witness_answer("test?", [])
    assert "not contain enough evidence" in result.answer_text.lower()


@pytest.mark.asyncio
@patch("hallucination_tribunal.tribunal.agents._call_llm_with_retry", new_callable=AsyncMock)
async def test_witness_with_sources(mock_llm, sources):
    mock_llm.return_value = {
        "answer_text": "External LLM APIs require approval.",
        "citations": [
            {
                "document_name": "ai_usage_policy.md",
                "page_number": 1,
                "section_title": "External LLM APIs",
                "chunk_id": "c1",
            }
        ],
        "uncertainty_notes": None,
    }
    result = await generate_witness_answer("Are external LLM APIs allowed?", sources)
    assert "approval" in result.answer_text
    assert len(result.citations) == 1


@pytest.mark.asyncio
@patch("hallucination_tribunal.tribunal.agents._call_llm_with_retry", new_callable=AsyncMock)
async def test_extract_claims(mock_llm, sources):
    mock_llm.return_value = {
        "claims": [
            {
                "claim_text": "External LLM APIs require approval.",
                "claim_type": "factual",
                "cited_sources": ["ai_usage_policy.md"],
                "extracted_from_sentence": "External LLM APIs require approval.",
            }
        ]
    }
    witness = WitnessAnswer(answer_text="External LLM APIs require approval.", citations=[])
    claims = await extract_claims(witness, sources)
    assert len(claims) == 1


@pytest.mark.asyncio
@patch("hallucination_tribunal.tribunal.agents._call_llm_with_retry", new_callable=AsyncMock)
async def test_generate_objections(mock_llm, sources):
    claims = [
        Claim(claim_id="claim-1", claim_text="All LLM APIs are always allowed.", extracted_from_sentence="")
    ]
    witness = WitnessAnswer(answer_text="All LLM APIs are always allowed.", citations=[])
    mock_llm.return_value = {
        "objections": [
            {
                "claim_id": "claim-1",
                "objection_type": "unsupported",
                "explanation": "Policy requires approval.",
                "missing_evidence": "Approval record",
                "contradicted_by_sources": ["ai_usage_policy.md"],
            }
        ]
    }
    objections = await generate_objections(claims, witness, sources)
    assert len(objections) == 1


@pytest.mark.asyncio
@patch("hallucination_tribunal.tribunal.agents._call_llm_with_retry", new_callable=AsyncMock)
async def test_generate_objections_null_contradicted_sources(mock_llm, sources):
    claims = [
        Claim(claim_id="claim-1", claim_text="All LLM APIs are always allowed.", extracted_from_sentence="")
    ]
    witness = WitnessAnswer(answer_text="All LLM APIs are always allowed.", citations=[])
    mock_llm.return_value = {
        "objections": [
            {
                "claim_id": "claim-1",
                "objection_type": "unsupported",
                "explanation": "Policy requires approval.",
                "missing_evidence": "Approval record",
                "contradicted_by_sources": None,
            }
        ]
    }
    objections = await generate_objections(claims, witness, sources)
    assert len(objections) == 1
    assert objections[0].contradicted_by_sources == []


@pytest.mark.asyncio
@patch("hallucination_tribunal.tribunal.agents._call_llm_with_retry", new_callable=AsyncMock)
async def test_generate_verdicts(mock_llm, sources):
    claims = [Claim(claim_id="claim-1", claim_text="Approval required.", extracted_from_sentence="")]
    witness = WitnessAnswer(answer_text="Approval required.", citations=[])
    objections = [
        ProsecutorObjection(
            claim_id="claim-1",
            objection_type="none",
            explanation="Supported by evidence.",
        )
    ]
    mock_llm.return_value = {
        "verdicts": [
            {
                "claim_id": "claim-1",
                "verdict": "Supported",
                "confidence": 0.95,
                "explanation": "Directly supported.",
                "supporting_sources": ["ai_usage_policy.md"],
                "recommended_revision": None,
            }
        ]
    }
    verdicts = await generate_verdicts(claims, objections, witness, sources)
    assert verdicts[0].verdict == Verdict.SUPPORTED


@pytest.mark.asyncio
@patch("hallucination_tribunal.tribunal.agents._call_llm_with_retry", new_callable=AsyncMock)
async def test_revise_final_answer(mock_llm):
    witness = WitnessAnswer(answer_text="Original answer.", citations=[])
    verdicts = [
        JudgeVerdict(
            claim_id="c1",
            verdict=Verdict.SUPPORTED,
            confidence=0.9,
            explanation="ok",
        )
    ]
    claims = [Claim(claim_id="c1", claim_text="Original answer.", extracted_from_sentence="")]
    mock_llm.return_value = {"final_answer": "Revised answer with citation [Policy, p. 1]"}
    result = await revise_final_answer(witness, verdicts, claims)
    assert "Revised answer" in result
