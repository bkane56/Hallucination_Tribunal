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


def coerce_verdict(value: Any) -> Any:
    from hallucination_tribunal.models.domain import Verdict

    if isinstance(value, Verdict):
        return value
    if isinstance(value, str):
        try:
            return Verdict(value)
        except ValueError:
            return value
    return str(value)


def coerce_reliability_score(value: Any) -> float | str:
    if value == "Not Applicable":
        return value
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return value
    return value


LlmStrList = Annotated[list[str], BeforeValidator(coerce_null_to_list)]
CoercedVerdict = Annotated[Any, BeforeValidator(coerce_verdict)]
CoercedReliabilityScore = Annotated[float | str, BeforeValidator(coerce_reliability_score)]
