# TERRAFORM
Installation de terraform
Les dossiers  et fichier de déploiement ont été effectués dans un codespace 

# Ceci est le lien de mon dépôt git dans lequel j'ai réalisé le td de TERRAFORM:
https://github.com/Anna-Rafaella/TERRAFORM/


Voici un exemple de fichier **README.md** clair, structuré et adapté à votre projet Terraform avec AWS. Ce document est rédigé en utilisant le pronom personnel "nous", comme demandé.

---

# Déploiement d'une Infrastructure Cloud avec Terraform et AWS/GCP

Ce projet consiste à déployer une infrastructure cloud complète sur **AWS** en utilisant **Terraform**. Nous avons configuré un **VPC**, des **instances EC2**, une **base de données RDS** et une **zone DNS Route 53** pour simuler une architecture cloud haute disponibilité.

## Structure du projet

Voici les principales étapes et ressources que nous avons mises en place :

1. **Configuration du VPC :**
   - Un **Virtual Private Cloud (VPC)** avec un CIDR block `10.0.0.0/16`.
   - Un sous-réseau associé au VPC pour nos instances et notre base de données.
   - Une **Internet Gateway** et une table de routage pour permettre l'accès à Internet.

2. **Instances EC2 :**
   - Trois instances EC2 pour garantir une meilleure disponibilité.
   - Chaque instance utilise une image Debian 9 et est connectée au VPC via le sous-réseau.

3. **Base de données RDS :**
   - Une base de données PostgreSQL 12 hébergée sur AWS RDS.
   - La base de données est privée et accessible uniquement via le VPC.

4. **Zone DNS Route 53 :**
   - Une zone DNS gérée pour le domaine `example.com`.
   - Un enregistrement DNS de type `A` pointant vers l'adresse IP publique de la première instance EC2.

## Prérequis

Avant de commencer, nous devons nous assurer d'avoir les éléments suivants :
- Un compte AWS actif.
- Terraform installé sur notre machine (version >= 1.0.0).
- Une clé SSH configurée sur AWS pour accéder aux instances EC2.

## Instructions

### 1. Cloner le projet

Clonons le projet dans notre environnement local :

```bash
git clone https://github.com/votre-repo/terraform-aws-project.git
cd terraform-aws-project
```

### 2. Initialiser Terraform

Initialisons Terraform pour télécharger les plugins nécessaires :

```bash
terraform init
```

### 3. Valider la configuration

Validons notre configuration pour nous assurer qu'il n'y a pas d'erreurs :

```bash
terraform validate
```

### 4. Planifier le déploiement

Générons un plan d'exécution pour visualiser les ressources qui seront créées :

```bash
terraform plan
```

### 5. Appliquer le déploiement

Déployons notre infrastructure en appliquant le plan Terraform :

```bash
terraform apply
```

Nous devrons confirmer l'exécution en tapant `yes` lorsque Terraform nous le demandera.

### 6. Vérification

Une fois le déploiement terminé, nous pouvons vérifier les ressources créées :
- Les instances EC2 sont accessibles via leur adresse IP publique.
- La base de données RDS est opérationnelle et accessible uniquement depuis le VPC.
- L'entrée DNS est correctement configurée dans Route 53.

### 7. Résultat du Terraform Plan

Voici le résultat du **terraform plan** que nous avons obtenu :

```plaintext
# Résultat du terraform plan (à copier/coller ici après exécution)
```

## Nettoyage

Pour éviter des coûts inutiles, nous pouvons détruire toutes les ressources créées avec la commande suivante :

```bash
terraform destroy
```

Nous devrons confirmer l'exécution en tapant `yes`.

## Structure des fichiers

Voici la structure des fichiers de notre projet :

```
/terraform-aws-project/
  ├── main.tf          # Configuration principale Terraform
  ├── provider.tf      # Déclaration du provider AWS
  ├── network.tf       # Configuration du VPC, sous-réseau, et routage
  ├── compute.tf       # Déploiement des instances EC2
  ├── database.tf      # Déploiement de la base de données RDS
  ├── dns.tf           # Configuration DNS avec Route 53
  ├── outputs.tf       # Sorties Terraform (IP, noms des ressources)
  ├── variables.tf     # Variables utilisées dans le projet
```

## Ressources créées

Voici les principales ressources que nous avons déployées :

1. **VPC** :
   - Nom : `my-vpc`
   - CIDR : `10.0.0.0/16`

2. **Instances EC2** :
   - Nom : `my-instance-0`, `my-instance-1`, `my-instance-2`
   - Type : `t2.micro`
   - Système d'exploitation : Debian 9

3. **Base de données RDS** :
   - Nom : `my-sql-instance`
   - Type : `db.t2.micro`
   - Moteur : PostgreSQL 12

4. **DNS Route 53** :
   - Zone DNS : `example.com`
   - Enregistrement : `www.example.com` pointant vers l'IP publique de la première instance EC2.

## Points d'amélioration

Voici quelques points que nous pourrions améliorer pour rendre notre infrastructure encore plus robuste :
- Ajouter un **Load Balancer** pour répartir le trafic entre les instances EC2.
- Activer le chiffrement pour la base de données RDS.
- Configurer des groupes d'instances managés pour un meilleur scaling automatique.

## Conclusion

Grâce à Terraform, nous avons pu déployer une infrastructure cloud complète sur AWS de manière déclarative et reproductible. Ce projet illustre les bonnes pratiques pour gérer des ressources cloud tout en garantissant une haute disponibilité.

---

