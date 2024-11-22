# Pour conteneuriser l'API et le consommateur
# Conteneurisation du frontend avec Nginx.
FROM nginx:alpine

COPY ./index.html /usr/share/nginx/html/
COPY ./script.js /usr/share/nginx/html/


RUN pip install --no-cache-dir -r requirements.txt

# Par défaut, démarre l'API
CMD ["python", "app.py"]
