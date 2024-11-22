# c. Configuration de l'API
# C'est le point d'entrée principal de l'API Flask.
from flask import Flask, request, jsonify
import redis
import pika
import json
import uuid

app = Flask(__name__)

# Connexion à Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Connexion à RabbitMQ
rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
rabbitmq_channel = rabbitmq_connection.channel()
rabbitmq_channel.queue_declare(queue='calcul_queue')

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

    # Placer la tâche dans RabbitMQ
    rabbitmq_channel.basic_publish(
        exchange='', routing_key='calcul_queue', body=json.dumps(task)
    )

    return jsonify({"id": calcul_id}), 202

@app.route('/api/calcul/<calcul_id>', methods=['GET'])
def recuperer_resultat(calcul_id):
    """
    Vérifie si le résultat est prêt dans Redis et le renvoie.
    """
    resultat = redis_client.get(calcul_id)
    if resultat:
        return jsonify({"id": calcul_id, "resultat": resultat.decode("utf-8")}), 200
    return jsonify({"error": "Résultat en attente ou ID invalide"}), 404

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
