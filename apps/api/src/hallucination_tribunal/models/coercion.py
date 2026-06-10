"""Coercion helpers for LLM JSON that may use null instead of empty lists."""

from typing import Annotated, Any, TypeVar

from pydantic import BeforeValidator

T = TypeVar("T")


def coerce_null_to_list(value: Any) -> list[Any]:
    """Normalize LLM output where optional list fields are returned as null."""
    if value is None:
        return []
    return value


LlmStrList = Annotated[list[str], BeforeValidator(coerce_null_to_list)]
