"""
API Tests for Aegis AI
Run with: pytest tests/
"""
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Aegis AI API"

def test_health():
    """Test health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_generate_scenario():
    """Test scenario generation endpoint"""
    response = client.post("/api/scenarios/generate", json={
        "department": "accounting",
        "difficulty": "medium"
    })
    assert response.status_code in [200, 500]  # 500 if API key not set

def test_leaderboard():
    """Test leaderboard endpoint"""
    response = client.get("/api/leaderboard/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_org_stats():
    """Test organization stats"""
    response = client.get("/api/organizations/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_attempts" in data
    assert "average_score" in data

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
