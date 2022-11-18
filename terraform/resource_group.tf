resource "azurerm_resource_group" "azure_rg" {
    name = "etl_resource_group"
    location = "${var.project_region}"
}