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