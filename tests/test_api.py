from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_journey_state_endpoint():
    """Test the journey state endpoint."""
    response = client.get("/api/journey/state")
    assert response.status_code == 200
    assert "state" in response.json()

def test_zkp_verify_endpoint():
    """Test the ZKP verification endpoint."""
    payload = {"age": 20, "location": "NY"}
    response = client.post("/api/journey/verify-eligibility", json=payload)
    assert response.status_code == 200
    assert response.json()["is_eligible"] is True
    assert "zkp_proof" in response.json()
