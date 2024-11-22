// Initialisation de Terraform et configuration du provider
terraform {
  required_providers {
    scaleway = {
      source  = "scaleway/scaleway"
      version = ">= 2.0" # Assurez-vous de la version supportée par Scaleway pour votre configuration
    }
  }
  required_version = ">= 0.13"
}

provider "scaleway" {
  project_id = var.scaleway_project_id
  region     = "fr-par"
}

// Création d'un Registre de Conteneurs
resource "scaleway_registry_namespace" "registry" {
  name        = "calculatrice-registry"
  description = "Registry pour les conteneurs de la calculatrice"
  project_id  = var.scaleway_project_id
  region      = "fr-par"
}

// Création d'un Cluster Kubernetes
resource "scaleway_k8s_cluster" "cluster" {
  name                        = "calculatrice-cluster"
  project_id                  = var.scaleway_project_id
  region                      = "fr-par"
  cni                         = "cilium"
  version                     = "1.25.0"
  delete_additional_resources = false
  tags                        = ["calculatrice-cloud-native"]
}

// Ajout des pools de nœuds
resource "scaleway_k8s_pool" "pool" {
  cluster_id  = scaleway_k8s_cluster.cluster.id
  name        = "calculatrice-node-pool"
  size        = 3
  node_type   = "DEV1-M"
  autohealing = true
  region      = "fr-par"
}

// Configuration des Bases de Données (Development et Production)
resource "scaleway_rdb_instance" "db_dev" {
  engine         = "PostgreSQL-15"
  name           = "calculatrice-db-dev"
  project_id     = var.scaleway_project_id
  is_ha_cluster  = true
  disable_backup = true
  region         = "fr-par"
  user_name      = "devuser"
  password       = "devpassword"
  node_type      = "DEV1-S"
  tags           = ["environment:development"]
}

resource "scaleway_rdb_instance" "db_prod" {
  engine         = "PostgreSQL-15"
  name           = "calculatrice-db-prod"
  project_id     = var.scaleway_project_id
  is_ha_cluster  = true
  disable_backup = true
  region         = "fr-par"
  user_name      = "produser"
  password       = "prodpassword"
  node_type      = "DEV1-S"
  tags           = ["environment:production"]
}

// Configuration des Entrées DNS
// Définition de variables pour le nom de monôme
variable "nommonome" {
  default     = "anna"
  description = "Nom du monome"
  type        = string
}

// Ajout des enregistrements DNS pour les Load Balancers 

resource "scaleway_domain_record" "dns_prod" {
  dns_zone  = "kiowy.net"
  name  = "calculatrice-${var.nommonome}-polytech-dijon"
  type  = "A"
  ttl   = 300
  data     = "1.2.3.4"
}

resource "scaleway_domain_record" "dns_dev" {
  dns_zone  = "kiowy.net"
  name  = "calculatrice-dev-${var.nommonome}-polytech-dijon"
  type  = "A"
  ttl   = 300
  data     = "1.2.3.5"
}


// Configuration des LoadBalancers (Développement et Production)
resource "scaleway_lb_ip" "prod_ip" {
  project_id = var.scaleway_project_id
  zone       = "fr-par-1"
}

resource "scaleway_lb_ip" "dev_ip" {
  project_id = var.scaleway_project_id
  zone       = "fr-par-1"
}

resource "scaleway_lb" "lb_prod" {
  name       = "calculatrice-lb-prod"
  project_id = var.scaleway_project_id
  zone       = "fr-par-1"
  ip_id      = scaleway_lb_ip.prod_ip.id
  type       = "lb"
}

resource "scaleway_lb" "lb_dev" {
  name       = "calculatrice-lb-dev"
  project_id = var.scaleway_project_id
  zone       = "fr-par-1"
  ip_id      = scaleway_lb_ip.dev_ip.id
  type       = "lb"
}
