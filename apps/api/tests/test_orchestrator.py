from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from hallucination_tribunal.core.providers.simple_embedding import SimpleEmbeddingProvider
from hallucination_tribunal.models.domain import (
    Claim,
    JudgeVerdict,
    ProsecutorObjection,
    Verdict,
    WitnessAnswer,
)
from hallucination_tribunal.tribunal.orchestrator import TribunalOrchestrator


def test_simple_embedding_provider():
    provider = SimpleEmbeddingProvider(dimension=8)
    vectors = provider.embed_texts(["hello world", "policy approval"])
    assert len(vectors) == 2
    assert len(vectors[0]) == 8
    query = provider.embed_query("hello")
    assert len(query) == 8


@pytest.mark.asyncio
@patch("hallucination_tribunal.tribunal.orchestrator.revise_final_answer", new_callable=AsyncMock)
@patch("hallucination_tribunal.tribunal.orchestrator.generate_verdicts", new_callable=AsyncMock)
@patch("hallucination_tribunal.tribunal.orchestrator.generate_objections", new_callable=AsyncMock)
@patch("hallucination_tribunal.tribunal.orchestrator.extract_claims", new_callable=AsyncMock)
@patch("hallucination_tribunal.tribunal.orchestrator.generate_witness_answer", new_callable=AsyncMock)
@patch("hallucination_tribunal.tribunal.orchestrator.RetrievalService")
async def test_orchestrator_run(
    mock_retrieval_cls,
    mock_witness,
    mock_claims,
    mock_objections,
    mock_verdicts,
    mock_revise,
):
    from hallucination_tribunal.models.domain import Citation, RetrievedSource

    mock_retrieval = MagicMock()
    mock_retrieval.retrieve = AsyncMock(
        return_value=[
            RetrievedSource(
                chunk_id="c1",
                document_id="d1",
                filename="policy.md",
                text="Approval required.",
                similarity_score=0.9,
            )
        ]
    )
    mock_retrieval_cls.return_value = mock_retrieval

    mock_witness.return_value = WitnessAnswer(
        answer_text="Approval is required.",
        citations=[Citation(document_name="policy.md")],
    )
    mock_claims.return_value = [
        Claim(claim_id="claim-1", claim_text="Approval is required.", extracted_from_sentence="")
    ]
    mock_objections.return_value = [
        ProsecutorObjection(
            claim_id="claim-1",
            objection_type="none",
            explanation="Supported.",
        )
    ]
    mock_verdicts.return_value = [
        JudgeVerdict(
            claim_id="claim-1",
            verdict=Verdict.SUPPORTED,
            confidence=0.95,
            explanation="Supported by policy.",
        )
    ]
    mock_revise.return_value = "Final answer with approval requirement."

    orchestrator = TribunalOrchestrator()
    result = await orchestrator.run("Are external APIs allowed?")

    assert result.final_answer == "Final answer with approval requirement."
    assert result.reliability_score == 1.0
