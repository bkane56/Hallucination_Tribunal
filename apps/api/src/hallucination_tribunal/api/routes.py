"""API route handlers."""

from datetime import datetime

from fastapi import APIRouter, File, HTTPException, UploadFile

from hallucination_tribunal import __version__
from hallucination_tribunal.core.config import get_settings
from hallucination_tribunal.documents.service import DocumentService
from hallucination_tribunal.evaluations.service import EvaluationService
from hallucination_tribunal.models.schemas import (
    DocumentListResponse,
    DocumentResponse,
    DocumentUploadResponse,
    EvaluationRunResponse,
    EvaluationRunsListResponse,
    HealthResponse,
    SampleDocumentImportRequest,
    SampleDocumentImportResponse,
    SampleDocumentImportResult,
    SampleDocumentListResponse,
    SampleDocumentResponse,
    TribunalAskRequest,
    TribunalAskResponse,
)
from hallucination_tribunal.tribunal.orchestrator import TribunalOrchestrator

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="ok", version=__version__)


@router.get("/health/ready")
async def readiness_check():
    settings = get_settings()
    directories = settings.ensure_data_directories()
    return {
        "status": "ready",
        "version": __version__,
        "environment": settings.app_env,
        "providers": {
            "llm": settings.llm_provider,
            "embedding": settings.embedding_provider,
            "vector_db": settings.vector_db_provider,
            "serverless": settings.is_serverless,
        },
        "directories_ready": all(path.exists() for path in directories),
    }


@router.post("/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    service = DocumentService()
    try:
        doc = await service.upload_document(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc), headers={"X-Error-Code": "VALIDATION_ERROR"}) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc), headers={"X-Error-Code": "INGESTION_ERROR"}) from exc

    return DocumentUploadResponse(
        document_id=doc.document_id,
        filename=doc.filename,
        status=doc.status.value,
        chunk_count=doc.chunk_count,
    )


@router.get("/documents/samples", response_model=SampleDocumentListResponse)
async def list_sample_documents():
    service = DocumentService()
    existing_filenames = {doc.filename for doc in await service.list_documents()}
    samples = []
    categories: list[str] = []
    for sample in service.list_sample_documents():
        if sample.category not in categories:
            categories.append(sample.category)
        samples.append(
            SampleDocumentResponse(
                sample_id=sample.sample_id,
                title=sample.title,
                category=sample.category,
                source=sample.source,
                url=sample.url,
                description=sample.description,
                good_for=sample.good_for,
                filename=sample.filename,
                already_imported=sample.filename in existing_filenames,
            )
        )
    return SampleDocumentListResponse(samples=samples, categories=categories)


@router.post("/documents/samples/import", response_model=SampleDocumentImportResponse)
async def import_sample_documents(request: SampleDocumentImportRequest):
    service = DocumentService()
    result = await service.import_sample_documents(request.sample_ids)

    imported: list[SampleDocumentImportResult] = []
    for item in result["imported"]:
        doc = item["document"]
        imported.append(
            SampleDocumentImportResult(
                sample_id=str(item["sample_id"]),
                document_id=doc.document_id,
                filename=doc.filename,
                status=doc.status.value,
                chunk_count=doc.chunk_count,
            )
        )

    skipped: list[SampleDocumentImportResult] = []
    for item in result["skipped"]:
        doc = item["document"]
        skipped.append(
            SampleDocumentImportResult(
                sample_id=str(item["sample_id"]),
                document_id=doc.document_id,
                filename=doc.filename,
                status="skipped",
                chunk_count=doc.chunk_count,
                message="Already in corpus",
            )
        )
    errors = [
        SampleDocumentImportResult(
            sample_id=err["sample_id"],
            status="error",
            message=err["error"],
        )
        for err in result["errors"]
    ]
    return SampleDocumentImportResponse(imported=imported, skipped=skipped, errors=errors)


@router.get("/documents", response_model=DocumentListResponse)
async def list_documents():
    service = DocumentService()
    docs = await service.list_documents()
    return DocumentListResponse(
        documents=[
            DocumentResponse(
                document_id=d.document_id,
                filename=d.filename,
                file_type=d.file_type,
                chunk_count=d.chunk_count,
                status=d.status,
                error_message=d.error_message,
                created_at=d.created_at,
                updated_at=d.updated_at,
            )
            for d in docs
        ]
    )


