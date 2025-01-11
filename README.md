Bien sûr ! Voici une proposition de **README.md** bien structuré et attrayant pour votre projet d'application Cloud Native **Calculatrice**. Ce fichier inclut une présentation claire, les étapes réalisées, ainsi que des détails techniques pertinents pour impressionner votre professeur.

---

# 🧮 **Calculatrice Cloud Native**

Bienvenue dans le projet **Calculatrice Cloud Native** ! Ce projet met en œuvre une application distribuée permettant d'effectuer des calculs via une architecture Cloud Native, intégrant des concepts modernes comme les microservices, la conteneurisation et l'orchestration avec Kubernetes.

---

## 🌟 **Objectifs du projet**

- Développer une **application Cloud Native** utilisant des technologies modernes.
- Illustrer les principes de **microservices** avec un frontend, un backend, une base de données Redis et un gestionnaire de messages RabbitMQ.
- Déployer et gérer l'application avec **Docker** et **Kubernetes**.
- Mettre en œuvre un pipeline de communication efficace entre les composants via RabbitMQ.

---

## 📑 **Architecture de l'application**

L'application est composée des composants suivants :

1. **Frontend** :
   - Une interface utilisateur simple en HTML, CSS et JavaScript.
   - Permet de soumettre des calculs (addition, soustraction, etc.) et d'afficher les résultats.

2. **Backend** :
   - Une API REST développée en Python avec Flask.
   - Connectée à Redis pour stocker temporairement les résultats et à RabbitMQ pour gérer les calculs asynchrones.

3. **Redis** :
   - Utilisé comme base de données temporaire pour stocker les résultats des calculs.

4. **RabbitMQ** :
   - Sert de broker de messages pour la communication entre les services.

5. **Consumer** :
   - Un worker Python qui consomme les messages RabbitMQ, effectue les calculs et enregistre les résultats dans Redis.

---

## 🚀 **Fonctionnalités principales**

- Soumission d'opérations mathématiques simples : addition, soustraction, multiplication, division.
- Traitement asynchrone des calculs via RabbitMQ.
- Récupération des résultats dès qu'ils sont prêts.
- Déploiement complet avec Docker et Kubernetes.

---

## 🛠️ **Technologies utilisées**

- **Python** (Flask) : pour l'API backend et le worker consumer.
- **Redis** : pour le stockage temporaire des résultats.
- **RabbitMQ** : pour la gestion des files de messages.
- **HTML, CSS, JavaScript** : pour le frontend.
- **Docker** : pour la conteneurisation des services.
- **Kubernetes** : pour l'orchestration des conteneurs.
- **Flask-CORS** : pour permettre la communication entre le frontend et le backend.

---

## 🏗️ **Étapes réalisées**

### 1️⃣ **Développement local**

1. Création du frontend avec une interface utilisateur basique (HTML, CSS, JS).
2. Développement de l'API backend en Flask :
   - Routes pour soumettre un calcul (`POST /api/calcul`) et récupérer un résultat (`GET /api/calcul/<id>`).
   - Connexion à Redis et RabbitMQ.
3. Développement du worker consumer pour consommer les messages RabbitMQ et traiter les calculs.

### 2️⃣ **Conteneurisation avec Docker**

- Création des fichiers **Dockerfile** pour chaque service (frontend, backend, consumer).
- Utilisation de **Docker Compose** pour tester l'application localement avec tous les services connectés.

### 3️⃣ **Déploiement avec Kubernetes**

1. Création des manifests Kubernetes pour :
   - Les **Deployments** (frontend, backend, consumer, RabbitMQ, Redis).
   - Les **Services** pour exposer les composants.
2. Tests et débogage des interactions entre les pods (problèmes de connexions résolus).
3. Utilisation de **kubectl logs** et autres outils pour surveiller l'état des services.

### 4️⃣ **Test et validation**

- Test des calculs via l'interface frontend.
- Vérification des interactions backend ↔ RabbitMQ ↔ Redis.
- Debugging et optimisation des workflows.

---

## ⚙️ **Instructions pour exécuter le projet**

### Prérequis

- **Docker** et **Kubernetes** installés sur votre machine.
- Accès à un cluster Kubernetes fonctionnel.

### Étapes

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/votre-utilisateur/calculatrice-cloud-native.git
   cd calculatrice-cloud-native
   ```

2. Déployer l'application avec Kubernetes :
   ```bash
   kubectl apply -f kubernetes/
   ```

3. Vérifier l'état des pods :
   ```bash
   kubectl get pods -n anna
   ```

4. Accéder au frontend :
   - Récupérez l'adresse IP ou le port exposé du service frontend :
     ```bash
     kubectl get svc -n anna
     ```
   - Ouvrez votre navigateur à l'adresse correspondante.

5. Tester l'application :
   - Soumettez des calculs via le frontend et observez les résultats.

---

## 🐞 Debugging et résolution des problèmes

### Logs des services
- Vérifiez les logs pour diagnostiquer les problèmes :
  ```bash
  kubectl logs <pod-name> -n anna
  ```

### Résolution des erreurs courantes
- Frontend inaccessible : Vérifiez que le service frontend est correctement exposé.
- Problèmes de connexion Redis ou RabbitMQ : Assurez-vous que les variables d'environnement pour `REDIS_HOST` et `RABBITMQ_HOST` sont correctement configurées.

---

## 📂 Structure du projet

```plaintext
calculatrice-cloud-native/
├── frontend/
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   └── Dockerfile
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── consumer/
│   ├── consumer.py
│   ├── requirements.txt
│   └── Dockerfile
├── kubernetes/
│   ├── frontend-deployment.yaml
│   ├── backend-deployment.yaml
│   ├── consumer-deployment.yaml
│   ├── redis-deployment.yaml
│   ├── rabbitmq-deployment.yaml
│   └── services.yaml
└── README.md
```

---

## 🎯 Points forts du projet

- Utilisation des meilleures pratiques Cloud Native.
- Architecture modulaire et extensible.
- Intégration fluide entre les composants grâce à RabbitMQ et Redis.
- Déploiement Kubernetes entièrement fonctionnel.

---

## 🤝 Contributeur

- **KAPANDE DENG ANNA RAFAELLA** - Développeuse principale  😊

---

## 🏆 Conclusion

Ce projet illustre parfaitement l'utilisation des technologies Cloud Native pour développer une application distribuée. Il combine des outils modernes pour offrir une solution robuste, évolutive et performante.

---
