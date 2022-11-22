variable "project_resourcegroup" {
    type = string
    default = "etl_resource_group"
}

variable "project_region" {
    type = string
    default = "East Us"
}

variable "project_container_name" {
    type = string
    default = "etldatalake"
}

variable "staging_container_name" {
    type = string
    default = "etlstaging"
}

variable "raw_data_dirname" {
    type = string
    default = "raw"
}

variable "access_data_dirname" {
    type = string
    default = "access"
}

variable "sqlflex_server_name" {
    type = string
    default = "etlhubpostgre9000"
}

variable "postgresql_database_name" {
    type = string
    default = "etlhub"
    description = "This is the Azure postgresql flexible server database name"
}

variable "sql_user" {
    type = string
    description = "This is the Azure postgresql flexible server user"
}

variable "sql_pass" {
    type = string
    description = "This is the Azure postgresql flexible server password"
}