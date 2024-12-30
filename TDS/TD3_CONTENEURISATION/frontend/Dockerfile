# Utiliser l'image nginx officielle? La dernière version
FROM nginx:latest

# Copier les fichiers HTML et img dans le répertoire par défaut de conteneur Ngnix
COPY ./index.html /usr/share/nginx/html/
#ça c'est pour les fichiers images
#COPY ./img /usr/share/nginx/html/

# Exposer le port 80 (port par défaut de nginx)
EXPOSE 80

# Le point d'entrée de l'application est nginx, donc nginx démarre par défaut
CMD ["nginx", "-g", "daemon off;"]
