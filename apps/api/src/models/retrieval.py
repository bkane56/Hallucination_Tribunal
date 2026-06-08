from pydantic import BaseModel, Field


class RetrievedSource(BaseModel):
    chunk_id: str
    document_id: str
    filename: str
    page_number: int | None = None
    section_title: str | None = None
    text: str
    similarity_score: float = Field(ge=0.0, le=1.0)


class RetrievalQuery(BaseModel):
    question: str = Field(min_length=1)
    document_ids: list[str] | None = None
    top_k: int = Field(default=6, ge=1, le=20)
