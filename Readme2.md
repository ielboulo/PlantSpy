# PlantSpy
PlantSpy is an AI tool (Deep Learning) allowing to detect the category of a plant, its health and its eventual sickness name.
<img src="https://i.imgur.com/vJJDnbv.png"/>

## 1-Présentation :

L'objet de ce projet est, à partir du modèle de machine learning précédent , de déployer une API qui propose à des tiers des services et de maintenir les modèles d’apprentissage automatique en production de manière fiable et efficace.

## 3-API
![image](https://user-images.githubusercontent.com/83654862/229580127-42a99964-4721-49e0-9c04-46802b78365a.png)
L'API de notre modèle a été faite en utilisant FastAPI.

Sur l'API, on donne les fonctionnalités suivantes à l'utilisateur : 
- 1- L'authentification avec un username + passeword. 
- 2- Prédiction de la catégorie de la plante à partir d'une image uploadé ou via URL. 
- 3- Prédiction de l'état de santé de la plante à partir d'une image uploadé ou via URL. 
- 4- Prédiction du nom de la maladie de la plante à partir d'une image uploadé ou via URL.
- 5- Possibilité pour les laboratoires d'analyse des maladies des plantes d'enrichir les données du projet

## 4-BDD
![image](https://user-images.githubusercontent.com/83654862/229581122-d0a0ebac-f3c0-4444-9dcd-7d3960685348.png)
Les utilisateurs ayant le droit de ce connecter à l'API sont stockées sur une base de données MongoDb

## 5-Sécurisation API & Rôles
La sécurité de l'API est d'abord assuré par la gestion des entêtes CORS (Cross-Origin Resource Sharing). La méthode de sécurisation pour l'authentification et les autorisations est Oauth2
![image](https://user-images.githubusercontent.com/83654862/229582928-ace83cf9-c8a5-4248-bd80-e3c25aec85f8.png)


## 6-Test Unitaires
![image](https://user-images.githubusercontent.com/55795871/229561394-c865cc90-1fec-4bb6-a99b-4ff5700d6d82.png)
### 1-1-Tests Unitaires du modèle :
Le fichier uniTest.py contient les tests unitaires qui permettent de vérifier si l'éxecution du modèle de prédiction de la catégorie de la plante est bonne, ainsi que de vérifier la validité des images données comme input au modèle. 
Ces tests unitaires actuellement s'appliquent seulement au modèle, comme première étape.

### 1-2-Tests Unitaires de l'API :
D'autres tests unitaires seront à implémenter afin de tester fonctionnellement l'API, qu'on verra par la suite.

## 2-Dockerisation de l'API et de la BDD
L'API, le server Oauth2 et le bdd sont contenairisé via Docker. La Bdd est isolé dans son propre container.

## 7-Testing & Monitoring
![image](https://user-images.githubusercontent.com/83654862/229588903-be262eb8-28ca-417f-a973-b58868c65d69.png)
Airflow nous permet de Monitorer de façon périodique l’évolution du projet :
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


Pour utiliser les modèles de prediction, il suffit de :

1- Fournir une image au script python  

2- Appliquer la mise en forme nécessaire (resize à 100x100, mise en place en array)

3- Appeler la fonction "Predict()" qui prend en argument l'image

En sortie, le système fournit sa prédiction comme suit :
nom_de_catégorie_de_plante + intervalle de confiance de prediction en % + [Healthy ou nom_maladie] + intervalle de confiance de prediction en %


**Example** :
1- Image en input : ./Models/NewPlantDiseasesDataset/test/test/AppleCedarRust1.JPG

2- Mise en forme en python :

        image = test_images[0]
        img = cv2.imread(image, cv2.IMREAD_COLOR)
        img_resized = cv2.resize(img, (100, 100))
        X_test = []
        X_test.append(img_resized)
        X_test = np.array(X_test) / 255

3- Appel du modèle:

        prediction_0 = predict(X_test)
       
        print("==> Prediction : " + str(prediction_0.iloc[0, 0]) +
               " for " + str(round(prediction_0.iloc[0, 1] * 100, 2)) +"% and as " +
               str(prediction_0.iloc[0, 2]) + " for " + str(round(prediction_0.iloc[0, 3] * 100, 2)) + "%")

Résultat :
==> Prediction : Apple for 94.95% and as Cedar_apple_rust for 100.0%

### 1-1-Tests Unitaires du modèle :
Le fichier uniTest.py contient les tests unitaires qui permettent de vérifier si l'éxecution du modèle de prédiction de la catégorie de la plante est bonne, ainsi que de vérifier la validité des images données comme input au modèle.
Ces tests unitaires actuellement s'appliquent seulement au modèle, comme première étape.

### 1-2-Tests Unitaires de l'API :
D'autres tests unitaires seront à implémenter afin de tester fonctionnellement l'API, qu'on verra par la suite.


## 2- Créer une API du modèle - FastAPI :

L'API de notre modèle a été faite en utilisant FastAPI.

Sur l'API, on donne les fonctionnalités suivantes à l'utilisateur :
1- L'authentification avec un username + passeword.
2- Prédiction de la catégorie de la plante à partir d'une image uploadé ou via URL.
3- Prédiction de l'état de santé de la plante à partir d'une image uploadé ou via URL.
4- Prédiction du nom de la maladie de la plante à partir d'une image uploadé ou via URL.

Pour l'authentification des utilisateurs, on utilisé le protocole OAuth, protocole de délégation d'authentification.
Les utilisateurs sont enregistrés dans une base de données MongoDB.


## 3- Isolation - Docker :

Afin d'isoler notre modèle, on a assuré son déploiement via Docker.
Ce processus va nous garantir la stabilité de l'API :
- En installant l'environnement python adapté : le fichier "requirements.txt" contient toutes les lib python à installer.
- La sécurité de l'API est assurée via la méthode d'authentification OAuth
- L'image de base utilisée est "mongo". Cela simplifie l'accés à une DataBase de type MongoDB dans laquelle on configure les comptes autorisés à accéder à l'API.

Pour plus de détails, voir le répertoire GitHub qui contient les fichiers de configurations nécessaires.

## 4- Testing et Monitoring - AirFlow :

Afin d'assurer un test automatique de l'API mise en place, on a utilisé la plateforme "AirFlow".
Le processus mis en place actuellement est comme suit :
On utilise un "DAG" composé de deux tâches ("task").
La première tâche consiste à tester l'application de prédiction avec un ensemble d'images.
La deuxième tâche consiste à récupérer les résultats de prédictions de la première tâche et les stocker dans un log (.CSV) afin de le mettre à disposition des Data Scientist pour vérifier la stabilité du modèle.

Une troisème devrait être implémentée prochainement; c'est le ré-entrainement du modèle.
Si l'accuracy des prédictions resultantes des tache 1 + 2 est en-dessous de 85%, une tâche de re-entraienemnt des modèles devrait être lancée.

## 5- CI/CD - GitHub Actions :

Afin de valider la stabilité de notre application, une CI/CD a été mise en place via GitHub Actions.
En effet, on implémenté le workflow suivant :
- Aprés chaque push, lancer automatiquement les tests unitaires
- Vérifier la stabilité des modèles.
- Vérifier la stabilité de l'authentification à l'application.
- Vérifier la stabilité de l'application FastAPI
On vérifie cette stabilité via le nombre de tests réussis. Un seuil de 80% de réussite est exigé.

Si le nombre de tests réussis est en dessous du seuil exigé, on revert le dernier commit sur le main du repo GitHub.

## 6- Interface Web - Bootstrap/React/CSS :

Afin de facilité l'utilisation de notre API, une interface web front-end est encours de développement. 
Elle permettra d'assurer l'accés aux fonctionnalités suivantes : authentification et prédictions de la catégorie de la plante, de son état de santé et de son eventuelle maladie.
