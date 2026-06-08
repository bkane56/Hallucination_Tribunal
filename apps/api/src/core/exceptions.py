from typing import Any


class TribunalError(Exception):
    """Base exception for domain errors."""

    code: str = "tribunal_error"
    status_code: int = 500

    def __init__(
        self,
        message: str,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.details = details


class ValidationError(TribunalError):
    code = "validation_error"
    status_code = 422


class NotFoundError(TribunalError):
    code = "not_found"
    status_code = 404


class UnsupportedFileTypeError(ValidationError):
    code = "unsupported_file_type"


class FileTooLargeError(ValidationError):
    code = "file_too_large"


class EmptyDocumentError(ValidationError):
    code = "empty_document"


class TextExtractionError(TribunalError):
    code = "text_extraction_failed"
    status_code = 422


class IngestionError(TribunalError):
    code = "ingestion_failed"


class RetrievalError(TribunalError):
    code = "retrieval_failed"


class LLMError(TribunalError):
    code = "llm_error"


class ProviderNotConfiguredError(TribunalError):
    code = "provider_not_configured"
    status_code = 503
