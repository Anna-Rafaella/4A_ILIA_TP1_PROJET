## 📚 FOUNDATION
Le dossier foundation permet de configurer l’infrastructure en code (IaC)

# 1. Configuration de Terraform et du Provider Scaleway
Nous allons d'abord définir les configurations de base pour Terraform et spécifier que nous allons utiliser le provider Scaleway.

terraform {
  required_providers {
    scaleway = {
      source = "scaleway/scaleway"
      version = ">= 2.0"  # Assurez-vous de la version supportée par Scaleway pour votre configuration
    }
  }
  required_version = ">= 0.13"
}

provider "scaleway" {
  project_id = var.scaleway_project_id
  region     = "fr-par"
}

# 2. Création d'un Registre de Conteneurs
Le registre de conteneurs est l’endroit où seront stockées les images Docker.

resource "scaleway_container_registry_namespace" "registry" {
  name = "calculatrice-registry"
  description = "Registry pour les conteneurs de la calculatrice"
  project_id = var.scaleway_project_id
  region     = "fr-par"
}



# 3. Création d'un Cluster Kubernetes
Le cluster Kubernetes sera utilisé pour déployer et gérer les microservices de l’application.

resource "scaleway_k8s_cluster" "cluster" {
  name                      = "calculatrice-cluster"
  project_id                = var.scaleway_project_id
  region                    = "fr-par"
  cni                       = "cilium"
  version                   = "1.25.0"
  delete_additional_resources = false
  tags                      = ["calculatrice-cloud-native"]
}
Ajout des pools de nœuds
resource "scaleway_k8s_pool" "pool" {
  cluster_id  = scaleway_k8s_cluster.cluster.id
  name        = "calculatrice-node-pool"
  size        = 3
  node_type   = "DEV1-M"
  autohealing = true
  region      = "fr-par"
}

# 4. Configuration des Bases de Données (Development et Production)
Les bases de données sont nécessaires pour stocker les données selon les environnements (développement et production).

resource "scaleway_rdb_instance" "db_dev" {
  engine          = "PostgreSQL-15"
  name            = "calculatrice-db-dev"
  project_id      = var.scaleway_project_id
  is_ha_cluster   = true
  disable_backup  = true
  region          = "fr-par"
  user_name       = "devuser"
  password        = "devpassword"
  node_type       = "DEV1-S"
  tags            = ["environment:development"]
}

resource "scaleway_rdb_instance" "db_prod" {
  engine          = "PostgreSQL-15"
  name            = "calculatrice-db-prod"
  project_id      = var.scaleway_project_id
  is_ha_cluster   = true
  disable_backup  = true
  region          = "fr-par"
  user_name       = "produser"
  password        = "prodpassword"
  node_type       = "DEV1-S"
  tags            = ["environment:production"]
}


# 5. Configuration des Entrées DNS
Pour accéder à votre application via des noms de domaine, nous allons configurer les entrées DNS nécessaires.

5.1- Définition des variables pour le nom du monôme
variable "nommonome" {
  default="anna"
 description = "Nom du monome"
  type        = string
}

5.2- Ajout des enregistrements DNS pour les Load Balancers

resource "scaleway_dns_record" "dns_prod" {
  zone = "kiowy.net"
  name = "calculatrice-${var.nombinome1}-${var.nombinome2}-polytech-dijon"
  type = "A"
  ttl  = 300
  value = scaleway_lb_ip.prod_ip.address
}

resource "scaleway_dns_record" "dns_dev" {
  zone = "kiowy.net"
  name = "calculatrice-dev-${var.nombinome1}-${var.nombinome2}-polytech-dijon"
  type = "A"
  ttl  = 300
  value = scaleway_lb_ip.dev_ip.address
}

# 6. Configuration des LoadBalancers (Développement et Production)
Les LoadBalancers seront utilisés pour diriger le trafic vers le cluster Kubernetes.

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


## 📚 Résultats après l'exécutionn des terraform

# terraform plan

@Anna-Rafaella ➜ /workspaces/4A_ILIA_TP1_PROJET/foundation (main) $ terraform plan
var.scaleway_access_key
  Scaleway Access Key for authentication

  Enter a value: my_scaleway_access_key

