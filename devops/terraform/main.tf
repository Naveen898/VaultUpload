provider "google" {
  credentials = file("<PATH_TO_YOUR_SERVICE_ACCOUNT_JSON>")
  project     = var.project_id
  region      = var.region
}

resource "google_storage_bucket" "vault_upload_bucket" {
  name     = "${var.project_id}-vault-upload"
  location = var.region

  versioning {
    enabled = true
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "google_storage_bucket_object" "uploaded_file" {
  name   = var.file_name
  bucket = google_storage_bucket.vault_upload_bucket.name
  source = var.file_path
}

output "bucket_name" {
  value = google_storage_bucket.vault_upload_bucket.name
}

output "file_url" {
  value = "gs://${google_storage_bucket.vault_upload_bucket.name}/${var.file_name}"
}