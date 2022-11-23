resource "azurerm_storage_account" "project_storage" {
    name = "sunglasseshubetl"
    resource_group_name = azurerm_resource_group.azure_rg.name
    location = var.project_region
    account_tier = "Standard"
    account_replication_type = "LRS"
    account_kind = "StorageV2"
    is_hns_enabled = true
}

resource "azurerm_storage_container" "project_data_lake" {
    name = var.project_container_name
    storage_account_name = azurerm_storage_account.project_storage.name
    container_access_type = "blob"
}

# With this line of code we are storing the information of the logged in azure account
data "azuread_client_config" "current"{}

resource "azurerm_role_assignment" "data-contributor-role" {
  scope                = azurerm_storage_container.project_data_lake.resource_manager_id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = data.azuread_client_config.current.object_id
}