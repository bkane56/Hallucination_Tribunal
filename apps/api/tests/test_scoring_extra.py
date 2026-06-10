import pytest

from hallucination_tribunal.tribunal.scoring import compute_overall_verdict
from hallucination_tribunal.models.domain import JudgeVerdict, Verdict


def test_overall_verdict_partially_supported():
    verdicts = [
        JudgeVerdict(
            claim_id="1",
            verdict=Verdict.PARTIALLY_SUPPORTED,
            confidence=0.7,
            explanation="partial",
        )
    ]
    assert compute_overall_verdict(verdicts) == Verdict.PARTIALLY_SUPPORTED


def test_overall_verdict_contradicted():
    verdicts = [
        JudgeVerdict(
            claim_id="1",
            verdict=Verdict.CONTRADICTED,
            confidence=0.1,
            explanation="bad",
        )
    ]
    assert compute_overall_verdict(verdicts) == Verdict.CONTRADICTED
