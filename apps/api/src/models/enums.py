from enum import StrEnum


class Verdict(StrEnum):
    SUPPORTED = "Supported"
    PARTIALLY_SUPPORTED = "Partially Supported"
    UNSUPPORTED = "Unsupported"
    CONTRADICTED = "Contradicted"
    NOT_ENOUGH_EVIDENCE = "Not Enough Evidence"


class OverallVerdict(StrEnum):
    ACCEPTED = "Accepted"
    REVISED = "Revised"
    REJECTED = "Rejected"


class ClaimType(StrEnum):
    FACTUAL = "factual"
    INFERENCE = "inference"
    PROCEDURAL = "procedural"
    QUANTITATIVE = "quantitative"


class ObjectionType(StrEnum):
    UNSUPPORTED = "unsupported"
    EXAGGERATED = "exaggerated"
    VAGUE = "vague"
    CONTRADICTED = "contradicted"
    MIS_CITED = "mis_cited"


class DocumentStatus(StrEnum):
    PENDING = "pending"
    INDEXING = "indexing"
    INDEXED = "indexed"
    FAILED = "failed"


class FileType(StrEnum):
    PDF = "pdf"
    MARKDOWN = "markdown"
    TXT = "txt"
    DOCX = "docx"
    HTML = "html"
