Voici une version corrigée et améliorée de votre README pour qu'il soit cohérent, clair et bien structuré :

---

# **Cloud Native Calculator Application**

---

## **Introduction**
Ce projet est une application Cloud Native de calculatrice distribuée, utilisant Flask pour le backend, Redis pour le stockage temporaire, RabbitMQ pour la gestion de la messagerie, et Kubernetes pour l'orchestration des conteneurs.  

Ce document décrit les **erreurs rencontrées** lors du développement, leurs **causes identifiées**, ainsi que les **solutions apportées** pour résoudre ces problèmes. 

---

## **Erreurs rencontrées et solutions**

### **1. Problème de connexion à Redis**
**Erreur :**  
Lors de l'initialisation de l'application, la connexion à Redis échouait avec le message suivant :  
```plaintext
Erreur de connexion à Redis
```

**Cause identifiée :**  
- Le service Redis n'était pas correctement configuré pour être accessible depuis le backend.
- Le nom d'hôte utilisé pour Redis dans le code était incorrect.

**Solution :**  
- Utilisation d'une variable d'environnement `REDIS_HOST` pour configurer dynamiquement l'hôte Redis dans le backend :
  ```python
  redis_host = os.getenv('REDIS_HOST', 'svc-redis')
  ```
- Vérification de la connectivité à Redis avec la commande `ping()` :
  ```python
  redis_client.ping()
  ```

---

### **2. Problème de connexion à RabbitMQ**
**Erreur :**  
Une erreur 500 survenait lorsque le backend tentait de publier une tâche dans RabbitMQ :  
```plaintext
Erreur de connexion à RabbitMQ
```

**Cause identifiée :**  
- La connexion à RabbitMQ était initialisée au démarrage de l'application. Si RabbitMQ redémarrait ou devenait temporairement indisponible, la connexion devenait invalide.

**Solution :**  
- La connexion à RabbitMQ a été déplacée dans la fonction `effectuer_calcul`, pour qu'elle soit créée et fermée dynamiquement à chaque requête :
  ```python
  rabbitmq_host = os.getenv('RABBITMQ_HOST', 'svc-rabbitmq')
  try:
      rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
      rabbitmq_channel = rabbitmq_connection.channel()
      rabbitmq_channel.queue_declare(queue='calcul_queue')

      # Publier la tâche dans RabbitMQ
      rabbitmq_channel.basic_publish(
          exchange='', routing_key='calcul_queue', body=json.dumps(task)
      )

      # Fermer la connexion RabbitMQ
      rabbitmq_channel.close()
      rabbitmq_connection.close()

      return jsonify({"id": calcul_id}), 202
  except pika.exceptions.AMQPConnectionError:
      return jsonify({"error": "Erreur de connexion à RabbitMQ"}), 500
  ```

---

### **3. Problème avec le frontend (page ne s'affichant pas)**
**Erreur :**  
Le frontend ne s'affichait pas dans le navigateur.

**Cause identifiée :**  
- Le Dockerfile du frontend ne copiait pas correctement les fichiers nécessaires dans le conteneur.

**Solution :**  
- Mise à jour du Dockerfile pour copier tous les fichiers frontend dans le répertoire HTML de Nginx :
  ```dockerfile
  FROM nginx:latest
  COPY . /usr/share/nginx/html
  EXPOSE 80
  CMD ["nginx", "-g", "daemon off;"]
  ```

---

### **4. Erreur 503 - Service Temporarily Unavailable**
**Erreur :**  
Lors de l'accès à l'API via l'URL, une erreur `503 Service Temporarily Unavailable` était affichée.

**Cause identifiée :**  
- L'API backend n'était pas exposée correctement via un service Kubernetes.

**Solution :**  
- Création d'un service Kubernetes de type `ClusterIP` pour exposer le backend à d'autres pods dans le cluster :
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: svc-api
    namespace: anna
  spec:
    ports:
    - port: 8080          # Port exposé par le service
      targetPort: 5000    # Port utilisé par Flask dans le Pod
    selector:
      app: api            # Correspond aux labels du Pod
  ```
- Vérification des logs du backend pour diagnostiquer les problèmes :
  ```bash
  kubectl logs <backend-pod-name> -n anna
  ```

---

### **5. Perte de connexion à RabbitMQ lors du redémarrage des pods**
**Erreur :**  
Après un redémarrage des pods RabbitMQ, le backend ne pouvait plus se connecter à RabbitMQ.

**Cause identifiée :**  
- Une connexion globale à RabbitMQ était maintenue ouverte dans le backend, et devenait invalide après un redémarrage.

**Solution :**  
- Suppression de la connexion globale et gestion dynamique de la connexion dans chaque requête (voir solution au problème 2).

---

### **6. Données invalides envoyées à l'API**
**Erreur :**  
L'API renvoyait une erreur 400 lorsque les données envoyées n'étaient pas correctement formatées.

**Cause identifiée :**  
- Les données JSON envoyées ne contenaient pas les champs obligatoires (`operation`, `a`, `b`).

**Solution :**  
- Ajout d'une vérification pour s'assurer que tous les champs requis sont présents avant de traiter la requête :
  ```python
  if not all(k in data for k in ("operation", "a", "b")):
      return jsonify({"error": "Requête invalide"}), 400
  ```

---

### **7. Problème de CORS (Cross-Origin Resource Sharing)**
**Erreur :**  
Le frontend ne pouvait pas appeler l'API backend en raison d'une erreur de CORS.

**Cause identifiée :**  
- Le backend n'était pas configuré pour accepter les requêtes provenant d'un domaine différent.

**Solution :**  
- Ajout de la bibliothèque Flask-CORS pour autoriser les requêtes entre domaines :
  ```python
  from flask_cors import CORS
  CORS(app, resources={r"/api/*": {"origins": "*"}})
  ```

---

## **Commandes utiles**

### **Vérification des pods et services**
```bash
kubectl get pods -n anna
kubectl get services -n anna
```

### **Vérification des logs**
```bash
kubectl logs <pod-name> -n anna
```

### **Tester l'API**
#### Effectuer un calcul
J'ai effectué le test de mon API sur PostMan

---
 😊
