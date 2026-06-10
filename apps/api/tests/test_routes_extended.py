from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.mark.asyncio
@patch("hallucination_tribunal.api.routes.TribunalOrchestrator")
async def test_ask_tribunal(mock_orchestrator_cls, client):
    from datetime import datetime

    from hallucination_tribunal.models.domain import Verdict, WitnessAnswer

    mock_result = MagicMock()
    mock_result.tribunal_result_id = "t1"
    mock_result.question = "test?"
    mock_result.final_answer = "Answer"
    mock_result.overall_verdict = Verdict.SUPPORTED
    mock_result.reliability_score = 1.0
    mock_result.retrieved_sources = []
    mock_result.witness_answer = WitnessAnswer(answer_text="Answer", citations=[])
    mock_result.claims = []
    mock_result.prosecutor_objections = []
    mock_result.judge_verdicts = []
    mock_result.created_at = datetime.utcnow()

    mock_orchestrator = AsyncMock()
    mock_orchestrator.run.return_value = mock_result
    mock_orchestrator_cls.return_value = mock_orchestrator

    response = await client.post(
        "/tribunal/ask",
        json={"question": "test?", "top_k": 3},
    )
    assert response.status_code == 200
    assert response.json()["final_answer"] == "Answer"


@pytest.mark.asyncio
@patch("hallucination_tribunal.api.routes.EvaluationService")
async def test_run_evaluations(mock_service_cls, client):
    from datetime import datetime

    mock_service = MagicMock()
    mock_service.run_evaluations = AsyncMock(
        return_value={
            "run_id": "r1",
            "started_at": datetime.utcnow(),
            "completed_at": datetime.utcnow(),
            "aggregate_metrics": {"pass_rate": 1.0},
            "case_results": [],
        }
    )
    mock_service_cls.return_value = mock_service

    response = await client.post("/evaluations/run")
    assert response.status_code == 200
    assert response.json()["run_id"] == "r1"
