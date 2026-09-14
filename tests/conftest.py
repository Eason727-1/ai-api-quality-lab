import pytest
from fastapi.testclient import TestClient

from ai_quality_lab.app import app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)

