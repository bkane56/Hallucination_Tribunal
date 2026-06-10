"""Tribunal orchestration pipeline."""

import time

from hallucination_tribunal.core.db import get_database
from hallucination_tribunal.core.logging import get_logger
from hallucination_tribunal.models.domain import TribunalResult, Verdict
from hallucination_tribunal.retrieval.service import RetrievalService
from hallucination_tribunal.tribunal.agents import (
    extract_claims,
    generate_objections,
    generate_verdicts,
    generate_witness_answer,
    revise_final_answer,
)
from hallucination_tribunal.tribunal.scoring import (
    compute_overall_verdict,
    compute_reliability_score,
)

logger = get_logger(__name__)


class TribunalOrchestrator:
    def __init__(self):
        self.retrieval = RetrievalService()
        self.db = get_database()

    async def run(
        self,
        question: str,
        document_ids: list[str] | None = None,
        top_k: int = 6,
    ) -> TribunalResult:
        start = time.perf_counter()

        sources = await self.retrieval.retrieve(
            question, top_k=top_k, document_ids=document_ids
        )
        logger.info(
            "retrieval_complete",
            chunk_count=len(sources),
            latency_ms=round((time.perf_counter() - start) * 1000, 2),
        )

        witness_start = time.perf_counter()
        witness = await generate_witness_answer(question, sources)
        logger.info(
            "witness_complete",
            latency_ms=round((time.perf_counter() - witness_start) * 1000, 2),
        )

        claims_start = time.perf_counter()
        claims = await extract_claims(witness, sources)
        logger.info(
            "claims_extracted",
            claim_count=len(claims),
            latency_ms=round((time.perf_counter() - claims_start) * 1000, 2),
        )

        prosecutor_start = time.perf_counter()
        objections = await generate_objections(claims, witness, sources)
        logger.info(
            "prosecutor_complete",
            objection_count=len(objections),
            latency_ms=round((time.perf_counter() - prosecutor_start) * 1000, 2),
        )

        judge_start = time.perf_counter()
        verdicts = await generate_verdicts(claims, objections, witness, sources)
        logger.info(
            "judge_complete",
            verdict_count=len(verdicts),
            latency_ms=round((time.perf_counter() - judge_start) * 1000, 2),
        )

        final_answer = await revise_final_answer(witness, verdicts, claims)
        reliability = compute_reliability_score(verdicts)
        overall = compute_overall_verdict(verdicts)

        result = TribunalResult(
            question=question,
            final_answer=final_answer,
            overall_verdict=overall,
            reliability_score=reliability,
            retrieved_sources=sources,
            witness_answer=witness,
            claims=claims,
            prosecutor_objections=objections,
            judge_verdicts=verdicts,
        )

        await self.db.save_tribunal_result(result)
        logger.info(
            "tribunal_complete",
            tribunal_result_id=result.tribunal_result_id,
            reliability_score=str(reliability),
            overall_verdict=str(overall),
            latency_ms=round((time.perf_counter() - start) * 1000, 2),
        )
        return result
