def test_health_endpoint_returns_version(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "1.0.0"}


def test_openapi_exposes_evaluation_endpoint(client):
    schema = client.get("/openapi.json").json()

    assert "/v1/evaluate" in schema["paths"]
    assert "post" in schema["paths"]["/v1/evaluate"]

