# Utiliser l'image officielle de RabbitMQ avec l'interface de gestion
FROM rabbitmq:management

# Définir les variables d'environnement pour le nom d'utilisateur et le mot de passe par défaut
ENV RABBITMQ_DEFAULT_USER=guest
ENV RABBITMQ_DEFAULT_PASS=guest

# Exposer les ports nécessaires
EXPOSE 5672 15672

# Lancer RabbitMQ avec l'interface de gestion
CMD ["rabbitmq-server"]
