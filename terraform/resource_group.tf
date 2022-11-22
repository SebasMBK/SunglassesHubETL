resource "azurerm_resource_group" "azure_rg" {
    name = var.project_resourcegroup
    location = var.project_region
}