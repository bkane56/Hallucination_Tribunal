from pydantic import BaseModel, Field


class Citation(BaseModel):
    chunk_id: str
    document_id: str
    filename: str
    page_number: int | None = None
    section_title: str | None = None
    display_text: str = Field(
        description="User-facing citation, e.g. [AI Policy Handbook, p. 4]"
    )


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: dict[str, str] | None = None


class ErrorResponse(BaseModel):
    error: ErrorDetail
