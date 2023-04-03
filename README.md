# PlantSpy
PlantSpy is an AI tool (Deep Learning) allowing to detect the category of a plant, its health and its eventual sickness name.


## 1-Les modèles de prédictions - Scripts Python :
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

### 1-2-Tests Unitaires du modèle :
Le fichier uniTest.py contient les tests unitaires qui permettent de vérifier si l'éxecution du modèle de prédiction de la catégorie de la plante est bonne, ainsi que de vérifier la validité des images données comme input au modèle. 
Ces tests unitaires actuellement s'appliquent seulement au modèle, comme première étape.
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

