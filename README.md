# PlantSpy
PlantSpy is an AI tool (Deep Learning) allowing to detect the category of a plant, its health and its eventual sickness name.
<img width="945" alt="Capture d’écran 2023-04-18 à 07 29 58" src="https://user-images.githubusercontent.com/46560616/232679957-ad44b647-4618-40b8-bfeb-c8fd87739bfe.png">

<img src="https://i.imgur.com/Oln0kaH.png"/>



## 1-Présentation :

L'objet de ce projet est, à partir du modèle de machine learning précédent , de déployer une API qui propose à des tiers des services et de maintenir les modèles d’apprentissage automatique en production de manière fiable et efficace.

<img width="948" alt="Capture d’écran 2023-04-18 à 07 30 51" src="https://user-images.githubusercontent.com/46560616/232679953-3270f8c1-a769-4549-bc36-c4175d81180c.png">

<img width="952" alt="Capture d’écran 2023-04-18 à 07 18 12" src="https://user-images.githubusercontent.com/46560616/232679980-3736a65a-d76e-489b-89de-5a7010cd2228.png">

<img width="952" alt="Capture d’écran 2023-04-18 à 07 19 29" src="https://user-images.githubusercontent.com/46560616/232680061-a67c18cd-3132-47ff-8804-1278d70837b5.png">


