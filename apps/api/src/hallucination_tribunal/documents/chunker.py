"""Document chunking utilities."""

from hallucination_tribunal.core.config import get_settings
from hallucination_tribunal.documents.extractors import ExtractedSegment
from hallucination_tribunal.models.domain import Chunk


def estimate_tokens(text: str) -> int:
    return max(1, len(text.split()))


def chunk_segments(
    segments: list[ExtractedSegment],
    document_id: str,
) -> list[Chunk]:
    settings = get_settings()
    chunk_size = settings.chunk_size
    chunk_overlap = settings.chunk_overlap

    chunks: list[Chunk] = []
    chunk_index = 0

    for segment in segments:
        text = segment.text
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(
                    Chunk(
                        document_id=document_id,
                        chunk_index=chunk_index,
                        text=chunk_text,
                        token_count=estimate_tokens(chunk_text),
                        source_page=segment.page,
                        source_section=segment.section,
                        metadata={
                            "source_page": segment.page,
                            "source_section": segment.section,
                        },
                    )
                )
                chunk_index += 1
            if end >= len(text):
                break
            start = max(end - chunk_overlap, start + 1)

    return chunks
