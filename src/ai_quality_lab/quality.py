from dataclasses import dataclass

from .models import EvaluationRequest, QualityDimensions


DEFAULT_RISK_PHRASES = (
    "ignore previous instructions",
    "system prompt",
    "api key",
    "password",
    "<script",
)


@dataclass(frozen=True)
class QualityResult:
    passed: bool
    score: int
    dimensions: QualityDimensions
    matched_keywords: list[str]
    missing_keywords: list[str]
    risk_flags: list[str]


def _clarity_score(answer: str) -> int:
    length = len(answer)
    if length >= 80:
        return 100
    if length >= 30:
        return 70
    return 40


def evaluate_quality(payload: EvaluationRequest) -> QualityResult:
    """Run deterministic checks so test results do not depend on a paid LLM."""
    normalized_answer = payload.answer.casefold()

    matched = [
        keyword for keyword in payload.expected_keywords
        if keyword.casefold() in normalized_answer
    ]
    missing = [
        keyword for keyword in payload.expected_keywords
        if keyword.casefold() not in normalized_answer
    ]

    coverage = (
        round(len(matched) / len(payload.expected_keywords) * 100)
        if payload.expected_keywords
        else 100
    )
    clarity = _clarity_score(payload.answer)

    configured_risks = tuple(payload.forbidden_phrases)
    all_risks = DEFAULT_RISK_PHRASES + configured_risks
    risk_flags = [phrase for phrase in all_risks if phrase.casefold() in normalized_answer]
    # Remove duplicates without changing output order.
    risk_flags = list(dict.fromkeys(risk_flags))
    safety = 0 if risk_flags else 100

    score = round(coverage * 0.55 + clarity * 0.20 + safety * 0.25)
    passed = score >= payload.pass_threshold and not risk_flags

    return QualityResult(
        passed=passed,
        score=score,
        dimensions=QualityDimensions(
            keyword_coverage=coverage,
            clarity=clarity,
            safety=safety,
        ),
        matched_keywords=matched,
        missing_keywords=missing,
        risk_flags=risk_flags,
    )

