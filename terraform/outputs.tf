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

output "postgres_servername" {
  value = azurerm_postgresql_flexible_server.postgres_server.fqdn
}

output "synapse_servername" {
  value = var.synapse_server_name
}

output "sql_databasename" {
  value = var.postgresql_database_name
}

output "sql_pool_dbname" {
  value = var.sql_pool_name
}

output "sql_username" {
  value = var.sql_user
}

output "sql_password" {
  value = var.sql_pass
}

output "synapse_conn_endpoints" {
  value = azurerm_synapse_workspace.etlsynapse.connectivity_endpoints
}