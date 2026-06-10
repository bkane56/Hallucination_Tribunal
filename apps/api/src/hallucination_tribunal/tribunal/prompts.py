"""Prompt template loading."""

from pathlib import Path

import yaml


def load_prompt(name: str) -> dict:
    prompts_dir = Path(__file__).resolve().parent.parent / "prompts"
    path = prompts_dir / f"{name}.yaml"
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def format_context(sources: list) -> str:
    if not sources:
        return "No retrieved evidence available."
    parts = []
    for i, src in enumerate(sources, 1):
        page = f", page {src.page_number}" if src.page_number else ""
        section = f", section: {src.section_title}" if getattr(src, "section_title", None) else ""
        parts.append(
            f"[Evidence {i}] Document: {src.filename}{page}{section}\n"
            f"Chunk ID: {src.chunk_id}\n"
            f"Content: {src.text}\n"
        )
    return "\n".join(parts)
