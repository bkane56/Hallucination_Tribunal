from src.models.enums import Verdict
from src.models.tribunal import JudgeVerdict

_VERDICT_WEIGHTS: dict[Verdict, float] = {
    Verdict.SUPPORTED: 1.0,
    Verdict.PARTIALLY_SUPPORTED: 0.6,
    Verdict.NOT_ENOUGH_EVIDENCE: 0.4,
    Verdict.UNSUPPORTED: 0.0,
    Verdict.CONTRADICTED: 0.0,
}


def calculate_reliability_score(verdicts: list[JudgeVerdict]) -> float | None:
    """Compute overall reliability from claim-level verdicts.

    Returns None when there are no verdicts (not applicable).
    """
    if not verdicts:
        return None

    total = sum(_VERDICT_WEIGHTS[v.verdict] for v in verdicts)
    return round(total / len(verdicts), 4)
