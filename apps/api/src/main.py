"""Compatibility entrypoint — use hallucination_tribunal.main:app in production."""

from hallucination_tribunal.main import app

__all__ = ["app"]
