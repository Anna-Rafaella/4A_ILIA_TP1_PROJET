
# **Cloud Native Calculator Application**
---

## **Erreurs rencontrées et solutions**

### **1. Problème de connexion à Redis**
**Erreur :**  
Lors de l'initialisation de l'application, une erreur de connexion à Redis a été rencontrée :  
```plaintext
Erreur de connexion à Redis
```

**Cause identifiée :**  
- Le service Redis n'était pas correctement configuré pour être accessible depuis le backend.
- Le nom d'hôte utilisé pour Redis était incorrect.

**Solution :**  
- Utilisation de la variable d'environnement `REDIS_HOST` pour configurer dynamiquement l'hôte Redis dans le backend :
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
Une erreur similaire a été rencontrée lors de la tentative de connexion à RabbitMQ (Erreur 500) :  
```plaintext
Erreur de connexion à RabbitMQ
```

**Cause identifiée :**  
- La connexion RabbitMQ était initialisée au démarrage de l'application, ce qui posait problème lorsque RabbitMQ redémarrait ou devenait temporairement indisponible.

**Solution :**  
- La connexion à RabbitMQ a été déplacée dans la fonction `effectuer_calcul` pour être créée et fermée dynamiquement à chaque requête :
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
Le frontend (interface utilisateur) ne s'affichait pas dans le navigateur.

**Cause identifiée :**  
- Mauvaise configuration du Dockerfile pour le frontend. Les fichiers du dossier `frontend` n'étaient pas copiés correctement dans le conteneur.

**Solution :**  
- Mise à jour du Dockerfile pour copier correctement tous les fichiers frontend dans le répertoire HTML de Nginx :
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
- L'API backend n'était pas exposée correctement dans Kubernetes à travers le service.

**Solution :**  
- Mise en place d'un service Kubernetes de type `ClusterIP` pour exposer le backend à d'autres pods dans le cluster :
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: svc-backend
  spec:
    selector:
      app: backend
    ports:
      - protocol: TCP
        port: 5000
        targetPort: 5000
  ```
- Vérification des logs avec `kubectl logs` pour s'assurer que le backend fonctionnait correctement :
  ```bash
  kubectl logs <backend-pod-name> -n <namespace>
  ```

---

### **5. Perte de connexion à RabbitMQ lors du redémarrage des pods**
**Erreur :**  
Après un redémarrage des pods RabbitMQ, le backend perdait la connexion, rendant l'API non fonctionnelle.

**Cause identifiée :**  
- La connexion globale à RabbitMQ était maintenue ouverte et devenait invalide après un redémarrage.

**Solution :**  
- Suppression de la connexion globale et gestion dynamique de la connexion dans chaque requête, comme mentionné dans la solution du problème 2.

---

### **6. Données invalides envoyées à l'API**
**Erreur :**  
L'API renvoyait une erreur 400 lorsque les données envoyées n'étaient pas correctement formatées.

**Cause identifiée :**  
- Les données JSON envoyées ne contenaient pas les champs requis (`operation`, `a`, `b`).

**Solution :**  
- Ajout d'une vérification pour valider la présence des champs nécessaires avant de traiter la requête :
  ```python
  if not all(k in data for k in ("operation", "a", "b")):
      return jsonify({"error": "Requête invalide"}), 400
  ```

---

### **7. Problème de CORS (Cross-Origin Resource Sharing)**
**Erreur :**  
Le frontend ne pouvait pas appeler l'API backend à cause d'une erreur de CORS.

**Cause identifiée :**  
- Le backend n'était pas configuré pour accepter les requêtes provenant du frontend.

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
kubectl get pods -n <namespace>
kubectl get services -n <namespace>
```

### **Vérification des logs**
```bash
kubectl logs <pod-name> -n anna
```


