# Utiliser l'image nginx officielle? La dernière version
FROM nginx:latest

# Copier tout le contenu du dossier "frontend" vers le dossier HTML de Nginx
COPY . /usr/share/nginx/html

# Exposer le port 80 le port sur lequel l'application va s'exécuter (pour accéder au service)
EXPOSE 80

# Le point d'entrée de l'application est nginx, donc nginx démarre par défaut
CMD ["nginx", "-g", "daemon off;"]






