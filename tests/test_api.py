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

from unittest.mock import patch, MagicMock

@patch("backend.api.advisor.get_model")
def test_advisor_ask_endpoint(mock_get_model):
    """Test the advisor ask endpoint with a mocked GenerativeModel."""
    # Mock the GenerativeModel and its generate_content response
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Mocked answer to election question."
    mock_model.generate_content.return_value = mock_response
    mock_get_model.return_value = mock_model
    
    payload = {"question": "How do I register?"}
    response = client.post("/api/advisor/ask", json=payload)
    
    assert response.status_code == 200
    assert response.json()["answer"] == "Mocked answer to election question."

@patch("backend.api.advisor.get_model")
def test_advisor_ask_endpoint_no_model(mock_get_model):
    """Test the advisor ask endpoint when RAG is not configured (no model)."""
    mock_get_model.return_value = None
    
    payload = {"question": "How do I register?"}
    response = client.post("/api/advisor/ask", json=payload)
    
    assert response.status_code == 500
    assert "detail" in response.json()
