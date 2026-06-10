"""Tribunal agent stages."""

import json
from typing import Any
from uuid import uuid4

from pydantic import ValidationError

from hallucination_tribunal.core.logging import get_logger
from hallucination_tribunal.core.providers.ollama_llm import get_llm_provider
from hallucination_tribunal.models.domain import (
    Citation,
    Claim,
    JudgeVerdict,
    ProsecutorObjection,
    RetrievedSource,
    Verdict,
    WitnessAnswer,
)
from hallucination_tribunal.tribunal.prompts import format_context, load_prompt

logger = get_logger(__name__)


async def _call_llm_with_retry(
    prompt_name: str,
    user_content: str,
    schema: dict[str, Any],
) -> dict[str, Any]:
    prompt = load_prompt(prompt_name)
    llm = get_llm_provider()
    system = prompt["system"]
    try:
        return await llm.generate_structured(system, user_content, schema)
    except (json.JSONDecodeError, ValidationError, KeyError) as first_error:
        logger.warning("llm_retry", prompt=prompt_name, error=str(first_error))
        retry_content = (
            f"{user_content}\n\nIMPORTANT: Respond with valid JSON only."
        )
        return await llm.generate_structured(system, retry_content, schema)


async def generate_witness_answer(
    question: str,
    sources: list[RetrievedSource],
) -> WitnessAnswer:
    if not sources:
        return WitnessAnswer(
            answer_text="The provided documents do not contain enough evidence to answer this question.",
            citations=[],
            uncertainty_notes="No evidence was retrieved from the document corpus.",
        )

    context = format_context(sources)
    user_content = f"Question: {question}\n\nRetrieved Evidence:\n{context}"
    schema = load_prompt("witness")["output_schema"]

    data = await _call_llm_with_retry("witness", user_content, schema)
    citations = [
        Citation(
            document_name=c.get("document_name", ""),
            page_number=c.get("page_number"),
            section_title=c.get("section_title"),
            chunk_id=c.get("chunk_id"),
        )
        for c in data.get("citations", [])
    ]
    return WitnessAnswer(
        answer_text=data.get("answer_text", ""),
        citations=citations,
        uncertainty_notes=data.get("uncertainty_notes"),
    )


async def extract_claims(
    witness: WitnessAnswer,
    sources: list[RetrievedSource],
) -> list[Claim]:
    context = format_context(sources)
    user_content = (
        f"Witness Answer:\n{witness.answer_text}\n\n"
        f"Retrieved Evidence:\n{context}"
    )
    schema = load_prompt("claim_extraction")["output_schema"]
    data = await _call_llm_with_retry("claim_extraction", user_content, schema)

    claims: list[Claim] = []
    for item in data.get("claims") or []:
        claims.append(
            Claim.model_validate(
                {
                    "claim_id": str(uuid4()),
                    "claim_text": item.get("claim_text", ""),
                    "claim_type": item.get("claim_type", "factual"),
                    "cited_sources": item.get("cited_sources"),
                    "extracted_from_sentence": item.get("extracted_from_sentence", ""),
                }
            )
        )
    return claims


async def generate_objections(
    claims: list[Claim],
    witness: WitnessAnswer,
    sources: list[RetrievedSource],
) -> list[ProsecutorObjection]:
    if not claims:
        return []

    context = format_context(sources)
    claims_text = json.dumps([c.model_dump() for c in claims], indent=2)
    user_content = (
        f"Witness Answer:\n{witness.answer_text}\n\n"
        f"Claims:\n{claims_text}\n\n"
        f"Retrieved Evidence:\n{context}"
    )
    schema = load_prompt("prosecutor")["output_schema"]
    data = await _call_llm_with_retry("prosecutor", user_content, schema)

    objections: list[ProsecutorObjection] = []
    default_claim_id = claims[0].claim_id
    for item in data.get("objections") or []:
        objections.append(
            ProsecutorObjection.model_validate(
                {
                    "objection_id": str(uuid4()),
                    "claim_id": item.get("claim_id") or default_claim_id,
                    "objection_type": item.get("objection_type", "unsupported"),
                    "explanation": item.get("explanation", ""),
                    "missing_evidence": item.get("missing_evidence"),
                    "contradicted_by_sources": item.get("contradicted_by_sources"),
                }
            )
        )
    return objections


async def generate_verdicts(
    claims: list[Claim],
    objections: list[ProsecutorObjection],
    witness: WitnessAnswer,
    sources: list[RetrievedSource],
) -> list[JudgeVerdict]:
    if not claims:
        return []

    context = format_context(sources)
    claims_text = json.dumps([c.model_dump() for c in claims], indent=2)
    objections_text = json.dumps([o.model_dump() for o in objections], indent=2)
    user_content = (
        f"Witness Answer:\n{witness.answer_text}\n\n"
        f"Claims:\n{claims_text}\n\n"
        f"Prosecutor Objections:\n{objections_text}\n\n"
        f"Retrieved Evidence:\n{context}"
    )
    schema = load_prompt("judge")["output_schema"]
    data = await _call_llm_with_retry("judge", user_content, schema)

    claim_map = {c.claim_id: c for c in claims}
    verdicts: list[JudgeVerdict] = []
    for item in data.get("verdicts", []):
        claim_id = item.get("claim_id", "")
        if claim_id not in claim_map and claims:
            claim_id = claims[len(verdicts) % len(claims)].claim_id
        try:
            verdict = Verdict(item.get("verdict", Verdict.NOT_ENOUGH_EVIDENCE.value))
        except ValueError:
            verdict = Verdict.NOT_ENOUGH_EVIDENCE
        verdicts.append(
            JudgeVerdict.model_validate(
                {
                    "claim_id": claim_id,
                    "verdict": verdict,
                    "confidence": float(item.get("confidence", 0.5)),
                    "explanation": item.get("explanation", ""),
                    "supporting_sources": item.get("supporting_sources"),
                    "recommended_revision": item.get("recommended_revision"),
                }
            )
        )
    return verdicts


async def revise_final_answer(
    witness: WitnessAnswer,
    verdicts: list[JudgeVerdict],
    claims: list[Claim],
) -> str:
    claims_text = json.dumps([c.model_dump() for c in claims], indent=2)
    verdicts_text = json.dumps(
        [v.model_dump(mode="json") for v in verdicts], indent=2
    )
    user_content = (
        f"Original Witness Answer:\n{witness.answer_text}\n\n"
        f"Claims:\n{claims_text}\n\n"
        f"Judge Verdicts:\n{verdicts_text}"
    )
    schema = load_prompt("final_revision")["output_schema"]
    data = await _call_llm_with_retry("final_revision", user_content, schema)
    return data.get("final_answer", witness.answer_text)
