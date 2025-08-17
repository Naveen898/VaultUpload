variable "project_name" {
  description = "The name of the project"
  type        = string
  default     = "VaultUpload"
}

variable "region" {
  description = "The cloud region for resource deployment"
  type        = string
  default     = "us-central1"
}

variable "bucket_name" {
  description = "The name of the cloud storage bucket"
  type        = string
}

variable "db_instance_name" {
  description = "The name of the database instance"
  type        = string
}

variable "db_user" {
  description = "The username for the database"
  type        = string
}

variable "db_password" {
  description = "The password for the database"
  type        = string
  sensitive   = true
}

variable "jwt_secret" {
  description = "Secret key for JWT token generation"
  type        = string
  sensitive   = true
}

variable "expiry_duration" {
  description = "Duration for file expiry in hours"
  type        = number
  default     = 24
}