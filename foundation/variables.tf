// Variables pour les identifiants

variable "scaleway_access_key" {
  description = "Scaleway Access Key for authentication"
  type        = string
}

variable "scaleway_secret_key" {
  description = "Scaleway Secret Key for authentication"
  type        = string
  sensitive   = true
}

variable "scaleway_project_id" {
  description = "Scaleway Project ID where the resources will be created"
  type        = string
  default     = "123e4567-e89b-12d3-a456-426614174000"
}



