from google.cloud import secretmanager
import os

def get_secret(secret_id: str, version_id: str = "latest") -> str:
    """
    Access the payload of the given secret version using Google Secret Manager.
    Assumes GOOGLE_CLOUD_PROJECT environment variable is set for the project containing the secret.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable is not set. Skipping secret manager.")
        return os.getenv(secret_id, "")
        
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    
    try:
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"Error accessing secret {secret_id}: {e}")
        # Fallback to env variables for local dev if secret fails
        return os.getenv(secret_id, "")
