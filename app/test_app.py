import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_home_returns_json(client):
    response = client.get("/")
    data = response.get_json()
    assert "message" in data
    assert "version" in data
    assert "environment" in data


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


def test_ready_endpoint(client):
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ready"


def test_info_endpoint(client):
    response = client.get("/api/info")
    assert response.status_code == 200
    data = response.get_json()
    assert data["app"] == "devops-cicd-pipeline"
    assert "version" in data
    assert "maintainer" in data


def test_unknown_route_returns_404(client):
    response = client.get("/nonexistent")
    assert response.status_code == 404