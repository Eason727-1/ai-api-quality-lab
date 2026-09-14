import pytest

from ai_quality_lab.models import EvaluationRequest
from ai_quality_lab.quality import evaluate_quality


def build_request(**overrides) -> EvaluationRequest:
    data = {
        "question": "如何降低接口测试漏测率？",
        "answer": "可以建立边界值、异常流与回归测试，并在流水线中持续执行。" * 2,
        "expected_keywords": ["边界值", "异常流", "回归测试"],
    }
    data.update(overrides)
    return EvaluationRequest(**data)


def test_full_keyword_coverage_passes():
    result = evaluate_quality(build_request())

    assert result.passed is True
    assert result.dimensions.keyword_coverage == 100
    assert result.missing_keywords == []


def test_partial_coverage_reports_missing_keyword():
    result = evaluate_quality(
        build_request(answer="边界值和回归测试能够提升质量。" * 4)
    )

    assert result.dimensions.keyword_coverage == 67
    assert result.missing_keywords == ["异常流"]


def test_keyword_matching_is_case_insensitive():
    result = evaluate_quality(
        build_request(answer="PYTEST can automate regression checks. " * 3,
                      expected_keywords=["pytest", "REGRESSION"])
    )

    assert result.matched_keywords == ["pytest", "REGRESSION"]


def test_no_expected_keywords_defaults_to_full_coverage():
    result = evaluate_quality(build_request(expected_keywords=[]))

    assert result.dimensions.keyword_coverage == 100


@pytest.mark.parametrize(
    ("answer", "expected_clarity"),
    [
        ("简短回答", 40),
        ("这是一个长度超过三十字符但不足八十字符的回答，用于验证清晰度评分的中间边界。", 70),
        ("这是一个足够长的回答。" * 10, 100),
    ],
)
def test_clarity_boundaries(answer, expected_clarity):
    result = evaluate_quality(build_request(answer=answer, expected_keywords=[]))

    assert result.dimensions.clarity == expected_clarity


def test_custom_forbidden_phrase_blocks_high_score_answer():
    result = evaluate_quality(
        build_request(
            answer="边界值、异常流与回归测试都已覆盖，但这里包含内部机密。" * 3,
            forbidden_phrases=["内部机密"],
        )
    )

    assert result.passed is False
    assert result.dimensions.safety == 0
    assert result.risk_flags == ["内部机密"]


def test_score_always_stays_in_valid_range():
    result = evaluate_quality(build_request(answer="短", expected_keywords=["未出现"]))

    assert 0 <= result.score <= 100

