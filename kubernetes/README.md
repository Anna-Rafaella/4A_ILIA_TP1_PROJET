## Étapes à suivre pour configurer l'environnement Kubernetes
# 1) Créer un Namespace :
Le namespace isolera vos ressources Kubernetes pour éviter les conflits avec d'autres applications.

# 2) Déclarer des ReplicaSets pour chaque microservice :
Les ReplicaSets s'assurent qu'un nombre défini de Pods (instances de conteneurs) sont toujours en cours d'exécution.

# 3) Configurer des Services pour exposer les Pods :
Les Services permettent aux Pods de communiquer entre eux et permettent d'accéder à votre application depuis l'extérieur.

# 4) Configurer un Ingress :
Le service Ingress rend le frontend accessible via un nom de domaine défini dans la section Fondation.