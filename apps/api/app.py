"""Vercel ASGI entrypoint."""

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from hallucination_tribunal.main import app

__all__ = ["app"]