var.scaleway_secret_key
  Scaleway Secret Key for authentication

  Enter a value: 


Terraform used the selected providers to generate the following execution
plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # scaleway_domain_record.dns_dev will be created
  + resource "scaleway_domain_record" "dns_dev" {
      + data            = "1.2.3.5"
      + dns_zone        = "kiowy.net"
      + fqdn            = (known after apply)
      + id              = (known after apply)
      + keep_empty_zone = false
      + name            = "calculatrice-dev-anna-polytech-dijon"
      + priority        = (known after apply)
      + project_id      = (known after apply)
      + root_zone       = (known after apply)
      + ttl             = 300
      + type            = "A"
    }

  # scaleway_domain_record.dns_prod will be created
  + resource "scaleway_domain_record" "dns_prod" {
      + data            = "1.2.3.4"
      + dns_zone        = "kiowy.net"
      + fqdn            = (known after apply)
      + id              = (known after apply)
      + keep_empty_zone = false
      + name            = "calculatrice-anna-polytech-dijon"
      + priority        = (known after apply)
      + project_id      = (known after apply)
      + root_zone       = (known after apply)
      + ttl             = 300
      + type            = "A"
    }

  # scaleway_k8s_cluster.cluster will be created
  + resource "scaleway_k8s_cluster" "cluster" {
      + apiserver_url               = (known after apply)
      + cni                         = "cilium"
      + created_at                  = (known after apply)
      + delete_additional_resources = false
      + id                          = (known after apply)
      + kubeconfig                  = (sensitive value)
      + name                        = "calculatrice-cluster"
      + organization_id             = (known after apply)
      + project_id                  = "123e4567-e89b-12d3-a456-426614174000"
      + region                      = "fr-par"
      + status                      = (known after apply)
      + tags                        = [
          + "calculatrice-cloud-native",
        ]
      + type                        = (known after apply)
      + updated_at                  = (known after apply)
      + upgrade_available           = (known after apply)
      + version                     = "1.25.0"
      + wildcard_dns                = (known after apply)

      + auto_upgrade (known after apply)

      + autoscaler_config (known after apply)

      + open_id_connect_config (known after apply)
    }

  # scaleway_k8s_pool.pool will be created
  + resource "scaleway_k8s_pool" "pool" {
      + autohealing            = true
      + autoscaling            = false
      + cluster_id             = (known after apply)
      + container_runtime      = "containerd"
      + created_at             = (known after apply)
      + current_size           = (known after apply)
      + id                     = (known after apply)
      + max_size               = (known after apply)
      + min_size               = 1
      + name                   = "calculatrice-node-pool"
      + node_type              = "DEV1-M"
      + nodes                  = (known after apply)
      + public_ip_disabled     = false
      + region                 = "fr-par"
      + root_volume_size_in_gb = (known after apply)
      + root_volume_type       = (known after apply)
      + size                   = 3
      + status                 = (known after apply)
      + updated_at             = (known after apply)
      + version                = (known after apply)
      + wait_for_pool_ready    = true
      + zone                   = (known after apply)

      + upgrade_policy (known after apply)
    }

  # scaleway_lb.lb_dev will be created
  + resource "scaleway_lb" "lb_dev" {
      + id                      = (known after apply)
      + ip_address              = (known after apply)
      + ip_id                   = (known after apply)
      + ip_ids                  = (known after apply)
      + ipv6_address            = (known after apply)
      + name                    = "calculatrice-lb-dev"
      + organization_id         = (known after apply)
      + project_id              = "123e4567-e89b-12d3-a456-426614174000"
      + region                  = (known after apply)
      + ssl_compatibility_level = "ssl_compatibility_level_intermediate"
      + type                    = "lb"
      + zone                    = "fr-par-1"
    }

  # scaleway_lb.lb_prod will be created
  + resource "scaleway_lb" "lb_prod" {
      + id                      = (known after apply)
      + ip_address              = (known after apply)
      + ip_id                   = (known after apply)
      + ip_ids                  = (known after apply)
      + ipv6_address            = (known after apply)
      + name                    = "calculatrice-lb-prod"
      + organization_id         = (known after apply)
      + project_id              = "123e4567-e89b-12d3-a456-426614174000"
      + region                  = (known after apply)
      + ssl_compatibility_level = "ssl_compatibility_level_intermediate"
      + type                    = "lb"
      + zone                    = "fr-par-1"
    }

  # scaleway_lb_ip.dev_ip will be created
  + resource "scaleway_lb_ip" "dev_ip" {
      + id              = (known after apply)
      + ip_address      = (known after apply)
      + is_ipv6         = false
      + lb_id           = (known after apply)
      + organization_id = (known after apply)
      + project_id      = "123e4567-e89b-12d3-a456-426614174000"
      + region          = (known after apply)
      + reverse         = (known after apply)
      + zone            = "fr-par-1"
    }

  # scaleway_lb_ip.prod_ip will be created
  + resource "scaleway_lb_ip" "prod_ip" {
      + id              = (known after apply)
      + ip_address      = (known after apply)
      + is_ipv6         = false
      + lb_id           = (known after apply)
      + organization_id = (known after apply)
      + project_id      = "123e4567-e89b-12d3-a456-426614174000"
      + region          = (known after apply)
      + reverse         = (known after apply)
      + zone            = "fr-par-1"
    }

  # scaleway_rdb_instance.db_dev will be created
  + resource "scaleway_rdb_instance" "db_dev" {
      + backup_same_region        = (known after apply)
      + backup_schedule_frequency = (known after apply)
      + backup_schedule_retention = (known after apply)
      + certificate               = (known after apply)
      + disable_backup            = true
      + endpoint_ip               = (known after apply)
      + endpoint_port             = (known after apply)
      + engine                    = "PostgreSQL-15"
      + id                        = (known after apply)
      + is_ha_cluster             = true
      + name                      = "calculatrice-db-dev"
      + node_type                 = "DEV1-S"
      + organization_id           = (known after apply)
      + password                  = (sensitive value)
      + project_id                = "123e4567-e89b-12d3-a456-426614174000"
      + read_replicas             = (known after apply)
      + region                    = "fr-par"
      + settings                  = (known after apply)
      + tags                      = [
          + "environment:development",
        ]
      + user_name                 = "devuser"
      + volume_size_in_gb         = (known after apply)
      + volume_type               = "lssd"

      + load_balancer (known after apply)

      + logs_policy (known after apply)
    }

  # scaleway_rdb_instance.db_prod will be created
  + resource "scaleway_rdb_instance" "db_prod" {
      + backup_same_region        = (known after apply)
      + backup_schedule_frequency = (known after apply)
      + backup_schedule_retention = (known after apply)
      + certificate               = (known after apply)
      + disable_backup            = true
      + endpoint_ip               = (known after apply)
      + endpoint_port             = (known after apply)
      + engine                    = "PostgreSQL-15"
      + id                        = (known after apply)
      + is_ha_cluster             = true
      + name                      = "calculatrice-db-prod"
      + node_type                 = "DEV1-S"
      + organization_id           = (known after apply)
      + password                  = (sensitive value)
      + project_id                = "123e4567-e89b-12d3-a456-426614174000"
      + read_replicas             = (known after apply)
      + region                    = "fr-par"
      + settings                  = (known after apply)
      + tags                      = [
          + "environment:production",
        ]
      + user_name                 = "produser"
      + volume_size_in_gb         = (known after apply)
      + volume_type               = "lssd"

      + load_balancer (known after apply)

      + logs_policy (known after apply)
    }

  # scaleway_registry_namespace.registry will be created
  + resource "scaleway_registry_namespace" "registry" {
      + description     = "Registry pour les conteneurs de la calculatrice"
      + endpoint        = (known after apply)
      + id              = (known after apply)
      + name            = "calculatrice-registry"
      + organization_id = (known after apply)
      + project_id      = "123e4567-e89b-12d3-a456-426614174000"
      + region          = "fr-par"
    }

Plan: 11 to add, 0 to change, 0 to destroy.

──────────────────────────────────────────────────────────────────────────

Note: You didn't use the -out option to save this plan, so Terraform can't
guarantee to take exactly these actions if you run "terraform apply" now.
