# PlantSpy
PlantSpy is an AI tool (Deep Learning) allowing to detect the category of a plant, its health and its eventual sickness name.


## 1-Scripts Python :
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
## 4- Testing et Monitoring - AirFlow :
## 5- CI/CD - GitHub Actions : 
## 6- Interface Web - Bootstrap/React/CSS :

