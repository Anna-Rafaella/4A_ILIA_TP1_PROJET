
---

```markdown
# Rapport de TD : Virtualisation avec VirtualBox

## Introduction

Dans le cadre de ce TD, nous avons exploré les concepts fondamentaux de la virtualisation à travers l'utilisation de VirtualBox. L'objectif principal était de configurer une machine virtuelle (VM), d'effectuer des partages de fichiers entre l'hôte et la VM, et d'installer des outils essentiels pour le développement, comme Apache, Docker, et Kubernetes.

Ce document détaille les étapes que nous avons suivies pour accomplir ces tâches, ainsi que les problèmes rencontrés et leurs solutions.

---

## Prérequis

Avant de commencer, nous avons vérifié que les éléments suivants étaient en place :
- Une version récente de VirtualBox installée sur l'hôte.
- Une image ISO d'un système d'exploitation (Ubuntu 22.04 LTS dans notre cas).
- Les permissions administratives sur l'hôte pour installer des logiciels supplémentaires.

---

## Étape 1 : Création et configuration de la machine virtuelle

1. **Création de la VM** :
   - Nous avons créé une nouvelle VM dans VirtualBox en sélectionnant :
     - **Nom** : `VM_Ubuntu`.
     - **Type** : Linux.
     - **Version** : Ubuntu (64 bits).
   - Nous avons alloué 2 Go de RAM et 20 Go d'espace disque pour la VM.

2. **Installation de l'OS** :
   - L'image ISO d'Ubuntu a été montée en tant que disque optique virtuel.
   - Nous avons suivi les étapes d'installation d'Ubuntu jusqu'à obtenir un environnement de bureau fonctionnel.

---

## Étape 2 : Installation des Guest Additions

Pour améliorer l'intégration entre l'hôte et la VM, nous avons installé les **Guest Additions** :
1. Dans VirtualBox, nous avons sélectionné **Périphériques > Insérer l'image CD des Additions Invités**.
2. Dans la VM, nous avons monté le CD-ROM et exécuté les commandes suivantes :
   ```bash
   sudo apt update
   sudo apt install build-essential dkms
   sudo sh /media/$USER/VBox_GAs*/VBoxLinuxAdditions.run
   ```
3. Après un redémarrage, les fonctionnalités comme le redimensionnement de l'écran et le partage de dossiers étaient disponibles.

---

## Étape 3 : Partage de dossiers entre l'hôte et la VM

1. **Configuration du dossier partagé dans VirtualBox** :
   - Nous avons ajouté un dossier partagé nommé `Partage` via l'onglet **Dossiers partagés** dans les paramètres de la VM.
   - Le dossier a été configuré avec un accès en lecture-écriture et rendu permanent.

2. **Montage du dossier dans la VM** :
   - Nous avons créé un point de montage dans la VM :
     ```bash
     sudo mkdir -p /mnt/partage
     ```
   - Ensuite, le dossier partagé a été monté avec la commande :
     ```bash
     sudo mount -t vboxsf Partage /mnt/partage
     ```
   - Les fichiers du dossier partagé étaient alors accessibles dans `/mnt/partage`.

---

## Étape 4 : Installation et configuration d'Apache

1. **Installation** :
   - Nous avons installé Apache avec la commande :
     ```bash
     sudo apt update
     sudo apt install apache2
     ```
   - Le service a été démarré et activé :
     ```bash
     sudo systemctl start apache2
     sudo systemctl enable apache2
     ```

2. **Accès depuis l'hôte** :
   - L'adresse IP de la VM a été récupérée avec `ip a`.
   - En entrant cette adresse dans le navigateur de l'hôte (par exemple, `http://192.168.56.101`), nous avons confirmé que le serveur web fonctionnait correctement.

---

## Étape 5 : Installation de Docker, Kubernetes et Terraform

1. **Installation de Docker** :
   - Nous avons suivi ces étapes :
     ```bash
     sudo apt install -y docker.io
     sudo systemctl start docker
     sudo systemctl enable docker
     sudo usermod -aG docker $USER
     ```
   - Après une reconnexion, Docker était fonctionnel.

2. **Installation de Kubernetes (kubectl)** :
   - Nous avons ajouté le dépôt officiel et installé kubectl :
     ```bash
     curl -LO "https://dl.k8s.io/release/$(curl -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
     chmod +x kubectl
     sudo mv kubectl /usr/local/bin/
     ```

3. **Installation de Terraform** :
   - Nous avons téléchargé et installé Terraform via HashiCorp :
     ```bash
     sudo apt install -y software-properties-common
     curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
     echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
     sudo apt update
     sudo apt install terraform
     ```

---

## Résolution des problèmes rencontrés

- **Erreur de montage des dossiers partagés** :
  - Solution : Nous avons ajouté l'utilisateur au groupe `vboxsf` :
    ```bash
    sudo usermod -aG vboxsf $USER
    ```
    Puis, nous avons redémarré la session.

- **Problèmes de permissions avec Docker** :
  - Solution : L'ajout de l'utilisateur au groupe `docker` a résolu le problème.

- **Accès au serveur Apache depuis l'hôte** :
  - Solution : Nous avons vérifié que le pare-feu de la VM permettait les connexions sur le port 80 :
    ```bash
    sudo ufw allow 80
    ```

---

## Conclusion

Ce TD nous a permis de comprendre les bases de la virtualisation et de maîtriser les outils nécessaires pour un environnement de développement complet. Grâce à VirtualBox, nous avons pu configurer une VM, partager des ressources entre l'hôte et la VM, et installer des outils essentiels pour le développement web et DevOps.

Les compétences acquises ici sont essentielles pour la gestion d'environnements virtualisés et la mise en place d'infrastructures modernes.

---

## Auteur(s)

- Kapande Deng Anna Rafaella
```

---
