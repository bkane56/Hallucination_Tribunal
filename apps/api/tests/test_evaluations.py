import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from hallucination_tribunal.evaluations.service import EvaluationService


@pytest.mark.asyncio
@patch("hallucination_tribunal.evaluations.service.TribunalOrchestrator")
async def test_evaluation_service_run(mock_orchestrator_cls, tmp_path, monkeypatch):
    from hallucination_tribunal.core.config import get_settings

    get_settings.cache_clear()
    monkeypatch.setenv("SQLITE_DATABASE_PATH", str(tmp_path / "test.db"))

    mock_result = MagicMock()
    mock_result.reliability_score = 0.8
    mock_result.final_answer = "The provided documents do not contain enough evidence"
    mock_result.retrieved_sources = []
    mock_result.witness_answer = MagicMock(citations=[])
    mock_result.claims = []
    mock_result.judge_verdicts = []

    mock_orchestrator = AsyncMock()
    mock_orchestrator.run.return_value = mock_result
    mock_orchestrator_cls.return_value = mock_orchestrator

    eval_dir = tmp_path / "evals"
    eval_dir.mkdir()
    (eval_dir / "test_cases.json").write_text(
        '[{"id":"t1","question":"test?","expected_source_document":"policy","expected_verdict_behavior":"refuse"}]',
        encoding="utf-8",
    )

    service = EvaluationService()
    service.eval_dir = eval_dir
    result = await service.run_evaluations()

    assert result["run_id"]
    assert result["aggregate_metrics"]["total_cases"] == 1
