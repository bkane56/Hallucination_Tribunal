"""Coercion helpers for LLM JSON that may use null instead of empty lists."""

import json
from typing import Annotated, Any, TypeVar

from pydantic import BeforeValidator

T = TypeVar("T")


def coerce_null_to_list(value: Any) -> list[Any]:
    """Normalize LLM output where list fields are null, JSON strings, or scalars."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return []
        if stripped.startswith("["):
            try:
                parsed = json.loads(stripped)
                if isinstance(parsed, list):
                    return parsed
            except json.JSONDecodeError:
                pass
        return [value]
    return value


LlmStrList = Annotated[list[str], BeforeValidator(coerce_null_to_list)]