## 2-API
![image](https://user-images.githubusercontent.com/83654862/229580127-42a99964-4721-49e0-9c04-46802b78365a.png)
L'API de notre modèle a été faite en utilisant FastAPI.

Sur l'API, on donne les fonctionnalités suivantes à l'utilisateur : 
- 1- L'authentification avec un username + passeword. 
- 2- Prédiction de la catégorie de la plante à partir d'une image uploadé ou via URL. 
- 3- Prédiction de l'état de santé de la plante à partir d'une image uploadé ou via URL. 
- 4- Prédiction du nom de la maladie de la plante à partir d'une image uploadé ou via URL.
- 5- Possibilité pour les laboratoires d'analyse des maladies des plantes d'enrichir les données du projet

## 3-BDD
![image](https://user-images.githubusercontent.com/83654862/229581122-d0a0ebac-f3c0-4444-9dcd-7d3960685348.png)
Les utilisateurs ayant le droit de ce connecter à l'API sont stockées sur une base de données MongoDb
Schema de la table user: ![image](https://user-images.githubusercontent.com/83654862/232719568-b34084d3-9719-49bf-a7a0-d29634d3e300.png)
Différents rôles possible pour les utilisateurs : 
- 1- admin, en tant qu'administrateur, il pourra ajouter ou supprimer des utilisateurs (fonctionnalité non implémenteée). 
- 2- categorie, avec ce rôle, on peut acceder au service de prédiction de la catégorie d'une image via URL ou fichier uploadé. 
- 3- santé, avec ce rôle il est possible de prédire l'état de santé de la plante à partir d'une image uploadé ou via URL. 
- 4- maladie, avec ce rôle il est possible de prédire, le cas échéant,le nom de la maladie de la plante à partir d'une image uploadé ou via URL.
- 5- stockage, avec ce rôle il est possible d'enrichir les images pour le réentrainement


## 4-Sécurisation API & Rôles
La sécurité de l'API est d'abord assuré par la gestion des entêtes CORS (Cross-Origin Resource Sharing). La méthode de sécurisation pour l'authentification et les autorisations est Oauth2
![image](https://user-images.githubusercontent.com/83654862/229582928-ace83cf9-c8a5-4248-bd80-e3c25aec85f8.png)


## 5-Test Unitaires
![image](https://user-images.githubusercontent.com/55795871/229561394-c865cc90-1fec-4bb6-a99b-4ff5700d6d82.png)
### 5-1-Tests Unitaires du modèle :
Le fichier uniTest.py contient les tests unitaires qui permettent de vérifier si l'éxecution du modèle de prédiction de la catégorie de la plante est bonne, ainsi que de vérifier la validité des images données comme input au modèle. 
Ces tests unitaires actuellement s'appliquent seulement au modèle, comme première étape.

### 5-2-Tests Unitaires de l'API :
D'autres tests unitaires seront à implémenter afin de tester fonctionnellement l'API, qu'on verra par la suite.

## 6-Dockerisation de l'API et de la BDD
L'API, le server Oauth2 et le bdd sont contenairisé via Docker. La Bdd est isolé dans son propre container.

## 7-Pipeline Airflow

Le fichier **docker-compose.yml** dans le dossier **airflow** définit un environnement de développement local pour Airflow, avec un serveur web, un planificateur, des workers Celery, une base de données PostgreSQL, un serveur Redis et un tableau de bord.

Ce projet MLOps met en œuvre un pipeline complet pour la classification des plantes en utilisant des images. Le pipeline comprend des étapes de prétraitement des données, d'entraînement et d'évaluation des modèles, ainsi que de comparaison et de sélection des modèles pour la production. Le pipeline est géré à l'aide d'Airflow pour assurer une exécution efficace et automatisée des tâches.

Les tâches suivantes sont définies dans le pipeline :

![image](https://user-images.githubusercontent.com/83654862/232091092-700ce203-6880-4dbf-b916-082e1155d419.png)


- **load_model_production** : chargement du modèle en production
- **load_images_test** : chargement des images de test
- **a_periodic_training** : entraînement périodique du modèle
- **predict_task** : prédiction des catégories à l'aide du modèle en production
- **predict_new_train_task** : prédiction des catégories à l'aide du nouveau modèle entraîné
- **save_predictions** : sauvegarde des prédictions du modèle en production dans un fichier CSV
- **save_predictions_train** : sauvegarde des prédictions du nouveau modèle entraîné dans un fichier CSV
- **calculate_accuracy** : calcul de la précision du modèle en production
- **calculate_accuracy_new_train** : calcul de la précision du nouveau modèle entraîné
- **choix_modele** : choix du meilleur modèle entre le modèle en production et le modèle nouvellement entraîné


## 8-CI/CD
![image](https://user-images.githubusercontent.com/55795871/229562323-a1fa782c-eb96-4ec9-8fa6-a80aec23f4e2.png)

Afin de valider la stabilité de notre application, une CI/CD a été mise en place via GitHub Actions. 
En effet, on implémenté le workflow suivant :
- Aprés chaque push, lancer automatiquement les tests unitaires
- Vérifier la stabilité des modèles.
- Vérifier la stabilité de l'authentification à l'application.
- Vérifier la stabilité de l'application FastAPI.
On vérifie cette stabilité via le nombre de tests réussis. Un seuil de 85% de réussite est exigé.

<img width="1020" alt="Capture d’écran 2023-04-18 à 07 47 49" src="https://user-images.githubusercontent.com/46560616/232683145-37679e9e-46c3-409e-b968-3c5c4c06a92f.png">

Si le nombre de tests réussis est en dessous du seuil exigé, on revert le dernier commit sur le main du repo GitHub.

Si tous les tests s'exécutent en respectant le seuil minimal de succés, un job automatique de déploiement est lancé pour générer une image docker de notre application sur Docker Hub :

https://hub.docker.com/layers/ilham8823/mlops_plantspy/1.0.1/images/sha256-a4e778379060a98d2dad27f4ccc22b1e0ad830d3cd9a5bc9ddcad65f92b7a7a5?context=repo

<img width="1274" alt="Capture d’écran 2023-04-18 à 07 51 17" src="https://user-images.githubusercontent.com/46560616/232683308-e400e04a-11e0-45ea-9e54-ecd4dd99f565.png">






## 9-Web Apps
![image](https://user-images.githubusercontent.com/55795871/229562421-7c00fdda-4f8a-4d82-9899-9cca19bc110e.png)
![image](https://user-images.githubusercontent.com/55795871/229562489-0ac0545a-dcf4-47da-ad60-66966f35da89.png)
Afin de facilité l'utilisation de notre API, une interface web front-end est mise en place. 
Elle assure, en fonction des droits de l'utilisateur, l'accés aux fonctionnalités suivantes : authentification,prédictions de la catégorie de la plante, de son état de santé et de son eventuelle maladie. Elle permet en outre de bénéficier du service dédié aux laboratoires d'analyse des maladies des plantes pour alimenter le projet en données nouvelles.


