"""Text extraction from uploaded documents."""

from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup
from docx import Document as DocxDocument
from pypdf import PdfReader


@dataclass
class ExtractedSegment:
    text: str
    page: int | None = None
    section: str | None = None


class TextExtractor:
    SUPPORTED_TYPES = {"pdf", "md", "txt", "docx", "html"}

    @classmethod
    def is_supported(cls, file_type: str) -> bool:
        return file_type.lower() in cls.SUPPORTED_TYPES

    @classmethod
    def extract(cls, file_path: Path, file_type: str) -> list[ExtractedSegment]:
        file_type = file_type.lower()
        if file_type == "pdf":
            return cls._extract_pdf(file_path)
        if file_type in {"md", "txt"}:
            return cls._extract_plain(file_path)
        if file_type == "docx":
            return cls._extract_docx(file_path)
        if file_type == "html":
            return cls._extract_html(file_path)
        raise ValueError(f"Unsupported file type: {file_type}")

    @staticmethod
    def _extract_pdf(file_path: Path) -> list[ExtractedSegment]:
        reader = PdfReader(str(file_path))
        segments: list[ExtractedSegment] = []
        for i, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                segments.append(ExtractedSegment(text=text.strip(), page=i))
        return segments

    @staticmethod
    def _extract_plain(file_path: Path) -> list[ExtractedSegment]:
        text = file_path.read_text(encoding="utf-8", errors="replace")
        if not text.strip():
            return []
        return [ExtractedSegment(text=text.strip())]

    @staticmethod
    def _extract_docx(file_path: Path) -> list[ExtractedSegment]:
        doc = DocxDocument(str(file_path))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        if not paragraphs:
            return []
        return [ExtractedSegment(text="\n".join(paragraphs))]

    @staticmethod
    def _extract_html(file_path: Path) -> list[ExtractedSegment]:
        html = file_path.read_text(encoding="utf-8", errors="replace")
        soup = BeautifulSoup(html, "lxml")
        for tag in soup(["script", "style"]):
            tag.decompose()
        text = soup.get_text(separator="\n")
        if not text.strip():
            return []
        return [ExtractedSegment(text=text.strip())]
