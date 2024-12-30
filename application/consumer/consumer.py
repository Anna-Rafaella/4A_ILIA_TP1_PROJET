import pika
import redis
import json
import os

# Récupération des variables d'environnement
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'svc-rabbitmq')
redis_host = os.getenv('REDIS_HOST', 'svc-redis')

# Connexion à Redis
redis_client = redis.Redis(host=redis_host, port=6379, db=0)

# Connexion à RabbitMQ
rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
rabbitmq_channel = rabbitmq_connection.channel()
rabbitmq_channel.queue_declare(queue='calcul_queue')

def effectuer_calcul(ch, method, properties, body):
    """
    Extrait une tâche de RabbitMQ, effectue le calcul,
    et stocke le résultat dans Redis.
    """
    try:
        task = json.loads(body)
        operation = task.get("operation")
        a = task.get("a")
        b = task.get("b")
        calcul_id = task.get("id")

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
    print(f"Calcul effectué : {calcul_id} -> {result}")

# Consommation des tâches
rabbitmq_channel.basic_consume(queue='calcul_queue', on_message_callback=effectuer_calcul, auto_ack=True)

print("Consommateur prêt. En attente de tâches...")
rabbitmq_channel.start_consuming()
