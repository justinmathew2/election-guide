import os
import logging
from google.cloud import secretmanager
from google.api_core.exceptions import GoogleAPIError

logger = logging.getLogger(__name__)

def get_secret(secret_id: str, version_id: str = "latest") -> str:
    """
    Access the payload of the given secret version using Google Secret Manager.
    Assumes GOOGLE_CLOUD_PROJECT environment variable is set for the project containing the secret.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        logger.warning("GOOGLE_CLOUD_PROJECT environment variable is not set. Skipping secret manager.")
        return os.getenv(secret_id, "")
        
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    
    try:
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except GoogleAPIError as e:
        logger.error(f"Google API Error accessing secret {secret_id}: {e}")
        # Fallback to env variables for local dev if secret fails
        return os.getenv(secret_id, "")
    except Exception as e:
        logger.error(f"Unexpected error accessing secret {secret_id}: {e}")
        return os.getenv(secret_id, "")
