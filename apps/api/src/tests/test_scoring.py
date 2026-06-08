from src.models import JudgeVerdict, Verdict
from src.tribunal.scoring import calculate_reliability_score


def test_reliability_score_none_when_empty() -> None:
    assert calculate_reliability_score([]) is None


def test_reliability_score_weighted_average() -> None:
    verdicts = [
        JudgeVerdict(
            claim_id="c1",
            verdict=Verdict.SUPPORTED,
            confidence=0.9,
            explanation="Supported.",
        ),
        JudgeVerdict(
            claim_id="c2",
            verdict=Verdict.PARTIALLY_SUPPORTED,
            confidence=0.7,
            explanation="Partial.",
        ),
    ]
    assert calculate_reliability_score(verdicts) == 0.8


def test_reliability_score_contradicted_counts_zero() -> None:
    verdicts = [
        JudgeVerdict(
            claim_id="c1",
            verdict=Verdict.CONTRADICTED,
            confidence=0.95,
            explanation="Contradicted.",
        ),
    ]
    assert calculate_reliability_score(verdicts) == 0.0
