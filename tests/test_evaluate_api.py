import pytest


VALID_PAYLOAD = {
    "question": "如何测试一个AI问答接口？",
    "answer": "使用接口测试覆盖正常、边界和异常场景，并检查准确性与安全性。" * 3,
    "expected_keywords": ["接口测试", "边界", "安全性"],
}


def test_evaluate_returns_structured_result_and_trace_id(client):
    response = client.post("/v1/evaluate", json=VALID_PAYLOAD)

    assert response.status_code == 200
    body = response.json()
    assert body["passed"] is True
    assert body["score"] == 100
    assert body["trace_id"] == response.headers["X-Trace-Id"]
    assert set(body["dimensions"]) == {"keyword_coverage", "clarity", "safety"}


def test_chinese_content_is_preserved(client):
    response = client.post("/v1/evaluate", json=VALID_PAYLOAD)

    assert response.json()["matched_keywords"] == ["接口测试", "边界", "安全性"]


@pytest.mark.parametrize("threshold", [-1, 101])
def test_threshold_boundary_rejects_invalid_values(client, threshold):
    payload = {**VALID_PAYLOAD, "pass_threshold": threshold}

    response = client.post("/v1/evaluate", json=payload)

    assert response.status_code == 422


@pytest.mark.parametrize("field", ["question", "answer"])
def test_required_text_rejects_blank_input(client, field):
    payload = {**VALID_PAYLOAD, field: "   "}

    response = client.post("/v1/evaluate", json=payload)

    assert response.status_code == 422


def test_answer_length_limit_is_enforced(client):
    payload = {**VALID_PAYLOAD, "answer": "a" * 4001}

    response = client.post("/v1/evaluate", json=payload)

    assert response.status_code == 422


def test_duplicate_keywords_are_normalized(client):
    payload = {**VALID_PAYLOAD, "expected_keywords": ["接口测试", "接口测试", "边界"]}

    response = client.post("/v1/evaluate", json=payload)

    assert response.status_code == 200
    assert response.json()["matched_keywords"] == ["接口测试", "边界"]


def test_blank_keyword_is_rejected(client):
    payload = {**VALID_PAYLOAD, "expected_keywords": ["接口测试", "   "]}

    response = client.post("/v1/evaluate", json=payload)

    assert response.status_code == 422
