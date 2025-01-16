# ERREURS RENCONTREES ET LEURS SOLUTIONS 
# ERREUR 1
Erreur de code "500" dû à la connexion incorrecte à Rabbitmq 
# CORRECTION 1
Ajout de la partie du code qui lui permetra de renouveller correctement ses connections à la base de donnée
 # Connexion à RabbitMQ (initialisée à chaque requête)
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
