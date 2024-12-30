## Etapes de la Construction et Exécution avec Docker

3. Construire et Exécuter avec Docker Compose
Une fois le fichier docker-compose.yml en place, vous pouvez construire et démarrer les services en utilisant Docker Compose.

Étape 1 : Construire les images Docker
Allez dans le répertoire racine (/Conteneurisation) où se trouve votre docker-compose.yml et exécutez la commande suivante pour construire toutes les images Docker :


docker-compose build
Étape 2 : Démarrer les services
Une fois les images construites, vous pouvez démarrer tous les services en arrière-plan avec la commande suivante :

docker-compose up -d
Cela démarrera vos services (backend, consumer, frontend, RabbitMQ, Redis) dans des conteneurs Docker.

4. Tagging des Images Docker pour Kubernetes
Quand vous passez à Kubernetes, vous devez pousser vos images Docker vers un registre Docker (par exemple, Docker Hub, Amazon ECR, Google Container Registry, etc.) pour qu'elles soient accessibles par votre cluster Kubernetes. Les images seront ensuite utilisées pour déployer vos pods.

Exemple de commandes pour taguer et pousser vos images vers un registre :
Taguer l'image backend :

docker tag backend:latest <votre_utilisateur_dockerhub>/backend:latest
Taguer l'image consumer :

docker tag consumer:latest <votre_utilisateur_dockerhub>/consumer:latest
Taguer l'image frontend :

docker tag frontend:latest <votre_utilisateur_dockerhub>/frontend:latest
Pousser les images vers Docker Hub :

docker push <votre_utilisateur_dockerhub>/backend:latest
docker push <votre_utilisateur_dockerhub>/consumer:latest
docker push <votre_utilisateur_dockerhub>/frontend:latest
5. Kubernetes : Déploiement des Services
Une fois que vos images sont sur un registre Docker (Docker Hub, etc.), vous pouvez créer des fichiers de déploiement Kubernetes pour chaque service (backend, frontend, consumer).

Exemple de fichier de déploiement Kubernetes pour le backend (backend-deployment.yml):

apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: <votre_utilisateur_dockerhub>/backend:latest
        ports:
        - containerPort: 5000
Exemple de service Kubernetes pour le backend (service.yml):

apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  selector:
    app: backend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
6. Déploiement dans Kubernetes
Pour déployer vos services dans Kubernetes, vous devez d'abord vous connecter à votre cluster Kubernetes (par exemple, via kubectl) et appliquer les fichiers de déploiement et de service.

Appliquer le fichier de déploiement :

kubectl apply -f backend-deployment.yml
kubectl apply -f consumer-deployment.yml
kubectl apply -f frontend-deployment.yml
Appliquer les services :

kubectl apply -f service.yml

## Comment tester si mon Api marche bien:

- Tout d'abord run ou exécuter les images des conteneurs de redis et rabbitmq dans le docker:

*  docker run rabbitmq -t 3.12-management
* docker run redis

- Ensuite, exécuter les fichiers app.py et consumer.py:
chose n'est pas clair dans les étapes ci-dessus !
