# Utiliser une image de base Python
FROM python:3.12-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Commande pour exécuter le consommateur
CMD ["python", "consumer.py"]
