## IMPLEMENTATION DE L'APPLICATION 

Organisation de l'application
La structure du projet pour la partie Application sera comme suit :

application/
│
├── backend/            # Contient le code de l'API Flask pour gérer les calculs
│   ├── app.py          # Code principal de l'API
│   ├── consumer.py     # Code du consommateur RabbitMQ
│   ├── config.py       # Configuration (RabbitMQ, Redis, etc.)
│   ├── requirements.txt# Dépendances Python
│   ├── Dockerfile      # Dockerfile pour conteneuriser l'API et le consommateur
│
├── frontend/           # Contient le code de l'interface utilisateur
│   ├── index.html      # Interface utilisateur
│   ├── script.js       # Logique client (JavaScript)
│   ├── Dockerfile      # Dockerfile pour conteneuriser le frontend
│
└── README.md           # Instructions pour cette partie


Pour commencer à implémenter la partie "Application" de ton projet, nous allons diviser la tâche en plusieurs sous-parties, en suivant les indications de notre projet

# 1. Création de l'API Backend (Flask + Redis + RabbitMQ)

L'API backend va permettre de recevoir des requêtes POST pour effectuer des calculs et des requêtes GET pour récupérer les résultats. Elle va interagir avec Redis pour stocker les résultats et utiliser RabbitMQ pour la gestion des files d'attente des calculs.

# a. Structure du projet
Tout d'abord, la structure du projet backend pourrait ressembler à ceci :

application/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── config.py

# b. Installation des dépendances
Pour implémenter l'API backend avec Flask et Redis, j'aurais  besoin des bibliothèques suivantes dans le fichier requirements.txt :

Flask==2.3.2
redis==4.10.1
pika==1.3.0  # Pour la connexion à RabbitMQ

# c. Configuration de l'API
Dans le fichier app.py, nous devrons définir deux routes principales :

POST /api/calcul - Pour effectuer un calcul (addition, soustraction, multiplication, division).
GET /api/calcul/{id} - Pour récupérer le résultat du calcul une fois qu'il est effectué

# d. Gestion des Calculs via RabbitMQ et Redis
Le code ci-dessus met en file d'attente les calculs dans RabbitMQ. Nous devons maintenant ajouter une logique de consommateur pour effectuer les calculs :

# 2. Frontend (HTML/JavaScript)
Le frontend permet aux utilisateurs de saisir des calculs et de récupérer les résultats.

Dossier : frontend/
Fichier : frontend/index.html
L'interface utilisateur principale.
