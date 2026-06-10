"""Reliability score computation."""

from hallucination_tribunal.models.domain import JudgeVerdict, VERDICT_SCORES, Verdict


def compute_reliability_score(verdicts: list[JudgeVerdict]) -> float | str:
    if not verdicts:
        return "Not Applicable"

    total = 0.0
    for verdict in verdicts:
        total += VERDICT_SCORES.get(verdict.verdict, 0.0)
    return round(total / len(verdicts), 2)


def compute_overall_verdict(verdicts: list[JudgeVerdict]) -> Verdict | str:
    if not verdicts:
        return Verdict.NOT_ENOUGH_EVIDENCE

    score = compute_reliability_score(verdicts)
    if score == "Not Applicable":
        return Verdict.NOT_ENOUGH_EVIDENCE
    if isinstance(score, float):
        if score >= 0.85:
            return Verdict.SUPPORTED
        if score >= 0.6:
            return Verdict.PARTIALLY_SUPPORTED
        if score >= 0.4:
            return Verdict.NOT_ENOUGH_EVIDENCE
        if any(v.verdict == Verdict.CONTRADICTED for v in verdicts):
            return Verdict.CONTRADICTED
        return Verdict.UNSUPPORTED
    return Verdict.NOT_ENOUGH_EVIDENCE
