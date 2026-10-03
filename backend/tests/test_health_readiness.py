"""Verify /health and /health/ready endpoints."""

from fastapi.testclient import TestClient

from pattern_specular.main import create_app


def test_health_liveness() -> None:
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_readiness() -> None:
    client = TestClient(create_app())
    response = client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "connected"
