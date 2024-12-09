from flask import Flask, request, jsonify
import redis
import pika
import json
import uuid
import os
from flask_cors import CORS  # Importer Flask-CORS

app = Flask(__name__)

# Appliquer CORS à toutes les routes
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Connexion à Redis
redis_host = os.getenv('REDIS_HOST', 'localhost')  # Utiliser la variable d'environnement pour Redis
try:
    redis_client = redis.Redis(host=redis_host, port=6379, db=0)
    redis_client.ping()  # Vérifier si Redis est accessible
    print("Connexion à Redis réussie")
except redis.exceptions.ConnectionError:
    print("Erreur de connexion à Redis")
    redis_client = None

# Connexion à RabbitMQ
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')  # Utiliser la variable d'environnement pour RabbitMQ
try:
    rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    rabbitmq_channel = rabbitmq_connection.channel()
    rabbitmq_channel.queue_declare(queue='calcul_queue')
    print("Connexion à RabbitMQ réussie")
except pika.exceptions.AMQPConnectionError:
    print("Erreur de connexion à RabbitMQ")
    rabbitmq_channel = None

@app.route('/api/calcul', methods=['POST'])
def effectuer_calcul():
    """
    Reçoit un calcul à effectuer, génère un ID unique,
    et place une tâche dans RabbitMQ pour le traitement.
    """
    data = request.json
    if not all(k in data for k in ("operation", "a", "b")):
        return jsonify({"error": "Requête invalide"}), 400

    calcul_id = str(uuid.uuid4())
    task = {
        "id": calcul_id,
        "operation": data["operation"],
        "a": data["a"],
        "b": data["b"]
    }

    # Placer la tâche dans RabbitMQ, si RabbitMQ est disponible
    if rabbitmq_channel:
        rabbitmq_channel.basic_publish(
            exchange='', routing_key='calcul_queue', body=json.dumps(task)
        )
        return jsonify({"id": calcul_id}), 202
    else:
        return jsonify({"error": "Erreur de connexion à RabbitMQ"}), 500

@app.route('/api/calcul/<calcul_id>', methods=['GET'])
def recuperer_resultat(calcul_id):
    """
    Vérifie si le résultat est prêt dans Redis et le renvoie.
    """
    if redis_client:
        resultat = redis_client.get(calcul_id)
        if resultat:
            return jsonify({"id": calcul_id, "resultat": resultat.decode("utf-8")}), 200
    return jsonify({"error": "Résultat en attente ou ID invalide"}), 404

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
