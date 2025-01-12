
---

# Déploiement avec Kubernetes  

## Étape 1 : Préparer vos images Docker  

Avant de déployer dans Kubernetes, on s'assure que nos images Docker sont disponibles dans le registre Docker Artefact Registry de Google .  

### Taguer et pousser les images :  
- **Taguer les images** :  
  ```bash
  docker tag backend:latest <votre_utilisateur_dockerhub>/backend:latest
  docker tag consumer:latest <votre_utilisateur_dockerhub>/consumer:latest
  docker tag frontend:latest <votre_utilisateur_dockerhub>/frontend:latest
  ```
- **Pousser les images vers Docker Hub** :  
  ```bash
  docker push <votre_utilisateur_dockerhub>/backend:latest
  docker push <votre_utilisateur_dockerhub>/consumer:latest
  docker push <votre_utilisateur_dockerhub>/frontend:latest
  ```  

---

## Étape 2 : Créer les fichiers de déploiement Kubernetes  

### Exemple de fichier de déploiement pour le backend (`backend-deployment.yml`)  
```yaml
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
```

### Exemple de fichier de service pour le backend (`service.yml`)  
```yaml
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
```  

---

## Étape 3 : Déployer dans Kubernetes  

Se connecter à notre cluster Kubernetes (via `kubectl`) et appliquer les fichiers de déploiement et de service.  

### Appliquer les fichiers de déploiement :  
```bash
kubectl apply -f backend-deployment.yml
kubectl apply -f consumer-deployment.yml
kubectl apply -f frontend-deployment.yml
```

### Appliquer les services :  
```bash
kubectl apply -f service.yml
```  

---

## Résumé des Étapes :  

1. **Préparez vos images Docker** : Taguez-les et poussez-les vers un registre Docker accessible.  
2. **Créez les fichiers de déploiement Kubernetes** pour chaque service.  
3. **Déployez les services dans Kubernetes** en appliquant les fichiers de déploiement et de service.  

--- 
