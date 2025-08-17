import os

CLOUD_STORAGE_PROVIDER = os.getenv("CLOUD_STORAGE_PROVIDER", "GCP")  # Options: GCP, AZURE

if CLOUD_STORAGE_PROVIDER == "GCP":
    GCP_BUCKET_NAME = os.getenv("GCP_BUCKET_NAME")
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
    GCP_SERVICE_ACCOUNT_JSON = os.getenv("GCP_SERVICE_ACCOUNT_JSON")
    
    # GCP specific configurations
    CLOUD_CONFIG = {
        "bucket_name": GCP_BUCKET_NAME,
        "project_id": GCP_PROJECT_ID,
        "service_account_json": GCP_SERVICE_ACCOUNT_JSON,
    }

elif CLOUD_STORAGE_PROVIDER == "AZURE":
    AZURE_STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
    AZURE_STORAGE_ACCOUNT_KEY = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
    AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")
    
    # Azure specific configurations
    CLOUD_CONFIG = {
        "account_name": AZURE_STORAGE_ACCOUNT_NAME,
        "account_key": AZURE_STORAGE_ACCOUNT_KEY,
        "container_name": AZURE_CONTAINER_NAME,
    }

else:
    raise ValueError("Unsupported cloud storage provider. Please set CLOUD_STORAGE_PROVIDER to either 'GCP' or 'AZURE'.")