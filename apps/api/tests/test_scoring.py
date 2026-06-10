import pytest

from hallucination_tribunal.models.domain import JudgeVerdict, Verdict
from hallucination_tribunal.tribunal.scoring import (
    compute_overall_verdict,
    compute_reliability_score,
)


def test_reliability_score_empty():
    assert compute_reliability_score([]) == "Not Applicable"


def test_reliability_score_weighted_average():
    verdicts = [
        JudgeVerdict(
            claim_id="1",
            verdict=Verdict.SUPPORTED,
            confidence=0.9,
            explanation="ok",
        ),
        JudgeVerdict(
            claim_id="2",
            verdict=Verdict.UNSUPPORTED,
            confidence=0.2,
            explanation="bad",
        ),
    ]
    assert compute_reliability_score(verdicts) == 0.5


def test_overall_verdict_supported():
    verdicts = [
        JudgeVerdict(
            claim_id="1",
            verdict=Verdict.SUPPORTED,
            confidence=0.95,
            explanation="ok",
        )
    ]
    assert compute_overall_verdict(verdicts) == Verdict.SUPPORTED


def test_overall_verdict_no_claims():
    assert compute_overall_verdict([]) == Verdict.NOT_ENOUGH_EVIDENCE
