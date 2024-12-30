# Utilise Debian comme base
FROM debian:latest

# Installe les outils nécessaires pour le débogage
RUN apt-get update && apt-get install -y bash htop vim net-tools

# Ajoute une variable d'environnement contenant mon prénom
ENV OWNER="ANNA"

#Ajout d'un nouvel utilisateur 'nonroot' pour l'exécution
RUN useradd nonroot
USER nonroot

# Utilise une commande pour garder le conteneur actif (pendant 3600 secondes)
CMD ["sleep", "3600"]
