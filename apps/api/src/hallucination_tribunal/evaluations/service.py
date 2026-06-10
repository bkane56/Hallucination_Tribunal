"""Evaluation service."""

import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from hallucination_tribunal.core.config import get_settings
from hallucination_tribunal.core.db import get_database
from hallucination_tribunal.core.logging import get_logger
from hallucination_tribunal.models.domain import Verdict
from hallucination_tribunal.models.schemas import EvaluationCaseResult
from hallucination_tribunal.tribunal.orchestrator import TribunalOrchestrator

logger = get_logger(__name__)


class EvaluationService:
    def __init__(self):
        self.settings = get_settings()
        self.db = get_database()
        self.orchestrator = TribunalOrchestrator()
        self.eval_dir = self.settings.resolve_path("./data/evals")

    def load_test_cases(self) -> list[dict]:
        path = self.eval_dir / "test_cases.json"
        if not path.exists():
            return []
        return json.loads(path.read_text(encoding="utf-8"))

    async def run_evaluations(self) -> dict:
        cases = self.load_test_cases()
        if not cases:
            raise ValueError("No evaluation test cases found")

        run_id = str(uuid4())
        started_at = datetime.utcnow()
        case_results: list[EvaluationCaseResult] = []

        for case in cases:
            result = await self._run_case(case)
            case_results.append(result)

        completed_at = datetime.utcnow()
        aggregate = self._aggregate_metrics(case_results)

        await self.db.save_evaluation_run(
            run_id,
            started_at,
            completed_at,
            aggregate,
            [c.model_dump(mode="json") for c in case_results],
        )

        logger.info("evaluation_run_complete", run_id=run_id, **aggregate)
        return {
            "run_id": run_id,
            "started_at": started_at,
            "completed_at": completed_at,
            "aggregate_metrics": aggregate,
            "case_results": case_results,
        }

    async def _run_case(self, case: dict) -> EvaluationCaseResult:
        question = case["question"]
        expected_source = case.get("expected_source_document", "")
        expected_behavior = case.get("expected_verdict_behavior", "")

        result = await self.orchestrator.run(question)

        retrieval_hit = any(
            expected_source.lower() in src.filename.lower()
            for src in result.retrieved_sources
        ) if expected_source else True

        citation_accuracy = 0.0
        if result.witness_answer.citations:
            citation_accuracy = min(
                1.0,
                len(result.witness_answer.citations) / max(len(result.claims), 1),
            )

        unsupported = sum(
            1 for v in result.judge_verdicts if v.verdict == Verdict.UNSUPPORTED
        )
        contradicted = sum(
            1 for v in result.judge_verdicts if v.verdict == Verdict.CONTRADICTED
        )

        passed = self._evaluate_pass(
            case, result, retrieval_hit, unsupported, contradicted
        )

        return EvaluationCaseResult(
            case_id=case.get("id", question[:20]),
            question=question,
            retrieval_hit=retrieval_hit,
            citation_accuracy=round(citation_accuracy, 2),
            unsupported_claim_count=unsupported,
            contradicted_claim_count=contradicted,
            reliability_score=result.reliability_score,
            expected_verdict_behavior=expected_behavior,
            passed=passed,
        )

    def _evaluate_pass(
        self,
        case: dict,
        result,
        retrieval_hit: bool,
        unsupported: int,
        contradicted: int,
    ) -> bool:
        behavior = case.get("expected_verdict_behavior", "")
        if behavior == "refuse":
            return "not contain enough evidence" in result.final_answer.lower()
        if behavior == "grounded":
            return retrieval_hit and contradicted == 0
        if behavior == "catch_unsupported":
            return unsupported > 0 or result.reliability_score != "Not Applicable"
        return retrieval_hit

    def _aggregate_metrics(
        self, case_results: list[EvaluationCaseResult]
    ) -> dict:
        total = len(case_results)
        if total == 0:
            return {}
        return {
            "total_cases": total,
            "passed_cases": sum(1 for c in case_results if c.passed),
            "pass_rate": round(
                sum(1 for c in case_results if c.passed) / total, 2
            ),
            "retrieval_hit_rate": round(
                sum(1 for c in case_results if c.retrieval_hit) / total, 2
            ),
            "avg_citation_accuracy": round(
                sum(c.citation_accuracy for c in case_results) / total, 2
            ),
            "total_unsupported_claims": sum(
                c.unsupported_claim_count for c in case_results
            ),
            "total_contradicted_claims": sum(
                c.contradicted_claim_count for c in case_results
            ),
            "verdict_distribution": self._verdict_distribution(case_results),
        }

    @staticmethod
    def _verdict_distribution(case_results: list[EvaluationCaseResult]) -> dict:
        return {
            "passed": sum(1 for c in case_results if c.passed),
            "failed": sum(1 for c in case_results if not c.passed),
        }
