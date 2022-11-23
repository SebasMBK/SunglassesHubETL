resource "azurerm_postgresql_flexible_server" postgres_server {
    name = var.sqlflex_server_name
    resource_group_name = azurerm_resource_group.azure_rg.name
    location = var.project_region
    version = "13"
    administrator_login = var.sql_user
    administrator_password = var.sql_pass
    storage_mb = 32768
    sku_name = "B_Standard_B1ms"
}

resource "azurerm_postgresql_flexible_server_database" "postgres_database" {
  name      = var.postgresql_database_name
  server_id = azurerm_postgresql_flexible_server.postgres_server.id
  collation = "en_US.utf8"
  charset   = "utf8"
}

# For educational purposes this server will allow all IP's, but this is never recommended for production services/instances
resource "azurerm_postgresql_flexible_server_firewall_rule" "postgres_firewall" {
  name             = "all_included"
  server_id        = azurerm_postgresql_flexible_server.postgres_server.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "255.255.255.255"
}