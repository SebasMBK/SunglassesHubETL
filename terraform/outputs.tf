output "storage_account_url" {
  value = azurerm_storage_account.project_storage.primary_blob_endpoint
  description = "Primary blob endpoint of the storage account"
}

output "etl_container_name" {
  value       = var.project_container_name
  description = "Name of the container that stores the project data"
}

output "etl_stagingarea_name" {
  value       = var.staging_container_name
  description = "Name of the container that stores the cleaned data"
}

output "raw_data_directory" {
  value = var.raw_data_dirname
  description = "Name of the directory that contains the raw level data"
}

output "access_data_directory" {
  value = var.access_data_dirname
  description = "Name of the directory that contains the access level data"
}