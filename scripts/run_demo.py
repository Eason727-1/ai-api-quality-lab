from fastapi.testclient import TestClient

from ai_quality_lab.app import app


client = TestClient(app)
response = client.post(
    "/v1/evaluate",
    json={
        "question": "如何保证接口质量？",
        "answer": "通过边界测试、异常测试和持续回归保证接口质量。" * 3,
        "expected_keywords": ["边界测试", "异常测试", "持续回归"],
    },
)

print(response.model_dump_json(indent=2) if hasattr(response, "model_dump_json") else response.json())