@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str):
    service = DocumentService()
    doc = await service.get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return DocumentResponse(
        document_id=doc.document_id,
        filename=doc.filename,
        file_type=doc.file_type,
        chunk_count=doc.chunk_count,
        status=doc.status,
        error_message=doc.error_message,
        created_at=doc.created_at,
        updated_at=doc.updated_at,
    )


@router.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    service = DocumentService()
    deleted = await service.delete_document(document_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"status": "deleted", "document_id": document_id}


@router.post("/documents/rebuild-index")
async def rebuild_index():
    service = DocumentService()
    result = await service.rebuild_index()
    return result


@router.post("/tribunal/ask", response_model=TribunalAskResponse)
async def ask_tribunal(request: TribunalAskRequest):
    orchestrator = TribunalOrchestrator()
    try:
        result = await orchestrator.run(
            question=request.question,
            document_ids=request.document_ids,
            top_k=request.top_k,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Tribunal pipeline failed ({type(exc).__name__}): {exc}",
            headers={"X-Error-Code": "TRIBUNAL_ERROR"},
        ) from exc

    return TribunalAskResponse(
        tribunal_result_id=result.tribunal_result_id,
        question=result.question,
        final_answer=result.final_answer,
        overall_verdict=result.overall_verdict,
        reliability_score=result.reliability_score,
        retrieved_sources=result.retrieved_sources,
        witness_answer=result.witness_answer,
        claims=result.claims,
        prosecutor_objections=result.prosecutor_objections,
        judge_verdict=result.judge_verdicts,
        created_at=result.created_at,
    )


@router.get("/tribunal/results/{tribunal_result_id}", response_model=TribunalAskResponse)
async def get_tribunal_result(tribunal_result_id: str):
    from hallucination_tribunal.core.db import get_database

    db = get_database()
    result = await db.get_tribunal_result(tribunal_result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Tribunal result not found")
    return TribunalAskResponse(
        tribunal_result_id=result.tribunal_result_id,
        question=result.question,
        final_answer=result.final_answer,
        overall_verdict=result.overall_verdict,
        reliability_score=result.reliability_score,
        retrieved_sources=result.retrieved_sources,
        witness_answer=result.witness_answer,
        claims=result.claims,
        prosecutor_objections=result.prosecutor_objections,
        judge_verdict=result.judge_verdicts,
        created_at=result.created_at,
    )


@router.post("/evaluations/run", response_model=EvaluationRunResponse)
async def run_evaluations():
    service = EvaluationService()
    try:
        result = await service.run_evaluations()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return EvaluationRunResponse(
        run_id=result["run_id"],
        started_at=result["started_at"],
        completed_at=result["completed_at"],
        aggregate_metrics=result["aggregate_metrics"],
        case_results=result["case_results"],
    )


@router.get("/evaluations/runs", response_model=EvaluationRunsListResponse)
async def list_evaluation_runs():
    from hallucination_tribunal.core.db import get_database

    db = get_database()
    runs = await db.list_evaluation_runs()
    return EvaluationRunsListResponse(
        runs=[
            EvaluationRunResponse(
                run_id=r["run_id"],
                started_at=datetime.fromisoformat(r["started_at"]),
                completed_at=datetime.fromisoformat(r["completed_at"]),
                aggregate_metrics=r["aggregate_metrics"],
                case_results=r["case_results"],
            )
            for r in runs
        ]
    )


@router.get("/evaluations/runs/{run_id}", response_model=EvaluationRunResponse)
async def get_evaluation_run(run_id: str):
    from hallucination_tribunal.core.db import get_database

    db = get_database()
    run = await db.get_evaluation_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Evaluation run not found")
    return EvaluationRunResponse(
        run_id=run["run_id"],
        started_at=datetime.fromisoformat(run["started_at"]),
        completed_at=datetime.fromisoformat(run["completed_at"]),
        aggregate_metrics=run["aggregate_metrics"],
        case_results=run["case_results"],
    )
