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

## 7-Testing & Monitoring
![image](https://user-images.githubusercontent.com/83654862/232091092-700ce203-6880-4dbf-b916-082e1155d419.png)Airflow nous permet de Monitorer de façon périodique l’évolution du projet :
- Assurer le maintien des performances grâce à la surveillance des métriques d’alerte
- Tracker les paramètres et alerter des déviations des performances
- réentrainement périodique du modèle à partir de toutes les données, y compris les nouvelles


## 8-CI/CD
![image](https://user-images.githubusercontent.com/55795871/229562323-a1fa782c-eb96-4ec9-8fa6-a80aec23f4e2.png)

Afin de valider la stabilité de notre application, une CI/CD a été mise en place via GitHub Actions. 
En effet, on implémenté le workflow suivant :
- Aprés chaque push, lancer automatiquement les tests unitaires
- Vérifier la stabilité des modèles.
- Vérifier la stabilité de l'authentification à l'application.
- Vérifier la stabilité de l'application FastAPI
On vérifie cette stabilité via le nombre de tests réussis. Un seuil de 80% de réussite est exigé.

Si le nombre de tests réussis est en dessous du seuil exigé, on revert le dernier commit sur le main du repo GitHub.


## 9-Web Apps
![image](https://user-images.githubusercontent.com/55795871/229562421-7c00fdda-4f8a-4d82-9899-9cca19bc110e.png)
![image](https://user-images.githubusercontent.com/55795871/229562489-0ac0545a-dcf4-47da-ad60-66966f35da89.png)
Afin de facilité l'utilisation de notre API, une interface web front-end est mise en place. 
Elle assure, en fonction des droits de l'utilisateur, l'accés aux fonctionnalités suivantes : authentification,prédictions de la catégorie de la plante, de son état de santé et de son eventuelle maladie. Elle permet en outre de bénéficier du service dédié aux laboratoires d'analyse des maladies des plantes pour alimenter le projet en données nouvelles.


