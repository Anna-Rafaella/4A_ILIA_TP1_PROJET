# Ce fichier contient le consommateur RabbitMQ, qui écoute les tâches de calcul et enregistre les résultats dans Redis.
import pika
import redis
import json
import os

# Connexion à Redis
redis_client = redis.Redis(host='redis', port=6379, db=0)

# Connexion à RabbitMQ
rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host='svc-rabbitmq'))
rabbitmq_channel = rabbitmq_connection.channel()
rabbitmq_channel.queue_declare(queue='calcul_queue')

# environment pour Backend  : Ajout des variables RABBITMQ_HOST et REDIS_HOST. 
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
redis_host = os.getenv('REDIS_HOST', 'localhost')

def effectuer_calcul(ch, method, properties, body):
    """
    Extrait une tâche de RabbitMQ, effectue le calcul,
    et stocke le résultat dans Redis.
    """
    task = json.loads(body)
    operation = task["operation"]
    a = task["a"]
    b = task["b"]
    calcul_id = task["id"]

    try:
        if operation == "addition":
            result = a + b
        elif operation == "soustraction":
            result = a - b
        elif operation == "multiplication":
            result = a * b
        elif operation == "division":
            result = a / b if b != 0 else "Erreur: Division par zéro"
        else:
            result = "Erreur: Opération inconnue"
    except Exception as e:
        result = f"Erreur: {str(e)}"

    # Enregistrer le résultat dans Redis
    redis_client.set(calcul_id, result)

# Consommation des tâches
rabbitmq_channel.basic_consume(queue='calcul_queue', on_message_callback=effectuer_calcul, auto_ack=True)

print("Consommateur prêt. En attente de tâches...")
rabbitmq_channel.start_consuming()
