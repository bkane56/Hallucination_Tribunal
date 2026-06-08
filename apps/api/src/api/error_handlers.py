import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core.exceptions import TribunalError
from src.models.common import ErrorDetail, ErrorResponse

logger = logging.getLogger(__name__)


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(TribunalError)
    async def tribunal_error_handler(
        _request: Request, exc: TribunalError
    ) -> JSONResponse:
        logger.warning("Tribunal error: %s", exc.message, extra={"code": exc.code})
        payload = ErrorResponse(
            error=ErrorDetail(
                code=exc.code,
                message=exc.message,
                details={k: str(v) for k, v in exc.details.items()}
                if exc.details
                else None,
            )
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=payload.model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        payload = ErrorResponse(
            error=ErrorDetail(
                code="request_validation_error",
                message="Request validation failed.",
                details={"errors": str(exc.errors())},
            )
        )
        return JSONResponse(status_code=422, content=payload.model_dump())

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        _request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        payload = ErrorResponse(
            error=ErrorDetail(
                code="http_error",
                message=str(exc.detail),
            )
        )
        return JSONResponse(status_code=exc.status_code, content=payload.model_dump())
