output "backend_service_url" {
  value = "http://${backend_service_name}.${namespace}.svc.cluster.local:${backend_service_port}"
}

output "frontend_service_url" {
  value = "http://${frontend_service_name}.${namespace}.svc.cluster.local:${frontend_service_port}"
}

output "bucket_name" {
  value = "${google_storage_bucket.bucket_name.name}"
}

output "jwt_secret" {
  value = "${var.jwt_secret}"
}