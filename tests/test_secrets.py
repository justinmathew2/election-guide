import os
import pytest
from unittest.mock import patch, MagicMock
from backend.core.secrets import get_secret
from google.api_core.exceptions import GoogleAPIError

def test_get_secret_no_project_id():
    with patch.dict(os.environ, clear=True):
        os.environ["TEST_SECRET"] = "local_value"
        assert get_secret("TEST_SECRET") == "local_value"

@patch("backend.core.secrets.secretmanager.SecretManagerServiceClient")
def test_get_secret_success(mock_client_class):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.payload.data.decode.return_value = "secret_value"
    mock_client.access_secret_version.return_value = mock_response
    mock_client_class.return_value = mock_client
    
    with patch.dict(os.environ, {"GOOGLE_CLOUD_PROJECT": "test-project"}):
        assert get_secret("TEST_SECRET") == "secret_value"

@patch("backend.core.secrets.secretmanager.SecretManagerServiceClient")
def test_get_secret_api_error(mock_client_class):
    mock_client = MagicMock()
    mock_client.access_secret_version.side_effect = GoogleAPIError("API Error")
    mock_client_class.return_value = mock_client
    
    with patch.dict(os.environ, {"GOOGLE_CLOUD_PROJECT": "test-project", "TEST_SECRET": "fallback_value"}):
        assert get_secret("TEST_SECRET") == "fallback_value"

@patch("backend.core.secrets.secretmanager.SecretManagerServiceClient")
def test_get_secret_unexpected_error(mock_client_class):
    mock_client = MagicMock()
    mock_client.access_secret_version.side_effect = Exception("Unexpected Error")
    mock_client_class.return_value = mock_client
    
    with patch.dict(os.environ, {"GOOGLE_CLOUD_PROJECT": "test-project", "TEST_SECRET": "fallback_value"}):
        assert get_secret("TEST_SECRET") == "fallback_value"
