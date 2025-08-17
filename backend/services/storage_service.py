'''
from google.cloud import storage
import os
from backend.utils.logger import logger

class StorageService:
    def __init__(self, bucket_name):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def upload_file(self, file_path, destination_blob_name):
        """Uploads a file to the cloud storage bucket."""
        try:
            blob = self.bucket.blob(destination_blob_name)
            blob.upload_from_filename(file_path)
            logger.info(f"File {file_path} uploaded to {destination_blob_name}.")
            return blob.public_url
        except Exception as e:
            logger.error(f"Failed to upload file {file_path}: {str(e)}")
            raise

    def download_file(self, source_blob_name, destination_file_path):
        """Downloads a file from the cloud storage bucket."""
        try:
            blob = self.bucket.blob(source_blob_name)
            blob.download_to_filename(destination_file_path)
            logger.info(f"File {source_blob_name} downloaded to {destination_file_path}.")
        except Exception as e:
            logger.error(f"Failed to download file {source_blob_name}: {str(e)}")
            raise

    def delete_file(self, blob_name):
        """Deletes a file from the cloud storage bucket."""
        try:
            blob = self.bucket.blob(blob_name)
            blob.delete()
            logger.info(f"File {blob_name} deleted from storage.")
        except Exception as e:
            logger.error(f"Failed to delete file {blob_name}: {str(e)}")
            raise

    def list_files(self):
        """Lists all files in the cloud storage bucket."""
        try:
            blobs = self.bucket.list_blobs()
            file_list = [blob.name for blob in blobs]
            logger.info("Files in bucket: " + ", ".join(file_list))
            return file_list
        except Exception as e:
            logger.error(f"Failed to list files in bucket: {str(e)}")
            raise
'''
import os

UPLOAD_DIR = "local_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def upload_file(file):
    # Save file locally instead of uploading to cloud
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return f"/{UPLOAD_DIR}/{file.filename}"

def download_file(file_id):
    # Read file from local storage
    file_path = os.path.join(UPLOAD_DIR, file_id)
    try:
        with open(file_path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        return None