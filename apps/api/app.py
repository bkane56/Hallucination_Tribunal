"""Vercel ASGI entrypoint — package is installed from pyproject.toml in this directory."""

from hallucination_tribunal.main import app

__all__ = ["app"]
