from pathlib import Path

import pytest

from hallucination_tribunal.documents.chunker import chunk_segments, estimate_tokens
from hallucination_tribunal.documents.extractors import ExtractedSegment, TextExtractor


def test_estimate_tokens():
    assert estimate_tokens("hello world") == 2


def test_chunk_segments_creates_multiple_chunks():
    long_text = "word " * 500
    segments = [ExtractedSegment(text=long_text, page=1)]
    chunks = chunk_segments(segments, "doc-1")
    assert len(chunks) > 1
    assert chunks[0].document_id == "doc-1"
    assert chunks[0].source_page == 1


def test_extract_plain_text(tmp_path: Path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello tribunal world", encoding="utf-8")
    segments = TextExtractor.extract(file_path, "txt")
    assert len(segments) == 1
    assert "tribunal" in segments[0].text


def test_extract_html(tmp_path: Path):
    file_path = tmp_path / "sample.html"
    file_path.write_text("<html><body><p>Policy text</p></body></html>", encoding="utf-8")
    segments = TextExtractor.extract(file_path, "html")
    assert len(segments) == 1
    assert "Policy text" in segments[0].text


def test_unsupported_type():
    assert not TextExtractor.is_supported("exe")
