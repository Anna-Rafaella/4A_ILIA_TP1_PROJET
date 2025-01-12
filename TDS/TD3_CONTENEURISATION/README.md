
---

# Étapes de Construction et d'Exécution avec Docker  

Ce guide nous accompagne dans la mise en place, la construction, l'exécution et le test de nos services conteneurisés avec Docker et Docker Compose.  

---

## 1. Construire et Exécuter avec Docker Compose  

Docker Compose simplifie la gestion et l'orchestration de nos services conteneurisés.  

### Étape 1 : Construire les images Docker  

1. Accédons au répertoire racine où se trouve notre fichier `docker-compose.yml` :  
   ```bash
   cd /Conteneurisation
   ```

2. Construisons les images Docker pour tous nos services définis dans le fichier `docker-compose.yml` :  
   ```bash
   docker-compose build
   ```  

   Cette commande crée des images Docker locales à partir des instructions définies dans les `Dockerfile` de chaque service.  

---

### Étape 2 : Démarrer les services  

1. Une fois les images construites, démarrons tous les services en arrière-plan :  
   ```bash
   docker-compose up -d
   ```  

2. Vérifions que les conteneurs fonctionnent correctement :  
   ```bash
   docker ps
   ```  

   Cette commande liste tous les conteneurs en cours d'exécution. Nous devrions voir nos services (backend, consumer, frontend, RabbitMQ, Redis) dans la liste.  

---

## 2. Taguer et Pousser les Images Docker dans un Registre  

Pour partager nos images Docker ou les rendre accessibles à d'autres environnements (comme Kubernetes), nous devons les **taguer** et les **pousser** vers un registre Docker (par exemple, Docker Hub, Amazon ECR, ou Google Container Registry).  

### Étape 1 : Taguer les images  

1. Après avoir construit nos images, taguons-les avec un nom qui inclut notre identifiant de registre Docker. Voici des exemples pour Docker Hub :  

   - **Taguer l'image backend** :  
     ```bash
     docker tag backend:latest <notre_utilisateur_dockerhub>/backend:latest
     ```  

   - **Taguer l'image consumer** :  
     ```bash
     docker tag consumer:latest <notre_utilisateur_dockerhub>/consumer:latest
     ```  

   - **Taguer l'image frontend** :  
     ```bash
     docker tag frontend:latest <notre_utilisateur_dockerhub>/frontend:latest
     ```  

### Étape 2 : Pousser les images dans le registre  

1. Connectons-nous à notre compte Docker Hub (ou un autre registre) :  
   ```bash
   docker login
   ```  

2. Poussons chaque image taguée vers le registre :  

   - **Pousser l'image backend** :  
     ```bash
     docker push <notre_utilisateur_dockerhub>/backend:latest
     ```  

   - **Pousser l'image consumer** :  
     ```bash
     docker push <notre_utilisateur_dockerhub>/consumer:latest
     ```  

   - **Pousser l'image frontend** :  
     ```bash
     docker push <notre_utilisateur_dockerhub>/frontend:latest
     ```  

---

## 3. Tester si les Services Fonctionnent Correctement  

### Étape 1 : Démarrer RabbitMQ et Redis Manuellement (si nécessaire)  

Si nous ne souhaitons pas utiliser Docker Compose pour RabbitMQ et Redis, nous pouvons les démarrer séparément avec les commandes suivantes :  

- **Démarrer RabbitMQ** (avec une interface de gestion) :  
  ```bash
  docker run -d --name rabbitmq -p 15672:15672 -p 5672:5672 rabbitmq:3.12-management
  ```  
  - Le port `15672` est utilisé pour l'interface de gestion.  
  - Le port `5672` est utilisé pour la communication entre services.  

- **Démarrer Redis** :  
  ```bash
  docker run -d --name redis -p 6379:6379 redis
  ```  
  - Le port `6379` est utilisé pour les communications avec Redis.  

---

### Étape 2 : Exécuter les Services Applicatifs  

1. Une fois RabbitMQ et Redis en cours d'exécution, exécutons les fichiers Python de nos services pour tester leur fonctionnement :  

   - **Backend** :  
     ```bash
     python app.py
     ```  

   - **Consumer** :  
     ```bash
     python consumer.py
     ```  

2. Vérifions les logs pour nous assurer que les services fonctionnent correctement et communiquent entre eux.  

---

## Résumé des Étapes  

1. **Préparons nos fichiers** : Assurons-nous que chaque service dispose de son propre `Dockerfile` et que le fichier `docker-compose.yml` est configuré correctement.  
2. **Construisons les images Docker** : Utilisons `docker-compose build` pour créer les images de tous les services.  
3. **Démarrons les services** : Lançons tous les conteneurs en arrière-plan avec `docker-compose up -d`.  
4. **Taguons et poussons nos images** : Préparons nos images pour un registre Docker et poussons-les avec `docker push`.  
5. **Démarrons RabbitMQ et Redis manuellement** (si nécessaire).  
6. **Testons les services** : Lançons les fichiers Python (`app.py`, `consumer.py`) et vérifions que tout fonctionne comme prévu.  

---  
