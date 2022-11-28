resource "azurerm_storage_data_lake_gen2_filesystem" "datalakefs" {
    name = var.staging_container_name
    storage_account_id = azurerm_storage_account.project_storage.id
}

resource "azurerm_synapse_workspace" "etlsynapse" {
    name = var.synapse_server_name
    resource_group_name = azurerm_resource_group.azure_rg.name
    location = var.project_region
    storage_data_lake_gen2_filesystem_id = azurerm_storage_data_lake_gen2_filesystem.datalakefs.id
    sql_administrator_login = var.sql_user
    sql_administrator_login_password = var.sql_pass

    aad_admin {
        login = "AzureAD Admin"
        object_id = data.azuread_client_config.current.object_id
        tenant_id = data.azuread_client_config.current.tenant_id
    }

    identity {
    type = "SystemAssigned"
    }
}

resource "azurerm_synapse_sql_pool" "etlsqlpool" {
    name = var.sql_pool_name
    synapse_workspace_id = azurerm_synapse_workspace.etlsynapse.id
    sku_name = "DW100c"
    create_mode = "Default"
}

# For educational purposes this server will allow all IP's, but this is never recommended for production services/instances
resource "azurerm_synapse_firewall_rule" "synapse_firewall" {
  name = "all_included"
  synapse_workspace_id = azurerm_synapse_workspace.etlsynapse.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "255.255.255.255"
}
